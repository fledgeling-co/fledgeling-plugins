"""Re-run every historical escape against a verdict source.

This is the plugin's self-validation and the tier-2 entry condition: a class may
only be closed by machine while the machine demonstrably catches everything it
has previously missed in that class. Exits 2 naming every case that is no longer
caught.

The verdict source is a command, given by `--verdict-cmd`, that receives a case
directory and prints a verdict JSON on stdout. So this script never calls a
model, which is what lets it sit in a gate: the thing deciding whether the
pipeline still works is not the pipeline.

A case counts as caught only when the returned verdict matches the one the case
says should have been returned AND names the defect class. Both halves are
needed. "Something is wrong here" on an item that is wrong for a different reason
is not the pipeline catching the escape; it is the pipeline being right by
accident, and a corpus that accepts it stops discriminating.

Four ways a case comes back not caught, all recorded with their reason rather
than collapsed into a bare count: the wrong verdict, the right verdict without
the class, a verdict source that exited non-zero or timed out, and output that is
not a verdict at all. The last is deliberately a failure of the check rather than
an error of the script — a source that cannot say what it found has not caught
anything, and treating it as an infrastructure problem is how a broken grader
reads as a passing corpus.

Writes three things, and none of them is the corpus: `regression-result.json`
(the latest run, which the ratchet reads), a row on `regression-runs.jsonl` (the
pass-rate series, which westgard.py charts) and a dated report.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import pathlib
import shlex
import shutil
import subprocess
import sys
import tempfile
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _cli import ERROR, FAILED, MISSING, OK, emit, entry, parser, rate, say
from _cli import run as dispatch
from _cli import now as clock
from _state import Absent, append_jsonl, read_json, state_dir, write_json
from feedback_record import FIXTURES
from regress_build import case_dir, regression_dir

_DESC = "Re-run every historical escape against a verdict source"


def result_path(root: str | pathlib.Path) -> pathlib.Path:
    return state_dir(root) / "regression-result.json"


def runs_path(root: str | pathlib.Path) -> pathlib.Path:
    return state_dir(root) / "regression-runs.jsonl"


def load_cases(root: str | pathlib.Path) -> list[dict[str, Any]]:
    base = regression_dir(root)
    if not base.exists():
        raise Absent(str(base))
    cases = []
    for d in sorted(p for p in base.iterdir() if p.is_dir()):
        f = d / "case.json"
        if f.exists():
            case = read_json(f)
            case["_dir"] = str(d)
            cases.append(case)
    return cases


def named_classes(verdict: dict[str, Any]) -> set[str]:
    """Every class the verdict names, in any of the shapes a lane may emit."""
    found: set[str] = set()
    single = verdict.get("defect_class")
    if isinstance(single, str):
        found.add(single)
    for key in ("classes", "defect_classes"):
        value = verdict.get(key)
        if isinstance(value, list):
            found.update(str(v) for v in value if isinstance(v, str))
    defects = verdict.get("defects")
    if isinstance(defects, list):
        for d in defects:
            if isinstance(d, dict):
                for key in ("class", "defect_class"):
                    if isinstance(d.get(key), str):
                        found.add(d[key])
    return found


def judge(case: dict[str, Any], verdict: dict[str, Any]) -> tuple[bool, str]:
    """(caught, reason). The reason is written for the not-caught line."""
    expected = case.get("expected_verdict", {})
    want = expected.get("verdict", "fail")
    got = verdict.get("verdict")
    if got != want:
        return False, f"returned {got!r}, the case expects {want!r}"
    must = [c for c in expected.get("must_mention", []) if c]
    if must:
        named = named_classes(verdict)
        absent = [c for c in must if c not in named]
        if absent:
            return False, (f"returned {got!r} but named {sorted(named) or 'no class'}, "
                           f"not {absent}")
    return True, f"returned {got!r} and named the class"


def run_case(case: dict[str, Any], template: str, timeout: float) -> dict[str, Any]:
    tokens = shlex.split(template)
    if any("{case}" in t for t in tokens):
        argv = [t.replace("{case}", case["_dir"]) for t in tokens]
    else:
        argv = tokens + [case["_dir"]]

    row: dict[str, Any] = {"case_id": case.get("case_id"),
                           "defect_class": case.get("defect_class"),
                           "item": case.get("item"),
                           "expected": case.get("expected_verdict", {}).get("verdict")}
    try:
        proc = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        row.update(caught=False, reason=f"the verdict source did not answer in {timeout:g}s",
                   verdict=None)
        return row
    except OSError as exc:
        row.update(caught=False, reason=f"the verdict source could not be run: {exc}",
                   verdict=None)
        return row

    if proc.returncode != 0:
        row.update(caught=False, verdict=None,
                   reason=f"the verdict source exited {proc.returncode}: "
                          f"{(proc.stderr or '').strip()[:200]}")
        return row
    try:
        verdict = json.loads(proc.stdout)
    except json.JSONDecodeError:
        row.update(caught=False, verdict=None,
                   reason="the verdict source printed no parseable verdict: "
                          f"{(proc.stdout or '').strip()[:120]!r}")
        return row
    if not isinstance(verdict, dict):
        row.update(caught=False, verdict=None,
                   reason=f"the verdict is a {type(verdict).__name__}, not an object")
        return row

    caught, reason = judge(case, verdict)
    row.update(caught=caught, reason=reason, verdict=verdict.get("verdict"))
    return row


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--verdict-cmd", help="command that receives a case directory and prints a "
                                         "verdict JSON; {case} is substituted, or the directory "
                                         "is appended (required)")
    p.add_argument("--class", dest="defect_class", action="append", default=[],
                   help="repeatable; only run cases in these classes")
    p.add_argument("--case", action="append", default=[], help="repeatable; only these case ids")
    p.add_argument("--timeout", type=float, default=120.0, help="seconds per case")
    p.add_argument("--no-record", action="store_true",
                   help="do not write the result, the run series or the report")


def main(args: argparse.Namespace) -> int:
    if not args.verdict_cmd:
        say(args, "--verdict-cmd is required: this script never calls a model itself")
        return ERROR

    cases = load_cases(args.root)
    if args.defect_class:
        cases = [c for c in cases if c.get("defect_class") in args.defect_class]
    if args.case:
        cases = [c for c in cases if c.get("case_id") in args.case]
    if not cases:
        say(args, f"no regression cases under {regression_dir(args.root)}"
                  + (" matching that filter" if (args.defect_class or args.case) else ""))
        emit(args, {"ok": False, "reason": "no cases", "cases": 0})
        return MISSING

    results = [run_case(c, args.verdict_cmd, args.timeout) for c in cases]
    not_caught = [r for r in results if not r["caught"]]
    when = clock(args)

    by_class: dict[str, dict[str, Any]] = {}
    for r in results:
        block = by_class.setdefault(str(r["defect_class"]),
                                    {"cases": 0, "caught": 0, "not_caught": []})
        block["cases"] += 1
        if r["caught"]:
            block["caught"] += 1
        else:
            block["not_caught"].append(r["case_id"])

    payload = {
        "ok": not not_caught,
        "at": when.isoformat(),
        "cases": len(results),
        "caught": len(results) - len(not_caught),
        "pass_rate": round((len(results) - len(not_caught)) / len(results), 6),
        "not_caught": [r["case_id"] for r in not_caught],
        "by_class": by_class,
        "results": results,
        "verdict_cmd": args.verdict_cmd,
    }

    # The verdict source has already run. Everything from here is recording, so a
    # failure is logged and reported rather than raised.
    errors: list[str] = []
    if not args.no_record:
        for write, label in (
            (lambda: write_json(result_path(args.root), {k: v for k, v in payload.items()
                                                         if k != "results"}), "regression-result.json"),
            (lambda: append_jsonl(runs_path(args.root),
                                  {"at": payload["at"], "cases": payload["cases"],
                                   "caught": payload["caught"],
                                   "pass_rate": payload["pass_rate"],
                                   "not_caught": payload["not_caught"]}), "regression-runs.jsonl"),
            (lambda: write_json(state_dir(args.root) / "reports"
                                / f"{when.date().isoformat()}-regression.json", payload), "the report"),
        ):
            try:
                state_dir(args.root, create=True)
                write()
            except Exception as exc:                               # noqa: BLE001
                errors.append(f"{label}: {type(exc).__name__}: {exc}")
    payload["record_errors"] = errors

    for r in results:
        if not r["caught"]:
            say(args, f"NOT CAUGHT  {r['case_id']}  [{r['defect_class']}]  {r['item']}  "
                      f"— {r['reason']}")
    say(args, rate(payload["caught"], payload["cases"], "historical escapes re-caught"))
    for e in errors:
        say(args, f"warning: the run happened but recording it failed — {e}")
    emit(args, payload)

    if not_caught:
        say(args, f"{len(not_caught)} case(s) no longer caught: "
                  f"{', '.join(payload['not_caught'])}")
        return FAILED
    return OK


def _parse(argv: list[str]) -> argparse.Namespace:
    p = parser(_DESC)
    _extra(p)
    return p.parse_args(argv)


def _run(argv: list[str]) -> tuple[int, str, str]:
    """Run one invocation through the real dispatcher, so the selftest observes
    the exit code a caller would see rather than the one main() returns."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = dispatch(main, None, _parse(argv))
    return code, out.getvalue(), err.getvalue()


def _source(mode: str, *extra: str) -> str:
    parts = [shlex.quote(sys.executable), shlex.quote(str(FIXTURES / "verdict_source.py")),
             "--mode", mode, *extra, "{case}"]
    return " ".join(parts)


def _corpus(tmp: str) -> None:
    """Build the corpus the way the pipeline does: record, then build."""
    import regress_build
    d = pathlib.Path(tmp) / ".warrant"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(FIXTURES / "warrant.toml", d / "warrant.toml")
    shutil.copy(FIXTURES / "lanes.toml", d / "lanes.toml")
    shutil.copy(FIXTURES / "escapes.jsonl", d / "escapes.jsonl")
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        regress_build.main(regress_build._parse(["--root", tmp, "--all"]))


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    missed = "esc-20260411-1a2b3c4d"

    with tempfile.TemporaryDirectory() as tmp:
        _corpus(tmp)
        base = ["--root", tmp, "--json", "--now", "2026-08-18T07:00:00+00:00"]

        code, out, _ = _run(base + ["--verdict-cmd", _source("catch")])
        payload = json.loads(out)
        cases.append(("a source that catches every case exits 0", code == OK))
        cases.append(("the pass rate is 1.0 over 5 cases",
                      payload["pass_rate"] == 1.0 and payload["cases"] == 5))
        cases.append(("stdout under --json is only the JSON object", out.lstrip().startswith("{")))
        cases.append(("the result the ratchet reads is written",
                      read_json(result_path(tmp))["ok"] is True))
        cases.append(("the run joins the pass-rate series westgard charts",
                      len(runs_path(tmp).read_text().splitlines()) == 1))

        code, out, err = _run(base + ["--verdict-cmd", _source("miss", "--miss-case", missed)])
        payload = json.loads(out)
        cases.append(("one case no longer caught exits 2", code == FAILED))
        cases.append(("it names the case", payload["not_caught"] == [missed]))
        cases.append(("the human line names it too", missed in err))
        cases.append(("the reason says what came back instead",
                      "expects 'fail'" in payload["results"][0]["reason"]))
        cases.append(("the rate it prints carries its denominator",
                      "4 of 5" in err))
        cases.append(("per-class rollup marks only the failing class",
                      payload["by_class"]["figure-lineage"]["not_caught"] == [missed]))
        cases.append(("the failing run joins the series too",
                      len(runs_path(tmp).read_text().splitlines()) == 2))

        code, out, _ = _run(base + ["--verdict-cmd", _source("miss")])
        cases.append(("every case missed names every case",
                      code == FAILED and len(json.loads(out)["not_caught"]) == 5))

        code, out, _ = _run(base + ["--verdict-cmd", _source("unnamed")])
        payload = json.loads(out)
        cases.append(("the right verdict without the class is not caught", code == FAILED))
        cases.append(("and the reason says the class was not named",
                      "not ['figure-lineage']" in payload["results"][0]["reason"]))

        code, out, _ = _run(base + ["--verdict-cmd", _source("garbage")])
        cases.append(("unparseable output is a failed check, not an error",
                      code == FAILED and
                      "no parseable verdict" in json.loads(out)["results"][0]["reason"]))

        code, out, _ = _run(base + ["--verdict-cmd", _source("crash")])
        cases.append(("a verdict source that exits non-zero is not caught",
                      code == FAILED and "exited 3" in json.loads(out)["results"][0]["reason"]))

        code, out, _ = _run(base + ["--verdict-cmd", "/nonexistent/grader {case}"])
        cases.append(("a verdict source that cannot be run is not caught",
                      code == FAILED and
                      "could not be run" in json.loads(out)["results"][0]["reason"]))

        code, out, _ = _run(base + ["--verdict-cmd", _source("slow"), "--timeout", "1"])
        cases.append(("a source that never answers is not caught",
                      code == FAILED and
                      "did not answer" in json.loads(out)["results"][0]["reason"]))

        code, out, _ = _run(base + ["--verdict-cmd", _source("catch"),
                                    "--class", "layout-drift"])
        cases.append(("--class narrows the run", json.loads(out)["cases"] == 2))
        code, out, _ = _run(base + ["--verdict-cmd", _source("catch"), "--case", missed])
        cases.append(("--case narrows the run to one", json.loads(out)["cases"] == 1))
        cases.append(("a filter that matches nothing exits 3",
                      _run(base + ["--verdict-cmd", _source("catch"),
                                   "--class", "no-such-class"])[0] == MISSING))

        no_brace = " ".join([shlex.quote(sys.executable),
                             shlex.quote(str(FIXTURES / "verdict_source.py")), "--mode", "catch"])
        cases.append(("a command without {case} gets the directory appended",
                      _run(base + ["--verdict-cmd", no_brace])[0] == OK))

        cases.append(("--verdict-cmd is required", _run(["--root", tmp])[0] == ERROR))

    with tempfile.TemporaryDirectory() as tmp:
        cases.append(("an absent corpus exits 3, not 2",
                      _run(["--root", tmp, "--verdict-cmd", _source("catch")])[0] == MISSING))

    with tempfile.TemporaryDirectory() as tmp:
        _corpus(tmp)
        # The run happened; a recording failure must not lose that.
        (state_dir(tmp) / "regression-result.json").mkdir()
        code, out, err = _run(["--root", tmp, "--json",
                               "--verdict-cmd", _source("catch")])
        payload = json.loads(out)
        cases.append(("a recording failure does not raise", code == OK))
        cases.append(("and is reported against the run that already happened",
                      bool(payload["record_errors"]) and "recording it failed" in err))

    return cases


if __name__ == "__main__":
    raise SystemExit(entry(_DESC, main, selftest, _extra))
