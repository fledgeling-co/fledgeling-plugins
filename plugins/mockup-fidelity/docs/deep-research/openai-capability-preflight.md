---
title: "Runtime capability preflights prevent vacuous success in UI-fidelity differs"
run_id: dr_cb03d59f6599e1a2
question: "How should an automated UI-fidelity differ that measures computed CSS styles from a rendered DOM detect and report that a measurement primitive is unavailable in its rendering engine, rather than silently reporting agreement? I need evidence-backed techniques and documented failure modes across four areas: (1) RUNTIME CAPABILITY PROBING — published patterns for feature-detecting CSS/DOM measurement primitives at runtime (probe-node round-trip: set a declaration, read getComputedStyle back, compare), how projects like Modernizr, CSS.supports, web-platform-tests and non-Chromium/alternative engines (Servo, LibWeb/Ladybird, WebKitGTK, headless shells) establish which computed-style properties and pseudo-element/SVG APIs are actually implemented, and known cases where a property returns an empty string or zero instead of throwing; (2) UNAVAILABLE-VS-CLEAN SIGNALLING — how test frameworks, static analysers and CI systems represent a three-valued outcome (pass / fail / could-not-evaluate) so a skipped or inconclusive check cannot be mistaken for a pass: TAP and JUnit skipped/error semantics, the literature on vacuous truth and vacuously-passing assertions in temporal-logic and property-based testing, mutation-testing and coverage-of-the-checker arguments, and published evidence on how often silently-inert checks certify untested code; (3) VISUAL-DIFF FALSE-POSITIVE CALIBRATION — measured tolerance choices in screenshot and DOM-diff comparison: anti-aliasing and subpixel-text thresholds, perceptual metrics (SSIM, CIEDE2000, pixelmatch/odiff/ImageMagick RMSE), what per-property tolerances are defensible for line-height, letter-spacing, width vs height, and how tools decide a difference is a defect rather than noise; (4) PUBLISHED FAILURE MODES OF AUTOMATED VISUAL REGRESSION — empirical studies and practitioner postmortems on flaky visual tests: font loading and web-font absence, animation and transition timing, scrollbar and viewport differences, GPU/compositor variation, dynamic data, and the reported false-positive and false-negative rates that follow. For each area I want concrete numbers, named tools and versions, and the specific mechanism behind each failure, plus any evidence on which mitigations were measured to work. Prioritise primary sources: specification text, engine bug trackers and commit history, tool documentation and issue threads, peer-reviewed empirical software-engineering studies, and first-party engineering write-ups."
provider: openai
model: gpt-5.6-terra
tier: fast
archetype: technical
sources: 57
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 3.50
completed: 2026-08-18T00:34:46.055Z
---
## Executive Summary

- **(High Confidence)** **Do not compare unavailable observations as values.** A UI-fidelity differ should perform a runtime capability preflight for every measurement primitive and property family it intends to compare, and classify an observation as `MEASURED`, `UNAVAILABLE`, `UNSTABLE`, or `ERROR` *before* equality comparison. Two empty strings or two zero rectangles must never be eligible for an “equal” result. This follows directly from CSSOM’s specified empty-string behavior for missing declarations and unsupported property writes, and SVG’s requirement that `getBBox()` compute geometry or throw when geometry cannot be computed. [CSSOM Level 1, living standard](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/?utm_source=openai)) [SVG 2, SVGGraphicsElement.getBBox()](https://svgwg.org/svg2-draft/types.html) ([svgwg.org](https://svgwg.org/svg2-draft/types.html))

- **(High Confidence)** **Use a connected probe-node round trip, not API presence or `CSS.supports()` alone.** The preflight must: write two distinct, non-default sentinel values to a connected and rendered probe; force a style read; verify that the returned values are non-empty, distinguishable, and semantically match the sentinels; and, where applicable, verify that the result changes when the sentinel changes. `CSS.supports()` establishes declaration parsing/support-query behavior, not that the engine exposes a usable resolved computed value through `getComputedStyle()`. [MDN CSS.supports() documentation](https://developer.mozilla.org/en-US/docs/Web/API/CSS/supports_static) ([developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Testing/Feature_detection?utm_source=openai)) [CSSOM Level 1](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/?utm_source=openai))

- **(High Confidence)** **Make “could not measure” a first-class non-success outcome.** Default policy should be: `PASS` only when every required observation was measured and no measured difference exceeded tolerance; `FAIL` for a measured mismatch; `INCONCLUSIVE` for an unavailable or unstable required primitive; and `ERROR` for harness/transport faults. `INCONCLUSIVE` must produce a non-zero process exit code—recommend `2`—and must not be serialized as TAP `# SKIP`, JUnit `<skipped>`, or a green “partial pass.” TAP explicitly treats skipped points as non-failing overall, which is unsuitable for an assertion that was required but not evaluated. [TAP format documentation](https://tapjs.org/tap-format/) ([tapjs.org](https://tapjs.org/tap-format/?utm_source=openai)) [JUnit User Guide: aborted tests / assumptions](https://docs.junit.org/current/user-guide/junit-user-guide-6.0.1.pdf) ([docs.junit.org](https://docs.junit.org/current/user-guide/junit-user-guide-6.0.1.pdf?utm_source=openai))

- **(High Confidence)** **For the reported failure—empty `boxShadow`, `backgroundImage`, `textTransform`, transition/animation fields, pseudo-element `content`, and all-zero SVG `getBBox()`—the correct result is `INCONCLUSIVE`, not agreement.** CSSOM specifies that `getPropertyValue()` returns `""` when a property declaration is absent and that setting an unsupported CSS property is a no-op; an empty string is therefore an ambiguous sentinel, not evidence of equal rendering. A positive-geometry SVG probe such as `<rect x="3" y="5" width="11" height="13">` returning `{0,0,0,0}` also fails the expected geometry observation. [CSSOM Level 1: getPropertyValue() and setProperty()](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/)) [SVG 2: getBBox()](https://svgwg.org/svg2-draft/types.html) ([svgwg.org](https://svgwg.org/svg2-draft/types.html))

- **(High Confidence)** **Do not apply screenshot-noise tolerances to computed-style values.** Pixel/image thresholds—such as Pixelmatch’s default per-pixel threshold of `0.1`, anti-aliasing suppression, or Playwright’s `maxDiffPixels` option—address raster comparison, not missing CSSOM observations. For computed-style DOM diffs, discrete values should compare semantically exactly; numeric layout values should use an engine- and environment-calibrated tolerance only after repeated-run measurement proves non-zero variance. There is no published universal tolerance that makes a `0.5px` line-height, letter-spacing, width, or height difference harmless. [Pixelmatch README](https://github.com/mapbox/pixelmatch) ([github.com](https://github.com/mapbox/pixelmatch?utm_source=openai)) [Playwright visual-comparison documentation](https://playwright.dev/docs/test-snapshots) ([playwright.dev](https://playwright.dev/docs/test-snapshots?utm_source=openai))

- **(High Confidence)** **Independently test the detector itself.** Add mutation/meta-tests that deliberately replace a working primitive with `""`, `{x:0,y:0,width:0,height:0}`, or a fixed constant, and assert that the differ returns `INCONCLUSIVE` and CI fails. This is the direct analogue of vacuity detection: a proposition can pass because its antecedent was never exercised, not because the system was validated. Formal-methods research identifies this as vacuous satisfaction and recommends explicit detection plus witness generation. [Beer et al., “Efficient Detection of Vacuity in Temporal Model Checking,” 2001](https://research.ibm.com/publications/efficient-detection-of-vacuity-in-temporal-model-checking) ([research.ibm.com](https://research.ibm.com/publications/efficient-detection-of-vacuity-in-temporal-model-checking?utm_source=openai))

- **(Medium Confidence)** **The trajectory favors richer preflight evidence, not broader tolerances.** WPT-style conformance testing, WebKit’s per-result status database, and Servo’s WPT reporting demonstrate that engines operationally distinguish pass, failure, timeout, crash, and expected failure rather than flattening every non-observation into success. A 2026 empirical study of 262 web visual-flakiness cases found 59.9% structure-related and 40.1% style-related failures, reinforcing that visual instability and missing observability require explicit classification. [WPT testharness.js API](https://web-platform-tests.org/writing-tests/testharness-api.html) ([web-platform-tests.org](https://web-platform-tests.org/writing-tests/testharness-api.html?utm_source=openai)) [WebKit Results Database documentation](https://results.webkit.org/documentation) ([results.webkit.org](https://results.webkit.org/documentation?utm_source=openai)) [Pei, Sohn, Papadakis, 2026](https://www.sciencedirect.com/science/article/abs/pii/S0164121226000609) ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S0164121226000609?utm_source=openai))

## Detailed Findings

### 1. How should an automated UI-fidelity differ detect and report that a measurement primitive is unavailable in its rendering engine, rather than silently reporting agreement?

#### Decision

**(High Confidence)** Implement a mandatory **capability preflight phase** before collecting any page-under-test observations. A property comparison may run only when both sides have independently demonstrated that the required primitive can observe a deliberately injected, non-default, distinguishable value. <INFERENCE from="[CSSOM requirement that computed-style declarations contain supported CSS properties and return resolved values; CSSOM empty-string behavior for absent declarations; SVG getBBox geometry requirement]">If a reader cannot distinguish intentionally different probe states, it cannot supply evidence for equality of production states; therefore it must be classified unavailable rather than compared.</INFERENCE> [CSSOM Level 1](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/?utm_source=openai)) [SVG 2](https://svgwg.org/svg2-draft/types.html) ([svgwg.org](https://svgwg.org/svg2-draft/types.html))

A recommended operational contract is:

| Observation state | Meaning | Comparator action | Overall run consequence |
|---|---|---|---|
| `MEASURED` | Probe showed distinct expected values and runtime read succeeded | Compare semantic values using property policy | Eligible for `PASS` or `FAIL` |
| `UNAVAILABLE` | API exists but cannot distinguish probe sentinels; returns empty/default/constant/zero sentinel; unsupported write; or missing pseudo/SVG observation | Do **not** compare values | `INCONCLUSIVE` if required |
| `UNSTABLE` | Repeated probe reads of fixed input vary outside calibrated stability bounds | Do **not** compare values | `INCONCLUSIVE` if required |
| `ERROR` | Exception, navigation failure, transport failure, malformed result, timeout | Do **not** compare values | `ERROR`; non-zero exit |
| `NOT_REQUESTED` | Property family excluded by scope | Do not compare | No effect, but disclose it |

**(High Confidence)** The differ must maintain the invariant:

```text
equal(a, b) is legal only if a.state == MEASURED && b.state == MEASURED
```

<INFERENCE from="[CSSOM’s specified empty-string return behavior; TAP skipped tests treated as overall pass]">Treating `"" == ""` or `0 == 0` as equality before establishing observability creates vacuous agreement: the detector confirms identical sentinel behavior, not identical UI behavior.</INFERENCE> [CSSOM Level 1](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/)) [TAP format documentation](https://tapjs.org/tap-format/) ([tapjs.org](https://tapjs.org/tap-format/?utm_source=openai))

---

#### 1.1 Runtime capability probing

**(High Confidence)** `typeof getComputedStyle === "function"`, property existence tests, user-agent sniffing, and `CSS.supports()` are insufficient as final gates. The CSS Conditional Rules feature query is useful as a **syntax/support-query precondition**, but the differ needs a behavioral test of the exact read path: set declaration → attach node → force style/layout read → obtain `getComputedStyle()` value → validate semantic round trip. MDN documents `CSS.supports()` as testing whether a browser supports a property/value declaration, while CSSOM defines `getComputedStyle()` in terms of supported properties and resolved values for a connected rendered element. [MDN CSS.supports()](https://developer.mozilla.org/en-US/docs/Web/API/CSS/supports_static) ([developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Testing/Feature_detection?utm_source=openai)) [CSSOM Level 1](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/?utm_source=openai))

**(High Confidence)** CSSOM specifically creates an empty declaration list unless the target is connected, part of the flat tree, and rendered; therefore a capability probe must insert its probe element into a rendered document rather than use a detached node. [CSSOM getComputedStyle() algorithm](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/?utm_source=openai))

**(High Confidence)** Modernizr provides an established first-party pattern for runtime feature probing: `Modernizr.testProp()` tests a property/value, while `Modernizr.testStyles()` injects CSS and DOM elements to test behavioral outcomes. This is directly applicable to a UI differ, but its result should be persisted as structured capability evidence rather than converted to a boolean feature flag. [Modernizr documentation](https://modernizr.com/docs/) ([modernizr.com](https://modernizr.com/docs/?utm_source=openai))

**Recommended probe algorithm**

```js
function probeComputedProperty({ property, first, second, verify }) {
  const node = document.createElement("div");
  node.id = "__ui_diff_probe__";
  node.style.cssText =
    "position:absolute !important;" +
    "left:-10000px !important;" +
    "top:-10000px !important;" +
    "display:block !important;" +
    "visibility:visible !important;";

  document.documentElement.append(node);

  try {
    const syntaxAccepted =
      typeof CSS?.supports === "function"
        ? CSS.supports(property, first)
        : null; // Diagnostic only; not proof.

    node.style.setProperty(property, first);
    const specifiedFirst = node.style.getPropertyValue(property);
    const observedFirst =
      getComputedStyle(node).getPropertyValue(property);

    node.style.setProperty(property, second);
    const specifiedSecond = node.style.getPropertyValue(property);
    const observedSecond =
      getComputedStyle(node).getPropertyValue(property);

    const result = {
      primitive: "Window.getComputedStyle",
      property,
      syntaxAccepted,
      specifiedFirst,
      specifiedSecond,
      observedFirst,
      observedSecond,
      state: "UNAVAILABLE",
      reason: null
    };

    if (!specifiedFirst || !specifiedSecond) {
      result.reason = "WRITE_NOT_ACCEPTED";
    } else if (!observedFirst || !observedSecond) {
      result.reason = "EMPTY_COMPUTED_VALUE";
    } else if (observedFirst === observedSecond) {
      result.reason = "NON_DISCRIMINATING_READ";
    } else if (!verify(observedFirst, observedSecond)) {
      result.reason = "SENTINEL_NOT_OBSERVED";
    } else {
      result.state = "MEASURED";
    }

    return result;
  } catch (error) {
    return {
      primitive: "Window.getComputedStyle",
      property,
      state: "ERROR",
      reason: "THREW",
      error: { name: error.name, message: error.message }
    };
  } finally {
    node.remove();
  }
}
```

**(High Confidence)** Use **two sentinels**, not one. A single sentinel can accidentally equal an initial value, an engine fallback, or a hard-coded default. Two semantically different sentinels make the probe metamorphic: changing the input must change the observation. <INFERENCE from="[CSSOM permits empty-string returns for undeclared properties and unsupported writes; Modernizr uses behavioral tests rather than API-name tests]">A two-sentinel round trip detects constant-return and default-return stubs that a single positive probe can miss.</INFERENCE> [CSSOM Level 1](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/)) [Modernizr documentation](https://modernizr.com/docs/) ([modernizr.com](https://modernizr.com/docs/?utm_source=openai))

**Suggested property-family probes**

| Property family | Probe values | Pass condition | Failure classification |
|---|---|---|---|
| `box-shadow` | `rgb(1,2,3) 3px 5px 7px 11px inset`; then `rgb(17,19,23) 2px 4px 6px 8px` | Both values non-empty; parsed shadow tuples differ and preserve relevant color/length/inset semantics | `EMPTY_COMPUTED_VALUE`, `NON_DISCRIMINATING_READ` |
| `background-image` | `linear-gradient(rgb(1,2,3), rgb(4,5,6))`; then a different angle/color sequence | Non-empty serialized image value; parse tree differs | `EMPTY_COMPUTED_VALUE` |
| `text-transform` | `uppercase`; then `lowercase` | Exact normalized keyword differs | `EMPTY_COMPUTED_VALUE` or `NON_DISCRIMINATING_READ` |
| `transition-*` | e.g. `transition-property: opacity`; then `transform`; pair with distinct duration/delay | Longhand values non-empty and distinguishable | `EMPTY_COMPUTED_VALUE` |
| `animation-*` | e.g. `animation-name: __probe_a`; then `__probe_b`; establish matching `@keyframes` rules | Non-empty and distinguishable | `EMPTY_COMPUTED_VALUE` |
| `::before` / `::after` content | Inject rule with `content: "__probe_A__"`; change to `__probe_B__` | `getComputedStyle(node, "::before").content` contains distinct generated-string serializations | `PSEUDO_UNAVAILABLE`, `EMPTY_PSEUDO_CONTENT` |
| SVG `getBBox()` | Connected `<svg><rect x="3" y="5" width="11" height="13"/></svg>`; mutate to width `17`, height `19` | Returned rect has expected positive width/height and changes after mutation | `SVG_BBOX_ZERO_SENTINEL`, `SVG_BBOX_CONSTANT`, `THREW` |

**(High Confidence)** The CSSOM specification itself explains why “no exception” is not evidence of support: `getPropertyValue()` returns the empty string when no matching declaration exists, and `setProperty()` returns without setting an unsupported CSS property. [CSSOM Level 1: getPropertyValue() and setProperty()](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/))

**(High Confidence)** Pseudo-element probing must create the pseudo-element. Merely calling `getComputedStyle(element, "::before")` is not enough: syntactic validity and pseudo-element existence are distinct, and an absent pseudo can legitimately produce no meaningful generated `content` observation. CSSOM parses a pseudo selector and otherwise produces declarations only when the corresponding object and rendered element qualify. [CSSOM getComputedStyle() algorithm](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/?utm_source=openai))

**(High Confidence)** For SVG, use a non-zero rect or path and mutate it. SVG 2 states that `getBBox()` invokes the bounding-box algorithm and returns a computed `DOMRect`; if a non-rendered element’s geometry cannot be computed, it should throw `InvalidStateError`. A `{0,0,0,0}` result for a connected positive-sized probe is therefore not a valid confirmation that the geometry primitive measured the intended shape. [SVG 2: getBBox()](https://svgwg.org/svg2-draft/types.html) ([svgwg.org](https://svgwg.org/svg2-draft/types.html))

**Engine and conformance practice**

| Project / engine | How capability is established | Relevant evidence | Implication for the differ |
|---|---|---|---|
| Modernizr | Runtime property and injected-style behavioral probes | `testProp()` and `testStyles()` are documented first-party mechanisms. [Modernizr documentation](https://modernizr.com/docs/) ([modernizr.com](https://modernizr.com/docs/?utm_source=openai)) | Use behavior tests, but retain raw observed values and reasons. |
| web-platform-tests | Assertion-driven conformance tests with explicit result states | WPT subtests have `PASS`, `FAIL`, `TIMEOUT`, `NOTRUN`, and `PRECONDITION_FAILED` states. [WPT testharness.js API](https://web-platform-tests.org/writing-tests/testharness-api.html) ([web-platform-tests.org](https://web-platform-tests.org/writing-tests/testharness-api.html?utm_source=openai)) | Adopt a similarly explicit precondition result rather than silently omitting observations. |
| Servo | Tracks platform conformance through WPT and capability listings | A Servo maintainer reported on February 19, 2026 that Servo runs against WPT and then passed 1.81 million tests; the maintainer cautioned WPT is imperfect for estimating real-world feature usability. [Servo discussion #42711](https://github.com/servo/servo/discussions/42711) ([github.com](https://github.com/servo/servo/discussions/42711?utm_source=openai)) | Do not infer property observability from aggregate WPT pass counts; probe the exact primitive/version/runtime. |
| WebKitGTK / WPE | Layout, pixel, WebDriver, and imported WPT suites; result database separates outcome types | WebKitGTK documents `run-webkit-tests --gtk`, optional pixel tests via `-p`, and WebDriver test output; WebKit’s results database differentiates crash, timeout, image, text, fail, error, warning, and pass. [WebKitGTK Layout Tests](https://trac.webkit.org/wiki/WebKitGtkLayoutTests) ([trac.webkit.org](https://trac.webkit.org/wiki/WebKitGtkLayoutTests?utm_source=openai)) [WebKit Results Database](https://results.webkit.org/documentation) ([results.webkit.org](https://results.webkit.org/documentation?utm_source=openai)) | Persist engine build, port, platform, and probe result because a nominal “WebKit” label hides real port-specific differences. |
| Ladybird / LibWeb | Public project repository exists, but this investigation did not find a first-party, property-level computed-style observability matrix comparable to WebKit’s result database | <MISSING_DATA>[A verified first-party Ladybird/LibWeb source enumerating computed-style and getBBox observability by property/API was sought; no verifiable source was retrieved in this investigation.]</MISSING_DATA> | Treat the runtime probe manifest—not project branding—as authoritative. |

**Source-discipline fit:** CSSOM and SVG 2 are normative specifications; Modernizr, Servo, WebKitGTK, and WebKit Results Database sources are first-party project documentation or maintainer statements; WPT documentation is maintained by the WPT project. These meet the requested primary/authoritative-source preference. [CSSOM](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/?utm_source=openai)) [SVG 2](https://svgwg.org/svg2-draft/types.html) ([svgwg.org](https://svgwg.org/svg2-draft/types.html))

---

#### 1.2 Unavailable-vs-clean signalling

**(High Confidence)** Report three logical outcomes to people and CI:

1. `PASS`: every required property was **measured**, and all comparisons were within their policy.
2. `FAIL`: every relevant property was measurable, and at least one measured comparison differed.
3. `INCONCLUSIVE`: at least one required property or primitive could not be measured reliably.

A fourth operational result, `ERROR`, should identify runner/harness faults separately from known lack of observability.

**(High Confidence)** Do **not** use TAP `# SKIP` for required unavailable measurements. TAP documents that `skip` marks a test as not performed and that failures of skipped points are not treated as failures overall; that makes a skipped required detector capable of producing a green aggregate test stream. [TAP format documentation](https://tapjs.org/tap-format/) ([tapjs.org](https://tapjs.org/tap-format/?utm_source=openai))

**(High Confidence)** Do **not** use JUnit’s aborted/skipped semantics for required unavailable measurements. JUnit uses `TestAbortedException` and assumptions to signal tests that should be aborted rather than marked failed; that is correct for an optional environmental precondition, but unsafe for a release gate claiming complete UI-fidelity certification. [JUnit User Guide](https://docs.junit.org/current/user-guide/junit-user-guide-6.0.1.pdf) ([docs.junit.org](https://docs.junit.org/current/user-guide/junit-user-guide-6.0.1.pdf?utm_source=openai))

**Recommended CI contract**

| Overall result | JSON `overall_status` | TAP encoding | JUnit/XML encoding | Process exit | Merge/deploy gate |
|---|---:|---|---|---:|---|
| Clean comparison | `PASS` | `ok` | normal `<testcase>` | `0` | Allow |
| Measured mismatch | `FAIL` | `not ok` | `<failure type="VisualDifference">` | `1` | Block |
| Required primitive unavailable / unstable | `INCONCLUSIVE` | `not ok ...` plus diagnostic YAML; **not** `# SKIP` | `<error type="MeasurementUnavailable">` or `<error type="MeasurementUnstable">` | `2` | Block by default |
| Harness defect / timeout / malformed artifact | `ERROR` | `Bail out!` or `not ok` | `<error type="HarnessError">` | `3` | Block |
| Optional capability unavailable | `PARTIAL` | `not ok` in a non-gating supplementary suite, or an explicit capability artifact | `<skipped>` only if the suite is explicitly non-certifying | `2` by default; `0` only under a named non-certifying policy | Do not label build “UI fidelity passed” |

**(Medium Confidence)** Exit codes `1`, `2`, and `3` are a recommended stable local contract, not an industry-standard mapping. <INFERENCE from="[TAP’s representation of skip as overall success; JUnit’s aborted-test semantics; WPT’s distinct precondition-failed and timeout statuses]">A custom non-zero `INCONCLUSIVE` exit code is necessary because standard test-report formats alone can preserve a skipped/aborted result without making the job fail.</INFERENCE> [TAP format documentation](https://tapjs.org/tap-format/) ([tapjs.org](https://tapjs.org/tap-format/?utm_source=openai)) [JUnit User Guide](https://docs.junit.org/current/user-guide/junit-user-guide-6.0.1.pdf) ([docs.junit.org](https://docs.junit.org/current/user-guide/junit-user-guide-6.0.1.pdf?utm_source=openai)) [WPT testharness.js API](https://web-platform-tests.org/writing-tests/testharness-api.html) ([web-platform-tests.org](https://web-platform-tests.org/writing-tests/testharness-api.html?utm_source=openai))

**Recommended machine-readable artifact**

```json
{
  "schema_version": "ui-fidelity-diff/v2",
  "overall_status": "INCONCLUSIVE",
  "exit_code": 2,
  "certification": {
    "claim": "No complete UI-fidelity conclusion is available",
    "pass_eligible": false
  },
  "engine": {
    "name": "example-engine",
    "version": "exact-build-id",
    "platform": "linux-x86_64",
    "headless": true
  },
  "coverage": {
    "requested_observations": 42,
    "measured_observations": 34,
    "unavailable_observations": 8,
    "unstable_observations": 0,
    "comparison_coverage": 0.8095238095
  },
  "capabilities": [
    {
      "primitive": "Window.getComputedStyle",
      "target": "::before.content",
      "state": "UNAVAILABLE",
      "reason": "EMPTY_PSEUDO_CONTENT",
      "probe": {
        "first_input": "\"__ui_probe_A__\"",
        "second_input": "\"__ui_probe_B__\"",
        "first_observed": "",
        "second_observed": ""
      }
    },
    {
      "primitive": "SVGGraphicsElement.getBBox",
      "target": "svg rect geometry",
      "state": "UNAVAILABLE",
      "reason": "SVG_BBOX_ZERO_SENTINEL",
      "probe": {
        "first_input": { "x": 3, "y": 5, "width": 11, "height": 13 },
        "first_observed": { "x": 0, "y": 0, "width": 0, "height": 0 },
        "second_input": { "x": 3, "y": 5, "width": 17, "height": 19 },
        "second_observed": { "x": 0, "y": 0, "width": 0, "height": 0 }
      }
    }
  ],
  "comparisons": [
    {
      "selector": ".card",
      "property": "box-shadow",
      "state": "NOT_COMPARED",
      "reason": "DEPENDENCY_UNAVAILABLE"
    }
  ]
}
```

**(High Confidence)** Keep `comparison_coverage` separate from an agreement percentage. A result such as “34/42 measured and all 34 equal” must be shown as `INCONCLUSIVE — 8 required observations unavailable`, not “100% agreement.” <INFERENCE from="[formal vacuity-detection literature; TAP skipped-state semantics]">An agreement denominator that excludes unavailable checks can make the result numerically perfect while omitting precisely the observations needed to substantiate the claim.</INFERENCE> [Beer et al., 2001](https://research.ibm.com/publications/efficient-detection-of-vacuity-in-temporal-model-checking) ([research.ibm.com](https://research.ibm.com/publications/efficient-detection-of-vacuity-in-temporal-model-checking?utm_source=openai)) [TAP format documentation](https://tapjs.org/tap-format/) ([tapjs.org](https://tapjs.org/tap-format/?utm_source=openai))

**(High Confidence)** Vacuity research is directly relevant. Beer et al. describe valid temporal-logic formulas that conceal real defects because an implication’s antecedent never occurs; they call this vacuity and propose detecting it even after a positive result. The UI-diff analogue is a detector whose differing-value path was never demonstrated. [Beer et al., 2001](https://research.ibm.com/publications/efficient-detection-of-vacuity-in-temporal-model-checking) ([research.ibm.com](https://research.ibm.com/publications/efficient-detection-of-vacuity-in-temporal-model-checking?utm_source=openai))

**(Medium Confidence)** Mutation testing is an appropriate detector-coverage control, but no peer-reviewed source found in this investigation quantifies how often *computed-style visual-diff detectors specifically* are silently inert. General mutation-testing literature supports the principle that a surviving mutant identifies behavior not distinguished by the test suite; equivalent-mutant rates, however, complicate direct score interpretation. [“On the use of commit-relevant mutants,” 2022](https://link.springer.com/article/10.1007/s10664-022-10138-1) ([link.springer.com](https://link.springer.com/article/10.1007/s10664-022-10138-1?utm_source=openai)) [Mutation-testing survey](https://dijkstra.eecs.umich.edu/kleach/eecs481/w21/readings/mutation-testing.pdf) ([dijkstra.eecs.umich.edu](https://dijkstra.eecs.umich.edu/kleach/eecs481/w21/readings/mutation-testing.pdf?utm_source=openai))

<MISSING_DATA>[A reliable empirical rate for “silently inert CSS/DOM visual-diff detector classes” was sought. No study was found that isolates this exact failure mode and reports a population rate. A publishable answer would require a corpus of differs, injected reader stubs, and observed false-certification outcomes.]</MISSING_DATA>

---

#### 1.3 Visual-diff false-positive calibration and per-property tolerances

**(High Confidence)** Screenshot comparison tools expose thresholds because raster images are affected by anti-aliasing, glyph rasterization, subpixel placement, and compositor differences. Pixelmatch’s documented default per-pixel sensitivity threshold is `0.1` on a `0–1` scale; by default it detects and ignores likely anti-aliased pixels. [Pixelmatch README](https://github.com/mapbox/pixelmatch) ([github.com](https://github.com/mapbox/pixelmatch?utm_source=openai))

**(High Confidence)** Pixelmatch’s `0.1` is **not** a permissible tolerance for computed CSS values. It is a color-difference sensitivity parameter in an image comparator using YIQ-based perceptual color difference and anti-aliasing heuristics. [Pixelmatch README](https://github.com/mapbox/pixelmatch) ([github.com](https://github.com/mapbox/pixelmatch?utm_source=openai))

**(High Confidence)** Playwright’s screenshot assertions use Pixelmatch and expose a separate `maxDiffPixels` control; its screenshot API can disable animations, hide carets, and apply a stylesheet to reduce volatility. [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots) ([playwright.dev](https://playwright.dev/docs/test-snapshots?utm_source=openai)) [Playwright Page screenshot API](https://playwright.dev/docs/next/api/class-page) ([playwright.dev](https://playwright.dev/docs/next/api/class-page?utm_source=openai))

**(High Confidence)** ImageMagick documents several metrics, including AE, MAE, RMSE, DSSIM, SSIM, and CIE-related workflows; it defines perfect RMSE as `0` and perfect SSIM as `1`. These metrics quantify image difference but do not establish whether a DOM computed-style primitive was available. [ImageMagick command-line options](https://imagemagick.org/script/command-line-options.php/) ([imagemagick.org](https://imagemagick.org/script/command-line-options.php/?utm_source=openai)) [ImageMagick compare documentation](https://imagemagick.org/compare/) ([imagemagick.org](https://imagemagick.org/compare/?utm_source=openai))

**(High Confidence)** CIEDE2000 is a standardized perceptual color-difference formula, but its purpose is color-difference estimation in colorimetric spaces; it is not a substitute for DOM-property equality or layout geometry comparison. [ISO/CIE 11664-6:2022](https://www.cie.co.at/publications/colorimetry-part-6-ciede2000-colour-difference-formula-1) ([cie.co.at](https://www.cie.co.at/publications/colorimetry-part-6-ciede2000-colour-difference-formula-1?utm_source=openai))

**Recommended tolerance policy**

| Property / output type | Default comparison | Suggested tolerance policy | Rationale |
|---|---|---|---|
| Keywords: `text-transform`, `display`, `position`, `visibility`, `transition-property` | Semantic exact equality | `0` | A different keyword is an intentional observable difference, not subpixel noise. |
| Structured CSS: `box-shadow`, `background-image`, `animation-*`, `transition-*` | Parse then compare normalized components | `0` after canonicalization; do not compare raw serialization alone | Serialization can vary; a missing/empty serialization is unavailable, not equivalent. |
| Computed lengths: `line-height`, `letter-spacing`, `font-size`, `width`, `height` | Compare normalized CSS-pixel values | Start at `0`; increase only from measured same-environment repeat-run variance | No general published basis supports ignoring a fixed `0.5px` or `1px` difference. |
| DOM rectangles: `getBoundingClientRect()`, SVG `getBBox()` | Compare all four components after positive probe | Environment-calibrated absolute tolerance only after stable runs establish a distribution | A width/height shift can reflow downstream content; generic thresholds hide real defects. |
| Screenshot pixels | Pixelmatch/SSIM/RMSE policy | Use tool-specific per-pixel plus aggregate-pixel limits, calibrated per baseline class | Rasterization noise is distinct from CSSOM observability. |
| Cross-engine comparison | Report engine divergence separately | Do not silently absorb with broad tolerances | Different layout/rendering engines can make legitimate implementation choices within specifications. |

**(High Confidence)** The only externally defensible universal default for a computed-style DOM differ is **exact semantic equality after normalization**, combined with engine-specific calibration for known numeric instability. <INSUFFICIENT_EVIDENCE>[No primary empirical study was found that validates one universal CSS-pixel tolerance for line-height, letter-spacing, width, or height across browser engines and operating systems. Tool documentation provides screenshot-level defaults, not property-level DOM tolerances.]</INSUFFICIENT_EVIDENCE>

**(Medium Confidence)** A defensible calibrated numeric tolerance is:

```text
tolerance(property, environment) =
  max(observed_repeat_run_delta_at_required_quantile, declared_precision_floor)
```

where the measured repeat-run distribution is collected under the exact engine build, font set, viewport, device scale factor, OS image, and headless/headed mode used by CI.

<INFERENCE from="[Pixelmatch and Playwright distinguish sensitivity from aggregate-difference budgets; general flaky-test studies identify environment/platform variation as a root cause]">The tolerance should be derived from measured noise in the deployment environment, rather than imported from a screenshot library or selected by visual intuition.</INFERENCE> [Pixelmatch README](https://github.com/mapbox/pixelmatch) ([github.com](https://github.com/mapbox/pixelmatch?utm_source=openai)) [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots) ([playwright.dev](https://playwright.dev/docs/test-snapshots?utm_source=openai)) [Parry et al., 2023 multivocal review of flaky-test causes](https://doi.org/10.1016/j.jss.2023.111837) ([doi.org](https://doi.org/10.1016/j.jss.2023.111837?utm_source=openai))

**Comparison tooling table — requested model-style columns are not applicable to deterministic image/DOM tools**

| Tool / component | Parameter Count | Context Window | Latency | Cost | License | Relevant comparison role |
|---|---:|---:|---|---|---|---|
| Custom CSSOM/SVG capability preflight | N/A — deterministic probe code | N/A — DOM-local | <MISSING_DATA>[No benchmark was supplied; measure in target engine.]</MISSING_DATA> | Engineering cost | Project-defined | Determines whether a DOM observation is certifying. |
| Pixelmatch | N/A | N/A | <MISSING_DATA>[The first-party README documents API and defaults but does not publish a universal latency benchmark.]</MISSING_DATA> | Open-source dependency | ISC | Pixel-level diff; default threshold `0.1`; optional anti-aliasing inclusion. [Pixelmatch README](https://github.com/mapbox/pixelmatch) ([github.com](https://github.com/mapbox/pixelmatch?utm_source=openai)) |
| ODiff | N/A | N/A | Repository benchmark: `1.168 ± 0.008s` versus `7.712 ± 0.069s` for Pixelmatch and `8.881 ± 0.121s` for ImageMagick on the repository’s cited Cypress-page case; treat as maintainer benchmark, not independent evidence. [ODiff README](https://github.com/dmtrKovalenko/odiff) ([github.com](https://github.com/dmtrKovalenko/odiff?utm_source=openai)) | Open-source dependency | <MISSING_DATA>[License was not independently verified in the retrieved source excerpt.]</MISSING_DATA> | Raster diff with layout-difference and anti-aliasing options. |
| Playwright screenshot assertions | N/A | N/A | <MISSING_DATA>[Official documentation exposes controls but not stable cross-platform latency figures.]</MISSING_DATA> | Open-source runner / infrastructure cost | Apache-2.0 project, not independently verified in retrieved excerpt | Screenshots, masking/style injection, animation/caret stabilization, Pixelmatch-backed comparison. [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots) ([playwright.dev](https://playwright.dev/docs/test-snapshots?utm_source=openai)) |
| ImageMagick `compare` | N/A | N/A | Hardware/input dependent; ImageMagick notes FFTW can yield an order-of-magnitude speedup for certain metrics. [ImageMagick compare documentation](https://imagemagick.org/compare/) ([imagemagick.org](https://imagemagick.org/compare/?utm_source=openai)) | Open-source dependency | <MISSING_DATA>[License omitted because it was not verified in retrieved documentation.]</MISSING_DATA> | RMSE, SSIM, AE, MAE, DSSIM, and related image metrics. |

---

#### 1.4 Published failure modes of automated visual regression

**(High Confidence)** A 2026 peer-reviewed empirical study specifically on web visual flakiness analyzed **262 cases**—**144** from **31 open-source web projects** and **118** from Chromium. It classified **59.9%** as structure-related and **40.1%** as style-related; visual commits averaged **11.7%** of project commits in the analyzed open-source projects. [Pei, Sohn, Papadakis, “An empirical study of web visual flakiness,” 2026](https://www.sciencedirect.com/science/article/abs/pii/S0164121226000609) ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S0164121226000609?utm_source=openai))

**(High Confidence)** The same study’s five concrete manifestation classes are directly relevant to screenshot and DOM comparison: DOM-structure issues, DOM-layout instability, timing-sensitive visual triggers, style-interpretation issues, and style-resource latency. [Pei dissertation reporting the study taxonomy and counts](https://orbilu.uni.lu/bitstream/10993/66145/1/thesis.pdf) ([orbilu.uni.lu](https://orbilu.uni.lu/bitstream/10993/66145/1/thesis.pdf?utm_source=openai))

| Failure mechanism | Mechanism causing false positive or false negative | Published evidence | Measured mitigation / implication |
|---|---|---|---|
| Web-font absence or late loading | Fallback font changes glyph widths, wrapping, line boxes, and screenshot pixels; a later font update can race screenshot capture | Playwright issue #29968 reports flaky full-page snapshots in Playwright `1.42.1` and attributes the behavior to Chromium font updates interfering with capture; the reporter’s workaround installed fonts locally and blocked remote requests. [Playwright issue #29968](https://github.com/microsoft/playwright/issues/29968) ([github.com](https://github.com/microsoft/playwright/issues/29968?utm_source=openai)) | Pin fonts, wait for `document.fonts.ready`, bundle fonts, and record font inventory. The cited workaround is case evidence, not a general measured rate. |
| Font hinting / kernel / rasterizer variation | Same container image can still inherit host kernel behavior; glyph hints and antialiasing may differ | Playwright issue #35143 records occasional font diffs despite a Docker image and identifies host-kernel differences as a plausible cause. [Playwright issue #35143](https://github.com/microsoft/playwright/issues/35143) ([github.com](https://github.com/microsoft/playwright/issues/35143?utm_source=openai)) | Use the same OS image, browser revision, kernel where feasible, font files, device scale factor, and snapshot baseline environment. |
| Animations and transitions | Capture can occur in an intermediate visual state; transition timing and animation frames vary | Playwright exposes `animations: "disabled"`; finite animations are fast-forwarded and infinite ones are canceled to their initial state during screenshot capture. [Playwright Page screenshot API](https://playwright.dev/docs/next/api/class-page) ([playwright.dev](https://playwright.dev/docs/next/api/class-page?utm_source=openai)) | Disable/fast-forward animation for screenshot tests; separately compare authored animation CSS only when its computed-style probes pass. |
| Caret, focus and volatile regions | Text caret blink, cursor/focus state, timestamps, ads, remote data, and live counters create non-product diffs | Playwright defaults screenshot caret behavior to hidden and supports injected styles to filter volatile elements. [Playwright Page screenshot API](https://playwright.dev/docs/next/api/class-page) ([playwright.dev](https://playwright.dev/docs/next/api/class-page?utm_source=openai)) [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots) ([playwright.dev](https://playwright.dev/docs/test-snapshots?utm_source=openai)) | Hide carets; use deterministic fixtures; mask or style only explicitly approved volatile regions; disclose masks in artifacts. |
| Viewport and scrollbar differences | Scrollbar width and viewport size change available layout width, causing responsive breakpoints and reflow | The 2026 visual-flakiness study identifies structure/layout instability and timing-sensitive triggers as major categories. [Pei et al., 2026](https://www.sciencedirect.com/science/article/abs/pii/S0164121226000609) ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S0164121226000609?utm_source=openai)) | Pin viewport, browser zoom, DPR, scrollbar mode, color scheme, locale, and reduced-motion configuration. |
| GPU/compositor variation | Different rasterization/compositor paths alter anti-aliasing and pixel output without a DOM style difference | Pixelmatch explicitly offers anti-aliased-pixel handling; its open issue #74 documents remaining false positives for thin/ring-like anti-aliased shapes. [Pixelmatch README](https://github.com/mapbox/pixelmatch) ([github.com](https://github.com/mapbox/pixelmatch?utm_source=openai)) [Pixelmatch issue #74](https://github.com/mapbox/pixelmatch/issues/74) ([github.com](https://github.com/mapbox/pixelmatch/issues/74?utm_source=openai)) | Use deterministic rendering where possible; retain anti-aliasing classification; inspect image diffs rather than converting them into DOM-property tolerances. |
| Asynchronous content / dynamic data | DOM state changes after an apparently ready page; screenshots or style reads sample different states | The ICSE 2021 UI-flaky-test study analyzed **235** flaky UI test samples from **62** web and Android projects; async-wait issues were more prevalent in web projects (**52.0%**) than mobile (**32.5%**), and cross-platform layout differences appeared more in web tests (**5.3%**) than mobile (**1.2%**). [Romano et al., ICSE 2021](https://weihang-wang.github.io/papers/UIFlaky-icse21.pdf) ([weihang-wang.github.io](https://weihang-wang.github.io/papers/UIFlaky-icse21.pdf?utm_source=openai)) | Wait for semantic readiness signals, not arbitrary sleeps; freeze fixture data and network responses. |
| General CI flakiness eroding trust | A noisy test corpus trains engineers to discount failures, increasing false-negative risk through ignored real regressions | Google reported approximately **1.5%** flaky test executions, roughly **16%** of tests with some flakiness, and about **84%** of observed pass-to-fail transitions involving flaky tests. [Google Testing Blog, 2016](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html) ([testing.googleblog.com](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html?m=1&utm_source=openai)) | Quarantine only after preserving a visible non-success classification; track flakiness and detector coverage rather than retrying until green. |

**(High Confidence)** WPT discourages timers because they are an observed source of CI instability; its default test-harness timeout is **10 seconds**, with a typical long-timeout setting of **60 seconds** before runner multipliers. [WPT testharness.js API](https://web-platform-tests.org/writing-tests/testharness-api.html) ([web-platform-tests.org](https://web-platform-tests.org/writing-tests/testharness-api.html?utm_source=openai))

**(Medium Confidence)** The strongest evidence supports environment control and synchronization, not indiscriminate threshold widening. The 2026 web-visual-flakiness study identifies resource latency, layout instability, timing-sensitive triggers, and style interpretation as recurring causes; Playwright’s official controls directly target animation, caret, and volatile-style sources; and WPT warns against timer-based tests. <INFERENCE from="[Pei et al. 2026 taxonomy; Playwright screenshot controls; WPT timer guidance]">The preferred mitigation order is: make the rendered state deterministic; prove primitive observability; then calibrate limited raster noise thresholds—not the reverse.</INFERENCE> [Pei et al., 2026](https://www.sciencedirect.com/science/article/abs/pii/S0164121226000609) ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S0164121226000609?utm_source=openai)) [Playwright Page screenshot API](https://playwright.dev/docs/next/api/class-page) ([playwright.dev](https://playwright.dev/docs/next/api/class-page?utm_source=openai)) [WPT testharness.js API](https://web-platform-tests.org/writing-tests/testharness-api.html) ([web-platform-tests.org](https://web-platform-tests.org/writing-tests/testharness-api.html?utm_source=openai))

### 2. What is the current state, and what is the strongest supporting evidence for it?

**(High Confidence)** The current state is that mature browser-engine and test ecosystems already use multi-state result models, but typical UI-diff implementations often still conflate “API returned something” with “property was measured.” WPT defines `PASS`, `FAIL`, `TIMEOUT`, `NOTRUN`, and `PRECONDITION_FAILED`; WebKit records pass, fail, text, image, timeout, crash, error, and warning outcomes; TAP and JUnit distinguish skipped/aborted execution from ordinary pass/fail. [WPT testharness.js API](https://web-platform-tests.org/writing-tests/testharness-api.html) ([web-platform-tests.org](https://web-platform-tests.org/writing-tests/testharness-api.html?utm_source=openai)) [WebKit Results Database documentation](https://results.webkit.org/documentation) ([results.webkit.org](https://results.webkit.org/documentation?utm_source=openai)) [TAP format documentation](https://tapjs.org/tap-format/) ([tapjs.org](https://tapjs.org/tap-format/?utm_source=openai)) [JUnit User Guide](https://docs.junit.org/current/user-guide/junit-user-guide-6.0.1.pdf) ([docs.junit.org](https://docs.junit.org/current/user-guide/junit-user-guide-6.0.1.pdf?utm_source=openai))

**(High Confidence)** The strongest supporting evidence for the recommended approach is the combination of: normative CSSOM/SVG behavior; established behavioral feature-detection patterns from Modernizr; WPT’s explicit precondition/result states; and formal vacuity-detection literature showing that a positive assertion can be meaningless unless the relevant condition is known to have occurred. [CSSOM Level 1](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/?utm_source=openai)) [SVG 2](https://svgwg.org/svg2-draft/types.html) ([svgwg.org](https://svgwg.org/svg2-draft/types.html)) [Modernizr documentation](https://modernizr.com/docs/) ([modernizr.com](https://modernizr.com/docs/?utm_source=openai)) [Beer et al., 2001](https://research.ibm.com/publications/efficient-detection-of-vacuity-in-temporal-model-checking) ([research.ibm.com](https://research.ibm.com/publications/efficient-detection-of-vacuity-in-temporal-model-checking?utm_source=openai))

**(Medium Confidence)** Servo’s February 19, 2026 maintainer statement that it passes **1.81 million** WPT tests demonstrates substantial conformance activity, but the same statement cautions that WPT is imperfect for estimating real-world feature usability. This supports a two-level strategy: use WPT/engine conformance information for ecosystem intelligence, but rely on runtime behavioral probes for the exact headless shell and property set used in a certification run. [Servo discussion #42711](https://github.com/servo/servo/discussions/42711) ([github.com](https://github.com/servo/servo/discussions/42711?utm_source=openai))

### 3. What are the contrasting viewpoints or competing evidence?

**(High Confidence)** One legitimate competing view is that unsupported features should be represented as skipped because test frameworks intentionally use skip/abort states for environment-dependent preconditions. TAP and JUnit both support that workflow. [TAP format documentation](https://tapjs.org/tap-format/) ([tapjs.org](https://tapjs.org/tap-format/?utm_source=openai)) [JUnit User Guide](https://docs.junit.org/current/user-guide/junit-user-guide-6.0.1.pdf) ([docs.junit.org](https://docs.junit.org/current/user-guide/junit-user-guide-6.0.1.pdf?utm_source=openai))

**(High Confidence)** That view is correct for a test suite asking, “does this optional feature work where available?” It is incorrect for a UI-fidelity certification asking, “did this run establish no visual difference for all requested properties?” In the latter case, skip semantics create a false interpretation risk because TAP can report an overall passing stream with skipped points. <INFERENCE from="[TAP documentation: skipped points are not treated as failure overall; certification claim requires evidence for all required observations]">A required unavailable measurement must be non-success even if the engine behavior is expected or accepted.</INFERENCE> [TAP format documentation](https://tapjs.org/tap-format/) ([tapjs.org](https://tapjs.org/tap-format/?utm_source=openai))

**(Medium Confidence)** Another competing practice is to suppress visual noise through broad image thresholds or masks. Pixelmatch, Playwright, ODiff, and ImageMagick intentionally offer thresholding and masking-like controls because raster comparison has real noise sources. [Pixelmatch README](https://github.com/mapbox/pixelmatch) ([github.com](https://github.com/mapbox/pixelmatch?utm_source=openai)) [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots) ([playwright.dev](https://playwright.dev/docs/test-snapshots?utm_source=openai)) [ODiff README](https://github.com/dmtrKovalenko/odiff) ([github.com](https://github.com/dmtrKovalenko/odiff?utm_source=openai)) [ImageMagick compare documentation](https://imagemagick.org/compare/) ([imagemagick.org](https://imagemagick.org/compare/?utm_source=openai))

**(High Confidence)** Broad tolerance is not a remedy for an unavailable DOM measurement. It changes a result from “we do not know” to “we will ignore some differences,” which is a different and weaker claim. <INFERENCE from="[CSSOM empty-string semantics; image tools’ documented raster-oriented thresholds]">The two controls must remain separate in configuration, reporting, and governance: capability availability controls whether a property may be compared; tolerance controls how measured values are judged.</INFERENCE> [CSSOM Level 1](https://drafts.csswg.org/cssom/) ([drafts.csswg.org](https://drafts.csswg.org/cssom/)) [Pixelmatch README](https://github.com/mapbox/pixelmatch) ([github.com](https://github.com/mapbox/pixelmatch?utm_source=openai))

### 4. What changed recently, and what is the trajectory?

**(High Confidence)** The most material recent development is the publication of the February 2026 empirical study on web visual flakiness. It isolates non-deterministic visual behavior as its own empirical category and provides a taxonomy across **262** real-world cases, including Chromium. [University of Luxembourg repository record for Pei, Sohn, Papadakis, 2026](https://orbilu.uni.lu/handle/10993/68138) ([orbilu.uni.lu](https://orbilu.uni.lu/handle/10993/68138?utm_source=openai))

**(High Confidence)** Tooling has also become more explicit about screenshot stabilization. Playwright documents animation disabling/fast-forwarding, hidden carets, and injected styles for screenshot determinism; these controls are materially better than fixed sleeps, which WPT identifies as an instability source. [Playwright Page screenshot API](https://playwright.dev/docs/next/api/class-page) ([playwright.dev](https://playwright.dev/docs/next/api/class-page?utm_source=openai)) [WPT testharness.js API](https://web-platform-tests.org/writing-tests/testharness-api.html) ([web-platform-tests.org](https://web-platform-tests.org/writing-tests/testharness-api.html?utm_source=openai))

**(Medium Confidence)** The likely trajectory is toward separating three concerns that older visual-diff stacks frequently blur: conformance/capability, state determinism, and visual difference judgment. <INFERENCE from="[WPT multi-state outcomes; WebKit result taxonomy; Pei et al. visual-flakiness taxonomy; Playwright deterministic capture controls]">A robust future differ will emit capability manifests and coverage evidence alongside DOM and image diffs, rather than treating a single pass/fail bitmap as sufficient certification.</INFERENCE> [WPT testharness.js API](https://web-platform-tests.org/writing-tests/testharness-api.html) ([web-platform-tests.org](https://web-platform-tests.org/writing-tests/testharness-api.html?utm_source=openai)) [WebKit Results Database](https://results.webkit.org/documentation) ([results.webkit.org](https://results.webkit.org/documentation?utm_source=openai)) [Pei et al., 2026](https://www.sciencedirect.com/science/article/abs/pii/S0164121226000609) ([sciencedirect.com](https://www.sciencedirect.com/science/article/abs/pii/S0164121226000609?utm_source=openai))

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| `getComputedStyle()` returns resolved values for supported properties of a connected, rendered target; computed declarations are otherwise empty | CSSWG | Living standard; accessed August 18, 2026 | Normative specification | https://drafts.csswg.org/cssom/ |
| `getPropertyValue()` returns `""` when no matching declaration exists; `setProperty()` returns without setting unsupported CSS properties | CSSWG | Living standard; accessed August 18, 2026 | Normative specification | https://drafts.csswg.org/cssom/ |
| SVG `getBBox()` must invoke bounding-box computation and return a computed `DOMRect`; inability to compute non-rendered geometry should throw | SVG Working Group | Editor’s draft; accessed August 18, 2026 | Normative specification | https://svgwg.org/svg2-draft/types.html |
| Modernizr supports property/value and injected-style behavioral feature tests | Modernizr project | Current docs; accessed August 18, 2026 | First-party technical documentation | https://modernizr.com/docs/ |
| WPT exposes `PASS`, `FAIL`, `TIMEOUT`, `NOTRUN`, and `PRECONDITION_FAILED` states | web-platform-tests project | Current docs; accessed August 18, 2026 | First-party technical documentation | https://web-platform-tests.org/writing-tests/testharness-api.html |
| Servo reported 1.81 million WPT passes and cautioned against treating WPT as a complete real-world usability measure | Servo maintainer | February 19, 2026 | First-party maintainer statement | https://github.com/servo/servo/discussions/42711 |
| WebKitGTK runs layout, pixel, WebDriver, and WPT-related tests; WebKit result DB distinguishes failures, image failures, timeouts, crashes, and errors | WebKit project | Current docs; accessed August 18, 2026 | First-party technical documentation | https://trac.webkit.org/wiki/WebKitGtkLayoutTests ; https://results.webkit.org/documentation |
| TAP skip/TODO directives can allow an overall passing stream despite skipped points | TapJS project | Current docs; accessed August 18, 2026 | First-party format documentation | https://tapjs.org/tap-format/ |
| JUnit assumptions abort rather than fail tests | JUnit team | Current guide retrieved August 2026 | First-party framework documentation | https://docs.junit.org/current/user-guide/junit-user-guide-6.0.1.pdf |
| Vacuous satisfaction can make a positive verification result misleading; vacuity detection should accompany success | Beer, Ben-David, Eisner, Rodeh / IBM Research | March 1, 2001 | Peer-reviewed formal-methods research | https://research.ibm.com/publications/efficient-detection-of-vacuity-in-temporal-model-checking |
| Pixelmatch default threshold is `0.1`; anti-aliasing detection is enabled unless `includeAA` is set | Mapbox Pixelmatch project | Current repository; accessed August 18, 2026 | First-party tool documentation | https://github.com/mapbox/pixelmatch |
| Playwright screenshot comparison uses Pixelmatch and exposes `maxDiffPixels`; screenshot capture supports animation disabling, caret hiding, and injected styles | Microsoft Playwright project | Current docs; accessed August 18, 2026 | First-party tool documentation | https://playwright.dev/docs/test-snapshots ; https://playwright.dev/docs/next/api/class-page |
| ImageMagick provides RMSE, SSIM, AE, MAE, DSSIM and other image metrics; perfect RMSE is zero and perfect SSIM is one | ImageMagick project | Current docs; accessed August 18, 2026 | First-party tool documentation | https://imagemagick.org/script/command-line-options.php/ ; https://imagemagick.org/compare/ |
| CIEDE2000 is standardized for color-difference calculation | CIE / ISO | 2022 | International standard | https://www.cie.co.at/publications/colorimetry-part-6-ciede2000-colour-difference-formula-1 |
| Web visual flakiness study analyzed 262 cases; 59.9% structure-related and 40.1% style-related | Pei, Sohn, Papadakis | February 2026 | Peer-reviewed empirical study | https://www.sciencedirect.com/science/article/abs/pii/S0164121226000609 |
| ICSE UI-flakiness study analyzed 235 samples across 62 projects; web async-wait rate was 52.0% versus 32.5% mobile | Romano et al. | 2021 | Peer-reviewed empirical study | https://weihang-wang.github.io/papers/UIFlaky-icse21.pdf |
| Google reported 1.5% flaky executions, about 16% of tests with some flakiness, and 84% of pass-to-fail transitions involving flaky tests | Google Testing Blog | May 27, 2016 | First-party engineering write-up | https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html |

## Knowledge Gaps

### Engine-specific observability evidence

<MISSING_DATA>[A versioned reproduction identifying the exact non-Chromium engine, shell, operating system, and build that return empty strings for `boxShadow`, `backgroundImage`, `textTransform`, transition/animation properties, and pseudo-element content—and all-zero `getBBox()`—was not provided. This is needed to distinguish an implementation defect, a detached/non-rendered probe, a binding-layer omission, and intentional API scope.]</MISSING_DATA>

### Ladybird / LibWeb property-level capability reporting

<MISSING_DATA>[A first-party Ladybird/LibWeb capability matrix specifically covering computed-style serialization, pseudo-element styles, CSS animation/transition fields, and SVG `getBBox()` was sought but not verified. Required evidence: versioned WPT result links, implementation issue references, or a first-party API support table.]</MISSING_DATA>

### Universal per-property DOM tolerances

<INSUFFICIENT_EVIDENCE>[No primary empirical source was found validating fixed universal tolerances for `line-height`, `letter-spacing`, width, height, or SVG geometry across browser engines. Existing tool defaults largely concern screenshot pixels, not computed CSS values.]</INSUFFICIENT_EVIDENCE>

### Detector-inertness prevalence

<MISSING_DATA>[No study was found reporting the percentage of CSS/DOM visual differs that silently certify equality because both observation paths return the same unavailable sentinel. Required evidence: a benchmark corpus of differ implementations subjected to capability-stub mutation.]</MISSING_DATA>

### Claimed mitigation effect sizes

<INSUFFICIENT_EVIDENCE>[Case reports and tool documentation support font pinning, animation control, and volatile-region styling, but broad before/after false-positive-rate measurements for these interventions in DOM-and-screenshot visual regression were not found in the primary sources reviewed.]</INSUFFICIENT_EVIDENCE>

## Recommended Next Steps

1. **Implement the capability manifest and non-success exit contract first.**  
   **Rationale:** This directly prevents the present false-certification mechanism. Add `MEASURED`/`UNAVAILABLE`/`UNSTABLE`/`ERROR` per primitive and make any required unavailable state return exit code `2`.

2. **Build a versioned probe corpus for all compared property families.**  
   **Rationale:** Each property needs positive and mutation sentinels, including generated pseudo-elements and connected positive-geometry SVG. Run it at process start and whenever engine build, OS image, font package, or shell mode changes.

3. **Create detector mutation tests.**  
   **Rationale:** Stub each reader to return `""`, a constant value, and zero geometry; verify that every one yields `INCONCLUSIVE`, never `PASS`. This is the practical vacuity check for the checker itself.

4. **Separate DOM-certification and screenshot-noise policies.**  
   **Rationale:** Keep computed-style semantic equality strict; configure Pixelmatch/SSIM/RMSE only in the raster layer. Capture both artifacts so a reviewer can see whether a detected problem is DOM, geometry, or pixels.

5. **Collect an engine matrix before admitting alternative engines to blocking CI.**  
   **Rationale:** Run the probe corpus against exact Servo, WebKitGTK/WPE, Ladybird/LibWeb, and any headless shell builds you intend to certify. Promote an engine from experimental to blocking only when required-observation coverage is complete and repeat-run stability is demonstrated.

## Sources

- [CSS Object Model (CSSOM) Module Level 1](https://drafts.csswg.org/cssom/?utm_source=openai)
- [Basic Data Types and Interfaces — SVG 2](https://svgwg.org/svg2-draft/types.html)
- [Implementing feature detection - Learn web development | MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Testing/Feature_detection?utm_source=openai)
- [Test Anything Protocol](https://tapjs.org/tap-format/?utm_source=openai)
- [JUnit User Guide](https://docs.junit.org/current/user-guide/junit-user-guide-6.0.1.pdf?utm_source=openai)
- [CSS Object Model (CSSOM) Module Level 1](https://drafts.csswg.org/cssom/)
- [GitHub - mapbox/pixelmatch: The smallest, simplest and fastest JavaScript pixel-level image compa...](https://github.com/mapbox/pixelmatch?utm_source=openai)
- [Visual comparisons | Playwright](https://playwright.dev/docs/test-snapshots?utm_source=openai)
- [Efficient detection of vacuity in temporal model checking for Formal Methods in System Design - I...](https://research.ibm.com/publications/efficient-detection-of-vacuity-in-temporal-model-checking?utm_source=openai)
- [testharness.js API — web-platform-tests documentation](https://web-platform-tests.org/writing-tests/testharness-api.html?utm_source=openai)
- [WebKit Results Database: Documentation](https://results.webkit.org/documentation?utm_source=openai)
- [An empirical study of web visual flakiness: Characterisation and fix strategies - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0164121226000609?utm_source=openai)
- [Modernizr Documentation](https://modernizr.com/docs/?utm_source=openai)
- [Roadmap for implemented features · servo servo · Discussion #42711 · GitHub](https://github.com/servo/servo/discussions/42711?utm_source=openai)
- [WebKitGtkLayoutTests – WebKit](https://trac.webkit.org/wiki/WebKitGtkLayoutTests?utm_source=openai)
- [On the use of commit-relevant mutants | Empirical Software Engineering | Springer Nature Link](https://link.springer.com/article/10.1007/s10664-022-10138-1?utm_source=openai)
- [IEEE TRANSACTIONS ON SOFTWARE ENGINEERING](https://dijkstra.eecs.umich.edu/kleach/eecs481/w21/readings/mutation-testing.pdf?utm_source=openai)
- [Page | Playwright](https://playwright.dev/docs/next/api/class-page?utm_source=openai)
- [ImageMagick | Command-line Options](https://imagemagick.org/script/command-line-options.php/?utm_source=openai)
- [ImageMagick | Command-line Tools: Compare](https://imagemagick.org/compare/?utm_source=openai)
- [Colorimetry-Part 6: CIEDE2000 Colour-Difference Formula | CIE](https://www.cie.co.at/publications/colorimetry-part-6-ciede2000-colour-difference-formula-1?utm_source=openai)
- [Test flakiness’ causes, detection, impact and responses: A multivocal review - ScienceDirect](https://doi.org/10.1016/j.jss.2023.111837?utm_source=openai)
- [GitHub - dmtrKovalenko/odiff: A very fast SIMD-first image comparison library (with nodejs API) ·...](https://github.com/dmtrKovalenko/odiff?utm_source=openai)
- [PhD-FSTM-2025-130](https://orbilu.uni.lu/bitstream/10993/66145/1/thesis.pdf?utm_source=openai)
- [Bug: toHaveScreenshot changes page style and changes font family · Issue #29968 · microsoft/pla...](https://github.com/microsoft/playwright/issues/29968?utm_source=openai)
- [Bug: There some font diff from the same docker env in CI and my machine · Issue #35143 · micros...](https://github.com/microsoft/playwright/issues/35143?utm_source=openai)
- [Improved anti-aliasing · Issue #74 · mapbox/pixelmatch · GitHub](https://github.com/mapbox/pixelmatch/issues/74?utm_source=openai)
- [An Empirical Analysis of UI-based Flaky Tests](https://weihang-wang.github.io/papers/UIFlaky-icse21.pdf?utm_source=openai)
- [Google Testing Blog: Flaky Tests at Google and How We Mitigate Them](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html?m=1&utm_source=openai)
- [ORBilu: An Empirical Study of Web Visual Flakiness: Characterisation and Fix Strategies - 2026](https://orbilu.uni.lu/handle/10993/68138?utm_source=openai)
