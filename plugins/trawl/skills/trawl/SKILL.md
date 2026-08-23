---
name: trawl
description: >-
  Evidence-grounded parallel divergent ideation for coding agents. Spawns isolated branches under a balanced frame portfolio (ordinary stakeholder, operational constraint, adversary, cross-domain mechanism, one wild seat), anchors against an explicit textbook baseline, converges with mechanism-level clustering and quality floors instead of raw scores, and boss-gates the winning pick against the baseline so the recommendation is shippable, not just novel. Use on /trawl (legacy: /adhd, "ADHD mode"), "brainstorm", "ideate", "what are my options", "widen the search", or any open-ended design, architecture, naming, API/SDK-surface, product-positioning, or fuzzy-debugging decision where multiple viable answers exist — even when the user doesn't say "brainstorm". Skip for syntax questions, lookups, bugs with a known root cause, or closed phrasing ("quick", "standard", "canonical", "textbook", "just"). Tier flags: --any (cheap), --standard, --100 (exhaustive).
---

# Trawl — cast wide, sift hard, ship the catch

The first three answers the model gives are the answers a senior engineer
gives in thirty seconds. Correct. Forgettable. Worse: they are the *same*
answers every time — when researchers over-sampled 4,000 ideas from one
aligned model, ~95% were semantic duplicates of each other. Diversity does
not come from asking again, from raising temperature, or from telling the
model to "be creative". It comes from architecture: isolated parallel
frames, explicit differentiation, and convergence rules that protect
distinct mechanisms instead of rewarding the highest average score.

This skill is that architecture. It also fixes the two known failure modes
of naive divergent ideation: recommending a dazzling idea that doesn't
solve the stated problem (defended by the baseline boss-gate), and wasting
branches on frames that don't fit the problem (defended by the frame
portfolio and apoptosis).

`references/evidence.md` holds the research grounding with citations —
read it when you need to justify or tune a mechanism, not on every run.

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It writes the frozen baseline, the frame ledger and each branch's ideas to files that later phases read back, computes every receipt number from those files, and reads each stated bound off the produced set. Other models skip it.

## Pre-flight router (run before anything else)

This skill is expensive: roughly 8–14 Agent calls at the standard tier,
5–10x a single answer. The router decides the tier; it never silently
skips the run when the user opted in.

**Step 1 — explicit invocation.** If the user typed `/trawl` (or legacy `/adhd` / "ADHD mode"), run it. `--any`, `--standard`, `--100` set the tier
directly; with no flag, default to standard. Do not second-guess an
explicit opt-in.

**Step 2 — self-judge (only when Step 1 didn't match).** Three questions:

1. **Open-ended?** Would a senior engineer give multiple viable answers,
   or is there one canonical answer? Canonical → answer directly.
2. **Stakes?** High (architecture, public API, naming a real product,
   fuzzy bug with no known root cause, schema design) → standard tier.
   Medium (real decision, low blast radius) → any% tier. Trivial →
   answer directly.
3. **Open phrasing?** "Quick", "standard", "canonical", "textbook",
   "just", "one-line" mean the user wants the direct answer. Answer
   directly, optionally appending: *"For a wider exploration under
   parallel frames with trap detection, run `/trawl <problem>`."*

**Tiers.** The output receipt states which tier ran, so a light run reads
as a deliberate choice, not a broken full run.

| Tier | Frames × yield | Convergence | ~Agent calls |
|---|---|---|---|
| **any%** | 2 × 3–5 | dedup + shortlist, no clustering pass | 3–4 |
| **standard** | 5 × 3–8 | full (cluster, floors, boss-gate, deepen 3) | 8–14 |
| **100%** | 7 × 3–8 | full + cross-cluster hybridization pass | 14–18 |

100% is reachable only by explicit ask (`--100` or stated high stakes) —
never by self-judgment, because the model's cost bias would otherwise
misroute borderline cases and stamp the result as sanctioned.

## Phase 0 — Baseline anchor (before diverging)

Write the pragmatic textbook answer inline — the 2–4 sentence answer a
competent senior engineer gives in thirty seconds — and name the
problem's **native stack** in one clause (the frameworks, tools, and
APIs the asker actually lives in: a Rails monolith means packwerk,
ActiveSupport, Sidekiq; a CLI means signals, TTYs, exit codes). Freeze
both verbatim. No Agent call; you'd produce this anyway.

The baseline does two jobs:

1. **Concrete ban list.** "The first three obvious answers are banned" is
   a phrase-level ban a model evades by rewording the same mechanism.
   Handing each branch the actual baseline text and requiring difference
   *in cause, intervention point, or assumption* makes anti-anchoring
   testable. (The measured version of this — generate, then explicitly
   differentiate — is the single strongest prompt-level diversity lever
   in the literature; see evidence.md.)
2. **Boss gate.** In Phase 3 the shortlist must beat this baseline
   head-to-head on the stated ask, or the skill openly recommends the
   baseline. This is what keeps the output shippable.
3. **Translation target.** Every idea that survives to the shortlist —
   however alien its source frame — must land back in the named stack.
   Blind judges comparing this skill's output against simpler
   alternatives consistently rewarded the version whose steps named the
   asker's actual tools; a wide exploration that ends in generic verbs
   ("instrument the boundaries") loses to a narrow one that says
   `packwerk init`.

## Phase 1 — Diverge (no critic)

**Pick frames as a portfolio, not from a menu.** Fill five seats
(two at any%: one grounded seat + the wild seat):

1. **Ordinary stakeholder** — a concrete occupational persona who lives
   with the consequences (night-shift support lead, legacy-system
   maintainer, accessibility tester, bootstrapped founder). Research
   finding: one-sentence *ordinary* personas partition knowledge better
   than celebrity or exotic ones.
2. **Operational constraint** — an extreme that breaks anchoring
   ($0/1-hour, no-network, provable-only, single-file).
3. **Adversary / inversion** — attacker, hostile competitor, or "how do
   we guarantee NOT-goal" inverted back.
4. **Cross-domain mechanism** — biology, logistics, markets, game design,
   speedrunning. The branch must extract a *named mechanism*, map it onto
   the problem, and state where the analogy breaks — this is what
   separates a transplant from a decorative metaphor.
5. **Wild seat** — one deliberately unfit-looking frame, exempt from any
   fit judgment. Occasionally this seat produces the reframe precisely
   because it looks wrong.

Compose bespoke frames freely from the template in
`references/frames.md` (domain-adjacent expert × temperament × constraint
style) — frames need not come from a fixed table. Before spawning, run
the **fit floor** on seats 1–4: the frame must have a nameable mechanism
that bites on this problem and a plausible route from its vocabulary back
to an action. The floor removes catastrophic mismatches only — it is not
a ranking, and the wild seat never faces it. A child's perspective on a
memory allocator fails the floor; the same perspective on onboarding UX
passes. `references/frames.md` has the full rubric, a persona catalog,
and worked examples.

**Spawn one Agent per frame, in parallel, isolated.** Each Agent gets
only: the problem, user context, its frame's vantage prompt, the frozen
baseline, and this instruction:

> You are in DIVERGENT mode — a generator, not a critic. First,
> privately note the default mechanisms in this baseline: [baseline].
> Then generate your ideas in one batch: at least 3, at most 8. Stop when
> your next idea would be a reworded sibling of one you already have —
> idea count is signal, not quota. Every idea must differ from the
> baseline in cause, intervention point, or assumption — say which.
> Then take a second pass over your own list and rewrite it to be bolder
> and more different; no two ideas may share a mechanism.
> Do not rank. Do not hedge. For each idea you may state one assumption
> and what would falsify it.
> Output a JSON array only:
> `[{"idea": "...", "mechanism": "...", "differs_from_baseline": "...", "assumption": "..."}, ...]`

The batch-then-differentiate second pass is load-bearing: it is the
best-measured diversity technique available (pooled similarity dropped
to near human-group levels in the benchmark that tested 35 strategies).

**Isolation invariant.** Branches run in parallel and never see each
other. Do not serialize. Do not share intermediate ideas between
branches, and do not feed one branch's output to another "for
inspiration" — the two intuitively-appealing versions of that (showing
similarity feedback, seeding with earlier top ideas) both *measurably
reduced* diversity in controlled tests. Anchoring is the disease this
skill treats; don't reintroduce it mid-flight.

## Phase 2 — Converge (critic on)

Work in this order; each step defends against a documented failure.

1. **Dedup by mechanism.** Two ideas with different wording and the same
   causal mechanism are one idea. Merge them, keeping the strongest
   phrasing. Lexical difference is not diversity.

2. **Cluster by underlying angle** (3–6 clusters), labeled by the play:
   "remove-the-server plays", "cache-shaped plays". Clustering is what
   makes the wide set readable and what the shortlist diversity rule
   operates on.

3. **Gate, don't score.** Direct 1–10 scoring by an LLM collapses toward
   the middle and does not model the novelty–feasibility tension (judges
   rate them independently; humans trade them off). So: apply pass/fail
   **floors** — soundness (the mechanism plausibly produces the claimed
   effect), feasibility (a small team could validate a first version),
   fit (it addresses the *stated* ask, not an adjacent one). Ideas below
   any floor are out. Novelty is never a floor and never rescues a
   floor failure.

4. **Flag traps with mechanisms.** A trap is an attractive idea that
   fails for a nameable reason (hidden cost, false economy, won't scale,
   premature abstraction). Every trap flag must cite the concrete failure
   mechanism — "sounds too exciting" is a tone judgment, not a trap.

5. **Shortlist for coverage, not average score.** Take the best surviving
   idea from each cluster, then pick 3 (2 at any%) that are maximally
   mutually different in mechanism. Never let two shortlist slots share a
   cluster — three variants of the strongest idea is convergence wearing
   a costume. When ranking within a cluster, compare pairwise (A vs B,
   then B v A; an unstable verdict is a tie) rather than assigning
   absolute numbers. One slot belongs to the most **non-obvious**
   floor-passing idea, explicitly marked — a shortlist of three safe
   cluster winners has quietly re-converged on the middle, which defeats
   the run's purpose.

6. **Apoptosis.** A frame whose entire yield failed the floors is dropped
   from the rendered output — its ideas go to a one-line note in the
   receipt ("frame X apoptosed: best idea failed feasibility"), not next
   to a serious problem where a silly persona reads as noise. Judge the
   output, never the persona: a wild frame that produced one strong idea
   survives in full.

`references/convergence.md` has judge-bias defenses (order-swapping,
blinding frame names before comparison, cross-model judging when the
CLI/library is in play) and the full floor rubrics.

## Phase 3 — Boss gate, then deepen

**Boss gate.** For each shortlist idea, run a blind head-to-head against
the frozen baseline: present both as unlabeled Option A / Option B
(randomize which is which), judged *only* on the stated ask — correctness
on the core problem, effort-to-ship, risk. Novelty is excluded; it was
already required to reach this point. Verdicts: BEATS / TIES / LOSES.

- The ★ recommendation must carry BEATS (high stakes) or at least TIE
  (exploratory asks — don't neuter playful sessions).
- If every shortlist idea LOSES, say so plainly and recommend the
  baseline, with the shortlist demoted to "worth exploring later". This
  is the honest outcome the previous generation of this skill couldn't
  produce, and it is the fix for the one benchmark loss it recorded.
- On a LOSS, optionally spawn one hybrid attempt: graft the finalist's
  single most interesting mechanism onto the baseline and re-gate. The
  hybrid is often the actually shippable winner.

**Deepen** one winner per shortlist cluster (one Agent call each):

> You are in FOCUS mode. Sketch how this idea actually works in 4–8
> sentences. Name the load-bearing risk. Name the first concrete step as
> a same-week starter in the problem's own toolchain, naming the actual
> tools, commands, or APIs (a Rails problem gets a packwerk or
> ActiveSupport::Notifications step, not "instrument the boundaries").
> Then 3–5 child ideas (variations, hybrids, unlocks). Output JSON only.

**100% tier only — hybridization pass.** One extra Agent takes the top
idea from each of the two most distant clusters and force-merges them
into 2–3 hybrids neither frame could reach alone. Pools generated under
different prompts overlap little — recombination is where the extra
tier's value lives.

## Output shape

Render in this order. Structure is half the value; do not collapse into
prose. And density is the other half: blind judges comparing runs of
this skill against plain answers read apparatus as dilution — "wrapped
in ceremony that doesn't improve cut quality" was a real verdict. The
brief and converge sections together must work as a standalone answer:
a reader who stops there gets the recommendation, why it wins on their
stated ask, and the first concrete step. Chips and receipts are one
line each; everything else earns its length or gets cut.

0. **Receipt** — one line: tier, frames spawned/returned, ideas
   generated/merged/floored, apoptosed frames, baseline verdict summary.
   Example: `Trawl standard — 5 frames, 27 ideas → 19 after merge, 4
   floored, 1 frame apoptosed (10-year-old: all ideas failed fit).
   ★ BEATS baseline. Upgrade: /trawl --100`.
1. **Brief** — the problem in one line, any reframe, and the frozen
   baseline in 2–4 sentences, labeled as such.
2. **Wide set** — every surviving idea, grouped by cluster, one phrase
   each, cluster labels naming the angle.
3. **Converge** — the shortlist with a one-line why each, its
   vs-baseline verdict chip (BEATS/TIES/LOSES), ★ on the recommended
   pick, and the non-obvious slot marked. The ★ pick's line states why
   it wins *on the stated ask* and its first step in the named stack —
   this section plus the Brief must stand alone as the answer.
   Traps listed separately, each with its failure mechanism.
4. **Focus** — the deepened winners: sketch, load-bearing risk, first
   concrete step, children.
5. **Provocation** — one wildcard question that opens a direction the
   run didn't take.

## Anti-patterns

- **Convergence disguised as divergence.** Ten variations of one
  mechanism is decoration, not breadth. The mechanism-dedup step exists
  because this is the default failure.
- **Sharing between branches mid-flight.** Feels collaborative; measured
  effect is homogenization. Pool only at the end.
- **Novelty worship.** LLM-judged novelty correlates *negatively* with
  ideas that survive contact with execution. Feasibility floors and the
  boss gate outrank novelty chips, always.
- **The boring-machine failure.** The boss gate judges "solves the
  stated ask with an articulable edge", not "which would a cautious
  senior ship". If every run ends in the baseline winning, the gate is
  miscalibrated — recheck against `references/convergence.md`.
- **Padding to quota.** Variable yield means a dry frame returns 3 ideas
  honestly. A frame returning filler to look productive dilutes scoring
  attention downstream.
- **Ceremony mistaken for value.** Receipts, chips, and verdicts serve
  audit and trust; they are one line each and never the show. If the
  wide set's framing, the frame names, or the apparatus outweigh the
  ideas, a blind reader scores the run as diluted — because it is.
- **Refusing to commit.** "Here are 20 ideas, you decide" is a cop-out.
  Converge with a real opinion and a named recommendation.

## Cost

any% ≈ 3–4 Agent calls. Standard ≈ 8–14. 100% ≈ 14–18. Not for every
keystroke — for decision points where the obvious answer being wrong is
expensive. The receipt makes the spend auditable after the fact.

## Companion history

This skill supersedes the original `adhd` skill (github.com/uditakhourii/adhd),
which validated the two-phase isolated-branch loop against single-shot
baselines (5W/1L on six problems). The changes here — baseline anchor and
boss gate, frame portfolio with fit floor and apoptosis, mechanism-level
convergence with floors instead of scores, tiers and receipts — each trace
to a documented failure mode or a measured result; `references/evidence.md`
carries the citations.
