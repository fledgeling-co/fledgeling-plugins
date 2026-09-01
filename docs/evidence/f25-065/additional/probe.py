#!/usr/bin/env python3
"""Independent F25-065 source-bound scope and mutation probe."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REVIEWED = "68c0c5b74b0d143b8738fc7e1c4283a0e2c89b6c"
SCRIPT = ROOT / "plugins/test-campaign/skills/test-campaign/scripts/vacuity-check.py"


def load_scan(tag: str):
    spec = importlib.util.spec_from_file_location(f"f25_065_additional_{tag}", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def scan_source(scan, source: str, scopes=None, mutators=("store", "record", "apply", "update")):
    with tempfile.TemporaryDirectory(prefix="f25-065-additional-") as directory:
        root = Path(directory)
        (root / "ExampleTests.swift").write_text(source)
        return scan.pass_blind(root, mutators, ("read", "load", "expect"), scopes or [])


def target_scope(scan, source: str, call: str, classification="direct-output"):
    block = scan.swift_body_spans(source)["blocks"][0]
    body = source[block["bodyStart"]:block["end"]]
    offset = body.index(call)
    return {
        "file": "ExampleTests.swift",
        "name": block["name"],
        "bodySHA256": hashlib.sha256(body.encode()).hexdigest(),
        "testEntry": block["testEntry"],
        "callOffset": offset,
        "callSHA256": scan.call_fingerprint(body, offset, offset + len(call)),
        "mutator": call.split("(")[0].split(".")[-1],
        "classification": classification,
        "rationale": "independent exact-call probe",
        "references": [{"path": "unused", "sha256": "0" * 64}],
    }


def helper_scope(scan, source: str, call_text="seed("):
    blocks = scan.swift_body_spans(source)["blocks"]
    helper = source[blocks[0]["bodyStart"]:blocks[0]["end"]]
    caller = source[blocks[1]["bodyStart"]:blocks[1]["end"]]
    target_offset = helper.index("store(")
    caller_offset = caller.index(call_text)
    row = target_scope(scan, source, "store(", "attributed-helper")
    row["callers"] = [{
        "file": "ExampleTests.swift",
        "name": blocks[1]["name"],
        "bodySHA256": hashlib.sha256(caller.encode()).hexdigest(),
        "testEntry": blocks[1]["testEntry"],
        "callOffset": caller_offset,
        "callSHA256": scan.call_fingerprint(
            caller, caller_offset, caller_offset + len(call_text)
        ),
    }]
    assert row["callOffset"] == target_offset
    return row


def current_observations(scan):
    observations = {}

    direct = "@Test func measure() { store() }"
    scope = target_scope(scan, direct, "store(")
    result = scan_source(scan, direct, [scope])
    assert result["mutating"] == 1 and result["scopedOnlyBodies"] == 1
    assert result["findings"] == [] and result["scopeFindings"] == []
    observations["rawDenominatorPreserved"] = True

    posture_drift = direct.replace("@Test ", "")
    result = scan_source(scan, posture_drift, [scope])
    assert result["mutating"] == 1 and result["scopeFindings"] and result["findings"]
    observations["targetTestEntryDriftRejectedOutsideUnchangedBody"] = True

    stale_offset = dict(scope, callOffset=scope["callOffset"] + 1)
    result = scan_source(scan, direct, [stale_offset])
    assert result["scopeFindings"]
    observations["exactCallOffsetRequired"] = True

    trailing = (
        "private func seed(_ body: () -> Void) { store(); body() }\n"
        "@Test func measure() { Fixtures.seed { configure() }; read() }"
    )
    trailing_scope = helper_scope(scan, trailing, "seed {")
    result = scan_source(scan, trailing, [trailing_scope])
    assert result["scopeFindings"] == []
    observations["qualifiedTrailingClosureCallerAccepted"] = True

    before = "private func seed() { store() }\n@Test func measure() { read(); seed() }"
    result = scan_source(scan, before, [helper_scope(scan, before)])
    assert any("no read after" in finding for finding in result["scopeFindings"])
    observations["readerBeforeCallerRejected"] = True

    commented = (
        "private func seed(_ body: () -> Void) { store(); body() }\n"
        "@Test func measure() { /* Fixtures.seed { */ read() }"
    )
    result = scan_source(scan, commented, [helper_scope(scan, commented, "seed {")])
    assert any("named helper call" in finding for finding in result["scopeFindings"])
    observations["nonExecutableCallerSpellingRejected"] = True

    blind_verbs = "@Test func blind() { record(); store(); apply(); update() }"
    result = scan_source(scan, blind_verbs)
    assert result["mutating"] == 1 and result["findings"]
    observations["noGlobalVerbExclusion"] = True
    return observations


def schema_observations(scan):
    with tempfile.TemporaryDirectory(prefix="f25-065-schema-") as directory:
        root = Path(directory)
        producer = root / "producer.swift"
        producer.write_text("producer")
        ref = {"path": "producer.swift", "sha256": hashlib.sha256(b"producer").hexdigest()}
        row = {
            "file": "ExampleTests.swift", "name": "measure", "bodySHA256": "0" * 64,
            "testEntry": True, "callOffset": 0, "callSHA256": "0" * 64,
            "mutator": "store", "classification": "direct-output",
            "rationale": "return contract", "references": [ref],
        }
        cases = {
            "unknownRecordField": {"version": 1, "scopes": [dict(row, surprise=True)]},
            "inapplicableCallersField": {"version": 1, "scopes": [dict(row, callers=[])]},
            "unknownTopLevelField": {"version": 1, "scopes": [row], "extra": True},
        }
        observed = {}
        for name, payload in cases.items():
            assert producer.read_text() == "producer"
            (root / "scopes.json").write_text(json.dumps(payload))
            rows, errors = scan.load_blind_scopes(root, "scopes.json")
            assert rows == [] and errors
            observed[name] = errors
        return observed


def run_mutant(name: str, old: bytes, new: bytes, observation):
    original = SCRIPT.read_bytes()
    assert original.count(old) == 1, name
    mutated = original.replace(old, new)
    outcome = {"name": name, "sourceChanged": mutated != original}
    try:
        SCRIPT.write_bytes(mutated)
        try:
            observation(load_scan(f"mutant_{name}"))
        except AssertionError as error:
            outcome["failedAsRequired"] = True
            outcome["assertion"] = str(error) or "independent assertion failed"
        else:
            raise AssertionError(f"{name} survived its independent observation")
    finally:
        SCRIPT.write_bytes(original)
    assert SCRIPT.read_bytes() == original
    outcome["sourceRestored"] = True
    return outcome


subprocess.check_call(["git", "merge-base", "--is-ancestor", REVIEWED, "HEAD"], cwd=ROOT)
original_bytes = SCRIPT.read_bytes()
original_hash = hashlib.sha256(original_bytes).hexdigest()
scan = load_scan("restored")
observations = current_observations(scan)
schema = schema_observations(scan)


def raw_denominator(scan):
    source = "@Test func measure() { store() }"
    result = scan_source(scan, source, [target_scope(scan, source, "store(")])
    assert result["mutating"] == 1


def exact_offset(scan):
    source = "@Test func measure() { store() }"
    row = target_scope(scan, source, "store(")
    row["callOffset"] += 1
    assert scan_source(scan, source, [row])["scopeFindings"]


def global_verbs(scan):
    result = scan_source(scan, "@Test func blind() { record(); store(); apply(); update() }")
    assert result["mutating"] == 1 and result["findings"]


mutants = [
    run_mutant(
        "drop-raw-mutating-denominator",
        b"            if calls:\n                mutating += 1\n",
        b"            if False and calls:\n                mutating += 1\n",
        raw_denominator,
    ),
    run_mutant(
        "ignore-exact-call-offset",
        b"call[0] == row.get(\"callOffset\") and\n",
        b"row.get(\"callOffset\") >= 0 and\n",
        exact_offset,
    ),
    run_mutant(
        "globally-exclude-four-verbs",
        b"            calls = []\n            for v in mutators:\n",
        b"            calls = []\n            for v in (v for v in mutators if v not in "
        b"{\"record\", \"store\", \"apply\", \"update\"}):\n",
        global_verbs,
    ),
]

assert SCRIPT.read_bytes() == original_bytes
assert hashlib.sha256(SCRIPT.read_bytes()).hexdigest() == original_hash
receipt = {
    "verdict": "PASS",
    "reviewedHead": REVIEWED,
    "sourceSHA256BeforeAndAfter": original_hash,
    "observations": observations,
    "strictSchema": schema,
    "actualSourceMutants": mutants,
    "sourceRestored": True,
}
Path(__file__).with_name("probe.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
