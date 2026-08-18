# The mechanical analytic — its blind spots, its false positives, and its prior art

Two scripts turn "I diffed both sides" from an aspiration into a fact: **`capture.mjs`** (the Node harness)
and **`analyze.js`** (the browser-injectable analyzer and differ it injects). They exist because the failure
mode that ships drift is **eyeballing the dumps** — even with both sides measured to disk, scanning JSON by
eye silently skips properties (a muted-vs-dark section label, a 13-vs-16 input font, a 16-vs-20 gutter, an
inherited `.card.ai-card` shadow). A script that compares **every captured property** per element cannot
skip one. The agent reads the **findings**, not the raw dumps; screenshots are a later, visual-only
confirmation.

Computed style is the only truth on the way in, too: a class like `.ai-card` may declare no `box-shadow`,
yet an element `class="card ai-card"` still HAS one, inherited from `.card`. Reading the class rules by hand
misses it.

- **How to run it** — flags, contracts, commands: [`run.md`](./run.md).
- **What this engine can and cannot measure** — dated, versioned, one home:
  [`../../references/engine-capability-matrix.md`](../../references/engine-capability-matrix.md).
- **Every real miss → the check that now catches its class**:
  [`../../references/issue-to-check-map.md`](../../references/issue-to-check-map.md).

This file covers the four things neither of those carries: what the tool still cannot see, what it
over-reports, the scrape trap, and when to reach for something else instead.

## ⚠️ Reference the LIVE rendered site, not a re-served static scrape

The single biggest source of "I matched the mock exactly but it still looks wrong": a
**runtime-hydrated site (Framer, most page builders, any SPA) does NOT render the same when its scraped HTML
is re-served from localhost.** The scrape freezes the markup + every breakpoint variant's CSS, but the
framework's JS resolves the *final* desktop layout at runtime — and re-served off-origin (with its
`framerusercontent`/`gstatic` fetches broken) that JS doesn't re-execute, so the page falls back to a
*different variant*. Real divergences this caused (all where the scraped CSS literally contained BOTH
values): a nav gap that was **10px in the served scrape but 16px on live**; a hero gradient that exists
**only as an `<img>` on live** (gone from the scrape); `text-wrap`/font resolution that differed. Every one
of those made the differ report "identical" against the wrong target.

**So: capture the reference from the LIVE URL** (`analyze.js` runs fine against `https://…` through the same
browser), not from a localhost-served scrape. Keep the scrape only for content/copy. If you can only get a
scrape, treat its resolved geometry as *suspect* and spot-check key values against the live site.

Three measurement disciplines that came from the same debugging:

- **Measure the STYLED element, not the inner text node.** A CTA's text node was `h=20` (read as "plain text
  link") while its button `<a>` was `h=42` (a pill). Pairing the text node's box led to deleting a real
  pill. Walk to the styled ancestor — the box-walk already does this; trust it over a hand `find(text)`.
- **Backgrounds can be `<img>`/`<canvas>`/SVG layers invisible to a `background-image` scan.** A hero
  "gradient" was a full-bleed `<img>` (an SVG), so `getComputedStyle(...).backgroundImage` was `none`. When
  hunting a visual fill, scan for large `img`/`canvas`/`svg` children too.
- **Self-host the EXACT webfont the live site loads** (the specific Google `vNN` woff2), not a same-named
  package — `@fontsource/inter` renders ~2px wider per label than Google's Inter v20, shifting widths and
  wrap points. Glyph-width fidelity needs the byte-identical file.

## Known remaining blind spots (verify these by eye / structurally)

### Nine classes this engine cannot measure at all

A runtime preflight switches these off and reports `available:false` with a verbatim reason rather than
agreeing. **Zero findings in a silenced class is not a pass** — it is a question nobody asked, and
`capture.mjs --assert` returns **3 (inconclusive)** rather than 0 while any of them is silenced. Each has to
be confirmed in a real browser, with the reason relayed verbatim and the confirming surface recorded.

| Silenced class | What goes unchecked |
|---|---|
| **shadow** | `box-shadow` computes to `""`, so **neither the depth NOR the presence of a shadow is checked** — a card that lost its elevation entirely reads as matching. There is no working longhand to fall back to. |
| **gradient** (the CSS half) | `background-image` computes to `""`, so a CSS gradient or `url()` fill is invisible. The full-bleed `<img>`/`<canvas>`/`svg` media-layer check still works, and it is what catches the hero and CTA-band cases. |
| **text-transform** | An all-caps-vs-title-case header whose SOURCE text is identical reads as matching. |
| **transition** | `transitionProperty` / `transitionDuration` compute to `""`, so a declared transition (a hover colour fade present on live, absent on the rebuild) is unmeasurable. |
| **animation** | `animationName` computes to `""` and `document.getAnimations()` reports `0` even with one running, so "reference animates, target is static" is unreportable. |
| **flex shorthand** | `flex` *and* `flexGrow` both compute empty, so flex-grow/shrink/basis reasoning has nothing to read. `display`, `flex-direction`, `row-gap` and `column-gap` are unaffected and still carry the layout class. |
| **pseudo-elements** | **REFUSED, not merely unavailable:** `getComputedStyle(el, '::after')` ignores the pseudo argument and returns the ELEMENT's own computed style, so reading it would fold the element's own border in as if the pseudo drew it. The `::after` border fold, the missing-bullet/`counter()` marker check and the systematic pseudo comparison are all off. A border, hairline, overlay or marker drawn on `::before`/`::after` must be confirmed in a real browser. |
| **`::placeholder`** | A placeholder's colour reads back as the input's own. |
| **SVG glyph extent** | `getBBox()` returns an all-zero rect **without throwing**, so icon-glyph size and the glyph-based trailing-arrow check cannot run. Both fall back to svg **PRESENCE** (the laid-out box) and their findings are labelled presence-only: a **MISSING** arrow or icon is caught, a **wrong-size or swapped** glyph is not, and a hidden or empty svg reads as present. |

The whole **font class** has no signal here either — no web font ever loads, so both sides render the same
fallback face and every font check honestly agrees. All of it is measured, dated and versioned in
[`engine-capability-matrix.md`](../../references/engine-capability-matrix.md).

### Classes the differ is structurally blind to, in any engine

It is **text-probe driven** — it diffs the styles of reference text nodes and their ancestor boxes, plus the
screen background and the structurally-paired non-text containers. These still need a structural pass and a
screenshot:

- **Non-text visual elements** with no associated text — a divider line, a standalone icon, an image, a
  decorative bar, a chart, an avatar. PARTIAL COVER: a leading tile/icon/avatar or trailing icon/badge that
  is mis-INSET is caught via `row-left-inset`/`row-right-inset` (the row's leftmost/rightmost edge), and the
  IoU text-less pairing plus the raster crop catch a *missing* one — but its identity and colour still are
  not compared.
- **App-EXTRA elements** — listed in the `extra` class (target text with no reference match). Still
  text-only (an extra non-text badge/divider with no text isn't caught) and inherently noisy (legitimate
  extra data rows appear too) — a scan aid, not a hard fail.
- **Icon glyph correctness** — a reference Material ligature vs an app SVG are different representations,
  and with glyph extent unavailable here the differ can only confirm that *something* is there.
  **Actionable:** treat every unmatched Material ligature (`arrow_upward`, `tune`, `add_circle`,
  `auto_awesome`) as a glyph to eye-check — it is a faithful SVG equivalent OR the wrong glyph. (Real misses
  caught this way: a paper-plane `send` where the mock is an up-arrow `↑`; a settings-gear where the mock is
  `tune`/sliders.)
- **Component-PRIMITIVE choice for an always-dynamic-text element** — when an element's text is *always*
  real data (a category badge, a status pill, a row title, a price), its text never equals a reference probe,
  so the differ **never style-compares it at all** and a wrong primitive is invisible. This is how a category
  rendered as a large title-case `Chip` survived where the mock uses a small uppercase `.badge`: the text
  never matched, so the 13/500-vs-10/600 gap was never seen. For every element whose text is dynamic,
  eye-check the *primitive* (chip vs badge vs row vs card).
- **Nested inline `<Text>` (RN harness limit)** — the harness resolves a deeply-nested inline span's
  `effStyle` as null, so its size/weight/colour can't be compared. Symptom: a section lead-in you can SEE is
  bold (`**Business.**`) reports `font-weight: null` — confirm by eye, don't chase.
- **`wrong-state` is NOT "missing".** A reference probe unmatched on the measured screen but present
  ELSEWHERE in the full dump means you measured the **wrong state** — a surface unopened, or the scope set
  to the wrong screen — so its geometry and style were never checked at all. Re-measure the populated state
  before trusting the report. (This is how the Invest "Example brokers" inset first hid: diffed against the
  wrong tab.)

So: **0 unexplained findings is necessary, not sufficient.** Always finish with a structural
present/divergent/absent pass and a screenshot for the classes above.

## Known false-positive patterns (over-reporting — recognise, don't chase)

The blind spots above are *under*-reporting (real defects the differ misses). These are the opposite — rows
the differ flags that are **not** defects. Recognise them so you neither chase a phantom nor blanket-dismiss
a real one:

- **Element-vs-container box (largely fixed; watch the residual).** When a reference label sits *directly*
  on a styled element (a `.btn`/`.badge` span whose directText IS the label), the box to compare is that
  element. The differ checks the text node's own box first (self-before-parent) so a button compares against
  a button — but if you still see a box row reading *"target = the element's own bg/radius/pad, reference =
  a parent card (radius 12, pad 0)"*, that is a residual of this asymmetry: trust the matched **text** props
  and eye-check the element's box rather than "fixing" it to the card's values.
- **Repeated short text collides across roles.** A short label that appears in several roles — e.g. `10-Q`
  as a *filter chip*, a *card badge*, AND a *glossary bold-span* — can pair with the wrong sibling.
  **Tell:** ONE short repeated string producing a *burst* of font + box mismatches with wildly different
  values is a role collision, not N separate defects. Find the app element for the role the reference probe
  actually came from and verify that one. (The reliable kill: a matching `data-fid` on the two real nodes.)
- **Text-inset behind a leading icon/affordance.** A label that sits *after* a leading icon (a badge, an
  icon-led row) is measured at the inner text's x on the app side, while the reference may carry the text on
  the container span and measure at the container edge. A `left-inset` off by ≈ icon-width + gap is this,
  not a gutter defect — the container starts at the same gutter on both.
- **A raster mismatch is a trigger, not a verdict.** Obscura rasterises identically on every machine, which
  keeps crop noise stable, but stable is not faithful and every text crop is drawn in a fallback face on
  BOTH sides. Open the diff crop; never file a percentage as a defect on its own.
- **Guardrail-honest divergence.** When the mock fabricates specifics the target's product guardrails forbid
  (a made-up "200 pages", "every figure traced to filings", a fabricated AI summary), the target *should*
  diverge to honest copy — this shows up as an unmatched reference string and is an **intentional**
  divergence. Classify it like real-data or native-chrome: a recorded product decision, not "probably fine".

## Prior art — when to reach for an off-the-shelf tool instead

- **Web/DOM target:** **OverlayQA** / **Pixelay** (design-QA tools that extract computed CSS and diff a live
  page against a **Figma** spec) overlap with this differ. Prefer them when your source of truth is Figma
  and you're not in an agent/CI loop — but note they are Figma-bound and AI-narrated rather than
  deterministic, and none scope an RN device dump. (Assertion libraries built on a packaged-browser driver —
  Playwright's `toHaveCSS` and the like — are not an option here: that driver is gone, and this differ is
  what replaced it.)
- **Pixel/visual regression (Percy, Chromatic, BackstopJS, Applitools):** these diff an app against **its
  own** screenshot baseline, not against a design — and fine-grained-UI recall from vision is low.
  Complementary (catches overlap / z-order), not a substitute for the property diff.
- **React Native target:** there is **no** off-the-shelf equivalent. `react-test-renderer` / RNTL +
  `StyleSheet.flatten()` give *declared* styles in a node env, not the on-device *rendered* geometry — the
  exact "source ≠ render" trap this skill defeats. The RN harness + this differ fill that gap.
