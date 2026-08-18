"""A Westgard multirule control chart over the regression corpus pass rate.

A single-threshold alarm on a true-negative-heavy queue either never fires or
fires constantly, which is why clinical laboratories stopped using one. The
multirule form asks several questions of the same series: is this run extreme, are
the last two extreme the same way, did the series jump, is it drifting, has it sat
on one side of the mean for long enough that "on target" has stopped being true.

Five rules, evaluated at the most recent run with the runs before it as context —
that is the decision point, and it is what makes "quiet" mean something:

  1-3s   the current run is more than 3 SD from the mean
  2-2s   the last two runs are both beyond 2 SD on the SAME side
  R-4s   the last two runs differ by more than 4 SD
  4-1s   the last four runs are all beyond 1 SD on the same side
  10-x   the last ten runs are all on the same side of the mean

Two-sided on purpose. A pass rate that jumps to 1.000 and stays there is as much a
signal as one that falls: it usually means the corpus stopped discriminating, and
a one-sided chart would call that health.

The SD floor is the one piece of arithmetic worth being explicit about. A corpus
sitting at exactly 1.000 for twenty runs has an SD of zero, and every rule then
divides by nothing or fires on the first imperfect run. `--sd-floor` puts a lower
bound under it and the output says when the bound was used, because a chart whose
sensitivity came from a floor rather than from the data should not be read as
though it came from the data.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import pathlib
import shutil
import statistics
import sys
import tempfile
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _cli import ERROR, FAILED, MISSING, OK, emit, entry, parser, say
from _cli import run as dispatch
from _state import Absent, read_jsonl, read_warrant
from feedback_record import FIXTURES
from regress_run import runs_path

_DESC = "Westgard multirule control chart over the regression corpus pass rate"

RULES = ("1-3s", "2-2s", "R-4s", "4-1s", "10-x")


def _side(z: float) -> int:
    return 1 if z > 0 else -1 if z < 0 else 0


def evaluate(series: list[float], mean: float, sd: float) -> list[dict[str, Any]]:
    """Every rule violated at the most recent point. Empty means in control."""
    if not series or sd <= 0:
        return []
    z = [(x - mean) / sd for x in series]
    out: list[dict[str, Any]] = []

    if abs(z[-1]) > 3:
        out.append({"rule": "1-3s", "z": round(z[-1], 3),
                    "detail": f"the current run is {z[-1]:+.2f} SD from the mean"})

    if len(z) >= 2 and abs(z[-1]) > 2 and abs(z[-2]) > 2 and _side(z[-1]) == _side(z[-2]):
        out.append({"rule": "2-2s", "z": [round(z[-2], 3), round(z[-1], 3)],
                    "detail": f"the last two runs are {z[-2]:+.2f} and {z[-1]:+.2f} SD out, "
                              "both on the same side"})

    if len(z) >= 2 and abs(z[-1] - z[-2]) > 4:
        out.append({"rule": "R-4s", "z": [round(z[-2], 3), round(z[-1], 3)],
                    "detail": f"the last two runs differ by {abs(z[-1] - z[-2]):.2f} SD"})

    if len(z) >= 4:
        window = z[-4:]
        if all(abs(v) > 1 for v in window) and len({_side(v) for v in window}) == 1:
            out.append({"rule": "4-1s", "z": [round(v, 3) for v in window],
                        "detail": "the last four runs are all beyond 1 SD on the same side"})

    if len(z) >= 10:
        window = z[-10:]
        sides = {_side(v) for v in window}
        if sides in ({1}, {-1}):
            out.append({"rule": "10-x", "z": [round(v, 3) for v in window],
                        "detail": "the last ten runs are all "
                                  f"{'above' if sides == {1} else 'below'} the mean"})
    return out


def load_series(root: str | pathlib.Path, field: str) -> list[float]:
    rows = read_jsonl(runs_path(root))
    if not rows:
        raise Absent(str(runs_path(root)))
    values = [r[field] for r in rows
              if isinstance(r.get(field), (int, float)) and not isinstance(r[field], bool)]
    return [float(v) for v in values]


def baseline(series: list[float], *, mean: float | None, sd: float | None,
             warrant: dict[str, Any] | None, window: int,
             sd_floor: float) -> dict[str, Any]:
    """(mean, sd) and where they came from. Declared beats computed, always.

    A computed baseline is taken from the runs BEFORE the current one. Including
    the run under test is what makes a control chart unable to see a collapse: the
    outlier widens the SD it is then compared against, and a pass rate falling
    from 1.000 to 0.980 reads as in control because it wrote its own limits.
    """
    block = (warrant or {}).get("westgard", {}) if isinstance(warrant, dict) else {}
    if mean is not None and sd is not None:
        source, n = "flags", len(series)
    elif isinstance(block.get("mean"), (int, float)) and isinstance(block.get("sd"), (int, float)):
        mean, sd, source, n = float(block["mean"]), float(block["sd"]), "warrant", len(series)
    else:
        head = series[:-1][:window]
        n = len(head)
        mean = statistics.fmean(head)
        sd = statistics.stdev(head) if len(head) >= 2 else 0.0
        source = f"the {n} run(s) before this one"

    floored = sd < sd_floor
    return {"mean": mean, "sd": max(sd, sd_floor), "declared_sd": sd,
            "sd_floored": floored, "sd_floor": sd_floor, "source": source, "n": n}


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--series", help="comma-separated values, instead of reading "
                                    ".warrant/regression-runs.jsonl")
    p.add_argument("--field", default="pass_rate", help="which field of each run row to chart")
    p.add_argument("--mean", type=float, help="declared baseline mean")
    p.add_argument("--sd", type=float, help="declared baseline SD; both flags or neither")
    p.add_argument("--baseline", type=int, default=10,
                   help="runs to compute the baseline from when none is declared (default 10)")
    p.add_argument("--sd-floor", type=float, default=0.005,
                   help="lower bound on the SD, so a corpus with no variance still charts "
                        "(default 0.005)")


def main(args: argparse.Namespace) -> int:
    if (args.mean is None) != (args.sd is None):
        say(args, "--mean and --sd go together: half a declared baseline is not one")
        return ERROR

    if args.series:
        try:
            series = [float(v) for v in args.series.replace(" ", "").split(",") if v]
        except ValueError as exc:
            say(args, f"--series is not a list of numbers: {exc}")
            return ERROR
    else:
        series = load_series(args.root, args.field)

    if len(series) < 5 and args.mean is None:
        say(args, f"{len(series)} run(s) in the series and no declared baseline: limits have to "
                  "come from the runs BEFORE the current one, and fewer than 4 of those is a "
                  "chart nobody should act on")
        emit(args, {"ok": False, "reason": "insufficient series", "runs": len(series)})
        return MISSING

    try:
        warrant: dict[str, Any] | None = read_warrant(args.root)
    except Absent:
        warrant = None

    base = baseline(series, mean=args.mean, sd=args.sd, warrant=warrant,
                    window=args.baseline, sd_floor=args.sd_floor)
    violations = evaluate(series, base["mean"], base["sd"])

    payload = {"ok": not violations, "runs": len(series), "series": series,
               "current": series[-1] if series else None,
               "baseline": base, "violations": violations,
               "rules_checked": list(RULES)}

    say(args, f"{len(series)} run(s), current {series[-1]:.4f}, baseline mean "
              f"{base['mean']:.4f} SD {base['sd']:.4f} (from {base['source']})")
    if base["sd_floored"]:
        say(args, f"note: the observed SD was {base['declared_sd']:.4f} and the floor "
                  f"{base['sd_floor']:.4f} was used instead; this chart's sensitivity comes "
                  "from the floor, not from the data")
    if not violations:
        say(args, f"in control: none of {', '.join(RULES)} fired")
        emit(args, payload)
        return OK

    for v in violations:
        say(args, f"VIOLATION {v['rule']}: {v['detail']}")
    say(args, f"{len(violations)} rule(s) violated: "
              f"{', '.join(v['rule'] for v in violations)}")
    emit(args, payload)
    return FAILED


def _parse(argv: list[str]) -> argparse.Namespace:
    p = parser(_DESC)
    _extra(p)
    return p.parse_args(argv)


def _run(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = dispatch(main, None, _parse(argv))
    return code, out.getvalue(), err.getvalue()


def _rules(series: list[float], mean: float = 0.95, sd: float = 0.01) -> set[str]:
    return {v["rule"] for v in evaluate(series, mean, sd)}


# Series built to trip exactly one rule, and near-misses built to trip none. Both
# halves are the point: a rule only ever seen passing has not been written, and a
# rule that fires on everything is not a rule.
FIRES: dict[str, list[float]] = {
    "1-3s": [0.953, 0.953, 0.936, 0.900],
    "2-2s": [0.952, 0.952, 0.925, 0.926],
    "R-4s": [0.950, 0.950, 0.972, 0.928],
    "4-1s": [0.955, 0.938, 0.937, 0.936, 0.935],
    "10-x": [0.955] * 10,
}
QUIET: dict[str, list[float]] = {
    "1-3s": [0.945, 0.921],                                  # 2.9 SD out, not 3
    "2-2s": [0.925, 0.931],                                  # only one of the two beyond 2 SD
    "R-4s": [0.972, 0.933],                                  # 3.9 SD apart, not 4
    "4-1s": [0.938, 0.937, 0.936, 0.941],                    # the newest is inside 1 SD
    "10-x": [0.955] * 4 + [0.945] + [0.955] * 5,             # one run on the other side
}
CLEAN = [0.955, 0.945] * 6


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []

    for rule in RULES:
        cases.append((f"{rule} fires on a series built to trip it",
                      _rules(FIRES[rule]) == {rule}))
    for rule in RULES:
        cases.append((f"{rule} stays quiet on a series built not to",
                      rule not in _rules(QUIET[rule])))
    cases.append(("an in-control series trips nothing at all", _rules(CLEAN) == set()))

    base = ["--json", "--mean", "0.95", "--sd", "0.01"]
    code, out, err = _run(base + ["--series", ",".join(str(v) for v in FIRES["1-3s"])])
    payload = json.loads(out)
    cases.append(("a violation exits 2", code == FAILED))
    cases.append(("the rule is named in the payload",
                  payload["violations"][0]["rule"] == "1-3s"))
    cases.append(("and in the human output", "VIOLATION 1-3s" in err))
    cases.append(("stdout under --json is only the JSON object", out.lstrip().startswith("{")))
    cases.append(("the rules it checked are listed",
                  payload["rules_checked"] == list(RULES)))

    code, out, err = _run(base + ["--series", ",".join(str(v) for v in CLEAN)])
    cases.append(("an in-control series exits 0", code == OK))
    cases.append(("and says which rules did not fire", "none of 1-3s" in err))

    code, out, _ = _run(base + ["--series", "0.95,0.95,0.972,0.928,0.90"])
    rules = {v["rule"] for v in json.loads(out)["violations"]}
    cases.append(("several rules can fire on one run", len(rules) >= 2))

    code, out, err = _run(["--json", "--series", "1.0,1.0,1.0,1.0,1.0,0.98"])
    payload = json.loads(out)
    cases.append(("a corpus with no variance still charts, via the floor",
                  payload["baseline"]["sd_floored"] and payload["baseline"]["sd"] == 0.005))
    cases.append(("and says the sensitivity came from the floor",
                  "comes from the floor" in err))
    cases.append(("a drop from a flat perfect corpus is a violation",
                  code == FAILED))

    cases.append(("--mean without --sd exits 1",
                  _run(["--series", "1,1,1,1", "--mean", "0.9"])[0] == ERROR))
    cases.append(("a --series that is not numbers exits 1",
                  _run(["--series", "0.9,banana"])[0] == ERROR))
    cases.append(("too short a series with no declared baseline exits 3",
                  _run(["--series", "0.9,0.95"])[0] == MISSING))
    cases.append(("but a declared baseline charts a short series",
                  _run(["--series", "0.9,0.95", "--mean", "0.95", "--sd", "0.01"])[0] == FAILED))

    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp) / ".warrant"
        d.mkdir(parents=True)
        cases.append(("no run series at all exits 3", _run(["--root", tmp])[0] == MISSING))

        shutil.copy(FIXTURES / "warrant.toml", d / "warrant.toml")
        with (d / "regression-runs.jsonl").open("w") as fh:
            for value in FIRES["4-1s"]:
                fh.write(json.dumps({"at": "2026-08-18T00:00:00+00:00", "cases": 5,
                                     "caught": 5, "pass_rate": value}) + "\n")
        code, out, _ = _run(["--root", tmp, "--json"])
        payload = json.loads(out)
        cases.append(("the series is read from the run log",
                      payload["runs"] == 5 and payload["current"] == 0.935))
        cases.append(("the baseline is taken from the warrant when it declares one",
                      payload["baseline"]["source"] == "warrant" and
                      payload["baseline"]["mean"] == 0.95))
        cases.append(("charting the run log fires the rule the series was built for",
                      code == FAILED and payload["violations"][0]["rule"] == "4-1s"))

        with (d / "regression-runs.jsonl").open("w") as fh:
            for value in CLEAN:
                fh.write(json.dumps({"pass_rate": value}) + "\n")
        cases.append(("an in-control run log exits 0", _run(["--root", tmp])[0] == OK))

    with tempfile.TemporaryDirectory() as tmp:
        # No warrant, no flags: the baseline comes from the head of the series.
        d = pathlib.Path(tmp) / ".warrant"
        d.mkdir(parents=True)
        with (d / "regression-runs.jsonl").open("w") as fh:
            for value in [0.98, 0.97, 0.98, 0.97, 0.98, 0.97, 0.60]:
                fh.write(json.dumps({"pass_rate": value}) + "\n")
        code, out, err = _run(["--root", tmp, "--json"])
        payload = json.loads(out)
        cases.append(("with nothing declared the baseline is computed from the head",
                      payload["baseline"]["source"].startswith("the 6 run(s) before")))
        cases.append(("a collapse against a computed baseline is a violation",
                      code == FAILED and "1-3s" in
                      {v["rule"] for v in payload["violations"]}))

    return cases


if __name__ == "__main__":
    raise SystemExit(entry(_DESC, main, selftest, _extra))
