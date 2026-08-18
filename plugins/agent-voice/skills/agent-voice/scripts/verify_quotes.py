#!/usr/bin/env python3
"""
verify_quotes.py — prove every vendor quote in this package is verbatim.

A sibling skill in this repository shipped three of its own sentences inside
quotation marks attributed to Google. The failure is invisible on review: a
plausible paraphrase reads exactly like a citation. So this script extracts
every block quote and every long inline quote from the reference files, and
checks each one appears in a source file, normalising only whitespace and
quote glyphs.

Sources are named on the command line, so the check runs against whatever
copies of the vendor documentation are on disk:

    python3 scripts/verify_quotes.py \\
        --sources /tmp/anthro-prompting-claude-opus-5.md \\
                  /tmp/anthro-best-practices.md \\
                  /tmp/anthro-migration-guide.md \\
                  ~/.claude/commands/gemini-prompt-engineering.md \\
        references/evidence.md references/agent-voice.md references/dialects.md

Exit 0 only when every extracted quote is found. A quote this cannot verify is
reported with the source list it was searched against, so a missing source file
is distinguishable from a wrong quote.
"""

import argparse
import re
import sys
import unicodedata


def normalise(text):
    """Collapse whitespace and fold the glyphs that differ between copies."""
    text = unicodedata.normalize("NFKC", text)
    # Every quote glyph folds to one character. A faithful rendering often
    # demotes a source's nested double quotes to singles, and that is a
    # typographic choice rather than a change of wording.
    for a, b in [("“", '"'), ("”", '"'), ("‘", '"'),
                 ("’", '"'), ("'", '"'), ("—", "-"), ("–", "-"),
                 (" ", " ")]:
        text = text.replace(a, b)
    text = re.sub(r"\[([^\]]{1,120})\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\*\*|\*|`|\\", "", text)
    text = re.sub(r"\s+", " ", text).strip().lower()
    # A block quote carries this package's own quotation marks around it; the
    # source has none, so they are punctuation of the citation rather than of
    # the quote.
    return text.strip('" ')


MARKER = re.compile(r"\[(Anthropic|Google)\]")


def extract(path, min_words):
    """Yield (label, quote, vendor) for spans that make a citation claim.

    Only attributed spans are checked, because those are the ones asserting a
    vendor wrote something. An ordinary quoted phrase in this package's own
    prose ("Background", "all states") asserts nothing and is not a citation, so
    including it buries the real signal under false positives.

    Two conventions carry attribution here:
      *"..."* followed within ~200 characters by `[Anthropic]` or `[Google]`
      a > block quote sitting under a heading that names one of them
    """
    raw = open(path, encoding="utf-8").read()
    out = []

    for m in re.finditer(r'\*"(.{20,900}?)"\*', raw, re.S):
        tail = raw[m.end():m.end() + 220]
        marker = MARKER.search(tail)
        if marker:
            line = raw[:m.start()].count("\n") + 1
            out.append((f"{path}:{line}", m.group(1), marker.group(1)))

    # Block quotes, attributed by the nearest preceding vendor section heading.
    vendor = None
    block, start = [], None
    for i, line in enumerate(raw.splitlines(), 1):
        if line.startswith("## ") or line.startswith("### "):
            found = MARKER.search(line) or re.search(r"`\[(Anthropic|Google)\]`", line)
            if line.startswith("## "):
                vendor = found.group(1) if found else None
        if line.lstrip().startswith(">"):
            if start is None:
                start = i
            block.append(re.sub(r"^\s*>\s?", "", line))
        elif block:
            if vendor:
                out.append((f"{path}:{start}", " ".join(block), vendor))
            block, start = [], None
    if block and vendor:
        out.append((f"{path}:{start}", " ".join(block), vendor))

    return [(l, q, v) for l, q, v in out if len(q.split()) >= min_words]


def fragments(quote):
    """Split an elided quote into the contiguous runs the source must contain.

    An ellipsis marks text the author deliberately left out, so the quote is not
    one contiguous string in the source and never will be. Each side of it is,
    which is what actually needs verifying.
    """
    parts = re.split(r"\s*(?:\u2026|\.\.\.)\s*", quote)
    return [p for p in parts if len(p.split()) >= 4] or [quote]


def main():
    ap = argparse.ArgumentParser(description="Verify vendor quotes are verbatim.")
    ap.add_argument("files", nargs="+", help="Reference files to check")
    ap.add_argument("--sources", nargs="+", required=True,
                    help="Source documents the quotes must appear in")
    ap.add_argument("--min-words", type=int, default=8,
                    help="Shortest quote to check (default 8 words)")
    args = ap.parse_args()

    corpus = []
    for s in args.sources:
        try:
            corpus.append((s, normalise(open(s, encoding="utf-8").read())))
        except OSError as e:
            print(f"warn  source unreadable: {s} ({e})")
    if not corpus:
        print("no readable sources; cannot verify anything")
        return 2

    found = unfound = 0
    misses = []
    for f in args.files:
        for label, quote, vendor in extract(f, args.min_words):
            frags = fragments(quote)
            missing = [fr for fr in frags
                       if not any(normalise(fr) in body for _, body in corpus)]
            if missing:
                unfound += 1
                misses.append((label, missing[0], vendor))
            else:
                found += 1

    for label, quote, vendor in misses:
        print(f"UNVERIFIED  {label}  attributed to [{vendor}]")
        print(f"            {quote[:220]}")

    print(f"\n{found} quote(s) verified verbatim, {unfound} unverified"
          f" (against {len(corpus)} source file(s))")
    if unfound:
        print("An unverified quote is either paraphrased, spans a passage the source"
              " splits differently, or is this package's own prose in quotation marks."
              " Check each one; do not attribute what a source did not write.")
    return 1 if unfound else 0


if __name__ == "__main__":
    sys.exit(main())
