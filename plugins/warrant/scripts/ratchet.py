"""Compute the tier each defect class has earned. Apply revocations; propose promotions.

A plain script rather than a model call, deliberately: the component deciding how
much authority a model holds is the one place a model should not sit. Everything
below is arithmetic and comparison over files other steps wrote.

Revocations apply immediately and need no signature, because every one of them
says the evidence a tier rested on has stopped holding, and asking permission to
stop trusting something is the wrong way round. Promotions are written out as a
proposal for the owner to sign, because a tier is authority and authority comes
from a person.

Five triggers, all automatic, all recorded with the reason:

  model_drift       a pinned model id or version differs from the one recorded
                    against the class's last calibration. PCAOB AS 2201 lets an
                    auditor lean on last period's testing of an automated control
                    only where the control is verified unchanged (C12); a
                    reversioned lane is a changed control, so the class drops to 0
                    until it re-earns the tier.
  regression_failing  a case in the class is no longer caught. That is the tier-2
                    entry condition failing, so the tier goes with it.
  new_escape        an escape reported in the class since its last calibration,
                    while the class held a tier above 0.
  westgard          a multirule violation on the corpus pass-rate chart. System
                    level, so it takes every class above 0 with it — the chart is
                    over one series and the signal cannot be attributed further.
  oracle_coverage   coverage below the class's tier-1 threshold.
  calibration_stale the class's calibration is older than [staleness]
                    calibration_max_days, or it has none at all. Evidence that has
                    gone stale is not evidence, and a class above tier 0 whose age
                    cannot be established is treated as stale for the same reason a
                    class with no coverage is treated as below its threshold.

Two places this is fail-closed rather than silent, and both are named in the
output. A class whose lanes cannot be compared — no calibration, or no
lanes.toml — is treated as drifted, because "unable to show the control is
unchanged" is the condition C12 fails on, not a missing file. And a class at a
tier above 0 with no coverage recorded is treated as below its threshold, for the
same reason `tier_of` defaults an unnamed class to 0: absence of evidence is not
evidence of coverage.

Tier 3 counts items closed in the class, from ledger rows carrying a
`defect_class`, inside the window the warrant declares, with no escape reported in
it. A row without a class is counted as unattributable and blocks the promotion
rather than being skipped, because skipping it would let a class reach tier 3 on
rows that may not be its own. Tier 4 is unreachable by design.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as _dt
import io
import json
import os
import pathlib
import shutil
import sys
import tempfile
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import westgard
from _cli import ERROR, FAILED, MISSING, OK, REVOKED, emit, entry, parser, say
from _cli import now as clock
from _cli import run as dispatch
from _state import (Absent, read_json, read_jsonl, read_lanes, read_warrant, state_dir,
                    write_json)
from feedback_record import FIXTURES, escapes_path, parse_model
from ledger import _lane_blocks
from regress_run import result_path, runs_path
from revoke import revoke

_DESC = "Compute earned tiers, apply revocations, propose promotions"

TRIGGERS = ("model_drift", "regression_failing", "new_escape", "westgard", "oracle_coverage")


def _stamp(raw: Any) -> _dt.datetime | None:
    if not isinstance(raw, str):
        return None
    try:
        return _dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def _calibrated_models(entry: dict[str, Any]) -> dict[str, str]:
    """lane -> "model_id@version" from either spelling of the calibration record."""
    models = entry.get("calibration", {}).get("models")
    out: dict[str, str] = {}
    if isinstance(models, list):
        for spec in models:
            try:
                parsed = parse_model(str(spec))
            except ValueError:
                continue
            out[parsed["lane"]] = f"{parsed['model_id']}@{parsed['version']}"
    elif isinstance(models, dict):
        for lane, pin in models.items():
            out[str(lane)] = str(pin)
    return out


def drift_of(entry: dict[str, Any], live: dict[str, tuple[str, str]]) -> list[str]:
    """Every way this class's lanes fail to match what it was calibrated against."""
    calibrated = _calibrated_models(entry)
    declared = entry.get("lanes")
    needed = [str(l) for l in declared] if isinstance(declared, list) \
        else sorted(set(calibrated) | set(live))
    if not needed:
        return ["no lane is pinned for this class, so the control cannot be shown unchanged"]

    problems: list[str] = []
    for lane in needed:
        want = calibrated.get(lane)
        got = f"{live[lane][0]}@{live[lane][1]}" if lane in live else None
        if want is None:
            problems.append(f"lane {lane!r} has no calibration recorded, so there is nothing "
                            "to show the control is unchanged against")
        elif got is None:
            problems.append(f"lane {lane!r} was calibrated at {want} and is no longer declared "
                            "in lanes.toml")
        elif got != want:
            problems.append(f"lane {lane!r} moved from {want} to {got}")
    return problems


def coverage_threshold(warrant: dict[str, Any], entry: dict[str, Any]) -> float:
    """The class's tier-1 coverage threshold, in any spelling the warrant uses.

    charter_init.py writes `[tiers] tier1_oracle_coverage_min` and `[oracle]
    lineage_coverage_min`; a per-class override is `oracle_coverage_min`. Reading
    only one spelling would silently fall back to the 0.95 default and gate a
    warrant against a number nobody wrote in it.
    """
    def _table(key: str) -> dict[str, Any]:
        value = warrant.get(key)
        return value if isinstance(value, dict) else {}

    for candidate in (entry.get("oracle_coverage_min"),
                      _table("thresholds").get("oracle_coverage_tier1"),
                      _table("tiers").get("tier1_oracle_coverage_min"),
                      _table("oracle").get("lineage_coverage_min")):
        if isinstance(candidate, (int, float)) and not isinstance(candidate, bool):
            return float(candidate)
    return 0.95


def tier_cap(entry: dict[str, Any]) -> int:
    """The highest tier the ratchet may ever propose for this class.

    `census = true` caps at 0: a class the warrant sends to a census review is one
    no machine closes, whatever the evidence says about it.
    """
    if isinstance(entry.get("max_tier"), int) and not isinstance(entry["max_tier"], bool):
        return int(entry["max_tier"])
    if entry.get("census") is True:
        return 0
    return 4


def _closed_in_window(root: str | pathlib.Path, defect_class: str,
                      window_days: int, when: _dt.datetime) -> tuple[int, int]:
    """Items this class closed inside the window, and how many rows could not be
    attributed to any class.

    An unattributable row is counted and reported rather than skipped. Skipping it
    silently would let a class reach tier 3 on rows that may not be its own, which
    is the same failure as defaulting an unnamed class to a tier it never earned.
    """
    from ledger import ledger_path
    rows = read_jsonl(ledger_path(root))
    cutoff = when - _dt.timedelta(days=window_days)
    closed = unattributed = 0
    for r in rows:
        if r.get("_malformed") or r.get("verdict") not in ("pass", "fail"):
            continue
        stamped = _stamp(r.get("at"))
        if stamped is None or stamped < cutoff:
            continue
        cls = r.get("defect_class")
        if cls is None:
            unattributed += 1
        elif cls == defect_class:
            closed += 1
    return closed, unattributed


def assess(root: str | pathlib.Path, warrant: dict[str, Any],
           when: _dt.datetime) -> dict[str, Any]:
    """Read every input and work out, per class, what fired and what was earned."""
    inputs: dict[str, Any] = {}

    try:
        lanes_doc = read_lanes(root)
        live = _lane_blocks(lanes_doc)
        inputs["lanes"] = {"present": True, "lanes": sorted(live)}
    except Absent:
        live = {}
        inputs["lanes"] = {"present": False,
                           "note": "no lanes.toml: no class's control can be shown unchanged"}

    health = read_json(state_dir(root) / "suite-health.json", default={})
    inputs["suite_health"] = {"present": bool(health)}
    mutation = health.get("mutation", {}).get("score") if isinstance(health, dict) else None
    cannot_fail = health.get("cannot_fail", {}).get("count") if isinstance(health, dict) else None
    thresholds = warrant.get("thresholds", {})
    assay_ok = (isinstance(mutation, (int, float))
                and mutation >= float(thresholds.get("mutation_score_min", 0.0))
                and isinstance(cannot_fail, int)
                and cannot_fail <= int(thresholds.get("cannot_fail_max", 0)))
    inputs["suite_health"].update(mutation_score=mutation, cannot_fail=cannot_fail,
                                  assay_green=assay_ok)

    regression = read_json(result_path(root), default={})
    inputs["regression"] = {"present": bool(regression),
                            "ok": regression.get("ok") if regression else None}
    by_class = regression.get("by_class", {}) if isinstance(regression, dict) else {}

    coverage_doc = read_json(state_dir(root) / "oracle-coverage.json", default={})
    inputs["oracle_coverage"] = {"present": bool(coverage_doc)}
    coverage = coverage_doc.get("classes", {}) if isinstance(coverage_doc, dict) else {}

    escapes = [r for r in read_jsonl(escapes_path(root)) if "_malformed" not in r]
    inputs["escapes"] = {"rows": len(escapes)}

    series = [r["pass_rate"] for r in read_jsonl(runs_path(root))
              if isinstance(r.get("pass_rate"), (int, float))]
    declared = warrant.get("westgard", {}) if isinstance(warrant.get("westgard"), dict) else {}
    has_declared = all(isinstance(declared.get(k), (int, float)) for k in ("mean", "sd"))
    # A declared baseline charts any series. A computed one needs runs before the
    # current one to compute from, which is westgard.py's own floor.
    minimum = 2 if has_declared else 5
    chart: dict[str, Any] = {"runs": len(series), "violations": [], "charted": False}
    if len(series) >= minimum:
        base = westgard.baseline(series, mean=None, sd=None, warrant=warrant,
                                 window=10, sd_floor=0.005)
        chart = {"runs": len(series), "baseline": base, "charted": True,
                 "violations": westgard.evaluate(series, base["mean"], base["sd"])}
    else:
        chart["note"] = (f"{len(series)} run(s) against a minimum of {minimum}: too few to "
                         "chart, so no control-chart signal either way")
    inputs["westgard"] = chart
    chart_rules = [v["rule"] for v in chart["violations"]]

    classes: dict[str, Any] = {}
    for entry in warrant.get("classes", []):
        name = str(entry.get("name", ""))
        if not name:
            continue
        tier = int(entry.get("tier", 0))
        cap = tier_cap(entry)
        # A panel-plane class is perceptual by declaration. references/tiers.md puts it on
        # the ladder at tier 2 ("tier 1 PLUS perceptual classes"), not at tier 1, so the
        # oracle plane is neither its entry nor grounds for revoking it.
        perceptual = str(entry.get("plane", "") or "").strip().lower() == "panel"
        calibrated_at = _stamp(entry.get("calibration", {}).get("at"))

        drift = drift_of(entry, live)
        cls_regression = by_class.get(name, {})
        not_caught = list(cls_regression.get("not_caught", []))
        unattributable = bool(regression) and regression.get("ok") is False and not by_class
        new_escapes = [e.get("escape_id") for e in escapes
                       if e.get("defect_class") == name
                       and (calibrated_at is None
                            or ((s := _stamp(e.get("reported_at"))) is not None
                                and s > calibrated_at))]
        threshold = coverage_threshold(warrant, entry)
        block = coverage.get(name, {}) if isinstance(coverage, dict) else {}
        measured = block.get("coverage") if isinstance(block, dict) else None
        gaps = block.get("lineage_gaps") if isinstance(block, dict) else None

        fired: list[dict[str, Any]] = []
        if drift:
            fired.append({"trigger": "model_drift", "reason": "; ".join(drift)})
        if not_caught:
            fired.append({"trigger": "regression_failing",
                          "reason": f"{len(not_caught)} regression case(s) no longer caught: "
                                    f"{', '.join(str(c) for c in not_caught)}"})
        elif unattributable:
            fired.append({"trigger": "regression_failing",
                          "reason": "the regression run is failing and its result records no "
                                    "per-class breakdown, so the failure cannot be attributed "
                                    "away from this class"})
        if new_escapes:
            fired.append({"trigger": "new_escape",
                          "reason": f"{len(new_escapes)} escape(s) reported since this class was "
                                    f"calibrated: {', '.join(str(e) for e in new_escapes)}"})
        if chart_rules:
            fired.append({"trigger": "westgard",
                          "reason": f"the corpus pass-rate chart violated {', '.join(chart_rules)}"})
        stale_days = int(warrant.get("staleness", {}).get("calibration_max_days", 0) or 0)
        if tier > 0 and stale_days > 0:
            if calibrated_at is None:
                fired.append({"trigger": "calibration_stale",
                              "reason": "this class has no calibration timestamp, so its "
                                        "evidence cannot be shown to be inside the "
                                        f"{stale_days}-day window the warrant declares"})
            else:
                age = (when - calibrated_at).days
                if age > stale_days:
                    fired.append({"trigger": "calibration_stale",
                                  "reason": f"the calibration is {age} day(s) old and the "
                                            f"warrant allows {stale_days}"})

        if perceptual:
            # No oracle coverage is expected for this class, so its absence is not drift.
            pass
        elif not isinstance(measured, (int, float)):
            globs = [g for g in entry.get("surfaces", []) if isinstance(g, str)]
            where = " ".join(globs) if globs else "the class's surfaces (the warrant names none)"
            fired.append({"trigger": "oracle_coverage",
                          "reason": f"no oracle coverage recorded for this class, so it cannot be "
                                    f"shown at or above its {threshold:.0%} tier-1 threshold",
                          "work_order": {
                              "surfaces": globs,
                              "produces": ".warrant/oracle-coverage.json",
                              "how": [
                                  f"warrant:oracle over {where}, then rollup_classes.py "
                                  f"to key the result by class",
                                  "or test-campaign, which measures the same surfaces per "
                                  "case and exports the file with "
                                  "`campaign.py export-warrant`",
                              ],
                          }})
        elif measured < threshold:
            fired.append({"trigger": "oracle_coverage",
                          "reason": f"oracle coverage is {measured:.1%} against a tier-1 "
                                    f"threshold of {threshold:.1%}"})

        oracle_green = isinstance(measured, (int, float)) and measured >= threshold \
            and (gaps in (None, 0))
        cases = int(cls_regression.get("cases", 0) or 0)
        regression_green = cases > 0 and not not_caught and not unattributable

        # The lineage oracle measures figure provenance, which a spec file or a story does
        # not carry, so requiring it of every class kept perceptual classes off the ladder
        # entirely — the opposite of what tier 2 exists for.
        blockers: list[str] = []
        earned = 0
        if oracle_green:
            earned = 1
        elif not perceptual:
            blockers.append("oracle plane not green for this class")
        if earned >= 1 or perceptual:
            for ok_, why in ((assay_ok, "the assay is not green"),
                             (regression_green, "no clean regression run covering this class"),
                             (not new_escapes, "an escape has been reported since calibration"),
                             (not chart_rules, "the control chart is out of control"),
                             (not drift, "the pinned lanes no longer match the calibration"),
                             (not any(f["trigger"] == "calibration_stale" for f in fired),
                              "the calibration is older than the warrant's window")):
                if not ok_:
                    blockers.append(why)
            if not blockers:
                earned = 2
        if earned >= 2:
            # charter_init.py writes `tier3_items_closed_min`; references/tiers.md and
            # earlier drafts of this script say `tier3_items`. Both are read, newest
            # name first, because warrant.toml is signed by a person: renaming the key
            # in the warrant would invalidate every signature in the wild to fix a
            # reader bug. A warrant already in use keeps working.
            tiers_tbl = warrant.get("tiers")
            tiers_tbl = tiers_tbl if isinstance(tiers_tbl, dict) else {}
            need = 0
            for candidate in (tiers_tbl.get("tier3_items_closed_min"),
                              tiers_tbl.get("tier3_items")):
                if isinstance(candidate, int) and not isinstance(candidate, bool) \
                        and candidate > 0:
                    need = candidate
                    break
            window = int(tiers_tbl.get("tier3_window_days", 0) or 0)
            if need <= 0 or window <= 0:
                blockers.append("tier 3 has no entry condition: set [tiers] "
                                "tier3_items_closed_min and tier3_window_days in the warrant")
            else:
                closed, unattributed = _closed_in_window(root, name, window, when)
                if unattributed:
                    blockers.append(f"tier 3 cannot be counted: {unattributed} ledger row(s) in "
                                    f"the window carry no defect_class, so they cannot be "
                                    f"attributed to a class")
                elif closed < need:
                    blockers.append(f"tier 3 needs {need} item(s) closed in this class over "
                                    f"{window} day(s); the ledger records {closed}")
                elif new_escapes:
                    blockers.append("tier 3 needs no escape in the window; this class has one")
                else:
                    earned = 3
        earned = min(earned, cap)

        classes[name] = {
            "current_tier": tier, "earned_tier": earned, "max_tier": cap,
            "triggers": fired, "blockers": blockers,
            "oracle": {"coverage": measured, "threshold": threshold, "lineage_gaps": gaps},
            "regression": {"cases": cases, "not_caught": not_caught},
            "escapes_since_calibration": new_escapes,
            "calibrated_at": entry.get("calibration", {}).get("at"),
            "lane_drift": drift,
        }

    return {"inputs": inputs, "classes": classes, "at": when.isoformat()}


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--dry-run", action="store_true",
                   help="report what would be revoked without writing the warrant")
    p.add_argument("--no-report", action="store_true",
                   help="do not write the proposal report")


def main(args: argparse.Namespace) -> int:
    warrant = read_warrant(args.root)
    when = clock(args)
    assessment = assess(args.root, warrant, when)
    version = str(warrant.get("version", "unsigned"))

    revocations: list[dict[str, Any]] = []
    for name, block in assessment["classes"].items():
        if block["current_tier"] <= 0 or not block["triggers"]:
            continue
        primary = block["triggers"][0]
        reason = " | ".join(t["reason"] for t in block["triggers"])
        if args.dry_run:
            revocations.append({"defect_class": name, "trigger": primary["trigger"],
                                "reason": reason, "previous_tier": block["current_tier"],
                                "changed": False, "dry_run": True,
                                "why": f"{name} would drop from tier {block['current_tier']} "
                                       "to tier 0"})
            continue
        try:
            result = revoke(args.root, name, reason=reason, trigger=primary["trigger"],
                            when=when, warrant_version=version)
        except ValueError as exc:
            result = {"defect_class": name, "trigger": primary["trigger"], "reason": reason,
                      "changed": False, "previous_tier": block["current_tier"],
                      "why": str(exc), "ledger_error": None}
        result["dry_run"] = False
        revocations.append(result)
        if result.get("changed"):
            block["current_tier"] = 0

    revoked_now = {r["defect_class"] for r in revocations}
    proposals = [
        {"defect_class": name, "from_tier": block["current_tier"],
         "to_tier": block["earned_tier"],
         "evidence": {"oracle": block["oracle"], "regression": block["regression"],
                      "assay_green": assessment["inputs"]["suite_health"]["assay_green"],
                      "calibrated_at": block["calibrated_at"]}}
        for name, block in assessment["classes"].items()
        if block["earned_tier"] > block["current_tier"] and name not in revoked_now
    ]

    payload = {**assessment, "revocations": revocations, "proposals": proposals,
               "revoked": sorted(r["defect_class"] for r in revocations if r.get("changed")
                                 or r.get("dry_run")),
               "warrant_version": version,
               "tier3": "counted from ledger rows carrying a defect_class; see this script's docstring",
               "tier4": "unreachable by design",
               "dry_run": bool(args.dry_run)}

    errors: list[str] = []
    if not args.no_report:
        try:
            state_dir(args.root, create=True)
            write_json(state_dir(args.root) / "reports"
                       / f"{when.date().isoformat()}-ratchet.json", payload)
        except Exception as exc:                                   # noqa: BLE001
            errors.append(f"{type(exc).__name__}: {exc}")
    payload["record_errors"] = errors

    for name, block in assessment["classes"].items():
        say(args, f"{name}: tier {block['current_tier']}, earned {block['earned_tier']}"
                  + (f" (capped at {block['max_tier']})" if block["max_tier"] < 4 else ""))
        for t in block["triggers"]:
            say(args, f"    {t['trigger']}: {t['reason']}")
            order = t.get("work_order")
            if isinstance(order, dict):
                surfaces = " ".join(order.get("surfaces") or []) or "(none named)"
                say(args, f"      surfaces: {surfaces}")
                say(args, f"      produces: {order.get('produces')}")
                for step in order.get("how") or []:
                    say(args, f"      run: {step}")
        for b in block["blockers"]:
            say(args, f"    blocker: {b}")
    for r in revocations:
        prefix = "WOULD REVOKE" if r.get("dry_run") else "REVOKED"
        say(args, f"{prefix} {r['defect_class']}: {r['trigger']}")
        if r.get("ledger_error"):
            say(args, f"  warning: the warrant was written but the ledger row failed — "
                      f"{r['ledger_error']}")
    for p in proposals:
        say(args, f"PROPOSED {p['defect_class']}: tier {p['from_tier']} -> {p['to_tier']} "
                  "— not applied; a promotion needs the owner's signature")
    for e in errors:
        say(args, f"warning: the assessment ran but writing the report failed — {e}")
    emit(args, payload)

    return REVOKED if revocations else OK


def _parse(argv: list[str]) -> argparse.Namespace:
    p = parser(_DESC)
    _extra(p)
    return p.parse_args(argv)


def _run(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = dispatch(main, None, _parse(argv))
    return code, out.getvalue(), err.getvalue()


BASE_FILES = {"warrant.toml": "warrant.toml", "lanes.toml": "lanes.toml",
              "suite-health.json": "suite-health.json",
              "oracle-coverage.json": "oracle-coverage.json",
              "escapes.jsonl": "escapes.jsonl",
              "regression-result.json": "regression-result.json",
              "regression-runs.jsonl": "regression-runs.jsonl"}


def _seed(tmp: str, **swap: str | None) -> pathlib.Path:
    """Copy the in-control fixture set, then swap or drop one file per trigger."""
    d = pathlib.Path(tmp) / ".warrant"
    d.mkdir(parents=True, exist_ok=True)
    for target, source in BASE_FILES.items():
        source = swap.get(target.replace(".", "_").replace("-", "_"), source)
        if source is None:
            continue
        shutil.copy(FIXTURES / source, d / target)
    return d


def _tiers(tmp: str) -> dict[str, int]:
    return {str(c["name"]): int(c.get("tier", 0)) for c in read_warrant(tmp).get("classes", [])}


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    NOW = ["--now", "2026-08-18T10:00:00+00:00"]

    # The in-control baseline. Every trigger below is one swap away from this, so
    # a trigger that fires here would make every other case unreadable.
    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp)
        code, out, err = _run(["--root", tmp, "--json"] + NOW)
        payload = json.loads(out)
        cases.append(("an in-control repository exits 0", code == OK))
        cases.append(("no revocation fires", payload["revocations"] == []))
        cases.append(("stdout under --json is only the JSON object", out.lstrip().startswith("{")))
        cases.append(("figure-lineage keeps tier 2", _tiers(tmp)["figure-lineage"] == 2))
        cases.append(("layout-drift has earned tier 2",
                      payload["classes"]["layout-drift"]["earned_tier"] == 2))
        cases.append(("so a promotion is PROPOSED, not applied",
                      [(p["defect_class"], p["from_tier"], p["to_tier"]) for p in payload["proposals"]]
                      == [("layout-drift", 1, 2)] and _tiers(tmp)["layout-drift"] == 1))
        cases.append(("the human output says the promotion needs a signature",
                      "needs the owner's signature" in err))
        cases.append(("a class the warrant caps is never proposed above the cap",
                      payload["classes"]["disclosure-content"]["earned_tier"] == 0))
        fl = payload["classes"]["figure-lineage"]
        cases.append(("tier 3 is blocked when the ledger records too few closed items",
                      fl["earned_tier"] < 3
                      and any("tier 3" in b for b in fl["blockers"])))

    # Staleness. The warrant declares the window; before this trigger existed the
    # key was written by charter_init and read by nothing.
    for label, days, expect_fired in (("stale calibration revokes", 1, True),
                                      ("fresh calibration does not", 3650, False)):
        with tempfile.TemporaryDirectory() as tmp:
            _seed(tmp)
            w = pathlib.Path(tmp) / ".warrant" / "warrant.toml"
            w.write_text(w.read_text()
                         + f'\n[staleness]\ncalibration_max_days = {days}\n')
            code, out, _ = _run(["--root", tmp, "--json", "--dry-run"] + NOW)
            fired = {f["trigger"] for c in json.loads(out)["classes"].values()
                     for f in c["triggers"]}
            cases.append((label, ("calibration_stale" in fired) is expect_fired))

    # Tier 3 earned: enough attributed rows in the window, and no escape in it.
    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp)
        import ledger as _ledger
        w = pathlib.Path(tmp) / ".warrant" / "warrant.toml"
        w.write_text(w.read_text() + '\n[tiers]\ntier3_items = 3\ntier3_window_days = 30\n')
        (pathlib.Path(tmp) / ".warrant" / "escapes.jsonl").write_text("")
        for i in range(3):
            _ledger.append_row(tmp, item=f"I-{i}", verdict="pass", tier=2,
                               defect_class="figure-lineage",
                               when=_dt.datetime(2026, 8, 17, tzinfo=_dt.timezone.utc))
        code, out, _ = _run(["--root", tmp, "--json", "--dry-run"] + NOW)
        earned = json.loads(out)["classes"]["figure-lineage"]["earned_tier"]
        cases.append(("tier 3 is earned on three attributed rows with no escape", earned == 3))

    # Tier 3 read through the spelling charter_init actually writes. Before this, the
    # charter wrote `tier3_items_closed_min` and this script read `tier3_items`, so
    # `need` was always 0 and every class that reached tier 2 stopped there with
    # "tier 3 has no entry condition" — Verified was unreachable by construction.
    # The tier-3 cases above hid it by hand-writing the reader's spelling.
    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp)
        import ledger as _ledger
        w = pathlib.Path(tmp) / ".warrant" / "warrant.toml"
        w.write_text(w.read_text()
                     + '\n[tiers]\ntier3_items_closed_min = 3\ntier3_window_days = 30\n')
        (pathlib.Path(tmp) / ".warrant" / "escapes.jsonl").write_text("")
        for i in range(3):
            _ledger.append_row(tmp, item=f"I-{i}", verdict="pass", tier=2,
                               defect_class="figure-lineage",
                               when=_dt.datetime(2026, 8, 17, tzinfo=_dt.timezone.utc))
        code, out, _ = _run(["--root", tmp, "--json", "--dry-run"] + NOW)
        fl3 = json.loads(out)["classes"]["figure-lineage"]
        cases.append(("tier 3 is earned through charter_init's tier3_items_closed_min spelling",
                      fl3["earned_tier"] == 3))
        cases.append(("and no longer reports tier 3 as having no entry condition",
                      not any("no entry condition" in b for b in fl3["blockers"])))

    # A perceptual class enters at tier 2 without the oracle plane. references/tiers.md
    # defines tier 2 as "tier 1 PLUS perceptual classes"; the ladder used to require
    # oracle greenness of every class, so a panel-plane class could never leave tier 0
    # however green its assay and regression corpus were.
    #
    # Oracle coverage is DROPPED here on purpose. With the in-control fixture the class is
    # oracle-green anyway, so it reaches tier 2 by the tier-1 route and the case passes
    # with or without the fix — it has to be denied that route to test anything.
    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp, oracle_coverage_json=None)
        w = pathlib.Path(tmp) / ".warrant" / "warrant.toml"
        w.write_text(w.read_text().replace('name = "layout-drift"',
                                           'name = "layout-drift"\nplane = "panel"', 1))
        code, out, _ = _run(["--root", tmp, "--json", "--dry-run"] + NOW)
        ld = json.loads(out)["classes"]["layout-drift"]
        cases.append(("a panel-plane class reaches tier 2 with no oracle coverage at all",
                      ld["earned_tier"] >= 2))
        cases.append(("and the oracle gate is not held against it",
                      not any("oracle plane not green" in b for b in ld["blockers"])))
        cases.append(("missing oracle coverage does not revoke a perceptual class",
                      not any(f["trigger"] == "oracle_coverage" for f in ld["triggers"])))
        cases.append(("while a non-perceptual class in the same run is still gated on it",
                      json.loads(out)["classes"]["figure-lineage"]["earned_tier"] == 0))

    # An unattributable row blocks rather than being skipped.
    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp)
        import ledger as _ledger
        w = pathlib.Path(tmp) / ".warrant" / "warrant.toml"
        w.write_text(w.read_text() + '\n[tiers]\ntier3_items = 3\ntier3_window_days = 30\n')
        (pathlib.Path(tmp) / ".warrant" / "escapes.jsonl").write_text("")
        for i in range(3):
            _ledger.append_row(tmp, item=f"I-{i}", verdict="pass", tier=2,
                               defect_class="figure-lineage",
                               when=_dt.datetime(2026, 8, 17, tzinfo=_dt.timezone.utc))
        _ledger.append_row(tmp, item="I-x", verdict="pass", tier=2, defect_class=None,
                           when=_dt.datetime(2026, 8, 17, tzinfo=_dt.timezone.utc))
        code, out, _ = _run(["--root", tmp, "--json", "--dry-run"] + NOW)
        fl2 = json.loads(out)["classes"]["figure-lineage"]
        cases.append(("an unattributable ledger row blocks tier 3 rather than being skipped",
                      fl2["earned_tier"] < 3
                      and any("unattributable" in b or "no defect_class" in b
                              for b in fl2["blockers"])))
        cases.append(("tier 4 is reported unreachable", "unreachable" in payload["tier4"]))
        cases.append(("the proposal is written to a dated report",
                      (pathlib.Path(tmp) / ".warrant" / "reports"
                       / "2026-08-18-ratchet.json").exists()))

    # One trigger at a time.
    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp, lanes_toml="lanes-drifted.toml")
        code, out, err = _run(["--root", tmp, "--json"] + NOW)
        payload = json.loads(out)
        fired = {r["defect_class"]: r["trigger"] for r in payload["revocations"]}
        cases.append(("a reversioned lane exits 4", code == REVOKED))
        cases.append(("model_drift is the trigger recorded",
                      set(fired.values()) == {"model_drift"}))
        cases.append(("every class depending on that lane drops to 0",
                      _tiers(tmp)["figure-lineage"] == 0 and _tiers(tmp)["layout-drift"] == 0))
        cases.append(("the reason names the version it moved to",
                      "2026-08-14" in payload["revocations"][0]["reason"]))
        cases.append(("a class already at tier 0 is not revoked again",
                      "disclosure-content" not in fired))
        cases.append(("the revocations are recorded in the ledger",
                      sum(1 for l in (pathlib.Path(tmp) / ".warrant" / "ledger.jsonl")
                          .read_text().splitlines() if l.strip()) == 2))
        cases.append(("a revoked class is not proposed a promotion in the same run",
                      payload["proposals"] == []))

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp, regression_result_json="regression-result-failing.json")
        code, out, _ = _run(["--root", tmp, "--json"] + NOW)
        fired = {r["defect_class"]: r["trigger"] for r in json.loads(out)["revocations"]}
        cases.append(("a failing regression run exits 4", code == REVOKED))
        cases.append(("regression_failing fires only on the class that failed",
                      fired == {"figure-lineage": "regression_failing"}))
        cases.append(("the class that still passes keeps its tier",
                      _tiers(tmp)["layout-drift"] == 1))

    with tempfile.TemporaryDirectory() as tmp:
        d = _seed(tmp)
        (d / "escapes.jsonl").write_text((FIXTURES / "escapes.jsonl").read_text() +
                                         (FIXTURES / "escapes-new.jsonl").read_text())
        code, out, _ = _run(["--root", tmp, "--json"] + NOW)
        payload = json.loads(out)
        fired = {r["defect_class"]: r["trigger"] for r in payload["revocations"]}
        cases.append(("a new escape in a class above tier 0 exits 4", code == REVOKED))
        cases.append(("new_escape fires on that class alone",
                      fired == {"figure-lineage": "new_escape"}))
        cases.append(("the reason names the escape",
                      "esc-20260812-6f708192" in payload["revocations"][0]["reason"]))
        cases.append(("escapes older than the calibration do not fire it",
                      payload["classes"]["layout-drift"]["escapes_since_calibration"] == []))

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp, regression_runs_jsonl="regression-runs-violation.jsonl")
        code, out, _ = _run(["--root", tmp, "--json"] + NOW)
        payload = json.loads(out)
        fired = {r["defect_class"]: r["trigger"] for r in payload["revocations"]}
        cases.append(("a control-chart violation exits 4", code == REVOKED))
        cases.append(("westgard fires on every class above tier 0",
                      fired == {"figure-lineage": "westgard", "layout-drift": "westgard"}))
        cases.append(("the reason names the rule",
                      "1-3s" in payload["revocations"][0]["reason"]))

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp, oracle_coverage_json="oracle-coverage-low.json")
        code, out, _ = _run(["--root", tmp, "--json"] + NOW)
        payload = json.loads(out)
        fired = {r["defect_class"]: r["trigger"] for r in payload["revocations"]}
        cases.append(("coverage below the class threshold exits 4", code == REVOKED))
        cases.append(("oracle_coverage fires on the class below its own threshold",
                      fired == {"figure-lineage": "oracle_coverage"}))
        cases.append(("a class above its own lower threshold is untouched",
                      _tiers(tmp)["layout-drift"] == 1))
        cases.append(("the reason carries the measurement and the threshold",
                      "82.5%" in payload["revocations"][0]["reason"] and
                      "95.0%" in payload["revocations"][0]["reason"]))

    # Fail-closed cases: an absent input is not a pass.
    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp, oracle_coverage_json=None)
        code, out, _ = _run(["--root", tmp, "--json"] + NOW)
        payload = json.loads(out)
        cases.append(("no coverage report at all exits 4, not 0", code == REVOKED))
        cases.append(("and says the class cannot be shown above its threshold",
                      "cannot be shown" in payload["revocations"][0]["reason"]))

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp, lanes_toml=None)
        code, out, _ = _run(["--root", tmp, "--json"] + NOW)
        payload = json.loads(out)
        cases.append(("no lanes.toml exits 4 rather than skipping the drift check",
                      code == REVOKED))
        cases.append(("and says the control cannot be shown unchanged",
                      "no longer declared" in payload["revocations"][0]["reason"]))

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp, suite_health_json=None)
        code, out, _ = _run(["--root", tmp, "--json"] + NOW)
        payload = json.loads(out)
        cases.append(("no suite health is not a revocation trigger", code == OK))
        cases.append(("but it blocks tier 2 and says so",
                      payload["classes"]["layout-drift"]["earned_tier"] == 1 and
                      any("assay is not green" in b
                          for b in payload["classes"]["layout-drift"]["blockers"])))

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp, regression_runs_jsonl=None)
        code, out, _ = _run(["--root", tmp, "--json"] + NOW)
        cases.append(("too short a run series charts nothing either way",
                      code == OK and json.loads(out)["inputs"]["westgard"]["charted"] is False))

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp, lanes_toml="lanes-drifted.toml")
        code, out, err = _run(["--root", tmp, "--json", "--dry-run"] + NOW)
        cases.append(("--dry-run still exits 4", code == REVOKED))
        cases.append(("but leaves the warrant alone",
                      _tiers(tmp)["figure-lineage"] == 2))
        cases.append(("and says it would have revoked", "WOULD REVOKE" in err))

    with tempfile.TemporaryDirectory() as tmp:
        # A warrant in charter_init.py's spelling: the threshold lives under
        # [tiers] and a census class is marked with `census`, not `max_tier`.
        d = _seed(tmp, warrant_toml=None)
        (d / "warrant.toml").write_text(
            'version = "2.0.0"\n'
            'owner = "Luke Rhodes"\n\n'
            "[oracle]\nlineage_coverage_min = 0.95\n\n"
            "[tiers]\ntier1_oracle_coverage_min = 0.99\n\n"
            '[[classes]]\nname = "figure-lineage"\ntier = 2\ncensus = false\n\n'
            '[[classes]]\nname = "disclosure-content"\ntier = 2\ncensus = true\n')
        code, out, _ = _run(["--root", tmp, "--json"] + NOW)
        payload = json.loads(out)
        fired = [t["trigger"] for t in payload["classes"]["figure-lineage"]["triggers"]]
        cases.append(("the threshold is read from charter_init's [tiers] spelling",
                      payload["classes"]["figure-lineage"]["oracle"]["threshold"] == 0.99
                      and "oracle_coverage" in fired))
        cases.append(("a census class is capped at tier 0 whatever its coverage",
                      payload["classes"]["disclosure-content"]["earned_tier"] == 0
                      and payload["classes"]["disclosure-content"]["max_tier"] == 0))
        cases.append(("and a census class holding a tier above 0 is still revoked",
                      code == REVOKED and _tiers(tmp)["disclosure-content"] == 0))

    with tempfile.TemporaryDirectory() as tmp:
        cases.append(("an absent warrant exits 3", _run(["--root", tmp])[0] == MISSING))

    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp) / ".warrant"
        d.mkdir(parents=True)
        (d / "warrant.toml").write_text('version = "0.1.0"\nowner = "nobody"\n')
        code, out, _ = _run(["--root", tmp, "--json"] + NOW)
        cases.append(("a warrant naming no classes exits 0 with nothing to do",
                      code == OK and json.loads(out)["classes"] == {}))

    return cases


if __name__ == "__main__":
    raise SystemExit(entry(_DESC, main, selftest, _extra))
