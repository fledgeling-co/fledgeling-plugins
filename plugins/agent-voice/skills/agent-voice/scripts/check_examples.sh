#!/usr/bin/env bash
# check_examples.sh — hold this skill's own worked examples to its own gate.
#
# Every <output> block in references/registers/*.md is a claim about what the
# voice produces. This extracts each one and lints it at that register's format
# key. A worked example that fails the lint teaches the opposite of the rule
# beside it, and examples steer generation harder than rules do.
#
# Usage:  ./scripts/check_examples.sh          (from the skill directory)
# Exit 0 only when every extracted example is clean on the hard checks.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

LINT="python3 scripts/agent_voice_lint.py"
CONFIG="scripts/agent-voice-lint.json"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

declare -A FMT=(
  [terminal-reply]=reply
  [work-report]=report
  [commit-and-pr]=commit
  [review-comment]=review
  [written-doc]=doc
  [skill-and-instruction]=skill
  [subagent-brief]=brief
)

pass=0; fail=0

for file in references/registers/*.md; do
  base="$(basename "$file" .md)"
  fmt="${FMT[$base]:-doc}"
  # Split the file on <output> ... </output> and write each block out.
  n=0
  while IFS= read -r -d '' block; do
    n=$((n + 1))
    out="$TMP/$base-$n.md"
    printf '%s' "$block" > "$out"
    if $LINT --config "$CONFIG" --format "$fmt" "$out" > "$TMP/log" 2>&1; then
      pass=$((pass + 1))
      printf 'ok    %s example %d (%s)\n' "$base" "$n" "$fmt"
    else
      fail=$((fail + 1))
      printf 'FAIL  %s example %d (%s)\n' "$base" "$n" "$fmt"
      grep '^FAIL' "$TMP/log" | sed 's/^/        /'
    fi
  done < <(python3 - "$file" <<'PY'
import re, sys
text = open(sys.argv[1], encoding="utf-8").read()
for m in re.finditer(r"<output>\n(.*?)\n</output>", text, re.S):
    sys.stdout.write(m.group(1) + "\0")
PY
)
  [ "$n" -eq 0 ] && printf 'warn  %s has no <output> block\n' "$base"
done

printf '\n%d example(s) clean, %d failing\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
