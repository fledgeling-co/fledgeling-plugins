#!/usr/bin/env python3
"""The scanner's own gate must distinguish incomplete work from zero findings."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'skills/test-campaign/scripts/vacuity-check.py'


class VacuityGateCoverage(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='vacuity-coverage-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / 'tests').mkdir()
        (self.root / 'tests' / 'ExampleTests.swift').write_text('@Test func example() { write(); read() }\n')
        self.inventory = {'requirement': [{'id': 'REQ-001', 'title': 'Counter', 'effect': 'none'}]}
        self.config = {'testRoot': 'tests', 'blindVocabulary': {'only': True, 'mutators': ['write'], 'readers': ['read']}}

    def run_gate(self, *options):
        (self.root / 'inventory.json').write_text(json.dumps(self.inventory))
        (self.root / 'campaign.json').write_text(json.dumps(self.config))
        return subprocess.run([sys.executable, str(SCRIPT), str(self.root), '--gate', *options],
                              text=True, capture_output=True, timeout=20)

    def test_complete_clean_measurement_passes(self):
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('blind:      examined=1', result.stdout)

    def test_manifest_reports_execution_and_zero_external_requirements(self):
        result = self.run_gate('--coverage-json')
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['schema'], 1)
        self.assertTrue(report['complete'])
        self.assertEqual(report['findings'], 0)
        self.assertEqual([(row['name'], row['population'], row['complete']) for row in report['passes']],
                         [('unclassed', 1, True), ('uncensused', 0, True), ('blind', 1, True)])
        self.assertIn('blind:      examined=1', result.stderr)

    def test_manifest_lists_skipped_passes_even_with_no_requirements(self):
        self.inventory['requirement'].clear()
        result = self.run_gate('--coverage-json')
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report['complete'])
        self.assertEqual([row['name'] for row in report['passes']], ['unclassed', 'uncensused', 'blind'])
        self.assertTrue(all(not row['complete'] and row['population'] is None for row in report['passes']))

    def test_manifest_preserves_partial_provider_results(self):
        self.inventory['requirement'][0].update(effect='filesystem-write', provider='SomeWriter')
        result = self.run_gate('--coverage-json')
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertFalse(report['complete'])
        provider_pass = next(row for row in report['passes'] if row['name'] == 'uncensused')
        self.assertFalse(provider_pass['complete'])
        self.assertEqual(provider_pass['population'], 1)

    def test_missing_test_root_holds_gate(self):
        del self.config['testRoot']
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('NOT RUN', result.stdout)
        self.assertIn('coverage=incomplete', result.stdout)

    def test_missing_test_directory_holds_gate(self):
        self.config['testRoot'] = 'does-not-exist'
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('SKIPPED', result.stdout)
        self.assertIn('coverage=incomplete', result.stdout)

    def test_empty_only_vocabulary_holds_gate(self):
        self.config['blindVocabulary']['mutators'] = []
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('NOT RUN', result.stdout)
        self.assertIn('coverage=incomplete', result.stdout)

    def test_unmeasured_test_file_marks_coverage_incomplete(self):
        (self.root / 'tests' / 'ExampleTests.swift').write_text('@Test func example() { writer.write { value in consume(value) }; read() }\n')
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('NOT MEASURED', result.stdout)
        self.assertIn('coverage=incomplete', result.stdout)

    def test_invalid_scope_marks_coverage_incomplete(self):
        self.config['blindScopeFile'] = 'missing-scopes.json'
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('INVALID SCOPE', result.stdout)
        self.assertIn('coverage=incomplete', result.stdout)

    def test_vocabulary_misfit_marks_coverage_incomplete(self):
        (self.root / 'tests' / 'ExampleTests.swift').write_text('@Test func example() { read() }\n')
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('VOCABULARY DOES NOT FIT', result.stdout)
        self.assertIn('coverage=incomplete', result.stdout)

    def test_missing_source_root_holds_gate_when_providers_need_resolution(self):
        self.inventory['requirement'][0].update(effect='filesystem-write', provider='SomeWriter')
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('NOT CHECKED', result.stdout)
        self.assertIn('coverage=incomplete', result.stdout)

    def test_invalid_declared_source_root_holds_gate(self):
        self.config['sourceRoot'] = 'does-not-exist'
        result = self.run_gate()
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn('NOT RESOLVED', result.stdout)
        self.assertIn('coverage=incomplete', result.stdout)

    def add_provider_tree(self):
        (self.root / 'Sources/scripts').mkdir(parents=True)
        (self.root / 'Sources/Driver.swift').write_text('func FallbackSymbol() {}\n')
        (self.root / 'Sources/scripts/stale.sh').write_text('# same path under the wrong root\n')
        project = self.root / 'project'
        for directory in ('scripts', 'scripts-other', 'Tests'):
            (project / directory).mkdir(parents=True, exist_ok=True)
        (project / 'scripts/run.sh').write_text('# OnlyInSupplementalTree\n')
        (project / 'scripts-other/run.sh').write_text('# neighbouring path\n')
        (project / 'Tests/Allowed.swift').write_text('func ownedFixture() {}\n')
        (project / 'Tests/Other.swift').write_text('func otherFixture() {}\n')
        self.config.update(sourceRoot='Sources', providerPaths={
            'root': 'project', 'include': ['scripts', 'Tests/Allowed.swift'],
        })
        return project

    def test_supplemental_providers_require_an_exact_allowed_file_claim(self):
        self.add_provider_tree()
        for provider, expected in (
            ('scripts/run.sh', 0), ('./scripts/run.sh', 0), ('Tests/Allowed.swift', 0),
            ('scripts-other/run.sh', 1), ('Tests/Other.swift', 1), ('scripts/', 1),
            ('run.sh', 1), ('OnlyInSupplementalTree', 1),
            ('scripts/stale.sh FallbackSymbol', 1),
            ('scripts/../scripts/run.sh', 1), ('scripts/stale.sh\0 FallbackSymbol', 1),
        ):
            with self.subTest(provider=provider):
                self.inventory['requirement'][0].update(effect='subprocess', provider=provider)
                result = self.run_gate('--coverage-json')
                self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
                self.assertTrue(json.loads(result.stdout)['complete'])

    def test_supplemental_provider_rejects_linked_file_and_linked_directory(self):
        project = self.add_provider_tree()
        script = project / 'scripts-other/run.sh'
        (project / 'scripts/linked.sh').symlink_to(script)
        (project / 'scripts/linked-dir').symlink_to(script.parent, target_is_directory=True)
        for provider in ('scripts/linked.sh', 'scripts/linked-dir/run.sh'):
            with self.subTest(provider=provider):
                self.inventory['requirement'][0].update(effect='subprocess', provider=provider)
                self.assertEqual(self.run_gate().returncode, 1)

    def test_invalid_provider_path_scope_cannot_clear_coverage(self):
        project = self.add_provider_tree()
        (project / 'scripts/alias.sh').symlink_to(project / 'scripts/run.sh')
        for include in ([], ['missing'], ['scripts/alias.sh'], ['scripts//run.sh'],
                        ['scripts', 'scripts/run.sh'], ['scripts', './scripts'],
                        ['../Sources'], ['/scripts'], ['scripts/run.sh\0']):
            with self.subTest(include=include):
                self.config['providerPaths']['include'] = include
                result = self.run_gate('--coverage-json')
                self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                self.assertFalse(json.loads(result.stdout)['complete'])
                self.assertIn('invalid providerPaths', result.stderr)


if __name__ == '__main__':
    unittest.main()
