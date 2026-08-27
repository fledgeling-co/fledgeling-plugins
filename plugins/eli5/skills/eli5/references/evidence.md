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

---

## 4. Measured in this repo, 27 Aug 2026

Section 1 is the research panel. This section is local measurement, and it is what the
`composition` family of the gate and the library recipes in `artifact-engineering.md` rest
on. Where a rule here has no panel source, it says so.

### 4.1 One mandated architecture produced three indistinguishable artifacts

Three explainers built by version 0.1.0 in `~/Dev/dAIolog/docs/warrant-web/`, plus the
skill's own bundled `evals/sample-artifact.html`:

| Artifact | Prose words | Visual scenes | Template phrases reused |
|---|---|---|---|
| `done-to-verified.html` | 1,024 | 3 | 10 |
| `what-changed-in-done.html` | 1,293 | 3 | 9 |
| `what-the-agents-are-doing.html` | 1,636 | 4 | 9 |
| `evals/sample-artifact.html` | 1,822 | 3 | 7 |

All three warrant-web pages opened with the same four headings in the same order, under the
same three-tab strip. Every phrase counted above came from the skill's own worked examples,
which were illustrations rather than rules — the model copied them because they were the only
concrete shapes in the file.

→ Rules: `references/forms.md` replaces the single architecture with eight precedents rather
than a specification; the gate's `no-template-boilerplate` fails at three or more copied
phrases; the composition budgets in §4.5 count words outside `<svg>` and `<canvas>`, so a
sentence moved onto the thing it explains costs nothing and satisfies spatial contiguity at
the same time (§1.7).

Anthropic's published frontend guidance names the same failure and is the source for the
identity pass: *"You tend to converge toward generic, 'on distribution' outputs… You still
tend to converge on common choices across generations. Avoid this."* It also states that
*"animations and interactive elements should be requested explicitly when desired"*, which
is why the interaction floor is a count rather than an encouragement.

### 4.2 A vendored library breaks the containment scan unless it is marked

Three.js r169 contains 3 `fetch(` calls, 2 `requestAnimationFrame` and 1
`cancelAnimationFrame`. Inlined without a marker it fails `no-network-calls` on every artifact
that uses it, measured against version 0.1.0 of the gate.

→ Rule: vendor blocks carry `data-vendor`, and the containment, animation-frame and
word-count scans read author code only.

### 4.3 Only a single-file Three.js build inlines

Measured in Chromium from `file://`. The split r17x pair (`three.module.min.js` re-exporting
`./three.core.min.js`) fails two ways, both silent to a reader:

| Route | Result |
|---|---|
| Inlined directly, split build | `Access to script at 'file:///…/three.core.min.js' … blocked by CORS policy` |
| Importmap `data:` URL, split build | `Failed to resolve module specifier "./three.core.min.js". Invalid relative url or base scheme isn't hierarchical.` |
| Export list rewritten to `const THREE`, single-file r169 | renders; `THREE.REVISION` reads `169`, WebGL context live |
| Importmap `data:` URL, single-file r169 | renders; 917 KB against 687 KB |

GSAP 3.13.0 inlines unchanged as a classic script: `gsap.to('#box',{x:120})` lands
`matrix(1, 0, 0, 1, 120, 0)`.

→ Rules: `scripts/vendor_lib.py` refuses a split build rather than emitting one that
half-works, and the export-rewrite route is the default.

### 4.4 The rebuilt gate, checked against its own inputs

`scripts/lint_explainer.py --self-test`: 29 of 29 rules proved able to fail against broken
fixtures, with the reference fixture passing all 29. §4.7 adds a thirtieth.

Two gate defects were found by running it rather than by reading it. `motion-steppable`
searched the whole page for the word `step`, so the prose *"each step moves one packet"*
satisfied a rule about controls; it now reads the control markup only. `boundary-reachable`
divided by the length of the raw HTML, so a 690 KB inlined library put every boundary at 1%
and the rule could no longer fire; it now measures against markup with scripts and styles
removed.

### 4.5 Total prose was the wrong measure on its own

A reference artifact built to the first cut of these rules — Solid form, Three.js inlined,
gimbal lock — passed at 367 words and was still read as wordy. Broken down, three blocks
carried 159 of the 367:

| Block | Words | Read as |
|---|---|---|
| What the account leaves out | 73 | a passage |
| The analogy boundary | 48 | a passage |
| How the middle ring carries the outer axis | 38 | a passage |
| Two figure captions | 14, 17 | captions, unremarked |

→ Rules: `prose-budget` fails above 350 and warns above 250; a new `prose-block` fails a
single text block above 50 and warns above 35; `prose-run` fails above 120; `opening-budget`
fails above 90; `visual-density` warns past 110 words per scene.

Rebuilt against them, the same artifact runs **188 words with no block over 25** and passes
29 of 29. The cuts were structural rather than compression: the leaves-out paragraph became
three list items, two explanatory sentences moved inside the SVG as annotations, and the
boundary lost half its length without losing its claim.

### 4.6 The gate cannot see a collision, and did not

At 90° of pitch in that rebuild, the yaw and roll axis labels landed on the same anchor and
drew on top of each other. Every one of the 29 checks passed. This is §1.9 exactly — the
markup was valid and the geometry was wrong — and it is why the skill's last step is to open
the file and look. The fix collapses the two labels into one below 12° of separation.

### 4.7 The gate could not see the failure the skill is named for

`done-to-verified.html`, rebuilt with 0.2.0, passed 24 of 24 checks at 200 words of prose,
no block over 28, three visual scenes, four interaction kinds. It was unreadable to anybody
outside the project it describes.

What shipped: *"193 of 200 cards carry evidence that bites. Verified is a different axis."*
and *"which classes to add, each one's oracle, and the closure count with its window."* The
terms *card*, *class*, *rung*, *oracle*, *assay*, *closure*, *escape* and *coverage* are
ordinary English words carrying private meanings, which is the hardest jargon to notice
because none of it looks technical. The page defined none of them.

Two measurements decided how to gate this.

**Readability metrics do not separate the two cases.** The unreadable artifact and a
readable one built the same day:

| | mean sentence | sentences ≤ 8 words | terms defined |
|---|---|---|---|
| `done-to-verified.html` | 8.0 words | 66% | 0 |
| gimbal reference | 8.5 words | 59% | 0 |

A sentence-length or short-sentence rule would fire identically on both, so the gate does not
carry one.

**Both pages defined nothing.** That is the signal, and it is checkable. `defines-its-terms`
fails on zero `<dfn>`, fails on a term used before its definition, and warns below three.

**The 0.2.0 prose budgets caused part of this.** Capping the page at 350 words and any block
at 50 pushed compression rather than cutting, and compressing a hard idea produces the
aphorism register — a conclusion with the mechanism removed. Text inside `<dfn>` is now
exempt from both budgets, exactly as text inside `<svg>` is, so defining a term costs the
author nothing and there is no incentive to compress instead.

→ Rules: the reader is named in SKILL.md as a curious sixteen-year-old or a sharp adult who
has never worked on this; every topic-specific word is defined at first use or replaced;
aphorisms are named as the compression failure rather than left implicit.
