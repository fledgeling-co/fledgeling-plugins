#!/usr/bin/env python3
"""Distinct additional probes for F25-065 terminal-helper repair 42ac3ea."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TARGET = "42ac3ea7aeff2c1a2db23ea83121a2f762839f1f"
SCRIPT_REL = "plugins/test-campaign/skills/test-campaign/scripts/vacuity-check.py"


def git_show(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{TARGET}:{path}"], cwd=ROOT)


source_bytes = git_show(SCRIPT_REL)
source_sha = hashlib.sha256(source_bytes).hexdigest()
exact_root = Path(tempfile.mkdtemp(prefix="f25-065-additional-r12-exact-"))
exact_script = exact_root / SCRIPT_REL
exact_script.parent.mkdir(parents=True)
exact_script.write_bytes(source_bytes)
spec = importlib.util.spec_from_file_location("f25_065_additional_r11", exact_script)
scan = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(scan)


def scope_for(source: str, helper_call: str = "seed(") -> dict:
    blocks = scan.swift_body_spans(source)["blocks"]
    helper_block = next(block for block in blocks if block["name"] == "seed")
    caller_block = next(block for block in blocks if block["name"] != "seed")
    helper = source[helper_block["bodyStart"]:helper_block["end"]]
    caller = source[caller_block["bodyStart"]:caller_block["end"]]
    target_offset = helper.index("store(")
    caller_offset = caller.index(helper_call)
    return {
        "file": "ExampleTests.swift",
        "name": "seed",
        "bodySHA256": hashlib.sha256(helper.encode()).hexdigest(),
        "testEntry": helper_block["testEntry"],
        "callOffset": target_offset,
        "callSHA256": scan.call_fingerprint(
            helper, target_offset, target_offset + len("store(")),
        "mutator": "store",
        "classification": "attributed-helper",
        "rationale": "bound caller must execute a later observation",
        "references": [],
        "callers": [{
            "file": "ExampleTests.swift",
            "name": caller_block["name"],
            "bodySHA256": hashlib.sha256(caller.encode()).hexdigest(),
            "testEntry": caller_block["testEntry"],
            "callOffset": caller_offset,
            "callSHA256": scan.call_fingerprint(
                caller, caller_offset, caller_offset + len(helper_call)),
        }],
    }


def direct(source: str, helper_call: str = "seed(") -> dict:
    with tempfile.TemporaryDirectory(prefix="f25-065-additional-r12-direct-") as directory:
        root = Path(directory)
        (root / "ExampleTests.swift").write_text(source)
        result = scan.pass_blind(root, ("store",), ("read",), [scope_for(source, helper_call)])
        return {
            "scopeFindings": result["scopeFindings"],
            "scopedCounts": result["scopedCounts"],
            "mutating": result["mutating"],
        }


def public_cli(source: str, helper_call: str = "seed(") -> dict:
    with tempfile.TemporaryDirectory(prefix="f25-065-additional-r12-cli-") as directory:
        root = Path(directory)
        tests = root / "tests"
        tests.mkdir()
        (tests / "ExampleTests.swift").write_text(source)
        producer = b"current producer contract\n"
        (root / "producer.swift").write_bytes(producer)
        (root / "inventory.json").write_text(json.dumps({
            "requirement": [{"id": "REQ-001", "title": "Observation", "effect": "none"}]
        }))
        row = scope_for(source, helper_call)
        row["references"] = [{
            "path": "producer.swift", "sha256": hashlib.sha256(producer).hexdigest()
        }]
        (root / "scopes.json").write_text(json.dumps({"version": 1, "scopes": [row]}))
        (root / "campaign.json").write_text(json.dumps({
            "testRoot": "tests",
            "blindVocabulary": {"only": True, "mutators": ["store"], "readers": ["read"]},
            "blindScopeFile": "scopes.json",
        }))
        run = subprocess.run(
            ["python3", str(exact_script), str(root), "--gate"],
            capture_output=True, text=True, timeout=30,
        )
        return {
            "exit": run.returncode,
            "invalidScope": "INVALID SCOPE" in run.stdout,
            "outputTail": "\n".join(run.stdout.splitlines()[-8:]),
        }


cases = {
    "returnSameLine": (
        "private func seed() -> Int { store(); return 7 }\n"
        "@Test func measure() -> Int { return seed(); read(); return 0 }", "seed("),
    "returnNewline": (
        "private func seed() -> Int { store(); return 7 }\n"
        "@Test func measure() -> Int { return\n seed(); read(); return 0 }", "seed("),
    "returnCommentNewline": (
        "private func seed() -> Int { store(); return 7 }\n"
        "@Test func measure() -> Int { return /* continued */\n seed(); read(); return 0 }", "seed("),
    "throwSameLine": (
        "private func seed() -> Error { store(); return Failure() }\n"
        "@Test func measure() throws { throw seed(); read() }", "seed("),
    "throwNewline": (
        "private func seed() -> Error { store(); return Failure() }\n"
        "@Test func measure() throws { throw\n seed(); read() }", "seed("),
    "directHelperThenReader": (
        "private func seed() { store() }\n@Test func measure() { seed(); read() }", "seed("),
    "balancedNestedArgumentsThenReader": (
        "private func seed(_ value: Int) { store() }\n"
        "@Test func measure() { seed(wrapper(value: (1 + 2))); read() }", "seed("),
    "argumentReaderOnly": (
        "private func seed(_ value: Int) { store() }\n"
        "@Test func measure() { seed(wrapper(value: read())) }", "seed("),
    "unparenthesizedTrailing": (
        "private func seed(_ body: () -> Void) { store(); body() }\n"
        "@Test func measure() { seed { read() } }", "seed {"),
    "parenthesizedTrailing": (
        "private func seed(_ body: () -> Void = {}) { store(); body() }\n"
        "@Test func measure() { seed() {}; read() }", "seed("),
    "qualifiedParenthesizedTrailing": (
        "private func seed(_ body: () -> Void = {}) { store(); body() }\n"
        "@Test func measure() { Fixtures.seed() {}; read() }", "seed("),
    "commentSeparatedTrailing": (
        "private func seed(_ body: () -> Void = {}) { store(); body() }\n"
        "@Test func measure() { seed() /* comment */ {}; read() }", "seed("),
    "newlineTrailing": (
        "private func seed(_ body: () -> Void = {}) { store(); body() }\n"
        "@Test func measure() { seed()\n {}; read() }", "seed("),
    "multipleTrailing": (
        "private func seed(_ first: () -> Void = {}, second: () -> Void) { store(); second() }\n"
        "@Test func measure() { seed() {} second: {}; read() }", "seed("),
    "nestedFalseHelperThenReader": (
        "private func seed() { store() }\n"
        "@Test func measure() { if false { seed() }; read() }", "seed("),
}

observed = {}
for name, (source, helper_call) in cases.items():
    observed[name] = {
        "source": source,
        "direct": direct(source, helper_call),
        "publicCLI": public_cli(source, helper_call),
    }

assert observed["returnSameLine"]["publicCLI"]["exit"] == 1
assert observed["returnNewline"]["publicCLI"]["exit"] == 0
assert observed["returnCommentNewline"]["publicCLI"]["exit"] == 0
assert observed["throwSameLine"]["publicCLI"]["exit"] == 1
assert observed["throwNewline"]["publicCLI"]["exit"] == 0
assert observed["directHelperThenReader"]["publicCLI"]["exit"] == 0
assert observed["balancedNestedArgumentsThenReader"]["publicCLI"]["exit"] == 0
assert observed["argumentReaderOnly"]["publicCLI"]["exit"] == 1
for trailing in ("unparenthesizedTrailing", "parenthesizedTrailing",
                 "qualifiedParenthesizedTrailing", "commentSeparatedTrailing",
                 "newlineTrailing", "multipleTrailing"):
    assert observed[trailing]["publicCLI"]["exit"] == 1
assert observed["nestedFalseHelperThenReader"]["publicCLI"]["exit"] == 1

result = {
    "verdict": "FAIL",
    "reviewedImplementation": TARGET,
    "scannerSHA256": source_sha,
    "blocker": (
        "The helper terminator guard splits the statement on newlines, so return or throw on the preceding line is lost before the helper call. The balanced later-reader tail then credits an unreachable reader."
    ),
    "cases": observed,
    "sourceRestored": hashlib.sha256(source_bytes).hexdigest() == source_sha,
    "mutationLocation": "git-show bytes loaded into temporary directories; shared source untouched",
}
Path(__file__).with_name("probe.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
