# Evidence — where every structural rule in this pipeline came from

Every load-bearing design decision in these plugins traces to a measured result, a documented
failure, or a dated incident. This file is the map. Read it before changing a rule — several
numbers are conservative defaults rather than measured optima, and the file says which; a rule
swapped without knowing which kind it was is how a pipeline drifts away from its evidence.

## The corpus

Four evidence streams, merged in August 2026:

1. **A four-backend Dossier deep-research panel** (run 2026-08-15, ~$9.70): OpenAI gpt-5.6-terra
   (62 sources), Google Gemini (37), Perplexity sonar-deep-research (19), xAI grok-4.3 (10).
   Full reports + source registries committed in `docs/deep-research/`. Citation verification:
   fabrication check **PASS** on both load-bearing reports (0 fabricated of 99 checked; blocks
   were bot-walls, not dead links). The Gemini member leans on weaker sourcing (social posts,
   ResearchGate mirrors) and one of its claims resolves to nothing ("Playwright MCP has emerged
   as the standard") — it is retained because discarding a member silently would misrepresent
   the panel, and its weak claims are marked held-loosely below.
2. **The WEB-4905 audit corpus**: 110 tickets, 1,454 requirements, **46% delivered as
   specified** while every completion note read as complete — and the improvement analysis
   written against it (`~/Dev/dAIolog/docs/reviews/pipeline-skills-improvement-analysis.md`),
   whose R1–R10 were applied to the predecessor pipelines and are carried forward here as the
   floor.
3. **The predecessor skills' own incident ledger** — thirty dated, incident-backed operating
   rules mined from the diolog fleet runs (preserved verbatim in
   `references/operational-rules.md`) plus the session-transcript trawl (stalled fleets, lost
   agents, worktree collisions, lane outages).
4. **Third-party method sources, credited**: Matt Pocock's skills library
   (github.com/mattpocock/skills, MIT) — fog-of-war deferral, the facts/decisions split,
   tracer-bullet slices, seam-agreed testing, the two-axis review; the Vercel Labs
   eve-software-factory-template (MIT) — the acceptance-criteria contract graded with evidence,
   physical verifier isolation, thread-as-ledger crash-safe counters; and the `clarify:clarify` skill's
   evidence corpus for the decision gate.

## Rule-by-rule sourcing

### The deterministic state machine with artifact-gated transitions
All four panel members converged: agents propose, the state machine advances; a stage is
complete only when its artifact exists (OpenAI report; MAST — arXiv:2503.13657, 1,642 traces,
κ=0.88: 44% of multi-agent failures are system-design, 24% task-verification). The predecessor
gap was concrete: no terminal state, no failure state, `Todo` overloaded, `In Progress` never
written — four of the tasks-pipeline intake's top findings. **Held firmly.**

### Cross-family verification (VERIFIER ∉ writer's family)
Anthropic's Petri observed GPT-5 judges rating GPT-5-family targets more leniently; a
pre-registered 2026 re-grade measured a 17.6-point same-family inflation (Reddit-published,
single case — **held loosely**, direction consistent across every panel member); the WEB-4905
central finding was author-graded acceptance. The eve template states the rule three times
("a different model doesn't share the implementer's idiom or blind spots") and its one design
error — a frontier implementer under a cheap reviewer — is inverted here (REVIEWER ≥ WRITER).
The ordered lane set (not one vendor) fixes the predecessor's single-thread independence layer
(weakness A1). **Held firmly; the magnitude, loosely.**

### Panels only at high-leverage gates, blind, position-swapped, structural verdicts
PoLL (arXiv:2404.18796): diverse panels beat a single frontier judge across six datasets at
~1/7th the cost. Shi et al. (arXiv:2406.07791, ~100k instances): non-random position bias.
Zhou et al. (arXiv:2409.16788): verbosity bias. MAST: more agents ≠ better — coordination is a
failure source, which is why panels are reserved for forks, never routine edits. **Held firmly.**

### The decision gate (assume-don't-ask, divergence test, second-opinion lanes)
ClarifyGPT (Mu et al., FSE 2024): ask-on-divergence lifted GPT-4 from 70.96% → 80.80%
(p = 3.2e-05). Ambig-SWE (ICLR 2026): told plainly to ask when unsure, a frontier model asked on
93–95% of already-fully-specified issues — encouragement produces indiscriminate asking, which
is why the gate is tests, not exhortation. Ask-or-Assume (arXiv:2603.26233): where the agent
correctly declined to ask, outcomes matched the no-information baseline — correct restraint
looks like nothing. The lane commands and their verification greps are inherited from `clarify`
(verified working) and extended to agy/grok with probe-before-use caveats. **Held firmly.**

### Assumption records with confidence, alternative-beaten, falsifier, blast radius
The OpenAI panel's assumption-resolution order; the "assuming X (rather than Y)" rule from the
predecessor sentinel (the anti-silent-narrowing device); wayfinder's fog-or-ticket test ("can
you state the question precisely now") for what may be deferred at all. **Held firmly.**

### Typed evidence, no partial status, the blocker protocol, caveat propagation
Directly from WEB-4905: every behavioural obligation had a prose escape hatch and the escape was
exercised ("record as unverified" → recorded and shipped); `file:line` was the only admissible
evidence class, so the cheapest kind won; ⚠ rows passed a disjunctive gate literally; merge
comments laundered hedges. R2/R4 revoked those licenses; this pipeline states them as
conjunctions over checkable artifacts. The Obscura longhand-not-shorthand measurement rule is a
dated local measurement (2026-08-13). **Held firmly — these are the 46%'s direct fixes.**

### Fail-to-pass tests, the state matrix, anti-vanity discipline
SWE-bench correctness study (arXiv:2503.15223): 7.8% of "solved" patches fail developer tests.
Meta TestGen-LLM (arXiv:2402.09171): 75% built / 57% stable / 25% added coverage — AI tests are
candidates, not proof. Patch-assessment study (PMC11269383): median 77% line coverage, median
21% mutation score — coverage percentage is vanity. Berkeley RDI: every audited SWE-bench-family
harness was reward-hackable to ~100%. The state matrix is the OpenAI panel's UI table merged
with the design stage's coverage bar; the three test anti-patterns and seam discipline are
Pocock's tdd skill, credited. **Held firmly.**

### The design stage and its review gates
The predecessor's largest unguarded seam (weakness A3/A4: the artifact every stage cites as UI
truth had no reviewer, no completeness gate). Field evidence from the trawl: design-stage user
rejections happened *despite* design skills being invoked — invoking is not gating — and
be-my-witness over-flags without scoping (dated commit). Platform routing (mac-design-studio;
web mirrors mac; Windows 11 pass) is operator policy, not measured — **held as policy.**

### Ledger/artifact memory, thread-as-ledger counters, idempotent comments
Stigmergy over conversational handoff (Gemini + Perplexity panels; practitioner reports of
compaction losing the *reasoning*); the eve template's crash-safe comment counter (post intent
before attempting); the predecessor incident "verdicts written outside git were lost entirely."
**Held firmly.**

### Fleet mechanics: global agent budget, verified runner lane, scripted completion
The ≤4-wave cap and the 8-slot fleet multiplied into the same rate limiter (weakness F1 — now
one budget). `agent()` null-returns reporting `completed`, the empty-`Promise.race` hang, the
runner model override not sticking — all dated incidents in `operational-rules.md`.
`check_completion.sh` mechanises the armada's completion rule because the prose version was its
most safety-critical unscripted check. **Held firmly.**

### Numbers held loosely (change with fresh measurement, not by vibe)
- The ≤4 concurrent wave cap and ~16 global budget: rate-limiter observations, not tuned optima.
- The 1-in-3 executor revert kill-switch: a judgement threshold.
- The 3-round gap-fix park: convergence heuristic.
- Executor lane order (agy > grok > codex-terra): **superseded 2026-08-22.** It was a
  throughput-preference policy from field use, and the re-sweep it asked for arrived — `defer`'s
  capability matrix, 106 tasks with opus as the reference. Against the best lane available per
  work shape the fixed order cost 16 points on average, 54 on a from-scratch page and 38 on
  regression-sensitive work, and its first choice grades RED on five of eleven shapes. The
  throughput premise did not hold either: per whole task gemini runs 4.0 minutes against
  `gpt-5.6-terra@medium`'s 2.2, at half the cost. The order was right on the three shapes it was
  tuned against and expensive elsewhere. Lane choice is now per-shape (`executor-lanes.md`); the
  compaction override and the Claude fail-back are unchanged, because the bench scores one
  bounded task per run and can see neither.
- The 17.6pp same-family inflation and the Theoria/Cooperative-Sabotage figures (Gemini panel):
  single weakly-sourced cases; the direction informs, the numbers do not gate anything.

## What was deliberately not changed
The non-technical comment discipline, the sentinel lenses, plan-tier anti-padding,
model-and-effort §6/§7 (oracle-vs-re-read; length budgets), the codex opt-out/egress machinery,
and gap-fix's two-consecutive-dry-audits exit — per WEB-4905 §7 ("What NOT to change"), each is
either load-bearing for the human loop or paid-for scar tissue. The reconciliation of work's
single re-audit vs gap-fix's double-dry loop is now stated where both live: work has the critic
and the front-loaded checklist; gap-fix is the belt-and-braces finisher.
