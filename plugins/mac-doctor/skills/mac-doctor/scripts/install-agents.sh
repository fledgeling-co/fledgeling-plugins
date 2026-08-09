#!/usr/bin/env bash
# Install/remove the mac-doctor launchd agents.
#
#   install-agents.sh                 write + load all five tiers
#   install-agents.sh --tiers 15m,1h  only these
#   install-agents.sh --uninstall     bootout + remove plists
#   install-agents.sh --status        loaded? last exit? last run?
#
# launchd rather than cron: it survives reboot, fires a missed run once on wake
# rather than replaying every interval, and reports exit status.
set -uo pipefail

LABEL_PREFIX="gg.rhodes.mac-doctor"
AGENT_DIR="$HOME/Library/LaunchAgents"
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$HOME/.claude/mac-doctor"
LOG_DIR="$STATE_DIR/logs"
ALL_TIERS="15m 1h 12h 1d 7d"

MODE="install"; TIERS="$ALL_TIERS"
while [ $# -gt 0 ]; do
  case "$1" in
    --uninstall) MODE="uninstall"; shift ;;
    --status)    MODE="status"; shift ;;
    --tiers)     TIERS="$(echo "${2:-}" | tr ',' ' ')"; shift 2 ;;
    -h|--help)   sed -n '2,9p' "$0"; exit 0 ;;
    *) shift ;;
  esac
done

mkdir -p "$AGENT_DIR" "$LOG_DIR" "$STATE_DIR/findings"

interval_xml() {
  case "$1" in
    15m) echo "  <key>StartInterval</key><integer>900</integer>" ;;
    1h)  echo "  <key>StartInterval</key><integer>3600</integer>" ;;
    12h) echo "  <key>StartInterval</key><integer>43200</integer>" ;;
    # Off-the-hour on purpose: every scheduler defaulting to 03:00 lands on the
    # same minute, and maintenance competing with maintenance is slower for free.
    1d)  printf '  <key>StartCalendarInterval</key>\n  <dict><key>Hour</key><integer>3</integer><key>Minute</key><integer>17</integer></dict>\n' ;;
    7d)  printf '  <key>StartCalendarInterval</key>\n  <dict><key>Weekday</key><integer>0</integer><key>Hour</key><integer>4</integer><key>Minute</key><integer>23</integer></dict>\n' ;;
  esac
}

# Short tiers run the shell path only: no model, no API spend, 96 runs a day.
# Long tiers get a model for the judgement calls.
program_xml() {
  local tier="$1"
  case "$tier" in
    15m|1h)
      # --apply is what makes these two tiers do anything at all. Without it every
      # run is a dry run that exits 0, and in `launchctl list` a job that found
      # nothing and a job that never acts look identical: PID blank, status 0.
      # These are the bands documented as acting silently, and reclaim.sh gates
      # each action on its own regardless of this flag.
      cat <<XML
  <key>ProgramArguments</key>
  <array>
    <string>$SKILL_DIR/scripts/reclaim.sh</string>
    <string>--tier</string><string>$tier</string>
    <string>--apply</string>
  </array>
XML
      ;;
    *)
      # `claude -p` is non-interactive; nothing in this path may ever prompt,
      # because a prompt under launchd hangs forever holding the agent slot.
      cat <<XML
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string><string>-lc</string>
    <string>command -v claude >/dev/null 2>&amp;1 &amp;&amp; exec claude -p "/mac-doctor $tier" || exec "$SKILL_DIR/scripts/reclaim.sh" --tier $tier</string>
  </array>
XML
      ;;
  esac
}

case "$MODE" in
uninstall)
  for t in $TIERS; do
    launchctl bootout "gui/$UID/$LABEL_PREFIX.$t" 2>/dev/null
    rm -f "$AGENT_DIR/$LABEL_PREFIX.$t.plist"
    echo "removed $LABEL_PREFIX.$t"
  done
  echo "State kept at $STATE_DIR -- the ledger outlives the agents."
  ;;
status)
  printf '%-8s %-10s %-10s %s\n' TIER LOADED "LAST EXIT" "LAST RUN"
  for t in $ALL_TIERS; do
    line=$(launchctl list 2>/dev/null | awk -v l="$LABEL_PREFIX.$t" '$3==l{print $1" "$2}')
    if [ -z "$line" ]; then printf '%-8s %-10s %-10s %s\n' "$t" no - -; continue; fi
    ec=$(echo "$line" | awk '{print $2}')
    lr=$(stat -f '%Sm' -t '%Y-%m-%d %H:%M' "$LOG_DIR/$t.out.log" 2>/dev/null || echo -)
    printf '%-8s %-10s %-10s %s\n' "$t" yes "$ec" "$lr"
  done
  echo
  echo "A nonzero exit with an empty log is almost always PATH: launchd does not"
  echo "source your profile, so docker/git/node/claude are absent unless the"
  echo "plist sets them. This installer copies the invoking shell's PATH in."
  ;;
install)
  for t in $TIERS; do
    plist="$AGENT_DIR/$LABEL_PREFIX.$t.plist"
    { cat <<XML
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>$LABEL_PREFIX.$t</string>
XML
      program_xml "$t"
      interval_xml "$t"
      cat <<XML
  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key><string>$PATH</string>
    <key>HOME</key><string>$HOME</string>
  </dict>
  <key>StandardOutPath</key><string>$LOG_DIR/$t.out.log</string>
  <key>StandardErrorPath</key><string>$LOG_DIR/$t.err.log</string>
  <key>ProcessType</key><string>Background</string>
  <key>LowPriorityIO</key><true/>
  <key>Nice</key><integer>10</integer>
  <key>RunAtLoad</key><false/>
</dict>
</plist>
XML
    } > "$plist"

    plutil -lint "$plist" >/dev/null 2>&1 || { echo "INVALID plist for $t, not loading"; continue; }
    launchctl bootout "gui/$UID/$LABEL_PREFIX.$t" 2>/dev/null
    if launchctl bootstrap "gui/$UID" "$plist" 2>/dev/null; then echo "loaded  $LABEL_PREFIX.$t"
    else echo "WROTE but failed to load $LABEL_PREFIX.$t (try: launchctl bootstrap gui/$UID $plist)"; fi
  done
  echo
  echo "Verify:  $0 --status"
  echo "Logs:    $LOG_DIR/"
  ;;
esac
