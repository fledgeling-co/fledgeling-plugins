#!/usr/bin/env bash
# Bring up N parallel audit lanes for a mockup-fidelity React Native re-audit.
#
# A single iOS simulator is a SERIAL resource — one agent at a time. To audit N
# frames at once, run N fully INDEPENDENT lanes, each its own:
#   git worktree  +  APFS-cloned node_modules  +  RN harness (own collector port)
#   +  its own Metro (own port)  +  its own iOS sim.
# Nothing is shared mutable: edits, commits, Metro hot-reload, and harness dumps
# are all per-lane, so the lanes can't corrupt each other. The user authenticates
# each new sim once it's up (Auth0 OTP can't be automated).
#
# Usage:  bash lanes-up.sh 2 3        # bring up lanes 2 and 3 (lane 0 = main tree)
# Writes the lane ledger to $MAIN/.mockup-fidelity/lanes/_lanes.json, which the
# parallel workflow (reaudit-parallel.workflow.js) reads via args.
# See references/batch-orchestration.md "Parallelism on a serial target".
set -uo pipefail

# ── CONFIG (fill in for your project) ────────────────────────────────────────
MAIN=/ABS/PATH/TO/main-repo                     # repo root (lane 0 = this tree)
APP_REL=apps/<app>                              # RN app dir, relative to repo root
SKILL=/ABS/PATH/TO/plugins/mockup-fidelity/skills/mockup-fidelity
BASE_REF=staging                                # branch each lane worktree bases on
SRC_SIM=<LANE0-SIM-UDID>                         # sim with the app installed (source of the .app)
BUNDLE_ID=<com.example.app>
DEVICE_TYPE="iPhone 16 Pro Max"                  # keep all lanes on ONE viewport
# Ports: lane K uses Metro 8082+K and collector 8799+K (lane 0 = 8082/8799).
# ─────────────────────────────────────────────────────────────────────────────

LANES_JSON=$MAIN/.mockup-fidelity/lanes/_lanes.json
mkdir -p "$MAIN/.mockup-fidelity/lanes"
APP0=$(xcrun simctl get_app_container "$SRC_SIM" "$BUNDLE_ID" 2>/dev/null)
[ -z "$APP0" ] && { echo "FATAL: source sim app container not found"; exit 1; }
rm -rf /tmp/mf-lane.app && cp -R "$APP0" /tmp/mf-lane.app

up_lane() {
  local K=$1
  local WT=$MAIN-lane-$K APPDIR=$MAIN-lane-$K/$APP_REL BRANCH=reaudit-lane-$K
  local METRO=$((8082 + K)) COLL=$((8799 + K))
  # Dump dir MUST be OUTSIDE every Metro watch root (a dump inside the tree → infinite
  # reload loop; see rn-harness/README.md GOTCHA #1). /tmp is safe for ALL lanes incl. lane 0.
  local LANEDIR=/tmp/mf-lane$K-dump DUMP=/tmp/mf-lane$K-dump/_latest.json
  mkdir -p "$LANEDIR"
  echo "════ LANE $K  (metro :$METRO  collector :$COLL  branch $BRANCH) ════"

  # 1. sim — reuse mf-lane-$K else create one on the chosen device type
  local SIM; SIM=$(xcrun simctl list devices | grep "mf-lane-$K (" | grep -oE "[0-9A-F-]{36}" | head -1)
  [ -z "$SIM" ] && SIM=$(xcrun simctl create "mf-lane-$K" "$DEVICE_TYPE") && echo "created sim $SIM"
  xcrun simctl boot "$SIM" 2>/dev/null
  xcrun simctl install "$SIM" /tmp/mf-lane.app
  xcrun simctl spawn "$SIM" defaults write "$BUNDLE_ID" RCT_jsLocation "localhost:$METRO"

  # 2. worktree on its own branch
  [ -d "$WT" ] || git -C "$MAIN" worktree add -b "$BRANCH" "$WT" "$BASE_REF" 2>&1 | tail -1

  # 3. node_modules — APFS CLONEFILE, never a symlink.
  #    A symlinked node_modules breaks Metro's resolver ("Unable to resolve
  #    ./node_modules/<entry>") — Metro won't crawl through the symlink. `cp -cR`
  #    is an APFS copy-on-write clone: a REAL directory, near-instant, tiny disk.
  if [ ! -e "$APPDIR/node_modules/.bin" ]; then
    rm -f "$APPDIR/node_modules"; cp -cR "$MAIN/$APP_REL/node_modules" "$APPDIR/node_modules"; echo "node_modules cloned (APFS)"
  fi

  # 3b. .env (and other gitignored runtime config) — a fresh worktree checkout does NOT
  #     carry gitignored files, so the app boots without dev-login secrets / BFF origin /
  #     feature gates (dev-login button never renders; requests hit the wrong backend).
  #     Copy it BEFORE Metro starts (env inlines at bundle time).
  [ -f "$MAIN/$APP_REL/.env" ] && cp "$MAIN/$APP_REL/.env" "$APPDIR/.env"

  # 4. harness (own collector port) + skip-worktree in this worktree's index
  mkdir -p "$APPDIR/.audit"; cp "$MAIN/$APP_REL/.audit/measure.js" "$APPDIR/.audit/measure.js"
  local LAYOUT="$APPDIR/app/_layout.tsx"
  grep -q "__MF_COLLECTOR" "$LAYOUT" || { local T; T=$(mktemp); { echo "if (__DEV__) { try { global.__MF_COLLECTOR = 'http://localhost:$COLL/dump'; require('../.audit/measure'); } catch {} }"; echo; cat "$LAYOUT"; } > "$T"; mv "$T" "$LAYOUT"; }
  git -C "$WT" update-index --skip-worktree "$APP_REL/app/_layout.tsx"

  # 5. collector (writes _latest.json into this lane's dir)
  lsof -ti :$COLL >/dev/null 2>&1 || { node "$SKILL/assets/rn-harness/collector.js" "$LANEDIR" "$COLL" > "/tmp/collector-lane$K.log" 2>&1 & echo "collector :$COLL up"; }

  # 6. Metro for the worktree (own port, --clear to crawl the cloned node_modules)
  lsof -ti :$METRO >/dev/null 2>&1 || ( cd "$APPDIR" && RCT_METRO_PORT=$METRO nohup npx expo start --port "$METRO" --dev-client --clear > "/tmp/metro-lane$K.log" 2>&1 & )
  for i in $(seq 1 40); do [ "$(curl -s http://localhost:$METRO/status 2>/dev/null)" = "packager-status:running" ] && break; sleep 2; done

  # 7. launch -> bundle build -> first harness dump
  local B; B=$(stat -f %m "$DUMP" 2>/dev/null || echo 0)
  xcrun simctl terminate "$SIM" "$BUNDLE_ID" 2>/dev/null; sleep 1; xcrun simctl launch "$SIM" "$BUNDLE_ID" >/dev/null
  local N; for i in $(seq 1 120); do N=$(stat -f %m "$DUMP" 2>/dev/null || echo 0); [ "$N" -gt "$B" ] && break; sleep 2; done
  [ "$N" -gt "$B" ] && echo "LANE $K READY ✓ — sim $SIM AWAITS LOGIN (dump $DUMP)" || echo "LANE $K: no dump — see /tmp/metro-lane$K.log"

  echo "{\"id\":$K,\"simUdid\":\"$SIM\",\"metroPort\":$METRO,\"collectorPort\":$COLL,\"worktree\":\"$WT\",\"appDir\":\"$APP_REL\",\"appDump\":\"$DUMP\",\"branch\":\"$BRANCH\"}" >> "$LANES_JSON.tmp"
}

for K in "$@"; do up_lane "$K"; done
[ -f "$LANES_JSON.tmp" ] && { node -e "const fs=require('fs');const rows=fs.readFileSync('$LANES_JSON.tmp','utf8').trim().split('\n').filter(Boolean).map(JSON.parse);const b={};for(const r of rows)b[r.id]=r;fs.writeFileSync('$LANES_JSON',JSON.stringify(Object.values(b).sort((a,b)=>a.id-b.id),null,2));"; rm -f "$LANES_JSON.tmp"; echo "=== lanes ledger ==="; cat "$LANES_JSON"; }

# TEARDOWN (after the run): for each lane K -> merge its branch, then
#   git -C $MAIN-lane-K update-index --no-skip-worktree $APP_REL/app/_layout.tsx
#   git -C $MAIN worktree remove $MAIN-lane-K --force ; git -C $MAIN branch -D reaudit-lane-K
#   kill the lane's Metro/collector ; xcrun simctl shutdown <sim> (or delete mf-lane-K)
