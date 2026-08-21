#!/usr/bin/env bash
# Check the policy against itself. Runs no model and costs nothing.
set -uo pipefail
cd "$(dirname "$0")"; fail=0
t() { if eval "$2" >/dev/null 2>&1; then printf '  ok    %s\n' "$1"; else printf '  FAIL  %s\n' "$1"; fail=1; fi; }

t "registry imports"            "python3 -c 'import lane_registry'"
t "lane_pick --report runs"     "python3 lane_pick.py --report"
t "every task resolves a lane"  "python3 -c '
import lane_pick as L
from lane_registry import TASKS
for k in TASKS: assert L.choose(k)[0] in L.LANES, k'"
t "sol is never max"            "python3 -c '
from lane_registry import LANES
assert LANES[\"codex-sol\"][\"effort\"] == \"medium\"'"
t "grok is xhigh"               "python3 -c '
from lane_registry import LANES
assert LANES[\"grok\"][\"effort\"] == \"xhigh\" and \"xhigh\" in LANES[\"grok\"][\"cmd\"]'"
t "opus verifies at xhigh"      "python3 -c '
from lane_registry import LANES, TASKS
assert TASKS[\"verification\"][\"allow\"] == [\"opus\"]
assert LANES[\"opus\"][\"effort\"] == \"xhigh\"'"
t "fable never verifies"        "python3 -c '
from lane_registry import TASKS
assert \"fable\" not in TASKS[\"verification\"][\"allow\"]'"
t "design review is claude only" "python3 -c '
from lane_registry import LANES, TASKS
assert all(LANES[l][\"family\"] == \"anthropic\" for l in TASKS[\"design-review\"][\"allow\"])'"
t "completeness is out of family" "python3 -c '
from lane_registry import LANES, TASKS
assert all(LANES[l][\"family\"] != \"anthropic\" for l in TASKS[\"completeness\"][\"allow\"])'"
t "no grok-4.5 anywhere"        "! grep -rn 'grok-4\.[0-5]' lane_registry.py lane_pick.py lane_probe.sh ../references"
t "glm carries the binding hdr" "python3 -c '
from lane_registry import LANES
assert LANES[\"glm\"][\"env\"][\"ANTHROPIC_CUSTOM_HEADERS\"] == \"X-Perch-Binding: glm\"'"
t "cheapest wins a tie"         "python3 -c '
from lane_registry import LANES
c = [(LANES[l][\"blended_usd_per_mtok\"], l) for l in (\"gemini\",\"glm\",\"grok\")]
assert [l for _, l in sorted(c)] == [\"gemini\",\"glm\",\"grok\"]'"
t "docs and registry agree"     "python3 -c '
import re
from lane_registry import LANES
doc = open(\"../references/lanes.md\").read()
missing = [s[\"model\"] for s in LANES.values() if s[\"model\"] not in doc]
assert not missing, missing'"

[ $fail -eq 0 ] && echo "  — all checks passed" || echo "  — FAILURES above"
exit $fail
