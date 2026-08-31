#!/usr/bin/env python3
"""Actual blind pass and public CLI fixtures; no Swift toolchain or third-party dependency."""
import importlib.util
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/test-campaign/scripts/vacuity-check.py'
REPO = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location('vacuity_swift_tests', SCRIPT)
SCAN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCAN)


class SwiftBodies(unittest.TestCase):
    def test_generated_catalogue_matches_canonical_plugin_version(self):
        manifest = json.loads((REPO / 'plugins/test-campaign/.claude-plugin/plugin.json').read_text())
        catalogue = json.loads((REPO / 'site/lib/catalogue.json').read_text())
        row = next(plugin for plugin in catalogue['skills'] if plugin['name'] == 'test-campaign')
        self.assertEqual(row['version'], manifest['version'])

    def scan(self, source, extras=None, mutators=('write', 'store'), scopes=None):
        with tempfile.TemporaryDirectory(prefix='swift-body-tests-') as directory:
            root = Path(directory)
            (root / 'ExampleTests.swift').write_text(source)
            for name, text in (extras or {}).items(): (root / name).write_text(text)
            return SCAN.pass_blind(root, mutators, ('read', 'load', 'expect'), scopes)

    def scope(self, source, call, classification='failure-sentinel'):
        parsed = SCAN.swift_body_spans(source)['blocks'][0]
        body = source[parsed['bodyStart']:parsed['end']]
        start = body.index(call)
        end = start + len(call)
        return {'file': 'ExampleTests.swift', 'name': parsed['name'],
                'bodySHA256': hashlib.sha256(body.encode()).hexdigest(),
                'testEntry': parsed['testEntry'],
                'callOffset': start, 'callSHA256': SCAN.call_fingerprint(body, start, end),
                'mutator': call.split('(')[0].split('.')[-1], 'classification': classification,
                'rationale': 'test fixture', 'references': [{'path': 'unused', 'sha256': '0' * 64}]}

    def test_exact_call_scope_removes_only_that_occurrence_then_rechecks_earlier_calls(self):
        source = 'func testScoped() { write(); read(); Issue.record("failure") }'
        scope = self.scope(source, 'record(')
        result = self.scan(source, mutators=('write', 'record'), scopes=[scope])
        self.assertEqual(self.names(result), [])
        self.assertEqual(result['scopedCounts']['failure-sentinel'], 1)
        source = 'func testStillBlind() { write(); Issue.record("failure") }'
        scope = self.scope(source, 'record(')
        result = self.scan(source, mutators=('write', 'record'), scopes=[scope])
        self.assertEqual(self.names(result), ['testStillBlind'])

    def test_scope_fails_closed_on_body_call_duplicate_and_helper_ambiguity(self):
        source = 'func testScoped() { write(); Issue.record("failure") }'
        scope = self.scope(source, 'record(')
        stale = dict(scope, bodySHA256='0' * 64)
        result = self.scan(source, mutators=('write', 'record'), scopes=[stale])
        self.assertTrue(result['scopeFindings'])
        wrong_call = dict(scope, callSHA256='0' * 64)
        result = self.scan(source, mutators=('write', 'record'), scopes=[wrong_call])
        self.assertTrue(result['scopeFindings'])
        result = self.scan(source, mutators=('write', 'record'), scopes=[scope, dict(scope)])
        self.assertTrue(result['scopeFindings'])
        helper = 'private func seed() { write() }\nfunc testCaller() { seed(); read() }'
        parsed = SCAN.swift_body_spans(helper)['blocks'][0]
        body = helper[parsed['bodyStart']:parsed['end']]
        caller_parsed = SCAN.swift_body_spans(helper)['blocks'][1]
        caller_body = helper[caller_parsed['bodyStart']:caller_parsed['end']]
        caller_offset = caller_body.index('seed(')
        helper_scope = {'file': 'ExampleTests.swift', 'name': 'seed',
            'bodySHA256': hashlib.sha256(body.encode()).hexdigest(), 'testEntry': False,
            'callOffset': body.index('write('),
            'callSHA256': SCAN.call_fingerprint(body, body.index('write('), body.index('write(')+6),
            'mutator': 'write', 'classification': 'attributed-helper', 'rationale': 'caller reads',
            'references': [{'path': 'unused', 'sha256': '0' * 64}], 'callers': [{
                'file': 'ExampleTests.swift', 'name': 'testCaller',
                'bodySHA256': hashlib.sha256(caller_body.encode()).hexdigest(),
                'testEntry': True,
                'callOffset': caller_offset,
                'callSHA256': SCAN.call_fingerprint(
                    caller_body, caller_offset, caller_offset + len('seed('))}]}
        result = self.scan(helper, scopes=[helper_scope])
        self.assertEqual(result['scopedCounts']['attributed-helper'], 1)
        arbitrary = dict(helper_scope)
        arbitrary['callers'] = [dict(helper_scope['callers'][0], name='seed')]
        result = self.scan(helper, scopes=[arbitrary])
        self.assertTrue(any('caller scope' in finding for finding in result['scopeFindings']))
        blind_helper = 'private func seed() { write() }\nfunc testCaller() { read(); seed() }'
        blocks = SCAN.swift_body_spans(blind_helper)['blocks']
        helper_body = blind_helper[blocks[0]['bodyStart']:blocks[0]['end']]
        caller_body = blind_helper[blocks[1]['bodyStart']:blocks[1]['end']]
        caller_offset = caller_body.index('seed(')
        blind_scope = dict(helper_scope,
            bodySHA256=hashlib.sha256(helper_body.encode()).hexdigest(),
            callOffset=helper_body.index('write('),
            callSHA256=SCAN.call_fingerprint(helper_body, helper_body.index('write('),
                                              helper_body.index('write(') + len('write(')),
            callers=[dict(helper_scope['callers'][0],
                bodySHA256=hashlib.sha256(caller_body.encode()).hexdigest(),
                callOffset=caller_offset,
                callSHA256=SCAN.call_fingerprint(
                    caller_body, caller_offset, caller_offset + len('seed(')))])
        result = self.scan(blind_helper, scopes=[blind_scope])
        self.assertTrue(any('no read after' in finding for finding in result['scopeFindings']))

        trailing = ('private func seed(_ body: () -> Void) { write(); body() }\n'
                    '@Test func measure() { seed { read() } }')
        blocks = SCAN.swift_body_spans(trailing)['blocks']
        helper_body = trailing[blocks[0]['bodyStart']:blocks[0]['end']]
        caller_body = trailing[blocks[1]['bodyStart']:blocks[1]['end']]
        caller_offset = caller_body.index('seed ')
        trailing_scope = dict(helper_scope,
            bodySHA256=hashlib.sha256(helper_body.encode()).hexdigest(),
            callOffset=helper_body.index('write('),
            callSHA256=SCAN.call_fingerprint(helper_body, helper_body.index('write('),
                                              helper_body.index('write(') + len('write(')),
            callers=[{'file': 'ExampleTests.swift', 'name': 'measure',
                'bodySHA256': hashlib.sha256(caller_body.encode()).hexdigest(),
                'testEntry': True, 'callOffset': caller_offset,
                'callSHA256': SCAN.call_fingerprint(
                    caller_body, caller_offset, caller_offset + len('seed {'))}])
        result = self.scan(trailing, scopes=[trailing_scope])
        self.assertEqual(result['scopeFindings'], [])

        commented = 'private func seed() { write() }\nfunc testCaller() { /* seed() */ read() }'
        blocks = SCAN.swift_body_spans(commented)['blocks']
        helper_body = commented[blocks[0]['bodyStart']:blocks[0]['end']]
        caller_body = commented[blocks[1]['bodyStart']:blocks[1]['end']]
        caller_offset = caller_body.index('seed(')
        comment_scope = dict(helper_scope,
            bodySHA256=hashlib.sha256(helper_body.encode()).hexdigest(),
            callOffset=helper_body.index('write('),
            callSHA256=SCAN.call_fingerprint(helper_body, helper_body.index('write('),
                                              helper_body.index('write(') + len('write(')),
            callers=[dict(helper_scope['callers'][0],
                bodySHA256=hashlib.sha256(caller_body.encode()).hexdigest(),
                callOffset=caller_offset,
                callSHA256=SCAN.call_fingerprint(
                    caller_body, caller_offset, caller_offset + len('seed(')))])
        result = self.scan(commented, scopes=[comment_scope])
        self.assertTrue(any('named helper call' in finding for finding in result['scopeFindings']))

    def test_attributed_helper_requires_an_executable_later_reader_call(self):
        producer = 'current producer contract\n'

        def attributed_scope(source, helper_call='seed('):
            blocks = SCAN.swift_body_spans(source)['blocks']
            helper = source[blocks[0]['bodyStart']:blocks[0]['end']]
            caller = source[blocks[1]['bodyStart']:blocks[1]['end']]
            target_offset = helper.index('write(')
            caller_offset = caller.index(helper_call)
            return {
                'file': 'ExampleTests.swift', 'name': 'seed',
                'bodySHA256': hashlib.sha256(helper.encode()).hexdigest(),
                'testEntry': False, 'callOffset': target_offset,
                'callSHA256': SCAN.call_fingerprint(
                    helper, target_offset, target_offset + len('write(')),
                'mutator': 'write', 'classification': 'attributed-helper',
                'rationale': 'caller reads after helper',
                'references': [{'path': 'producer.swift',
                    'sha256': hashlib.sha256(producer.encode()).hexdigest()}],
                'callers': [{'file': 'ExampleTests.swift', 'name': 'measure',
                    'bodySHA256': hashlib.sha256(caller.encode()).hexdigest(),
                    'testEntry': True, 'callOffset': caller_offset,
                    'callSHA256': SCAN.call_fingerprint(
                        caller, caller_offset, caller_offset + len(helper_call))}],
            }

        invalid = [
            'private func seed() { write() }\n@Test func measure() { seed(); let already = 1 }',
            'private func seed() { write() }\n@Test func measure() { seed(); already() }',
            'private func seed() { write() }\n@Test func measure() { seed(); read }',
            ('private func seed() { write() }\n'
             '@Test func measure() { seed(); let read = false; if read { print("x") } }'),
            ('private func seed() { write() }\n'
             '@Test func measure() { seed(); switch value { '
             'case .read(let x): print(x); default: break } }'),
            ('private func seed() { write() }\n'
             '@Test func measure() { seed(); let selector = #selector(read(_:)) }'),
            ('private func seed() { write() }\n'
             '@Test func measure() { seed(); let function = read(_:) }'),
        ]
        for source in invalid:
            with self.subTest(source=source):
                scope = attributed_scope(source)
                direct = self.scan(source, scopes=[scope])
                self.assertTrue(any('no read after' in finding
                                    for finding in direct['scopeFindings']))
                cli = self.cli({'ExampleTests.swift': source},
                    {'blindScopeFile': 'scopes.json'}, {
                        'producer.swift': producer,
                        'scopes.json': json.dumps({'version': 1, 'scopes': [scope]}),
                    })
                self.assertEqual(cli.returncode, 1, cli.stdout + cli.stderr)
                self.assertIn('INVALID SCOPE', cli.stdout)

        valid = [
            ('private func seed() { write() }\n'
             '@Test func measure() { Fixtures.seed(); read() }', 'seed('),
            ('private func seed(_ body: () -> Void) { write(); body() }\n'
             '@Test func measure() { Fixtures.seed { configure() }; read {} }', 'seed {'),
            ('private func seed() { write() }\n'
             '@Test func measure() { Fixtures.seed(); let value = read(label: input) }', 'seed('),
        ]
        for source, helper_call in valid:
            with self.subTest(source=source):
                scope = attributed_scope(source, helper_call)
                direct = self.scan(source, scopes=[scope])
                self.assertEqual(direct['scopeFindings'], [])
                cli = self.cli({'ExampleTests.swift': source},
                    {'blindScopeFile': 'scopes.json'}, {
                        'producer.swift': producer,
                        'scopes.json': json.dumps({'version': 1, 'scopes': [scope]}),
                    })
                self.assertEqual(cli.returncode, 0, cli.stdout + cli.stderr)

    def test_scope_binds_target_and_caller_test_entry_posture(self):
        source = '@Test func measure() { write() }'
        scope = self.scope(source, 'write(')
        result = self.scan(source.replace('@Test ', ''), scopes=[scope])
        self.assertTrue(result['scopeFindings'])

        helper = 'private func seed() { write() }\n@Test func measure() { seed(); read() }'
        blocks = SCAN.swift_body_spans(helper)['blocks']
        helper_body = helper[blocks[0]['bodyStart']:blocks[0]['end']]
        caller_body = helper[blocks[1]['bodyStart']:blocks[1]['end']]
        offset = caller_body.index('seed(')
        helper_scope = {'file': 'ExampleTests.swift', 'name': 'seed',
            'bodySHA256': hashlib.sha256(helper_body.encode()).hexdigest(), 'testEntry': False,
            'callOffset': helper_body.index('write('),
            'callSHA256': SCAN.call_fingerprint(helper_body, helper_body.index('write('),
                                                helper_body.index('write(') + len('write(')),
            'mutator': 'write', 'classification': 'attributed-helper', 'rationale': 'caller reads',
            'references': [{'path': 'unused', 'sha256': '0' * 64}], 'callers': [{
                'file': 'ExampleTests.swift', 'name': 'measure',
                'bodySHA256': hashlib.sha256(caller_body.encode()).hexdigest(), 'testEntry': True,
                'callOffset': offset,
                'callSHA256': SCAN.call_fingerprint(caller_body, offset, offset + len('seed('))}]}
        result = self.scan(helper.replace('@Test ', ''), scopes=[helper_scope])
        self.assertTrue(any('caller scope' in finding for finding in result['scopeFindings']))

    def test_scope_file_schema_and_reference_hashes_fail_closed(self):
        with tempfile.TemporaryDirectory(prefix='swift-scope-load-') as directory:
            root = Path(directory); (root / 'producer.swift').write_text('producer')
            ref = {'path': 'producer.swift',
                   'sha256': hashlib.sha256(b'producer').hexdigest()}
            scope = {'file': 'x', 'name': 'x', 'bodySHA256': '0' * 64, 'callOffset': 0,
                     'testEntry': True,
                     'callSHA256': '0' * 64, 'mutator': 'write', 'classification': 'direct-output',
                     'rationale': 'return is the contract', 'references': [ref]}
            (root / 'scopes.json').write_text(json.dumps({'version': 1, 'scopes': [scope]}))
            rows, errors = SCAN.load_blind_scopes(root, 'scopes.json')
            self.assertEqual(len(rows), 1); self.assertEqual(errors, [])
            (root / 'producer.swift').write_text('drift')
            _, errors = SCAN.load_blind_scopes(root, 'scopes.json')
            self.assertTrue(any('drifted' in error for error in errors))
            (root / 'producer.swift').write_text('producer')
            for value in [False, 0, {}, []]:
                _, errors = SCAN.load_blind_scopes(root, value)
                self.assertTrue(errors)
            payload = {'version': True, 'scopes': [dict(scope, callOffset=True)]}
            (root / 'scopes.json').write_text(json.dumps(payload))
            rows, errors = SCAN.load_blind_scopes(root, 'scopes.json')
            self.assertEqual(rows, []); self.assertTrue(errors)
            payload = {'version': 1, 'scopes': [dict(scope, testEntry=1)]}
            (root / 'scopes.json').write_text(json.dumps(payload))
            rows, errors = SCAN.load_blind_scopes(root, 'scopes.json')
            self.assertEqual(rows, []); self.assertTrue(any('test-entry' in error for error in errors))
            for payload in [
                {'version': 1, 'scopes': [dict(scope, surprise=True)]},
                {'version': 1, 'scopes': [dict(scope, callers=[])]},
                {'version': 1, 'scopes': [scope], 'extra': True},
            ]:
                (root / 'scopes.json').write_text(json.dumps(payload))
                rows, errors = SCAN.load_blind_scopes(root, 'scopes.json')
                self.assertEqual(rows, []); self.assertTrue(errors)
            payload = {'version': 1, 'scopes': [dict(scope, classification='attributed-helper')]}
            (root / 'scopes.json').write_text(json.dumps(payload))
            rows, errors = SCAN.load_blind_scopes(root, 'scopes.json')
            self.assertEqual(rows, []); self.assertTrue(any('caller' in error for error in errors))

    def names(self, result):
        return [item.split(' — ')[0] for item in result['findings']]

    def cli(self, files, campaign_extra=None, root_files=None):
        with tempfile.TemporaryDirectory(prefix='swift-body-cli-tests-') as directory:
            root = Path(directory)
            (root / 'tests').mkdir()
            (root / 'inventory.json').write_text(json.dumps({'requirement': [
                {'id': 'REQ-001', 'title': 'Counter', 'effect': 'none'}]}))
            campaign = {'testRoot': 'tests',
                'blindVocabulary': {'only': True, 'mutators': ['write'], 'readers': ['read']}}
            campaign.update(campaign_extra or {})
            (root / 'campaign.json').write_text(json.dumps(campaign))
            for name, text in (root_files or {}).items():
                (root / name).write_text(text)
            for name, text in files.items():
                path = root / 'tests' / name
                if isinstance(text, bytes): path.write_bytes(text)
                else: path.write_text(text)
            return subprocess.run(['python3', str(SCRIPT), str(root), '--gate'],
                                  capture_output=True, text=True, timeout=20)

    def test_original_four_controls_keep_their_meaning(self):
        fixtures = [
            ('func testHasRead() { let x = load(); #expect(x == 1) }\nprivate func fixture() { write() }', ['fixture'], 2),
            ('func testReadsMutationResult() { #expect(store("x").verdict == 1) }', ['testReadsMutationResult'], 1),
            ('func testReallyBlind() { store("x") }', ['testReallyBlind'], 1),
            ('func testSeparateRead() { store("x"); #expect(read() == 1) }', [], 1),
        ]
        for source, names, examined in fixtures:
            with self.subTest(names=names, source=source):
                result = self.scan(source)
                self.assertEqual(result['notMeasured'], [])
                self.assertEqual(self.names(result), names)
                self.assertEqual(result['examined'], examined)
        result = self.scan('func testHasRead() { load() }\nprivate func fixture() { write() }')
        self.assertIn('ExampleTests.swift:2)', result['findings'][0])

    def test_following_reader_cannot_clear_a_blind_test(self):
        result = self.scan('func testBlind() { write() }\nprivate func helper() { read() }')
        self.assertEqual(self.names(result), ['testBlind'])

    def test_nested_declarations_cannot_supply_parent_reader_or_mutation(self):
        result = self.scan('func testBlind() { write(); func helper() { read() } }')
        self.assertEqual(self.names(result), ['testBlind'])
        result = self.scan('func testRead() { read(); func helper() { write() } }')
        self.assertEqual(self.names(result), ['helper'])
        result = self.scan('func testBlind() { write(); struct Local { func helper() { read() } } }')
        self.assertEqual(self.names(result), ['testBlind'])

    def test_nested_attributes_cannot_supply_parent_readers(self):
        for declaration in ['@Wrapper(read()) func helper() {}',
                            '@Wrapper(read()) struct Local {}']:
            with self.subTest(declaration=declaration):
                result = self.scan('func testBlind() { write(); ' + declaration + ' }')
                self.assertEqual(result['notMeasured'], [])
                self.assertEqual(self.names(result), ['testBlind'])

    def test_reader_after_nested_declaration_stays_in_its_parent(self):
        result = self.scan('func testOuter() { write(); func helper() { write() }; read() }')
        self.assertEqual(result['notMeasured'], [])
        self.assertEqual(self.names(result), ['helper'])
        result = self.scan('func testReturn() -> Myfunc { write(); read() }')
        self.assertEqual(result['notMeasured'], [])
        self.assertEqual(self.names(result), [])

    def test_called_helpers_excluded_but_explicit_test_entries_retained(self):
        result = self.scan('private func fixture() { write() }\nfunc testIt() { fixture(); read() }')
        self.assertEqual(result['swiftExcludedHelpers'], 1)
        self.assertEqual(result['examined'], 1)
        self.assertEqual(self.names(result), [])
        for declaration in ['@Test func mutation()', '@Testing.Test() private func mutation()', 'func testMutation()']:
            name = 'testMutation' if 'testMutation' in declaration else 'mutation'
            with self.subTest(declaration=declaration):
                result = self.scan(declaration + ' { write() }\nfunc invokes() { ' + name + '() }')
                self.assertEqual(self.names(result), [name])
                self.assertEqual(result['swiftTestEntries'], 1)

    def test_generic_signature_attributes_defaults_and_typed_throws(self):
        source = '''struct GenericTests {
@Test("scope", arguments: [1, 2])
@MainActor
private static func measured<T: Sequence>(
  _ value: T, operation: () -> Void = { read() }
) async throws(Failure) -> Int where T.Element == Int {
  if true { write() }
  return 1
}
func caller() { measured([1]) }
}
'''
        result = self.scan(source)
        self.assertEqual(result['notMeasured'], [])
        self.assertEqual(self.names(result), ['measured'])
        self.assertEqual(result['swiftTestEntries'], 1)
        self.assertEqual(result['examined'], 2)

    def test_comments_and_literal_delimiters_are_not_calls_or_bodies(self):
        strings = [r'"write() read() func fake() { }"', r'"escaped \" write() }"',
                   r'#"write() \(read()) }"#', r'##"write() \#(read()) }"##',
                   '"""\nwrite()\nfunc fake() { read() }\n"""',
                   '##"""\nwrite() \\#(read())\n"""##']
        for literal in strings:
            with self.subTest(literal=literal):
                result = self.scan('func testLiteral() { let s = ' + literal + ' }')
                self.assertEqual(result['notMeasured'], [])
                self.assertEqual(result['mutating'], 0)
                self.assertEqual(result['declBlocks'], 1)
        result = self.scan('''func testBlind() {
 write()
 /* read() /* func fake() { read() } */ */
 // read() }
 let text = "read()"
}''')
        self.assertEqual(self.names(result), ['testBlind'])

    def test_executable_interpolation_is_preserved_recursively(self):
        mutations = [r'"\(write())"', r'#"\#(write())"#', r'##"\##(write())"##',
                     '"""\n\\(write())\n"""', r'"outer \("inner \(write())")"',
                     r'"\({ write(); return 1 }())"']
        for literal in mutations:
            with self.subTest(literal=literal):
                result = self.scan('func testInterpolation() { let s = ' + literal + ' }')
                self.assertEqual(result['notMeasured'], [])
                self.assertEqual(self.names(result), ['testInterpolation'])
        result = self.scan(r'func testRead() { write(); let s = "\(read())" }')
        self.assertEqual(result['notMeasured'], [])
        self.assertEqual(self.names(result), [])

    def test_escaped_identifiers_and_protocol_requirements(self):
        result = self.scan('protocol Store { func read() -> Int }\nfunc testEscaped() { store.`write`() }')
        self.assertEqual(result['notMeasured'], [])
        self.assertEqual(result['swiftBodylessRequirements'], 1)
        self.assertEqual(self.names(result), ['testEscaped'])
        result = self.scan('func `func`() { read() }\nfunc testCall() { `func`() }')
        self.assertEqual(result['notMeasured'], [])

    def test_ordinary_arithmetic_slash_is_not_rejected(self):
        for expression in ['4 / 2', 'value / count', 'value / max(1, count)', 'value /= 2', 'measure { 4 } / 2']:
            with self.subTest(expression=expression):
                result = self.scan('func testMath() { let x = ' + expression + '; write(); read() }')
                self.assertEqual(result['notMeasured'], [])
                self.assertEqual(self.names(result), [])

    def test_unsupported_and_malformed_forms_are_explicit(self):
        forms = [
            'func testBad() { let x = #/read() { /#; write() }',
            'func testBad() { let x = /read()/; write() }',
            'func testBad() { let x = /ambiguous; write() }',
            'func testBad() { let s = "unterminated }',
            'func testBad() { let s = #"unterminated" }',
            'func testBad() { /* unterminated',
            'func testBad() { let s = "\\(write()" }',
            'func testBad() { write() ] }',
            'func testBad() { write()',
            'func testBad()\nfunc testGood() { write(); read() }',
            'func testBad<T() { write() }',
            'func testBad() { let x = \'read()\' }',
        ]
        for source in forms:
            with self.subTest(source=source):
                result = self.scan(source)
                self.assertEqual(result['examined'], 0)
                self.assertEqual(result['swiftMeasuredFiles'], 0)
                self.assertEqual(len(result['notMeasured']), 1)
                self.assertIn('ExampleTests.swift:', result['notMeasured'][0])

    def test_public_cli_clean_blind_unsupported_mixed_empty_and_unreadable(self):
        clean = 'func testClean() { write(); read() }'
        blind = 'func testBlind() { write() }'
        bad = 'func testRegex() { let re = #/read()/ #; write() }'
        fixtures = [
            ({'GoodTests.swift': clean}, 0, 'blind=0'),
            ({'BlindTests.swift': blind}, 1, 'testBlind — last mutator'),
            ({'BadTests.swift': bad}, 1, 'NOT MEASURED'),
            ({'GoodTests.swift': clean, 'BadTests.swift': bad}, 1, 'measured-files=1 unmeasured-files=1'),
            ({'BlindTests.swift': blind, 'BadTests.swift': bad}, 1, 'testBlind — last mutator'),
            ({}, 1, '0 test blocks recognised'),
            ({'NoBlocksTests.swift': 'let counter = 1'}, 1, '0 test blocks recognised'),
            ({'BadTests.swift': b'func testBad() {\xff}'}, 1, 'UnicodeDecodeError'),
        ]
        for files, code, phrase in fixtures:
            with self.subTest(files=files):
                result = self.cli(files)
                self.assertEqual(result.returncode, code, result.stdout + result.stderr)
                self.assertIn(phrase, result.stdout)

    def test_public_cli_rejects_invalid_scope_configuration(self):
        source = 'func testBlind() { write() }'
        for value in [False, 0, {}, []]:
            with self.subTest(value=value):
                result = self.cli({'BlindTests.swift': source}, {'blindScopeFile': value})
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertIn('blindScopeFile must be a nonempty string', result.stdout)
        payload = {'version': True, 'scopes': []}
        result = self.cli({'BlindTests.swift': source}, {'blindScopeFile': 'scopes.json'},
                          {'scopes.json': json.dumps(payload)})
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('must contain version 1', result.stdout)

    def test_other_languages_remain_on_their_existing_extractor(self):
        result = self.scan('func testClean() { write(); read() }', {
            'ExampleTests.rs': 'fn blind() { write(); }',
            'ExampleTests.ts': 'it("blind arrow", () => { write(); });',
        })
        self.assertEqual(set(self.names(result)), {'blind', 'blind arrow'})
        self.assertEqual(result['examined'], 3)
        self.assertEqual(result['specBlocks'], 1)
        self.assertEqual(result['notMeasured'], [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
