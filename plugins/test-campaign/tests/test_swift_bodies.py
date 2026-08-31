#!/usr/bin/env python3
"""Actual blind pass and public CLI fixtures; no Swift toolchain or third-party dependency."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/test-campaign/scripts/vacuity-check.py'
SPEC = importlib.util.spec_from_file_location('vacuity_swift_tests', SCRIPT)
SCAN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SCAN)


class SwiftBodies(unittest.TestCase):
    def scan(self, source, extras=None):
        with tempfile.TemporaryDirectory(prefix='swift-body-tests-') as directory:
            root = Path(directory)
            (root / 'ExampleTests.swift').write_text(source)
            for name, text in (extras or {}).items(): (root / name).write_text(text)
            return SCAN.pass_blind(root, ('write', 'store'), ('read', 'load', 'expect'))

    def names(self, result):
        return [item.split(' — ')[0] for item in result['findings']]

    def cli(self, files):
        with tempfile.TemporaryDirectory(prefix='swift-body-cli-tests-') as directory:
            root = Path(directory)
            (root / 'tests').mkdir()
            (root / 'inventory.json').write_text(json.dumps({'requirement': [
                {'id': 'REQ-001', 'title': 'Counter', 'effect': 'none'}]}))
            (root / 'campaign.json').write_text(json.dumps({'testRoot': 'tests',
                'blindVocabulary': {'only': True, 'mutators': ['write'], 'readers': ['read']}}))
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
