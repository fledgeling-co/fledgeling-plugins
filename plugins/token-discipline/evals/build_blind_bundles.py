#!/usr/bin/env python3
"""Build blind A/B bundles from real paired diolog-swe-bench transcripts.

Judges never see which arm produced which side, never see the skill files, and never see the
benchmark's own grade. Order is seeded-random per pair so 'A' carries no information.

Usage: build_blind_bundles.py <out_dir> [n_pairs]
"""
import json
import os
import random
import sys
from pathlib import Path

RUNS = Path.home() / "Dev/diolog-swe-bench/results/runs"
PURE = "__claude__claude-opus-5__xhigh__"
CAVE = "__claude__claude-opus-5-caveman__xhigh__"
SEED = 20260809


def final_text(run_dir: Path) -> str | None:
    p = run_dir / "transcript-raw.json"
    if not p.exists():
        return None
    try:
        j = json.loads(p.read_text())
    except Exception:
        return None
    if isinstance(j, list):
        j = next((e for e in reversed(j) if isinstance(e, dict) and e.get("result")), {})
    if not isinstance(j, dict):
        return None
    t = j.get("result")
    return t if isinstance(t, str) and len(t.strip()) > 200 else None


def collect(marker: str) -> dict[str, str]:
    """taskId -> final text, newest run wins."""
    out: dict[str, str] = {}
    for d in sorted(RUNS.iterdir()):
        if marker not in d.name:
            continue
        task = d.name.split("__", 1)[0]
        if task in out:
            continue
        t = final_text(d)
        if t:
            out[task] = t
    return out


def main() -> None:
    out_dir = Path(sys.argv[1])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    out_dir.mkdir(parents=True, exist_ok=True)

    pure, cave = collect(PURE), collect(CAVE)
    shared = sorted(set(pure) & set(cave))
    rng = random.Random(SEED)
    rng.shuffle(shared)
    picked = shared[:n]

    key = {}
    for i, task in enumerate(picked, 1):
        # Seeded coin decides which arm is shown as A.
        cave_is_a = rng.random() < 0.5
        a, b = (cave[task], pure[task]) if cave_is_a else (pure[task], cave[task])
        key[f"pair{i:02d}"] = {
            "task": task,
            "A": "caveman" if cave_is_a else "pure",
            "B": "pure" if cave_is_a else "caveman",
        }
        (out_dir / f"pair{i:02d}.md").write_text(
            f"# Pair {i:02d}\n\n"
            "Two AI engineering assistants completed the SAME software task in the same repo. "
            "Below is each one's final report to the engineer who asked for the work.\n\n"
            "Judge ONLY on how useful the report is to that engineer: does it say what was "
            "actually done, surface problems honestly, flag uncertainty where it exists, and give "
            "them what they need to trust and act on the result?\n\n"
            "Ignore length, tone and formatting except where they change usefulness.\n\n"
            f"## Response A\n\n{a}\n\n---\n\n## Response B\n\n{b}\n\n---\n\n"
            "Answer with exactly two lines and nothing else:\n"
            "VERDICT: A or B or TIE\n"
            "REASON: one sentence\n"
        )

    (out_dir / "_key.json").write_text(json.dumps(key, indent=2))
    print(f"{len(picked)} bundles -> {out_dir}")
    print(f"key withheld from judges at {out_dir/'_key.json'}")


if __name__ == "__main__":
    main()
