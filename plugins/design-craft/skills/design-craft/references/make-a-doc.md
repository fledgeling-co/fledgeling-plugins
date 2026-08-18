# Make a Doc: Page-Style Documents That Print Perfectly

Build a document (resume, one-pager, memo, letter, report, proposal) as an HTML page that reads as paper on screen AND prints cleanly with zero tweaking. Use this when the deliverable is a *document* — something the user will print, save as PDF, or hand to someone — rather than a screen UI.

**A document has two renderings — screen and print — and both ship.** Most web-styled documents fall apart in the print dialog: backgrounds vanish, sections split mid-heading, animations freeze half-played. Design for both from the first line.

**Length is part of the design.** A document runs as long as its substance needs and stops there — the page count is an outcome, not a target to fill. Cut restated summaries, "Overview" sections that repeat the opening paragraph, and boilerplate headings carrying one sentence each; a two-page memo that says the thing beats a six-page memo that circles it. If the brief names a length or a page count, that is a constraint to design to, and content gets cut to fit rather than type shrunk to hide the overflow.

## Phase 1: Screen presentation — paper on a desk

- **Page container:** `max-width: 816px` (US Letter at 96dpi), centered (`margin: auto`), white background, 64–72px padding, subtle shadow (`0 2px 12px rgba(0,0,0,0.08)`), 2–4px border-radius. The size matters: 816px means what the user sees on screen is what lands on the printed page, so no layout surprises at print time.
- **Desk background:** the page sits on a muted neutral body background (e.g. `#F0EEE6`) so it reads as paper on a desk, not a web page.
- **Multi-page documents:** one `.page` container per page, with a visible gap between them — the user sees the page breaks before printing, instead of discovering them in the print preview.
- **Document typography, not web typography:** 14–16px body with a clear hierarchy, real inner margins, never edge-to-edge text. Restrained palette — documents are mostly ink on paper; color is for meaning (tags, accents), not decoration.

## Phase 2: Print CSS — the browser's Print must produce a clean document

Add `@media print` from the start, not as a retrofit:

- **Strip the desk:** remove the body background, the page shadow/border/radius, and any on-screen chrome (toolbars, buttons, tweak panels). The page container becomes `width: auto; margin: 0; padding: 0`.
- **Margins via `@page`:** set `@page { margin: 0.75in; }` and rely on it for outer margins — CSS padding inside the page would double up with printer margins.
- **Break control:** `break-inside: avoid` on sections, heading+first-paragraph groups, list items, and table rows, so nothing splits awkwardly; `break-after: page` between `.page` containers so each declared page is a real printed page.

```css
@media print {
  body { background: none; }
  .page { width: auto; margin: 0; padding: 0;
          box-shadow: none; border-radius: 0; break-after: page; }
  .toolbar, .tweaks { display: none; }
  section, li, tr { break-inside: avoid; }
}
@page { margin: 0.75in; }
```

- **Backgrounds:** `print-color-adjust: exact` **only** on elements whose background carries meaning (a resume's skill tags, a status chip); let purely decorative backgrounds drop — browsers strip them by default, and forcing them everywhere wastes ink and muddies the print.
- **Links print legibly** in body ink — never rely on hover styling to make a link findable on paper.

## Phase 3: Make print safety structural, not a patch

The failure this phase prevents: the PDF exports with blank rows where the animated content should be.

### When you own the CSS: invert the states (always prefer this)

> **The resting style IS the final style. The "from" state lives only inside `@keyframes`.**

```css
/* right — at rest the row is visible; the keyframes only say where it came from */
.row { opacity: 1; transform: none }
@keyframes fadeUp { from { opacity: 0; transform: translateY(8px) } }
.section.seen .row { animation: fadeUp 650ms var(--ease-out) both }

/* wrong — at rest the row is invisible. Kill the animation and the row is GONE. */
.row { opacity: 0 }
@keyframes fadeUp { to { opacity: 1 } }
```

Written this way, `animation: none` yields the settled design. Print, `prefers-reduced-motion`, and a JS-disabled fallback are then all correct **by construction**, and the neutraliser is one honest rule:

```css
@media print, (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important }
}
```

This also removes the whole class of "reveal-safety" bugs that `motion-design.md` Phase 8 flags on sight (content visibility gated on a class-triggered transition ships blank sections). The same inversion fixes both.

### When you don't own the CSS: skip to the last frame

For inherited stylesheets, third-party widgets, or a deck you're exporting rather than authoring, you cannot invert the states. Jump every animation to its finished frame instead:

```css
@media print {
  *, *::before, *::after {
    animation-delay: -99s !important; animation-duration: .001s !important;
    animation-iteration-count: 1 !important; animation-fill-mode: both !important;
    animation-play-state: running !important; transition-duration: 0s !important;
  }
}
```

The negative delay skips to the end; `fill-mode: both` holds the final keyframe. Treat it as the fallback it is: it depends on every keyframe's `100%` being the intended resting state, which is exactly the assumption you cannot check in code you didn't write.

### Verify it rather than assuming it — and know what this engine cannot verify

**On the sanctioned engine, print and reduced-motion emulation do not work.** `Emulation.setEmulatedMedia` is accepted and inert (measured 13 Aug 2026), so `matchMedia('print')` stays false and a "print pass" run through Obscura returns the screen rendering with a clean result. That is the exact collision `visual-verification.md` Phase 0 rule 4 exists to prevent, so:

- **The structural fix above is the verification.** Written with the resting style as the final style, `animation: none` yields the settled design *by construction* — there is nothing to emulate. Prefer the invert over any check.
- **Grep instead of emulate**, which works on any engine: list every rule that sets `opacity` under 0.05, `visibility: hidden`, a near-zero `scale`, or a fully-dashed SVG stroke as a **resting** state, and check each one is inside `@keyframes` rather than on the selector. `scripts/design-lint.py`'s `reveal-blank` check does exactly this and fails at major. Each hit is content that will be missing from the PDF.
- **Check for transient overlay labels** ("Checking…", "Loading…") that are visible at rest, because they will print.
- **Say "not checked"** for the emulated passes in your report rather than reporting them clean.

Either way, be clear with the user: **animations do not play in a PDF** — the export shows each section's finished state.

## Phase 3.5: The physical checks — this is paper, not a screen

Print has constraints a screen does not, and none of them are visible in the browser preview. Run these before calling a document done:

- **Grayscale.** Render or print the document in mono and look at it. A palette that separates by hue collapses: two status chips that read as "approved" and "blocked" in colour become two identical grey chips, and a chart's series become indistinguishable. Every distinction that carries meaning needs a second signal — a label, a pattern, a position, a weight.
- **Hairlines.** A `0.5px` rule at low opacity — which `typesetting.md` recommends on screen — can drop out entirely on paper or land as a broken dotted line. **Minimum printed rule weight is 0.25pt at full ink, and 0.5pt is the safe floor**; a decorative hairline that must survive printing gets 0.5pt and ≥60% ink.
- **Ink flood.** A large dark fill drinks ink, shows every roller mark, and cockles cheap paper. Reserve dark grounds for small areas; on a full page, invert the relationship and let the paper be the ground.
- **Rich black, when it is going to a press.** `#000000` prints as flat single-channel black in a CMYK workflow and looks washed against photographic black. Note it for the user rather than solving it in CSS — this is a prepress decision, not a stylesheet one.
- **Bleed, trim and safe margin, for anything that will be cut.** A design that runs to the page edge needs 3mm of bleed beyond the trim line and nothing important within 5mm inside it. The browser has no bleed concept, so state the requirement in the handover and keep the safe margin honest in the layout.
- **Fold order is panel order, and this is where folded pieces go wrong.** On a trifold's **outside** face the front cover is the **rightmost** panel (inside flap, back cover, front cover, left to right); the inside face reads as one continuous three-panel spread. Lay the panels out in fold order, not reading order, and label each one in the source so nobody re-sorts them.

## Phase 4: The `-print.html` variant (when the source isn't already a doc)

When exporting an existing design (a deck, a scrolling page) rather than authoring a document from scratch, write a print-ready copy: the source path with `-print` inserted before the extension — **same directory, same basename**. `slides/deck.html` → `slides/deck-print.html`.

- **Never change directory depth** and never write to the project root when the source is in a subdirectory: any change in depth breaks every relative URL (`@font-face src: url(...)`, `<img src>`, `<link href>`, CSS `background: url(...)`) and the print render shows missing images and system-font fallbacks.
- In the print copy: convert scroll-based or interactive layouts to static paged layouts; remove hover states and `overflow: hidden` clipping; apply the Phase 2 print CSS and Phase 3 animation freeze; drop JavaScript interactivity that makes no sense on paper; preserve all visual content.
- The `-print.html` is plumbing, not a deliverable — tell the user which file to print, but the styled original remains the artifact.

## Phase 5: PDF export (when the user wants a file, not a dialog)

If the user wants an actual `.pdf` (to attach, email, or upload), render it through **Obscura** — the only sanctioned browser on this machine. Playwright, Puppeteer, `chrome-headless-shell` and the Chrome MCP are removed; do not reach for them and do not tell the user to install one.

Two routes, in order of preference:

```bash
# 1. The MCP server's own paginated print path, which honours print media
obscura mcp        # then: browser_navigate <url> ; browser_pdf { print_background: true,
                   #        paper_width: 8.5, paper_height: 11, margin_top: 0.75, ... }

# 2. Or drive Page.printToPDF over CDP against a served page
obscura serve --port 9222 &
# then send Page.printToPDF with printBackground:true, paperWidth:8.5, paperHeight:11
```

Serve the document over HTTP first (`python3 -m http.server`) and pass the served URL — `file://` breaks relative `@font-face` and image URLs, and the PDF then bakes in fallback fonts and missing images permanently. **Web fonts do not load in this engine at all**, so a PDF exported here carries the fallback face: that is a limitation to state in the handover, not a defect to hunt. When the user needs the real typeface in the PDF, the honest answer is the browser's own Print dialog on their machine.

Wait for the page to settle before printing (network idle plus a short delay for any JS that lays out content).

## Phase 6: Verify the export

Open the resulting PDF (Read tool) and check page by page: no content split mid-section; no blank pages from stray `break-after`; meaningful backgrounds present, decorative ones dropped; images loaded; page count matches the `.page` count. Fonts will be the fallback face on this engine — check the *layout* survived the substitution rather than checking the face. If anything is off, fix the print CSS in the source and re-export — never hand-edit the PDF.

## Summarize

Report: the screen file, the print file (if separate), the PDF (if exported); the page count; anything that was frozen or removed for print; the physical checks you ran (grayscale, hairline weights, fold order where it applies); and anything you could not verify — including the emulated print and reduced-motion passes, which this engine cannot perform.
