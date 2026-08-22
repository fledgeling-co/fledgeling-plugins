#!/usr/bin/env python3
"""Open a NEW Claude Code session in its own Ghostty tab, with a brief as its first turn.

The mechanism is lifted from recover-claude-code's open_tabs.py, which hardened it against
failures that are silent. Kept verbatim where it matters, because plugins cannot import each
other's code and a re-derived version would re-learn these the hard way:

  * A new tab comes from the File MENU, not a keystroke. `ghostty +new-window` reports success
    and does something else.
  * Ghostty creates the tab group only once a window holds two or more tabs, so on a
    single-tab window `tab group 1 of window 1` does not exist and the query ERRORS. That read
    as "cannot open a tab" and failed every tab of one recovery. A window with no tab group has
    exactly one tab, so the probe returns 1 rather than raising.
  * CONFIRM the tab count moved. The keystroke route fails silently, and typing a bootstrap
    line into whatever session happened to be focused types it into someone else's live
    conversation.
  * The brief goes to disk and the tab is sent ONE `source <script>` line, keeping quoting and
    shell metacharacters out of the keystroke path entirely.
  * The brief is passed as a command-line ARGUMENT so it lands as a real first turn.

Difference from recovery: a NEW session takes no `--resume` and never `--fork-session`.

Refuses to act without --go. Dry-run is the default because the failure mode is typing into a
stranger's session.
"""
import argparse, json, os, subprocess, sys, time
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


def osa(script, timeout=60):
    r = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or "osascript failed")
    return r.stdout.strip()


def tab_count():
    return int(osa(OSA_COUNT))


def new_tab(timeout=6.0):
    before = tab_count()
    osa(OSA_NEW_TAB)
    deadline = time.time() + timeout
    while time.time() < deadline:
        if tab_count() > before:
            return
        time.sleep(0.25)
    raise RuntimeError(
        f"tab count did not move past {before} -- NOT typing, because the focused session "
        "may be someone else's live conversation")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cwd", required=True, help="working directory for the new session")
    ap.add_argument("--brief", required=True, help="path to a file holding the first turn")
    ap.add_argument("--label", default="flagship", help="used in the scratch filenames")
    ap.add_argument("--workdir", default="/tmp/flagship", help="where the bootstrap is written")
    ap.add_argument("--go", action="store_true", help="actually open the tab (default: dry-run)")
    a = ap.parse_args()

    cwd, brief = Path(a.cwd).expanduser(), Path(a.brief).expanduser()
    if not cwd.is_dir():
        print(f"refusing: {cwd} is not a directory", file=sys.stderr); return 64
    if not brief.is_file():
        print(f"refusing: brief {brief} does not exist", file=sys.stderr); return 64
    text = brief.read_text().strip()
    if len(text) < 100:
        print(f"refusing: brief is {len(text)} chars -- a session spawned on an empty brief "
              "surveys nothing and reports confidently", file=sys.stderr); return 64

    wd = Path(a.workdir); wd.mkdir(parents=True, exist_ok=True)
    boot = wd / f"{a.label}-bootstrap.sh"
    briefcopy = wd / f"{a.label}-brief.md"
    briefcopy.write_text(text + "\n")
    boot.write_text(
        "#!/bin/bash\n"
        f"cd {cwd!s}\n"
        f'claude --dangerously-skip-permissions "$(cat {briefcopy!s})"\n')
    boot.chmod(0o755)

    plan = {"cwd": str(cwd), "brief_chars": len(text), "bootstrap": str(boot),
            "line_to_type": f"source {boot}",
            "note": "no --resume and never --fork-session: this is a NEW session"}

    if not a.go:
        plan["dry_run"] = True
        plan["next"] = "re-run with --go to open the tab"
        print(json.dumps(plan, indent=2)); return 0

    try:
        before = tab_count()
        new_tab()
        osa(OSA_TYPE.format(text=f"source {boot}"))
        plan.update(opened=True, tabs_before=before, tabs_after=tab_count())
    except Exception as e:
        plan.update(opened=False, error=str(e))
        print(json.dumps(plan, indent=2)); return 1
    print(json.dumps(plan, indent=2)); return 0


if __name__ == "__main__":
    sys.exit(main())
