#!/usr/bin/env python3
"""
grade_assertions.py — evaluate every structural assertion in evals.json
across Candidate and Predecessor outputs, outputting grading.json.
"""

import json
import pathlib
import subprocess
import re

BASE_DIR = pathlib.Path("/tmp/luke-evals")
EVALS_JSON = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-luke-content/evals/evals.json")
evals_data = json.load(open(EVALS_JSON))["evals"]

def grade_eval(e):
    eid = e["id"]
    assertions = e["assertions"]

    c_text = (BASE_DIR / "candidate" / f"{eid}.txt").read_text()
    p_text = (BASE_DIR / "predecessor" / f"{eid}.txt").read_text()

    prompt = f"""You are an independent, objective evaluation grader.
Your job is to check each assertion against two candidate outputs (Candidate and Predecessor) for the eval:
Eval ID: {eid}
Eval Name: {e['name']}

Prompt:
{e['prompt']}

Assertions to check:
{json.dumps(assertions, indent=2)}

Candidate Output:
\"\"\"
{c_text}
\"\"\"

Predecessor Output:
\"\"\"
{p_text}
\"\"\"

For EACH assertion, evaluate whether Candidate PASSED or FAILED (with quoted evidence), and whether Predecessor PASSED or FAILED (with quoted evidence).

Output MUST be a valid JSON object matching this schema:
{{
  "eval_id": {eid},
  "eval_name": "{e['name']}",
  "candidate": [
    {{
      "assertion": "...",
      "passed": true/false,
      "evidence": "quoted excerpt proving pass/fail"
    }}
  ],
  "predecessor": [
    {{
      "assertion": "...",
      "passed": true/false,
      "evidence": "quoted excerpt proving pass/fail"
    }}
  ]
}}
Only return the raw JSON object, no markdown fences.
"""
    cmd = f"claude --model claude-fable-5 --effort high -p '{prompt}' < /dev/null"
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    raw = res.stdout.strip()
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except Exception as ex:
        print(f"Error parsing json for eval {eid}: {ex}")
        print("Raw was:", raw[:300])
        return None

def main():
    results = []
    for e in evals_data:
        print(f"Grading eval {e['id']}: {e['name']}...")
        r = grade_eval(e)
        if r:
            results.append(r)

    out_path = BASE_DIR / "grading.json"
    out_path.write_text(json.dumps(results, indent=2))
    print(f"\nGrading complete. Written to {out_path}")

if __name__ == "__main__":
    main()
