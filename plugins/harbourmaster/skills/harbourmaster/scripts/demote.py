#!/usr/bin/env python3
"""Deprioritise heavy work that was started around the wrapper, and undo it.

The wrapper governs what opts in. This governs what did not — which on a real
machine is most of it. It never kills anything and never signals anything: the
only verb is `taskpolicy`, which moves a process down the scheduler and can be
moved back.

Measured on Mac16,5 on 2026-08-22: a spinning process at 95.5 %CPU dropped to
13.3 %CPU under `taskpolicy -b -p`, and returned to 100.0 %CPU under
`taskpolicy -B -p`. Children inherit the demotion, so demoting a build's root
process reaches the compilers underneath it.

## What it will not touch, and why

- **Anything not owned by the invoking user.** Root and system processes are
  out of scope entirely; the machine's own housekeeping is not the problem.
- **`claude` and other agent runtimes, by default.** They are the thing issuing
  the work, and a demoted agent makes the whole session unresponsive while the
  builds it started carry on at full speed — the wrong end of the pipe. Pass
  `--include-agents` to override.
- **Anything already demoted by us.** Recorded so a 60-second cadence does not
  re-issue the same call forever.
- **Windowed/interactive processes**, by name, since demoting the UI is how a
  maintenance tool gets uninstalled.

## The hazard worth naming

Demotion can invert priorities: a low-priority process holding a lock that a
high-priority one waits on now holds it for longer. macOS mitigates this for
its own primitives and cannot for everything. The families below are compute,
not coordination, which is why the list is an allowlist rather than a
denylist — but the risk is real and is the reason nothing here is automatic
below `critical` pressure.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import berths  # noqa: E402
import ledger  # noqa: E402

STATE = berths.HOME / "demoted.json"

# Compute engines: heavy, restartable, and not holding the UI together.
DEMOTABLE = re.compile(
    r"(^|/)(rustc|cargo|swift-frontend|swiftc|xcodebuild|clang|cc1|ld|"
    r"esbuild|tsc|vitest|jest|webpack|rollup|turbo|next-server|"
    r"ninja|cmake|make|gradle|java|python3?|ruby|go|node)(\s|$)"
)
AGENTS = re.compile(r"(^|/)(claude|codex|agy|grok|cursor-agent|gemini)(\s|$)")
NEVER = re.compile(
    r"(WindowServer|loginwindow|Finder|Dock|SystemUIServer|launchd|kernel_task|"
    r"coreaudiod|bluetoothd|Terminal|iTerm|Ghostty|harbourmaster|taskpolicy)"
)


def load() -> dict:
    try:
        return json.loads(STATE.read_text())
    except (OSError, ValueError):
        return {}


def save(data: dict) -> None:
    berths.HOME.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2))
    tmp.replace(STATE)


def candidates(min_cpu: float, include_agents: bool) -> list[dict]:
    me = os.getuid()
    out = []
    raw = subprocess.run(
        ["ps", "-Axo", "pid=,uid=,pcpu=,command="],
        capture_output=True, text=True, timeout=20).stdout
    for line in raw.splitlines():
        parts = line.split(None, 3)
        if len(parts) < 4:
            continue
        pid, uid, pcpu, command = parts
        try:
            pid, uid, pcpu = int(pid), int(uid), float(pcpu)
        except ValueError:
            continue
        if uid != me or pid == os.getpid() or pcpu < min_cpu:
            continue
        if NEVER.search(command):
            continue
        if AGENTS.search(command) and not include_agents:
            continue
        if not (DEMOTABLE.search(command) or (include_agents and AGENTS.search(command))):
            continue
        out.append({"pid": pid, "pcpu": pcpu, "command": command[:160]})
    return sorted(out, key=lambda c: -c["pcpu"])


def apply(pids: list[int], flag: str) -> list[int]:
    """`-b` demotes, `-B` restores. A pid that has exited is not an error."""
    done = []
    for pid in pids:
        result = subprocess.run(["taskpolicy", flag, "-p", str(pid)],
                                capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            done.append(pid)
    return done


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="without this nothing is changed")
    parser.add_argument("--min-cpu", type=float, default=40.0)
    parser.add_argument("--max", type=int, default=8,
                        help="most processes to demote in one pass")
    parser.add_argument("--include-agents", action="store_true")
    parser.add_argument("--restore", action="store_true",
                        help="return everything we demoted to normal priority")
    args = parser.parse_args()

    state = load()
    demoted: dict[str, str] = state.get("demoted", {})

    if args.restore:
        pids = [int(p) for p in demoted]
        restored = apply(pids, "-B") if args.apply else []
        if args.apply:
            state["demoted"] = {}
            save(state)
            ledger.record({"kind": "restore", "detail": f"{len(restored)} processes"})
        print(json.dumps({"action": "restore", "candidates": len(pids),
                          "restored": len(restored), "applied": args.apply}, indent=2))
        return 0

    snap = berths.snapshot()
    pressure = snap["verdict"]["overall"]

    # Pressure has to be back to healthy before we hand priority back, not
    # merely off critical — otherwise the machine oscillates between demoting
    # and restoring the same processes every cadence.
    if pressure == "healthy" and demoted:
        pids = [int(p) for p in demoted]
        restored = apply(pids, "-B") if args.apply else []
        if args.apply:
            state["demoted"] = {}
            save(state)
            ledger.record({"kind": "restore", "detail":
                           f"{len(restored)} processes; pressure healthy"})
        print(json.dumps({"action": "auto-restore", "pressure": pressure,
                          "restored": len(restored), "applied": args.apply}, indent=2))
        return 0

    if pressure != "critical":
        print(json.dumps({"action": "none", "pressure": pressure,
                          "reason": "demotion is reserved for critical pressure"},
                         indent=2))
        return 0

    found = [c for c in candidates(args.min_cpu, args.include_agents)
             if str(c["pid"]) not in demoted][: args.max]
    applied = apply([c["pid"] for c in found], "-b") if args.apply else []

    if args.apply and applied:
        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        for pid in applied:
            demoted[str(pid)] = now
        state["demoted"] = demoted
        save(state)
        ledger.record({"kind": "demote", "detail":
                       f"{len(applied)} processes under critical pressure"})

    print(json.dumps({
        "action": "demote", "pressure": pressure, "applied": args.apply,
        "demoted_now": len(applied), "already_demoted": len(demoted),
        "candidates": [{"pid": c["pid"], "pcpu": c["pcpu"],
                        "command": c["command"][:70]} for c in found],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
