#!/usr/bin/env bash
# check_package.sh — the whole gate for this skill, in one command.
#
# Four checks, each of which has caught a real defect during the build:
#   1. lint fixtures        — the lint still fires on what it claims to catch
#   2. worked examples      — every <output> block passes the register it teaches
#   3. shipped files        — this package obeys its own rules
#   4. quote verification   — every vendor quote is verbatim, not paraphrased
#
# Usage:  ./scripts/check_package.sh
# Exit 0 only when all four pass. Check the exit code, not the output: piping
# this through grep reports grep's status instead.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

LINT="python3 scripts/agent_voice_lint.py"
CONFIG="scripts/agent-voice-lint.json"
rc=0

hr() { printf '\n== %s\n' "$1"; }

hr "1. lint fixtures"
$LINT --self-test | tail -1 || rc=1

hr "2. worked examples"
./scripts/check_examples.sh | tail -1 || rc=1

hr "3. shipped files against their own rules"
# SKILL.md and the rule files are agent-read. evidence.md and the field guide are
# documentation a reader looks things up in, not rules a model executes.
fail=0
for f in SKILL.md references/agent-voice.md references/dialects.md references/registers/*.md; do
  if ! $LINT --config "$CONFIG" --format skill "$f" > /tmp/av-pkg.log 2>&1; then
    fail=$((fail + 1)); printf 'FAIL  %s\n' "$f"; grep '^FAIL' /tmp/av-pkg.log | sed 's/^/        /'
  fi
done
for f in references/evidence.md references/ai-writing-signs.md; do
  if ! $LINT --config "$CONFIG" --format doc "$f" > /tmp/av-pkg.log 2>&1; then
    fail=$((fail + 1)); printf 'FAIL  %s\n' "$f"; grep '^FAIL' /tmp/av-pkg.log | sed 's/^/        /'
  fi
done
if [ "$fail" -eq 0 ]; then echo "all shipped files clean on the hard checks"; else rc=1; fi

hr "4. vendor quotes verbatim"
SOURCES=()
for s in /tmp/anthro-prompting-claude-opus-5.md \
         /tmp/anthro-best-practices.md \
         /tmp/anthro-claude-prompting-best-practices.md \
         /tmp/anthro-migration-guide.md \
         "$HOME/.claude/commands/gemini-prompt-engineering.md"; do
  [ -f "$s" ] && SOURCES+=("$s")
done
if [ "${#SOURCES[@]}" -eq 0 ]; then
  echo "skipped: no vendor source copies on disk."
  echo "  Fetch them to re-run this check:"
  echo "    curl -sL https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5.md -o /tmp/anthro-prompting-claude-opus-5.md"
  echo "    curl -sL https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md -o /tmp/anthro-best-practices.md"
  echo "    curl -sL https://platform.claude.com/docs/en/about-claude/models/migration-guide.md -o /tmp/anthro-migration-guide.md"
  echo "  The Gemini corpus ships as a slash command, not a URL."
  echo "  A skipped check is not a passed one; this exits 1 so nothing reads it as green."
  rc=1
else
  python3 scripts/verify_quotes.py \
    references/evidence.md references/agent-voice.md references/dialects.md \
    references/registers/*.md --sources "${SOURCES[@]}" | tail -3 || rc=1
fi

printf '\n'
if [ "$rc" -eq 0 ]; then echo "PACKAGE: all four checks pass."; else echo "PACKAGE: at least one check failed."; fi
exit "$rc"
