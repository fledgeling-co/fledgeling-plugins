#!/usr/bin/env bash
# Does the skill fire on its own, and stay out of the way when it should not?
#
# This is a control, not a benchmark: one positive and one near-miss. It
# exists because the obvious way to measure triggering failed twice, both
# times for the same reason, and the failure looked exactly like a broken
# description.
#
#   attempt 1  skill-creator's run_loop over twenty one-line queries.
#              0% recall on the shipped description AND on a full rewrite,
#              identical to the digit. Bare conversational prompts carry no
#              work, and Claude only consults a skill for work it cannot do
#              inline, so nothing ever triggered.
#   attempt 2  a substantive-sounding prompt in an empty directory. The run
#              refused it and said why: "this app" had no referent, so there
#              was nothing to add offline support to and no fork to ask about.
#   attempt 3  this one. A real app, from fixtures/offline-app, whose README
#              says coverage on site is bad, so the fork is genuine.
#
# The lesson generalises past this skill: a trigger query needs enough work
# behind it to be worth consulting a skill for, and when it does not have
# that, the measurement fails silently at 0%.
#
#   ./run_trigger_check.sh [workdir]
set -u

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$HERE/../skills/clarify" && pwd)"
WORK="${1:-/tmp/clarify-trigger-check}"

rm -rf "$WORK"
mkdir -p "$WORK/.claude/skills"
cp -R "$HERE/fixtures/offline-app/." "$WORK/"
cp -R "$SKILL_DIR" "$WORK/.claude/skills/"

run_one() {
  local name="$1" prompt="$2"
  ( cd "$WORK" && claude -p "$prompt" \
      --strict-mcp-config \
      --output-format stream-json --verbose \
      > "$WORK/$name.jsonl" 2>"$WORK/$name.err" )
  python3 - "$WORK/$name.jsonl" "$name" <<'PY'
import json, sys
path, name = sys.argv[1], sys.argv[2]
offered, tools, skills, denied = False, [], [], []
for line in open(path):
    try:
        d = json.loads(line)
    except Exception:
        continue
    if d.get("subtype") == "init":
        offered = "clarify" in (d.get("skills") or [])
    # `message` is a dict on assistant turns and a bare STRING on control events
    # such as `permission_denied`. Assuming the dict crashed this whole check
    # once, on a run whose only real problem was the gateway being briefly down
    # — so the harness reported nothing at all about a case that had run.
    msg = d.get("message")
    if isinstance(msg, str):
        if d.get("subtype") == "permission_denied":
            denied.append(msg[:60])
        continue
    for c in (msg or {}).get("content") or []:
        if isinstance(c, dict) and c.get("type") == "tool_use":
            tools.append(c.get("name"))
            if c.get("name") == "Skill":
                skills.append((c.get("input") or {}).get("skill"))
# A non-firing result only means something if the skill was on offer. And
# `fired` has to name WHICH skill: any Skill call at all would otherwise read as
# this skill firing, which on the near-miss case is the difference between a
# pass and a false positive.
#
# Match the QUALIFIED name. The Skill tool reports `clarify:clarify`, so a bare
# `"clarify" in skills` membership test is False on a run that fired correctly —
# which is the same plugin:skill naming mistake this repo documents elsewhere,
# made inside the check that was supposed to catch it. The bare form is accepted
# too, because a skill copied into .claude/skills/ can register unqualified.
fired = any(str(x) in ("clarify", "clarify:clarify") for x in skills)
print(f"{name:<10} offered={offered}  fired={fired}  skills={skills}  tools={tools[:8]}"
      + (f"  DENIED={len(denied)}: {denied[:1]}" if denied else ""))
PY
}

echo "expect: positive fires, nearmiss does not"
run_one positive "Surveyors keep losing notes when they walk out of coverage. Add offline support to this app. Nothing in the repo says which way to go and we have never discussed it."
run_one nearmiss "Explain what the useCreateNote hook does and when onSuccess fires. I am new to React Query."
echo "transcripts in $WORK"
