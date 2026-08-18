"""Append one hash-chained row to the decision ledger.

This is the artifact an auditor reads instead of a signature per item, so its
integrity property is the whole point: a ledger that can be edited after the
fact proves nothing. Each row carries `prev`, the SHA-256 of the previous row's
canonical JSON body, and `hash`, the SHA-256 of its own. The self hash is there
so a flipped byte in the newest row is caught too — `prev` alone leaves the
final row unlinked, and the final row is the one a tamperer reaches first.

Every key is present on every row, null where there is no value, because the
canonical form has to be reproducible from what is on disk. A key that is
sometimes absent hashes differently from a key that is null, and the chain
would break on the writer's mood rather than on tampering.

Appends only. Nothing here rewrites a line, and a corrupt tail is reported
rather than repaired: the append still happens, because refusing to record a
decision is worse than recording it onto a chain that already has a break in
it, and `ledger_verify.py` will name the break either way.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as _dt
import hashlib
import io
import json
import os
import pathlib
import sys
import tempfile
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _cli import ERROR, FAILED, MISSING, OK, emit, entry, parser, say
from _cli import run as dispatch
from _cli import now as clock
from _state import Absent, append_jsonl, read_jsonl, read_lanes, read_warrant, state_dir

_DESC = "Append one hash-chained row to .warrant/ledger.jsonl"

GENESIS = "0" * 64
VERDICTS = ("pass", "fail", "inconclusive", "revoked")

# The row shape. Fixed, ordered here for readers; the canonical form sorts keys.
FIELDS = ("index", "at", "item", "defect_class", "warrant_version", "model_id",
          "model_version", "evidence_digest", "verdict", "tier", "outcome", "note", "prev")


def ledger_path(root: str | pathlib.Path) -> pathlib.Path:
    return state_dir(root) / "ledger.jsonl"


def canonical(body: dict[str, Any]) -> str:
    """The bytes a row's hash is taken over. Sorted, tight, no whitespace."""
    return json.dumps(body, sort_keys=True, separators=(",", ":"))


def row_hash(body: dict[str, Any]) -> str:
    body = {k: v for k, v in body.items() if k != "hash"}
    return hashlib.sha256(canonical(body).encode("utf-8")).hexdigest()


def tail(path: pathlib.Path) -> tuple[int, str, list[str]]:
    """(next index, hash to link against, warnings about what is already there)."""
    warnings: list[str] = []
    if not path.exists():
        return 0, GENESIS, warnings
    lines = [ln for ln in path.read_text().splitlines() if ln.strip()]
    if not lines:
        return 0, GENESIS, warnings
    for offset, line in enumerate(reversed(lines)):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            warnings.append(f"row {len(lines) - 1 - offset} is not valid JSON; "
                            "linking against the last row that is")
            continue
        if not isinstance(row, dict) or "hash" not in row:
            warnings.append(f"row {len(lines) - 1 - offset} carries no hash; "
                            "linking against the last row that does")
            continue
        index = row.get("index")
        next_index = int(index) + 1 if isinstance(index, int) else len(lines)
        if offset:
            warnings.append(f"{offset} unusable row(s) sit after row {next_index - 1}; "
                            "the chain already has a break in it")
        return next_index, str(row["hash"]), warnings
    warnings.append("no usable row in the existing ledger; linking from genesis")
    return len(lines), GENESIS, warnings


def append_row(root: str | pathlib.Path, *, item: str, verdict: str, tier: int,
               defect_class: str | None = None,
               warrant_version: str | None = None, model_id: str | None = None,
               model_version: str | None = None, evidence_digest: str | None = None,
               outcome: str | None = None, note: str | None = None,
               when: _dt.datetime | None = None) -> tuple[dict[str, Any], list[str]]:
    """Append one row and return it with any warnings about the existing chain.

    Callers that have already had an external effect of their own catch whatever
    this raises rather than letting it abort them; see revoke.py.
    """
    path = ledger_path(root)
    state_dir(root, create=True)
    index, prev, warnings = tail(path)
    body = {
        "index": index,
        "at": (when or _dt.datetime.now(_dt.timezone.utc)).isoformat(),
        "item": item,
        # Which class authorised this. Without it the tier-3 entry condition
        # ("N items closed in this class with no escapes") cannot be counted, and
        # an auditor cannot tell which policy covered a decision.
        "defect_class": defect_class,
        "warrant_version": warrant_version,
        "model_id": model_id,
        "model_version": model_version,
        "evidence_digest": evidence_digest,
        "verdict": verdict,
        "tier": int(tier),
        "outcome": outcome,
        "note": note,
        "prev": prev,
    }
    row = dict(body)
    row["hash"] = row_hash(body)
    append_jsonl(path, row)
    return row, warnings


def _lane_default(root: str | pathlib.Path) -> tuple[str | None, str | None]:
    """The pinned model, when exactly one lane is declared and none was given."""
    try:
        lanes = read_lanes(root)
    except Absent:
        return None, None
    blocks = _lane_blocks(lanes)
    if len(blocks) == 1:
        only = next(iter(blocks.values()))
        return only[0], only[1]
    return None, None


def _lane_blocks(lanes: dict[str, Any]) -> dict[str, tuple[str, str]]:
    """role -> (model_id, version), from either lanes.toml spelling."""
    out: dict[str, tuple[str, str]] = {}
    for block in lanes.get("lanes", []) if isinstance(lanes.get("lanes"), list) else []:
        role = str(block.get("role", "")).strip()
        if role:
            out[role] = (str(block.get("model_id", "")), str(block.get("version", "")))
    if isinstance(lanes.get("lanes"), dict):
        for role, block in lanes["lanes"].items():
            if isinstance(block, dict):
                out[str(role)] = (str(block.get("model_id", "")), str(block.get("version", "")))
    return out


def _warrant_version(root: str | pathlib.Path) -> str:
    try:
        return str(read_warrant(root).get("version", "unsigned"))
    except Absent:
        return "unsigned"


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--class", dest="defect_class",
                   help="the defect class this decision was authorised under; the tier-3 "
                        "entry condition counts closed items per class, so a row without it "
                        "cannot be counted")
    p.add_argument("--item", help="the item the decision is about (required)")
    p.add_argument("--verdict", help=f"one of {', '.join(VERDICTS)} (required)")
    p.add_argument("--tier", type=int, default=0, help="the tier that authorised the verdict")
    p.add_argument("--warrant-version", help="defaults to the warrant's version, or 'unsigned'")
    p.add_argument("--model-id", help="defaults to the sole lane's pinned id, when there is one")
    p.add_argument("--model-version")
    p.add_argument("--evidence-digest", help="digest of the snapshot the verdict was written from")
    p.add_argument("--outcome", help="what later emerged, when it has")
    p.add_argument("--note")


def main(args: argparse.Namespace) -> int:
    if not args.item:
        say(args, "--item is required: a ledger row with no item is not a decision record")
        return ERROR
    if args.verdict not in VERDICTS:
        say(args, f"--verdict must be one of {', '.join(VERDICTS)}; got {args.verdict!r}")
        return ERROR
    if not 0 <= args.tier <= 4:
        say(args, f"--tier must be 0-4; got {args.tier}")
        return ERROR

    model_id, model_version = args.model_id, args.model_version
    if not model_id:
        model_id, model_version = _lane_default(args.root)

    row, warnings = append_row(
        args.root,
            defect_class=args.defect_class,
        item=args.item,
        verdict=args.verdict,
        tier=args.tier,
        warrant_version=args.warrant_version or _warrant_version(args.root),
        model_id=model_id,
        model_version=model_version,
        evidence_digest=args.evidence_digest,
        outcome=args.outcome,
        note=args.note,
        when=clock(args),
    )

    # The row is on disk. Everything below is reporting, and a failure in it is
    # logged rather than raised: raising here invites a retry that appends twice.
    try:
        for warning in warnings:
            say(args, f"warning: {warning}")
        say(args, f"row {row['index']} appended: {row['item']} {row['verdict']} "
                  f"tier {row['tier']} hash {row['hash'][:12]}")
        emit(args, {"appended": True, "row": row, "warnings": warnings,
                    "ledger": str(ledger_path(args.root))})
    except Exception as exc:                                       # noqa: BLE001
        print(f"row {row['index']} was appended; reporting it failed: "
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


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    with tempfile.TemporaryDirectory() as tmp:
        base = ["--root", tmp, "--json"]
        code, out, _ = _run(base + ["--item", "WEB-1", "--verdict", "pass", "--tier", "2",
                                    "--evidence-digest", "a" * 64,
                                    "--now", "2026-08-18T00:00:00+00:00"])
        first = json.loads(out)["row"]
        cases.append(("first append exits 0", code == OK))
        cases.append(("genesis row links to 64 zeros", first["prev"] == GENESIS))
        cases.append(("genesis row index is 0", first["index"] == 0))
        cases.append(("stdout under --json is only the JSON object", out.lstrip().startswith("{")))

        code, out, _ = _run(base + ["--item", "WEB-2", "--verdict", "fail", "--tier", "1",
                                    "--now", "2026-08-18T00:01:00+00:00"])
        second = json.loads(out)["row"]
        cases.append(("second row links to the first row's hash",
                      second["prev"] == first["hash"]))
        cases.append(("index increments", second["index"] == 1))
        cases.append(("row hash recomputes from what is on disk",
                      row_hash(second) == second["hash"]))

        reordered = {k: second[k] for k in reversed(list(second.keys()))}
        cases.append(("hash is stable under key order", row_hash(reordered) == second["hash"]))

        rows = read_jsonl(ledger_path(tmp))
        cases.append(("append-only: both rows still present", len(rows) == 2))

        cases.append(("missing --item exits 1", _run(base + ["--verdict", "pass"])[0] == ERROR))
        cases.append(("unknown verdict exits 1",
                      _run(base + ["--item", "X", "--verdict", "maybe"])[0] == ERROR))
        cases.append(("tier out of range exits 1",
                      _run(base + ["--item", "X", "--verdict", "pass", "--tier", "9"])[0] == ERROR))
        cases.append(("verdict 'revoked' is accepted, so a revocation is a ledger row",
                      _run(base + ["--item", "class:figure-lineage", "--verdict", "revoked"])[0] == OK))

    with tempfile.TemporaryDirectory() as tmp:
        # A chain that already has a break in it. The append must still happen.
        path = ledger_path(tmp)
        state_dir(tmp, create=True)
        _run(["--root", tmp, "--item", "WEB-1", "--verdict", "pass"])
        with path.open("a") as fh:
            fh.write("{ this is not json\n")
        code, out, err = _run(["--root", tmp, "--json", "--item", "WEB-2", "--verdict", "pass"])
        payload = json.loads(out)
        cases.append(("corrupt tail still appends", code == OK and payload["appended"]))
        cases.append(("corrupt tail is reported as a warning",
                      any("not valid JSON" in w for w in payload["warnings"])))
        cases.append(("corrupt tail links to the last usable row",
                      payload["row"]["prev"] != GENESIS))

    with tempfile.TemporaryDirectory() as tmp:
        # The external-effect rule: the row lands, and a reporting failure after
        # it is logged rather than raised.
        real_stdout = sys.stdout

        class Broken(io.StringIO):
            def write(self, _s: str) -> int:
                raise OSError("stdout went away")

        args = _parse(["--root", tmp, "--json", "--item", "WEB-9", "--verdict", "pass"])
        err = io.StringIO()
        try:
            with contextlib.redirect_stderr(err):
                sys.stdout = Broken()
                code = main(args)
        finally:
            sys.stdout = real_stdout
        cases.append(("a reporting failure after the append does not raise", code == OK))
        cases.append(("the appended row survives that failure",
                      len(read_jsonl(ledger_path(tmp))) == 1))
        cases.append(("the reporting failure is logged", "was appended" in err.getvalue()))

    return cases


if __name__ == "__main__":
    raise SystemExit(entry(_DESC, main, selftest, _extra))
