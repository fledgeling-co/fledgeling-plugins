#!/usr/bin/env bash
# slipway canary: scaffold representative module permutations into temp dirs and
# run the full gate on each. Template rot is the classic scaffolder failure
# (fresh create-turbo/next scaffolds have shipped broken); this makes "the
# templates still work today" a command. Run weekly (ship-armada daemon).
# Usage: canary.sh [--quick]   (--quick runs only the all-modules permutation)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PERMS=(
  "all:web,api,macos,ios,rn,tokens,data,auth,admin,push,waitlist,rust"
  "saas:web,tokens,data,auth,admin"
  "native:macos,ios,rust"
  "site:web,tokens"
)
[ "${1:-}" = "--quick" ] && PERMS=("${PERMS[0]}")
fail=0
for perm in "${PERMS[@]}"; do
  name="${perm%%:*}"; modules="${perm#*:}"
  DEST="$(mktemp -d)"
  echo "== canary: $name ($modules)"
  if ! "$SCRIPT_DIR/scaffold.sh" --codename "canary$name" --display "Canary"       --description "slipway canary ($name)." --modules "$modules"       --dest "$DEST" 2>&1 | tail -2 | grep -q "gate(typecheck+build): yes\|install: skipped"; then
    echo "   scaffold/gate FAILED for $name"; fail=1
  fi
  case ",$modules," in *,web,*|*,api,*|*,tokens,*)
    (cd "$DEST/canary$name" && pnpm turbo run lint --output-logs=errors-only >/dev/null 2>&1) || { echo "   lint FAILED for $name"; fail=1; };;
  esac
  rm -rf "$DEST"
done
[ "$fail" = 0 ] && echo "slipway canary: all permutations healthy ($(date +%Y-%m-%d))" || { echo "slipway canary: FAILURES — fix the templates"; exit 1; }
