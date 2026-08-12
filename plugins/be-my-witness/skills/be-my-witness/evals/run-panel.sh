#!/usr/bin/env bash
# C4 — the blind panel.
#
# Judges see two anonymised answers to the same question and are never told that a
# skill exists, let alone which arm used it. Arm order is FLIPPED on half the cases,
# because position bias is the failure this whole skill is about and a panel that
# ignores it would be measuring its own ordering.
#
# Judges run from a scratch cwd for the same reason the baseline arm does: an agent
# with file tools and the skill in its working directory is not blind to it.
set -uo pipefail
cd "$(dirname "$0")/.."
OUT="evals/panel"; mkdir -p "$OUT"
JUDGE_CWD="$(mktemp -d)"; trap 'rm -rf "$JUDGE_CWD"' EXIT

# Heterogeneous families: a different Claude and a different model family entirely.
for id in "$@"; do
  b="evals/runs/$id.baseline.txt"; k="evals/runs/$id.skill.txt"
  [ -f "$b" ] && [ -f "$k" ] || { echo "!! $id: missing an arm"; continue; }

  # Flip the presentation order on odd-numbered cases.
  n="${id##*-}"; n="${n#0}"
  if [ $((n % 2)) -eq 1 ]; then first="$k"; second="$b"; map="A=skill B=baseline";
  else first="$b"; second="$k"; map="A=baseline B=skill"; fi

  q="$(python3 -c "
import json
d=json.load(open('evals/evals.json'))
c=next(c for c in d['cases'] if c['id']=='$id')
print(c['prompt'])
print()
print('The reviewer was judging a UI screenshot. Assertions the answer should satisfy:')
for a in c['assertions']: print(' -', a)")"

  prompt="$(printf 'Two reviewers answered the same question about a UI screenshot. Judge which answer is more useful and more honest to whoever has to act on it.\n\n=== THE QUESTION ===\n%s\n\n=== ANSWER A ===\n%s\n\n=== ANSWER B ===\n%s\n\nReply with exactly one line: WINNER: A, WINNER: B, or WINNER: TIE, then at most three sentences of reason.\n' \
      "$q" "$(cat "$first")" "$(cat "$second")")"

  echo "=== $id · $map ==="
  printf '%s\n' "$prompt" | (cd "$JUDGE_CWD" && claude --model claude-fable-5 --effort high -p) > "$OUT/$id.judge-claude.txt" 2>&1
  echo "  claude: $(grep -oiE 'WINNER: *(A|B|TIE)' "$OUT/$id.judge-claude.txt" | head -1)  [$map]"

  printf '%s\n' "$prompt" > "$JUDGE_CWD/p.txt"
  perl -e 'alarm shift @ARGV; exec @ARGV' 420 \
    codex exec -m gpt-5.6-sol -c model_reasoning_effort="high" -s read-only \
    -o "$OUT/$id.judge-codex.md" "$(cat "$JUDGE_CWD/p.txt")" < /dev/null \
    > "$OUT/$id.judge-codex.log" 2>&1
  echo "  codex:  $(grep -oiE 'WINNER: *(A|B|TIE)' "$OUT/$id.judge-codex.md" 2>/dev/null | head -1)  [$map]"
done
