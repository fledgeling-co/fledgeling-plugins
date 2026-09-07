"""Regression cases for the source reference gate (no model calls)."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from check_skill_references import audit, references


class SkillReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".claude-plugin").mkdir()
        entries = []
        for plugin, children in {"shipyard": ["shipyard", "triage"], "ship-feature": ["ship-feature"]}.items():
            directory = self.root / "plugins" / plugin
            (directory / ".claude-plugin").mkdir(parents=True)
            (directory / ".claude-plugin/plugin.json").write_text(json.dumps({"name": plugin}))
            for child in children:
                skill = directory / "skills" / child
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text(f"---\nname: {child}\n---\n# {child}\n")
            entries.append({"name": plugin, "source": f"./plugins/{plugin}"})
        (self.root / ".claude-plugin/marketplace.json").write_text(json.dumps({"plugins": entries}))
        self.skill = self.root / "plugins/ship-feature/skills/ship-feature/SKILL.md"

    def check_text(self, text):
        self.skill.write_text(text)
        return audit(self.root)

    def test_resolves_every_subskill_not_only_plugin_main(self):
        result = self.check_text('Use `shipyard:triage`.\nSkill({skill: "ship-feature:ship-feature"})')
        self.assertEqual(result["skills"], 3)
        self.assertEqual(result["findings"], [])

    def test_all_three_failure_shapes(self):
        result = self.check_text('Invoke `ship-feature`.\nUse `plugin:ship-feature:ship-feature`.\nUse `create-test-suite:create-test-suite`.\nUse `shipyard:missing`.')
        self.assertEqual({i["code"] for i in result["findings"]}, {"bare-plugin-skill", "invented-namespace", "retired-skill", "missing-local-skill"})

    def test_bare_prose_slash_and_json_calls(self):
        result = self.check_text('The `ship-feature` skill owns delivery.\n/ship-feature fix the bug\n{"skill": "triage"}')
        self.assertEqual(len(result["findings"]), 3)

    def test_paths_frontmatter_css_markers_and_standalone_are_not_calls(self):
        result = self.check_text('---\nname: ship-feature\n---\n# ship-feature\nRead `skills/ship-feature/SKILL.md`.\nUse `skill-creator`.\nUse `/verify`.\n<!-- mac-craft:metrics -->\nfont-family:system-ui;\n')
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["external_references"], [])

    def test_historical_records_stay_outside_gate(self):
        root = self.skill.parent
        (root / "evals").mkdir()
        (root / "evals/old.md").write_text('Invoke `ship-feature`.')
        (root / "references").mkdir()
        (root / "references/evidence.md").write_text('Use `create-test-suite:create-test-suite`.')
        result = self.check_text('Use `ship-feature:ship-feature`.')
        self.assertEqual(result["findings"], [])
        self.assertFalse(any("evals" in name or "evidence.md" in name for name in result["inventory"]))

    def test_quoted_runner_prompt_and_failure_clause_are_checked(self):
        result = self.check_text('> Invoke `ship-feature`.\nInvoke `ship-feature`; if it failed, report it.\nSkill({skill: "ship-feature"}) // record any Unknown skill failure')
        self.assertEqual(len(result["findings"]), 3)

    def test_reviewed_historical_excerpt_only_exempts_its_exact_line(self):
        text = 'The old call was `ship-feature`.\n> Invoke `ship-feature`.'
        found = list(references(text, {"ship-feature"}, ['The old call was `ship-feature`.']))
        self.assertEqual(found, [(2, "ship-feature", True)])

    def test_external_source_is_not_claimed_installed(self):
        result = self.check_text('Use `external-craft:external-craft` when installed.')
        self.assertEqual(result["findings"], [])
        self.assertEqual(result["external_references"], [{"identifier": "external-craft:external-craft", "source_resolved": False, "locations": [{"file": "plugins/ship-feature/skills/ship-feature/SKILL.md", "line": 1}]}])
        self.assertIn("runtime", result["limits"])

    def test_no_repeated_finding_for_same_call(self):
        found = list(references('Skill({skill: "shipyard:triage"})', {"triage"}))
        self.assertEqual(len(found), 1)

    def test_missing_relative_reference_fails_but_runtime_paths_do_not(self):
        result = self.check_text('[missing](references/missing.md)\n[here](SKILL.md#usage)\n[web](https://example.com/guide)\n[runtime](/tmp/output.md)')
        self.assertEqual([i["code"] for i in result["findings"]], ["broken-local-link"])

    def test_mismatched_declared_name_is_rejected(self):
        self.skill.write_text('---\nname: wrong-name\n---\n')
        with self.assertRaisesRegex(ValueError, "skill name differs"):
            audit(self.root)

    def test_unknown_explicit_skill_calls_fail_but_dynamic_values_are_not_guessed(self):
        result = self.check_text('Skill({skill: "totally-missing"})\n{"skill": "also-missing"}\nSkill({skill: selectedSkill})\nSkill(args)')
        self.assertEqual([(item["identifier"], item["code"]) for item in result["findings"]], [("totally-missing", "unknown-skill"), ("also-missing", "unknown-skill")])

    def test_unknown_qualified_slash_calls_have_external_locations(self):
        result = self.check_text('/diagram-design:doctor\n/diagram-design:export-diagram file')
        self.assertEqual(result["findings"], [])
        self.assertEqual([item["identifier"] for item in result["external_references"]], ["diagram-design:doctor", "diagram-design:export-diagram"])
        self.assertEqual([item["locations"][0]["line"] for item in result["external_references"]], [1, 2])

    def test_xml_tags_and_tscon_destination_are_not_skill_referrals(self):
        result = self.check_text('<dc:format>image/svg+xml</dc:format><dc:title></dc:title>\nUse `tscon %sessionname% /dest:console`.\nUse `/unknown-plugin:unknown-skill`.')
        self.assertEqual(result["findings"], [])
        self.assertEqual([item["identifier"] for item in result["external_references"]], ["unknown-plugin:unknown-skill"])

    def test_literal_tool_arguments_preserve_exact_syntax(self):
        result = self.check_text('Skill({skill: "/ship-feature:ship-feature"})\n{"skill": "Shipyard:triage"}\nSkill("shipyard:triage with args")\nSkill({skill: "<resolved-id>"})\nSkill({skill: selectedSkill})\nSkill("dynamic-" + suffix)')
        self.assertEqual([(item["identifier"], item["code"]) for item in result["findings"]], [("/ship-feature:ship-feature", "invalid-skill-identifier"), ("Shipyard:triage", "invalid-skill-identifier"), ("shipyard:triage with args", "invalid-skill-identifier")])

    def test_missing_skill_in_known_external_plugin_fails(self):
        external = self.root / "external"
        (external / ".claude-plugin").mkdir(parents=True)
        plugin = external / "plugins/remote"
        (plugin / ".claude-plugin").mkdir(parents=True)
        (plugin / ".claude-plugin/plugin.json").write_text(json.dumps({"name": "remote"}))
        skill = plugin / "skills/actual"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text('---\nname: actual\n---\n')
        (external / ".claude-plugin/marketplace.json").write_text(json.dumps({"plugins": [{"name": "remote", "source": "plugins/remote"}]}))
        self.skill.write_text('Use `remote:missing`.')
        result = audit(self.root, [external])
        self.assertEqual([item["code"] for item in result["findings"]], ["missing-external-skill"])

    def test_name_in_body_is_not_frontmatter_and_yaml_comments_are_accepted(self):
        result = self.check_text('---\ndescription: Example\n---\n```yaml\nname: another-config\n```')
        self.assertEqual(result["findings"], [])
        result = self.check_text('---\nname: "ship-feature" # stable identifier\n---\nname: unrelated-example')
        self.assertEqual(result["findings"], [])

    def test_historical_excerpt_does_not_hide_active_call_on_same_line(self):
        excerpt = 'The old call was `ship-feature`.'
        found = list(references(excerpt + ' Invoke `ship-feature`.', {"ship-feature"}, [excerpt]))
        self.assertEqual(found, [(1, "ship-feature", True)])

    def test_builtin_description_does_not_hide_a_later_plugin_call(self):
        found = list(references('The bundled `/code-review` command is separate. Invoke `code-review`.', {"code-review"}))
        self.assertEqual(found, [(1, "code-review", True)])

    def test_generated_instruction_templates_are_scanned(self):
        template = self.skill.parent / "templates/CLAUDE.header.tmpl"
        template.parent.mkdir()
        template.write_text('Invoke `ship-feature`.')
        result = audit(self.root)
        self.assertIn(str(template.relative_to(self.root)), result["inventory"])
        self.assertEqual(result["findings"][0]["code"], "bare-plugin-skill")

    def test_cli_exit_status_distinguishes_findings_from_source_only_unknowns(self):
        checker = Path(__file__).with_name("check_skill_references.py")
        def run(body):
            self.skill.write_text(body)
            return subprocess.run([sys.executable, str(checker), "--root", str(self.root), "--json"], text=True, capture_output=True)
        failed = run('Skill({skill: "totally-missing"})')
        self.assertEqual(failed.returncode, 1)
        self.assertEqual(json.loads(failed.stdout)["findings"][0]["code"], "unknown-skill")
        passed = run('Use `shipyard:triage`.')
        self.assertEqual(passed.returncode, 0)
        external = run('Use `unknown-plugin:unknown-skill`.')
        self.assertEqual(external.returncode, 0)
        self.assertFalse(json.loads(external.stdout)["external_references"][0]["source_resolved"])


if __name__ == "__main__":
    unittest.main()
