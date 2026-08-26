# Evidence

Every structural rule in this skill traces to a row here. Four independent
research backends were commissioned on the same question (Dossier panel
`dr_1b861aa96bc059c8`, 2026-08-26); their full reports are committed under
`docs/deep-research/`. Support is counted in independent **families**, not in
how many pages agree.

| Backend | Model | Sources | Cost | Report |
|---|---|---|---|---|
| Gemini Deep Research | `deep-research-preview-04-2026` | 49 | $3.00 | `panel-01-gemini-llm-architectures.md` |
| Perplexity Sonar Deep Research | sonar-deep-research | 19 | $2.00 | `panel-02-perplexity-cognitive-science.md` |
| xAI | `grok-4.3` | 11 | $1.20 | `panel-03-xai-pedagogical-architectures.md` |
| Claude Code (free lane) | Claude Code | 6 | $0.00 | `panel-04-claude-empirical-constraints.md` |
| Antigravity CLI | — | — | $0.00 | **died at startup**, version probe refused the binary. Recorded, not chased. |

Citation verification ran on the two load-bearing reports.
**Gemini: 49 checked, 0 fabricated, 0 dead links** (39 opened directly; 7 bot-walled, 3 timed out).
**Perplexity: 19 checked, 0 fabricated, 0 dead links** (8 opened directly; 7 more confirmed
registered by DOI behind publisher 403s). A resolving URL is not proof the source supports the
claim, which is why the convergence column below counts families rather than links.

---

## 1. Findings that became rules

### 1.1 Analogy must map relations, and must state where it stops
**Convergence: 4 of 4 families.** Gentner's structure-mapping theory holds that analogy aligns
*relational systems*, not object attributes, governed by the systematicity principle: prefer
deeply interconnected higher-order relations over isolated surface similarities. Misconceptions
arise when non-alignable attributes get projected from base to target.

The failure is not hypothetical and it is durable. Perplexity's review of analogy competence in
science teaching (Eriksson) calls analogies "double-edged swords" whose induced misconceptions
are hard to detect and harder to correct; misconceptions formed this way are "robust and
resistant to change." The named mitigations are the same across families: identify the
correspondences up front, and produce an explicit *limits of the analogy* segment.

→ Rules: the **Boundary Card is mandatory**, it names what does *not* map, and per §1.6 it is
never buried below tier 2.

### 1.2 One analogy is a trap; the reductive bias needs a second lens
**Convergence: 3 of 4 families** (xAI, Claude, Perplexity). Spiro, Feltovich and Coulson's
cognitive flexibility theory holds that in complex ill-structured domains a single analogy
collapses non-linear, multi-factorial systems into static single-cause models. The mitigation
named in all three: multi-analogy ensembles that "criss-cross the conceptual landscape", plus
explicit boundary charting per analogy. Perplexity adds that *far* analogies — fewer surface
similarities, real structural correspondence — reduce overinterpretation.

→ Rule: any topic with more than one mechanism gets a **second, structurally different lens**,
not a restatement of the first.

### 1.3 Interactivity is worth little without a prediction
**Convergence: 2 of 4 families** (Claude carries the numbers, xAI corroborates the mechanism via
PhET's predict-run-investigate cycles). Chi's ICAP framework grades engagement Passive → Active →
Constructive → Interactive. Dragging a slider is merely *Active*: d ≈ 0.20–0.40 over passive.
Formulating a hypothesis first is *Constructive*: d ≈ 0.40–0.60 over active.

This is the highest-leverage finding in the corpus, and it is the one an explainer skill most
reliably misses. A slider that merely responds is close to decorative. A slider the reader has
committed a guess against is a learning instrument.

→ Rule: every interactive artifact carries at least one **Predict-Observe-Explain beat** — the
reader commits before the reveal.

### 1.4 An open sandbox fails novices
**Convergence: 2 of 4 families** (Claude, xAI). Kirschner, Sweller and Clark (2006): unguided
exploration of complex domains overloads novices, who then tinker unsystematically without
forming causal models. The mitigation is *faded guidance* — lock advanced parameters early,
unlock them once the reader has been through the guided beats.

→ Rule: **one live variable in tier 1.** Multi-parameter sandboxes are tier 3 or absent.

### 1.5 The same scaffolding that helps novices harms experts
**Source: Claude (Kalyuga, Chandler & Sweller, 1998/2003), 1 family, uncontested.** The expertise
reversal effect: scaffolds that lift novices measurably impede experts (d < 0).

→ Rule: a **skip-ahead control** is required. Nobody is forced through tier 1 to reach tier 3.
Held at one-family support; it is cheap to honour and costs nothing if wrong.

### 1.6 Progressive disclosure works, and shallow beats deep
**Convergence: 4 of 4 families** on the principle; **Perplexity alone** on the depth cap, which is
the part that changes what gets built. UX research warns that nested disclosure buries
functionality users then never find; a single secondary layer usually suffices, and extra
complexity should be handled by *combining* patterns rather than deepening the hierarchy. The
concrete recommendation is roughly three levels — intuitive story, simplified mechanism, formal
detail — with tabs or toggles rather than nested expanders. And explicitly: essential caveats,
"for example, where an analogy breaks down", must be reachable within the first or second layer.

→ Rules: **exactly three tiers, no nesting**, and the Boundary Card sits at tier 1 or 2.

### 1.7 The measurable multimedia levers, with their effect sizes
**Source: Claude, corroborated in principle by Perplexity and Gemini.** Mayer's CTML
meta-analyses give this skill its layout constraints rather than taste:

| Principle | Effect | What it forbids |
|---|---|---|
| Spatial contiguity | d = 0.72–1.19 | Labels and readouts in a separate card from the diagram |
| Segmenting | d = 0.79–0.98 | One continuous animation instead of reader-paced steps |
| Coherence / seductive detail | d = 0.65–0.86 | Decorative art, background particles, ambient motion |
| Signaling | g = 0.46–0.53 | Unhighlighted state transitions |

→ Rules: readouts live **inside or adjacent to the diagram**; every mark must encode a real
variable; state changes are signalled.

### 1.8 Animation is transient, and transience is the defect
**Source: Claude (Tversky, Morrison & Bétrancourt, 2002).** Animations often fail to beat static
graphics because they are fleeting — the reader cannot hold the intermediate states. They succeed
when the learner controls playback and can inspect stationary intermediate stages. Perplexity's
meta-analytic read is more favourable to animation overall but agrees the advantage comes from
information volume, "which can be a liability if not well managed", and that realistic detail only
helps high-visuospatial learners.

→ Rule: **no autoplay-only motion.** Every animation is steppable and inspectable at rest.

### 1.9 LLMs hallucinate coordinates, and cannot see the result
**Convergence: 2 of 4 families** (Gemini carries it in depth, Claude names the same defect class).
Models process `120` as the subword tokens `["1","2","0"]` co-occurring in training data, not as a
point in a plane, so raw SVG path emission is statistical prediction rather than geometric
placement — the HiVG work documents severe token redundancy and warped output. Compounding it,
SVG-generating models are trained against a *text* target and never render their output, so
syntactically perfect XML routinely draws overlapping boxes, labels past borders and arrows
through text. Gemini names this **open-loop visual blindness**.

The mitigation with evidence behind it is the **Drawing-with-Thought** paradigm (Reason-SVG): force
explicit design rationale before any code — concept sketch, canvas plan, shape decomposition,
coordinate calculation against a stated bounding box, styling, then assembly with z-order resolved.

→ Rules: `references/artifact-engineering.md` carries the **geometry contract** — declare the
viewBox and the grid, place every element against a named band, before emitting markup.

### 1.10 The rendering failure modes are specific and checkable
**Source: Claude, with Gemini corroborating the CSP half.** Four named defects: hardcoded pixel
widths instead of a `viewBox` (clipping inside constrained panels); pointer loss on touch drags
without `setPointerCapture` and `touch-action: none`; unbounded `requestAnimationFrame` loops
leaking CPU and desynchronising state; and CDN race conditions. Gemini adds that sandboxed artifact
runtimes whitelist CDNs aggressively — a library pulled from an unapproved host **fails silently**.

→ Rules: all five are enforced mechanically by `scripts/lint_explainer.py`, which exits non-zero.

### 1.11 "Explain like I'm 5" degrades into baby-talk
**Source: Claude, explicitly; Gemini corroborates the direction of travel.** ELI5 prompts in
foundation models "frequently degrade into condescending baby-talk, superficial metaphors, or
visual truncation." Gemini records the field moving from "simplistic explain-like-I-am-5
directives (which produced childish prose) to structured multi-tier conceptual models."

Claude's anti-pattern table is the operational form: *"Imagine a little hungry monster eating
cookies inside your computer RAM"* against *"Think of computer memory like a grid of numbered
postal lockers that can each hold one letter."* Same reading age. One of them is true.

**Measured here, 2026-08-26.** Running the original skill six times against hard topics produced
the failure in 4 of 6 artifacts, and the markers are specific enough to detect: *"Grown-up word:
DNS"*, *"grown-ups call the boss the leader"*, *"the magic rule"*, *"it gets the crown"*, *"a
little timer goes ding"*. Naming a mechanism "magic" is worth noting on its own, since it is the
exact inverse of explaining it.

→ Rule: the **register is a brilliant colleague from another field**, and the linter carries a
baby-talk lexicon built from those measured markers rather than from imagination.

*Provenance caveat:* that lexicon was strengthened **after** measuring the baseline, so the rule is
fitted to observed output. `EVALS.md` records this, and the blind panel — which never sees the
linter — is what carries the neutral half of the comparison.

### 1.12 Simplification can leave the reader worse off than ignorance
**Source: Perplexity.** Removing mechanism without signalling that it was removed produces the
illusion of explanatory depth: readers believe they understand more than they do, which "can hinder
further learning and lead to inappropriate application." The mitigation is to mark epistemic status
in the text itself — "in this simplified picture", "this analogy helps with one aspect but not
others" — and to offer the path to the fuller account.

→ Rule: **tier 3 states what it is still leaving out.**

---

## 2. Held loosely — where the panel disagreed

These are recorded rather than resolved. Each is a real fork with evidence on both sides.

**2.1 Direct SVG generation against deterministic layout engines.** Gemini presents both camps:
fine-tuned direct generation (LLM4SVG) against the pragmatist position that a model without a
visual cortex cannot do collision detection or edge routing and should emit node/edge JSON to
Dagre or similar. *This skill takes the first path and mitigates it*, because a single-file
zero-dependency artifact has no layout engine available to hand off to — the CSP that makes the
artifact portable is the same constraint that removes the alternative. The geometry contract in
`artifact-engineering.md` is the mitigation, and it is not a claim that the fork is settled.

**2.2 DSL fragility against framework token bloat.** Gemini records unresolved disagreement:
Mermaid and similar DSLs delegate layout safely but fail hard on one stray character, crashing the
artifact silently, while React components survive component-level failure through error boundaries
at much higher token cost. Neither side has production reliability metrics. This skill emits
hand-built inline SVG, which sits outside both, and inherits §1.9's risk rather than either of
these.

**2.3 Animation against static graphics.** §1.8 above. Perplexity's meta-analysis finds a moderate
overall advantage for animation; Claude cites Tversky et al. finding animations frequently fail on
transience. Both agree on the resolution — learner-controlled playback — so the rule is safe even
though the underlying question is not settled.

**2.4 How fast to fade scaffolding.** Claude records this as explicitly conflicting across CLT and
constructionist literature, varying by domain between discrete algorithmic logic and continuous
physics. This skill fixes three tiers by fiat and offers the skip control; that is a defensible
default, not a finding.

---

## 3. What nobody could tell us

The panel converged on the same gaps, which bound what this skill may claim.

- **No large-scale trials of AI-generated explainers.** xAI and Claude both flag the absence of
  randomised trials measuring learning gains, misconception rates or retention from AI-generated
  against human-crafted interactive artifacts. Every effect size quoted in §1.3 and §1.7 comes from
  human-authored instructional material. They justify the design; they do not predict this skill's
  output.
- **No optimal counts.** xAI: no quantitative basis for the right number of disclosure layers or
  analogies per domain. The three-tier rule is §1.6's UX evidence plus a decision, and §2.4 says so.
- **No context-saturation thresholds.** Gemini: the token point at which spatial consistency
  degrades in multi-turn SVG work is unmeasured across models.
- **No cost or latency benchmarks** for explainer architectures at all (Perplexity returned
  `MISSING_DATA` for every engineering cell in its comparison table rather than estimating).
