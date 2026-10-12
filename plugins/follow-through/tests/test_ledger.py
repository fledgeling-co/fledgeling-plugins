"""Fixture-only behavioral invariants; no accounts, connectors or network."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ledger", ROOT / "scripts/ledger.py")
ledger = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ledger)


def fixture():
    return {"schema_version": 1, "goal": "Review selected notices", "stop_condition": "Each has a next action",
            "as_of": "2026-09-30T12:00:00Z", "sources": [{"id": "s1", "kind": "current",
            "scope": "example", "locator": "fixture://billing/1", "observed_at": "2026-09-30T11:45:00Z"}],
            "items": [{"id": "i1", "domain": "ops", "scope": "example", "identity": "credit-1",
            "state": "actionable", "summary": "Credit deadline needs a decision", "owner": "operator",
            "evidence": ["s1"], "volatile": True, "max_age_hours": 1, "next_action": "Prepare options"}]}


class LedgerTests(unittest.TestCase):
    def test_fresh_direct_source(self):
        self.assertEqual(ledger.validate(fixture()), [])

    def test_history_is_not_current_even_when_recent(self):
        d = fixture(); d["sources"][0]["kind"] = "history"
        self.assertTrue(ledger.validate(d))

    def test_fresh_read_of_old_report_cannot_prove_balance(self):
        d = fixture(); d["sources"][0].update(kind="reported", event_at="2026-08-01T10:00:00Z")
        self.assertTrue(ledger.validate(d))

    def test_expired_source(self):
        d = fixture(); d["as_of"] = "2026-09-30T14:00:00Z"
        self.assertTrue(ledger.validate(d))

    def test_timezone_and_future_observations(self):
        for value in ["2026-09-30T13:00:00Z", "2026-09-30T11:00:00"]:
            d = fixture(); d["sources"][0]["observed_at"] = value
            self.assertTrue(ledger.validate(d))

    def test_duplicates_fail_instead_of_disappearing(self):
        d = fixture(); duplicate = copy.deepcopy(d["items"][0]); duplicate["id"] = "i2"
        d["items"].append(duplicate)
        self.assertTrue(ledger.validate(d))

    def test_same_identity_different_account_is_not_duplicate(self):
        d = fixture(); source = copy.deepcopy(d["sources"][0]); source.update(id="s2", scope="other")
        item = copy.deepcopy(d["items"][0]); item.update(id="i2", scope="other", evidence=["s2"])
        d["sources"].append(source); d["items"].append(item)
        self.assertEqual(ledger.validate(d), [])

    def test_cross_account_join_fails(self):
        d = fixture(); d["sources"][0]["scope"] = "other"
        self.assertTrue(ledger.validate(d))

    def test_completion_requires_result_and_current_evidence(self):
        d = fixture(); d["items"][0]["state"] = "completed"
        self.assertTrue(ledger.validate(d))
        d["items"][0].update(outcome="Balance verified", completion_evidence=["s1"])
        self.assertEqual(ledger.validate(d), [])
        d["sources"][0]["kind"] = "history"
        self.assertTrue(ledger.validate(d))

    def test_unknown_has_visible_next_step(self):
        d = fixture(); d["items"][0].update(state="unverified", evidence=[])
        self.assertEqual(ledger.validate(d), [])
        del d["items"][0]["next_action"]
        self.assertTrue(ledger.validate(d))

    def test_bad_source_link_and_dismissal(self):
        d = fixture(); d["items"][0]["evidence"] = ["missing"]
        self.assertTrue(ledger.validate(d))
        d = fixture(); d["items"][0]["state"] = "dismissed"
        self.assertTrue(ledger.validate(d))

    def test_summary_keeps_unresolved_denominator(self):
        d = fixture(); d["items"][0].update(state="blocked", evidence=[])
        s = ledger.summary(d)
        self.assertEqual(s["total"], 1); self.assertEqual(s["counts"]["blocked"], 1)
        self.assertEqual(s["items"][0]["next_action"], "Prepare options")

    def test_cli_is_read_only_and_failure_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "ledger.json"; content = json.dumps(fixture())
            path.write_text(content)
            for command in ["check", "summary"]:
                run = subprocess.run([sys.executable, str(ROOT / "scripts/ledger.py"), command, str(path)], capture_output=True)
                self.assertEqual(run.returncode, 0); self.assertEqual(path.read_text(), content)
            d = fixture(); d["sources"][0]["kind"] = "history"; path.write_text(json.dumps(d))
            run = subprocess.run([sys.executable, str(ROOT / "scripts/ledger.py"), "summary", str(path)], capture_output=True)
            self.assertEqual(run.returncode, 1)

    def test_bad_structures_are_errors_not_tracebacks(self):
        for data in [None, [], {"sources": None}, {"schema_version": 1, "goal": "x", "stop_condition": "x",
                    "as_of": "2026-09-30T12:00:00Z", "sources": [None], "items": [None]}]:
            self.assertTrue(ledger.validate(data))

    def test_malformed_enums_and_numbers_do_not_crash(self):
        for section, field, value in [("sources", "kind", []), ("items", "domain", {}),
                                      ("items", "state", []), ("items", "max_age_hours", True),
                                      ("items", "max_age_hours", float("nan"))]:
            d = fixture(); d[section][0][field] = value
            self.assertTrue(ledger.validate(d))


if __name__ == "__main__":
    unittest.main()
