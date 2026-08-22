#!/usr/bin/env python3
"""Prove every gate in reckon.py can fail.

A gate that has never been seen to fail is indistinguishable from a gate that
cannot fail. Each case here builds a ledger that is wrong in exactly one way
and asserts the intended violation fires with the intended exit code — and the
clean control asserts the same gates stay quiet on a sound ledger, so a gate
that fires on everything is caught too.

Run: python3 selftest.py     (exit 0 = every gate demonstrated)
"""

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("reckon", os.path.join(HERE, "reckon.py"))
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)

FAILURES = []


def ledger(rows, **over):
    base = {
        "tool": "reckon", "version": 1, "project": "fixture",
        "headline": "fixture",
        "summary": {"counts": None},
        "denominators": {
            "cases_adjudicated": {"n": 1, "of": 2, "pct": 50.0, "means": "x"},
            "decisions_taken": {"n": 0, "of": 2, "pct": 0.0, "means": "x"},
            "requirements_observed": {"n": 1, "of": 2, "pct": 50.0, "means": "x"},
            "surfaces_spoken_for": {"n": 1, "of": 2, "pct": 50.0, "means": "x"},
            "briefs_joined": {"n": 2, "of": 2, "pct": 100.0, "means": "x"},
            "is_floor": True, "floor_note": "x",
        },
        "join": {"edges": [], "briefs_joined": 2, "briefs_total": 2, "pct": 100.0, "weak": False},
        "blockers": [], "rows": rows,
    }
    base.update(over)
    if base["summary"].get("counts") is None:
        from collections import Counter
        base["summary"]["counts"] = dict(Counter(r["class"] for r in rows))
    return base


def case(cid, status, cls, note="reason recorded"):
    return {"id": cid, "entity": "case", "class": cls, "kind": R.KIND_OF[cls],
            "status": status, "title": "c", "why": "", "note": note, "is_work_item": False}


def req(rid, evidence, cls):
    return {"id": rid, "entity": "requirement", "class": cls, "kind": R.KIND_OF[cls],
            "evidence": evidence, "title": "r", "why": "", "is_work_item": cls != "verified-done"}


def brief(bid, cls, edges):
    return {"id": bid, "entity": "brief", "class": cls, "kind": R.KIND_OF[cls],
            "edges": edges, "title": "b", "why": "", "is_work_item": True}


def expect(name, rows_or_ledger, want_code, want_substring, want_kind=None):
    led = rows_or_ledger if isinstance(rows_or_ledger, dict) else ledger(rows_or_ledger)
    violations, warnings = R.gate(led)
    code = R.verdict(violations)
    blob = " ".join(m for _, m in violations) + " " + " ".join(warnings)
    ok = code == want_code and want_substring.lower() in blob.lower()
    if want_kind:
        ok = ok and any(k == want_kind for k, _ in violations)
    print("%-46s exit=%d %s" % (name, code, "ok" if ok else "FAILED"))
    if not ok:
        FAILURES.append("%s: exit %d (wanted %d); saw: %s" % (name, code, want_code, blob[:300]))
    return led


# --- the control: a sound ledger must stay silent --------------------------
clean = [
    case("CASE-1", "pass", "verified-done"),
    case("CASE-2", "blocked", "unmeasured"),
    case("CASE-3", "n/a", "waived"),
    req("REQ-1", "observed", "verified-done"),
    req("REQ-2", "reported", "unmeasured"),
    brief("BRIEF-a", "unbuilt", []),
    brief("BRIEF-b", "retirable", [{"target": "REQ-1", "method": "cited", "confidence": 1.0}]),
]
expect("clean ledger passes", clean, 0, "")

# --- 1. conservation -------------------------------------------------------
expect("duplicate id caught", clean + [case("CASE-1", "fail", "broken")],
       1, "more than one ledger row", "conservation")

expect("row with no id caught", clean + [case("", "fail", "broken")],
       1, "carry no id", "conservation")

# --- 2. placement: the central failure ------------------------------------
expect("blocked case presenting as done",
       [case("CASE-9", "blocked", "verified-done")] + clean[1:],
       1, "silent-done", "placement")

expect("inconclusive case presenting as broken",
       [case("CASE-9", "inconclusive", "broken")] + clean[1:],
       1, "may only be unmeasured", "placement")

expect("carried case presenting as done",
       [case("CASE-9", "unselected", "verified-done")] + clean[1:],
       1, "may only be unmeasured", "placement")

expect("self-reported requirement retiring itself",
       clean[:3] + [req("REQ-9", "reported", "verified-done")] + clean[4:],
       1, "cannot retire", "placement")

expect("unknown-evidence requirement retiring itself",
       clean[:3] + [req("REQ-9", "unknown", "retirable")] + clean[4:],
       1, "cannot retire", "placement")

expect("class outside the partition",
       clean + [{"id": "X-1", "entity": "brief", "class": "probably-fine", "kind": "product-work",
                 "title": "x", "why": "", "is_work_item": True}],
       1, "not one of the partition", "placement")

expect("retirement on a token-overlap guess",
       clean[:5] + [brief("BRIEF-b", "retirable",
                          [{"target": "REQ-1", "method": "overlap", "confidence": 0.31}])],
       1, "retiring intent on a guess", "placement")

expect("n/a presenting as verified-done",
       [case("CASE-9", "n/a", "verified-done")] + clean[1:],
       1, "may only be waived", "placement")

expect("waiver with no recorded reason",
       clean + [{"id": "CASE-W", "entity": "case", "class": "waived", "kind": "exception",
                 "status": "", "title": "w", "why": "", "note": "", "is_work_item": False}],
       1, "omission wearing a decision", "placement")

# --- 3. disclosure ---------------------------------------------------------
missing_denom = ledger(clean)
del missing_denom["denominators"]["requirements_observed"]
expect("absent denominator caught", missing_denom, 2, "reads as though it covered everything", "disclosure")

lying_summary = ledger(clean)
lying_summary["summary"]["counts"] = {"verified-done": 99}
expect("summary disagreeing with rows", lying_summary, 2, "disagrees with its rows", "disclosure")

# --- 4. weak join is a warning that degrades a claim, not a blocker --------
weak = ledger([r for r in clean if r["id"] != "BRIEF-b"])
weak["denominators"]["briefs_joined"] = {"n": 1, "of": 10, "pct": 10.0, "means": "x"}
v, w = R.gate(weak)
ok = R.verdict(v) == 0 and any("join" in x for x in w)
print("%-46s exit=%d %s" % ("weak join warns without blocking", R.verdict(v), "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("weak join should warn at exit 0, saw exit %d / %r" % (R.verdict(v), w))

# --- 5. ratchet ------------------------------------------------------------
prev = ledger([case("CASE-1", "blocked", "unmeasured"), req("REQ-1", "reported", "unmeasured")])

silent = ledger([case("CASE-1", "blocked", "verified-done"), req("REQ-1", "reported", "unmeasured")])
bad = R.ratchet(prev, silent)
ok = len(bad) == 1 and "no evidence-bearing event" in bad[0]
print("%-46s %s" % ("ratchet catches a silent reclassification", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("ratchet silent reclassification: %r" % bad)

vanished = ledger([req("REQ-1", "reported", "unmeasured")])
bad = R.ratchet(prev, vanished)
ok = len(bad) == 1 and "stopped being counted" in bad[0]
print("%-46s %s" % ("ratchet catches an item that vanished", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("ratchet vanished item: %r" % bad)

earned = ledger([case("CASE-1", "pass", "verified-done"), req("REQ-1", "observed", "verified-done")])
bad = R.ratchet(prev, earned)
ok = not bad
print("%-46s %s" % ("ratchet allows an earned transition", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("ratchet blocked an earned transition: %r" % bad)

# --- 6. classification behaviour ------------------------------------------
camp = {"present": True, "header": {}, "cases": [], "flows": [], "components": [],
        "requirements": [{"id": "REQ-1", "text": "the widget saves", "evidence": "reported"}],
        "surfaces": [{"id": "SURF-1", "title": "orphan surface", "slug": "orphan"}],
        "defects": []}
rows = R.classify([], camp, [], False)
by = {r["id"]: r for r in rows}
ok = by["SURF-1"]["class"] == "unnamed" and by["REQ-1"]["class"] == "unmeasured"
print("%-46s %s" % ("orphan surface -> unnamed; reported -> unmeasured", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("classification: %r" % {k: v["class"] for k, v in by.items()})

camp2 = dict(camp, requirements=[{"id": "REQ-1", "text": "x", "evidence": "contradicted"}])
rows2 = R.classify([], camp2, [], False)
ok = [r for r in rows2 if r["id"] == "REQ-1"][0]["class"] == "undecided"
print("%-46s %s" % ("contradicted evidence -> undecided", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("contradicted should be undecided")

# --- 7. every class in the partition is reachable --------------------------
reachable = set()
for status in R.LEGAL_CLASS:
    reachable |= R.LEGAL_CLASS[status]
reachable |= {"unbuilt", "unnamed", "undecided"}
unreachable = set(R.CLASSES) - reachable
ok = not unreachable
print("%-46s %s" % ("every class is reachable", "ok" if ok else "FAILED %s" % unreachable))
if not ok:
    FAILURES.append("unreachable classes: %s" % unreachable)

# --- 8. a registry field is free-form JSON, not reliably a string ----------
#
# Measured on one real campaign: of 52 defect rows `evidence` was None on 31, a
# string on 16 and a LIST on 5, and the undefended read crashed `build` outright
# with AttributeError. The pre-fix expression is restated verbatim below and
# asserted to FAIL on that input first — without it this row is green in any
# registry whose fields happen to all be strings, which is exactly where the
# defect is invisible.
PRE_FIX = lambda text: (text or "").lower()          # noqa: E731 — the read as it was

listed = ["evidence/shots/board.png", "evidence/runs/gate.log"]
try:
    PRE_FIX(listed)
    pre_fix_crashes = False
except AttributeError:
    pre_fix_crashes = True

# The call is guarded because the defect's own failure mode is an exception:
# an unguarded call turns this row into a traceback that takes the suite down
# and abandons every row below it, which is a worse instrument than a red line.
try:
    got, raised = R.tokens(listed), None
except Exception as exc:                                    # noqa: BLE001 — the defect IS the raise
    got, raised = set(), "%s: %s" % (type(exc).__name__, exc)

ok = pre_fix_crashes and raised is None and {"evidence", "shots", "board", "png"} <= got
print("%-46s %s" % ("a list-valued registry field yields tokens",
                    "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append(
        "list-valued field: pre-fix crashes=%s, raised=%s, tokens=%s"
        % (pre_fix_crashes, raised, sorted(got)))

# The other shapes the same fields carry, and the one that must stay empty.
try:
    shapes_ok = (
        R.tokens(None) == set()
        and R.tokens("plain string here") >= {"plain", "string", "here"}
        and "nested" in R.tokens({"a": ["nested value"], "b": 12345})
        and "12345" in R.tokens({"a": ["nested value"], "b": 12345})
    )
except Exception:                                           # noqa: BLE001
    shapes_ok = False
print("%-46s %s" % ("None, str, dict and scalar all flatten",
                    "ok" if shapes_ok else "FAILED"))
if not shapes_ok:
    FAILURES.append("flatten_text does not cover every registry shape")

print()
if FAILURES:
    print("%d self-test failure(s):" % len(FAILURES))
    for f in FAILURES:
        print("  -", f)
    sys.exit(1)
print("all gates demonstrated failing on a bad fixture, and silent on a good one")
sys.exit(0)
