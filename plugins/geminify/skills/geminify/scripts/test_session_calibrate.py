"""Regression cases for exact skill source identity, without reading user plugins."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("session_calibrate", Path(__file__).with_name("session_calibrate.py"))
calibrate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calibrate)


class SourceResolutionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.roots = patch.object(calibrate, "PLUGIN_ROOTS", [self.root])
        self.roots.start()
        self.addCleanup(self.roots.stop)

    def plugin(self, plugin, skill, version="1.0.0", directory=None):
        base = self.root / plugin / version
        manifest = base / ".claude-plugin/plugin.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(json.dumps({"name": plugin, "version": version}))
        target = base / "skills" / (directory or skill)
        target.mkdir(parents=True, exist_ok=True)
        (target / "SKILL.md").write_text(f"---\nname: {skill}\n---\n")
        return target

    def test_exact_plugin_and_declared_name_resolve(self):
        target = self.plugin("shipyard", "triage", directory="internal-dir")
        self.assertEqual(calibrate.find_skill_dir("shipyard:triage"), target)
        self.assertIsNone(calibrate.find_skill_dir("shipyard:internal-dir"))

    def test_wrong_prefix_and_bare_plugin_skill_do_not_resolve(self):
        self.plugin("ship-feature", "ship-feature")
        for name in ["ship-feature", "other:ship-feature", "plugin:ship-feature:ship-feature", "fledgeling-plugins:ship-feature"]:
            with self.subTest(name=name):
                self.assertIsNone(calibrate.find_skill_dir(name))

    def test_newer_semver_beats_lexical_order(self):
        self.plugin("example", "review", "1.9.0")
        target = self.plugin("example", "review", "1.10.0")
        self.assertEqual(calibrate.find_skill_dir("example:review"), target)

    def test_standalone_skill_keeps_its_bare_identity(self):
        target = self.root / "standalone"
        target.mkdir()
        (target / "SKILL.md").write_text("---\nname: skill-creator\n---\n")
        self.assertEqual(calibrate.find_skill_dir("skill-creator"), target)
        self.assertIsNone(calibrate.find_skill_dir("invented:skill-creator"))

    def test_command_does_not_swallow_a_plugin_prefix(self):
        with patch.object(calibrate, "COMMAND_ROOTS", [self.root]):
            (self.root / "review.md").write_text("Review source.")
            self.assertEqual(calibrate.find_command("review"), self.root / "review.md")
            self.assertIsNone(calibrate.find_command("invented:review"))

    def test_source_receipt_is_labelled_as_source_only(self):
        self.plugin("example", "review")
        result = calibrate.build(["example:review"], "Gemini 3.8")
        self.assertTrue(result["coverage"][0]["resolved"])
        self.assertIn("source-only", result["resolutionEvidence"])


if __name__ == "__main__":
    unittest.main()
