#!/usr/bin/env python3
"""Who is live, what they hold, and what is unattached.

The session registry (~/.claude/sessions/<PID>.json) is the liveness AUTHORITY -- it carries
sessionId, cwd, pid, the peer name and a status. Two probes that look plausible do not work:
`ps` output does not contain the session id, and the scratchpad directory is named by a
per-process id that stops matching once a session has been resumed.

Names are the address for SendMessage -- but a session can appear under a name its own
conductor does not recognise from inside. Reconcile by cwd and pid, never by name alone: two
sessions were established as a conductor's own workers only after it counted processes per
worktree rather than trusting the names it was given.

Read-only. Touches nothing.
"""
import argparse, json, os, subprocess, sys
from pathlib import Path

SESSIONS = Path.home() / ".claude/sessions"


def sh(args, cwd=None):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=20, cwd=cwd)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def alive(pid):
    try:
        os.kill(int(pid), 0)
        return True
    except (OSError, ValueError, TypeError):
        return False


def repo_state(cwd):
    if not cwd or not Path(cwd).is_dir():
        return {}
    top = sh(["git", "-C", cwd, "rev-parse", "--show-toplevel"])
    if not top:
        return {"repo": None}
    st = {"repo": top, "branch": sh(["git", "-C", top, "rev-parse", "--abbrev-ref", "HEAD"])}
    st["ai_branches"] = len([l for l in sh(
        ["git", "-C", top, "branch", "--list", "ai/*"]).splitlines() if l.strip()])
    st["worktrees"] = len([l for l in sh(
        ["git", "-C", top, "worktree", "list"]).splitlines() if l.strip()])
    st["hooks_path"] = sh(["git", "-C", top, "config", "--get", "core.hooksPath"]) or "(unset)"
    # A repo can carry an origin for a repository that has NEVER been created: 453 commits,
    # `Repository not found`, and no origin/main -- indistinguishable from a never-fetched
    # remote. Check before ordering a push, not after.
    st["origin"] = sh(["git", "-C", top, "remote", "get-url", "origin"]) or "(none)"
    return st


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check-remotes", action="store_true",
                    help="run `git ls-remote` per repo (network; proves the remote EXISTS)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = []
    if SESSIONS.is_dir():
        for f in sorted(SESSIONS.glob("*.json")):
            try:
                d = json.loads(f.read_text())
            except Exception:
                continue
            pid = d.get("pid") or f.stem
            row = {"name": d.get("name"), "session_id": d.get("sessionId"),
                   "pid": pid, "status": d.get("status"), "cwd": d.get("cwd"),
                   "alive": alive(pid)}
            row.update(repo_state(d.get("cwd")))
            if a.check_remotes and row.get("repo"):
                ls = sh(["git", "-C", row["repo"], "ls-remote", "--heads", "origin"])
                row["remote_exists"] = bool(ls)
                if not ls and row.get("origin") not in ("(none)", ""):
                    row["REMOTE_WARNING"] = (
                        "origin is configured but ls-remote returned nothing -- the repository "
                        "may never have been created. Creating it is outward-facing.")
            rows.append(row)

    out = {"sessions": rows, "count": len(rows),
           "live": sum(1 for r in rows if r["alive"]),
           "notes": [
               "names are the SendMessage address; reconcile ownership by cwd+pid, not by name",
               "ask each session for its own state -- do not derive it and do not trust ARMADA.md",
               "ARMADA.md describes each project TWICE (index + detail); the index is read first "
               "and is the half that goes stale",
           ]}
    if not a.check_remotes:
        out["notes"].append("re-run with --check-remotes before ordering any push")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
