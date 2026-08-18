---
title: "Automated contrast gating and AST linting policies for generative front-end agents"
run_id: dr_c83a53f20f4d843e
question: "What does the evidence say about building reliable *automated design-generation and design-review pipelines* for coding agents (LLM agents that author HTML/CSS/JS visual artifacts and then verify them), and what are the documented failure modes? I need to defend specific engineering decisions in a rebuilt agent skill. Cover, as separate subtopics: (1) **Automated colour-contrast enforcement** — WCAG 2.x 4.5:1/3:1 vs APCA/WCAG 3 readiness, how automated checkers compute effective contrast against gradients/images/opacity/overlapping layers, the documented false-negative and false-positive rates of automated a11y tooling (axe-core, Lighthouse, IBM Equal Access), and what proportion of real contrast defects automated checks provably cannot see. (2) **Deterministic lint for generated front-end output** — regex/substring heuristics versus real CSS/HTML parsing, published false-positive taxonomies for style linters, and how mature linters handle severity tiers, self-exemption of their own documentation/fixtures, and suppression. (3) **The measurable signature of \"AI-generated\" visual design** — any empirical or perceptual-study evidence about which cues make generated UI detectable to humans (typeface choice, gradient use, spacing regularity, section-structure homogeneity, copy register), and evidence about detection of AI-generated *layouts* specifically rather than images. (4) **Headless-browser verification that silently returns a false clean** — known divergences of non-Chromium/alternative rendering engines and CDP emulation domains, `getComputedStyle` shorthand-vs-longhand behaviour, pseudo-element computed styles, animation/transition execution under headless, and the general engineering practice for distinguishing \"measurement unavailable\" from \"measurement clean\". (5) **Anti-convergence / mode-collapse in LLM design generation** — published evidence that LLMs converge on a narrow aesthetic, measured diversity of LLM-generated design variants, and interventions that demonstrably widen the search (temperature, explicit axis enumeration, forced material/family diversity, discard-your-top-pick protocols). (6) **Content-Security-Policy-constrained sandboxes for published HTML artifacts** — what `connect-src 'self'` / `script-src 'unsafe-eval'` style policies mean for CDN-loaded libraries, web fonts, and inline transpilation, and the documented failure signature when a sandboxed page silently loses a blocked resource. Time horizon: 2023 to now, weighted to 2025-2026. Exclude: design-tool product reviews, Figma plugin ecosystems, generative *image* model comparisons, and general prompt-engineering advice not specific to visual/front-end output."
provider: openai
model: gpt-5.6-terra
tier: fast
archetype: technical
sources: 48
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 3.50
completed: 2026-08-18T01:37:12.802Z
---
## Executive Summary

- **(High Confidence)** Add a **hard WCAG 2.x contrast gate** for determinate, rendered text: fail normal text below **4.5:1**, large text below **3:1**, and required non-text UI boundaries/states below **3:1**. Do **not** substitute APCA/WCAG 3 yet: WCAG 3 remains a Working Draft and explicitly says its contrast algorithm is still undetermined. [w3.org](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum) ([w3.org](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html?locale=en_GB&utm_source=openai)) [w3.org](https://www.w3.org/TR/wcag-3.0/) ([w3.org](https://www.w3.org/TR/wcag-3.0/))

- **(High Confidence)** A contrast result must be tri-state—`PASS`, `FAIL`, or `UNMEASURABLE/REVIEW_REQUIRED`—never binary. axe-core accounts for background opacity but documents that it does not report text over `background-image`, obscuring layers, or images of text; gradients, pseudo-element backgrounds, borders, foreground opacity, and overlays are known difficult cases. A “clean” automated scan is therefore not evidence that these cases pass. [dequeuniversity.com](https://dequeuniversity.com/rules/axe/4.0/color-contrast?application=AxeChrome) ([dequeuniversity.com](https://dequeuniversity.com/rules/axe/4.0/color-contrast?application=AxeChrome&utm_source=openai))

- **(High Confidence)** Replace regex/substrings with **parse-based HTML, CSS, and JavaScript checks**. Use regex only for cheap prefilters or prohibited literal detection after file classification. HTML has specified error-recovery parsing semantics, and mature CSS lint stacks operate on ASTs; regex cannot reliably distinguish a CSS declaration from a comment, Markdown code fence, string, custom syntax, or a generated fixture. [html.spec.whatwg.org](https://html.spec.whatwg.org/multipage/parsing.html) ([html.spec.whatwg.org](https://html.spec.whatwg.org/multipage/parsing.html?utm_source=openai)) [postcss.org](https://postcss.org/docs/postcss-architecture) ([postcss.org](https://postcss.org/docs/postcss-architecture?utm_source=openai))

- **(High Confidence)** Adopt severity tiers and disciplined exemptions: `BLOCKER` for parse failure/security/runtime failures, `ERROR` for deterministic standards violations, `WARNING` for likely design-quality problems, and `ADVISORY` for anti-convergence signals. Exclude documentation, fixtures, vendored files, and generated reports by path before parsing; require narrowly scoped, reasoned suppressions for source artifacts. Stylelint and ESLint both support severity, file ignores, scoped disables, and reporting of needless or undocumented disables. [stylelint.io](https://stylelint.io/user-guide/configure/) ([stylelint.io](https://stylelint.io/user-guide/configure/?utm_source=openai)) [stylelint.io](https://stylelint.io/user-guide/ignore-code/) ([stylelint.io](https://stylelint.io/user-guide/ignore-code/?utm_source=openai)) [eslint.org](https://eslint.org/docs/latest/use/configure/rules) ([eslint.org](https://eslint.org/docs/latest/use/configure/rules?utm_source=openai))

- **(Medium Confidence)** Do **not** hard-ban “AI-looking” cues such as Inter, purple, gradients, centered hero copy, or card grids. The evidence supports a broader risk of LLM design homogenization and lower design-concept diversity than human crowdsourcing, but there is insufficient direct perceptual evidence that any particular front-end cue reliably identifies AI-authored layouts to humans. Make anti-convergence mandatory as a **generation-process constraint**, not an aesthetic police rule. [codesign.berkeley.edu](https://codesign.berkeley.edu/pdfs/papers/ma-llmdiverse-jcise.pdf) ([codesign.berkeley.edu](https://codesign.berkeley.edu/pdfs/papers/ma-llmdiverse-jcise.pdf)) [microsoft.com](https://www.microsoft.com/en-us/research/publication/interrogating-design-homogenization-in-web-vibe-coding/) ([microsoft.com](https://www.microsoft.com/en-us/research/publication/interrogating-design-homogenization-in-web-vibe-coding/))

- **(High Confidence)** Treat headless verification as an instrument with failure states, not as an oracle. Forbid “false-clean” conclusions from a single screenshot, a single engine, shorthand `getComputedStyle()` reads, default animation-disabled snapshots, or tests that ignore console errors, page crashes, failed requests, font-load status, CSP violations, and unavailable measurements. CSSOM permits shorthand serialization to be empty, Playwright disables animations by default for screenshot assertions, and Chromium’s headless implementation has documented output differences. [w3.org](https://www.w3.org/TR/cssom-1/) ([w3.org](https://www.w3.org/TR/cssom-1/?utm_source=openai)) [playwright.dev](https://playwright.dev/docs/api/class-pageassertions) ([playwright.dev](https://playwright.dev/docs/api/class-pageassertions?utm_source=openai)) [github.com](https://github.com/microsoft/playwright/issues/33566) ([github.com](https://github.com/microsoft/playwright/issues/33566?utm_source=openai))

- **(High Confidence)** In CSP-constrained published-artifact sandboxes, require **self-contained/local assets** by default. `connect-src 'self'` governs script-initiated connections, not `<script src>` or font loading; external scripts, stylesheet-hosted web fonts, and inline transpilers require separately compatible `script-src`, `style-src`, and `font-src` policies. `unsafe-eval` permits string-to-code execution but does not authorize an unapproved CDN or ordinary inline script. [w3.org](https://www.w3.org/TR/CSP/) ([w3.org](https://www.w3.org/TR/CSP/)) [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src) ([developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src?utm_source=openai))

---

## Detailed Findings

### What does the evidence say about automated colour-contrast enforcement for coding-agent pipelines?

#### Decision

**(High Confidence)** Implement a hard contrast gate for rendered, analyzable content using WCAG 2.x thresholds:

| Target | Hard gate | Rationale | Gate outcome |
|---|---:|---|---|
| Normal text and images of text | `>= 4.5:1` | WCAG 2.x AA minimum | `PASS` / `FAIL` |
| Large text | `>= 3:1` | WCAG 2.x AA minimum | `PASS` / `FAIL` |
| Required non-text UI components, focus indicators, and graphical boundaries | `>= 3:1` | WCAG 2.x non-text contrast model | `PASS` / `FAIL` |
| Text on gradients, photos, video, canvas, opaque overlays, or complex stacked layers | No automatic pass without reliable per-pixel analysis | Static foreground/background pairing is not sufficient | `REVIEW_REQUIRED` or `FAIL_BY_POLICY` |
| WCAG 3 / APCA | Advisory experimentation only | WCAG 3 is non-final; its contrast algorithm remains undecided | Never a compliance replacement |

WCAG 2.2 requires **4.5:1** for normal text and **3:1** for large text, treating the values as unrounded thresholds: `4.499:1` fails. [w3.org](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum) ([w3.org](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html?locale=en_GB&utm_source=openai)) WCAG’s sufficient technique describes measuring the background pixels immediately adjacent to glyphs where backgrounds or letters vary in luminance, rather than comparing one global foreground/background token pair. [w3.org](https://www.w3.org/WAI/WCAG22/Techniques/general/G18) ([w3.org](https://www.w3.org/WAI/WCAG22/Techniques/general/G18?utm_source=openai))

**(High Confidence)** WCAG 3/APCA is not ready to replace WCAG 2.x gating. The March 3, 2026 WCAG 3 Working Draft says publication is not endorsement and that the contrast algorithm is “yet to be determined”; “APCA” does not appear as an adopted algorithm in that draft. [w3.org](https://www.w3.org/TR/wcag-3.0/) ([w3.org](https://www.w3.org/TR/wcag-3.0/?utm_source=openai))

#### What automated contrast tools actually compute

**(High Confidence)** A check based only on CSS source colors is weaker than a rendered-scene check. The WCAG technique expects a contrast measurement at the letter/background boundary; therefore gradients, photographs, overlays, and blending require evaluating the effective rendered pixels near each glyph. [w3.org](https://www.w3.org/WAI/WCAG22/Techniques/general/G18) ([w3.org](https://www.w3.org/WAI/WCAG22/Techniques/general/G18?utm_source=openai))

**(High Confidence)** axe-core’s documented `color-contrast` rule accounts for **background transparency and opacity**, but explicitly identifies foreground opacity, CSS gradients, pseudo-element backgrounds, borders used as backgrounds, overlapping foreground elements, and off-viewport positioned elements as difficult. It does not report text with a `background-image`, text obscured by another element, or images of text. [dequeuniversity.com](https://dequeuniversity.com/rules/axe/4.0/color-contrast?application=AxeChrome) ([dequeuniversity.com](https://dequeuniversity.com/rules/axe/4.0/color-contrast?application=AxeChrome&utm_source=openai))

<INFERENCE from="W3C G18 pixel-adjacent measurement requirement; axe-core documented exclusions for background-image and obscuring layers">A coding-agent gate should not label a variable-background text region as clean merely because a declared `color` and an ancestor `background-color` have acceptable contrast. The gate should emit `REVIEW_REQUIRED`; for an autonomous publish pipeline, convert that state to a release block unless the text sits on a declared opaque backing surface.</INFERENCE>

#### What the tools’ coverage data does—and does not—prove

| Tool / study | Measured evidence | What it supports | What it does **not** support |
|---|---|---|---|
| axe-core / Deque coverage report | In Deque’s 13,000+-page-state, nearly 300,000-issue audit dataset, automated testing found **57.38%** of all issues; for WCAG 1.4.3 contrast, it found **73,733 of 88,714** issues, while **14,981** were manual. [deque.com](https://www.deque.com/automated-accessibility-coverage-report/) ([deque.com](https://www.deque.com/automated-accessibility-coverage-report/)) | In that dataset, **16.89%** of recorded minimum-contrast defects were not automatically found. | A universal axe-core recall rate, a per-rule false-negative rate, or a general false-positive rate. |
| Lighthouse | Lighthouse’s accessibility score is a weighted average of binary audits, with weights based on axe user-impact assessments; manual and low-impact audits are excluded from the score. [developer.chrome.com](https://developer.chrome.com/docs/lighthouse/accessibility/scoring) ([developer.chrome.com](https://developer.chrome.com/docs/lighthouse/accessibility/scoring?authuser=9)) | A 100 Lighthouse score is only a pass on included automated audits. | Independent validation of axe-core, comprehensive WCAG conformance, or a “no contrast defects” conclusion. |
| IBM Equal Access | IBM directs users to stop on `Violations` or `Needs Review`, then proceed to manual and screen-reader testing after clean automation because automated checks cover only a subset of requirements. [ibm.com](https://www.ibm.com/able/toolkit/verify/automated/) ([ibm.com](https://www.ibm.com/able/toolkit/verify/automated/)) | A three-way outcome model—violation, review, clean—is operationally mature. | A published IBM-wide precision/recall rate for contrast. |
| Pool, W4A 2023 | Across nine tools and 121 pages, every tool found issues missed by others; 49 of 1,089 attempted page-tool tests, **4%**, failed. [jpdev.pro](https://jpdev.pro/jpdev/pub/pubs/etc/accessibility-metatesting.pdf) ([jpdev.pro](https://jpdev.pro/jpdev/pub/pubs/etc/accessibility-metatesting.pdf)) | Tool outputs are complementary; operational failure itself suppresses discovery. | That running all tools eliminates manual testing. |

**(High Confidence)** The strongest quantified answer to “what proportion cannot automated checks see?” is conditional, not universal: Deque’s audit dataset reports that **42.62%** of all issues and **16.89%** of its recorded WCAG 1.4.3 contrast issues were manual rather than automatically detected. These are observed audit shares, not portable false-negative rates for every page, implementation, or tool version. [deque.com](https://www.deque.com/automated-accessibility-coverage-report/) ([deque.com](https://www.deque.com/automated-accessibility-coverage-report/))

<MISSING_DATA>Peer-reviewed, tool-version-specific precision, recall, false-positive, and false-negative rates for axe-core, Lighthouse, and IBM Equal Access specifically on rendered contrast defects involving gradients, images, opacity, and occlusion were sought. No directly comparable, recent validated benchmark was found. A benchmark would need a labeled corpus of rendered DOM states with expert pixel-level contrast adjudication, including complex compositing cases.</MISSING_DATA>

#### Recommended contrast policy

```text
CONTRAST-001 [ERROR]
For each visible text run in a supported rendered state:
  if effective background is determinately a solid/composited color:
      calculate WCAG 2 contrast
      fail if below applicable threshold
  else:
      emit CONTRAST-UNMEASURABLE

CONTRAST-UNMEASURABLE [BLOCKER in autonomous publishing]
Text may not pass automatically when its backdrop includes:
  background-image, gradient, video, canvas, filter, blend mode,
  unbounded opacity composition, pseudo-element backdrop, or occlusion.

Resolution:
  add an opaque backing layer with verified contrast;
  or collect a pixel-sampled rendered proof across all states and viewports;
  or require human accessibility review.
```

**(High Confidence)** This is stricter than axe-core’s documented behavior by design: it prevents an agent from converting an unsupported analysis case into a false clean. [dequeuniversity.com](https://dequeuniversity.com/rules/axe/4.0/color-contrast?application=AxeChrome) ([dequeuniversity.com](https://dequeuniversity.com/rules/axe/4.0/color-contrast?application=AxeChrome&utm_source=openai))

---

### What does the evidence say about deterministic lint for generated front-end output?

#### Decision

**(High Confidence)** Use a parser/AST as the enforcement substrate:

1. Parse HTML using an HTML5-compatible parser or browser DOM parser.
2. Parse CSS with PostCSS-compatible syntax appropriate to the artifact.
3. Parse JavaScript with an ECMAScript parser.
4. Run policy rules against AST nodes and source-file classes.
5. Reserve regex for prefiltering, literal bans, or post-parse value checks—not structural interpretation.

The HTML Standard defines a parser and well-defined error handling for `text/html`; a string search cannot reproduce DOM construction, implicit nodes, recovery, or element context. [html.spec.whatwg.org](https://html.spec.whatwg.org/multipage/parsing.html) ([html.spec.whatwg.org](https://html.spec.whatwg.org/multipage/parsing.html?utm_source=openai)) PostCSS describes its parser as producing an AST consumed by tools including Stylelint, Autoprefixer, and CSSnano. [postcss.org](https://postcss.org/docs/postcss-architecture) ([postcss.org](https://postcss.org/docs/postcss-architecture?utm_source=openai))

| Approach | Reliable for | Failure modes | Policy status |
|---|---|---|---|
| Regex / substring scan | Literal prohibited URLs, known exact tokens, simple file-path routing | Matches comments/docs/examples; misses escaped, minified, reordered, computed, inherited, or custom-syntax cases; cannot establish HTML/CSS structure | Allowed only as a prefilter or narrow literal check |
| HTML/CSS/JS AST | Tags, attributes, CSS declarations, selectors, import nodes, script nodes, locations | Requires syntax selection and explicit handling of templates/embedded languages | Required |
| Rendered-browser inspection | Cascaded values, layout, loaded fonts, interactions, runtime/CSP effects | Engine/version/state/environment dependence; unsupported measurement risks | Required for visual/runtime claims |
| Screenshot-only judgment | Human review aid and regression artifact | Cannot prove semantic, interactive, accessibility, loading, or state correctness | Never a release gate alone |

**(High Confidence)** Mature lint systems also model the operational problem the proposed gate faces: Stylelint supports custom syntax for embedded CSS, ignores by file pattern, error/warning severity, scoped disables, descriptions, and reports for needless, invalid, unscoped, or descriptionless suppressions. [stylelint.io](https://stylelint.io/user-guide/configure/) ([stylelint.io](https://stylelint.io/user-guide/configure/?utm_source=openai)) [stylelint.io](https://stylelint.io/user-guide/options/) ([stylelint.io](https://stylelint.io/user-guide/options/?utm_source=openai)) [stylelint.io](https://stylelint.io/user-guide/ignore-code/) ([stylelint.io](https://stylelint.io/user-guide/ignore-code/?utm_source=openai)) ESLint likewise supports rule severities and file-scoped configuration, and states that CI-enforced rules are normally errors because they cause a nonzero exit. [eslint.org](https://eslint.org/docs/latest/use/configure/rules) ([eslint.org](https://eslint.org/docs/latest/use/configure/rules?utm_source=openai))

#### False-positive taxonomy and suppression policy

**(Medium Confidence)** Recent front-end-linter literature does not provide a single accepted quantitative false-positive taxonomy tailored to generated HTML/CSS. However, documented Stylelint cases show a recurring class: correct or required syntax in one language/toolchain context is misclassified by a generic rule—for example, a Sass mixed-declarations migration pattern triggering `no-duplicate-selectors`. [github.com](https://github.com/stylelint/stylelint/issues/7893) ([github.com](https://github.com/stylelint/stylelint/issues/7893?utm_source=openai))

Use this practical taxonomy:

| False-positive class | Example | Mitigation |
|---|---|---|
| Non-source content | Rule wording appears in Markdown, docs, prompt fixtures, snapshots | Classify and exclude `docs/**`, `fixtures/**`, `examples/**`, `dist/**`, lockfiles before lint |
| Embedded language | CSS in `<style>`, CSS-in-JS template literals, Markdown fences | Parse using declared custom syntax and source type |
| Framework/custom syntax | CSS Modules, Sass, utility directives, custom elements | Add parser/plugin support or a scoped rule exception |
| Intentional design exception | A necessary `!important`, animation, visual treatment, legacy selector | Allow a single-node suppression with rule ID, reason, owner, and expiry |
| Detector uncertainty | Raster backdrop, runtime-generated DOM, third-party widget | Emit `REVIEW_REQUIRED`, not a false `PASS` or a source-style error |

<INSUFFICIENT_EVIDENCE>A statistically validated, front-end-specific taxonomy assigning false-positive rates to regex gates, CSS AST rules, and rendered-browser checks could not be corroborated in the requested period. The taxonomy above is an engineering classification assembled from mature-linter mechanisms and reported rule-context failures, rather than a published rate model.</INSUFFICIENT_EVIDENCE>

#### Recommended severity model

| Tier | CI behavior | Examples |
|---|---|---|
| `BLOCKER` | Cannot publish | HTML/CSS/JS parse failure; CSP resource block; uncaught runtime exception; page crash; contrast unmeasurable in autonomous release; missing required local asset |
| `ERROR` | Fails build | WCAG contrast below threshold; forbidden remote asset; invalid semantic structure; unsafe inline transpiler; unapproved suppression |
| `WARNING` | Build passes, review queue created | Excessive visual repetition; unapproved gradient; unsupported responsive state; probable generic copy |
| `ADVISORY` | Informational only | Typeface-family concentration; likely default aesthetic; optional design-system deviation |

**(High Confidence)** Do not lint your own policy prose or fixtures with source rules. The routing rule should be explicit and precede parsing:

```text
lint_targets = artifacts/**/*.html, artifacts/**/*.css, artifacts/**/*.js
exclude      = docs/**, fixtures/**, examples/**, reports/**, vendor/**, dist/**
```

<INFERENCE from="Stylelint ignoreFiles and .stylelintignore support; Stylelint custom syntax support; ESLint file-scoped configuration">A source-classification phase removes the dominant “gate fires on its own documentation” failure mode more reliably than adding ever-more-exact regex exclusions.</INFERENCE>

---

### What is the measurable signature of “AI-generated” visual design, especially layouts?

#### Decision

**(Medium Confidence)** Do not claim that a specific typography choice, gradient, spacing scale, three-card section, or copy register proves a UI was AI-generated. The evidence supports **homogenization risk**, not a dependable human-detectable signature for individual front-end layouts.

A 2025 study generated 4,000 GPT-4 design concepts across five topics and found human crowdsourced concepts consistently more diverse than LLM-generated concepts across its metrics. It found `temperature = 1` and `top-p = 1` produced the most diverse LLM sets in that experiment, but prompt interventions had more effect than parameter changes; a critique-based generation/editing method had the highest diversity among tested prompting methods while still not reaching human diversity. [codesign.berkeley.edu](https://codesign.berkeley.edu/pdfs/papers/ma-llmdiverse-jcise.pdf) ([codesign.berkeley.edu](https://codesign.berkeley.edu/pdfs/papers/ma-llmdiverse-jcise.pdf))

Microsoft Research’s March 2026 work frames web vibe-coding homogenization as a sociotechnical risk and argues that frictionless generation can exacerbate it; this is a design-risk analysis and case-study mitigation proposal, not a controlled measurement of human detection accuracy for layouts. [microsoft.com](https://www.microsoft.com/en-us/research/publication/interrogating-design-homogenization-in-web-vibe-coding/) ([microsoft.com](https://www.microsoft.com/en-us/research/publication/interrogating-design-homogenization-in-web-vibe-coding/))

<MISSING_DATA>Controlled perceptual studies were sought in which participants identify AI-authored versus human-authored HTML/CSS/JS layouts while isolating cues such as typeface, gradients, spacing regularity, repeated card geometry, section homogeneity, and copy register. No sufficiently rigorous, recent study establishing reliable cue-by-cue detection rates was corroborated.</MISSING_DATA>

#### What to hard-enforce instead

**(Medium Confidence)** Make anti-convergence a hard **workflow** rule, but keep visual “slop” cues as warnings unless they violate an approved design brief.

```text
VARIANT-001 [BLOCKER]
Generate at least three candidate directions before selection.

VARIANT-002 [BLOCKER]
Each candidate must differ on at least two declared axes:
  layout archetype;
  typography family/class;
  color strategy;
  surface/material treatment;
  information hierarchy;
  imagery/illustration strategy;
  density and whitespace strategy.

VARIANT-003 [ERROR]
Candidate metadata must declare its axis values and reference screenshot hashes.

VARIANT-004 [WARNING]
Flag variants whose DOM section sequence, typography stack,
token set, and component geometry are near-duplicates.
```

<INFERENCE from="Ma et al. 2025: LLM design concepts were less diverse than human concepts; critique-based prompting improved diversity; Microsoft Research 2026: productive friction may counter web-vibe-coding homogenization">Mandatory structured divergence is defensible; a hard ban on individual fashionable visual cues is not. The former targets measured output concentration, while the latter would encode unsupported taste claims and create avoidable false positives.</INFERENCE>

#### Grep-checkable anti-slop rules: appropriate and inappropriate uses

| Rule wording | Machine check | Recommended tier | Reason |
|---|---|---|---|
| “No remote font URL unless allowlisted.” | AST URL extraction / `@font-face src` inspection | `ERROR` | Deployment reliability/security rule |
| “No `linear-gradient()`, `radial-gradient()`, or `conic-gradient()` unless the design brief explicitly allows gradients.” | CSS AST declaration-value inspection | `WARNING`, then `ERROR` only under a no-gradient brief | Objective and reviewable; not intrinsically a quality defect |
| “Typography must use an approved font stack.” | CSS AST `font-family` inspection | `ERROR` when a brand system exists | Brand conformance, not AI detection |
| “Do not use Inter.” | String/AST check | `ADVISORY` only | No direct evidence supports treating it as an AI-authorship signal |
| “Avoid generic copy.” | Not reliably grep-checkable | Human/LLM review queue | Requires semantic judgment |
| “Do not make every section a centered heading plus equal cards.” | DOM/layout similarity metric | `WARNING` | More meaningful than a gradient/font ban, but still heuristic |

**(High Confidence)** Do not make “discard your top pick” mandatory on the claim that it is empirically proven to widen front-end design search. The reviewed evidence supports critique-and-revision and deliberate divergence; it does not directly validate that specific protocol for HTML/CSS layout diversity. [codesign.berkeley.edu](https://codesign.berkeley.edu/pdfs/papers/ma-llmdiverse-jcise.pdf) ([codesign.berkeley.edu](https://codesign.berkeley.edu/pdfs/papers/ma-llmdiverse-jcise.pdf))

---

### What headless-browser measurements silently return a false clean, and what should be forbidden?

#### Decision

**(High Confidence)** A measurement must return one of `PASS`, `FAIL`, or `UNAVAILABLE`; unavailable evidence must not be coerced to clean.

```json
{
  "check_id": "visual.background-composition",
  "status": "PASS | FAIL | UNAVAILABLE",
  "engine": "chromium",
  "engine_version": "pinned-version",
  "headless_mode": "new-headless | shell | headed",
  "viewport": {"width": 1440, "height": 900, "dpr": 1},
  "states_tested": ["default", "hover", "focus-visible"],
  "evidence": {"screenshot": "sha256:...", "computed_longhands": {}},
  "unavailable_reason": null
}
```

<INFERENCE from="CSSOM’s specification of empty shorthand serialization; Playwright’s documented animation disabling; documented headless implementation differences">This schema is necessary because a browser API can legitimately return an empty or state-dependent value, while a browser runner can alter rendering behavior. Treating either as “no problem” creates false-clean results.</INFERENCE>

#### Prohibited false-clean measurements

| Forbidden conclusion | Why it is invalid | Replacement |
|---|---|---|
| “`getComputedStyle(el).background` is empty, so no background exists.” | CSSOM permits a shorthand serialization to return an empty string when it cannot exactly represent all longhand values. [w3.org](https://www.w3.org/TR/cssom-1/) ([w3.org](https://www.w3.org/TR/cssom-1/?utm_source=openai)) | Query `background-color`, `background-image`, `background-position`, `background-size`, `background-repeat`, `opacity`, `filter`, and stacking context longhands separately. |
| “One screenshot proves visual correctness.” | Chromium headless modes have documented differences in screenshots, PDFs, GPU/WebGL behavior, and performance. [github.com](https://github.com/microsoft/playwright/issues/33566) ([github.com](https://github.com/microsoft/playwright/issues/33566?utm_source=openai)) | Pin browser engine/version/mode; test critical artifacts in a headed Chromium canary plus required target engines. |
| “A default Playwright snapshot proves animation/motion is clean.” | Playwright screenshot assertions disable animations by default; finite animations are fast-forwarded and infinite ones canceled for the capture. [playwright.dev](https://playwright.dev/docs/api/class-pageassertions) ([playwright.dev](https://playwright.dev/docs/api/class-pageassertions?utm_source=openai)) | Run separate motion tests with animations allowed, deterministic virtual time, and `prefers-reduced-motion: reduce`. |
| “Pseudo-element styling was not measured because the element lacks a child node.” | `getComputedStyle(element, "::before")` and `::after` are supported APIs. [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle.) ([developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle.?utm_source=openai)) | Explicitly inspect `::before`, `::after`, `::marker`, and state-dependent pseudo-elements where relevant. |
| “A single Chromium CDP emulation run proves mobile/Safari behavior.” | CDP is for Chromium/Blink instrumentation; its tip-of-tree protocol changes frequently and has no backwards-compatibility guarantee. [chromedevtools.github.io](https://chromedevtools.github.io/devtools-protocol/index.html) ([chromedevtools.github.io](https://chromedevtools.github.io/devtools-protocol/index.html?utm_source=openai)) | Treat CDP emulation as a Chromium test environment, not device/browser equivalence; run target-engine tests separately. |
| “No browser exception means the inspection worked.” | Playwright has documented WebKit failures, including a 2026 regression in which reading a complex computed `background` shorthand crashed the render process. [github.com](https://github.com/microsoft/playwright/issues/41573) ([github.com](https://github.com/microsoft/playwright/issues/41573?utm_source=openai)) | Subscribe to page crash, console error, unhandled page error, failed request, and test-timeout events; fail closed. |

**(High Confidence)** `getComputedStyle()` returns resolved values and can inspect pseudo-elements, but a longhand-specific query is more reliable for analysis than depending on shorthand serialization. [w3.org](https://www.w3.org/TR/cssom-1/) ([w3.org](https://www.w3.org/TR/cssom-1/?utm_source=openai)) [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle.) ([developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle.?utm_source=openai))

#### Required headless verification contract

```text
BROWSER-001 [BLOCKER]
Fail if page crash, uncaught page exception, failed same-origin asset request,
CSP violation, or required font failure occurs.

BROWSER-002 [BLOCKER]
Fail if a required visual measurement is UNAVAILABLE.

BROWSER-003 [ERROR]
For every check, record browser engine, exact version, headless mode,
viewport, DPR, color scheme, reduced-motion preference, and checked states.

BROWSER-004 [ERROR]
Do not use CSS shorthands as the only source for background, font, border,
animation, transform, or transition measurements.

BROWSER-005 [ERROR]
Do not use a screenshot with default animation suppression as proof that
motion behavior, focus visibility, or transition end-states are correct.
```

---

### What does the evidence say about anti-convergence or mode collapse in LLM design generation?

#### Decision

**(Medium Confidence)** Make anti-convergence mandatory for variant generation, but define success as **documented structural and semantic diversity**, not “avoid whatever currently looks AI-generated.”

The strongest directly relevant study found lower diversity in GPT-4-generated design concepts than human crowdsourced concepts across five problems; generation parameters changed diversity, but critique-based prompting and targeted prompt structure had larger effects in that study. [codesign.berkeley.edu](https://codesign.berkeley.edu/pdfs/papers/ma-llmdiverse-jcise.pdf) ([codesign.berkeley.edu](https://codesign.berkeley.edu/pdfs/papers/ma-llmdiverse-jcise.pdf))

**(Medium Confidence)** Temperature alone should not be your anti-mode-collapse control. In the study, `temperature=1` and `top-p=1` yielded the most diverse LLM set among tested combinations, but the authors report that prompt-structure interventions had a greater observed effect than parameter combinations. [codesign.berkeley.edu](https://codesign.berkeley.edu/pdfs/papers/ma-llmdiverse-jcise.pdf) ([codesign.berkeley.edu](https://codesign.berkeley.edu/pdfs/papers/ma-llmdiverse-jcise.pdf))

| Intervention | Evidence strength | Pipeline decision |
|---|---|---|
| Increase temperature / top-p | Medium: parameter settings affected diversity in one GPT-4 design-concept study | Use as a controlled exploration variable; record settings |
| Generate candidates over explicit design axes | Medium: reasoned anti-convergence mechanism; not independently measured as a front-end-layout intervention | Mandatory |
| Critique then revise / self-edit variants | Medium: highest diversity among tested prompt approaches in the cited study | Mandatory for one candidate refinement pass |
| Force different material/type/layout families | Medium-Low: sensible operationalization of axis diversity, but not directly benchmarked as an independent treatment | Mandatory metadata constraint |
| Discard-the-top-pick protocol | Low: no corroborated direct evidence | Optional experiment, not a policy mandate |

<INSUFFICIENT_EVIDENCE>No recent controlled benchmark was corroborated that measures diversity specifically across multiple fully rendered HTML/CSS/JS website variants while independently varying temperature, material-family constraints, axis enumeration, and discard-first-selection protocols.</INSUFFICIENT_EVIDENCE>

#### Recommended hard diversity gate

```text
DIVERSITY-001 [BLOCKER]
Each task must produce 3–5 candidates before selection.

DIVERSITY-002 [BLOCKER]
No two candidates may share all of:
  layout archetype,
  typography classification,
  palette strategy,
  surface strategy,
  section order,
  visual-density class.

DIVERSITY-003 [ERROR]
The reviewer must receive a side-by-side render plus a machine-readable
variant manifest before selecting a candidate.

DIVERSITY-004 [WARNING]
Flag near-duplicate candidates by:
  DOM tree similarity,
  section-order similarity,
  CSS-token overlap,
  screenshot perceptual-hash similarity.
```

**(Medium Confidence)** The anti-convergence gate should fail the *generation run* when all variants collapse into one family, but should not fail a selected artifact merely because it uses a common font or gradient that is allowed by the approved brief. [microsoft.com](https://www.microsoft.com/en-us/research/publication/interrogating-design-homogenization-in-web-vibe-coding/) ([microsoft.com](https://www.microsoft.com/en-us/research/publication/interrogating-design-homogenization-in-web-vibe-coding/))

---

### What does the evidence say about CSP-constrained sandboxes for published HTML artifacts?

#### Decision

**(High Confidence)** Publish generated artifacts as self-contained or locally bundled packages. Do not recommend CDN JavaScript libraries, remote web fonts, or browser-side transpilers unless the sandbox policy explicitly allowlists every required fetch class and the artifact is verified under that exact final policy.

| Requirement / policy | Actual consequence | Pipeline rule |
|---|---|---|
| `connect-src 'self'` | Restricts script-initiated connections such as `fetch`, XHR, WebSocket, EventSource, Beacon, and related interfaces—not ordinary `<script src>` loading. [w3.org](https://www.w3.org/TR/CSP/) ([w3.org](https://www.w3.org/TR/CSP/)) | Do not infer that a CDN script is allowed because `connect-src` permits self. |
| `script-src 'self'` | External CDN scripts are blocked unless their origin is separately allowed; ordinary inline scripts are blocked unless authorized by nonce/hash or unsafe inline policy. [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy) ([developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy?no_head=1&utm_source=openai)) | Bundle local scripts; use external scripts only by explicit policy exception. |
| `unsafe-eval` | Allows `eval()`, `Function()`, and string compilation paths; it does not authorize blocked URLs or ordinary inline scripts. [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src) ([developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src?utm_source=openai)) | Do not enable merely to make agent output work. |
| `font-src 'self'` | Blocks remote font resources not sourced from self. [w3.org](https://www.w3.org/TR/CSP/) ([w3.org](https://www.w3.org/TR/CSP/)) | Self-host approved fonts or use system-font stacks. |
| Remote Google-font-style stylesheet | Requires compatible stylesheet permission **and** compatible font-resource permission. | Avoid by default; localize the CSS and WOFF2 assets. |
| `@babel/standalone` / `type="text/babel"` | Babel Standalone automatically compiles and executes browser-side Babel scripts. [babeljs.io](https://babeljs.io/docs/babel-standalone/) ([babeljs.io](https://babeljs.io/docs/babel-standalone/?utm_source=openai)) | Ban from published artifacts; transpile before publication. |

**(High Confidence)** The failure signature is commonly visual degradation rather than a page-level crash: a blocked script may leave controls inert; a blocked font causes fallback typography and layout shifts; a blocked stylesheet removes intended styling; a blocked fetch may leave an empty widget. The CSP specification requires blocked `connect-src` fetches to return network errors and provides `SecurityPolicyViolationEvent` data for violation handling and reporting. [w3.org](https://www.w3.org/TR/CSP/) ([w3.org](https://www.w3.org/TR/CSP/))

#### Mandatory final-policy test

```text
CSP-001 [BLOCKER]
Serve the artifact with the exact production CSP header/meta policy.

CSP-002 [BLOCKER]
Capture:
  - SecurityPolicyViolationEvent entries,
  - console CSP errors,
  - failed requests and blocked URLs,
  - document.fonts.ready completion,
  - required document.fonts.check(...) results,
  - runtime errors and failed dynamic imports.

CSP-003 [ERROR]
No external script, style, font, image, fetch endpoint, WebSocket,
iframe, or module import may be used unless it appears in an explicit
per-artifact allowlist and passes the final-policy test.

CSP-004 [ERROR]
Disallow browser-side transpilation (`text/babel`, Babel Standalone,
TypeScript compilers, eval-based loaders) in published artifacts.
```

<INFERENCE from="CSP Level 3 directive-specific resource restrictions; Babel Standalone browser compilation behavior">A sandbox that permits a preview to render without recording CSP violations can silently ship a visually degraded or nonfunctional artifact. CSP verification must therefore be part of the same release gate as screenshot and DOM verification, not a separate security-only check.</INFERENCE>

### Technical comparison: pipeline components, not foundation-model selection

No named model/API was in scope; therefore parameter count, context window, vendor latency, and token cost cannot be responsibly compared. <MISSING_DATA>No fixed model vendor, model version, API schema, rate limit, or deployment region was specified. Those values are provider- and date-specific and should be benchmarked only after selecting candidate models.</MISSING_DATA>

| Component | Parameter Count | Context Window | Latency | Cost | License / source posture |
|---|---:|---:|---:|---:|---|
| HTML/CSS/JS AST lint | N/A | N/A | Workload-dependent; no universal published latency | Local CI compute | HTML Standard / PostCSS ecosystem; parse-based |
| axe-core/Lighthouse audit | N/A | N/A | Page-state dependent | Local CI compute | axe-core-derived checks; Lighthouse is open source |
| Browser rendering / Playwright | N/A | N/A | Browser, page, font, animation, and hardware dependent | Local CI compute | Chromium/Firefox/WebKit runner stack |
| CSP policy test | N/A | N/A | Network and asset dependent | Local CI compute | W3C CSP standard |
| LLM variant generator | Not selected | Not selected | <MISSING_DATA> | <MISSING_DATA> | Must be benchmarked separately |

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| WCAG 2.2 normal text threshold is 4.5:1; large text is 3:1; values are not rounded | W3C WAI | Updated November 18, 2025 | W3C standards guidance; primary normative interpretation | https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum |
| Pixel-adjacent measurement is needed where backgrounds vary | W3C WAI | Updated November 18, 2025 | W3C sufficient technique; primary standards implementation guidance | https://www.w3.org/WAI/WCAG22/Techniques/general/G18 |
| WCAG 3 contrast algorithm is not yet determined | W3C Accessibility Guidelines Working Group | March 3, 2026 | W3C Working Draft; primary but explicitly non-final | https://www.w3.org/TR/wcag-3.0/ |
| axe-core accounts for background opacity but excludes/struggles with background images, gradients, occlusion, pseudo-elements, and other complex scenes | Deque axe rule documentation | Undated, accessed August 18, 2026 | Maintainer rule documentation; primary tool behavior source | https://dequeuniversity.com/rules/axe/4.0/color-contrast?application=AxeChrome |
| Deque audit dataset found 57.38% automated issue coverage and 83.11% automated share for WCAG 1.4.3 issues | Deque Systems | Undated, accessed August 18, 2026 | Vendor audit dataset; useful quantitative evidence but not independent | https://www.deque.com/automated-accessibility-coverage-report/ |
| Lighthouse is a weighted average of axe-based binary audits and excludes manual audits from score | Chrome for Developers | Updated 2025 | Official tool documentation; primary | https://developer.chrome.com/docs/lighthouse/accessibility/scoring |
| IBM automation produces Violations/Needs Review and requires manual/screen-reader testing afterwards | IBM | Undated, accessed August 18, 2026 | Official tool-process guidance; primary | https://www.ibm.com/able/toolkit/verify/automated/ |
| Nine a11y tools had complementary issue discovery; 4% of attempted runs failed | Jonathan Robert Pool, ACM W4A | April 30, 2023 | Peer-reviewed conference paper | https://jpdev.pro/jpdev/pub/pubs/etc/accessibility-metatesting.pdf |
| Browser HTML parsing uses specified recovery behavior | WHATWG | Living Standard, accessed August 18, 2026 | Primary web-platform specification | https://html.spec.whatwg.org/multipage/parsing.html |
| PostCSS tooling uses a CSS AST, including Stylelint ecosystem tools | PostCSS | Undated, accessed August 18, 2026 | Maintainer architecture documentation; primary | https://postcss.org/docs/postcss-architecture |
| Stylelint supports severity, ignores, custom syntax, scoped disables, and disable-reporting controls | Stylelint | Undated, accessed August 18, 2026 | Official project documentation; primary | https://stylelint.io/user-guide/configure/ |
| GPT-4 design concepts were less diverse than human crowdsourced concepts; critique-based intervention improved LLM diversity | Ma, Grandi, McComb, Goucher-Lambert | February 2025; online December 23, 2024 | Peer-reviewed ASME journal article | https://codesign.berkeley.edu/pdfs/papers/ma-llmdiverse-jcise.pdf |
| Web vibe coding may create design homogenization; productive friction is proposed as mitigation | Shin et al., Microsoft Research | March 2026 | Research preprint/research analysis; direct subject relevance but not controlled perception trial | https://www.microsoft.com/en-us/research/publication/interrogating-design-homogenization-in-web-vibe-coding/ |
| CSSOM shorthand serialization can return empty string; `getComputedStyle` accepts pseudo-element argument | W3C CSSWG | Living specification, accessed August 18, 2026 | Primary web-platform specification | https://www.w3.org/TR/cssom-1/ |
| Playwright default screenshot behavior disables animations | Microsoft Playwright | Undated, accessed August 18, 2026 | Official API documentation; primary | https://playwright.dev/docs/api/class-pageassertions |
| Chromium headless mode has documented differences in screenshots, PDFs, GPU/WebGL, and performance | Microsoft Playwright | November 13, 2024 | Maintainer release/compatibility notice; primary operational evidence | https://github.com/microsoft/playwright/issues/33566 |
| CSP `connect-src` and `font-src` restrict different fetch classes | W3C | Living specification, accessed August 18, 2026 | Primary web security specification | https://www.w3.org/TR/CSP/ |
| `unsafe-eval` enables string-code evaluation but does not allow arbitrary resource origins | MDN | Updated 2025 | Platform-reference documentation, corroborated by CSP specification | https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src |
| Babel Standalone compiles and executes browser `text/babel` / `text/jsx` scripts | Babel project | Undated, accessed August 18, 2026 | Official project documentation; primary | https://babeljs.io/docs/babel-standalone/ |

---

## Knowledge Gaps

### Tool-accuracy gaps

<MISSING_DATA>Comparable, peer-reviewed false-positive and false-negative rates for axe-core, Lighthouse, and IBM Equal Access on the same labeled corpus of rendered contrast defects were not found. Needed: a version-pinned benchmark covering solid backgrounds, alpha compositing, gradients, images, pseudo-elements, occlusion, filters, canvas, and interaction states.</MISSING_DATA>

<MISSING_DATA>No universal percentage exists for “contrast defects automation can never see.” The defensible observed figure is Deque’s dataset-specific 16.89% manual share for WCAG 1.4.3, not a general law.</MISSING_DATA>

### AI-layout perception gaps

<MISSING_DATA>Recent controlled human-subject evidence isolating whether people detect AI-generated web layouts from typography, gradients, spacing, section structure, and copy register was not corroborated. Needed: blinded, preregistered studies with matched human/LLM briefs and source-code-generated renders.</MISSING_DATA>

### Intervention gaps

<INSUFFICIENT_EVIDENCE>Explicit axis enumeration, forced material-family diversity, and discard-first-choice protocols are plausible controls, but only critique/revision and parameter variation had directly relevant measured support in the reviewed evidence. Their effect should be instrumented internally rather than represented as settled science.</INSUFFICIENT_EVIDENCE>

### Runtime measurement gaps

<MISSING_DATA>No cross-engine benchmark was found that quantifies how often headless visual checks create false-clean results across CSS compositing, fonts, animation timing, and responsive behavior. Needed: a maintained adversarial fixture suite run across pinned Chromium, Firefox, WebKit, and headed target browsers.</MISSING_DATA>

---

## Recommended Next Steps

1. **Build an adversarial contrast corpus.**  
   **Rationale:** It should contain solid colors, alpha stacks, gradients, photos, videos, pseudo-elements, blurred backgrounds, overlapping elements, and focus/hover states. Label each case as `PASS`, `FAIL`, or `UNMEASURABLE`; use it to regression-test the Python gate against browser renders.

2. **Run a version-pinned three-tool accessibility benchmark.**  
   **Rationale:** Execute axe-core, Lighthouse, and IBM Equal Access against the same rendered states, then manually adjudicate findings. This will produce organization-specific precision/recall and reveal whether a second tool adds meaningful marginal coverage.

3. **Implement AST lint with path classification before policy rules.**  
   **Rationale:** Start with HTML parsing, PostCSS AST traversal, JavaScript parsing, source/fixture/doc classification, and structured suppression records. Do not port regex gates wholesale; retain only literal prefilters with tests proving their scope.

4. **Create a headless “evidence contract” test harness.**  
   **Rationale:** Require browser/version/mode metadata, request logs, CSP violations, font status, runtime exceptions, longhand computed styles, screenshots, and `UNAVAILABLE` states. Add a headed Chromium canary and periodic Firefox/WebKit runs for critical artifact classes.

5. **A/B-test anti-convergence policy on real agent tasks.**  
   **Rationale:** Compare baseline generation against mandatory axis matrices plus critique/revision. Measure pairwise screenshot similarity, DOM similarity, CSS-token overlap, human preference, accessibility pass rate, and time-to-selection before hardening any anti-slop rule.

## Sources

- [Understanding Success Criterion 1.4.3: Contrast (Minimum) | WAI | W3C](https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html?locale=en_GB&utm_source=openai)
- [W3C Accessibility Guidelines (WCAG) 3.0](https://www.w3.org/TR/wcag-3.0/)
- [Axe Rules | Deque University | Deque Systems](https://dequeuniversity.com/rules/axe/4.0/color-contrast?application=AxeChrome&utm_source=openai)
- [HTML Standard](https://html.spec.whatwg.org/multipage/parsing.html?utm_source=openai)
- [PostCSS Architecture](https://postcss.org/docs/postcss-architecture?utm_source=openai)
- [Configuring | Stylelint](https://stylelint.io/user-guide/configure/?utm_source=openai)
- [Ignoring code | Stylelint](https://stylelint.io/user-guide/ignore-code/?utm_source=openai)
- [Configure Rules - ESLint - Pluggable JavaScript Linter](https://eslint.org/docs/latest/use/configure/rules?utm_source=openai)
- [Do Large Language Models Produce Diverse Design Concepts? A Comparative Study with Human-Crowdsou...](https://codesign.berkeley.edu/pdfs/papers/ma-llmdiverse-jcise.pdf)
- [Interrogating Design Homogenization in Web Vibe Coding - Microsoft Research](https://www.microsoft.com/en-us/research/publication/interrogating-design-homogenization-in-web-vibe-coding/)
- [CSS Object Model (CSSOM)](https://www.w3.org/TR/cssom-1/?utm_source=openai)
- [PageAssertions | Playwright](https://playwright.dev/docs/api/class-pageassertions?utm_source=openai)
- [Changes in Chromium headless in Playwright v1.49 · Issue #33566 · microsoft/playwright · GitHub](https://github.com/microsoft/playwright/issues/33566?utm_source=openai)
- [Content Security Policy Level 3](https://www.w3.org/TR/CSP/)
- [Content-Security-Policy: script-src directive - HTTP | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/script-src?utm_source=openai)
- [G18: Ensuring that a contrast ratio of at least 4.5:1 exists between text (and images of text) an...](https://www.w3.org/WAI/WCAG22/Techniques/general/G18?utm_source=openai)
- [W3C Accessibility Guidelines (WCAG) 3.0](https://www.w3.org/TR/wcag-3.0/?utm_source=openai)
- [The Automated Accessibility Coverage Report - Deque](https://www.deque.com/automated-accessibility-coverage-report/)
- [Lighthouse accessibility score  |  Chrome for Developers](https://developer.chrome.com/docs/lighthouse/accessibility/scoring?authuser=9)
- [www.ibm.com](https://www.ibm.com/able/toolkit/verify/automated/)
- [Accessibility Metatesting](https://jpdev.pro/jpdev/pub/pubs/etc/accessibility-metatesting.pdf)
- [Options | Stylelint](https://stylelint.io/user-guide/options/?utm_source=openai)
- [Fix `no-duplicate-selectors` false positives for single nesting selector · Issue #7893 · stylelin...](https://github.com/stylelint/stylelint/issues/7893?utm_source=openai)
- [Window: getComputedStyle() method - Web APIs | MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle.?utm_source=openai)
- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/index.html?utm_source=openai)
- [Bug: WebKit render process crashes in `getComputedStyle().getPropertyValue('background')` for m...](https://github.com/microsoft/playwright/issues/41573?utm_source=openai)
- [Content-Security-Policy (CSP) header - HTTP | MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy?no_head=1&utm_source=openai)
- [@babel/standalone · Babel](https://babeljs.io/docs/babel-standalone/?utm_source=openai)
