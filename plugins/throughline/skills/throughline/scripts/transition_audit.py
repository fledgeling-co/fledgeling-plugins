#!/usr/bin/env python3
"""Transition audit: the deterministic gate on a drafted scene.

Reads one scene file (markdown prose, blank-line paragraphs) and reports, per
consecutive paragraph pair, whether the second paragraph carries an anchor
back to the first. A paragraph with no anchor is an orphan: it reads as a
self-contained micro-idea rather than a continuation, which is the documented
failure shape (see references/evidence.md, E3 and E7).

Also checks the things a drafter gets wrong that a reader notices and a
script can count: the word band, first-person leakage in a third-person
scene, proper nouns absent from the cast, a stock list of prose tells,
em dashes, and rhythm uniformity.

Usage:
  transition_audit.py SCENE.md [--beat ID --beats beats.json] [--bible bible.md]
                      [--cast "A,B,C"] [--min N --max N] [--em-dash forbid|warn]
                      [--json OUT.json] [--quiet]
  transition_audit.py --self-test

Exit 0 when no hard failure fired; exit 1 otherwise. Warnings never fail.

Hard failures: orphan paragraph (unless preceded by a scene-break line),
word count outside the band, first-person leak in a third-person scene,
em dash when --em-dash forbid, a tell from the "hard" list.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

SCENE_BREAK = re.compile(r"^\s*(\*\s*\*\s*\*|#{1,6}\s.*|---+|~~~+)\s*$")
PERSONAL = {
    "he", "she", "they", "it", "him", "her", "them", "his", "hers", "their",
    "theirs", "its", "himself", "herself", "themselves", "itself",
}
DEICTIC = {
    "this", "that", "these", "those", "here", "there", "then", "now", "still",
    "again", "so", "and", "but", "instead", "meanwhile", "beside", "behind",
    "above", "below", "inside", "outside", "later", "afterwards", "afterward",
}
STOPWORDS = set("""
a an the and or but if then than so as of at by for from in into on onto to
with without over under up down out off is are was were be been being have
has had do does did not no yes this that these those there here it its he
she they them his her their we you i me my our your who whom which what
when where why how all any both each few more most other some such only own
same too very can will just should now once about after before again against
because through during until while above below between very s t d ll re ve
m said says say one two three way back like get got
""".split())
FIRST_PERSON = re.compile(r"(?<![\w'])(I|I'm|I'd|I'll|I've|me|my|mine|myself)(?![\w'])")
QUOTE_SPAN = re.compile(r"[\"“][^\"”]*[\"”]")
WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")
CAP_TOKEN = re.compile(r"(?<![.!?]\s)(?<!^)\b([A-Z][a-z]{2,})\b")
EM_DASH = "—"

# Tells. "hard" ones fail; "soft" ones warn. Sources: kylehughes
# writing-prose-like-a-human-for-agents (Gemini report), the Fable 5.1
# mannered-prose guidance (Anthropic docs), agent-voice ai-writing-signs.
TELLS_HARD = [
    r"\ba testament to\b", r"\btapestry\b", r"\bdelve[sd]?\b",
    r"\blittle did (he|she|they|i) know\b", r"\bin a world where\b",
]
TELLS_SOFT = [
    r"\bcouldn'?t help but\b", r"\ba sense of\b", r"\bthe weight of\b",
    r"\bpalpable\b", r"\bunspoken\b", r"\bsomething shifted\b",
    r"\bfor a moment,?\b", r"\bsuddenly\b", r"\bfound (him|her|them)self\b",
    r"\bit was(n'?t| not) (just |only )?[^.]{1,40}[,;] it was\b",
    r"\bnot (just|only|merely) [^.]{1,40}, but\b",
    r"\bin that moment\b", r"\bfelt like\b", r"\bseemed to\b",
    r"\bechoed\b", r"\bpiercing\b", r"\bshiver\b", r"\bbreath (he|she|they) (didn'?t|hadn'?t) know\b",
    r"\bsteeled (him|her|them)self\b", r"\bin the end,?\b", r"\ba beat\b",
]


def split_paragraphs(text: str) -> list[dict]:
    """Return paragraphs with their line index and whether a break precedes them."""
    lines = text.splitlines()
    paras: list[dict] = []
    buf: list[str] = []
    start = 0
    break_before = False
    for i, line in enumerate(lines + [""]):
        if line.strip() == "":
            if buf:
                paras.append({"text": " ".join(s.strip() for s in buf), "line": start + 1,
                              "break_before": break_before})
                buf = []
                break_before = False
            continue
        if SCENE_BREAK.match(line):
            if buf:
                paras.append({"text": " ".join(s.strip() for s in buf), "line": start + 1,
                              "break_before": break_before})
                buf = []
            break_before = True
            continue
        if not buf:
            start = i
        buf.append(line)
    return paras


def content_words(text: str) -> set[str]:
    out = set()
    for w in WORD.findall(text.lower()):
        w = w.strip("'’-")
        if len(w) >= 4 and w not in STOPWORDS:
            out.add(stem(w))
    return out


def stem(w: str) -> str:
    for suf in ("ing", "edly", "ed", "es", "s", "ly"):
        if len(w) > len(suf) + 3 and w.endswith(suf):
            return w[: -len(suf)]
    return w


def first_sentence(text: str) -> str:
    m = re.match(r"(.+?[.!?][\"”’']?)(\s|$)", text)
    return m.group(1) if m else text[:200]


def strip_quotes(text: str) -> str:
    return QUOTE_SPAN.sub(" ", text)


def names_in(text: str, cast: set[str]) -> set[str]:
    return {n for n in cast if re.search(rf"\b{re.escape(n)}\b", text)}


def anchor_for(prev: str, cur: str, cast: set[str]) -> dict:
    """What ties `cur` to `prev`. Empty `kinds` means orphan."""
    fs = first_sentence(cur)
    kinds = []
    fs_words = [w.lower().strip("'’") for w in WORD.findall(strip_quotes(fs) or fs)]
    if any(w in PERSONAL for w in fs_words):
        kinds.append("pronoun")
    elif any(w in DEICTIC for w in fs_words[:4]):
        kinds.append("connective")
    prev_names = names_in(prev, cast)
    if prev_names & names_in(fs, cast):
        kinds.append("shared-name")
    shared_fs = content_words(fs) & content_words(prev)
    if shared_fs:
        kinds.append("shared-word:" + ",".join(sorted(shared_fs)[:3]))
    if cur.lstrip().startswith(("\"", "“")):
        # A spoken line answers the scene it sits in; dialogue is responsive by nature.
        kinds.append("dialogue-turn")
    shared_any = content_words(cur) & content_words(prev)
    return {"kinds": kinds, "shared_any": sorted(shared_any)[:5]}


def audit(text: str, *, cast: set[str], min_words: int, max_words: int,
          pov: str, em_dash: str) -> dict:
    paras = split_paragraphs(text)
    words = sum(len(WORD.findall(p["text"])) for p in paras)
    fails: list[dict] = []
    warns: list[dict] = []
    pairs: list[dict] = []

    if words < min_words or words > max_words:
        fails.append({"check": "word-band", "detail": f"{words} words, band {min_words}-{max_words}"})

    for i in range(1, len(paras)):
        prev, cur = paras[i - 1], paras[i]
        a = anchor_for(prev["text"], cur["text"], cast)
        orphan = not a["kinds"] and not a["shared_any"]
        pairs.append({"para": i + 1, "line": cur["line"], "anchor": a["kinds"],
                      "orphan": orphan, "break_before": cur["break_before"]})
        if orphan and not cur["break_before"]:
            fails.append({"check": "orphan-paragraph", "line": cur["line"],
                          "detail": f"paragraph {i + 1} shares nothing with paragraph {i}: "
                                    f"\"{first_sentence(cur['text'])[:90]}\""})
        elif not a["kinds"] and not cur["break_before"]:
            warns.append({"check": "weak-anchor", "line": cur["line"],
                          "detail": f"paragraph {i + 1} opens without a referent; "
                                    f"later overlap only: {a['shared_any']}"})

    if pov == "third":
        leaks = []
        for p in paras:
            narr = strip_quotes(p["text"])
            n = len(FIRST_PERSON.findall(narr))
            if n:
                leaks.append((p["line"], n))
        total = sum(n for _, n in leaks)
        if total > 2:
            fails.append({"check": "first-person-leak", "detail": f"{total} first-person tokens "
                          f"outside dialogue in a third-person scene, lines {[l for l, _ in leaks][:6]}"})

    em = text.count(EM_DASH)
    if em:
        (fails if em_dash == "forbid" else warns).append(
            {"check": "em-dash", "detail": f"{em} em dash(es)"})

    for pat in TELLS_HARD:
        for m in re.finditer(pat, text, flags=re.I):
            fails.append({"check": "tell", "detail": f"\"{m.group(0)}\" at offset {m.start()}"})
    soft_hits = {}
    for pat in TELLS_SOFT:
        hits = re.findall(pat, text, flags=re.I)
        if hits:
            soft_hits[pat] = len(hits)
    for pat, n in soft_hits.items():
        warns.append({"check": "tell-soft", "detail": f"{n} x /{pat}/"})

    # Proper nouns not in cast: a continuity tripwire, not a verdict.
    if cast:
        seen: dict[str, int] = {}
        for p in paras:
            for m in CAP_TOKEN.finditer(p["text"]):
                tok = m.group(1)
                if tok not in cast and tok.lower() not in STOPWORDS:
                    seen[tok] = seen.get(tok, 0) + 1
        unknown = sorted(t for t, n in seen.items() if n >= 2)
        if unknown:
            warns.append({"check": "unlisted-proper-noun", "detail": ", ".join(unknown[:12])})

    # Rhythm: uniform sentence lengths and repeated paragraph openers.
    sents = [s for s in re.findall(r"[^.!?]+[.!?]+[\"”’]?", text) if WORD.search(s)]
    lens = [len(WORD.findall(s)) for s in sents]
    if len(lens) >= 8:
        cv = statistics.pstdev(lens) / (statistics.mean(lens) or 1)
        if cv < 0.35:
            warns.append({"check": "uniform-rhythm", "detail": f"sentence-length CV {cv:.2f} (<0.35)"})
    openers = [WORD.findall(p["text"])[0].lower() for p in paras if WORD.findall(p["text"])]
    for i in range(2, len(openers)):
        if openers[i] == openers[i - 1] == openers[i - 2]:
            warns.append({"check": "repeated-opener", "line": paras[i]["line"],
                          "detail": f"three paragraphs in a row open with \"{openers[i]}\""})
            break

    return {"words": words, "paragraphs": len(paras), "pairs": pairs,
            "fails": fails, "warns": warns, "exit": 1 if fails else 0}


def load_beat(beats_path: Path, beat_id: str) -> dict:
    data = json.loads(beats_path.read_text())
    for b in data.get("scenes", data if isinstance(data, list) else []):
        if b.get("id") == beat_id:
            return b
    sys.exit(f"beat {beat_id!r} not found in {beats_path}")


def cast_from_bible(bible: Path) -> set[str]:
    names = set()
    for line in bible.read_text().splitlines():
        m = re.match(r"^#{2,4}\s+([A-Z][\w'’-]*)(?:\s|$)", line)
        if m:
            names.add(m.group(1))
    return names


def print_report(r: dict, path: str, quiet: bool) -> None:
    print(f"{path}: {r['words']} words, {r['paragraphs']} paragraphs, "
          f"{len(r['fails'])} fail(s), {len(r['warns'])} warning(s)")
    for f in r["fails"]:
        print(f"  FAIL  {f['check']:<22} {f.get('detail', '')}")
    for w in r["warns"]:
        print(f"  warn  {w['check']:<22} {w.get('detail', '')}")
    if not quiet:
        for p in r["pairs"]:
            tag = "ORPHAN" if p["orphan"] and not p["break_before"] else ("break" if p["break_before"] else "ok")
            print(f"  para {p['para']:>3} line {p['line']:>4} {tag:<6} {'; '.join(p['anchor'])}")


COHERENT = """Bisk reached the platform as the lights went. The beacon behind her was still lit, a small hard point in the dark, and she kept her back to it so she could see the tunnel mouth.

The tunnel mouth was where they would come from. She had counted the sounds on the way up: the wet dragging step, the clicking, the long silence between. The silence was the part she disliked.

She disliked it because it meant they were listening too. Bisk set her shell against the beacon post and let the heat of it come through, and for a while there was only that, the warmth at her back and the cold in front.

"You don't have to stay," said the station voice from the speaker above her. It had said this twice already.

"I know," Bisk said. "Tell the train to go."

The train went. She heard it before she felt it, the rails singing under the platform, then the wind of it, then nothing but the beacon and the tunnel and the first click from the dark.
"""

ORPHANED = """Bisk reached the platform as the lights went. The beacon behind her was still lit, a small hard point in the dark, and she kept her back to it so she could see the tunnel mouth.

Ferns unfurled in the greenhouse, a tapestry of green, a testament to patience. Somewhere a kettle sang.

The tunnel mouth was where they would come from. She had counted the sounds on the way up: the wet dragging step, the clicking, the long silence between.
"""


def self_test() -> int:
    ok = True
    cast = {"Bisk"}
    r = audit(COHERENT, cast=cast, min_words=50, max_words=2000, pov="third", em_dash="forbid")
    ok &= _expect("a coherent scene passes", r["exit"] == 0, r)
    r = audit(ORPHANED, cast=cast, min_words=10, max_words=2000, pov="third", em_dash="forbid")
    checks = {f["check"] for f in r["fails"]}
    ok &= _expect("an orphan paragraph fails", "orphan-paragraph" in checks, r)
    ok &= _expect("a hard tell fails", "tell" in checks, r)
    r = audit(ORPHANED.replace("\n\nFerns", "\n\n* * *\n\nFerns"), cast=cast, min_words=10,
              max_words=2000, pov="third", em_dash="forbid")
    ok &= _expect("a scene break excuses the orphan", not any(
        f["check"] == "orphan-paragraph" for f in r["fails"]), r)
    r = audit(COHERENT, cast=cast, min_words=500, max_words=2000, pov="third", em_dash="forbid")
    ok &= _expect("a scene under the word band fails", any(
        f["check"] == "word-band" for f in r["fails"]), r)
    fp = COHERENT.replace("She had counted", "I had counted").replace("she kept", "I kept").replace(
        "She disliked", "I disliked")
    r = audit(fp, cast=cast, min_words=50, max_words=2000, pov="third", em_dash="forbid")
    ok &= _expect("first-person narration in a third-person scene fails", any(
        f["check"] == "first-person-leak" for f in r["fails"]), r)
    r = audit(fp, cast=cast, min_words=50, max_words=2000, pov="first", em_dash="forbid")
    ok &= _expect("the same text passes when the scene is first person", not any(
        f["check"] == "first-person-leak" for f in r["fails"]), r)
    r = audit(COHERENT.replace(", a small", " — a small"), cast=cast, min_words=50,
              max_words=2000, pov="third", em_dash="forbid")
    ok &= _expect("an em dash fails under --em-dash forbid", any(
        f["check"] == "em-dash" for f in r["fails"]), r)
    r = audit(COHERENT.replace(", a small", " — a small"), cast=cast, min_words=50,
              max_words=2000, pov="third", em_dash="warn")
    ok &= _expect("an em dash only warns under --em-dash warn", r["exit"] == 0, r)
    r = audit(COHERENT.replace("station voice", "Marlow voice").replace("the train", "Marlow"),
              cast=cast, min_words=50, max_words=2000, pov="third", em_dash="forbid")
    ok &= _expect("a proper noun outside the cast warns", any(
        w["check"] == "unlisted-proper-noun" for w in r["warns"]), r)
    print(f"\n{'all' if ok else 'NOT all'} self-tests passed")
    return 0 if ok else 1


def _expect(label: str, cond: bool, r: dict) -> bool:
    print(f"  {'pass' if cond else 'FAIL'}  {label}")
    if not cond:
        print("        ", json.dumps({"fails": r["fails"], "warns": r["warns"]})[:400])
    return bool(cond)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scene", nargs="?")
    ap.add_argument("--beat")
    ap.add_argument("--beats", type=Path)
    ap.add_argument("--bible", type=Path)
    ap.add_argument("--cast", default="")
    ap.add_argument("--min", type=int)
    ap.add_argument("--max", type=int)
    ap.add_argument("--pov", choices=["first", "third"], default=None)
    ap.add_argument("--em-dash", choices=["forbid", "warn"], default="forbid")
    ap.add_argument("--json", type=Path)
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if not a.scene:
        ap.error("scene path required (or --self-test)")

    cast = {c.strip() for c in a.cast.split(",") if c.strip()}
    if a.bible and a.bible.exists():
        cast |= cast_from_bible(a.bible)
    min_w, max_w, pov = 300, 1500, "third"
    if a.beat and a.beats:
        b = load_beat(a.beats, a.beat)
        min_w = b.get("words", {}).get("min", min_w)
        max_w = b.get("words", {}).get("max", max_w)
        pov = "first" if str(b.get("person", "third")).startswith("first") else "third"
        cast |= set(b.get("present", [])) | set(b.get("also_present", []))
    if a.min:
        min_w = a.min
    if a.max:
        max_w = a.max
    if a.pov:
        pov = a.pov

    text = Path(a.scene).read_text()
    r = audit(text, cast=cast, min_words=min_w, max_words=max_w, pov=pov, em_dash=a.em_dash)
    print_report(r, a.scene, a.quiet)
    if a.json:
        a.json.parent.mkdir(parents=True, exist_ok=True)
        a.json.write_text(json.dumps(r, indent=2))
    return r["exit"]


if __name__ == "__main__":
    sys.exit(main())
