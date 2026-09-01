#!/usr/bin/env python3
"""Deterministic signals over a finished agent session's transcript.

A session's transcript is the only place that records what the model *did* as
distinct from what it *said*. Every probe here pairs one against the other and
emits a citable location, so a later reader can check the claim rather than take
it.

Nothing here decides anything. It produces a ranked worklist telling an expensive
reader where to point, which is the whole economy of the pass: a frontier model
re-reading a session's work costs more than the session did.

    signals.py <session.jsonl> [--json] [--out signals.json] [--selftest]

Exit codes
    0   scan complete
    1   transcript unreadable, or not an agent session transcript
    4   one or more probes could not run — named individually, because a probe
        that could not run is not a probe that passed
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

SCHEMA = 2
GLYPH = "\U0001FAE5"

# ---------------------------------------------------------------- vocabularies

# A sentence asserting a check happened. Deliberately narrow: a claim in the
# future or conditional tense is not an assertion that something ran.
CLAIM_RE = re.compile(
    r"[^.!?\n]{0,200}?\b(?:"
    r"all (?:\d+\s+)?(?:tests?|checks?|specs?|assertions?|suites?|cases?)\s+(?:pass|passed|are passing|green)"
    r"|(?:tests?|suite|build|lint|typecheck|gate|campaign)\s+(?:passes|passed|is green|are green|succeeded)"
    r"|(?:I|we)\s+(?:ran|verified|confirmed|validated|measured)"
    r"|verified\s+(?:that|the|it|by|out|against)"
    r"|100%\s+(?:pass|passing|coverage|comparable|of)"
    r"|exit(?:ed|s)?\s+(?:code\s+)?0"
    r"|(?:no|zero)\s+(?:errors?|failures?|regressions?|violations?)"
    r"|(?:vendor|independently|out.of.family)[- ]verified"
    r")[^.!?\n]{0,200}",
    re.I,
)

CLEAN_RE = re.compile(
    r"\b(?:clean|passed|passing|green|verified|0 failures|no failures|all good|"
    r"succeeded|complete|success)\b",
    re.I,
)

DONE_RE = re.compile(
    r"\b(?:complete(?:d|ly)?|done|finished|shipped|merged|ready to (?:merge|ship)|"
    r"production[- ]ready|fully (?:implemented|working|functional)|"
    r"all (?:items?|tasks?|features?|requirements?|waves?) (?:are )?(?:complete|done|implemented|merged))\b",
    re.I,
)

# Human dissatisfaction — the only external ground truth a transcript carries.
CORRECT_RE = re.compile(
    r"(?:you (?:didn'?t|did not|failed to|haven'?t|never)"
    r"|that'?s (?:wrong|not right|incorrect)"
    r"|(?:doesn'?t|does not|isn'?t) work"
    r"|still (?:broken|failing|not)"
    r"|nothing happen"
    r"|why (?:didn'?t|aren'?t|are you not|is it not|haven'?t)"
    r"|(?:it'?s|its) (?:broken|blank|empty|missing)"
    r"|told you"
    r"|(?:lied|made (?:that|it) up|fabricat)"
    r"|(?:not|never) (?:actually|really) (?:ran|run|tested|checked)"
    r"|didn'?t (?:you|it) (?:read|run|follow|invoke)"
    r"|help me understand why)",
    re.I,
)

# Files a later session plans from. Band-1 blast radius.
DURABLE_RE = re.compile(
    r"(?:ARMADA\.md|ORCHESTRATOR\.md|LEDGER\.md|PRD\.md|ROADMAP\.md"
    r"|/(?:specs?|plans?|briefs?|features-to-triage)/[^\s\"']+\.md"
    r"|(?:cases|inventory|ledger|registry|claims)\.json)",
    re.I,
)

# Gate inputs — files a gate reads and trusts. Editing one moves the number
# without moving the thing under test.
GATE_INPUT_RE = re.compile(
    r"(?:cases|inventory|ledger|registry|claims|pairs|worklist|manifest|sources_map"
    r"|arming|ratchet|campaign|coverage)[^/\s]*\.(?:json|jsonl|ya?ml|toml)$",
    re.I,
)

TEST_OR_SRC_RE = re.compile(
    r"\.(?:ts|tsx|js|jsx|py|swift|rs|go|rb|java|kt|c|cc|cpp|h|m|mm|sh|mjs|cjs)$",
    re.I,
)

LANE_RE = re.compile(
    r"\b(?P<bin>agy|codex|grok|cursor-agent|claude|gemini|llm)\b[^|;&]*?"
    r"(?:--model|-m)[= ]+(?P<model>[A-Za-z0-9._/:-]+)"
)

FAMILY = [
    ("google", re.compile(r"gemini|agy|bard|palm", re.I)),
    ("anthropic", re.compile(r"claude|opus|sonnet|haiku|fable", re.I)),
    ("openai", re.compile(r"gpt|codex|o[1-9]\b|luna|sol", re.I)),
    ("xai", re.compile(r"grok", re.I)),
    ("deepseek", re.compile(r"deepseek", re.I)),
    ("zhipu", re.compile(r"glm", re.I)),
]

STOP_NOUNS = {
    "the", "with", "that", "this", "from", "into", "your", "their", "work", "project",
    "projects", "time", "times", "thing", "things", "other", "others", "case", "cases",
    "way", "ways", "part", "parts", "point", "points", "detail", "details", "item",
    "items", "aspect", "aspects", "respect", "respects", "effort", "efforts",
}

POLL_RE = re.compile(r"^\s*(?:ps\s+(?:aux|-p)|pgrep|tail\b|lsof|sleep\s+\d+\s*$|jobs\b)", re.I)

SPAWN_TOOLS = {"Agent", "Task", "Workflow", "SendMessage"}
TODO_TOOLS = {"TaskCreate", "TaskUpdate", "TaskList", "TodoWrite"}


def family_of(name: str) -> str:
    for fam, rx in FAMILY:
        if rx.search(name or ""):
            return fam
    return "unknown"


# ------------------------------------------------------------------- alias map

def load_script_aliases(repo: str | None) -> dict[str, str]:
    """Resolve `npm run X` / `pnpm X` / `make X` to what they actually execute.

    Without this a probe reports honest work as fabricated. Measured: three
    "All N Playwright tests passed" claims looked unsupported because no command
    contained the string `Playwright`; `pnpm e2e` had run seven times. A probe
    that cries wolf on correct behaviour is how a verification pass gets
    switched off, so this runs before any "never ran" claim is made.
    """
    aliases: dict[str, str] = {}
    if not repo or not os.path.isdir(repo):
        return aliases
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in {"node_modules", ".git", "dist", "build", ".next", "target"}]
        if root.count(os.sep) - repo.count(os.sep) > 3:
            dirs[:] = []
        if "package.json" in files:
            try:
                with open(os.path.join(root, "package.json"), errors="replace") as fh:
                    for name, body in (json.load(fh).get("scripts") or {}).items():
                        aliases.setdefault(name, body)
            except Exception:
                pass
        if "Makefile" in files:
            try:
                with open(os.path.join(root, "Makefile"), errors="replace") as fh:
                    for line in fh:
                        m = re.match(r"^([A-Za-z0-9_.-]+):(?!=)", line)
                        if m:
                            aliases.setdefault(m.group(1), m.group(1))
            except Exception:
                pass
    return aliases


def expand(cmd: str, aliases: dict[str, str], depth: int = 0) -> str:
    """One command plus everything its package-script aliases expand to."""
    if depth > 2:
        return cmd
    out = [cmd]
    for name, body in aliases.items():
        if re.search(r"(?:^|[\s;&|])(?:npm run|pnpm|yarn|make|npm)\s+%s\b" % re.escape(name), cmd):
            out.append(expand(body, aliases, depth + 1))
    return " ".join(out)


# --------------------------------------------------------------------- reading

class Session:
    """A parsed transcript. Every record keeps its source line number."""

    def __init__(self, path: str):
        self.path = path
        self.records: list[tuple[int, dict]] = []
        self.turns: list[dict] = []       # assistant text blocks
        self.tools: list[dict] = []       # tool_use, in order
        self.results: dict[str, dict] = {}  # tool_use_id -> result
        self.humans: list[dict] = []
        self.models = Counter()
        self.skills: list[dict] = []
        self.marker_injected = False
        self.sidechains = 0
        self.format = "unknown"
        self.attribution = {
            "mode": "whole-transcript",
            "agent_path": None,
            "parent_thread_id": None,
            "start_line": 1,
            "inherited_records_excluded": 0,
            "paths": [],
            "modified_paths": [],
        }
        self.call_outputs = 0
        self.output_count = 0
        self.output_ids: list[str] = []
        self.orphan_calls: list[dict] = []
        self.orphan_outputs: list[dict] = []
        self._read()

    def _read(self) -> None:
        parsed: list[tuple[int, dict]] = []
        with open(self.path, errors="replace") as fh:
            for ln, line in enumerate(fh, 1):
                if "Begin every conversational response" in line:
                    self.marker_injected = True
                try:
                    o = json.loads(line)
                except Exception:
                    continue
                parsed.append((ln, o))

        if any(o.get("type") == "response_item" for _, o in parsed):
            self._read_codex(parsed)
        else:
            self._read_claude(parsed)
        self._finish_pairing()

    @staticmethod
    def _text(value) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            return " ".join(
                x.get("text", "") for x in value
                if isinstance(x, dict) and isinstance(x.get("text"), str)
            )
        return ""

    @staticmethod
    def _codex_tool_name(payload: dict) -> str:
        name = payload.get("name") or "?"
        if payload.get("type") == "custom_tool_call" and name == "exec":
            return "Bash"
        if name in {"spawn_agent", "followup_task", "send_message"}:
            return "Agent" if name == "spawn_agent" else "SendMessage"
        return name

    @staticmethod
    def _codex_input(payload: dict) -> tuple[dict, str]:
        raw = payload.get("input") if payload.get("type") == "custom_tool_call" \
            else payload.get("arguments")
        if isinstance(raw, dict):
            inp = raw
        elif isinstance(raw, str):
            try:
                parsed = json.loads(raw)
                inp = parsed if isinstance(parsed, dict) else {"raw": raw}
            except Exception:
                inp = {"raw": raw}
        else:
            inp = {}
        command = inp.get("cmd") or inp.get("command") or ""
        if not command and isinstance(raw, str):
            command = raw
        return inp, command

    @staticmethod
    def _paths_from_tool(inp: dict, command: str, repo: str | None) -> set[str]:
        blob = json.dumps(inp, ensure_ascii=False) + " " + (command or "")
        candidates = set(re.findall(
            r"(?:/[^\s\"'`,;:(){}\[\]]+|(?<![\w.-])(?:docs|src|tests?|apps|packages|macos|plugins)"
            r"/[^\s\"'`,;:(){}\[\]]+)", blob))
        out: set[str] = set()
        for raw in candidates:
            p = re.split(r"(?:\\\\n|\\n)", raw, maxsplit=1)[0].rstrip(".>)\\")
            if not p or p.startswith(("/tmp/", "/private/tmp/")):
                continue
            if repo and os.path.isabs(p):
                try:
                    rel = os.path.relpath(p, repo)
                except ValueError:
                    continue
                if rel == "." or rel.startswith("../"):
                    continue
                p = rel
            elif os.path.isabs(p):
                continue
            p = p.lstrip("./")
            if p and not p.startswith(".git/"):
                out.add(p)
        return out

    @classmethod
    def _modified_paths_from_tool(cls, inp: dict, command: str, repo: str | None) -> set[str]:
        blob = json.dumps(inp, ensure_ascii=False) + " " + (command or "")
        fragments: list[str] = []
        fragments.extend(re.findall(r"\*\*\* (?:Update|Add|Delete) File:\s*([^\r\n*]+)", blob))
        fragments.extend(re.findall(r"(?:^|[;&|]\s*)(?:cp|mv|touch|mkdir|tee|screencapture)\b[^;&|]*?"
                                    r"((?:/|(?:docs|src|tests?|apps|packages|macos|plugins)/)[^\s;&|]+)",
                                    blob, re.M))
        fragments.extend(re.findall(r">{1,2}\s*((?:/|(?:docs|src|tests?|apps|packages|macos|plugins)/)"
                                    r"[^\s;&|]+)", blob))
        if any(k in inp for k in ("file_path", "path")) and re.search(
                r"(?:apply_patch|\b(?:Edit|Write|NotebookEdit|MultiEdit)\b)", blob):
            fragments.append(str(inp.get("file_path") or inp.get("path") or ""))
        return cls._paths_from_tool({"paths": fragments}, "", repo)

    def _read_codex(self, parsed: list[tuple[int, dict]]) -> None:
        self.format = "codex-response-item"
        metas = [(ln, o.get("payload") or {}) for ln, o in parsed if o.get("type") == "session_meta"]
        own = next((m for _, m in metas if m.get("thread_source") == "subagent"),
                   metas[0][1] if metas else {})
        agent_path = own.get("agent_path")
        start_line = 1
        boundary_found = not agent_path
        if agent_path:
            for ln, o in parsed:
                q = o.get("payload") or {}
                if (o.get("type") == "response_item" and q.get("type") == "agent_message"
                        and q.get("recipient") == agent_path):
                    start_line = ln
                    boundary_found = True
                    break
        model = next(((o.get("payload") or {}).get("model") for _, o in parsed
                      if o.get("type") == "turn_context" and (o.get("payload") or {}).get("model")), "")
        repo = own.get("cwd")
        self.attribution.update({
            "mode": "subagent-owned-segment" if agent_path else "whole-transcript",
            "agent_path": agent_path,
            "parent_thread_id": own.get("parent_thread_id"),
            "start_line": start_line,
            "inherited_records_excluded": sum(1 for ln, _ in parsed if ln < start_line),
            "error": None if boundary_found else
            f"no agent_message addressed to declared agent_path {agent_path}",
        })
        paths: set[str] = set()
        modified_paths: set[str] = set()
        call_ordinal = 0
        for ln, o in parsed:
            if ln < start_line:
                continue
            q = o.get("payload") or {}
            if o.get("type") != "response_item":
                continue
            self.records.append((ln, o))
            typ = q.get("type")
            if typ == "message" and q.get("role") == "assistant":
                text = self._text(q.get("content")).strip()
                if text:
                    self.turns.append({"line": ln, "text": text, "model": model})
                    if model:
                        self.models[model] += 1
            elif typ == "message" and q.get("role") == "user":
                text = self._text(q.get("content")).strip()
                if text:
                    self.humans.append({"line": ln, "text": text})
            elif typ == "agent_message" and (not agent_path or q.get("recipient") == agent_path):
                text = self._text(q.get("content")).strip()
                if text:
                    self.humans.append({"line": ln, "text": text})
            elif typ in {"custom_tool_call", "function_call"}:
                call_ordinal += 1
                inp, command = self._codex_input(q)
                name = self._codex_tool_name(q)
                path = inp.get("file_path") or inp.get("path") or ""
                rec = {
                    "line": ln, "id": q.get("call_id") or q.get("id"), "name": name,
                    "source_name": q.get("name") or "?", "input": inp,
                    "command": command, "path": path, "model": model,
                    "ordinal": call_ordinal,
                }
                self.tools.append(rec)
                paths.update(self._paths_from_tool(inp, command, repo))
                modified_paths.update(self._modified_paths_from_tool(inp, command, repo))
                if name == "Skill":
                    self.skills.append({"line": ln, "skill": inp.get("skill", "?")})
            elif typ in {"custom_tool_call_output", "function_call_output"}:
                self.output_count += 1
                text = self._text(q.get("output"))
                call_id = q.get("call_id") or ""
                self.output_ids.append(call_id)
                self.results[call_id] = {
                    "line": ln, "text": text,
                    "is_error": bool(re.search(r"(?:Script failed|Process exited with code [1-9])", text)),
                }
        self.attribution["paths"] = sorted(paths)
        self.attribution["modified_paths"] = sorted(modified_paths)

    def _read_claude(self, parsed: list[tuple[int, dict]]) -> None:
        self.format = "claude-message"
        call_ordinal = 0
        for ln, o in parsed:
                self.records.append((ln, o))
                if o.get("isSidechain"):
                    self.sidechains += 1
                    continue
                msg = o.get("message") or {}
                content = msg.get("content")
                blocks = content if isinstance(content, list) else (
                    [{"type": "text", "text": content}] if isinstance(content, str) else []
                )
                if o.get("type") == "assistant":
                    model = msg.get("model") or ""
                    if model:
                        self.models[model] += 1
                    for b in blocks:
                        if not isinstance(b, dict):
                            continue
                        if b.get("type") == "text" and (b.get("text") or "").strip():
                            self.turns.append({"line": ln, "text": b["text"], "model": model})
                        elif b.get("type") == "tool_use":
                            call_ordinal += 1
                            inp = b.get("input") or {}
                            rec = {
                                "line": ln,
                                "id": b.get("id"),
                                "name": b.get("name") or "?",
                                "input": inp,
                                "command": inp.get("command") or "",
                                "path": inp.get("file_path") or "",
                                "model": model,
                                "ordinal": call_ordinal,
                            }
                            self.tools.append(rec)
                            if rec["name"] == "Skill":
                                self.skills.append({"line": ln, "skill": inp.get("skill", "?")})
                elif o.get("type") == "user":
                    tool_result = False
                    for b in blocks:
                        if isinstance(b, dict) and b.get("type") == "tool_result":
                            tool_result = True
                            raw = b.get("content")
                            text = raw if isinstance(raw, str) else " ".join(
                                x.get("text", "") for x in (raw or []) if isinstance(x, dict)
                            )
                            self.results[b.get("tool_use_id") or ""] = {
                                "line": ln,
                                "text": text,
                                "is_error": bool(b.get("is_error")),
                            }
                            self.output_count += 1
                            self.output_ids.append(b.get("tool_use_id") or "")
                    if not tool_result and not o.get("isMeta"):
                        text = " ".join(
                            b.get("text", "") for b in blocks
                            if isinstance(b, dict) and b.get("type") == "text"
                        ) or (content if isinstance(content, str) else "")
                        t = (text or "").strip()
                        if t and not t.startswith(("<system-reminder", "<local-command", "<command-name",
                                                   "Caveat:", "[Request interrupted", "<task-notification")):
                            self.humans.append({"line": ln, "text": t})
        self.attribution["paths"] = sorted({
            p for t in self.tools
            for p in self._paths_from_tool(t["input"], t["command"], None)
        })
        self.attribution["modified_paths"] = sorted({
            p for t in self.edits()
            for p in self._paths_from_tool(t["input"], t["command"], None)
        })

    def _finish_pairing(self) -> None:
        call_counts = Counter(t.get("id") for t in self.tools if t.get("id"))
        result_counts = Counter(self.output_ids)
        self.call_outputs = sum(1 for i, n in call_counts.items()
                                if n == 1 and result_counts.get(i) == 1)
        self.orphan_calls = [
            {"ordinal": t["ordinal"], "line": t["line"], "id": t.get("id"), "name": t["name"]}
            for t in self.tools if call_counts.get(t.get("id")) != 1
            or result_counts.get(t.get("id")) != 1
        ]
        self.orphan_outputs = [
            {"line": self.results[i]["line"], "id": i}
            for i, n in sorted(result_counts.items())
            if n != 1 or call_counts.get(i) != 1
            if i in self.results
        ]

    def result_for(self, tool: dict) -> dict:
        return self.results.get(tool.get("id") or "", {})

    def bash(self) -> list[dict]:
        return [t for t in self.tools if t["name"] == "Bash"]

    def edits(self) -> list[dict]:
        return [t for t in self.tools if t["name"] in ("Edit", "Write", "NotebookEdit", "MultiEdit")]

    def text_after(self, line: int, window: int = 6) -> list[dict]:
        return [t for t in self.turns if line < t["line"] <= line + 400][:window]


def failed(result: dict) -> bool:
    if not result:
        return False
    if result.get("is_error"):
        return True
    return bool(re.search(r"\bExit code [1-9]\d*\b", result.get("text") or ""))


def finding(pid: str, title: str, line: int, quote: str, band: int, confidence: str,
            remedy: str = "", **extra) -> dict:
    f = {
        "probe": pid,
        "title": title,
        "line": line,
        "quote": " ".join((quote or "").split())[:400],
        "band": band,
        "confidence": confidence,
        "remedy": remedy,
    }
    f.update(extra)
    return f


# ----------------------------------------------------------------- the probes
# Each probe returns a list of findings. Every one has a paired fixture in
# selftest.py: an input where it must fire, and one where it must stay silent.

def t1_overlay_unread(s: Session, ctx) -> list[dict]:
    """A skill was invoked and the model-specific overlay beside it went unread."""
    out = []
    base_by_line: dict[int, str] = {}
    for ln, o in s.records:
        if o.get("type") != "user":
            continue
        msg = (o.get("message") or {})
        c = msg.get("content")
        text = c if isinstance(c, str) else " ".join(
            b.get("text", "") for b in (c or []) if isinstance(b, dict) and b.get("type") == "text")
        m = re.search(r"Base directory for this skill:\s*(\S+)", text or "")
        if m:
            base_by_line[ln] = m.group(1)
    reads = " ".join(json.dumps(t["input"]) for t in s.tools if t["name"] in ("Read", "Bash"))
    for ln, base in base_by_line.items():
        overlay = os.path.join(base, "gemini.md")
        if not os.path.exists(overlay):
            continue
        if "gemini.md" in reads and os.path.basename(base) in reads:
            continue
        out.append(finding(
            "T1", f"overlay present and unread: {os.path.basename(base)}/gemini.md",
            ln, base, 3, "observed",
            remedy=f"read {overlay} and re-check the overrides it names"))
    return out


def t2_skill_scripts_unrun(s: Session, ctx) -> list[dict]:
    """A skill ships deterministic checks and none of them ran."""
    out = []
    allcmd = ctx["allcmd"]
    seen = set()
    for ln, o in s.records:
        if o.get("type") != "user":
            continue
        c = (o.get("message") or {}).get("content")
        text = c if isinstance(c, str) else " ".join(
            b.get("text", "") for b in (c or []) if isinstance(b, dict) and b.get("type") == "text")
        m = re.search(r"Base directory for this skill:\s*(\S+)", text or "")
        if not m:
            continue
        base = m.group(1)
        sdir = os.path.join(base, "scripts")
        if base in seen or not os.path.isdir(sdir):
            continue
        seen.add(base)
        names = [f for f in os.listdir(sdir) if f.endswith((".py", ".sh", ".mjs", ".js"))]
        if not names:
            continue
        ran = [n for n in names if n in allcmd]
        if not ran:
            out.append(finding(
                "T2", f"{os.path.basename(base)}: 0 of {len(names)} bundled scripts ran",
                ln, ", ".join(sorted(names)[:6]), 2, "observed",
                remedy=f"run the skill's own checks under {sdir}"))
    return out


def t3_red_gate_green_report(s: Session, ctx) -> list[dict]:
    """A tool failed and the next thing the model said was that things are clean."""
    out = []
    for t in s.bash():
        r = s.result_for(t)
        if not failed(r):
            continue
        for nxt in s.text_after(t["line"], window=2):
            if not CLEAN_RE.search(nxt["text"][:900]):
                continue
            head = (t["command"] or "").split()[0:4]
            if any(tok in nxt["text"] for tok in head if len(tok) > 4):
                continue  # the failure is named — that is disclosure, not a finding
            out.append(finding(
                "T3", "a failing command is followed by a clean claim that does not name it",
                nxt["line"], nxt["text"][:300], 2, "observed",
                command=" ".join((t["command"] or "").split())[:200],
                command_line=t["line"],
                remedy="name the failing command and its exit code, or re-run it"))
            break
    return out


def t4_laundering_window(s: Session, ctx) -> list[dict]:
    """A gate went red, then green, and only its own input changed in between.

    Neither a skipped gate nor a fabricated claim: the gate ran and its number is
    true of a file the run wrote to make it true. The remedy is a revert, which
    restores the gate's ability to fail.
    """
    out = []
    runs: dict[str, list[tuple[int, bool, dict]]] = defaultdict(list)
    for t in s.bash():
        key = None
        for tok in re.findall(r"[\w./-]+\.(?:py|sh|mjs|js)\b", t["command"] or ""):
            key = os.path.basename(tok)
            break
        if not key:
            continue
        runs[key].append((t["line"], failed(s.result_for(t)), t))
    for key, seq in runs.items():
        for i in range(len(seq) - 1):
            ln_red, red, _ = seq[i]
            if not red:
                continue
            for ln_green, green, _ in seq[i + 1:]:
                if green:
                    continue
                touched = [e for e in s.edits() if ln_red < e["line"] < ln_green]
                paths = [e["path"] for e in touched if e["path"]]
                reverts = [b for b in s.bash() if ln_red < b["line"] < ln_green
                           and re.search(r"git (?:checkout|restore|stash)\b", b["command"] or "")]
                if not paths and not reverts:
                    break
                gate_inputs = [p for p in paths if GATE_INPUT_RE.search(os.path.basename(p))]
                real = [p for p in paths if TEST_OR_SRC_RE.search(p)]
                if (gate_inputs or reverts) and not real:
                    out.append(finding(
                        "T4", f"{key} went red then green with only its own input edited",
                        ln_green, ", ".join(os.path.basename(p) for p in gate_inputs[:5]) or
                        " ".join((reverts[0]["command"] or "").split())[:120],
                        1, "observed",
                        red_line=ln_red,
                        edited=[os.path.basename(p) for p in gate_inputs[:8]],
                        reverted=bool(reverts),
                        remedy=f"revert the edits between {ln_red} and {ln_green}, re-run {key}"))
                break
    return out


def t5_gate_suppressed(s: Session, ctx) -> list[dict]:
    out = []
    for t in s.bash():
        cmd = t["command"] or ""
        if not re.search(r"[\w./-]+\.(?:py|sh|mjs)\b", cmd):
            continue
        if not re.search(r"\|\|\s*true|>\s*/dev/null|2>&1\s*$|\|\|\s*:", cmd):
            continue
        base = None
        for tok in re.findall(r"[\w./-]+\.(?:py|sh|mjs)\b", cmd):
            base = os.path.basename(tok)
            break
        later = [b for b in s.bash() if b["line"] > t["line"] and base and base in (b["command"] or "")
                 and not re.search(r"\|\|\s*true|>\s*/dev/null", b["command"] or "")]
        if later:
            continue
        # A fallback branch that never printed is a gate that ran and exited 0.
        # Measured: `berths.py … 2>/dev/null || echo "berths fallback"` produced
        # JSON and never the fallback string, and was reported as suppressed.
        fb = re.search(r"\|\|\s*echo\s+[\"\']([^\"\']{4,})[\"\']", cmd)
        res = (s.result_for(t).get("text") or "")
        if fb and fb.group(1) not in res and res.strip():
            continue
        out.append(finding(
            "T5", f"gate output suppressed and never re-run unsuppressed: {base}",
            t["line"], " ".join(cmd.split())[:200], 2, "observed",
            remedy=f"re-run {base} and read its exit code"))
    return out


def t6_orphan_exit_status(s: Session, ctx) -> list[dict]:
    """`echo $?` as its own call. The harness spawns a shell per call, so it
    reports the status of nothing."""
    return [finding("T6", "`echo $?` issued as a standalone call — reports nothing",
                    t["line"], t["command"], 2, "observed",
                    remedy="re-run the command and read its own exit code")
            for t in s.bash() if (t["command"] or "").strip() in ("echo $?", "echo $?;", 'echo "$?"')]


def t7_lane_family(s: Session, ctx) -> list[dict]:
    """An independence gate that resolved to the running model's own family."""
    out = []
    own = family_of(next(iter(s.models), "") if s.models else "")
    for t in s.bash():
        cmd = t["command"] or ""
        m = LANE_RE.search(cmd)
        if not m:
            continue
        lane_family = family_of(m.group("model"))
        if lane_family == "unknown" or own == "unknown":
            continue
        if lane_family != own:
            continue
        out.append(finding(
            "T7", f"reviewer lane is in-family ({lane_family}) with the running model",
            t["line"], " ".join(cmd.split())[:220], 1, "observed",
            lane_model=m.group("model"), session_model=next(iter(s.models), ""),
            remedy="re-route with lane_pick.py --task verification, excluding this family"))
    return out


def t8_lane_output_unread(s: Session, ctx) -> list[dict]:
    """A reviewer was invoked, its output redirected to a file, and nobody opened it."""
    out = []
    for t in s.bash():
        cmd = t["command"] or ""
        if not LANE_RE.search(cmd):
            continue
        m = re.search(r">\s*([\w./-]+\.(?:md|txt|json|log))", cmd)
        if not m:
            continue
        target = os.path.basename(m.group(1))
        # The readback is often in the same compound command
        # (`agy … > /tmp/x.md; cat /tmp/x.md`). Looking only at later calls
        # reported twelve honest readbacks as unread on a measured run.
        after_redirect = cmd[m.end():]
        if re.search(r"\b(?:cat|head|tail|less|bat)\b[^|;&]*" + re.escape(target), after_redirect):
            continue
        # …or the review text simply came back in this call's own result.
        own = (s.result_for(t).get("text") or "")
        if len(own.strip()) > 200:
            continue
        later = " ".join(
            (b["command"] or "") + json.dumps(b["input"])
            for b in s.tools if b["line"] > t["line"] and b["name"] in ("Bash", "Read"))
        if target in later:
            continue
        out.append(finding(
            "T8", f"reviewer output never read back: {target}",
            t["line"], " ".join(cmd.split())[:220], 1, "observed",
            remedy=f"read {m.group(1)} before citing the review"))
    return out


def t9_lane_from_recollection(s: Session, ctx) -> list[dict]:
    lanes = [t for t in s.bash() if LANE_RE.search(t["command"] or "")]
    if not lanes:
        return []
    if "lane_pick.py" in ctx["allcmd"]:
        return []
    return [finding(
        "T9", f"{len(lanes)} reviewer lane(s) chosen without lane_pick.py",
        lanes[0]["line"], " ".join((lanes[0]["command"] or "").split())[:200], 3, "observed",
        remedy="lane_pick.py --task verification --json")]


def t10_bulk_arming(s: Session, ctx) -> list[dict]:
    """Arming set by assignment rather than by watching a test fail."""
    out = []
    for t in s.tools:
        if t["name"] not in ("Edit", "Write", "MultiEdit", "Bash"):
            continue
        blob = json.dumps(t["input"])
        # The field arrives inside a JSON string, so its quotes are escaped one
        # level deeper than they look. Matching the unescaped form silently found
        # nothing — the selftest caught it; a live run would not have.
        armed = len(re.findall(r'\\?"armed\\?"\s*:\s*true', blob, re.I))
        rung = len(re.findall(r'\\?"oracle\\?"\s*:\s*\\?"', blob, re.I))
        if armed > 5 or rung > 5:
            out.append(finding(
                "T10", f"{max(armed, rung)} arming/rung fields set in one call",
                t["line"], os.path.basename(t["path"]) or t["name"], 1, "observed",
                armed=armed, rungs=rung,
                remedy="each armed case needs the mutation that made it fail, named"))
    return out


def t11_denominator_elision(s: Session, ctx) -> list[dict]:
    """A gate printed a class the report then dropped.

    Anchored hard on purpose. An earlier draft allowed any non-digit run between
    the keyword and the number, and matched `blind.\\n132` out of a `cat -n`
    listing — a line number reported as a denominator. The keyword and its figure
    must now sit on one line, separated only by horizontal space or a colon or
    equals, so a class name wrapping onto a numbered source line cannot match.
    """
    out = []
    kw = r"(?:skipped|unmeasured|unchecked|undecided|unjoined|blind|decayed|unmatched|unbacked)"
    pat = re.compile(
        rf"\b{kw}\b[ \t]*[:=]?[ \t]*(\d+)\b" rf"|\b(\d+)[ \t]+{kw}\b", re.I)
    for t in s.tools:
        r = s.result_for(t)
        text = r.get("text") or ""
        if not text:
            continue
        for line_text in text[:8000].splitlines():
            # A source listing is not a gate summary. `cat -n` and grep -n emit a
            # leading line number; skip those lines entirely.
            if re.match(r"^\s*\d+[:\t\|]", line_text):
                continue
            m = pat.search(line_text)
            if not m:
                continue
            n = m.group(1) or m.group(2)
            if not n or n == "0":
                continue
            later = [x for x in s.turns if x["line"] > r.get("line", t["line"])]
            if not later:
                continue
            # Search every later prose turn, not the next few. A session that
            # carried the full partition in its closing report was flagged on an
            # interim run eight turns earlier.
            window = " ".join(x["text"] for x in later)
            if n in window:
                continue
            if not (CLEAN_RE.search(window) or DONE_RE.search(window)):
                continue
            out.append(finding(
                "T11", f"a printed non-zero class ({' '.join(m.group(0).split())}) "
                       f"is absent from the report that follows",
                r.get("line", t["line"]), " ".join(line_text.split())[:180], 1, "observed",
                figure=n,
                remedy="report every class the gate printed, summing to its total"))
            break
    return out


def t12_no_delegation(s: Session, ctx) -> list[dict]:
    """A fan-out skill ran and nothing was ever spawned."""
    fanout = [s_ for s_ in s.skills
              if re.search(r"ship-fleet|shipyard|ship-feature|ship-armada|fleet", s_["skill"], re.I)]
    if not fanout:
        return []
    spawns = [t for t in s.tools if t["name"] in SPAWN_TOOLS]
    if spawns or s.sidechains:
        return []
    todo = [t for t in s.tools if t["name"] in TODO_TOOLS]
    return [finding(
        "T12", f"{fanout[0]['skill']} ran with zero spawned agents "
               f"({len(todo)} todo-tool calls are not delegation)",
        fanout[0]["line"], fanout[0]["skill"], 1, "observed",
        remedy="check the ledger's isolation claims against git branch/worktree state")]


def t13_polling(s: Session, ctx) -> list[dict]:
    """Reported as one line and never read further — real token cost, no correctness cost."""
    bash = s.bash()
    if not bash:
        return []
    polls = [t for t in bash if POLL_RE.search(t["command"] or "")]
    runs, best, prev = 0, 0, None
    for t in s.tools:
        sig = (t["name"], json.dumps(t["input"], sort_keys=True)[:400])
        if sig == prev:
            runs += 1
            best = max(best, runs + 1)
        else:
            runs = 0
        prev = sig
    share = len(polls) / len(bash)
    if share < 0.30 and best < 6:
        return []
    return [finding(
        "T13", f"polling is {share:.0%} of Bash calls; longest identical run {best}",
        polls[0]["line"] if polls else bash[0]["line"],
        " ".join((polls[0]["command"] if polls else bash[0]["command"] or "").split())[:160],
        3, "observed",
        share=round(share, 3), longest_run=best,
        remedy="`until <check>; do sleep N; done` or the harness's own notification")]


def t15_instrument_absorbed(s: Session, ctx) -> list[dict]:
    """A named instrument was unavailable and the reader was never told.

    The distinction this draws is load-bearing in both directions. An instrument
    that genuinely was not in the session's manifest is an environment failure,
    not the model's. What survives is narrower: the user asked for it and the
    reply never mentions it.
    """
    out = []
    asked: dict[str, int] = {}
    # A slash-command, not a path segment. `/Users/lukerhodes/Dev/fledgeling-plugins`
    # offered seven "instruments" on a measured run — every one a directory. So the
    # token must open at a word boundary, must not be preceded by a path character,
    # and must not be followed by one.
    rx = re.compile(r"(?:(?<=\s)|(?<=^)|(?<=`))/([a-z][a-z0-9-]{3,})(:[a-z0-9-]+)?(?![\w/.-])",
                    re.M)
    for h in s.humans:
        for m in rx.finditer(h["text"]):
            asked.setdefault(m.group(1), h["line"])
    if not asked:
        return []
    prose = " ".join(t["text"] for t in s.turns).lower()
    used = " ".join(x["skill"] for x in s.skills).lower() + " " + " ".join(t["name"] for t in s.tools).lower()
    for name, ln in asked.items():
        if name == "root":
            continue  # Codex agent addresses (`/root/task`) are hierarchy, not instruments.
        if name in used:
            continue
        if name in prose:
            continue  # mentioned to the reader, even if only to say it is missing
        out.append(finding(
            "T15", f"instrument `/{name}` was asked for, never used, and never mentioned",
            ln, name, 2, "strong-inference",
            remedy=f"say plainly whether /{name} was available, and what stood in for it"))
    return out


def t16_categorical_scope(s: Session, ctx) -> list[dict]:
    """A categorical scope in the brief, with no count reported against it.

    Matched on token boundaries: substring matching gives a false pass, measured
    — `MenuBarExtra` cleared the token "menus" in the audit this came from.
    """
    if not s.humans:
        return []
    brief = s.humans[0]
    nouns: list[str] = []
    for m in re.finditer(r"\b(?:all|every|each)\s+((?:[a-z]+(?:,\s*|\s+and\s+|\s+)){0,5}[a-z]+)\b",
                         brief["text"], re.I):
        for tok in re.split(r",\s*|\s+and\s+|\s+", m.group(1)):
            tok = tok.strip().lower()
            # Abstract nouns carry no denominator. "every project has work" is a
            # standing directive, not a deliverable scope, and it produced two
            # findings on a measured run that nothing could ever have satisfied.
            if len(tok) > 3 and tok not in STOP_NOUNS and tok.endswith("s"):
                nouns.append(tok)
    if not nouns:
        return []
    prose = " ".join(t["text"] for t in s.turns)
    out = []
    for tok in dict.fromkeys(nouns):
        stem = tok.rstrip("s")
        counted = re.search(r"\b\d+\s*(?:of|/)\s*\d+\s+%ss?\b" % re.escape(stem), prose, re.I) \
            or re.search(r"\b\d+\s+%ss?\b" % re.escape(stem), prose, re.I)
        if counted:
            continue
        out.append(finding(
            "T16", f"categorical scope `{tok}` in the brief, no count reported against it",
            brief["line"], tok, 2, "strong-inference",
            remedy=f"report a fraction for {tok}: delivered over enumerated"))
    return out[:8]


def t17_figure_without_provenance(s: Session, ctx) -> list[dict]:
    """A figure in a durable claim that no earlier tool result printed.

    Order is the whole probe. An order-blind version — "does this number appear
    anywhere in the session" — passes the exact case it was written for, because
    the figure usually does appear later, in the very artifact being questioned.
    So the search is bounded to results that arrived *before* the claim.

    Item ids are excluded by shape. `MT-0166` and `DEF-010` carry three- and
    four-digit runs that are identifiers rather than measurements, and flagging
    them buries the one figure that matters.
    """
    out = []
    prior: list[tuple[int, str]] = []
    for t in s.tools:
        r = s.result_for(t)
        if r.get("text"):
            prior.append((r.get("line", t["line"]), r["text"]))
    for turn in s.turns:
        if not DURABLE_RE.search(turn["text"]):
            continue
        # strip identifiers before looking for measurements
        cleaned = re.sub(r"\b[A-Z]{2,6}-?\d{3,5}\b", " ", turn["text"])
        cleaned = re.sub(r"\b(?:19|20)\d{2}-\d{2}-\d{2}\b", " ", cleaned)
        for n in dict.fromkeys(re.findall(r"\b(\d{3,}(?:,\d{3})*)\b", cleaned)):
            bare = n.replace(",", "")
            earlier = " ".join(txt for ln, txt in prior if ln < turn["line"])
            if n in earlier or bare in earlier:
                continue
            out.append(finding(
                "T17", f"the figure {n} appears in a durable claim and in no earlier tool result",
                turn["line"], " ".join(turn["text"].split())[:220], 1, "observed",
                figure=n,
                remedy=f"produce {n} from a command, or strike it from the artifact"))
    return out[:12]


PROBES = [
    ("T1", t1_overlay_unread), ("T2", t2_skill_scripts_unrun), ("T3", t3_red_gate_green_report),
    ("T4", t4_laundering_window), ("T5", t5_gate_suppressed), ("T6", t6_orphan_exit_status),
    ("T7", t7_lane_family), ("T8", t8_lane_output_unread), ("T9", t9_lane_from_recollection),
    ("T10", t10_bulk_arming), ("T11", t11_denominator_elision), ("T12", t12_no_delegation),
    ("T13", t13_polling), ("T15", t15_instrument_absorbed), ("T16", t16_categorical_scope),
    ("T17", t17_figure_without_provenance),
]


# ------------------------------------------------------------------ assertions

def extract_assertions(s: Session, aliases: dict[str, str], allcmd: str) -> list[dict]:
    """The universe the partition has to cover: what the session asserted."""
    out = []
    for t in s.turns:
        for m in CLAIM_RE.finditer(t["text"]):
            quote = " ".join(m.group(0).split())[:300]
            named = set(re.findall(r"[\w./-]+\.(?:py|sh|mjs|js|ts)\b", quote))
            named |= set(re.findall(
                r"\b(?:pytest|jest|vitest|playwright|xcodebuild|swiftc|cargo|turbo|eslint|tsc|obscura)\b",
                quote, re.I))
            missing = sorted(n for n in named if os.path.basename(n).lower() not in allcmd.lower())
            out.append({
                "kind": "gate" if named else "figure" if re.search(r"\d", quote) else "status",
                "line": t["line"], "text": quote,
                "names": sorted(named), "unmatched": missing,
                "durable": bool(DURABLE_RE.search(quote)),
            })
    for t in s.turns:
        if DONE_RE.search(t["text"]):
            out.append({"kind": "status", "line": t["line"],
                        "text": " ".join(t["text"].split())[:300],
                        "names": [], "unmatched": [], "durable": bool(DURABLE_RE.search(t["text"]))})
    seen, uniq = set(), []
    for a in out:
        k = (a["kind"], a["text"][:120])
        if k in seen:
            continue
        seen.add(k)
        uniq.append(a)
    return uniq


def marker(s: Session) -> dict:
    """Reported only when the instruction was actually injected, and only over
    first replies. Counting every text block is what produced a false reading of
    195 misses where the true figure was 1."""
    if not s.marker_injected:
        return {"applicable": False, "note": "the marker instruction never appeared in this session"}
    ok = miss = wrong = 0
    awaiting = False
    human_lines = {h["line"] for h in s.humans}
    for t in s.turns:
        if any(h < t["line"] for h in human_lines):
            pass
    if s.format == "codex-response-item":
        # Codex keeps one response item per prose turn, so the already-attributed
        # turns and human messages are the faithful equivalent of Claude blocks.
        for h in s.humans:
            later = [t for t in s.turns if t["line"] > h["line"]]
            if not later:
                continue
            text = later[0]["text"].strip()
            if text.startswith(GLYPH):
                ok += 1
            elif text[:1] and ord(text[0]) > 0x1F000:
                wrong += 1
            else:
                miss += 1
        return {"applicable": True, "present": ok, "absent": miss, "wrong_glyph": wrong,
                "note": "diagnostics only — never a finding"}
    for ln, o in s.records:
        if o.get("isSidechain"):
            continue
        if o.get("type") == "user" and ln in human_lines:
            awaiting = True
        elif o.get("type") == "assistant" and awaiting:
            blocks = (o.get("message") or {}).get("content") or []
            text = "".join(b.get("text", "") for b in blocks
                           if isinstance(b, dict) and b.get("type") == "text").strip()
            if not text:
                continue
            awaiting = False
            if text.startswith(GLYPH):
                ok += 1
            elif text[:1] and ord(text[0]) > 0x1F000:
                wrong += 1
            else:
                miss += 1
    return {"applicable": True, "present": ok, "absent": miss, "wrong_glyph": wrong,
            "note": "diagnostics only — never a finding"}


def group(findings: list[dict]) -> list[dict]:
    """Collapse repeats of one shape into one row carrying every occurrence.

    A probe that fires 22 times produces 22 rows, and a 128-row worklist is read
    by nobody — which costs the same as not running. The row keeps every line
    number, so nothing is hidden and the count itself becomes the evidence:
    "in-family reviewer lane ×22" is a stronger statement than any single line.
    """
    buckets: dict[tuple, dict] = {}
    for f in findings:
        key = (f["probe"], re.sub(r"\d+", "N", f["title"]))
        b = buckets.get(key)
        if b is None:
            b = dict(f)
            b["occurrences"] = []
            buckets[key] = b
        b["occurrences"].append({"line": f["line"], "quote": f["quote"]})
    out = []
    for b in buckets.values():
        n = len(b["occurrences"])
        b["count"] = n
        if n > 1:
            b["title"] = f"{b['title']}  (×{n})"
        b["lines"] = [o["line"] for o in b["occurrences"]][:40]
        out.append(b)
    out.sort(key=lambda f: (f["band"],
                            {"observed": 0, "strong-inference": 1, "weak-inference": 2}
                            .get(f["confidence"], 3),
                            -f["count"]))
    return out


def scan(path: str, repo: str | None) -> dict:
    s = Session(path)
    recognized = len(s.turns) + len(s.tools)
    if not s.records or recognized == 0 or s.attribution.get("error"):
        raise SystemExit(1)
    aliases = load_script_aliases(repo)
    allcmd = " ".join(expand(t["command"] or "", aliases) for t in s.bash())
    allcmd += " " + " ".join(os.path.basename(t["path"]) for t in s.tools if t["path"])
    ctx = {"aliases": aliases, "allcmd": allcmd, "repo": repo}

    findings, could_not_run = [], []
    for pid, fn in PROBES:
        try:
            findings.extend(fn(s, ctx))
        except Exception as exc:  # a probe that could not run is not a probe that passed
            could_not_run.append({"probe": pid, "error": f"{type(exc).__name__}: {exc}"})
    if s.format == "codex-response-item" and (s.orphan_calls or s.orphan_outputs):
        could_not_run.append({
            "probe": "TRANSCRIPT-PAIRING",
            "error": f"{len(s.orphan_calls)} call(s) and {len(s.orphan_outputs)} output(s) are unpaired",
        })

    corrections = [{"line": h["line"], "text": h["text"][:400]}
                   for h in s.humans if CORRECT_RE.search(h["text"])]

    findings = group(findings)
    return {
        "schema": SCHEMA,
        "transcript": os.path.abspath(path),
        "repo": os.path.abspath(repo) if repo else None,
        "transcript_format": s.format,
        "attribution": s.attribution,
        "models": dict(s.models.most_common()),
        "counts": {
            "records": len(s.records), "assistant_prose_turns": len(s.turns),
            "tool_calls": len(s.tools), "tool_outputs": s.output_count,
            "paired_tool_calls": s.call_outputs,
            "orphan_tool_calls": len(s.orphan_calls),
            "orphan_tool_outputs": len(s.orphan_outputs),
            "bash": len(s.bash()),
            "human_turns": len(s.humans), "skills": len(s.skills),
            "sidechain_records": s.sidechains,
            "spawns": sum(1 for t in s.tools if t["name"] in SPAWN_TOOLS),
        },
        "skills_invoked": [x["skill"] for x in s.skills],
        "tool_pairing": {
            "calls": [{"ordinal": t["ordinal"], "line": t["line"], "id": t.get("id"),
                       "name": t["name"], "output_line": s.results.get(t.get("id") or "", {}).get("line")}
                      for t in s.tools],
            "orphan_calls": s.orphan_calls,
            "orphan_outputs": s.orphan_outputs,
        },
        "assertions": extract_assertions(s, aliases, allcmd),
        "findings": findings,
        "human_corrections": corrections,
        "marker": marker(s),
        "probes_that_could_not_run": could_not_run,
        "alias_map_size": len(aliases),
    }


def render(d: dict) -> str:
    c = d["counts"]
    lines = [
        f"transcript   {d['transcript']}",
        f"format       {d['transcript_format']} · attribution {d['attribution']['mode']} "
        f"from :{d['attribution']['start_line']} "
        f"({d['attribution']['inherited_records_excluded']} inherited record(s) excluded)",
        f"models       {', '.join(d['models']) or '(none recorded)'}",
        f"volume       {c['tool_calls']} tool calls · {c['tool_outputs']} outputs · "
        f"{c['paired_tool_calls']} paired · {c['orphan_tool_calls']} call orphan(s) · "
        f"{c['orphan_tool_outputs']} output orphan(s) · {c['bash']} bash · "
        f"{c['assistant_prose_turns']} prose turns · {c['human_turns']} human turns",
        f"delegation   {c['spawns']} spawn call(s) · {c['sidechain_records']} sidechain records",
        f"skills       {len(d['skills_invoked'])} invocation(s): "
        f"{', '.join(dict.fromkeys(d['skills_invoked'])) or '—'}",
        f"assertions   {len(d['assertions'])} extracted "
        f"({sum(1 for a in d['assertions'] if a['durable'])} land in a durable artifact)",
        f"aliases      {d['alias_map_size']} package/make script(s) resolved before any "
        f"\"never ran\" claim",
        f"",
        f"FINDINGS     {len(d['findings'])} shape(s), "
        f"{sum(f.get('count', 1) for f in d['findings'])} occurrence(s)",
    ]
    for f in d["findings"]:
        lines.append(f"  [band {f['band']}] {f['probe']:<4} {f['title']}")
        seen = f.get("lines") or [f["line"]]
        where = f":{seen[0]}" if len(seen) == 1 else f":{seen[0]} +{len(seen) - 1} more"
        lines.append(f"            {where}  {f['quote'][:100]}")
        if f.get("remedy"):
            lines.append(f"            → {f['remedy']}")
    if d["human_corrections"]:
        lines.append("")
        lines.append(f"HUMAN CORRECTIONS  {len(d['human_corrections'])} "
                     f"(ground truth — outranks anything the session said about itself)")
        for h in d["human_corrections"][:6]:
            lines.append(f"  :{h['line']}  {h['text'][:150]}")
    if d["probes_that_could_not_run"]:
        lines.append("")
        lines.append("PROBES THAT COULD NOT RUN (not the same as probes that passed)")
        for p in d["probes_that_could_not_run"]:
            lines.append(f"  {p['probe']}: {p['error']}")
    m = d["marker"]
    lines.append("")
    lines.append("diagnostics  " + (
        f"marker present {m['present']}, absent {m['absent']}, wrong glyph {m['wrong_glyph']}"
        if m.get("applicable") else f"marker: {m['note']}"))
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("transcript", nargs="?")
    ap.add_argument("--repo", help="repository the session worked in; enables package-script alias resolution")
    ap.add_argument("--json", action="store_true", help="JSON on stdout, table on stderr")
    ap.add_argument("--out", help="write the JSON here")
    ap.add_argument("--selftest", action="store_true", help="run the paired fixtures")
    a = ap.parse_args()

    if a.selftest:
        here = os.path.dirname(os.path.abspath(__file__))
        return subprocess.call([sys.executable, os.path.join(here, "selftest.py")])

    if not a.transcript:
        ap.error("a transcript path is required")
    if not os.path.exists(a.transcript):
        print(f"signals: no such transcript: {a.transcript}", file=sys.stderr)
        return 1
    try:
        d = scan(a.transcript, a.repo)
    except SystemExit:
        print("signals: transcript held no parseable records", file=sys.stderr)
        return 1

    table = render(d)
    if a.json:
        print(json.dumps(d, indent=1))
        print(table, file=sys.stderr)
    else:
        print(table)
    if a.out:
        with open(a.out, "w") as fh:
            json.dump(d, fh, indent=1)
    return 4 if d["probes_that_could_not_run"] else 0


if __name__ == "__main__":
    sys.exit(main())
