#!/usr/bin/env bash
# slipway canary: scaffold representative module permutations into temp dirs and
# run the full gate on each. Template rot is the classic scaffolder failure
# (fresh create-turbo/next scaffolds have shipped broken); this makes "the
# templates still work today" a command. Run weekly (ship-armada daemon).
# Usage: canary.sh [--quick]   (--quick runs only the all-modules permutation)
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# An unrecognised flag used to fall straight through this test and scaffold every
# permutation, which is minutes of work and gigabytes of disk the caller did not
# ask for. A typo should cost nothing.
QUICK=0
case "${1:-}" in
  "")        ;;
  --quick)   QUICK=1 ;;
  -h|--help) echo "usage: canary.sh [--quick]"; exit 0 ;;
  *)         echo "canary.sh: unrecognised argument '$1'" >&2
             echo "usage: canary.sh [--quick]" >&2
             exit 2 ;;
esac

# Each permutation scaffolds a full monorepo into a temp dir. The loop removes
# its own, but only on the way past: interrupt the run and the current one
# survives, which is how 1.4GB was left behind in /var/folders once. The trap
# makes cleanup unconditional.
DEST=""
# An `if`, not an `&&` chain: the chain's false test became the script's exit
# status, so a run whose loop had already removed its last dir exited 1.
cleanup() { if [ -n "$DEST" ] && [ -d "$DEST" ]; then rm -rf "$DEST"; fi; }
trap cleanup EXIT INT TERM

PERMS=(
  "all:web,api,macos,ios,rn,tokens,data,auth,admin,push,waitlist,observability,rust"
  "saas:web,tokens,data,auth,admin"
  "native:macos,ios,rust"
  "site:web,tokens"
)
[ "$QUICK" = 1 ] && PERMS=("${PERMS[0]}")
fail=0
for perm in "${PERMS[@]}"; do
  name="${perm%%:*}"; modules="${perm#*:}"
  DEST="$(mktemp -d)"
  echo "== canary: $name ($modules)"
  # The scaffold's last line reports each step; the gate is the full one (lint,
  # typecheck, test, build, e2e smoke, swift/cargo where present), so a "gate: yes"
  # is the whole verdict for this permutation.
  if ! "$SCRIPT_DIR/scaffold.sh" --codename "canary$name" --display "Canary" \
       --description "slipway canary ($name)." --modules "$modules" --dest "$DEST" \
       > "$DEST/scaffold.log" 2>&1 || ! tail -3 "$DEST/scaffold.log" | grep -q "gate: yes"; then
    echo "   FAILED for $name; last lines of the scaffold log:"; tail -25 "$DEST/scaffold.log" | sed 's/^/     /'
    fail=1
  fi
  rm -rf "$DEST"
done
[ "$fail" = 0 ] && echo "slipway canary: all permutations healthy ($(date +%Y-%m-%d))" || { echo "slipway canary: FAILURES — fix the templates"; exit 1; }
