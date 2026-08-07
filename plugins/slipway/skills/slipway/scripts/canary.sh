#!/usr/bin/env bash
# slipway canary: scaffold every module into a temp dir and run the full gate.
# Template rot is the classic scaffolder failure (fresh create-turbo/next scaffolds
# have shipped broken); this makes "the templates still work today" a command.
# Run weekly (the ship-armada daemon is a good home). Exit 0 = templates healthy.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="$(mktemp -d)"
trap 'rm -rf "$DEST"' EXIT
"$SCRIPT_DIR/scaffold.sh" \
  --codename canary --display "Canary" --description "slipway canary run." \
  --modules web,api,macos,ios,rn,tokens,data,auth,admin,push,rust \
  --dest "$DEST" 2>&1 | tail -3
cd "$DEST/canary"
pnpm turbo run lint typecheck build --output-logs=errors-only
echo "slipway canary: templates healthy ($(date +%Y-%m-%d))"
