#!/usr/bin/env python3
"""Safety/transport behavior tests; never contact live sessions."""
import copy
import datetime as dt
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import fleet_sessions as fleet


class FleetTests(unittest.TestCase):
    def packet(self, **changes):
        p = {"packet_id": "dispatch-1", "provider": "codex",
             "session_id": "00000000-0000-4000-8000-000000000001",
             "cwd": "/tmp/owned-repo", "observed_at": fleet.now().isoformat(),
             "state": "idle", "task": "approved build", "owner": "conductor",
             "evidence": "roster and plan", "reviewed_original_authorization": True,
             "owns_coordination": True, "no_pending_owner_or_permission_decision": True,
             "message": "Literal `$(touch /tmp/should-not-exist)`\ncontinue approved step"}
        p.update(changes)
        return p

    def test_shell_characters_preserved_as_one_argument(self):
        p = self.packet()
        r = fleet.plan(p)
        self.assertEqual(r["argv"][-1], p["message"])
        self.assertIsNone(r["stdin"])

    def test_terminal_and_unknown_states_refused(self):
        for state in ["completed", "cancelled", "blocked", "waiting", "shell", "unknown"]:
            with self.subTest(state=state), self.assertRaises(ValueError):
                fleet.plan(self.packet(state=state))

    def test_stale_future_and_naive_observation_refused(self):
        for stamp in [(fleet.now()-dt.timedelta(minutes=6)).isoformat(),
                      (fleet.now()+dt.timedelta(minutes=1)).isoformat(), "2026-09-30T09:00:00"]:
            with self.subTest(stamp=stamp), self.assertRaises(ValueError):
                fleet.plan(self.packet(observed_at=stamp))

    def test_missing_owner_or_grant_refused(self):
        for key in ["owns_coordination", "reviewed_original_authorization", "no_pending_owner_or_permission_decision"]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                fleet.plan(self.packet(**{key: False}))

    def test_unsupported_provider_and_short_id_refused(self):
        for change in [dict(provider="claude"), dict(provider="grok"), dict(session_id="short"), dict(cwd="relative")]:
            with self.subTest(change=change), self.assertRaises(ValueError):
                fleet.plan(self.packet(**change))

    def test_probe_timeout_is_uncertain(self):
        with patch.object(subprocess, "run", side_effect=subprocess.TimeoutExpired(
                ["codex"], 1, output=b'{"success":true,"msg_id":"fixture"}', stderr=b'late hook')):
            receipt = fleet.probe(["codex"])
            self.assertEqual(receipt["status"], "timeout")
            self.assertIsNone(receipt["returncode"])
            self.assertEqual(json.loads(receipt["stdout"])["msg_id"], "fixture")
            self.assertEqual(receipt["stderr"], "late hook")

    def test_send_journal_survives_timeout_and_suppresses_retry(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(fleet, "preflight", return_value="/bin/codex"), patch.object(fleet, "probe", return_value={"status": "timeout", "returncode": None}) as transport:
            journal = Path(temp)/"dispatch.json"
            p = self.packet()
            self.assertEqual(fleet.execute(p, journal)["status"], "uncertain_or_failed")
            self.assertEqual(fleet.execute(p, journal)["status"], "duplicate_suppressed")
            self.assertEqual(fleet.execute(self.packet(packet_id="new-id"), journal)["status"], "duplicate_suppressed")
            self.assertEqual(transport.call_count, 1)
            self.assertEqual(json.loads(journal.read_text())[0]["session_id"], p["session_id"])
            changed = copy.deepcopy(p)
            changed["message"] = "changed"
            with self.assertRaises(ValueError):
                fleet.execute(changed, journal)

    def test_closed_muse_ingress_prevents_send(self):
        outputs = [{"returncode": 0, "stdout": "send --target"},
                   {"returncode": 0, "stdout": json.dumps({"status": "unavailable", "error_code": "external_agent_ingress_closed"})}]
        with patch.object(fleet.shutil, "which", return_value="/bin/muse"), patch.object(fleet, "probe", side_effect=outputs):
            with self.assertRaisesRegex(ValueError, "ingress unavailable"):
                fleet.preflight(self.packet(provider="muse"))

    def test_muse_uuid_and_cwd_must_match_listing(self):
        for listing in [[{"session_id": self.packet()["session_id"], "cwd": "/wrong"}], {"unexpected": []}]:
            outputs = [{"returncode": 0, "stdout": "send --target"}, {"returncode": 0, "stdout": json.dumps(listing)}]
            with patch.object(fleet.shutil, "which", return_value="/bin/muse"), patch.object(fleet, "probe", side_effect=outputs):
                with self.assertRaises(ValueError):
                    fleet.preflight(self.packet(provider="muse"))

    def test_success_is_transport_evidence_only(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(fleet, "preflight", return_value="/bin/codex"), patch.object(fleet, "probe", return_value={"returncode": 0, "stdout": "queued"}):
            row = fleet.execute(self.packet(), Path(temp)/"journal.json")
            self.assertEqual(row["status"], "transport_returned_success")
            self.assertNotIn("completed", row)


if __name__ == "__main__":
    unittest.main()
