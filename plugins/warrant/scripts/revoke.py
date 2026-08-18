"""Drop one defect class to tier 0, with the reason written down.

Never silently: the reason is required, and it lands in the warrant next to the
trigger and the timestamp, plus a ledger row. A class that lost its authority
without a record of why is a class somebody will quietly restore.

The warrant is edited as TEXT rather than re-serialised. The contract keeps TOML
writing deliberately narrow — charter_init.py emits a fixed schema it fully
controls and nothing else serialises to TOML — and a revocation has to preserve a
document a person signed, comments and key order included. So this rewrites the
`tier` line inside the one `[[classes]]` block whose `name` matches, upserts three
keys beside it, and leaves every other byte alone. The edit is parsed with
tomllib BEFORE it replaces the original, so a text edit that would have produced
an unreadable warrant leaves the warrant it could not parse untouched.

Ordering matters for the same reason it does in ledger.py: the warrant is written
first, and if the ledger append then fails it is logged rather than raised. The
authority is already gone at that point, and raising invites a retry that revokes
twice and appends twice.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import pathlib
import re
import shutil
import sys
import tempfile
import tomllib
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _cli import ERROR, FAILED, MISSING, OK, emit, entry, parser, say
from _cli import now as clock
from _cli import run as dispatch
from _state import Absent, read_warrant, tier_of, toml_kv, warrant_path
from feedback_record import FIXTURES

_DESC = "Drop one defect class to tier 0, with the reason recorded"

_NAME = re.compile(r'^\s*name\s*=\s*"(?P<name>(?:[^"\\]|\\.)*)"\s*$')
_TIER = re.compile(r"^\s*tier\s*=\s*(?P<tier>\d+)\s*$")


def _blocks(lines: list[str]) -> list[tuple[int, int, int]]:
    """(header, end of the block's own keys, end of the block) per [[classes]].

    A block's own keys stop at its first sub-table header, because a key written
    after `[classes.calibration]` would belong to the calibration table instead.
    """
    out: list[tuple[int, int, int]] = []
    for i, line in enumerate(lines):
        if line.strip() != "[[classes]]":
            continue
        key_end = block_end = len(lines)
        for j in range(i + 1, len(lines)):
            stripped = lines[j].lstrip()
            if stripped.startswith("["):
                if key_end == len(lines):
                    key_end = j
                if not stripped.startswith("[classes."):
                    block_end = j
                    break
        out.append((i, min(key_end, block_end), block_end))
    return out


def _upsert(lines: list[str], header: int, key_end: int, key: str, value: Any) -> int:
    """Replace the key inside this block, or add it. Returns the new key_end."""
    pattern = re.compile(rf"^\s*{re.escape(key)}\s*=")
    for j in range(header + 1, key_end):
        if pattern.match(lines[j]):
            lines[j] = toml_kv(key, value)
            return key_end
    at = key_end
    while at - 1 > header and not lines[at - 1].strip():
        at -= 1
    lines.insert(at, toml_kv(key, value))
    return key_end + 1


def set_tier_zero(path: pathlib.Path, defect_class: str, *, reason: str,
                  trigger: str, at: str) -> dict[str, Any]:
    """Edit the warrant in place. Returns what happened; raises only if the edit
    would produce a warrant tomllib cannot read, in which case nothing is written."""
    if not path.exists():
        raise Absent(str(path))
    original = path.read_text()
    lines = original.splitlines()

    target: tuple[int, int, int] | None = None
    for header, key_end, block_end in _blocks(lines):
        for j in range(header + 1, key_end):
            m = _NAME.match(lines[j])
            if m and m.group("name") == defect_class:
                target = (header, key_end, block_end)
                break
        if target:
            break

    if target is None:
        return {"changed": False, "found": False, "previous_tier": 0,
                "why": f"the warrant does not name {defect_class!r}, so it already holds "
                       "tier 0 by default and there is no authority to take away"}

    header, key_end, _ = target
    previous = 0
    tier_line = None
    for j in range(header + 1, key_end):
        m = _TIER.match(lines[j])
        if m:
            previous, tier_line = int(m.group("tier")), j
            break
    if previous == 0:
        return {"changed": False, "found": True, "previous_tier": 0,
                "why": f"{defect_class} already holds tier 0"}

    lines[tier_line] = "tier = 0"
    key_end = _upsert(lines, header, key_end, "revoked_at", at)
    key_end = _upsert(lines, header, key_end, "revoked_trigger", trigger)
    key_end = _upsert(lines, header, key_end, "revoked_reason", reason)

    candidate = "\n".join(lines) + "\n"
    try:
        tomllib.loads(candidate)
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(f"the edit would leave {path} unreadable ({exc}); "
                         "the warrant has not been touched") from exc

    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(candidate)
    tmp.replace(path)
    return {"changed": True, "found": True, "previous_tier": previous,
            "why": f"{defect_class} dropped from tier {previous} to tier 0"}


def revoke(root: str | pathlib.Path, defect_class: str, *, reason: str, trigger: str,
           when: Any, warrant_version: str | None = None) -> dict[str, Any]:
    """Revoke and record. Used by ratchet.py as well as by the CLI."""
    at = when.isoformat()
    result = set_tier_zero(warrant_path(root), defect_class,
                           reason=reason, trigger=trigger, at=at)
    result.update(defect_class=defect_class, reason=reason, trigger=trigger, at=at,
                  ledger_row=None, ledger_error=None)
    if not result["changed"]:
        return result

    # The authority is gone. A failure below is logged, not raised.
    import ledger
    try:
        row, _ = ledger.append_row(
            root, item=f"class:{defect_class}", verdict="revoked", tier=0,
            warrant_version=warrant_version or str(read_warrant(root).get("version", "unsigned")),
            outcome=f"tier {result['previous_tier']} -> 0",
            note=f"{trigger}: {reason}", when=when)
        result["ledger_row"] = row
    except Exception as exc:                                       # noqa: BLE001
        result["ledger_error"] = f"{type(exc).__name__}: {exc}"
    return result


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--class", dest="defect_class", help="the class to drop to tier 0 (required)")
    p.add_argument("--reason", help="why, in words a later reader can act on (required)")
    p.add_argument("--trigger", default="manual",
                   help="what fired it: model_drift, regression_failing, new_escape, "
                        "westgard, oracle_coverage or manual")


def main(args: argparse.Namespace) -> int:
    if not args.defect_class:
        say(args, "--class is required")
        return ERROR
    if not args.reason:
        say(args, "--reason is required: a revocation with no reason is one somebody will "
                  "quietly reverse")
        return ERROR

    try:
        result = revoke(args.root, args.defect_class, reason=args.reason,
                        trigger=args.trigger, when=clock(args))
    except ValueError as exc:
        say(args, str(exc))
        return ERROR

    say(args, result["why"])
    if result["changed"]:
        say(args, f"  trigger: {result['trigger']}")
        say(args, f"  reason:  {result['reason']}")
        say(args, f"  at:      {result['at']}")
    if result["ledger_error"]:
        say(args, f"warning: the warrant was written but the ledger row failed — "
                  f"{result['ledger_error']}")
    emit(args, result)
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


def _seed(tmp: str) -> pathlib.Path:
    d = pathlib.Path(tmp) / ".warrant"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(FIXTURES / "warrant.toml", d / "warrant.toml")
    shutil.copy(FIXTURES / "lanes.toml", d / "lanes.toml")
    return d


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    import ledger

    with tempfile.TemporaryDirectory() as tmp:
        _seed(tmp)
        base = ["--root", tmp, "--json", "--now", "2026-08-18T09:00:00+00:00"]
        code, out, _ = _run(base + ["--class", "figure-lineage",
                                    "--reason", "the grader was reversioned",
                                    "--trigger", "model_drift"])
        result = json.loads(out)
        warrant = read_warrant(tmp)
        cases.append(("a revocation exits 0", code == OK))
        cases.append(("the class drops to tier 0", tier_of(warrant, "figure-lineage") == 0))
        cases.append(("the previous tier is reported", result["previous_tier"] == 2))
        block = next(c for c in warrant["classes"] if c["name"] == "figure-lineage")
        cases.append(("the reason is written into the warrant",
                      block["revoked_reason"] == "the grader was reversioned"))
        cases.append(("the trigger is written into the warrant",
                      block["revoked_trigger"] == "model_drift"))
        cases.append(("the timestamp is written into the warrant",
                      block["revoked_at"] == "2026-08-18T09:00:00+00:00"))
        cases.append(("the block's sub-table survives the edit",
                      block["calibration"]["at"] == "2026-07-01T00:00:00+00:00"))
        cases.append(("other classes are untouched",
                      tier_of(warrant, "layout-drift") == 1))
        cases.append(("the warrant's own fields are untouched",
                      warrant["owner"] == "Luke Rhodes" and warrant["version"] == "1.4.0"))
        cases.append(("the comments a person signed are preserved",
                      "# A fixture warrant." in (pathlib.Path(tmp) / ".warrant"
                                                 / "warrant.toml").read_text()))
        rows = [json.loads(l) for l in
                ledger.ledger_path(tmp).read_text().splitlines() if l.strip()]
        cases.append(("a ledger row records the revocation",
                      len(rows) == 1 and rows[0]["verdict"] == "revoked"))
        cases.append(("the row names the class as its item",
                      rows[0]["item"] == "class:figure-lineage"))
        cases.append(("and carries the reason and trigger",
                      "model_drift" in rows[0]["note"] and "reversioned" in rows[0]["note"]))
        cases.append(("and the tier it came from",
                      rows[0]["outcome"] == "tier 2 -> 0"))

        code, out, err = _run(base + ["--class", "figure-lineage", "--reason", "again"])
        result = json.loads(out)
        cases.append(("revoking an already-zero class changes nothing",
                      code == OK and result["changed"] is False))
        cases.append(("and appends no second ledger row",
                      len(ledger.ledger_path(tmp).read_text().splitlines()) == 1))
        cases.append(("and says why", "already holds tier 0" in err))

        code, out, err = _run(base + ["--class", "no-such-class", "--reason", "why not"])
        cases.append(("a class the warrant does not name reports rather than fails",
                      code == OK and json.loads(out)["found"] is False))
        cases.append(("and says it already holds tier 0 by default",
                      "tier 0 by default" in err))

        cases.append(("a missing --reason exits 1",
                      _run(["--root", tmp, "--class", "layout-drift"])[0] == ERROR))
        cases.append(("a missing --class exits 1",
                      _run(["--root", tmp, "--reason", "because"])[0] == ERROR))

    with tempfile.TemporaryDirectory() as tmp:
        cases.append(("an absent warrant exits 3",
                      _run(["--root", tmp, "--class", "x", "--reason", "y"])[0] == MISSING))

    with tempfile.TemporaryDirectory() as tmp:
        d = _seed(tmp)
        # The ledger cannot be written. The warrant edit must still stand.
        (d / "ledger.jsonl").mkdir()
        code, out, err = _run(["--root", tmp, "--json", "--class", "layout-drift",
                               "--reason", "oracle coverage fell below the tier-1 threshold",
                               "--trigger", "oracle_coverage"])
        result = json.loads(out)
        cases.append(("a ledger failure does not raise", code == OK))
        cases.append(("the revocation still stands",
                      tier_of(read_warrant(tmp), "layout-drift") == 0))
        cases.append(("and the ledger failure is reported",
                      bool(result["ledger_error"]) and "ledger row failed" in err))

    with tempfile.TemporaryDirectory() as tmp:
        d = _seed(tmp)
        # A reason with a quote and a backslash in it, which is where a hand-rolled
        # TOML writer usually produces a file nothing can read.
        code, out, _ = _run(["--root", tmp, "--json", "--class", "figure-lineage",
                             "--reason", 'the grader said "pass" on C:\\evidence\\1'])
        block = next(c for c in read_warrant(tmp)["classes"] if c["name"] == "figure-lineage")
        cases.append(("a reason with quotes and backslashes still parses",
                      block["revoked_reason"] == 'the grader said "pass" on C:\\evidence\\1'))

    return cases


if __name__ == "__main__":
    raise SystemExit(entry(_DESC, main, selftest, _extra))
