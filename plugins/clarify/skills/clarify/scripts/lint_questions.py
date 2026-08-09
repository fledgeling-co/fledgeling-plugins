#!/usr/bin/env python3
"""Lint an AskUserQuestion payload before it reaches the user.

Reads the tool input as JSON (a file path, or stdin with `-`) and checks it
against the authoring rules in SKILL.md. Every rule here is mechanical: the
things that need judgment — is this question worth asking at all, does the
recommendation have a real reason behind it — are not checked here and are
not claimed to be.

    lint_questions.py payload.json
    cat payload.json | lint_questions.py -
    lint_questions.py payload.json --json

Exit 0 clean, 1 on any error, 2 on a malformed payload. Warnings never fail
the run on their own; --strict promotes them.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass, field

# Limits. The structural four come from Anthropic's interactive-commands
# reference; the length caps come from this skill's own research corpus and
# are cited in references/evidence.md.
MAX_QUESTIONS = 4
MIN_OPTIONS = 2
MAX_OPTIONS = 4
MAX_HEADER_CHARS = 12
MAX_QUESTION_WORDS = 20
MAX_LABEL_WORDS = 5
MAX_DESCRIPTION_WORDS = 30
SIMILARITY_LIMIT = 0.80

RECOMMENDED_RE = re.compile(r"\(recommended\)", re.I)
# Shapes that read as internal vocabulary rather than plain English.
PATH_RE = re.compile(r"(?:^|\s)(?:[~.]?/[\w.\-/]+|[\w\-]+/[\w\-]+/[\w.\-]+)")
CAMEL_RE = re.compile(r"\b[a-z]+[A-Z][A-Za-z]*\b")
SNAKE_RE = re.compile(r"\b[a-z]+_[a-z_]+\b")
ACRONYM_RE = re.compile(r"\b[A-Z]{3,}\b")
# Acronyms common enough that a reader is not being asked to decode anything.
ACRONYM_ALLOW = {
    "API", "CLI", "CSS", "CSV", "DNS", "GPU", "HTML", "HTTP", "HTTPS", "IDE",
    "JSON", "JWT", "MCP", "PDF", "RAM", "SDK", "SQL", "SSH", "SSL", "TLS",
    "UI", "URL", "UUID", "XML", "YAML", "AI", "CPU", "OS", "PR", "QA", "UX",
    "README", "TODO", "CI", "DB", "MVP", "SEO", "USB", "WIFI", "ID",
}
HEDGE_WORDS = {"maybe", "possibly", "perhaps", "somehow", "etc", "stuff", "things"}

# Two labels differing by exactly one opposed word are maximally DIFFERENT in
# meaning while being maximally similar as strings ("drop the newest data" /
# "drop the oldest data"). Character similarity cannot tell that apart from a
# synonym pair, so opposed pairs are exempted from the duplicate check by name.
OPPOSED = [
    {"newest", "oldest"}, {"new", "old"}, {"first", "last"}, {"before", "after"},
    {"enable", "disable"}, {"on", "off"}, {"add", "remove"}, {"keep", "drop"},
    {"include", "exclude"}, {"more", "less"}, {"most", "least"}, {"min", "max"},
    {"start", "stop"}, {"open", "closed"}, {"allow", "deny"}, {"show", "hide"},
    {"up", "down"}, {"in", "out"}, {"asc", "desc"}, {"always", "never"},
    {"local", "remote"}, {"read", "write"}, {"push", "pull"}, {"yes", "no"},
]



@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def words(text: str) -> list[str]:
    return [w for w in re.split(r"\s+", text.strip()) if w]


def similar(a: str, b: str) -> float:
    norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()
    return difflib.SequenceMatcher(None, norm(a), norm(b)).ratio()


def opposed(a: str, b: str) -> bool:
    """True when the two labels differ by a known opposed word pair.

    'Drop the newest data' and 'Drop the oldest data' are 0.9 similar as
    strings and mean opposite things. Without this, the duplicate check fires
    hardest on the clearest choices.
    """
    wa = {w.lower().strip(".,()") for w in words(a)}
    wb = {w.lower().strip(".,()") for w in words(b)}
    diff = wa ^ wb
    return any(pair <= diff for pair in OPPOSED)


def check_plain_language(text: str, where: str, rep: Report) -> None:
    """Flag vocabulary that makes a reader decode rather than decide."""
    if PATH_RE.search(text):
        rep.warn(where, "contains a file path — say what it does, not where it lives")
    if CAMEL_RE.search(text) or SNAKE_RE.search(text):
        rep.warn(where, "contains a code identifier — translate it into plain words")
    unknown = {a for a in ACRONYM_RE.findall(text) if a not in ACRONYM_ALLOW}
    if unknown:
        rep.warn(where, f"unexplained acronym(s): {', '.join(sorted(unknown))}")
    hedges = {w.lower().strip(".,") for w in words(text)} & HEDGE_WORDS
    if hedges:
        rep.warn(where, f"vague wording: {', '.join(sorted(hedges))}")


def lint(payload: dict) -> Report:
    rep = Report()
    questions = payload.get("questions")

    if not isinstance(questions, list) or not questions:
        rep.error("payload", "no questions array")
        return rep
    if len(questions) > MAX_QUESTIONS:
        rep.error(
            "payload",
            f"{len(questions)} questions, limit is {MAX_QUESTIONS} — "
            "drop the ones you can answer yourself",
        )

    for i, q in enumerate(questions, 1):
        where = f"q{i}"
        if not isinstance(q, dict):
            rep.error(where, "not an object")
            continue

        text = (q.get("question") or "").strip()
        header = (q.get("header") or "").strip()
        options = q.get("options") or []
        multi = bool(q.get("multiSelect"))

        # --- the question itself
        if not text:
            rep.error(where, "empty question")
        else:
            n = len(words(text))
            if n > MAX_QUESTION_WORDS:
                rep.error(where, f"question is {n} words, cap is {MAX_QUESTION_WORDS}")
            if not text.endswith("?"):
                rep.warn(where, "does not end in a question mark")
            check_plain_language(text, f"{where} question", rep)

        # --- the header
        if not header:
            rep.error(where, "empty header")
        elif len(header) > MAX_HEADER_CHARS:
            rep.error(
                where,
                f"header {len(header)} chars ('{header}'), cap is {MAX_HEADER_CHARS}",
            )

        # --- the options
        if not isinstance(options, list) or not (MIN_OPTIONS <= len(options) <= MAX_OPTIONS):
            rep.error(
                where,
                f"{len(options) if isinstance(options, list) else 0} options, "
                f"want {MIN_OPTIONS}-{MAX_OPTIONS}",
            )
            continue

        labels, recommended = [], []
        for j, opt in enumerate(options, 1):
            ow = f"{where}.opt{j}"
            if not isinstance(opt, dict):
                rep.error(ow, "not an object")
                continue
            label = (opt.get("label") or "").strip()
            desc = (opt.get("description") or "").strip()
            labels.append(label)

            if not label:
                rep.error(ow, "empty label")
            else:
                if RECOMMENDED_RE.search(label):
                    recommended.append(label)
                bare = RECOMMENDED_RE.sub("", label).strip()
                n = len(words(bare))
                if n > MAX_LABEL_WORDS:
                    rep.error(ow, f"label is {n} words, cap is {MAX_LABEL_WORDS}")
                if bare.lower() == "other":
                    rep.error(ow, "'Other' is added automatically — do not author it")
                check_plain_language(bare, f"{ow} label", rep)

            if not desc:
                rep.error(ow, "no description — say what changes if this is chosen")
            else:
                n = len(words(desc))
                if n > MAX_DESCRIPTION_WORDS:
                    rep.error(ow, f"description is {n} words, cap is {MAX_DESCRIPTION_WORDS}")
                check_plain_language(desc, f"{ow} description", rep)

        # --- one recommendation, on single-select only
        if not multi:
            if len(recommended) == 0:
                rep.error(where, "no option marked (Recommended) — lead with the one you'd pick")
            elif len(recommended) > 1:
                rep.error(where, f"{len(recommended)} options marked (Recommended), want exactly 1")
            if recommended and not RECOMMENDED_RE.search(labels[0] if labels else ""):
                rep.warn(where, "the recommended option is not listed first")
        elif recommended:
            rep.warn(where, "multi-select carries a (Recommended) mark — usually a single-select in disguise")

        # --- options must be genuinely different choices
        for a in range(len(labels)):
            for b in range(a + 1, len(labels)):
                la = RECOMMENDED_RE.sub("", labels[a]).strip()
                lb = RECOMMENDED_RE.sub("", labels[b]).strip()
                if la and lb and similar(la, lb) >= SIMILARITY_LIMIT and not opposed(la, lb):
                    rep.error(
                        where,
                        f"options {a+1} and {b+1} are near-duplicates "
                        f"('{la}' / '{lb}') — collapse them or find the real fork",
                    )

    # --- headers should not repeat across the batch
    heads = [(q.get("header") or "").strip().lower() for q in questions if isinstance(q, dict)]
    dupes = {h for h in heads if h and heads.count(h) > 1}
    if dupes:
        rep.error("payload", f"repeated header(s): {', '.join(sorted(dupes))}")

    return rep


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("payload", help="JSON file, or - for stdin")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--strict", action="store_true", help="warnings fail too")
    args = ap.parse_args()

    try:
        raw = sys.stdin.read() if args.payload == "-" else open(args.payload).read()
        payload = json.loads(raw)
    except (OSError, json.JSONDecodeError) as e:
        print(f"could not read payload: {e}", file=sys.stderr)
        return 2

    if isinstance(payload, list):
        payload = {"questions": payload}

    rep = lint(payload)
    failed = bool(rep.errors) or (args.strict and bool(rep.warnings))

    if args.json:
        print(json.dumps({"ok": not failed, "errors": rep.errors, "warnings": rep.warnings}, indent=2))
    else:
        for e in rep.errors:
            print(f"ERROR  {e}")
        for w in rep.warnings:
            print(f"WARN   {w}")
        if not rep.errors and not rep.warnings:
            print("clean")
        elif not failed:
            print(f"\npassed with {len(rep.warnings)} warning(s)")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
