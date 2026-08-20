#!/usr/bin/env bash
# prepush-scan.sh — the mechanical half of the prepush gate.
#
# Scans the OUTGOING diff (unpushed commits) for the blocker classes that are decidable by pattern
# rather than by judgement, and prints them as `RULE<TAB>file:line<TAB>note` rows. The judgement
# classes — broken contracts, weakened guard tests, auth and validation regressions, destructive
# data changes — are yours; see references/prepush.md.
#
#   ./prepush-scan.sh              # auto-resolve the outgoing range
#   ./prepush-scan.sh --base main  # pin the base
#
# Never prints a matched secret value. A hit is reported by file, line and rule only, because the
# output of this script reaches a report and a committed secret is burned even after deletion.
#
# Exit 0 = nothing found · 1 = at least one hit · 2 = could not run.

set -uo pipefail
BASE=""
while [ $# -gt 0 ]; do
  case "$1" in
    --base) BASE="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,16p' "$0"; exit 0 ;;
    *) echo "prepush-scan.sh: unknown argument: $1" >&2; exit 2 ;;
  esac
done

git rev-parse --git-dir >/dev/null 2>&1 || { echo "prepush-scan.sh: not a git repository" >&2; exit 2; }

if [ -z "$BASE" ]; then
  if git rev-parse --verify --quiet '@{push}' >/dev/null 2>&1; then BASE='@{push}'
  elif git rev-parse --verify --quiet '@{upstream}' >/dev/null 2>&1; then BASE='@{upstream}'
  else
    db="$(git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||')"
    [ -z "$db" ] && for b in main master; do git rev-parse --verify --quiet "refs/heads/$b" >/dev/null && db="$b" && break; done
    [ -z "$db" ] && { echo "prepush-scan.sh: no upstream and no default branch — pass --base" >&2; exit 2; }
    BASE="$db"
  fi
fi

RANGE="$BASE..HEAD"
COMMITS="$(git rev-list --count "$RANGE" 2>/dev/null || echo 0)"
if [ "$COMMITS" -eq 0 ]; then
  echo "# outgoing range $RANGE — 0 commits. Nothing to gate."
  exit 0
fi

echo "# outgoing range: $RANGE ($COMMITS commit(s))"
echo "# rows are RULE<TAB>file:line<TAB>note — values are never printed"
# Added lines only, with their file and new-file line number. Deletions cannot introduce a leak.
ADDED="$(git diff -U0 "$RANGE" 2>/dev/null | awk '
  /^\+\+\+ b\// { f=substr($0,7); next }
  /^@@/ { split($3,a,","); ln=a[1]; sub(/^\+/,"",ln); ln+=0; next }
  /^\+/ && !/^\+\+\+/ { print f "\t" ln "\t" substr($0,2); ln++ }
')"

scan() { # scan <rule> <extended-regex> <note>
  printf '%s\n' "$ADDED" | grep -vE '^[[:space:]]*$' | while IFS=$'\t' read -r f ln body; do
    printf '%s' "$body" | grep -qiE "$2" && printf '%s\t%s:%s\t%s\n' "$1" "$f" "$ln" "$3"
  done
}

OUT="$(mktemp)"; trap 'rm -f "$OUT"' EXIT
add() { [ -n "$1" ] && printf '%s\n' "$1" >> "$OUT"; return 0; }

# 1. Secrets — shape-based, deliberately noisy; a false positive costs one glance, a miss is a rotation.
add "$(scan SECRET-aws-key '\bAKIA[0-9A-Z]{16}\b' 'AWS access key id shape')"
add "$(scan SECRET-private-key 'BEGIN [A-Z ]*PRIVATE KEY' 'PEM private key block')"
add "$(scan SECRET-provider-token '\b(sk_live_|sk_test_|rk_live_|ghp_|gho_|ghs_|github_pat_|xox[baprs]-|sk-ant-|AIza[0-9A-Za-z_-]{20})' 'provider token prefix')"
add "$(scan SECRET-conn-string '(mongodb(\+srv)?|postgres(ql)?|mysql|redis|amqp)://[^/[:space:]]*:[^@[:space:]]+@' 'connection string with inline password')"
add "$(scan SECRET-assigned-literal '(password|passwd|secret|api[_-]?key|access[_-]?token|private[_-]?key|client[_-]?secret)["'"'"']?\s*[:=]\s*["'"'"'][^"'"'"'${}<>]{12,}' 'credential assigned a literal — confirm it is not a placeholder')"

# 2. Debug leftovers
add "$(scan DEBUG-debugger '(^|[^A-Za-z0-9_])debugger\s*;' 'debugger statement')"
add "$(scan DEBUG-test-focus '\b(describe|it|test|context)\.(only|skip)\s*\(|\bit\.todo\s*\(|\bfdescribe\s*\(|\bfit\s*\(|\bxit\s*\(' 'focused or skipped test')"
add "$(scan DEBUG-console '\bconsole\.(log|debug|dir)\s*\(' 'console output — a blocker in server code, a note elsewhere')"

# 3. Accidental payload
NEWFILES="$(git diff --name-only --diff-filter=A "$RANGE" 2>/dev/null)"
PAYLOAD="$(mktemp)"
printf '%s\n' "$NEWFILES" | grep -vE '^$' | while read -r f; do
  case "$f" in
    *.env|*.env.*|*.pem|*.p12|*.pfx|*.keystore|*.jks|id_rsa*|*.mobileprovision|*credentials*|*.p8)
      printf 'PAYLOAD-credential-file\t%s\tcredential-shaped file newly tracked\n' "$f" ;;
    *.zip|*.tar|*.tar.gz|*.tgz|*.jar|*.dmg|*.exe|*.so|*.dylib|*.mp4|*.mov|*.psd|*.sketch)
      printf 'PAYLOAD-binary\t%s\tbinary newly tracked\n' "$f" ;;
    */dist/*|*/build/*|*/.next/*|*/out/*|*/coverage/*|*/node_modules/*|*/__pycache__/*)
      printf 'PAYLOAD-generated\t%s\tgenerated directory newly tracked\n' "$f" ;;
  esac
  sz=$(git cat-file -s "$(git rev-parse "HEAD:$f" 2>/dev/null)" 2>/dev/null || echo 0)
  [ "$sz" -gt 1048576 ] && printf 'PAYLOAD-large\t%s\t%s bytes\n' "$f" "$sz"
done > "$PAYLOAD" 2>/dev/null
add "$(cat "$PAYLOAD" 2>/dev/null)"; rm -f "$PAYLOAD"

# Lockfile churn with no manifest change is a real tell for a bad merge or a stray install.
LOCKS="$(git diff --name-only "$RANGE" 2>/dev/null | grep -cE '(package-lock\.json|pnpm-lock\.yaml|yarn\.lock|bun\.lockb|Cargo\.lock|poetry\.lock|uv\.lock)$' || true)"
MANIFESTS="$(git diff --name-only "$RANGE" 2>/dev/null | grep -cE '(package\.json|Cargo\.toml|pyproject\.toml|go\.mod)$' || true)"
if [ "${LOCKS:-0}" -gt 0 ] && [ "${MANIFESTS:-0}" -eq 0 ]; then
  add "$(printf 'PAYLOAD-lock-drift\t(lockfile)\tlockfile changed with no manifest change')"
fi

# 4. Notes, not blockers.
add "$(scan NOTE-marker '(^|[^A-Za-z0-9_])(TODO|FIXME|HACK|XXX)\b' 'marker added in the range')"

sort -u "$OUT" | grep -vE '^$' || true
COUNT="$(sort -u "$OUT" | grep -cvE '^$' || true)"
echo "# ${COUNT:-0} mechanical hit(s). Judgement classes 4-7 in prepush.md need your reading; see prepush.md."
[ "${COUNT:-0}" -gt 0 ] && exit 1 || exit 0
