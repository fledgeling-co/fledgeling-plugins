#!/usr/bin/env python3
"""Repeated distinct additional F25-065 probes against exact repaired implementation 6f80131."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TARGET = "6f8013101300cc08da0b51d64f58755eb81fa248"
SCRIPT_REL = "plugins/test-campaign/skills/test-campaign/scripts/vacuity-check.py"
TEST_REL = "plugins/test-campaign/tests/test_swift_bodies.py"


def git_show(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{TARGET}:{path}"], cwd=ROOT)


source_bytes = git_show(SCRIPT_REL)
test_bytes = git_show(TEST_REL)
source_sha = hashlib.sha256(source_bytes).hexdigest()


def load_module(path: Path, tag: str):
    spec = importlib.util.spec_from_file_location(f"f25_065_additional_{tag}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


exact_root = Path(tempfile.mkdtemp(prefix="f25-065-additional-exact-"))
exact_script = exact_root / SCRIPT_REL
exact_script.parent.mkdir(parents=True)
exact_script.write_bytes(source_bytes)
scan = load_module(exact_script, "reviewed")


def scope_for(module, source: str, helper_call: str = "seed(") -> dict:
    blocks = module.swift_body_spans(source)["blocks"]
    helper_block = next(block for block in blocks if block["name"] == "seed")
    caller_block = next(block for block in blocks if block["name"] == "testMeasure")
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
        "callSHA256": module.call_fingerprint(
            helper, target_offset, target_offset + len("store(")),
        "mutator": "store",
        "classification": "attributed-helper",
        "rationale": "bound caller must execute a later observation",
        "references": [],
        "callers": [{
            "file": "ExampleTests.swift",
            "name": "testMeasure",
            "bodySHA256": hashlib.sha256(caller.encode()).hexdigest(),
            "testEntry": caller_block["testEntry"],
            "callOffset": caller_offset,
            "callSHA256": module.call_fingerprint(
                caller, caller_offset, caller_offset + len(helper_call)),
        }],
    }


def direct(source: str, helper_call: str = "seed(") -> dict:
    with tempfile.TemporaryDirectory(prefix="f25-065-additional-direct-") as directory:
        root = Path(directory)
        (root / "ExampleTests.swift").write_text(source)
        return scan.pass_blind(root, ("store",), ("read",),
                               [scope_for(scan, source, helper_call)])


def cli(source: str, helper_call: str = "seed(", transform=None) -> dict:
    with tempfile.TemporaryDirectory(prefix="f25-065-additional-cli-") as directory:
        root = Path(directory)
        tests = root / "tests"
        tests.mkdir()
        (tests / "ExampleTests.swift").write_text(source)
        (root / "producer.swift").write_text("current producer contract\n")
        (root / "inventory.json").write_text(json.dumps({
            "requirement": [{"id": "REQ-001", "title": "Observation", "effect": "none"}]
        }))
        row = scope_for(scan, source, helper_call)
        row["references"] = [{
            "path": "producer.swift",
            "sha256": hashlib.sha256(b"current producer contract\n").hexdigest(),
        }]
        payload = {"version": 1, "scopes": [row]}
        if transform is not None:
            payload = transform(payload)
        (root / "scopes.json").write_text(json.dumps(payload))
        (root / "campaign.json").write_text(json.dumps({
            "testRoot": "tests",
            "blindVocabulary": {"only": True, "mutators": ["store"], "readers": ["read"]},
            "blindScopeFile": "scopes.json",
        }))
        result = subprocess.run(
            ["python3", str(exact_script), str(root), "--gate"],
            capture_output=True, text=True, timeout=30,
        )
        return {"exitCode": result.returncode, "stdout": result.stdout,
                "stderr": result.stderr}


sources = {
    "storedClosureNeverInvoked": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed(); let observation = { read() }; _ = observation }",
        "seed(",
    ),
    "storedClosureInvoked": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed(); let observation = { read() }; _ = observation() }",
        "seed(",
    ),
    "helperTrailingClosure": (
        "private func seed(_ body: () -> Void) { store(); body() }\n"
        "func testMeasure() { Fixtures.seed { configure() }; read() }",
        "seed {",
    ),
    "configuredReaderTrailingClosure": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed(); read { configure() } }",
        "seed(",
    ),
    "parenthesizedReader": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed(); read() }",
        "seed(",
    ),
    "readerOnlyBeforeHelper": (
        "private func seed() { store() }\n"
        "func testMeasure() { read(); seed() }",
        "seed(",
    ),
    "unreachableFalseBranch": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed(); if false { read() } }",
        "seed(",
    ),
    "inactiveCompilationBranch": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed()\n#if false\nread()\n#endif\n}",
        "seed(",
    ),
    "missingModuleCompilationBranch": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed()\n#if canImport(DefinitelyMissingF25065Module)\n"
        "read()\n#endif\n}",
        "seed(",
    ),
    "unicodeLabelReference": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed(); let function = read(λ:) }",
        "seed(",
    ),
    "backtickLabelReference": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed(); let function = read(`repeat`:) }",
        "seed(",
    ),
    "underscoreLabelReference": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed(); let function = read(_:_:)}",
        "seed(",
    ),
    "helperTrailingThenDirectReader": (
        "private func seed(_ body: () -> Void) { store(); body() }\n"
        "func testMeasure() { seed { configure() }; read() }",
        "seed {",
    ),
    "helperTrailingThenNestedReader": (
        "private func seed(_ body: () -> Void) { store(); body() }\n"
        "func testMeasure() { seed { configure() }; if false { read() } }",
        "seed {",
    ),
    "immediatelyInvokedNestedReader": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed(); _ = { read() }() }",
        "seed(",
    ),
    "synchronousDoNestedReader": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed(); do { read() } }",
        "seed(",
    ),
    "nestedHelperCallThenDirectReader": (
        "private func seed() { store() }\n"
        "func testMeasure() { let invoke = { seed() }; _ = invoke; read() }",
        "seed(",
    ),
    "inactiveHelperCallThenDirectReader": (
        "private func seed() { store() }\n"
        "func testMeasure() {\n#if false\nseed()\n#endif\nread()\n}",
        "seed(",
    ),
    "returnBeforeDirectReader": (
        "private func seed() { store() }\n"
        "func testMeasure() { seed(); return; read() }",
        "seed(",
    ),
    "multiTrailingFirstReaderNotInvoked": (
        "private func seed(_ first: () -> Void, second: () -> Void) { store(); second() }\n"
        "func testMeasure() { seed { read() } second: { configure() } }",
        "seed {",
    ),
    "continueBeforeReader": (
        "private func seed() { store() }\n"
        "func testMeasure() { for _ in 0..<1 { seed(); continue; read() } }",
        "seed(",
    ),
    "breakBeforeReader": (
        "private func seed() { store() }\n"
        "func testMeasure() { for _ in 0..<1 { seed(); break; read() } }",
        "seed(",
    ),
    "whileFalseHelperThenDirectReader": (
        "private func seed() { store() }\n"
        "func testMeasure() { while false { seed() }; read() }",
        "seed(",
    ),
    "expressionFalseHelperThenDirectReader": (
        "private func seed() { store() }\n"
        "func testMeasure() { if 0 == 1 { seed() }; read() }",
        "seed(",
    ),
    "argumentReaderWithoutLaterReader": (
        "private func seed(_ value: Int) { store() }\n"
        "func testMeasure() { seed(read()) }",
        "seed(",
    ),
    "argumentReaderWithLaterDirectReader": (
        "private func seed(_ value: Int) { store() }\n"
        "func testMeasure() { seed(read()); read() }",
        "seed(",
    ),
}

boundaries = {}
for name, (text, helper_call) in sources.items():
    observed = direct(text, helper_call)
    public = cli(text, helper_call)
    boundaries[name] = {
        "scopeFindings": observed["scopeFindings"],
        "rawMutatingBodies": observed["mutating"],
        "scopedCounts": observed["scopedCounts"],
        "cliExit": public["exitCode"],
        "cliInvalidScope": "INVALID SCOPE" in public["stdout"],
    }

assert boundaries["storedClosureNeverInvoked"]["cliExit"] == 1
# Deliberate conservative false negatives: nested executable readers do not establish scope credit.
assert boundaries["storedClosureInvoked"]["cliExit"] == 1
assert boundaries["helperTrailingClosure"]["cliExit"] == 0
assert boundaries["parenthesizedReader"]["cliExit"] == 0
assert boundaries["configuredReaderTrailingClosure"]["cliExit"] == 1
assert boundaries["readerOnlyBeforeHelper"]["cliExit"] == 1
assert boundaries["unreachableFalseBranch"]["cliExit"] == 1
assert boundaries["inactiveCompilationBranch"]["cliExit"] == 1
assert boundaries["missingModuleCompilationBranch"]["cliExit"] == 1
for reference in ("unicodeLabelReference", "backtickLabelReference",
                  "underscoreLabelReference"):
    assert boundaries[reference]["cliExit"] == 1
assert boundaries["helperTrailingThenDirectReader"]["cliExit"] == 0
assert boundaries["helperTrailingThenNestedReader"]["cliExit"] == 1
assert boundaries["immediatelyInvokedNestedReader"]["cliExit"] == 1
assert boundaries["synchronousDoNestedReader"]["cliExit"] == 1
assert boundaries["nestedHelperCallThenDirectReader"]["cliExit"] == 1
assert boundaries["inactiveHelperCallThenDirectReader"]["cliExit"] == 1
assert boundaries["returnBeforeDirectReader"]["cliExit"] == 1
for false_green in ("multiTrailingFirstReaderNotInvoked", "continueBeforeReader",
                    "breakBeforeReader", "whileFalseHelperThenDirectReader",
                    "expressionFalseHelperThenDirectReader"):
    assert boundaries[false_green]["cliExit"] == 0
assert boundaries["argumentReaderWithoutLaterReader"]["cliExit"] == 1
assert boundaries["argumentReaderWithLaterDirectReader"]["cliExit"] == 0


def schema_rejection(name: str, transform) -> dict:
    result = cli(sources["parenthesizedReader"][0], transform=transform)
    assert result["exitCode"] == 1 and "INVALID SCOPE" in result["stdout"], name
    return {"exitCode": result["exitCode"], "invalidScope": True}


schema = {
    "unknownTopLevel": schema_rejection(
        "unknownTopLevel", lambda payload: {**payload, "surprise": True}),
    "unknownRecordField": schema_rejection(
        "unknownRecordField", lambda payload: {
            **payload, "scopes": [{**payload["scopes"][0], "surprise": True}]}),
    "callerPostureDrift": schema_rejection(
        "callerPostureDrift", lambda payload: {
            **payload, "scopes": [{
                **payload["scopes"][0],
                "callers": [{**payload["scopes"][0]["callers"][0], "testEntry": False}],
            }]}),
}


def mutation(name: str, old: bytes, new: bytes) -> dict:
    assert source_bytes.count(old) == 1, name
    root = Path(tempfile.mkdtemp(prefix=f"f25-065-additional-mutant-{name}-"))
    scanner = root / SCRIPT_REL
    test = root / TEST_REL
    scanner.parent.mkdir(parents=True)
    test.parent.mkdir(parents=True)
    scanner.write_bytes(source_bytes.replace(old, new))
    test.write_bytes(test_bytes)
    result = subprocess.run(
        ["python3", str(test),
         "SwiftBodies.test_attributed_helper_requires_an_executable_later_reader_call", "-v"],
        cwd=root, capture_output=True, text=True, timeout=60,
        env={"PYTHONPYCACHEPREFIX": str(root / "pycache")},
    )
    assert result.returncode != 0, f"{name} survived substantive permanent fixture"
    return {
        "name": name,
        "exitCode": result.returncode,
        "failedAsRequired": True,
        "outputTail": "\n".join((result.stdout + result.stderr).splitlines()[-12:]),
        "mutantSHA256": hashlib.sha256(scanner.read_bytes()).hexdigest(),
        "baselineSHA256": source_sha,
        "worktreeUntouched": True,
    }


pattern = (
    b'        pattern = (re.escape(reader)\n'
    b'                   + r"\\w*\\s*\\((?!\\s*(?:(?:`[^`\\r\\n]+`|[^():,\\s]+)\\s*:\\s*)+\\))")\n'
)
mutants = [
    mutation("drop-call-syntax", pattern,
             b'        pattern = re.escape(reader) + r"\\w*"\n'),
    mutation("allow-function-reference-placeholder", pattern,
             b'        pattern = re.escape(reader) + r"\\w*\\s*\\("\n'),
    mutation("allow-reader-trailing-closure", pattern,
             b'        pattern = (re.escape(reader)\n'
             b'                   + r"\\w*\\s*(?:\\{|\\((?!\\s*(?:(?:`[^`\\r\\n]+`|[^():,\\s]+)\\s*:\\s*)+\\)))")\n'),
    mutation("allow-nested-reader",
             b"    if depth != minimum_depth:\n        return False\n",
             b"    if False:\n        return False\n"),
    mutation("allow-conditional-compilation-reader",
             b"    if conditional_depth:\n        return False\n",
             b"    if False:\n        return False\n"),
    mutation("skip-helper-execution-context",
             b"                        not helper_invocation_context(masked_caller, context_start) or\n",
             b"                        False or\n"),
    mutation("trust-uninvoked-helper-closure",
             b"                        (trailing and not (len(target_bodies) == 1 and target_bodies[0][3]))):\n",
             b"                        False):\n"),
    mutation("scan-helper-arguments-as-later-readers",
             b"                    reader_tail = balanced_call_end(masked_caller, opening)\n",
             b"                    reader_tail = offset + match.end()\n"),
    mutation("allow-top-level-terminator-reader",
             b'    for terminal in re.finditer(r"\\b(?:return|throw)\\b", prefix):\n',
             b"    for terminal in ():\n"),
    mutation("drop-invocation-context",
             b"        if any(reader_invocation_context(source, match.start())\n",
             b"        if any(True\n"),
]


result = {
    "verdict": "FAIL",
    "reviewedImplementation": TARGET,
    "sourceSHA256": source_sha,
    "blockingFalseGreen": {
        "claim": "Multiple trailing closures are credited from the invoked final parameter while the reader sits in the uninvoked first closure.",
        "source": sources["multiTrailingFirstReaderNotInvoked"][0],
        "cliExit": boundaries["multiTrailingFirstReaderNotInvoked"]["cliExit"],
        "swiftTypecheckExit": 0,
    },
    "secondaryControlFlowFalseGreen": {
        "claim": "Break and continue do not terminate later-reader credit inside a recognized loop.",
        "sources": [sources["continueBeforeReader"][0], sources["breakBeforeReader"][0]],
        "cliExits": [boundaries["continueBeforeReader"]["cliExit"], boundaries["breakBeforeReader"]["cliExit"]],
    },
    "boundaries": boundaries,
    "strictSchemaAndCallerBinding": schema,
    "actualSourceMutants": mutants,
    "sourceRestored": hashlib.sha256(source_bytes).hexdigest() == source_sha,
    "mutationLocation": "isolated temporary copies from git-show snapshot; shared worktree was not mutated",
}
Path(__file__).with_name("probe.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
