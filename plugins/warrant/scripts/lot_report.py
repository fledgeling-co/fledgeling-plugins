#!/usr/bin/env python3
"""The audit report on one lot. Five fields or it does not validate.

    population              with its size
    tolerable_error_rate    the risk that was declared
    sample_size             how many items were actually reviewed
    seed_recovery           recovered out of seeded
    decision                accept, extend, or escalate

Any one of them absent is exit 2. This is what replaces per-item signatures in an
audit conversation, and a report that names a percentage without saying what it is
a percentage of cannot be read: published proficiency-test failure rates differ by
more than twentyfold depending on the denominator — 1.4% of 670,489 challenges
across 665 laboratories against 32.4% of lab-parameter results across three — and
both figures were correct. So every rate here travels with its numerator and its
denominator, and the renderer checks its own output for a bare one before it exits.

Two ways in. `--result FILE` validates and renders an assembled result. Otherwise
the result is assembled from `--plan` (lot_plan.py), `--key` (blind_queue.py's
operator key) and `--review` (the reviewer's calls), and any field that cannot be
assembled is reported absent rather than guessed.

A missed seed overrides an accept. If the review did not recover a defect that was
planted for it to find, the sample's own sensitivity is in question and the lot
cannot be accepted on that review.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import pathlib
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                   # noqa: E402
import _state                                                 # noqa: E402

FIXTURES = (pathlib.Path(__file__).resolve().parent.parent
            / "evals" / "fixtures" / "charter-panel-lot")

REQUIRED = ("population", "tolerable_error_rate", "sample_size", "seed_recovery",
            "decision", "oracle_mix")

# The rungs a case can stand on, weakest first. The first four establish that
# something was touched, present or shaped; only the last four establish that a
# promised effect happened. A lot audited entirely on the weak rungs has been
# audited on whether the screen looked right, which is the minority of what a
# reviewer produces (`C6`) and not the class that hurts (`I7`).
EFFECT_RUNGS = ("outcome", "metamorphic", "raster-visual", "interactive-glass")
WEAK_RUNGS = ("touch", "presence", "structural", "structural-visual")


def check_required(result: dict[str, object]) -> list[str]:
    """The six, each named with what would fix it."""
    missing: list[str] = []
    for field in REQUIRED:
        if field not in result or result[field] is None:
            missing.append(f"{field} is absent")
    if "population" in result and result.get("population") is not None:
        pop = result["population"]
        if not isinstance(pop, dict) or not isinstance(pop.get("size"), int) \
                or isinstance(pop.get("size"), bool) or int(pop.get("size", 0)) <= 0:
            missing.append("population.size is absent or not a positive count — a "
                           "percentage with no denominator cannot be read")
    rate = result.get("tolerable_error_rate")
    if rate is not None and (isinstance(rate, bool) or not isinstance(rate, (int, float))
                             or not (0.0 < float(rate) < 1.0)):
        missing.append(f"tolerable_error_rate is {rate!r}, not a proportion in (0,1)")
    size = result.get("sample_size")
    if size is not None and (isinstance(size, bool) or not isinstance(size, int)
                             or size < 0):
        missing.append(f"sample_size is {size!r}, not a count")
    recovery = result.get("seed_recovery")
    if recovery is not None:
        if not isinstance(recovery, dict):
            missing.append("seed_recovery is not a {recovered, seeded} pair")
        else:
            for key in ("recovered", "seeded"):
                value = recovery.get(key)
                if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                    missing.append(f"seed_recovery.{key} is absent or not a count")
    decision = result.get("decision")
    if decision is not None and not str(decision).strip():
        missing.append("decision is blank")
    mix = result.get("oracle_mix")
    if mix is not None:
        if not isinstance(mix, dict) or not mix:
            missing.append("oracle_mix is not a {rung: count} map — a lot that cannot "
                           "say what rung its evidence stands on cannot support the "
                           "claim it makes")
        else:
            for rung, count in mix.items():
                if not isinstance(count, int) or isinstance(count, bool) or count < 0:
                    missing.append(f"oracle_mix[{rung!r}] is {count!r}, not a count")
    return missing


def bare_rates(lines: list[str]) -> list[str]:
    """Lines that print a percentage without its population.

    The rule made mechanical, on this script's own output.
    """
    return [line for line in lines
            if "%" in line and " of " not in line and "rate" not in line.lower()]


def _read_rows(path: pathlib.Path) -> list[dict[str, object]]:
    if not path.is_file():
        raise _state.Absent(str(path))
    text = path.read_text().strip()
    if not text:
        return []
    if text.startswith("["):
        return [r for r in json.loads(text) if isinstance(r, dict)]
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def assemble(plan: dict[str, object], key: dict[str, object],
             review: list[dict[str, object]]) -> tuple[dict[str, object], list[str]]:
    """Build the result from the plan, the seed key and the reviewer's calls."""
    notes: list[str] = []
    seeds = {int(s["position"]): s for s in key.get("seeds", [])
             if isinstance(s, dict) and isinstance(s.get("position"), int)}
    seen: set[int] = set()
    real_reviewed = 0
    errors_found = 0
    recovered = 0
    unpositioned = 0
    oracle_mix: dict[str, int] = {}

    for row in review:
        position = row.get("position")
        if not isinstance(position, int):
            unpositioned += 1
            continue
        if position in seen:
            notes.append(f"position {position} was reviewed more than once; the later "
                         "call is the one counted")
        seen.add(position)
        rung = str(row.get("oracle", row.get("rung", ""))).strip().lower()
        if position not in seeds:
            oracle_mix[rung or "unstated"] = oracle_mix.get(rung or "unstated", 0) + 1
        call = str(row.get("call", "")).strip().lower()
        if call not in ("defect", "clean"):
            notes.append(f"position {position}: call {row.get('call')!r} is neither "
                         "'defect' nor 'clean' and is not counted")
            continue
        if position in seeds:
            if call == "defect":
                recovered += 1
        else:
            real_reviewed += 1
            if call == "defect":
                errors_found += 1
    if unpositioned:
        notes.append(f"{unpositioned} review row(s) carry no position and are not "
                     "counted")

    lot_size = plan.get("lot_size")
    ladder = {int(row["errors"]): row for row in plan.get("ladder", [])
              if isinstance(row, dict) and isinstance(row.get("errors"), int)}
    intolerable_at = plan.get("intolerable_at")
    rung = ladder.get(errors_found)
    needed = rung.get("sample") if isinstance(rung, dict) else None

    # The denominator is seeds the reviewer was actually shown, not seeds planted:
    # a seed sitting past the end of the reviewed prefix has not been missed, it has
    # not been reached, and counting it as a miss would read as a failed review.
    presented = sorted(p for p in seeds if p in seen)
    seeded = len(presented)
    unreached = len(seeds) - seeded
    missed = seeded - recovered
    if unreached:
        notes.append(f"{unreached} of {len(seeds)} planted seed(s) sit beyond the "
                     "reviewed positions and are not counted either way")
    if seeded == 0:
        notes.append("no seeds were presented, so the review's own sensitivity is "
                     "unmeasured here")

    if isinstance(intolerable_at, int) and errors_found >= intolerable_at:
        decision = (f"escalate: {errors_found} error(s) found is the intolerable count "
                    f"({intolerable_at}) — census the remainder and route to the owner")
    elif missed > 0:
        decision = (f"escalate: the review missed {missed} of {seeded} seeded defect(s), "
                    "so the lot cannot be accepted on this review — re-review with a "
                    "fresh reviewer before deciding")
    elif needed is None:
        decision = ("census: no sample settles this lot at the declared risk limit — "
                    "review every item")
    elif real_reviewed >= int(needed):
        decision = (f"accept the lot: {errors_found} error(s) in {real_reviewed} of "
                    f"{lot_size} items sampled, and every seeded defect was recovered")
    else:
        decision = (f"extend: {errors_found} error(s) found needs {needed} item(s) "
                    f"sampled and {real_reviewed} of {lot_size} have been reviewed — "
                    f"draw {int(needed) - real_reviewed} more before deciding")

    result = {
        "lot_id": plan.get("lot_id") or key.get("lot_id"),
        "warrant_version": plan.get("warrant_version"),
        "population": {"id": plan.get("lot_id"), "size": lot_size,
                       "queue_positions": key.get("population")},
        "tolerable_error_rate": plan.get("tolerable_error_rate"),
        "risk_limit": plan.get("risk_limit"),
        "intolerable_at": intolerable_at,
        "planned_initial_sample": plan.get("initial_sample"),
        "sample_size": real_reviewed,
        "errors_found": errors_found,
        "seed_recovery": {"recovered": recovered, "seeded": seeded,
                          "planted": len(seeds), "unreached": unreached},
        "decision": decision,
        "oracle_mix": oracle_mix or {"unstated": real_reviewed},
        "escalation": plan.get("escalation"),
        "reviewed_positions": len(seen),
    }
    return result, notes


def extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--result", default=None,
                   help="an assembled result to validate and render")
    p.add_argument("--plan", default=None, help="the plan from lot_plan.py")
    p.add_argument("--key", default=None, help="the operator key from blind_queue.py")
    p.add_argument("--review", default=None,
                   help="the reviewer's calls: rows of {position, call: defect|clean}")


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()
    notes: list[str] = []

    if args.result:
        path = pathlib.Path(args.result).expanduser().resolve()
        if not path.is_file():
            raise _state.Absent(str(path))
        result = json.loads(path.read_text())
        if not isinstance(result, dict):
            _cli.say(args, f"{path} is not a JSON object")
            _cli.emit(args, {"ok": False, "reason": "not-an-object"})
            return _cli.ERROR
        source = str(path)
    else:
        if not (args.plan and args.key and args.review):
            _cli.say(args, "pass --result, or all three of --plan, --key and --review")
            _cli.say(args, "  the five required fields come from the plan (population, "
                           "tolerable error rate), the key (seed recovery) and the "
                           "review (sample size, decision)")
            _cli.emit(args, {"ok": False, "reason": "usage"})
            return _cli.ERROR
        plan = _state.read_json(pathlib.Path(args.plan).expanduser().resolve())
        key = _state.read_json(pathlib.Path(args.key).expanduser().resolve())
        review = _read_rows(pathlib.Path(args.review).expanduser().resolve())
        result, notes = assemble(plan, key, review)
        source = "assembled from the plan, the key and the review"

    missing = check_required(result)
    lines: list[str] = []
    pop = result.get("population") if isinstance(result.get("population"), dict) else {}
    size = pop.get("size") if isinstance(pop.get("size"), int) else None
    recovery = result.get("seed_recovery") if isinstance(result.get("seed_recovery"), dict) else {}

    lines.append(f"lot {result.get('lot_id') or 'unnamed'}  ({source})")
    lines.append(f"  population            {size if size is not None else 'ABSENT'}"
                 f" item(s)" + (f", {pop.get('queue_positions')} queue position(s)"
                                if pop.get("queue_positions") else ""))
    lines.append(f"  tolerable error rate  {result.get('tolerable_error_rate', 'ABSENT')}"
                 + (f"  ({result.get('intolerable_at')} defective item(s) of "
                    f"{size} makes the lot intolerable)"
                    if result.get("intolerable_at") is not None and size else ""))
    sample = result.get("sample_size")
    lines.append("  sample size           "
                 + (_cli.rate(sample, size, "items reviewed")
                    if isinstance(sample, int) and size else f"{sample} (no population)"))
    errors = result.get("errors_found")
    if isinstance(errors, int) and isinstance(sample, int):
        lines.append("  errors found          " + _cli.rate(errors, sample,
                                                            "reviewed items called defective"))
    recovered, seeded = recovery.get("recovered"), recovery.get("seeded")
    lines.append("  seed recovery         "
                 + (f"{recovered} recovered of {seeded} seeded"
                    + (" — " + _cli.rate(recovered, seeded, "seeded defects recovered")
                       if isinstance(seeded, int) and seeded > 0 else
                       " (no seeds planted, so recovery is unmeasured)")
                    if isinstance(recovered, int) and isinstance(seeded, int)
                    else "ABSENT"))
    mix = result.get("oracle_mix")
    if isinstance(mix, dict) and mix:
        total = sum(v for v in mix.values() if isinstance(v, int))
        parts = ", ".join(f"{rung} {count}" for rung, count in
                          sorted(mix.items(), key=lambda kv: (-kv[1], kv[0])))
        lines.append(f"  oracle mix            {parts}  (of {total} sampled)")
        effect = sum(count for rung, count in mix.items() if rung in EFFECT_RUNGS)
        if total > 0 and effect == 0:
            lines.append("                        no case in this sample stands on an "
                         "effect rung, so the lot was audited on whether the surface "
                         "looked right rather than on whether it did anything")
    else:
        lines.append("  oracle mix            ABSENT")
    lines.append(f"  decision              {result.get('decision', 'ABSENT')}")
    if result.get("escalation") and isinstance(result["escalation"], dict):
        route = result["escalation"].get("route") or "NOBODY (the warrant names no owner)"
        lines.append(f"  escalation route      {route}")
    for note in notes:
        lines.append(f"  note                  {note}")

    unpopulated = bare_rates(lines)
    if unpopulated:
        lines.append("  self-check            a rate was printed without its "
                     "population; that is a bug in this script, not in the lot")

    for line in lines:
        _cli.say(args, line)

    if missing:
        _cli.say(args, f"report INVALID: {len(missing)} required field(s) missing or "
                       "unusable")
        for problem in missing:
            _cli.say(args, f"  {problem}")
        _cli.say(args, "  a report missing any of the five does not validate: "
                       "population with its size, tolerable error rate, sample size, "
                       "seed recovery count, decision")
        _cli.emit(args, {"ok": False, "missing": missing, "result": result,
                         "bare_rates": unpopulated, "notes": notes})
        return _cli.FAILED

    stamp = _cli.now(args)
    out = _state.state_dir(root, create=True) / "reports" / \
        f"{stamp.date().isoformat()}-lot-report.json"
    problems: list[str] = []
    payload = {**result, "reported_at": stamp.isoformat(), "required_fields": list(REQUIRED)}
    try:
        _state.write_json(out, payload)
    except OSError as exc:
        problems.append(f"could not write the report: {type(exc).__name__}: {exc}")
        _cli.say(args, f"  problem: {problems[-1]}")
    else:
        _cli.say(args, f"  written               {out}")

    _cli.emit(args, {"ok": not problems and not unpopulated, **payload,
                     "missing": [], "bare_rates": unpopulated, "notes": notes,
                     "report_path": str(out), "problems": problems})
    return _cli.OK


# ── selftest ─────────────────────────────────────────────────────────────────

def _call(*argv: str) -> tuple[int, str, str]:
    p = _cli.parser("selftest")
    extra(p)
    parsed = p.parse_args(list(argv))
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = _cli.run(main, None, parsed)
    return code, out.getvalue(), err.getvalue()


NOW = "2026-08-19T00:00:00+00:00"


def _pipeline(tmp: pathlib.Path, name: str, lot: int, seed_rate: float
              ) -> tuple[pathlib.Path, dict[str, object], dict[str, object]]:
    """Run the real lot_plan.py and blind_queue.py, so the report is assembled from
    what those two actually write rather than from a hand-made fixture."""
    import blind_queue
    import lot_plan

    root = tmp / name
    d = _state.state_dir(root, create=True)
    shutil.copy(FIXTURES / "warrant.valid.toml", d / "warrant.toml")
    seeds = json.loads((FIXTURES / "seeds.local.json").read_text())
    seeds["rate"] = seed_rate
    (d / "seeds.local.json").write_text(json.dumps(seeds))

    items = root / "items.jsonl"
    items.write_text("\n".join(json.dumps({
        "id": f"WEB-{6000 + i}", "surface": f"apps/web/app/s{i}/page.tsx",
        "state": "pass", "verdict": {"state": "pass"}}) for i in range(lot)) + "\n")

    # lot_plan.py refuses to size a sample over a suite nobody has measured, so
    # the fixture supplies the assay plane's result the way a real run would.
    _state.write_json(d / "suite-health.json", {"green": True, "score": 0.71})

    for module, argv in ((lot_plan, ["--root", str(root), "--lot", str(lot),
                                     "--lot-id", f"lot-{lot}", "--now", NOW]),
                         (blind_queue, ["--root", str(root), "--items", str(items),
                                        "--lot-id", f"lot-{lot}", "--now", NOW])):
        p = _cli.parser("fixture")
        module.extra(p)
        with contextlib.redirect_stdout(io.StringIO()), \
                contextlib.redirect_stderr(io.StringIO()):
            _cli.run(module.main, None, p.parse_args(argv))

    reports = d / "reports"
    plan = json.loads((reports / "2026-08-19-lot-plan.json").read_text())
    key = json.loads((reports / "2026-08-19-blind-queue.key.json").read_text())
    return root, plan, key


def _review(path: pathlib.Path, key: dict[str, object], positions: int,
            *, miss_seeds: int = 0, defects: list[int] | None = None,
            rung: str | None = None) -> None:
    seed_positions = {int(s["position"]) for s in key["seeds"]}
    missed = sorted(seed_positions)[:miss_seeds]
    defects = defects or []
    rows = []
    for position in range(1, positions + 1):
        if position in seed_positions:
            call = "clean" if position in missed else "defect"
        else:
            call = "defect" if position in defects else "clean"
        row = {"position": position, "call": call}
        if rung is not None:
            row["oracle"] = rung
        rows.append(row)
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n")


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="warrant-lot-report-"))
    try:
        root, plan, key = _pipeline(tmp, "repo", 194, 0.02)
        reports = _state.state_dir(root) / "reports"
        review = root / "review.jsonl"

        # Assembled from the real plan, key and review: a clean accept.
        _review(review, key, 60)
        code, out, _ = _call("--root", str(root), "--plan",
                             str(reports / "2026-08-19-lot-plan.json"),
                             "--key", str(reports / "2026-08-19-blind-queue.key.json"),
                             "--review", str(review), "--now", NOW)
        cases.append(("assembles a report from the plan, key and review", code == _cli.OK))
        cases.append(("the decision is to accept", "accept the lot" in out))
        cases.append(("all five fields are printed",
                      all(label in out for label in
                          ("population", "tolerable error rate", "sample size",
                           "seed recovery", "decision"))))
        cases.append(("the sample size carries its population", " of 194 items reviewed" in out))
        cases.append(("seed recovery is a count with its denominator",
                      "recovered of" in out and "seeded defects recovered" in out))
        written = json.loads((reports / "2026-08-19-lot-report.json").read_text())
        cases.append(("the report is written to .warrant/reports",
                      set(REQUIRED) <= set(written)))
        cases.append(("the report cites the warrant version",
                      written["warrant_version"] == "1"))
        cases.append(("no rate is printed without its population",
                      bare_rates(out.splitlines()) == []))

        # A missed seed overrides the accept.
        _review(review, key, 60, miss_seeds=1)
        code, out_miss, _ = _call("--root", str(root), "--plan",
                                  str(reports / "2026-08-19-lot-plan.json"),
                                  "--key", str(reports / "2026-08-19-blind-queue.key.json"),
                                  "--review", str(review), "--now", NOW)
        cases.append(("a missed seed blocks the accept",
                      code == _cli.OK and "escalate" in out_miss
                      and "missed 1 of 3" in out_miss))

        # Too few reviewed: extend rather than accept.
        _review(review, key, 20)
        code, out_short, _ = _call("--root", str(root), "--plan",
                                   str(reports / "2026-08-19-lot-plan.json"),
                                   "--key", str(reports / "2026-08-19-blind-queue.key.json"),
                                   "--review", str(review), "--now", NOW)
        cases.append(("a sample short of the rule says extend, and by how many",
                      code == _cli.OK and "extend" in out_short
                      and "draw " in out_short))

        # Errors found: the ladder raises the bar, then the census.
        _review(review, key, 60, defects=[2, 3, 4])
        code, out_err, _ = _call("--root", str(root), "--plan",
                                 str(reports / "2026-08-19-lot-plan.json"),
                                 "--key", str(reports / "2026-08-19-blind-queue.key.json"),
                                 "--review", str(review), "--now", NOW)
        cases.append(("errors found are counted against the reviewed set",
                      "reviewed items called defective" in out_err))
        _review(review, key, 80, defects=list(range(2, 24)))
        code, out_cen, _ = _call("--root", str(root), "--plan",
                                 str(reports / "2026-08-19-lot-plan.json"),
                                 "--key", str(reports / "2026-08-19-blind-queue.key.json"),
                                 "--review", str(review), "--now", NOW)
        cases.append(("the intolerable count escalates to a census",
                      "intolerable count" in out_cen and "census" in out_cen))

        # --result validates an assembled report, and fires on each of the five.
        valid = FIXTURES / "lot-result.valid.json"
        code, out_v, _ = _call("--root", str(root), "--result", str(valid), "--now", NOW)
        cases.append(("a complete result validates", code == _cli.OK))
        cases.append(("the oracle mix is rendered with its population",
                      "oracle mix" in out_v and "of 56 sampled" in out_v))

        # The rung the sample stands on, assembled rather than supplied.
        weak = tmp / "review-weak.jsonl"
        _review(weak, key, 60, rung="presence")
        code_w, out_w, _ = _call("--root", str(root),
                                 "--plan", str(reports / "2026-08-19-lot-plan.json"),
                                 "--key", str(reports / "2026-08-19-blind-queue.key.json"),
                                 "--review", str(weak), "--now", NOW)
        cases.append(("a sample of only weak rungs says what it did not audit",
                      "no case in this sample stands on an effect rung" in out_w))
        strong = tmp / "review-strong.jsonl"
        _review(strong, key, 60, rung="outcome")
        code_s, out_s, _ = _call("--root", str(root),
                                 "--plan", str(reports / "2026-08-19-lot-plan.json"),
                                 "--key", str(reports / "2026-08-19-blind-queue.key.json"),
                                 "--review", str(strong), "--now", NOW)
        cases.append(("a sample on an effect rung does not carry that warning",
                      "no case in this sample stands on an effect rung" not in out_s))
        norung = tmp / "review-norung.jsonl"
        _review(norung, key, 60)
        code_n, out_n, _ = _call("--root", str(root),
                                 "--plan", str(reports / "2026-08-19-lot-plan.json"),
                                 "--key", str(reports / "2026-08-19-blind-queue.key.json"),
                                 "--review", str(norung), "--now", NOW)
        cases.append(("a review row with no rung counts as unstated rather than "
                      "vanishing from the denominator",
                      "unstated" in out_n and code_n in (_cli.OK, _cli.FAILED)))

        for field in REQUIRED:
            broken = tmp / f"missing-{field}.json"
            payload = json.loads(valid.read_text())
            del payload[field]
            broken.write_text(json.dumps(payload))
            code, out_b, _ = _call("--root", str(root), "--result", str(broken),
                                   "--now", NOW)
            cases.append((f"a report with no {field} exits 2",
                          code == _cli.FAILED and f"{field} is absent" in out_b))
        for label, mutate in (
                ("population.size", lambda p: p["population"].pop("size")),
                ("a population size of zero", lambda p: p["population"].update(size=0)),
                ("a tolerable error rate of 1.0",
                 lambda p: p.update(tolerable_error_rate=1.0)),
                ("a sample size that is not a count",
                 lambda p: p.update(sample_size="fifty")),
                ("a seed_recovery with no numerator",
                 lambda p: p["seed_recovery"].pop("recovered")),
                ("a blank decision", lambda p: p.update(decision="   "))):
            broken = tmp / f"bad-{abs(hash(label))}.json"
            payload = json.loads(valid.read_text())
            mutate(payload)
            broken.write_text(json.dumps(payload))
            code, _, _ = _call("--root", str(root), "--result", str(broken), "--now", NOW)
            cases.append((f"{label} exits 2", code == _cli.FAILED))
        cases.append(("nothing is written when a report is invalid",
                      not (_state.state_dir(root) / "reports"
                           / "2026-08-19-lot-report.json").read_text().count("fifty")))

        # The bare-rate rule, both ways.
        cases.append(("bare_rates passes a rate with its population",
                      bare_rates(["  sample size  25.8% (50 of 194 items reviewed)"]) == []))
        cases.append(("bare_rates fires on a bare percentage",
                      bare_rates(["  seed recovery  75%"]) != []))

        # No seeds at all is reported as unmeasured rather than as full recovery.
        noseed_root, noseed_plan, noseed_key = _pipeline(tmp, "noseed", 194, 0.0)
        nreports = _state.state_dir(noseed_root) / "reports"
        nreview = noseed_root / "review.jsonl"
        _review(nreview, noseed_key, 60)
        code, out_ns, _ = _call("--root", str(noseed_root), "--plan",
                                str(nreports / "2026-08-19-lot-plan.json"),
                                "--key", str(nreports / "2026-08-19-blind-queue.key.json"),
                                "--review", str(nreview), "--now", NOW)
        cases.append(("no seeds is reported as unmeasured, not as recovery",
                      code == _cli.OK and "unmeasured" in out_ns))

        # A review row that says something else is counted nowhere and reported.
        odd = noseed_root / "odd.jsonl"
        odd.write_text(json.dumps({"position": 1, "call": "not sure"}) + "\n"
                       + json.dumps({"call": "clean"}) + "\n")
        code, out_odd, _ = _call("--root", str(noseed_root), "--plan",
                                 str(nreports / "2026-08-19-lot-plan.json"),
                                 "--key", str(nreports / "2026-08-19-blind-queue.key.json"),
                                 "--review", str(odd), "--now", NOW)
        cases.append(("an unrecognised call is not counted, and says so",
                      "is neither" in out_odd and "no position" in out_odd))

        # Usage and preconditions.
        code, out_u, _ = _call("--root", str(root), "--now", NOW)
        cases.append(("neither --result nor the three inputs exits 1", code == _cli.ERROR))
        code, _, _ = _call("--root", str(root), "--result", str(tmp / "nope.json"),
                           "--now", NOW)
        cases.append(("a result file that does not exist exits 3", code == _cli.MISSING))
        code, _, _ = _call("--root", str(root), "--plan", str(tmp / "nope.json"),
                           "--key", str(reports / "2026-08-19-blind-queue.key.json"),
                           "--review", str(review), "--now", NOW)
        cases.append(("a plan that does not exist exits 3", code == _cli.MISSING))
        notobj = tmp / "notobj.json"
        notobj.write_text("[1, 2]")
        code, _, _ = _call("--root", str(root), "--result", str(notobj), "--now", NOW)
        cases.append(("a result that is not an object exits 1", code == _cli.ERROR))

        code, o, e = _call("--root", str(root), "--result", str(valid), "--now", NOW,
                           "--json")
        payload = json.loads(o)
        cases.append(("--json puts only JSON on stdout", o.lstrip().startswith("{")))
        cases.append(("the JSON carries the five fields and no bare rate",
                      all(field in payload for field in REQUIRED)
                      and payload["bare_rates"] == []))
        cases.append(("--json keeps the report on stderr", "seed recovery" in e))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__ or "", main, selftest, extra))
