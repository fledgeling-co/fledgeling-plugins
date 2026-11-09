#!/usr/bin/env bash
# Refresh the bundled team-files snapshot in references/team-files/ from a
# team-files checkout. The snapshot is what scaffold.sh copies into every new
# project's docs/, so an installed plugin works without the checkout.
#
# DESIGN.md is never copied: it carries one product's aesthetic, and a new
# project gets its own DESIGN.md from design-md-from-website:design-md-from-website.
#
# Usage: sync-team-files.sh [<team-files-dir>]   (default ~/Dev/bella-team-files,
#        then /Volumes/LLMs/Dev/bella-team-files)
# After syncing, run scripts/check-conformance.py: a new or renamed section in
# the docs fails it until references/team-files-conformance.md maps it.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUT="$SCRIPT_DIR/../references/team-files"
FILES=(CODING_PRACTICES.md NEW_PROJECT_BEST_PRACTICES.md CLAUDE-STARTER.md)

SRC="${1:-}"
if [ -z "$SRC" ]; then
  for c in "$HOME/Dev/bella-team-files" "/Volumes/LLMs/Dev/bella-team-files"; do
    if [ -f "$c/CODING_PRACTICES.md" ] && [ -f "$c/NEW_PROJECT_BEST_PRACTICES.md" ]; then SRC="$c"; break; fi
  done
fi
[ -n "$SRC" ] || { echo "no team-files checkout found; pass its path" >&2; exit 1; }
for f in "${FILES[@]}"; do
  [ -f "$SRC/$f" ] || { echo "missing $SRC/$f" >&2; exit 1; }
done

mkdir -p "$OUT"
for f in "${FILES[@]}"; do cp "$SRC/$f" "$OUT/$f"; done
COMMIT="$(git -C "$SRC" rev-parse HEAD 2>/dev/null || echo unknown)"
python3 - "$OUT" "$COMMIT" "${FILES[@]}" <<'PY'
import hashlib, json, pathlib, sys, datetime
out, commit, files = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
json.dump({
    "source_commit": commit,
    "synced": datetime.date.today().isoformat(),
    "excluded": ["DESIGN.md"],
    "files": {f: hashlib.sha256((out / f).read_bytes()).hexdigest() for f in files},
}, open(out / "SOURCE.json", "w"), indent=2)
open(out / "SOURCE.json", "a").write("\n")
PY
echo "synced ${#FILES[@]} files from $SRC ($COMMIT) into $OUT"
