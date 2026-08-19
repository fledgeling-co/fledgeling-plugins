# Engine capability matrix — what this engine can and cannot answer

**This file is the single home for capability facts.** Before it existed, one paragraph about the font
class appeared in six places, and the copies had already diverged — one said the packaged-browser driver
"is gone" while another still described the harness as running Playwright. Six copies of one fact meant
that fact was the only capability anyone ever re-checked, and eight further classes were silently
unmeasurable for nine versions. When a capability changes, change it here, and let the other files link.

**Every row is a measurement, not an architectural truth.** A capability claim without a date and a
version is the habit that produced the defect above: it reads as settled when it is a reading someone
took once, on one machine, against one build.

---

## Measured 18 August 2026 · obscura 0.2.0 · macOS 15 (Darwin 25.6.0)

Method: an authored `<style>` rule (not an inline `style` attribute — see the trap below) applied to a
laid-out element, read back through `getComputedStyle`. This is the same round trip
`analyze.js`'s `probeCapabilities()` runs at capture time, so the table and the tool cannot drift.

### Cannot be measured — the differ switches these classes off

| Read | Set to | Comes back | Working longhand? |
|---|---|---|---|
| `boxShadow` | `3px 5px 7px 11px rgb(1,2,3)` | `""` | **none exists** |
| `backgroundImage` | `linear-gradient(rgb(1,2,3), rgb(4,5,6))` | `""` | **none exists** |
| `textTransform` | `uppercase` | `""` | **none exists** |
| `transitionProperty` / `transitionDuration` | `color 1s` | `""` / `""` | **none** |
| `animationName` / `animationDuration` | `mfprobekfa 2s infinite` | `""` / `""` | **none** |
| `document.getAnimations().length` | one running animation | `0` | — |
| `flex` **and** `flexGrow` | `1 1 auto` | `""` / `""` | **longhand also empty** |
| `getComputedStyle(el, '::after')` | `content:"X"; border-top:3px` | the **element's own** style | — |
| `getComputedStyle(input, '::placeholder').color` | `rgb(1,2,3)` | the **input's own** colour | — |
| `path.getBBox()` | `M2 2 L14 9 Z` | `{0,0,0,0}`, and does **not** throw | — |

### Can be measured — these carry the audit

| Read | Set to | Comes back |
|---|---|---|
| `paddingTop` / `marginTop` | `16px` / `40px` | correct (the **shorthands** `padding` and `margin` return `0px`) |
| `borderTopLeftRadius` | `9px` | correct (the shorthand `borderRadius` returns `0px`) |
| `borderTopWidth` / `borderTopColor` | `1px solid #123456` | correct (the shorthand `border` returns `""`) |
| `rowGap` / `columnGap` | `8px` | correct (the shorthand `gap` returns `normal`) |
| `outlineWidth` | `2px solid green` | correct (the shorthand `outline` returns `""`) |
| `lineHeight` | `27.9px`, and `1.5` on `20px` | `27.9px` and `30px` — resolved, so the value-based line-height check is sound |
| `letterSpacing` | `1.5px` | correct |
| `display`, `flexDirection`, `fontSize`, `fontWeight`, `color`, `backgroundColor`, `textAlign`, `width`, `height` | — | correct |
| `document.styleSheets[].cssRules` | — | readable, and `:hover` selectors enumerate — the interaction-state layer is live |
| `Emulation.setDeviceMetricsOverride` | 390×900 | `innerWidth: 390` and `matchMedia("(max-width:500px)")` true — the responsive layer is sound |

**Read shorthands as unknown, never as zero.** Five shorthands return `0px` or `""` while their
longhands are correct. A spacing assertion written against `padding` passes on two zeros.

---

## Three traps that make the obvious approach wrong

### 1. An inline `style` attribute is echoed back verbatim, so an inline probe reports a false PASS

Set `el.style.boxShadow = '0 2px 4px rgba(0,0,0,.3)'` and `getComputedStyle(el).boxShadow` returns
`"0 2px 4px rgba(0,0,0,.3)"` — the string you wrote, uncanonicalised, from an engine that does not
implement the property. A real browser would return `"rgba(0, 0, 0, 0.3) 0px 2px 4px 0px"`.

This matters twice over. It is why `probeCapabilities()` uses an inserted **stylesheet rule** rather
than an inline style: the published probe-node recipes all set the declaration inline, and every one of
them would report box-shadow as measurable here. And a two-sentinel metamorphic probe does not save an
inline approach either — two different inline values read back as two different strings, so the
discriminating check passes too. The stylesheet path is the only correct route, and only a measurement
finds that out.

It is also a **false-positive** source in the diff itself: one side declaring a shorthand inline and the
other in a stylesheet compares `"0 2px 4px …"` against `""`. Normalise any shorthand string before
comparing it, the way v2.5.1 already does for `fontFeatureSettings`.

### 2. `CSS.supports()` disagrees with the engine, in both directions

Measured over ten declarations: it answered `true` for `text-transform`, `background-image`, `animation`
and `flex` — all of which compute to `""` — and `false` for `letter-spacing`, which works. Four
false-positives and one false-negative out of ten. `CSS.supports` answers a question about declaration
parsing, not about whether a resolved value comes back through `getComputedStyle`. It is a diagnostic to
record, never the gate.

### 3. A pseudo-element read returns a plausible WRONG value, not an empty one

A probe declaring `border-top: 9px` on the element and `content:"X"; border-top: 3px` on its `::after`
reads back `9px` from the pseudo — the element's own border, field for field identical to
`getComputedStyle(el)`. So pseudo measurement is **refused**, not merely marked unavailable. Dropping the
content-truthiness guard that currently skips these nodes would not restore the `::after` border fold; it
would start folding each element's own border in as if the pseudo drew it, double-reporting one defect as
two and inventing values on both sides.

---

## What the engine does that a fidelity differ must not report as an application defect

These are engine artefacts. A differ that files them as app bugs burns the reader's trust, and the
published work on visual-regression flakiness is consistent that a noisy corpus trains people to
discount real failures.

- **Web fonts never load.** A working woff2 and a 404'd one measure identically, every `@font-face`
  stays `unloaded`, and named families collapse onto three generic metric buckets (Georgia==serif,
  Arial==Impact==sans-serif, Courier New==monospace). Every typeface question moves to a real browser.
  `feature-check.mjs` is worse than unavailable here — its verdict **inverts**, because both probe rows
  render the same fallback and identical MEANS "ineffective", so every requested OpenType feature is
  reported as a defect, confidently and wrongly. Do not run it against an obscura capture.
- **An `opacity: 0` entry keyframe strands its element at opacity 0.03 forever.** No animation executes,
  so the element never animates in. It looks exactly like a z-index or stacking bug.
- **Native form controls do not render at all.** A real radio input draws nothing, which looks exactly
  like a missing affordance.
- **A line carrying an inline citation marker gets mangled** — a space is eaten and the line breaks
  before the anchor. Review typography on a marker-stripped copy.
- **`Emulation.setEmulatedMedia` is accepted and inert.** `prefers-reduced-motion` and `print` stay
  false, so there is no reduced-motion or print pass. A CDP method returning without an error proves
  only that it was accepted; assert the observable it is supposed to change.
- **Rendering is a fixed 1280×720 for `obscura fetch`, with no viewport flag.** Use `obscura serve` plus
  CDP for any other viewport, and for anything that needs a promise awaited — neither `obscura fetch
  --eval` nor the MCP `browser_evaluate` awaits one, so neither can run `analyze.js`.

Obscura's rasterisation is deterministic across machines, which keeps raster-crop noise stable. Stable is
not faithful: every text crop is drawn in a fallback face on both sides. A raster percentage is a trigger
to open the diff crop, never a verdict.

---

## The second engine · proctor MCP · native macOS

Read alongside `references/native-lane.md`, which carries the method. This section is the capability
facts, because this file is their single home and a second copy is how the first nine classes stayed
hidden for nine versions.

**The engine's capability is not fixed — it has two tiers, and which one a run is in is measured
per app, not assumed.** `proctor_inspect` returns a resolved view and layer hierarchy for an app
embedding `ProctorReflector`, and `reflectorUnavailable` for one that does not. Establish the tier with
a two-level inspect before Phase 2 and record it; every style row below inverts on it.

| Read | Tier A (reflector) | Tier B (`reflectorUnavailable`) |
|---|---|---|
| resolved colour, font, corner radius, opacity, shadow | measured, with `CALayer` model **and** presentation values | **inconclusive** — the ceiling is the tree plus pixels |
| layout constraints | measured (`includeConstraints`, large) | inconclusive |
| frame geometry, containment, alignment | measured | measured |
| hit-target size, label, role, enabled, focus order | measured | measured |
| structure and ordering | measured | measured |
| contrast | measured from pixels | measured from pixels |
| observer disagreement (`agree`) | measured | measured |

**What this engine measures that obscura cannot.** Five classes obscura returns `""` for are readable
here as layer properties rather than as CSSOM declarations, which is the reason this lane exists for web
targets too and not only for native ones:

| Class | obscura | proctor, Tier A |
|---|---|---|
| `boxShadow` | `""`, no working longhand | layer `shadowOpacity` / `shadowOffset` / `shadowRadius` |
| `borderRadius` shorthand | `0px` | layer `cornerRadius` |
| animation in flight | `getAnimations()` returns `0` while the animation runs | model vs presentation values differ exactly while in flight |
| whether a capture is current | no signal at all | `SCFrameStatus`, `dirtyRectCount`, `framesWaited`, `trustworthy` |
| a control with no node behind it | not expressible | **unconfirmed** — see the note below |

**`unexposedControl` did not fire, measured 20 Aug 2026.** The tool documents this disagreement
kind and gives a worked example at 96×28. A fixture planting exactly that
(`evals/fixtures/mac-settings`) produced six to seven `agree` findings across three runs and none
of them was `unexposedControl`, at 38×22 and again at 96×28 with a label — while
`proctor_assert` `exists` on the same control returned `found: false` and the capture showed it
painted. `ghostNode`, its mirror image, fired correctly in the same runs. The row above says
unconfirmed rather than measured because a capability read from documentation and never exercised
is the thing this file exists to stop.

**Known ceilings, stated as capability rather than as clean rows.** An iOS Simulator target has no
accessibility tree, no elements and no geometry — `proctor_ios` is a device lane and its screenshots
carry no frame status, so they are untrustworthy by construction; the React Native lane remains the
answer there. A macOS submenu built lazily reports `submenuPopulated: false` and is not descended into,
which is inconclusive rather than an absent menu. And the reflector is a debug-build dependency, so a
release build measures at Tier B whatever its debug twin managed.

**A tolerance here is calibrated, never defaulted.** Every geometry assertion takes `tolerance` in
points and defaults it to 1.0. The evidence behind this skill is explicit that a numeric tolerance is
defensible only after repeated-run measurement proves non-zero variance, so `proctor_stability` runs
first and its `stepInstability` sets the number. A default carried into a report is an assumption
wearing a calibration's clothes.

---

## Re-measuring this table

`node assets/diff/capture.mjs --ref <url> --target <url> --out <dir>` prints the preflight block on every
run, and `target.findings.json` carries `summary.capabilities` for both sides plus an `inconclusive[]`
array naming the detector classes each silenced capability takes with it. To probe without a full
capture, inject `analyze.js` and call `globalThis.__MF_PROBE__()`.

When a row here changes, the tool notices before you do — the preflight is the source and this file is
the readable copy. Update the date and the version in the heading, not just the cell.
