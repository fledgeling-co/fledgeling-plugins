#!/usr/bin/env python3
"""Public-CLI probes for strict blindScopeFile schema refusal."""
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[4]
SCRIPT = ROOT / "plugins/test-campaign/skills/test-campaign/scripts/vacuity-check.py"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_case(scope_value, source: str, scope_payload=None):
    with tempfile.TemporaryDirectory(prefix="f65-primary-cli-") as directory:
        root = Path(directory)
        tests = root / "tests"
        tests.mkdir()
        (tests / "ExampleTests.swift").write_text(source)
        (root / "inventory.json").write_text(json.dumps({"requirement": [
            {"id": "REQ-001", "title": "Counter", "effect": "none"}
        ]}))
        campaign = {
            "testRoot": "tests",
            "blindVocabulary": {
                "only": True,
                "mutators": ["write"],
                "readers": ["read"],
            },
            "blindScopeFile": scope_value,
        }
        (root / "campaign.json").write_text(json.dumps(campaign))
        if scope_payload is not None:
            (root / "producer.swift").write_text("producer contract")
            (root / "scopes.json").write_text(json.dumps(scope_payload))
        result = subprocess.run(
            ["python3", str(SCRIPT), str(root), "--gate"],
            capture_output=True,
            text=True,
            timeout=20,
        )
        output = result.stdout + result.stderr
        return {
            "configuredValue": scope_value,
            "exitCode": result.returncode,
            "output": output,
            "invalidScopeReported": "INVALID SCOPE" in output,
        }


# The body is exactly " write() ", so the real mutator offset is 1. Python
# accepts both JSON booleans as integers, allowing an invalid record to suppress
# the only mutator and clear the public gate.
source = "func testInvalidBooleanScope() { write() }"
body = " write() "
reference = b"producer contract"
call_fingerprint = hashlib.sha256(b"write(").hexdigest()
scope = {
    "file": "ExampleTests.swift",
    "name": "testInvalidBooleanScope",
    "bodySHA256": sha(body.encode()),
    "callOffset": True,
    "callSHA256": call_fingerprint,
    "mutator": "write",
    "classification": "direct-output",
    "rationale": "invalid booleans must be refused",
    "references": [{"path": "producer.swift", "sha256": sha(reference)}],
}
boolean = run_case("scopes.json", source, {"version": True, "scopes": [scope]})
boolean["case"] = "version:true and callOffset:true"
boolean["failOpen"] = (
    boolean["exitCode"] == 0
    and not boolean["invalidScopeReported"]
    and "records=1" in boolean["output"]
    and "direct-output=1" in boolean["output"]
)

# The attributed-helper class is accepted without naming or binding any caller.
# Its sole reference is an unrelated file; no record field can carry a caller
# body/call identity.
helper_scope = dict(
    scope,
    name="seed",
    callOffset=1,
    classification="attributed-helper",
    rationale="claims attribution without naming a caller",
)
helper = run_case(
    "scopes.json",
    "private func seed() { write() }\nfunc testCaller() { seed(); read() }",
    {"version": 1, "scopes": [helper_scope]},
)
helper["case"] = "attributed helper with no named source-bound caller"
helper["failOpen"] = (
    helper["exitCode"] == 0
    and not helper["invalidScopeReported"]
    and "attributed-helper=1" in helper["output"]
)

# A valid clean body isolates configuration validation: each present but invalid
# falsy value is silently treated as absence and the public gate exits zero.
falsy = []
for value in (False, 0, {}, []):
    item = run_case(value, "func testClean() { write(); read() }")
    item["case"] = "falsy configured non-string blindScopeFile"
    item["failOpen"] = item["exitCode"] == 0 and not item["invalidScopeReported"]
    falsy.append(item)

receipt = {
    "reviewedSourceSHA256": sha(SCRIPT.read_bytes()),
    "booleanRecord": boolean,
    "unboundAttributedHelper": helper,
    "falsyConfiguredValues": falsy,
    "invalidBooleanClearsPublicGate": boolean["failOpen"],
    "unboundAttributedHelperClearsPublicGate": helper["failOpen"],
    "allFalsyConfiguredValuesClearPublicGateWithoutDiagnostic": all(
        item["failOpen"] for item in falsy
    ),
}
print(json.dumps(receipt, indent=2))
raise SystemExit(
    0
    if receipt["invalidBooleanClearsPublicGate"]
    and receipt["unboundAttributedHelperClearsPublicGate"]
    and receipt["allFalsyConfiguredValuesClearPublicGateWithoutDiagnostic"]
    else 1
)
