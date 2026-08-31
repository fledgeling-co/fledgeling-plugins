#!/usr/bin/env python3
"""Independent public-CLI faults and valid edges for the F25-065 repair."""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[4]
SCRIPT = ROOT / "plugins/test-campaign/skills/test-campaign/scripts/vacuity-check.py"
SPEC = importlib.util.spec_from_file_location("f65_primary_repair", SCRIPT)
SCAN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCAN)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def invoke(source: str, configured, payload=None):
    with tempfile.TemporaryDirectory(prefix="f65-primary-repair-") as directory:
        root = Path(directory)
        tests = root / "tests"
        tests.mkdir()
        (tests / "ExampleTests.swift").write_text(source)
        (root / "inventory.json").write_text(json.dumps({"requirement": [
            {"id": "REQ-001", "title": "Counter", "effect": "none"}
        ]}))
        (root / "campaign.json").write_text(json.dumps({
            "testRoot": "tests",
            "blindVocabulary": {
                "only": True,
                "mutators": ["write"],
                "readers": ["read"],
            },
            "blindScopeFile": configured,
        }))
        if payload is not None:
            (root / "producer.swift").write_text("producer contract")
            (root / "scopes.json").write_text(json.dumps(payload))
        run = subprocess.run(
            ["python3", str(SCRIPT), str(root), "--gate"],
            capture_output=True,
            text=True,
            timeout=20,
        )
        return {"exitCode": run.returncode, "output": run.stdout + run.stderr}


def base_scope(source: str, name: str, call: str):
    block = next(item for item in SCAN.swift_body_spans(source)["blocks"] if item["name"] == name)
    body = source[block["bodyStart"]:block["end"]]
    offset = body.index(call)
    return {
        "file": "ExampleTests.swift",
        "name": name,
        "bodySHA256": digest(body.encode()),
        "callOffset": offset,
        "callSHA256": SCAN.call_fingerprint(body, offset, offset + len(call)),
        "mutator": "write",
        "classification": "direct-output",
        "rationale": "independent repair probe",
        "references": [{
            "path": "producer.swift",
            "sha256": digest(b"producer contract"),
        }],
    }


blind = "func testBlind() { write() }"
ordinary = base_scope(blind, "testBlind", "write(")
version_bool = invoke(blind, "scopes.json", {"version": True, "scopes": [ordinary]})
offset_bool = invoke(
    blind,
    "scopes.json",
    {"version": 1, "scopes": [dict(ordinary, callOffset=True)]},
)

falsy = []
for value in (False, 0, {}, []):
    result = invoke("func testClean() { write(); read() }", value)
    result["configuredValue"] = value
    falsy.append(result)

helper_source = (
    "private func seed() { write() }\n"
    "func testCaller() { Fixtures.seed(); read() }"
)
helper_scope = base_scope(helper_source, "seed", "write(")
helper_scope["classification"] = "attributed-helper"
caller_block = next(
    item for item in SCAN.swift_body_spans(helper_source)["blocks"]
    if item["name"] == "testCaller"
)
caller_body = helper_source[caller_block["bodyStart"]:caller_block["end"]]
caller_offset = caller_body.index("seed(")
caller = {
    "file": "ExampleTests.swift",
    "name": "testCaller",
    "bodySHA256": digest(caller_body.encode()),
    "callOffset": caller_offset,
    "callSHA256": SCAN.call_fingerprint(
        caller_body, caller_offset, caller_offset + len("seed(")
    ),
}
unbound_helper = invoke(
    helper_source,
    "scopes.json",
    {"version": 1, "scopes": [helper_scope]},
)
valid_helper_scope = dict(helper_scope, callers=[caller])
valid_helper = invoke(
    helper_source,
    "scopes.json",
    {"version": 1, "scopes": [valid_helper_scope]},
)
drifted_helper = invoke(
    helper_source,
    "scopes.json",
    {"version": 1, "scopes": [dict(
        valid_helper_scope,
        callers=[dict(caller, callSHA256="0" * 64)],
    )]},
)

checks = {
    "versionBooleanRejected": version_bool["exitCode"] == 1
        and "must contain version 1" in version_bool["output"],
    "offsetBooleanRejected": offset_bool["exitCode"] == 1
        and "invalid call offset" in offset_bool["output"],
    "falsyConfiguredValuesRejected": all(
        item["exitCode"] == 1
        and "blindScopeFile must be a nonempty string" in item["output"]
        for item in falsy
    ),
    "unboundHelperRejected": unbound_helper["exitCode"] == 1
        and "attributed helper has no bound caller" in unbound_helper["output"],
    "qualifiedValidCallerAccepted": valid_helper["exitCode"] == 0
        and "attributed-helper=1" in valid_helper["output"],
    "callerFingerprintDriftRejected": drifted_helper["exitCode"] == 1
        and "does not bind its named helper call" in drifted_helper["output"],
}
receipt = {
    "reviewedSourceSHA256": digest(SCRIPT.read_bytes()),
    "checks": checks,
    "cases": {
        "versionBoolean": version_bool,
        "offsetBoolean": offset_bool,
        "falsyConfiguredValues": falsy,
        "unboundHelper": unbound_helper,
        "qualifiedValidCaller": valid_helper,
        "driftedCallerFingerprint": drifted_helper,
    },
}
print(json.dumps(receipt, indent=2))
raise SystemExit(0 if all(checks.values()) else 1)
