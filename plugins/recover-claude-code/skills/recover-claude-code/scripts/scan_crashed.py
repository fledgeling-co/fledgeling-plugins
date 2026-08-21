#!/usr/bin/env python3
"""Find Claude Code sessions that stopped without exiting, and what they left unfinished.

Read-only, stdlib only. Nothing here writes, resumes, or opens anything.

Liveness comes from the session registry rather than a process-table guess:

    ~/.claude/sessions/<PID>.json
      {"pid":.., "sessionId":.., "cwd":.., "procStart":.., "name":.., "status":.., "updatedAt":..}

A session is LIVE when its id appears there under a pid that is still running and still
belongs to Claude Code. Everything else with recent transcript activity is a recovery
candidate. That direction matters: the expensive mistake is calling a live session dead and
resuming it twice, so liveness is asserted from positive evidence and absence is what makes
a candidate.

Per candidate it reports the interrupted work, which lives in three places:

    <project>/<SESSION>.jsonl                              the session transcript
    <project>/<SESSION>/subagents/workflows/<runId>/       journal + one file per agent
    <project>/<SESSION>/workflows/scripts/<name>-<runId>.js  the script, to resume with

The script and the journal are filed under *different* project directories whenever a
session works outside the directory it started in, so the script is found by searching
every project directory for the run id rather than by joining paths onto the journal's.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

def _default_root() -> Path:
    return Path(os.environ.get("RCC_CLAUDE_HOME") or (Path.home() / ".claude"))


PROJECTS = _default_root() / "projects"
REGISTRY = _default_root() / "sessions"


def set_root(root: Path) -> None:
    """Point the scan at a different .claude directory.

    The live machine cannot exercise the detection path on demand — you would have to
    crash a terminal to get a stopped session with work owed — so the golden fixture in
    tests/ supplies one instead, and every path here is resolved through these two globals
    so the fixture is scanned by exactly the code that scans the real thing.
    """
    global PROJECTS, REGISTRY, _SCRIPT_INDEX
    PROJECTS = root / "projects"
    REGISTRY = root / "sessions"
    _SCRIPT_INDEX = None

# A transcript written this recently is treated as live even with no registry entry, so a
# session that is mid-write while the registry is being rewritten is never called dead.
FRESH_WRITE_SECONDS = 120

ITEM_RE = re.compile(r"\b([A-Z]{2,10}-\d{3,4})\b")


# ---------------------------------------------------------------- liveness

def _running_pids() -> dict[int, str]:
    """pid -> command name, for every process this user can see."""
    try:
        out = subprocess.run(
            ["ps", "-axo", "pid=,comm="], capture_output=True, text=True, timeout=15
        ).stdout
    except Exception:
        return {}
    pids = {}
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        pid, _, rest = line.partition(" ")
        try:
            pids[int(pid)] = rest.strip()
        except ValueError:
            continue
    return pids


def live_sessions() -> dict[str, dict]:
    """sessionId -> registry record, for sessions whose process is genuinely still there.

    The guard against a recycled pid vouching for a dead session is the command name, not
    the start time: the registry file is itself named `<pid>.json`, so a reused pid
    overwrites the record rather than inheriting it, and all that is left to rule out is a
    pid that now belongs to something that is not Claude Code. Comparing `procStart`
    against `ps lstart` looks stricter and is not — the two are formatted differently and
    sit in different time zones, so the comparison fails for every live session and the
    whole registry reads as dead.
    """
    pids = _running_pids()
    # A fixture cannot own real pids. When it declares which of its records are live, that
    # declaration stands in for the process table and the rest of the logic is unchanged.
    declared = os.environ.get("RCC_FAKE_LIVE_PIDS")
    if declared:
        pids = {int(x): "claude" for x in declared.split(",") if x.strip().isdigit()}
    live: dict[str, dict] = {}
    for f in REGISTRY.glob("*.json"):
        try:
            rec = json.loads(f.read_text())
        except Exception:
            continue
        sid, pid = rec.get("sessionId"), rec.get("pid")
        if not sid or not isinstance(pid, int) or pid not in pids:
            continue
        if "claude" not in pids[pid].lower():
            continue
        rec["_registryFile"] = str(f)
        live[sid] = rec
    return live


# ---------------------------------------------------------------- transcripts

def _tail_entries(path: Path, n: int = 40) -> list[dict]:
    """Last n parsable JSON lines. Reads the tail only, so a 120MB transcript is cheap."""
    try:
        size = path.stat().st_size
        with path.open("rb") as fh:
            fh.seek(max(0, size - 512 * 1024))
            chunk = fh.read()
    except OSError:
        return []
    lines = chunk.split(b"\n")[1:] if size > 512 * 1024 else chunk.split(b"\n")
    out = []
    for raw in lines[-n * 3 :]:
        if not raw.strip():
            continue
        try:
            out.append(json.loads(raw))
        except Exception:
            continue
    return out[-n:]


def _first_entry(path: Path) -> dict | None:
    try:
        with path.open("r", errors="replace") as fh:
            for line in fh:
                if line.strip():
                    return json.loads(line)
    except Exception:
        return None
    return None


def transcript_shape(entries: list[dict]) -> dict:
    """Did this transcript stop mid-turn, and what was in flight when it did?

    An assistant turn whose tool_use ids are not all answered by a later tool_result is
    the shape a crash leaves. Claude Code classifies that as an interrupted turn on
    resume and auto-submits a continue prompt, which is the behaviour a recovery has to
    get in front of.
    """
    pending: dict[str, str] = {}
    answered: set[str] = set()
    last_role = None
    for e in entries:
        t = e.get("type")
        if t in ("user", "assistant"):
            last_role = t
        msg = e.get("message") or {}
        content = msg.get("content")
        if not isinstance(content, list):
            continue
        for b in content:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "tool_use":
                pending[b.get("id", "")] = b.get("name", "?")
            elif b.get("type") == "tool_result":
                answered.add(b.get("tool_use_id", ""))
    unanswered = {k: v for k, v in pending.items() if k and k not in answered}
    return {
        "mid_turn": bool(unanswered),
        "unanswered_tools": sorted(set(unanswered.values())),
        "last_role": last_role,
    }


# ---------------------------------------------------------------- workflow runs

_SCRIPT_INDEX: dict[str, str] | None = None
_RUN_ID_RE = re.compile(r"-(wf_[0-9a-f-]{8,})\.js$")


def _script_index() -> dict[str, str]:
    """run id -> persisted script path, built in one pass over every project directory.

    Claude Code writes the script under the project directory of the *shell's* working
    directory at launch time, while the journal is filed under the project directory of
    the session's *original* cwd. Those differ for any session working in a subdirectory
    or a worktree, so the script cannot be found by joining onto the journal's path — it
    has to be looked up by run id across all of them. Indexing once keeps that to a single
    glob instead of one per run, which matters when the projects directory holds tens of
    thousands of entries.
    """
    global _SCRIPT_INDEX
    if _SCRIPT_INDEX is None:
        _SCRIPT_INDEX = {}
        for p in glob.iglob(str(PROJECTS / "*" / "*" / "workflows" / "scripts" / "*.js")):
            m = _RUN_ID_RE.search(p)
            if not m:
                continue
            prev = _SCRIPT_INDEX.get(m.group(1))
            if prev is None or _mtime(Path(p)) > _mtime(Path(prev)):
                _SCRIPT_INDEX[m.group(1)] = p
    return _SCRIPT_INDEX


def _script_for_run(run_id: str) -> str | None:
    return _script_index().get(run_id)


def _journal(run_dir: Path) -> dict:
    started: list[tuple[str, str]] = []
    results: set[str] = set()
    for line in _read_lines(run_dir / "journal.jsonl"):
        try:
            e = json.loads(line)
        except Exception:
            continue
        if e.get("type") == "started":
            started.append((e.get("key", ""), e.get("agentId", "")))
        elif e.get("type") == "result":
            results.add(e.get("key", ""))
    keys = list(dict.fromkeys(k for k, _ in started))
    pending = [k for k in keys if k not in results]
    return {
        "started_attempts": len(started),
        "distinct_calls": len(keys),
        "results": len(results),
        "pending_keys": pending,
        "pending_agents": [a for k, a in started if k in pending],
    }


def _read_lines(p: Path) -> list[str]:
    try:
        return p.read_text(errors="replace").splitlines()
    except OSError:
        return []


def _agent_state(path: Path, now: float) -> dict:
    entries = _tail_entries(path, 30)
    first = _first_entry(path)
    prompt = ""
    if first:
        c = (first.get("message") or {}).get("content")
        prompt = c if isinstance(c, str) else json.dumps(c)[:4000]
    shape = transcript_shape(entries)
    # An API error is only believed when it is how the transcript actually ends. Matching
    # the phrase anywhere turns an agent that merely *discussed* rate limits into a
    # failure, which is how one recovery came to record a usage limit that never happened.
    err = None
    for e in reversed(entries[-6:]):
        blob = json.dumps(e.get("message") or {})
        m = re.search(r"API Error[^\"\\]{0,140}", blob)
        if m:
            err = m.group(0)
            break
    try:
        st = path.stat()
        lines = sum(1 for _ in path.open("rb"))
    except OSError:
        st, lines = None, 0
    return {
        "agent_id": path.stem.replace("agent-", ""),
        "transcript": str(path),
        "lines": lines,
        "mtime": st.st_mtime if st else 0,
        "quiet_for": round(now - st.st_mtime) if st else -1,
        "item": (ITEM_RE.search(prompt).group(1) if ITEM_RE.search(prompt) else None),
        "prompt_head": " ".join(prompt.split())[:160],
        "mid_turn": shape["mid_turn"],
        "unanswered_tools": shape["unanswered_tools"],
        "terminal_error": err,
    }


def _cwd_from_file(transcript: Path) -> str | None:
    """Last working directory recorded anywhere in the transcript.

    The tail-entries pass misses a session whose final entries carry no cwd at all — one
    ending in a run of queue operations recorded none on 2026-08-22, and the recovery would
    have run `cd None`. Deriving the path from the project directory name is not a
    substitute: that name is the cwd with separators replaced, so it is ambiguous for any
    path containing a dash, which `/Users/…/Dev/mcp-router` does. This reads the value the
    session actually wrote, scanning the last megabyte so the cost does not grow with the
    length of a long session.
    """
    try:
        size = transcript.stat().st_size
        with transcript.open("rb") as fh:
            fh.seek(max(0, size - 1_000_000))
            blob = fh.read().decode("utf-8", "replace")
    except OSError:
        return None
    hits = re.findall(r'"cwd"\s*:\s*"((?:[^"\\]|\\.)*)"', blob)
    for raw in reversed(hits):
        try:
            path = json.loads(f'"{raw}"')
        except ValueError:
            continue
        if os.path.isdir(path):
            return path
    return None


def workflow_runs(project: Path, session: str, now: float) -> list[dict]:
    base = project / session / "subagents" / "workflows"
    runs = []
    for run_dir in sorted(base.glob("wf_*")):
        if not run_dir.is_dir():
            continue
        j = _journal(run_dir)
        agents = [_agent_state(p, now) for p in sorted(run_dir.glob("agent-*.jsonl"))]
        newest = max([a["mtime"] for a in agents] + [_mtime(run_dir / "journal.jsonl")])
        snap = project / session / "workflows" / f"{run_dir.name}.json"
        runs.append(
            {
                "run_id": run_dir.name,
                "dir": str(run_dir),
                "journal": j,
                "agents": agents,
                "script_path": _script_for_run(run_dir.name),
                "snapshot": str(snap) if snap.exists() else None,
                "newest_write": newest,
                "quiet_for": round(now - newest) if newest else -1,
                # Unfinished = the journal is still owed a result for a call that started.
                "unfinished": bool(j["pending_keys"]),
                "resumable_prefix": j["results"],
            }
        )
    return runs


def loose_subagents(project: Path, session: str, now: float) -> list[dict]:
    """Task-tool subagents, which sit beside the workflow directory rather than in it."""
    base = project / session / "subagents"
    return [_agent_state(p, now) for p in sorted(base.glob("agent-*.jsonl"))]


def _mtime(p: Path) -> float:
    try:
        return p.stat().st_mtime
    except OSError:
        return 0.0


# ---------------------------------------------------------------- assembly

def scan(minutes: int, project_filter: str | None) -> dict:
    now = time.time()
    cutoff = now - minutes * 60
    live = live_sessions()
    sessions = []

    for transcript in PROJECTS.glob("*/*.jsonl"):
        project = transcript.parent
        if project_filter and project_filter not in project.name:
            continue
        st = _mtime(transcript)
        if st < cutoff:
            continue
        sid = transcript.stem
        reg = live.get(sid)
        fresh = (now - st) < FRESH_WRITE_SECONDS
        entries = _tail_entries(transcript, 40)
        shape = transcript_shape(entries)
        cwd = None
        for e in reversed(entries):
            if e.get("cwd"):
                cwd = e["cwd"]
                break
        if cwd is None:
            cwd = _cwd_from_file(transcript)
        runs = workflow_runs(project, sid, now)
        loose = loose_subagents(project, sid, now)
        state = "LIVE" if reg else ("WRITING" if fresh else "STOPPED")
        sessions.append(
            {
                "session_id": sid,
                "project": project.name,
                "transcript": str(transcript),
                "cwd": (reg or {}).get("cwd") or cwd,
                "name": (reg or {}).get("name"),
                "state": state,
                "pid": (reg or {}).get("pid"),
                "quiet_for": round(now - st),
                "mid_turn": shape["mid_turn"],
                "unanswered_tools": shape["unanswered_tools"],
                "workflow_runs": runs,
                "loose_subagents": loose,
                "unfinished_runs": [r for r in runs if r["unfinished"]],
            }
        )

    sessions.sort(key=lambda s: (s["state"] != "STOPPED", -len(s["unfinished_runs"]), s["project"]))
    return {
        "scanned_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "window_minutes": minutes,
        "live_registry_entries": len(live),
        "sessions": sessions,
    }


def report(data: dict) -> None:
    stopped = [s for s in data["sessions"] if s["state"] == "STOPPED"]
    live = [s for s in data["sessions"] if s["state"] != "STOPPED"]
    # A stopped session with nothing owed and no interrupted turn needs no recovery: it is
    # a session someone finished with. Separating those keeps the report to what is
    # actionable, because a list where most rows need no action trains the reader to skim.
    actionable = [s for s in stopped if s["unfinished_runs"] or s["mid_turn"]
                  or any(a["mid_turn"] for a in s["loose_subagents"])]
    quiet = [s for s in stopped if s not in actionable]

    print(f"scanned {data['scanned_at']} · window {data['window_minutes']}m · "
          f"{len(data['sessions'])} sessions touched · "
          f"{len(actionable)} to recover, {len(quiet)} stopped cleanly, {len(live)} live")

    if not actionable:
        print("\nNothing to recover: no stopped session is owed a result or was cut mid-turn.")
    for s in actionable:
        print("\n" + "=" * 78)
        print(f"{s['name'] or s['session_id'][:8]}   {s['session_id']}")
        print(f"  project    {s['project']}")
        print(f"  cwd        {s['cwd']}")
        print(f"  quiet for  {s['quiet_for']}s")
        if s["mid_turn"]:
            print(f"  cut mid-turn, unanswered: {', '.join(s['unanswered_tools']) or 'unknown'}")
            print("             resuming this auto-submits a continue prompt")
        for r in s["unfinished_runs"]:
            j = r["journal"]
            print(f"  run {r['run_id']}  {j['results']}/{j['distinct_calls']} done, "
                  f"{len(j['pending_keys'])} owed  (quiet {r['quiet_for']}s)")
            print(f"    script   {r['script_path'] or 'NOT FOUND ON DISK'}")
            for a in r["agents"]:
                flag = "mid-tool" if a["mid_turn"] else ("error" if a["terminal_error"] else "ended")
                print(f"    {a['item'] or a['agent_id'][:12]:<14} {a['lines']:>5} lines  {flag}")
                if a["terminal_error"]:
                    print(f"      {a['terminal_error']}")
        done_runs = [r for r in s["workflow_runs"] if not r["unfinished"]]
        if done_runs:
            print(f"  ({len(done_runs)} completed run(s) here, nothing owed)")
        mid = [a for a in s["loose_subagents"] if a["mid_turn"]]
        if mid:
            print(f"  {len(mid)} task subagent(s) stopped mid-tool:")
            for a in mid:
                print(f"    {a['item'] or a['agent_id'][:12]:<14} {a['lines']:>5} lines")

    if quiet:
        print("\n" + "-" * 78)
        print(f"stopped cleanly, nothing owed: "
              f"{', '.join((s['name'] or s['session_id'][:8]) for s in quiet)}")

    if live:
        print("\n" + "-" * 78)
        print("LIVE — do not resume, do not relaunch their runs:")
        for s in live:
            tag = s["state"]
            print(f"  {s['name'] or s['session_id'][:8]:<24} pid {str(s['pid'] or '?'):<8} "
                  f"{tag:<8} {s['cwd']}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--minutes", type=int, default=60, help="activity window (default 60)")
    ap.add_argument("--project", help="substring filter on the project directory name")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--root", help="a .claude directory to scan instead of ~/.claude")
    args = ap.parse_args()

    if args.root:
        set_root(Path(args.root).expanduser())

    if not PROJECTS.is_dir():
        print(f"no project directory at {PROJECTS}", file=sys.stderr)
        return 2
    data = scan(args.minutes, args.project)
    if args.json:
        json.dump(data, sys.stdout, indent=1)
        print()
    else:
        report(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
