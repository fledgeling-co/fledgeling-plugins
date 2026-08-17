#!/usr/bin/env python3
"""scan_skill.py — read a target SKILL.md and report what a gemini.md must cover.

Two outputs, both derived from the target rather than from a template:

  1. The QUOTA LEDGER: every categorical quantifier and relative qualifier in the
     skill, with its line, so each one can be given an objective count. This is
     the mechanic the whole skill turns on — Google's own prompt health checklist
     names "Ambiguity" and prescribes objective constraints over relative
     qualifiers, and a measured Gemini run satisfied every categorical noun in a
     brief with exactly one instance.

  2. The MODULE TRIGGERS: which optional sections the gemini.md needs, decided by
     what the skill demonstrably contains rather than by classifying it as
     "design" or "not design". A skill that never renders anything gets no
     capture guidance; a skill that ships a probe gets the whole gate module.

Usage:
    scan_skill.py <path-to-SKILL.md> [--json] [--refs]

    --json   machine-readable output
    --refs   also scan sibling references/*.md (slower, wider)

stdlib only, so it runs in any sandbox.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# ── The quota scan ────────────────────────────────────────────────────────────
# A quota row needs a categorical quantifier attached to a COUNTABLE DELIVERABLE.
# That restriction is not fussiness — it is what makes the ledger readable. The
# unrestricted version of this regex returned 83 rows for one 292-line skill,
# nearly all of them ordinary prose distributives ("each traced to", "every
# request", "any model"), which buried the four rows that actually name an
# unbounded deliverable. A ledger nobody reads is a ledger that changes nothing.
DELIVERABLE = (
    r"surfaces?|states?|screens?|pages?|slides?|menus?|flows?|actions?|"
    r"components?|elements?|views?|routes?|variants?|cases?|cells?|sections?|"
    r"items?|fields?|controls?|breakpoints?|viewports?|platforms?|modes?|"
    r"steps?|findings?|claims?|figures?|tests?|checks?|files?|entries|rows?|"
    r"decks?|icons?|assets?|images?|captures?|crops?|interactions?|"
    r"transitions?|animations?|errors?|edge\s+cases?|paths?|branches?|"
    r"scenarios?|dimensions?|lenses?|axes|stages?|phases?|units?|"
    r"pixels?|tokens?|colours?|colors?|sizes?|widths?|targets?|surfaces"
)
CATEGORICAL = re.compile(
    r"\b(?:all|every|each|any)\s+"
    r"(?:the\s+|its\s+|your\s+|their\s+|other\s+|single\s+)?"
    rf"(?:{DELIVERABLE})\b"
    rf"|\b(?:comprehensive(?:ly)?|exhaustive(?:ly)?)\b"
    rf"|\bthe\s+(?:whole|entire|full)\s+(?:{DELIVERABLE})\b"
    rf"|\bincluding\s+(?:all|every)\s+(?:the\s+)?(?:{DELIVERABLE})\b",
    re.I,
)
# Everything the loose form used to catch. Counted, never listed: knowing there
# are 79 distributives tells you the prose is emphatic; reading them tells you
# nothing you can act on.
DISTRIBUTIVE = re.compile(r"\b(?:all|every|each|any)\s+[a-z][a-z-]{2,}\b", re.I)

# Relative qualifiers: subjective words with no measurable definition. Google's
# checklist gives the fix directly — "write a summary of 3 sentences or less"
# instead of "write a brief summary".
RELATIVE = re.compile(
    r"\b(?:brief(?:ly)?|short(?:ly)?|concise(?:ly)?|thorough(?:ly)?|detailed|"
    r"appropriate(?:ly)?|reasonable|reasonably|sufficient(?:ly)?|adequate(?:ly)?|"
    r"proportional(?:ly)?|as\s+needed|where\s+relevant|where\s+appropriate|"
    r"rarely|sparingly|enough|substantial(?:ly)?|significant(?:ly)?|"
    r"high[- ]quality|polished|clean|proper(?:ly)?)\b",
    re.I,
)

# Emphasis in the register Google says stopped helping: "foundation model
# performance will no longer improve and in many cases will get worse".
EMPHASIS = re.compile(
    r"\b(?:MANDATORY|CRITICAL|REQUIRED|ABSOLUTE|FORBIDDEN|NEVER|ALWAYS|MUST)\b"
)

# ── Module triggers ───────────────────────────────────────────────────────────
# Each module is (name, why it exists, trigger words). A module fires when the
# skill's own text contains at least MIN_TRIGGERS distinct triggers, so a skill's
# gemini.md carries only the sections its subject matter earns.
#
# The threshold and the specificity of these words are both load-bearing. With
# single-hit matching on common words ("verify", "script", "source", "states"),
# seven of eight modules fired on a decision-routing skill that renders nothing —
# a classifier that says yes to everything discriminates as poorly as a gate that
# always passes, and it would have put capture-protocol guidance in a file about
# asking better questions.
MIN_TRIGGERS = 3

MODULES: list[tuple[str, str, tuple[str, ...]]] = [
    (
        "visual",
        "the skill renders something and someone has to look at it",
        ("screenshot", "capture", "crop", "render", "viewport", "pixel",
         "mockup", "figma", "obscura", "playwright", "devicescalefactor",
         "dpr", "computed style", "getboundingclientrect", "look at the",
         "open the render", "contrast ratio", "breakpoint"),
    ),
    (
        "gate",
        "the skill ships a deterministic check whose output can be quoted",
        ("preflight", "probe", "lint", "blocker", "exit code", "exits non-zero",
         "denominator", "axe", "wcag", "gate run", "run-preflight",
         "scripts/", "pass/fail", "assertion", "worklist"),
    ),
    (
        "states",
        "the skill enumerates states, edge cases or unhappy paths",
        ("empty state", "loading state", "error state", "first-run", "unhappy",
         "partial", "skeleton", "state matrix", "edge case", "designed states"),
    ),
    (
        "platform-values",
        "the skill cites vendor-published values that go stale",
        ("design system", "hig", "fluent", "material design", "design token",
         "tokens.css", "type ramp", "palette", "border-radius", "control height",
         "human interface", "winui", "swiftui", "brand guideline"),
    ),
    (
        "authorship",
        "the skill produces prose or figures a reader will act on",
        ("microcopy", "voice", "tone of voice", "provenance", "citation",
         "as at", "disclosure", "investor", "compliance", "headline",
         "lorem ipsum", "fabricat", "unsourced", "real content"),
    ),
    (
        "delegation",
        "the skill spawns subagents or workflows",
        ("subagent", "agent tool", "workflow(", "fan-out", "fan out",
         "delegate", "spawn", "judge panel", "parallel(", "pipeline(",
         "orchestrat", "runner"),
    ),
    (
        "injection",
        "the skill ingests content it did not author",
        ("untrusted", "prompt injection", "reviewed content", "treat it as data",
         "not instruction", "third-party", "webfetch", "scrape"),
    ),
    (
        "count-contract",
        "the skill already promises a count, so the contract just needs extending",
        ("slide count", "whole count", "n of n", "worklist", "ledger",
         "inventory", "enumerate", "numbered list", "resuming at"),
    ),
]


def scan(text: str, label: str) -> dict:
    lines = text.splitlines()
    quotas, relatives, emphasis = [], [], []
    distributives = 0
    for i, raw in enumerate(lines, 1):
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("<!--"):
            continue
        for m in CATEGORICAL.finditer(line):
            quotas.append({"file": label, "line": i, "phrase": m.group(0).strip(),
                            "context": line.strip()[:150]})
        distributives += len(DISTRIBUTIVE.findall(line))
        for m in RELATIVE.finditer(line):
            relatives.append({"file": label, "line": i, "phrase": m.group(0).strip(),
                              "context": line.strip()[:150]})
        for m in EMPHASIS.finditer(line):
            emphasis.append({"file": label, "line": i, "word": m.group(0),
                             "context": line.strip()[:150]})
    return {"quotas": quotas, "relatives": relatives, "emphasis": emphasis,
            "distributives": distributives}


def modules_for(text: str, min_triggers: int = MIN_TRIGGERS) -> list[dict]:
    low = text.lower()
    out = []
    for name, why, triggers in MODULES:
        hits = [t for t in triggers if t in low]
        if len(hits) >= min_triggers:
            out.append({"module": name, "why": why, "matched": hits[:8],
                        "matchCount": len(hits)})
    out.sort(key=lambda m: -m["matchCount"])
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("skill")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--refs", action="store_true")
    ap.add_argument("--min", type=int, default=MIN_TRIGGERS,
                    help=f"distinct trigger words a module needs (default {MIN_TRIGGERS})")
    a = ap.parse_args()

    p = pathlib.Path(a.skill)
    if not p.is_file():
        print(f"no such file: {p}", file=sys.stderr)
        return 2

    texts = [(p.name, p.read_text(encoding="utf-8", errors="replace"))]
    if a.refs:
        for r in sorted((p.parent / "references").glob("*.md")):
            texts.append((f"references/{r.name}",
                          r.read_text(encoding="utf-8", errors="replace")))

    agg = {"quotas": [], "relatives": [], "emphasis": []}
    distributives = 0
    for label, t in texts:
        s = scan(t, label)
        for k in agg:
            agg[k].extend(s[k])
        distributives += s["distributives"]
    joined = "\n".join(t for _, t in texts)
    mods = modules_for(joined, a.min)

    result = {
        "target": str(p),
        "filesScanned": [label for label, _ in texts],
        "lines": sum(len(t.splitlines()) for _, t in texts),
        "quotaLedger": agg["quotas"],
        "relativeQualifiers": agg["relatives"],
        "emphasis": agg["emphasis"],
        "modules": mods,
        "summary": {
            "categorical": len(agg["quotas"]),
            "distributiveProse": distributives,
            "relative": len(agg["relatives"]),
            "emphasisTokens": len(agg["emphasis"]),
            "modulesTriggered": [m["module"] for m in mods],
            "minTriggers": a.min,
        },
    }

    if a.json:
        print(json.dumps(result, indent=1))
        return 0

    s = result["summary"]
    print(f"target      {p}")
    print(f"scanned     {', '.join(result['filesScanned'])}  ({result['lines']} lines)")
    print(f"quota rows  {s['categorical']}   relative {s['relative']}   "
          f"emphasis {s['emphasisTokens']}   (distributive prose, not quotas: "
          f"{s['distributiveProse']})")
    print(f"modules     {', '.join(s['modulesTriggered']) or '(none — core only)'}"
          f"   [>= {s['minTriggers']} triggers]")
    for m in mods:
        print(f"              {m['module']:<16} {m['matchCount']:>2} hits — {m['why']}")
    if s["categorical"] == 0 and s["relative"] == 0:
        print("\nNothing to quota. Say so in the file rather than inventing rows —\n"
              "a skill with no unbounded scope needs no ledger.")
        return 0

    print("\n── quota ledger: give each of these a number ──")
    seen = set()
    for q in result["quotaLedger"]:
        key = q["phrase"].lower()
        if key in seen:
            continue
        seen.add(key)
        print(f'  {q["file"]}:{q["line"]:<5} "{q["phrase"]}"')
    print("\n── relative qualifiers: replace with a measurable bound ──")
    seen = set()
    for r in result["relativeQualifiers"][:40]:
        key = r["phrase"].lower()
        if key in seen:
            continue
        seen.add(key)
        print(f'  {r["file"]}:{r["line"]:<5} "{r["phrase"]}"')
    if result["emphasis"]:
        print(f"\n── emphasis tokens ({len(result['emphasis'])}) ──")
        print("  Google: escalating language 'will no longer improve and in many")
        print("  cases will get worse'. Read these as plain rules; don't add more.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
