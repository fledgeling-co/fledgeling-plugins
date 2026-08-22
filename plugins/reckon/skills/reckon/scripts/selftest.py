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

# --- 7. reachability is checked by production, in section 13 ---------------
#
# This slot used to union a hand-written literal against CLASSES, which meant a
# class nothing could produce still read as reachable — the check could not
# distinguish a live predicate from a dead one, which is the whole thing it
# existed to do. Section 13 collects what `classify()` actually emits instead.

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

# --- 9. a defect's own recorded status decides its class -------------------
#
# The registry carries `status` on every defect row. The pre-fix classifier
# never read it: every defect row was hardcoded `broken`, so a campaign that
# had repaired 100 of its 110 defects reported all 110 as remaining product
# work. The pre-fix expression is restated verbatim and asserted to produce
# the wrong answer first — without that, this row is green on any registry
# whose defects all happen to be open, which is exactly where it cannot see
# the defect.
PRE_FIX_DEFECT = lambda d: "broken"                  # noqa: E731 — the classing as it was


def defect_class(status, **extra):
    row = {"id": "DEF-1", "title": "a repaired thing"}
    if status is not None:
        row["status"] = status
    row.update(extra)
    camp = {"present": True, "header": {}, "cases": [], "flows": [], "components": [],
            "requirements": [], "surfaces": [], "defects": [row]}
    got = [r for r in R.classify([], camp, [], False) if r["entity"] == "defect"][0]
    return got


pre = PRE_FIX_DEFECT({"status": "fixed"})
row = defect_class("fixed")
ok = pre == "broken" and row["class"] == "verified-done" and row["is_work_item"] is False
print("%-46s %s" % ("a fixed defect is not remaining work", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("fixed defect: pre-fix=%r now=%r work=%r" % (pre, row["class"], row["is_work_item"]))

row = defect_class("open")
ok = row["class"] == "broken" and row["is_work_item"] is True
print("%-46s %s" % ("an open defect is still remaining work", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("open defect: %r" % row["class"])

# The fail-closed direction, chosen rather than inherited. A status this tool
# does not recognise is the one place where guessing done would be the
# unrecoverable error, so it stays `broken` and says which word it did not know.
row = defect_class("marinated")
ok = row["class"] == "broken" and "marinated" in (row.get("why") or "")
print("%-46s %s" % ("an unrecognised defect status stays broken", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("unrecognised defect status: %r / %r" % (row["class"], row.get("why")))

row = defect_class(None)
# The class alone would agree with the pre-fix code, which said `broken` about
# everything; the reason is what shows the status was read and found missing.
ok = row["class"] == "broken" and "no status" in (row.get("why") or "")
print("%-46s %s" % ("a defect with no status stays broken", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("statusless defect: %r / %r" % (row["class"], row.get("why")))

row = defect_class("wontfix")
# `bool(row.get("status"))` would have been true whatever the code did, since
# the fixture sets it. The reason has to name the decision, and the ledger gate
# has to accept the row on that reason alone.
row["title"] = "w"
v, _ = R.gate(ledger(clean + [row]))
ok = (row["class"] == "waived" and row["status"] == "wontfix"
      and "wontfix" in (row.get("why") or "") and not v)
print("%-46s %s" % ("a wontfix defect is a waiver with its reason", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("wontfix defect: %r why=%r gate=%r" % (row["class"], row.get("why"), v))

# The gate must hold this as legality, not preference: a defect row whose class
# contradicts its own status is a placement violation, the same protection
# cases have had since the first version.
expect("defect claiming done on an unknown status",
       clean + [{"id": "DEF-8", "entity": "defect", "class": "verified-done", "kind": "none",
                 "status": "marinated", "title": "d", "why": "", "is_work_item": False}],
       1, "may only be broken", "placement")

expect("defect classed against its own status",
       clean + [{"id": "DEF-9", "entity": "defect", "class": "verified-done", "kind": "none",
                 "status": "open", "title": "d", "why": "", "is_work_item": False}],
       1, "may only be broken", "placement")

# --- 10. an unjoined brief is not an unbuilt one ---------------------------
#
# 75 of 91 briefs landed in `unbuilt` on a 17.6% join, and every one of them
# named an item that had shipped. `unbuilt` claims the registry answered and
# said no; the join answering nothing is a different fact with the opposite
# conclusion, and folding the second into the first is this tool's own target
# failure arriving from the other direction.
PRE_FIX_BRIEF = lambda edges: "unbuilt"              # noqa: E731 — the classing as it was

CAMP_MIN = {"present": True, "header": {}, "cases": [], "flows": [], "components": [],
            "requirements": [{"id": "REQ-1", "text": "the widget saves rows", "evidence": "observed"}],
            "surfaces": [], "defects": []}


def brief_row(text, edges, camp=None, status=""):
    b = {"id": "BRIEF-x", "file": "x.md", "path": "x.md", "title": "a brief",
         "text": text, "status": status, "generated_by": None, "source_ids": []}
    rows = R.classify([b], camp or CAMP_MIN, edges, False)
    return [r for r in rows if r["entity"] == "brief"][0]


row = brief_row("nothing in here matches anything", [])
ok = (PRE_FIX_BRIEF([]) == "unbuilt" and row["class"] == "unjoined"
      and row["kind"] == "decision-work" and row["is_work_item"] is True)
print("%-46s %s" % ("a brief nothing joined is unjoined, not unbuilt", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("unjoined brief: class=%r kind=%r" % (row["class"], row.get("kind")))

# `unbuilt` has to stay a live predicate or the partition carries a class
# nothing can produce. It survives on the one piece of positive evidence of
# absence available here: the brief names ids on purpose, and the registry
# does not hold them.
row = brief_row("this implements REQ-404 and DEF-404",
                [{"brief": "BRIEF-x", "target": "REQ-404", "method": "cited", "confidence": 1.0},
                 {"brief": "BRIEF-x", "target": "DEF-404", "method": "cited", "confidence": 1.0}])
ok = row["class"] == "unbuilt" and row["kind"] == "product-work"
print("%-46s %s" % ("a brief citing ids the registry lacks is unbuilt", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("dangling-citation brief: %r / %r" % (row["class"], row.get("why")))

# An unjoined row that says only "I could not tell" sends its reader to grep.
# The join already computed the near miss and threw it away below threshold.
row = brief_row("the widget saves rows sometimes", [])
near = row.get("near_misses") or []
ok = row["class"] == "unjoined" and near and near[0]["target"] == "REQ-1" and near[0]["score"] > 0
print("%-46s %s" % ("an unjoined row carries its nearest candidate", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("near_misses: %r" % near)

# Once a repaired defect stops being `broken`, a brief joined only to that
# defect must stop being `broken` too — otherwise the fault simply moves one
# hop out and reports the same repaired work as remaining.
camp_fixed = dict(CAMP_MIN, defects=[{"id": "DEF-7", "title": "a repaired thing", "status": "fixed"}])
row = brief_row("this is about DEF-7",
                [{"brief": "BRIEF-x", "target": "DEF-7", "method": "cited", "confidence": 1.0}],
                camp=camp_fixed)
# Naming the exact class matters: `!= "broken"` would also accept `unjoined`
# or `unbuilt`, which would mean the defect branch had stopped running at all.
ok = row["class"] == "unmeasured"
print("%-46s %s" % ("a brief joined only to a fixed defect is not broken", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("brief on a fixed defect: %r" % row["class"])

camp_open = dict(CAMP_MIN, defects=[{"id": "DEF-7", "title": "a live thing", "status": "open"}])
row = brief_row("this is about DEF-7",
                [{"brief": "BRIEF-x", "target": "DEF-7", "method": "cited", "confidence": 1.0}],
                camp=camp_open)
ok = row["class"] == "broken"
print("%-46s %s" % ("a brief joined to an open defect is still broken", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("brief on an open defect: %r" % row["class"])

expect("unjoined is inside the partition",
       clean + [{"id": "BRIEF-u", "entity": "brief", "class": "unjoined", "kind": "decision-work",
                 "title": "u", "why": "", "edges": [], "is_work_item": True}],
       0, "")

# A dangling citation is evidence of absence only when there is a registry that
# could have held the target. With no campaign at all, `unbuilt` would be a
# claim that the registry was asked, and it was not — `references/no-campaign.md`
# says every brief lands in `unjoined` or `waived`, and this holds the code to it.
CAMP_NONE = {"present": False, "header": {}, "cases": [], "requirements": [], "surfaces": [],
             "defects": [], "flows": [], "components": []}
row = brief_row("this implements REQ-404",
                [{"brief": "BRIEF-x", "target": "REQ-404", "method": "cited", "confidence": 1.0}],
                camp=CAMP_NONE)
ok = row["class"] == "unjoined" and "no registry" in (row.get("why") or "")
print("%-46s %s" % ("with no campaign, a citation is not evidence", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("no-campaign dangling citation: %r / %r" % (row["class"], row.get("why")))

# 5b — a dangling citation must not discard a usable overlap edge
row = brief_row("the widget saves rows",
                [{"brief": "BRIEF-x", "target": "REQ-404", "method": "cited", "confidence": 1.0},
                 {"brief": "BRIEF-x", "target": "REQ-1", "method": "overlap", "confidence": 0.4}])
ok = row["class"] not in ("unbuilt", "unjoined")
print("%-46s %s" % ("a dangling citation keeps a usable overlap edge", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("dangling citation discarded an overlap edge: %r" % row["class"])

# --- 11. the reverse-citation scan may not accept a file number ------------
#
# The scan exists so a registry note naming a brief by its project id
# (`SCR-0075`) produces a confidence-1.0 edge. On a queue named `NN-slug` the
# same code builds tokens like `03-menu` out of a position in a directory
# listing, and a positional guess wearing a citation's confidence can carry a
# retirement. Measured on the campaign this was written against: the scan
# contributed 0 of 92 cited edges, so requiring a project-id shape costs
# nothing there and closes the guess.
camp_note = {"present": True, "header": {}, "cases": [], "flows": [], "components": [],
             "requirements": [{"id": "REQ-1", "text": "unrelated", "note": "see 03-menu for context"}],
             "surfaces": [], "defects": []}
numbered = [{"id": "BRIEF-03-menu-bar", "file": "03-menu-bar-key-equivalents.md",
             "path": "x", "title": "menu bar", "text": "no ids here", "status": "",
             "generated_by": None, "source_ids": []}]
edges = R.build_join(numbered, camp_note)
ok = not any(e["method"] == "cited" for e in edges)
print("%-46s %s" % ("a file number is not a citation", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("number-shaped reverse citation still fires: %r" % edges)

camp_id = {"present": True, "header": {}, "cases": [], "flows": [], "components": [],
           "requirements": [{"id": "REQ-1", "text": "unrelated", "note": "DEF-0015 / SCR-0075"}],
           "surfaces": [], "defects": []}
ided = [{"id": "BRIEF-SCR-0075", "file": "SCR-0075-dead-credential.md", "path": "x",
         "title": "dead credential", "text": "no ids here", "status": "",
         "generated_by": None, "source_ids": []}]
edges = R.build_join(ided, camp_id)
ok = any(e["method"] == "cited" and e["target"] == "REQ-1" for e in edges)
print("%-46s %s" % ("a project id in a note is still a citation", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("documented reverse citation stopped working: %r" % edges)

# --- 12. the report and the headline show what cannot be classed -----------
led = ledger(clean + [{"id": "BRIEF-u", "entity": "brief", "class": "unjoined",
                       "kind": "decision-work", "title": "an unjoinable brief", "why": "no edge",
                       "edges": [], "near_misses": [{"target": "REQ-1", "score": 0.09}],
                       "is_work_item": True}])
led["blockers"] = []
text = R.render(led)
ok = "`unjoined`" in text and "Unjoined" in text and "BRIEF-u" in text
print("%-46s %s" % ("the report gives unjoined its own section", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("render omits unjoined")

# --- 13. every class is reachable, by production rather than by assertion --
#
# The previous version of this check unioned a hand-written literal, so a class
# nothing could produce would still be reported reachable — a dead predicate
# reading as a live one. Collect what `classify` actually emits instead.
produced = set()
for camp_fixture, brief_fixture, edge_fixture in (
    ({"present": True, "header": {}, "cases": [], "flows": [], "components": [],
      "requirements": [{"id": "REQ-1", "text": "x", "evidence": "contradicted"}],
      "surfaces": [{"id": "SURF-1", "title": "orphan", "slug": "o"}],
      "defects": [{"id": "DEF-1", "title": "d", "status": "open"},
                  {"id": "DEF-2", "title": "d2", "status": "fixed"},
                  {"id": "DEF-3", "title": "d3", "status": "wontfix"}]},
     [{"id": "BRIEF-1", "file": "f.md", "path": "p", "title": "t", "text": "no ids", "status": "",
       "generated_by": None, "source_ids": []}], []),
    ({"present": True, "header": {},
      "cases": [{"id": "CASE-1", "surface": "SURF-1", "state": "s", "status": "pass",
                 "oracle": "effect-witness"},
                {"id": "CASE-2", "surface": "SURF-1", "state": "s", "status": "blocked",
                 "oracle": "outcome"}],
      "flows": [], "components": [],
      "requirements": [{"id": "REQ-1", "text": "x", "evidence": "observed"}],
      "surfaces": [{"id": "SURF-1", "title": "claimed", "slug": "c"}], "defects": []},
     [{"id": "BRIEF-2", "file": "g.md", "path": "p", "title": "t", "text": "REQ-1 and SURF-1",
       "status": "", "generated_by": None, "source_ids": []},
      {"id": "BRIEF-3", "file": "h.md", "path": "p", "title": "t", "text": "REQ-404", "status": "",
       "generated_by": None, "source_ids": []}],
     [{"brief": "BRIEF-2", "target": "REQ-1", "method": "cited", "confidence": 1.0},
      {"brief": "BRIEF-2", "target": "SURF-1", "method": "cited", "confidence": 1.0},
      {"brief": "BRIEF-3", "target": "REQ-404", "method": "cited", "confidence": 1.0}]),
):
    produced |= {r["class"] for r in R.classify(brief_fixture, camp_fixture, edge_fixture, False)}

unreachable = set(R.CLASSES) - produced
ok = not unreachable
print("%-46s %s" % ("every class is produced by a real fixture",
                    "ok" if ok else "FAILED %s" % sorted(unreachable)))
if not ok:
    FAILURES.append("classes no fixture produces: %s" % sorted(unreachable))

# --- 14. the repair has to be able to reach an installed copy --------------
#
# The delivery half of this item, and the reason it was worth its own row: the
# `flatten_text` repair in section 8 was correct, committed, and stranded. Both
# version strings read 1.0.0, so no installed copy ever saw it, and the crash
# kept happening to everybody who was not sitting in this checkout. A repair
# only in the source is the same invisibility the tool objects to.
#
# Two things are checkable and both have failed here before: the plugin's own
# manifest and the marketplace entry drifting apart, and the pair sitting at
# the version that strands this file's behaviour.
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
plugin_json = os.path.join(ROOT, "plugins", "reckon", ".claude-plugin", "plugin.json")
market_json = os.path.join(ROOT, ".claude-plugin", "marketplace.json")


def _version_pair():
    with open(plugin_json, encoding="utf-8") as fh:
        mine = json.load(fh)["version"]
    with open(market_json, encoding="utf-8") as fh:
        entry = [x for x in json.load(fh)["plugins"] if x["name"] == "reckon"][0]
    return mine, entry["version"]


if os.path.exists(plugin_json) and os.path.exists(market_json):
    mine, listed = _version_pair()
    ok = mine == listed
    print("%-46s %s" % ("the manifest and the marketplace agree", "ok" if ok else "FAILED"))
    if not ok:
        FAILURES.append("version drift: plugin.json %s, marketplace %s" % (mine, listed))

    parts = tuple(int(x) for x in mine.split(".")[:3])
    ok = parts >= (1, 1, 0)
    print("%-46s %s" % ("the published version carries these repairs", "ok" if ok else "FAILED"))
    if not ok:
        FAILURES.append("published version %s predates the behaviour this file asserts" % mine)
else:
    print("%-46s %s" % ("version check skipped (not in the plugin repo)", "skip"))

# --- 15. a weak join withholds retirement and says so ----------------------
#
# The gate's warning was tested; the behaviour it warns about was not. A brief
# that would retire on a strong join must come out `undecided` on a weak one,
# with the weakness named in the row — otherwise the run reports a retirement
# it has just told the reader not to trust.
CAMP_STRONG = {"present": True, "header": {}, "cases": [
    {"id": "CASE-1", "surface": "SURF-1", "state": "s", "status": "pass", "oracle": "effect-witness"}],
    "flows": [], "components": [],
    "requirements": [{"id": "REQ-1", "text": "the widget saves rows", "evidence": "observed"}],
    "surfaces": [{"id": "SURF-1", "title": "the widget", "slug": "widget"}], "defects": []}
STRONG_EDGES = [{"brief": "BRIEF-x", "target": "REQ-1", "method": "cited", "confidence": 1.0},
                {"brief": "BRIEF-x", "target": "SURF-1", "method": "cited", "confidence": 1.0}]


def brief_row_weak(weak):
    b = {"id": "BRIEF-x", "file": "x.md", "path": "x.md", "title": "the widget saves rows",
         "text": "REQ-1 SURF-1", "status": "", "generated_by": None, "source_ids": []}
    return [r for r in R.classify([b], CAMP_STRONG, STRONG_EDGES, weak) if r["entity"] == "brief"][0]


strong, weak_row = brief_row_weak(False), brief_row_weak(True)
ok = (strong["class"] == "retirable" and weak_row["class"] == "undecided"
      and "join as a whole is too weak" in weak_row["why"])
print("%-46s %s" % ("a weak join withholds retirement, and says why", "ok" if ok else "FAILED"))
if not ok:
    FAILURES.append("weak-join degrade: strong=%r weak=%r why=%r"
                    % (strong["class"], weak_row["class"], weak_row.get("why")))

# --- 16. the headline, end to end through the real entry point -------------
#
# Nothing below `classify` was executed by this file before, so `cmd_build` —
# the headline, the work arithmetic and the two written artifacts — could have
# been deleted and every row above would still have passed. The headline is the
# one figure most readers will act on without opening the ledger, so it is
# checked against a fixture whose true answer is known by construction: one
# open defect is the only product work, one repaired defect and one unjoinable
# brief are not.
import shutil
import tempfile

tmp = tempfile.mkdtemp(prefix="reckon-selftest-")
try:
    briefs_dir = os.path.join(tmp, "briefs")
    camp_dir = os.path.join(tmp, "campaign")
    out_dir = os.path.join(tmp, "out")
    os.makedirs(briefs_dir)
    os.makedirs(camp_dir)
    with open(os.path.join(briefs_dir, "01-nothing-answers-to-this.md"), "w") as fh:
        fh.write("# A brief about zebras\n\nzebras zebras zebras\n")
    with open(os.path.join(camp_dir, "campaign.json"), "w") as fh:
        json.dump({"project": "fixture"}, fh)
    with open(os.path.join(camp_dir, "cases.json"), "w") as fh:
        json.dump([{"id": "CASE-1", "surface": "SURF-1", "state": "s", "status": "pass",
                    "oracle": "outcome"}], fh)
    with open(os.path.join(camp_dir, "inventory.json"), "w") as fh:
        json.dump({"requirement": [{"id": "REQ-1", "text": "the widget saves rows",
                                    "evidence": "observed"}],
                   "surface": [{"id": "SURF-1", "title": "the widget", "slug": "widget"}],
                   "defect": [{"id": "DEF-1", "title": "the widget drops rows", "status": "open",
                               "evidence": ["evidence/one.json"]},
                              {"id": "DEF-2", "title": "the widget used to drop rows",
                               "status": "fixed", "evidence": ["evidence/two.json"]}]}, fh)

    code = R.main(["build", "--briefs", briefs_dir, "--campaign", camp_dir, "--out", out_dir])
    with open(os.path.join(out_dir, "ledger.json"), encoding="utf-8") as fh:
        built = json.load(fh)
    report = open(os.path.join(out_dir, "reckoning.md"), encoding="utf-8").read()

    kinds = built["summary"]["work_by_kind"]
    ok = (code == 0
          and kinds.get("product-work") == 1                     # DEF-1, and nothing else
          and built["summary"]["counts"].get("unjoined") == 1
          and "`unjoined`" in built["headline"]
          and "1 brief(s) could not be tied" in built["headline"])
    print("%-46s %s" % ("the headline counts what is actually left", "ok" if ok else "FAILED"))
    if not ok:
        FAILURES.append("headline: code=%r kinds=%r headline=%r" % (code, kinds, built["headline"]))

    # Read the rows rather than slicing the prose: a string search over a
    # report is satisfied by an id appearing anywhere, including a section that
    # means the opposite. Both defects carry a list-valued `evidence`, so this
    # is also section 8's crash on the real `build` path rather than a fixture.
    by_id = {r["id"]: r for r in built["rows"]}
    remaining = {r["id"] for r in built["rows"] if r.get("is_work_item")}
    ok = (by_id["DEF-2"]["class"] == "verified-done" and "DEF-2" not in remaining
          and by_id["DEF-1"]["class"] == "broken" and "DEF-1" in remaining
          and "Broken (1)" in report)
    print("%-46s %s" % ("a repaired defect is absent from what remains",
                        "ok" if ok else "FAILED"))
    if not ok:
        FAILURES.append("repaired defect: DEF-2=%r remaining=%r"
                        % (by_id["DEF-2"]["class"], sorted(remaining)))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print()
if FAILURES:
    print("%d self-test failure(s):" % len(FAILURES))
    for f in FAILURES:
        print("  -", f)
    sys.exit(1)
print("all gates demonstrated failing on a bad fixture, and silent on a good one")
sys.exit(0)
