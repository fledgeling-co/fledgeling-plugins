#!/bin/bash
cd "$(dirname "$0")"; C=/Volumes/LLMs/Dev/fledgeling-plugins/plugins/clarify/skills/clarify/scripts
GROK_M=$(python3 $C/latest_model.py grok 2>/dev/null); AGY_M=$(python3 $C/latest_model.py gemini 2>/dev/null); CODEX=$(python3 $C/latest_model.py codex 2>/dev/null)
lane() { # name file
  f="$2"; base="${f%.txt}"; p="$(cat "$f")"
  case "$1" in
    sol)  ( cd /tmp && perl -e 'alarm shift @ARGV; exec @ARGV' 600 "$CODEX" exec -m gpt-6.2-sol -c model_reasoning_effort="high" -s read-only --skip-git-repo-check -o "$OLDPWD/$base.sol.md" "$p" < /dev/null > "$OLDPWD/$base.sol.log" 2>&1 ) ;;
    grok) ( cd /tmp && perl -e 'alarm shift @ARGV; exec @ARGV' 600 grok -m "$GROK_M" --effort high -p "$p" > "$OLDPWD/$base.grok.md" 2> "$OLDPWD/$base.grok.log" ) ;;
    wonder) ( cd /tmp && perl -e 'alarm shift @ARGV; exec @ARGV' 600 muse exec --model muse-wonder-1.0 --reasoning-effort high --disable-write --disable-shell --disable-web-tools --approval-mode untrusted --no-session-log --workspace /tmp "$p" < /dev/null > "$OLDPWD/$base.wonder.md" 2> "$OLDPWD/$base.wonder.log" ) ;;
  esac
}
export -f lane; export CODEX GROK_M AGY_M
for f in *.fwd.txt *.rev.txt; do for l in sol grok wonder; do echo "$l $f"; done; done | xargs -P 6 -L 1 bash -c 'lane "$0" "$1"'
echo "models: codex=$CODEX grok=$GROK_M"; wc -c *.md | tail -20
