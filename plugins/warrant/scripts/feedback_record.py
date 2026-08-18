"""Record one escape: a case where the pipeline was wrong and the owner said so.

This is what replaced the prospective reader study. A study measures one model
version on one date; an escape corpus re-measures every version against every
mistake ever found, and it grows. What it cannot do is produce a rate, because
you only learn about the escapes somebody noticed — see escape_report.py, which
refuses to print one.

The row records the evidence digest the wrong verdict was written from. That is
the field that makes an escape reproducible rather than anecdotal: without it a
regression case is a description of a mistake, and with it the case can be
re-run against the same inputs. It also records the model id and version live in
each lane at the time, which is what the ratchet compares a later calibration
against — a lane whose model has moved has changed the control.

The escape id is derived from the class, item, digest and description rather than
allocated, so reporting the same escape twice is a no-op instead of two rows in
an append-only file.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import os
import pathlib
import sys
import tempfile
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import _schema
from _cli import ERROR, FAILED, MISSING, OK, emit, entry, parser, say
from _cli import run as dispatch
from _cli import now as clock
from _state import Absent, append_jsonl, read_jsonl, read_lanes, read_warrant, state_dir, tier_of

_DESC = "Record one escape in .warrant/escapes.jsonl"

PLUGIN_ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_PATH = PLUGIN_ROOT / "schemas" / "escape.schema.json"
FIXTURES = PLUGIN_ROOT / "evals" / "fixtures" / "feedback-ratchet-ledger"


def escapes_path(root: str | pathlib.Path) -> pathlib.Path:
    return state_dir(root) / "escapes.jsonl"


def schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text())


def escape_id(when: Any, defect_class: str, item: str, digest: str, missed: str) -> str:
    """Deterministic, so the same report twice is the same escape twice."""
    seed = "\x1f".join([defect_class, item, digest, missed.strip()])
    short = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:8]
    return f"esc-{when.strftime('%Y%m%d')}-{short}"


def parse_model(spec: str) -> dict[str, str]:
    """`lane=model_id@version`. The id may contain slashes and dots; the version
    is whatever follows the last @, so `google/gemini-3.1-pro@2026-06-15` parses."""
    if "=" not in spec:
        raise ValueError(f"expected lane=model_id@version, got {spec!r}")
    lane, rest = spec.split("=", 1)
    if "@" not in rest:
        raise ValueError(f"{spec!r} pins no version; a lane without one cannot be compared later")
    model_id, version = rest.rsplit("@", 1)
    for name, value in (("lane", lane), ("model_id", model_id), ("version", version)):
        if not value.strip():
            raise ValueError(f"{spec!r} has an empty {name}")
    return {"lane": lane.strip(), "model_id": model_id.strip(), "version": version.strip()}


def lanes_as_models(root: str | pathlib.Path) -> list[dict[str, str]]:
    """The live lanes, in the shape the escape row stores them."""
    from ledger import _lane_blocks
    blocks = _lane_blocks(read_lanes(root))
    return [{"lane": role, "model_id": mid, "version": ver}
            for role, (mid, ver) in sorted(blocks.items())]


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--class", dest="defect_class", help="the warrant's name for the class (required)")
    p.add_argument("--item", help="the item the wrong verdict was written about (required)")
    p.add_argument("--missed", help="what was missed, in enough detail to assert on (required)")
    p.add_argument("--evidence-digest", help="digest of the snapshot the wrong verdict "
                                             "was written from (required)")
    p.add_argument("--kind", default="missed_defect",
                   help="missed_defect or outcome_mismatch")
    p.add_argument("--expected-verdict", help="pass, fail or inconclusive; regress_build "
                                              "defaults to fail")
    p.add_argument("--severity", help="low, medium or high")
    p.add_argument("--warrant-version", help="defaults to the warrant's version")
    p.add_argument("--model", action="append", default=[], metavar="LANE=ID@VERSION",
                   help="repeatable; defaults to every lane in lanes.toml")
    p.add_argument("--tier-at-time", type=int, help="defaults to the tier the warrant "
                                                   "currently gives the class")
    p.add_argument("--verdict-id", help="ledger row hash of the wrong verdict")
    p.add_argument("--note")


def main(args: argparse.Namespace) -> int:
    missing = [flag for flag, value in (("--class", args.defect_class), ("--item", args.item),
                                        ("--missed", args.missed),
                                        ("--evidence-digest", args.evidence_digest))
               if not value]
    if missing:
        say(args, f"required and absent: {', '.join(missing)}")
        return ERROR

    models: list[dict[str, str]] = []
    try:
        for spec in args.model:
            models.append(parse_model(spec))
    except ValueError as exc:
        say(args, f"--model: {exc}")
        return ERROR

    warrant: dict[str, Any] | None = None
    try:
        warrant = read_warrant(args.root)
    except Absent:
        warrant = None

    if not models:
        try:
            models = lanes_as_models(args.root)
        except Absent as exc:
            say(args, f"no --model given and no lanes to read: {exc}")
            return MISSING
    if not models:
        say(args, "lanes.toml declares no lanes; pass --model instead")
        return MISSING

    warrant_version = args.warrant_version or (warrant or {}).get("version")
    if not warrant_version:
        say(args, "no --warrant-version given and no warrant to read it from")
        return MISSING

    when = clock(args)
    row: dict[str, Any] = {
        "escape_id": escape_id(when, args.defect_class, args.item,
                               args.evidence_digest, args.missed),
        "kind": args.kind,
        "defect_class": args.defect_class,
        "item": args.item,
        "missed": args.missed,
        "warrant_version": str(warrant_version),
        "models": models,
        "evidence_digest": args.evidence_digest,
        "reported_at": when.isoformat(),
    }
    tier = args.tier_at_time
    if tier is None and warrant is not None:
        tier = tier_of(warrant, args.defect_class)
    if tier is not None:
        row["tier_at_time"] = tier
    for key, value in (("severity", args.severity), ("verdict_id", args.verdict_id),
                       ("expected_verdict", args.expected_verdict), ("notes", args.note)):
        if value:
            row[key] = value

    violations = _schema.validate(row, schema())
    if violations:
        say(args, f"the escape does not validate against {SCHEMA_PATH.name}:")
        for v in violations:
            say(args, f"  {v}")
        emit(args, {"recorded": False, "violations": violations, "escape": row})
        return FAILED

    path = escapes_path(args.root)
    existing = {r.get("escape_id") for r in read_jsonl(path)}
    if row["escape_id"] in existing:
        say(args, f"{row['escape_id']} is already recorded; appending nothing")
        emit(args, {"recorded": False, "duplicate": True, "escape_id": row["escape_id"],
                    "escape": row})
        return OK

    state_dir(args.root, create=True)
    append_jsonl(path, row)

    # Recorded. Reporting failures below are logged, not raised.
    try:
        say(args, f"{row['escape_id']} recorded: {row['defect_class']} / {row['item']} "
                  f"({row['kind']}, tier {row.get('tier_at_time', '?')} at the time)")
        emit(args, {"recorded": True, "duplicate": False, "escape_id": row["escape_id"],
                    "escape": row, "escapes": str(path)})
    except Exception as exc:                                       # noqa: BLE001
        print(f"{row['escape_id']} was recorded; reporting it failed: "
              f"{type(exc).__name__}: {exc}", file=sys.stderr)
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


def _seed(tmp: str) -> str:
    import shutil
    d = pathlib.Path(tmp) / ".warrant"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(FIXTURES / "warrant.toml", d / "warrant.toml")
    shutil.copy(FIXTURES / "lanes.toml", d / "lanes.toml")
    return tmp


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    good = ["--class", "figure-lineage", "--item", "WEB-5042",
            "--missed", "Dividend per share tied to no record in the disclosure it names.",
            "--evidence-digest", "a" * 64, "--now", "2026-08-18T04:00:00+00:00"]

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp)
        base = ["--root", tmp, "--json"]
        code, out, _ = _run(base + good)
        payload = json.loads(out)
        cases.append(("a valid escape records and exits 0", code == OK and payload["recorded"]))
        cases.append(("stdout under --json is only the JSON object", out.lstrip().startswith("{")))
        cases.append(("models default to every lane in lanes.toml",
                      [m["lane"] for m in payload["escape"]["models"]] == ["grader", "lens-mock"]))
        cases.append(("warrant version is taken from the warrant",
                      payload["escape"]["warrant_version"] == "1.4.0"))
        cases.append(("tier at the time is taken from the warrant",
                      payload["escape"]["tier_at_time"] == 2))
        first_id = payload["escape_id"]

        code, out, _ = _run(base + good)
        again = json.loads(out)
        cases.append(("the id is deterministic", again["escape_id"] == first_id))
        cases.append(("a duplicate report appends nothing",
                      code == OK and again["duplicate"] and
                      len(read_jsonl(escapes_path(tmp))) == 1))

        code, out, _ = _run(base + good + ["--item", "WEB-5043"])
        cases.append(("a different item is a different escape",
                      json.loads(out)["escape_id"] != first_id and
                      len(read_jsonl(escapes_path(tmp))) == 2))

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp)
        base = ["--root", tmp, "--json"]
        code, out, err = _run(base + good + ["--evidence-digest", "short"])
        cases.append(("a digest too short to identify a snapshot exits 2", code == FAILED))
        cases.append(("the violation names evidence_digest",
                      any("evidence_digest" in v for v in json.loads(out)["violations"])))
        cases.append(("a rejected escape is not appended",
                      read_jsonl(escapes_path(tmp)) == []))

        code, out, _ = _run(base + good + ["--kind", "nearly_missed"])
        cases.append(("an unknown kind exits 2 against the schema enum",
                      code == FAILED and any("is not one of" in v
                                             for v in json.loads(out)["violations"])))
        code, out, _ = _run(base + good + ["--severity", "catastrophic"])
        cases.append(("an unknown severity exits 2", code == FAILED))
        code, out, _ = _run(base + good + ["--tier-at-time", "9"])
        cases.append(("a tier above the ladder exits 2", code == FAILED))
        code, out, _ = _run(base + good + ["--missed", "short"])
        cases.append(("a description too thin to assert on exits 2", code == FAILED))

        cases.append(("a missing --class exits 1, not 2",
                      _run(base + ["--item", "X", "--missed", "a description here",
                                   "--evidence-digest", "a" * 64])[0] == ERROR))
        cases.append(("a missing --evidence-digest exits 1",
                      _run(base + ["--class", "c", "--item", "X",
                                   "--missed", "a description here"])[0] == ERROR))
        cases.append(("an unparseable --model exits 1",
                      _run(base + good + ["--model", "grader-without-a-version"])[0] == ERROR))
        cases.append(("a --model with no version exits 1",
                      _run(base + good + ["--model", "grader=some/model"])[0] == ERROR))

    with tempfile.TemporaryDirectory() as tmp:
        base = ["--root", tmp, "--json"]
        cases.append(("no warrant and no lanes exits 3, not 1",
                      _run(base + good)[0] == MISSING))
        code, out, _ = _run(base + good + ["--warrant-version", "1.4.0",
                                           "--model", "grader=anthropic/claude-opus-4.8@2026-07-01"])
        cases.append(("explicit version and model record without a warrant", code == OK))
        cases.append(("tier at the time is omitted when nothing knows it",
                      "tier_at_time" not in json.loads(out)["escape"]))

    fixture_rows = read_jsonl(FIXTURES / "escapes.jsonl") + read_jsonl(FIXTURES / "escapes-new.jsonl")
    bad = [(r.get("escape_id"), _schema.validate(r, schema())) for r in fixture_rows]
    cases.append((f"all {len(fixture_rows)} fixture escapes validate against the schema",
                  all(not v for _, v in bad)))
    cases.append(("the schema rejects an escape with no models at all",
                  bool(_schema.validate({**fixture_rows[0], "models": []}, schema()))))
    return cases


if __name__ == "__main__":
    raise SystemExit(entry(_DESC, main, selftest, _extra))
