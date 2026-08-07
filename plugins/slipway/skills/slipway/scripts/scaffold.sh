#!/usr/bin/env bash
# slipway scaffold.sh — deterministic project scaffolder for ~/Dev projects.
#
# Renders the template tree into a new project directory with token substitution,
# assembles the composite files (Caddyfile, docker-compose, CLAUDE.md, README) from
# per-module fragments, copies the operating specs, initialises git, installs deps,
# generates Xcode projects, and runs the typecheck gate. Designed so the calling
# agent supplies decisions (flags) and the script does the work.
#
# Usage:
#   scaffold.sh --codename loft --display "Loft" \
#     [--description "One-line description"] \
#     [--modules web,api,macos,ios,tokens,data]   # default: web,tokens
#     [--bundle-prefix app.loft]                  # default: app.<codename>
#     [--dest ~/Dev] [--port-web N] [--port-api N] \
#     [--team-files ~/Dev/bella-team-files] \
#     [--no-install] [--dry-run]
#
# Safe by default: refuses to write into an existing directory; --dry-run prints
# the plan (ports, paths, modules) and writes nothing; never runs sudo — hosts and
# Caddy commands are printed and written to SETUP-NEXT-STEPS.md for the user.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TPL="$SCRIPT_DIR/../templates"

CODENAME="" DISPLAY="" DESCRIPTION="" BUNDLE_PREFIX="" MODULES="web,tokens"
DEST="$HOME/Dev" PORT_WEB="" PORT_API="" TEAM_FILES="$HOME/Dev/bella-team-files"
NO_INSTALL=0 DRY_RUN=0 MACOS_STYLE="window" OP_ACCOUNT="" OP_VAULT=""

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
    --dest) DEST="$2"; shift 2;;
    --port-web) PORT_WEB="$2"; shift 2;;
    --port-api) PORT_API="$2"; shift 2;;
    --team-files) TEAM_FILES="$2"; shift 2;;
    --no-install) NO_INSTALL=1; shift;;
    --dry-run) DRY_RUN=1; shift;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

[ -n "$CODENAME" ] || { echo "--codename is required" >&2; exit 2; }
[[ "$CODENAME" =~ ^[a-z][a-z0-9-]*$ ]] || { echo "codename must be lowercase alnum/hyphen, got: $CODENAME" >&2; exit 2; }
[ -n "$DISPLAY" ] || DISPLAY="$(python3 -c "print('$CODENAME'.replace('-',' ').title())")"
[ -n "$DESCRIPTION" ] || DESCRIPTION="$DISPLAY."
[ -n "$BUNDLE_PREFIX" ] || BUNDLE_PREFIX="app.$(echo "$CODENAME" | tr -d '-')"
PROJECT_DIR="$DEST/$CODENAME"

has_module() { case ",$MODULES," in *",$1,"*) return 0;; *) return 1;; esac; }

# module implications: push→auth→data→web (the lib/ stack lives in apps/web);
# admin needs the data services too.
if has_module push && ! has_module auth; then MODULES="auth,$MODULES"; fi
if has_module auth && ! has_module data; then MODULES="data,$MODULES"; fi
if has_module admin && ! has_module data; then MODULES="data,$MODULES"; fi
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

echo "== slipway scaffold"
echo "   project:  $PROJECT_DIR"
echo "   display:  $DISPLAY"
echo "   modules:  $MODULES"
echo "   bundle:   $BUNDLE_PREFIX.<app>"
echo "   ports:    web=$PORT_WEB api=$PORT_API"
echo "   host:     $CODENAME.local"
[ "$DRY_RUN" = 1 ] && { echo "   (dry run — nothing written)"; exit 0; }

PNPM_VERSION="$(pnpm --version 2>/dev/null || echo 10.17.1)"

# ---- render engine: copies a template dir into a target dir.
#   *.tmpl        → token-substituted, suffix stripped
#   dot_<name>    → renamed to .<name> (files or top-level dirs)
#   everything else copied verbatim
export SW_CODENAME="$CODENAME" SW_DISPLAY="$DISPLAY" SW_DESCRIPTION="$DESCRIPTION" \
       SW_BUNDLE_PREFIX="$BUNDLE_PREFIX" SW_PORT_WEB="$PORT_WEB" SW_PORT_API="$PORT_API" \
       SW_PNPM_VERSION="$PNPM_VERSION" SW_YEAR="$(date +%Y)" SW_DATE="$(date +%Y-%m-%d)" SW_PORT_ADMIN="$PORT_ADMIN"
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
has_module web    && render_dir web    "$PROJECT_DIR/apps/web"
has_module api    && render_dir api    "$PROJECT_DIR/apps/api"
has_module macos  && render_dir macos  "$PROJECT_DIR/apps/macos"
has_module ios    && render_dir ios    "$PROJECT_DIR/apps/ios"
has_module tokens && render_dir tokens "$PROJECT_DIR/packages/design-tokens"
has_module data   && render_dir data   "$PROJECT_DIR/apps/web"
has_module auth   && render_dir auth   "$PROJECT_DIR/apps/web"   # overwrites data's models/types with the User-bearing versions
has_module push   && render_dir push   "$PROJECT_DIR/apps/web"
has_module admin  && render_dir admin  "$PROJECT_DIR/apps/admin"

# tokens: generate tokens.css NOW (pure node, no deps) so the committed file is in
# sync and the gate's drift check passes from the first run.
has_module tokens && (cd "$PROJECT_DIR/packages/design-tokens" && node build.mjs >/dev/null)

# rn (React Native / Expo, BP §18): the app plus the monorepo accommodations —
# node-linker=hoisted in the root .npmrc (Metro/autolinking need a flat node_modules).
if has_module rn; then
  render_dir rn      "$PROJECT_DIR/apps/mobile"
  render_dir rn-root "$PROJECT_DIR"
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

# rust: cross-OS core crate + cargo workspace at the root
if has_module rust; then
  render_dir rust      "$PROJECT_DIR"
  render_dir rust-root "$PROJECT_DIR"
fi

# auth/push: merge web deps + env keys
if has_module auth; then
  node -e '
    const fs = require("fs"); const p = process.argv[1];
    const j = JSON.parse(fs.readFileSync(p, "utf8"));
    j.dependencies = { ...j.dependencies, jose: "latest", resend: "latest", "@react-email/components": "latest" };
    fs.writeFileSync(p, JSON.stringify(j, null, 2) + "\n");
  ' "$PROJECT_DIR/apps/web/package.json"
  cat "$TPL/fragments/env/auth.env" >> "$PROJECT_DIR/apps/web/.env.example"
fi
if has_module push; then
  cat "$TPL/fragments/env/push.env" >> "$PROJECT_DIR/apps/web/.env.example"
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
    j.dependencies = { ...j.dependencies, mongoose: "latest", ioredis: "latest" };
    fs.writeFileSync(p, JSON.stringify(j, null, 2) + "\n");
  ' "$PROJECT_DIR/apps/web/package.json"
  cat "$TPL/fragments/env/data.env" >> "$PROJECT_DIR/apps/web/.env.example"
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
assemble caddy   "$PROJECT_DIR/Caddyfile"              web api admin
if has_module web || has_module api || has_module data; then
  assemble compose "$PROJECT_DIR/docker-compose.dev.yml" web api data
fi
assemble claude  "$PROJECT_DIR/CLAUDE.md"              web api rn macos ios tokens data auth admin push rust
assemble readme  "$PROJECT_DIR/README.md"              web api rn macos ios tokens data auth admin push rust

# ---- 3. operating specs + AGENTS.md symlink
mkdir -p "$PROJECT_DIR/docs"
for f in CODING_PRACTICES.md NEW_PROJECT_BEST_PRACTICES.md; do
  if [ -f "$TEAM_FILES/$f" ]; then cp "$TEAM_FILES/$f" "$PROJECT_DIR/docs/$f"
  else echo "WARN: $TEAM_FILES/$f not found — docs/$f not copied" >&2; fi
done
mkdir -p "$PROJECT_DIR/docs/features-to-triage" "$PROJECT_DIR/docs/specs" "$PROJECT_DIR/docs/plans" "$PROJECT_DIR/design/mocks/html"
printf '# LEDGER\n\n| ID | Feature | Status |\n|---|---|---|\n' > "$PROJECT_DIR/docs/features-to-triage/LEDGER.md"
ln -s CLAUDE.md "$PROJECT_DIR/AGENTS.md"

# ---- 4. guard: no unrendered tokens
if grep -rn "{{[A-Z_]*}}" "$PROJECT_DIR" --include='*' -l 2>/dev/null | grep -q .; then
  echo "ERROR: unrendered template tokens remain:" >&2
  grep -rn "{{[A-Z_]*}}" "$PROJECT_DIR" -l >&2
  exit 1
fi

# ---- 5. git + install + native projects + gate
cd "$PROJECT_DIR"
git init -q -b main
git add -A
git commit -qm "Scaffold $DISPLAY via slipway (modules: $MODULES)"

INSTALL_OK=""; GATE_OK=""; XCODE_OK=""
if [ "$NO_INSTALL" = 0 ] && [ -f package.json ]; then
  if pnpm install --silent; then
    INSTALL_OK=yes
    if pnpm turbo run typecheck build --output-logs=errors-only; then GATE_OK=yes; fi
  fi
fi
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
if [ -n "$INSTALL_OK" ] || [ -n "$XCODE_OK" ] || [ -n "$RUST_OK" ]; then
  git add -A && git commit -qm "Post-scaffold: lockfile + generated projects" 2>/dev/null || true
fi

# ---- 6. next-steps file (the only manual part: sudo + accounts)
{
  render_fragment "fragments/next-steps/header.tmpl"
  echo
  echo '## 1. Hosts + Caddy (needs sudo — run these yourself)'
  echo
  echo '```bash'
  hosts_line="127.0.0.1 $CODENAME.local\\n127.0.0.1 api.$CODENAME.local"
  has_module admin && hosts_line="$hosts_line\\n127.0.0.1 admin.$CODENAME.local"
  echo "sudo sh -c 'printf \"$hosts_line\\n\" >> /etc/hosts'"
  echo "sed '/^{/,/^}/d' \"$PROJECT_DIR/Caddyfile\" | sudo tee /opt/homebrew/etc/caddy/conf.d/$CODENAME.caddy >/dev/null"
  echo 'sudo caddy reload --config /opt/homebrew/etc/Caddyfile   # or: sudo brew services start caddy'
  echo '```'
  echo
  has_module web && { echo '## 2. Vercel'; echo; echo '```bash'; echo "cd $PROJECT_DIR/apps/web && vercel link"; echo '```'; echo; }
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
  has_module web && echo '- Web e2e (Playwright): one-time `pnpm --filter web exec playwright install chromium`, then `pnpm --filter web test:e2e`. Build suites with the acceptance-e2e skill.'
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
    echo 'Fill MONGODB_URI and REDIS_URL in apps/web/.env.local (or `docker compose -f docker-compose.dev.yml up` for local Mongo+Redis).'
    echo
  fi
  if has_module auth; then
    echo '## Auth & email'
    echo
    echo '- Generate secrets into apps/web/.env.local: `openssl rand -base64 32` for JWT_SECRET (and ADMIN_JWT_SECRET in apps/admin/.env.local).'
    echo '- Resend: verify the sender domain, set RESEND_API_KEY + RESEND_FROM_EMAIL. Until then the code email will fail — use the Dev login button on /login (non-prod only).'
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
  echo '## Finally'
  echo
  echo "- \`cd $PROJECT_DIR && pnpm dev\` then open http://$CODENAME.local"
  echo '- Bootstrap DESIGN.md (the visual source of truth) with the design-md-from-website or design-craft skill before the first UI feature.'
  echo '- Add this project to ~/Dev/ARMADA.md with the armada-sync skill.'
} > "$PROJECT_DIR/SETUP-NEXT-STEPS.md"

echo
echo "== done: $PROJECT_DIR"
echo "   install: ${INSTALL_OK:-skipped/failed}  gate(typecheck+build): ${GATE_OK:-skipped/failed}  xcodegen: ${XCODE_OK:-skipped}  cargo: ${RUST_OK:-skipped}"
echo "   manual steps → $PROJECT_DIR/SETUP-NEXT-STEPS.md"
