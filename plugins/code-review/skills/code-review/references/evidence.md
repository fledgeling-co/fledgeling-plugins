# Evidence — where each rule came from

Every structural choice in this skill traces to one of four sources. This file names which, so a
reader can check a rule rather than take it on the skill's word, and so a future editor knows which
lines are load-bearing measurements and which are design taste.

Four provenance classes are used below:

| Class | Meaning |
|---|---|
| **B** | The Claude Code built-in `/code-review` prompt architecture, recovered from the CLI bundle |
| **P** | The predecessor skill this one descends from (`code-review` 1.3.0, and its project-specific fork) |
| **M** | A measurement — a study, a census, or an incident with numbers attached |
| **D** | A design decision made here, with its reasoning stated and no external citation |

Where a measurement is **inherited from a predecessor without a first-party citation available at
the time of writing**, it is marked `M (inherited)`. Those are worth re-sourcing before they are
quoted outside this skill.

---

## The pipeline shape

| Rule | Class | Source |
|---|---|---|
| Phase 0 gathers the diff with `git diff @{upstream}...HEAD`, falling back to `main...HEAD` then `HEAD~1`, and unions in the working tree when the range is empty or the tree is dirty | B | The built-in's shared Phase 0 preamble: *"If there are uncommitted changes, or the range diff is empty, also run `git diff HEAD` … the review often runs before the commit."* |
| Find surfaces, Verify filters, and the finder never pre-filters | B | *"Pass every candidate with a nameable failure scenario through — finders that silently drop half-believed candidates bypass the verify step and are the dominant cause of misses."* |
| Fourteen angles; twelve selected by depth, two trigger-fired | B + P | The built-in ships 8 angles at medium/high and 10 at xhigh/max, in the same three groups — correctness, cleanup, conventions. The angle set here extends that with the trigger-fired pair and the checklist angle. |
| Angle E — wrapper, proxy and adapter correctness | B | *"check that every method routes to the wrapped instance and not back through a registry/session/global"* and *"check that the wrapper forwards all the methods the callers actually use"*. This skill's angle M is that angle generalised to mirrors and hand-copied types. |
| Angles do not suppress each other | B | *"Do NOT let one angle's conclusions suppress another's — if two angles flag the same line for different reasons, record both."* |
| Three verdicts: CONFIRMED, PLAUSIBLE, REFUTED; drop only REFUTED | B | Verbatim from the built-in's verify phase, including the definitions and *"Keep CONFIRMED and PLAUSIBLE. Drop REFUTED."* |
| PLAUSIBLE by default for realistic-but-unproven; REFUTED needs something constructible from the code | B | *"do not refute a candidate for being 'speculative' or 'depends on runtime state' when the state is realistic"*, with the same example list (races, rare-but-reachable nil, falsy zero, off-by-one, retry storms, un-anchored regex). |
| One verifier vote, not a panel | M | See "Why one verifier" below. |
| Gap sweep by a fresh finder holding the verified list | B | *"Run one more finder as a fresh reviewer who has the verified list … looking ONLY for defects not already listed. Do not re-derive or re-confirm anything already there — the job is gaps."* and *"If nothing new, return an empty sweep — do not pad."* |
| Fleet size `clamp(ceil(locDelta / 150), 2, 8)` | B | The built-in computes finder count from diff size with the same divisor and the same clamp: *"scale your investigation depth to the diff size rather than using a fixed large fleet."* |
| Finding floor of `min(fileCount, 4)`, and no invented finding to reach it | B | The built-in's floor wrapper: *"If fewer genuine findings exist, emit what you have — do not invent to hit the floor."* |
| Correctness outranks cleanup, altitude and conventions when the cap forces a cut | B | *"Correctness bugs always outrank cleanup, altitude, and conventions findings when the output cap forces a cut."* |
| Degradation is reported, not absorbed: no `Agent` tool means every angle runs inline and the report says so | B | *"State clearly in your summary that this was a single-pass review done without the Agent tool, not the full multi-agent fan-out, so whoever reads it isn't misled about what actually ran."* |
| Depth flips the objective from precision to recall rather than only changing the budget | B | medium is *"reviewing for **precision** … every finding you surface should be one a maintainer would act on"*; high is *"reviewing for **recall** … a missed bug ships"*. |
| Six gates, not five: Gate 6 (Observable) added | D | The predecessor ran five. Gate 6 exists because a config declaration and a served result are different things, and the `Vary` case in `nextjs-checklist.md` §9.7 is a finding that reads clean in source and fails in one `curl -I`. |
| Sharding above a file/LoC threshold; per-shard output files; orchestrator concatenates | P + M | Predecessor architecture, kept whole. The per-shard rule is an incident, below. |
| Suppressions persisted across runs for `by-design` and `globally-mitigated`, never for `one-off` | P | Predecessor. The `one-off` exclusion is its own rule: a wrong line number today would mask a real bug at that location tomorrow. |
| Mitigating-controls map built before Find | P | Predecessor: *"A candidate that a global control already mitigates should never be born — killing false positives at Find is far cheaper than refuting them at Verify."* |
| Verifiers run on Sonnet | P | Predecessor. The work is bounded — read one file, grep two symbols, return JSON — and the failure mode is a missing grep rather than shallow reasoning. |
| Coverage ledger with four states (`checked`, `not-applicable`, `not-checked`, `no-oracle`) | D + M | Not in either predecessor's output contract. Added because a pass and a cannot-run serialize identically; the census below is why. |
| Repo discovery replaces a hard-coded project map | D | This skill's central generalisation. A map written into a skill goes stale silently and only fits one repo; a map derived from the target repo at runtime is right by construction and right everywhere. |
| The absent-framework refutation | P (mechanism) + D (generalisation) | The project-specific fork hard-coded *"there is no NestJS and no Prisma here, so a finding that names a NestJS guard or a Prisma call is refuted at Gate 1"*. The mechanism was right and the constant was wrong; here the absences are established during discovery and passed into every verifier prompt. |

---

## Measurements

### Why one verifier, not a panel

`M (inherited)`. Nine frontier judges spanning seven model families behaved as roughly **two**
effective independent votes on a reward-modelling and NLI benchmark; panel accuracy ran 8 to 22
percentage points below what genuinely independent voting would have produced, and the best single
judge matched or beat the whole panel in every tested condition. Established aggregation methods
closed at most 11% of the gap even when given the correct answers.

The result has prior art in software specifically: 27 independently written implementations of one
specification, tested about a million times (Knight and Leveson, 1986), failed in correlated ways
and rejected the independence hypothesis outright.

Correlation is worse in this pipeline than in that benchmark, because a second verifier would
receive the same candidate, the same file and the same controls map. Agreement between readers
sharing a brief and a source pool is not corroboration.

### Why a report must not read as a verdict

`M (inherited)`. Pre-populating a reviewer's queue with a machine verdict and asking for
confirmation is the one intervention the medical-imaging literature measures as making reviewers
*worse*: specificity fell from 90.2% to 87.2% across 429,345 scans in one study, and reader
sensitivity was significantly lower with the aid in another.

The consequence in `output-format.md`: a PLAUSIBLE finding states what would confirm it rather than
asserting the failure, and `BLOCK` means a CRITICAL finding exists, not that anyone has decided.

### Why AI-authored diffs get extra weight on security and on angle B

`M (inherited)`. Across 1.2 million 2025 commits from 2,168 repositories, of which 48,563 were
agent-authored, agent commits added mocks to tests at 36% against 26% and modified test files at 23%
against 13%. Association, not causation — but it raises the prior on exactly two shapes this review
hunts: a guard replaced by a mock, and a test edited in the same commit as the code it guards.

### Why the agent budget is capped at 8 shards

`M (inherited)`. One measured run went from 23 descendant processes at zero subagents to 74 at
three and 266 at twenty, with resident memory rising from 0.2 GiB to 11.7 GiB. Shipped concurrency
ceilings are ceilings, not recommendations.

This is also what the Opus 5 prompting guidance asks for independently: *"If your harness supports
subagents, give explicit guidance on which scenarios warrant delegation, or set deterministic caps
on how many agents can be launched."*

### Why per-shard output files are not a preference

`M (incident)`. `Write` has overwrite semantics. N parallel shards writing one `candidates.jsonl`
means the last writer wins and every earlier shard's findings are destroyed with no error — 5 of 8
shards and about 85 candidates were lost this way in a live review of the predecessor skill.

### Why a fan-out is reconciled against a bucket list

`M (inherited)`. A harness that loses an agent to a rate limit, a usage limit, a dropped connection
or a 5xx returns `null` for that agent with zero retries, filters the `null` out, and reports the
wave `completed`. Measured on one machine across three runs: 96 agents started and 35 never
returned; 128 and 50; 107 and 52.

### Why the coverage ledger exists

`M (inherited)`. From the census this rule comes from: 230 cases closed, 220 of 220 armed, 10
marked not-applicable with structural reasons, zero failures — and zero cases at a rung that asked
for an effect outside the process, because no such rung existed. Every gate was green and the
central claim had never been tested. The same census found 26 of 32 state-changing test functions
never re-read the observable afterwards, and a sweep of 7 mutating operations found 3 that returned
success while changing nothing.

### Why sharding at all

`M (incident)`. A 200-file, 25k-LoC diff reviewed in one context produced 2 of roughly 10 real
findings, because most files were never read. Single-context coverage degrades sharply past about
20 files.

### Why the cleanup angles are not decoration

`M (inherited)`. In the code-review literature the large majority of defects human reviewers raise
are evolvability findings rather than functional ones, so a reviewer emitting only bugs is emitting
a minority of what a review is for.

---

## What the predecessor contributed that this skill kept

The predecessor (`code-review` 1.3.0) is the origin of the sharding architecture, the verifier
fan-out, the suppressions file, the mitigating-controls map, the candidate and verification JSONL
schemas, the severity taxonomy and its calibration rules, the multi-instance consolidation format,
the "what the report does not contain" list, the prepush mode and its verdict set, the quality
lenses and their per-lens scope rules, and the six framework checklists.

Two things the project-specific fork had dropped are restored here:

- **`nestjs-checklist.md`** — deleted in the fork because that stack was absent from that one repo.
  A general skill cannot assume any stack's absence, so the file is back, gated on the repo profile
  rather than on path patterns, and its TypeORM/Prisma section (§10) is read against whichever ORM
  is actually installed.
- **Multi-tenancy** — the fork narrowed the predecessor's tenancy section to single-user scoping.
  `logic-bugs-checklist.md` §2 now covers both dimensions in one section, keeping the predecessor's
  cross-tenant role lookup, the trusted-tenant-header escalation, and the shared-component literal
  case including its stylesheet-fallback variant, alongside the fork's visibility-filter and
  identity-from-client items.

Also restored from the predecessor's security checklist: the raw-SQL and ORM-escape-hatch items
(Prisma `$queryRawUnsafe` and its equivalents), the NestJS CORS and `rawBody` webhook items, the
`@nestjs/jwt` algorithm pinning, and the `ValidationPipe({ whitelist, forbidNonWhitelisted })` form
of the mass-assignment fix.

**Where the two disagreed, the fork won**, and each file says so in place:

- **Three-state verify over a post-verify confidence gate.** The predecessor ran a Gate 0 that
  dropped confirmed findings below a numeric threshold. The fork replaced it with the built-in's
  three verdicts, keeping confidence only as the rule that selects what goes to a verifier. Kept, because it matches
  the built-in and because a PLAUSIBLE finding with its confirming step named is more useful to a
  developer than a dropped one.
- **Six gates over five.** Gate 6 is additive; nothing was removed.
- **The finding floor, the budget line, the agent budget and the coverage ledger** are all fork
  additions with no predecessor equivalent, and all are kept.

---

## Prompting decisions, and the guidance behind them

This skill is written to be executed by Claude Opus 5, which changes what belongs in it.

| Decision | Source |
|---|---|
| No instruction to be conservative or to report only high-severity issues | *"If your review prompt says 'only report high-severity issues' or 'be conservative,' the model may follow that instruction literally and report less; ask it to report everything and filter in a separate pass instead."* This is exactly the Find/Verify split, arrived at independently by the predecessor. |
| No verification scaffolding — no "double-check", no "verify with a subagent", no final verification step | *"Claude Opus 5 verifies its own work without being told to … instructions like these cause over-verification."* The verifier fan-out is a different agent judging a different question, which is not the same thing and stays. |
| Explicit agent caps rather than "delegate when useful" | *"give explicit guidance on which scenarios warrant delegation, or set deterministic caps on how many agents can be launched."* |
| Calm trigger language throughout — "Use X when …", never "CRITICAL: you MUST" | Current models overtrigger on aggressive phrasing; the guidance is to dial it back. |
| Explicit length calibration on the report and on subagent replies | Effort controls thinking, not visible output; written deliverables run long unless a length rule is stated. |
| Reply discipline in the shard and verifier prompt templates — no narration between tool calls | *"Claude Opus 5 narrates readily during agentic work"*, and a narrating subagent spends output tokens on text the orchestrator discards. |
| Scope stated plainly, with the diff-only rule and its four named exceptions | *"Deliver what was asked, at the scope intended"* — Opus 5 follows instructions literally and otherwise widens scope. |

---

## Deliberately not adopted

- **`ReportFindings` as the output contract.** The built-in emits through a typed tool when a
  harness flag is set. This skill does not: the tool is absent on some install paths, its entry
  shape has no severity, no consolidated multi-instance locations and no coverage ledger, and its
  contract forbids also printing the findings as text. `output-format.md` carries the full reasoning.
- **A judge panel.** See "Why one verifier".
- **Whole-repo sweeps.** The built-in licenses no repo-wide scan, and neither does this skill,
  except where a quality lens's scope rule extends it explicitly (`quality-lenses.md`).
- **A `--fix` mode.** The built-in has one. This skill is read-only on source by design, so that a
  review and an edit are two decisions rather than one.
