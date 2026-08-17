#!/usr/bin/env python3
"""verify_quotes.py — every quoted vendor claim in a gemini.md must be verbatim.

This script exists because of a specific, recorded mistake. While hand-authoring
the first five gemini.md files, the sentence "Verification is prompted rather than
automatic" was written inside quotation marks and attributed to Google's guidance
in three separate files. Google never wrote it: it was a fair paraphrase of what
their thinking guide and agentic template actually say, promoted to a quotation by
the act of putting quote marks around it. Nothing in a review pass caught it,
because a plausible paraphrase reads exactly like a citation.

A gemini.md whose authority rests on vendor documentation cannot carry invented
vendor sentences. So the check is mechanical: pull every quoted span out of the
file, and require each one to appear verbatim in a source corpus.

Usage:
    verify_quotes.py <gemini.md> [--corpus PATH]... [--min-len N] [--json]

    --corpus     a source file quotes may come from. Repeatable. Defaults to
                 ../references/gemini-corpus.md beside the script.
    --min-len    shortest span to check (default 20 chars). Short spans are
                 usually field names or single words, not claims.

Exit codes:
    0  every checkable quote resolved
    1  at least one quote did not appear in any corpus
    2  usage / missing file

stdlib only.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Spans this file quotes but which are NOT vendor claims: the target skill's own
# words, the measured artifact's output, and the author's illustrative examples.
# A quote is exempt when its paragraph names one of these sources.
EXEMPT_MARKERS = (
    "[measured", "[derived", "this skill", "the skill already", "skill.md",
    "its own words", "the run", "the artifact", "measured", "for example",
    "e.g.", "such as", "template", "write ", "report it as",
)

SMART = {
    "“": '"', "”": '"', "‘": "'", "’": "'",
    "–": "-", "—": "-", "…": "...", " ": " ",
}


def is_docs_para(para: str) -> bool:
    """Detect the [docs] tag on the RAW paragraph.

    Not on norm() output: norm() strips bracketed spans so that a grammatical
    alteration like "provide[s]" still matches its source, and that same rule
    deletes the "[docs]" tag. Running tag detection through it took the checked
    count to zero across every file and turned the whole gate green — a false pass
    caught only because the negative control was re-run after the change. Keep the
    two readings of a paragraph separate.
    """
    return "[docs]" in para.lower()


def norm(s: str) -> str:
    """Fold everything that varies between a source and a faithful citation of it:
    smart punctuation, markdown emphasis, line wrapping, and — importantly — the
    quote characters themselves. A writer nesting a quote inside a quote switches
    double to single ('write a summary of 3 sentences or less'), and that is still
    a verbatim citation.

    Two other conventions of honest citation are folded here rather than treated as
    fabrication, because a checker that rejects them trains people to stop citing:
    a bracketed grammatical alteration ("provide[s] direct answers" for a source
    reading "models provide direct answers"), and a quote that ends early and
    closes with a full stop where the source sentence continued."""
    for a, b in SMART.items():
        s = s.replace(a, b)
    s = re.sub(r"\[[^\]\n]{0,12}\]", "", s)   # provide[s] -> provide
    s = re.sub(r"[*_`\"']", "", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower().rstrip(".,;:!?")


def paragraphs(text: str) -> list[str]:
    return re.split(r"\n\s*\n", text)


def quoted_spans(para: str) -> tuple[list[str], bool]:
    """Split on double-quote characters and take the odd segments.

    A regex of the form "([^"]{20,})" looks correct and is not: in a paragraph
    carrying several quotations it pairs the CLOSING mark of one with the OPENING
    mark of the next, emitting spans like `of an airport board returns *"` — prose
    masquerading as a citation, which then fails the corpus check and buries the
    real failures underneath it. Alternating segments is the only correct reading
    of balanced quoting; an odd number of marks means the paragraph is unbalanced,
    which is reported rather than guessed at.
    """
    p = para.replace("“", '"').replace("”", '"')
    parts = p.split('"')
    balanced = len(parts) % 2 == 1
    return [parts[i] for i in range(1, len(parts), 2)], balanced


def fragments(quote: str) -> list[str]:
    """An elision is legitimate citation practice, so `"A … B"` is checked as A
    and B independently. Without this, every properly elided quote reports as
    fabricated."""
    parts = re.split(r"\s*(?:…|\.\.\.)\s*", quote)
    keep = [p for p in parts if len(norm(p)) >= 12]
    return keep or [quote]


def extract(text: str, min_len: int) -> tuple[list[dict], list[str]]:
    """Every quoted span, with the paragraph it sits in and whether it is
    presented as a documentation claim."""
    out, unbalanced = [], []
    for para in paragraphs(text):
        is_docs = is_docs_para(para)
        spans, balanced = quoted_spans(para)
        if is_docs and not balanced:
            unbalanced.append(para.strip()[:120])
            continue
        for span in spans:
            if len(span.strip()) < min_len:
                continue
            out.append({
                "quote": span.strip(),
                "isDocsClaim": is_docs,
                "paragraph": para.strip()[:200],
            })
    return out, unbalanced


def exempt(q: dict) -> bool:
    p = norm(q["paragraph"])
    # A quote inside a [docs] paragraph is a vendor claim unless the paragraph
    # also names a non-vendor source for it.
    if not q["isDocsClaim"]:
        return True
    return any(k in p for k in ("[measured", "[derived", "the skill already says",
                                "in the skill's own words"))


def main() -> int:
    here = pathlib.Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--corpus", action="append", default=[])
    ap.add_argument("--min-len", type=int, default=20)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    t = pathlib.Path(a.target)
    if not t.is_file():
        print(f"no such file: {t}", file=sys.stderr)
        return 2

    corpora = [pathlib.Path(c) for c in a.corpus] or \
              [here.parent / "references" / "gemini-corpus.md"]
    missing_corpus = [c for c in corpora if not c.is_file()]
    if missing_corpus:
        print("corpus not found: " + ", ".join(str(c) for c in missing_corpus),
              file=sys.stderr)
        return 2

    haystack = norm("\n".join(c.read_text(encoding="utf-8", errors="replace")
                              for c in corpora))
    quotes, unbalanced = extract(t.read_text(encoding="utf-8", errors="replace"),
                                 a.min_len)

    checked, verified, failures, skipped = 0, 0, [], 0
    for q in quotes:
        if exempt(q):
            skipped += 1
            continue
        checked += 1
        frags = fragments(q["quote"])
        missing = [f for f in frags if norm(f) not in haystack]
        if not missing:
            verified += 1
        else:
            failures.append({**q, "missingFragments": missing})

    result = {
        "target": str(t),
        "corpora": [str(c) for c in corpora],
        "quotesFound": len(quotes),
        "docsClaimsChecked": checked,
        "verified": verified,
        "notVendorClaims": skipped,
        "unbalancedParagraphs": unbalanced,
        "failures": [{"quote": f["quote"][:160],
                      "missing": [m[:120] for m in f["missingFragments"]],
                      "paragraph": f["paragraph"][:160]} for f in failures],
    }

    if a.json:
        print(json.dumps(result, indent=1))
        return 1 if (failures or unbalanced) else 0

    print(f"target   {t}")
    print(f"corpus   {', '.join(str(c) for c in corpora)}")
    print(f"quotes   {len(quotes)} found · {checked} presented as [docs] claims · "
          f"{skipped} not vendor claims")
    if unbalanced:
        print(f"\nUNBALANCED — {len(unbalanced)} [docs] paragraph(s) have an odd "
              f"number of quote marks,\nso their citations cannot be read:\n")
        for u in unbalanced:
            print(f"  {u}…")
        return 1
    if checked == 0:
        print("\nNo [docs] claims to verify. That is a result, not a pass: a "
              "gemini.md\nwith no cited vendor guidance rests on n=1 alone.")
        return 0
    if not failures:
        print(f"\nOK — {verified}/{checked} vendor quotes appear verbatim in the corpus.")
        return 0
    print(f"\nFAIL — {len(failures)}/{checked} quoted as documentation but not "
          f"found in any corpus:\n")
    for f in failures:
        print(f'  "{f["quote"][:150]}"')
        for m in f["missingFragments"]:
            if norm(m) != norm(f["quote"]):
                print(f"    missing fragment: \"{m[:110]}\"")
        print(f"    in: {f['paragraph'][:130]}…\n")
    print("Either quote the source verbatim, or drop the quote marks and let the")
    print("sentence stand as your own gloss. A paraphrase in quotation marks is")
    print("a fabricated citation, whether or not it is a fair summary.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
