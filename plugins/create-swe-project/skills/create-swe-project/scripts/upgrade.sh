#!/usr/bin/env bash
# slipway upgrade <project-dir> [--apply]: bring a scaffolded project up to the
# CURRENT templates, Copier-style but honest about ownership:
#   - re-scaffolds the same config (from .slipway/manifest.json) into a temp dir
#   - files the user never modified (hash matches state.json) -> replaced
#   - files the user modified where the template also moved -> 3-way merge when the
#     project's manifest carries a template_ref that resolves in this skill's git repo
#     (the BASE render is the templates the project was born from, via git archive);
#     a clean merge is applied, a conflicting one is written alongside as
#     <file>.slipway-new for a human merge; the user's file is never clobbered
#   - without a resolvable template_ref: 2-way, conflicts always -> .slipway-new
#   - new template files -> added; user-deleted files -> respected
# Default is a DRY RUN report; pass --apply to write. Never deletes user files.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="${1:?usage: upgrade.sh <project-dir> [--apply]}"
APPLY="${2:-}"
MANIFEST="$PROJECT/.slipway/manifest.json"
[ -f "$MANIFEST" ] || { echo "no $MANIFEST — not a slipway project" >&2; exit 1; }

IFS=$'\t' read -r CODENAME DISPLAY MODULES MACOS_STYLE MACOS_DIST BUNDLE PORT_WEB TEMPLATE_REF <<EOF2
$(python3 -c "
import json; m=json.load(open('$MANIFEST'))
print('\t'.join([m['codename'], json.dumps(m['display']), ','.join(m['modules']), m.get('macos_style') or 'window', m.get('macos_dist') or 'direct', m['bundle_prefix'], str(m['ports']['web']), m.get('template_ref') or '-']))")
EOF2

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
DISPLAY_PLAIN="$(python3 -c "import json,sys;print(json.loads(sys.argv[1]))" "$DISPLAY")"
SCAFFOLD_ARGS=(--codename "$CODENAME" --display "$DISPLAY_PLAIN" --modules "$MODULES" \
  --macos-style "$MACOS_STYLE" --macos-dist "$MACOS_DIST" \
  --bundle-prefix "$BUNDLE" --port-web "$PORT_WEB" --no-install)

# NEW render (current templates)
mkdir -p "$TMP/new"
"$SCRIPT_DIR/scaffold.sh" "${SCAFFOLD_ARGS[@]}" --dest "$TMP/new" >/dev/null 2>&1

# BASE render (the templates the project was born from), when template_ref resolves.
# git archive at the ref gives the whole skill tree as it was; its own scaffold.sh
# renders it, so template *and* renderer are the born-from versions.
BASE_DIR=""
BASE_MODE="2-way (no template_ref recorded)"
if [ "$TEMPLATE_REF" != "-" ]; then
  if git -C "$SCRIPT_DIR" cat-file -e "$TEMPLATE_REF" 2>/dev/null; then
    REPO_ROOT="$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)"
    SKILL_PREFIX="$(git -C "$SCRIPT_DIR" rev-parse --show-prefix)"   # .../skills/slipway/scripts/
    mkdir -p "$TMP/skill-at-ref" "$TMP/base"
    git -C "$REPO_ROOT" archive "$TEMPLATE_REF" | tar -x -C "$TMP/skill-at-ref"
    OLD_SCAFFOLD="$TMP/skill-at-ref/${SKILL_PREFIX}scaffold.sh"
    if [ -x "$OLD_SCAFFOLD" ] || [ -f "$OLD_SCAFFOLD" ]; then
      if bash "$OLD_SCAFFOLD" "${SCAFFOLD_ARGS[@]}" --dest "$TMP/base" >/dev/null 2>&1; then
        BASE_DIR="$TMP/base/$CODENAME"
        BASE_MODE="3-way (base: ${TEMPLATE_REF:0:12})"
      else
        BASE_MODE="2-way (born-from scaffold failed to render at ${TEMPLATE_REF:0:12})"
      fi
    else
      BASE_MODE="2-way (scaffold.sh missing at ${TEMPLATE_REF:0:12})"
    fi
  else
    BASE_MODE="2-way (template_ref ${TEMPLATE_REF:0:12} not in this checkout)"
  fi
fi

python3 - "$PROJECT" "$TMP/new/$CODENAME" "$APPLY" "$BASE_DIR" "$BASE_MODE" <<'PY'
import hashlib, json, pathlib, shutil, subprocess, sys
project, fresh = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
apply = sys.argv[3] == "--apply"
base_dir = pathlib.Path(sys.argv[4]) if sys.argv[4] else None
base_mode = sys.argv[5]
state = json.loads((project / ".slipway" / "state.json").read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
replaced, merged, conflicted, added, skipped_deleted = [], [], [], [], []

def three_way(cur: pathlib.Path, base: pathlib.Path, new: pathlib.Path):
    """git merge-file -p: returns merged text on a clean merge, else None."""
    r = subprocess.run(["git", "merge-file", "-p",
                        "-L", "yours", "-L", "slipway-base", "-L", "slipway-new",
                        str(cur), str(base), str(new)], capture_output=True)
    return r.stdout if r.returncode == 0 else None

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
        # user modified AND template moved — try 3-way if we have the born-from render
        base_file = base_dir / rel if base_dir else None
        out = three_way(cur, base_file, p) if base_file and base_file.exists() else None
        if out is not None:
            merged.append(rel)
            if apply: cur.write_bytes(out)
        else:
            conflicted.append(rel)
            if apply: shutil.copy2(p, cur.with_name(cur.name + ".slipway-new"))
if apply:                                     # refresh state for files now matching a template lineage
    for rel in replaced + added:
        state[rel] = {"sha256": sha(project / rel), "ownership": state.get(rel, {}).get("ownership", "starter")}
    for rel in merged:                        # merged files count as user-modified vs the NEW template
        state[rel] = {"sha256": sha(fresh / rel), "ownership": state.get(rel, {}).get("ownership", "starter")}
    (project / ".slipway" / "state.json").write_text(json.dumps(state, indent=1) + "\n")
print(json.dumps({"mode": "applied" if apply else "dry-run", "base": base_mode,
                  "replaced": replaced, "added": added, "merged_3way": merged,
                  "conflicted_written_as_.slipway-new": conflicted,
                  "user_deleted_respected": skipped_deleted}, indent=1))
PY
if [ "$APPLY" = "--apply" ]; then
  # Advance the lineage: state.json now tracks the CURRENT templates, so the next
  # upgrade must 3-way against them, not the original born-from ref.
  CURRENT_REF="$(git -C "$SCRIPT_DIR" rev-parse HEAD 2>/dev/null || echo "")"
  python3 - "$MANIFEST" "$CURRENT_REF" <<'PY'
import json, sys
m = json.load(open(sys.argv[1]))
m["template_ref"] = sys.argv[2] or None
json.dump(m, open(sys.argv[1], "w"), indent=1)
PY
  echo "Run the project's gate now (pnpm gate) before committing the upgrade." >&2
fi
