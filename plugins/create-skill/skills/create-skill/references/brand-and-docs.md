# Brand and docs — shipping the improved skill like a product

## The user checkpoints (hard gates, in this order)

1. **Name**: 3–4 candidates via AskUserQuestion, each with a one-line
   rationale, one marked recommended. Mine the marketplace's existing
   naming threads. The plugin directory is created/renamed only after
   the answer.
2. **Icon concepts**: 2–3 subject-mined directions described in words
   (register, glyph device, signature move) via AskUserQuestion. No
   icon or banner generation before the answer. The user chooses the
   concept, not just the rendering.

## Icon

### The marketplace aesthetic (bake this into every icon brief)

The set has a committed family look, learned from what the user actually
chose across six icons. Brief the mac-design-studio agent with all of it:

- **Outside shape is non-negotiable**: full-bleed 1024 on the set's exact
  superellipse (the path every sibling ships; a rounded-rect
  approximation visibly breaks the shelf). Any raster take that ships
  gets masked with that same path.
- **Ground register**: porcelain/daylight by default. The dark deep-sea
  register belongs to trawl alone; treat it as taken.
- **One warm accent**, in the vermilion/ember/amber family (kin to
  Fledgeling's #C4622D), reserved for the focal or semantic element —
  the seal, the hone line, the catch, the hull. Never spent on
  decoration.
- **Material over flatness**: rich, soft-3D Tahoe gel-glass — volumetric
  gel, authored translucency and overlap, one soft top light, real
  contact shadows. The user has twice chosen the raster take's richer
  material over a flatter vector (and once shipped the raster outright),
  so push the painterly volumetric end of the register and rebuild the
  winning material into the layered master.
- **Subject-mined literal glyph** with a stated signature move (the
  before/after boundary, the seal on the entry, the three hulls in
  echelon). No category clip-art, no glyph-on-blue-ramp.
- **16px survival** stays a non-negotiable audit check.

### The pipeline

**Route icon work to `create-mac-icon`.** Do not restate its procedure here and
do not brief an agent to reinvent it: it carries the direction catalogue, the
ground-truth corpus the master is measured against, the three-engine floor, the
`audit.html` template, the material-recipes library that grows with every
commission, and the measured fidelity loop with its scoring harness, review
sheet and blind judge panel. A hand-rolled icon pass gets none of that and
starts every lesson over.

Spawn an **Opus agent** briefed to read `create-mac-icon`'s SKILL.md and follow
it, plus:

- the chosen concept from the user checkpoint,
- the **marketplace aesthetic** above, since that is this repo's house style
  rather than the skill's,
- the sibling icons' glyph devices, so none is duplicated,
- and NO git operations.

Write the brief following `references/opus-5-prompting.md`: state first, task
last, no verification scaffolding, an explicit no-subagents cap, and the
artifacts named as things to sample values out of rather than reason about.

Expect back: the layered SVG master with its build script, the Arrow and raster
takes, `audit.html` with every take scored including losers, the fidelity run
directory, and any new construction appended to the skill's recipe library.

## Banner

Composed HTML via design-craft with ux-craft's Read-mode lens — never a
generated image standing in for typography:

- The **real icon asset** beside a **set wordmark** (a deliberate,
  defensible font choice; never the model's default reach), one-line
  essence, subject-mined palette.
- `banner-src.html` kept in assets/ so it's editable forever.
- **Derive the composition from the icon's own build script**, not from a
  sibling banner. The icon is a hand-authored master with named constants,
  so its cell sizes, light axis and accent are readable facts rather than
  estimates. Copying a sibling's measured light vector is the
  re-eyeballing the derivation exists to prevent; each icon is lit
  differently.
- Look at the render before accepting it, and crop into the small
  elements. A device that reads at 300px in the icon may be illegible at
  the same scale out on a 1600x520 bench, and the honest fix is usually to
  simplify it rather than to enlarge it and break the claim it was making.

### Render it with the script, because every failure here is silent

```bash
python3 scripts/render_banner.py plugins/<name>/assets/banner-src.html \
        --font "<Family>" --weight 700
```

It asserts five things, each of which has produced a wrong banner that
looked right:

1. **The viewport override took effect.** A CDP method returning without an
   error proves only that it was accepted, so `window.innerWidth` is read
   back.
2. **The font loaded**, measured as an advance against a monospace control.
3. **Every image decoded.**
4. **Nothing overflows the frame**, so no text is cropped in the PNG.
5. **The PNG is exactly 3200x1040**, from 1600x520 at deviceScaleFactor 2.

It also picks a port no sibling agent is using, because two parallel
renders on one port is a race whose symptom is a blank capture rather than
an error.

### Then score it, because five assertions are not a review

`render_banner.py` proves the banner rendered. It says nothing about whether
the banner is any good or whether it agrees with its siblings, and for a long
time nothing else did either. An icon commission gets a corpus, three engines,
a 12-point rubric, a contact sheet at six sizes and a fidelity loop. A banner
got the five assertions above and no eyes at all, and three banners shipped
wrong through that gap while passing every check made of them:

- `resume-session` at 1600x520, the layout size at deviceScaleFactor 1, so half
  resolution and soft on every retina display.
- `create-test-suite` and `whats-left` at 3200x840 from a 1600x420 layout.
- `create-test-suite` and `whats-left` again, for a defect no size check could
  ever find: their wordmarks are set in `Iowan Old Style` and `Avenir Next`,
  local macOS faces with nothing linked, so re-rendering either on another
  machine or in CI silently substitutes a different face. The banner still
  renders, still passes, and is a different banner.

So a banner now gets its own sheet and its own 12-point rubric, same shape as
the icon's and with the same 10/12 delivery bar:

```bash
python3 scripts/banner_sheet.py sheet  plugins/<name>/assets   # renders + banner-audit.html
python3 scripts/banner_sheet.py check  plugins/<name>/assets   # exit 0 required
python3 scripts/banner_sheet.py family .                       # every banner, one page
```

Checks 1, 2, 3, 7 and 12 are non-negotiable and mechanical, so `check` decides
them: the exact 3200x1040, the real icon asset referenced rather than redrawn, a
**linked** web font rather than the rendering machine's furniture, no em dash in
the copy, and a retained `banner-src`. The other seven are register, accent,
derivation from the icon's own build constants, overflow, legibility at 900px
and at 400px, and whether anything overlaps illegibly. Those need a person, and
the renders are what they look at. `check` also resolves every image the sheet
displays and refuses a sheet older than the banner it describes, both lessons
borrowed from the icon sheet.

Rendering the display sizes needs no browser: the banner already exists and each
size is a downscale. That is deliberate. A resize cannot fail silently, and the
icon pipeline learned where the silent failures live.

**`family` is the view that matters most and the one nobody had.** Drift across
a set is invisible one banner at a time: each looks considered alone. Stacked at
README width, the set currently shows twelve different display faces across
twenty-seven banners, where this document asks for "a set wordmark". Whether
that is variety or drift is a taste call, but it cannot be made without the page.

Note that a `file://` load of any of these sheets renders with no images, because
the browser here refuses `file://` subresources. That looks exactly like a 404
and is not one. Serve the directory and open it over http, or trust `check`,
which resolves the paths on disk.

Three facts about this environment's browser, measured 2026-08-17, each of
which cost a debugging round:

- **`obscura serve` needs a flattened CDP session.** Connecting to the page
  socket at `/json/list` succeeds and then fails every page, runtime and
  emulation call with `{"code": -32601, "message": "No page for session"}`,
  which reads like a missing method and is a missing session. Connect to
  the **browser** socket from `/json/version`, `Target.createTarget`,
  `Target.attachToTarget` with `flatten: true`, and pass the returned
  `sessionId` on every command. With that, `Emulation.setDeviceMetricsOverride`
  works and the viewport reads back correctly.
- **A `file://` page does not load `file://` subresources.** The `<img>`
  reports `complete: false` and `naturalWidth: 0`, the banner renders with a
  hole where the icon goes, and nothing errors. Inline artwork as a data
  URI, sized to what it actually displays at.
- **`document.fonts.check()` under-reports.** It returned `false` for a font
  the engine was demonstrably rendering with, so the advance measurement is
  the oracle and `check()` is advisory. Web fonts *do* load, given a settle
  window.

media-gen-pro is for imagery a design genuinely needs (icon engines,
scene art); diagrams are mermaid, natively rendered and maintainable —
never raster.

## README and EVALS.md

Both through **create-luke-content** (marketing persona over the base
voice), then `voice_lint.py --format marketing` until hard-checks clean.
The em-dash ban covers alt text, table cells, and the GitHub repo
description. Ground every claim in the built artifacts; numbers come
from the evals, never from enthusiasm.

Structure for a **non-technical reader**:

- README: banner, badges, the problem in plain words, how it works
  (one mermaid if it earns its place), install block, and "does it
  actually work" told as report-card + blind-taste-test **against not
  having the skill at all**, which is the honest baseline for something
  new. Links into the deep material.
- EVALS.md: the deep half — full tables, the with-skill versus no-skill
  numbers, judge families and harnesses, costs, the flip story, and the
  caveats stated rather than buried. Where the baseline matched the
  skill, say so and say what you did about it.

## Root README and shipping

- Add the skill's row to the marketplace root README: icon (128px
  raster), description in the table's established voice, README link.
- **Every row needs its own `<br clear="left" />` before it.** The icon is
  floated left, so a row without one floats up beside the previous entry's
  paragraph and renders as an overlapping mess that reads to a human as
  "my plugin isn't in the README". No script checks this; one row in the
  repo is currently missing it.
- Run `node site/scripts/build-catalogue.mjs` and check the **exit code**.
  It fails on a missing SKILL.md, a missing icon, a missing banner, or a
  version that disagrees between `plugin.json` and the marketplace
  manifest. It cannot see the root-README row or its `<br clear>`, so read
  those yourself.
- Commit at checkpoints (skill built · evals graded · panel judged ·
  brand landed), push when pushing is in scope, update the portfolio
  manifest if the marketplace is tracked in one, and fix the GitHub
  repo description if the roster changed (`gh repo edit`).
