#!/usr/bin/env bash
# slipway scaffold.sh — deterministic project scaffolder for ~/Dev projects.
#
# Renders the template tree into a new project directory with token substitution,
# assembles the composite files (Caddyfile, docker-compose, CLAUDE.md, README) from
# per-module fragments, copies the operating specs (CODING_PRACTICES.md and
# NEW_PROJECT_BEST_PRACTICES.md, bundled in references/team-files/), initialises
# git, installs deps, pins every "latest" to the range it resolved, generates
# Xcode projects, and runs the full quality gate. Designed so the calling agent
# supplies decisions (flags) and the script does the work.
#
# Usage:
#   scaffold.sh --codename loft --display "Loft" \
#     [--description "One-line description"] \
#     [--modules web,api,macos,ios,tokens,data]   # default: web,tokens
#     [--bundle-prefix app.loft]                  # default: app.<codename>
#     [--dest ~/Dev] [--port-web N] [--port-api N] \
#     [--team-files <dir>]                        # default: the bundled snapshot
#     [--no-install] [--dry-run]
#
# Safe by default: refuses to write into an existing directory; --dry-run prints
# the plan (ports, paths, modules) and writes nothing; never runs sudo — Caddy
# commands are printed and written to SETUP-NEXT-STEPS.md for the user.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TPL="$SCRIPT_DIR/../templates"

CODENAME="" DISPLAY="" DESCRIPTION="" BUNDLE_PREFIX="" MODULES="web,tokens"
DEST="$HOME/Dev" PORT_WEB="" PORT_API="" TEAM_FILES=""
NO_INSTALL=0 DRY_RUN=0 PLAN=0 MACOS_STYLE="window" MACOS_DIST="direct" OP_ACCOUNT="" OP_VAULT="" GITHUB_ORG="" DESIGN_REF=""

while [ $# -gt 0 ]; do
  case "$1" in
    --codename) CODENAME="$2"; shift 2;;
    --display) DISPLAY="$2"; shift 2;;
    --description) DESCRIPTION="$2"; shift 2;;
    --modules) MODULES="$2"; shift 2;;
    --bundle-prefix) BUNDLE_PREFIX="$2"; shift 2;;
    --macos-style) MACOS_STYLE="$2"; shift 2;;  # window (sidebar+search) | menubar
    --op-account) OP_ACCOUNT="$2"; shift 2;;    # 1Password account/team id → .env.local
    --op-vault) OP_VAULT="$2"; shift 2;;        # 1Password vault → .env.local
    --macos-dist) MACOS_DIST="$2"; shift 2;;    # direct (Developer ID, no sandbox) | mas (App Store, sandboxed)
    --github-org) GITHUB_ORG="$2"; shift 2;;    # sets the git remote; repo creation stays a next-step
    --design-ref) DESIGN_REF="$2"; shift 2;;    # reference site/brand for the DESIGN.md bootstrap
    --dest) DEST="$2"; shift 2;;
    --port-web) PORT_WEB="$2"; shift 2;;
    --port-api) PORT_API="$2"; shift 2;;
    --team-files) TEAM_FILES="$2"; shift 2;;
    --no-install) NO_INSTALL=1; shift;;
    --dry-run) DRY_RUN=1; shift;;
    --plan) PLAN=1; shift;;                     # emit the JSON plan (files/ports/modules), write nothing
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

[ -n "$CODENAME" ] || { echo "--codename is required" >&2; exit 2; }
[[ "$CODENAME" =~ ^[a-z][a-z0-9-]*$ ]] || { echo "codename must be lowercase alnum/hyphen, got: $CODENAME" >&2; exit 2; }
[ -n "$DISPLAY" ] || DISPLAY="$(python3 -c "print('$CODENAME'.replace('-',' ').title())")"
[ -n "$DESCRIPTION" ] || DESCRIPTION="$DISPLAY."
[ -n "$BUNDLE_PREFIX" ] || BUNDLE_PREFIX="app.$(echo "$CODENAME" | tr -d '-')"
PROJECT_DIR="$DEST/$CODENAME"
# *.localhost: loopback with no /etc/hosts entry on macOS 26+, and a secure
# context in browsers, so Secure cookies work on the dev origin (BP §20).
HOST="$CODENAME.localhost"

has_module() { case ",$MODULES," in *",$1,"*) return 0;; *) return 1;; esac; }

# module implications: push→auth→data→web (the lib/ stack lives in apps/web);
# admin needs the data services too.
if has_module push && ! has_module auth; then MODULES="auth,$MODULES"; fi
if has_module auth && ! has_module data; then MODULES="data,$MODULES"; fi
if has_module admin && ! has_module data; then MODULES="data,$MODULES"; fi
if has_module waitlist && ! has_module data; then MODULES="data,$MODULES"; fi
if has_module observability && ! has_module web; then MODULES="web,$MODULES"; fi
if has_module data && ! has_module web; then MODULES="web,$MODULES"; fi

[ -e "$PROJECT_DIR" ] && { echo "refusing: $PROJECT_DIR already exists" >&2; exit 1; }

# ---- port allocation: scan machine Caddy conf.d + repo Caddyfiles for used ports,
# pick the first free block of 10 starting at 3100.
used_ports() {
  { grep -rhoE 'localhost:[0-9]{4,5}' /opt/homebrew/etc/caddy/conf.d "$DEST"/*/Caddyfile 2>/dev/null || true; } \
    | grep -oE '[0-9]+' | sort -un
}
if [ -z "$PORT_WEB" ]; then
  USED="$(used_ports)"
  base=3100
  while :; do
    conflict=0
    for p in $(seq "$base" $((base + 9))); do
      if echo "$USED" | grep -qx "$p"; then conflict=1; break; fi
    done
    [ "$conflict" = 0 ] && break
    base=$((base + 10))
  done
  PORT_WEB=$base
fi
[ -n "$PORT_API" ] || PORT_API=$((PORT_WEB + 1))
PORT_ADMIN=$((PORT_WEB + 2))

if [ "${PLAN:-0}" != 1 ]; then
  echo "== slipway scaffold"
  echo "   project:  $PROJECT_DIR"
  echo "   display:  $DISPLAY"
  echo "   modules:  $MODULES"
  echo "   bundle:   $BUNDLE_PREFIX.<app>"
  echo "   ports:    web=$PORT_WEB api=$PORT_API"
  echo "   host:     $HOST"
fi
if [ "$PLAN" = 1 ]; then
  python3 - "$TPL" "$MODULES" "$CODENAME" "$PORT_WEB" "$PORT_API" "$PORT_ADMIN" <<'PY'
import json, pathlib, sys
tpl, modules, codename = pathlib.Path(sys.argv[1]), sys.argv[2].split(","), sys.argv[3]
DIR_TARGET = {"base": ".", "web": "apps/web", "api": "apps/api", "macos": "apps/macos",
              "ios": "apps/ios", "rn": "apps/mobile", "rn-root": ".", "tokens": "packages/design-tokens",
              "data": "apps/web", "auth": "apps/web", "push": "apps/web", "waitlist": "apps/web",
              "observability": "apps/web", "admin": "apps/admin", "rust": ".", "rust-root": "."}
dirs = ["base"] + [m for m in modules if (tpl / m).is_dir()]
if "rn" in modules: dirs.append("rn-root")
if "rust" in modules: dirs.append("rust-root")
files = []
for d in dirs:
    for p in sorted((tpl / d).rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(tpl / d))
            rel = "/".join(("." + q[4:]) if q.startswith("dot_") else q for q in rel.split("/"))
            rel = rel[:-5] if rel.endswith(".tmpl") else rel
            files.append(str(pathlib.PurePosixPath(DIR_TARGET[d]) / rel))
print(json.dumps({"codename": codename, "modules": modules,
                  "ports": {"web": int(sys.argv[4]), "api": int(sys.argv[5]), "admin": int(sys.argv[6])},
                  "file_count": len(files), "files": sorted(set(files))}, indent=1))
PY
  exit 0
fi
[ "$DRY_RUN" = 1 ] && { echo "   (dry run — nothing written)"; exit 0; }

# A reviewed pin, not whatever pnpm the caller's directory resolves (corepack
# reads the nearest packageManager, so running from inside another repo used to
# stamp that repo's pnpm here). pnpm 11+ is required: catalogs, allowBuilds,
# minimumReleaseAge on by default (BP §2, §17). Bump it here; canary.sh proves it.
PNPM_VERSION="12.18.0"
export COREPACK_ENABLE_DOWNLOAD_PROMPT=0

# Generated projects run on Node 24.9+ (BP §1; NestJS 12's ESM packages need it
# under Jest). When the shell's node is older, use an nvm-installed 24 for the
# install and gate rather than failing in a way that looks like a broken test.
node_ok() { node -e 'const [a,b]=process.versions.node.split(".").map(Number);process.exit(a>24||(a===24&&b>=9)?0:1)' 2>/dev/null; }
if ! node_ok; then
  NODE24="$(ls -d "${NVM_DIR:-$HOME/.nvm}"/versions/node/v24.* 2>/dev/null | sort -V | tail -1)"
  if [ -n "$NODE24" ] && [ -x "$NODE24/bin/node" ]; then
    export PATH="$NODE24/bin:$PATH"
    [ "${PLAN:-0}" = 1 ] || echo "   node:     $(node --version) from $NODE24 (the shell default is older)"
  else
    echo "WARN: node $(node --version 2>/dev/null) is older than 24.9 and no nvm Node 24 was found; the gate will refuse to run (nvm install 24)" >&2
  fi
fi

# Operating specs: --team-files wins, else the snapshot bundled with this skill,
# which is what the templates were written against. A team-files checkout that
# has moved on is reported, not silently preferred.
BUNDLED_TEAM_FILES="$SCRIPT_DIR/../references/team-files"
[ -n "$TEAM_FILES" ] || TEAM_FILES="$BUNDLED_TEAM_FILES"
for f in CODING_PRACTICES.md NEW_PROJECT_BEST_PRACTICES.md; do
  [ -f "$TEAM_FILES/$f" ] || { echo "ERROR: $TEAM_FILES/$f not found; the generated CLAUDE.md requires it" >&2; exit 1; }
done
for live in "$HOME/Dev/bella-team-files" "/Volumes/LLMs/Dev/bella-team-files"; do
  [ -f "$live/CODING_PRACTICES.md" ] || continue
  if ! cmp -s "$live/CODING_PRACTICES.md" "$BUNDLED_TEAM_FILES/CODING_PRACTICES.md" \
     || ! cmp -s "$live/NEW_PROJECT_BEST_PRACTICES.md" "$BUNDLED_TEAM_FILES/NEW_PROJECT_BEST_PRACTICES.md"; then
    echo "NOTE: $live differs from the bundled team-files snapshot; run scripts/sync-team-files.sh and update the templates" >&2
  fi
  break
done

# ---- render engine: copies a template dir into a target dir.
#   *.tmpl        → token-substituted, suffix stripped
#   dot_<name>    → renamed to .<name> (files or top-level dirs)
#   everything else copied verbatim
export SW_CODENAME="$CODENAME" SW_DISPLAY="$DISPLAY" SW_DESCRIPTION="$DESCRIPTION" \
       SW_BUNDLE_PREFIX="$BUNDLE_PREFIX" SW_PORT_WEB="$PORT_WEB" SW_PORT_API="$PORT_API" \
       SW_PNPM_VERSION="$PNPM_VERSION" SW_YEAR="$(date +%Y)" SW_DATE="$(date +%Y-%m-%d)" SW_PORT_ADMIN="$PORT_ADMIN" \
       SW_HOST="$HOST" SW_DB_NAME="$(echo "$CODENAME" | tr '-' '_')"
export SW_ID_PREFIX="$(python3 -c "import os;print(os.environ['SW_CODENAME'].replace('-','')[:3].upper())")"
export SW_APP_NAME="$(python3 -c "import re,os; print(''.join(w.capitalize() for w in re.split(r'[^A-Za-z0-9]+', os.environ['SW_DISPLAY']) if w))")"
if [ "$MACOS_STYLE" = "menubar" ]; then
  export SW_LSUIELEMENT="LSUIElement: YES                # menu-bar agent — no Dock icon"
else
  export SW_LSUIELEMENT="# LSUIElement: YES              # uncomment to make this a menu-bar agent"
fi
render_dir() { # render_dir <template-subdir> <target-dir>
  python3 - "$TPL/$1" "$2" <<'PY'
import os, sys, pathlib, shutil
src, dst = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
tokens = {k[3:]: v for k, v in os.environ.items() if k.startswith("SW_")}
def rendered(text):
    for k, v in tokens.items():
        text = text.replace("{{" + k + "}}", v)
    return text
for p in sorted(src.rglob("*")):
    if p.is_dir():
        continue
    rel = p.relative_to(src)
    parts = [q[4:] and "." + q[4:] if q.startswith("dot_") else q for q in rel.parts]
    out = dst.joinpath(*parts)
    if out.name.endswith(".tmpl"):
        out = out.with_name(out.name[:-5])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered(p.read_text()))
    else:
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, out)
    if os.access(p, os.X_OK):
        os.chmod(out, 0o755)
PY
}
render_fragment() { # render_fragment <fragment-file> → stdout, token-substituted
  python3 - "$TPL/$1" <<'PY'
import os, sys, pathlib
text = pathlib.Path(sys.argv[1]).read_text()
for k, v in os.environ.items():
    if k.startswith("SW_"):
        text = text.replace("{{" + k[3:] + "}}", v)
sys.stdout.write(text)
PY
}

mkdir -p "$PROJECT_DIR"

# ---- 1. base + selected modules
render_dir base "$PROJECT_DIR"
# server-lib (env, http guards, logger, vitest config) and csp (nonce proxy) go
# into every Next app; kv (node-redis + rate limiter) into every app that has
# Redis. The same template source renders into each, so the copies start equal.
if has_module web; then
  render_dir web        "$PROJECT_DIR/apps/web"
  render_dir server-lib "$PROJECT_DIR/apps/web"
  render_dir csp        "$PROJECT_DIR/apps/web"
fi
has_module data && render_dir kv "$PROJECT_DIR/apps/web"
has_module api    && render_dir api    "$PROJECT_DIR/apps/api"
has_module macos  && render_dir macos  "$PROJECT_DIR/apps/macos"
has_module ios    && render_dir ios    "$PROJECT_DIR/apps/ios"
has_module tokens && render_dir tokens "$PROJECT_DIR/packages/design-tokens"
has_module data   && render_dir data   "$PROJECT_DIR/apps/web"
has_module auth   && render_dir auth   "$PROJECT_DIR/apps/web"   # overwrites data's models/types with the User-bearing versions
has_module push   && render_dir push   "$PROJECT_DIR/apps/web"
if has_module admin; then
  render_dir admin      "$PROJECT_DIR/apps/admin"
  render_dir server-lib "$PROJECT_DIR/apps/admin"
  render_dir csp        "$PROJECT_DIR/apps/admin"
  render_dir kv         "$PROJECT_DIR/apps/admin"
fi
has_module waitlist && render_dir waitlist "$PROJECT_DIR/apps/web"
has_module observability && render_dir observability "$PROJECT_DIR/apps/web"   # overwrites next.config + csp-origins with the Sentry versions

# tokens: generate tokens.css NOW (pure node, no deps) so the committed file is in
# sync and the gate's drift check passes from the first run.
has_module tokens && (cd "$PROJECT_DIR/packages/design-tokens" && node build.mjs >/dev/null)

# rn (React Native / Expo, BP §18): pnpm's default isolated layout and Expo's
# automatic Metro monorepo config (SDK 54+), so no root .npmrc and no hand-written
# watchFolders.
has_module rn && render_dir rn "$PROJECT_DIR/apps/mobile"

# macos distribution: pick the matching entitlements (direct = Developer ID, no
# sandbox; mas = App Store, sandboxed — a review requirement).
if has_module macos; then
  if [ "$MACOS_DIST" = "mas" ]; then
    mv "$PROJECT_DIR/apps/macos/Signing/App-mas.entitlements" "$PROJECT_DIR/apps/macos/Signing/App.entitlements"
    rm "$PROJECT_DIR/apps/macos/Signing/App-direct.entitlements"
  else
    mv "$PROJECT_DIR/apps/macos/Signing/App-direct.entitlements" "$PROJECT_DIR/apps/macos/Signing/App.entitlements"
    rm "$PROJECT_DIR/apps/macos/Signing/App-mas.entitlements"
  fi
fi

# macos style: exactly one App.swift variant survives (window = NavigationSplitView
# sidebar + top nav with search; menubar = MenuBarExtra agent).
if has_module macos; then
  if [ "$MACOS_STYLE" = "menubar" ]; then
    mv "$PROJECT_DIR/apps/macos/Sources/AppMain/App-menubar.swift" "$PROJECT_DIR/apps/macos/Sources/AppMain/App.swift"
    rm "$PROJECT_DIR/apps/macos/Sources/AppMain/App-window.swift"
  else
    mv "$PROJECT_DIR/apps/macos/Sources/AppMain/App-window.swift" "$PROJECT_DIR/apps/macos/Sources/AppMain/App.swift"
    rm "$PROJECT_DIR/apps/macos/Sources/AppMain/App-menubar.swift"
  fi
fi

# AI model registry only makes sense where the AI SDK is wired (web/api)
if ! has_module web && ! has_module api; then
  rm -f "$PROJECT_DIR/docs/AI-MODEL-USAGE.md"
fi

# rust: cross-OS core crate + cargo workspace at the root
if has_module rust; then
  render_dir rust      "$PROJECT_DIR"
  render_dir rust-root "$PROJECT_DIR"
fi

# api+data: the API gets the data-layer clients too (dAIolog pattern)
if has_module api && has_module data; then
  node -e '
    const fs = require("fs"); const p = process.argv[1];
    const j = JSON.parse(fs.readFileSync(p, "utf8"));
    j.dependencies = { ...j.dependencies, "@nestjs/mongoose": "latest", mongoose: "catalog:", redis: "catalog:" };
    fs.writeFileSync(p, JSON.stringify(j, null, 2) + "\n");
  ' "$PROJECT_DIR/apps/api/package.json"
fi

# auth/push: merge web deps + env keys
if has_module auth; then
  node -e '
    const fs = require("fs"); const p = process.argv[1];
    const j = JSON.parse(fs.readFileSync(p, "utf8"));
    j.dependencies = { ...j.dependencies, jose: "catalog:", resend: "catalog:", "@react-email/components": "catalog:" };
    j.devDependencies = { ...j.devDependencies, "mongodb-memory-server": "catalog:" };
    fs.writeFileSync(p, JSON.stringify(j, null, 2) + "\n");
  ' "$PROJECT_DIR/apps/web/package.json"
  render_fragment "fragments/env/auth.env" >> "$PROJECT_DIR/apps/web/.env.example"
fi
if has_module push; then
  render_fragment "fragments/env/push.env" >> "$PROJECT_DIR/apps/web/.env.example"
fi
if has_module waitlist; then
  node -e '
    const fs = require("fs"); const p = process.argv[1];
    const j = JSON.parse(fs.readFileSync(p, "utf8"));
    j.devDependencies = { ...j.devDependencies, "mongodb-memory-server": "catalog:" };
    fs.writeFileSync(p, JSON.stringify(j, null, 2) + "\n");
  ' "$PROJECT_DIR/apps/web/package.json"
fi
if has_module observability; then
  node -e '
    const fs = require("fs"); const p = process.argv[1];
    const j = JSON.parse(fs.readFileSync(p, "utf8"));
    j.dependencies = { ...j.dependencies, "@sentry/nextjs": "latest" };
    fs.writeFileSync(p, JSON.stringify(j, null, 2) + "\n");
  ' "$PROJECT_DIR/apps/web/package.json"
  render_fragment "fragments/env/observability.env" >> "$PROJECT_DIR/apps/web/.env.example"
fi

# 1Password: seed .env.local from .env.example with OP_ACCOUNT/OP_VAULT filled.
# Identifiers only — real secret values arrive via scripts/env-pull.sh (op CLI),
# never through an agent.
if [ -n "$OP_ACCOUNT" ] && has_module web; then
  python3 - "$PROJECT_DIR/apps/web/.env.example" "$PROJECT_DIR/apps/web/.env.local" "$OP_ACCOUNT" "$OP_VAULT" <<'PY'
import sys
src, dst, account, vault = sys.argv[1:5]
lines = []
for line in open(src).read().splitlines():
    if line.startswith("OP_ACCOUNT="): line = f"OP_ACCOUNT={account}"
    elif line.startswith("OP_VAULT="): line = f"OP_VAULT={vault}"
    lines.append(line)
open(dst, "w").write("\n".join(lines) + "\n")
PY
fi

# data module: merge extra deps + env keys into the web app
if has_module data; then
  node -e '
    const fs = require("fs"); const p = process.argv[1];
    const j = JSON.parse(fs.readFileSync(p, "utf8"));
    j.dependencies = { ...j.dependencies, mongoose: "catalog:", redis: "catalog:" };
    j.devDependencies = { ...j.devDependencies, tsx: "catalog:" };
    // Scripts import server-only modules, so they run under the react-server condition (BP §14).
    j.scripts = { ...j.scripts, script: "tsx --env-file-if-exists=.env.local --conditions=react-server" };
    fs.writeFileSync(p, JSON.stringify(j, null, 2) + "\n");
  ' "$PROJECT_DIR/apps/web/package.json"
  render_fragment "fragments/env/data.env" >> "$PROJECT_DIR/apps/web/.env.example"
fi

# ---- 2. composite files from fragments
assemble() { # assemble <fragment-group> <out-file> [module...]
  local group="$1" out="$2"; shift 2
  : > "$out"
  render_fragment "fragments/$group/header.tmpl" >> "$out"
  for m in "$@"; do
    if has_module "$m" && [ -f "$TPL/fragments/$group/$m.tmpl" ]; then
      render_fragment "fragments/$group/$m.tmpl" >> "$out"
    fi
  done
  [ -f "$TPL/fragments/$group/footer.tmpl" ] && render_fragment "fragments/$group/footer.tmpl" >> "$out" || true
}
# Rows that land inside a fragment rather than after it: the CLAUDE.md routing
# map and command block, and the compose service details that depend on which
# other workspace members exist.
rows() { # rows <group> <module...> → concatenated rendered rows for selected modules
  local group="$1"; shift
  for m in "$@"; do
    if has_module "$m" && [ -f "$TPL/fragments/$group/$m.tmpl" ]; then render_fragment "fragments/$group/$m.tmpl"; fi
  done
}
SW_ROUTING_ROWS="$(rows routing web api admin auth data push waitlist observability rn tokens macos ios rust)"
SW_COMMAND_ROWS="$(rows commands web api admin data rn tokens macos rust)"
[ -n "$SW_ROUTING_ROWS" ] && SW_ROUTING_ROWS="$SW_ROUTING_ROWS
"
[ -n "$SW_COMMAND_ROWS" ] && SW_COMMAND_ROWS="$SW_COMMAND_ROWS
"
MEMBERS=""   # workspace members whose node_modules a container must not share
has_module web    && MEMBERS="$MEMBERS apps/web"
has_module api    && MEMBERS="$MEMBERS apps/api"
has_module admin  && MEMBERS="$MEMBERS apps/admin"
has_module rn     && MEMBERS="$MEMBERS apps/mobile"
has_module tokens && MEMBERS="$MEMBERS packages/design-tokens"
HEAVY=""     # trees no JS container reads (BP §21: they exhaust kern.maxfiles)
has_module rn    && HEAVY="$HEAVY apps/mobile/ios apps/mobile/android"
has_module macos && HEAVY="$HEAVY apps/macos"
has_module ios   && HEAVY="$HEAVY apps/ios"
has_module rust  && HEAVY="$HEAVY target"
masks_for() { # masks_for <own-member> → compose volume lines shadowing everything else
  local m
  for m in $MEMBERS; do [ "$m" = "$1" ] || printf '      - /repo/%s/node_modules\n' "$m"; done
  for m in $HEAVY; do printf '      - /repo/%s\n' "$m"; done
}
SW_COMPOSE_MASKS_WEB="$(masks_for apps/web)"
SW_COMPOSE_MASKS_API="$(masks_for apps/api)"
[ -n "$SW_COMPOSE_MASKS_WEB" ] && SW_COMPOSE_MASKS_WEB="$SW_COMPOSE_MASKS_WEB
"
[ -n "$SW_COMPOSE_MASKS_API" ] && SW_COMPOSE_MASKS_API="$SW_COMPOSE_MASKS_API
"
SW_COMPOSE_DATA_ENV=""
if has_module data; then
  SW_COMPOSE_DATA_ENV="      MONGODB_URI: mongodb://mongo:27017/${SW_DB_NAME}_dev?replicaSet=rs0&directConnection=true
      REDIS_URL: redis://redis:6379
    depends_on:
      mongo: { condition: service_healthy }
      redis: { condition: service_healthy }
"
fi
export SW_ROUTING_ROWS SW_COMMAND_ROWS SW_COMPOSE_MASKS_WEB SW_COMPOSE_MASKS_API SW_COMPOSE_DATA_ENV

assemble caddy   "$PROJECT_DIR/Caddyfile"              web api admin
if has_module web || has_module api || has_module data; then
  assemble compose "$PROJECT_DIR/docker-compose.dev.yml" web api data
fi
assemble claude  "$PROJECT_DIR/CLAUDE.md"              web api rn macos ios tokens data auth admin push waitlist observability rust
assemble readme  "$PROJECT_DIR/README.md"              web api rn macos ios tokens data auth admin push waitlist observability rust
mkdir -p "$PROJECT_DIR/docs"
assemble arch    "$PROJECT_DIR/docs/ARCHITECTURE.md"    web api admin macos ios rn tokens rust
assemble testing "$PROJECT_DIR/docs/TESTING.md"         web admin api rn macos ios rust
assemble deploy  "$PROJECT_DIR/docs/DEPLOYMENT.md"      web admin macos ios rn api
assemble divergences "$PROJECT_DIR/docs/DIVERGENCES.md" web auth admin

# ---- 3. operating specs + AGENTS.md symlink
mkdir -p "$PROJECT_DIR/docs"
for f in CODING_PRACTICES.md NEW_PROJECT_BEST_PRACTICES.md; do cp "$TEAM_FILES/$f" "$PROJECT_DIR/docs/$f"; done
TEAM_FILES_COMMIT="$(python3 -c "import json,sys;print(json.load(open(sys.argv[1])).get('source_commit',''))" "$TEAM_FILES/SOURCE.json" 2>/dev/null || git -C "$TEAM_FILES" rev-parse HEAD 2>/dev/null || echo "")"
mkdir -p "$PROJECT_DIR/docs/features-to-triage" "$PROJECT_DIR/docs/specs" "$PROJECT_DIR/docs/plans" "$PROJECT_DIR/docs/deep-research" "$PROJECT_DIR/design/mocks/html" "$PROJECT_DIR/design/icon" "$PROJECT_DIR/design/marketing/assets"
printf '# LEDGER\n\n| ID | Feature | Status |\n|---|---|---|\n' > "$PROJECT_DIR/docs/features-to-triage/LEDGER.md"
ln -s CLAUDE.md "$PROJECT_DIR/AGENTS.md"

# ---- provenance manifest (.slipway/manifest.json): template version + every
# answer that shaped this project. The record that makes a future upgrade/diff
# story possible — scaffolders that skip it (shadcn) cannot separate user edits
# from template changes later.
SLIPWAY_VERSION="$(python3 -c "import json;print(json.load(open('$SCRIPT_DIR/../../../.claude-plugin/plugin.json'))['version'])" 2>/dev/null || echo unknown)"
# Template version tag: the skill repo's commit at scaffold time. Lets upgrade.sh
# render the templates this project was BORN from and do a true 3-way merge.
# Absent when running from a non-git install (plugin cache) — upgrade falls back to 2-way.
TEMPLATE_REF="$(git -C "$SCRIPT_DIR" rev-parse HEAD 2>/dev/null || echo "")"
TEMPLATE_DIRTY="false"
if [ -n "$TEMPLATE_REF" ] && [ -n "$(git -C "$SCRIPT_DIR" status --porcelain 2>/dev/null)" ]; then TEMPLATE_DIRTY="true"; fi
mkdir -p "$PROJECT_DIR/.slipway"
python3 - "$PROJECT_DIR/.slipway/manifest.json" <<PY
import json, os, sys
json.dump({
    "slipway_version": "$SLIPWAY_VERSION",
    "template_ref": "$TEMPLATE_REF" or None,
    "template_ref_dirty": "$TEMPLATE_DIRTY" == "true",
    "scaffolded": "$(date +%Y-%m-%dT%H:%M:%S%z)",
    "codename": "$CODENAME",
    "display": os.environ["SW_DISPLAY"],
    "modules": "$MODULES".split(","),
    "bundle_prefix": "$BUNDLE_PREFIX",
    "macos_style": "$MACOS_STYLE",
    "macos_dist": "$MACOS_DIST",
    "github_org": "$GITHUB_ORG" or None,
    "design_ref": "$DESIGN_REF" or None,
    "ports": {"web": $PORT_WEB, "api": $PORT_API, "admin": $PORT_ADMIN},
    "op_vault": "$OP_VAULT" or None,
    "host": "$HOST",
    "team_files": {"source": "$TEAM_FILES", "commit": "$TEAM_FILES_COMMIT" or None},
}, open(sys.argv[1], "w"), indent=2)
PY

# ---- state inventory (.slipway/state.json): SHA256 of every generated file +
# ownership class. This is what makes drift detection and upgrades possible —
# an unmodified hash means the file is safely replaceable by a newer template.
# Written before the first commit, and again after the install pins ranges.
write_state() {
python3 - "$PROJECT_DIR" <<'PY2'
import hashlib, json, pathlib, subprocess, sys
root = pathlib.Path(sys.argv[1])
GENERATOR_OWNED = ("docs/CODING_PRACTICES.md", "docs/NEW_PROJECT_BEST_PRACTICES.md",
                   "scripts/env-pull.sh", "scripts/gate.mjs", "scripts/check-env.mjs",
                   "scripts/worktree-add.sh", "scripts/prune-merged-worktrees.sh",
                   ".slipway/", ".husky/pre-push")
listed = subprocess.run(["git", "-C", str(root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                        capture_output=True, text=True)
paths = sorted(set(listed.stdout.split("\0")) - {""}) if listed.returncode == 0 else \
    sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and ".git/" not in str(p))
state = {}
for rel in paths:
    p = root / rel
    if p.name in ("state.json", "next-env.d.ts", "pnpm-lock.yaml") or p.is_symlink() or not p.is_file():
        continue
    ownership = "generator" if any(rel.startswith(g) or rel == g.rstrip("/") for g in GENERATOR_OWNED) else "starter"
    state[rel] = {"sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "ownership": ownership}
(root / ".slipway" / "state.json").write_text(json.dumps(state, indent=1) + "\n")
PY2
}

# ---- 4. guard: no unrendered tokens
if grep -rn "{{[A-Z_]*}}" "$PROJECT_DIR" --include='*' -l 2>/dev/null | grep -q .; then
  echo "ERROR: unrendered template tokens remain:" >&2
  grep -rn "{{[A-Z_]*}}" "$PROJECT_DIR" -l >&2
  exit 1
fi

# ---- 5. git + install + native projects + gate
cd "$PROJECT_DIR"
git init -q -b main
write_state
# The one root .gitignore must reach inside every app (BP §17, CP §6.8): prove it
# on nested paths before anything is committed.
for must in apps/web/.env.local apps/web/.env apps/web/.env.production apps/admin/.env.local apps/web/.vercel/project.json; do
  git check-ignore -q "$must" || { echo "ERROR: .gitignore does not ignore $must" >&2; exit 1; }
done
if git check-ignore -q apps/web/.env.example; then echo "ERROR: .gitignore ignores apps/web/.env.example" >&2; exit 1; fi
git add -A
git commit -qm "Scaffold $DISPLAY via slipway (modules: $MODULES)"
[ -n "$GITHUB_ORG" ] && git remote add origin "git@github.com:$GITHUB_ORG/$CODENAME.git"

INSTALL_OK=""; GATE_OK=""; XCODE_OK=""; PIN_OK=""; BROWSER_OK=""
# Native projects first: the gate's swift test reads apps/macos.
if has_module macos || has_module ios; then
  if command -v xcodegen >/dev/null 2>&1; then
    XCODE_OK=yes
    has_module macos && (cd apps/macos && xcodegen generate --quiet)
    has_module ios   && (cd apps/ios   && xcodegen generate --quiet)
  else
    echo "WARN: xcodegen not installed (brew install xcodegen) — .xcodeproj not generated" >&2
  fi
fi
RUST_OK=""
if has_module rust; then
  if command -v cargo >/dev/null 2>&1; then
    if (cd "$PROJECT_DIR" && cargo test -q >/dev/null 2>&1); then RUST_OK=yes; fi
  else
    echo "WARN: cargo not installed (rustup) — rust crate not verified" >&2
  fi
fi
if [ "$NO_INSTALL" = 0 ] && [ -f package.json ]; then
  if pnpm install --silent; then
    INSTALL_OK=yes
    # Committed specifiers become real caret ranges (BP §2, CP §4 A03): every
    # "latest" in a package.json or the catalog is rewritten to the version the
    # cooldown-respecting install resolved, then the lockfile catches up.
    if pnpm list -r --json --depth 0 > .slipway/resolved.json 2>/dev/null \
       && python3 "$SCRIPT_DIR/pin-latest.py" "$PROJECT_DIR" .slipway/resolved.json \
       && pnpm install --silent; then PIN_OK=yes; fi
    rm -f .slipway/resolved.json
    if has_module web; then
      if pnpm --filter web exec playwright install chromium >/dev/null 2>&1; then BROWSER_OK=yes
      else echo "WARN: playwright install chromium failed; the e2e smoke step of the gate will fail until it is installed" >&2; fi
    fi
    if pnpm gate; then GATE_OK=yes; fi
  fi
fi
if [ -n "$INSTALL_OK" ] || [ -n "$XCODE_OK" ] || [ -n "$RUST_OK" ]; then
  write_state
  git add -A && git commit -qm "Post-scaffold: lockfile, pinned ranges, generated projects" 2>/dev/null || true
fi

# ---- 6. next-steps file (the only manual part: sudo + accounts)
{
  render_fragment "fragments/next-steps/header.tmpl"
  echo
  echo '## 1. Caddy (no sudo — BP §20)'
  echo
  echo "Mirror the repo Caddyfile's route blocks (not its global block) into the machine-wide Caddy, validate, reload:"
  echo
  echo '```bash'
  echo "sed '/^{/,/^}/d' \"$PROJECT_DIR/Caddyfile\" > /opt/homebrew/etc/caddy/conf.d/$CODENAME.caddy"
  echo 'caddy validate --config /opt/homebrew/etc/Caddyfile && caddy reload --config /opt/homebrew/etc/Caddyfile'
  echo '# Caddy not running yet: brew services start caddy'
  echo '```'
  echo
  macos_major="$(sw_vers -productVersion 2>/dev/null | cut -d. -f1 || echo 26)"
  if [ "${macos_major:-26}" -lt 26 ] 2>/dev/null; then
    echo "This Mac runs macOS $macos_major, which doesn't resolve *.localhost on its own. Add hosts lines (needs sudo):"
    echo
    echo '```bash'
    for h in "$HOST" "api.$HOST" "admin.$HOST"; do echo "printf '127.0.0.1 $h\\n::1 $h\\n' | sudo tee -a /etc/hosts >/dev/null"; done
    echo '```'
  else
    echo "macOS 26+ resolves \`*.localhost\` to loopback, so no /etc/hosts entry is needed."
  fi
  echo
  if has_module web; then
    echo '## 2. Vercel'
    echo
    echo 'Link each Next app before the first push. Once linked, the pre-push gate builds it with a real `vercel build` (BP §19); until then it says it fell back to next build.'
    echo
    echo '```bash'
    echo "cd $PROJECT_DIR/apps/web && vercel link && vercel pull"
    has_module admin && echo "cd $PROJECT_DIR/apps/admin && vercel link && vercel pull"
    echo '```'
    echo
  fi
  if has_module macos || has_module ios; then
    echo '## 3. Release path (TestFlight / App Store / notarized DMG)'
    echo
    echo 'Debug/simulator builds need nothing. For release:'
    echo '- Create an App Store Connect API key (Users & Access → Integrations) and fill `apps/<platform>/fastlane/.env` (ASC_KEY_ID / ASC_ISSUER_ID / ASC_KEY_PATH / DEVELOPMENT_TEAM — copy from fastlane/.env.example).'
    echo '- TestFlight: `cd apps/ios && bundle install && bundle exec fastlane beta` (same lane exists for apps/macos MAS builds).'
    echo '- Direct mac distribution: `apps/macos/scripts/sign.sh` → `notarize.sh` (one-time: `xcrun notarytool store-credentials notary`) → `build-dmg.sh`.'
    echo
  fi
  echo '## Testing'
  echo
  has_module web && echo "- Web e2e (Playwright, against the built app): \`pnpm --filter web build && pnpm --filter web test:e2e\`. Chromium: ${BROWSER_OK:+installed by the scaffold}${BROWSER_OK:-not installed — run \`pnpm --filter web exec playwright install chromium\`}. Build acceptance suites with \`acceptance-e2e:acceptance-e2e\`."
  has_module api && echo '- API unit (jest + @swc/jest): `pnpm --filter api test`.'
  has_module rn && echo '- Mobile device E2E (Maestro): `brew install maestro`, app in simulator, then `cd apps/mobile && maestro test .maestro/`.'
  has_module rust && echo '- Rust: `cargo test` at the repo root.'
  echo
  if [ -n "$OP_ACCOUNT" ]; then
    echo '## Secrets (1Password)'
    echo
    echo "apps/web/.env.local is seeded with OP_ACCOUNT=$OP_ACCOUNT / OP_VAULT=${OP_VAULT:-<unset>}. Add op:// references for each secret and run \`scripts/env-pull.sh\` to resolve them via the op CLI (values go straight to the file)."
    echo
  fi
  if has_module rn; then
    echo '## Mobile (Expo)'
    echo
    echo 'First run: `cd apps/mobile && npx expo install --fix` to align Expo-pinned dependency versions, then `pnpm dev`.'
    echo 'Release builds are LOCAL: `npx expo prebuild` then Xcode/fastlane with the same ASC key — Expo modules are fine, EAS/Expo cloud services are not used.'
    echo
  fi
  if has_module data; then
    echo '## 4. Data services'
    echo
    echo '`docker compose -f docker-compose.dev.yml up mongo redis` starts a local Mongo single-node replica set and Redis; `.env.example` already points at them. Copy it to `apps/web/.env.local` and keep the database name ending `_dev` or `_test`, which is what `scripts/lib/assert-local-db.ts` accepts.'
    echo
  fi
  if has_module auth; then
    echo '## Auth & email'
    echo
    echo '- Generate secrets into apps/web/.env.local with `openssl rand -base64 32`: JWT_SECRET (and ADMIN_JWT_SECRET in apps/admin/.env.local). Both must be at least 32 characters; the code refuses shorter ones.'
    echo '- Resend: verify the sender domain, set RESEND_API_KEY + RESEND_FROM_EMAIL. Outside production, email only reaches domains listed in OUTBOUND_ALLOWED_DOMAINS (empty means nobody, BP §24), so add your own domain there to receive sign-in codes locally; or use the Dev login button on /login.'
    has_module admin && echo '- Admin: set ADMIN_EMAILS (comma-separated allowlist) in apps/admin/.env.local.'
    echo
  fi
  if has_module push; then
    echo '## Push (APNs)'
    echo
    echo 'Create a .p8 key (Apple Developer → Keys → APNs), then fill APNS_KEY_ID / APNS_TEAM_ID / APNS_PRIVATE_KEY_B64 (base64 of the .p8) / APNS_BUNDLE_ID in apps/web/.env.local. Sandbox first (APNS_ENVIRONMENT=sandbox).'
    echo
  fi
  if has_module web; then
    echo '## Vercel dashboard'
    echo
    echo 'vercel.json already pins regions to syd1 with a /api/health warm cron. In the dashboard (Project Settings → Functions), set Function CPU to **Performance** — that tier is not expressible in vercel.json.'
    echo
  fi
  if [ -n "$GITHUB_ORG" ]; then
    echo '## GitHub'
    echo
    echo "The remote is set to git@github.com:$GITHUB_ORG/$CODENAME.git. Create it and push:"
    echo '```bash'
    echo "gh repo create $GITHUB_ORG/$CODENAME --private --source \"$PROJECT_DIR\" --push"
    echo '```'
    echo
  fi
  if [ -n "$DESIGN_REF" ]; then
    echo '## Design system'
    echo
    echo "Bootstrap DESIGN.md from the chosen reference before the first UI feature: run the design-md-from-website skill against $DESIGN_REF (it measures real computed styles)."
    echo
  fi
  echo '## Finally'
  echo
  echo "- \`cd $PROJECT_DIR && pnpm dev\` then open http://$HOST"
  echo '- Bootstrap DESIGN.md (the visual source of truth) with the design-md-from-website or design-craft skill before the first UI feature.'
  echo '- Add this project to ~/Dev/ARMADA.md with the armada-sync skill.'
} > "$PROJECT_DIR/SETUP-NEXT-STEPS.md"

echo
echo "== done: $PROJECT_DIR"
echo "   install: ${INSTALL_OK:-skipped/failed}  pin: ${PIN_OK:-skipped/failed}  gate: ${GATE_OK:-skipped/failed}  xcodegen: ${XCODE_OK:-skipped}  cargo: ${RUST_OK:-skipped}"
echo "   manual steps → $PROJECT_DIR/SETUP-NEXT-STEPS.md"
