#!/usr/bin/env python3
"""
voice_lint.py — deterministic guardrail for a voice-persona content draft.

Config-driven: reads a voice-lint.json generated alongside it in the persona
package, so one script serves every person's package. Why this exists: banned
phrases, dash policy, and AI-tell density are the things a language model most
reliably slips on, and "I checked" is not the same as checking. Run it on the
final draft body before delivering; it catches the mechanical failures so the
human review can focus on whether it actually sounds like the person.

Usage:
    python3 voice_lint.py --config voice-lint.json --format linkedin draft.md
    python3 voice_lint.py draft.md                # built-in defaults, no config
    cat draft.md | python3 voice_lint.py -
    python3 voice_lint.py --extract-fingerprint corpus/*.md
        # prints the stylometric "fingerprint" JSON block for voice-lint.json;
        # the lint then flags drafts that drift from the corpus rhythm

Exit code is non-zero on any hard failure (em dash where forbidden, banned
phrase, chat leakage, markdown artifacts where the format renders none), so it
can gate delivery. Everything else is advisory and never fails the run.
"""

import argparse
import json
import re
import sys

# ---------------------------------------------------------------- defaults

# Universal AI-cliché phrases (lowercase substring match). Drawn from
# ai-writing-signs.md; a generated config extends this list, never shrinks it.
DEFAULT_CLICHES = [
    "dynamic landscape", "let's dive in", "lets dive in", "let's break it down",
    "lets break it down", "in today's fast-paced", "in todays fast-paced",
    "fast-paced world", "game-changer", "game changer", "unlock the power",
    "unlock the potential", "delve into", "delving into", "robust synergy",
    "ever-evolving", "ever evolving", "navigate the complexities",
    "at the end of the day", "move the needle", "needle-moving",
    "leverage the power", "it's no secret that", "its no secret that",
    "buckle up", "the bottom line is", "paradigm shift", "best-in-class",
    "low-hanging fruit", "supercharge", "rich tapestry", "stands as a testament",
    "serves as a testament", "is a testament to", "marking a pivotal",
    "a pivotal moment", "underscores the importance", "underscores its",
    "highlights the importance", "highlighting the importance",
    "in the heart of", "nestled in", "nestled within",
    "evolving landscape", "indelible mark", "deeply rooted",
    "valuable insights", "key takeaway", "in an era of", "in an era where",
    "important to note", "worth noting that", "it should be noted",
]

# Words from the AI-vocabulary corpus studies. Individually weak, dense
# together strong — so this is a density check, not a per-word ban.
AI_VOCAB = [
    "delve", "tapestry", "testament", "underscore", "underscores", "pivotal",
    "crucial", "intricate", "intricacies", "meticulous", "meticulously",
    "boasts", "showcase", "showcases", "showcasing", "garner", "garnered",
    "fostering", "bolster", "bolstered", "interplay", "vibrant", "enduring",
    "groundbreaking", "seamless", "seamlessly", "cutting-edge", "world-class",
    "renowned", "multifaceted", "holistic",
]

# Assistant-correspondence leakage: fatal in ghostwritten content.
CHAT_LEAKAGE = [
    "i hope this helps", "certainly!", "of course!", "would you like me to",
    "let me know if you", "here's a draft", "here is a draft",
    "feel free to adjust", "i've kept the tone", "as an ai",
    "[your name]", "[insert", "[link to", "[topic]", "[company]",
]

# Structural AI-tell regexes (advisory): negative parallelisms, participle
# analysis tails, inline-header bullets.
# Quiet claim shapes (advisory): frequency/comparative assertions phrased as calm
# domain wisdom. "Most X <verb>..." and "more ... than <baseline>" are statistics
# even when no number appears; they need a source, a hedge ("a common", "often"),
# or an internal referent the reader can check. Sentences already carrying a
# citation "(...)" nearby still warn — the human judges.
QUIET_FREQ = re.compile(
    r"(?im)(?:^|(?<=[.!?:]\s)|(?<=[.!?:]\s\s))most\s+(?:[a-z][\w-]*\s+){1,3}"
    r"(?:is|are|was|were|comes?|goes?|gets?|has|have|do|does|happens?|fails?|reads?|"
    r"re-\w+s?|\w+ises?|\w+izes?)\b"
)
QUIET_COMPARATIVE = re.compile(
    r"(?i)\b(?:more|better|worse|faster|harder|longer)\s+[\w\s-]{0,35}\bthan\s+"
    r"(?:news|memory|any\b|anything|anyone|most\b|all\b|either\b|ever\b)"
)

NEG_PARALLEL = re.compile(
    r"(?i)\b(it'?s not just|isn'?t just|not only .{3,60} but also"
    r"|it'?s not (?:a |an |about )?\w+[,;] it'?s"
    r"|\w+ (?:the|a|an|your|his|her|their) (?:\w+ ){0,2}?\w+, never (?:the|a|an|your|his|her|their) \w+"
    r"|not (?:the|a|an) \w+, but (?:the|a|an) \w+)"
)
PARTICIPLE_TAIL = re.compile(
    r"(?i),\s(?:highlighting|underscoring|emphasi[sz]ing|showcasing|reflecting"
    r"|demonstrating|ensuring|fostering|cementing|solidifying|signaling"
    r"|signalling|reinforcing)\s[^.]{5,}\.$"
)
BOLD_HEADER_BULLET = re.compile(r"^\s*[-*•]\s+\*\*[^*]+:?\*\*")
MARKDOWN_BOLD = re.compile(r"\*\*[^*]+\*\*")
MARKDOWN_HEADING = re.compile(r"^#{1,6}\s")
EM_DASHES = ["—", "―"]
EN_DASH = "–"
EMOJI = re.compile(
    "[\U0001F300-\U0001FAFF\U00002700-\U000027BF\U0001F1E6-\U0001F1FF⬀-⯿☀-⛿]"
)

# Formats where the destination renders no markdown, so surviving syntax is a
# paste artifact.
PLAINTEXT_FORMATS = {"linkedin", "short", "slack", "email"}

BUILTIN_FORMATS = {
    "linkedin":  {"max_chars": 3000, "warn_words": 450,
                  "note": "150-400 words tends to over-perform for feed posts"},
    "blog":      {"min_words": 1200,
                  "note": "long-form sweet spot is ~1500-2200 words"},
    "marketing": {"note": "demonstrate concretely; hype adjectives warn"},
    "short":     {"warn_words": 90, "info_chars": 280,
                  "note": "one idea; X budget is 280 chars"},
    "slack":     {"warn_words": 120, "note": "long messages become docs or calls"},
    "email":     {"warn_words": 250, "note": "long emails go unread"},
    "review":    {"note": "calm register; bare negations warn"},
    "brief":     {"max_segment_words": 450, "note": "spoken/segmented register"},
}

HYPE_ADJECTIVES = ["revolutionary", "seamless", "cutting-edge", "world-class",
                   "next-generation", "innovative", "game-changing", "unparalleled"]

US_TELLS = ["organize", "organized", "organizing", "color", "behavior", "optimize",
            "optimized", "favorite", "analyze", "center,", "utilize", "realize"]
AU_TELLS = ["organise", "colour", "behaviour", "optimise", "favourite", "analyse",
            "utilise", "realise"]


def read_text(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_config(path):
    cfg = {
        "em_dash": "forbid",
        "banned_phrases": list(DEFAULT_CLICHES),
        "advisory_phrases": [],
        "ai_vocab_extra": [],
        "spelling": "none",
        "exclamations": "allow",
        "emoji": "allow",
        "formats": {},
    }
    if path:
        with open(path, "r", encoding="utf-8") as f:
            user = json.load(f)
        for key, val in user.items():
            if key == "banned_phrases":
                cfg["banned_phrases"] = sorted(set(DEFAULT_CLICHES) | {p.lower() for p in val})
            elif key == "formats":
                cfg["formats"].update(val)
            else:
                cfg[key] = val
    return cfg


def line_hits(text, phrases):
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        for p in phrases:
            if p in low:
                hits.append((i, p, line.strip()))
    return hits


# ---------------------------------------------------------- stylometrics
# Deterministic fingerprint of the subconscious layer (sentence rhythm,
# contractions, punctuation densities, nominalizations). Computed from the
# corpus at persona-build time (--extract-fingerprint), compared against each
# draft as ADVISORIES: LLM output drifts toward uniform mid-length sentences
# and abstract nouns even when the surface style matches, and a model judging
# its own fidelity is uncalibrated — these numbers are the calibrated check.

NOMINALIZATION = re.compile(
    r"\b\w{4,}(?:tion|tions|sion|sions|ment|ments|ness|ance|ence|ities|ity)\b", re.I)
CONTRACTION = re.compile(r"\b\w+['’](?:t|s|re|ve|ll|d|m)\b", re.I)


def split_sentences(text):
    # strip code blocks, headings, list markers; keep prose
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^#{1,6} .*$", " ", text, flags=re.M)
    text = re.sub(r"^\s*[-*•]\s+", "", text, flags=re.M)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z\"'“(])", text)
    return [p.strip() for p in parts if len(re.findall(r"\b\w+\b", p)) >= 2]


def fingerprint(text):
    sents = split_sentences(text)
    if not sents:
        return None
    lens = [len(re.findall(r"\b\w+\b", s)) for s in sents]
    n_words = sum(lens)
    mean = sum(lens) / len(lens)
    sd = (sum((l - mean) ** 2 for l in lens) / len(lens)) ** 0.5
    paras = [p for p in re.split(r"\n\s*\n", text) if split_sentences(p)]
    para_sents = [len(split_sentences(p)) for p in paras]
    return {
        "mean_sentence_words": round(mean, 1),
        "sd_sentence_words": round(sd, 1),
        "contraction_per_100w": round(100 * len(CONTRACTION.findall(text)) / n_words, 2),
        "comma_per_sentence": round(text.count(",") / len(sents), 2),
        "semicolon_per_1000w": round(1000 * text.count(";") / n_words, 2),
        "nominalization_per_1000w": round(1000 * len(NOMINALIZATION.findall(text)) / n_words, 1),
        "mean_paragraph_sentences": round(sum(para_sents) / max(1, len(para_sents)), 1),
    }


def repeated_phrases(text, allow=(), n=4, limit=8):
    """Distinctive word runs (n+ words) occurring 2+ times — the once-per-document
    rule, made checkable. Repeating a natural TERM is human (elegant variation is
    the AI tell); repeating a rhetorical PHRASE is templating. The n-gram check
    can't tell them apart, so results are advisories and scaffold labels belong
    in the config's repeat_allowlist."""
    body = re.sub(r"```.*?```", " ", text, flags=re.S)
    words = re.findall(r"[a-z'’]+", body.lower())
    if len(words) < n * 2:
        return []
    shingles = [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]
    counts = {}
    for s in shingles:
        counts[s] = counts.get(s, 0) + 1
    repset = {i for i, s in enumerate(shingles) if counts[s] >= 2}
    phrases = {}
    k = 0
    while k < len(shingles):
        if k in repset:
            j = k
            while j + 1 in repset and j + 1 - k < 12:
                j += 1
            phrase = " ".join(words[k:j + n])
            phrases[phrase] = phrases.get(phrase, 0) + 1
            k = j + 1
        else:
            k += 1
    allow_low = [a.lower() for a in allow]
    out = [(p, c) for p, c in phrases.items()
           if c >= 2 and not any(a in p for a in allow_low)]
    return sorted(out, key=lambda x: -x[1])[:limit]


def compare_fingerprint(draft_fp, target):
    """Yield advisory strings where the draft deviates markedly from the corpus."""
    checks = [
        ("mean_sentence_words", 0.35, "average sentence length"),
        ("sd_sentence_words", 0.40, "sentence-length variance (uniform rhythm is an LLM tell)"),
        ("contraction_per_100w", 0.50, "contraction rate"),
        ("comma_per_sentence", 0.50, "comma density"),
        ("nominalization_per_1000w", 0.50, "nominalization rate (-tion/-ment/-ness abstractions)"),
    ]
    for key, tol, label in checks:
        want = target.get(key)
        got = draft_fp.get(key)
        if want is None or got is None or want == 0:
            continue
        if abs(got - want) / want > tol:
            direction = "above" if got > want else "below"
            yield (f"{label}: draft {got} vs corpus {want} "
                   f"({direction} the ±{int(tol*100)}% band)")


def main():
    ap = argparse.ArgumentParser(description="Lint a voice-persona draft.")
    ap.add_argument("path", nargs="+",
                    help="Draft to lint (or - for stdin); with --extract-fingerprint, corpus files")
    ap.add_argument("--config", default=None, help="Path to voice-lint.json")
    ap.add_argument("--format", dest="fmt", default=None,
                    help="Format key (linkedin, blog, marketing, short, slack, email, review, brief)")
    ap.add_argument("--extract-fingerprint", action="store_true",
                    help="Compute the stylometric fingerprint of the given corpus files and print "
                         "the JSON block to paste into voice-lint.json")
    args = ap.parse_args()

    if args.extract_fingerprint:
        corpus = "\n\n".join(read_text(p) for p in args.path)
        fp = fingerprint(corpus)
        if fp is None:
            print("no prose found in corpus files"); sys.exit(1)
        n_words = len(re.findall(r"\b\w+\b", corpus))
        print(json.dumps({"fingerprint": fp}, indent=2))
        note = ("stable" if n_words >= 2000 else
                "usable but below the ~2,000-word stability threshold" if n_words >= 800 else
                "thin — treat these numbers as rough")
        print(f"// corpus: {n_words} words ({note})")
        sys.exit(0)

    if len(args.path) > 1:
        print("lint takes one draft at a time"); sys.exit(2)
    args.path = args.path[0]

    cfg = load_config(args.config)
    text = read_text(args.path)
    lines = text.splitlines()
    failures = 0

    # --- Em dashes ---
    em_hits = [(i, l.strip()) for i, l in enumerate(lines, 1)
               if any(d in l for d in EM_DASHES)]
    if em_hits:
        if cfg["em_dash"] == "forbid":
            failures += len(em_hits)
            print("FAIL  em dash found (use ; , . or parentheses, or restructure):")
        else:
            print("warn  em dash found (allowed for this voice, but check density and"
                  " the spaced punchy pattern):")
        for i, line in em_hits:
            print(f"      line {i}: {line}")
    else:
        print("ok    no em dashes")

    # --- En dash outside numeric ranges (advisory) ---
    for i, line in enumerate(lines, 1):
        for m in re.finditer(re.escape(EN_DASH), line):
            c = m.start()
            left = line[c - 1] if c > 0 else " "
            right = line[c + 1] if c + 1 < len(line) else " "
            if not (left.isdigit() and right.isdigit()):
                print(f"warn  en dash outside a numeric range, line {i}: {line.strip()}")
                break

    # --- Banned phrases ---
    hits = line_hits(text, cfg["banned_phrases"])
    if hits:
        failures += len(hits)
        print("FAIL  banned phrase(s) found (rewrite in plain language):")
        for i, p, line in hits:
            print(f"      line {i}: \"{p}\"  ->  {line}")
    else:
        print("ok    no banned phrases")

    # --- Chat leakage / placeholders ---
    leaks = line_hits(text, CHAT_LEAKAGE)
    if leaks:
        failures += len(leaks)
        print("FAIL  assistant-correspondence or placeholder leakage:")
        for i, p, line in leaks:
            print(f"      line {i}: \"{p}\"  ->  {line}")
    else:
        print("ok    no chat leakage or placeholders")

    # --- Markdown artifacts in plaintext destinations ---
    if args.fmt in PLAINTEXT_FORMATS:
        md_hits = [(i, l.strip()) for i, l in enumerate(lines, 1)
                   if MARKDOWN_BOLD.search(l) or MARKDOWN_HEADING.match(l)]
        if md_hits:
            failures += len(md_hits)
            print(f"FAIL  markdown syntax in a '{args.fmt}' draft (destination renders none):")
            for i, line in md_hits[:5]:
                print(f"      line {i}: {line}")

    # --- Advisory phrases from config ---
    for i, p, line in line_hits(text, [p.lower() for p in cfg["advisory_phrases"]]):
        print(f"warn  advisory phrase \"{p}\", line {i}: {line}")

    # --- AI-vocabulary density (advisory; the strongest soft tell) ---
    vocab = set(AI_VOCAB) | {w.lower() for w in cfg["ai_vocab_extra"]}
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text.lower())
    found = sorted({w for w in words if w in vocab})
    if len(found) >= 3:
        print(f"warn  {len(found)} distinct AI-vocabulary words ({', '.join(found)}); "
              "one may be fine, this density is a tell")
    elif found:
        print(f"info  AI-vocabulary present: {', '.join(found)} (fine in isolation; watch density)")

    # --- Structural tells (advisory) ---
    for i, line in enumerate(lines, 1):
        if NEG_PARALLEL.search(line):
            print(f"warn  negative parallelism (\"not just X, but Y\" shape), line {i}: {line.strip()}")
        if PARTICIPLE_TAIL.search(line.rstrip()):
            print(f"warn  participle analysis tail (\", highlighting/ensuring ...\"), line {i}: {line.strip()}")
        if BOLD_HEADER_BULLET.match(line):
            print(f"warn  inline-header bullet (bullet + bold label + colon), line {i}: {line.strip()}")
        if QUIET_FREQ.search(line):
            print(f"warn  quiet frequency claim (\"Most X ...\" is a statistic even without a number"
                  f" - source it, hedge it, or make it checkable), line {i}: {line.strip()}")
        if QUIET_COMPARATIVE.search(line):
            print(f"warn  quiet comparative claim (\"more ... than <baseline>\" needs a source or a"
                  f" hedge), line {i}: {line.strip()}")

    # --- Emoji / exclamations per config ---
    emoji_lines = [(i, l.strip()) for i, l in enumerate(lines, 1) if EMOJI.search(l)]
    if emoji_lines and cfg["emoji"] == "forbid":
        failures += len(emoji_lines)
        print("FAIL  emoji found (forbidden for this voice):")
        for i, line in emoji_lines[:5]:
            print(f"      line {i}: {line}")
    elif len(emoji_lines) > 1 and cfg["emoji"] == "ration":
        print(f"warn  {len(emoji_lines)} lines with emoji; this voice rations them (≤1)")

    bangs = text.count("!")
    if bangs and cfg["exclamations"] == "forbid":
        failures += bangs
        print(f"FAIL  {bangs} exclamation mark(s); forbidden for this voice")
    elif bangs > 1 and cfg["exclamations"] == "ration":
        print(f"warn  {bangs} exclamation marks; this voice rations them")

    # --- Spelling variety (advisory) ---
    if cfg["spelling"] == "AU":
        for i, p, line in line_hits(text, US_TELLS):
            print(f"warn  US spelling \"{p}\" (voice is AU/UK), line {i}")
    elif cfg["spelling"] == "US":
        for i, p, line in line_hits(text, AU_TELLS):
            print(f"warn  AU/UK spelling \"{p}\" (voice is US), line {i}")

    # --- Stylometric fingerprint (advisory) ---
    target_fp = cfg.get("fingerprint") or {}
    if target_fp:
        draft_words = len(re.findall(r"\b\w+\b", text))
        if draft_words < 120:
            print(f"info  fingerprint skipped ({draft_words} words; stats are unstable under ~120)")
        else:
            draft_fp = fingerprint(text)
            if draft_fp:
                devs = list(compare_fingerprint(draft_fp, target_fp))
                if devs:
                    for d in devs:
                        print(f"warn  fingerprint: {d}")
                else:
                    print("ok    stylometric fingerprint within corpus bands")

    # --- Repeated distinctive phrases (advisory; once-per-document rule) ---
    reps = repeated_phrases(text, allow=cfg.get("repeat_allowlist", []))
    if reps:
        print("warn  repeated phrases (a natural term repeating is fine; a rhetorical "
              "phrase or landing line repeating is templating - judge each):")
        for p, c in reps:
            print(f"        {c}x \"{p}\"")

    # --- Stats + format advisories ---
    n_words = len(re.findall(r"\b\w+\b", text))
    n_chars = len(text)
    print(f"info  {n_words} words, {n_chars} characters")

    hook = next((ln.strip() for ln in lines if ln.strip()), "")
    if hook:
        print(f"info  hook (first line, {len(hook)} chars; ~140-200 show before 'see more'): {hook[:200]}")

    fspec = {**BUILTIN_FORMATS.get(args.fmt or "", {}), **cfg["formats"].get(args.fmt or "", {})}
    if fspec:
        if fspec.get("max_chars") and n_chars > fspec["max_chars"]:
            print(f"warn  {n_chars} chars exceeds the {fspec['max_chars']}-char limit for this format")
        if fspec.get("warn_words") and n_words > fspec["warn_words"]:
            print(f"warn  {n_words} words is long for this format ({fspec.get('note', '')})")
        if fspec.get("min_words") and n_words < fspec["min_words"]:
            print(f"warn  {n_words} words is short for this format ({fspec.get('note', '')})")
        if fspec.get("info_chars") and n_chars > fspec["info_chars"]:
            print(f"info  {n_chars} chars exceeds {fspec['info_chars']} (X/Twitter budget)")
        if args.fmt == "marketing":
            for adj in HYPE_ADJECTIVES:
                if adj in text.lower():
                    print(f"warn  hype adjective \"{adj}\"; demonstrate the benefit concretely instead")
        if args.fmt == "brief" and fspec.get("max_segment_words"):
            seg, longest = 0, 0
            for line in lines:
                if not line.strip() or MARKDOWN_HEADING.match(line):
                    longest, seg = max(longest, seg), 0
                else:
                    seg += len(re.findall(r"\b\w+\b", line))
            longest = max(longest, seg)
            if longest > fspec["max_segment_words"]:
                print(f"warn  longest unbroken segment ~{longest} words; insert a seam before "
                      f"~{fspec['max_segment_words']}")

    print()
    if failures:
        print(f"RESULT: {failures} hard issue(s) — fix before delivering.")
        sys.exit(1)
    print("RESULT: clean on the hard checks.")
    sys.exit(0)


if __name__ == "__main__":
    main()
