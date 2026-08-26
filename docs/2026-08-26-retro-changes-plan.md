# Plan — changes from the 2026-08-26 pipeline retrospective

Evidence for every item is in `~/Dev/dAIolog/docs/retro-2026-08-26/`
(`RETROSPECTIVE.md` and the JSON under `data/`).

## A · defer — lane policy

| # | Change | Why |
|---|---|---|
| A1 | Add `codex-luna-max` (`gpt-5.6-luna`, effort `max`) as an implementation lane | Owner directive. **UNVERIFIED** — codex is 401 on an expired refresh token, so the model could not be probed. Ships marked `unverified: true` and excluded from routing until a probe passes |
| A2 | Rank `glm` → `grok` → `codex-sol` (medium) above `gemini` | Owner directive, and first-party evidence: gemini failed 8 of 12 as an autonomous builder, and is 95% of cash for 20% of output |
| A3 | Apply a first-party **delivery penalty** to gemini's bench grade rather than deleting the lane | The bench measures a model *building*; this measures whether the artefact arrived. Different things, so record it as a separate adjustment with its provenance |
| A4 | Prefer `codex-luna-max` wherever gemini was the implementation pick | Owner directive, scoped to implementation, not to reasoning-heavy classes |
| A5 | Raise per-lane timeout guidance to 900 s | 23 of grok's 24 failures were a 120 s harness bound on a lane whose median call is 150 s — 3,240 s of wait, a third of the lane budget |
| A6 | New section: when to run opus at lower effort | Nothing in the skill said `xhigh` is not the default for mechanical work |

## B · ship-fleet — scheduling and briefs

| # | Change | Why |
|---|---|---|
| B1 | Cap wave width at 5, stated as a correctness rule | 92 agents died silently at exactly 180.0 s; wider caused it. Corroborated externally at the same number |
| B2 | Verify per item via `pipeline()`, not a wave barrier | Phase 5 is 42.6 of 54.3 agent-hours; external effect size 17.6–35.1% |
| B3 | Fan-out tripwire: fail a wave whose summed agent seconds ÷ wall clock is under 1.2 | Seven runs delivered a speedup of exactly 1.00 and nothing noticed |
| B4 | Derive failure from `started − results`, never `error_rows` | `error_rows` is 0 across all 147 journals while 146 agents failed to return |
| B5 | Paste the guardrails into the brief; never name a file | 0 of 409 subagent contexts received `CLAUDE.md`; 69 briefs asked, 3 complied |

## C · dAIolog — the repo changes

| # | Change | Why |
|---|---|---|
| C1 | `tools/gate-reporter.cjs` — a three-line jest reporter, full JSON to `.gates/` | 88% of gate calls pipe, 23% have no readable verdict, 361 of 678 rework chains contain no edit |
| C2 | `scripts/limit` — a vendored `timeout` shim | 40 calls died on `command not found: timeout`; macOS ships no coreutils |
| C3 | `docs/BRIEF-GUARDRAILS.md` — the paste-in block B5 refers to | Gives the brief-writer one file to inline |
| C4 | Record the two refuted projects in the decision register | Five frames proposed the daemon, four the memoiser; both measured dead |

## D · other skills

| # | Change | Why |
|---|---|---|
| D1 | `warrant` — put a worked `snapshot_evidence.py` invocation in the skill body | 19 of 46 calls died on the same two invocation mistakes across 30 agents |
| D2 | `stocktake` — make a skipped `gates.py` loud | It ran once, with `--help`, so six gate points went unchecked on a sweep that graded 53 cards |
| D3 | `harbourmaster` — note that `governor-run` is the real cost surface | Its keyed scripts cost 118 s; the wrapper it ships cost 10,903 s |

## Not doing, and why

- **A warm resident test daemon.** Bootstrap is 0.44 s against a 2.7 s median call — ≤9% recovery for a process that must invalidate on every config and lockfile change.
- **A gate memoiser keyed on the tree hash.** Only 26 repeated calls (223 s) were identical commands whose every run passed.
- **Import-graph test selection.** Dead on runtime (27 s suite) and now on defect detection too — no published safety-loss measurement exists for JS/TS.
