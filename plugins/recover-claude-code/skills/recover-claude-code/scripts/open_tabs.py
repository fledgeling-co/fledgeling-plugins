#!/usr/bin/env python3
"""Open a Ghostty tab per crashed session and resume each one where it left off.

Three mechanics here were measured on 2026-08-21 (Ghostty 1.3.1, Claude Code 2.1.238,
macOS 26.6) because the obvious approaches all fail quietly:

  - **A new tab comes from the File menu, not a keystroke.** `ghostty +new-window` reports
    "not supported on this platform" on macOS, and a synthesised `cmd+T` through System
    Events is accepted and does nothing — the tab count does not move and no error is
    raised. Clicking `File > New Tab` through the accessibility API does open one.
  - **Typing text through System Events does work.** So the tab is driven by typing one
    short `source <file>` line rather than a long command, which keeps quoting, newlines
    and shell metacharacters out of the keystroke path entirely.
  - **`claude --resume <id> "<prompt>"` submits that prompt as a real user turn.** So the
    recovery brief is handed over as an argument, and there is no need to send an escape
    to head off the "Continue from where you left off." that Claude Code auto-submits when
    it restores a session that was cut mid-turn. Passing a brief replaces that turn with
    one that says what actually happened and what to do about it.

`--fork-session` is never used. Resume reuses the original session id, and a workflow's
journal is filed under the session id, so forking would silently orphan every run this is
trying to recover.
"""
from __future__ import annotations

import argparse
import json
import os
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path

OSA_COUNT = '''
tell application "System Events" to tell process "ghostty"
  try
    return (count of radio buttons of tab group 1 of window 1) as string
  on error
    return "1"
  end try
end tell
'''

OSA_NEW_TAB = '''
tell application "Ghostty" to activate
delay 0.4
tell application "System Events" to tell process "ghostty"
  click menu item "New Tab" of menu 1 of menu bar item "File" of menu bar 1
end tell
'''

OSA_TYPE = '''
tell application "Ghostty" to activate
delay 0.3
tell application "System Events"
  keystroke "{text}"
  delay 0.35
  key code 36
end tell
return "typed"
'''


def osa(script: str) -> str:
    r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "osascript failed")
    return r.stdout.strip()


def tab_count() -> int:
    """How many tabs the front window has.

    Ghostty creates the tab group only once a window holds two or more tabs, so on a
    single-tab window `tab group 1 of window 1` does not exist and the query errors. That
    read as "cannot open a tab" and failed every tab of a recovery on 2026-08-22. A window
    with no tab group has exactly one tab, so the probe reports 1 rather than raising.
    """
    return int(osa(OSA_COUNT))


def new_tab(timeout: float = 6.0) -> None:
    """Open a tab and confirm the count actually moved.

    Confirming matters because the keystroke route fails silently: a recovery that assumed
    the tab existed would type its bootstrap line into whatever session happened to be
    focused, which is someone else's live conversation. The confirmation polls rather than
    sleeping a fixed interval, because a cold Ghostty takes longer to draw the first tab
    than a warm one takes to draw the tenth.
    """
    before = tab_count()
    osa(OSA_NEW_TAB)
    deadline = time.time() + timeout
    while time.time() < deadline:
        time.sleep(0.3)
        if tab_count() == before + 1:
            return
    raise RuntimeError(f"no new tab appeared (count stayed {before})")


STAND_DOWN = (
    "The terminal process crashed and this session has just been reopened. Nothing was in "
    "flight when it died, so there is no interrupted work to resume and nothing to chase. "
    "Do not start any work, do not relaunch any workflow, and do not act on a run that was "
    "already abandoned before the crash. Say in one line where you left off, then wait."
)


def in_flight(session: dict, window: float) -> tuple[list[dict], list[dict]]:
    """The runs and loose subagents this crash actually interrupted.

    A long-lived session accumulates journals from runs that were abandoned days earlier, and
    every one of them is still "owed a result" — one session here carried 21. Feeding all of
    them to a recovered session invites it to go and chase work that was deliberately dropped,
    so a run counts only when one of its agents was still writing within `window` seconds of
    the crash.
    """
    runs = []
    for r in session.get("unfinished_runs") or []:
        agents = [a for a in (r.get("agents") or []) if 0 <= a.get("quiet_for", -1) < window]
        if agents:
            r = dict(r)
            r["agents"] = agents
            runs.append(r)
    loose = [a for a in (session.get("loose_subagents") or [])
             if 0 <= a.get("quiet_for", -1) < window]
    return runs, loose


def resolve_cwd(session: dict) -> str | None:
    """Where to reopen the session.

    The scan reads cwd from the tail of the transcript, and a session whose last entries are
    all queue operations records none — one did on 2026-08-22, and `cd None` would have been
    typed into a terminal. The project directory name is the fallback: it is the launch cwd
    with the separators replaced, which is lossy for a path that itself contains a dash, so it
    is only used when the transcript offers nothing and the result is checked before use.
    """
    if session.get("cwd"):
        return session["cwd"]
    guess = "/" + session.get("project", "").lstrip("-").replace("-", "/")
    return guess if os.path.isdir(guess) else None


def write_bootstrap(dirpath: Path, index: int, session: dict, brief_path: Path | None,
                    model: str | None, extra_args: str) -> Path:
    """One shell script per tab.

    Everything hard — the cd, the quoting, the brief — lives in this file so the only thing
    typed into the terminal is a short `source` line with no metacharacters in it.

    With no brief (an idle reopen) the session is resumed with no prompt at all, and
    CLAUDE_CODE_RESUME_PROMPT carries a stand-down line: Claude Code auto-submits a continue
    prompt when it classifies the restored transcript as an interrupted turn, and on a session
    that was merely sitting idle that would start work nobody asked for.
    """
    cwd = session["cwd"]
    sid = session["session_id"]
    name = session.get("name") or sid[:8]
    model_arg = f" --model {shlex.quote(model)}" if model else ""
    extra = (" " + extra_args) if extra_args else ""
    if brief_path is None:
        launch = (f"export CLAUDE_CODE_RESUME_PROMPT={shlex.quote(STAND_DOWN)}\n"
                  f"exec claude --dangerously-skip-permissions{model_arg}{extra} "
                  f"--resume {shlex.quote(sid)}")
    else:
        launch = (f"exec claude --dangerously-skip-permissions{model_arg}{extra} \\\n"
                  f"  --resume {shlex.quote(sid)} \"$(cat {shlex.quote(str(brief_path))})\"")
    script = f"""#!/bin/zsh
# recover-claude-code: tab {index} — {name}
# session {sid}
print -P "%F{{cyan}}recovering {name}%f  ({sid})"
cd {shlex.quote(cwd)} || {{ print "cannot cd to {cwd}"; return 1 }}
{launch}
"""
    p = dirpath / f"tab-{index:02d}-{sid[:8]}.sh"
    p.write_text(script)
    p.chmod(0o755)
    return p


def write_brief(dirpath: Path, index: int, session: dict, runs: list[dict],
                loose: list[dict]) -> Path:
    """The first turn the resumed session sees.

    It leads with what happened, because the session's own last memory is of work in progress
    and it will otherwise carry on as if nothing broke. It points at the branch before the
    transcript, because what landed in git is the authority on what was done and an agent's
    own account is only evidence of what it was attempting. And it names every agent that was
    in flight, not only the ones that died loudly: an agent that reached the end of its turn
    without returning a result looks healthy in the journal and is exactly the one whose
    context is worth promoting.
    """
    lines = [
        "This session was interrupted: the terminal process died while it was working, "
        "not because the work finished. Before continuing, establish what actually landed.",
        "",
        f"Stopped about {session['quiet_for'] // 60} minutes ago.",
    ]
    if session.get("mid_turn"):
        lines += [
            f"It was cut mid-turn with an unanswered "
            f"{', '.join(session['unanswered_tools']) or 'tool call'}, so anything that "
            f"call was going to report never arrived.",
        ]
    if runs:
        lines += ["", "Interrupted background work:"]
        for r in runs:
            j = r["journal"]
            lines.append(
                f"  {r['run_id']}: {j['results']} of {j['distinct_calls']} agent calls "
                f"returned, {len(j['pending_keys'])} still owed."
            )
            lines.append(f"    script: {r['script_path'] or 'not persisted to disk'}")
    agents = [a for r in runs for a in r["agents"]] + list(loose)
    if agents:
        lines += [
            "",
            "Agents that were in flight when the process died. Each has its own transcript "
            "holding the context it had built up — the files it read, what it had concluded. "
            "promote_agent.py brings that back as a resumable session; relaunching them from "
            "their original prompt throws it away and re-derives it at full cost.",
            "",
        ]
        for a in sorted(agents, key=lambda a: -(a.get("lines") or 0)):
            state = ("stopped mid-tool" if a.get("mid_turn")
                     else a.get("terminal_error")
                     or "reached the end of its turn but never returned a result")
            label = a.get("item") or a.get("agent_id", "?")[:9]
            lines.append(f"  {label}: {a.get('lines')} lines — {state}")
            head = (a.get("prompt_head") or "").strip()
            if head and not a.get("item"):
                lines.append(f"    {head[:150]}")
            lines.append(f"    transcript: {a['transcript']}")
    lines += [
        "",
        "Start by reconciling against version control rather than against your own last "
        "message: the branch and its commits are what actually happened, and the runners "
        "committed incrementally, so most of their work is probably on disk. Then decide "
        "what is genuinely outstanding.",
        "",
        "The recover-claude-code skill covers how to bring an interrupted run back with the "
        "context it had, rather than restarting its agents from a blank slate. Read it "
        "before relaunching anything, and leave any run that is still live alone.",
    ]
    p = dirpath / f"brief-{index:02d}-{session['session_id'][:8]}.md"
    p.write_text("\n".join(lines) + "\n")
    return p


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--scan", required=True,
                    help="scan_crashed.py --json output, or - to read stdin")
    ap.add_argument("--workdir", default=None,
                    help="where to write the per-tab scripts (default: a new /tmp directory)")
    ap.add_argument("--dry-run", action="store_true",
                    help="write the scripts and print what would be typed, open nothing")
    ap.add_argument("--limit", type=int, default=0, help="open at most this many tabs")
    ap.add_argument("--model", help="pass --model to each resumed session")
    ap.add_argument("--claude-args", default="", help="extra args for every claude invocation")
    ap.add_argument("--settle", type=float, default=2.0,
                    help="seconds between opening a tab and typing into it")
    ap.add_argument("--fresh-within", type=float, default=3600.0,
                    help="an agent quiet for less than this many seconds when the process "
                         "died counts as interrupted by this crash (default 3600). Runs whose "
                         "agents all went quiet earlier were abandoned before it.")
    ap.add_argument("--include-idle", action="store_true",
                    help="also reopen stopped sessions that were owed nothing — resumed with "
                         "no prompt, so they come back where they were and wait.")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.scan == "-" else Path(args.scan).expanduser().read_text()
    data = json.loads(raw)

    stopped = [s for s in data["sessions"] if s["state"] == "STOPPED"]
    skipped: list[tuple[str, str]] = []
    targets: list[tuple[dict, list[dict], list[dict]]] = []
    for s in stopped:
        cwd = resolve_cwd(s)
        if not cwd:
            skipped.append((s["session_id"][:8], "no working directory could be resolved"))
            continue
        s = dict(s, cwd=cwd)
        runs, loose = in_flight(s, args.fresh_within)
        if runs or loose or s["mid_turn"]:
            targets.append((s, runs, loose))
        elif args.include_idle:
            targets.append((s, [], []))
        elif s["unfinished_runs"]:
            skipped.append((s["session_id"][:8],
                            f"{len(s['unfinished_runs'])} run(s), all abandoned before the crash"))
    if args.limit:
        targets = targets[: args.limit]

    if not targets:
        print("nothing to recover: no stopped session was interrupted mid-flight")
        for sid, why in skipped:
            print(f"  skipped {sid}: {why}")
        return 0

    workdir = Path(args.workdir).expanduser() if args.workdir else Path(
        f"/tmp/rcc-{time.strftime('%Y%m%d-%H%M%S')}")
    workdir.mkdir(parents=True, exist_ok=True)

    ledger = []
    for i, (s, runs, loose) in enumerate(targets, 1):
        idle = not (runs or loose or s["mid_turn"])
        brief = None if idle else write_brief(workdir, i, s, runs, loose)
        boot = write_bootstrap(workdir, i, s, brief, args.model, args.claude_args)
        ledger.append({"index": i, "session_id": s["session_id"], "name": s.get("name"),
                       "cwd": s["cwd"], "bootstrap": str(boot),
                       "brief": str(brief) if brief else None, "idle": idle,
                       "runs": [r["run_id"] for r in runs],
                       "agents": sum(len(r["agents"]) for r in runs) + len(loose),
                       "opened": False})

    print(f"{len(targets)} session(s) to recover · scripts in {workdir}\n")
    for e in ledger:
        print(f"  {e['index']:>2}. {(e['name'] or e['session_id'][:8]):<24} {e['cwd']}")
        if e["idle"]:
            print("      owed nothing — reopened with no prompt")
        else:
            print(f"      {len(e['runs'])} interrupted run(s), {e['agents']} agent(s) in flight"
                  f"{': ' + ', '.join(e['runs']) if e['runs'] else ''}")
    for sid, why in skipped:
        print(f"  --  {sid} skipped: {why}")

    if args.dry_run:
        print(f"\ndry run: nothing opened. Each tab would be sent:  source <bootstrap>")
        (workdir / "ledger.json").write_text(json.dumps(ledger, indent=1))
        print(f"ledger: {workdir / 'ledger.json'}")
        return 0

    print(f"\nopening tabs — do not type in Ghostty while this runs\n")
    failures = 0
    for e in ledger:
        try:
            new_tab()
            time.sleep(args.settle)
            osa(OSA_TYPE.format(text=f"source {e['bootstrap']}"))
            e["opened"] = True
            print(f"  opened  {e['name'] or e['session_id'][:8]}")
        except Exception as exc:  # a failed tab must not take the rest of the run with it
            failures += 1
            e["error"] = str(exc)
            print(f"  FAILED  {e['name'] or e['session_id'][:8]}: {exc}")
        time.sleep(0.6)

    (workdir / "ledger.json").write_text(json.dumps(ledger, indent=1))
    opened = sum(1 for e in ledger if e["opened"])
    print(f"\n{opened} opened, {failures} failed · ledger {workdir / 'ledger.json'}")
    if failures:
        print("Re-run the failed ones by sourcing their bootstrap script in a tab yourself.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
