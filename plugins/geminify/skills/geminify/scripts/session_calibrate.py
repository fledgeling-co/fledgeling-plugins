#!/usr/bin/env python3
"""session_calibrate.py — the receipt ledger for a Gemini runner's own session.

`scan_skill.py` reads one target and says what a `gemini.md` must cover. This
script answers the other question: **this session is about to run on Gemini, with
these skills loaded — what does the runner have to do differently, and what has to
be true at the end for the claim "I followed them" to be checkable?**

It exists because of a measured gap. Across 18 Aug - 1 Sep 2026, six sessions
invoked `geminify:geminify`; three of them were runners calibrating themselves
rather than authoring a file, and the skill had no procedure for that. One of the
three (`graft/aa239a23`) loaded five skills and read zero `gemini.md` files while
running on Gemini. Nothing detected it, because nothing counted.

So the output is a ledger with denominators rather than advice. Every row is a
file path that either was read or was not, and a claim of adherence names the
count.

Three sections:

  1. COVERAGE  — each named skill, whether a gemini.md exists beside it, and the
     path to read. A skill with no gemini.md is not an error; it is a row that
     says the core overrides apply unmodified.

  2. RECEIPTS  — the skills this session is expected to *invoke*, as an unticked
     ledger. A pipeline that names an upstream skill is satisfiable by writing
     compliant output without ever calling it, which is the single most common
     failure in the corpus. A receipt is the Skill tool call, not the quality of
     the result.

  3. REFERRAL  — the runner's own family, so an "out-of-family" consult cannot
     resolve to itself. 225 of 2,062 `agy` dispatches in that window were issued
     by a Gemini-family model calling Gemini.

Usage:
    session_calibrate.py --skills ship-fleet:ship-fleet,better-goal:better-goal
    session_calibrate.py --skills-from-transcript <session.jsonl>
    session_calibrate.py --skills X --model gemini-3.7-flash-high --json

stdlib only, so it runs in any sandbox.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

PLUGIN_ROOTS = [
    Path.home() / ".claude/plugins/cache",
    Path.home() / ".claude/plugins/marketplaces",
    Path.home() / ".claude/skills",
]

# User and project commands resolve through the Skill tool without a SKILL.md.
# Treating one as missing reports a working skill as broken, which is the same
# class of error as reporting a broken one as working.
COMMAND_ROOTS = [
    Path.home() / ".claude/commands",
    Path(".claude/commands"),
]

GEMINI_FAMILY = re.compile(r"gemini|antigravity|(?:^|[/:_-])agy(?:$|[/:_-])", re.I)

# Families a Gemini runner may refer to for an out-of-family second opinion.
OUT_OF_FAMILY = {
    "claude": "claude --model claude-fable-5 --effort high -p",
    "openai": "codex exec -m gpt-5.6-sol -c model_reasoning_effort=\"high\" -s read-only",
    "xai": "grok -m grok-4.6 --effort xhigh -p",
}


def family_of(model: str) -> str:
    """Name the model's family, so a referral can exclude it."""
    if not model:
        return "unknown"
    if GEMINI_FAMILY.search(model):
        return "gemini"
    m = model.lower()
    if "claude" in m or "opus" in m or "sonnet" in m or "haiku" in m or "fable" in m:
        return "claude"
    if "gpt" in m or "openai" in m or "luna" in m or "codex" in m:
        return "openai"
    if "grok" in m:
        return "xai"
    if "glm" in m:
        return "zai"
    return "unknown"


def find_skill_dir(name: str) -> Path | None:
    """Resolve `plugin:skill` or a bare skill name to the directory holding SKILL.md.

    Prefers the highest version directory when a plugin cache holds several.
    """
    skill = name.split(":")[-1]
    hits: list[Path] = []
    for root in PLUGIN_ROOTS:
        if not root.exists():
            continue
        for p in root.rglob(f"skills/{skill}/SKILL.md"):
            hits.append(p.parent)
        direct = root / skill / "SKILL.md"
        if direct.exists():
            hits.append(direct.parent)
    if not hits:
        return None
    # A cache path carries the version as a path segment; the lexically greatest
    # is the newest for the semver shapes in use here.
    return sorted(hits, key=lambda p: str(p))[-1]


def marketplace_names(mp_root: Path) -> set[str]:
    """Plugin names a marketplace actually publishes."""
    mf = mp_root / ".claude-plugin/marketplace.json"
    if not mf.exists():
        return set()
    try:
        data = json.load(open(mf, errors="replace"))
    except (ValueError, OSError):
        return set()
    return {e.get("name") for e in data.get("plugins", []) if isinstance(e, dict)}


def is_registered(skill_dir: Path) -> bool | None:
    """Whether the Skill tool can resolve this, which is not the same as it being on disk.

    Measured: `create-test-suite` sits in the plugin cache at 0.3.0 and is absent
    from its marketplace's 53 published entries. Ten Skill calls naming it failed
    with `Unknown skill` while the directory existed the whole time. Returns None
    when the path is not under a marketplace layout and the question does not apply.
    """
    parts = skill_dir.parts
    for anchor in ("marketplaces", "cache"):
        if anchor not in parts:
            continue
        i = parts.index(anchor)
        if i + 2 >= len(parts):
            continue
        marketplace = parts[i + 1]
        # Two layouts share this tree and differ by one segment:
        #   marketplaces/<mp>/plugins/<plugin>/skills/<skill>
        #   cache/<mp>/<plugin>/<version>/skills/<skill>
        # Taking parts[i+2] blindly reads the literal "plugins" as the plugin name
        # and reports every working skill as unloadable.
        j = i + 2
        if parts[j] == "plugins" and j + 1 < len(parts):
            j += 1
        plugin_name = parts[j]
        # marketplace.json lives with the checkout, never with the cache copy.
        names = marketplace_names(Path.home() / ".claude/plugins/marketplaces" / marketplace)
        if not names:
            return None
        return plugin_name in names
    return None


def skills_from_transcript(path: str) -> list[str]:
    """Every skill this session actually invoked, in first-seen order."""
    seen: list[str] = []
    try:
        fh = open(path, errors="replace")
    except OSError:
        return seen
    with fh:
        for line in fh:
            if '"Skill"' not in line:
                continue
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            msg = obj.get("message") or {}
            for block in msg.get("content") or []:
                if not isinstance(block, dict) or block.get("type") != "tool_use":
                    continue
                if block.get("name") != "Skill":
                    continue
                nm = str((block.get("input") or {}).get("skill", ""))
                if nm and nm not in seen:
                    seen.append(nm)
    return seen


def find_command(name: str) -> Path | None:
    """A user or project command that the Skill tool resolves without a SKILL.md."""
    stem = name.split(":")[-1]
    for root in COMMAND_ROOTS:
        p = root / f"{stem}.md"
        if p.exists():
            return p
    return None


def build(skills: list[str], model: str) -> dict:
    coverage = []
    for name in skills:
        d = find_skill_dir(name)
        if d is None:
            cmd = find_command(name)
            if cmd is not None:
                coverage.append({
                    "skill": name, "resolved": True, "registered": True,
                    "kind": "command", "dir": str(cmd.parent),
                    "geminiMd": None, "lines": 0,
                })
                continue
            coverage.append({"skill": name, "resolved": False, "registered": False, "geminiMd": None, "dir": None})
            continue
        g = d / "gemini.md"
        coverage.append(
            {
                "skill": name,
                "resolved": True,
                "registered": is_registered(d),
                "dir": str(d),
                "geminiMd": str(g) if g.exists() else None,
                "lines": sum(1 for _ in open(g, errors="replace")) if g.exists() else 0,
            }
        )
    fam = family_of(model)
    return {
        "model": model or "(not supplied)",
        "family": fam,
        "coverage": coverage,
        "withGeminiMd": [c for c in coverage if c["geminiMd"]],
        "withoutGeminiMd": [c for c in coverage if c["resolved"] and not c["geminiMd"]],
        "unresolved": [c for c in coverage if not c["resolved"]],
        "unregistered": [c for c in coverage if c["resolved"] and c.get("registered") is False],
        "referralLanes": {k: v for k, v in OUT_OF_FAMILY.items() if k != fam},
    }


def render(r: dict) -> None:
    cov = r["coverage"]
    have = r["withGeminiMd"]
    lack = r["withoutGeminiMd"]
    dead = r["unresolved"]

    print(f"model: {r['model']}   family: {r['family']}")
    print()
    print(f"── 1. COVERAGE — read {len(have)} of {len(cov)} before starting ──")
    for c in cov:
        if not c["resolved"]:
            print(f"  [NOT ON DISK ] {c['skill']}  — no SKILL.md found; check the plugin:skill form")
        elif c.get("kind") == "command":
            print(f"  [command    ] {c['skill']}  — a command file, no gemini.md layer; core overrides apply")
        elif c.get("registered") is False:
            print(f"  [UNLOADABLE  ] {c['skill']}  — on disk, absent from its marketplace.json")
            print(f"                 the Skill tool answers `Unknown skill` and the run continues without it")
        elif c["geminiMd"]:
            print(f"  [READ ME  ]  {c['skill']}  ({c['lines']} lines)")
            print(f"               {c['geminiMd']}")
        else:
            print(f"  [no gemini.md] {c['skill']}  — core overrides apply unmodified")
    print()
    print(f"  read-count to report when you claim calibration: {len(have)} of {len(have)} gemini.md files")
    if dead:
        print(f"  names not on disk: {len(dead)} — each loads nothing and raises nothing")
    if r["unregistered"]:
        print(f"  unloadable names: {len(r['unregistered'])} — present on disk, unpublished by their marketplace")

    print()
    print(f"── 2. RECEIPTS — {len(cov)} skills named, {len(cov)} Skill tool calls owed ──")
    print("  Fill the third column with the tool-call turn, not with a description of the output.")
    print()
    print("  | skill | invoked (y/n) | receipt |")
    print("  |---|---|---|")
    for c in cov:
        print(f"  | {c['skill']} | | |")
    print()
    print("  A phase that names an upstream skill is satisfied by the Skill tool call.")
    print("  Writing output that conforms to the skill's rules is not a receipt.")

    print()
    print("── 3. REFERRAL — lanes that are out-of-family for this runner ──")
    if r["family"] == "unknown":
        print("  Family unknown: pass --model, or the exclusion cannot be applied.")
    for k, v in sorted(r["referralLanes"].items()):
        print(f"  {k:8s} {v}")
    if r["family"] == "gemini":
        print()
        print("  Excluded: the gemini lane (`agy`, `gemini-*`). A consult sent there")
        print("  returns an in-family answer and the artifact records independence")
        print("  that was never obtained.")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skills", default="", help="comma-separated plugin:skill names")
    ap.add_argument("--skills-from-transcript", default="", help="read invoked skills from a session .jsonl")
    ap.add_argument("--model", default=os.environ.get("GEMINIFY_MODEL", ""), help="the model serving this session")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    skills = [s.strip() for s in a.skills.split(",") if s.strip()]
    if a.skills_from_transcript:
        skills += [s for s in skills_from_transcript(a.skills_from_transcript) if s not in skills]
    if not skills:
        ap.error("no skills given: pass --skills or --skills-from-transcript")

    r = build(skills, a.model)
    if a.json:
        json.dump(r, sys.stdout, indent=1)
        print()
    else:
        render(r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
