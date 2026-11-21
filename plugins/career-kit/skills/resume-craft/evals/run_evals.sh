#!/bin/bash
# Run every eval twice: with the skill (told to read it) and without. Neutral cwd per run.
W="$(cd "$(dirname "$0")" && pwd)"; S="$1"; IT="${2:-iteration-1}"
python3 - "$S/evals/evals.json" "$W" "$IT" "$S" <<'PY'
import json,sys,os,shutil
ev=json.load(open(sys.argv[1])); W,IT,S=sys.argv[2:5]
jobs=[]
for e in ev["evals"]:
    for arm in ("with_skill","without_skill"):
        d=f"{W}/{IT}/{e['name']}/{arm}"; os.makedirs(d+"/outputs",exist_ok=True)
        for f in e["files"]: shutil.copy(f"{W}/fixture/{f}",d)
        p=e["prompt"]
        if arm=="with_skill":
            p=f"Use the skill at {S}/SKILL.md: read it first, read whichever of its reference files it points you to for this task, and follow it.\n\n"+p
        open(d+"/prompt.txt","w").write(p)
        jobs.append(d+("|"+S if arm=="with_skill" else "|"))
open(f"{W}/{IT}/jobs.txt","w").write("\n".join(jobs)+"\n")
PY
run_one() {
  d="${1%%|*}"; s="${1##*|}"; cd "$d" || exit 1
  extra=(); [ -n "$s" ] && extra=(--add-dir "$s")
  start=$(date +%s)
  perl -e 'alarm shift @ARGV; exec @ARGV' 1200 claude -p "$(cat prompt.txt)" \
    --permission-mode acceptEdits --disable-slash-commands --output-format json \
    --allowedTools Read Write Edit Glob Grep "Bash(python3:*)" "Bash(ls:*)" "Bash(wc:*)" \
    "${extra[@]}" < /dev/null > result.json 2> stderr.txt
  echo "{\"exit\": $?, \"duration_s\": $(( $(date +%s) - start ))}" > timing.json
}
export -f run_one
xargs -P 4 -I{} bash -c 'run_one "{}"' < "$W/$IT/jobs.txt"
echo "all runs finished"
