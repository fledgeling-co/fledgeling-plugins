# Evidence — what each rule rests on

Every structural rule in this skill traces to one of three things: a measurement taken on this machine, a
documented failure in the skill's own history, or published work. This file records the third and the open
conflicts. When a claim here is a measurement, it carries its date and version, because a capability claim
without one reads as settled when it is a reading someone took once.

The full research corpus is committed under `docs/deep-research/` — four independent reports, exported
whole with their source registries, so any claim below can be checked from inside the repo.

---

## The panel

Four backends, run on one brief, 18 August 2026. Reserved at $9.70 worst case.

| Backend | Report | Sources |
|---|---|---|
| Google Gemini Deep Research | `gemini-capability-preflight.md` | 40 |
| OpenAI gpt-5.6 | `openai-capability-preflight.md` | 57 |
| Perplexity Sonar Deep Research | `perplexity-tristate-reporting.md` | 19 |
| xAI Grok | `xai-runtime-probing.md` | 10 |

**Citation verification** on the load-bearing report (OpenAI, 57 citations): fabrication check **PASS**,
0 dead links, 0 malformed URLs, 53 of 57 opened directly. Two blocked (ScienceDirect paywall) and two
unreachable (a JUnit user-guide PDF). One claim rests on the unreachable PDF alone — JUnit's
`TestAbortedException` semantics — and is therefore **not** load-bearing here: the same conclusion is
independently supported by the TAP documentation and by WPT's result states, and nothing in this skill
depends on the JUnit detail.

---

## What the panel agreed on, and what this skill does about it

**The probe-node round trip is the established pattern, and API presence is not a substitute.** All four
reports converge. `CSS.supports()` answers a question about declaration *parsing*, not about whether a
resolved value comes back through `getComputedStyle`; MDN and CSSOM are cited for the distinction, and
Modernizr's `testProp()` / `testStyles()` are named as the first-party precedent for behavioural rather
than name-based detection. → `probeCapabilities()` in `analyze.js`.

**The probe must use two sentinels, not one.** From the OpenAI report: a single sentinel can accidentally
equal an initial value, an engine fallback, or a hard-coded default, so a reader that returns the same
thing for every input passes a one-shot probe. Two semantically different sentinels make the probe
metamorphic — changing the input must change the observation — and the failure gets its own name,
`NON_DISCRIMINATING_READ`. → adopted; every probe reads twice and requires the reads to differ.

**The probe node must be connected and rendered.** CSSOM creates an empty declaration list unless the
target is connected, in the flat tree, and rendered, so a detached node answers a different question. →
the probe mounts to `document.body` at `position:absolute; left:-9999px` with a real size.

**"Could not measure" must be a first-class non-success outcome.** Unanimous. The recommended encoding is
JUnit `<error>` (not `<failure>`, not `<skipped>`) and explicitly **not** TAP `# SKIP`, because TAP treats
skipped points as non-failing overall — a skipped required detector can produce a green aggregate stream.
→ `inconclusive[]` in the artifact, printed on every run, and its own exit code.

**Coverage is not agreement.** From the OpenAI report, in the form that changed this build: "34/42
measured and all 34 equal" must be shown as `INCONCLUSIVE — 8 required observations unavailable`, never as
"100% agreement", because an agreement denominator that excludes unavailable checks can be numerically
perfect while omitting precisely the observations needed to substantiate the claim. → `summary.scoreCovers`
and `summary.scoreCaveat`; the score is never emitted bare when a class is silenced.

**Vacuous truth is the right frame, and it has a literature.** Beer, Ben-David, Eisner and Rodeh (IBM,
2001), *Efficient Detection of Vacuity in Temporal Model Checking*: a valid formula can conceal a real
defect because an implication's antecedent never occurs, and vacuity should be detected *even after a
positive result*. The UI-diff analogue is a detector whose differing-value path was never demonstrated. →
the preflight is that detection, and the stubbed-reader control in `measurement-enforcement.md` is the
witness generation.

**Test the detector, not only the subject.** Both the OpenAI and Perplexity reports recommend mutating the
oracle: stub each reader to return `""`, a fixed constant, and zero geometry, and assert that every one
yields INCONCLUSIVE rather than PASS. → the second required control in the seeded-defect eval.

**Do not import screenshot tolerances into computed-style comparison.** Pixelmatch's default threshold of
`0.1` is a YIQ colour-difference sensitivity parameter for a raster comparator with anti-aliasing
heuristics; it says nothing about whether a CSSOM observation was available. The defensible default for a
computed-style differ is exact semantic equality after normalisation, with a numeric tolerance derived only
from *measured* repeat-run variance in the actual environment. → the existing per-property tolerances keep
their derivations (`FM_TOL = 0.007` against a measured ~1.8% real case, 0.6px line-height because the
resolved value is precise, 2px height vs 10px width because height is discrete and width is
content-driven), and the 12% raster threshold stays scoped to the raster layer alone.

**Engine artefacts must not be filed as application defects.** The published failure modes match what this
engine does: absent web fonts change glyph widths and wrapping; animations captured mid-transition are
non-deterministic; viewport and scrollbar differences move breakpoints; GPU and compositor paths alter
anti-aliasing. Two empirical anchors worth carrying: Pei, Sohn and Papadakis (2026) classified 262 web
visual-flakiness cases as 59.9% structure-related and 40.1% style-related; Romano et al. (ICSE 2021)
analysed 235 flaky UI tests across 62 projects and found async-wait issues in 52.0% of web cases against
32.5% of mobile. And the reason it matters that noise stays low — Google reported roughly 1.5% of test
executions flaky, about 16% of tests showing some flakiness, and about 84% of pass-to-fail transitions
involving a flaky test: a noisy corpus trains people to discount real failures. → the false-positive
patterns section in `assets/diff/README.md`, and the engine-artefact list in
`references/engine-capability-matrix.md`.

---

## Where this skill departs from the research, and why

These are recorded rather than resolved. Each is a place where following the published guidance would have
produced a worse tool on this engine.

**1. The published probe recipe sets the declaration inline. Here that reports a false PASS.** Both the
Gemini and OpenAI reports give a probe that writes through `node.style` — `probeNode.style.boxShadow =
"10px 10px 5px red"` and `node.style.setProperty(property, first)` respectively. Measured 18 August 2026,
obscura 0.2.0: an inline `style` attribute is **echoed back verbatim** through `getComputedStyle`, even for
a property the engine does not implement. `el.style.boxShadow = '0 2px 4px rgba(0,0,0,.3)'` reads back as
that exact string, uncanonicalised, where a real browser returns `"rgba(0, 0, 0, 0.3) 0px 2px 4px 0px"`.

So an inline probe reports box-shadow as measurable, and the two-sentinel refinement does not save it —
two different inline values read back as two different strings, so the discriminating check passes too.
Only an inserted **stylesheet rule** takes the path an authored page takes. The published pattern is right
about the shape and wrong about the mechanism, and no amount of reasoning finds that: a measurement does.

**2. The panel recommends exit code 2 for inconclusive; this tool uses 3.** OpenAI and Perplexity both
land on 0/1/2 with 2 as INCONCLUSIVE; Gemini instead proposes the documented POSIX conventions, `125`
(which `git bisect` reserves for "the current source code cannot be tested") or `77` (automake's skip).
The panel does not agree with itself, and the local constraint decides it: `capture.mjs` already used exit
2 for usage and fatal errors before this change, and silently redefining an existing code is worse than
picking an unused one. So: 0 clean-and-complete, 1 findings, 2 usage/fatal, 3 inconclusive. The
substantive point every source shares — that inconclusive needs a *distinct non-zero* code and must never
fold into 0 — is honoured.

**3. `--allow-inconclusive` is a deliberate loosening, modelled on pytest's `xfail_strict`.** The
Perplexity report notes the tension between keeping suites green and enforcing coverage, and that pytest
lets teams choose. The escape hatch exists because a run whose silenced classes have all been confirmed in
a real browser genuinely is complete. It is guarded by documentation rather than by code, which is a known
weakness: nothing stops an agent passing the flag without doing the confirming. The ledger row required by
THE LAW rule 7 is the compensating control, and it is prose — so this is the softest joint in the design.

**4. The research has no number for the thing this skill is fixing.** Every report looked for a published
rate of silently-inert visual-diff detectors and none found one; all four filed it as a knowledge gap, and
OpenAI specified what would be needed (a benchmark corpus of differs subjected to capability-stub
mutation). The 9-of-9 figure in this plugin is a measurement of one engine, not an industry rate, and
should not be quoted as one.

**5. Ladybird and LibWeb have no first-party capability matrix.** Both reports that looked for one came
back empty; Ladybird's `Properties.json` lists properties at a syntax level, which is a starting point and
not an answer. This is why the matrix in this plugin is dated and machine-stamped rather than presented as
a property of "the engine".

---

## Measurements taken for this build

All on macOS 15 (Darwin 25.6.0), obscura 0.2.0, 18 August 2026. Full table:
`references/engine-capability-matrix.md`.

- Nine detector classes fail the round trip and are switched off.
- `getComputedStyle(el, '::after')` ignores the pseudo argument and returns the element's own computed
  style — so pseudo measurement is refused rather than merely unavailable, because reading it would fold
  the element's own border in as if the pseudo drew it.
- `CSS.supports()` disagreed with the engine on 5 of 10 declarations: false for `letter-spacing` (which
  works), true for `text-transform`, `background-image`, `animation` and `flex` (which do not).
- `path.getBBox()` returns an all-zero rect and does not throw. The Mermaid.js issue thread on the same
  behaviour argues for throwing rather than caching a bad value; this tool cannot make the engine throw,
  so it does the reachable equivalent — refuses the glyph claim, falls back to svg presence, and labels
  the finding presence-only.
- `lineHeight` resolves correctly (`27.9px`, and `1.5` on `20px` → `30px`), so the value-based
  line-height check is sound. `letterSpacing`, `rowGap`/`columnGap` and the border/radius/padding/margin
  longhands are all correct; five shorthands are not.
- `Emulation.setDeviceMetricsOverride` works and `document.styleSheets[].cssRules` is readable with
  `:hover` enumerable, so the responsive and interaction-state layers are live.

## A measurement from this build's own eval

On the ten-defect fixture in `evals/`, the version of this differ without a preflight caught 5, reported
one on the right element under the wrong property name, and returned **exit 0** — a clean shell status for
a page carrying ten planted defects. The rebuilt version catches 7, declares 3 inconclusive with reasons,
and exits 3. The delta that matters is not 5→7; it is four silent false passes → zero.

The layout miss was a compound failure worth recording, because it argues for the repair rather than for a
looser pairing rule: with a card ABSENT earlier in the tree, every later sibling index shifted, the row
container path-paired to a different element, and the flex-direction flip was reported as a `display`
mismatch instead. In isolation the same flip reported correctly. So an absent element hides layout defects
on everything after it, and `layout/container-pairing-repaired` is the note that says so.
