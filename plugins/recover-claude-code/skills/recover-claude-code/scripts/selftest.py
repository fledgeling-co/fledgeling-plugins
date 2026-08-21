#!/usr/bin/env python3
"""Build a fixture .claude directory and assert the scan reads it correctly.

The live machine cannot exercise detection on demand: to get a stopped session with work
owed you would have to crash a terminal. So this writes a synthetic tree in the shapes
measured from a real crash (Ghostty died at 14:32:44 on 2026-08-21, taking eighteen
sessions and their in-flight workflow agents with it) and checks the scan against it.

Five properties, each of which was a real defect before it was a test:

  1. a stopped session owed a result is reported
  2. a session in the registry under a running pid is never reported, however quiet
  3. the persisted script is found when it sits under a *different* project directory
     than the journal, which is what happens whenever a session works in a worktree
  4. an agent that merely mentions a rate limit is not called failed; only one whose
     transcript actually ends in an API error is
  5. a stopped session with nothing owed is not dressed up as recoverable

Run: python3 scripts/selftest.py     (exit 0 all pass, 1 on any failure)
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCAN = HERE / "scan_crashed.py"


def w(path: Path, lines: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(x) for x in lines) + "\n")


def turn(role: str, text: str = "", tool: str | None = None, tool_id: str | None = None,
         result_for: str | None = None, cwd: str = "/Users/someone/Dev", sid: str = "",
         agent: str | None = None) -> dict:
    content: list[dict] = []
    if text:
        content.append({"type": "text", "text": text})
    if tool:
        content.append({"type": "tool_use", "id": tool_id, "name": tool, "input": {}})
    if result_for:
        content = [{"type": "tool_result", "tool_use_id": result_for, "content": "ok"}]
    e = {
        "type": role, "message": {"role": role, "content": content},
        "cwd": cwd, "sessionId": sid, "timestamp": "2026-08-21T04:32:00.000Z",
        "version": "2.1.238", "uuid": f"u{len(text)}{tool or ''}{result_for or ''}",
    }
    if agent:
        # A real subagent transcript is a sidechain under the parent session, so a fixture
        # that omits these does not exercise the two fields promotion has to strip.
        e["isSidechain"] = True
        e["agentId"] = agent
    return e


def build(root: Path) -> dict:
    """A fixture with one crashed session, one live session, one clean session."""
    projects = root / "projects"
    registry = root / "sessions"
    registry.mkdir(parents=True, exist_ok=True)

    crashed = "aaaaaaaa-1111-4111-8111-aaaaaaaaaaaa"
    alive = "bbbbbbbb-2222-4222-8222-bbbbbbbbbbbb"
    clean = "cccccccc-3333-4333-8333-cccccccccccc"

    # --- the crashed session: started in ~/Dev, working in a worktree ---------------
    home_proj = projects / "-Users-someone-Dev"
    w(home_proj / f"{crashed}.jsonl", [
        turn("user", "ship ORD-0081", cwd="/Users/someone/Dev", sid=crashed),
        turn("assistant", "dispatching", tool="Workflow", tool_id="t1",
             cwd="/Users/someone/Dev", sid=crashed),
        # no tool_result for t1: this is the mid-turn shape a crash leaves
    ])

    run = "wf_dead1234abc"
    run_dir = home_proj / crashed / "subagents" / "workflows" / run
    # two calls started, one returned: the journal is owed one result
    w(run_dir / "journal.jsonl", [
        {"type": "started", "key": "v2:aaa", "agentId": "a0001"},
        {"type": "result", "key": "v2:aaa", "agentId": "a0001", "result": "ORD-0080 done"},
        {"type": "started", "key": "v2:bbb", "agentId": "a0002"},
    ])
    w(run_dir / "agent-a0001.jsonl", [
        turn("user", "You are a runner for ORD-0080", sid=crashed, agent="a0001"),
        turn("assistant", "done", sid=crashed, agent="a0001"),
    ])
    # the agent that was mid-flight, and which *discusses* a rate limit without hitting one
    w(run_dir / "agent-a0002.jsonl", [
        turn("user", "You are a runner for ORD-0081. Note the codex lane is "
                     "rate-limited until 27 Aug, so use grok instead.",
             sid=crashed, agent="a0002"),
        turn("assistant", "reading the spec", tool="Read", tool_id="t9",
             sid=crashed, agent="a0002"),
    ])
    # the script lands under the *worktree's* project directory, not the journal's
    wt_proj = projects / "-Users-someone-Dev-orderly"
    sp = wt_proj / crashed / "workflows" / "scripts" / f"ord-0081-{run}.js"
    sp.parent.mkdir(parents=True, exist_ok=True)
    sp.write_text("export const meta = { name: 'ord-0081', description: 'x' }\n")

    # a second run in the same session that really did end in an API error
    run2 = "wf_dead5678def"
    run2_dir = home_proj / crashed / "subagents" / "workflows" / run2
    w(run2_dir / "journal.jsonl", [{"type": "started", "key": "v2:ccc", "agentId": "a0003"}])
    w(run2_dir / "agent-a0003.jsonl", [
        turn("user", "You are a verifier for ORD-0096", sid=crashed, agent="a0003"),
        turn("assistant", "API Error: Connection lost mid-response.",
             sid=crashed, agent="a0003"),
    ])

    # a third run that fully completed: it must not be listed as needing recovery
    run3 = "wf_done9999ghi"
    run3_dir = home_proj / crashed / "subagents" / "workflows" / run3
    w(run3_dir / "journal.jsonl", [
        {"type": "started", "key": "v2:eee", "agentId": "a0005"},
        {"type": "result", "key": "v2:eee", "agentId": "a0005", "result": "ORD-0079 merged"},
    ])
    w(run3_dir / "agent-a0005.jsonl", [
        turn("user", "You are a runner for ORD-0079", sid=crashed, agent="a0005"),
        turn("assistant", "merged", sid=crashed, agent="a0005"),
    ])

    # --- a live session, quiet for ages, which must never be touched ---------------
    live_proj = projects / "-Users-someone-Dev-perch"
    w(live_proj / f"{alive}.jsonl", [
        turn("user", "keep going", cwd="/Users/someone/Dev/perch", sid=alive),
        turn("assistant", "working", tool="Bash", tool_id="t5",
             cwd="/Users/someone/Dev/perch", sid=alive),
    ])
    lr = live_proj / alive / "subagents" / "workflows" / "wf_live0000aaa"
    w(lr / "journal.jsonl", [{"type": "started", "key": "v2:ddd", "agentId": "a0004"}])
    w(lr / "agent-a0004.jsonl", [
        turn("user", "live runner PER-0001", sid=alive, agent="a0004")])
    (registry / "42424.json").write_text(json.dumps({
        "pid": 42424, "sessionId": alive, "cwd": "/Users/someone/Dev/perch",
        "procStart": "Fri Aug 21 04:00:00 2026", "version": "2.1.238",
        "kind": "interactive", "name": "perch-live", "status": "busy",
        "updatedAt": int(time.time() * 1000),
    }))

    # --- a session that stopped cleanly: nothing owed, no interrupted turn ---------
    w(live_proj / f"{clean}.jsonl", [
        turn("user", "what changed?", cwd="/Users/someone/Dev/perch", sid=clean),
        turn("assistant", "two commits", cwd="/Users/someone/Dev/perch", sid=clean),
    ])

    # make every transcript look recently touched but past the fresh-write grace period
    stamp = time.time() - 400
    for p in projects.rglob("*.jsonl"):
        os.utime(p, (stamp, stamp))
    return {"crashed": crashed, "alive": alive, "clean": clean,
            "run": run, "run2": run2, "run3": run3, "script": str(sp)}


def run_scan(root: Path) -> dict:
    env = dict(os.environ, RCC_FAKE_LIVE_PIDS="42424")
    out = subprocess.run(
        [sys.executable, str(SCAN), "--root", str(root), "--minutes", "60", "--json"],
        capture_output=True, text=True, env=env, timeout=120,
    )
    if out.returncode != 0:
        raise SystemExit(f"scan failed: {out.stderr[:2000]}")
    return json.loads(out.stdout)


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="rcc-fixture-"))
    failures: list[str] = []
    try:
        ids = build(root)
        data = run_scan(root)
        by_id = {s["session_id"]: s for s in data["sessions"]}

        def check(name: str, ok: bool, detail: str = "") -> None:
            print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  — {detail}" if detail and not ok else ""))
            if not ok:
                failures.append(name)

        crashed = by_id.get(ids["crashed"])
        alive = by_id.get(ids["alive"])
        clean = by_id.get(ids["clean"])

        check("1. the crashed session is found and marked stopped",
              bool(crashed) and crashed["state"] == "STOPPED",
              f"state={crashed and crashed['state']}")
        check("1b. it is reported as cut mid-turn on an unanswered Workflow call",
              bool(crashed) and crashed["mid_turn"] and "Workflow" in crashed["unanswered_tools"],
              f"{crashed and crashed['unanswered_tools']}")
        check("1c. the two runs owed a result are listed, the completed one is not",
              bool(crashed) and {r["run_id"] for r in crashed["unfinished_runs"]}
              == {ids["run"], ids["run2"]}
              and len(crashed["workflow_runs"]) == 3,
              f"{crashed and [r['run_id'] for r in crashed['unfinished_runs']]}")

        check("2. the live session is never a recovery candidate",
              bool(alive) and alive["state"] == "LIVE" and alive["name"] == "perch-live",
              f"state={alive and alive['state']}")

        run = next((r for r in (crashed or {}).get("unfinished_runs", [])
                    if r["run_id"] == ids["run"]), None)
        check("3. the script is found under a different project dir than the journal",
              bool(run) and run["script_path"] == ids["script"],
              f"{run and run['script_path']}")
        check("3b. the resumable prefix is counted from the journal's results",
              bool(run) and run["resumable_prefix"] == 1 and run["journal"]["distinct_calls"] == 2,
              f"{run and run['journal']}")

        a2 = next((a for a in (run or {}).get("agents", []) if a["agent_id"] == "a0002"), None)
        check("4. an agent that only mentions a rate limit is not called failed",
              bool(a2) and a2["terminal_error"] is None and a2["mid_turn"] is True,
              f"err={a2 and a2['terminal_error']}")
        run2 = next((r for r in (crashed or {}).get("unfinished_runs", [])
                     if r["run_id"] == ids["run2"]), None)
        a3 = next((a for a in (run2 or {}).get("agents", []) if a["agent_id"] == "a0003"), None)
        check("4b. an agent whose transcript ends in an API error is",
              bool(a3) and a3["terminal_error"] is not None
              and "Connection lost" in a3["terminal_error"],
              f"err={a3 and a3['terminal_error']}")

        check("5. the cleanly-stopped session is present but owed nothing",
              bool(clean) and clean["state"] == "STOPPED"
              and not clean["unfinished_runs"] and not clean["mid_turn"],
              f"{clean and (clean['mid_turn'], len(clean['unfinished_runs']))}")

        check("6. the item id is read off the agent's own prompt",
              bool(a2) and a2["item"] == "ORD-0081", f"item={a2 and a2['item']}")

        # --- what open_tabs.py does with the scan -------------------------------
        sys.path.insert(0, str(Path(__file__).parent))
        import open_tabs

        fresh_run = {"run_id": "wf_fresh", "script_path": None, "unfinished": True, "owed": 1,
                     "journal": {"results": 0, "distinct_calls": 1, "pending_keys": ["k"],
                                 "started_attempts": 1, "pending_agents": []},
                     "agents": [{"agent_id": "afresh", "transcript": "/tmp/f.jsonl", "lines": 90,
                                 "quiet_for": 900, "item": "NEW-1", "prompt_head": "",
                                 "mid_turn": False, "unanswered_tools": [],
                                 "terminal_error": None}]}
        stale_run = dict(fresh_run, run_id="wf_stale",
                         agents=[dict(fresh_run["agents"][0], agent_id="astale",
                                      quiet_for=200_000, item="OLD-1")])
        both = {"session_id": "s", "project": "-tmp", "cwd": "/tmp", "quiet_for": 900,
                "mid_turn": False, "unanswered_tools": [], "state": "STOPPED",
                "unfinished_runs": [fresh_run, stale_run], "loose_subagents": []}
        runs, loose = open_tabs.in_flight(both, 3600)
        check("7. a run abandoned before the crash is not treated as interrupted",
              [r["run_id"] for r in runs] == ["wf_fresh"],
              f"kept={[r['run_id'] for r in runs]}")

        loose_only = dict(both, unfinished_runs=[], loose_subagents=[
            {"agent_id": "aloose", "transcript": "/tmp/l.jsonl", "lines": 313, "quiet_for": 880,
             "item": None, "prompt_head": "You are the runner for R17", "mid_turn": False,
             "unanswered_tools": [], "terminal_error": None}])
        _, loose = open_tabs.in_flight(loose_only, 3600)
        check("8. a session whose only in-flight work is a background agent is recoverable",
              len(loose) == 1, f"loose={len(loose)}")

        check("9. a cwd containing a dash is not guessed from the project directory name",
              open_tabs.resolve_cwd({"project": "-Users-x-Dev-mcp-router", "cwd": None}) is None,
              "a lossy guess must be rejected, not passed to cd")

        brief = open_tabs.write_brief(root, 99, both, runs, [])
        check("10. the brief names an agent that ended without returning a result",
              "NEW-1" in brief.read_text() and "OLD-1" not in brief.read_text(),
              "fresh agent listed, abandoned one omitted")
    finally:
        shutil.rmtree(root, ignore_errors=True)

    print()
    if failures:
        print(f"{len(failures)} failed: {', '.join(failures)}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
