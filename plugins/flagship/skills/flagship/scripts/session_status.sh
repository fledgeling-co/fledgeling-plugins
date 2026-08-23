#!/bin/zsh
# One board read, one fleet read, one line per live session.
#
# Exists because every figure here has a shelf life and this file's author held
# five of them too long in one night. Prints the timestamp WITH the numbers, the
# claims as the deduplicated view, and marks holds and exclusions so the output
# cannot be mistaken for a dispatchable set.
set -u
BERTHS=${FLAGSHIP_BERTHS:-$HOME/Dev/fledgeling-plugins/plugins/harbourmaster/skills/harbourmaster/scripts/berths.py}
print -r -- "== berths at $(date '+%H:%M:%S') =="
python3 "$BERTHS" 2>/dev/null | python3 -c '
import json,sys
d=json.load(sys.stdin)
print("  available",d["available"],"ceiling",d["ceiling"],"in_use",d["in_use"],"/",d["capacity"],
      "|",d["pressure"]["overall"],"|",d["load_per_core"],"per core")
for c in d.get("claims",[]): print("   ",c["slots"],c["project"],"/",c["label"])
'
print -r -- "== sessions =="
for f in $HOME/.claude/sessions/*.json(N); do
  python3 - "$f" <<'PY' 2>/dev/null
import json,sys,os,time,glob
d=json.load(open(sys.argv[1])); pid=d.get("pid"); name=d.get("name") or ""
if not pid or os.system(f"kill -0 {pid} 2>/dev/null")!=0: sys.exit()
held=set()
for hf in glob.glob(os.path.expanduser("~/.claude/flagship/holds/*.hold")):
    try:
        if time.time()-os.path.getmtime(hf) < 4*3600: held.add(open(hf).read().strip())
    except OSError: pass
st=d.get("status") or "unknown"
tag="(held)" if name in held else ""
print(f"  {st:<7} {tag}{name}")
PY
done | sort
print -r -- "  load: $(sysctl -n vm.loadavg)"
