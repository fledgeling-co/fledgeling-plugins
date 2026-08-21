#!/usr/bin/env bash
# Probe every lane cheaply and say which are live.
#
# A lane is available when a probe says so, not when you remember it working.
# Each probe asks for one fixed string, so a wrong-model answer is visible and a
# lane that returns nothing is reported down rather than assumed fine.
#
#   lane_probe.sh            # all lanes
#   lane_probe.sh glm grok   # just these
set -uo pipefail
TIMEOUT="${LANE_PROBE_TIMEOUT:-180}"
PROMPT='Reply with exactly: LANE OK'
LANES=("$@"); [ ${#LANES[@]} -eq 0 ] && LANES=(gemini grok glm codex-terra codex-sol fable opus)

run() { perl -e 'alarm shift @ARGV; exec @ARGV' "$TIMEOUT" "$@" 2>&1; }
# Strip a SessionStart marker glyph; a claude -p one-shot inherits session hooks.
ok()  { printf '  %-13s \033[32mup\033[0m    %s\n' "$1" "$(echo "$2" | tr -d '\000-\037' | sed 's/^[^A-Za-z]*//' | head -c 60)"; }
down(){ printf '  %-13s \033[31mDOWN\033[0m  %s\n' "$1" "$(echo "$2" | tail -1 | head -c 100)"; }

for lane in "${LANES[@]}"; do
  case "$lane" in
    gemini) out=$(run agy --model gemini-3.7-flash-high -p "$PROMPT") ;;
    grok)   out=$(run grok -m grok-4.6 --effort xhigh -p "$PROMPT") ;;
    glm)    out=$(ANTHROPIC_BASE_URL=http://127.0.0.1:8858 \
                  ANTHROPIC_API_KEY=local-proxy-supplies-the-real-credential \
                  ANTHROPIC_CUSTOM_HEADERS="X-Perch-Binding: glm" \
                  run claude --effort high -p "$PROMPT") ;;
    fable)  out=$(run claude --model claude-fable-5 --effort high -p "$PROMPT") ;;
    opus)   out=$(run claude --model claude-opus-5 --effort xhigh -p "$PROMPT") ;;
    codex-terra|codex-sol)
      m=gpt-5.6-terra; e=high
      [ "$lane" = codex-sol ] && { m=gpt-5.6-sol; e=medium; }
      f=$(mktemp /tmp/lane-probe.XXXXXX.md)
      log=$(run codex exec -m "$m" -c model_reasoning_effort="$e" -s read-only \
                --skip-git-repo-check -o "$f" "$PROMPT" </dev/null)
      # The header prints correctly on a run that produced nothing, so the
      # output file is the evidence, not the flags that were accepted.
      if [ -s "$f" ]; then out=$(cat "$f"); else out="empty -o file — ${log}"; fi
      rm -f "$f" ;;
    *) down "$lane" "unknown lane"; continue ;;
  esac
  if echo "$out" | grep -qi 'LANE OK'; then ok "$lane" "$out"; else down "$lane" "$out"; fi
done
