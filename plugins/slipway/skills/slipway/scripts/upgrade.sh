#!/usr/bin/env bash
# slipway upgrade <project-dir> [--apply]: bring a scaffolded project up to the
# CURRENT templates, Copier-style but honest about ownership:
#   - re-scaffolds the same config (from .slipway/manifest.json) into a temp dir
#   - files the user never modified (hash matches state.json) -> replaced
#   - files the user modified -> newer template written alongside as <file>.slipway-new
#     for a human merge; the user's file is never touched
#   - new template files -> added
# Default is a DRY RUN report; pass --apply to write. Never deletes user files.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="${1:?usage: upgrade.sh <project-dir> [--apply]}"
APPLY="${2:-}"
MANIFEST="$PROJECT/.slipway/manifest.json"
[ -f "$MANIFEST" ] || { echo "no $MANIFEST — not a slipway project" >&2; exit 1; }

read -r CODENAME DISPLAY MODULES MACOS_STYLE MACOS_DIST BUNDLE PORT_WEB <<EOF2
$(python3 -c "
import json; m=json.load(open('$MANIFEST'))
print(m['codename'], json.dumps(m['display']), ','.join(m['modules']), m.get('macos_style','window'), m.get('macos_dist','direct'), m['bundle_prefix'], m['ports']['web'])")
EOF2

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
"$SCRIPT_DIR/scaffold.sh" --codename "$CODENAME" --display "$(python3 -c "import json,sys;print(json.loads(sys.argv[1]))" "$DISPLAY")" \
  --modules "$MODULES" --macos-style "$MACOS_STYLE" --macos-dist "$MACOS_DIST" \
  --bundle-prefix "$BUNDLE" --port-web "$PORT_WEB" --dest "$TMP" --no-install >/dev/null 2>&1

python3 - "$PROJECT" "$TMP/$CODENAME" "$APPLY" <<'PY'
import hashlib, json, pathlib, shutil, sys
project, fresh = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
apply = sys.argv[3] == "--apply"
state = json.loads((project / ".slipway" / "state.json").read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
replaced, conflicted, added, skipped_deleted = [], [], [], []
for p in sorted(fresh.rglob("*")):
    if p.is_dir() or ".git/" in str(p):
        continue
    rel = str(p.relative_to(fresh))
    if rel.startswith(".slipway/"):
        continue
    cur = project / rel
    new_hash = sha(p)
    if rel not in state:
        if not cur.exists():
            added.append(rel)
            if apply: cur.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(p, cur)
        continue
    if not cur.exists():
        skipped_deleted.append(rel)          # user deleted it on purpose — respect that
    elif sha(cur) == state[rel]["sha256"]:
        if new_hash != state[rel]["sha256"]:
            replaced.append(rel)
            if apply: shutil.copy2(p, cur)
    elif new_hash != state[rel]["sha256"]:
        conflicted.append(rel)               # user modified AND template moved
        if apply: shutil.copy2(p, cur.with_name(cur.name + ".slipway-new"))
if apply:                                     # refresh state for replaced/added files
    for rel in replaced + added:
        state[rel] = {"sha256": sha(project / rel), "ownership": state.get(rel, {}).get("ownership", "starter")}
    (project / ".slipway" / "state.json").write_text(json.dumps(state, indent=1) + "\n")
print(json.dumps({"mode": "applied" if apply else "dry-run", "replaced": replaced,
                  "added": added, "conflicted_written_as_.slipway-new": conflicted,
                  "user_deleted_respected": skipped_deleted}, indent=1))
PY
[ "$APPLY" = "--apply" ] && echo "Run the project's gate now (pnpm gate) before committing the upgrade." >&2 || true
