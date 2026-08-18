#!/usr/bin/env python3
"""Build the reviewer's queue, carrying no verdict, with seeds mixed in.

The human sample has to be blind to the machine verdict. In 323,973 women,
screening with a computer aid showed no accuracy gain, and among the radiologists
who read both with and without it sensitivity was significantly LOWER with the aid
— odds ratio 0.53. Pre-populating a reviewer's queue with the verdict is the
cheapest thing to build and the one thing the evidence forbids.

So the queue is a projection, not a filter: it carries an allowlist of fields and
nothing else, and the result is checked for a leak before either file is written.
A leak is exit 2 and nothing is written.

    reviewer file  .warrant/reports/<date>-blind-queue.json      order + ids
    operator key   .warrant/reports/<date>-blind-queue.key.json  which are seeds
                                                                 (mode 0600)

The seed rate is read from a side file (`--seeds`, default
`.warrant/seeds.local.json`), never from the warrant. The warrant is signed,
diffable and shared, so a rate written there is a rate the reviewer can read and
calibrate to. Keep the side file out of version control.

Seeds sit in the queue as ordinary items and the reviewer artifact does not say
which they are — not their count, not their positions. That is what makes the
recovery count in `lot_report.py` mean anything.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import io
import json
import pathlib
import random
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                   # noqa: E402
import _state                                                 # noqa: E402

FIXTURES = (pathlib.Path(__file__).resolve().parent.parent
            / "evals" / "fixtures" / "charter-panel-lot")

# What a reviewer needs to find the item, and nothing that hints at an answer.
ALLOWED = ("id", "surface", "url", "item_type")

# Substring-matched against every key in the queue, case-insensitively.
BANNED_KEYS = ("verdict", "state", "pass", "fail", "inconclusive", "score",
               "confidence", "tier", "panel", "lane", "machine", "seed",
               "known_bad", "expected", "defect", "severity", "recommend",
               "prediction", "label")

BANNED_VALUES = ("pass", "fail", "inconclusive", "passed", "failed", "ok",
                 "not ok", "green", "red")


def read_items(path: pathlib.Path) -> list[dict[str, object]]:
    if not path.is_file():
        raise _state.Absent(str(path))
    text = path.read_text().strip()
    if not text:
        return []
    if text.startswith("["):
        rows = json.loads(text)
    else:
        rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    return [row for row in rows if isinstance(row, dict)]


def leaks(rows: list[dict[str, object]]) -> list[str]:
    """Every way a verdict could reach the reviewer through this queue."""
    found: list[str] = []
    for i, row in enumerate(rows, start=1):
        for key, value in row.items():
            low = str(key).lower()
            for banned in BANNED_KEYS:
                if banned in low:
                    found.append(f"position {i}: the field {key!r} would carry a "
                                 f"verdict to the reviewer (matched {banned!r})")
                    break
            text = str(value).strip().lower()
            if text in BANNED_VALUES:
                found.append(f"position {i}: {key}={value!r} reads as a verdict")
            elif "verdict" in text:
                found.append(f"position {i}: {key} mentions a verdict: {value!r}")
    return found


def order_seed(salt: str, lot_id: str, warrant_version: str, ids: list[str]) -> int:
    """A reproducible order that is not the panel's order.

    Seeded from the side file's salt, so an auditor can reproduce the queue while
    the order still carries no information about the verdicts.
    """
    h = hashlib.sha256()
    h.update(f"{salt}\n{lot_id}\n{warrant_version}\n".encode())
    for item in sorted(ids):
        h.update(item.encode() + b"\n")
    return int.from_bytes(h.digest()[:8], "big")


def extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--items", default=None,
                   help="JSON array or JSONL of the items to review")
    p.add_argument("--seeds", default=None,
                   help="side file with the seed rate and the known-bad items "
                        "(default: <root>/.warrant/seeds.local.json)")
    p.add_argument("--lot-id", default=None, help="a name for this lot")
    p.add_argument("--carry", action="append", default=[], metavar="FIELD",
                   help="carry one more field through to the reviewer; refused if it "
                        "would leak a verdict")


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()
    warrant = _state.read_warrant(root)                        # Absent -> exit 3

    if not args.items:
        _cli.say(args, "pass --items PATH: the queue is built from the items to review")
        _cli.emit(args, {"ok": False, "reason": "no-items"})
        return _cli.ERROR
    items = read_items(pathlib.Path(args.items).expanduser().resolve())
    if not items:
        _cli.say(args, "there are no items to review")
        _cli.emit(args, {"ok": False, "reason": "empty-queue"})
        return _cli.MISSING

    seeds_path = pathlib.Path(args.seeds).expanduser().resolve() if args.seeds \
        else _state.state_dir(root) / "seeds.local.json"
    if not seeds_path.is_file():
        _cli.say(args, f"no seed file at {seeds_path}")
        _cli.say(args, "  the seed rate lives in a side file rather than in the "
                       "warrant, because a rate in the signed file is a rate the "
                       "reviewer can read")
        _cli.emit(args, {"ok": False, "reason": "no-seeds", "seeds": str(seeds_path)})
        return _cli.MISSING
    seeds_doc = _state.read_json(seeds_path)
    rate = seeds_doc.get("rate")
    pool = [s for s in seeds_doc.get("items", []) if isinstance(s, dict)]
    if isinstance(rate, bool) or not isinstance(rate, (int, float)) \
            or not (0.0 <= float(rate) < 1.0):
        _cli.say(args, f"{seeds_path}: rate is {rate!r}, which is not a proportion "
                       "in [0,1)")
        _cli.emit(args, {"ok": False, "reason": "bad-seed-rate", "rate": rate})
        return _cli.ERROR
    rate = float(rate)

    wanted = round(rate * len(items))
    shortfall = max(0, wanted - len(pool))
    chosen = pool[:wanted]

    lot_id = args.lot_id or f"lot-{len(items)}"
    version = str(warrant.get("version", ""))
    salt = str(seeds_doc.get("salt", ""))

    combined: list[tuple[dict[str, object], dict[str, object] | None]] = \
        [(row, None) for row in items] + [(seed, seed) for seed in chosen]
    allowed = tuple(ALLOWED) + tuple(args.carry)
    queue_rows: list[dict[str, object]] = []
    for row, _seed in combined:
        queue_rows.append({key: row[key] for key in allowed if key in row})

    ids = [str(row.get("id", "")) for row in queue_rows]
    if any(not i for i in ids):
        _cli.say(args, "every item needs an id; the queue cannot point at an item "
                       "without one")
        _cli.emit(args, {"ok": False, "reason": "missing-id"})
        return _cli.ERROR

    rng = random.Random(order_seed(salt, lot_id, version, ids))
    order = list(range(len(combined)))
    rng.shuffle(order)

    reviewer_rows: list[dict[str, object]] = []
    key_rows: list[dict[str, object]] = []
    for position, index in enumerate(order, start=1):
        row, seed = combined[index]
        reviewer_rows.append({"position": position, **queue_rows[index]})
        if seed is not None:
            key_rows.append({
                "position": position,
                "id": seed.get("id"),
                "defect": seed.get("defect"),
                "expected": seed.get("expected", "fail"),
                "defect_class": seed.get("defect_class"),
            })

    # The assertion, before anything is written.
    found = leaks(reviewer_rows)
    if found:
        _cli.say(args, f"NOT written: {len(found)} way(s) a verdict would reach the "
                       "reviewer")
        for leak in found[:10]:
            _cli.say(args, f"  {leak}")
        _cli.say(args, "  the human sample has to be blind: reading with a machine "
                       "aid measured significantly LOWER sensitivity than reading "
                       "without it (odds ratio 0.53)")
        _cli.emit(args, {"ok": False, "reason": "verdict-leak", "leaks": found,
                         "queue": None, "key": None})
        return _cli.FAILED

    stamp = _cli.now(args)
    reports = _state.state_dir(root, create=True) / "reports"
    queue_path = reports / f"{stamp.date().isoformat()}-blind-queue.json"
    key_path = reports / f"{stamp.date().isoformat()}-blind-queue.key.json"

    queue_doc = {
        "schema": "warrant.blind-queue/1",
        "lot_id": lot_id,
        "built_at": stamp.isoformat(),
        "warrant_version": version,
        "population": len(reviewer_rows),
        "fields": sorted({k for row in reviewer_rows for k in row if k != "position"}),
        "note": "This queue carries no verdict, by construction and by assertion. "
                "Review each item on its own evidence and record your call before "
                "looking at anything else.",
        "order": reviewer_rows,
    }
    problems: list[str] = []
    _state.write_json(queue_path, queue_doc)
    # Written from here on: a later failure is reported rather than raised.
    try:
        _state.write_json(key_path, {
            "schema": "warrant.blind-queue-key/1",
            "lot_id": lot_id,
            "built_at": stamp.isoformat(),
            "seed_rate": rate,
            "seeded": len(key_rows),
            "population": len(reviewer_rows),
            "shortfall": shortfall,
            "seeds": key_rows,
            "note": "Operator only. The reviewer artifact does not say which items "
                    "are seeded, or how many.",
        })
        key_path.chmod(0o600)
    except OSError as exc:
        problems.append(f"could not write the key: {type(exc).__name__}: {exc}")

    leaked_in_file = leaks(json.loads(queue_path.read_text())["order"])
    if leaked_in_file:
        problems.append(f"the written queue carries {len(leaked_in_file)} leak(s): "
                        f"{leaked_in_file[0]}")

    _cli.say(args, f"queue  {queue_path}")
    _cli.say(args, f"key    {key_path}  (operator only, mode 600)")
    _cli.say(args, f"  {len(reviewer_rows)} position(s): {len(items)} item(s) plus "
                   + _cli.rate(len(key_rows), len(reviewer_rows), "seeded"))
    _cli.say(args, f"  seed rate {rate} read from {seeds_path.name}, not from the warrant")
    _cli.say(args, f"  fields carried: {', '.join(queue_doc['fields'])}")
    _cli.say(args, "  no verdict field, and no seed marker, in the reviewer artifact")
    if shortfall:
        _cli.say(args, f"  SHORTFALL: the rate asks for {wanted} seed(s) and the pool "
                       f"holds {len(pool)}; {shortfall} short, so the recovery count "
                       "rests on a smaller denominator than planned")
    for problem in problems:
        _cli.say(args, f"  problem after writing: {problem}")

    _cli.emit(args, {
        "ok": not problems,
        "queue": str(queue_path),
        "key": str(key_path),
        "lot_id": lot_id,
        "population": len(reviewer_rows),
        "items": len(items),
        "seeds": {"count": len(key_rows), "of": len(reviewer_rows), "rate": rate,
                  "shortfall": shortfall},
        "fields": queue_doc["fields"],
        "leaks": [],
        "problems": problems,
    })
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


def _root(tmp: pathlib.Path, name: str, *, seeds: bool = True) -> pathlib.Path:
    root = tmp / name
    d = _state.state_dir(root, create=True)
    shutil.copy(FIXTURES / "warrant.valid.toml", d / "warrant.toml")
    if seeds:
        shutil.copy(FIXTURES / "seeds.local.json", d / "seeds.local.json")
    return root


def selftest() -> list[tuple[str, bool]]:
    cases: list[tuple[str, bool]] = []
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="warrant-blind-queue-"))
    items = str(FIXTURES / "items.jsonl")
    try:
        root = _root(tmp, "repo")
        code, out, _ = _call("--root", str(root), "--items", items, "--now", NOW)
        cases.append(("builds a queue", code == _cli.OK))
        queue_path = _state.state_dir(root) / "reports" / "2026-08-19-blind-queue.json"
        key_path = _state.state_dir(root) / "reports" / "2026-08-19-blind-queue.key.json"
        queue = json.loads(queue_path.read_text())
        key = json.loads(key_path.read_text())
        cases.append(("the queue holds the items plus the seeds",
                      queue["population"] == 12 + 3 and len(queue["order"]) == 15))
        cases.append(("the seed count follows the side file's rate",
                      key["seeded"] == round(0.25 * 12) == 3))
        cases.append(("the rate is reported with its population",
                      "3 of 15 seeded" in out))

        # The input items carry verdicts; the queue must not.
        raw = queue_path.read_text().lower()
        cases.append(("the input items do carry verdicts",
                      any("verdict" in line.lower()
                          for line in pathlib.Path(items).read_text().splitlines())))
        cases.append(("no verdict field reaches the queue",
                      leaks(queue["order"]) == []))
        cases.append(("the words a verdict arrives as are absent from the file",
                      '"verdict"' not in raw and '"state"' not in raw
                      and '"confidence"' not in raw))
        cases.append(("the queue does not say which items are seeded",
                      "seed" not in raw and "known_bad" not in raw))
        cases.append(("the queue does not say how many are seeded",
                      "seeded" not in raw))
        cases.append(("only allowlisted fields survive",
                      set(queue["fields"]) <= set(ALLOWED)))
        cases.append(("the queue tells the reviewer to record their own call first",
                      "before looking at anything else" in queue["note"]))

        # The key is the operator's, and it is where the answers live.
        cases.append(("the key names the seeded positions",
                      all("position" in row and "expected" in row
                          for row in key["seeds"])))
        cases.append(("the key is mode 600", oct(key_path.stat().st_mode)[-3:] == "600"))
        cases.append(("the key carries the numerator and denominator",
                      key["seeded"] == 3 and key["population"] == 15))

        # Order: reproducible, and not the input order.
        again = _root(tmp, "again")
        code, _, _ = _call("--root", str(again), "--items", items, "--now", NOW)
        queue2 = json.loads((_state.state_dir(again) / "reports"
                             / "2026-08-19-blind-queue.json").read_text())
        cases.append(("the order is reproducible from the salt",
                      [r["id"] for r in queue["order"]]
                      == [r["id"] for r in queue2["order"]]))
        input_ids = [json.loads(line)["id"] for line in
                     pathlib.Path(items).read_text().splitlines() if line.strip()]
        cases.append(("the order is not the panel's order",
                      [r["id"] for r in queue["order"]][:12] != input_ids))
        salted = _root(tmp, "salted")
        doc = json.loads((FIXTURES / "seeds.local.json").read_text())
        doc["salt"] = "a different salt"
        (_state.state_dir(salted) / "seeds.local.json").write_text(json.dumps(doc))
        code, _, _ = _call("--root", str(salted), "--items", items, "--now", NOW)
        queue3 = json.loads((_state.state_dir(salted) / "reports"
                             / "2026-08-19-blind-queue.json").read_text())
        cases.append(("a different salt gives a different order",
                      [r["id"] for r in queue3["order"]]
                      != [r["id"] for r in queue["order"]]))

        # The rate comes from the side file, not the warrant.
        drift = _root(tmp, "drift")
        wpath = _state.state_dir(drift) / "warrant.toml"
        wpath.write_text(wpath.read_text().replace("tolerable_error_rate = 0.05",
                                                  "tolerable_error_rate = 0.5"))
        code, _, _ = _call("--root", str(drift), "--items", items, "--now", NOW)
        key_drift = json.loads((_state.state_dir(drift) / "reports"
                                / "2026-08-19-blind-queue.key.json").read_text())
        cases.append(("changing the warrant's rate does not change the seed count",
                      key_drift["seeded"] == 3))
        loud = _root(tmp, "loud")
        doc = json.loads((FIXTURES / "seeds.local.json").read_text())
        doc["rate"] = 0.08
        (_state.state_dir(loud) / "seeds.local.json").write_text(json.dumps(doc))
        code, _, _ = _call("--root", str(loud), "--items", items, "--now", NOW)
        key_loud = json.loads((_state.state_dir(loud) / "reports"
                               / "2026-08-19-blind-queue.key.json").read_text())
        cases.append(("changing the side file's rate does change the seed count",
                      key_loud["seeded"] == round(0.08 * 12) == 1))

        # The refusal: a queue that would carry a verdict is not written.
        leaky = _root(tmp, "leaky")
        code, out_leak, _ = _call("--root", str(leaky), "--items", items,
                                  "--carry", "verdict", "--now", NOW)
        cases.append(("--carry verdict exits 2", code == _cli.FAILED))
        cases.append(("the refusal names the field and the position",
                      "'verdict'" in out_leak and "position" in out_leak))
        cases.append(("nothing is written on a leak",
                      not (_state.state_dir(leaky) / "reports"
                           / "2026-08-19-blind-queue.json").exists()))
        code, out_leak2, _ = _call("--root", str(leaky), "--items", items,
                                   "--carry", "state", "--now", NOW)
        cases.append(("--carry state exits 2", code == _cli.FAILED))
        code, out_leak3, _ = _call("--root", str(leaky), "--items", items,
                                   "--carry", "defect_class", "--now", NOW)
        cases.append(("--carry defect_class exits 2 as well", code == _cli.FAILED))

        # A verdict hidden in the value of an allowlisted field.
        tainted = tmp / "tainted.jsonl"
        rows = [json.loads(line) for line in
                pathlib.Path(items).read_text().splitlines() if line.strip()]
        rows[0]["id"] = "fail"
        tainted.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        code, out_v, _ = _call("--root", str(leaky), "--items", str(tainted), "--now", NOW)
        cases.append(("a verdict in the value of an allowed field exits 2",
                      code == _cli.FAILED and "reads as a verdict" in out_v))
        rows[0]["id"] = "WEB-5001 (machine verdict: pass)"
        tainted.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
        code, out_v2, _ = _call("--root", str(leaky), "--items", str(tainted), "--now", NOW)
        cases.append(("a verdict mentioned inside a value exits 2",
                      code == _cli.FAILED and "mentions a verdict" in out_v2))
        cases.append(("the leak check passes a clean row",
                      leaks([{"position": 1, "id": "WEB-5001",
                              "surface": "apps/web/page.tsx"}]) == []))

        # A field that is safe is carried.
        code, out_c, _ = _call("--root", str(_root(tmp, "carry")), "--items", items,
                               "--carry", "surface", "--now", NOW)
        cases.append(("--carry surface is allowed", code == _cli.OK))

        # Shortfall is reported rather than silently shrinking the denominator.
        short = _root(tmp, "short")
        doc = json.loads((FIXTURES / "seeds.local.json").read_text())
        doc["rate"] = 0.9
        (_state.state_dir(short) / "seeds.local.json").write_text(json.dumps(doc))
        code, out_s, _ = _call("--root", str(short), "--items", items, "--now", NOW)
        cases.append(("a seed shortfall is reported",
                      code == _cli.OK and "SHORTFALL" in out_s
                      and "smaller denominator" in out_s))

        # Preconditions.
        code, out_ns, _ = _call("--root", str(_root(tmp, "noseed", seeds=False)),
                                "--items", items, "--now", NOW)
        cases.append(("no seed file exits 3",
                      code == _cli.MISSING and "no seed file" in out_ns))
        badrate = _root(tmp, "badrate")
        (_state.state_dir(badrate) / "seeds.local.json").write_text(
            json.dumps({"rate": 1.4, "items": []}))
        code, out_br, _ = _call("--root", str(badrate), "--items", items, "--now", NOW)
        cases.append(("a seed rate outside [0,1) exits 1", code == _cli.ERROR))
        code, _, _ = _call("--root", str(root), "--now", NOW)
        cases.append(("no --items exits 1", code == _cli.ERROR))
        code, _, _ = _call("--root", str(root), "--items", str(tmp / "nope.jsonl"),
                           "--now", NOW)
        cases.append(("an items file that does not exist exits 3", code == _cli.MISSING))
        empty = tmp / "empty.jsonl"
        empty.write_text("")
        code, _, _ = _call("--root", str(root), "--items", str(empty), "--now", NOW)
        cases.append(("an empty queue exits 3", code == _cli.MISSING))
        code, _, _ = _call("--root", str(tmp / "no-warrant"), "--items", items)
        cases.append(("no warrant exits 3", code == _cli.MISSING))
        noid = tmp / "noid.jsonl"
        noid.write_text(json.dumps({"surface": "x"}) + "\n")
        code, out_ni, _ = _call("--root", str(root), "--items", str(noid), "--now", NOW)
        cases.append(("an item with no id exits 1",
                      code == _cli.ERROR and "needs an id" in out_ni))

        code, o, e = _call("--root", str(_root(tmp, "jsonmode")), "--items", items,
                           "--now", NOW, "--json")
        payload = json.loads(o)
        cases.append(("--json puts only JSON on stdout", o.lstrip().startswith("{")))
        cases.append(("the JSON carries no verdict field",
                      "verdict" not in json.dumps(payload).lower().replace(
                          "verdict-leak", "").replace("no verdict", "")))
        cases.append(("the JSON reports the seed count for the operator",
                      payload["seeds"]["count"] == 3 and payload["seeds"]["of"] == 15))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__ or "", main, selftest, extra))
