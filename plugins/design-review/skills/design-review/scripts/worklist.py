#!/usr/bin/env python3
"""
worklist.py — the coverage ledger, and the gate that reads it.

A review's two silent failure modes are covering a subset of the surfaces and
running a subset of the stages. Both produce a report indistinguishable from a
finished one. The ledger makes each an enumeration, and `check` refuses to
clear while any cell is open.

The count is fixed by `init` before capture and never shrinks silently. A
denominator set after the fact always equals its numerator.

Usage:
    python worklist.py init  <workdir> --surfaces /dashboard,/settings,/billing
    python worklist.py init  <workdir> --surfaces-file routes.txt
    python worklist.py set   <workdir> --surface /settings --stage states --value done
    python worklist.py set   <workdir> --surface /billing  --stage flow \\
                             --value "n/a: no task flow on this surface"
    python worklist.py check <workdir>            # exit 1 while any cell is open
    python worklist.py check <workdir> --json

Ledger lives at <workdir>/worklist.md — markdown so a human reads it and a
fresh session resumes from it.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Stages 2-8 of the pipeline. Each finds a defect class the others are blind to,
# which is why a partial stage set is a coverage gap rather than a shortcut.
STAGES = ["gates", "render", "states", "inventory", "craft", "flow", "system", "intent"]

OPEN = "open"
DONE = "done"
NA_PREFIX = "n/a"

HEADER_RE = re.compile(r"^\|\s*#\s*\|\s*Surface\s*\|", re.I)
ROW_RE = re.compile(r"^\|\s*(\d+)\s*\|(.+)\|\s*$")


def ledger_path(workdir: Path) -> Path:
    return workdir / "worklist.md"


def cell_state(value: str) -> str:
    """done | n/a | open. Anything unrecognised counts as open, deliberately —
    an ambiguous cell is not evidence that the work happened."""
    v = value.strip().lower()
    if v == DONE:
        return DONE
    if v.startswith(NA_PREFIX):
        return NA_PREFIX
    return OPEN


def render(surfaces: list[str], cells: dict[str, dict[str, str]], sample_note: str) -> str:
    widths = [max(len(s), 4) for s in STAGES]
    surf_w = max([len(s) for s in surfaces] + [7])

    lines = [
        "# Coverage ledger",
        "",
        "Written at stage 0, before capture. The surface count is a contract: it is",
        "the denominator in the report's Coverage block and in the verdict line.",
        "",
        "Cells are `done`, `n/a: <reason>`, or `open`. `check` exits 1 while any is",
        "open. Stopping short is declared with a resume point, never absorbed.",
        "",
    ]
    if sample_note:
        lines += [f"**Sample:** {sample_note}", ""]

    head = "| # | " + "Surface".ljust(surf_w) + " | " + " | ".join(
        s.ljust(w) for s, w in zip(STAGES, widths)) + " |"
    rule = "|---|" + "-" * (surf_w + 2) + "|" + "|".join(
        "-" * (w + 2) for w in widths) + "|"
    lines += [head, rule]

    for i, surf in enumerate(surfaces, 1):
        row = cells.get(surf, {})
        vals = [row.get(st, OPEN) for st in STAGES]
        lines.append(
            f"| {i} | " + surf.ljust(surf_w) + " | " + " | ".join(
                v.ljust(w) for v, w in zip(vals, widths)) + " |")

    return "\n".join(lines) + "\n"


def parse(workdir: Path) -> tuple[list[str], dict[str, dict[str, str]], str]:
    p = ledger_path(workdir)
    if not p.exists():
        sys.exit(f"No ledger at {p}. Run `worklist.py init` at stage 0, before capturing.")

    surfaces: list[str] = []
    cells: dict[str, dict[str, str]] = {}
    sample = ""
    stage_order = STAGES

    for line in p.read_text().splitlines():
        if line.startswith("**Sample:**"):
            sample = line.split("**Sample:**", 1)[1].strip()
            continue
        if HEADER_RE.match(line):
            parts = [c.strip() for c in line.strip().strip("|").split("|")]
            stage_order = [c.lower() for c in parts[2:]]
            continue
        m = ROW_RE.match(line)
        if not m or set(m.group(2)) <= set("-| "):
            continue
        parts = [c.strip() for c in m.group(2).split("|")]
        if not parts:
            continue
        surf, values = parts[0], parts[1:]
        surfaces.append(surf)
        cells[surf] = {st: (values[i] if i < len(values) else OPEN)
                       for i, st in enumerate(stage_order)}

    if not surfaces:
        sys.exit(f"{p} has no surface rows. Re-run `init`.")
    return surfaces, cells, sample


def cmd_init(args) -> int:
    workdir = Path(args.workdir).resolve()
    workdir.mkdir(parents=True, exist_ok=True)

    if args.surfaces_file:
        raw = Path(args.surfaces_file).read_text().splitlines()
    else:
        raw = args.surfaces.split(",")
    surfaces = [s.strip() for s in raw if s.strip() and not s.strip().startswith("#")]
    if not surfaces:
        sys.exit("No surfaces given. The enumeration is the point — a review with no "
                 "worklist has no denominator.")

    p = ledger_path(workdir)
    if p.exists() and not args.force:
        sys.exit(f"{p} exists. Use --force to replace it — but shrinking a worklist "
                 f"mid-review is exactly the silent-narrowing failure this file prevents.")

    p.write_text(render(surfaces, {}, args.sample or ""))
    print(f"Wrote {p} — {len(surfaces)} surfaces x {len(STAGES)} stages "
          f"= {len(surfaces) * len(STAGES)} cells, all open.")
    if args.sample:
        print(f"Sample declared: {args.sample}")
    else:
        print("No sample declared: this is a full review of every surface listed.")
    return 0


def cmd_set(args) -> int:
    workdir = Path(args.workdir).resolve()
    surfaces, cells, sample = parse(workdir)

    if args.surface not in cells:
        sys.exit(f"'{args.surface}' is not on the worklist. Surfaces: {', '.join(surfaces)}\n"
                 f"Adding a surface mid-review is fine; do it with `init --force` and a "
                 f"complete list, so the denominator stays visible.")
    stages = STAGES if args.stage == "all" else [args.stage]
    for st in stages:
        if st not in STAGES:
            sys.exit(f"Unknown stage '{st}'. Stages: {', '.join(STAGES)}")
        cells[args.surface][st] = args.value

    ledger_path(workdir).write_text(render(surfaces, cells, sample))
    print(f"{args.surface}: {', '.join(stages)} -> {args.value}")
    return 0


def cmd_check(args) -> int:
    workdir = Path(args.workdir).resolve()
    surfaces, cells, sample = parse(workdir)

    open_cells: list[tuple[str, str]] = []
    counts = {DONE: 0, NA_PREFIX: 0, OPEN: 0}
    complete_surfaces = 0

    for surf in surfaces:
        row = cells[surf]
        states = {st: cell_state(row.get(st, OPEN)) for st in STAGES}
        for st, state in states.items():
            counts[state] += 1
            if state == OPEN:
                open_cells.append((surf, st))
        if all(s != OPEN for s in states.values()):
            complete_surfaces += 1

    total = len(surfaces) * len(STAGES)
    report = {
        "surfaces": len(surfaces),
        "surfacesComplete": complete_surfaces,
        "cells": total,
        "done": counts[DONE],
        "na": counts[NA_PREFIX],
        "open": counts[OPEN],
        "openCells": [{"surface": s, "stage": st} for s, st in open_cells],
        "sample": sample,
        "clear": not open_cells,
    }

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Surfaces: {complete_surfaces} of {len(surfaces)} complete")
        print(f"Cells:    {counts[DONE]} done · {counts[NA_PREFIX]} n/a · {counts[OPEN]} open "
              f"(of {total})")
        if sample:
            print(f"Sample:   {sample}")
        if open_cells:
            print("\nOpen:")
            by_surface: dict[str, list[str]] = {}
            for s, st in open_cells:
                by_surface.setdefault(s, []).append(st)
            for s, sts in by_surface.items():
                print(f"  {s}: {', '.join(sts)}")
            print(f"\nNot ready to report. Either finish these, or mark each `n/a: <reason>`,")
            print(f"or declare the stop: \"{complete_surfaces} of {len(surfaces)} surfaces "
                  f"reviewed, resuming at {complete_surfaces + 1}\" — in the reply, in the")
            print("verdict line, and in the Coverage block. Never silently.")
        else:
            print("\nEvery cell accounted for. The verdict line still carries the fraction: "
                  f"({len(surfaces)} of {len(surfaces)} surfaces, all stages).")

    return 1 if open_cells else 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Coverage ledger for a design review.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("init", help="Fix the worklist at stage 0, before capture.")
    i.add_argument("workdir")
    g = i.add_mutually_exclusive_group(required=True)
    g.add_argument("--surfaces", help="Comma-separated surfaces in scope.")
    g.add_argument("--surfaces-file", help="One surface per line; # comments ignored.")
    i.add_argument("--sample", help="Declare a deliberate sample: which, chosen how, "
                                    "and what it cannot speak for.")
    i.add_argument("--force", action="store_true", help="Replace an existing ledger.")
    i.set_defaults(fn=cmd_init)

    s = sub.add_parser("set", help="Mark a cell done or n/a.")
    s.add_argument("workdir")
    s.add_argument("--surface", required=True)
    s.add_argument("--stage", required=True, help=f"One of: {', '.join(STAGES)}, or 'all'.")
    s.add_argument("--value", required=True, help="done | n/a: <reason> | open")
    s.set_defaults(fn=cmd_set)

    c = sub.add_parser("check", help="Exit 1 while any cell is open.")
    c.add_argument("workdir")
    c.add_argument("--json", action="store_true")
    c.set_defaults(fn=cmd_check)

    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
