#!/usr/bin/env python3
"""Bounded native inventory and opt-in, journalled external sends. No shell/UI hacks."""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid

PROVIDERS = {"claude": "claude", "codex": "codex", "grok": "grok",
             "cursor": "cursor-agent", "muse": "muse"}


def now():
    return dt.datetime.now(dt.timezone.utc)


def probe(argv, stdin=None, timeout=12):
    try:
        r = subprocess.run(argv, input=stdin, text=True, capture_output=True,
                           timeout=timeout, shell=False)
        return {"argv": argv, "returncode": r.returncode, "stdout": r.stdout,
                "stderr": r.stderr, "status": "returned"}
    except subprocess.TimeoutExpired as e:
        # A final native receipt can precede slow shutdown hooks. Preserve evidence,
        # but a timeout never authorises an automatic retry or establishes delivery.
        def decoded(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        return {"argv": argv, "status": "timeout", "returncode": None,
                "stdout": decoded(e.stdout), "stderr": decoded(e.stderr)}
    except OSError as e:
        return {"argv": argv, "status": "unavailable", "error": str(e),
                "returncode": None}


def json_result(result):
    if result.get("returncode") != 0:
        raise ValueError("native probe failed or timed out")
    try:
        return json.loads(result["stdout"])
    except (KeyError, ValueError) as e:
        raise ValueError("native probe did not return valid JSON") from e


def inventory():
    result = {"schema_version": 1, "observed_at": now().isoformat(), "providers": {}}
    commands = {"claude": ["agents", "--json"],
                "muse": ["session-message", "list", "--json"],
                "grok": ["leader", "list"], "cursor": ["persist", "list"]}
    for provider, binary in PROVIDERS.items():
        path = shutil.which(binary)
        row = {"binary": path, "coverage": "native probe only; not all machine sessions"}
        result["providers"][provider] = row
        if path is None:
            row["status"] = "not_installed"
            continue
        row["version"] = probe([path, "--version"])
        row["help"] = probe([path, "--help"])
        if provider in commands:
            row["inventory"] = probe([path, *commands[provider]])
            if provider in {"claude", "muse"}:
                try:
                    data = json_result(row["inventory"])
                    row["sessions_or_status"] = data
                    if isinstance(data, dict) and data.get("status") == "unavailable":
                        row["status"] = "unavailable"
                except ValueError as e:
                    row["status"] = "unavailable"
                    row["error"] = str(e)
        else:
            row["status"] = "interactive_or_app_inventory_required"
            row["instructions"] = "Use Codex app list_threads/read_thread or codex agents TUI."
    return result


def validate_packet(p, at=None):
    required = ("packet_id", "provider", "session_id", "cwd", "observed_at",
                "state", "task", "owner", "evidence", "message")
    if not isinstance(p, dict) or any(not isinstance(p.get(k), str) or not p[k].strip()
                                      for k in required):
        raise ValueError("packet requires nonempty string identity, task, evidence and message fields")
    if p["provider"] not in {"codex", "muse"}:
        raise ValueError("only verified Codex queue and Muse send adapters are supported")
    try:
        if str(uuid.UUID(p["session_id"])) != p["session_id"]:
            raise ValueError()
    except ValueError as e:
        raise ValueError("use an exact canonical full session UUID") from e
    if not Path(p["cwd"]).is_absolute():
        raise ValueError("cwd must be absolute")
    if p["state"] not in {"idle", "working", "busy"}:
        raise ValueError("blocked/question/completed/cancelled/unknown targets cannot be sent to")
    for key in ("reviewed_original_authorization", "owns_coordination",
                "no_pending_owner_or_permission_decision"):
        if p.get(key) is not True:
            raise ValueError("missing review attestation: " + key)
    stamp = dt.datetime.fromisoformat(p["observed_at"].replace("Z", "+00:00"))
    if stamp.tzinfo is None or not -5 <= ((at or now()) - stamp).total_seconds() <= 300:
        raise ValueError("observation must be timezone-aware and less than five minutes old")
    if len(p["message"].encode()) > 16000:
        raise ValueError("send one bounded packet (maximum 16000 bytes)")
    return p


def plan(p):
    validate_packet(p)
    if p["provider"] == "codex":
        argv = ["codex", "queue", "--thread", p["session_id"], "--message", p["message"]]
        stdin = None
    else:
        argv = ["muse", "session-message", "send", "--target", p["session_id"], "--json"]
        stdin = p["message"]
    return {"status": "dry_run", "provider": p["provider"], "session_id": p["session_id"],
            "argv": argv, "stdin": stdin, "task": p["task"], "owner": p["owner"]}


def preflight(p):
    binary = shutil.which(PROVIDERS[p["provider"]])
    if binary is None:
        raise ValueError("provider binary not installed")
    help_args = ["queue", "--help"] if p["provider"] == "codex" else ["session-message", "--help"]
    help_result = probe([binary, *help_args])
    help_text = help_result.get("stdout", "") + help_result.get("stderr", "")
    expected = ["--thread", "--message"] if p["provider"] == "codex" else ["send", "--target"]
    if help_result.get("returncode") != 0 or not all(x in help_text for x in expected):
        raise ValueError("current CLI does not advertise the expected send adapter")
    if p["provider"] == "muse":
        listing = json_result(probe([binary, "session-message", "list", "--json"]))
        if isinstance(listing, dict) and listing.get("status") == "unavailable":
            raise ValueError("Muse ingress unavailable: " + str(listing.get("error_code")))
        # A changing vendor schema must be resolved manually, not guessed.
        sessions = listing if isinstance(listing, list) else listing.get("sessions") if isinstance(listing, dict) else None
        if not isinstance(sessions, list) or not any(isinstance(s, dict) and
            (s.get("session_id") == p["session_id"] or s.get("sessionId") == p["session_id"])
            and s.get("cwd") == p["cwd"] for s in sessions):
            raise ValueError("Muse target UUID/cwd not established by current native listing")
    return binary


def execute(p, journal):
    send = plan(p)
    binary = preflight(p)
    validate_packet(p)  # Probes may have used the remaining freshness window.
    journal = Path(journal)
    if journal.is_symlink():
        raise ValueError("journal must not be a symlink")
    journal.parent.mkdir(parents=True, exist_ok=True)
    content_hash = hashlib.sha256(json.dumps(p, sort_keys=True).encode()).hexdigest()
    dedup = hashlib.sha256(json.dumps([p["provider"], p["session_id"], p["message"]]).encode()).hexdigest()
    fd = os.open(journal, os.O_RDWR | os.O_CREAT | getattr(os, "O_NOFOLLOW", 0), 0o600)
    with os.fdopen(fd, "r+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        raw = f.read()
        rows = json.loads(raw) if raw else []
        if not isinstance(rows, list):
            raise ValueError("invalid journal; do not replace it")
        for row in rows:
            if row["packet_id"] == p["packet_id"]:
                if row["packet_sha256"] != content_hash:
                    raise ValueError("dispatch ID already used with different content")
                return {"status": "duplicate_suppressed", "previous": row}
            if row.get("dedup_sha256") == dedup:
                return {"status": "duplicate_suppressed", "previous": row}
        row = {"packet_id": p["packet_id"], "packet_sha256": content_hash,
               "dedup_sha256": dedup, "provider": p["provider"], "session_id": p["session_id"],
               "task": p["task"], "owner": p["owner"], "at": now().isoformat(),
               "status": "pending_uncertain"}
        rows.append(row)

        def save():
            f.seek(0)
            json.dump(rows, f, indent=2)
            f.write("\n")
            f.truncate()
            f.flush()
            os.fsync(f.fileno())

        save()  # Intent survives crash or timeout; never auto-retry.
        send["argv"][0] = binary
        row["receipt"] = probe(send["argv"], stdin=send["stdin"], timeout=20)
        row["status"] = "transport_returned_success" if row["receipt"].get("returncode") == 0 else "uncertain_or_failed"
        save()
        return row



def waiting_choice_route(p):
    """Read-only handoff plan. A peer receipt cannot resolve another host's callback."""
    if not isinstance(p, dict) or p.get("provider") != "claude":
        raise ValueError("choice planning requires an identified Claude target")
    if not isinstance(p.get("session_id"), str):
        raise ValueError("choice planning requires a string target UUID")
    try:
        if str(uuid.UUID(p["session_id"])) != p["session_id"]:
            raise ValueError()
    except (ValueError, KeyError) as e:
        raise ValueError("choice planning requires the canonical full target UUID") from e
    if p.get("state") != "waiting" or p.get("waiting_tool") != "AskUserQuestion":
        raise ValueError("this planner handles an exact waiting clarification, not permissions or ordinary idle work")
    for key in ("identity_verified", "original_scope_reviewed", "explicit_user_decision"):
        if p.get(key) is not True:
            raise ValueError("missing choice review attestation: " + key)
    if not isinstance(p.get("observed_at"), str):
        raise ValueError("choice planning requires an observation timestamp")
    stamp = dt.datetime.fromisoformat(p["observed_at"].replace("Z", "+00:00"))
    if stamp.tzinfo is None or not -5 <= (now()-stamp).total_seconds() <= 300:
        raise ValueError("choice observation must be fresh and timezone-aware")
    choices, selected = p.get("choices"), p.get("selected_label")
    if not isinstance(choices, list) or not choices or not all(isinstance(c, str) and c.strip() for c in choices):
        raise ValueError("use the exact choices emitted by the current tool request")
    if not isinstance(selected, str) or choices.count(selected) != 1:
        raise ValueError("the settled user decision must match exactly one current choice label")
    version = p.get("cli_version")
    if not isinstance(version, str) or not version.strip():
        raise ValueError("record the observed CLI version")
    base = {"status": "dry_run", "session_id": p["session_id"], "cli_version": version,
            "selected_label": selected, "peer_message": "does not establish callback resolution",
            "prompt_answered": False}
    if p.get("supported_controls_reviewed") is not True:
        return dict(base, route="recheck_current_supported_controls",
                    next_step="Review current help/documentation before requesting local input")
    kind = p.get("kind")
    if kind not in {"interactive", "background", "sdk"}:
        raise ValueError("target runtime kind must be established")
    # Capability observations are per-run facts, not permanent provider prohibitions.
    if kind == "sdk" and p.get("owns_sdk_query") is True:
        route, step = "own_sdk_callback", "Return the user's choice through this query's supported canUseTool callback"
    elif kind == "background" and p.get("agent_view_peek_available") is True:
        route, step = "background_agent_view", "Use the verified background row's choice in agent-view peek"
    else:
        route, step = "original_prompt_input", "Select the settled exact label in the existing target prompt and submit"
    return dict(base, route=route, next_step=step,
                remote_control="unavailable for observed custom endpoint" if p.get("custom_base_url") is True
                               else "not established; verify requirements before use")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("inventory")
    chooser = sub.add_parser("choice")
    chooser.add_argument("--packet", required=True)
    sender = sub.add_parser("send")
    sender.add_argument("--packet", required=True)
    sender.add_argument("--execute", action="store_true")
    sender.add_argument("--journal")
    args = parser.parse_args()
    try:
        if args.command == "inventory":
            result = inventory()
        elif args.command == "choice":
            result = waiting_choice_route(json.loads(Path(args.packet).read_text()))
        else:
            packet = json.loads(Path(args.packet).read_text())
            if args.execute and not args.journal:
                raise ValueError("execute requires an explicit private journal path")
            result = execute(packet, args.journal) if args.execute else plan(packet)
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, KeyError) as e:
        print(json.dumps({"status": "refused", "reason": str(e)}))
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
