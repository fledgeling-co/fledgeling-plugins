#!/usr/bin/env python3
"""Record a finished agent's real result in a copy of a workflow's journal.

Why this exists. `Workflow({scriptPath, resumeFromRunId})` replays an `agent()` call from
cache when the journal already holds a `result` line for its key. The cache key is a
sha256 chain over (previous key, prompt, normalised opts), and the miss flag is sticky:
after the first miss nothing is consulted again, so replay is a prefix rather than a set.

An agent that was still running when the process died leaves a `started` line and no
`result`. On resume it is the first miss, so it re-runs from a blank slate — and every
later call re-runs too, including ones whose results are sitting on disk. For a run that
was ten agents deep that means re-doing work that is already committed.

Splicing closes that hole: finish the interrupted agent (promote its transcript with
promote_agent.py and let it run to a real conclusion), then write what it actually returned
into the journal under the key its own `started` line already recorded. The resumed run then
replays the whole prefix and moves on to the calls that never started.

Two rules make this safe rather than clever:

  - **The result must be real.** Distilling "what it looked like it achieved" from a partial
    transcript manufactures exactly the failure this family of tooling already suffers from:
    runs have reported items MERGED whose branches were tens of commits short of the
    integration branch. A journal is a record of what an agent said, and a forged line is a
    lie that every later decision is built on. This script will not invent one — you pass
    the text the finished agent returned.
  - **Never edit the original.** It writes into a copy of the run directory and prints the
    path, so the original journal stays exactly as the crash left it and a second attempt
    costs nothing.

Because the copy lives under a different session, the resumed run has to be launched from a
session whose id resolves to it — see the skill's SKILL.md for which session that is.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


def read_journal(p: Path) -> list[dict]:
    out = []
    for line in p.read_text(errors="replace").splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def owed_keys(entries: list[dict]) -> list[tuple[str, str]]:
    """(key, agentId) for each call that started and never returned, in start order."""
    started, done = [], set()
    for e in entries:
        if e.get("type") == "started":
            started.append((e.get("key", ""), e.get("agentId", "")))
        elif e.get("type") == "result":
            done.add(e.get("key", ""))
    seen, out = set(), []
    for k, a in started:
        if k and k not in done and k not in seen:
            seen.add(k)
            out.append((k, a))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("run_dir", help="the wf_<runId> directory holding journal.jsonl")
    ap.add_argument("--agent-id", help="which owed agent to record a result for")
    ap.add_argument("--result-file", help="file holding the text the finished agent returned")
    ap.add_argument("--dest", help="where to write the copy (default: alongside, .recovered)")
    ap.add_argument("--list", action="store_true", help="show what the journal is owed and stop")
    args = ap.parse_args()

    run = Path(args.run_dir).expanduser()
    journal = run / "journal.jsonl"
    if not journal.is_file():
        print(f"no journal at {journal}", file=sys.stderr)
        return 2

    entries = read_journal(journal)
    owed = owed_keys(entries)
    results = sum(1 for e in entries if e.get("type") == "result")

    if args.list or not (args.agent_id and args.result_file):
        print(f"{run.name}: {results} result(s) recorded, {len(owed)} owed")
        for k, a in owed:
            print(f"  agent {a}  key {k}")
        if not owed:
            print("  nothing owed: this run needs no splice")
        if not (args.agent_id and args.result_file):
            print("\npass --agent-id and --result-file to record one, "
                  "with the text the finished agent actually returned")
        return 0

    match = [(k, a) for k, a in owed if a == args.agent_id]
    if not match:
        print(f"agent {args.agent_id} is not owed a result in this journal. Owed: "
              f"{', '.join(a for _, a in owed) or 'none'}", file=sys.stderr)
        return 1
    key, agent = match[0]

    text = Path(args.result_file).expanduser().read_text()
    if not text.strip():
        print("refusing: the result file is empty. A journal line has to carry what the "
              "agent returned, and an empty one is a forged success.", file=sys.stderr)
        return 1

    dest = Path(args.dest).expanduser() if args.dest else run.parent / f"{run.name}.recovered"
    if dest.exists():
        print(f"refusing: {dest} already exists — remove it or pass a different --dest",
              file=sys.stderr)
        return 1
    shutil.copytree(run, dest)

    with (dest / "journal.jsonl").open("a") as fh:
        fh.write(json.dumps({"type": "result", "key": key, "agentId": agent,
                             "result": text}) + "\n")

    print(f"recorded {len(text)} chars for agent {agent} (key {key})")
    print(f"  original untouched  {run}")
    print(f"  spliced copy        {dest}")
    print(f"\nThe copy has to sit at <project>/<SESSION>/subagents/workflows/{run.name} for "
          f"the session you resume from.\nSee SKILL.md — 'Relocating a run' — for the move "
          f"and which session id resolves it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
