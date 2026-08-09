#!/usr/bin/env python3
"""Build blind A/B bundles from the eval run outputs.

Judges see two questions (or two responses) side by side and never learn which
came from the skill, never see the skill files, and are never told that either
side is a baseline. Order is seeded-random per pair, so "A" carries no
information.

Judged evals only. The gate evals (did it ask at all?) are settled by the
presence or absence of a payload file and need no judge; sending them to a
panel would buy an opinion about something already decided.

Usage: build_blind_bundles.py <runs_dir> <out_dir>
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

SEED = 20260809

# eval name -> what the judge is asked to weigh. Phrased as the reader's
# interest, never as "which followed the rules better" — a judge told the rules
# would just re-run the linter.
CRITERIA = {
    "genuine-fork-gets-a-batched-recommended-question":
        "Which set of questions could a busy engineer answer correctly in less time, "
        "without having to work out the consequences of each option themselves?",
    "plain-language-and-length-caps":
        "Which question could someone who is NOT a specialist in this area still answer "
        "correctly, because the choice is described by what happens rather than by what "
        "it is called?",
    "three-open-axes-batch-into-one-round":
        "Which approach costs the person fewer interruptions and less re-reading to get "
        "the same decisions made?",
    "near-synonym-options-are-collapsed":
        "Which set of options presents genuinely different choices, rather than the same "
        "choice worded several ways?",
    "a-note-on-an-answer-overrides-the-label":
        "The person chose an option AND attached a written constraint to it. Which "
        "response actually respects that written constraint in what it plans to do?",
}


def read_side(run_dir: Path) -> str | None:
    """The payload if one was written, otherwise the response text."""
    payload = run_dir / "payload.json"
    if payload.exists():
        try:
            q = json.loads(payload.read_text()).get("questions", [])
        except Exception:
            return None
        out = []
        for item in q:
            out.append(f"**{item.get('question','').strip()}**")
            for o in item.get("options", []):
                out.append(f"- **{o.get('label','')}** — {o.get('description','')}")
            out.append("")
        body = "\n".join(out).strip()
        return body or None

    tr = run_dir / "transcript.txt"
    if tr.exists():
        t = tr.read_text().strip()
        return t if len(t) > 80 else None
    return None


def main() -> None:
    runs, out_dir = Path(sys.argv[1]), Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)

    key, made, skipped = {}, 0, []
    for name, criterion in CRITERIA.items():
        s, b = read_side(runs / name / "skill"), read_side(runs / name / "baseline")
        if not s or not b:
            skipped.append(f"{name} (skill={'ok' if s else 'empty'}, baseline={'ok' if b else 'empty'})")
            continue

        made += 1
        skill_is_a = rng.random() < 0.5
        a, bb = (s, b) if skill_is_a else (b, s)
        pair = f"pair{made:02d}"
        key[pair] = {
            "eval": name,
            "A": "skill" if skill_is_a else "baseline",
            "B": "baseline" if skill_is_a else "skill",
        }

        (out_dir / f"{pair}.md").write_text(
            f"# {pair}\n\n"
            "Two AI coding assistants each needed something from the person they were "
            "working for, and each produced what is below.\n\n"
            f"**Judge on this and nothing else:** {criterion}\n\n"
            "Ignore length, tone and formatting except where they change how easy this is "
            "to answer well. Neither option is a reference answer.\n\n"
            f"## Option A\n\n{a}\n\n---\n\n## Option B\n\n{bb}\n\n---\n\n"
            "Answer with exactly two lines and nothing else:\n"
            "VERDICT: A or B or TIE\n"
            "REASON: one sentence\n"
        )

    (out_dir / "_key.json").write_text(json.dumps(key, indent=2))
    print(f"{made} bundles -> {out_dir}")
    for s in skipped:
        print(f"  skipped: {s}")
    print(f"key withheld from judges at {out_dir / '_key.json'}")


if __name__ == "__main__":
    main()
