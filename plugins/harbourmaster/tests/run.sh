#!/usr/bin/env bash
# Gate tests for check_surface.py — the phantom-argument guard.
#
# berths.py silently ignores arguments it does not parse, so an instruction
# telling a runner `berths.py claim` reads the status report and exits 0 with
# nothing held. A guard for that class has to be watched failing before it is
# trusted, so this proves each direction fires on a fixture built to trip it,
# and then proves the real tree is clean.
#
#   ./tests/run.sh        # quiet unless something fails
#   ./tests/run.sh -v     # show each case's output
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
GUARD="$HERE/check_surface.py"
VERBOSE="${1:-}"
PASS=0; FAIL=0
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT

say() { [ "$VERBOSE" = "-v" ] && echo "$@"; return 0; }

# Assert the guard's exit code and that its output carries a distinguishing
# phrase — exit code alone would not prove the RIGHT check fired.
expect() {
  local label="$1" want="$2" phrase="$3"; shift 3
  local out rc
  out="$("$@" 2>&1)"; rc=$?
  if [ "$rc" != "$want" ]; then
    echo "FAIL  $label: exit $rc, wanted $want"; echo "$out" | sed 's/^/      /'
    FAIL=$((FAIL+1)); return
  fi
  if [ -n "$phrase" ] && ! printf '%s' "$out" | grep -qF -e "$phrase"; then
    echo "FAIL  $label: exit $rc but output lacks '$phrase'"
    echo "$out" | sed 's/^/      /'
    FAIL=$((FAIL+1)); return
  fi
  say "pass  $label"
  PASS=$((PASS+1))
}

# --- fixtures ---------------------------------------------------------------
# The bad tokens are assembled at runtime so this file never contains a string
# the guard would flag if the tests/ exclusion ever regressed.
C="cl"; C="$C aim"; CLAIM="${C/ /}"                 # "claim"
FRESH="--fr"; FRESH="${FRESH}esh"                   # "--fresh"

BAD="$WORK/bad"; mkdir -p "$BAD"
{
  printf 'Claim a berth first:\n\n```bash\npython3 berths.py %s --weight 4\n```\n' "$CLAIM"
  printf '\nThen read `berths.py %s` at tick time.\n' "$FRESH"
} > "$BAD/instructions.md"

GOOD="$WORK/good"; mkdir -p "$GOOD"
{
  printf 'Wrap the build:\n\n```bash\n'
  printf 'governor-run --weight 4 --project x --label build -- pnpm build\n'
  printf 'berths.py --quiet\n```\n'
  printf '\nProse about how `berths.py` reports what is free is fine.\n'
} > "$GOOD/instructions.md"

DRIFT="$WORK/scripts"; mkdir -p "$DRIFT"
for s in berths.py pressure.py governor-run demote.py thermal.py; do
  printf '# stub with no flags at all\n' > "$DRIFT/$s"
done

# --- direction 2: the scan --------------------------------------------------
expect "fires on a phantom subcommand"  1 "phantom subcommand" \
  python3 "$GUARD" --root "$BAD"
expect "fires on a phantom flag"        1 "phantom flag" \
  python3 "$GUARD" --root "$BAD"
expect "names the berths-only flag"     1 "$FRESH" \
  python3 "$GUARD" --root "$BAD"
expect "clears a correct fixture"       0 "clean" \
  python3 "$GUARD" --root "$GOOD"

# --- direction 1: the surface table cannot drift ahead of the scripts -------
expect "fails when a declared flag is absent from source" 2 "drifted" \
  env HARBOURMASTER_SCRIPTS_DIR="$DRIFT" python3 "$GUARD" --root "$GOOD"
expect "fails when the scripts are missing" 2 "cannot be verified" \
  env HARBOURMASTER_SCRIPTS_DIR="$WORK/nowhere" python3 "$GUARD" --root "$GOOD"

# --- the real tree ----------------------------------------------------------
expect "the repository is clean" 0 "clean" python3 "$GUARD"

# --- runtime refusal --------------------------------------------------------
# The guard protects instruction files; these prove the scripts themselves no
# longer read as success over an argument they do not parse. pressure.py set
# the family convention (exit 2, name the argument); berths.py and ledger.py
# now follow it. Validation runs before any work, so nothing here reads the
# machine or writes FLEET.md.
S="$HERE/../skills/harbourmaster/scripts"
expect "berths.py refuses a phantom subcommand" 2 "governor-run" \
  python3 "$S/berths.py" "$CLAIM"
expect "berths.py refuses a phantom flag"       2 "unknown argument" \
  python3 "$S/berths.py" "$FRESH"
expect "pressure.py refuses a phantom subcommand" 2 "unknown argument" \
  python3 "$S/pressure.py" "$CLAIM"
expect "ledger.py refuses a phantom flag"       2 "unknown argument" \
  python3 "$S/ledger.py" --bogus

echo "$PASS passed, $FAIL failed"
[ "$FAIL" = "0" ]
