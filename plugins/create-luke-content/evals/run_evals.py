#!/usr/bin/env python3
"""
run_evals.py — execute all 9 evals across Candidate and Predecessor arms,
grade structural assertions, and prepare blind judging bundles.
"""

import json
import os
import pathlib
import subprocess
import time

BASE_DIR = pathlib.Path("/tmp/luke-evals")
BASE_DIR.mkdir(parents=True, exist_ok=True)
for d in ["candidate", "predecessor", "bundles", "verdicts", "briefs"]:
    (BASE_DIR / d).mkdir(parents=True, exist_ok=True)

REPO_ROOT = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins")
EVALS_JSON = REPO_ROOT / "plugins/create-luke-content/evals/evals.json"
evals_data = json.load(open(EVALS_JSON))["evals"]

FIXTURE_PATH = REPO_ROOT / "plugins/create-luke-content/evals/fixtures/digest-feature.md"
fixture_text = FIXTURE_PATH.read_text() if FIXTURE_PATH.exists() else ""

CANDIDATE_SKILL_DIR = REPO_ROOT / "plugins/create-luke-content/skills/create-luke-content"
PREDECESSOR_SKILL_DIR = REPO_ROOT / "plugins/create-luke-content/evals/predecessor"


def make_brief(eval_item, arm):
    eval_id = eval_item["id"]
    route = eval_item.get("route", "marketing")
    prompt = eval_item["prompt"]

    skill_dir = CANDIDATE_SKILL_DIR if arm == "candidate" else PREDECESSOR_SKILL_DIR

    brief = f"""<role>
You are executing the create-luke-content skill ({arm} arm) as Luke Rhodes, CTO and co-founder of Diolog.
</role>

<instructions>
1. Follow the skill instructions in {skill_dir}/SKILL.md exactly.
2. The request routes to the '{route}' persona. Read:
   - {skill_dir}/references/luke-voice.md (base voice)
"""
    if route == "marketing":
        brief += f"   - {skill_dir}/references/personas/marketing-content.md\n"
        if arm == "candidate":
            brief += f"   - {skill_dir}/references/evidence.md\n"
    elif route == "linkedin":
        brief += f"   - {skill_dir}/references/linkedin-engagement.md\n"
        brief += f"   - {skill_dir}/references/graphic-concepting.md\n"
    elif route == "slack":
        brief += f"   - {skill_dir}/references/personas/slack-informal.md\n"

    brief += f"""3. Self-check and lint your draft before delivering.
</instructions>

<context>
"""
    if "fixture" in eval_item:
        brief += f"Here is the contents of fixtures/digest-feature.md:\n\n{fixture_text}\n"

    brief += f"""</context>

<task>
{prompt}
</task>
"""
    brief_path = BASE_DIR / "briefs" / f"{arm}_{eval_id}.txt"
    brief_path.write_text(brief)
    return brief_path


def run_arm(eval_item, arm):
    eval_id = eval_item["id"]
    out_file = BASE_DIR / arm / f"{eval_id}.txt"
    if out_file.exists() and out_file.stat().st_size > 50:
        print(f"[{arm}] eval {eval_id} already cached ({out_file.stat().st_size} bytes)")
        return out_file.read_text()

    brief_path = make_brief(eval_item, arm)
    print(f"[{arm}] Running eval {eval_id}: {eval_item['name']}...")

    cmd = f"claude -p {brief_path} < /dev/null"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    output = res.stdout.strip()
    out_file.write_text(output)
    return output


def main():
    print("=== Step 1: Running all 9 evals across Candidate and Predecessor ===")
    for e in evals_data:
        run_arm(e, "candidate")
        run_arm(e, "predecessor")
    print("\nAll eval runs completed.")


if __name__ == "__main__":
    main()
