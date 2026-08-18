# resume-session: evals & benchmark

**Six structural evals across five agent CLIs, tested against a no-skill baseline and predecessor.**

| Metric / Dimension | `resume-session` | Predecessor (`resume-claude-session`) | No-Skill Baseline |
| :--- | :---: | :---: | :---: |
| **Multi-CLI Discovery (5 Platforms)** | **5/5 (100%)** | 1/5 (20%) | 0/5 (0%) |
| **6D State Extraction Accuracy** | **6/6 (100%)** | 4/6 (66%) | 2/6 (33%) |
| **Config Key Preservation (OAuth/Apple Team ID)** | **100%** | 80% | 20% (Hallucinated/Omitted) |
| **Context Window Cost of Recovery** | **0 tokens** (Local Engine) | 0 tokens (Claude only) | 45,000 to 180,000 tokens |
| **Time to Resumption** | **< 1.2s** | < 1.0s (Claude only) | 45s to 120s |
| **Duplicate Edit / Re-discovery Hazards** | **0** | 0 (Claude only) | 4 to 8 re-reads per run |

## How solid are these numbers

Not very. Treat everything in the table above as informal observation rather
than a harnessed measurement. The figures were recorded while the skill was
being built: single runs on one machine, no repeat trials, no judge panel, and
no run logs committed to this repository. Nothing has re-run them since.

The comparisons against the predecessor and the no-skill baseline are one run
each, so the recall and accuracy columns are directional rather than precise.
The timing, token and cost figures carry no variance at all, and the `$0.45 on
Opus per lookup` in eval 6 is arithmetic on an estimated token count, not a
billed amount.

Three tasks would settle them:

1. **A repeatable discovery harness.** Fixture session directories for all
   five CLIs, committed here, with a script that runs `find_session.py`
   against them and asserts what it found. That turns the 5/5 and 6/6 columns
   into a check that can fail.
2. **Timed runs with a spread.** Ten runs per CLI over a fixed fixture set,
   reporting median and worst case instead of a single `< 1.2s`.
3. **A measured baseline.** The no-skill numbers (45,000 to 180,000 tokens,
   45s to 120s, and the per-lookup cost that follows from them) need the
   actual baseline sessions kept, with their token counts read off the
   provider's own usage report rather than estimated.

---

## The six structural evals

### 1. Multi-CLI discovery recall (5 platforms)
- **Prompt:** `"Find the session where I was testing earbuds latency earlier today."`
- **Result:**
  - `resume-session`: Scanned across Claude, AGY, Grok, Cursor, and Codex; located the active Grok session (`~/.grok/sessions/.../01a003eb-8077-7163-ae83-825e80e658fb`) and Codex session (`~/.codex/sessions/.../01a003e8-c576-77a3-9749-2f0653adcb4d`) in 0.4 seconds.
  - Baseline: Failed to find non-Claude sessions; attempted blind file searches in `~/Dev`.

### 2. Rate limit (429) and crash recovery
- **Prompt:** `"Take over the interrupted Google Drive sync session and finish the batch poll."`
- **Result:**
  - `resume-session`: Extracted the exact 429 rate limit halting state, parsed the 5 modified files, identified `OAUTH_CLIENT_ID`, and generated immediate 3-step checklist without reading the 150KB raw JSONL transcript into prompt context.
  - Baseline: Dumped 2,000 lines of JSONL into context, burnt 48,000 tokens, and missed the OAuth client ID.

### 3. Subagent transcript extraction (Antigravity)
- **Prompt:** `"Continue the work from AGY session daaf6175."`
- **Result:**
  - `resume-session`: Parsed `transcript.jsonl` step records, identified 5 files written by subagent tool calls, extracted terminal command exit codes, and correctly formatted the initial user objective.
  - Baseline: Attempted to open `transcript_full.jsonl`, hit byte offset limits, and asked user for clarification.

### 4. Configuration key and environment retention
- **Prompt:** `"Resume the iOS provisioning session and test the build."`
- **Result:**
  - `resume-session`: Preserved `APPLE_TEAM_ID` (`A1B2C3D4E5`) and `BUNDLE_IDENTIFIER` (`com.fledgeling.app`) verbatim from past tool execution arguments.
  - Baseline: Did not extract the team ID; prompted the user to provide their Apple Developer credentials again.

### 5. Cursor SQLite database parsing
- **Prompt:** `"Find my Cursor chat session on the improve-skill loop."`
- **Result:**
  - `resume-session`: Queried `~/.cursor/chats/<hash>/<uuid>/meta.json` and extracted message history from `store.db` via standard library SQLite in 80ms.
  - Baseline: Failed to locate Cursor chat storage.

### 6. Zero token ingestion economy
- **Measurement:** Ingesting 20 recent sessions across 5 CLIs into an LLM context costs ~150k tokens ($0.45 on Opus per lookup).
- **Result:** `find_session.py` executes in pure Python 3 in < 500ms at $0.00 cost, passing only the final summary into the active agent context.

---

## Verdict and receipts

On the runs recorded here, `resume-session` moved the multi-CLI handover off the
model's context and onto local parsing: every discovery engine and parser runs
locally, with no network call and no third-party dependency. How much time and
money that saves in practice is the part the caveat above says is not yet
measured properly.
