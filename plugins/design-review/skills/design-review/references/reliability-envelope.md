# Reliability envelope

What automated review can and cannot detect. These numbers set what the skill may assert, what it must hedge, and what it must refuse. Read once before your first review.

## Automated accessibility has a hard ceiling

Against 35 expert manual audits on production sites (Jan 2026 benchmark):

| Tool | Share of manually-reported issues found |
|---|---|
| axe-core | 22.6% |
| WAVE | 30% |
| SortSite | 40% |
| Evinced (AI-vision, industry max) | 62.8% |

So 37.2–77.4% of accessibility defects require human judgment.

Per-category, automation is worse than the headline:

- Keyboard navigation failures: **2.49%** automated detection (Deque coverage research)
- Screen reader compatibility: **~23%**

**The volume trap.** Deque telemetry reports axe-core catching 57.38% of issues *by volume*. That number is inflated by a handful of high-prevalence, trivially-detectable syntax errors — low contrast, missing alt, missing labels — which exist in enormous quantities. Volume is not criteria coverage. Never quote 57% as coverage.

Automated tools can verify that an `aria-label` exists. They cannot evaluate whether it describes the context, or whether ARIA state transitions correctly during a dynamic interaction.

## WCAG 3.0 codifies the split

WCAG 3.0 replaces true/false criteria with Bronze/Silver/Gold and introduces **Assertions** — formal claims that an organisation executed procedures requiring human judgment (usability testing with disabled users, heuristic evaluation, plain-language review). An automated agent cannot satisfy an Assertion. Baseline compliance can be automated; context-dependent assertions hand off to humans.

## Model judgment of visual quality

**Single model, repeated runs:** ICC(2,1) 0.555 — "fair" reliability, stable enough for directional signal. Mean per-design MAD 0.15.

**Across models, free-form scoring:** ICC(2,1) 0.021, Krippendorff's α −0.088. A negative alpha means judges disagree *more than chance*. A consensus-of-models does not validate subjective visual quality.

**Across models, constrained to binary checklists:** ArtifactsBench reached 94.4% ranking consistency with human preference and >90% pairwise agreement using a two-model ensemble against a strict 10-dimension rubric.

The difference is entirely the decomposition. **Atomic binary criteria hold; free-form scores collapse.** This is why every visual judgment in this skill is MET/UNMET and never a 1–10 score.

**With interactivity in scope,** agreement drops regardless: human pairwise agreement 84.56%, best model 70.34% pairwise, 63.91% pointwise. Pointwise runs ~8% below pairwise on identical data.

## Human agreement is itself low

Professional designers reach Krippendorff's α ≈ 0.25 on pairwise UI design preference. Two consequences:

1. A criterion humans cannot agree on should be cut, not automated.
2. An α ≥ 0.80 target is only meaningful against a rubric-bound expert consensus on binary checks — never against unguided aesthetic preference, where it is unreachable by construction.

## Known model failure modes

**Spatial blindness.** Bounding-box IoU 0.323 for model-only vs human-only critiques. Mitigation: draw coordinate rulers/grid on the crop edge — measured +55% improvement in spatial critique and bounding-box accuracy.

**Aesthetic prior / homogenization.** Models systematically privilege generic, templated, "safe" output and penalise distinctive, culturally specific, or original design. An unanchored visual judge inside a slop-detecting review will push *toward* slop. Mitigations: anchor references in the prompt; never let a model verdict alone produce a "this is generic" finding; prefer the systematisation check, which measures specification rather than taste.

**Verbosity/density bias.** Models equate visual density with quality and effort, rewarding cluttered layouts over elegant minimal ones. Explicit clutter penalties are required to counteract it.

**Position bias.** In any A/B comparison, models favour one slot. If comparing, run both orders and discard splits. No model is naturally symmetric — the best measured ~95%.

**Self-preference.** Models overrate outputs from their own architectural family. If judging output a Claude model generated, prefer a different-family judge or a deterministic check.

**Rendering-Evaluation Fidelity Principle.** Adding high-fidelity styling over unfixed structural defects makes a visual judge score *lower* — the new styling exposes overlaps that flat colour concealed. A score drop after a visual improvement is not automatically a regression. Check structure before reporting one.

**Quality Ceiling Effect.** Iterative refinement is bounded by the judge's perceptual headroom. Once a design is inside the judge's distinguishability threshold, further optimisation stops registering. Do not keep iterating against a judge that has stopped discriminating.

## The refusal set

Always defer to a human, and name the reason in the report:

- Cognitive accessibility
- Screen-reader flow and announced output
- Whether focus *order* is sensible for the task (order existing and matching DOM is checkable; whether it makes sense is not)
- Dynamic ARIA state transitions
- Whether alt text meaningfully describes context
- Whether a deliberate deviation is *good*, as opposed to deliberate
- Any WCAG 3.0 Assertion

## Baseline conditions

Useful for calibrating how alarming a finding should sound.

WebAIM Million, February 2026, top 1,000,000 home pages:

- 95.9% had a detected WCAG 2 failure, up from 94.8%
- 56.1 average errors per page, up 10.1% from 51
- Low-contrast text on 83.9% of pages, averaging 34 instances per page, up 15%

Six error types account for 96% of all detected errors:

| Error | % of home pages |
|---|---|
| Low contrast text | 83.9% |
| Missing alternative text | 53.1% |
| Missing form input labels | 51.0% |
| Empty links | 46.3% |
| Empty buttons | 30.6% |
| Missing document language | 13.5% |

Corroborated independently: UK GDS / Ireland NDA public-sector monitoring found 10 of 1,151 sites with no accessibility issues.

## The unresolved question

Whether "AI slop" names a property of artifacts or of observers is genuinely open.

**Position A:** AI tools produce a distinct, identifiable, low-quality output with recognisable tells.

**Position B:** the tools faithfully reproduce an industry-wide SaaS convergence that predates them; "slop" is a taste claim wearing a quality claim's clothes.

No systematic content analysis exists — no sampled corpus, no coded features, no frequency counts. No reproducible benchmark compares equivalent briefs across generation tools for visual distinctiveness. The tell-list circulating in practitioner writing is plausible and widely repeated, and entirely anecdotal.

Do not assume Position A. Ground findings in checks that survive under Position B — which is why the tell-list is Tier 3 (prompts, never gates) and the systematisation check exists.

## Consequences for how findings are worded

- Report what was checked and what was not, as separate claims.
- "The lint passed" and "verified" are different sentences. A gate is downstream of the findings that motivated it: it proves a known defect has not returned; it is structurally incapable of finding one nobody has met.
- Coverage is silent. A rule whose selector matches nothing passes without warning. When gates come back clean, ask which components no rule mentions.
- Detection is stronger than ranking. Every finding carries evidence so a human can re-rank cheaply.
