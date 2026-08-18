#!/usr/bin/env python3
"""Validate classified fields against the taxonomy that governs them.

The class of error this exists for is a value that passes every type check and
every format check while sitting in the wrong field: "Q3" filed as the currency
and "AUD" filed as the period. Both are real members of the vocabulary, so
nothing looks malformed, no parser complains, and the figure that later renders
from the record is wrong in a way no screenshot shows.

The taxonomy is a JSON map of field to {"allowed": [...], "required": bool}. An
empty allowed list means the field is unconstrained rather than closed, so a free
text note can still be declared and still be required. When a value is rejected,
every other field whose vocabulary does contain it is named, because "AUD is not
a period_type" is a report and "AUD is not a period_type, but it is a currency"
is a diagnosis.

Unknown fields are reported but not fatal unless --strict: a record growing a
field the taxonomy has not caught up with is a documentation lag, while a record
whose values are in the wrong fields is a data defect, and treating them alike
would train someone to pass --strict off permanently.
"""

from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import _cli                                                        # noqa: E402
import _state                                                      # noqa: E402


def load_taxonomy(path: pathlib.Path) -> dict[str, dict[str, Any]]:
    data = _state.read_json(path)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: a taxonomy is an object of field -> rules")
    taxonomy: dict[str, dict[str, Any]] = {}
    for field, rules in data.items():
        if not isinstance(rules, dict):
            raise ValueError(f"{path}: field {field!r} must map to an object of rules")
        allowed = rules.get("allowed", [])
        if not isinstance(allowed, list):
            raise ValueError(f"{path}: field {field!r} has a non-list 'allowed'")
        taxonomy[field] = {"allowed": allowed, "required": bool(rules.get("required", False))}
    return taxonomy


def load_records(path: pathlib.Path) -> list[tuple[str, dict[str, Any]]]:
    """Records with a label each, from one JSON file or a directory of them."""
    if not path.exists():
        raise _state.Absent(str(path))
    files = sorted(path.rglob("*.json")) if path.is_dir() else [path]
    out: list[tuple[str, dict[str, Any]]] = []
    for file in files:
        data = _state.read_json(file)
        items = data if isinstance(data, list) else [data]
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                raise ValueError(f"{file}: entry {index} is not a record")
            out.append((f"{file.name}#{index}", item))
    return out


def _elsewhere(taxonomy: dict[str, dict[str, Any]], field: str, value: Any) -> list[str]:
    """Which other fields would have accepted this value."""
    return sorted(other for other, rules in taxonomy.items()
                  if other != field and value in rules["allowed"])


def check_record(taxonomy: dict[str, dict[str, Any]], label: str, record: dict[str, Any],
                 id_field: str, strict: bool) -> tuple[list[dict[str, Any]], list[str]]:
    """Violations for one record, plus the unknown field names it carried."""
    violations: list[dict[str, Any]] = []
    unknown: list[str] = []
    record_id = record.get(id_field, label)

    for field, rules in taxonomy.items():
        if rules["required"] and field not in record:
            violations.append({"record": label, "record_id": record_id, "field": field,
                               "kind": "missing_required", "value": None,
                               "detail": f"required field {field!r} is absent"})

    for field, value in record.items():
        if field == id_field:
            continue
        if field not in taxonomy:
            unknown.append(field)
            if strict:
                violations.append({"record": label, "record_id": record_id, "field": field,
                                   "kind": "unknown_field", "value": value,
                                   "detail": f"field {field!r} is not in the taxonomy"})
            continue
        allowed = taxonomy[field]["allowed"]
        if not allowed:
            continue                              # declared and deliberately unconstrained
        for item in (value if isinstance(value, list) else [value]):
            if isinstance(item, (dict, list)):
                violations.append({"record": label, "record_id": record_id, "field": field,
                                   "kind": "unclassifiable", "value": item,
                                   "detail": f"field {field!r} holds a nested value, which no "
                                             f"vocabulary can classify"})
                continue
            if item in allowed:
                continue
            misfiled = _elsewhere(taxonomy, field, item)
            detail = f"{item!r} is not an allowed {field}"
            if misfiled:
                detail += f", but it is a valid value of {', '.join(misfiled)}"
            violations.append({"record": label, "record_id": record_id, "field": field,
                               "kind": "not_allowed", "value": item,
                               "misfiled_as": misfiled, "detail": detail})
    return violations, unknown


def check(taxonomy: dict[str, dict[str, Any]], records: list[tuple[str, dict[str, Any]]],
          id_field: str = "record_id", strict: bool = False) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []
    unknown: dict[str, int] = {}
    for label, record in records:
        found, names = check_record(taxonomy, label, record, id_field, strict)
        violations.extend(found)
        for name in names:
            unknown[name] = unknown.get(name, 0) + 1
    clean = len(records) - len({v["record"] for v in violations})
    return {
        "records": len(records),
        "clean": clean,
        "fields": len(taxonomy),
        "violations": violations,
        "unknown_fields": unknown,
    }


def main(args: argparse.Namespace) -> int:
    if not args.taxonomy or not args.records:
        # Not argparse-required: --selftest has to run without either of them.
        _cli.say(args, "--taxonomy and --records are both required")
        return _cli.ERROR
    taxonomy = load_taxonomy(pathlib.Path(args.taxonomy).expanduser().resolve())
    records = load_records(pathlib.Path(args.records).expanduser().resolve())
    if not records:
        _cli.say(args, f"no records found under {args.records}")
        return _cli.MISSING

    result = check(taxonomy, records, args.id_field, args.strict)
    result["strict"] = args.strict
    result["generated_at"] = _cli.now(args).isoformat()

    _cli.say(args, f"taxonomy: {result['fields']} field(s) over {result['records']} record(s)")
    _cli.say(args, "clean: " + _cli.rate(result["clean"], result["records"], "records"))
    for violation in result["violations"]:
        _cli.say(args, f"  {violation['kind'].upper()} {violation['record']} "
                       f"({violation['record_id']}): {violation['detail']}")
    if result["unknown_fields"] and not args.strict:
        _cli.say(args, "  fields not in the taxonomy (not fatal without --strict): "
                       + ", ".join(f"{k} x{v}" for k, v in sorted(result["unknown_fields"].items())))
    _cli.emit(args, result)
    return _cli.FAILED if result["violations"] else _cli.OK


def _extra(p: argparse.ArgumentParser) -> None:
    p.add_argument("--taxonomy", help="JSON map of field -> {allowed, required}")
    p.add_argument("--records", help="JSON file of records, or a directory of them")
    p.add_argument("--id-field", default="record_id",
                   help="record key naming the record, excluded from field checks")
    p.add_argument("--strict", action="store_true",
                   help="also fail on a field the taxonomy does not name")


def selftest() -> list[tuple[str, bool]]:
    """Every rule observed rejecting something and observed accepting something."""
    import contextlib
    import io
    import json
    import tempfile

    cases: list[tuple[str, bool]] = []
    fx = (pathlib.Path(__file__).resolve().parent.parent
          / "evals" / "fixtures" / "oracle-assay" / "taxonomy")
    taxonomy = load_taxonomy(fx / "taxonomy.json")

    sound = check(taxonomy, load_records(fx / "records" / "sound.json"))
    cases.append(("a conforming record passes", sound["violations"] == []))
    cases.append(("clean count carries its denominator",
                  sound["clean"] == 1 and sound["records"] == 1))
    cases.append(("an empty allowed list accepts free text", sound["violations"] == []))
    cases.append(("a list field accepts allowed members", sound["violations"] == []))
    cases.append(("the id field is not treated as a classified field",
                  check(taxonomy, load_records(fx / "records" / "sound.json"),
                        strict=True)["violations"] == []))

    misfiled = check(taxonomy, load_records(fx / "records" / "misfiled.json"))
    kinds = {(v["field"], v["kind"]) for v in misfiled["violations"]}
    cases.append(("a value in the wrong field is rejected",
                  ("currency", "not_allowed") in kinds and ("period_type", "not_allowed") in kinds))
    hint = next(v for v in misfiled["violations"] if v["field"] == "currency")
    cases.append(("the rejection names where the value does belong",
                  hint["misfiled_as"] == ["period_type"]
                  and "valid value of period_type" in hint["detail"]))
    orphan = next(v for v in misfiled["violations"] if v["value"] == "provisional")
    cases.append(("a value in no vocabulary gets no misfiled hint",
                  orphan["misfiled_as"] == [] and orphan["field"] == "tags"))
    cases.append(("a list field rejects one bad member and keeps the good one",
                  sum(1 for v in misfiled["violations"] if v["field"] == "tags") == 1))

    missing = check(taxonomy, load_records(fx / "records" / "missing-required.json"))
    cases.append(("an absent required field is rejected",
                  any(v["kind"] == "missing_required" and v["field"] == "period_type"
                      for v in missing["violations"])))
    cases.append(("an optional absent field is not rejected",
                  not any(v["field"] == "unit" for v in missing["violations"])))

    unknown_records = load_records(fx / "records" / "unknown-field.json")
    loose = check(taxonomy, unknown_records)
    cases.append(("an unknown field is reported without --strict",
                  loose["violations"] == [] and loose["unknown_fields"] == {"exchange": 1}))
    tight = check(taxonomy, unknown_records, strict=True)
    cases.append(("--strict turns the unknown field into a violation",
                  any(v["kind"] == "unknown_field" for v in tight["violations"])))
    other_id = check(taxonomy, unknown_records, id_field="pk", strict=True)
    cases.append(("--id-field decides which key is exempt",
                  any(v["field"] == "record_id" for v in other_id["violations"])))

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = pathlib.Path(tmp)
        # A required field with an unconstrained vocabulary is still required.
        (tmp_path / "tax.json").write_text(json.dumps({"note": {"allowed": [], "required": True}}))
        (tmp_path / "rec.json").write_text(json.dumps([{"record_id": "a"}]))
        free = check(load_taxonomy(tmp_path / "tax.json"), load_records(tmp_path / "rec.json"))
        cases.append(("an unconstrained field is still required when declared so",
                      any(v["kind"] == "missing_required" for v in free["violations"])))
        (tmp_path / "rec2.json").write_text(json.dumps([{"record_id": "a", "note": "anything"}]))
        cases.append(("and passes once present",
                      check(load_taxonomy(tmp_path / "tax.json"),
                            load_records(tmp_path / "rec2.json"))["violations"] == []))
        # A nested value cannot be classified by any vocabulary.
        (tmp_path / "rec3.json").write_text(json.dumps([{"currency": {"code": "AUD"}}]))
        nested = check(taxonomy, load_records(tmp_path / "rec3.json"))
        cases.append(("a nested value is unclassifiable",
                      any(v["kind"] == "unclassifiable" for v in nested["violations"])))

        def run(argv: list[str]) -> tuple[int, str]:
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                rc = _cli.entry("selftest", main, None, _extra, argv)
            return rc, err.getvalue()

        rc, _ = run(["--root", tmp, "--taxonomy", str(fx / "taxonomy.json"),
                     "--records", str(fx / "records" / "sound.json"), "--json"])
        cases.append(("a conforming record exits 0 through main", rc == _cli.OK))
        rc, err = run(["--root", tmp, "--taxonomy", str(fx / "taxonomy.json"),
                       "--records", str(fx / "records" / "misfiled.json"), "--json"])
        cases.append(("a misfiled record exits 2 through main", rc == _cli.FAILED))
        cases.append(("the failing run names the field and the value",
                      "currency" in err and "period_type" in err))
        rc, _ = run(["--root", tmp, "--taxonomy", str(fx / "nope.json"),
                     "--records", str(fx / "records" / "sound.json"), "--json"])
        cases.append(("an absent taxonomy exits 3", rc == _cli.MISSING))
        rc, _ = run(["--root", tmp, "--taxonomy", str(fx / "taxonomy.json"),
                     "--records", str(fx / "records" / "nope.json"), "--json"])
        cases.append(("absent records exit 3", rc == _cli.MISSING))
        rc, _ = run(["--root", tmp, "--json"])
        cases.append(("missing arguments exit 1, not 2", rc == _cli.ERROR))
    return cases


if __name__ == "__main__":
    raise SystemExit(_cli.entry(__doc__.splitlines()[0], main, selftest, _extra))
