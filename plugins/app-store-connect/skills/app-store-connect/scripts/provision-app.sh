#!/usr/bin/env bash
# provision-app.sh — the App Store Connect side of a new app: bundle ID, capabilities and,
# optionally, the app record. Plans by default and sends no write; --apply performs the writes.
#
# Exit codes: 0 plan printed or apply finished; 1 an asc call failed; 2 bad arguments;
# 3 the asc profile does not belong to the team it is mapped to.
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: provision-app.sh --team TEAM --identifier REVERSE.DNS --name NAME [options]

TEAM is a key under "teams" in ~/.config/app-store-connect/accounts.json
(or $ASC_ACCOUNTS_DIR/accounts.json); references/accounts-file.md gives the format.

Plans by default: every asc call runs with --read-only and nothing is written.

Options:
  --platform IOS|MAC_OS|UNIVERSAL       bundle ID platform (default UNIVERSAL)
  --entitlements PATH                   reconcile capabilities from this .entitlements file
  --capability TYPE                     add one capability, repeatable (e.g. PUSH_NOTIFICATIONS)
  --app-record                          also create the App Store Connect app record (web session)
  --app-name NAME                       store name for --app-record (default: --name)
  --sku SKU                             SKU for --app-record (default: the identifier)
  --app-platform IOS|MAC_OS|UNIVERSAL   platform for --app-record (default IOS)
  --apply                               perform the writes
EOF
}

team="" identifier="" name="" platform="UNIVERSAL" entitlements="" app_record=0
app_name="" sku="" app_platform="IOS" apply=0
capabilities=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --team) team="${2:-}"; shift 2 ;;
    --identifier) identifier="${2:-}"; shift 2 ;;
    --name) name="${2:-}"; shift 2 ;;
    --platform) platform="${2:-}"; shift 2 ;;
    --entitlements) entitlements="${2:-}"; shift 2 ;;
    --capability) capabilities+=("${2:-}"); shift 2 ;;
    --app-record) app_record=1; shift ;;
    --app-name) app_name="${2:-}"; shift 2 ;;
    --sku) sku="${2:-}"; shift 2 ;;
    --app-platform) app_platform="${2:-}"; shift 2 ;;
    --apply) apply=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "provision-app: unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if [[ -z "$team" || -z "$identifier" || -z "$name" ]]; then
  usage >&2; exit 2
fi
if [[ -n "$entitlements" && ! -f "$entitlements" ]]; then
  echo "provision-app: entitlements file not found: $entitlements" >&2; exit 2
fi

# Account details live outside this public script, in the private accounts file.
accounts_file="${ASC_ACCOUNTS_DIR:-$HOME/.config/app-store-connect}/accounts.json"
if [[ ! -f "$accounts_file" ]]; then
  echo "provision-app: no accounts file at $accounts_file; build it as references/accounts-file.md describes" >&2
  exit 2
fi
team_fields=$(python3 - "$accounts_file" "$team" <<'PY'
import json, sys
teams = json.load(open(sys.argv[1])).get("teams", {})
t = teams.get(sys.argv[2])
if not t:
    sys.stderr.write("provision-app: --team must be one of: %s\n" % ", ".join(sorted(teams)))
    sys.exit(2)
missing = [k for k in ("profile", "team_id", "apple_id") if not t.get(k)]
if missing:
    sys.stderr.write("provision-app: team %s is missing %s in the accounts file\n" % (sys.argv[2], ", ".join(missing)))
    sys.exit(2)
print(t["profile"], t["team_id"], t["apple_id"])
PY
) || exit 2
read -r profile team_id apple_id <<<"$team_fields"
app_name="${app_name:-$name}"
sku="${sku:-$identifier}"

mode="PLAN"; ro=(--read-only)
if [[ $apply -eq 1 ]]; then mode="APPLY"; ro=(); fi

say() { printf '%s\n' "$*"; }

# asc writes JSON to stdout and warnings to stderr; keep them apart so the JSON parses.
asc_json() { asc --profile "$profile" ${ro[@]+"${ro[@]}"} "$@" --output json 2>/dev/null; }

json_field() {
  # json_field <python expression over d> — reads JSON on stdin, prints the expression.
  python3 -c "import json,sys; d=json.load(sys.stdin); print($1)"
}

say "provision-app: $mode on team $team ($team_id) with asc profile '$profile'"

# 1. Prove the profile reaches the team it is mapped to, before anything else is read or written.
seed=$(asc_json bundle-ids list --limit 1 | json_field "(d.get('data') or [{}])[0].get('attributes',{}).get('seedId','')") || {
  echo "provision-app: asc --profile $profile could not list bundle IDs; run: asc auth doctor" >&2; exit 1; }
if [[ -n "$seed" && "$seed" != "$team_id" ]]; then
  echo "provision-app: profile '$profile' lists bundle IDs under team $seed, not $team_id; stopping" >&2
  exit 3
fi

lookup_bundle() {
  asc_json bundle-ids list --identifier "$identifier" --limit 200 | python3 -c '
import json, sys
d = json.load(sys.stdin)
for b in d.get("data", []):
    if b["attributes"].get("identifier") == sys.argv[1]:
        print(b["id"]); break
' "$identifier"
}

# 2. Bundle ID.
rid=$(lookup_bundle)
if [[ -n "$rid" ]]; then
  say "bundle ID: $identifier exists (resource $rid); no change"
elif [[ $apply -eq 0 ]]; then
  say "bundle ID: $identifier does not exist; --apply creates it as $platform named \"$name\""
else
  asc --profile "$profile" bundle-ids create --identifier "$identifier" --name "$name" \
    --platform "$platform" --output json >/dev/null
  rid=$(lookup_bundle)
  if [[ -z "$rid" ]]; then
    echo "provision-app: create returned but $identifier does not read back; check asc bundle-ids list" >&2
    exit 1
  fi
  say "bundle ID: created $identifier (resource $rid)"
fi

# 3. Capabilities from an entitlements file: reconcile plans adds/updates and preserves the rest.
if [[ -n "$entitlements" ]]; then
  if [[ -z "$rid" ]]; then
    say "capabilities: after the bundle ID exists, reconcile from $entitlements"
  elif [[ $apply -eq 0 ]]; then
    say "capabilities: reconcile plan from $entitlements"
    asc --profile "$profile" --read-only bundle-ids capabilities reconcile plan \
      --bundle "$rid" --entitlements "$entitlements" --output table
  else
    asc --profile "$profile" bundle-ids capabilities reconcile apply \
      --bundle "$rid" --entitlements "$entitlements" --confirm --output table
  fi
fi

# 4. Individually named capabilities, skipped when already enabled.
if [[ ${#capabilities[@]} -gt 0 ]]; then
  existing=""
  if [[ -n "$rid" ]]; then
    existing=$(asc_json bundle-ids capabilities list --bundle "$rid" | \
      json_field "' '.join(c['attributes'].get('capabilityType','') for c in d.get('data',[]))")
  fi
  for cap in "${capabilities[@]}"; do
    if [[ " $existing " == *" $cap "* ]]; then
      say "capability: $cap already enabled; no change"
    elif [[ $apply -eq 0 || -z "$rid" ]]; then
      say "capability: --apply adds $cap"
    else
      asc --profile "$profile" bundle-ids capabilities add --bundle "$rid" --capability "$cap" \
        --if-exists skip --output json >/dev/null
      say "capability: added $cap"
    fi
  done
fi

# 5. Push needs a team APNs key as well as the capability; the API cannot create one.
wants_push=0
for cap in "${capabilities[@]+"${capabilities[@]}"}"; do
  [[ "$cap" == "PUSH_NOTIFICATIONS" ]] && wants_push=1
done
if [[ -n "$entitlements" ]] && grep -q "aps-environment" "$entitlements"; then wants_push=1; fi
if [[ $wants_push -eq 1 ]]; then
  say "push: the capability is handled above; sending also needs the team's APNs key (SKILL.md step 7)"
fi

# 6. App Store Connect app record, through a web session. --if-exists skip makes a re-run safe;
#    --auto-rename=false stops asc from creating the app under a suffixed name if the name is taken.
if [[ $app_record -eq 1 ]]; then
  existing_app=$(asc_json apps list --bundle-id "$identifier" | \
    json_field "(d.get('data') or [{}])[0].get('id','')")
  if [[ -n "$existing_app" ]]; then
    say "app record: exists for $identifier (app $existing_app); no change"
  elif [[ $apply -eq 0 ]]; then
    say "app record: --apply creates \"$app_name\" (SKU $sku, $app_platform) as $apple_id"
  else
    asc --profile "$profile" web apps create --apple-id "$apple_id" --name "$app_name" \
      --bundle-id "$identifier" --sku "$sku" --platform "$app_platform" \
      --if-exists skip --auto-rename=false \
      --two-factor-method sms --two-factor-code-command "asc web auth messages-code --timeout 50s" \
      --output json >/dev/null
    created_app=$(asc --profile "$profile" --read-only apps list --bundle-id "$identifier" --output json 2>/dev/null | \
      json_field "(d.get('data') or [{}])[0].get('id','')")
    if [[ -z "$created_app" ]]; then
      echo "provision-app: apps create returned but no app reads back for $identifier" >&2; exit 1
    fi
    say "app record: created (app $created_app)"
  fi
fi

say "provision-app: $mode finished"
