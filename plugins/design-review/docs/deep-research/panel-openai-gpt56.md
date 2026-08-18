---
title: "Automated web UI accessibility testing requires deterministic browser gates and model assistance"
run_id: dr_6b9ccaa7086e1283
question: "Evidence-backed techniques and known failure modes for automated design/UI review systems that combine deterministic browser-measured gates with model judgement, specifically for building a skill (agent instruction set) that reviews rendered web UI. Cover, as separate subtopics: (1) computing text/background contrast correctly when the backdrop is a gradient, image, or translucent layer — what algorithms and standards bodies actually specify (WCAG 2.x ratio limits, APCA/WCAG 3 status, per-pixel vs computed-style sampling), and the documented failure rate of naive computed-style ancestor-walk approaches; (2) reliability envelopes of automated accessibility testing — measured criteria-coverage percentages for axe-core and comparable engines, false-positive/false-negative rates, and the specific WCAG criteria that automation provably cannot reach; (3) how mature test/verification tooling distinguishes \"check passed\" from \"check could not run\" — three-state result taxonomies, unmeasurable-population reporting, coverage denominators, and evidence that conflating them causes shipped defects; (4) headless-browser engine divergence as a measurement hazard: documented cases where a non-Chrome or reduced engine returned an empty/zero computed value that a checker read as a real measurement, and mitigation patterns (longhand-vs-shorthand reads, capability probing, feature detection before assertion); (5) layout-integrity and visual-defect detection by DOM geometry rather than pixels — published techniques, measured over-fire rates, and which defect classes are provably computable; (6) empirical findings on LLM-as-judge for visual and design quality — inter-rater agreement figures, position/verbosity bias, and whether model consensus validates subjective visual judgement; (7) prompt-level and instruction-design findings specific to review/critique agents: severity taxonomies that reduce false positives, restraint mechanisms against finding-count inflation, and structures that prevent fabricated observations (\"I audited 47 buttons\" with no measurement behind it). For each subtopic give the strongest primary sources, the numbers, and where the literature disagrees."
provider: openai
model: gpt-5.6-terra
tier: fast
archetype: technical
sources: 40
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 3.50
completed: 2026-08-18T00:33:40.798Z
---
## Executive Summary

- **(High Confidence)** Treat rendered-UI review as a **two-tier system**: deterministic browser gates may assert only directly measured, fully-resolved predicates; model review may prioritize, explain, and propose fixes, but must not create compliance failures or factual observations without attached browser evidence. W3C ACT explicitly distinguishes `passed`, `failed`, `cantTell`, `untested`, and `inapplicable`; a clean deterministic result is not equivalent to full WCAG conformance. [w3.org](https://www.w3.org/TR/act-rules-format/) ([w3.org](https://www.w3.org/TR/act-rules-format/?utm_source=openai))

- **(High Confidence)** For WCAG 2.x, a contrast gate must use the WCAG relative-luminance ratio against the **actual specified backdrop at each relevant text location**, with thresholds of **4.5:1 for normal text** and **3:1 for large text** at AA. A single inherited `background-color` or ancestor walk is not a valid resolution method when backgrounds include images, gradients, masks, opacity, blend modes, or intervening stacking contexts. [w3.org](https://www.w3.org/TR/WCAG22/#contrast-minimum) ([w3.org](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html?pt=BureoF4GVB&utm_source=openai))

- **(High Confidence)** The right result for unresolved backdrops is **could-not-run / needs-review**, not pass and not automatic fail. axe-core itself returns incomplete results when a background image prevents a reliable color determination, and its repository states that `color-contrast` is known not to work in JSDOM. [github.com](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-development.md) [github.com](https://github.com/dequelabs/axe-core) ([github.com](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-development.md?utm_source=openai))

- **(Medium Confidence)** Automation coverage claims must be scoped to a population and a definition. Deque reports that axe-core found **57% of issues in its audited HTML-page dataset**, but its own per-criterion table reports **0% automated detection** for many criteria, including Meaningful Sequence, Reflow, Non-text Contrast, Focus Visible, Keyboard Trap, and Focus Order. This is issue-weighted coverage, not proof that 57% of WCAG conformance is automated. [accessibility.deque.com](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf) ([accessibility.deque.com](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf))

- **(High Confidence)** DOM-geometry layout checks should survive only for **objective geometric predicates**: visible-box overlap, clipping/protrusion, off-viewport placement, and breakpoint-localized wrapping/alignment changes. They must be deduplicated by root cause and separated from “non-observable issues.” ReDeCheck found **147 true-positive reports corresponding to one distinct failure** on one page; it also documented false and non-observable geometry reports caused by invisible padding and `overflow: hidden`. [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf) ([researchgate.net](https://www.researchgate.net/publication/317300653_Automated_Layout_Failure_Detection_for_Responsive_Web_Pages_Without_an_Explicit_Oracle))

- **(High Confidence)** Do not score subjective visual/design quality as an autonomous release gate. In a UI-mockup study, GPT-4 feedback achieved **0.603 precision, 0.380 recall, and 0.466 F1** against a constructed issue set; human raters’ agreement on whether feedback was accurate/helpful was only **Fleiss’ κ = 0.112 / 0.100**. This means disagreement is intrinsic to the task, not evidence that model consensus establishes truth. [people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf) ([people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf))

- **(High Confidence)** The review skill needs a hard evidence contract: every finding must carry target identity, UI state, viewport, browser/engine, measured values, rule version, and screenshot or DOM evidence. A model may state “could not verify” but may not claim “I audited 47 buttons” unless the run manifest contains 47 target records. This follows the ACT result model’s target-level outcomes and axe-core’s target-level result arrays. [w3.org](https://www.w3.org/TR/act-rules-format/) [github.com](https://github.com/dequelabs/axe-core/blob/develop/doc/API.md) ([w3.org](https://www.w3.org/TR/act-rules-format/?utm_source=openai))

- **(Medium Confidence)** Use model judgement as a **review-assistance layer**, not as evidence aggregation by vote. LLM judges exhibit documented position, verbosity, and self-enhancement biases; in one benchmark, GPT-4’s order-swap consistency was only **65.0%**, and the “repetitive-list” verbosity attack fooled Claude-v1 and GPT-3.5 **91.3%** of the time. [papers.nips.cc](https://papers.nips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf) ([papers.nips.cc](https://papers.nips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf))

---

## Detailed Findings

### 1. Evidence-backed techniques and known failure modes for deterministic browser gates plus model judgement in rendered-web-UI review

#### 1.1 Computing contrast over gradients, images, translucency, and layered backdrops

**Decision:** Implement a **resolved-backdrop contrast gate**, not a computed-style ancestor walk.

WCAG 2.x requires a relative-luminance contrast ratio of at least **4.5:1** for normal text and **3:1** for large text at Level AA. WCAG evaluates contrast “with respect to the specified background over which the text is rendered in normal usage”; it also advises using foreground/background values from the user agent or markup/styles rather than anti-aliased glyph pixels. [w3.org](https://www.w3.org/TR/WCAG22/#contrast-minimum) [w3.org](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) ([w3.org](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html?pt=BureoF4GVB&utm_source=openai))

The WCAG 2.x contrast formula is:

\[
CR = \frac{L_{lighter}+0.05}{L_{darker}+0.05}
\]

where relative luminance is calculated from linearized sRGB channel values. [w3.org](https://www.w3.org/WAI/WCAG20/versions/techniques/wcag20-techniques-20081211-a4.pdf) ([w3.org](https://www.w3.org/WAI/WCAG20/versions/techniques/wcag20-techniques-20081211-a4.pdf?utm_source=openai))

A backdrop can vary spatially. W3C ACT examples explicitly describe contrast as a **range** over a gradient or background image: one passing gradient example ranges from **12.6:1 to 7:1**, while a failing image example ranges from **1.4:1 to 4.7:1**. A text item therefore fails if any relevant normal-use portion of the text has contrast below its required threshold. [w3.org](https://www.w3.org/WAI/standards-guidelines/act/rules/09o5cg/) ([w3.org](https://www.w3.org/WAI/standards-guidelines/act/rules/09o5cg/))

| Backdrop condition | Legitimate deterministic method | Gate result if unresolved | Why |
|---|---|---|---|
| Opaque solid color | Read resolved foreground and resolved opaque background; apply WCAG 2 ratio. | Pass / fail | Fully computable. |
| CSS linear/radial gradient with parseable stops and no raster layer | Evaluate the composited gradient at all sampled text-background locations; retain the minimum ratio. | Could-not-run if unsupported syntax, external variable, filter, or blend cannot be resolved. | A single endpoint or average can miss the worst location. |
| Static raster image | Sample the rendered background behind text locations, excluding anti-aliased glyph pixels; compute worst-case ratio. | Could-not-run if image pixels, cross-origin resource, animation frame, or occluding layer cannot be reliably obtained. | The image’s backdrop varies by position. |
| Semi-transparent foreground/background | Alpha-composite all layers in CSS paint order, then calculate the ratio from the resulting opaque colors. | Could-not-run where blend/filter/mask/canvas/video pixels cannot be resolved. | Raw `rgba()` channel values are not the visible colors. |
| Video, canvas, animated gradient, dynamic image, filter, `mix-blend-mode` | Sample known stable frames and report a temporal sample scope; never generalize sampled success to all time. | Could-not-run for universal WCAG assertion. | The content has an unbounded or state-dependent backdrop population. |

<INFERENCE from="WCAG 2.x specifies contrast against the specified normal-use background; W3C ACT represents gradients/images as contrast ranges; axe-core returns incomplete when background color cannot be determined due to a background image">For a rendered-UI gate, the defensible operational rule is: resolve the paint stack analytically where CSS is deterministic; otherwise sample the rendered backdrop at documented text locations and frames; issue pass/fail only if the sampled population is explicitly bounded and fully resolved. </INFERENCE> [w3.org](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) [w3.org](https://www.w3.org/WAI/standards-guidelines/act/rules/09o5cg/) [github.com](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-development.md) ([w3.org](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html?pt=BureoF4GVB&utm_source=openai))

**Do not use literal screen-pixel text colors.** WCAG warns that anti-aliasing can make on-screen text pixels lighter than the specified foreground color, which is why the normative evaluation convention uses underlying colors rather than edge pixels of glyphs. Rendered pixel sampling is appropriate for the **background beneath text**, not for sampling anti-aliased foreground glyph pixels. [w3.org](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) ([w3.org](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html?pt=BureoF4GVB&utm_source=openai))

**Unresolvable-backdrop policy.** axe-core’s color-contrast implementation treats a background image as an incomplete result because “The background color could not be determined due to a background image.” [github.com](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-development.md) ([github.com](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-development.md?utm_source=openai)) The agent skill should adopt the same posture: **never transform unknown into pass**; distinguish “not measured” from “measured and acceptable.”

**APCA / WCAG 3 status.** WCAG 3 remains a W3C Working Draft as of **March 3, 2026**, and W3C states that a Working Draft is not an endorsement and may change. [w3.org](https://www.w3.org/TR/2026/WD-wcag-3.0-20260303/) ([w3.org](https://www.w3.org/TR/wcag-3.0/)) APCA’s own compliance documentation calls APCA “the candidate contrast method for WCAG 3” and “currently in public beta”; it is not a substitute for WCAG 2.x conformance claims. [git.apcacontrast.com](https://git.apcacontrast.com/documentation/minimum_compliance.html) ([git.apcacontrast.com](https://git.apcacontrast.com/documentation/minimum_compliance.html?utm_source=openai))

**Recommendation:** Use WCAG 2.2 contrast ratios for compliance gates today; optionally calculate APCA as **advisory design telemetry**, clearly labelled non-normative.

<MISSING_DATA>A peer-reviewed or authoritative study quantifying the failure rate of a generic “computed-style ancestor walk” contrast algorithm was sought. No source located establishes a transferable percentage. The available primary evidence instead documents the failure mechanism: image/gradient/transparency backdrops are unresolved by simple computed-color logic, and axe-core correctly emits incomplete rather than pretending to measure them. A benchmark would need a corpus with pixel/paint-stack ground truth and defined ancestor-walk implementations.</MISSING_DATA>

---

#### 1.2 Reliability envelopes of automated accessibility testing

**Decision:** Report automated accessibility results as **detected-issue yield**, **criterion applicability**, and **unmeasured remainder**—not as “WCAG compliance percentage.”

axe-core states that it can find “on average **57% of WCAG issues automatically**,” while returning incomplete results where it cannot be certain. [github.com](https://github.com/dequelabs/axe-core) ([github.com](https://github.com/dequelabs/axe-core?utm_source=openai)) Its 2021 coverage report attributes **57%** of the issues in its selected HTML audit corpus to automation. [accessibility.deque.com](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf) ([accessibility.deque.com](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf?utm_source=openai))

That figure is useful but narrow:

1. It is **issue-weighted**, not a count of fully automatable WCAG success criteria.  
2. It comes from the tool vendor’s audit corpus and methodology.  
3. It does not mean that a page with no axe violations satisfies WCAG.  
4. It does not measure all rendered states, interactive flows, assistive-technology behavior, or semantic appropriateness.

The same report shows major criteria for which its observed automated share was **0.00%**, including 1.3.2 Meaningful Sequence, 1.4.10 Reflow, 1.4.11 Non-text Contrast, 2.1.2 No Keyboard Trap, 2.4.3 Focus Order, 2.4.4 Link Purpose, 2.4.7 Focus Visible, 3.2.1 On Focus, 3.2.2 On Input, and 3.3.1 Error Identification. [accessibility.deque.com](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf) ([accessibility.deque.com](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf))

| Reliability question | Strongest available evidence | Interpretation for this skill |
|---|---|---|
| How many real issues can axe automation find? | Deque reported **57%** of issues in its selected audit dataset. [accessibility.deque.com](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf) | Use as a vendor-specific yield estimate, not an assurance level. |
| Can one engine cover all detectable issues? | A 2023 metatesting study comparing nine tools concluded that tools are complementary. [arxiv.org](https://arxiv.org/abs/2304.07591) | Combining engines can increase detection diversity, but does not make semantic criteria automated. |
| Are axe reports designed to avoid false positives? | axe’s project manifesto says it returns zero false positives “bugs notwithstanding.” [github.com](https://github.com/dequelabs/axe-core) | Treat this as a design objective, not an independently measured universal false-positive rate. |
| What does a pass mean? | ACT says many rule passes still mean “further testing is needed” for the corresponding WCAG requirement. [w3.org](https://www.w3.org/TR/act-rules-format/) | A rule pass can establish a narrow predicate, not full success-criterion satisfaction. |
| What cannot be established from a static rendered page? | W3C ACT describes rules as partial checks, often checking only a specific implementation condition rather than an entire success criterion. [w3.org](https://www.w3.org/WAI/standards-guidelines/act/rules/about/) | Intent, semantics, task completion, logical order, suitable alternatives, and user interaction must retain review states. |

<CONFLICTING_EVIDENCE>Practitioners often repeat that automation finds “20–30%” of accessibility issues, while Deque reports 57%. These are not necessarily contradictory: the former commonly refers to the fraction of WCAG criteria thought fully automatable, while Deque’s number is issue-weighted detection in a selected audit corpus. The two denominators differ. Deque’s own report confirms many criteria had 0% automated issue detection in that corpus. </CONFLICTING_EVIDENCE> [accessibility.deque.com](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf) [github.com](https://github.com/dequelabs/axe-core) ([accessibility.deque.com](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf))

<MISSING_DATA>Comparable, current, independently replicated false-positive and false-negative rates for axe-core, WAVE, QualWeb, IBM Equal Access, and Alfa on the same rendered, interactive web corpus were not located in the available primary evidence. The 2023 metatesting work establishes complementarity, but does not provide a single universal precision/recall figure suitable for product assurance claims. A useful benchmark would require expert-labelled findings across stateful applications, including a stated mapping from tool rules to target-level truth.</MISSING_DATA>

---

#### 1.3 Pass, fail, and could-not-run: result taxonomy, denominators, and silent failure prevention

**Decision:** Use an external **three-state product taxonomy**—`pass`, `fail`, `could-not-run`—but retain the richer internal ACT-compatible states: `passed`, `failed`, `cantTell`, `untested`, and `inapplicable`.

W3C ACT specifies five outcomes:

- `passed`: target met all expectations;
- `failed`: target did not meet all expectations;
- `cantTell`: applicability or expectation satisfaction could not be fully determined;
- `untested`: the target was not evaluated;
- `inapplicable`: no portion of the test subject matched the rule applicability. [w3.org](https://www.w3.org/TR/act-rules-format/) ([w3.org](https://www.w3.org/TR/act-rules-format/?utm_source=openai))

The critical distinction is that ACT does **not** treat a passed partial rule as automatic WCAG conformance. For many mappings, all passed/inapplicable results still mean “further testing is needed.” [w3.org](https://www.w3.org/TR/act-rules-format/) ([w3.org](https://www.w3.org/TR/act-rules-format/?utm_source=openai))

**Recommended external mapping**

| Internal state | Product-facing state | Include in compliance denominator? | Required report behavior |
|---|---:|---:|---|
| `passed` | Pass | Yes | State predicate, measured values, target, and evidence. |
| `failed` | Fail | Yes | State violated threshold and reproducible target/state/viewport. |
| `cantTell` | Could-not-run | Yes, in measurement-coverage denominator; no, in resolved-outcome denominator | State blocker: image, dynamic layer, unsupported CSS, cross-origin raster, timing, etc. |
| `untested` | Could-not-run | Yes, in run-completion denominator | State why it was skipped: page error, timeout, blocked frame, unsupported engine. |
| `inapplicable` | Not applicable | No | Retain count, but do not call it passed. |

<INFERENCE from="W3C ACT defines distinct passed/failed/cantTell/untested/inapplicable outcomes and says passed outcomes of many partial checks still require further testing">A UI-review system should calculate at least three denominators: (1) in-scope targets, (2) targets with a resolved deterministic verdict, and (3) targets that could not be measured. Reporting only a passed percentage masks the unmeasurable population. </INFERENCE> [w3.org](https://www.w3.org/TR/act-rules-format/) ([w3.org](https://www.w3.org/TR/act-rules-format/?utm_source=openai))

**Recommended metrics**

\[
\text{Resolved measurement rate} = \frac{P+F}{P+F+C}
\]

\[
\text{Deterministic pass rate} = \frac{P}{P+F}
\]

\[
\text{Could-not-run rate} = \frac{C}{P+F+C}
\]

where \(P\) is passes, \(F\) failures, and \(C\) could-not-run results. `Inapplicable` counts should be reported separately rather than included in the pass rate.

**Example report line**

> Contrast — 119 applicable text targets: 101 resolved pass, 5 resolved fail, 13 could not be resolved because of image/video/translucent backdrops. Deterministic pass rate: 95.3% of resolved targets; measurement yield: 89.1% of applicable targets. No full WCAG conformance assertion made.

This directly avoids the silent condition in which an unsupported measurement and a clean UI both appear as “no findings.”

<INSUFFICIENT_EVIDENCE>A direct longitudinal study proving that conflating pass and could-not-run specifically caused released accessibility defects was not located. However, the failure mechanism is demonstrated by standards and tools: ACT reserves `cantTell` and `untested`; axe returns `incomplete`; and DOM-layout research identifies non-observable reports separately from actual faults. The defect-shipping consequence is a strong operational inference, not a directly measured causal estimate.</INSUFFICIENT_EVIDENCE>

---

#### 1.4 Browser-engine and headless-environment divergence

**Decision:** A browser gate must prove that its measurement environment is capable of producing the relevant measurement before it interprets empty strings, `0`, or missing data as real CSS/layout values.

Two documented hazards are directly relevant:

1. **JSDOM has no layout engine.** Its own documentation states that layout is outside scope and that it returns zeros for many layout-related properties. [github.com](https://github.com/jsdom/jsdom) ([github.com](https://github.com/jsdom/jsdom?utm_source=openai))  
2. **axe-core states that `color-contrast` is known not to work with JSDOM.** [github.com](https://github.com/dequelabs/axe-core) ([github.com](https://github.com/dequelabs/axe-core?utm_source=openai))  
3. **Firefox/Gecko documented shorthand computed-style divergence.** A Mozilla bug reported that `getComputedStyle(element).getPropertyValue('border')` returned an empty string in Firefox Nightly while Safari Technology Preview and Blink/Edge returned a shorthand value for the same test. [bugzilla.mozilla.org](https://bugzilla.mozilla.org/show_bug.cgi?id=137688) ([bugzilla.mozilla.org](https://bugzilla.mozilla.org/show_bug.cgi?id=137688&utm_source=openai))  
4. Mozilla also documented cases in which lack of presentation returned a style object whose length was `0` and whose declarations returned empty strings. [bugzilla.mozilla.org](https://bugzilla.mozilla.org/show_bug.cgi?id=1467722) ([bugzilla.mozilla.org](https://bugzilla.mozilla.org/show_bug.cgi?id=1467722&utm_source=openai))

| Hazard | Incorrect checker behavior | Required mitigation |
|---|---|---|
| JSDOM layout zeros | Treat `getBoundingClientRect().width === 0` as evidence that an element is collapsed or invisible. | Mark geometry checks unsupported; use Chromium/WebKit/Firefox with real layout. |
| Empty shorthand property | Treat `getComputedStyle(el).border === ""` as “no border.” | Query `border-top-width`, `border-right-width`, `border-bottom-width`, `border-left-width`, styles, and colors individually. |
| Styles not loaded / no presentation | Treat empty computed styles as default or transparent colors. | Require a capability probe and settle condition before assertions. |
| Headless font fallback | Treat geometry or line wrap as portable without checking fonts. | Pin browser revision, installed fonts, device scale factor, locale, viewport, and font-loading completion. |
| Browser divergence | Treat one engine’s output as cross-browser fact. | Report engine-specific result; run matrix only for high-risk visual checks. |

<INFERENCE from="jsdom documents zero-valued layout behavior; Mozilla documents empty computed-style values in no-presentation and shorthand scenarios; axe documents color-contrast incompatibility with JSDOM">A measurement is valid only if a preflight capability probe passes. The probe should create a visible test element with known longhand styles and dimensions, verify non-zero geometry, verify expected computed longhand values, and verify font loading before any UI assertion runs. </INFERENCE> [github.com](https://github.com/jsdom/jsdom) [bugzilla.mozilla.org](https://bugzilla.mozilla.org/show_bug.cgi?id=137688) [github.com](https://github.com/dequelabs/axe-core) ([github.com](https://github.com/jsdom/jsdom?utm_source=openai))

<MISSING_DATA>A primary-source case was not located in which a named production UI checker is conclusively shown to have read an empty/zero value from a non-Chrome engine and shipped that value as a real measurement. The browser and reduced-engine behaviors themselves are documented. To establish the full causal chain, a reproducible checker issue or postmortem is required.</MISSING_DATA>

---

#### 1.5 DOM-geometry layout checks: what survives high over-fire rates

**Decision:** Retain geometry checks only where the output is framed as a factual geometry predicate—not as a complete visual-quality judgement.

The foundational ReDeCheck research models a page across viewport widths using DOM element coordinates and detects five responsive layout failure types: element collision, element protrusion, viewport protrusion, small-range failures, and wrapping failures. [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf) ([researchgate.net](https://www.researchgate.net/publication/317300653_Automated_Layout_Failure_Detection_for_Responsive_Web_Pages_Without_an_Explicit_Oracle)) It found **33 distinct responsive layout failures across 26 live pages**, while producing **137 distinct viewport ranges**, requiring an average of **4.2 viewport inspections per actual responsive layout failure**. [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf) ([researchgate.net](https://www.researchgate.net/publication/317300653_Automated_Layout_Failure_Detection_for_Responsive_Web_Pages_Without_an_Explicit_Oracle))

The same work demonstrates finding-count inflation: **147 small-range reports** on Accountkiller collapsed to **one distinct underlying failure**. [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf) ([researchgate.net](https://www.researchgate.net/publication/317300653_Automated_Layout_Failure_Detection_for_Responsive_Web_Pages_Without_an_Explicit_Oracle))

It also explains why pure DOM geometry over-fires:

- geometry can show a collision caused only by invisible padding;
- protrusion can be non-observable because `overflow: hidden` clips it;
- coincidental alignment can be mislabeled as a small-range defect;
- a presumed row may be inferred incorrectly, creating wrapping false positives. [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf) ([eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf))

A 2021 follow-on system, Verve, was designed specifically to classify DOM-reported responsive layout failures as true positives, false positives, or non-observable issues using viewport reachability and image analysis. [onlinelibrary.wiley.com](https://onlinelibrary.wiley.com/doi/10.1002/stvr.1756) ([onlinelibrary.wiley.com](https://onlinelibrary.wiley.com/doi/full/10.1002/stvr.1756?utm_source=openai))

| Defect predicate | Deterministically computable? | Release-gate status | Required qualification |
|---|---:|---:|---|
| Two visible, unrelated interactive targets’ painted boxes overlap | Yes, if paint order and visibility are known | High-signal fail or review | Do not flag parent/child containment or intentional overlays. |
| A required target’s visible box lies outside scrollable reachable area | Yes, with scroll geometry and visibility | High-signal fail | Exclude off-canvas menus until intended state is opened. |
| Text or required action is clipped by `overflow: hidden` | Partially | Review unless text clipping is directly observed | Geometry alone cannot prove that meaningful pixels are lost. |
| Responsive row unexpectedly wraps | Partially | Review | Requires product/semantic expectation of non-wrapping. |
| Alignment inconsistency / “looks crowded” | No | Model advisory only | Intent is not derivable from DOM coordinates. |
| Aesthetic hierarchy / balance / rhythm | No | Model advisory only | Requires subjective judgement and design context. |

<INFERENCE from="ReDeCheck reports repeated reports for one root failure and documents false/non-observable DOM-geometry issues; Verve adds visual classification">The agent must cluster geometry events before reporting: canonicalize by affected component subtree, viewport interval, UI state, and failure mechanism. Severity is assigned once per root cause, not once per overlapping descendant pair. </INFERENCE> [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf) [onlinelibrary.wiley.com](https://onlinelibrary.wiley.com/doi/10.1002/stvr.1756) ([researchgate.net](https://www.researchgate.net/publication/317300653_Automated_Layout_Failure_Detection_for_Responsive_Web_Pages_Without_an_Explicit_Oracle))

<MISSING_DATA>Recent, independently replicated precision/recall or false-positive rates for DOM-only responsive-layout checks on modern JavaScript-heavy web applications were not located. The available source provides strong failure-mode evidence and report-inflation evidence, but not a current universal “over-fire percentage.”</MISSING_DATA>

---

#### 1.6 LLM-as-judge for visual and design quality

**Decision:** Do not use model consensus as validation of subjective UI quality. Use models for evidence-grounded critique, triage, explanation, and repair suggestions; score them only against a task-specific, human-labelled calibration set.

The most directly relevant UI study found that GPT-4-generated mockup feedback was rated **accurate in 52%**, partially accurate in **19%**, and inaccurate in **29%** of suggestions. It was considered helpful/very helpful in **49%** of cases, moderately helpful in **15%**, and slightly/not helpful in **36%**. [people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf) ([people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf))

Against the study’s constructed ground-truth issue set, GPT-4 reached **precision 0.603**, **recall 0.380**, and **F1 0.466**; an average individual human evaluator reached **precision 0.829**, **recall 0.336**, and **F1 0.478**. [people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf) ([people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf))

However, human agreement was itself low: Fleiss’ κ was **0.112** for accuracy ratings and **0.100** for helpfulness ratings—only slight agreement. [people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf) ([people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf))

This matters: a model’s disagreement with one rater is not necessarily a model defect; nor does agreement between several models turn an aesthetic preference into an objective defect.

General LLM-judge research identifies additional reliability hazards:

| Bias / reliability result | Evidence | Implication for UI review |
|---|---|---|
| Position bias | In order-swapped comparisons, GPT-4 was consistent only **65.0%** of the time; Claude-v1 was **23.8%** under the default prompt. [papers.nips.cc](https://papers.nips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf) | Randomize presentation order and require order-swap invariance for any scored pairwise evaluation. |
| Verbosity bias | A repetitive-list attack fooled Claude-v1 and GPT-3.5 **91.3%** of the time; GPT-4 failed **8.7%** of the time. [papers.nips.cc](https://papers.nips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf) | Do not reward longer critique explanations; constrain reports to evidence-linked claims. |
| Self-enhancement / model-family preference | GPT-4 was reported to favor itself by a **10 percentage-point** higher win rate; Claude-v1 by **25 points** in the studied setting. [papers.nips.cc](https://papers.nips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf) | Avoid judging a model’s own output with the same model family as the sole evaluator. |
| Cross-model consensus limits | Nine judges unanimously agreed on only **23.4%** of instances, though **94.6%** achieved majority agreement in one study. [arxiv.org](https://arxiv.org/abs/2406.07791) | Majority agreement measures consensus, not correctness or human alignment. |
| Perceptual-judgment bias | Recent multimodal-judge research defines a failure mode where the model does not penalize a claim contradicting the image. [perception-judge.github.io](https://perception-judge.github.io/) | Require the model to cite a visible region or deterministic measurement before asserting a visual fact. |

<INFERENCE from="UI feedback studies show limited precision and low rater agreement; general LLM-judge studies show position, verbosity, and self-enhancement biases; multimodal judge work identifies visual-claim grounding failures">Model consensus is insufficient as a release criterion for subjective visual judgement. It can increase confidence only after calibration against representative human-labelled UI cases and bias tests, including order swap, wording swap, and evidence-removal ablations. </INFERENCE> [people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf) [papers.nips.cc](https://papers.nips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf) [arxiv.org](https://arxiv.org/abs/2406.07791) ([people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf))

---

#### 1.7 Prompt and instruction design for critique agents

**Decision:** Give the model no authority to invent observations, promote subjective findings to blocking severity, or count targets absent an evidence manifest.

The most transferable evidence supports **constraint-and-review structures**, not free-form “act as a senior designer” prompting.

A 2025 study found that adding self-critique reduced inappropriate LLM hints by **90.7%** in synthetic conversations and by **24–75%** in a real high-school pilot. The task is educational feedback rather than UI review, so the transfer is directional rather than conclusive. [aclanthology.org](https://aclanthology.org/2025.aimecon-sessions.9/) ([aclanthology.org](https://aclanthology.org/2025.aimecon-sessions.9/))

A 2026 industrial study of LLM-assisted static-analysis triage found that hybrid static-analysis/LLM techniques eliminated **94–98%** of false positives while maintaining high recall in a 433-alarm Tencent dataset; the study also found that manual inspection took **10–20 minutes per alarm**. This supports a staged architecture in which deterministic analysis proposes candidates and models triage/contextualize them, rather than generating unrestricted findings. [arxiv.org](https://arxiv.org/abs/2601.18844) ([arxiv.org](https://arxiv.org/abs/2601.18844))

**Recommended instruction architecture**

1. **Evidence collector, deterministic only**  
   Emits structured facts: DOM target, role, bounding box, computed longhands, scroll geometry, screenshot crop, accessibility-tree facts, UI state, browser version, and rule result.

2. **Eligibility gate**  
   The model sees only targets with a deterministic failure, a deterministic ambiguity, or a deliberately sampled subjective-review queue.

3. **Critique generator**  
   Must classify each statement as:
   - `measured_fact`,
   - `inference`,
   - `design_recommendation`,
   - `could_not_verify`.

4. **Evidence validator**  
   Rejects any finding whose target, evidence ID, and measurement are absent; rejects counts not derivable from the manifest.

5. **Deduplicator and severity normalizer**  
   Clusters descendant events and assigns one root-cause finding.

**Recommended severity taxonomy**

| Severity | Admission rule | Example |
|---|---|---|
| Blocker | Direct, reproducible functional or accessibility failure with complete deterministic evidence. | Focused required control is clipped and unreachable; normal-size text measures 2.7:1 on a fully resolved solid backdrop. |
| High | Direct user-impacting failure; no reasonable workaround. | Overlapping elements obscure a checkout action at a documented viewport. |
| Medium | Measured defect with limited scope or workaround. | One responsive breakpoint produces clipped supplementary content. |
| Needs review | Evidence incomplete or applicability subjective. | Text sits over a cross-origin animated video; model suspects poor hierarchy. |
| Improvement | Non-failing design advice; never counted as defect rate. | Increase spacing consistency or strengthen visual grouping. |

<INFERENCE from="ACT separates determinate from indeterminate outcomes; ReDeCheck demonstrates large report inflation for one root cause; LLM judge research demonstrates bias and UI critique research demonstrates imperfect precision">A severity taxonomy reduces false positives only if severity is an admission control, not merely prose. “Blocker/High” must require deterministic evidence; subjective model critique defaults to Needs review or Improvement. </INFERENCE> [w3.org](https://www.w3.org/TR/act-rules-format/) [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf) [people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf) ([w3.org](https://www.w3.org/TR/act-rules-format/?utm_source=openai))

**Finding-count restraint rules**

- One issue key per `{root component, mechanism, UI state, viewport interval}`.
- Collapse descendant overlap reports into one root-cause record.
- Cap the output to one primary finding plus linked affected targets unless separate causes are evidenced.
- Do not report subjective “improvements” in the defect count.
- Do not permit a model to raise severity after deterministic evidence says `could-not-run`.
- Require an explicit `evidence_ids[]` field for every sentence framed as an observation.
- Require a `target_count` field generated by code, never prose.

**Minimal finding schema**

```json
{
  "finding_id": "contrast:button.primary@desktop:001",
  "category": "accessibility.contrast",
  "severity": "high",
  "outcome": "fail",
  "assertion_type": "measured_fact",
  "target": {
    "stable_dom_id": "checkout-submit",
    "selector": "[data-testid='checkout-submit']",
    "accessible_name": "Place order"
  },
  "environment": {
    "browser": "Chromium 126",
    "viewport_css_px": [1440, 900],
    "device_scale_factor": 1,
    "ui_state": ["loaded", "checkout-step-3"]
  },
  "measurement": {
    "foreground": "#767676",
    "resolved_background": "#FFFFFF",
    "contrast_ratio": 4.54,
    "threshold": 4.5,
    "method": "resolved-solid-backdrop"
  },
  "evidence_ids": ["dom-182", "style-182", "screenshot-71"],
  "root_cause_key": "color-token:text-secondary-on-surface",
  "recommendation": "Use a text token with ratio >= 4.5:1 on surface."
}
```

The `could-not-run` counterpart must preserve the same target and environment fields, but set `measurement_status: "unresolved"` and identify the exact blocker—for example, `background-image-cross-origin`, `dynamic-video`, `unsupported-mix-blend-mode`, `font-not-loaded`, or `layout-engine-unsupported`.

---

### 2. What is the current state, and what is the strongest supporting evidence for it?

The current state as of **August 18, 2026** is:

- **WCAG 2.2 remains the operative W3C Recommendation for contrast conformance claims.** WCAG 3 is still a Working Draft, not a completed standard. [w3.org](https://www.w3.org/TR/WCAG22/) [w3.org](https://www.w3.org/TR/2026/WD-wcag-3.0-20260303/) ([w3.org](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html?pt=BureoF4GVB&utm_source=openai))
- **APCA is not yet a WCAG conformance replacement.** It is a candidate method associated with WCAG 3 work and public beta language, so it belongs in advisory design analysis rather than present-day WCAG gate logic. [git.apcacontrast.com](https://git.apcacontrast.com/documentation/minimum_compliance.html) ([git.apcacontrast.com](https://git.apcacontrast.com/documentation/minimum_compliance.html?utm_source=openai))
- **Automated accessibility engines are valuable but intrinsically partial.** axe-core’s own materials explicitly expose incomplete cases and document known environmental limitations such as JSDOM contrast support. [github.com](https://github.com/dequelabs/axe-core) [github.com](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-development.md) ([github.com](https://github.com/dequelabs/axe-core?utm_source=openai))
- **Mature accessibility test specifications already provide the required taxonomy.** The product should not invent a boolean-only result protocol when ACT has explicit determination, indeterminacy, nonexecution, and inapplicability states. [w3.org](https://www.w3.org/TR/act-rules-format/) ([w3.org](https://www.w3.org/TR/act-rules-format/?utm_source=openai))
- **LLM review is useful as assistance but not established as autonomous visual-quality verification.** Direct UI studies show meaningful but imperfect model issue detection and very low agreement even among humans over subjective feedback quality. [people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf) ([people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf))

---

### 3. What are the contrasting viewpoints or competing evidence?

| Topic | Position A | Position B | Decision |
|---|---|---|---|
| Automation coverage | axe-core reports 57% issue detection in its dataset. [accessibility.deque.com](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf) | Many WCAG criteria remain unautomated or only partially testable; ACT says a passed rule often still needs further testing. [w3.org](https://www.w3.org/TR/act-rules-format/) | Report issue yield and unmeasured scope separately; do not use a single compliance score. |
| Contrast measurement | WCAG recommends underlying specified colors rather than anti-aliased text pixels. [w3.org](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html) | Real rendered backdrops can vary spatially and require rendered-background sampling or paint-stack computation. [w3.org](https://www.w3.org/WAI/standards-guidelines/act/rules/09o5cg/) | Use style values for foreground; resolve/sample actual backdrop values at text locations. |
| APCA | APCA may improve perceptual modelling and is a WCAG 3 candidate. [git.apcacontrast.com](https://git.apcacontrast.com/documentation/minimum_compliance.html) | WCAG 3 is still draft; WCAG 2.x ratio rules govern current conformance claims. [w3.org](https://www.w3.org/TR/2026/WD-wcag-3.0-20260303/) | WCAG 2.2 for gates; APCA advisory only. |
| Model consensus | Some tightly specified artifact benchmarks claim >90% agreement with expert preferences. [artifactsbenchmark.github.io](https://artifactsbenchmark.github.io/) | General LLM judges show order and verbosity bias; subjective UI-feedback studies show low human agreement. [papers.nips.cc](https://papers.nips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf) [people.eecs.berkeley.edu](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf) | Consensus may be used only after local calibration against a narrow rubric and representative human labels. |
| DOM geometry | Geometry precisely computes box relations. [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf) | Geometry does not establish visual observability or intent; invisible padding and clipping create non-observable reports. [eprints.whiterose.ac.uk](https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf) | Keep objective geometry predicates; route visual/intent interpretation to review. |

---

### 4. What changed recently, and what is the trajectory?

- WCAG 3 has progressed in draft form, but its **March 3, 2026** Working Draft status remains explicitly non-normative and subject to change. [w3.org](https://www.w3.org/TR/2026/WD-wcag-3.0-20260303/) ([w3.org](https://www.w3.org/TR/wcag-3.0/))
- Multimodal-judge research is moving toward **fine-grained, criterion-level, evidence-aware evaluation**, including work explicitly identifying perceptual judgement bias—the tendency to accept claims inconsistent with visible evidence. [perception-judge.github.io](https://perception-judge.github.io/) ([perception-judge.github.io](https://perception-judge.github.io/))
- Recent UX-judge benchmarking is beginning to require browser exploration and structured reports before model critique, rather than using screenshots alone. UXBench describes “coverage-gated browser exploration” and evaluates whether critiques support downstream repair. [arxiv.org](https://arxiv.org/abs/2606.16262) ([arxiv.org](https://arxiv.org/abs/2606.16262))
- The practical trajectory is therefore **not** “replace deterministic checks with a stronger vision model.” It is: deterministic measurement first; explicit indeterminate state second; evidence-bounded model review third; calibrated human review for subjective or safety-critical residuals.

<INFERENCE from="ACT’s partial-check semantics, recent browser-exploration UX benchmark design, and perceptual-judge bias research">The durable architecture is staged verification, not monolithic visual scoring: browser measurements establish facts; models convert facts into explanations and prioritize ambiguous queues; humans adjudicate the residual population that neither layer can establish. </INFERENCE> [w3.org](https://www.w3.org/TR/act-rules-format/) [arxiv.org](https://arxiv.org/abs/2606.16262) [perception-judge.github.io](https://perception-judge.github.io/) ([w3.org](https://www.w3.org/TR/act-rules-format/?utm_source=openai))

### Comparison Table

No specific commercial or open-weight judge model was named for procurement. Therefore, the comparison below describes the system layers rather than inventing unstable parameter, context-window, latency, or API-cost figures for unnamed models.

| Evaluation layer | Parameter Count | Context Window | Latency | Cost | License | Technical reality / appropriate authority |
|---|---:|---:|---:|---:|---|---|
| Deterministic browser gate: axe-core | N/A; rule engine | DOM + accessibility tree + rendered CSS context | axe-core documents analysis over **10 seconds** on pages with more than **50,000 elements** on a “relatively decent CPU.” [github.com](https://github.com/dequelabs/axe-core/blob/develop/doc/API.md) | Local compute | MPL-2.0 repository project | Can produce target-level violations, passes, incompletes, and inapplicables; cannot establish full WCAG conformance. |
| Deterministic rendered geometry gate | N/A; browser engine | Current page state plus viewport matrix | <MISSING_DATA>Benchmark required for target app.</MISSING_DATA> | Local/browser infrastructure | Browser-dependent | Best for measurable geometry; must capability-probe engine and fonts. |
| Multimodal/LLM critique layer | Model-dependent | Screenshot, DOM evidence, measurements, rubric | <MISSING_DATA>No selected model or API configuration.</MISSING_DATA> | Model/API-dependent | Model-dependent | Must not be a release authority without task-specific human calibration. |
| Human expert adjudication | N/A | Full product and task context | Variable | Labor cost | N/A | Required for semantic, contextual, and subjective residuals. |

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| WCAG AA contrast threshold is 4.5:1 normal text and 3:1 large text. | W3C, WCAG 2.2 | October 5, 2023 | W3C Recommendation; normative standard | https://www.w3.org/TR/WCAG22/#contrast-minimum |
| WCAG contrast is measured against the specified normal-use background; anti-aliased screen pixels are not the foreground reference. | W3C WAI, Understanding SC 1.4.3 | Current supporting guidance | W3C explanatory guidance | https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html |
| Gradients and images yield a range of contrast values, including W3C passing and failing examples. | W3C WAI, ACT Rule 09o5cg | Current ACT rule | W3C-reviewed informative test rule | https://www.w3.org/WAI/standards-guidelines/act/rules/09o5cg/ |
| WCAG 3 remains a Working Draft rather than an adopted conformance standard. | W3C Accessibility Guidelines Working Group | March 3, 2026 | W3C Working Draft | https://www.w3.org/TR/2026/WD-wcag-3.0-20260303/ |
| APCA is a candidate WCAG 3 method and public beta, not current WCAG conformance. | Myndex / APCA documentation | Current | Algorithm steward documentation | https://git.apcacontrast.com/documentation/minimum_compliance.html |
| axe-core reports 57% automated issue finding in its study. | Deque Systems | March 10, 2021 | Vendor empirical coverage report; methodology disclosed | https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf |
| Numerous WCAG criteria had 0% automated issue detection in the axe coverage study. | Deque Systems | March 10, 2021 | Vendor empirical coverage report | https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf |
| ACT defines passed, failed, cantTell, untested, and inapplicable outcomes. | W3C | Current edition | W3C technical specification | https://www.w3.org/TR/act-rules-format/ |
| ACT rules are partial checks and are informative rather than WCAG conformance determinations. | W3C WAI | Current | W3C explanatory documentation | https://www.w3.org/WAI/standards-guidelines/act/rules/about/ |
| axe returns incomplete where background image prevents determining contrast. | Deque axe-core repository | Current | Maintainer documentation/source repository | https://github.com/dequelabs/axe-core/blob/develop/doc/rule-development.md |
| axe-core says color-contrast is known not to work with JSDOM. | Deque axe-core repository | Current | Maintainer documentation/source repository | https://github.com/dequelabs/axe-core |
| JSDOM returns zero values for many layout properties because layout is out of scope. | jsdom project | Current | Maintainer documentation/source repository | https://github.com/jsdom/jsdom |
| Firefox shorthand computed-style retrieval returned an empty string in documented cross-engine testing. | Mozilla Bugzilla | 2021 test record | Browser-engine bug record with repro | https://bugzilla.mozilla.org/show_bug.cgi?id=137688 |
| ReDeCheck found finding-count inflation and non-observable geometry issues. | Walsh, Kapfhammer, McMinn | 2017 | Peer-reviewed ISSTA paper; foundational, outside requested date window | https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf |
| Verve classifies DOM-reported layout failures as true, false, or non-observable using visual analysis. | Althomali et al. | 2021 | Peer-reviewed Software Testing, Verification and Reliability paper | https://onlinelibrary.wiley.com/doi/10.1002/stvr.1756 |
| GPT-4 UI feedback had 0.603 precision, 0.380 recall, 0.466 F1; human agreement was low. | Duan et al. | 2024 | CHI peer-reviewed study | https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf |
| LLM judges exhibit position, verbosity, and self-enhancement biases. | Zheng et al. | 2023 | NeurIPS peer-reviewed paper | https://papers.nips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf |
| Judge agreement is incomplete even across multiple LLMs. | Shi et al. | June 2024 | Research preprint; large multi-model experiment | https://arxiv.org/abs/2406.07791 |
| Self-critique constrained inappropriate feedback in measured studies. | Burleigh, Han, Dicerbo | October 2025 | Conference proceedings study | https://aclanthology.org/2025.aimecon-sessions.9/ |
| Hybrid static-analysis/LLM triage reduced false positives in an industrial dataset. | Du et al. | January 2026 | Industrial empirical research; 433-alarm dataset | https://arxiv.org/abs/2601.18844 |

---

## Knowledge Gaps

### Missing empirical benchmarks

<MISSING_DATA>A validated benchmark measuring the precision, recall, false-positive rate, and false-negative rate of generic computed-style ancestor-walk contrast algorithms against rendered paint-stack ground truth was not found. Needed: open corpus of gradients, images, opacity stacks, blend modes, shadows, canvas/video backgrounds, and expert/WCAG-labelled contrast outcomes.</MISSING_DATA>

<MISSING_DATA>A current, independent head-to-head accuracy evaluation of axe-core, QualWeb, Alfa, Equal Access, WAVE, and related engines against the same interactive WCAG 2.2-labelled application corpus was not found. Needed: common target-level labels, interactive state coverage, and published rule-to-criterion mappings.</MISSING_DATA>

<MISSING_DATA>A modern, independently replicated over-fire rate for DOM-only responsive-layout checks across SPA frameworks, component libraries, and real browser matrices was not found. Needed: corpus with screenshots, DOM snapshots, intended-design annotations, and root-cause clustering labels.</MISSING_DATA>

### Causal evidence gaps

<INSUFFICIENT_EVIDENCE>Direct production postmortems proving that a specific UI checker converted empty/zero computed browser values into clean measurement outcomes and thereby shipped a defect were not located. Browser-engine and reduced-environment measurement failures are documented, but the checker-to-release causal chain was not verified.</INSUFFICIENT_EVIDENCE>

<INSUFFICIENT_EVIDENCE>No direct study was located showing that a UI-review severity taxonomy alone reduces model false positives or finding-count inflation. The proposed taxonomy is grounded in evidence about indeterminate test outcomes, report duplication, and model bias, but should be validated on the team’s own review corpus.</INSUFFICIENT_EVIDENCE>

### Scope and standardization gaps

<CONFLICTING_EVIDENCE>APCA has substantial practitioner and research interest as a more perceptual contrast method, but it is not a current WCAG conformance method. Teams operating under WCAG 2.2 legal or contractual requirements must keep WCAG 2.x ratio gates even if they add APCA advisory scoring.</CONFLICTING_EVIDENCE>

---

## Recommended Next Steps

1. **Build a contrast-resolution benchmark before implementing a contrast “pass” gate.**  
   **Rationale:** The highest-risk silent error is passing text whose backdrop was never actually resolved. Include gradients, image crops, nested alpha, `backdrop-filter`, masks, blend modes, video/canvas, and cross-origin images; label each target as resolvable, fail, pass, or indeterminate.

2. **Adopt a target-level result contract and publish measurement coverage beside findings.**  
   **Rationale:** Implement the ACT-inspired internal outcomes now. Require every run to report `pass`, `fail`, `could-not-run`, and `not-applicable`, with resolved measurement rate and could-not-run rate.

3. **Create a browser capability matrix and preflight probe suite.**  
   **Rationale:** Test Chromium, Firefox, WebKit if required, and explicitly reject JSDOM for layout/contrast gates. Probe longhand CSS reads, bounding rectangles, font loading, raster screenshot capability, scroll geometry, and shadow DOM access before running substantive assertions.

4. **Calibrate the model-review layer on a human-labelled UI critique set.**  
   **Rationale:** Measure precision by severity, evidence-grounding compliance, order-swap invariance, verbosity sensitivity, duplicate-finding rate, and false claim rate. Do not use model consensus as an acceptance criterion until it outperforms a defined baseline on this local set.

5. **Run an ablation experiment on restraint mechanisms.**  
   **Rationale:** Compare: unrestricted critique; rubric-only critique; evidence-bound critique; evidence-bound critique plus deduplication and severity admission rules. Evaluate the number of fabricated observations, duplicate reports per root cause, high-severity false positives, and human reviewer acceptance.

## Sources

- [Accessibility Conformance Testing (ACT) Rules Format 1.1](https://www.w3.org/TR/act-rules-format/?utm_source=openai)
- [Understanding Success Criterion 1.4.3: Contrast (Minimum) | WAI | W3C](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html?pt=BureoF4GVB&utm_source=openai)
- [axe-core/doc/rule-development.md at develop · dequelabs/axe-core · GitHub](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-development.md?utm_source=openai)
- [Deque - The Automated Accessibility Coverage Report](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf)
- [(PDF) Automated Layout Failure Detection for Responsive Web Pages Without an Explicit Oracle](https://www.researchgate.net/publication/317300653_Automated_Layout_Failure_Detection_for_Responsive_Web_Pages_Without_an_Explicit_Oracle)
- [Generating Automatic Feedback on UI Mockups with Large Language Models](https://people.eecs.berkeley.edu/~bjoern/papers/duan-heuristic-chi2024.pdf)
- [https://papers.nips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf](https://papers.nips.cc/paper_files/paper/2023/file/91f18a1287b398d378ef22505bf41832-Paper-Datasets_and_Benchmarks.pdf)
- [Techniques for WCAG 2.0](https://www.w3.org/WAI/WCAG20/versions/techniques/wcag20-techniques-20081211-a4.pdf?utm_source=openai)
- [Text has enhanced contrast | ACT Rule | WAI | W3C](https://www.w3.org/WAI/standards-guidelines/act/rules/09o5cg/)
- [W3C Accessibility Guidelines (WCAG) 3.0](https://www.w3.org/TR/wcag-3.0/)
- [APCA™ INTEGRATION COMPLIANCE | APCA](https://git.apcacontrast.com/documentation/minimum_compliance.html?utm_source=openai)
- [GitHub - dequelabs/axe-core: Accessibility engine for automated Web UI testing · GitHub](https://github.com/dequelabs/axe-core?utm_source=openai)
- [Deque - The Automated Accessibility Coverage Report](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf?utm_source=openai)
- [GitHub - jsdom/jsdom: A JavaScript implementation of various web standards, for use with Node.js ...](https://github.com/jsdom/jsdom?utm_source=openai)
- [137688 - getPropertyValue on computed style (getComputedStyle) does not do shorthand properties](https://bugzilla.mozilla.org/show_bug.cgi?id=137688&utm_source=openai)
- [1467722 - Don't return null from getComputedStyle when there's no presentation.](https://bugzilla.mozilla.org/show_bug.cgi?id=1467722&utm_source=openai)
- [Automated Layout Failure Detection for Responsive Web Pages Without an Explicit Oracle](https://eprints.whiterose.ac.uk/116989/10/c50-3.pdf)
- [Automated visual classification of DOM‐based presentation failure reports for responsive web page...](https://onlinelibrary.wiley.com/doi/full/10.1002/stvr.1756?utm_source=openai)
- [Beyond the Hint: Using Self-Critique to Constrain LLM Feedback in Conversation-Based Assessment -...](https://aclanthology.org/2025.aimecon-sessions.9/)
- [Reducing False Positives in Static Bug Detection with LLMs: An Empirical Study in Industry](https://arxiv.org/abs/2601.18844)
- [Mitigating Perceptual Judgment Bias in Multimodal LLM-as-a-Judge](https://perception-judge.github.io/)
- [UXBench: Measuring the Actionability of LLM-Generated UX Critiques](https://arxiv.org/abs/2606.16262)
