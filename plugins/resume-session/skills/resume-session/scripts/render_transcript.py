#!/usr/bin/env python3
"""render_transcript.py : turn one agent session into a readable transcript, split to fit a reader.

Normalises a Claude Code, Codex, Antigravity (AGY), Muse, Cursor or Grok session into one event
stream (user, assistant, tool call, tool result, error, todo, compaction), renders it as Markdown
with numbered event anchors, and writes:

  <out>/transcript.md        the whole session, when it fits the reader's budget
  <out>/chunks/chunk-NNN.md  the same events split at user-turn boundaries, for fan-out readers
  <out>/manifest.json        token estimates, chunk ranges, the detail level used, and the plan

Conversation text (user and assistant messages) is never shortened by the detail level. Tool
inputs and outputs are, because they dominate size: a 200 MB Codex rollout is mostly tool output.
The detail level is chosen automatically as the richest one where the session either fits the
reader's budget whole or splits into no more than --max-chunks chunks.

Usage:
  python3 render_transcript.py --ref codex://threads/<uuid> --budget-tokens 400000
  python3 render_transcript.py --ref <uuid-or-prefix> --cli muse --out /tmp/rs-<id>
  python3 render_transcript.py --file path/to/session.jsonl --cli claude --detail lean
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import sqlite3
import sys
from typing import Any, Dict, Iterator, List, Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import find_session as fs  # noqa: E402

CHARS_PER_TOKEN = 3.6  # conservative estimate for mixed prose, code and JSON

# (tool-call chars, tool-result head chars, tool-result tail chars, system-message chars, one-line calls)
DETAIL_LEVELS = {
    "full": (6000, 6000, 2000, 3000, False),
    "normal": (1500, 1200, 400, 1500, False),
    "lean": (300, 240, 100, 600, True),
    "minimal": (200, 0, 0, 300, True),  # tool results dropped except errors
}
KEY_ARGS = ("command", "cmd", "CommandLine", "file_path", "path", "Path", "AbsolutePath", "TargetFile",
            "pattern", "query", "url", "name", "skill", "task_name", "objective", "Prompt", "description",
            "subagent_type", "target", "message")
DETAIL_ORDER = ["full", "normal", "lean", "minimal"]
USER_TEXT_CAP = 20000  # a pasted log can be huge; keep head and tail beyond this
ASSISTANT_TEXT_CAP = 30000


def est_tokens(text: str) -> int:
    return int(len(text) / CHARS_PER_TOKEN) + 1


def clip(text: str, head: int, tail: int = 0) -> str:
    if text is None:
        return ""
    if len(text) <= head + tail:
        return text
    if head <= 0 and tail <= 0:
        return f"[{len(text)} chars omitted]"
    mid = len(text) - head - tail
    return text[:head] + f"\n[... {mid} chars omitted ...]\n" + (text[-tail:] if tail else "")


def ev(role: str, text: str = "", ts: Any = None, **kw: Any) -> Dict[str, Any]:
    d = {"role": role, "text": text or "", "ts": ts}
    d.update(kw)
    return d


# ── Per-CLI event iterators ──────────────────────────────────────────────────

def iter_claude(path: pathlib.Path) -> Iterator[Dict[str, Any]]:
    plain_users = fs.claude_plain_user_texts(path)
    for line in fs.iter_jsonl_lines(path):
        try:
            d = json.loads(line)
        except Exception:
            continue
        t, ts = d.get("type"), d.get("timestamp")
        if t == "queue-operation" and d.get("operation") == "enqueue":
            q = d.get("content")
            if isinstance(q, str) and q.strip() and not fs.is_injected(q) and q.strip() not in plain_users:
                yield ev("user", "(sent while the agent was mid-turn) " + q.strip(), ts)
            continue
        if t == "summary" and d.get("summary"):
            yield ev("compaction", d["summary"], ts)
            continue
        msg = d.get("message") if isinstance(d.get("message"), dict) else None
        if not msg:
            continue
        content = msg.get("content")
        if t == "user":
            if d.get("isCompactSummary") and isinstance(content, str):
                yield ev("compaction", content, ts)
                continue
            if isinstance(content, str):
                if not fs.is_injected(content) and not d.get("isMeta"):
                    yield ev("user", content, ts)
                continue
            for item in content or []:
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "text" and item.get("text") and not fs.is_injected(item["text"]):
                    yield ev("user", item["text"], ts)
                elif item.get("type") == "tool_result":
                    c = item.get("content")
                    if isinstance(c, list):
                        c = "\n".join(x.get("text", "") for x in c if isinstance(x, dict))
                    yield ev("tool_result", str(c or ""), ts, error=bool(item.get("is_error")))
        elif t == "assistant":
            for item in content or []:
                if not isinstance(item, dict):
                    continue
                if item.get("type") == "text" and item.get("text"):
                    yield ev("assistant", item["text"], ts, model=msg.get("model"))
                elif item.get("type") == "tool_use":
                    yield ev("tool_call", json.dumps(item.get("input"), ensure_ascii=False), ts, tool=item.get("name"))


def iter_agy(path: pathlib.Path) -> Iterator[Dict[str, Any]]:
    full = path.parent / "transcript_full.jsonl"
    src = full if full.exists() else path
    for line in fs.iter_jsonl_lines(src):
        try:
            d = json.loads(line)
        except Exception:
            continue
        st, ts, content = d.get("type"), d.get("created_at"), d.get("content")
        if st == "USER_INPUT" and isinstance(content, str):
            m = re.search(r"<USER_REQUEST>(.*?)</USER_REQUEST>", content, re.DOTALL)
            yield ev("user", m.group(1).strip() if m else content, ts)
        elif st == "PLANNER_RESPONSE":
            if isinstance(content, str) and content.strip():
                yield ev("assistant", content, ts)
            for tc in d.get("tool_calls") or []:
                if isinstance(tc, dict):
                    a = tc.get("args")
                    yield ev("tool_call", a if isinstance(a, str) else json.dumps(a, ensure_ascii=False), ts, tool=tc.get("name"))
        elif st == "CHECKPOINT" and isinstance(content, str):
            yield ev("compaction", content, ts)
        elif st == "SYSTEM_MESSAGE" and isinstance(content, str):
            yield ev("system", content, ts)
        elif st in ("GENERIC", "RUN_COMMAND") and content:
            err = st == "RUN_COMMAND" and d.get("exit_code", 0) not in (0, None)
            yield ev("tool_result", str(content), ts, error=err)


def iter_codex(path: pathlib.Path) -> Iterator[Dict[str, Any]]:
    for line in fs.iter_jsonl_lines(path):
        try:
            d = json.loads(line)
        except Exception:
            continue
        rtype, ts = d.get("type"), d.get("timestamp")
        p = d.get("payload") or {}
        if not isinstance(p, dict):
            continue
        pt = p.get("type")
        if rtype == "compacted":
            yield ev("compaction", p.get("message") or "[context compacted; replacement history not rendered]", ts)
        elif rtype == "event_msg":
            if pt and ("error" in pt or "aborted" in pt):
                yield ev("error", json.dumps(p, ensure_ascii=False)[:2000], ts)
        elif rtype == "response_item":
            role = p.get("role")
            if pt == "message" and role == "user":
                text = fs.codex_item_text(p.get("content")).strip()
                if text and not fs.is_injected(text):
                    yield ev("user", text, ts)
            elif pt == "message" and role == "assistant":
                text = fs.codex_item_text(p.get("content"))
                if text:
                    yield ev("assistant", text, ts)
            elif pt in ("function_call", "custom_tool_call"):
                body = p.get("arguments") or p.get("input") or ""
                if not isinstance(body, str):
                    body = json.dumps(body, ensure_ascii=False)
                if "gAAAA" in body:  # encrypted inter-agent payloads carry no readable text
                    body = re.sub(r"gAAAA[A-Za-z0-9_\-=]{20,}", "[encrypted]", body)
                yield ev("tool_call", body, ts, tool=p.get("name"))
            elif pt in ("function_call_output", "custom_tool_call_output"):
                out = p.get("output")
                text = fs.codex_item_text(out) if not isinstance(out, str) else out
                text = re.sub(r"^Script completed\s+Wall time [\d.]+ seconds\s+Output:\s*", "", text or "")
                yield ev("tool_result", text, ts)
            elif pt == "agent_message":
                text = fs.codex_item_text(p.get("content"))
                yield ev("system", f"agent message from {p.get('author')} to {p.get('recipient')}: {text}", ts)


def iter_muse(path: pathlib.Path) -> Iterator[Dict[str, Any]]:
    last_intent = None
    for rec, ptype, payload in fs.muse_events(path):
        ts = int(rec["recorded_at"]) // 1000 if rec.get("recorded_at") else None
        if ptype == "runtime.user_intent.accepted":
            if payload.get("intent_id") and payload.get("intent_id") == last_intent:
                continue
            last_intent = payload.get("intent_id")
            text = fs.muse_user_text(payload)
            if text:
                yield ev("user", text, ts)
        elif ptype == "runtime.session" and payload.get("kind") == "run":
            e = payload.get("event") or {}
            k = e.get("kind")
            if k == "assistant_message_committed" and e.get("text"):
                yield ev("assistant", e["text"], ts)
            elif k == "reasoning_summary_committed" and e.get("text"):
                yield ev("note", e["text"], ts)
            elif k == "assistant_tool_calls_committed":
                for tc in e.get("tool_calls") or []:
                    yield ev("tool_call", tc.get("args") or "", ts, tool=tc.get("name"))
            elif k == "tool_result_batch_committed":
                for r in e.get("results") or []:
                    yield ev("tool_result", r.get("text") or "", ts, error=bool(r.get("is_error")))
            elif k == "todo_snapshot_updated":
                items = e.get("items") or []
                lines = [f"[{i.get('status')}] {i.get('text')}" for i in items if isinstance(i, dict)]
                yield ev("todo", "\n".join(lines), ts)
            elif k == "terminal":
                term = e.get("terminal")
                if term not in ("completed", "succeeded", None):
                    yield ev("error", f"run {term}: {e.get('reason') or ''}", ts)
        elif ptype == "subagent.control.result_ready":
            r = payload.get("record") or {}
            yield ev("system", f"subagent {r.get('subagent_id')} result: {r.get('summary') or ''}", ts)


def iter_cursor(chat_dir: pathlib.Path) -> Iterator[Dict[str, Any]]:
    store = chat_dir / "store.db"
    if not store.exists():
        return
    try:
        conn = fs.ro_connect(store)
        rows = conn.execute("SELECT data FROM blobs").fetchall()
        conn.close()
    except Exception:
        return
    for (data,) in rows:
        if not isinstance(data, bytes):
            continue
        txt = data.decode("utf-8", errors="replace")
        if not (txt.startswith("{") and txt.endswith("}")):
            continue
        try:
            obj = json.loads(txt)
        except Exception:
            continue
        role, content = obj.get("role"), obj.get("content")
        if isinstance(content, list):
            content = "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
        if role in ("user", "assistant") and content:
            m = re.search(r"<user_query>(.*?)</user_query>", content, re.DOTALL)
            yield ev(role, m.group(1).strip() if m else content)


def iter_grok(session_dir: pathlib.Path) -> Iterator[Dict[str, Any]]:
    chat = session_dir / "chat_history.jsonl"
    if not chat.exists():
        return
    for line in fs.iter_jsonl_lines(chat):
        try:
            d = json.loads(line)
        except Exception:
            continue
        content = d.get("content")
        if isinstance(content, list):
            content = "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
        if d.get("type") in ("user", "assistant") and content:
            yield ev(d["type"], content, d.get("timestamp"))


ITERATORS = {"claude": iter_claude, "agy": iter_agy, "codex": iter_codex, "muse": iter_muse,
             "cursor": iter_cursor, "grok": iter_grok}


# ── Rendering and chunking ───────────────────────────────────────────────────

def squash(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def summarize_call(text: str, cap: int) -> str:
    """One line naming what a tool call acted on: its command, path, query or objective."""
    try:
        a = json.loads(text)
    except Exception:
        a = None
    if isinstance(a, dict):
        parts = []
        for k in KEY_ARGS:
            v = a.get(k)
            if v:
                v = " ".join(v) if isinstance(v, list) else str(v)
                parts.append(f"{k}={squash(v)}")
            if sum(len(x) for x in parts) > cap:
                break
        line = "; ".join(parts) or re.sub(r"\s+", " ", text)
    else:
        files = [m.group(1)[0] + ":" + m.group(2).strip() for m in fs.APPLY_PATCH_FILE_RE.finditer(text or "")]
        cmds = re.findall(r"cmd:\s*\"((?:[^\"\\]|\\.){1,200})\"", text or "")
        line = "; ".join(([f"patch {', '.join(files)}"] if files else []) + [f"cmd={c}" for c in cmds])
        line = line or re.sub(r"\s+", " ", text or "")
    return line[:cap] + ("..." if len(line) > cap else "")


def render_event(n: int, e: Dict[str, Any], level: str) -> Optional[str]:
    call_cap, res_head, res_tail, sys_cap, one_line = DETAIL_LEVELS[level]
    ts = fs.format_timestamp(e.get("ts")) if e.get("ts") else ""
    stamp = f" {ts}" if ts and ts != "Unknown" else ""
    role, text = e["role"], fs.redact(e.get("text") or "")
    if role == "user":
        return f"### #{n}{stamp} USER\n\n{clip(text, USER_TEXT_CAP - 4000, 4000)}\n"
    if role == "assistant":
        return f"### #{n}{stamp} ASSISTANT\n\n{clip(text, ASSISTANT_TEXT_CAP - 5000, 5000)}\n"
    if role == "tool_call":
        if one_line:
            return f"- #{n} `{e.get('tool')}` {summarize_call(text, call_cap)}\n"
        return f"#### #{n}{stamp} tool call `{e.get('tool')}`\n```\n{clip(text, call_cap)}\n```\n"
    if role == "tool_result":
        if e.get("error"):
            return f"#### #{n}{stamp} tool result (ERROR)\n```\n{clip(text, max(res_head, 800), max(res_tail, 400))}\n```\n"
        if res_head == 0 and res_tail == 0:
            return None
        if one_line:
            return f"  - #{n} result: {squash(clip(text, res_head, res_tail))}\n"
        return f"#### #{n}{stamp} tool result\n```\n{clip(text, res_head, res_tail)}\n```\n"
    if role == "error":
        return f"### #{n}{stamp} ERROR\n\n```\n{text}\n```\n"
    if role == "compaction":
        return f"### #{n}{stamp} COMPACTION SUMMARY (written by the session's own harness)\n\n{clip(text, 12000, 2000)}\n"
    if role == "todo":
        return f"#### #{n}{stamp} todo list\n```\n{text}\n```\n"
    if role == "note":
        return f"#### #{n}{stamp} reasoning summary\n\n{clip(text, 1200)}\n"
    if role == "system":
        return f"#### #{n}{stamp} system / agent message\n\n{clip(text, sys_cap)}\n"
    return None


def render_all(events: List[Dict[str, Any]], level: str) -> List[Dict[str, Any]]:
    out = []
    for n, e in enumerate(events, 1):
        r = render_event(n, e, level)
        if r is not None:
            out.append({"n": n, "role": e["role"], "ts": e.get("ts"), "md": r, "tokens": est_tokens(r)})
    return out


def split_chunks(rendered: List[Dict[str, Any]], chunk_tokens: int) -> List[List[Dict[str, Any]]]:
    """Split at a user turn when one falls in the last 40% of a chunk, else at any event."""
    chunks: List[List[Dict[str, Any]]] = []
    cur: List[Dict[str, Any]] = []
    size = 0
    for r in rendered:
        if cur and size + r["tokens"] > chunk_tokens:
            cut = None
            for i in range(len(cur) - 1, 0, -1):
                if cur[i]["role"] == "user" and sum(x["tokens"] for x in cur[:i]) >= 0.6 * chunk_tokens:
                    cut = i
                    break
            if cut:
                chunks.append(cur[:cut])
                cur = cur[cut:]
            else:
                chunks.append(cur)
                cur = []
            size = sum(x["tokens"] for x in cur)
        cur.append(r)
        size += r["tokens"]
    if cur:
        chunks.append(cur)
    return chunks


def header(meta: Dict[str, Any], extra: str = "") -> str:
    lines = [
        f"# Session transcript: {fs.redact(meta.get('custom_name') or meta.get('title') or meta.get('session_id') or '')}",
        "",
        f"- CLI: {meta.get('cli_type')}  |  session: `{meta.get('session_id')}`",
        f"- Working directory: `{meta.get('cwd')}`  |  branch: `{meta.get('git_branch')}`",
        f"- Models: {', '.join(meta.get('models') or [])}",
        f"- Source: `{meta.get('file_path')}`",
    ]
    if extra:
        lines.append(extra)
    lines.append("")
    lines.append("Event numbers (`#N`) are stable anchors across the full transcript and every chunk.")
    lines.append("")
    return "\n".join(lines)


def private_out_dir(requested: Optional[str], session_id: str) -> pathlib.Path:
    """The output directory, created owner-only and refused if it is a symlink or someone else's.

    Transcripts carry a session's prompts and tool output, so they never default to the shared
    /tmp, where another local user could pre-create the predictable path or plant a symlink in it.
    """
    if requested:
        out = pathlib.Path(os.path.expanduser(requested))
    else:
        base = pathlib.Path(os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache")) / "resume-session"
        base.mkdir(parents=True, exist_ok=True, mode=0o700)
        out = base / re.sub(r"[^A-Za-z0-9._-]", "_", session_id)
    for d in [out.parent, out] if not requested else [out]:
        if d.is_symlink():
            raise SystemExit(f"refusing to write through a symlink: {d}")
    out.mkdir(parents=True, exist_ok=True, mode=0o700)
    st = out.stat()
    if st.st_uid != os.getuid():
        raise SystemExit(f"refusing to write into a directory owned by another user: {out}")
    os.chmod(out, 0o700)
    for sub in ("chunks", "briefs", "findings"):
        if (out / sub).is_symlink():
            raise SystemExit(f"refusing to write through a symlink: {out / sub}")
    return out


BRIEF_TEMPLATE = pathlib.Path(__file__).resolve().parent.parent / "references" / "chunk-reader-brief.md"


def fill_brief(fields: Dict[str, Any]) -> Optional[str]:
    """Fill the chunk-reader brief (the text between its two --- rules) from manifest fields."""
    if not BRIEF_TEMPLATE.exists():
        return None
    parts = BRIEF_TEMPLATE.read_text(encoding="utf-8").split("\n---\n")
    if len(parts) < 3:
        return None
    template = parts[1].strip() + "\n"
    missing = sorted(set(re.findall(r"\{([a-z_]+)\}", template)) - set(fields))
    if missing:
        raise SystemExit(f"chunk-reader brief names fields the manifest lacks: {missing}")
    return re.sub(r"\{([a-z_]+)\}",
                  lambda m: str(fields[m.group(1)]) if fields[m.group(1)] is not None else "not recorded",
                  template)


def main() -> int:
    ap = argparse.ArgumentParser(description="Render one agent session as a readable, chunked transcript.")
    ap.add_argument("--ref", help="Deeplink (codex://threads/<id>), UUID or prefix, or Muse session name")
    ap.add_argument("--file", help="Path to a session file or session directory instead of --ref")
    ap.add_argument("--cli", choices=[c for c in fs.CLI_CHOICES if c != "repo"], default="all")
    ap.add_argument("--out", help="Output directory (default: ~/.cache/resume-session/<session-id>, mode 0700)")
    ap.add_argument("--budget-tokens", type=int, default=0,
                    help="Tokens the reading model can spend on the whole transcript; 0 forces fan-out planning")
    ap.add_argument("--chunk-tokens", type=int, default=120000, help="Target tokens per chunk (default 120000)")
    ap.add_argument("--max-chunks", type=int, default=8, help="Most chunks a fan-out may use (default 8)")
    ap.add_argument("--detail", choices=["auto"] + DETAIL_ORDER, default="auto")
    args = ap.parse_args()

    if args.file:
        fpath = pathlib.Path(os.path.expanduser(args.file))
        cli = args.cli
        if cli == "all":
            print("--file needs --cli to name the session format.", file=sys.stderr)
            return 2
        meta = fs.load_session_details(cli, fpath, quick_scan=False)
    elif args.ref:
        try:
            meta = fs.resolve_session(args.ref, args.cli)
        except fs.AmbiguousRef as amb:
            print(f"{args.ref!r} matches more than one session; pass --cli or a longer id:", file=sys.stderr)
            for line in amb.args[0]:
                print("  " + line, file=sys.stderr)
            return 2
        if not meta:
            note = fs.parse_session_ref(args.ref).get("note")
            print(f"No local session matches {args.ref!r}." + (f" {note}" if note else ""), file=sys.stderr)
            return 1
        cli, fpath = meta["cli_type"], pathlib.Path(meta["file_path"])
    else:
        ap.print_usage(sys.stderr)
        return 2

    events = list(ITERATORS[cli](fpath))
    if not events:
        print(f"Parsed 0 events from {fpath}; the format may have changed.", file=sys.stderr)
        return 1

    # One reader at lean detail or richer beats several readers at higher detail: a single reader
    # keeps the session's causality intact. So: whole-session fit first (down to lean), then a
    # fan-out within --max-chunks, then minimal detail either way.
    cache: Dict[str, Any] = {}

    def at(level: str):
        if level not in cache:
            rendered = render_all(events, level)
            total = sum(r["tokens"] for r in rendered)
            cache[level] = (level, rendered, total, split_chunks(rendered, args.chunk_tokens))
        return cache[level]

    rich = ["full", "normal", "lean"] if args.detail == "auto" else [args.detail]
    chosen = None
    for level in rich:
        lv, rendered, total, chunks = at(level)
        if args.budget_tokens and total <= args.budget_tokens:
            chosen = (lv, rendered, total, chunks, "full")
            break
    if not chosen:
        for level in rich:
            lv, rendered, total, chunks = at(level)
            if len(chunks) <= args.max_chunks:
                chosen = (lv, rendered, total, chunks, "fanout")
                break
    if not chosen:
        lv, rendered, total, chunks = at("minimal" if args.detail == "auto" else args.detail)
        fits = bool(args.budget_tokens) and total <= args.budget_tokens
        chosen = (lv, rendered, total, chunks, "full" if fits else "fanout")
    level, rendered, total, chunks, mode = chosen
    if mode == "fanout" and len(chunks) == 1:
        mode = "full"

    out = private_out_dir(args.out, meta["session_id"])
    (out / "chunks").mkdir(parents=True, exist_ok=True)
    for old in (out / "chunks").glob("chunk-*.md"):
        old.unlink()
    # Each render gets an id and its own findings directory. Findings from an earlier render can
    # then never sit at a path this manifest names, so a runner that skips re-rendering, or reads a
    # directory left by an interrupted run, cannot mistake stale reader output for current output.
    import time
    render_id = time.strftime("%Y%m%d-%H%M%S")
    findings_dir = out / "findings" / render_id
    findings_dir.mkdir(parents=True, exist_ok=True)
    (out / "briefs").mkdir(exist_ok=True)
    for old in (out / "briefs").glob("chunk-*.md"):
        old.unlink()

    goal = fs.redact(meta.get("first_prompt") or "")
    full_md = header(meta, f"- Detail level: {level}  |  events: {len(events)}  |  est. tokens: {total}") + "\n".join(r["md"] for r in rendered)
    (out / "transcript.md").write_text(full_md, encoding="utf-8")

    chunk_info = []
    last_user = ""
    for i, ch in enumerate(chunks, 1):
        carry = ""
        if i > 1:
            carry = (f"\n## Carried in from earlier chunks\n\nSession goal (first user message):\n\n> "
                     + fs.clean_text_snippet(goal, 1500)
                     + "\n\nMost recent user message before this chunk:\n\n> "
                     + fs.redact(fs.clean_text_snippet(last_user, 800)) + "\n")
        body = header(meta, f"- Chunk {i} of {len(chunks)}  |  events #{ch[0]['n']}-#{ch[-1]['n']}  |  detail: {level}") + carry + "\n" + "\n".join(r["md"] for r in ch)
        name = f"chunk-{i:03d}.md"
        (out / "chunks" / name).write_text(body, encoding="utf-8")
        for r in ch:
            if r["role"] == "user":
                last_user = events[r["n"] - 1]["text"]
        chunk_info.append({
            "chunk_number": i, "chunk_count": len(chunks),
            "file": str(out / "chunks" / name),
            "findings": str(findings_dir / f"chunk-{i:03d}.md"),
            "first_event": ch[0]["n"], "last_event": ch[-1]["n"],
            "ts_start": fs.format_timestamp(ch[0]["ts"]) if ch[0]["ts"] else None,
            "ts_end": fs.format_timestamp(ch[-1]["ts"]) if ch[-1]["ts"] else None,
            "est_tokens": est_tokens(body), "lines": body.count("\n") + 1,
            "user_turns": sum(1 for r in ch if r["role"] == "user"),
        })

    counts: Dict[str, int] = {}
    for e in events:
        counts[e["role"]] = counts.get(e["role"], 0) + 1
    manifest = {
        "render_id": render_id,
        "session_id": meta["session_id"], "cli": cli,
        "title": fs.redact(meta.get("custom_name") or meta.get("title") or ""),
        "goal": fs.clean_text_snippet(goal, 2000),
        "cwd": meta.get("cwd"), "source": str(fpath), "events": len(events), "event_counts": counts,
        "detail_level": level, "est_tokens_total": total, "budget_tokens": args.budget_tokens,
        "mode": mode, "transcript": str(out / "transcript.md"),
        "transcript_lines": full_md.count("\n") + 1, "chunks": chunk_info,
        "native_resume": fs.NATIVE_RESUME.get(cli, "").format(id=meta["session_id"]) or None,
        "subagent_dir": meta.get("subagent_dir"),
    }
    if mode == "fanout":
        for c in chunk_info:
            brief = fill_brief({**{k: manifest[k] for k in ("title", "cli", "session_id", "cwd", "goal")}, **c})
            if brief:
                bpath = out / "briefs" / f"chunk-{c['chunk_number']:03d}.md"
                bpath.write_text(brief, encoding="utf-8")
                c["brief"] = str(bpath)
    if mode == "fanout" and len(chunks) > args.max_chunks:
        manifest["warning"] = (f"{len(chunks)} chunks even at detail 'minimal'; raise --chunk-tokens "
                               f"or --max-chunks, or read the oldest and newest chunks first.")
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print(f"{cli} session {meta['session_id']} ({manifest['title']})")
    print(f"events: {len(events)}  detail: {level}  est. tokens: {total}  mode: {mode}")
    if mode == "full":
        print(f"read in full: {out / 'transcript.md'} ({manifest['transcript_lines']} lines)")
    else:
        print(f"fan out over {len(chunks)} chunks:")
        for c in chunk_info:
            print(f"  {c['file']}  events #{c['first_event']}-#{c['last_event']}  ~{c['est_tokens']} tokens  {c['user_turns']} user turns")
        print(f"reader briefs: {out / 'briefs'}/chunk-NNN.md (one per chunk, fields filled)")
    if manifest.get("warning"):
        print("warning: " + manifest["warning"])
    print(f"manifest: {out / 'manifest.json'}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
