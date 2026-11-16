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

    def run_gate(self):
        (self.root / 'inventory.json').write_text(json.dumps(self.inventory))
        (self.root / 'campaign.json').write_text(json.dumps(self.config))
        return subprocess.run([sys.executable, str(SCRIPT), str(self.root), '--gate'],
                              text=True, capture_output=True, timeout=20)

    def test_complete_clean_measurement_passes(self):
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('blind:      examined=1', result.stdout)

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


if __name__ == '__main__':
    unittest.main()
