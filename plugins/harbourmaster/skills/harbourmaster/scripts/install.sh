#!/usr/bin/env bash
# Install (or inspect) harbourmaster's background agents and privilege grants.
#
# Nothing here runs as a side effect of using the skill. The wrapper and the
# reports work with none of it; this adds the two things a one-shot invocation
# cannot do — sample thermals across a dwell window, and notice pressure
# between sessions.
set -uo pipefail

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export SKILL_DIR
HOME_DIR="${HARBOURMASTER_HOME:-$HOME/.claude/harbourmaster}"
AGENT_DIR="$HOME/Library/LaunchAgents"
LABEL_GOV="gg.fledgeling.harbourmaster.governor"
LABEL_THERM="gg.fledgeling.harbourmaster.thermal"
PY="$(command -v python3)"

usage() {
  cat <<'USAGE'
Usage: install.sh [--status] [--install] [--uninstall] [--grants]

  --status     What is installed, what is granted, what is running (default)
  --grants     Report the sudo grants the thermal lane needs, and how to add
               any that are missing. Prints commands; runs none of them.
  --install    Load the governor and thermal LaunchAgents
  --uninstall  Unload and remove them; restores any demoted process first
USAGE
}

# ---------------------------------------------------------------- grants ----
# The thermal lane needs to READ powermetrics and, to act, to WRITE pmset.
# Both are root-only. This never edits sudoers: it reports, and prints what a
# human would run. Editing the privilege table of a machine is not something a
# skill should do on its own.
check_grants() {
  local read_ok write_ok
  sudo -n powermetrics -n 1 -i 200 --samplers cpu_power >/dev/null 2>&1 \
    && read_ok=yes || read_ok=no
  sudo -n pmset -g custom >/dev/null 2>&1 && write_ok=yes || write_ok=no

  echo "sudo grants"
  echo "  powermetrics (read frequency)   : $read_ok"
  echo "  pmset        (set power mode)   : $write_ok"
  echo
  if [[ -e /etc/sudoers.d/zephyr-powermetrics || -e /etc/sudoers.d/zephyr-pmset ]]; then
    echo "  Existing rules found under /etc/sudoers.d (installed by the zephyr"
    echo "  project). harbourmaster reuses them and adds nothing."
    echo
  fi
  if [[ "$read_ok" == no ]]; then
    cat <<'GRANT'
  To grant the READ (throttle detection cannot work without it):
    echo "$(id -un) ALL=(root) NOPASSWD: /usr/bin/powermetrics" \
      | sudo tee /etc/sudoers.d/harbourmaster-powermetrics
    sudo chmod 440 /etc/sudoers.d/harbourmaster-powermetrics

GRANT
  fi
  if [[ "$write_ok" == no ]]; then
    cat <<'GRANT'
  To grant the WRITE (switching to High Power). Scoped to powermode alone,
  so it cannot change sleep, hibernation or wake behaviour:
    printf '%s ALL=(root) NOPASSWD: /usr/bin/pmset -c powermode 0, /usr/bin/pmset -c powermode 2\n' "$(id -un)" \
      | sudo tee /etc/sudoers.d/harbourmaster-pmset
    sudo chmod 440 /etc/sudoers.d/harbourmaster-pmset

GRANT
  fi
  [[ "$read_ok" == yes && "$write_ok" == yes ]] && echo "  Nothing to add."
}

write_agent() {
  local label="$1" interval="$2"; shift 2
  local plist="$AGENT_DIR/$label.plist"
  mkdir -p "$AGENT_DIR" "$HOME_DIR/logs"
  {
    echo '<?xml version="1.0" encoding="UTF-8"?>'
    echo '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">'
    echo '<plist version="1.0"><dict>'
    echo "  <key>Label</key><string>$label</string>"
    echo '  <key>ProgramArguments</key><array>'
    for arg in "$@"; do echo "    <string>$arg</string>"; done
    echo '  </array>'
    echo "  <key>StartInterval</key><integer>$interval</integer>"
    echo "  <key>StandardOutPath</key><string>$HOME_DIR/logs/$label.log</string>"
    echo "  <key>StandardErrorPath</key><string>$HOME_DIR/logs/$label.err</string>"
    # Nice the agent itself: a governor that competes for the CPU it is
    # measuring changes the number it reports.
    echo '  <key>Nice</key><integer>10</integer>'
    echo '  <key>ProcessType</key><string>Background</string>'
    echo '</dict></plist>'
  } > "$plist"
  launchctl unload "$plist" 2>/dev/null
  launchctl load "$plist" 2>/dev/null && echo "  loaded $label" \
    || echo "  FAILED to load $label"
}

do_install() {
  echo "installing agents"
  # 60s: fast enough to catch a pinned machine, slow enough that the sampling
  # is not itself a load.
  write_agent "$LABEL_GOV" 60 "$PY" "$SKILL_DIR/demote.py" --apply
  # 300s, each run sampling 60s — the dwell the user asked for. Two agents
  # rather than one because their cadences and costs differ by an order.
  write_agent "$LABEL_THERM" 300 "$PY" "$SKILL_DIR/thermal.py" --duration 60
  echo
  echo "note: the governor agent only acts at CRITICAL pressure, never kills,"
  echo "      and restores what it demoted once pressure returns to healthy."
}

do_uninstall() {
  echo "restoring anything demoted"
  "$PY" "$SKILL_DIR/demote.py" --restore --apply >/dev/null 2>&1
  for label in "$LABEL_GOV" "$LABEL_THERM"; do
    local plist="$AGENT_DIR/$label.plist"
    [[ -e "$plist" ]] || continue
    launchctl unload "$plist" 2>/dev/null
    rm -f "$plist" && echo "  removed $label"
  done
}

do_status() {
  echo "harbourmaster"
  echo "  home     : $HOME_DIR"
  echo "  scripts  : $SKILL_DIR"
  echo
  echo "agents"
  for label in "$LABEL_GOV" "$LABEL_THERM"; do
    if launchctl list 2>/dev/null | grep -q "$label"; then
      echo "  $label : loaded"
    else
      echo "  $label : not installed"
    fi
  done
  echo
  check_grants
  echo
  echo "berths"
  "$PY" - <<'PYBERTH'
import json, subprocess, sys, os
script = os.path.join(os.environ["SKILL_DIR"], "berths.py")
try:
    out = subprocess.run([sys.executable, script], capture_output=True,
                         text=True, timeout=60)
    d = json.loads(out.stdout)
    print(f"  {d['in_use']}/{d['ceiling']} in use, {d['available']} available"
          f" ({d['pressure']['overall']} pressure, load/core {d['load_per_core']})")
except Exception as exc:
    print(f"  (unavailable: {exc})")
PYBERTH
}

case "${1:---status}" in
  --install)   do_install ;;
  --uninstall) do_uninstall ;;
  --grants)    check_grants ;;
  --status)    do_status ;;
  -h|--help)   usage ;;
  *)           usage; exit 64 ;;
esac
