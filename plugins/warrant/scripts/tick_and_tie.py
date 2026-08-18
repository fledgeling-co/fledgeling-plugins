#!/usr/bin/env python3
"""Recompute every rendered figure from its source record and compare.

Lineage proves a figure has a source. This proves the source says what the
figure says, which is the actual defect class: a page that renders beautifully
and states a number no record supports. The comparison is arithmetic, so it
costs nothing per run and cannot change its mind between runs.

Each figure declares where its value comes from. data-source-ref names the
record, and then either data-source-field names a field on it or
data-source-expr names a computation over it -- sum, count, min, max, avg over a
dotted path, or a two-term ratio, difference, sum or product. Anything a figure
displays that is genuinely derived should say so here, because a figure that
carries a formula gets its arithmetic checked rather than just its digits.

Tolerances are declared in the warrant, never in this file. [oracle.tolerance]
maps a figure id or a source field to one of exact, abs:N, rel:N or pct:N; with
no entry the defaults are exact for integers and 0.005 relative for floats. The
tolerance actually applied travels with every result, because a comparison whose
tolerance a reader has to go and look up is a comparison they will assume.

Magnitude suffixes are deliberately not parsed. "1.2m" could be 1,200,000 or
1.2, and guessing the scale of a rendered number is the exact class of error
this plane exists to catch, so such a figure is reported unresolved instead.
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                        # noqa: E402
import _state                                                      # noqa: E402
import lineage_extract                                             # noqa: E402

DEFAULT_FLOAT_RELATIVE = 0.005

_CLEAN = re.compile(r"[\s,$£€%]|AUD|USD|NZD", re.IGNORECASE)
_NUMBER = re.compile(r"^[+-]?\d+(\.\d+)?([eE][+-]?\d+)?$")
_AGGREGATES = ("sum", "count", "avg", "min", "max")
_BINARY = re.compile(r"^([A-Za-z0-9_.\-]+)\s*([+\-*/])\s*([A-Za-z0-9_.\-]+)$")


class Unresolved(Exception):
    """The figure could not be tied at all -- a different answer from a mismatch."""


# -- rendered values ----------------------------------------------------------

def parse_rendered(text: str | None) -> int | float:
    """Turn displayed text into a number, or raise Unresolved.

    Handles thousands separators, currency marks, percent signs and the
    accounting convention where parentheses mean negative.
    """
    if text is None:
        raise Unresolved("no rendered text")
    raw = text.strip()
    if not raw:
        raise Unresolved("empty rendered text")
    negative = raw.startswith("(") and raw.endswith(")")
    if negative:
        raw = raw[1:-1]
    cleaned = _CLEAN.sub("", raw)
    if not _NUMBER.match(cleaned):
        raise Unresolved(f"cannot read a number from {text.strip()!r}")
    value: int | float = int(cleaned) if re.match(r"^[+-]?\d+$", cleaned) else float(cleaned)
    return -value if negative else value


# -- source records -----------------------------------------------------------

def load_sources(path: pathlib.Path) -> dict[str, Any]:
    """Records by id: one JSON file per record in a directory, or one file of many."""
    if not path.exists():
        raise _state.Absent(str(path))
    records: dict[str, Any] = {}
    if path.is_dir():
        for file in sorted(path.rglob("*.json")):
            data = _state.read_json(file)
            key = data.get("id") if isinstance(data, dict) and isinstance(data.get("id"), str) \
                else file.stem
            records[key] = data
        return records

    data = _state.read_json(path)
    if isinstance(data, list):
        for item in data:
            if not isinstance(item, dict) or "id" not in item:
                raise Unresolved(f"{path}: every record in a list needs an id")
            records[str(item["id"])] = item
    elif isinstance(data, dict) and data and all(isinstance(v, dict) for v in data.values()):
        records.update({str(k): v for k, v in data.items()})
    elif isinstance(data, dict):
        records[str(data.get("id", path.stem))] = data
    else:
        raise Unresolved(f"{path}: not a record, a list of records, or a map of them")
    return records


def resolve_path(record: Any, dotted: str) -> Any:
    """Walk a dotted path, mapping over any list it meets."""
    current = record
    for part in dotted.split("."):
        if isinstance(current, list):
            current = [item.get(part) if isinstance(item, dict) else None for item in current]
            continue
        if not isinstance(current, dict) or part not in current:
            raise Unresolved(f"no field {dotted!r} on the record")
        current = current[part]
    return current


def _numbers(value: Any, dotted: str) -> list[float]:
    items = value if isinstance(value, list) else [value]
    out = []
    for item in items:
        if isinstance(item, bool) or not isinstance(item, (int, float)):
            raise Unresolved(f"{dotted!r} holds a non-numeric member {item!r}")
        out.append(item)
    return out


def _term(record: Any, token: str) -> float:
    if _NUMBER.match(token):
        return float(token)
    value = resolve_path(record, token)
    return _numbers(value, token)[0]


def recompute(record: Any, expr: str) -> int | float:
    """Evaluate one declared expression over a source record.

    Deliberately a fixed grammar rather than eval(): a verification tool that
    executes strings from the surface under test is not a verification tool.
    """
    expr = expr.strip()
    for name in _AGGREGATES:
        if expr.startswith(f"{name}(") and expr.endswith(")"):
            inner = expr[len(name) + 1:-1].strip()
            value = resolve_path(record, inner)
            if name == "count":
                return len(value) if isinstance(value, list) else 1
            series = _numbers(value, inner)
            if not series:
                raise Unresolved(f"{inner!r} is empty, so {name}() has no value")
            if name == "sum":
                return sum(series)
            if name == "avg":
                return sum(series) / len(series)
            return min(series) if name == "min" else max(series)

    if expr.startswith("pct(") and expr.endswith(")"):
        body = expr[4:-1]
        match = _BINARY.match(body)
        if not match or match.group(2) != "/":
            raise Unresolved(f"pct() takes a/b, got {body!r}")
        left, right = _term(record, match.group(1)), _term(record, match.group(3))
        if right == 0:
            raise Unresolved("pct() divides by zero")
        return 100.0 * left / right

    match = _BINARY.match(expr)
    if match:
        left, op, right = _term(record, match.group(1)), match.group(2), _term(record, match.group(3))
        if op == "+":
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if right == 0:
            raise Unresolved("expression divides by zero")
        return left / right

    value = resolve_path(record, expr)
    return _numbers(value, expr)[0]


# -- tolerances ---------------------------------------------------------------

def parse_tolerance(spec: Any) -> tuple[str, float]:
    """One declared tolerance as (kind, magnitude)."""
    if isinstance(spec, bool):
        raise Unresolved(f"a boolean is not a tolerance: {spec!r}")
    if isinstance(spec, (int, float)):
        return ("rel", float(spec))
    text = str(spec).strip().lower()
    if text == "exact":
        return ("exact", 0.0)
    for kind in ("abs", "rel", "pct"):
        if text.startswith(f"{kind}:"):
            try:
                magnitude = float(text.split(":", 1)[1])
            except ValueError as exc:
                raise Unresolved(f"unreadable tolerance {spec!r}") from exc
            return ("rel", magnitude / 100.0) if kind == "pct" else (kind, magnitude)
    raise Unresolved(f"unknown tolerance {spec!r}; use exact, abs:N, rel:N or pct:N")


def tolerance_for(table: dict[str, Any], figure_id: str, field: str | None,
                  source_value: Any) -> tuple[str, float, str]:
    """The tolerance to apply, and where it came from, in that order of precedence."""
    for key, why in ((figure_id, f"warrant: figure {figure_id}"),
                     (field, f"warrant: field {field}")):
        if key and key in table:
            kind, magnitude = parse_tolerance(table[key])
            return kind, magnitude, why

    integral = isinstance(source_value, int) and not isinstance(source_value, bool)
    if integral:
        spec = table.get("default_integer", "exact")
        kind, magnitude = parse_tolerance(spec)
        return kind, magnitude, ("warrant: default_integer" if "default_integer" in table
                                 else "default for integers")
    spec = table.get("default_float_relative", DEFAULT_FLOAT_RELATIVE)
    kind, magnitude = parse_tolerance(spec)
    return kind, magnitude, ("warrant: default_float_relative"
                             if "default_float_relative" in table else "default for floats")


def describe_tolerance(kind: str, magnitude: float, why: str) -> str:
    return f"{'exact' if kind == 'exact' else f'{kind}:{magnitude:g}'} ({why})"


def within(rendered: float, source: float, kind: str, magnitude: float) -> bool:
    if kind == "exact":
        return rendered == source
    delta = abs(rendered - source)
    if kind == "abs":
        return delta <= magnitude
    if source == 0:
        # A relative tolerance around zero admits everything, so it admits nothing.
        return rendered == 0
    return delta <= magnitude * abs(source)


# -- the check ----------------------------------------------------------------

def tie(figures: list[dict[str, Any]], records: dict[str, Any],
        tolerance_table: dict[str, Any], skip_unsourced: bool = False) -> dict[str, Any]:
    """Compare every figure with its source. Returns the report; judges nothing."""
    results: list[dict[str, Any]] = []
    for figure in figures:
        row: dict[str, Any] = {
            "id": figure["id"],
            "file": figure.get("file"),
            "line": figure.get("line"),
            "source": figure.get("source"),
            "basis": figure.get("expr") or figure.get("field") or "value",
            "rendered": None,
            "source_value": None,
            "tolerance": None,
            "status": "tied",
            "detail": "",
        }
        if not figure.get("source"):
            if skip_unsourced:
                row["status"] = "skipped"
                row["detail"] = "no source ref; lineage_gate owns this one"
                results.append(row)
                continue
            row["status"] = "unresolved"
            row["detail"] = "no source ref, so the figure cannot be tied to anything"
            results.append(row)
            continue
        try:
            record = records.get(figure["source"])
            if record is None:
                raise Unresolved(f"no source record {figure['source']!r}")
            # data-value wins over the text when present: a formatted render
            # ("1.2m") can be unreadable while the element still carries the number.
            rendered = parse_rendered(figure.get("value") or figure.get("text"))
            expected = recompute(record, figure["expr"]) if figure.get("expr") \
                else recompute(record, figure.get("field") or "value")
            kind, magnitude, why = tolerance_for(tolerance_table, figure["id"],
                                                 figure.get("field"), expected)
            row["rendered"] = rendered
            row["source_value"] = expected
            row["tolerance"] = describe_tolerance(kind, magnitude, why)
            if not within(float(rendered), float(expected), kind, magnitude):
                row["status"] = "mismatch"
                row["detail"] = (f"rendered {rendered!r}, source {expected!r}, "
                                 f"tolerance {row['tolerance']}")
        except Unresolved as exc:
            row["status"] = "unresolved"
            row["detail"] = str(exc)
        results.append(row)

    return {
        "figures": results,
        "mismatches": [r for r in results if r["status"] == "mismatch"],
        "unresolved": [r for r in results if r["status"] == "unresolved"],
        "checked": sum(1 for r in results if r["status"] != "skipped"),
        "tied": sum(1 for r in results if r["status"] == "tied"),
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
    }


def tolerance_table(root: pathlib.Path) -> tuple[dict[str, Any], str]:
    """[oracle.tolerance] from the warrant, or the documented defaults."""
    try:
        warrant = _state.read_warrant(root)
    except _state.Absent:
        return {}, "no warrant; using built-in defaults"
    table = warrant.get("oracle", {}).get("tolerance", {})
    return dict(table), f"warrant {warrant.get('version', '(unversioned)')}"


def main(args: argparse.Namespace) -> int:
    root = pathlib.Path(args.root).expanduser().resolve()
    if not args.sources:
        # argparse cannot mark this required: --selftest has to run without it.
        _cli.say(args, "--sources is required (a directory of JSON source records)")
        return _cli.ERROR
    records = load_sources(pathlib.Path(args.sources).expanduser().resolve())

    if args.report:
        report = _state.read_json(pathlib.Path(args.report).expanduser().resolve())
    else:
        target = pathlib.Path(args.input).expanduser().resolve() if args.input else root
        paths = lineage_extract.surfaces_for(target, args.glob)
        if not paths:
            _cli.say(args, f"no files matching {args.glob} under {target}")
            return _cli.MISSING
        report = lineage_extract.extract(paths, root if target.is_dir() else None)

    table, provenance = tolerance_table(root)
    result = tie(report["figures"], records, table, args.skip_unsourced)
    result["tolerance_source"] = provenance
    result["records"] = len(records)
    result["generated_at"] = _cli.now(args).isoformat()

    _cli.say(args, f"tick and tie against {len(records)} source record(s); "
                   f"tolerances from {provenance}")
    _cli.say(args, "tied: " + _cli.rate(result["tied"], result["checked"], "figures checked"))
    for row in result["mismatches"]:
        _cli.say(args, f"  MISMATCH {row['id']} ({row['file']}:{row['line']}, "
                       f"{row['basis']}): {row['detail']}")
    for row in result["unresolved"]:
        _cli.say(args, f"  UNRESOLVED {row['id']} ({row['file']}:{row['line']}): {row['detail']}")
    _cli.emit(args, result)
    return _cli.FAILED if (result["mismatches"] or result["unresolved"]) else _cli.OK


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--sources",
                   help="directory of JSON source records, or one file holding many")
    p.add_argument("--input", help="HTML file or directory of them (default: --root)")
    p.add_argument("--glob", default="*.html", help="filename pattern when --input is a directory")
    p.add_argument("--report", help="a lineage_extract JSON report to tie instead of re-walking")
    p.add_argument("--skip-unsourced", action="store_true",
                   help="leave unsourced figures to lineage_gate instead of failing here")


def selftest() -> list[tuple[str, bool]]:
    """Every rule twice: once tying, once not."""
    import contextlib
    import io
    import shutil
    import tempfile

    cases: list[tuple[str, bool]] = []
    fx = (pathlib.Path(__file__).resolve().parent.parent
          / "evals" / "fixtures" / "oracle-assay")
    tick, lineage = fx / "tick", fx / "lineage"
    records = load_sources(tick / "sources")
    filing = records["filing-2026-q3"]

    # -- rendered-value parsing, both directions
    cases.append(("currency and separators parse", parse_rendered("$1,204,000") == 1204000))
    cases.append(("a percent parses as a float", parse_rendered("18.4%") == 18.4))
    cases.append(("parentheses mean negative", parse_rendered("(88,000)") == -88000))
    for label, text in (("a magnitude suffix is refused, not guessed", "1.204m"),
                        ("empty text is unresolved", "   "),
                        ("prose is unresolved", "n/a")):
        try:
            parse_rendered(text)
            cases.append((label, False))
        except Unresolved:
            cases.append((label, True))

    # -- recompute, both directions
    cases.append(("a bare field resolves", recompute(filing, "revenue") == 1204000))
    cases.append(("sum over a path recomputes", recompute(filing, "sum(segments.amount)") == 1204000))
    cases.append(("count over a path recomputes", recompute(filing, "count(segments)") == 2))
    cases.append(("a ratio recomputes",
                  abs(recompute(filing, "pct(npat_loss/revenue)") + 7.3089700996677) < 1e-9))
    for label, expr in (("an unknown field is unresolved", "no_such_field"),
                        ("a non-numeric member is unresolved", "segments.name"),
                        ("a malformed expression is unresolved", "sum(")):
        try:
            recompute(filing, expr)
            cases.append((label, False))
        except Unresolved:
            cases.append((label, True))

    # -- tolerance parsing and resolution
    cases.append(("exact parses", parse_tolerance("exact") == ("exact", 0.0)))
    cases.append(("abs parses", parse_tolerance("abs:1") == ("abs", 1.0)))
    cases.append(("pct becomes relative", parse_tolerance("pct:0.5") == ("rel", 0.005)))
    try:
        parse_tolerance("within a bit")
        cases.append(("an unknown tolerance form is refused", False))
    except Unresolved:
        cases.append(("an unknown tolerance form is refused", True))
    cases.append(("integers default to exact",
                  tolerance_for({}, "headcount", "headcount", 312)[0] == "exact"))
    cases.append(("floats default to 0.005 relative",
                  tolerance_for({}, "margin", "margin", 18.4)[:2] == ("rel", 0.005)))
    cases.append(("a warrant entry outranks the default",
                  tolerance_for({"margin": "rel:0.0001"}, "margin", "margin", 18.4)[1] == 0.0001))
    cases.append(("a figure id outranks a field",
                  tolerance_for({"margin": "abs:9", "npat-loss": "exact"},
                                "npat-loss", "margin", 1.0)[0] == "exact"))
    cases.append(("relative around zero demands exact",
                  within(0.001, 0.0, "rel", 0.5) is False and within(0.0, 0.0, "rel", 0.5) is True))

    # -- the check itself, on the sound and the drifted render
    sound = lineage_extract.extract([tick / "render" / "sound.html"])
    drift = lineage_extract.extract([tick / "render" / "drift.html"])

    ok = tie(sound["figures"], records, {})
    by_id = {r["id"]: r for r in ok["figures"]}
    cases.append(("a sound render ties completely",
                  ok["mismatches"] == [] and ok["unresolved"] == [] and ok["tied"] == 6))
    cases.append(("an exact integer ties", by_id["revenue-total"]["status"] == "tied"))
    cases.append(("a float inside the default tolerance ties",
                  by_id["margin"]["status"] == "tied" and by_id["margin"]["rendered"] == 18.42))
    cases.append(("an accounting negative ties",
                  by_id["npat-loss"]["source_value"] == -88000))
    cases.append(("a recomputed sum ties", by_id["segment-sum"]["status"] == "tied"))
    cases.append(("every result names the tolerance applied",
                  all(r["tolerance"] for r in ok["figures"])))

    bad = tie(drift["figures"], records, {})
    bad_by_id = {r["id"]: r for r in bad["figures"]}
    cases.append(("an off-by-one integer is a mismatch",
                  bad_by_id["headcount"]["status"] == "mismatch"))
    cases.append(("the mismatch names rendered, source and tolerance",
                  "rendered 313" in bad_by_id["headcount"]["detail"]
                  and "source 312" in bad_by_id["headcount"]["detail"]
                  and "exact" in bad_by_id["headcount"]["detail"]))
    cases.append(("a float outside tolerance is a mismatch",
                  bad_by_id["margin"]["status"] == "mismatch"))
    cases.append(("a recomputed count that disagrees is a mismatch",
                  bad_by_id["segment-count"]["status"] == "mismatch"))
    cases.append(("an unreadable render is unresolved, not tied",
                  bad_by_id["npat-loss"]["status"] == "unresolved"))
    cases.append(("a missing source record is unresolved",
                  bad_by_id["guidance-fy27"]["status"] == "unresolved"
                  and "nope-2026" in bad_by_id["guidance-fy27"]["detail"]))
    cases.append(("the figure that does tie is left alone",
                  bad_by_id["revenue-total"]["status"] == "tied"))

    # -- a declared tolerance changes the verdict in both directions
    table = {"margin": "rel:0.0001", "headcount": "abs:1"}
    tightened = {r["id"]: r for r in tie(sound["figures"], records, table)["figures"]}
    cases.append(("a tightened warrant tolerance turns a tie into a mismatch",
                  tightened["margin"]["status"] == "mismatch"))
    widened = {r["id"]: r for r in tie(drift["figures"], records, table)["figures"]}
    cases.append(("a widened warrant tolerance turns a mismatch into a tie",
                  widened["headcount"]["status"] == "tied"))
    cases.append(("the applied tolerance says it came from the warrant",
                  "warrant: figure headcount" in widened["headcount"]["tolerance"]))

    # -- unsourced figures: failed by default, deferred on request
    gap = lineage_extract.extract([lineage / "unsourced" / "kpi.html"])
    default_gap = {r["id"]: r for r in tie(gap["figures"], records, {})["figures"]}
    cases.append(("an unsourced figure is unresolved by default",
                  all(default_gap[i]["status"] == "unresolved"
                      and "no source ref" in default_gap[i]["detail"]
                      for i in ("guidance-fy27", "npat"))))
    deferred = {r["id"]: r for r in
                tie(gap["figures"], records, {}, skip_unsourced=True)["figures"]}
    cases.append(("--skip-unsourced defers it to lineage_gate",
                  all(deferred[i]["status"] == "skipped" for i in ("guidance-fy27", "npat"))))
    cases.append(("a sourced figure naming no field is still unresolved",
                  default_gap["revenue-total"]["status"] == "unresolved"))

    # -- through main(), including the warrant read and the absent-sources path
    def run(argv: list[str]) -> tuple[int, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            rc = _cli.entry("selftest", main, None, _extra, argv)
        return rc, err.getvalue()

    with tempfile.TemporaryDirectory() as tmp:
        rc, _ = run(["--root", tmp, "--sources", str(tick / "sources"),
                     "--input", str(tick / "render" / "sound.html"), "--json"])
        cases.append(("a sound render exits 0 through main", rc == _cli.OK))
        rc, err = run(["--root", tmp, "--sources", str(tick / "sources"),
                       "--input", str(tick / "render" / "drift.html"), "--json"])
        cases.append(("a drifted render exits 2 through main", rc == _cli.FAILED))
        cases.append(("the failing run names the figure", "headcount" in err))

        # The same sound render fails once the warrant tightens margin.
        state = _state.state_dir(tmp, create=True)
        shutil.copyfile(tick / "warrant-tolerance.toml", state / "warrant.toml")
        rc, err = run(["--root", tmp, "--sources", str(tick / "sources"),
                       "--input", str(tick / "render" / "sound.html"), "--json"])
        cases.append(("the warrant's tolerance is read and applied by main",
                      rc == _cli.FAILED and "margin" in err))

        rc, _ = run(["--root", tmp, "--sources", str(tick / "no-such-dir"),
                     "--input", str(tick / "render" / "sound.html"), "--json"])
        cases.append(("absent sources exit 3", rc == _cli.MISSING))
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__.splitlines()[0], main, selftest, _extra))
