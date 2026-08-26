#!/usr/bin/env python3
"""
run_evals_parallel.py — run remaining evals concurrently (capped at 4 workers)
"""

import json
import pathlib
import subprocess
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = pathlib.Path("/tmp/luke-evals")
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


def run_single(item):
    eval_item, arm = item
    eval_id = eval_item["id"]
    out_file = BASE_DIR / arm / f"{eval_id}.txt"
    if out_file.exists() and out_file.stat().st_size > 50:
        print(f"[{arm}] eval {eval_id} already exists ({out_file.stat().st_size} bytes)")
        return eval_id, arm, True

    brief_path = make_brief(eval_item, arm)
    print(f"[{arm}] Starting eval {eval_id}: {eval_item['name']}...")
    cmd = f"claude -p {brief_path} < /dev/null"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    out_file.write_text(res.stdout.strip())
    print(f"[{arm}] Finished eval {eval_id}: {eval_item['name']} ({len(res.stdout)} chars)")
    return eval_id, arm, True


def main():
    # Kill any sequential run first
    tasks = []
    for e in evals_data:
        tasks.append((e, "candidate"))
        tasks.append((e, "predecessor"))

    print(f"Running {len(tasks)} eval arms with max 4 workers...")
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run_single, tasks))
    print("All tasks finished:", len(results))


if __name__ == "__main__":
    main()
