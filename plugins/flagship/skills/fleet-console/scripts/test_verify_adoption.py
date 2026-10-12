import copy
from pathlib import Path
import tempfile
import unittest
import verify_adoption as adoption

class AdoptionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name)/'source.md'
        self.cache = Path(self.temp.name)/'cached.md'
        self.source.write_text('---\nname: fleet-console\n---\nOwned continuation.')
        self.cache.write_bytes(self.source.read_bytes())
        self.target = 'flagship@example-market'
        self.rows = [{'pluginId': self.target, 'version': '1.7.1', 'installed': True, 'enabled': True},
                     {'pluginId': 'other@example-market', 'version': '2.0.0', 'installed': True, 'enabled': True}]
        self.codex = {'installed': self.rows, 'available': []}

    def verify(self, before=None, after=None, provider='codex'):
        return adoption.verify(self.codex if before is None else before,
                               self.codex if after is None else after, provider,
                               self.target, '1.7.1', self.source, self.cache)

    def test_correct_codex_installed_schema_and_hash(self):
        r = self.verify()
        self.assertEqual(r['installed_count'], 2)
        self.assertEqual(r['other_count'], 1)
        self.assertIn('not established', r['active_session_loaded'])

    def test_empty_wrong_schema_available_only_and_malformed_refused(self):
        for snapshot in [{}, {'plugins': []}, {'installed': []}, {'available': self.rows},
                         {'installed': [None]}, {'installed': [{'name': 'unknown'}]}]:
            with self.subTest(snapshot=snapshot), self.assertRaises(ValueError):
                self.verify(snapshot, snapshot)

    def test_missing_duplicate_disabled_uninstalled_and_old_version_refused(self):
        cases = [self.rows[1:], self.rows+self.rows[:1]]
        for change in [{'enabled': False}, {'installed': False}, {'version': '1.6.0'}]:
            rows = copy.deepcopy(self.rows); rows[0].update(change); cases.append(rows)
        for rows in cases:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                self.verify(after={'installed': rows})

    def test_unrelated_state_changes_and_new_install_refused(self):
        for field, value in [('enabled', False), ('version', '3.0.0'), ('pluginId', 'different@example')]:
            rows = copy.deepcopy(self.rows); rows[1][field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.verify(after={'installed': rows})
        with self.assertRaises(ValueError): self.verify(before={'installed': self.rows[1:]})

    def test_empty_and_mismatched_cache_refused(self):
        for text in ['', 'old installed skill']:
            self.cache.write_text(text)
            with self.assertRaises(ValueError): self.verify()
        self.source.write_text(''); self.cache.write_text('')
        with self.assertRaises(ValueError): self.verify()

    def test_claude_schema_and_ambiguous_scope(self):
        rows = [{'id': self.target, 'version': '1.7.1', 'scope': 'user', 'enabled': True}]
        self.assertEqual(self.verify(rows, rows, 'claude')['installed_count'], 1)
        with self.assertRaises(ValueError):
            self.verify(rows, rows+[dict(rows[0], scope='project')], 'claude')

if __name__ == '__main__': unittest.main()
