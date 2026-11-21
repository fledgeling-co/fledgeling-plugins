#!/usr/bin/env python3
"""Read Fledgeling's model roster: which models a skill's panel runs, and at what effort.

    roster.py lanes frontier          # fable,astra,argon,carbon,wonder-full
    roster.py lanes --for clarify     # the lanes of the tier that consumer uses
    roster.py model argon             # the model id to pass to the CLI, resolved now
    roster.py effort argon            # high | xhigh, from the lane's tier
    roster.py fallback argon          # the id to re-run on when the lane fails, or nothing
    roster.py show [tier]             # lane, family, cli, model, effort; tab separated
    roster.py table <tier>            # the same as a Markdown table, for a SKILL.md

The roster is roster.json beside this file. The source is models/roster.json at the root of the
fledgeling-plugins repository; scripts/sync_model_roster.py copies it and this script into each
plugin that uses it, because an installed plugin cannot read another plugin's files.

A tier sets the effort for the lanes in it, and a lane may carry its own. By the owner's
directive of 21 November 2026 the frontier lanes run at medium, except wonder-full at high, and
the daily lanes run at xhigh. A lane says how its model id is found:

    pinned         the exact id in the roster; the CLI has no newest-model alias
    alias          a CLI alias that already tracks the newest model (claude --model opus)
    newest-grok    the highest version `grok models` lists, or the roster's id when that fails
    newest-gemini  the highest gemini-<version>-<name>-<effort> that `agy models` lists. agy puts
                   the effort in the model id. When agy lists none, the lane's fallback lane is
                   used if it has one, and otherwise the id gemini-4-<name>-<effort> is printed
                   so the CLI's own error says what is missing.

FP_<LANE>_MODEL overrides a lane's model (FP_WONDER_FULL_MODEL for wonder-full) and switches its
fallback off. Notes about a failed listing or a fallback go to stderr, so a runner can keep them
in the lane's log; only the answer goes to stdout.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROSTER = json.loads((Path(__file__).resolve().parent / "roster.json").read_text(encoding="utf-8"))
LANES, TIERS = ROSTER["lanes"], ROSTER["tiers"]


def note(msg):
    print(f"roster: {msg}", file=sys.stderr)


def version(text):
    return tuple(int(p) for p in re.findall(r"\d+", text))


def listing(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60, stdin=subprocess.DEVNULL)
        return (out.stdout or "") + (out.stderr or "")
    except (OSError, subprocess.SubprocessError) as e:
        note(f"{' '.join(cmd)} failed ({e})")
        return ""


def tier_of(lane):
    for name, tier in TIERS.items():
        if lane in tier["lanes"]:
            return name
    sys.exit(f"roster: lane {lane!r} is in no tier")


def effort(lane):
    return LANES[lane].get("effort") or TIERS[tier_of(lane)]["effort"]


def newest_gemini(name, eff):
    found = []
    for line in listing(["agy", "models"]).splitlines():
        m = re.match(rf"^(gemini-(\d+(?:\.\d+)*)-{re.escape(name)}-{eff})\b", line.strip())
        if m:
            found.append((version(m.group(2)), m.group(1)))
    return max(found)[1] if found else None


def newest_grok():
    found = []
    for line in listing(["grok", "models"]).splitlines():
        m = re.match(r"^\s*[-*]?\s*(grok-(\d+(?:\.\d+)*))\s*(?:\(default\))?\s*$", line)
        if m:
            found.append((version(m.group(2)), m.group(1)))
    return max(found)[1] if found else None


def override(lane):
    return os.environ.get("FP_" + lane.upper().replace("-", "_") + "_MODEL", "")


def model(lane, use_fallback=True):
    if lane not in LANES:
        sys.exit(f"roster: unknown lane {lane!r}; known: {', '.join(LANES)}")
    if override(lane):
        return override(lane)
    spec = LANES[lane]
    how = spec["resolve"]
    if how in ("pinned", "alias"):
        return spec["model"]
    if how == "newest-grok":
        found = newest_grok()
        if not found:
            note(f"no grok model listed; using {spec['model']}")
        return found or spec["model"]
    if how == "newest-gemini":
        eff = effort(lane)
        found = newest_gemini(spec["name"], eff)
        if found:
            return found
        fb = spec.get("fallback")
        if use_fallback and fb:
            fb_id = model(fb, use_fallback=False)
            note(f"agy lists no {spec['name']} at {eff}; falling back to {fb_id}")
            return fb_id
        pin = f"gemini-4-{spec['name']}-{eff}"
        note(f"agy lists no {spec['name']} at {eff}; using {pin}")
        return pin
    sys.exit(f"roster: lane {lane!r} has unknown resolve {how!r}")


def fallback(lane):
    fb = LANES[lane].get("fallback")
    if not fb or override(lane):
        return ""
    return model(fb, use_fallback=False)


def lanes_of(arg):
    if arg in TIERS:
        return TIERS[arg]["lanes"]
    sys.exit(f"roster: unknown tier {arg!r}; known: {', '.join(TIERS)}")


def rows(tier=None):
    for t in ([tier] if tier else list(TIERS)):
        for lane in lanes_of(t):
            spec = LANES[lane]
            how = spec["resolve"]
            if how == "newest-gemini":
                shown = f"newest gemini-<v>-{spec['name']}-{effort(lane)}"
                if spec.get("fallback"):
                    fb = LANES[spec["fallback"]]
                    shown += f", then {fb['name']} at {effort(spec['fallback'])}"
            elif how == "newest-grok":
                shown = f"newest the CLI lists ({spec['model']} when written)"
            else:
                shown = spec["model"]
            yield t, lane, spec["label"], spec["family"], spec["cli"], shown, effort(lane)


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd, args = argv[1], argv[2:]
    if cmd == "lanes":
        if args and args[0] == "--for":
            consumer = args[1]
            if consumer not in ROSTER["consumers"]:
                sys.exit(f"roster: {consumer!r} is not a listed consumer")
            entry = ROSTER["consumers"][consumer]
            print(",".join(lanes_of(entry["tier"] if isinstance(entry, dict) else entry)))
        else:
            print(",".join(lanes_of(args[0])))
    elif cmd == "model":
        print(model(args[0]))
    elif cmd == "effort":
        print(effort(args[0]))
    elif cmd == "fallback":
        print(fallback(args[0]))
    elif cmd == "show":
        for t, lane, label, family, cli, _, eff in rows(args[0] if args else None):
            print("\t".join((t, lane, family, cli, model(lane), eff)))
    elif cmd == "table":
        print("| Lane | Model | Family | CLI | Model id | Effort |\n|---|---|---|---|---|---|")
        for _, lane, label, family, cli, shown, eff in rows(args[0]):
            print(f"| `{lane}` | {label} | {family} | `{cli}` | {shown} | {eff} |")
    else:
        sys.exit(f"roster: unknown command {cmd!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
