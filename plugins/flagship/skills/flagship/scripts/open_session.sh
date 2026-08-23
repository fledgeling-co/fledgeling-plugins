#!/bin/zsh
# Open a Ghostty tab and start a session in it, proving FOCUS rather than count.
#
# The failure this exists to prevent, measured 2026-08-23: a tab was opened, the
# tab COUNT was confirmed to move 15 -> 16, and the bootstrap line was then typed
# into whatever had focus -- which was a live session sixteen hours into its own
# campaign. It read the brief and executed it. The work got done; the session it
# was done in was hijacked, and a tab sat empty.
#
# A count moving proves a tab was CREATED. It does not prove keystrokes land in
# it. Those are two claims and only one was checked -- the same shape as every
# other single-field inference in this corpus.
#
# So: type a marker into the tab first and read it back out of the tab's own
# title before typing anything that matters. If the marker does not come back,
# nothing is typed at all.
set -u
BRIEF="${1:?usage: open_session.sh <brief-file> [cwd]}"
CWD="${2:-$HOME/Dev}"
[ -r "$BRIEF" ] || { print -u2 "no such brief: $BRIEF"; exit 1; }

MARK="spawn-$$-$(od -An -N2 -tu2 < /dev/urandom | tr -d ' ')"
BOOT="/tmp/${MARK}.sh"
cat > "$BOOT" <<BOOTEOF
#!/bin/zsh
cd $(printf %q "$CWD") || return 1
exec claude --dangerously-skip-permissions "\$(cat $(printf %q "$BRIEF"))"
BOOTEOF
chmod +x "$BOOT"

count() {
  osascript -e 'tell application "System Events" to tell process "ghostty"
    try
      return (count of radio buttons of tab group 1 of window 1) as string
    on error
      return "1"
    end try
  end tell' 2>/dev/null
}
before=$(count)
osascript -e 'tell application "Ghostty" to activate
delay 0.4
tell application "System Events" to tell process "ghostty"
  click menu item "New Tab" of menu 1 of menu bar item "File" of menu bar 1
end tell' >/dev/null 2>&1

for i in {1..15}; do sleep 0.4; [ "$(count)" = "$((before+1))" ] && break; done
[ "$(count)" = "$((before+1))" ] || { print -u2 "no new tab (count stayed $before) — typed nothing"; exit 1; }

# SELECT the new tab. Creating a tab does not necessarily focus it -- measured:
# the count moved to 17 while the front window title still read another
# session's cwd, so the focus proof refused (correctly) and nothing was typed.
# Clicking the last radio button in the tab group is what actually activates it.
osascript -e 'tell application "Ghostty" to activate
delay 0.3
tell application "System Events" to tell process "ghostty"
  try
    set tabs_ to radio buttons of tab group 1 of window 1
    click (item -1 of tabs_)
  end try
end tell' >/dev/null 2>&1
sleep 1.5

# PROVE FOCUS. Set the tab's own title to the marker, then read the FRONT tab's
# title back. A shell that received the keystroke is the shell that renames it;
# a live Claude session would render the text as a prompt and never set a title.
osascript -e "tell application \"Ghostty\" to activate
delay 0.3
tell application \"System Events\" to keystroke \"printf '\\\\033]0;${MARK}\\\\007'\"
delay 0.2
tell application \"System Events\" to key code 36" >/dev/null 2>&1
sleep 1.2
title=$(osascript -e 'tell application "System Events" to tell process "ghostty"
  try
    return (value of attribute "AXTitle" of window 1) as string
  on error
    return ""
  end try
end tell' 2>/dev/null)

case "$title" in
  *"$MARK"*) : ;;
  *) print -u2 "FOCUS NOT PROVEN — front window title is '${title}', expected to contain '${MARK}'."
     print -u2 "Typed a title escape only; no brief was sent. Nothing was delivered to another session."
     exit 2 ;;
esac

osascript -e "tell application \"Ghostty\" to activate
delay 0.3
tell application \"System Events\" to keystroke \"source ${BOOT}\"
delay 0.35
tell application \"System Events\" to key code 36" >/dev/null 2>&1
print -r -- "focus proven via ${MARK}; brief sent from ${BOOT}"
