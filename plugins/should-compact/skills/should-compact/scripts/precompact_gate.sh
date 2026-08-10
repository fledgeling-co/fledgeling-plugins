#!/usr/bin/env bash
#
# precompact_gate.sh — the PreCompact hook body for should-compact.
#
# Claude Code fires PreCompact immediately before it summarises, on both triggers, and hands the
# hook a JSON object on stdin: { session_id, transcript_path, trigger, custom_instructions }.
# What this script does with its exit code is the whole mechanism, and the contract is verified
# against Claude Code 2.1.226 rather than taken from documentation:
#
#   exit 2                     compaction is BLOCKED. The reason is read from STDERR.
#   exit 0 + {"decision":"block","reason":"…"} on stdout
#                              also blocked.
#   exit 0 + plain text on stdout
#                              the text becomes `newCustomInstructions` and compaction proceeds.
#                              Plain text, not JSON: the raw stdout IS the instruction string, so
#                              an envelope is handed to the summariser verbatim.
#   exit 1                     a WARNING. Compaction proceeds anyway. This is the trap — it looks
#                              like a UNIX abort and is not one, so this script never exits 1.
#
# FAILS OPEN. Every error path exits 0 with empty stdout, which is exactly today's behaviour: the
# compaction happens with Claude Code's own prompt. A gate that fails closed would be a gate that
# can wedge a session it was supposed to protect.
#
# NEVER VETOES AT THE WALL. Automatic compaction fires at a median 99.8% of the window (n=235
# events), so by the time the trigger arrives there is almost no runway left. Blocking there does
# not buy a better moment, it buys a hard overflow. Below MIN_HEADROOM_TOKENS the gate scores,
# logs, and lets the compaction through with the score attached.

set -uo pipefail

SCORER="${SHOULD_COMPACT_SCORER:-}"          # command that reads the hook JSON and prints a score
THRESHOLD="${SHOULD_COMPACT_THRESHOLD:-4}"   # below this, veto
MIN_HEADROOM_TOKENS="${SHOULD_COMPACT_MIN_HEADROOM:-40000}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

payload="$(cat || true)"

# Everything below is best-effort. `jq` is not assumed.
field() {
  printf '%s' "$payload" | sed -n "s/.*\"$1\"[[:space:]]*:[[:space:]]*\"\([^\"]*\)\".*/\1/p" | head -1
}
session="$(field session_id)"
transcript="$(field transcript_path)"
[ -n "$session" ] || session="unknown"

# No scorer wired means this hook is installed but not armed. Say nothing, change nothing.
if [ -z "$SCORER" ]; then
  exit 0
fi

# Ask the scorer. It prints, on stdout, a JSON object carrying at least {"score": N}. A scorer that
# hangs must not hang the compaction, so it is bounded; a timeout is a failure to score, which
# fails open like every other failure here.
#
# BOUND IT PORTABLY. macOS ships no `timeout` — it is GNU coreutils, and a bare `timeout ...` there
# fails instantly with "command not found", which this script would read as "the scorer produced no
# score" and fail open on EVERY run. That is a gate that is installed, armed, and silently never
# fires, which is worse than one that is absent. `perl -e alarm` is the portable stand-in and perl
# ships with macOS; with neither available the scorer runs unbounded, which is honest — the risk is
# a slow compaction, not a wedged one, because Claude Code times the hook out itself.
_bounded() {
  local secs="$1"; shift
  if command -v timeout >/dev/null 2>&1; then
    timeout "$secs" "$@"
  elif command -v perl >/dev/null 2>&1; then
    perl -e 'alarm shift @ARGV; exec @ARGV' "$secs" "$@"
  else
    "$@"
  fi
}

verdict="$(printf '%s' "$payload" | _bounded "${SHOULD_COMPACT_TIMEOUT:-25}" sh -c "$SCORER" 2>/dev/null)" || verdict=""
score="$(printf '%s' "$verdict" | sed -n 's/.*"score"[[:space:]]*:[[:space:]]*\([0-9][0-9]*\).*/\1/p' | head -1)"
reason="$(printf '%s' "$verdict" | sed -n 's/.*"reasoning"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"
boundary="$(printf '%s' "$verdict" | sed -n 's/.*"boundary"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1)"

# Unscoreable → proceed. An absent score is not a low score.
case "$score" in
  ''|*[!0-9]*) exit 0 ;;
esac

if [ "$score" -ge "$THRESHOLD" ]; then
  verd="compact"
else
  verd="hold"
fi

# Headroom check. `transcript_path` is a JSONL file whose size tracks the conversation; ~3.5 chars
# per token is the same rough ratio the rest of this toolchain uses for an estimate it never
# presents as a measurement. When the file cannot be read, headroom is UNKNOWN, and unknown headroom
# is treated as no headroom — the safe direction is to let the compaction happen.
headroom_ok=0
if [ -n "$transcript" ] && [ -r "$transcript" ]; then
  bytes="$(wc -c < "$transcript" 2>/dev/null | tr -d ' ')"
  window="${SHOULD_COMPACT_WINDOW_TOKENS:-1000000}"
  if [ -n "$bytes" ]; then
    est=$(( bytes / 4 ))
    if [ $(( window - est )) -gt "$MIN_HEADROOM_TOKENS" ]; then headroom_ok=1; fi
  fi
fi

# Log every decision, including the ones that change nothing — a gate whose quiet turns are
# invisible cannot be told from a gate that never ran.
if [ -x "$HERE/session_log.py" ]; then
  "$HERE/session_log.py" append --session "$session" --score "$score" --verdict "$verd" \
    ${boundary:+--boundary "$boundary"} --note "${reason:-no reason given}" >/dev/null 2>&1 || true
fi

if [ "$score" -lt "$THRESHOLD" ] && [ "$headroom_ok" -eq 1 ]; then
  # Veto. The reason goes to STDERR, which is where Claude Code reads it from on exit 2.
  printf 'should-compact: %s/10 — %s\n' "$score" "${reason:-mid-task}" >&2
  exit 2
fi

# Proceed. Hand the summariser the pinned tier from the log as its custom instructions, plain text.
# This is the hand-off to compaction-quality: FACTS is already the verbatim tier it asks for,
# extracted while the session was fresh rather than reconstructed from the whole transcript.
if [ -x "$HERE/session_log.py" ]; then
  facts="$("$HERE/session_log.py" tail --session "$session" --narrative 0 2>/dev/null)" || facts=""
  if [ -n "$facts" ]; then
    printf 'Reproduce the following VERBATIM in a pinned block at the top of the summary, before section 1. These were recorded during the session, not reconstructed from it.\n\n%s\n' "$facts"
  fi
fi
exit 0
