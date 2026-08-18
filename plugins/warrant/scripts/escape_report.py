"""Counts, classes and trends over the escape corpus. No rate, ever.

Feedback gives a numerator with no denominator. You learn about the escapes
somebody noticed, and nothing in this file knows how many items went past
uninspected, so every percentage this script could compute would be a percentage
of the wrong population. C19 is the cautionary case: published proficiency-test
failure rates differ more than twentyfold by denominator — 1.4% of 670,489
challenges across 665 laboratories against 32.4% of lab-parameter results across
three — and both figures were correct. A reader given one of those without its
denominator has been misled by an accurate number.

So `--rate` exits 1 with that reason rather than printing something. The refusal
is the feature; a flag that quietly produced a number would make the limit
invisible again.

What it does emit: escapes per class, escapes per month, days since the last
escape in each class, and which of the warrant's classes have never had one. The
trend is a count in the last 90 days against the count in the 90 before it, which
is comparable to itself over time without pretending to be a rate.

"Never had an escape" needs a roster to be false about, and the roster is the
warrant's class list, so an absent warrant is exit 3 rather than a report with a
silently empty never-list.
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
from collections import Counter
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _cli import ERROR, FAILED, MISSING, OK, emit, entry, parser, say
from _cli import now as clock
from _cli import run as dispatch
from _state import Absent, read_jsonl, read_warrant, state_dir, write_json
from feedback_record import FIXTURES, escapes_path

_DESC = "Counts, classes and trends over .warrant/escapes.jsonl"

REFUSAL = ("this script will not print a rate: feedback yields a numerator with no "
           "denominator, because you only learn about the escapes somebody noticed. "
           "C19 — published proficiency-test failure rates differ more than twentyfold by "
           "denominator (1.4% of 670,489 challenges across 665 laboratories against 32.4% "
           "of lab-parameter results across three) and both were correct. Use the counts, "
           "the per-class series and the 90-day trend instead.")


def _when(row: dict[str, Any]) -> _dt.datetime | None:
    raw = row.get("reported_at")
    if not isinstance(raw, str):
        return None
    try:
        return _dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def _days(later: _dt.datetime, earlier: _dt.datetime) -> int:
    return int((later - earlier).total_seconds() // 86400)


def report(rows: list[dict[str, Any]], warrant_classes: list[str],
           when: _dt.datetime, months: int | None) -> dict[str, Any]:
    malformed = sum(1 for r in rows if "_malformed" in r)
    rows = [r for r in rows if "_malformed" not in r]
    undated = [r.get("escape_id") for r in rows if _when(r) is None]

    per_class = Counter(str(r.get("defect_class")) for r in rows)
    per_month: Counter[str] = Counter()
    last_seen: dict[str, _dt.datetime] = {}
    for r in rows:
        stamp = _when(r)
        if stamp is None:
            continue
        per_month[f"{stamp.year:04d}-{stamp.month:02d}"] += 1
        cls = str(r.get("defect_class"))
        if cls not in last_seen or stamp > last_seen[cls]:
            last_seen[cls] = stamp

    series = sorted(per_month.items())
    if months:
        series = series[-months:]

    recent_start = when - _dt.timedelta(days=90)
    previous_start = when - _dt.timedelta(days=180)
    recent = sum(1 for r in rows if (s := _when(r)) and s >= recent_start)
    previous = sum(1 for r in rows if (s := _when(r)) and previous_start <= s < recent_start)

    classes: dict[str, Any] = {}
    for cls in sorted(set(warrant_classes) | set(per_class)):
        stamp = last_seen.get(cls)
        classes[cls] = {
            "escapes": per_class.get(cls, 0),
            "last_escape": stamp.isoformat() if stamp else None,
            "days_since_last_escape": _days(when, stamp) if stamp else None,
            "in_warrant": cls in warrant_classes,
        }

    return {
        "at": when.isoformat(),
        "total_escapes": len(rows),
        "classes": classes,
        "per_class": dict(sorted(per_class.items())),
        "per_month": dict(series),
        "never_escaped": sorted(c for c in warrant_classes if not per_class.get(c)),
        "classes_outside_the_warrant": sorted(c for c in per_class if c not in warrant_classes),
        "trend": {
            "last_90_days": recent,
            "previous_90_days": previous,
            "direction": "more" if recent > previous else "fewer" if recent < previous else "unchanged",
            "counts_not_rates": True,
        },
        "malformed_rows": malformed,
        "undated_rows": undated,
        "rate": None,
        "rate_refused": REFUSAL,
    }


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--rate", action="store_true",
                   help="refused: see the reason this script prints instead")
    p.add_argument("--months", type=int, help="show only the most recent N months")
    p.add_argument("--report", action="store_true",
                   help="also write .warrant/reports/<date>-escapes.json")


def main(args: argparse.Namespace) -> int:
    if args.rate:
        say(args, REFUSAL)
        emit(args, {"ok": False, "rate": None, "rate_refused": REFUSAL})
        return ERROR

    try:
        warrant = read_warrant(args.root)
    except Absent as exc:
        say(args, f"no warrant at {exc}: the roster of defect classes lives there, and "
                  "'never had an escape' needs a roster to be false about")
        emit(args, {"ok": False, "reason": "no warrant"})
        return MISSING
    warrant_classes = [str(c.get("name")) for c in warrant.get("classes", []) if c.get("name")]

    rows = read_jsonl(escapes_path(args.root))
    when = clock(args)
    payload = report(rows, warrant_classes, when, args.months)

    errors: list[str] = []
    if args.report:
        try:
            state_dir(args.root, create=True)
            write_json(state_dir(args.root) / "reports"
                       / f"{when.date().isoformat()}-escapes.json", payload)
        except Exception as exc:                                   # noqa: BLE001
            errors.append(f"{type(exc).__name__}: {exc}")
    payload["record_errors"] = errors

    say(args, f"{payload['total_escapes']} escape(s) recorded across "
              f"{len(payload['per_class'])} class(es)")
    say(args, "by class:")
    for cls, block in payload["classes"].items():
        mark = "" if block["in_warrant"] else "  (not named in the warrant)"
        if block["escapes"]:
            say(args, f"  {cls:<24} {block['escapes']:>3}  last "
                      f"{block['last_escape'][:10]} ({block['days_since_last_escape']} days ago)"
                      f"{mark}")
        else:
            say(args, f"  {cls:<24} {block['escapes']:>3}  never{mark}")
    say(args, "by month:")
    for month, count in payload["per_month"].items():
        say(args, f"  {month}  {count:>3}  {'#' * count}")
    trend = payload["trend"]
    say(args, f"trend (counts, not rates): {trend['last_90_days']} in the last 90 days "
              f"against {trend['previous_90_days']} in the 90 before — {trend['direction']}")
    if payload["never_escaped"]:
        say(args, f"never had an escape: {', '.join(payload['never_escaped'])}")
    if payload["classes_outside_the_warrant"]:
        say(args, "escaped but not named in the warrant (so holding tier 0 by default): "
                  f"{', '.join(payload['classes_outside_the_warrant'])}")
    if payload["malformed_rows"]:
        say(args, f"{payload['malformed_rows']} malformed row(s) skipped")
    for e in errors:
        say(args, f"warning: the report ran but writing it failed — {e}")
    emit(args, payload)
    return OK


def _parse(argv: list[str]) -> argparse.Namespace:
    p = parser(_DESC)
    _extra(p)
    return p.parse_args(argv)


def _run(argv: list[str]) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = dispatch(main, None, _parse(argv))
    return code, out.getvalue(), err.getvalue()


def _seed(tmp: str, escapes: bool = True) -> pathlib.Path:
    d = pathlib.Path(tmp) / ".warrant"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(FIXTURES / "warrant.toml", d / "warrant.toml")
    if escapes:
        shutil.copy(FIXTURES / "escapes.jsonl", d / "escapes.jsonl")
    return d


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp)
        base = ["--root", tmp, "--json", "--now", "2026-08-18T00:00:00+00:00"]
        code, out, err = _run(base)
        payload = json.loads(out)
        cases.append(("the report exits 0", code == OK))
        cases.append(("stdout under --json is only the JSON object", out.lstrip().startswith("{")))
        cases.append(("escapes per class are counted",
                      payload["per_class"] == {"figure-lineage": 2, "layout-drift": 2,
                                               "tenant-leak": 1}))
        cases.append(("the total matches the sum of the classes",
                      payload["total_escapes"] == sum(payload["per_class"].values()) == 5))
        cases.append(("escapes per month are bucketed",
                      payload["per_month"] == {"2026-04": 1, "2026-05": 2, "2026-06": 2}))
        cases.append(("days since the last escape are measured against --now",
                      payload["classes"]["figure-lineage"]["days_since_last_escape"] == 106))
        cases.append(("a class the warrant names with no escape reads never",
                      payload["never_escaped"] == ["disclosure-content"]))
        cases.append(("its last escape is null rather than absent",
                      payload["classes"]["disclosure-content"]["last_escape"] is None))
        cases.append(("a class outside the warrant is named as such",
                      payload["classes_outside_the_warrant"] == ["tenant-leak"]))
        cases.append(("the trend is two counts and a direction",
                      payload["trend"]["last_90_days"] == 3 and
                      payload["trend"]["previous_90_days"] == 2 and
                      payload["trend"]["direction"] == "more"))
        cases.append(("the payload carries no rate", payload["rate"] is None))
        cases.append(("nothing in the human output is a percentage", "%" not in err))

        code, out, err = _run(base + ["--rate"])
        cases.append(("--rate exits 1", code == ERROR))
        cases.append(("and says why, with the C19 denominators",
                      "670,489" in err and "denominator" in err))
        cases.append(("and prints no number in place of one",
                      json.loads(out)["rate"] is None))

        code, out, _ = _run(base + ["--months", "2"])
        cases.append(("--months trims the series to the most recent",
                      list(json.loads(out)["per_month"]) == ["2026-05", "2026-06"]))

        code, out, _ = _run(base + ["--report"])
        cases.append(("--report writes a dated report",
                      (pathlib.Path(tmp) / ".warrant" / "reports"
                       / "2026-08-18-escapes.json").exists()))

    with tempfile.TemporaryDirectory() as tmp:
        d = _seed(tmp)
        (d / "escapes.jsonl").write_text(
            (FIXTURES / "escapes.jsonl").read_text() +
            (FIXTURES / "escapes-new.jsonl").read_text() + "{ not json\n")
        code, out, _ = _run(["--root", tmp, "--json", "--now", "2026-08-18T00:00:00+00:00"])
        payload = json.loads(out)
        cases.append(("a malformed row is counted, not fatal",
                      code == OK and payload["malformed_rows"] == 1))
        cases.append(("a newer escape moves the days-since figure",
                      payload["classes"]["figure-lineage"]["days_since_last_escape"] == 5))
        cases.append(("and the trend direction with it",
                      payload["trend"]["last_90_days"] == 4))

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp, escapes=False)
        code, out, err = _run(["--root", tmp, "--json", "--now", "2026-08-18T00:00:00+00:00"])
        payload = json.loads(out)
        cases.append(("no escapes recorded is a report, not an error",
                      code == OK and payload["total_escapes"] == 0))
        cases.append(("every class in the warrant then reads never",
                      payload["never_escaped"] == ["disclosure-content", "figure-lineage",
                                                   "layout-drift"]))
        cases.append(("and the trend is two zeros, not a divide",
                      payload["trend"] == {"last_90_days": 0, "previous_90_days": 0,
                                           "direction": "unchanged", "counts_not_rates": True}))

    with tempfile.TemporaryDirectory() as tmp:
        cases.append(("an absent warrant exits 3, not 0 with an empty never-list",
                      _run(["--root", tmp])[0] == MISSING))

    with tempfile.TemporaryDirectory() as tmp:
        d = _seed(tmp)
        (d / "reports").mkdir()
        (d / "reports" / "2026-08-18-escapes.json").mkdir()
        code, out, err = _run(["--root", tmp, "--json", "--report",
                               "--now", "2026-08-18T00:00:00+00:00"])
        cases.append(("a report-write failure does not lose the report",
                      code == OK and bool(json.loads(out)["record_errors"])))

    return cases


if __name__ == "__main__":
    raise SystemExit(entry(_DESC, main, selftest, _extra))
