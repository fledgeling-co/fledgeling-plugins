#!/usr/bin/env python3
"""Print the newest model id a CLI currently offers, so a lane always runs the latest release.

    latest_model.py grok                    # newest plain grok-N.N from `grok models`, e.g. grok-4.7
    latest_model.py gemini                  # newest gemini-<version>-hydrogen-xhigh from `agy models`
    latest_model.py gemini --name argon --effort medium     # exactly that name and effort
    latest_model.py opus | fable            # the claude CLI alias, which already tracks the newest model
    latest_model.py codex                   # path of the newest codex CLI on this machine

The Anthropic families need no lookup: `claude --model opus` and `claude --model fable` resolve to
the newest Opus and Fable on every call. grok and agy have no such alias, so this reads their model
lists and picks the highest version number. clarify's Gemini lane is Hydrogen at xhigh (owner
directive, 18 Nov 2026): the newest gemini-<version>-hydrogen-xhigh that `agy models` lists.

`codex` prints a binary path, not a model id. The standalone codex install can lag the CLI the
ChatGPT app bundles, and measured 18 Nov 2026 codex 0.163.0 refused gpt-6.2-sol ("not supported
when using Codex with a ChatGPT account") while the bundled 0.169.0 served it. FP_CODEX_BIN wins.

If the listing fails or matches nothing, it prints --fallback (or the built-in pin below) on stdout,
says so on stderr and exits 0, so a lane still runs and its log shows that the pin was used.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

PINS = {"grok": "grok-4.7", "gemini": "gemini-4-hydrogen-xhigh", "opus": "opus",
        "fable": "fable", "codex": "codex"}
# clarify's Gemini lane: Hydrogen at xhigh (owner directive, 18 Nov 2026).
GEMINI_CHAIN = (("hydrogen", "xhigh"),)
CODEX_BUNDLED = "/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex"


def version(text):
    return tuple(int(p) for p in re.findall(r"\d+", text))


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


def newest_gemini(chain):
    found = {}
    for line in listing(["agy", "models"]).splitlines():
        m = re.match(r"^(gemini-(\d+(?:\.\d+)*)-([a-z0-9-]+?)-(low|medium|high|xhigh))\b", line.strip())
        if m:
            found.setdefault((m.group(3), m.group(4)), []).append((version(m.group(2)), m.group(1)))
    for i, key in enumerate(chain):
        if key in found:
            if i:
                print(f"latest_model: agy offers no {chain[0][0]} model at {chain[0][1]}; using {key[0]} at {key[1]}",
                      file=sys.stderr)
            return max(found[key])[1]
    return None


def newest_codex():
    if os.environ.get("FP_CODEX_BIN"):
        return os.environ["FP_CODEX_BIN"]
    best = None
    for path in dict.fromkeys(p for p in (shutil.which("codex"), CODEX_BUNDLED) if p and os.access(p, os.X_OK)):
        try:
            out = listing([path, "--version"])
        except (OSError, subprocess.SubprocessError):
            continue
        m = re.search(r"(\d+\.\d+\.\d+)", out)
        if m and (best is None or version(m.group(1)) > best[0]):
            best = (version(m.group(1)), path)
    return best[1] if best else None


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("family", choices=sorted(PINS))
    ap.add_argument("--name", help="gemini only: the model name to take (hydrogen, argon)")
    ap.add_argument("--effort", choices=["low", "medium", "high", "xhigh"],
                    help="gemini only: the effort is part of the agy model id")
    ap.add_argument("--fallback", help="id to print when the CLI listing fails")
    a = ap.parse_args()
    if a.family == "gemini" and (a.name or a.effort):
        chain = ((a.name or GEMINI_CHAIN[0][0], a.effort or GEMINI_CHAIN[0][1]),)
        pin = f"gemini-4-{chain[0][0]}-{chain[0][1]}"
    else:
        chain, pin = GEMINI_CHAIN, PINS[a.family]
    fallback = a.fallback or pin
    if a.family in ("opus", "fable"):
        print(fallback)
        return
    try:
        found = {"grok": newest_grok, "codex": newest_codex}.get(a.family, lambda: newest_gemini(chain))()
    except (OSError, subprocess.SubprocessError) as e:
        found = None
        print(f"latest_model: {a.family} listing failed ({e})", file=sys.stderr)
    if not found:
        print(f"latest_model: no {a.family} model found; using pin {fallback}", file=sys.stderr)
    print(found or fallback)


if __name__ == "__main__":
    main()
