#!/usr/bin/env bash
# Check the policy against itself. Runs no model and costs nothing.
set -uo pipefail
cd "$(dirname "$0")"; fail=0
t() { if eval "$2" >/dev/null 2>&1; then printf '  ok    %s\n' "$1"; else printf '  FAIL  %s\n' "$1"; fail=1; fi; }

# Policy checks must not read live meters: scanning the codex session store costs
# seconds per check and makes the result depend on today's usage. FAKE_METERS
# gives every lane identical headroom, so what these assert is the POLICY.
FAKE='
import lane_pick as L
from lane_registry import LANES
def fake(now=None, over={}):
    return {l: {"lane": l, "model": LANES[l]["model"], "family": LANES[l]["family"],
                "price": LANES[l]["blended_usd_per_mtok"], "tier": 1, "used_pct": 5.0,
                "days_left": 5.0, "allowance": 0.19, "measured": True, "note": None,
                "used": "5.0", "unit": "%", "source": "synthetic", "budget_source": "test",
                **over.get(l, {})} for l in LANES}
L.measure = fake
'

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
t "no grok-4.5 in any command"  "python3 -c '
import re
from lane_registry import LANES
# The guard is about what RUNS, not about what is cited. capability_matrix.json
# records grok-4.5 as the version the bench measured, which is provenance for a
# proxy grade and must stay readable; a lane that INVOKES 4.5 is the bug.
bad = [l for l, s in LANES.items()
       if re.search(r\"grok-4\.[0-5]\", \" \".join([s[\"model\"]] + list(s[\"cmd\"])
                                                  + list(s[\"fallback_cmd\"] or [])))]
assert not bad, bad'"
t "no grok-4.5 in the run docs" "! grep -rn 'grok-4\.[0-5]' lane_probe.sh ../references/lanes.md ../references/wire-verify.md"
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

# --- capability layer ------------------------------------------------------

t "matrix loads"                "python3 -c '
from lane_registry import CAPABILITY
assert CAPABILITY and CAPABILITY[\"schema\"] == 1'"
t "every shape is measured"     "python3 -c '
from lane_registry import CAPABILITY, SHAPES
missing = [s for s in SHAPES if s not in CAPABILITY[\"shapes\"]]
assert not missing, missing'"
t "every bench_key resolves"    "python3 -c '
from lane_registry import CAPABILITY, LANES
bad = [l for l, s in LANES.items()
       if s.get(\"bench_key\") and s[\"bench_key\"] not in CAPABILITY[\"lanes\"]]
assert not bad, bad'"
t "evidence is a known value"   "python3 -c '
from lane_registry import LANES
bad = [l for l, s in LANES.items() if s.get(\"evidence\") not in (\"exact\", \"proxy\", \"none\")]
assert not bad, bad'"
t "proxy never reaches drop-in" "python3 -c '
from lane_registry import LANES, SHAPES, DROP_IN, shape_grade
bad = [(l, s) for l in LANES if LANES[l].get(\"evidence\") == \"proxy\" for s in SHAPES
       if (shape_grade(l, s) or {}).get(\"gate\") in DROP_IN]
assert not bad, bad'"
t "opus is fail-back not band"  "python3 -c '
from lane_registry import SHAPES, gate_lanes, REFERENCE_LANE
for s in SHAPES:
    g = gate_lanes(\"implementation\", s)
    assert REFERENCE_LANE not in g[\"dropin\"] + g[\"guarded\"] + g[\"refused\"], s
    assert g[\"failback\"] == [REFERENCE_LANE], s'"
t "some shape displaces opus"   "python3 -c '
from lane_registry import SHAPES, gate_lanes
hit = [s for s in SHAPES if gate_lanes(\"implementation\", s)[\"dropin\"]]
assert len(hit) >= 4, hit'"
t "judgement classes abstain"   "python3 -c '
from lane_registry import TASKS, gate_lanes
for k in (\"verification\", \"referral\", \"completeness\", \"design-review\"):
    assert not TASKS[k][\"shape_gated\"], k
    g = gate_lanes(k, \"react-ui\")
    assert g[\"dropin\"] == TASKS[k][\"allow\"] and not g[\"refused\"], k'"
t "no shape routes past a RED"  "python3 -c \"\$FAKE
from lane_registry import SHAPES
for s in SHAPES:
    lane, _, _, v = L.choose('implementation', shape=s)
    assert lane not in v['refused'], (s, lane)\""
t "tie-break uses \$/task"       "python3 -c '
import lane_pick as L
assert L.task_cost(\"codex-terra-medium\") < L.task_cost(\"codex-terra-max\")
assert L.task_cost(\"codex-sol-high\") < L.task_cost(\"opus\")'"
t "score leads inside a band"   "python3 -c \"\$FAKE
from lane_registry import SHAPES
# 0.05 is written out rather than imported: a check that reads the constant it
# guards cannot fail when that constant moves, which is how this one first
# passed against a margin widened to 100%. The policy is the assertion.
for s in SHAPES:
    lane, _, _, v = L.choose('implementation', shape=s)
    sc = {l: L.delivery_adjusted(l, (v['grades'][l] or {}).get('mean'))
          for l in v['considered'] + v['outranked']}
    sc = {k: x for k, x in sc.items() if x is not None}
    if not sc or lane not in sc: continue
    assert sc[lane] >= max(sc.values()) - 0.05 - 1e-9, (s, lane, sc)\""
t "margin is the GREEN margin"  "python3 -c '
from lane_registry import EQUIVALENCE_POINTS as EQ
assert abs(EQ - 0.05) < 1e-9, EQ'"
t "usage leads inside margin"   "python3 -c '
import lane_pick as L
from lane_registry import equivalent_set, EQUIVALENCE_POINTS as EQ
g = {\"a\": {\"mean\": 0.80}, \"b\": {\"mean\": 0.77}, \"c\": {\"mean\": 0.50}}
eq = equivalent_set([\"a\", \"b\", \"c\"], g)
assert eq == [\"a\", \"b\"], eq          # c is outranked, a and b are swappable
assert equivalent_set([\"c\"], g) == [\"c\"]
assert equivalent_set([\"a\"], {}) == [\"a\"]   # unmeasured routes rather than stalls'"
t "spent top scorer steps aside" "python3 -c \"\$FAKE
best, _, _, _ = L.choose('implementation', shape='regression-sensitive')
L.measure = lambda now=None: fake(over={best: {'used_pct': 100.0, 'allowance': 0.0}})
nxt, _, _, _ = L.choose('implementation', shape='regression-sensitive')
assert nxt != best, (best, nxt)\""
t "codex lanes share a meter"   "python3 -c '
import lane_pick as L
from lane_registry import LANES
# One rate-limit read feeds every codex lane, so the wiring is what is asserted;
# reading the live meter here would cost seconds and prove the same thing.
assert L.CODEX_LANES == {l for l, s in LANES.items() if s[\"meter\"] == \"codex\"}
assert L.CODEX_LANES <= L.TIER1 and L.CLAUDE_LANES <= L.TIER1'"
t "sol never max, both lanes"   "python3 -c '
from lane_registry import LANES
sol = [l for l, s in LANES.items() if s[\"model\"] == \"gpt-5.6-sol\"]
assert sol and all(LANES[l][\"effort\"] != \"max\" for l in sol), sol
assert all(\"max\" not in \" \".join(LANES[l][\"cmd\"]) for l in sol), sol'"
t "luna cites the bench that freed it" "python3 -c '
from lane_registry import LANES, DECLINED, EXTERNAL_BENCH, TASKS
luna = [l for l, s in LANES.items() if \"luna\" in s[\"model\"]]
assert luna, \"the lane was removed\"
for l in luna:
    key = LANES[l].get(\"external_bench\")
    assert key in EXTERNAL_BENCH, (l, key)
    assert LANES[l].get(\"usd_per_task_external\"), l
    assert LANES[l][\"bench_key\"] is None, \"a local grade it never earned\"
assert \"gpt-5.6-luna\" in DECLINED and \"SUPERSEDED\" in DECLINED[\"gpt-5.6-luna\"]
row = EXTERNAL_BENCH[\"deepswe-1.1\"][\"rows\"]
assert row[\"gpt-5.6-luna@max\"][\"usd_per_task\"] < row[\"grok-4.6@xhigh\"][\"usd_per_task\"]
assert any(l in TASKS[\"implementation\"][\"allow\"] for l in luna)'"
t "a penalty is still applied"  "python3 -c '
from lane_registry import DELIVERY_PENALTY, delivery_adjusted
assert DELIVERY_PENALTY, \"the delivery table was emptied\"
for lane, e in DELIVERY_PENALTY.items():
    assert e[\"points\"] > 0 and e[\"measured\"] and e[\"lift_it_when\"], lane
    assert delivery_adjusted(lane, 50) < 50, lane'"
t "capability doc quotes data"  "python3 -c '
from lane_registry import CAPABILITY, SHAPES
doc = open(\"../references/capability.md\").read()
missing = [s for s in SHAPES if s not in doc]
assert not missing, missing
n = CAPABILITY[\"source\"][\"visible_tasks\"]
assert str(n) in doc, n'"
t "--matrix runs"               "python3 lane_pick.py --matrix"
t "--shape routes every shape"  "python3 -c \"\$FAKE
from lane_registry import SHAPES
for s in SHAPES:
    lane, _, _, v = L.choose('implementation', shape=s)
    assert lane in LANES and v['shape'] == s, s\""

[ $fail -eq 0 ] && echo "  — all checks passed" || echo "  — FAILURES above"
exit $fail
