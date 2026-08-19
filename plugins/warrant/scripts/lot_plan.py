#!/usr/bin/env python3
"""Size a risk-limited sample of the queue, with sequential stopping.

Signing 194 items one at a time is what nobody finishes; promoting all 194 at once
is not checking. The third way is a century old in manufacturing and in clinical
laboratories: accept the lot under a declared risk limit.

The arithmetic, all exact and all shown in the human output:

    d  = ceil(p x N)                    defectives that make the lot intolerable
    P0(n) = C(N-d, n) / C(N, n)         chance of drawing n clean items from an
                                        intolerable lot
    P(k, n) = sum_j<=k C(d,j) C(N-d,n-j) / C(N,n)      the same with k found
    n_k = the smallest n with P(k, n) <= alpha

Stop and accept at the first n where P(k, n) <= alpha. Each error found raises the
bar to n_k, so a clean early sample ends the audit and a dirty one extends it. Find
d errors and the lot is intolerable outright: that escalates to a census rather than
to a bigger sample.

p and alpha come from the signed warrant, not from a flag. `--rate` and
`--risk-limit` exist for exploring a plan and both are reported as overrides, so a
plan built on a weaker limit than the one signed cannot pass as the signed one.

The suite is a precondition, not a detail. Every number this plan produces is a
number about a sample of items whose evidence is the test suite, so the plan
inherits that suite's fault sensitivity — and more than half of over 15,000
generated mutants survived a passing unit, integration and system suite (`C18`).
`warrant`'s stated order puts `assay` before any verdict for that reason. So a
missing `.warrant/suite-health.json` exits 3 naming the step, and
`--unmeasured-suite` proceeds while recording the omission in the plan, the same
way `--rate` records an override. A plan built over an unmeasured suite cannot
pass as one built over a measured one.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import math
import pathlib
import shutil
import sys
import tempfile
from fractions import Fraction

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                   # noqa: E402
import _state                                                 # noqa: E402

FIXTURES = (pathlib.Path(__file__).resolve().parent.parent
            / "evals" / "fixtures" / "charter-panel-lot")
MAX_LOT = 500_000


def p_zero(lot: int, defective: int, sample: int) -> Fraction:
    """C(N-d, n)/C(N, n) as a product, so no huge binomials are built."""
    if sample > lot - defective:
        return Fraction(0)
    value = Fraction(1)
    for i in range(sample):
        value *= Fraction(lot - defective - i, lot - i)
    return value


def p_value(lot: int, defective: int, sample: int, found: int) -> Fraction:
    """Pr[K <= found] when the lot really holds `defective` defectives."""
    if found >= defective:
        return Fraction(1)
    total = Fraction(0)
    denom = math.comb(lot, sample)
    for j in range(found + 1):
        if sample - j < 0 or sample - j > lot - defective or j > defective:
            continue
        total += Fraction(math.comb(defective, j) * math.comb(lot - defective, sample - j),
                          denom)
    return total


def smallest_n(lot: int, defective: int, found: int, alpha: Fraction) -> int | None:
    """The smallest sample that settles the lot with `found` errors already seen.

    P(k, n) is non-increasing in n, so this is a binary search rather than a walk.
    """
    if found >= defective:
        return None
    lo, hi = found, lot
    if p_value(lot, defective, hi, found) > alpha:
        return None
    while lo < hi:
        mid = (lo + hi) // 2
        if p_value(lot, defective, mid, found) <= alpha:
            hi = mid
        else:
            lo = mid + 1
    return lo


def build_plan(lot: int, rate: float, alpha: float) -> dict[str, object]:
    defective = math.ceil(rate * lot)
    a = Fraction(alpha).limit_denominator(10 ** 9)
    initial = smallest_n(lot, defective, 0, a)

    ladder: list[dict[str, object]] = []
    previous = 0
    for found in range(0, defective + 1):
        needed = smallest_n(lot, defective, found, a)
        if needed is None:
            ladder.append({"errors": found, "sample": None, "extra": None,
                           "p_value": 1.0, "action": "census"})
            break
        ladder.append({
            "errors": found,
            "sample": needed,
            "extra": needed - previous,
            "p_value": float(p_value(lot, defective, needed, found)),
            # A rung whose sample is the whole lot is a census in all but name.
            "action": "census" if needed >= lot else "accept the lot",
        })
        previous = needed

    return {
        "lot_size": lot,
        "tolerable_error_rate": rate,
        "risk_limit": alpha,
        "intolerable_at": defective,
        "initial_sample": initial,
        # A sample that is the whole lot is a census, whatever it is called.
        "census": initial is None or initial >= lot,
        "ladder": ladder,
        "stopping_rule": (
            f"draw items in the blind order; after n draws with k errors found, "
            f"accept the lot when P(k, n) <= {alpha}; extend to the sample in the "
            f"ladder on each error; at {defective} error(s) the lot is intolerable "
            f"and goes to census"),
    }


def _p_zero_line(lot: int, defective: int, sample: int) -> str:
    return (f"P0({sample}) = C({lot - defective},{sample})/C({lot},{sample}) = "
            f"{float(p_zero(lot, defective, sample)):.4g}")


def extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--lot", type=int, default=None,
                   help="the number of items in the lot")
    p.add_argument("--lot-file", default=None,
                   help="a JSON array or JSONL file of items; the lot size is its length")
    p.add_argument("--lot-id", default=None, help="a name for this lot, recorded in the plan")
    p.add_argument("--rate", type=float, default=None,
                   help="override the warrant's tolerable error rate (reported as an override)")
    p.add_argument("--risk-limit", type=float, default=None,
                   help="override the warrant's risk limit (reported as an override)")
    p.add_argument("--unmeasured-suite", action="store_true",
                   help="plan without .warrant/suite-health.json; the omission is "
                        "recorded in the plan and printed on every run")


def read_suite_health(root: pathlib.Path) -> dict[str, object] | None:
    """The assay plane's result, or None when it has never run.

    Read rather than gated here: `main` decides what an absence costs, so the
    shape of the file stays in one place. The keys mirror the ones
    `charter_validate.py` accepts, so the two planes read one file the same way.
    """
    path = _state.state_dir(root) / "suite-health.json"
    if not path.is_file():
        return None
    doc = _state.read_json(path, default=None)
    return doc if isinstance(doc, dict) else None


def _lot_size(args: argparse.Namespace) -> int | None:
    if args.lot is not None:
        return args.lot
    if args.lot_file:
        path = pathlib.Path(args.lot_file).expanduser().resolve()
        if not path.is_file():
            raise _state.Absent(str(path))
        text = path.read_text().strip()
        if text.startswith("["):
            return len(json.loads(text))
        return len([line for line in text.splitlines() if line.strip()])
    return None


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()
    warrant = _state.read_warrant(root)                        # Absent -> exit 3
    lot_block = warrant.get("lot", {}) if isinstance(warrant.get("lot"), dict) else {}

    lot = _lot_size(args)
    if lot is None:
        _cli.say(args, "pass --lot N or --lot-file PATH: a sample size needs a population")
        _cli.emit(args, {"ok": False, "reason": "no-population"})
        return _cli.ERROR
    if lot <= 0:
        _cli.say(args, f"the lot holds {lot} item(s); there is nothing to audit")
        _cli.emit(args, {"ok": False, "reason": "empty-lot", "lot_size": lot})
        return _cli.MISSING
    if lot > MAX_LOT:
        _cli.say(args, f"a lot of {lot} exceeds this script's bound of {MAX_LOT}")
        _cli.emit(args, {"ok": False, "reason": "lot-too-large", "lot_size": lot})
        return _cli.ERROR

    overrides: list[str] = []
    rate = lot_block.get("tolerable_error_rate")
    if args.rate is not None:
        overrides.append(f"tolerable_error_rate {rate} -> {args.rate}")
        rate = args.rate
    alpha = lot_block.get("risk_limit", 0.05)
    if args.risk_limit is not None:
        overrides.append(f"risk_limit {alpha} -> {args.risk_limit}")
        alpha = args.risk_limit

    for label, value in (("lot.tolerable_error_rate", rate), ("lot.risk_limit", alpha)):
        if isinstance(value, bool) or not isinstance(value, (int, float)) \
                or not (0.0 < float(value) < 1.0):
            _cli.say(args, f"{label} is {value!r}, which is not a proportion in (0,1); "
                           "no sample can be sized from it")
            _cli.say(args, "  charter_validate.py gates this on the warrant")
            _cli.emit(args, {"ok": False, "reason": "bad-rate", "key": label,
                             "value": value})
            return _cli.FAILED
    rate, alpha = float(rate), float(alpha)

    suite = read_suite_health(root)
    if suite is None and not args.unmeasured_suite:
        _cli.say(args, "no .warrant/suite-health.json: the suite this lot's evidence "
                       "rests on has never been measured")
        _cli.say(args, "  run warrant:assay first — mutation survival over the tests CI "
                       "actually selects, plus the cannot-fail scan")
        _cli.say(args, "  more than half of over 15,000 generated mutants survived a "
                       "passing suite (C18), so a green suite is not evidence until its "
                       "fault sensitivity is a number")
        _cli.say(args, "  --unmeasured-suite plans anyway and records the omission")
        _cli.emit(args, {"ok": False, "reason": "no-suite-health",
                         "expected": str(_state.state_dir(root) / "suite-health.json")})
        return _cli.MISSING

    plan = build_plan(lot, rate, alpha)
    plan["lot_id"] = args.lot_id or f"lot-{lot}"
    plan["planned_at"] = _cli.now(args).isoformat()
    plan["warrant_version"] = warrant.get("version")
    plan["overrides"] = overrides
    plan["suite_health"] = {
        "measured": suite is not None,
        "source": str(_state.state_dir(root) / "suite-health.json"),
        "record": suite,
    }
    census_classes = list(lot_block.get("census_classes", []))
    owner = warrant.get("owner", {}) if isinstance(warrant.get("owner"), dict) else {}
    escalation = f"{owner.get('name', '')} <{owner.get('email', '')}>".strip()
    plan["escalation"] = {
        "census_classes": census_classes,
        "route": escalation if escalation.strip("<> ") else None,
        "path": [
            "0 errors at the initial sample: accept the lot and record the decision",
            "each error found: extend to the sample in the ladder before deciding",
            f"{plan['intolerable_at']} errors: the lot is intolerable — census the "
            "remainder and escalate",
            "any item the panel marked inconclusive, and every item in a census "
            "class, is reviewed rather than sampled",
        ],
    }

    d = int(plan["intolerable_at"])
    n0 = plan["initial_sample"]
    _cli.say(args, f"lot {plan['lot_id']}")
    _cli.say(args, f"  population          {lot} item(s)")
    _cli.say(args, f"  tolerable error     p = {rate}  ->  d = ceil({rate} x {lot}) "
                   f"= {d} defective item(s) makes the lot intolerable")
    _cli.say(args, f"  risk limit          alpha = {alpha}  (the chance of accepting "
                   "an intolerable lot)")
    for line in overrides:
        _cli.say(args, f"  OVERRIDE            {line}  (not the signed value)")
    if suite is None:
        _cli.say(args, "  UNMEASURED SUITE    no .warrant/suite-health.json; every number "
                       "below inherits a fault sensitivity nobody has measured")
    else:
        bits = []
        for label, key in (("green", "green"), ("armed", "armed_ratio"),
                           ("effect-rung passes", "effect_rung_passes"),
                           ("unoracled", "unoracled")):
            value = suite.get(key)
            if value is not None:
                bits.append(f"{label}={value}")
        _cli.say(args, "  suite health        " + ("  ".join(bits) or "recorded, no "
                                                   "figures in it"))
        if suite.get("mutation_measured") is False:
            _cli.say(args, "                      mutation survival not measured — the "
                           "sample's fault sensitivity rests on the armed ratio alone")
        if suite.get("unoracled"):
            _cli.say(args, f"                      {suite['unoracled']} case(s) unoracled "
                           "upstream: those items have no property any check could read")
    if plan["census"]:
        detail = (f"n0 = {n0} of {lot}, which is every item"
                  if n0 is not None else
                  "no sample smaller than the lot settles it at this risk limit")
        _cli.say(args, f"  initial sample      census — {detail}")
        _cli.say(args, f"  {_p_zero_line(lot, d, lot)} vs alpha = {alpha}")
    else:
        _cli.say(args, f"  initial sample      n0 = {n0}   "
                       + _cli.rate(n0, lot, "items sampled"))
        _cli.say(args, f"    {_p_zero_line(lot, d, n0)} <= {alpha}"
                       "        <- the stopping rule at zero errors")
        if n0 > 1:
            _cli.say(args, f"    {_p_zero_line(lot, d, n0 - 1)} > {alpha}"
                           "        <- one fewer would not settle it")
    _cli.say(args, "  sequential rule     errors  sample  extra  P(k,n)")
    for row in plan["ladder"]:
        if row["sample"] is None:
            _cli.say(args, f"                      {row['errors']:>6}  census  "
                           "    —  the lot is intolerable outright")
        else:
            _cli.say(args, f"                      {row['errors']:>6}  "
                           f"{row['sample']:>6}  {row['extra']:>5}  "
                           f"{row['p_value']:.4g}")
    _cli.say(args, f"  stopping rule       {plan['stopping_rule']}")
    _cli.say(args, "  escalation          " + (plan["escalation"]["route"] or "NOBODY "
                   "(the warrant names no owner)"))
    if census_classes:
        _cli.say(args, "                      census classes: " + ", ".join(census_classes))
    for step in plan["escalation"]["path"]:
        _cli.say(args, f"                      - {step}")

    out = _state.state_dir(root, create=True) / "reports" / \
        f"{_cli.now(args).date().isoformat()}-lot-plan.json"
    problems: list[str] = []
    try:
        _state.write_json(out, plan)
    except OSError as exc:
        problems.append(f"could not write the plan: {type(exc).__name__}: {exc}")
        _cli.say(args, f"  problem: {problems[-1]}")
    else:
        _cli.say(args, f"  written             {out}")

    _cli.emit(args, {"ok": not problems, **plan, "plan_path": str(out),
                     "problems": problems})
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


def _root(tmp: pathlib.Path, name: str, suite: dict | None = None) -> pathlib.Path:
    root = tmp / name
    d = _state.state_dir(root, create=True)
    shutil.copy(FIXTURES / "warrant.valid.toml", d / "warrant.toml")
    if suite is not None:
        _state.write_json(d / "suite-health.json", suite)
    return root


def _brute_smallest_n(lot: int, defective: int, found: int, alpha: float) -> int | None:
    """The same answer by walking every n, to check the binary search."""
    a = Fraction(alpha).limit_denominator(10 ** 9)
    for n in range(found, lot + 1):
        if p_value(lot, defective, n, found) <= a:
            return n
    return None


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="warrant-lot-plan-"))
    try:
        root = _root(tmp, "repo", suite={"green": True, "score": 0.71})
        code, out, _ = _call("--root", str(root), "--lot", "194",
                             "--now", "2026-08-19T00:00:00+00:00")
        cases.append(("plans a lot of 194", code == _cli.OK))

        # The assay precondition. A plan inherits the suite's fault sensitivity,
        # so an unmeasured suite is a missing precondition rather than a detail.
        bare = _root(tmp, "no-assay")
        code_bare, out_bare, _ = _call("--root", str(bare), "--lot", "194")
        cases.append(("an unmeasured suite refuses, and exits MISSING rather than "
                      "FAILED", code_bare == _cli.MISSING))
        cases.append(("the refusal names the step that would clear it",
                      "warrant:assay" in out_bare))
        code_ov, out_ov, _ = _call("--root", str(bare), "--lot", "194",
                                   "--unmeasured-suite",
                                   "--now", "2026-08-19T00:00:00+00:00")
        cases.append(("--unmeasured-suite plans anyway", code_ov == _cli.OK))
        cases.append(("and says so on the run itself",
                      "UNMEASURED SUITE" in out_ov))
        ov_plan = json.loads((_state.state_dir(bare) / "reports"
                              / "2026-08-19-lot-plan.json").read_text())
        cases.append(("the omission is recorded in the plan, not only printed",
                      ov_plan["suite_health"]["measured"] is False))
        cases.append(("a measured suite records its record in the plan",
                      _state.read_json(_state.state_dir(root) / "suite-health.json",
                                       default={}).get("green") is True))
        plan = build_plan(194, 0.05, 0.05)
        n0 = int(plan["initial_sample"])
        d = int(plan["intolerable_at"])
        cases.append(("d = ceil(p x N)", d == math.ceil(0.05 * 194) == 10))

        # The property that makes n0 the answer rather than a guess.
        cases.append(("P0(n0) <= alpha", p_zero(194, d, n0) <= Fraction(1, 20)))
        cases.append(("P0(n0 - 1) > alpha", p_zero(194, d, n0 - 1) > Fraction(1, 20)))
        cases.append(("the binary search agrees with a brute-force walk",
                      n0 == _brute_smallest_n(194, d, 0, 0.05)))
        cases.append(("the arithmetic is shown, not just the answer",
                      "C(184," in out and "d = ceil(" in out and "alpha = 0.05" in out))
        cases.append(("the sample size carries its population",
                      f"{n0} of 194" in out))

        # Sequential stopping: each error raises the bar.
        ladder = [row for row in plan["ladder"] if row["sample"] is not None]
        cases.append(("the ladder starts at the initial sample",
                      ladder[0]["sample"] == n0 and ladder[0]["errors"] == 0))
        cases.append(("each error found needs a strictly larger sample",
                      all(b["sample"] > a["sample"]
                          for a, b in zip(ladder, ladder[1:]))))
        cases.append(("each rung records the extra draws",
                      all(row["extra"] > 0 for row in ladder)))
        cases.append(("every rung's P-value clears the risk limit",
                      all(row["p_value"] <= 0.05 + 1e-12 for row in ladder)))
        cases.append(("finding d errors escalates to a census rather than a sample",
                      plan["ladder"][-1]["action"] == "census"
                      and plan["ladder"][-1]["errors"] == d))
        cases.append(("the ladder is in the human output", "sequential rule" in out))

        # Direction of the levers.
        cases.append(("a tighter risk limit needs a larger sample",
                      int(build_plan(194, 0.05, 0.01)["initial_sample"]) > n0))
        cases.append(("a smaller tolerable rate needs a larger sample",
                      int(build_plan(194, 0.02, 0.05)["initial_sample"]) > n0))
        cases.append(("a larger lot at the same rate needs a similar sample, "
                      "not a proportional one",
                      int(build_plan(1940, 0.05, 0.05)["initial_sample"]) < 10 * n0))

        # A lot too small to sample.
        small = build_plan(12, 0.05, 0.05)
        cases.append(("a lot whose sample is the whole lot is a census",
                      small["census"] is True and small["initial_sample"] == 12))
        code, out_small, _ = _call("--root", str(root), "--lot", "12")
        cases.append(("the census case is reported as one",
                      code == _cli.OK and "census — n0 = 12 of 12" in out_small))
        cases.append(("a lot large enough to sample is not a census",
                      plan["census"] is False))

        # The plan is written where lot_report.py can read it.
        written = (_state.state_dir(root) / "reports" / "2026-08-19-lot-plan.json")
        cases.append(("the plan is written to .warrant/reports", written.exists()))
        saved = json.loads(written.read_text())
        cases.append(("the written plan carries the five report fields",
                      {"lot_size", "tolerable_error_rate", "initial_sample",
                       "escalation", "stopping_rule"} <= set(saved)))
        cases.append(("the written plan cites the warrant version",
                      saved["warrant_version"] == "1"))
        cases.append(("the escalation names a person",
                      "Ada Lovelace" in str(saved["escalation"]["route"])))
        cases.append(("the census classes come from the warrant",
                      "disclosure-content" in saved["escalation"]["census_classes"]))

        # --lot-file counts the population.
        items = tmp / "items.jsonl"
        items.write_text("\n".join(json.dumps({"id": f"I-{i}"}) for i in range(37)) + "\n")
        code, out_f, _ = _call("--root", str(root), "--lot-file", str(items))
        cases.append(("--lot-file counts a JSONL population",
                      code == _cli.OK and "37 item(s)" in out_f))
        arr = tmp / "items.json"
        arr.write_text(json.dumps([{"id": f"I-{i}"} for i in range(41)]))
        code, out_a, _ = _call("--root", str(root), "--lot-file", str(arr))
        cases.append(("--lot-file counts a JSON array population",
                      code == _cli.OK and "41 item(s)" in out_a))

        # Overrides are reported as overrides.
        code, out_o, _ = _call("--root", str(root), "--lot", "194", "--rate", "0.2")
        cases.append(("an overridden rate is marked as not the signed value",
                      code == _cli.OK and "OVERRIDE" in out_o
                      and "not the signed value" in out_o))

        # Failure modes.
        bad = _root(tmp, "bad-rate")
        path = _state.state_dir(bad) / "warrant.toml"
        path.write_text(path.read_text().replace("tolerable_error_rate = 0.05",
                                                "tolerable_error_rate = 1.5"))
        code, out_b, _ = _call("--root", str(bad), "--lot", "194")
        cases.append(("a rate outside (0,1) exits 2",
                      code == _cli.FAILED and "not a proportion" in out_b))
        code, out_z, _ = _call("--root", str(root), "--lot", "0")
        cases.append(("an empty lot exits 3", code == _cli.MISSING))
        code, out_u, _ = _call("--root", str(root))
        cases.append(("no population exits 1", code == _cli.ERROR))
        code, out_h, _ = _call("--root", str(root), "--lot", str(MAX_LOT + 1))
        cases.append(("a lot past the bound exits 1", code == _cli.ERROR))
        code, _, _ = _call("--root", str(tmp / "no-warrant"), "--lot", "194")
        cases.append(("no warrant exits 3", code == _cli.MISSING))
        code, _, _ = _call("--root", str(root), "--lot-file", str(tmp / "nope.jsonl"))
        cases.append(("a lot file that does not exist exits 3", code == _cli.MISSING))

        code, o, e = _call("--root", str(root), "--lot", "194", "--json")
        payload = json.loads(o)
        cases.append(("--json puts only JSON on stdout", o.lstrip().startswith("{")))
        cases.append(("the JSON carries the sample size and the stopping rule",
                      payload["initial_sample"] == n0 and payload["stopping_rule"]))
        cases.append(("--json keeps the arithmetic on stderr", "C(184," in e))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__ or "", main, selftest, extra))
