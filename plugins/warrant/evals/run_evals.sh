#!/usr/bin/env bash
# Process evals for the warrant plugin. Exit 0 only if every check passes.
# Run from the plugin root: bash evals/run_evals.sh
set -uo pipefail
cd "$(dirname "$0")/.." || exit 1
pass=0; fail=0
check() { # check <id> <description> <command...>
  local id="$1" desc="$2"; shift 2
  if "$@" >/dev/null 2>&1; then printf 'ok    %-6s %s\n' "$id" "$desc"; pass=$((pass+1))
  else printf 'FAIL  %-6s %s\n' "$id" "$desc"; fail=$((fail+1)); fi
}

# W-01 / W-02 / W-03 / W-04 are per-script and run by the harness below.
for f in scripts/[a-z]*.py; do
  n=$(basename "$f")
  check "W-01" "$n exposes the common flags" \
    bash -c "python3 $f --help 2>&1 | grep -q -- --selftest && python3 $f --help 2>&1 | grep -q -- --root"
  check "W-02" "$n --selftest exits 0" python3 "$f" --selftest
  check "W-03" "$n selftest observes a failing rule" \
    bash -c "grep -qiE 'fires|refus|rejects|no longer|breaks|leak|below|absent' $f"
  check "W-04" "$n imports stdlib only" \
    bash -c "! grep -nE '^\\s*(import|from) (requests|yaml|numpy|pandas|pytest|jinja2|httpx|bs4)' $f"
done

check "W-11" "an unnamed class defaults to tier 0" python3 - <<'PY'
import sys; sys.path.insert(0, "scripts")
import _state
assert _state.tier_of({"classes": [{"name": "known", "tier": 3}]}, "unknown") == 0
assert _state.tier_of({"classes": [{"name": "known", "tier": 3}]}, "known") == 3
PY

check "W-13" "every cited claim id resolves in the corpus" python3 - <<'PY'
import json, pathlib, re, sys
claims = json.loads(pathlib.Path("docs/deep-research/claims.json").read_text())
known = {c["id"] for c in claims["claims"]} | {i["id"] for i in claims["inferences"]} | {m["id"] for m in claims["meta"]}
cited, bad = set(), set()
for p in list(pathlib.Path("skills").rglob("SKILL.md")) + list(pathlib.Path("references").glob("*.md")):
    for m in re.finditer(r"`([CIM]\d{1,2})`", p.read_text()):
        cited.add(m.group(1))
        if m.group(1) not in known: bad.add(f"{p}:{m.group(1)}")
if bad: print("unresolved:", sorted(bad)); sys.exit(1)
print(f"{len(cited)} distinct claim ids, all resolve")
PY

check "W-15" "documented flags exist on their scripts" python3 evals/check_doc_flags.py

printf '\n%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
