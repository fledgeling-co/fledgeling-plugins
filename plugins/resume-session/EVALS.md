# resume-session: evals & benchmark

**The structural eval suite at `evals/evals.json` is defined and has not been run,
so nothing it asserts is a measured result.** It holds eight prompts and 43
checkable assertions, described in its own section below. The table that follows
here is a separate and older thing: informal observations recorded while the skill
was being built. Neither is a harnessed measurement, and the caveat under the table
explains how far the table's figures can be trusted.

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

## The structural suite at `evals/evals.json` (defined, not run)

Eight prompts, 43 assertions, none of them run. The suite exists because the six
evals further down this page were written as narrative results rather than as
checks: they describe what happened once, and there is no file anywhere that a
later reader could re-run to find out whether it still happens. `evals.json` is
that file. Every assertion in it is a pass or fail property of the briefing the
skill produces, or of the commands the run issued, never a rating out of ten.

| Eval | What it targets | Why it can fail |
|---|---|---|
| `multi-cli-discovery-by-topic` | The bundled engine used across platforms rather than ad hoc searching | A topic search with no CLI named is where a run reaches for `find` and `grep` over the home directory |
| `six-dimension-briefing-complete` | All six dimensions present and individually labelled | A briefing that reads well and quietly drops the terminal state or the config keys |
| `no-transcript-ingestion` | The whole economic claim of the skill | A 100 KB transcript is right there, and reading it is the obvious move |
| `config-keys-verbatim` | Values reproduced character for character | Normalising, reformatting or example-shaping a real credential all fail it |
| `native-resume-does-not-restore-processes` | The documented trap: a natively resumed session does not bring back background tasks | A dev server and two background tasks that the user will assume came back |
| `ambiguous-id-prefix` | Disambiguating rather than resuming the first hit | Measured on this machine on 2026-08-18: the prefix `0` matched ten sessions across two different CLIs |
| `takeover-continuity-protocol` | Reconcile, honour standing decisions, run gates, then continue | Re-reading the four modified files from scratch, or re-litigating a settled decision, both fail it |
| `adv-absent-config-key` | **The adversarial case.** Two credentials are demanded, one of which the session never recorded | The briefing template has a slot for it, so filling that slot with a well-formed invention is the cheap wrong answer, and it looks exactly like a right one |

One assertion carries a `[control]` label, in the briefing-completeness eval: the
discovery engine emits the working directory and branch, so any run that uses the
tool passes it. It is kept as a shape guard on the output and named so nobody counts
it as evidence that the skill adds anything.

### What was checked by hand, on 2026-08-18

These are the only measurements on this page taken deliberately rather than
recorded in passing. Each was run against the shipped file.

| Check | Result |
|---|---|
| `skills/resume-session/SKILL.md` frontmatter parses (opening and closing `---`, `name`, `description`) | Passes. `name: resume-session` matches the directory and the plugin manifest. |
| SKILL.md length against the 500-line ceiling the repository's conformance gate enforces | Passes, at 187 lines. |
| `scripts/find_session.py` compiles under Python 3 | Passes. |
| It fails on a bad flag | Passes: exits 2 with a usage message on `--cli notacli`. |
| It fails on a query that matches nothing | Passes: exits 1 and prints "No sessions found matching criteria". |
| It succeeds and returns structured output | Passes: `--json` returns an object carrying `total_matches` and `results`, and each result carries the fields the six dimensions are built from (`cli_type`, `cwd`, `env_configs`, `decisions`, `files_read` and the rest). |
| Each of the six discovery lanes runs | Five of six returned three sessions each on this machine (`claude`, `agy`, `cursor`, `codex`, `grok`). The sixth, `repo`, returned nothing under `--recent` alone and returned three when given `--path` pointing at a directory tree that holds repository ledgers. That is a real difference in how the lane is driven, and it is not documented in SKILL.md. |
| A self-test or committed fixture set | **None exists.** There is no test file, no fixture directory and no `--selftest` flag, so every result above depends on what happens to be on this machine today and cannot be reproduced on another. |
| Everything the plugin claims to ship exists on disk | Passes for the script and the icon set. One separate gap the repository conformance gate reports: `assets/banner.png` is 1600x520 where the family ships 3200x1040, so it is half resolution on a retina display. That is a banner issue, not an evals issue. |

### Which claims rest on someone else's evidence

None, and that is worth saying plainly, because it cuts both ways. This skill
depends on no sibling and borrows no sibling's numbers, so nothing here is inherited
credit. It also means the six narrative evals below are the only account of it that
exists, and the caveat above them is the whole of the qualification.

### What would settle the suite

The first task named under the caveat above, the committed fixture tree, is also
the first thing this suite needs, and for the same reason: without it, every result
depends on the machine it ran on. Two further runs would finish the job.

1. **The eight prompts run twice, with the skill and with no skill.** The
   predecessor named in the table above has no committed snapshot in this
   repository, so it cannot form a reproducible arm; the no-skill baseline can.
   Grade with an independent agent that never sees the skill, one pass or fail per
   assertion with quoted evidence.
2. **The adversarial case judged on its own, on a fixture with a known absence.**
   A session that provably contains no Apple Team ID, and a prompt that insists on
   one, is the single most valuable check in this suite: a fabricated credential in
   a handover briefing is the failure that costs the most and announces itself the
   least. It needs the fixture from task one before it can be run honestly, because
   proving a value is absent requires a session whose contents are known.

---

## The six structural evals

These are the informal development-time observations behind the table at the top of
this page, not the suite in `evals.json`. They were written up as narrative results
after the fact, which is why they cannot be re-run: read them with the caveat above
in hand.

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
