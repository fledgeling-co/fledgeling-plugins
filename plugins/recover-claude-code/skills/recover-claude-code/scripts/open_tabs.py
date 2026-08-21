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
import shlex
import subprocess
import sys
import time
from pathlib import Path

OSA_NEW_TAB = '''
tell application "Ghostty" to activate
delay 0.5
tell application "System Events" to tell process "ghostty"
  set c0 to count of radio buttons of tab group 1 of window 1
  click menu item "New Tab" of menu 1 of menu bar item "File" of menu bar 1
  delay 1.2
  set c1 to count of radio buttons of tab group 1 of window 1
end tell
return (c0 as string) & " " & (c1 as string)
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


def new_tab() -> None:
    """Open a tab and confirm the count actually moved.

    Confirming matters because the keystroke route fails silently: a recovery that assumed
    the tab existed would type its bootstrap line into whatever session happened to be
    focused, which is someone else's live conversation.
    """
    out = osa(OSA_NEW_TAB)
    try:
        before, after = (int(x) for x in out.split())
    except ValueError:
        raise RuntimeError(f"could not read the tab count back (got {out!r})")
    if after != before + 1:
        raise RuntimeError(f"no new tab appeared (count {before} -> {after})")


def write_bootstrap(dirpath: Path, index: int, session: dict, brief_path: Path,
                    model: str | None, extra_args: str) -> Path:
    """One shell script per tab.

    Everything hard — the cd, the quoting, the brief — lives in this file so the only thing
    typed into the terminal is a short `source` line with no metacharacters in it.
    """
    cwd = session["cwd"]
    sid = session["session_id"]
    name = session.get("name") or sid[:8]
    model_arg = f" --model {shlex.quote(model)}" if model else ""
    script = f"""#!/bin/zsh
# recover-claude-code: tab {index} — {name}
# session {sid}
print -P "%F{{cyan}}recovering {name}%f  ({sid})"
cd {shlex.quote(cwd)} || {{ print "cannot cd to {cwd}"; return 1 }}
exec claude --dangerously-skip-permissions{model_arg}{(' ' + extra_args) if extra_args else ''} \\
  --resume {shlex.quote(sid)} "$(cat {shlex.quote(str(brief_path))})"
"""
    p = dirpath / f"tab-{index:02d}-{sid[:8]}.sh"
    p.write_text(script)
    p.chmod(0o755)
    return p


def write_brief(dirpath: Path, index: int, session: dict) -> Path:
    """The first turn the resumed session sees.

    It leads with what happened, because the session's own last memory is of work in
    progress and it will otherwise carry on as if nothing broke. It points at the branch
    before the transcript, because what landed in git is the authority on what was done and
    an agent's own account is only evidence of what it was attempting.
    """
    runs = session.get("unfinished_runs", [])
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
            for a in r["agents"]:
                if a["mid_turn"] or a["terminal_error"]:
                    lines.append(
                        f"    {a['item'] or a['agent_id']}: {a['lines']} lines of work, "
                        f"{'stopped mid-tool' if a['mid_turn'] else a['terminal_error']}"
                    )
                    lines.append(f"      transcript: {a['transcript']}")
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
    args = ap.parse_args()

    raw = sys.stdin.read() if args.scan == "-" else Path(args.scan).expanduser().read_text()
    data = json.loads(raw)

    targets = [
        s for s in data["sessions"]
        if s["state"] == "STOPPED" and (s["unfinished_runs"] or s["mid_turn"])
    ]
    if args.limit:
        targets = targets[: args.limit]

    if not targets:
        print("nothing to recover: no stopped session is owed a result or was cut mid-turn")
        return 0

    workdir = Path(args.workdir).expanduser() if args.workdir else Path(
        f"/tmp/rcc-{time.strftime('%Y%m%d-%H%M%S')}")
    workdir.mkdir(parents=True, exist_ok=True)

    ledger = []
    for i, s in enumerate(targets, 1):
        brief = write_brief(workdir, i, s)
        boot = write_bootstrap(workdir, i, s, brief, args.model, args.claude_args)
        ledger.append({"index": i, "session_id": s["session_id"], "name": s.get("name"),
                       "cwd": s["cwd"], "bootstrap": str(boot), "brief": str(brief),
                       "runs": [r["run_id"] for r in s["unfinished_runs"]], "opened": False})

    print(f"{len(targets)} session(s) to recover · scripts in {workdir}\n")
    for e in ledger:
        print(f"  {e['index']:>2}. {(e['name'] or e['session_id'][:8]):<24} {e['cwd']}")
        print(f"      {len(e['runs'])} interrupted run(s): {', '.join(e['runs']) or '-'}")

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
