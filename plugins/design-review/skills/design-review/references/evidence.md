# Evidence

Where this skill's numbers come from, what they actually measure, and where the
literature disagrees with itself. Read this before quoting any figure in a report;
several widely-repeated numbers mean something narrower than they sound.

Sourced from a four-backend deep-research panel run 18 August 2026 (xAI Grok,
Perplexity Sonar Deep Research, Google Gemini Deep Research, OpenAI gpt-5.6).
Full reports are committed under `docs/deep-research/`. Citation verification
across all four: **100 citations checked, 0 fabricated, 0 dead links**; the
blocked minority are paywalls and bot walls, and existence was confirmed
separately for the two DOI-registered ones.

## The result taxonomy is already normative — use its names

W3C's **ACT Rules Format** defines five outcomes a test may report:

| Outcome | Meaning |
|---|---|
| `passed` | The target met all expectations. |
| `failed` | The target did not meet all expectations. |
| `cantTell` | Applicability, or whether expectations were met, could not be fully determined. |
| `untested` | The target was not evaluated. |
| `inapplicable` | No part of the subject matched the rule's applicability. |

<https://www.w3.org/TR/act-rules-format/>

Two consequences this skill takes literally:

- **`cantTell` is the state a two-state gate destroys**, and it is where an
  unresolvable backdrop, an unreadable channel and a probe that timed out all
  belong. `probeContrast()` returns four populations rather than a failure list
  for exactly this reason.
- **A passed rule is not conformance.** ACT states that for many mappings, all
  passed and inapplicable results still mean *further testing is needed*, because
  a rule checks a specific implementation condition rather than a whole success
  criterion. So "no failures detected among the checks that ran" is the strongest
  sentence available, and "passes WCAG" is never one of them.

axe-core ships the same idea as `incomplete`, and its message for the case this
skill's contrast gate used to get wrong is worth quoting exactly: *"The
background color could not be determined due to a background image."* It also
documents that `color-contrast` **does not work under JSDOM** — an engine that
cannot do the measurement says so rather than returning zero.

**The cost of conflating the two is measured.** On a 285-homepage scan, treating
axe's `incomplete` results as violations moved the reported failure rate to
**97.9%**. That delta is the size of the population a pass/fail gate absorbs
silently. Held at medium confidence: the source is a vendor scan write-up, and no
peer-reviewed study establishes the causal chain from conflated states to a
shipped defect. Both the OpenAI and Gemini panel members flagged that gap
independently.

## Contrast over a gradient: the range, and the disagreement about which end

WCAG 2.x is the operative standard for a conformance gate: **4.5:1 normal text,
3:1 large text** at AA, via `(L_lighter + 0.05) / (L_darker + 0.05)`.
<https://www.w3.org/TR/WCAG22/#contrast-minimum>

WCAG evaluates contrast *"with respect to the specified background over which the
text is rendered in normal usage"*, and advises taking foreground and background
values **from the user agent or the markup and styles rather than from
anti-aliased glyph pixels** — anti-aliasing makes edge pixels lighter than the
specified colour.
<https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html>

That single advisory is why this skill resolves backdrops from computed and
declared style rather than switching to pixel sampling. Pixel sampling is right
for *the background beneath text*; it is wrong for the foreground.

W3C's ACT rule **09o5cg** treats a gradient or image backdrop as a **range**, and
publishes worked examples: a passing gradient spanning **12.6:1 to 7:1**, and a
failing image spanning **1.4:1 to 4.7:1**.
<https://www.w3.org/WAI/standards-guidelines/act/rules/09o5cg/>

Note the failing example reaches 4.7:1 at one end and still fails. The operative
sentence: *a text item fails if any relevant normal-use portion of the text has
contrast below its required threshold.* WebAIM says the same thing to
practitioners — **test the area where contrast is lowest**.
<https://webaim.org/articles/contrast/>

**Held loosely, because the sources genuinely differ.** ACT's own automatable
formulation takes the *highest possible* contrast between the foreground and
background pixel sets, and then explicitly cautions that passing it does **not**
mean the text has sufficient contrast — if some pixels pass and others do not,
legibility has no clear determination method. So the normative-adjacent rule is
lenient-and-disclaimed, while the practitioner guidance and the
any-portion-fails sentence are strict.

This skill takes the strict reading: **score against the worst recovered stop.**
It is the conservative direction, it matches WebAIM and the any-portion sentence,
and a fabricated pass is worse here than a conditional finding. The cost is real
and is declared on every record: a glyph may not actually sit over the worst
stop, so a gradient-stop failure is a **High**, not a Blocker, unless it fails
against every stop. `backdropSource` on each record says which reading produced
it.

**APCA is not a gate.** WCAG 3 remains a Working Draft (3 March 2026), APCA was
removed from the July 2023 draft as exploratory content that did not advance, and
APCA's own documentation calls it a candidate method in public beta. Use WCAG 2.x
for anything that blocks; APCA only as labelled advisory telemetry.
<https://www.w3.org/TR/wcag-3.0/> ·
<https://git.apcacontrast.com/documentation/minimum_compliance.html> ·
<http://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html>

**No published failure rate exists for naive ancestor-walk contrast.** Two panel
members searched for one independently and both returned an explicit
`MISSING_DATA`. The mechanism is well documented; the rate is not. So this
skill's own figure is offered as what it is: **on `evals/fixtures/landing.html`,
obscura 0.2.0, 18 Aug 2026, five of seven reported contrast failures were scored
against a backdrop that is not there — `rgb(255,255,255)` on a purple gradient —
and the mitigation field read `false` on all seven.** Of those five, exactly one
was a wholly fabricated failure: the h1 passes its 3.0 large-text floor at every
stop (worst 3.53:1) and was reported at 1.0:1. The other four are real failures
whose ratios were wrong by 1.9 to 2.5 points, which is the more insidious half —
the verdict looks right, so nobody re-checks the number. One fixture, one engine,
one date. It is a demonstration, not a rate.

## Automation coverage: the 57% is not what it sounds like

The two figures practitioners trade are both Deque's, measuring different things,
and reconciling them is what makes either quotable:

| Figure | What it counts | Denominator |
|---|---|---|
| **57%** | Issues found automatically, weighted by volume, in Deque's own audit corpus (2,000+ audits, 13,000+ pages, ~300,000 issues) | all issues recorded |
| **~32%** (16 of 50) | Level AA success criteria for which automation detected at least one issue | WCAG 2.1 AA criteria |

<https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf>

The 57% is high because a small set of criteria carries most of the volume: seven
categories account for over 80% of issues — 3.1.1 Language of Page, 4.1.1
Parsing, 1.4.3 Contrast, 2.4.1 Bypass Blocks, 1.1.1 Non-Text Content, 4.1.2
Name/Role/Value, 1.3.1 Info and Relationships. Structural and semantic checks a
DOM read does well.

**The per-criterion zeros are the number that should shape a review.** In the
same report, automated issue detection was **0.00%** for: 1.3.2 Meaningful
Sequence, 1.4.10 Reflow, 1.4.11 Non-text Contrast, 2.1.2 No Keyboard Trap, 2.4.3
Focus Order, 2.4.4 Link Purpose, 2.4.7 Focus Visible, 3.2.1 On Focus, 3.2.2 On
Input, 3.3.1 Error Identification.

Note **2.4.7 Focus Visible at 0%** in particular. This skill has a focus gate; it
reads stylesheets and states outright that a replacement declared in a different
rule is not detected. That honesty is the right calibration, and the 0% is why.

Other envelope figures, held at lower confidence because they come from a
practitioner aggregation rather than a primary study: false-positive rates
averaging 25–35% across automated tools, false negatives reaching ~60% for
complex interaction and cognitive issues, and ~45% accuracy on keyboard traps and
focus order. <https://testparty.ai/blog/ai-tools-accuracy-statistics>

Also worth carrying: **4.1% of the top million home pages have zero *detected*
automated errors**, which is a floor on conformance rather than a measure of it.

A 2023 metatesting study across nine tools concluded they are **complementary**
rather than ranked — no single engine dominates.
<https://arxiv.org/abs/2304.07591>

## Layout geometry inflates, and the size of the inflation is published

**ReDeCheck** (Walsh, Kapfhammer & McMinn, ISSTA 2017) models a page across
viewport widths from DOM coordinates and detects five responsive failure types:
element collision, element protrusion, viewport protrusion, small-range failures,
wrapping failures.
<https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf>

Its numbers are the strongest available argument for root-cause clustering:

- **33 distinct responsive layout failures across 26 live pages**
- **137 distinct viewport ranges** reported, i.e. **4.2 viewport inspections per
  real failure**
- **147 small-range reports on one page (Accountkiller) collapsed to ONE distinct
  underlying failure**

And the four named over-fire mechanisms, each of which this skill's probes can
produce:

- a collision caused only by invisible padding;
- a protrusion that is non-observable because `overflow: hidden` clips it;
- coincidental alignment mislabelled as a small-range defect;
- a row inferred incorrectly, producing a wrapping false positive.

**Verve** (Althomali et al., *Software Testing, Verification & Reliability*, 2021)
exists to classify DOM-reported layout failures as true positive, false positive,
or **non-observable**, using viewport reachability and image analysis. That third
category is the one prose usually loses.
<https://doi.org/10.1002/stvr.1756>

**VizAssert** (PLDI 2018) formalises the browser rendering algorithm and verifies
visual-layout assertions across *all possible* renderings rather than a sampled
few, covering 14 accessibility and usability guidelines. It is the proof that some
layout properties are genuinely provable rather than heuristic, and the ceiling
this skill's geometry probes fall short of.
<https://homes.cs.washington.edu/~mernst/pubs/verify-layout-pldi2018.pdf>

This skill's own independently measured over-fire rate on one 14-screen surface —
**2 real, 35 false** — sits in the same range as ReDeCheck's, which is mild
corroboration that the number was not a fluke of one bad page.

What survives as a release gate, per the panel: overlap of two visible unrelated
interactive targets; a required target outside the reachable scroll area. What is
review-only: clipping (geometry cannot prove meaningful pixels were lost),
unexpected wrapping (needs a product expectation), and anything about alignment
or crowding. Intent is not derivable from DOM coordinates.

## Model judgement: what the numbers actually say

The most directly relevant study is Duan et al., **CHI 2024**, on LLM-generated
feedback for UI mockups.
<https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf>

| | Precision | Recall | F1 |
|---|---|---|---|
| GPT-4 | 0.603 | 0.380 | 0.466 |
| Average individual human evaluator | 0.829 | 0.336 | **0.478** |

And the finding that reframes both rows: **human inter-rater agreement was Fleiss'
κ = 0.112 on accuracy and 0.100 on helpfulness** — slight agreement. Its
suggestions were rated accurate in 52% of cases, partially accurate in 19%,
inaccurate in 29%.

**This corrects a claim earlier versions of this skill made.** It said model
agreement on free-form visual scoring is "worse than chance across models". The
evidence does not support that phrasing. What it supports is narrower and more
useful: a model performs at roughly the level of one individual human evaluator,
and *humans barely agree with each other* on this task. So disagreement is
intrinsic to the task rather than evidence of a model defect — and agreement
between models does not convert an aesthetic preference into a defect.

Judge biases, from Zheng et al., **NeurIPS 2023**:
<https://papers.nips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf>

- **Position bias**: GPT-4 order-swap consistency **65.0%**; Claude-v1 **23.8%**
  under the default prompt.
- **Verbosity bias**: a repetitive-list attack fooled Claude-v1 and GPT-3.5
  **91.3%** of the time; GPT-4 **8.7%**.
- **Self-enhancement**: GPT-4 favoured its own output by ~10 percentage points,
  Claude-v1 by ~25.

Consensus limits: across nine judges, unanimity on only **23.4%** of instances
while 94.6% reached majority. Majority measures consensus, not correctness.
<https://arxiv.org/abs/2406.07791>

**Order-swapping is not a fix.** One panel member reported that swapping as a
debiasing technique *barely moved aggregate accuracy*, and 65% consistency says
the same thing from the other side. Treat a flip under swap as evidence of bias,
not as noise to average away.

The **WebDevJudge** benchmark (ICLR 2026) puts human pairwise agreement on
interactive web UI at 84.56% against GPT-4.1's 70.34% pairwise and
Claude-3.7-Sonnet's 63.91% single-answer. Held at **medium confidence only**: the
panel member reporting these figures sourced them from a secondary write-up rather
than the paper, and that URL is bot-blocked. The primary arXiv record for the
positional-bias half does resolve. <https://arxiv.org/html/2510.18560v3>

Two things follow for practice, and both are already the skill's position:
absolute scoring is compromised enough that a 1–10 visual score should never
exist, and model judgement belongs in Tier 3 with no severity attached.

## Restraint and anti-fabrication have measured support

The staged shape — deterministic proposes, model triages — is the strongest
result here. A 2026 industrial study on a 433-alarm Tencent dataset found hybrid
static-analysis-plus-LLM triage eliminated **94–98% of false positives** while
holding recall, against 10–20 minutes of manual inspection per alarm.
<https://arxiv.org/abs/2601.18844>

Self-critique reduced inappropriate LLM output by **90.7%** in synthetic
conversations and 24–75% in a school pilot. Directional only — the task is
educational feedback, not UI review.
<https://aclanthology.org/2025.aimecon-sessions.9/>

The anti-fabrication mechanism the panel converged on, from two members
independently: **require a deterministic reference per finding, and have
something automatically reject a finding that lacks one.** A `target_count` must
be *generated by code, never by prose*. If the model says 47 buttons and the
inventory says 9, the output is inconsistent and gets rejected rather than
softened. `scripts/audit_run.py claims` is that validator here.

Severity must work as **admission control rather than description**: Blocker and
High require complete deterministic evidence, subjective critique defaults to
needs-review, and a model may not raise severity on a target whose deterministic
result was `cantTell`.

**Held open.** No study was located showing that a severity taxonomy *alone*
reduces false positives or count inflation. It is grounded in the indeterminate-
outcome, report-duplication and judge-bias evidence above rather than measured
directly, and the honest next step is an ablation on this skill's own corpus:
unrestricted critique, versus rubric-only, versus evidence-bound, versus
evidence-bound with deduplication and admission rules.

## Where the panel disagreed with itself

Carried rather than resolved, because the resolution is not available:

- **Gradient contrast: worst stop or highest-possible.** ACT's automatable rule
  says highest and disclaims it; WebAIM and ACT's own prose say lowest. This
  skill picks lowest and labels every record. If a future ACT revision settles it
  the other way, `gradientStops()` is the one function to change.
- **Coverage: 57% or 30–40%.** Reconciled above as different denominators, but
  the UK Government Digital Service figure of ~30% is a different corpus again,
  and no independent replication of any of them was located.
- **WebDevJudge's figures** are secondary-sourced and bot-blocked. Believe the
  direction, not the decimals.
- **Whether "AI slop" names a property of artifacts or of observers** remains
  unresolved and is why the tell-list is Tier 3 and cannot gate. Nothing in this
  panel changed that; see `reliability-envelope.md`.
