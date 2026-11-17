#!/usr/bin/env python3
"""Print the newest model id a CLI currently offers, so a lane always runs the latest release.

    latest_model.py grok                    # newest plain grok-N.N from `grok models`, e.g. grok-4.7
    latest_model.py gemini                  # newest gemini-<version>-argon-medium from `agy models`, or
                                            # the newest gemini-<version>-hydrogen-xhigh when agy lists no Argon at medium
    latest_model.py gemini --name hydrogen --effort xhigh   # exactly that name and effort, no fallback
    latest_model.py opus                    # the claude CLI alias, which tracks the newest Opus
    latest_model.py fable                   # the pinned panel model, claude-fable-5-2
    latest_model.py codex                   # path of the newest codex CLI on this machine

Opus needs no lookup: `claude --model opus` resolves to the newest Opus on every call. The fable
panel lane is pinned to `claude-fable-5-2` (run at medium effort by run_panel.sh), so it resolves
to that exact id rather than the `fable` alias. grok and agy have no such alias, so this reads
their model lists and picks the highest version number.

The Google lane is Gemini Argon at medium, and Gemini Hydrogen at xhigh only when Argon at medium
is unavailable (owner directive, 18 Nov 2026). This resolver covers "agy lists no Argon at
medium"; run_panel.sh covers the other case, an Argon run that fails, by re-running on Hydrogen.

`codex` prints a binary path, not a model id. The standalone codex install can lag the CLI the
ChatGPT app bundles, and measured 18 Nov 2026 codex 0.163.0 refused gpt-6.2-astra ("not supported
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

PINS = {"grok": "grok-4.7", "gemini": "gemini-4-argon-medium", "opus": "opus",
        "fable": "claude-fable-5-2", "codex": "codex"}
# The Google lane in order of preference: Argon at medium, then Hydrogen at xhigh (owner directive, 18 Nov 2026).
GEMINI_CHAIN = (("argon", "medium"), ("hydrogen", "xhigh"))
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
    ap.add_argument("--name", help="gemini only: the model name to take (argon, hydrogen); disables the fallback chain")
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
