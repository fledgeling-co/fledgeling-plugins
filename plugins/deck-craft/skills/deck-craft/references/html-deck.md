# HTML deck — the self-contained fixed-stage target

One HTML file, no build step, no dependencies. Every slide is authored at a fixed 1920×1080 and the whole stage scales to fit the viewport, letterboxing rather than reflowing. That invariant is what makes a deck a deck: content that reflows for a phone is a web page, and the presenter can no longer predict what the audience sees.

## Phase 0: The one structural decision, and what it costs to get wrong

**The stage is a fixed pixel box scaled by a transform. It is never a fluid box with a `min-height`.** This is the single decision the rest of the file depends on, so it comes before the shell rather than inside it.

```css
/* ✅ a stage: authored at one size, scaled as a unit */
.slide-wrap { width: 100%; max-width: 1600px; aspect-ratio: 16 / 9;
              position: relative; overflow: hidden; }
.stage      { width: 1920px; height: 1080px; position: absolute; top: 0; left: 0;
              transform-origin: top left; }   /* JS sets transform: scale(s) */

/* ❌ a web section wearing a slide's name */
.slide-stage { width: 100%; min-height: 820px; }
```

The wrong version does not fail loudly. It fails as a cascade, and every symptom looks like a separate bug:

- **The box is no longer 16:9.** Measured on a real nine-slide investor deck built this way: every slide rendered 1240×820, aspect 1.51 against the 1.78 it claimed. On a 16:9 projector that is either letterboxed waste or a crop.
- **Type collapses to web density.** With no fixed height to fill, sizes get chosen to fit a browser window: that deck carried **294 text elements below the 24px floor**, median 22px, 43 of them under 18px — unreadable from row four. The type was not a separate mistake; there was nowhere for 32px body copy to go.
- **Overflow stops being computable.** Against a fixed 1080px height, "does it fit" is a boolean. Against `min-height`, the box simply grows, so the question becomes "does it look right in the window I happen to have open" — which is why that deck's own validation pass found and fixed table clipping on slide 3 and shipped the identical defect on slide 8.
- **Voids open at the foot of every slide.** Content stops at its natural height and the rest of the box is empty: 200–330px on seven of nine slides, 30% of the canvas on the worst.

One line settles it, and it belongs in the gate before the second slide is authored:

```js
const r = document.querySelector('.slide-wrap').getBoundingClientRect();
Math.abs(r.width / r.height - 16 / 9) < 0.02;   // must be true
```

`scripts/run-preflight.sh` runs this across every slide along with the rest of the computable gate.

### Phase 0B: Presentation Viewport Centering & Snap Mechanics (Vertical Decks)

When building a vertical single-page presentation deck, an unbuffered container causes the **final slide** (and any slide navigated to via `End` or `scrollIntoView`) to be cut off at the bottom, occluded by fixed floating HUD controls or scrolled past the viewport bounds.

To guarantee that **every slide (including the last slide) is vertically centered and 100% visible on any screen**:
1. **Viewport-Adaptive Slide Wrap**:
   ```css
   .slide-wrap {
     width: min(92vw, calc((100vh - 96px) * 16 / 9), 1920px);
     aspect-ratio: 16 / 9;
     position: relative;
     overflow: hidden;
     background: var(--canvas);
     border-radius: var(--radius-md);
     box-shadow: 0 16px 48px rgba(0, 0, 0, 0.55);
     scroll-snap-align: center;
     scroll-snap-stop: always;
     flex-shrink: 0;
   }
   ```
2. **Centered Container Viewport Padding**:
   ```css
   .deck-container {
     width: 100vw;
     display: flex;
     flex-direction: column;
     align-items: center;
     gap: 32px;
     padding: calc((100vh - min(92vw * 9 / 16, calc(100vh - 96px), 1080px)) / 2) 0;
     scroll-snap-type: y mandatory;
   }
   ```
3. **Block-Center Navigation**:
   ```javascript
   function goTo(i) {
     if (i < 0 || i >= total) return;
     wraps[i].scrollIntoView({ behavior: 'smooth', block: 'center' });
     updateHUD(i);
   }
   ```
This provides equal top and bottom margins on the target **13" MacBook Air standard screen resolution (1470×956 / 1440×900)**, keeping the slide content completely clear of floating HUD bars.

## Phase 1: Build the shell once

Don't hand-roll scaling per slide. The shell holds every slide, scales the stage, handles keyboard/tap nav, shows a counter, and persists position to `localStorage` so a reload doesn't lose the presenter's place.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>NAME-THIS-FROM-THE-CONTENT</title>
  <style>
    :root { --slide-w: 1920px; --slide-h: 1080px; }
    * { box-sizing: border-box; }
    html, body { margin: 0; height: 100%; background: #111; overflow: hidden; }
    #stage {
      position: absolute; top: 50%; left: 50%;
      width: var(--slide-w); height: var(--slide-h);
      transform-origin: center center;   /* JS sets transform: translate(-50%,-50%) scale(s) */
    }
    .slide {
      position: absolute; inset: 0; display: none;
      width: var(--slide-w); height: var(--slide-h);
      background: #FAFAFA; color: #1A1A1A;
    }
    .slide[data-active] { display: block; }
    #counter {
      position: fixed; bottom: 16px; right: 20px; z-index: 10;
      font: 500 14px/1 system-ui, sans-serif; color: #fff; opacity: .6;
    }
    @media print {
      html, body { overflow: visible; background: #fff; }
      /* `relative`, never `static`. #stage is the containing block for every
         absolutely-positioned descendant — the slides themselves, and any
         inset:0 image, scrim or pinned footer inside them. Making it static
         re-anchors all of them to the page box, and the whole deck composites
         onto page 1. Drop the centring, keep the positioning. */
      #stage { position: relative; top: auto; left: auto;
               transform: none !important; width: auto; height: auto; }
      .slide { position: relative; inset: auto; display: block !important;
               width: var(--slide-w); height: var(--slide-h);
               page-break-after: always; overflow: hidden; }
      #counter { display: none; }
    }
    @page { size: 1920px 1080px; margin: 0; }
  </style>
</head>
<body>
  <div id="stage">
    <section class="slide" data-screen-label="01 Title" data-active><!-- … --></section>
    <section class="slide" data-screen-label="02 Agenda"><!-- … --></section>
  </div>
  <div id="counter"></div>
  <script>
    const stage = document.getElementById('stage');
    const slides = [...stage.querySelectorAll('.slide')];
    const counter = document.getElementById('counter');
    const KEY = 'deck.slide';
    let i = Math.min(+(localStorage.getItem(KEY) || 0), slides.length - 1);

    function fit() {
      const s = Math.min(innerWidth / 1920, innerHeight / 1080);
      stage.style.transform = `translate(-50%, -50%) scale(${s})`;
    }
    function show(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach((sl, k) => sl.toggleAttribute('data-active', k === i));
      counter.textContent = `${i + 1} / ${slides.length}`;
      localStorage.setItem(KEY, i);
    }
    addEventListener('resize', fit);
    addEventListener('keydown', (e) => {
      if (['ArrowRight', 'PageDown', ' '].includes(e.key)) show(i + 1);
      if (['ArrowLeft', 'PageUp'].includes(e.key)) show(i - 1);
    });
    addEventListener('click', (e) => show(i + (e.clientX > innerWidth / 2 ? 1 : -1)));
    fit(); show(i);
  </script>
</body>
</html>
```

**The filename and the `<title>` are what the deck is CALLED, and they are content rather than tool.** Name both the way the user would name the deck — `alfabs-q4-fy26-investor-update.html`, `Alfabs Q4 FY26 Investor Update` — never after the format, the tool, or a placeholder. An HTML deck is emailed, dropped in a Slack channel and attached to a board paper: the filename is what a director sees in their downloads folder, and `deck.html` beside four other files called `deck.html` is a real failure rather than an untidy one.

This template shipped `<title>Deck</title>` until 18 Aug 2026, which is precisely the string the gate now refuses, so every deck built from it inherited the defect and nothing said so. The placeholder above is deliberately one that cannot survive review. `run-preflight.sh` reports `genericName` as a blocker against `deck`, `presentation`, `slides`, `untitled`, `new deck` and the matching filenames.


Each slide is a direct child `<section class="slide">` of `#stage`, carrying a 1-indexed `data-screen-label` so the user can say "fix slide 04" and you both mean the same slide.

Adapt freely — transitions, a progress bar, an ESC overview grid, wheel and swipe navigation. Keep the invariant: authored at fixed size, stage scales to fit, never re-layout for a narrow viewport.

### The defensive base, added once

Most of what a deck review finds is preventable in the stylesheet rather than repairable per slide. Each rule below exists because its absence has shipped:

```css
/* Metrics, status pills and any figure compared column to column never wrap
   and never shift width digit to digit. Without this, "12 Mo" breaks across
   two lines inside a stat and "ON TRACK" stacks inside its badge — the
   commonest cosmetic defect in generated decks, and the one that reads
   loudest at distance. */
.stat, .stat-number, .metric, .status-pill, .badge, .chip, td.num, .mono-cell {
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
  font-feature-settings: "tnum";
}

/* Keep the nowrap list to things that are genuinely atomic. `.stat` is the
   TILE, not its number: putting the tile in this list makes white-space:nowrap
   cascade to its label and note, so a long note cannot wrap, the tile's
   min-content blows past its grid track, and the last tile in a four-up row is
   clipped at the slide edge. Measured — it cost one rebuild. List `.stat-num`,
   never `.stat`. The same trap applies to any wrapper whose child is the atom. */

/* Reserve the foot of every slide. This space is structural: it is what keeps
   the last line of body copy off the footer rule and out from under any
   floating control dock — and it is a QUANTITY, not a guess. The reserve must
   exceed the foot's RENDERED height including any wrap, and a foot string that
   fits the full width can wrap to two lines inside a column narrowed by an
   editorial photo, which silently eats it. Measured: one 22px shortfall here
   put content into the footer on three separate slides, and it read as three
   separate bugs. Set it generously, and keep foot strings to one line at the
   NARROWEST column the deck uses. */
.slide > .pad { padding-bottom: var(--pad-bottom, 80px); }

/* Two rules that keep that reserve honest, both learned the same way:
   1. The reserve must exceed the foot's RENDERED height. A foot at
      `bottom: 46px` with 18px padding, a 1px rule and one 21px line is 97px
      tall from the slide's base — so 116px reserved left 19px, and a foot
      string that wrapped to two lines on the narrowest column ate it and put
      body copy through the rule on five slides at once.
   2. So keep every foot string to ONE line at the deck's narrowest column.
      An editorial split's copy column is ~810px, not 1712px; write the foot
      to fit there and the wide slides get the margin for free. */

/* A rowspan cell draws its own bottom border below the LAST row it spans, so
   a grouped table ends with a stray hairline under one column only. It reads
   as a rendering fault and is one declaration. */
.data-table td[rowspan] { border-bottom: none; }

/* A table given less width than its columns need clips silently at the
   container edge — no scrollbar, no warning, just a truncated last column.
   Give data tables a floor and let the layout fail visibly instead. */
.data-table { width: 100%; table-layout: fixed; }
.data-table td, .data-table th { overflow-wrap: anywhere; }
.grid-with-table { grid-template-columns: minmax(560px, 1.3fr) 1fr; }

/* Copy over a full-bleed photograph needs its own positioning to win the
   paint order, and the photograph needs a scrim before white type sits on it.
   Both, or the text is invisible while its layout is perfect. */
.slide > .copy { position: relative; }
.scrim { position: absolute; inset: 0;
         background: linear-gradient(90deg, rgba(16,15,15,.92), rgba(20,18,18,.55)); }

/* A bullet list laid out as a CSS grid: `li:first-child { margin-top: 0 }`
   zeroes only the DOM-first item, so the second column's first row keeps its
   margin and sits a gap lower than the first column's. Use row-gap for the
   rhythm and zero every item's margin in grid mode. */
.chevlist.chevgrid li { margin-top: 0; }        /* pair with `gap: 22px 72px` */

/* Give a text leaf a block box wherever a gate has to measure it: an inline
   <span> that is the only child of a plain block can return a zero-size rect
   in some engines, which every probe reads as "invisible". */
.card-num { display: block; margin: 0; }

/* Terminate every font stack with a generic: a bare family that fails to load
   falls back to serif and the deck silently changes character. */
:root {
  --font-display: Figtree, system-ui, sans-serif;
  --font-mono: 'IBM Plex Mono', ui-monospace, Menlo, monospace;
}

/* Universal accessible focus outline */
:focus-visible {
  outline: 2px solid var(--color-primary, #D72229);
  outline-offset: 3px;
}

/* Guard against sticky header occlusion when navigating to slide anchors */
.slide-section, .slide, .slide-wrap {
  scroll-margin-top: var(--header-height, 60px);
}

/* Dual-theme contrast tokens on dark bands (#2E2B2B / #181717) */
.slide-dark {
  --color-primary-on-dark: #FF5A5F;
  --color-success-on-dark: #4ADE80;
  --color-info-on-dark: #60A5FA;
}
.slide-dark .badge-primary { background: rgba(215, 34, 41, 0.25); color: var(--color-primary-on-dark); }
.slide-dark .badge-success { background: rgba(74, 222, 128, 0.15); color: var(--color-success-on-dark); }
.slide-dark .badge-info    { background: rgba(96, 165, 250, 0.15); color: var(--color-info-on-dark); }

/* Badges over photo scrim overlays must be solid primary with crisp white text */
.scrim-overlay .stat-badge, .media-frame .scrim .stat-badge {
  background: var(--color-primary, #D72229) !important;
  color: #FFFFFF !important;
  font-weight: 700;
  letter-spacing: 0.08em;
}

/* Reduced motion accessibility */
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  *, *::before, *::after {
    transition: none !important;
    animation: none !important;
  }
}
```

The nowrap and tabular-numbers rule is the highest-yield line in the block. A real validation pass spent 24 minutes finding, by eye and one slide at a time, three defects this single rule prevents outright.

**Centre the stage with `left/top: 50%` and a translate, not with flex or grid centring.** The shell above does this for a reason. `place-items: center` on a container narrower than the 1920px stage does **not** centre it: CSS flex and grid *start-align* an item larger than its area rather than letting it overflow both sides. The layout box lands at `left: 0` instead of `-120px`, and a `scale()` about the element's own centre then pushes the whole deck sideways by half the overflow — a dead band down one edge and the opposite edge of every slide cut off. It looks like a margin bug and it is a centring bug. If you must use grid, place the stage with explicit half-size margins instead:

```css
.stage { position: absolute; left: 50%; top: 50%;
         margin-left: -960px; margin-top: -540px;   /* half of 1920 × 1080 */
         transform: scale(var(--s)); transform-origin: center center; }
```

### The Floating Minimalist Chrome Standard (Never Sticky Website Navbars)

A slide deck is an unencumbered fullscreen presentation, **not a multi-page web application**. 
- **Never add a sticky top header or website navbar** (e.g. `<header id="top-nav-bar">` with logo, company name, and ticker). A top navbar steals vertical space, compromises the 16:9 stage aspect, and transforms a presentation deck into a generic portal.
- **Implement the standard floating trinity**:
  1. **Top Scroll Progress Line (`#progress-bar`)**: Fixed 4px hairline across the top of the viewport (`height: 4px; background: var(--primary); transition: width 80ms ease-out;`).
  2. **Right-Hand Floating Dot Rail (`#side-nav`)**: Vertical glassmorphic pill (`background: rgba(24, 23, 23, 0.85); backdrop-filter: blur(12px); border-radius: 9999px;`) with interactive dot indicators and hover tooltips showing slide titles (`01 Cover`, `02 Highlights`, ...).
  3. **Bottom Floating Controller (`#controls`)**: Glassmorphic pill containing previous/next arrow buttons, slide counter (`01 / 12`), and a dedicated PDF print button (`window.print()`).
  4. **Keyboard Navigation Support**: Always bind `ArrowDown`/`PageDown`/`j`/`J` (next), `ArrowUp`/`PageUp`/`k`/`K` (prev), `Home` (slide 1), and `End` (last slide).

**If the deck has persistent chrome — a control bar, a progress rail — give it its own band rather than floating it over the stage.** Reserve the space in the scaling container (`inset: 0 0 104px 0`) and compute `s` against *that* box, not the viewport. Chrome floated at `bottom: 28px` sits on slide content at every 16:9-ish window, where the letterbox is only a few dozen pixels.

**Size the reserve by arithmetic, then measure it.** The reserve is a quantity, not a round number that felt safe. On a vertically-centred deck the slide's margin is half the reserve, so the controller clears the stage only when

```
reserve / 2  >  controllerBottomOffset + controllerHeight   (+ ~20px of visible gap)
```

Worked on a real deck: controller at `bottom: 20px`, measured height 56px, so it occupies the lower 76px. A 156px reserve gives 78px of margin and **2px** of clearance — arithmetically a pass and visually touching. 200px gives 100px of margin and 24px of clearance, which is what shipped. Getting this wrong is not subtle at review time and is invisible at build time: a second deck from the same brief floated its controller with no reserve at all and it sat over the stage on all twelve slides, while a text-versus-dock check scored zero because the footer line happened to stop 17px short of it. Measure the box, not the last line of text:

```js
const w = document.querySelector('.slide-wrap').getBoundingClientRect();
const c = document.getElementById('controls').getBoundingClientRect();
({ gapToControls: Math.round(c.top - w.bottom),      // must be > 0, want ≥ 20
   marginTop: Math.round(w.top),
   marginBottom: Math.round(innerHeight - w.bottom) });  // these two must match
```

**Auto-hiding controls hold open on `:focus-visible`, not `document.activeElement`.** A mouse click leaves focus on the button it clicked, so an `activeElement` check re-arms the timer forever and the chrome never retires again for the rest of the session. `controls.querySelector(':focus-visible')` matches keyboard focus only, which is the case that actually needs the hold. Hidden chrome must also stay keyboard-reachable: wake it on `keydown` so the first Tab brings it back before focus resolves.

**Slide visibility must not use `display`.** `.slide { display: none }` looks fine until a later layout rule sets `.slide-content { display: flex }` and every slide renders at once. Toggle with an attribute or class that controls `visibility` + `opacity` + `pointer-events`, or keep `display` toggling but assert nothing downstream overrides it. If `~/Dev/frontend-slides/viewport-base.css` is available, read it and inline its contents — it encodes this and the rest of the stage behaviour.

## Phase 2: Commit the type scale before the first slide

Define the scale as custom properties in the base `<style>`. This is what stops you defaulting to web density, and it means one number resizes the whole deck later.

```css
:root { --type-title: 64px; --type-subtitle: 44px; --type-body: 34px; --type-small: 28px;
        --pad-top: 100px; --pad-bottom: 80px; --pad-x: 100px; --gap-title: 52px; --gap-item: 28px; }
```

Every `font-size` uses a `--type-*`; every padding and gap uses `--pad-*`/`--gap-*`. The explicit `--pad-bottom` reserves breathing room at the base of every slide — that space is structural, not empty. If the values don't feel generous, they aren't.

## Phase 3: Write slides as literal static HTML

Never React, never a JS array rendered into the DOM. Static markup is directly editable: the user or a later agent can retype a heading in place, where content generated from an array forces every tweak to round-trip through you.

Two details keep it editable. Each piece of text lives in its own leaf element — put "Revenue" in its own `<span>` inside the `<h2>` rather than mixing text and a child span in one parent. And repeated structure is written out: three bullet `<li>`s in the markup, not one looped from an array. The repetition is the point — it lets bullet two be edited without touching bullet one.

Reach for script only when a slide needs behaviour static markup can't express: a live chart, real state.

Build one slide at a time, in order, and show the user the file after 1–2 slides rather than perfecting fifteen in private.

## Phase 4: The wrapper-collapse failure mode

The shell sizes only the `<section>`. A wrapper `<div>` inside it is an ordinary block at `height: auto`, so:

- if its children are all `position: absolute` (a full-bleed `inset: 0` image, a scrim), it collapses to zero height and the image vanishes;
- if they're in flow, it stops at content height, so a full-bleed background covers only the top band with blank space below.

Add once to the base styles:

```css
.slide > *:not(img):not(picture):not(video):not(svg):not(canvas):not(.pinned) {
  height: 100%; box-sizing: border-box;
}
```

Keep one in-flow wrapper per slide. **Any other top-level element must be `position: absolute` *and* excluded from that selector** — give it a `.pinned` class and extend the `:not()` chain. Positioning it absolutely is not enough on its own: the rule still applies `height: 100%`, so a footer pinned with `bottom: 44px` becomes a 1080px-tall box growing *upward*, and its flex content renders at the top of the slide instead. The tell is a sliver of footer text along the slide's top edge and nothing at the bottom — and because the element is present and styled, every overflow and collision check passes.

**A percentage height resolves against a parent sized by `top`/`bottom` less reliably than against one sized by `inset`.** The editorial media column is where this bites: `.media { position: absolute; top: 0; bottom: 0; width: 700px }` with `.media img { width: 100%; height: 100% }` renders the photograph at its *natural* height in some engines, so a 3:4 image in a 700px column stops at 933px of a 1080px slide and leaves a band of blank canvas beneath it. The tell is that the full-bleed cover photo on the same deck is correct — because that one is pinned with `inset: 0`. Pin the image the same way and the class disappears:

```css
.media     { position: absolute; top: 0; bottom: 0; height: 100%; overflow: hidden; }
.media img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
```

**Never negate a CSS function directly.** `-clamp(...)`, `-min(...)`, `-max(...)` are silently ignored — the declaration does nothing and the layout is subtly wrong with no error. Use `calc(-1 * clamp(...))`.

## Phase 5: Imagery

**Decide the medium before the treatment.** The medium is set by what the region *shows*, never by what feels buildable in a `<style>` block:

- A photograph, a site, a product in use, a human figure, machinery — **raster**, whatever the stack.
- A texture named as one — paper grain, woven cloth, concrete, brushed metal, ore — **raster**. It needs no depth argument to qualify, and "layered CSS gradients" is not a texture medium.
- Rules, hairlines, drawn marks, flat shape systems, diagrams with countable elements, and the accent devices in `layout-specs.md` — **authored SVG or CSS**. That is where code belongs, and choosing it there is craft rather than economy.
- Anything with shading, perspective or figure drawing is *illustration* however line-drawn it looks, and no build session authors illustration by hand.

Writing a gradient where the direction committed to a photograph is not a treatment choice; it is the quiet deletion of the design, and it is how a cover promising a mine site ships as a blue wash. **A field or texture also carries a quantity commitment** — write down its rough density and coverage before building ("dense stipple over the top third, fading out by the title") because a field rebuilt at a tenth of its density passes every check and still isn't the design.

Then choose the treatment. View every image before placing it. Full-bleed photographs may aspect-fill; screenshots and diagrams must aspect-fit and are rarely overlaid; transparent or aspect-fit images sit on a contrasting ground. Text over an image needs protection — a card, a gradient, a blur — matched to how the brand does it elsewhere rather than invented per slide.

**Content over a full-bleed image needs its own positioning to win the paint order.** A `position: absolute; inset: 0` photograph and its scrim paint *above* every static in-flow sibling, whatever the source order — so the slide's copy wrapper needs `position: relative` (a `z-index` is not required, and adding one invites a stacking-context fight later). Miss it and the entire text of the slide is invisible while its layout is perfect: real boxes, real sizes, correct fonts, so overflow, collision, contrast and inventory checks all pass. The confirmation is one line, and it belongs in the per-slide gate for every slide carrying an image:

```js
const r = heading.getBoundingClientRect();
document.elementFromPoint(r.left + 10, r.top + 10);   // must be the text, not the photo
```

**Check the composite, not the asset.** A texture buried under a near-opaque colour wash ships the wash, and an image at low opacity behind other paint is a compliance token rather than a material. Judge every asset in the rendered capture beside what it was meant to be.

### Fonts travel with the file too

A generic fallback stops a missing family from breaking the page; it does not stop the deck arriving in a different typeface. A deck that must open offline, over `file://`, or inside a sandboxed portal carries its own fonts as base64 `woff2`, which costs far less than it sounds: a variable Figtree plus two IBM Plex Mono weights is ~40KB for the latin subsets.

```bash
# Ask Google Fonts for CSS2 with a browser UA, then take the /* latin */ blocks only —
# the response also carries cyrillic, greek and vietnamese subsets you do not need.
curl -s -A "$UA" "https://fonts.googleapis.com/css2?family=Figtree:wght@400..900&display=swap"
```

Parse out each `/* latin */` block's `url(...)`, fetch the `woff2`, base64 it into an `@font-face` `src`, and keep the generic at the end of the stack anyway. One variable font file covers every weight you author.

### The Asset Optimization & Inlining Pipeline (Single-File Portability)

When generating high-resolution photography or renders (e.g. via `media-gen-pro`) for standalone HTML presentations:
1. **Downsample raw multi-megabyte assets to 1600px width at 80–85% JPEG quality**:
   ```bash
   sips -s format jpeg -s formatOptions 82 -Z 1600 raw_asset.webp --out asset_1600.jpg
   ```
2. **Embed assets directly as Base64 Data URIs** inside the HTML file:
   ```python
   import base64

   def get_b64(path):
       with open(path, 'rb') as f:
           return 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')
   ```
   ```html
   <img src="data:image/jpeg;base64,/9j/4AAQSkZJRg..." alt="Documentary description" />
   ```
3. **Why this is mandatory**: Standalone HTML presentations must open flawlessly over `file://`, in headless browser tests, and across sandbox environments without broken relative path dependencies or CDN network latency.

**Author against the placeholder even when the real images are coming.** The
imagery is commissioned early and generated in parallel (`SKILL.md` §4b), so for
most of the build it has not landed yet. That is not a reason to leave the slide
half-built: a placeholder with the asset's exact box gives the layout its real
geometry, so overflow, chrome reserve and ink extent all measure correctly, and
the final swap is one `src` edit that moves nothing. Building the slide around a
gap and fitting the picture afterwards inverts that and re-opens every
measurement.

With no real assets, use honest placeholders and say so: a striped background with a monospace label naming the asset and its dimensions. A placeholder shows intent; a hand-drawn SVG of a person or an abstract concept shows you didn't have the asset, and a gradient standing in for a photograph shows it while pretending otherwise.

## Phase 6: Speaker notes (only when asked)

Off by default. When requested, put each note as plain text in a `data-speaker-notes` attribute on its own `<section>`, so it travels with the slide through reorder, duplicate and delete. Never a positional JSON array in the head — one reorder silently misaligns every note after it.

Render the current note in a presenter overlay behind a key toggle. Write full conversational scripts, what the presenter actually says, not bullet outlines. And once the script carries the narrative, strip text off the slides: lean on large figures, quotes, full-bleed images, one-line headlines. A slide that is mostly text has put the script on the slide instead of in the notes.

## Phase 7: Print and PDF

The `@media print` block in the shell is the floor: it un-scales the stage, forces every slide visible, and page-breaks between them. Verify by actually printing to PDF, because several things break silently:

- a background colour that doesn't print (`print-color-adjust: exact` on the elements that need it);
- an animation frozen mid-play because the slide was authored in a hidden state — authoring each slide in its final visible layout (SKILL.md §5) is what makes print free;
- **the containing-block collapse**: switching the stage or a slide to `position: static` for print re-anchors every absolutely-positioned descendant to the page box. Full-bleed photographs, scrims and pinned footers from *all* slides then pile onto page 1, while pages 2+ look correct. Use `position: relative` and reset `top`/`left`/`margin` instead. Page 1 rendering the *last* slide's photograph under the *last* slide's footer is this bug's signature.

**Open the exported pages, and not just the first one.** The page count is not the check — a 12-page PDF whose page 1 is a composite of twelve slides still counts twelve pages. Open page 1, one photo-bearing slide from the middle, and the last, and confirm each carries the right content, the right image and the right page number.

If a headless export is available (`~/Dev/frontend-slides/scripts/export-pdf.sh` is one), use it rather than asking the user to print by hand. Obscura's own PDF output is raster-backed — no selectable text, no outlines, no headers/footers and incomplete paged-media CSS — so it can show you that a slide composited wrongly but never that the print typography is right.

## Phase 8: Verify

Serve over HTTP, never `file://` — module scripts, fetches and some fonts fail silently from the filesystem.

**Run `scripts/run-preflight.sh <url>` first.** It measures, in one call, what would otherwise be nine slides × three tool round-trips of looking: stage geometry against 16:9, the type floor, overflow, collision with chrome, text laid over text, copy invisible under its own photograph, chart axis honesty, the accent budget, dead bands at a slide's foot, and — with `--regulated` — whether the deck states its disclosures at all. Fix what it names, then spend the looking on what it cannot see. A validation pass that inspected a nine-slide deck screenshot-by-screenshot took 24 minutes and still missed both of that deck's truncated-axis charts; the script finds them in seconds and returns the implied baseline.

Read its output the way it is written: a non-empty `notes` entry saying a check *failed* means that check did **not run**, which is not the same as clean. An empty result is not a pass either — the runner exits non-zero and says so.

**Measure a scaled stage in one unit system.** `getBoundingClientRect()` returns rendered pixels; `getComputedStyle()` returns the authored value. Comparing a child's rendered edge against its parent's computed padding subtracts one system from the other, and what it reports is not a defect. Measured at `s = 0.667`: an audit reported copy overflowing its container by exactly 52px on every slide, cards by 16px, stat tiles by 12px — which are `104 × (1−s)/s`, `32 × (1−s)/s` and `24 × (1−s)/s`, each container's own padding converted by the scale. Nothing was clipped. The signature is an overflow that is **constant per container class and identical on every instance**, where a real one varies with content. Convert first:

```js
const s = stage.getBoundingClientRect().width / 1920;
const cs = getComputedStyle(parent);
const inset = (parseFloat(cs.paddingRight) + parseFloat(cs.borderRightWidth)) * s;
const overflowAuthored =
  (el.getBoundingClientRect().right - (parent.getBoundingClientRect().right - inset)) / s;
```

`deck-preflight.js` already normalises sizes to the authored canvas; any probe you write beside it needs the same conversion.

**On a vertical scroll deck, isolate the slide you want to capture.** A URL fragment does not reliably scroll the page before the capture fires, so `deck.html#s07` returns the same image as `deck.html`. Write a copy of the file per slide with one injected rule and capture that — the slide then sits at the top of the document, filling the viewport at exactly 16:9, with the real floating chrome over it:

```js
src.replace('</head>', `<style>.slide-wrap:not(#s07){display:none!important}</style></head>`)
```

Give every `.slide-wrap` a stable `id` for this, and the deck gains portal deep-links for free.

**Capture the viewport, not the element.** An element screenshot (a `Page.captureScreenshot` with a `clip` taken from the stage's own `getBoundingClientRect()`) renders the element's own box and is structurally blind to where that box actually sits: a stage shifted 120px off-centre, half of it past the right edge of the window, screenshots as a perfect slide. So does a stage sitting under a floating control bar. Element captures are for cropping a component you have already located; they can never establish that the deck fits its window.

**A ratio check is not a placement check either.** `getBoundingClientRect().width / .height === 1.778` stays true when the box is the right size in the wrong place. Measure the edges against the viewport:

```js
const r = stage.getBoundingClientRect();
({ clipL: Math.max(0, -r.left),
   clipR: Math.max(0, r.right  - innerWidth),
   clipT: Math.max(0, -r.top),
   clipB: Math.max(0, r.bottom - innerHeight) });   // every one must be 0
```

Run it at several window sizes, including a few that are wider and narrower than 16:9. Then walk the deck per `references/deck-review.md`.
