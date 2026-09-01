#!/usr/bin/env python3
"""Independent public-CLI and exact-source probes for F25-065 upstream review."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TARGET = "de4de21e35d314cbefc155ab0016de222ca3fd59"
RETAINED_FAILS = (
    "dd80213bd27aa880b6227aa4b961f649e0d314a0",
    "4c5ed872410051e0bfa5d3634a49d03f32efc014",
    "78895b88a46510d893a699cb79ea789828f7509e",
    "824e9aa0c891d7a61bbf663dc3ee93a9df821750",
    "9b09eca75af7ae70b26841e705c73e3661aa69af",
    "db6ded00ca8f6faa2ac8e5fd280b0c9e8b310071",
    "66bb795908189830ffcf39067e9b46f6851ce879",
    "49790b372ae2a5d57262d4d5d417d01d2c222d8e",
    "a6dc3884a4a95c25b7e1d9ed96fe854a55d111b5",
    "cbda7209143b30c44135f0227b8e6fb437169d04",
)
SCRIPT_REL = "plugins/test-campaign/skills/test-campaign/scripts/vacuity-check.py"
SCRIPT = ROOT / SCRIPT_REL


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


target_source = git("show", f"{TARGET}:{SCRIPT_REL}")
assert SCRIPT.read_bytes() == target_source
source_hash = hashlib.sha256(target_source).hexdigest()


def load_module(path: Path, tag: str):
    spec = importlib.util.spec_from_file_location(f"f25_065_primary_final_{tag}", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


scan = load_module(SCRIPT, "reviewed")


def scope_for(module, source: str, caller_call: str = "seed(") -> dict:
    blocks = module.swift_body_spans(source)["blocks"]
    assert len(blocks) >= 2
    helper = source[blocks[0]["bodyStart"]:blocks[0]["end"]]
    caller = source[blocks[1]["bodyStart"]:blocks[1]["end"]]
    target_offset = helper.index("store(")
    caller_offset = caller.index(caller_call)
    return {
        "file": "ExampleTests.swift",
        "name": "seed",
        "bodySHA256": hashlib.sha256(helper.encode()).hexdigest(),
        "testEntry": blocks[0]["testEntry"],
        "callOffset": target_offset,
        "callSHA256": module.call_fingerprint(
            helper, target_offset, target_offset + len("store(")
        ),
        "mutator": "store",
        "classification": "attributed-helper",
        "rationale": "named caller reads after helper",
        "references": [],
        "callers": [{
            "file": "ExampleTests.swift",
            "name": blocks[1]["name"],
            "bodySHA256": hashlib.sha256(caller.encode()).hexdigest(),
            "testEntry": blocks[1]["testEntry"],
            "callOffset": caller_offset,
            "callSHA256": module.call_fingerprint(
                caller, caller_offset, caller_offset + len(caller_call)
            ),
        }],
    }


def run_pass(module, source: str, row: dict | None = None) -> dict:
    with tempfile.TemporaryDirectory(prefix="f25-065-primary-pass-") as directory:
        test_root = Path(directory)
        (test_root / "ExampleTests.swift").write_text(source)
        return module.pass_blind(
            test_root,
            ("record", "store", "apply", "update", "write"),
            ("read", "load", "expect", "get"),
            [] if row is None else [row],
        )


def run_cli(source: str, row: dict | None, campaign_scope: object = "scopes.json",
            payload_transform=None) -> dict:
    with tempfile.TemporaryDirectory(prefix="f25-065-primary-cli-") as directory:
        root = Path(directory)
        tests = root / "tests"
        tests.mkdir()
        (tests / "ExampleTests.swift").write_text(source)
        (root / "inventory.json").write_text(json.dumps({
            "requirement": [{"id": "REQ-001", "title": "Counter", "effect": "none"}]
        }))
        campaign = {
            "testRoot": "tests",
            "blindVocabulary": {
                "only": True,
                "mutators": ["store"],
                "readers": ["read", "load", "expect", "get"],
            },
            "blindScopeFile": campaign_scope,
        }
        (root / "campaign.json").write_text(json.dumps(campaign))
        (root / "producer.swift").write_text("current producer contract\n")
        if row is not None:
            bound = json.loads(json.dumps(row))
            bound["references"] = [{
                "path": "producer.swift",
                "sha256": hashlib.sha256(b"current producer contract\n").hexdigest(),
            }]
            payload = {"version": 1, "scopes": [bound]}
            if payload_transform is not None:
                payload = payload_transform(payload)
            (root / "scopes.json").write_text(json.dumps(payload))
        result = subprocess.run(
            ["python3", str(SCRIPT), str(root), "--gate"],
            capture_output=True,
            text=True,
            timeout=20,
        )
        return {"exitCode": result.returncode, "stdout": result.stdout, "stderr": result.stderr}


sources = {
    "unqualifiedParenthesizedReader": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); read() }",
        "seed(",
    ),
    "qualifiedParenthesizedHelperWithReader": (
        "private func seed() { store() }\n"
        "@Test func measure() { Fixtures.seed(); read() }",
        "seed(",
    ),
    "readerBefore": (
        "private func seed() { store() }\n"
        "@Test func measure() { read(); seed() }",
        "seed(",
    ),
    "commentOnlyReader": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); /* read() */ }",
        "seed(",
    ),
    "stringOnlyReader": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); let note = \"read()\" }",
        "seed(",
    ),
    "identifierSubstringOnly": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); let already = 1 }",
        "seed(",
    ),
    "bareReaderNameOnly": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); read }",
        "seed(",
    ),
    "readerShapedControlCondition": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); let read = false; if read { print(\"x\") } }",
        "seed(",
    ),
    "nestedReaderDeclaration": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); func read() { print(\"x\") } }",
        "seed(",
    ),
    "enumReaderPattern": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); switch value { case .read(let x): print(x); default: break } }",
        "seed(",
    ),
    "selectorReaderReference": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); let selector = #selector(read(_:)) }\n"
        "@objc func read(_ value: Any) {}",
        "seed(",
    ),
    "assignedReaderFunctionReference": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); let function = read(_:) }\n"
        "func read(_ value: Int) -> Int { value }",
        "seed(",
    ),
    "multipleLabelReaderFunctionReference": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); let function = read(first:second:) }\n"
        "func read(first: Int, second: Int) -> Int { first + second }",
        "seed(",
    ),
    "assignedLabeledReaderCall": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); let result = read(label: input) }",
        "seed(",
    ),
    "assignedMultipleLabeledReaderCall": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); let result = read(first: one, second: two) }",
        "seed(",
    ),
    "escapedLabelReaderFunctionReference": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); let function = read(`repeat`:) }\n"
        "func read(`repeat` value: Int) -> Int { value }",
        "seed(",
    ),
    "localGetterDeclaration": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); var value: Int { get { 1 } }; _ = 2 }",
        "seed(",
    ),
    "sameLineDefaultArgument": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); func local(value: Int = read()) {} }",
        "seed(",
    ),
    "splitLineDefaultArgument": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); func local(value: Int =\nread()) {} }",
        "seed(",
    ),
    "splitLineReaderDeclaration": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); func\nread() {} }",
        "seed(",
    ),
    "unicodeLabelReaderFunctionReference": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); let function = read(λ:) }\n"
        "func read(λ value: Int) -> Int { value }",
        "seed(",
    ),
    "storedClosureReader": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); let observation = { configure(); read() }; _ = observation }",
        "seed(",
    ),
    "unreachableReader": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); if false { configure(); read() } }",
        "seed(",
    ),
    "immediatelyInvokedClosureReader": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); ({ read() })() }",
        "seed(",
    ),
    "closureCaptureReader": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); let closure = { [value = read()] in value }; _ = closure }",
        "seed(",
    ),
    "readerInsideHelperTrailingClosure": (
        "private func seed(_ body: () -> Void) { store() }\n"
        "@Test func measure() { seed { read() } }",
        "seed {",
    ),
    "autoclosureReaderArgument": (
        "private func seed(_ observation: @autoclosure () -> Int) { store() }\n"
        "@Test func measure() { seed(read()) }",
        "seed(",
    ),
    "trailingHelperInvokesAfterMutation": (
        "private func seed(_ body: () -> Void) { store(); body() }\n"
        "@Test func measure() { seed { read() } }",
        "seed {",
    ),
    "trailingHelperInvokesBeforeMutation": (
        "private func seed(_ body: () -> Void) { body(); store() }\n"
        "@Test func measure() { seed { read() } }",
        "seed {",
    ),
    "balancedHelperArgumentsThenReader": (
        "private func seed(_ value: Int) { store() }\n"
        "@Test func measure() { seed(read()); read() }",
        "seed(",
    ),
    "helperInsideStoredClosure": (
        "private func seed() { store() }\n"
        "@Test func measure() { let invoke = { seed() }; _ = invoke; read() }",
        "seed(",
    ),
    "helperInsideInactiveDirective": (
        "private func seed() { store() }\n"
        "@Test func measure() {\n#if false\nseed()\n#endif\nread()\n }",
        "seed(",
    ),
    "readerAfterReturn": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); return; read() }",
        "seed(",
    ),
    "helperAtReturnThenReader": (
        "private func seed() -> Int { store(); return 1 }\n"
        "@Test func measure() -> Int { return seed(); read() }",
        "seed(",
    ),
    "deferReader": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); defer { read() } }",
        "seed(",
    ),
    "loopReader": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed(); while read() { break } }",
        "seed(",
    ),
    "inactiveDirectiveReader": (
        "private func seed() { store() }\n"
        "@Test func measure() { seed();\n#if false\nread()\n#endif\n }",
        "seed(",
    ),
}

boundaries = {}
for name, (source, call) in sources.items():
    row = scope_for(scan, source, call)
    direct = run_pass(scan, source, row)
    public = run_cli(source, row)
    boundaries[name] = {
        "scopeFindings": direct["scopeFindings"],
        "scopedCounts": direct["scopedCounts"],
        "rawMutatingBodies": direct["mutating"],
        "cliExit": public["exitCode"],
        "cliInvalidScope": "INVALID SCOPE" in public["stdout"],
    }

assert boundaries["unqualifiedParenthesizedReader"]["cliExit"] == 0
assert boundaries["qualifiedParenthesizedHelperWithReader"]["cliExit"] == 0
assert boundaries["assignedLabeledReaderCall"]["cliExit"] == 0
assert boundaries["assignedMultipleLabeledReaderCall"]["cliExit"] == 0
assert boundaries["balancedHelperArgumentsThenReader"]["cliExit"] == 0
for name in ("readerBefore", "commentOnlyReader", "stringOnlyReader",
             "identifierSubstringOnly", "bareReaderNameOnly",
             "readerShapedControlCondition", "nestedReaderDeclaration",
             "enumReaderPattern", "selectorReaderReference",
             "assignedReaderFunctionReference",
             "multipleLabelReaderFunctionReference",
             "escapedLabelReaderFunctionReference", "localGetterDeclaration",
             "sameLineDefaultArgument", "splitLineDefaultArgument",
             "splitLineReaderDeclaration", "unicodeLabelReaderFunctionReference",
             "storedClosureReader", "unreachableReader",
             "immediatelyInvokedClosureReader", "closureCaptureReader",
             "readerInsideHelperTrailingClosure", "deferReader", "loopReader",
             "inactiveDirectiveReader", "autoclosureReaderArgument",
             "helperInsideStoredClosure", "helperInsideInactiveDirective",
             "readerAfterReturn", "trailingHelperInvokesAfterMutation",
             "trailingHelperInvokesBeforeMutation"):
    assert boundaries[name]["cliExit"] == 1 and boundaries[name]["cliInvalidScope"]

assert boundaries["helperAtReturnThenReader"]["cliExit"] == 0



base_source = sources["unqualifiedParenthesizedReader"][0]
base_row = scope_for(scan, base_source)
schema_cases = {}

for label, value in {
    "configuredFalse": False,
    "configuredZero": 0,
    "configuredObject": {},
    "configuredArray": [],
}.items():
    result = run_cli(base_source, None, campaign_scope=value)
    assert result["exitCode"] == 1 and "nonempty string" in result["stdout"]
    schema_cases[label] = result["exitCode"]


def schema_case(label, transform):
    result = run_cli(base_source, base_row, payload_transform=transform)
    assert result["exitCode"] == 1 and "INVALID SCOPE" in result["stdout"]
    schema_cases[label] = result["exitCode"]


schema_case("boolVersion", lambda p: {**p, "version": True})
schema_case("boolCallOffset", lambda p: {
    **p, "scopes": [{**p["scopes"][0], "callOffset": True}]
})
schema_case("integerTestEntry", lambda p: {
    **p, "scopes": [{**p["scopes"][0], "testEntry": 1}]
})
schema_case("unknownTopField", lambda p: {**p, "surprise": True})
schema_case("unknownRowField", lambda p: {
    **p, "scopes": [{**p["scopes"][0], "surprise": True}]
})
schema_case("emptyReferenceHash", lambda p: {
    **p, "scopes": [{**p["scopes"][0], "references": [{"path": "producer.swift", "sha256": ""}]}]
})
schema_case("unknownClassification", lambda p: {
    **p, "scopes": [{**p["scopes"][0], "classification": "unknown"}]
})
schema_case("staleBody", lambda p: {
    **p, "scopes": [{**p["scopes"][0], "bodySHA256": "0" * 64}]
})
schema_case("staleCallFingerprint", lambda p: {
    **p, "scopes": [{**p["scopes"][0], "callSHA256": "0" * 64}]
})
schema_case("staleCallOffset", lambda p: {
    **p, "scopes": [{**p["scopes"][0], "callOffset": p["scopes"][0]["callOffset"] + 1}]
})
schema_case("unmatchedFile", lambda p: {
    **p, "scopes": [{**p["scopes"][0], "file": "MissingTests.swift"}]
})
schema_case("duplicateScope", lambda p: {**p, "scopes": p["scopes"] * 2})


def observe_exact_recheck(module):
    source = "@Test func measure() { write(); Issue.record(\"failure\") }"
    block = module.swift_body_spans(source)["blocks"][0]
    body = source[block["bodyStart"]:block["end"]]
    offset = body.index("record(")
    row = {
        "file": "ExampleTests.swift", "name": "measure",
        "bodySHA256": hashlib.sha256(body.encode()).hexdigest(), "testEntry": True,
        "callOffset": offset,
        "callSHA256": module.call_fingerprint(body, offset, offset + len("record(")),
        "mutator": "record", "classification": "failure-sentinel",
        "rationale": "failure sentinel", "references": [{"path": "x", "sha256": "0" * 64}],
    }
    result = run_pass(module, source, row)
    assert result["mutating"] == 1
    assert result["scopedCounts"]["failure-sentinel"] == 1
    assert result["findings"], "earlier write was suppressed with the scoped record"


def observe_executable_caller(module):
    source = (
        "private func seed() { store() }\n"
        "@Test func measure() { /* seed() */ read() }"
    )
    result = run_pass(module, source, scope_for(module, source))
    assert any("named helper call" in finding for finding in result["scopeFindings"])


def observe_posture(module):
    source = "@Test func measure() { store() }"
    block = module.swift_body_spans(source)["blocks"][0]
    body = source[block["bodyStart"]:block["end"]]
    offset = body.index("store(")
    row = {
        "file": "ExampleTests.swift", "name": "measure",
        "bodySHA256": hashlib.sha256(body.encode()).hexdigest(), "testEntry": True,
        "callOffset": offset,
        "callSHA256": module.call_fingerprint(body, offset, offset + len("store(")),
        "mutator": "store", "classification": "direct-output", "rationale": "return",
        "references": [{"path": "x", "sha256": "0" * 64}],
    }
    drifted = source.replace("@Test ", "")
    result = run_pass(module, drifted, row)
    assert result["scopeFindings"] and result["findings"]


def observe_no_global_suppression(module):
    result = run_pass(module, "@Test func blind() { record(); store(); apply(); update() }")
    assert result["mutating"] == 1 and result["findings"]


def observe_identifier_boundary(module):
    assert not module.has_reader_call("let already() = 1", ("read",)), \
        "identifier substring accepted as reader call"


def observe_call_syntax(module):
    assert not module.has_reader_call("read", ("read",)), \
        "bare reader name accepted as reader call"


def observe_control_condition(module):
    assert not module.has_reader_call("if read { print(x) }", ("read",)), \
        "control condition accepted as reader call"


def observe_qualified_pattern(module):
    assert not module.has_reader_call("case .read(let x)", ("read",)), \
        "qualified enum pattern accepted as reader call"


def observe_invocation_context(module):
    assert not module.has_reader_call("case .read(let x)", ("read",)), \
        "enum pattern accepted after removing invocation context"


def observe_function_reference_placeholder(module):
    assert not module.has_reader_call("let function = read(_:)", ("read",)), \
        "function-reference placeholder accepted as invocation"


def observe_reader_trailing_closure(module):
    assert not module.has_reader_call("read {}", ("read",)), \
        "reader trailing closure accepted after restoring withdrawn shape"


def observe_nested_reader(module):
    assert not module.has_reader_call("let closure = { configure(); read() }", ("read",)), \
        "stored closure reader accepted after removing depth guard"


def observe_conditional_reader(module):
    assert not module.has_reader_call("#if false\nread()", ("read",)), \
        "conditional-compilation reader accepted after removing directive guard"


def observe_helper_trailing_closure(module):
    source = sources["readerInsideHelperTrailingClosure"][0]
    result = run_pass(module, source, scope_for(module, source, "seed {"))
    assert result["scopeFindings"], "helper trailing closure accepted"


def observe_case_invalid(module, name, call="seed("):
    source = sources[name][0]
    result = run_pass(module, source, scope_for(module, source, call))
    assert result["scopeFindings"], f"{name} accepted"


def run_mutant(name: str, old: bytes, new: bytes, observation) -> dict:
    assert target_source.count(old) == 1, name
    mutated = target_source.replace(old, new)
    with tempfile.TemporaryDirectory(prefix="f25-065-primary-mutant-") as directory:
        path = Path(directory) / "vacuity-check.py"
        path.write_bytes(mutated)
        mutant = load_module(path, name.replace("-", "_"))
        try:
            observation(mutant)
        except AssertionError as error:
            return {"name": name, "failedAsRequired": True,
                    "assertion": str(error) or "independent assertion failed"}
    raise AssertionError(f"mutant {name} survived its source-bound observation")


mutants = [
    run_mutant(
        "drop-call-syntax",
        b'        pattern = (re.escape(reader)\n                   + r"\\w*\\s*\\((?!\\s*(?:(?:`[^`\\r\\n]+`|[^():,\\s]+)\\s*:\\s*)+\\))")\n',
        b'        pattern = re.escape(reader) + r"\\w*"\n',
        observe_call_syntax,
    ),
    run_mutant(
        "allow-function-reference-placeholder",
        b'        pattern = (re.escape(reader)\n                   + r"\\w*\\s*\\((?!\\s*(?:(?:`[^`\\r\\n]+`|[^():,\\s]+)\\s*:\\s*)+\\))")\n',
        b'        pattern = re.escape(reader) + r"\\w*\\s*\\("\n',
        observe_function_reference_placeholder,
    ),
    run_mutant(
        "allow-reader-trailing-closure",
        b'        pattern = (re.escape(reader)\n                   + r"\\w*\\s*\\((?!\\s*(?:(?:`[^`\\r\\n]+`|[^():,\\s]+)\\s*:\\s*)+\\))")\n',
        b'        pattern = (re.escape(reader)\n                   + r"\\w*\\s*(?:\\{|\\((?!\\s*(?:(?:`[^`\\r\\n]+`|[^():,\\s]+)\\s*:\\s*)+\\)))")\n',
        observe_reader_trailing_closure,
    ),
    run_mutant(
        "allow-nested-closure-reader",
        b"    if depth != minimum_depth:\n        return False\n",
        b"    if False:\n        return False\n",
        observe_nested_reader,
    ),
    run_mutant(
        "allow-conditional-compilation-reader",
        b"    if conditional_depth:\n        return False\n",
        b"    if False:\n        return False\n",
        observe_conditional_reader,
    ),
    run_mutant(
        "skip-helper-execution-context",
        b"                        not helper_invocation_context(masked_caller, context_start)):\n",
        b"                        False):\n",
        lambda module: observe_case_invalid(module, "helperInsideStoredClosure"),
    ),
    run_mutant(
        "scan-helper-arguments-as-later-readers",
        b"                reader_tail = balanced_call_end(masked_caller, opening)\n",
        b"                reader_tail = offset + match.end()\n",
        lambda module: observe_case_invalid(module, "autoclosureReaderArgument"),
    ),
    run_mutant(
        "allow-top-level-terminator-reader",
        b'    for terminal in re.finditer(r"\\b(?:return|throw)\\b", prefix):\n',
        b"    for terminal in ():\n",
        lambda module: observe_case_invalid(module, "readerAfterReturn"),
    ),
    run_mutant(
        "drop-invocation-context",
        b"        if any(reader_invocation_context(source, match.start())\n",
        b"        if any(True\n",
        observe_invocation_context,
    ),
]

retained_paths = (
    "docs/evidence/f25-065/primary-final/verification.md",
    "docs/evidence/f25-065/primary-reader-repair/verification.md",
    "docs/evidence/f25-065/primary-reader-repair2/verification.md",
    "docs/evidence/f25-065/primary-reader-repair3/verification.md",
    "docs/evidence/f25-065/primary-reader-repair4/verification.md",
    "docs/evidence/f25-065/primary-reader-repair5/verification.md",
    "docs/evidence/f25-065/primary-reader-repair6/verification.md",
    "docs/evidence/f25-065/primary-reader-repair7/verification.md",
    "docs/evidence/f25-065/primary-reader-repair8/verification.md",
    "docs/evidence/f25-065/primary-reader-repair9/verification.md",
)
retained_fail_unchanged = [
    git("show", f"{commit}:{path}") == (ROOT / path).read_bytes()
    for commit, path in zip(RETAINED_FAILS, retained_paths)
]
assert all(retained_fail_unchanged)

discarded = json.loads((ROOT / "docs/evidence/f25-065/reader-call-repair4/mutations.json").read_text())
assert discarded["allRejected"] is False
assert sum(not row["failedAsRequired"] for row in discarded["mutants"]) == 3

receipt = {
    "verdict": "FAIL",
    "reviewedHead": TARGET,
    "retainedPriorFailures": list(RETAINED_FAILS),
    "retainedPriorFailureUnchanged": retained_fail_unchanged,
    "sourceSHA256": source_hash,
    "blockingFalseGreen": {
        "claim": "A helper accepted in return position loses the return terminator when later-reader search slices after the balanced helper call.",
        "source": sources["helperAtReturnThenReader"][0],
        "cliExit": boundaries["helperAtReturnThenReader"]["cliExit"],
    },
    "boundaries": boundaries,
    "strictSchemaCases": schema_cases,
    "actualSourceMutants": mutants,
    "discardedRedundantGuardAttempt": {"allRejected": discarded["allRejected"], "survivors": 3},
    "sourceRestored": SCRIPT.read_bytes() == target_source,
}
Path(__file__).with_name("probe.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
