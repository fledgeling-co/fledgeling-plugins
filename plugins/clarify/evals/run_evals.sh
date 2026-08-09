#!/usr/bin/env bash
# Run every eval in evals.json twice — once with the skill, once with nothing —
# and collect what each arm would have asked.
#
# The problem this works around: the skill's primary output is an
# AskUserQuestion tool call, and a headless runner has no user to answer it. So
# both arms are asked to WRITE the payload they would have sent, as JSON, and
# then stop. That makes the output lintable and judgeable. It is slightly
# artificial — the agent knows it is composing rather than calling — but both
# arms carry the artificiality equally, so the comparison stays fair. The
# gate evals depend on the *absence* of that file, which is why the prompt makes
# writing it conditional rather than mandatory.
#
#   ./run_evals.sh [outdir] [concurrency] [name-filter]
#
# Writes <outdir>/<eval-name>/{skill,baseline}/{payload.json,transcript.txt}.
# name-filter, if given, restricts the run to eval names containing it.
# Runs no git commands and spawns no agents of its own.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$HERE/../skills/clarify" && pwd)"
EVALS="$HERE/evals.json"
OUT="${1:-/tmp/clarify-evals/iteration-1}"
CONCURRENCY="${2:-6}"
FILTER="${3:-}"

mkdir -p "$OUT"
command -v claude >/dev/null || { echo "claude not on PATH" >&2; exit 1; }
command -v jq >/dev/null || { echo "jq not on PATH" >&2; exit 1; }

# Tools the runner is allowed. No git, no network, no push — the whitelist is
# what enforces "subagents never run git", rather than asking them not to.
ALLOWED='Read,Write,Edit,Glob,Grep,Bash(python3:*),Bash(ls:*),Bash(cat:*)'

# Run each child in its own process group so a superseded run can be killed as a
# group rather than orphaning children. setsid is Linux-only; macOS needs the
# perl fallback. Neither is fatal — plain exec still works, it is just less
# cleanly killable.
if command -v setsid >/dev/null; then
  NEWPG=(setsid)
elif command -v perl >/dev/null; then
  NEWPG=(perl -MPOSIX -e 'POSIX::setsid(); exec @ARGV' --)
else
  NEWPG=()
fi

harness_note() {
  cat <<'EOF'

---
HARNESS NOTE — how to deliver your answer in this environment.

There is no interactive user here, so you cannot call AskUserQuestion.

If, working normally, you WOULD ask the user something before proceeding: write
the exact payload you would have sent to the file named below, as JSON matching
the AskUserQuestion tool's input schema:

  {"questions":[{"question":"...","header":"...","multiSelect":false,
    "options":[{"label":"...","description":"..."}]}]}

If you would NOT ask anything, do not create that file. Do the task instead and
say what you decided.

Either way, write your normal user-facing response as text. Deliver what was
asked, at the scope intended.

PAYLOAD FILE: __PAYLOAD__
EOF
}

run_arm() {
  local name="$1" prompt="$2" arm="$3" fixture="$4"
  local dir="$OUT/$name/$arm"
  mkdir -p "$dir"
  local payload="$dir/payload.json" brief="$dir/brief.txt"

  # A fixture is copied per-arm so the two arms cannot see each other's edits.
  local workdir="$dir/work"
  mkdir -p "$workdir"
  if [ -n "$fixture" ] && [ "$fixture" != "null" ] && [ -d "$HERE/$fixture" ]; then
    cp -R "$HERE/$fixture/." "$workdir/"
  fi

  {
    printf '%s\n' "$prompt"
    harness_note | sed "s#__PAYLOAD__#$payload#"
    if [ "$arm" = "skill" ]; then
      printf '\nBefore answering, read and follow the skill at: %s/SKILL.md\n' "$SKILL_DIR"
    fi
  } > "$brief"

  # Pass the brief's PATH, not its text: ~7KB as a -p argument fails
  # deterministically with "Prompt is too long".
  # --strict-mcp-config keeps the child's context clean of this session's MCP
  # servers, which otherwise load their tool definitions into every child.
  ( cd "$workdir" && "${NEWPG[@]}" claude -p "Read $brief and do what it says." \
      --strict-mcp-config \
      --allowedTools "$ALLOWED" \
      > "$dir/transcript.txt" 2>"$dir/stderr.txt" )

  # A run that produced nothing is a harness failure, not a "did not ask".
  local asked="no"
  [ -f "$payload" ] && asked="yes"
  [ -s "$dir/transcript.txt" ] || asked="RUN-FAILED"
  printf '%s\t%s\tasked=%s\n' "$name" "$arm" "$asked"
}

echo "skill:    $SKILL_DIR"
echo "out:      $OUT"
echo "parallel: $CONCURRENCY"
echo

n=$(jq '.evals | length' "$EVALS")
for i in $(seq 0 $((n - 1))); do
  name=$(jq -r ".evals[$i].name" "$EVALS")
  [ -n "$FILTER" ] && [[ "$name" != *"$FILTER"* ]] && continue
  prompt=$(jq -r ".evals[$i].prompt" "$EVALS")
  fixture=$(jq -r ".evals[$i].cwd // \"\"" "$EVALS")
  for arm in skill baseline; do
    while [ "$(jobs -rp | wc -l)" -ge "$CONCURRENCY" ]; do sleep 2; done
    run_arm "$name" "$prompt" "$arm" "$fixture" &
  done
done
wait

echo
echo "=== asked / did not ask ==="
for d in "$OUT"/*/; do
  name=$(basename "$d")
  for arm in skill baseline; do
    if [ ! -s "$d/$arm/transcript.txt" ]; then
      printf '%-45s %-9s RUN-FAILED  %s\n' "$name" "$arm" "$(head -1 "$d/$arm/stderr.txt" 2>/dev/null)"
    elif [ -f "$d/$arm/payload.json" ]; then
      lint=$(python3 "$SKILL_DIR/scripts/lint_questions.py" "$d/$arm/payload.json" >/dev/null 2>&1 && echo lint-clean || echo lint-fail)
      printf '%-45s %-9s ASKED       %s\n' "$name" "$arm" "$lint"
    else
      printf '%-45s %-9s no-ask\n' "$name" "$arm"
    fi
  done
done
echo
echo "done -> $OUT"
