---
name: resume-session
description: >-
  Locate, parse, and resume work from past sessions across any AI coding agent CLI (Claude Code, Antigravity/AGY, Cursor IDE, Codex, Grok, or repo workspaces). Discovers sessions by query, UUID, workspace path, or recency, extracts the 6-dimensional takeover state (initial goal, terminal errors, modified files, config keys, decisions, immediate next steps), and produces an uncorrupted continuity briefing without redundant re-discovery.
---

# `resume-session`

When an AI coding session ends unexpectedly (whether from a token limit, a compaction, an API timeout, a context clear, or simply switching between agent tools: Claude Code, Antigravity, Cursor, Codex, Grok), the next agent typically spends hundreds of tokens re-exploring the codebase, re-discovering environment configuration, or re-asking the user for context that was already established.

`resume-session` discovers past sessions across all major agent CLIs, parses their exact transcripts on disk, extracts the **6-dimensional takeover state**, and produces an actionable continuity handover so work continues immediately without lost context or redundant discovery.

---

## The 6-Dimensional Takeover State

Every resumed session is distilled into six concrete dimensions:

| Dimension | Extracted Data | Why It Matters |
| :--- | :--- | :--- |
| **1. Session Identity & Provenance** | Session UUID, CLI platform, model used, branch, last active timestamp | Anchors the session to the exact commit and tool chain |
| **2. Initial Goal & Intent** | Verbatim initial user prompt, objective spec, referenced task IDs | Prevents goal drift and scope expansion |
| **3. Terminal State & Last Context** | Exact halting error (429, 503, tool crash, compaction), last assistant response | Explains why the previous agent stopped |
| **4. Modified Files & Artifacts** | List of created, edited, and deleted files, plus read artifacts | Prevents duplicate edits and tracks active surfaces |
| **5. Technical Config & Keys** | Apple Team IDs, Bundle IDs, OAuth client IDs, ports, env vars | Eliminates config re-discovery and secret recreation |
| **6. Immediate Next Steps** | Actionable checklist of pending tasks and verification gates | Zero-delay continuation into active implementation |

---

## Phase 1: Multi-CLI Discovery

Use the bundled discovery engine `scripts/find_session.py` to search for sessions across all platforms.

```bash
# Search by topic or project name across all CLIs
python3 plugins/resume-session/skills/resume-session/scripts/find_session.py --name "Google Drive"

# Show the 5 most recent sessions across all CLIs on the machine
python3 plugins/resume-session/skills/resume-session/scripts/find_session.py --recent 5

# Filter by a specific CLI platform
python3 plugins/resume-session/skills/resume-session/scripts/find_session.py --cli agy --recent 5
python3 plugins/resume-session/skills/resume-session/scripts/find_session.py --cli claude --path ~/Dev/my-app
python3 plugins/resume-session/skills/resume-session/scripts/find_session.py --cli grok --name "earbuds"
python3 plugins/resume-session/skills/resume-session/scripts/find_session.py --cli codex --recent 5
python3 plugins/resume-session/skills/resume-session/scripts/find_session.py --cli cursor --recent 5

# Target a specific session ID
python3 plugins/resume-session/skills/resume-session/scripts/find_session.py --id daaf6175 --details
```

### CLI Discovery Matrix

| Platform | Primary Storage Location | File Format |
| :--- | :--- | :--- |
| **Claude Code** | `~/.claude/projects/<slug>/*.jsonl`<br>`~/.claude/sessions/*.jsonl`<br>`<repo>/.claude/*.jsonl` | JSONL lines with user/assistant turns, `aiTitle`, `cwd`, and tool calls |
| **Antigravity (AGY)** | `~/.gemini/antigravity-cli/brain/<uuid>/.system_generated/logs/transcript.jsonl` | Step records with `source`, `type`, `tool_calls`, `content`, and checkpoints |
| **Cursor IDE** | `~/.cursor/chats/<ws_hash>/<uuid>/meta.json`<br>`~/.cursor/chats/<ws_hash>/<uuid>/store.db` | SQLite blob store containing JSON message records and workspace metadata |
| **Codex / OpenAI** | `~/.codex/sessions/YYYY/MM/DD/*.jsonl`<br>`~/.codex/session_index.jsonl` | Structured event stream with `session_meta`, `turn_context`, and response items |
| **Grok / X.AI** | `~/.grok/sessions/<encoded_path>/<uuid>/chat_history.jsonl`<br>`summary.json` | Chat history JSONL, session summaries, prompt context, and event logs |
| **Repo Workspaces** | `docs/goals/goal-*.md`<br>`docs/plans/plan-*.md`<br>`ORCHESTRATOR.md`, `handover_report.md` | Markdown ledgers, plan files, and repository-level handover documents |

---

## Phase 2: 6D State Extraction

Once a candidate session is identified, extract the full 6-dimensional state:

```bash
# Print the full takeover briefing to terminal
python3 plugins/resume-session/skills/resume-session/scripts/find_session.py --id <SESSION_ID> --details

# Export the takeover briefing to a markdown file
python3 plugins/resume-session/skills/resume-session/scripts/find_session.py --id <SESSION_ID> --export handover.md

# Output machine-readable JSON for automated toolchains
python3 plugins/resume-session/skills/resume-session/scripts/find_session.py --id <SESSION_ID> --json
```

---

## Phase 3: Takeover Handover Briefing

The generated briefing synthesises the entire past session into a structured handover report:

```markdown
# Takeover Briefing: Continue Feature Build

**CLI Platform:** `Claude Code` (or `AGY` / `Cursor` / `Codex` / `Grok`)
**Source Session ID:** `131dedc9-527f-475b-96c2-862dcf79f5fb`  
**Working Directory:** `/Users/lukerhodes/Dev/my-app`  
**Git Branch:** `feature/new-auth`  
**Models Used:** `claude-opus-5`  
**Last Recorded Active:** `2026-08-15 15:45:10`  

---

## 1. Initial Goal & User Intent
> Implement Apple Sign-In and session persistence with rotating refresh tokens.

## 2. Key Documentation & Artifact References
- **Plan Doc:** `docs/plans/plan-AUTH-001.md`
- **Spec Doc:** `docs/specs/spec-AUTH-001.md`

## 3. Work Completed & Modified Files
The session modified 4 files:
- `apps/web/lib/auth/apple.ts`
- `apps/api/src/auth/jwt.strategy.ts`
- `packages/db/schema.prisma`
- `apps/web/app/api/auth/callback/route.ts`

## 4. Technical Environment & Decisions
- **Config `APPLE_TEAM_ID`:** `A1B2C3D4E5`
- **Config `BUNDLE_IDENTIFIER`:** `com.fledgeling.app`
- **Config `PORT`:** `3000`
- DECISION: Reject third-party OAuth wrappers in favour of direct web crypto tokens.

## 5. Terminal State & Last Context
> [!WARNING]
> **Session Halted on Error:**
> `Rate limit exceeded (429): Token quota depleted on claude-opus-5.`

**Last Assistant Output:**
> "All database migrations applied. Next step is writing unit tests for jwt.strategy.ts."

## 6. Immediate Next Steps for Takeover Agent
1. Run `git status` in `/Users/lukerhodes/Dev/my-app` to verify uncommitted changes.
2. Read `docs/plans/plan-AUTH-001.md` to check step 4 status.
3. Resume execution: Implement unit tests for `jwt.strategy.ts` and run test suite.
```

---

## Phase 4: Execution Continuity

When taking over a session, follow this 4-step execution protocol:

1. **Reconcile Workspace State:**
   ```bash
   git status
   git diff --stat
   ```
   Confirm which file changes are already on disk versus what was only planned.

2. **Verify Standing Constraints & Environment:**
   Review Section 4 of the handover report (Apple Team IDs, OAuth keys, architecture decisions) so you do not violate constraints already decided.

3. **Run Pre-flight Gates:**
   Run the project's typecheck or test suite to ensure the baseline is sound before making new edits:
   ```bash
   pnpm typecheck # or npm test / cargo test / pytest
   ```

4. **Continue the Work:**
   Proceed directly to the uncompleted items in Section 6 of the briefing.

---

## Platform-Specific Details & Cheatsheet

### 1. Antigravity (AGY)
- **Transcript Path:** `~/.gemini/antigravity-cli/brain/<uuid>/.system_generated/logs/transcript.jsonl`
- **Brain Artifacts:** `<appDataDir>/brain/<uuid>/` (contains plans, analysis reports, generated assets)
- **Key Feature:** Captures subagent invocations, tool call arguments, and user-facing checkpoints.

### 2. Claude Code
- **Transcript Path:** `~/.claude/projects/-<slug>/<uuid>.jsonl`
- **Native Resume:** `claude --resume <uuid>`
- **Trap to Avoid:** When a session is resumed natively, monitor/background bash tasks are not restored; verify running dev servers manually.

### 3. Cursor IDE
- **Chat Path:** `~/.cursor/chats/<workspace_hash>/<session_uuid>/`
- **Storage:** `meta.json` (timestamps and cwd) + `store.db` (SQLite containing conversation JSON blobs).
- **Key Feature:** Full IDE editor state and multi-tab context.

### 4. Codex / OpenAI CLI
- **Transcript Path:** `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`
- **Index:** `~/.codex/session_index.jsonl` (fast mapping of thread names to UUIDs).
- **Key Feature:** High-fidelity turn context logs including sandbox permissions and tool execution outputs.

### 5. Grok / X.AI CLI
- **Session Path:** `~/.grok/sessions/<url_encoded_path>/<uuid>/`
- **Key Files:** `chat_history.jsonl`, `summary.json`, `prompt_context.json`, `events.jsonl`.
- **Key Feature:** Structured summaries and sandbox rewind points.
