#!/usr/bin/env python3
"""Board-triage ledger — one row per card, so a sweep survives the session.

A full board is hours of serial verification. The state has to be a file: a
resumed session reads the ledger and continues rather than restarting, and
"how far did it get" is answerable without reading a transcript.

Rows are written when a card is FINISHED. A half-written row is
indistinguishable from a finished one three hours later.

  board_ledger.py init <dir> --columns "A,B,C" [--map role=Column ...]
  board_ledger.py add <dir> --key K --column C [--title T]
  board_ledger.py next <dir>
  board_ledger.py record <dir> --key K --verdict V [--lane L] [--sha S]
                              [--landed C] [--requirements N] [--work-at W]
                              [--brief P] [--question Q] [--note N]
  board_ledger.py status <dir> [--json]
"""
import argparse, json, os, sys
from datetime import datetime, timezone

VERDICTS = {"done", "needs-work", "needs-info", "inconclusive", "blocked", "no-change"}
WORK_AT = {"merged", "unmerged-branch", "unpushed", "worktree", "absent", "unknown"}
LEDGER = "board-triage-ledger.json"


def path(d):
    return os.path.join(d, LEDGER)


def load(d):
    p = path(d)
    if not os.path.exists(p):
        sys.exit(f"no ledger at {p} — run `init` first")
    with open(p) as f:
        return json.load(f)


def save(d, data):
    with open(path(d), "w") as f:
        json.dump(data, f, indent=1)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def cmd_init(a):
    os.makedirs(a.dir, exist_ok=True)
    if os.path.exists(path(a.dir)) and not a.force:
        sys.exit(f"ledger already exists at {path(a.dir)} — pass --force to replace")
    mapping = {}
    for m in a.map or []:
        if "=" not in m:
            sys.exit(f"--map wants role=Column, got {m!r}")
        role, col = m.split("=", 1)
        mapping[role.strip()] = col.strip()
    save(a.dir, {
        "started": now(),
        "columns_in_scope": [c.strip() for c in a.columns.split(",") if c.strip()],
        "role_map": mapping,
        "rows": [],
    })
    print(f"ledger at {path(a.dir)}")


def cmd_add(a):
    data = load(a.dir)
    if any(r["key"] == a.key for r in data["rows"]):
        print(f"{a.key} already present")
        return
    data["rows"].append({
        "key": a.key, "title": a.title or "", "column_at_intake": a.column,
        "verdict": None, "lane": None, "sha": None, "landed": None,
        "requirements": None, "work_at": None, "brief": None,
        "question": None, "note": None, "finished": None,
    })
    save(a.dir, data)
    print(f"added {a.key}")


def cmd_next(a):
    data = load(a.dir)
    for r in data["rows"]:
        if r["verdict"] is None:
            print(json.dumps(r))
            return
    print("")  # empty: nothing left, and an empty line is easy to test for
    sys.exit(0)


def cmd_record(a):
    data = load(a.dir)
    row = next((r for r in data["rows"] if r["key"] == a.key), None)
    if row is None:
        sys.exit(f"{a.key} is not in the ledger — `add` it first")
    if a.verdict not in VERDICTS:
        sys.exit(f"verdict {a.verdict!r} not one of: {', '.join(sorted(VERDICTS))}")
    if a.work_at and a.work_at not in WORK_AT:
        sys.exit(f"--work-at {a.work_at!r} not one of: {', '.join(sorted(WORK_AT))}")

    # The rules that stop a row claiming more than it carries.
    if a.verdict == "done" and not (a.lane and a.sha):
        sys.exit("a `done` row needs both --lane (who graded it) and --sha (what was graded)")
    if a.verdict == "needs-info" and not a.question:
        sys.exit("a `needs-info` row needs --question: a card moved there with no "
                 "question is a card nobody can answer")
    if a.verdict == "inconclusive" and not a.note:
        sys.exit("an `inconclusive` row needs --note saying what could not be gathered")
    if a.verdict == "needs-work" and not a.brief:
        sys.exit("a `needs-work` row needs --brief pointing at the features-to-triage file")

    for k in ("verdict", "lane", "sha", "landed", "requirements", "work_at",
              "brief", "question", "note"):
        v = getattr(a, k if k != "work_at" else "work_at")
        if v is not None:
            row[k] = v
    row["finished"] = now()
    save(a.dir, data)
    print(f"{a.key}: {a.verdict}")


def cmd_status(a):
    data = load(a.dir)
    rows = data["rows"]
    counts = {}
    for r in rows:
        counts[r["verdict"] or "pending"] = counts.get(r["verdict"] or "pending", 0) + 1
    if a.json:
        print(json.dumps({"total": len(rows), "counts": counts}, indent=1))
        return
    done = len(rows) - counts.get("pending", 0)
    print(f"{done}/{len(rows)} cards finished")
    for k in sorted(counts):
        print(f"  {counts[k]:>3}  {k}")
    inconclusive = [r["key"] for r in rows if r["verdict"] == "inconclusive"]
    if inconclusive:
        print(f"\ninconclusive ({len(inconclusive)}) — these BLOCK, they are not passes:")
        for k in inconclusive:
            print(f"  {k}")


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    i = sub.add_parser("init"); i.add_argument("dir"); i.add_argument("--columns", required=True)
    i.add_argument("--map", action="append"); i.add_argument("--force", action="store_true")
    i.set_defaults(fn=cmd_init)

    ad = sub.add_parser("add"); ad.add_argument("dir"); ad.add_argument("--key", required=True)
    ad.add_argument("--column", required=True); ad.add_argument("--title")
    ad.set_defaults(fn=cmd_add)

    n = sub.add_parser("next"); n.add_argument("dir"); n.set_defaults(fn=cmd_next)

    r = sub.add_parser("record"); r.add_argument("dir"); r.add_argument("--key", required=True)
    r.add_argument("--verdict", required=True); r.add_argument("--lane"); r.add_argument("--sha")
    r.add_argument("--landed"); r.add_argument("--requirements", type=int)
    r.add_argument("--work-at", dest="work_at"); r.add_argument("--brief")
    r.add_argument("--question"); r.add_argument("--note"); r.set_defaults(fn=cmd_record)

    s = sub.add_parser("status"); s.add_argument("dir"); s.add_argument("--json", action="store_true")
    s.set_defaults(fn=cmd_status)

    a = p.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
