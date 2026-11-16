#!/usr/bin/env python3
"""Print the newest model id a CLI currently offers, so a lane always runs the latest release.

    latest_model.py grok                    # newest plain grok-N.N from `grok models`, e.g. grok-4.7
    latest_model.py gemini --effort medium  # newest gemini-<version>-argon-medium from `agy models`
    latest_model.py opus | fable            # the claude CLI alias, which already tracks the newest model

The Anthropic families need no lookup: `claude --model opus` and `claude --model fable` resolve to
the newest Opus and Fable on every call. grok and agy have no such alias, so this reads their model
lists and picks the highest version number. For gemini it takes Argon, never Hydrogen (owner
directive, 16 Nov 2026): the newest gemini-<version>-argon-<effort> that `agy models` lists.

If the listing fails or matches nothing, it prints --fallback (or the built-in pin below) on stdout,
says so on stderr and exits 0, so a lane still runs and its log shows that the pin was used.
"""
import argparse
import re
import subprocess
import sys

PINS = {"grok": "grok-4.7", "gemini": "gemini-4-argon-{effort}", "opus": "opus", "fable": "fable"}
# Gemini lane: Argon only; Hydrogen is never chosen (owner directive, 16 Nov 2026).
GEMINI_NAME = "argon"


def version(text):
    return tuple(int(p) for p in text.split("."))


def listing(cmd):
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)
    return (out.stdout or "") + (out.stderr or "")


def newest_grok():
    found = []
    for line in listing(["grok", "models"]).splitlines():
        m = re.match(r"^\s*[-*]?\s*(grok-(\d+(?:\.\d+)*))\s*(?:\(default\))?\s*$", line)
        if m:
            found.append((version(m.group(2)), m.group(1)))
    return max(found)[1] if found else None


def newest_gemini(effort):
    found = []
    for line in listing(["agy", "models"]).splitlines():
        m = re.match(r"^(gemini-(\d+(?:\.\d+)*)-([a-z0-9-]+?)-(low|medium|high|xhigh))\b", line.strip())
        if m and m.group(4) == effort and m.group(3) == GEMINI_NAME:
            found.append((version(m.group(2)), m.group(1)))
    return max(found)[1] if found else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("family", choices=sorted(PINS))
    ap.add_argument("--effort", default="high", choices=["low", "medium", "high"],
                    help="gemini only: the effort is part of the agy model id")
    ap.add_argument("--fallback", help="id to print when the CLI listing fails")
    a = ap.parse_args()
    fallback = a.fallback or PINS[a.family].format(effort=a.effort)
    if a.family in ("opus", "fable"):
        print(a.family)
        return
    try:
        found = newest_grok() if a.family == "grok" else newest_gemini(a.effort)
    except (OSError, subprocess.SubprocessError) as e:
        found = None
        print(f"latest_model: {a.family} listing failed ({e})", file=sys.stderr)
    if not found:
        print(f"latest_model: no {a.family} model found; using pin {fallback}", file=sys.stderr)
    print(found or fallback)


if __name__ == "__main__":
    main()
