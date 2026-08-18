"""Walk the ledger chain and stop at the first break.

Exits 2 on the first break, naming the row index and what did not match, because
an auditor asking "has this been edited" needs one answer and its location
rather than a list of consequences: one flipped byte in row 3 breaks row 3's own
hash and row 4's link, and reporting both invites the reader to think two things
happened.

Four ways a row can be wrong, checked in this order:

  malformed  the line is not a JSON object
  hash       the row's canonical body does not hash to its stored `hash`
  prev       the row's `prev` is not the previous row's stored `hash`
  index      the row's `index` is not its position in the file

The hash check is what catches a flipped byte anywhere, including in the newest
row. The prev check is what catches a row that was removed, reordered or
inserted whole. Both are needed: re-hashing a tampered row repairs its self
hash and leaves the link broken, and splicing an untouched row from elsewhere
leaves the self hash intact and the link broken.
"""

from __future__ import annotations

import argparse
import contextlib
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
from _state import read_jsonl
from ledger import GENESIS, ledger_path, row_hash

_DESC = "Verify the hash chain in .warrant/ledger.jsonl"


def verify(lines: list[str]) -> tuple[dict[str, Any] | None, int]:
    """(the first break or None, rows examined).

    Returns rather than raises, so callers can report the break with the rest of
    their own output.
    """
    prev_hash = GENESIS
    examined = 0
    for index, line in enumerate(lines):
        examined = index + 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            return {"row": index, "problem": "malformed",
                    "detail": f"line is not valid JSON: {exc}"}, examined
        if not isinstance(row, dict):
            return {"row": index, "problem": "malformed",
                    "detail": f"line is a {type(row).__name__}, not a JSON object"}, examined
        for key in ("hash", "prev", "index"):
            if key not in row:
                return {"row": index, "problem": "malformed",
                        "detail": f"row carries no {key!r}"}, examined

        recomputed = row_hash(row)
        if recomputed != row["hash"]:
            return {"row": index, "problem": "hash",
                    "detail": f"row content hashes to {recomputed} but the row stores "
                              f"{row['hash']}; this row has been altered",
                    "expected": recomputed, "found": row["hash"]}, examined
        if row["prev"] != prev_hash:
            return {"row": index, "problem": "prev",
                    "detail": f"row links to {row['prev']} but row {index - 1} hashes to "
                              f"{prev_hash}; a row has been removed, reordered or inserted",
                    "expected": prev_hash, "found": row["prev"]}, examined
        if row["index"] != index:
            return {"row": index, "problem": "index",
                    "detail": f"row is at position {index} but records index {row['index']}",
                    "expected": index, "found": row["index"]}, examined
        prev_hash = row["hash"]
    return None, examined


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--ledger", help="path to a ledger file; defaults to .warrant/ledger.jsonl")


def main(args: argparse.Namespace) -> int:
    path = pathlib.Path(args.ledger) if args.ledger else ledger_path(args.root)
    if not path.exists():
        say(args, f"no ledger at {path}")
        emit(args, {"ok": False, "reason": "no ledger", "ledger": str(path)})
        return MISSING

    lines = [ln for ln in path.read_text().splitlines() if ln.strip()]
    break_, examined = verify(lines)
    head = json.loads(lines[-1])["hash"] if break_ is None and lines else None
    payload = {"ok": break_ is None, "rows": examined, "ledger": str(path),
               "head": head, "break": break_}

    if break_ is None:
        say(args, f"chain intact over {examined} row(s)")
        emit(args, payload)
        return OK

    say(args, f"chain breaks at row {break_['row']}: {break_['problem']} — {break_['detail']}")
    emit(args, payload)
    return FAILED


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


def _chain(tmp: str, n: int = 4) -> pathlib.Path:
    import ledger
    for i in range(n):
        ledger.append_row(tmp, item=f"WEB-{i}", verdict="pass", tier=2,
                          warrant_version="1.4.0", model_id="anthropic/claude-opus-4.8",
                          model_version="2026-07-01", evidence_digest=f"{i}" * 64)
    return ledger.ledger_path(tmp)


def _flip(path: pathlib.Path, row: int, find: str, replace: str) -> None:
    """One byte, in place. The file stays valid JSON so only the chain can object."""
    lines = path.read_text().splitlines()
    assert find in lines[row], f"fixture wrong: {find!r} not in row {row}"
    lines[row] = lines[row].replace(find, replace, 1)
    path.write_text("\n".join(lines) + "\n")


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []

    with tempfile.TemporaryDirectory() as tmp:
        _chain(tmp)
        code, out, _ = _run(["--root", tmp, "--json"])
        cases.append(("an untampered chain verifies", code == OK))
        cases.append(("it reports the rows it examined", json.loads(out)["rows"] == 4))

    with tempfile.TemporaryDirectory() as tmp:
        path = _chain(tmp)
        _flip(path, 1, '"1111', '"1211')                     # one byte, mid-chain
        code, out, err = _run(["--root", tmp, "--json"])
        payload = json.loads(out)
        cases.append(("a flipped byte in a historical row exits 2", code == FAILED))
        cases.append(("it names the row", payload["break"]["row"] == 1))
        cases.append(("it names what did not match", payload["break"]["problem"] == "hash"))
        cases.append(("the human line names the row too", "row 1" in err))

    with tempfile.TemporaryDirectory() as tmp:
        path = _chain(tmp)
        _flip(path, 3, '"3333', '"3433')                     # the newest row
        code, out, _ = _run(["--root", tmp, "--json"])
        cases.append(("a flipped byte in the NEWEST row is caught",
                      code == FAILED and json.loads(out)["break"]["row"] == 3))

    with tempfile.TemporaryDirectory() as tmp:
        path = _chain(tmp)
        _flip(path, 0, '"prev": "0000', '"prev": "1000')     # the genesis link
        code, out, _ = _run(["--root", tmp, "--json"])
        cases.append(("a rewritten genesis link is caught", code == FAILED))

    with tempfile.TemporaryDirectory() as tmp:
        path = _chain(tmp)
        lines = path.read_text().splitlines()
        del lines[1]
        path.write_text("\n".join(lines) + "\n")
        code, out, _ = _run(["--root", tmp, "--json"])
        payload = json.loads(out)
        cases.append(("a removed row is caught by the link",
                      code == FAILED and payload["break"]["problem"] == "prev"))
        cases.append(("it names the row that no longer links",
                      payload["break"]["row"] == 1))

    with tempfile.TemporaryDirectory() as tmp:
        path = _chain(tmp)
        lines = path.read_text().splitlines()
        lines[1], lines[2] = lines[2], lines[1]
        path.write_text("\n".join(lines) + "\n")
        cases.append(("reordered rows are caught", _run(["--root", tmp])[0] == FAILED))

    with tempfile.TemporaryDirectory() as tmp:
        path = _chain(tmp)
        with path.open("a") as fh:
            fh.write('{"index": 4, "hash": "deadbeef", "prev": "cafe"}\n')
        code, out, _ = _run(["--root", tmp, "--json"])
        cases.append(("a forged appended row is caught",
                      code == FAILED and json.loads(out)["break"]["row"] == 4))

    with tempfile.TemporaryDirectory() as tmp:
        path = _chain(tmp)
        with path.open("a") as fh:
            fh.write("{ truncated\n")
        code, out, _ = _run(["--root", tmp, "--json"])
        cases.append(("a malformed line is caught as malformed",
                      code == FAILED and json.loads(out)["break"]["problem"] == "malformed"))

    with tempfile.TemporaryDirectory() as tmp:
        path = _chain(tmp)
        _flip(path, 2, '"index": 2', '"index": 7')
        code, out, _ = _run(["--root", tmp, "--json"])
        # An index edit changes the body, so the self hash objects first. That
        # ordering is deliberate: the strongest available answer is the one to
        # report, and "this row was altered" is stronger than "its number is wrong".
        cases.append(("an edited index is caught", code == FAILED))
        cases.append(("the self hash objects before the index does",
                      json.loads(out)["break"]["problem"] == "hash"))

    with tempfile.TemporaryDirectory() as tmp:
        # A row that is internally consistent but sits at the wrong position, so
        # the index rule is the only one left to fire.
        import ledger
        path = ledger.ledger_path(tmp)
        rows = []
        prev = GENESIS
        for i in (0, 1, 3):
            body = {"index": i, "at": "2026-08-18T00:00:00+00:00", "item": f"WEB-{i}",
                    "warrant_version": "1.4.0", "model_id": None, "model_version": None,
                    "evidence_digest": None, "verdict": "pass", "tier": 0,
                    "outcome": None, "note": None, "prev": prev}
            row = dict(body)
            row["hash"] = row_hash(body)
            prev = row["hash"]
            rows.append(row)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
        code, out, _ = _run(["--root", tmp, "--json"])
        cases.append(("a skipped index is caught by the index rule",
                      code == FAILED and json.loads(out)["break"]["problem"] == "index"))

    with tempfile.TemporaryDirectory() as tmp:
        cases.append(("an absent ledger exits 3, not 2", _run(["--root", tmp])[0] == MISSING))
        p = pathlib.Path(tmp) / ".warrant" / "ledger.jsonl"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("")
        cases.append(("an empty ledger verifies", _run(["--root", tmp])[0] == OK))

    return cases


if __name__ == "__main__":
    raise SystemExit(entry(_DESC, main, selftest, _extra))
