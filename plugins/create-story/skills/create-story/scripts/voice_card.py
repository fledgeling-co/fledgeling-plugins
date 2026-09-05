#!/usr/bin/env python3
"""Voice card: compose a bible `## Voice` section from an author base and named
influences, then measure a scene against the bands it declares.

The catalogue (references/influences.md) holds one card per author. A card is
a `## <Name>` heading followed by `key: value` lines and a `moves:` list. The
numeric keys are bands a scene can be measured against; the moves are rules a
drafter can follow and a critic can quote a slip of. Composition is
deterministic so the same choice of influences produces the same Voice section
every time, and so the section can say which card each rule came from.

Usage:
  voice_card.py compose --base "Luke Rhodes" [--influence NAME ...] [--sample FILE]
                        [--catalogue references/influences.md] [--max-rules 5]
  voice_card.py check SCENE.md --bible story/bible.md [--quiet]
  voice_card.py list [--catalogue ...]
  voice_card.py --self-test

A card may also carry `recall:` lines, a model's memory of the books rather than
a sourced observation; `compose --use-recall` lets them fill rule slots after the
sourced moves, and each such rule is suffixed [recall] so the critic knows its
standing.

`compose` prints a `## Voice` block to stdout: the merged bands as one JSON
line, at most --max-rules rules (base first, then each influence in turn, round
robin, so no single influence crowds the others), a Borrow and Leave list, and
the sample. Paste it into the bible in place of the existing `## Voice`.

`check` reads the `bands:` line from the bible's Voice section and measures the
scene: mean sentence length in words, dialogue share (words inside quotation
marks), the longest paragraph, and narrating person. Exit 1 when a measured
value falls outside its band. Tense is not measured; the critic reads it.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_CATALOGUE = HERE.parent / "references" / "influences.md"

BAND_KEYS = ("sentence_mean", "dialogue_share", "paragraph_max")


def parse_catalogue(text: str) -> dict[str, dict]:
    cards: dict[str, dict] = {}
    cur = None
    fenced = False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            cur = m.group(1).strip()
            cards[cur] = {"moves": [], "recall": [], "borrow": [], "leave": [], "sources": []}
            continue
        if cur is None:
            continue
        m = re.match(r"^-\s+(.*)$", line)
        if m and cards[cur].get("_list"):
            cards[cur][cards[cur]["_list"]].append(m.group(1).strip())
            continue
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            k, v = m.group(1), m.group(2).strip()
            if k in ("moves", "recall", "borrow", "leave", "sources"):
                cards[cur]["_list"] = k
                if v:
                    cards[cur][k].append(v)
            else:
                cards[cur]["_list"] = None
                cards[cur][k] = v
        elif line.strip() == "":
            cards[cur]["_list"] = None
    for c in cards.values():
        c.pop("_list", None)
    return cards


def band(v: str) -> tuple[float, float] | None:
    m = re.match(r"^\s*([\d.]+)\s*-\s*([\d.]+)\s*$", v or "")
    return (float(m.group(1)), float(m.group(2))) if m else None


def merge_bands(cards: list[dict]) -> dict:
    """Intersect where the bands overlap, else take the base card's band."""
    out = {}
    for k in BAND_KEYS:
        bs = [band(c.get(k, "")) for c in cards]
        bs = [b for b in bs if b]
        if not bs:
            continue
        lo, hi = max(b[0] for b in bs), min(b[1] for b in bs)
        out[k] = [lo, hi] if lo <= hi else list(bs[0])
    persons = [c.get("person") for c in cards if c.get("person")]
    if persons:
        out["person"] = persons[0] if persons[0] != "any" else next((p for p in persons if p != "any"), "any")
    tenses = [c.get("tense") for c in cards if c.get("tense")]
    if tenses:
        out["tense"] = tenses[0] if tenses[0] != "any" else next((t for t in tenses if t != "any"), "any")
    return out


def compose(cards: dict[str, dict], base: str, influences: list[str],
            sample: str | None, max_rules: int, use_recall: bool = False) -> str:
    missing = [n for n in [base] + influences if n not in cards]
    if missing:
        raise SystemExit(f"not in the catalogue: {', '.join(missing)}; `voice_card.py list` shows the names")
    chosen = [cards[base]] + [cards[n] for n in influences]
    names = [base] + influences
    bands = merge_bands(chosen)
    rules: list[tuple[str, str]] = []
    # Sourced moves first; recall lines (a model's memory of the books, marked
    # as such on the card) join the queue only when asked for, after them.
    queues = [list(c["moves"]) + ([f"{r} [recall]" for r in c["recall"]] if use_recall else [])
              for c in chosen]
    # Base first, then round robin, so each influence lands at least one rule
    # before any lands a second.
    while len(rules) < max_rules and any(queues):
        for name, q in zip(names, queues):
            if q and len(rules) < max_rules:
                rules.append((name, q.pop(0)))
    out = ["## Voice", ""]
    out.append(f"bands: {json.dumps(bands)}")
    out.append(f"composed_from: {json.dumps(names)}")
    out.append("")
    for i, (name, rule) in enumerate(rules, 1):
        out.append(f"{i}. {rule} ({name})")
    out.append("")
    borrow = [f"{b} ({n})" for n, c in zip(names, chosen) for b in c["borrow"]]
    leave = [f"{b} ({n})" for n, c in zip(names, chosen) for b in c["leave"]]
    if borrow:
        out.append("Borrow: " + "; ".join(borrow) + ".")
    if leave:
        out.append("Leave: " + "; ".join(leave) + ".")
    out.append("")
    if sample:
        out.append("Sample:")
        out.append("")
        out.append(sample.strip())
    else:
        out.append("Sample: none yet. Write one of at most 300 words in this voice before the first scene; `voice_card.py check` warns until it exists.")
    return "\n".join(out) + "\n"


def voice_section(bible: str) -> str:
    m = re.search(r"^##\s+Voice\s*$(.*?)(?=^##\s|\Z)", bible, re.S | re.M)
    return m.group(1) if m else ""


def measure(scene: str) -> dict:
    paras = [p.strip() for p in re.split(r"\n\s*\n", scene.strip()) if p.strip()
             and not re.match(r"^(\*\s*\*\s*\*|#{1,6}\s|---+)", p.strip())]
    words = scene.split()
    quoted = re.findall(r"[\"“]([^\"”]+)[\"”]", scene)
    qwords = sum(len(q.split()) for q in quoted)
    outside = re.sub(r"[\"“][^\"”]+[\"”]", " ", scene)
    sents = [s for s in re.findall(r"[^.!?]+[.!?]+[\"”’]?", outside) if s.strip()]
    lens = [len(s.split()) for s in sents]
    mean = sum(lens) / len(lens) if lens else 0
    first = len(re.findall(r"\b(I|me|my|mine|we|our|us)\b", outside))
    third = len(re.findall(r"\b(he|she|they|him|her|them|his|hers|their)\b", outside, re.I))
    person = "first" if first > third else "third"
    return {
        "sentence_mean": round(mean, 1),
        "dialogue_share": round(qwords / len(words), 2) if words else 0,
        "paragraph_max": max((len(p.split()) for p in paras), default=0),
        "person": person,
        "sentences": len(lens),
        "words": len(words),
    }


def check(scene: str, bible: str) -> tuple[list[str], list[str], dict]:
    fails, warns = [], []
    sec = voice_section(bible)
    if not sec.strip():
        return ["bible has no ## Voice section"], [], {}
    m = re.search(r"^bands:\s*(\{.*\})\s*$", sec, re.M)
    if not m:
        return [], ["Voice section has no bands: line; nothing to measure (compose it with voice_card.py)"], {}
    bands = json.loads(m.group(1))
    if "Sample: none yet" in sec:
        warns.append("Voice section has no sample yet")
    got = measure(scene)
    for k in BAND_KEYS:
        if k in bands:
            lo, hi = bands[k]
            v = got[k]
            if v < lo or v > hi:
                fails.append(f"{k} {v} outside band {lo}-{hi}")
    if bands.get("person") in ("first", "third") and got["person"] != bands["person"]:
        fails.append(f"person reads as {got['person']}, voice says {bands['person']}")
    return fails, warns, got


SELF_CATALOGUE = """# Influences

## Base A
person: third
tense: past
sentence_mean: 5-16
dialogue_share: 0.1-0.5
paragraph_max: 120
moves:
- Plain verbs with a named actor.
- No em dashes; a semicolon or a full stop instead.
borrow:
- the short paragraph
leave:
- nothing

## Author B
person: first
tense: present
sentence_mean: 4-12
dialogue_share: 0.15-0.6
paragraph_max: 80
moves:
- Every chapter ends on a one-line hook.
- Jokes as pressure valves after a hard beat.
borrow:
- the log-entry frame
leave:
- the profanity density
"""

SELF_SCENE = """The train went. Bisk heard it before she felt it, a long pull of air down the tunnel.

"You don't have to stay," said the voice. "Nobody would know."

She knew. She set her back against the post and watched the dark.
"""


def self_test() -> int:
    cases = []
    cards = parse_catalogue(SELF_CATALOGUE)
    cases.append(("the catalogue parses two cards", set(cards) == {"Base A", "Author B"}))
    cases.append(("moves parse as a list", cards["Author B"]["moves"][0].startswith("Every chapter")))
    v = compose(cards, "Base A", ["Author B"], None, 5)
    cases.append(("compose emits a bands line", "bands:" in v))
    b = json.loads(re.search(r"^bands:\s*(\{.*\})", v, re.M).group(1))
    cases.append(("overlapping bands intersect", b["sentence_mean"] == [5.0, 12.0]))
    cases.append(("base person wins", b["person"] == "third"))
    cases.append(("rules round-robin base first", "(Base A)" in v.splitlines()[5] and "(Author B)" in v.splitlines()[6]))
    cases.append(("no sample warns in the block", "Sample: none yet" in v))
    got = measure(SELF_SCENE)
    cases.append(("dialogue share is measured", 0.15 < got["dialogue_share"] < 0.4))
    fails, warns, _ = check(SELF_SCENE, "# Bible\n\n" + v + "\n## World\n")
    cases.append(("the fixture scene passes its bands", not fails))
    cases.append(("a missing sample warns", any("sample" in w for w in warns)))
    bad = SELF_SCENE.replace("She knew.", "She knew that the station had been built in a year when nobody expected trains to run again and the tunnel had been cut through rock that nobody had surveyed properly, which was the kind of thing she noticed now.")
    fails, _, _ = check(bad, "# Bible\n\n" + v)
    cases.append(("a long-sentence scene fails the band", any("sentence_mean" in f for f in fails)))
    try:
        compose(cards, "Base A", ["Nobody"], None, 5)
        cases.append(("an unknown influence is refused", False))
    except SystemExit:
        cases.append(("an unknown influence is refused", True))
    ok = True
    for name, passed in cases:
        print(f"  {'pass' if passed else 'FAIL'}  {name}")
        ok = ok and passed
    print("\nall self-tests passed" if ok else "\nself-test failures")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--self-test", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("compose")
    c.add_argument("--base", required=True)
    c.add_argument("--influence", action="append", default=[])
    c.add_argument("--sample")
    c.add_argument("--catalogue", default=str(DEFAULT_CATALOGUE))
    c.add_argument("--max-rules", type=int, default=5)
    c.add_argument("--use-recall", action="store_true",
                   help="let a card's recall lines fill rule slots after its sourced moves")
    k = sub.add_parser("check")
    k.add_argument("scene")
    k.add_argument("--bible", required=True)
    k.add_argument("--quiet", action="store_true")
    l = sub.add_parser("list")
    l.add_argument("--catalogue", default=str(DEFAULT_CATALOGUE))
    a = ap.parse_args(argv)
    if a.self_test:
        return self_test()
    if a.cmd == "list":
        cards = parse_catalogue(Path(a.catalogue).read_text())
        for n, c in cards.items():
            print(f"{n}: {c.get('person', '?')} person, {c.get('tense', '?')} tense, {len(c['moves'])} moves, {len(c['recall'])} recall, {len(c['sources'])} sources")
        return 0
    if a.cmd == "compose":
        cards = parse_catalogue(Path(a.catalogue).read_text())
        sample = Path(a.sample).read_text() if a.sample else None
        sys.stdout.write(compose(cards, a.base, a.influence, sample, a.max_rules, a.use_recall))
        return 0
    if a.cmd == "check":
        fails, warns, got = check(Path(a.scene).read_text(), Path(a.bible).read_text())
        print(f"{a.scene}: {len(fails)} fail(s), {len(warns)} warning(s)  measured {json.dumps(got)}")
        for f in fails:
            print(f"  FAIL  {f}")
        if not a.quiet:
            for w in warns:
                print(f"  warn  {w}")
        return 1 if fails else 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
