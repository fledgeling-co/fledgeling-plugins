# The evidence behind this skill

Every rule in `SKILL.md` traces to a row here. The full corpus, the instruments
and the unedited agent output live in `docs/gemini-audit/` at the repository root.

## The corpus

18 sessions across 13 repositories, all driven by a Google Gemini model inside the
Claude Code harness — same tools, same skills, same instruction files, different
model. Each was read end to end from its JSONL transcript, cross-checked against
the repository state it left behind, and then adversarially refuted by a second
independent reader. **161 findings raised, 148 stand**, 13 refuted and dropped.

Selected from a wider census of 130 sessions in which a Gemini model served any
turn; 64 of those had a Gemini model on ≥90% of assistant turns, totalling 142 MB
and 12,230 assistant turns.

**The control arm is 37 Claude sessions** from the same eleven repositories in the
same window (14–26 August 2026). It exists because "Gemini did X" means nothing
without knowing whether Claude does X too, and it changed two verdicts.

## The distribution that decides where the pass looks

Pre-refutation labels, which is what the refutation stage was handed:

| category | n | | category | n |
|---|--:|---|---|--:|
| gate-skipped | 33 | | context-loss | 6 |
| evidence-substitution | 25 | | retry-thrash | 5 |
| fabricated-verification | 24 | | other | 4 |
| instruction-violation | 24 | | artifact-quality | 3 |
| premature-completion | 9 | | delegation-absent | 3 |
| quota-collapse | 7 | | recovery-failure | 2 |
| bound-exceeded | 2 | | scope-drift | 1 |

Refutation recategorised at least four across boundaries and revised roughly forty
severities, mostly downward. The ratio survives every individual move:

> the four account-shaped categories are **106 of 148, 72%**.
> categorical scope collapse and exceeded bounds together are **9 of 148, 6%**.

That is why the pass aims at the account rather than at the artifact, and why the
expensive tier is capped at twelve sites.

## The two measurements with a control arm

**Delegation.** Across 64 Gemini sessions and 12,230 turns: **7** agent-spawning
calls. The 37-session Claude control: **1,631**. Like-for-like on sessions
invoking `ship-fleet` or `shipyard`: 19 of 22 Claude sessions spawned agents (1,531
calls) against 1 of 8 Gemini sessions (7 calls). `AskUserQuestion` runs the same
way, 6 against 300.

The consequence is not idleness. The orchestrator does the work inline and the
skill's central mechanic never runs — one session wrote 13 specs and 13 plans by
hand and edited product source directly on `main` while its `ORCHESTRATOR.md`
recorded per-item worktrees that were never created.

**The response marker is a non-signal.** Gemini carried it on 29% of prose turns
against the Claude control's 2.9% — the opposite of the expected direction. Both
arms are contaminated: the instruction is hook-injected and fired in 43 of 64
Gemini and 15 of 37 Claude sessions, runner sessions are not expected to emit it,
and restricting one session to turn-final replies took 195 apparent misses down to
1. Recorded here so nobody re-derives it as a defect.

## What the method cannot see

- **Transcript forensics favour reporting failures over artifact-internal ones.** A
  fabricated delivery note is visible; a doubled CSS shadow inside a rendered page
  is not. The distribution above is biased toward the account and against the
  artifact. This is why two of the twelve read sites are deliberately unaimed.
- **Six sessions carry a routing alias rather than a model id.** One session's
  records carry four different model ids across its turns, so per-finding
  attribution inside it is weak.
- **Nothing ran on a Pro tier.** The corpus is `flash` and `flash-high` only.
- **No session exercised** the `warrant` family, `stocktake`, `code-review`,
  `spec-validation` or `defer` — among the most gate-heavy skills in the
  ecosystem, all of which ship a model overlay.
- **All thirteen repositories are greenfield projects** carrying ORCHESTRATOR and
  LEDGER conventions. R1, R2 and R6 assume such files exist. Nothing establishes
  the pass works on a repository without them.
- **Sessions from 17–19 August ran materially older skill versions** than ship
  today. A gap found there may already be closed.

## Open questions

**Should this run on Claude sessions too?** Two controls point opposite ways. A
required command wrapper was omitted on 85 of 85 Gemini invocations and largely
honoured on Claude, which is family-specific. But `Done (Merged)` without
independent review was done identically by a Claude session in the same repository
three weeks earlier. The probes are family-neutral; the *ranking* is tuned to a
Gemini signature, and nobody has measured how badly that misweights a Claude run.

**Which frontier model should run it?** `defer` says Fable judges but does not
verify, which points to Opus at high effort. But the deterministic and cheap-read
tiers are mechanical work a cheaper lane handles fine, and no split pass has been
measured.

**What does it cost against the session it audits?** Unmeasured. The design targets
a small multiple of a single feature's verify stage. Above about a fifth of the
audited session's cost, the rebuild threshold should come down.

**Is re-running a gate safe?** Some campaign scripts write to the registry they
read. The pass restricts itself to read-only gates, which is conservative and
probably leaves cheap recoveries on the table. Which gates are idempotent is
per-repo and undocumented.
