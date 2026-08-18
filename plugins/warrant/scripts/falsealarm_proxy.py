"""Flag probable false rejections from ledger churn, without a human reviewing one.

A missed defect gets reported. A wrongly-failed good item does not: nobody
escalates a pass they had to work for, so false rejections stay invisible and
their cost reads as the pipeline working. This script recovers part of that from
the only trace they leave — an item that failed, was resubmitted, and passed.

Substantive change is decided by the evidence digest, because that is the one
field that says whether the second submission was actually a different artefact:

  strong    the fail and the following pass carry the SAME evidence digest, so
            the pipeline returned two different verdicts on identical evidence.
            One of them is wrong and the pass is the one nobody complained about.
  weak      the digest differs, but the pass followed inside the churn window, so
            the resubmission is unlikely to contain a substantive change. This
            reads a clock, not the change, and is the weaker half on purpose.

What this is not: a false-rejection rate. There is no denominator — the number of
good items the pipeline wrongly failed is exactly the quantity nobody measured,
and a percentage over the churn candidates would divide by the wrong population.
C19 is the cautionary case: published proficiency-test failure rates differ more
than twentyfold by denominator and both figures were correct. So this exits 0 with
a candidate list, and the list says on its face that it came from a proxy.
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

from _cli import ERROR, FAILED, MISSING, OK, emit, entry, parser, say
from _cli import now as clock
from _cli import run as dispatch
from _state import read_jsonl, state_dir, write_json
from feedback_record import FIXTURES
from ledger import ledger_path

_DESC = "Flag fail/resubmit/pass churn as a probable false rejection"

DISCLAIMER = ("these are candidates from a churn proxy, not measured false rejections: "
              "no rate is emitted because the population of good items wrongly failed is "
              "the quantity nobody measured")


def _when(row: dict[str, Any]) -> _dt.datetime | None:
    raw = row.get("at")
    if not isinstance(raw, str):
        return None
    try:
        return _dt.datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def candidates(rows: list[dict[str, Any]], window_minutes: float) -> list[dict[str, Any]]:
    """Every fail followed by a pass on the same item, classified by digest."""
    by_item: dict[str, list[tuple[int, dict[str, Any]]]] = {}
    for position, row in enumerate(rows):
        item = row.get("item")
        if isinstance(item, str):
            by_item.setdefault(item, []).append((position, row))

    found: list[dict[str, Any]] = []
    for item, entries in by_item.items():
        entries.sort(key=lambda e: (e[1].get("index", e[0]), e[0]))
        for offset, (position, row) in enumerate(entries):
            if row.get("verdict") != "fail":
                continue
            follow = next(((p, r) for p, r in entries[offset + 1:]
                           if r.get("verdict") == "pass"), None)
            if follow is None:
                continue
            pass_position, pass_row = follow
            fail_digest = row.get("evidence_digest")
            pass_digest = pass_row.get("evidence_digest")
            fail_at, pass_at = _when(row), _when(pass_row)
            elapsed = ((pass_at - fail_at).total_seconds() / 60.0
                       if fail_at and pass_at else None)

            same = bool(fail_digest) and fail_digest == pass_digest
            if same:
                strength, why = "strong", ("the same evidence digest was failed and then "
                                           "passed, so the evidence did not change")
            elif elapsed is not None and elapsed <= window_minutes:
                strength, why = "weak", (f"the evidence changed but the pass followed "
                                         f"{elapsed:.0f} min later, inside the "
                                         f"{window_minutes:g} min churn window")
            else:
                continue

            found.append({
                "item": item,
                "strength": strength,
                "why": why,
                "fail_row": row.get("index", position),
                "pass_row": pass_row.get("index", pass_position),
                "fail_digest": fail_digest,
                "pass_digest": pass_digest,
                "same_digest": same,
                "elapsed_minutes": round(elapsed, 2) if elapsed is not None else None,
                "authorising_tier": row.get("tier"),
            })
    found.sort(key=lambda c: (c["strength"] != "strong", c["fail_row"]))
    return found


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--ledger", help="path to a ledger file; defaults to .warrant/ledger.jsonl")
    p.add_argument("--window-minutes", type=float, default=30.0,
                   help="a pass this soon after a fail is churn even when the digest moved "
                        "(default 30)")
    p.add_argument("--strong-only", action="store_true",
                   help="only report same-digest candidates")
    p.add_argument("--report", action="store_true",
                   help="also write .warrant/reports/<date>-falsealarm.json")


def main(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.ledger) if args.ledger else ledger_path(args.root)
    if not path.exists():
        say(args, f"no ledger at {path}")
        emit(args, {"ok": False, "reason": "no ledger", "ledger": str(path)})
        return MISSING

    rows = [r for r in read_jsonl(path) if "_malformed" not in r]
    found = candidates(rows, args.window_minutes)
    if args.strong_only:
        found = [c for c in found if c["strength"] == "strong"]

    when = clock(args)
    payload = {
        "candidates": found,
        "counts": {"strong": sum(1 for c in found if c["strength"] == "strong"),
                   "weak": sum(1 for c in found if c["strength"] == "weak"),
                   "total": len(found)},
        "ledger_rows": len(rows),
        "items_seen": len({r.get("item") for r in rows if isinstance(r.get("item"), str)}),
        "window_minutes": args.window_minutes,
        "is_measurement": False,
        "rate": None,
        "disclaimer": DISCLAIMER,
        "at": when.isoformat(),
    }

    errors: list[str] = []
    if args.report:
        try:
            state_dir(args.root, create=True)
            write_json(state_dir(args.root) / "reports"
                       / f"{when.date().isoformat()}-falsealarm.json", payload)
        except Exception as exc:                                   # noqa: BLE001
            errors.append(f"{type(exc).__name__}: {exc}")
    payload["record_errors"] = errors

    say(args, f"{len(found)} churn candidate(s) over {payload['ledger_rows']} ledger row(s), "
              f"{payload['items_seen']} item(s): "
              f"{payload['counts']['strong']} strong, {payload['counts']['weak']} weak")
    say(args, DISCLAIMER)
    for c in found:
        say(args, f"  {c['strength'].upper():<6} {c['item']}  rows {c['fail_row']}->"
                  f"{c['pass_row']}  {c['why']}")
    for e in errors:
        say(args, f"warning: the scan ran but writing the report failed — {e}")
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


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    churn = str(FIXTURES / "ledger-churn.jsonl")

    code, out, err = _run(["--ledger", churn, "--json"])
    payload = json.loads(out)
    by_item = {c["item"]: c for c in payload["candidates"]}
    cases.append(("the scan exits 0 even with candidates found", code == OK))
    cases.append(("stdout under --json is only the JSON object", out.lstrip().startswith("{")))
    cases.append(("a fail then a pass on the SAME digest is strong",
                  by_item.get("WEB-5100", {}).get("strength") == "strong"))
    cases.append(("a different digest inside the window is weak",
                  by_item.get("WEB-5101", {}).get("strength") == "weak"))
    cases.append(("a different digest outside the window is not a candidate",
                  "WEB-5102" not in by_item))
    cases.append(("a fail with no later pass is not a candidate", "WEB-5103" not in by_item))
    cases.append(("a pass with no fail is not a candidate", "WEB-5104" not in by_item))
    cases.append(("a pass BEFORE the fail does not count as a resubmission",
                  "WEB-5105" not in by_item))
    cases.append(("an intervening inconclusive does not break the pairing",
                  by_item.get("WEB-5106", {}).get("strength") == "strong"))
    cases.append(("the pairing names both rows",
                  by_item["WEB-5100"]["fail_row"] == 2 and by_item["WEB-5100"]["pass_row"] == 3))
    cases.append(("strong candidates sort first",
                  payload["candidates"][0]["strength"] == "strong"))
    cases.append(("the counts add up",
                  payload["counts"]["total"] ==
                  payload["counts"]["strong"] + payload["counts"]["weak"] == 3))

    cases.append(("no rate is emitted", payload["rate"] is None))
    cases.append(("the payload says it is not a measurement",
                  payload["is_measurement"] is False))
    cases.append(("the human output carries the disclaimer", DISCLAIMER in err))

    code, out, _ = _run(["--ledger", churn, "--json", "--window-minutes", "1"])
    cases.append(("shrinking the window drops the weak candidate",
                  json.loads(out)["counts"]["weak"] == 0))
    code, out, _ = _run(["--ledger", churn, "--json", "--window-minutes", "600"])
    cases.append(("widening it past the slow resubmission picks that one up",
                  json.loads(out)["counts"]["weak"] == 2))
    code, out, _ = _run(["--ledger", churn, "--json", "--strong-only"])
    cases.append(("--strong-only reports same-digest candidates alone",
                  json.loads(out)["counts"] == {"strong": 2, "weak": 0, "total": 2}))

    with tempfile.TemporaryDirectory() as tmp:
        cases.append(("an absent ledger exits 3, not 2", _run(["--root", tmp])[0] == MISSING))
        d = pathlib.Path(tmp) / ".warrant"
        d.mkdir(parents=True)
        (d / "ledger.jsonl").write_text("")
        code, out, _ = _run(["--root", tmp, "--json"])
        cases.append(("an empty ledger reports zero candidates, not an error",
                      code == OK and json.loads(out)["counts"]["total"] == 0))

    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp) / ".warrant"
        d.mkdir(parents=True)
        shutil.copy(churn, d / "ledger.jsonl")
        (d / "ledger.jsonl").open("a").write("{ not json\n")
        code, out, _ = _run(["--root", tmp, "--json"])
        cases.append(("a malformed row is skipped rather than fatal",
                      code == OK and json.loads(out)["counts"]["total"] == 3))
        code, out, _ = _run(["--root", tmp, "--json", "--report",
                             "--now", "2026-08-18T08:00:00+00:00"])
        cases.append(("--report writes a dated report",
                      (d / "reports" / "2026-08-18-falsealarm.json").exists()))

    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp) / ".warrant"
        (d / "reports").mkdir(parents=True)
        shutil.copy(churn, d / "ledger.jsonl")
        (d / "reports" / "2026-08-18-falsealarm.json").mkdir()
        code, out, err = _run(["--root", tmp, "--json", "--report",
                               "--now", "2026-08-18T08:00:00+00:00"])
        cases.append(("a report-write failure does not lose the scan",
                      code == OK and bool(json.loads(out)["record_errors"])))

    return cases


if __name__ == "__main__":
    raise SystemExit(entry(_DESC, main, selftest, _extra))
