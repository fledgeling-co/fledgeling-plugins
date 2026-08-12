#!/usr/bin/env bash
# Run eval cases through both arms: with the skill loaded, and without.
#
# The baseline is the honest comparison — the same prompt, no skill — because the
# question this set answers is "does this skill earn its context window", and only
# a no-skill arm can answer it. Each arm runs in a fresh process so neither can
# see the other.
#
#   ./run-evals.sh BMW-02 BMW-04 ...   # named cases
#   ./run-evals.sh --all               # every case still marked "authored"
set -uo pipefail
cd "$(dirname "$0")/.."
OUT="evals/runs"; mkdir -p "$OUT"
SKILL_DIR="$PWD"
# Scratch cwd for the baseline arm: no skill, no references, no fixtures tree.
BASE_CWD="$(mktemp -d)"
trap 'rm -rf "$BASE_CWD"' EXIT
MODEL="${EVAL_MODEL:-claude-fable-5}"

cases=("$@")
if [ "${1:-}" = "--all" ]; then
  mapfile -t cases < <(python3 -c "
import json
d=json.load(open('evals/evals.json'))
print('\n'.join(c['id'] for c in d['cases'] if c.get('status')=='authored'))")
fi

for id in "${cases[@]}"; do
  prompt="$(python3 -c "
import json,sys
d=json.load(open('evals/evals.json'))
c=next((c for c in d['cases'] if c['id']=='$id'), None)
if not c: sys.exit('no case $id')
fx=c.get('fixture','')
import os
if 'tests/fixtures' in fx:
    fx = ' '.join(os.path.abspath(t) if 'tests/fixtures' in t else t for t in fx.split())
print(c['prompt'] + ('\n\nFixtures (read the images at these paths): ' + fx if 'tests/fixtures' in fx else '\n\nScenario: ' + fx))
print('\nAnswer in under 140 words.')")"
  [ -z "$prompt" ] && { echo "!! $id: no prompt"; continue; }

  echo "=== $id baseline ==="
  printf '%s\n' "$prompt" | (cd "$BASE_CWD" && claude --model "$MODEL" --effort high -p) > "$OUT/$id.baseline.txt" 2>&1
  if grep -qiE 'SKILL\.md|be-my-witness' "$OUT/$id.baseline.txt"; then
    echo "!! $id: BASELINE CONTAMINATED — it referenced the skill. Do not grade this case."
  fi
  tail -c 700 "$OUT/$id.baseline.txt"; echo

  echo "=== $id with-skill ==="
  { cat SKILL.md; printf '\n---\nThe above is a skill you have loaded. Follow it.\n\nTask: %s\n' "$prompt"; } \
    | claude --model "$MODEL" --effort high -p > "$OUT/$id.skill.txt" 2>&1
  tail -c 700 "$OUT/$id.skill.txt"; echo
done
