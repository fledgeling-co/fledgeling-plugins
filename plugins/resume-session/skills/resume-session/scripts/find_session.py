#!/usr/bin/env python3
"""find_session.py : Universal Multi-CLI session discovery, parsing, and takeover engine.

Pure Python 3 standard library script. Locates, inspects, and extracts 6-dimensional
takeover state across ALL major AI coding agent CLIs and workspace artifacts:
  - Claude Code (~/.claude/projects/, ~/.claude/sessions/, repo-local .claude/)
  - Antigravity / AGY (~/.gemini/antigravity-cli/brain/<uuid>/)
  - Cursor IDE (~/.cursor/chats/, ~/Library/Application Support/Cursor/User/workspaceStorage/)
  - Codex / OpenAI CLI (~/.codex/sessions/, ~/.codex/session_index.jsonl, ~/.openai/sessions/)
  - Grok / X.AI CLI (~/.grok/sessions/, ~/.xai/sessions/)
  - Generic Repo Workspaces (docs/goals/, docs/plans/, ORCHESTRATOR.md, handover_report.md)

Usage:
  python3 find_session.py --recent 5
  python3 find_session.py --name "Google Drive" --details
  python3 find_session.py --cli agy --recent 10
  python3 find_session.py --cli claude --path ~/Dev/fledgeling-plugins
  python3 find_session.py --id daaf6175 --json
  python3 find_session.py --id daaf6175 --export handover.md
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import re
import sqlite3
import sys
import urllib.parse
from typing import Any, Dict, List, Optional, Set, Tuple

# ── Home Paths & Common Roots ────────────────────────────────────────────────
USER_HOME = pathlib.Path(os.path.expanduser("~"))
CLAUDE_HOME = USER_HOME / ".claude"
CLAUDE_PROJECTS = CLAUDE_HOME / "projects"
CLAUDE_SESSIONS = CLAUDE_HOME / "sessions"

AGY_HOME = USER_HOME / ".gemini" / "antigravity-cli"
AGY_BRAIN = AGY_HOME / "brain"

CURSOR_HOME = USER_HOME / ".cursor"
CURSOR_CHATS = CURSOR_HOME / "chats"
CURSOR_WS = USER_HOME / "Library" / "Application Support" / "Cursor" / "User" / "workspaceStorage"

CODEX_HOME = USER_HOME / ".codex"
CODEX_SESSIONS = CODEX_HOME / "sessions"
CODEX_INDEX = CODEX_HOME / "session_index.jsonl"
OPENAI_HOME = USER_HOME / ".openai"
OPENAI_SESSIONS = OPENAI_HOME / "sessions"

GROK_HOME = USER_HOME / ".grok"
GROK_SESSIONS = GROK_HOME / "sessions"
XAI_HOME = USER_HOME / ".xai"
XAI_SESSIONS = XAI_HOME / "sessions"


# ── Path & Text Helpers ───────────────────────────────────────────────────────

def path_to_claude_slug(path_str: str) -> str:
    """Convert an absolute path to a Claude projects slug (e.g. /Users/foo/bar -> -Users-foo-bar)."""
    abs_path = os.path.abspath(os.path.expanduser(path_str))
    slug = abs_path.replace(os.sep, "-")
    if not slug.startswith("-"):
        slug = "-" + slug
    return slug


def clean_text_snippet(text: Optional[str], max_len: int = 140) -> str:
    """Clean newlines and truncate text snippet cleanly."""
    if not text:
        return ""
    cleaned = re.sub(r"\s+", " ", text).strip()
    if len(cleaned) > max_len:
        return cleaned[: max_len - 3] + "..."
    return cleaned


def format_timestamp(ts_val: Any, mtime: float = 0) -> str:
    """Convert timestamp string or millisecond epoch to formatted string."""
    if isinstance(ts_val, (int, float)) and ts_val > 10000000000:
        # Millisecond timestamp e.g. 1786144545694
        try:
            dt = datetime.datetime.fromtimestamp(ts_val / 1000.0)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pass
    elif isinstance(ts_val, str) and ts_val:
        try:
            clean_ts = ts_val.replace("Z", "+00:00")
            dt = datetime.datetime.fromisoformat(clean_ts)
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pass
    if mtime > 0:
        try:
            return datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pass
    return "Unknown"


def extract_env_keys_from_string(text: str, configs: Dict[str, str]) -> None:
    """Extract known configuration keys, team IDs, bundle IDs, ports, endpoints from text."""
    if not text:
        return

    # Apple Team ID
    m_team = re.search(r"(?:APPLE_TEAM_ID|DEVELOPMENT_TEAM)[=\s:]+([A-Z0-9]{10})\b", text)
    if m_team and "APPLE_TEAM_ID" not in configs:
        configs["APPLE_TEAM_ID"] = m_team.group(1)

    # Bundle Identifier
    m_bundle = re.search(r"(?:BUNDLE_ID|BUNDLE_IDENTIFIER|bundleIdentifier)[=\s:]+([a-zA-Z0-9_\-\.]{5,50})\b", text)
    if m_bundle and "BUNDLE_IDENTIFIER" not in configs:
        configs["BUNDLE_IDENTIFIER"] = m_bundle.group(1)

    # OAuth Client ID
    m_client = re.search(r"(?:CLIENT_ID|client_id|oauth_client_id)[=\s:]+([a-zA-Z0-9_\-\.]{8,60})\b", text, re.IGNORECASE)
    if m_client and "OAUTH_CLIENT_ID" not in configs:
        configs["OAUTH_CLIENT_ID"] = m_client.group(1)

    # Port
    m_port = re.search(r"\b(?:PORT|localhost:)[=\s:]+([1-9][0-9]{2,4})\b", text)
    if m_port and "PORT" not in configs:
        configs["PORT"] = m_port.group(1)

    # Database URLs / Names
    m_db = re.search(r"(?:DATABASE_URL|POSTGRES_URL)[=\s:]+([^\s\"']+)", text)
    if m_db and "DATABASE_URL" not in configs:
        configs["DATABASE_URL"] = m_db.group(1)


# ── Per-CLI Candidate Finders ─────────────────────────────────────────────────

def find_claude_candidates(target_id: Optional[str], target_path: Optional[str]) -> List[Tuple[str, pathlib.Path, float, int]]:
    """Find candidate Claude Code session files (id, path, mtime, size)."""
    results: List[Tuple[str, pathlib.Path, float, int]] = []
    if not CLAUDE_PROJECTS.exists() and not CLAUDE_SESSIONS.exists():
        return results

    target_slug = path_to_claude_slug(target_path) if target_path else None

    # 1. ~/.claude/projects/
    if CLAUDE_PROJECTS.exists():
        try:
            for pdir in CLAUDE_PROJECTS.iterdir():
                if not pdir.is_dir():
                    continue
                if target_slug and (pdir.name != target_slug and not pdir.name.startswith(target_slug + "-") and target_path not in pdir.name):
                    continue
                try:
                    for entry in pdir.iterdir():
                        if entry.is_file() and entry.suffix == ".jsonl":
                            sid = entry.stem
                            if target_id and target_id.lower() not in sid.lower():
                                continue
                            st = entry.stat()
                            results.append(("claude", entry, st.st_mtime, st.st_size))
                except Exception:
                    continue
        except Exception:
            pass

    # 2. ~/.claude/sessions/
    if CLAUDE_SESSIONS.exists():
        try:
            for entry in CLAUDE_SESSIONS.glob("*.jsonl"):
                sid = entry.stem
                if target_id and target_id.lower() not in sid.lower():
                    continue
                st = entry.stat()
                results.append(("claude", entry, st.st_mtime, st.st_size))
        except Exception:
            pass

    # 3. repo-local .claude/ if target_path given
    if target_path:
        local_claude = pathlib.Path(os.path.expanduser(target_path)) / ".claude"
        if local_claude.exists():
            try:
                for entry in local_claude.glob("**/*.jsonl"):
                    sid = entry.stem
                    if target_id and target_id.lower() not in sid.lower():
                        continue
                    st = entry.stat()
                    results.append(("claude", entry, st.st_mtime, st.st_size))
            except Exception:
                pass

    return results


def find_agy_candidates(target_id: Optional[str], target_path: Optional[str]) -> List[Tuple[str, pathlib.Path, float, int]]:
    """Find candidate Antigravity (AGY) session transcripts."""
    results: List[Tuple[str, pathlib.Path, float, int]] = []
    if not AGY_BRAIN.exists():
        return results

    try:
        for bdir in AGY_BRAIN.iterdir():
            if not bdir.is_dir():
                continue
            sid = bdir.name
            if target_id and target_id.lower() not in sid.lower():
                continue
            transcript = bdir / ".system_generated" / "logs" / "transcript.jsonl"
            if transcript.exists():
                try:
                    st = transcript.stat()
                    results.append(("agy", transcript, st.st_mtime, st.st_size))
                except Exception:
                    pass
    except Exception:
        pass

    return results


def find_cursor_candidates(target_id: Optional[str], target_path: Optional[str]) -> List[Tuple[str, pathlib.Path, float, int]]:
    """Find candidate Cursor IDE chat sessions."""
    results: List[Tuple[str, pathlib.Path, float, int]] = []
    if not CURSOR_CHATS.exists():
        return results

    try:
        for ws_dir in CURSOR_CHATS.iterdir():
            if not ws_dir.is_dir():
                continue
            for chat_dir in ws_dir.iterdir():
                if not chat_dir.is_dir():
                    continue
                sid = chat_dir.name
                if target_id and target_id.lower() not in sid.lower():
                    continue
                meta_file = chat_dir / "meta.json"
                store_file = chat_dir / "store.db"
                target_f = meta_file if meta_file.exists() else store_file
                if target_f.exists():
                    try:
                        st = target_f.stat()
                        results.append(("cursor", chat_dir, st.st_mtime, st.st_size))
                    except Exception:
                        pass
    except Exception:
        pass

    return results


def find_codex_candidates(target_id: Optional[str], target_path: Optional[str]) -> List[Tuple[str, pathlib.Path, float, int]]:
    """Find candidate Codex / OpenAI sessions."""
    results: List[Tuple[str, pathlib.Path, float, int]] = []
    
    # 1. Check ~/.codex/sessions
    if CODEX_SESSIONS.exists():
        try:
            for entry in CODEX_SESSIONS.glob("**/*.jsonl"):
                sid = entry.stem
                if target_id and target_id.lower() not in sid.lower():
                    continue
                try:
                    st = entry.stat()
                    results.append(("codex", entry, st.st_mtime, st.st_size))
                except Exception:
                    pass
        except Exception:
            pass

    # 2. Check ~/.openai/sessions
    if OPENAI_SESSIONS.exists():
        try:
            for entry in OPENAI_SESSIONS.glob("**/*.jsonl"):
                sid = entry.stem
                if target_id and target_id.lower() not in sid.lower():
                    continue
                try:
                    st = entry.stat()
                    results.append(("codex", entry, st.st_mtime, st.st_size))
                except Exception:
                    pass
        except Exception:
            pass

    return results


def find_grok_candidates(target_id: Optional[str], target_path: Optional[str]) -> List[Tuple[str, pathlib.Path, float, int]]:
    """Find candidate Grok / X.AI sessions."""
    results: List[Tuple[str, pathlib.Path, float, int]] = []
    
    # 1. ~/.grok/sessions/
    if GROK_SESSIONS.exists():
        try:
            for ws_dir in GROK_SESSIONS.iterdir():
                if not ws_dir.is_dir():
                    continue
                for session_dir in ws_dir.iterdir():
                    if not session_dir.is_dir():
                        continue
                    sid = session_dir.name
                    if target_id and target_id.lower() not in sid.lower():
                        continue
                    chat_history = session_dir / "chat_history.jsonl"
                    summary_f = session_dir / "summary.json"
                    target_f = chat_history if chat_history.exists() else summary_f
                    if target_f.exists():
                        try:
                            st = target_f.stat()
                            results.append(("grok", session_dir, st.st_mtime, st.st_size))
                        except Exception:
                            pass
        except Exception:
            pass

    # 2. ~/.xai/sessions/
    if XAI_SESSIONS.exists():
        try:
            for ws_dir in XAI_SESSIONS.iterdir():
                if not ws_dir.is_dir():
                    continue
                for session_dir in ws_dir.iterdir():
                    if not session_dir.is_dir():
                        continue
                    sid = session_dir.name
                    if target_id and target_id.lower() not in sid.lower():
                        continue
                    chat_history = session_dir / "chat_history.jsonl"
                    if chat_history.exists():
                        try:
                            st = chat_history.stat()
                            results.append(("grok", session_dir, st.st_mtime, st.st_size))
                        except Exception:
                            pass
        except Exception:
            pass

    return results


def find_repo_candidates(target_path: Optional[str]) -> List[Tuple[str, pathlib.Path, float, int]]:
    """Find workspace handover artifacts in current or target repository."""
    results: List[Tuple[str, pathlib.Path, float, int]] = []
    root = pathlib.Path(os.path.expanduser(target_path)) if target_path else pathlib.Path.cwd()
    if not root.exists():
        return results

    patterns = [
        "docs/goals/goal-*.md",
        "docs/plans/plan-*.md",
        "docs/specs/spec-*.md",
        "ORCHESTRATOR.md",
        "LEDGER.md",
        "handover_report.md",
        "HANDOVER.md",
    ]

    for pat in patterns:
        for match in root.glob(pat):
            try:
                st = match.stat()
                results.append(("repo", match, st.st_mtime, st.st_size))
            except Exception:
                pass

    return results


# ── Per-CLI Session Parsers ───────────────────────────────────────────────────

def create_empty_session_record(cli_type: str, session_id: str, file_path: str, mtime: float, size: int) -> Dict[str, Any]:
    """Create initial baseline schema dictionary for a session."""
    return {
        "session_id": session_id,
        "cli_type": cli_type,
        "file_path": file_path,
        "file_size": size,
        "mtime": mtime,
        "custom_name": None,
        "title": None,
        "cwd": None,
        "git_branch": None,
        "models": [],
        "first_prompt": None,
        "last_prompts": [],
        "last_assistant": None,
        "last_error": None,
        "turn_count": 0,
        "timestamps": [],
        "files_written": [],
        "files_read": [],
        "commands": [],
        "goal_refs": [],
        "plan_refs": [],
        "spec_refs": [],
        "env_configs": {},
        "decisions": [],
        "next_steps": [],
    }


def parse_claude_session(filepath: pathlib.Path, quick_scan: bool = True) -> Dict[str, Any]:
    """Parse Claude Code session JSONL file."""
    st = filepath.stat() if filepath.exists() else None
    meta = create_empty_session_record("claude", filepath.stem, str(filepath), st.st_mtime if st else 0, st.st_size if st else 0)
    
    models_set = set()
    files_written_set = set()
    files_read_set = set()
    goal_set = set()
    plan_set = set()
    spec_set = set()

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line_idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue

                t = d.get("type")

                if "aiTitle" in d and d["aiTitle"]:
                    title = d["aiTitle"].strip()
                    if not meta["title"]:
                        meta["title"] = title

                if "timestamp" in d and d["timestamp"]:
                    meta["timestamps"].append(d["timestamp"])

                if "cwd" in d and d["cwd"] and not meta["cwd"]:
                    meta["cwd"] = d["cwd"]

                if "gitBranch" in d and d["gitBranch"] and not meta["git_branch"]:
                    meta["git_branch"] = d["gitBranch"]

                # User Messages
                if t == "user" and isinstance(d.get("message"), dict):
                    content = d["message"].get("content")
                    if isinstance(content, str):
                        meta["turn_count"] += 1
                        if "The user named this session" in content:
                            m = re.search(r'The user named this session\s+["“]([^"”]+)["”]', content)
                            if m:
                                meta["custom_name"] = m.group(1).strip()

                        if not meta["first_prompt"] and not content.startswith("<system-reminder>"):
                            meta["first_prompt"] = content.strip()

                        if not content.startswith("<system-reminder>"):
                            meta["last_prompts"].append(content.strip())
                            if len(meta["last_prompts"]) > 4:
                                meta["last_prompts"].pop(0)

                        extract_env_keys_from_string(content, meta["env_configs"])

                # Assistant Messages
                elif t == "assistant" and isinstance(d.get("message"), dict):
                    msg = d["message"]
                    if "model" in msg and msg["model"]:
                        models_set.add(msg["model"])

                    content = msg.get("content")
                    if isinstance(content, list):
                        for item in content:
                            if not isinstance(item, dict):
                                continue
                            item_type = item.get("type")
                            if item_type == "text":
                                txt = item.get("text", "")
                                meta["last_assistant"] = txt
                                if "API Error:" in txt or ("error" in txt.lower() and ("503" in txt or "429" in txt or "over_reserve" in txt)):
                                    meta["last_error"] = txt.strip()
                                for dec_match in re.finditer(r"(?:REJECTED|CHOSEN|DECISION|CONSTRAINT|NOTE):\s*([^\n\.]+)", txt, re.IGNORECASE):
                                    dec_str = dec_match.group(0).strip()
                                    if dec_str not in meta["decisions"] and len(meta["decisions"]) < 10:
                                        meta["decisions"].append(dec_str)

                            elif item_type == "tool_use":
                                tool_name = item.get("name")
                                inp = item.get("input", {})
                                if not isinstance(inp, dict):
                                    continue

                                if tool_name in ("Write", "Edit", "create_or_update_file", "write_to_file", "replace_file_content"):
                                    fp = inp.get("file_path") or inp.get("path") or inp.get("TargetFile")
                                    if fp:
                                        files_written_set.add(fp)
                                        if "goal-" in fp: goal_set.add(fp)
                                        elif "plan-" in fp: plan_set.add(fp)
                                        elif "spec-" in fp: spec_set.add(fp)

                                elif tool_name in ("Read", "view_file", "get_file_contents"):
                                    fp = inp.get("file_path") or inp.get("path") or inp.get("AbsolutePath")
                                    if fp:
                                        files_read_set.add(fp)
                                        if "goal-" in fp: goal_set.add(fp)
                                        elif "plan-" in fp: plan_set.add(fp)
                                        elif "spec-" in fp: spec_set.add(fp)

                                elif tool_name in ("Bash", "run_command"):
                                    cmd = inp.get("command") or inp.get("CommandLine")
                                    if cmd:
                                        meta["commands"].append(cmd)
                                        extract_env_keys_from_string(cmd, meta["env_configs"])

                elif t == "custom-title" and "customTitle" in d:
                    meta["custom_name"] = d["customTitle"]

                if quick_scan and line_idx > 300 and meta["custom_name"] and meta["first_prompt"] and meta["cwd"]:
                    break
    except Exception:
        pass

    meta["models"] = sorted(list(models_set))
    meta["files_written"] = sorted(list(files_written_set))
    meta["files_read"] = sorted(list(files_read_set))
    meta["goal_refs"] = sorted(list(goal_set))
    meta["plan_refs"] = sorted(list(plan_set))
    meta["spec_refs"] = sorted(list(spec_set))

    return meta


def parse_agy_session(filepath: pathlib.Path, quick_scan: bool = True) -> Dict[str, Any]:
    """Parse Google Antigravity (AGY) transcript.jsonl session."""
    st = filepath.stat() if filepath.exists() else None
    # filepath is ~/.gemini/antigravity-cli/brain/<uuid>/.system_generated/logs/transcript.jsonl
    session_id = filepath.parents[2].name
    meta = create_empty_session_record("agy", session_id, str(filepath), st.st_mtime if st else 0, st.st_size if st else 0)

    files_written_set = set()
    files_read_set = set()
    goal_set = set()
    plan_set = set()
    spec_set = set()

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line_idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue

                stype = d.get("type")
                source = d.get("source")
                content = d.get("content")
                created_at = d.get("created_at")

                if created_at:
                    meta["timestamps"].append(created_at)

                # Extract conversation summary title if present in CONVERSATION_HISTORY
                if stype == "CONVERSATION_HISTORY" and isinstance(content, str):
                    m_conv = re.search(r"## Conversation [a-f0-9\-]+:\s*([^\n]+)", content)
                    if m_conv and not meta["title"]:
                        meta["title"] = m_conv.group(1).strip()

                # User Inputs
                if stype == "USER_INPUT" and isinstance(content, str):
                    meta["turn_count"] += 1
                    # Extract prompt text
                    prompt_text = content
                    if "<USER_REQUEST>" in content:
                        m_req = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", content, re.DOTALL)
                        if m_req:
                            prompt_text = m_req.group(1).strip()
                    elif content.startswith("USER_OBJECTIVE:") or "# USER Objective:" in content:
                        m_obj = re.search(r"# USER Objective:\s*([^\n]+)", content)
                        if m_obj and not meta["title"]:
                            meta["title"] = m_obj.group(1).strip()

                    if not meta["first_prompt"]:
                        meta["first_prompt"] = prompt_text

                    meta["last_prompts"].append(prompt_text)
                    if len(meta["last_prompts"]) > 4:
                        meta["last_prompts"].pop(0)

                    extract_env_keys_from_string(content, meta["env_configs"])

                # Planner Responses & Model Actions
                elif stype == "PLANNER_RESPONSE":
                    if isinstance(content, str):
                        meta["last_assistant"] = content
                    tool_calls = d.get("tool_calls", [])
                    if isinstance(tool_calls, list):
                        for tc in tool_calls:
                            if not isinstance(tc, dict):
                                continue
                            tname = tc.get("name")
                            args = tc.get("args", {})
                            if isinstance(args, str):
                                try:
                                    args = json.loads(args)
                                except Exception:
                                    args = {}

                            if tname in ("write_to_file", "replace_file_content"):
                                target_f = args.get("TargetFile") or args.get("target_file") or args.get("path")
                                if target_f:
                                    target_f = target_f.strip("\"'")
                                    files_written_set.add(target_f)
                                    if "goal-" in target_f: goal_set.add(target_f)
                                    elif "plan-" in target_f: plan_set.add(target_f)
                                    elif "spec-" in target_f: spec_set.add(target_f)

                            elif tname in ("view_file", "read_resource"):
                                target_f = args.get("AbsolutePath") or args.get("path")
                                if target_f:
                                    target_f = target_f.strip("\"'")
                                    files_read_set.add(target_f)
                                    if "goal-" in target_f: goal_set.add(target_f)
                                    elif "plan-" in target_f: plan_set.add(target_f)
                                    elif "spec-" in target_f: spec_set.add(target_f)

                            elif tname == "run_command":
                                cmd = args.get("CommandLine") or args.get("command")
                                cwd = args.get("Cwd")
                                if cwd and not meta["cwd"]:
                                    meta["cwd"] = cwd.strip("\"'")
                                if cmd:
                                    meta["commands"].append(cmd)
                                    extract_env_keys_from_string(cmd, meta["env_configs"])

                elif stype == "RUN_COMMAND":
                    if d.get("exit_code", 0) != 0 and content:
                        meta["last_error"] = str(content)[:300]

                if quick_scan and line_idx > 250 and meta["first_prompt"] and (meta["title"] or meta["cwd"]):
                    break
    except Exception:
        pass

    # If title not found, use first line of first prompt
    if not meta["title"] and meta["first_prompt"]:
        first_line = meta["first_prompt"].split("\n")[0].strip()
        meta["title"] = first_line[:60]

    meta["models"] = ["Antigravity / AGY"]
    meta["files_written"] = sorted(list(files_written_set))
    meta["files_read"] = sorted(list(files_read_set))
    meta["goal_refs"] = sorted(list(goal_set))
    meta["plan_refs"] = sorted(list(plan_set))
    meta["spec_refs"] = sorted(list(spec_set))

    return meta


def parse_cursor_session(chat_dir: pathlib.Path, quick_scan: bool = True) -> Dict[str, Any]:
    """Parse Cursor IDE chat session directory."""
    session_id = chat_dir.name
    meta_file = chat_dir / "meta.json"
    store_file = chat_dir / "store.db"

    st = meta_file.stat() if meta_file.exists() else (store_file.stat() if store_file.exists() else None)
    meta = create_empty_session_record("cursor", session_id, str(chat_dir), st.st_mtime if st else 0, st.st_size if st else 0)

    # 1. Read meta.json
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8", errors="replace") as f:
                data = json.load(f)
                meta["cwd"] = data.get("cwd")
                if "createdAtMs" in data:
                    meta["timestamps"].append(data["createdAtMs"])
                if "updatedAtMs" in data:
                    meta["timestamps"].append(data["updatedAtMs"])
                if "name" in data and data["name"]:
                    meta["title"] = data["name"]
        except Exception:
            pass

    # 2. Read messages from store.db (SQLite)
    if store_file.exists():
        try:
            conn = sqlite3.connect(f"file:{store_file}?mode=ro", uri=True)
            cur = conn.cursor()
            cur.execute("SELECT data FROM blobs")
            for row in cur.fetchall():
                data = row[0]
                if not isinstance(data, bytes):
                    continue
                try:
                    txt = data.decode("utf-8", errors="replace")
                    if not (txt.startswith("{") and txt.endswith("}")):
                        continue
                    obj = json.loads(txt)
                    role = obj.get("role")
                    content = obj.get("content")
                    if role == "user":
                        meta["turn_count"] += 1
                        user_txt = ""
                        if isinstance(content, str):
                            user_txt = content
                        elif isinstance(content, list):
                            for item in content:
                                if isinstance(item, dict) and item.get("type") == "text":
                                    user_txt += item.get("text", "") + "\n"
                        if user_txt:
                            user_txt = user_txt.strip()
                            if "<user_query>" in user_txt:
                                m_q = re.search(r"<user_query>(.*?)</user_query>", user_txt, re.DOTALL)
                                if m_q: user_txt = m_q.group(1).strip()
                            if not meta["first_prompt"]:
                                meta["first_prompt"] = user_txt
                            meta["last_prompts"].append(user_txt)
                            if len(meta["last_prompts"]) > 4:
                                meta["last_prompts"].pop(0)
                            extract_env_keys_from_string(user_txt, meta["env_configs"])

                    elif role == "assistant":
                        if isinstance(content, str):
                            meta["last_assistant"] = content
                except Exception:
                    continue
            conn.close()
        except Exception:
            pass

    if not meta["title"] and meta["first_prompt"]:
        first_line = meta["first_prompt"].split("\n")[0].strip()
        meta["title"] = first_line[:60]

    meta["models"] = ["Cursor Agent"]
    return meta


def parse_codex_session(filepath: pathlib.Path, quick_scan: bool = True) -> Dict[str, Any]:
    """Parse Codex / OpenAI session JSONL file."""
    st = filepath.stat() if filepath.exists() else None
    session_id = filepath.stem
    if session_id.startswith("rollout-") and len(session_id) > 28:
        # e.g. rollout-2026-08-04T23-21-29-019fccef-b4ff-7d60-b920-7aadb940ee72
        session_id = session_id[28:]

    meta = create_empty_session_record("codex", session_id, str(filepath), st.st_mtime if st else 0, st.st_size if st else 0)

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line_idx, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except Exception:
                    continue

                rtype = d.get("type")
                payload = d.get("payload", {})
                ts = d.get("timestamp")
                if ts:
                    meta["timestamps"].append(ts)

                if rtype == "session_meta" and isinstance(payload, dict):
                    if payload.get("id") and not meta["session_id"]:
                        meta["session_id"] = payload.get("id")
                    if payload.get("cwd") and not meta["cwd"]:
                        meta["cwd"] = payload.get("cwd")

                elif rtype == "turn_context" and isinstance(payload, dict):
                    if payload.get("cwd") and not meta["cwd"]:
                        meta["cwd"] = payload.get("cwd")
                    if payload.get("summary") and not meta["title"]:
                        meta["title"] = payload.get("summary")
                    if payload.get("model"):
                        meta["models"].append(payload.get("model"))

                elif rtype == "response_item" and isinstance(payload, dict):
                    role = payload.get("role")
                    content = payload.get("content")
                    if role == "user":
                        meta["turn_count"] += 1
                        user_str = ""
                        if isinstance(content, list):
                            for citem in content:
                                if isinstance(citem, dict) and "text" in citem:
                                    user_str += citem["text"] + "\n"
                        elif isinstance(content, str):
                            user_str = content

                        if user_str:
                            user_str = user_str.strip()
                            if not meta["first_prompt"] and not user_str.startswith("<recommended_plugins>"):
                                meta["first_prompt"] = user_str
                            meta["last_prompts"].append(user_str)
                            if len(meta["last_prompts"]) > 4:
                                meta["last_prompts"].pop(0)
                            extract_env_keys_from_string(user_str, meta["env_configs"])

                    elif role == "assistant":
                        if isinstance(content, list):
                            for citem in content:
                                if isinstance(citem, dict) and "text" in citem:
                                    meta["last_assistant"] = citem["text"]
                        elif isinstance(content, str):
                            meta["last_assistant"] = content

                if quick_scan and line_idx > 250 and meta["first_prompt"] and meta["cwd"]:
                    break
    except Exception:
        pass

    if not meta["title"] and meta["first_prompt"]:
        meta["title"] = meta["first_prompt"].split("\n")[0][:60].strip()

    meta["models"] = sorted(list(set(meta["models"]))) if meta["models"] else ["Codex / OpenAI"]
    return meta


def parse_grok_session(session_dir: pathlib.Path, quick_scan: bool = True) -> Dict[str, Any]:
    """Parse Grok / X.AI session directory."""
    session_id = session_dir.name
    summary_file = session_dir / "summary.json"
    chat_file = session_dir / "chat_history.jsonl"

    st = chat_file.stat() if chat_file.exists() else (summary_file.stat() if summary_file.exists() else None)
    meta = create_empty_session_record("grok", session_id, str(session_dir), st.st_mtime if st else 0, st.st_size if st else 0)

    # 1. Read summary.json if present
    if summary_file.exists():
        try:
            with open(summary_file, "r", encoding="utf-8", errors="replace") as f:
                sdata = json.load(f)
                info = sdata.get("info", {})
                if isinstance(info, dict):
                    meta["cwd"] = info.get("cwd")
                    if info.get("id"): meta["session_id"] = info.get("id")
                if sdata.get("session_summary"):
                    meta["title"] = sdata.get("session_summary")
        except Exception:
            pass

    # 2. Read chat_history.jsonl
    if chat_file.exists():
        try:
            with open(chat_file, "r", encoding="utf-8", errors="replace") as f:
                for line_idx, line in enumerate(f):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                    except Exception:
                        continue

                    stype = d.get("type")
                    content = d.get("content")

                    if stype == "user":
                        meta["turn_count"] += 1
                        user_str = ""
                        if isinstance(content, list):
                            for c in content:
                                if isinstance(c, dict) and "text" in c:
                                    user_str += c["text"] + "\n"
                        elif isinstance(content, str):
                            user_str = content

                        if user_str:
                            user_str = user_str.strip()
                            if not meta["first_prompt"]:
                                meta["first_prompt"] = user_str
                            meta["last_prompts"].append(user_str)
                            if len(meta["last_prompts"]) > 4:
                                meta["last_prompts"].pop(0)
                            extract_env_keys_from_string(user_str, meta["env_configs"])

                    elif stype == "assistant":
                        if isinstance(content, str):
                            meta["last_assistant"] = content

                    if quick_scan and line_idx > 250 and meta["first_prompt"] and meta["cwd"]:
                        break
        except Exception:
            pass

    if not meta["title"] and meta["first_prompt"]:
        meta["title"] = meta["first_prompt"].split("\n")[0][:60].strip()

    meta["models"] = ["Grok / X.AI"]
    return meta


def parse_repo_session(filepath: pathlib.Path) -> Dict[str, Any]:
    """Parse repository workspace artifact (goal, plan, orchestrator, handover)."""
    st = filepath.stat() if filepath.exists() else None
    session_id = filepath.stem
    meta = create_empty_session_record("repo", session_id, str(filepath), st.st_mtime if st else 0, st.st_size if st else 0)
    meta["cwd"] = str(filepath.parent.resolve())
    meta["title"] = f"Workspace Artifact: {filepath.name}"

    try:
        content = filepath.read_text(encoding="utf-8", errors="replace")
        lines = content.splitlines()
        first_lines = [l for l in lines if l.strip() and not l.startswith("#")]
        if first_lines:
            meta["first_prompt"] = first_lines[0].strip()

        # Check for error or status blocks
        if "## Gaps" in content or "## Status" in content:
            meta["last_assistant"] = content[:600]

        extract_env_keys_from_string(content, meta["env_configs"])
        if "goal-" in filepath.name: meta["goal_refs"].append(str(filepath))
        elif "plan-" in filepath.name: meta["plan_refs"].append(str(filepath))
        elif "spec-" in filepath.name: meta["spec_refs"].append(str(filepath))
    except Exception:
        pass

    return meta


# ── Universal Matcher & Session Loader ────────────────────────────────────────

def matches_query(meta: Dict[str, Any], query: str) -> bool:
    """Check if session matches query string across names, titles, prompts, goals, paths."""
    q = query.lower().strip()
    if not q:
        return True

    # 1. Match session ID or CLI type
    if q in meta.get("session_id", "").lower():
        return True
    if q == meta.get("cli_type", "").lower():
        return True

    # 2. Match custom name or title
    if meta.get("custom_name") and q in meta["custom_name"].lower():
        return True
    if meta.get("title") and q in meta["title"].lower():
        return True

    # 3. Match initial prompt
    if meta.get("first_prompt") and q in meta["first_prompt"].lower():
        return True

    # 4. Match goal or plan references
    for g in meta.get("goal_refs", []) + meta.get("plan_refs", []) + meta.get("spec_refs", []):
        if q in g.lower():
            return True

    # 5. Match project path or cwd
    if meta.get("cwd") and q in meta["cwd"].lower():
        return True
    if q in meta.get("file_path", "").lower():
        return True

    return False


def load_session_details(cli_type: str, fpath: pathlib.Path, quick_scan: bool = False) -> Dict[str, Any]:
    """Route session loading to appropriate parser."""
    if cli_type == "claude":
        return parse_claude_session(fpath, quick_scan=quick_scan)
    elif cli_type == "agy":
        return parse_agy_session(fpath, quick_scan=quick_scan)
    elif cli_type == "cursor":
        return parse_cursor_session(fpath, quick_scan=quick_scan)
    elif cli_type == "codex":
        return parse_codex_session(fpath, quick_scan=quick_scan)
    elif cli_type == "grok":
        return parse_grok_session(fpath, quick_scan=quick_scan)
    elif cli_type == "repo":
        return parse_repo_session(fpath)
    return create_empty_session_record(cli_type, fpath.stem, str(fpath), 0, 0)


# ── Formatters & Handover Briefing Generator ─────────────────────────────────

def format_session_summary(meta: Dict[str, Any], index: int = 1) -> str:
    """Format compact terminal summary of a session."""
    cli = meta.get("cli_type", "agent").upper()
    name = meta.get("custom_name") or meta.get("title") or "Untitled Session"
    sid = meta.get("session_id", "unknown")
    cwd = meta.get("cwd") or "Unknown working directory"
    branch = meta.get("git_branch")
    cwd_str = f"{cwd} ({branch})" if branch else cwd
    turns = meta.get("turn_count", 0)
    size_kb = meta.get("file_size", 0) / 1024
    mtime_str = format_timestamp(meta.get("timestamps")[-1] if meta.get("timestamps") else None, meta.get("mtime", 0))
    models = ", ".join(meta.get("models", [])) or cli

    lines = [
        f"[{index}] [{cli}] {name}",
        f"    Session ID:  {sid}",
        f"    Working Dir: {cwd_str}",
        f"    Last Active: {mtime_str} | {turns} turns | {size_kb:.1f} KB | {models}",
        f"    Path:        {meta.get('file_path')}",
    ]

    if meta.get("first_prompt"):
        snippet = clean_text_snippet(meta["first_prompt"], 120)
        lines.append(f"    Prompt:      \"{snippet}\"")

    if meta.get("last_error"):
        err_snippet = clean_text_snippet(meta["last_error"], 100)
        lines.append(f"    Status:      HALTED on error: {err_snippet}")

    return "\n".join(lines)


def generate_handover_report(meta: Dict[str, Any]) -> str:
    """Generate comprehensive Markdown takeover briefing for agent continuity."""
    cli = meta.get("cli_type", "agent").upper()
    name = meta.get("custom_name") or meta.get("title") or f"{cli} Session"
    sid = meta.get("session_id", "unknown")
    cwd = meta.get("cwd") or "Unknown"
    branch = meta.get("git_branch") or "main"
    models = ", ".join(meta.get("models", [])) or cli
    last_active = format_timestamp(meta.get("timestamps")[-1] if meta.get("timestamps") else None, meta.get("mtime", 0))

    report = [
        f"# Takeover Briefing: {name}",
        f"",
        f"**CLI Platform:** `{cli}`  ",
        f"**Source Session ID:** `{sid}`  ",
        f"**Working Directory:** `{cwd}`  ",
        f"**Git Branch:** `{branch}`  ",
        f"**Models Used:** `{models}`  ",
        f"**Last Recorded Active:** `{last_active}`  ",
        f"**Transcript / State Path:** `{meta.get('file_path')}`  ",
        f"",
        f"---",
        f"",
        f"## 1. Initial Goal & User Intent",
        f"",
        f"> {meta.get('first_prompt', 'No initial prompt extracted.')}",
        f"",
    ]

    # Goal & Spec References
    all_refs = meta.get("goal_refs", []) + meta.get("plan_refs", []) + meta.get("spec_refs", [])
    if all_refs:
        report.append("## 2. Key Documentation & Artifact References")
        for g in meta.get("goal_refs", []):
            report.append(f"- **Goal Doc:** `{g}`")
        for p in meta.get("plan_refs", []):
            report.append(f"- **Plan Doc:** `{p}`")
        for s in meta.get("spec_refs", []):
            report.append(f"- **Spec Doc:** `{s}`")
        report.append("")

    # Completed Work & Modified Files
    report.append("## 3. Work Completed & Modified Files")
    if meta.get("files_written"):
        report.append(f"The session modified or created **{len(meta['files_written'])} files**:")
        for fw in meta["files_written"][:25]:
            report.append(f"- `{fw}`")
        if len(meta["files_written"]) > 25:
            report.append(f"- *...and {len(meta['files_written']) - 25} additional files.*")
    else:
        report.append("No file modifications recorded in transcript.")
    report.append("")

    # Environment & Discovered Keys
    if meta.get("env_configs") or meta.get("decisions"):
        report.append("## 4. Technical Environment & Decisions")
        for k, v in meta.get("env_configs", {}).items():
            report.append(f"- **Config `{k}`:** `{v}`")
        for dec in meta.get("decisions", []):
            report.append(f"- {dec}")
        report.append("")

    # Terminal State
    report.append("## 5. Terminal State & Last Context")
    if meta.get("last_error"):
        report.append(f"> [!WARNING]")
        report.append(f"> **Session Halted on Error:**")
        report.append(f"> `{meta['last_error']}`")
        report.append("")

    if meta.get("last_prompts"):
        report.append("**Recent User Prompts:**")
        for p in meta["last_prompts"][-2:]:
            clean_p = clean_text_snippet(p, 200)
            report.append(f"- \"{clean_p}\"")
        report.append("")

    if meta.get("last_assistant"):
        report.append("**Last Assistant Output:**")
        ast_snippet = clean_text_snippet(meta["last_assistant"], 500)
        report.append(f"```text\n{ast_snippet}\n```")
        report.append("")

    # Actionable Immediate Next Steps
    report.append("## 6. Immediate Next Steps for Takeover Agent")
    report.append(f"1. **Verify Workspace State:** Run `git status` and `git diff` in `{cwd}` to confirm what is committed vs uncommitted.")
    if meta.get("plan_refs"):
        report.append(f"2. **Inspect Plan:** Read `{meta['plan_refs'][0]}` to verify which task items were completed vs remaining.")
    elif meta.get("goal_refs"):
        report.append(f"2. **Inspect Goal:** Read `{meta['goal_refs'][0]}` to check the current objective ledger.")
    else:
        report.append("2. **Inspect Uncommitted Diff:** Review recent file edits and run tests / typechecks to establish baseline.")
    report.append("3. **Resume Execution:** Pick up the unfinished task directly without redundant re-discovery.")
    report.append("")

    return "\n".join(report)


# ── Main Entrypoint ──────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Universal Multi-CLI session discovery, parsing, and takeover engine.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--name", "-n", type=str, help="Search by session title, custom name, or topic keyword")
    parser.add_argument("--id", "-i", type=str, help="Search by session UUID or UUID prefix")
    parser.add_argument("--cli", "-c", type=str, choices=["all", "claude", "agy", "cursor", "codex", "grok", "repo"], default="all", help="Filter by CLI engine (default: all)")
    parser.add_argument("--path", "-p", "--cwd", type=str, dest="path", help="Filter by project directory or folder name")
    parser.add_argument("--recent", "-r", nargs="?", const=10, type=int, help="Show N most recent sessions (default 10)")
    parser.add_argument("--details", "-d", action="store_true", help="Print detailed 6D takeover briefing for matched session")
    parser.add_argument("--json", "-j", action="store_true", help="Output results as structured JSON")
    parser.add_argument("--export", "-e", type=str, help="Export takeover briefing Markdown report to target file path")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Maximum results to return (default 10)")
    parser.add_argument("--deep", action="store_true", help="Deep scan: fully parse transcripts rather than fast header scan")

    args = parser.parse_args()

    target_id = args.id.strip() if args.id else None
    target_name = args.name.strip() if args.name else None
    target_path = args.path.strip() if args.path else None
    cli_filter = args.cli.lower()
    recent_count = args.recent if args.recent is not None else (10 if not (target_id or target_name or target_path) else None)

    # 1. Gather raw candidates from target CLIs
    raw_candidates: List[Tuple[str, pathlib.Path, float, int]] = []

    if cli_filter in ("all", "claude"):
        raw_candidates.extend(find_claude_candidates(target_id, target_path))
    if cli_filter in ("all", "agy"):
        raw_candidates.extend(find_agy_candidates(target_id, target_path))
    if cli_filter in ("all", "cursor"):
        raw_candidates.extend(find_cursor_candidates(target_id, target_path))
    if cli_filter in ("all", "codex"):
        raw_candidates.extend(find_codex_candidates(target_id, target_path))
    if cli_filter in ("all", "grok"):
        raw_candidates.extend(find_grok_candidates(target_id, target_path))
    if cli_filter in ("all", "repo") and target_path:
        raw_candidates.extend(find_repo_candidates(target_path))

    # Sort all candidates by mtime descending
    raw_candidates.sort(key=lambda x: x[2], reverse=True)

    if not raw_candidates:
        if args.json:
            print(json.dumps({"error": "No matching sessions found", "results": []}, indent=2))
        else:
            print(f"No sessions found matching criteria (cli={cli_filter}).")
        return 1

    # 2. Parse candidates and filter
    matches: List[Dict[str, Any]] = []
    need_full_parse = args.details or bool(args.export) or args.deep or (target_id is not None)

    # Scan up to 500 candidates
    scan_limit = max(recent_count * 4 if recent_count else 50, 200)
    for cli_type, fpath, mtime, size in raw_candidates[:scan_limit]:
        meta = load_session_details(cli_type, fpath, quick_scan=not need_full_parse)
        if target_name:
            if not matches_query(meta, target_name):
                continue
        elif target_id:
            if target_id.lower() not in meta["session_id"].lower():
                continue

        matches.append(meta)
        if len(matches) >= (recent_count or args.limit):
            break

    if not matches:
        if args.json:
            print(json.dumps({"error": "No sessions matched search query", "results": []}, indent=2))
        else:
            print(f"No sessions matched query '{target_name or target_id}'.")
        return 1

    # If details or export requested on top match, ensure full parse
    if (args.details or args.export) and matches:
        top = matches[0]
        matches[0] = load_session_details(top["cli_type"], pathlib.Path(top["file_path"]), quick_scan=False)

    # Export if requested
    if args.export and matches:
        report_content = generate_handover_report(matches[0])
        out_p = pathlib.Path(os.path.expanduser(args.export))
        out_p.parent.mkdir(parents=True, exist_ok=True)
        out_p.write_text(report_content, encoding="utf-8")
        if not args.json:
            print(f"Exported takeover briefing to: {out_p.resolve()}\n")

    # Output formatting
    if args.json:
        out_obj = {
            "total_matches": len(matches),
            "results": matches,
        }
        print(json.dumps(out_obj, indent=2))
    elif args.details and matches:
        print(generate_handover_report(matches[0]))
    else:
        print(f"Found {len(matches)} session(s):\n")
        for idx, m in enumerate(matches, 1):
            print(format_session_summary(m, idx))
            print()

    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        try:
            devnull = os.open(os.devnull, os.O_WRONLY)
            os.dup2(devnull, sys.stdout.fileno())
        except Exception:
            pass
        sys.exit(0)
    except KeyboardInterrupt:
        sys.exit(130)
