#!/usr/bin/env python3
"""List, and optionally stop, Claude Code sessions that outlived their terminal.

A terminal dying does not kill the sessions inside it. Measured on 2026-08-22: a Ghostty
crash took 22 sessions off the screen and four of them were still running twenty minutes
later, one of them mid-run with a live `caffeinate` child it had spawned to keep the machine
awake. Recovering on top of those gives two processes appending to one transcript and two
agents on one worktree, which is the one irreversible mistake this tooling can make.

An orphan is a session in `~/.claude/sessions/<PID>.json` whose pid is alive and which holds
no controlling terminal. That test is the one that works: parentage does not separate them,
because a session in a healthy Ghostty tab is parented to `login` and so is every other tab,
and "not in my own process tree" would condemn every session but the caller's. A session
attached to a tab has a tty; one whose terminal died, or that was started as a background
process, reports `??`. The calling session is excluded by ancestry as well, belt and braces.

Read-only by default. `--kill` sends SIGTERM, which lets each session flush its transcript;
a transcript that is still being written is what makes the recovery brief accurate.
"""
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

REGISTRY = Path.home() / ".claude" / "sessions"


def ps_field(pid: int, fmt: str) -> str:
    r = subprocess.run(["ps", "-o", f"{fmt}=", "-p", str(pid)], capture_output=True, text=True)
    return r.stdout.strip()


def alive(pid: int) -> bool:
    return bool(ps_field(pid, "pid"))


def ancestry(pid: int) -> list[int]:
    """Every pid from here up to init, so the caller can never target itself."""
    chain, seen = [], set()
    while pid and pid > 1 and pid not in seen:
        seen.add(pid)
        chain.append(pid)
        try:
            pid = int(ps_field(pid, "ppid") or 0)
        except ValueError:
            break
    return chain


def sessions() -> list[dict]:
    out = []
    for f in sorted(REGISTRY.glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except (OSError, ValueError):
            continue
        pid = d.get("pid")
        if not pid or not alive(int(pid)):
            continue
        pid = int(pid)
        out.append({
            "pid": pid,
            "session_id": d.get("sessionId"),
            "name": d.get("name"),
            "status": d.get("status"),
            "cwd": d.get("cwd"),
            "ppid": ps_field(pid, "ppid"),
            "tty": ps_field(pid, "tty"),
            "etime": ps_field(pid, "etime"),
            "command": ps_field(pid, "command")[:60],
            "registry": str(f),
        })
    return out


def transcript_lines(session_id: str) -> int:
    """How much conversation a session actually holds.

    A supervisor that keeps a warm pool registers sessions that were never used. They look
    exactly like a crashed session in the registry and have no transcript at all, so this
    separates "someone's work is still running" from "a pool slot is sitting ready".
    """
    if not session_id:
        return -1
    hits = list((Path.home() / ".claude" / "projects").glob(f"*/{session_id}.jsonl"))
    if not hits:
        return 0
    try:
        with hits[0].open("rb") as fh:
            return sum(1 for _ in fh)
    except OSError:
        return -1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--kill", action="store_true",
                    help="send SIGTERM to the orphans (default: list only)")
    ap.add_argument("--force", action="store_true",
                    help="SIGKILL anything still alive after --wait")
    ap.add_argument("--wait", type=float, default=8.0,
                    help="seconds to wait for a terminated session to exit (default 8)")
    ap.add_argument("--all-detached", action="store_true",
                    help="also target detached sessions that are working. Claude Code runs "
                         "genuine background sessions without a terminal too, so by default "
                         "a busy one is listed and left alone.")
    ap.add_argument("--include-empty", action="store_true",
                    help="also target sessions with no transcript. These are usually a "
                         "supervisor's warm pool and come straight back; leaving them alone "
                         "costs nothing, because an idle session writes nothing.")
    args = ap.parse_args()

    mine = set(ancestry(os.getpid()))
    rows = sessions()
    orphans, kept = [], []
    for s in rows:
        s["lines"] = transcript_lines(s["session_id"])
        s["detached"] = s["tty"] in ("", "??")
        if s["pid"] in mine:
            s["why"] = "this session"
        elif not s["detached"]:
            s["why"] = f"attached to {s['tty']} — a live terminal tab"
        elif s["lines"] == 0 and not args.include_empty:
            s["why"] = "no transcript — a warm-pool slot, not crashed work"
        elif s["status"] == "busy" and not args.all_detached:
            s["why"] = "detached but working — pass --all-detached to stop it too"
        else:
            orphans.append(s)
            continue
        kept.append(s)

    for s in kept:
        print(f"  keep    {str(s['session_id'])[:8]}  pid {s['pid']:<7} {s['why']}")
    if not orphans:
        print("no orphaned sessions")
        return 0

    print(f"\n{len(orphans)} session(s) running with no terminal:")
    for s in orphans:
        print(f"  {str(s['session_id'])[:8]}  pid {s['pid']:<7} {str(s['status'] or '?'):<6} "
              f"{s['etime']:>10}  {s['lines']:>6} lines  {s['cwd']}")
        if s.get("name"):
            print(f"            {s['name']}")
    if not args.kill:
        print("\nlisting only. Re-run with --kill to stop them.")
        return 0

    for s in orphans:
        try:
            os.kill(s["pid"], signal.SIGTERM)
        except OSError as exc:
            print(f"  could not signal {s['pid']}: {exc}")
    deadline = time.time() + args.wait
    while time.time() < deadline and any(alive(s["pid"]) for s in orphans):
        time.sleep(0.5)

    survivors = [s for s in orphans if alive(s["pid"])]
    if survivors and args.force:
        for s in survivors:
            try:
                os.kill(s["pid"], signal.SIGKILL)
            except OSError:
                pass
        time.sleep(1.0)
        survivors = [s for s in orphans if alive(s["pid"])]

    for s in orphans:
        print(f"  {'STILL RUNNING' if alive(s['pid']) else 'exited      '}  "
              f"{str(s['session_id'])[:8]}  pid {s['pid']}")

    back = [s for s in sessions() if s["session_id"] in {o["session_id"] for o in orphans}]
    if back:
        print(f"\n{len(back)} came back under a new pid — something is supervising them. "
              f"Find it before killing again:")
        print("  ps -axo pid=,ppid=,command= | grep -iE 'relay|perch|supervis|daemon'")
    return 1 if survivors else 0


if __name__ == "__main__":
    raise SystemExit(main())
