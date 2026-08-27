#!/usr/bin/env python3
"""
run_blind_panel.py — execute the blind quality panel across 3 independent judge families:
1. OpenAI gpt-5.6-sol (via codex exec)
2. xAI grok-4.6 (via grok CLI or cursor-agent)
3. Anthropic fable-5 (via claude CLI)
"""

import json
import os
import pathlib
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = pathlib.Path("/tmp/luke-evals")
BUNDLES_DIR = BASE_DIR / "bundles"
VERDICTS_DIR = BASE_DIR / "verdicts"
VERDICTS_DIR.mkdir(parents=True, exist_ok=True)

EVALS_JSON = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-luke-content/evals/evals.json")
evals_data = json.load(open(EVALS_JSON))["evals"]

def run_codex_judge(eid):
    bundle_file = BUNDLES_DIR / f"{eid}.md"
    out_file = VERDICTS_DIR / f"{eid}.codex.md"
    log_file = VERDICTS_DIR / f"{eid}.codex.log"
    if out_file.exists() and out_file.stat().st_size > 50:
        return "codex", eid, True

    prompt = f"Read the judging bundle at {bundle_file} and deliver your verdict."
    cmd = (f"perl -e 'alarm shift @ARGV; exec @ARGV' 900 "
           f"codex exec -m gpt-5.6-sol -c model_reasoning_effort=\"high\" "
           f"-s read-only -o {out_file} \"{prompt}\" < /dev/null > {log_file} 2>&1")
    subprocess.run(cmd, shell=True)
    return "codex", eid, out_file.exists()

def run_grok_judge(eid):
    bundle_file = BUNDLES_DIR / f"{eid}.md"
    out_file = VERDICTS_DIR / f"{eid}.grok.md"
    log_file = VERDICTS_DIR / f"{eid}.grok.log"
    if out_file.exists() and out_file.stat().st_size > 50:
        return "grok", eid, True

    prompt = bundle_file.read_text()
    # Try grok CLI first, fallback cursor-agent
    p_file = VERDICTS_DIR / f"prompt_grok_{eid}.txt"
    p_file.write_text(prompt)
    cmd = (f"perl -e 'alarm shift @ARGV; exec @ARGV' 900 "
           f"grok -m grok-4.6 --effort xhigh -p \"$(cat {p_file})\" < /dev/null > {out_file} 2> {log_file}")
    res = subprocess.run(cmd, shell=True)
    if not out_file.exists() or out_file.stat().st_size < 30:
        # Fallback to cursor-agent
        cmd = f"cursor-agent -p --force --model grok-4.6 \"$(cat {p_file})\" < /dev/null > {out_file} 2> {log_file}"
        subprocess.run(cmd, shell=True)
    return "grok", eid, out_file.exists()

def run_fable_judge(eid):
    bundle_file = BUNDLES_DIR / f"{eid}.md"
    out_file = VERDICTS_DIR / f"{eid}.fable.md"
    log_file = VERDICTS_DIR / f"{eid}.fable.log"
    if out_file.exists() and out_file.stat().st_size > 50:
        return "fable", eid, True

    cmd = f"claude --model claude-fable-5 --effort high -p \"$(cat {bundle_file})\" --strict-mcp-config < /dev/null > {out_file} 2> {log_file}"
    subprocess.run(cmd, shell=True)
    return "fable", eid, out_file.exists()

def main():
    print("=== Step 3: Dispatching Blind Judging Panel ===")
    tasks = []
    for e in evals_data:
        eid = e["id"]
        tasks.append((run_codex_judge, eid))
        tasks.append((run_grok_judge, eid))
        tasks.append((run_fable_judge, eid))

    print(f"Dispatching {len(tasks)} judge evaluations...")
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(fn, eid) for fn, eid in tasks]
        for f in futures:
            lane, eid, success = f.result()
            print(f"[{lane}] Eval {eid}: {'SUCCESS' if success else 'FAILED'}")

if __name__ == "__main__":
    main()
