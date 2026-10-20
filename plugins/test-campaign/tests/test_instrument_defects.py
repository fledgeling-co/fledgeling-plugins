#!/usr/bin/env python3
"""Regression fixtures for the instrument defects in the mcp-router registry.

Each test builds the smallest campaign that trips one defect, runs the real script
against it, and asserts the observable the defect corrupted. Each was watched to fail
against the 0.20.0 scripts before its fix, so none of them passes by construction.
"""
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/test-campaign/scripts'
PY = sys.executable


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace('-', '_'), SCRIPTS / f'{name}.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(script, *args, env=None):
    return subprocess.run([PY, str(SCRIPTS / script), *args], capture_output=True, text=True,
                          env=env, timeout=120)


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=1) + '\n', encoding='utf-8')


class InstrumentDefects(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='instrument-defect-tests-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def campaign(self, name, inventory, cases):
        d = self.root / name
        self.assertEqual(run('campaign.py', 'init', str(d), '--project', 'Fixture',
                             '--lanes', 'web').returncode, 0)
        write_json(d / 'inventory.json', inventory)
        write_json(d / 'cases.json', cases)
        return d

    # DEF-061 — a route template is a family of addresses, one per parameter value.
    def test_route_template_ties_to_one_segment_and_nothing_more(self):
        tie = load('capture-lineage').tie
        route = 'app://mac/servers/{server}/document'
        self.assertEqual(tie('mac/servers/g17-capability/document', route), (True, ''))
        self.assertEqual(tie('app://mac/servers/g17/document', 'app://mac/servers/:server/document'),
                         (True, ''))
        self.assertEqual(tie('mac/servers/g17/document', 'app://mac/servers/*/document'), (True, ''))
        self.assertFalse(tie('mac/servers/g17/logs', route)[0], 'a literal segment must still match')
        self.assertFalse(tie('mac/servers/a/b/document', route)[0], 'one parameter is one segment')
        self.assertFalse(tie('mac/servers//document', route)[0], 'a parameter is non-empty')
        self.assertEqual(tie('mac/servers/a/document', 'app://mac/servers/a/document'), (True, ''))
        self.assertFalse(tie('x', 'src/app.tsx')[0], 'a source-file route is still refused')

    # DEF-051 — a pair with a design render and no build capture is not comparable.
    def test_worklist_demotes_a_pair_with_no_build_capture(self):
        d = self.root / 'worklist'
        shots = d / 'evidence/shots'
        for name in ('mock/SURF-001.png', 'mock/SURF-002.png', 'SURF-001.build.png'):
            (shots / name).parent.mkdir(parents=True, exist_ok=True)
            (shots / name).write_bytes(b'\x89PNG')
        write_json(shots / 'pairs.json', [
            {'surface': 'SURF-001', 'reference': 'evidence/shots/mock/SURF-001.png',
             'shot': 'evidence/shots/SURF-001.build.png', 'viewport': {'width': 1, 'height': 1},
             'settleMs': 0},
            {'surface': 'SURF-002', 'reference': 'evidence/shots/mock/SURF-002.png',
             'shot': None, 'reason': 'build half uncaptured', 'viewport': {'width': 1, 'height': 1},
             'settleMs': 0},
        ])
        result = run('witness-worklist.py', str(d))
        # Exit 1 is the script's own answer while any surface is uncompared: it is not a pass.
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn('pairs=2  judgeable=1  WITHOUT a reference=1', result.stdout)
        judged = json.loads((d / 'witness-worklist.json').read_text(encoding='utf-8'))
        self.assertEqual([p['surface'] for p in judged], ['SURF-001'])

    # DEF-054 — the uncorroborated report must name the file, not only the surface.
    def test_uncorroborated_report_names_the_attached_file(self):
        d = self.root / 'attach'
        write_json(d / 'inventory.json', {'surface': [{'id': 'SURF-001', 'name': 'Servers',
                                                       'route': '/servers'}]})
        (d / 'evidence/shots').mkdir(parents=True)
        (d / 'evidence/shots/SURF-001.png').write_bytes(b'\x89PNG')
        result = run('attach-shots.py', str(d))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertRegex(result.stdout, r'(?m)^\s+SURF-001\s+evidence/shots/SURF-001\.png$')

    # DEF-056 and DEF-052 — every case prints, and open defects are named in the ledger.
    def test_ledger_prints_every_case_and_the_open_defects(self):
        inventory = {
            'surface': [{'id': 'SURF-001', 'label': 'Servers', 'route': '/servers', 'lane': 'web'}],
            'defect': [
                {'id': 'DEF-901', 'severity': 'high', 'status': 'open · detector',
                 'title': 'Open registry defect'},
                {'id': 'DEF-902', 'severity': 'low', 'status': 'fixed', 'title': 'Closed defect'},
            ],
        }
        cases = [
            {'id': 'CASE-0001', 'surface': 'SURF-001', 'lane': 'web', 'status': 'pass', 'armed': True},
            {'id': 'CASE-0002', 'lane': 'router-daemon', 'status': 'pass'},
        ]
        d = self.campaign('ledger', inventory, cases)
        result = run('campaign.py', 'report', str(d))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        ledger = (d / 'ledger.md').read_text(encoding='utf-8')
        self.assertIn('CASE-0001', ledger)
        self.assertIn('CASE-0002', ledger, 'a case with no surface must still be printed')
        self.assertIn('1 open defect(s)', ledger)
        self.assertIn('- DEF-901 · high · Open registry defect', ledger)
        self.assertNotIn('DEF-902', ledger, 'a closed defect is not an open one')

    # DEF-052 — the evidence page renders the registry, not only failing cases.
    def test_evidence_page_renders_open_defects(self):
        inventory = {'surface': [], 'defect': [
            {'id': 'DEF-903', 'severity': 'medium', 'status': 'open', 'text': 'Registry-only defect'}]}
        d = self.campaign('page', inventory, [])
        result = run('evidence-page.py', str(d))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        page = (d / 'evidence.html').read_text(encoding='utf-8')
        self.assertIn('Open defects in the registry', page)
        self.assertIn('DEF-903', page)
        self.assertIn('Registry-only defect', page)

    # DEF-501 — the registry is UTF-8 whatever the host's console codepage says.
    def test_registry_reads_under_an_ascii_locale(self):
        d = self.campaign('encoding', {'surface': [{'id': 'SURF-001', 'label': 'Servers — list',
                                                    'route': '/servers'}]},
                          [{'id': 'CASE-0001', 'surface': 'SURF-001', 'lane': 'web', 'status': 'pass'}])
        # The read is the defect under test. stdout is pinned to UTF-8 so a redirected ASCII
        # pipe cannot fail the print that follows the write; a Windows console is not that pipe.
        env = dict(os.environ, PYTHONUTF8='0', PYTHONCOERCECLOCALE='0', LC_ALL='C', PYTHONIOENCODING='utf-8')
        result = run('campaign.py', 'report', str(d), env=env)
        self.assertNotIn('UnicodeDecodeError', result.stderr)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Servers — list', (d / 'ledger.md').read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
