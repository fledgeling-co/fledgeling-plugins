#!/usr/bin/env bash
# run_evals.sh — run every eval in evals.json for both arms (new | old).
#
# Design notes (each one a paid-for lesson from the clarify harness):
# - Pass the brief's PATH via a prompt file, not inline: ~7KB as -p fails.
# - --strict-mcp-config keeps the child's context clean of session MCP servers.
# - Tool whitelist (no git, no network) enforces "eval agents never run git"
#   structurally rather than asking nicely.
# - Per-run fixture COPY so arms can't see each other's edits.
# - A run that produced no answer.md is a HARNESS FAILURE, not a skill result.
# - Same model both arms — the comparison is the skills, not the model.
set -uo pipefail

cd "$(dirname "$0")/.."          # plugin root (ship-pipeline)
PLUGIN_ROOT="$PWD"
EVALS="$PLUGIN_ROOT/evals/evals.json"
RUNS="$PLUGIN_ROOT/evals/runs/$(date +%Y%m%d-%H%M%S)"
MODEL="${EVAL_MODEL:-claude-sonnet-5}"
mkdir -p "$RUNS"

ids=$(python3 -c "import json;print('\n'.join(e['id'] for e in json.load(open('$EVALS'))['evals']))")

for id in $ids; do
  for arm in new old; do
    run_dir="$RUNS/$id-$arm"
    mkdir -p "$run_dir"
    # fresh fixture copy per run
    cp -R "$PLUGIN_ROOT/evals/fixtures/scribble" "$run_dir/fixture"

    python3 - "$EVALS" "$id" "$arm" "$PLUGIN_ROOT" "$run_dir" <<'PYEOF'
import json, sys
evals, eid, arm, root, run_dir = sys.argv[1:6]
e = next(x for x in json.load(open(evals))['evals'] if x['id'] == eid)
skills = e['skill_new'] if arm == 'new' else e['skill_old']
skill_paths = "\n".join(f"  {root}/{p}" for p in skills)
prompt = f"""You are an agent following a skill. Read these skill/reference documents COMPLETELY, in order, before doing anything else — they are your entire procedure and authority:
{skill_paths}

Your working repository is the fixture at {run_dir}/fixture (treat it as the target repo; its docs/ tree is the pipeline's artifact store). Do not run git and do not access the network.

<task>
{e['task']}
</task>

Write your complete final output to {run_dir}/answer.md. Deliver what was asked, at the scope intended; make routine judgment calls yourself. Where the skill's procedure requires a tool you do not have (a tracker MCP, a browser, an external CLI), state exactly what you would run and what its output gates — do not pretend it ran."""
open(f"{run_dir}/prompt.txt","w").write(prompt)
PYEOF

    echo "[$(date +%H:%M:%S)] $id/$arm starting"
    ( cd "$run_dir/fixture" && perl -e 'alarm shift @ARGV; exec @ARGV' 900 \
        claude -p "Read and follow the instructions in $run_dir/prompt.txt" \
        --model "$MODEL" --strict-mcp-config \
        --allowedTools "Read,Write,Edit,Glob,Grep" \
        > "$run_dir/stdout.log" 2> "$run_dir/stderr.log" )
    rc=$?
    if [[ ! -s "$run_dir/answer.md" ]]; then
      echo "RUN-FAILED (rc=$rc, no answer.md)" > "$run_dir/RUN-FAILED"
      echo "[$(date +%H:%M:%S)] $id/$arm RUN-FAILED"
    else
      echo "[$(date +%H:%M:%S)] $id/$arm done ($(wc -l < "$run_dir/answer.md") lines)"
    fi
  done
done

echo "runs complete: $RUNS"
