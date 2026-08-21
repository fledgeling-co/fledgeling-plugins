#!/usr/bin/env python3
"""Turn a dead subagent's transcript into a session you can resume.

A workflow or task subagent does not get a session of its own. Its transcript is a
sidechain filed under the parent session:

    <project>/<PARENT-SESSION>/subagents/workflows/<runId>/agent-<agentId>.jsonl
    <project>/<PARENT-SESSION>/subagents/agent-<agentId>.jsonl

Every line carries `isSidechain: true`, an `agentId`, and the *parent's* `sessionId`. It is
otherwise a well-formed transcript, so rewriting those three fields and filing the copy
where `--resume` looks for a session makes the agent's whole accumulated context — the
files it read, the commands it ran, what it had concluded — resumable as a first-class
session.

Measured on 2026-08-21 against Claude Code 2.1.238: a promoted 95-line workflow-agent
transcript resumed and, asked from memory with no tools, named the item it had been working
on, its branch, and a specific finding it had already closed. That is the whole point. A
replacement agent started from the same prompt has none of it and repeats the work.

The copy is written to the project directory for `--cwd`, because `claude --resume` resolves
a session id inside the project directory of the working directory it is run from.

The original is never touched, so a second attempt is always possible.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path


def project_slug(path: str) -> str:
    """Claude Code's project-directory name for a filesystem path.

    It is the absolute path with every character that is not a letter, digit or hyphen
    replaced by a hyphen, which is why `/Users/me/Dev/app` becomes `-Users-me-Dev-app`.
    """
    return re.sub(r"[^A-Za-z0-9-]", "-", os.path.abspath(os.path.expanduser(path)))


def read_jsonl(p: Path) -> list[dict]:
    out = []
    for line in p.read_text(errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            out.append(json.loads(line))
        except Exception:
            continue
    return out


def promote(src: Path, cwd: str, claude_home: Path, session_id: str | None = None,
            quiet_seconds: int = 60) -> dict:
    if not src.is_file():
        raise SystemExit(f"no transcript at {src}")

    # A transcript still being appended belongs to a run that is still going. Promoting it
    # would put a second agent on the same work, which is the one outcome worth refusing.
    age = time.time() - src.stat().st_mtime
    if age < quiet_seconds:
        raise SystemExit(
            f"refusing: {src.name} was written {int(age)}s ago and may still be live "
            f"(needs {quiet_seconds}s of quiet; pass --force if you are certain)"
        )

    entries = read_jsonl(src)
    if not entries:
        raise SystemExit(f"{src} holds no parsable entries")

    new_id = session_id or str(uuid.uuid4())
    parents = {e.get("sessionId") for e in entries if e.get("sessionId")}
    agents = {e.get("agentId") for e in entries if e.get("agentId")}

    for e in entries:
        e["sessionId"] = new_id
        e.pop("isSidechain", None)
        e.pop("agentId", None)

    proj = claude_home / "projects" / project_slug(cwd)
    proj.mkdir(parents=True, exist_ok=True)
    dst = proj / f"{new_id}.jsonl"
    dst.write_text("\n".join(json.dumps(e) for e in entries) + "\n")

    return {
        "session_id": new_id,
        "transcript": str(dst),
        "entries": len(entries),
        "from": str(src),
        "parent_sessions": sorted(x for x in parents if x),
        "agent_ids": sorted(x for x in agents if x),
        "cwd": os.path.abspath(os.path.expanduser(cwd)),
        "resume_command": (
            f"cd {os.path.abspath(os.path.expanduser(cwd))} && "
            f"claude --dangerously-skip-permissions --resume {new_id}"
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("transcript", help="path to an agent-<id>.jsonl sidechain transcript")
    ap.add_argument("--cwd", required=True,
                    help="working directory the resumed session should run in "
                         "(use the one from the agent's own transcript)")
    ap.add_argument("--session-id", help="use this uuid instead of generating one")
    ap.add_argument("--claude-home", default=str(Path.home() / ".claude"))
    ap.add_argument("--force", action="store_true",
                    help="promote even if the transcript was written seconds ago")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    info = promote(
        Path(args.transcript).expanduser(),
        args.cwd,
        Path(args.claude_home).expanduser(),
        args.session_id,
        quiet_seconds=0 if args.force else 60,
    )
    if args.json:
        json.dump(info, sys.stdout, indent=1)
        print()
    else:
        print(f"promoted {info['entries']} entries from {Path(info['from']).name}")
        print(f"  parent session  {', '.join(info['parent_sessions']) or 'unknown'}")
        print(f"  agent id        {', '.join(info['agent_ids']) or 'unknown'}")
        print(f"  new session     {info['session_id']}")
        print(f"  written to      {info['transcript']}")
        print(f"\n{info['resume_command']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
