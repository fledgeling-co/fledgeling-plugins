#!/usr/bin/env python3
"""Append to, and read the tail of, a should-compact session log.

The log is append-only ON PURPOSE. Incremental summarisation decays measurably — SUMIE tops out
around F1 80.4% and falls with each pass, BooookScore records 82.4 coherence for incremental
updating against 90.8 for summarising chunks independently — so a log that rewrites itself becomes
a summary of a summary and, by the third pass, a generic recap. This script therefore has no
"rewrite" mode and no "compress the log" mode, and adding one would defeat the file's purpose.

Two sections, because they decay differently:

  FACTS      append-only, never pruned. Constraints, corrections, rejected approaches with their
             reasons, exact identifiers. The items a successor cannot re-derive.
  NARRATIVE  one line per run. Allowed to be lossy; it exists to show the shape of the session.

Usage
  session_log.py path --session <id>
  session_log.py append --session <id> --score 8 --verdict compact \
                 --boundary "planning→implementation" --note "plan written, no tool open" \
                 [--fact "CONSTRAINT: ..."] [--fact "REJECTED: ..."]
  session_log.py tail --session <id> [--narrative 12]

Reads and writes only under ~/.claude/should-compact (or $SHOULD_COMPACT_HOME). No network.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import pathlib
import re
import sys

FACTS_HEADER = "## FACTS"
NARRATIVE_HEADER = "## NARRATIVE"
_SAFE_SESSION = re.compile(r"[^A-Za-z0-9._-]")

# A single fact line is capped so one runaway paste cannot turn the log into the transcript it
# exists to replace. Long-form belongs in a file the log points at.
MAX_FACT_CHARS = 400
MAX_NOTE_CHARS = 200


def home() -> pathlib.Path:
    root = os.environ.get("SHOULD_COMPACT_HOME")
    return pathlib.Path(root) if root else pathlib.Path.home() / ".claude" / "should-compact"


def log_path(session: str) -> pathlib.Path:
    """One file per session. The id is sanitised because it reaches the filesystem."""
    safe = _SAFE_SESSION.sub("-", session).strip("-") or "unknown"
    return home() / f"{safe}.md"


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


def _ensure(path: pathlib.Path) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    seed = (
        f"# should-compact · session log\n\n"
        f"{FACTS_HEADER}\n<!-- append-only, never rewritten, never pruned -->\n\n"
        f"{NARRATIVE_HEADER}\n"
    )
    path.write_text(seed, encoding="utf-8")
    return seed


def _clip(text: str, limit: int) -> str:
    text = " ".join(text.split())
    return text if len(text) <= limit else text[: limit - 1] + "…"


def append(session: str, score: int, verdict: str, boundary: str | None,
           note: str, facts: list[str]) -> pathlib.Path:
    path = log_path(session)
    body = _ensure(path)

    # Facts go under FACTS, in order, and duplicates are dropped — a fact restated every run would
    # crowd out the ones stated once, which are exactly the ones worth keeping.
    existing = set()
    for line in body.splitlines():
        if line.startswith("- "):
            existing.add(line[2:].strip())

    new_facts = []
    for fact in facts:
        clipped = _clip(fact, MAX_FACT_CHARS)
        if clipped and clipped not in existing:
            new_facts.append(f"- {clipped}")
            existing.add(clipped)

    if new_facts:
        idx = body.index(NARRATIVE_HEADER)
        body = body[:idx].rstrip("\n") + "\n" + "\n".join(new_facts) + "\n\n" + body[idx:]

    where = f" · {boundary}" if boundary else ""
    line = f"- {_now()} · {score}/10 · {verdict}{where} · {_clip(note, MAX_NOTE_CHARS)}"
    body = body.rstrip("\n") + "\n" + line + "\n"

    path.write_text(body, encoding="utf-8")
    return path


def tail(session: str, narrative: int) -> str:
    """Everything in FACTS, plus the last N narrative lines. `narrative=0` means FACTS only.

    FACTS is never truncated: it is the tier whose whole value is that it survives. Truncating it
    to save tokens would reintroduce the loss the two-tier split exists to prevent.

    Returns "" when FACTS holds nothing and no narrative was asked for — an empty answer, not an
    empty-looking header. The hook feeds this straight into a summarisation prompt, and a block of
    headings with no content under them reads to the model as an instruction it cannot follow.
    """
    path = log_path(session)
    if not path.exists():
        return f"(no log yet at {path})"
    body = path.read_text(encoding="utf-8")
    if NARRATIVE_HEADER not in body:
        return body
    head, _, rest = body.partition(NARRATIVE_HEADER)

    facts = [ln for ln in head.splitlines() if ln.startswith("- ")]
    lines = [ln for ln in rest.splitlines() if ln.startswith("- ")]
    kept = lines[-narrative:] if narrative > 0 else []

    if not facts and not kept:
        return ""
    out = head.rstrip()
    if kept:
        out += "\n\n" + NARRATIVE_HEADER + "\n" + "\n".join(kept)
    return out + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = p.add_subparsers(dest="cmd", required=True)

    q = sub.add_parser("path")
    q.add_argument("--session", required=True)

    a = sub.add_parser("append")
    a.add_argument("--session", required=True)
    a.add_argument("--score", type=int, required=True, choices=range(0, 11))
    a.add_argument("--verdict", required=True, choices=["compact", "wait", "hold"])
    a.add_argument("--boundary", default=None)
    a.add_argument("--note", default="")
    a.add_argument("--fact", action="append", default=[])

    t = sub.add_parser("tail")
    t.add_argument("--session", required=True)
    t.add_argument("--narrative", type=int, default=12)

    args = p.parse_args()
    if args.cmd == "path":
        print(log_path(args.session))
    elif args.cmd == "append":
        print(append(args.session, args.score, args.verdict, args.boundary,
                     args.note, args.fact))
    else:
        sys.stdout.write(tail(args.session, args.narrative))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
