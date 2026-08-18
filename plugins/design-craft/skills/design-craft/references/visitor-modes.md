# Visitor Modes: What Success Looks Like on This Surface

Before choosing a direction, name what the visitor is here to do. The mode governs what outranks what — the same craft rule reads differently on a campaign page and a settings panel, and most generated design fails by applying one surface's grammar to another's job.

**Pick the mode from the requested surface, not from the product.** A developer tool's landing page is **Persuade**. A fashion house's documentation is **Read**. A docs index is **Read**, not Persuade. The product's category tells you nothing about the mode of the page you were asked for.

| Mode | The visitor… | Design's job | Typical surfaces |
|---|---|---|---|
| **Persuade** | decides and acts | earn attention and action; design *is* the product | landing pages, marketing, campaigns, pricing |
| **Operate** | completes a task | scanability, consistency, native expectation; brand lives in precise details | app UI, dashboards, editors, admin, settings, tools |
| **Read** | understands something | structure for comprehension, then make the reading worth staying in | docs, articles, guides, help, changelogs |
| **Experience** | is inside the work itself | let the artifact lead from the first viewport; the interface recedes | portfolios, galleries, showcases |

State the mode once, in the direction contract, and let it bind downstream. When a deliverable spans modes (a marketing site with a docs section), each surface carries its own mode — don't average them into one register.

## What each mode changes

**Persuade.** The opening must make the offer intelligible and desirable, expose a clear action, and demonstrate something only this product can prove. Conversion lives inside the chosen form's own vocabulary: a hook that lands in one line, a visible primary action, a legible reading order. A committed form that hides the offer or the action hasn't finished translating. Bold colour strategies (Committed, Full palette, Drenched — `frontend-aesthetic-direction.md`) have permission here.

**Operate.** Expression may never obscure the task, the state, or a familiar affordance. Restrained is the colour floor; a single surface can earn Committed (one dashboard where a category colour carries a report, a drenched welcome screen) but the product as a whole doesn't. Depth below.

**Read.** Comprehension and wayfinding stay intact. Prose measure (65–75ch), heading hierarchy, and navigation matter more than component density. Read surfaces take the typography and consistency rules below; skip the component-density ones.

**Experience.** The work leads from the first viewport. Chrome, nav, and captions recede — but the visitor still has to be able to move through the work, and "immersive" is never a licence to hide the exit.

## Operate depth (and Read notes)

Everything below is written for Operate surfaces; Read surfaces take the typography and consistency sections and leave the rest.

### The product-slop test

Familiarity is often a feature here. The test is whether a category-fluent user can trust the interface immediately, or has to pause at every subtly-off component.

Product UI's failure mode isn't flatness — it's **strangeness without purpose**: over-decorated buttons, mismatched form controls, gratuitous motion, display faces where labels should be, invented affordances for standard tasks. The bar is *earned familiarity*. The tool should disappear into the task.

This inverts the anti-slop reflex, and the inversion is the point: on a Persuade surface, reaching for the category default means you stopped deciding; on an Operate surface, refusing the category default for flavour means you spent the user's fluency on your own expression.

### Typography

- **One family is often right.** Product UI doesn't need a display/body pairing — a well-tuned sans carries headings, buttons, labels, body, and data.
- **Fixed rem scale, not fluid.** `clamp()`-sized headings don't serve product UI: users view at consistent DPI, and a fluid `h1` that shrinks inside a sidebar looks worse, not better. Keep fluid type for Persuade and Experience.
- **Tighter scale ratio** — 1.125–1.2 between steps. There are more type elements here than on a brand surface, and exaggerated contrast reads as noise.
- **Prose still caps at 65–75ch.** Data and compact UI run denser; a table at 120ch+ is fine.

### Colour

- Restrained is the floor (`frontend-aesthetic-direction.md` Phase 3).
- **State-rich semantic vocabulary**, standardized once and reused: hover, focus, active, disabled, selected, loading, error, warning, success, info.
- **Accent for primary actions, current selection, and state indicators only** — never decoration.
- **A second neutral layer** for sidebars, toolbars, and panels: slightly cooler or warmer than the content surface. This one move is most of what separates a designed product shell from a page with a grey strip down the side.
- Heavy or full-saturation accents on inactive states are a defect, not emphasis.

### Layout and components

- **Responsive behavior is structural** — collapse the sidebar, reflow the table, drive columns off breakpoints — not fluid typography.
- **Every interactive component ships default, hover, focus, active, disabled, loading, and error.** Half a set is a defect (`interaction-states-pass.md`).
- **Skeletons for loading**, matched to the layout they replace — not a spinner in the middle of content.
- **Empty states teach the interface**, they don't announce "nothing here."
- **Consistent affordances across the surface**: same button shape, same form-control vocabulary, same icon style. If the save button looks different in two places, one of them is wrong.
- **Overlays escape their container** — the symptom is a dropdown that opens and is cut off by an ancestor's `overflow`; `interaction-states-pass.md` Phase 1 owns the fix list.

### Motion

- **150–250ms on most transitions.** Users are in flow; don't make them wait for choreography.
- **Motion conveys state, not decoration** — state change, feedback, loading, reveal, and nothing else.
- **No orchestrated page-load sequence.** Product loads into a task; nobody wants to watch it arrive.

### What Operate surfaces are allowed

Product can afford things a brand surface can't, and refusing them is its own failure:

- System fonts and familiar workhorse sans defaults.
- Standard navigation patterns — top bar + side nav, breadcrumbs, tabs, command palettes.
- Density: many rows, many labels, a lot of visible information when the user needs it.
- Consistency over surprise. The same vocabulary screen to screen is a virtue here; delight is saved for moments, never spread across pages (`laws-of-composition.md`, Peak-End).

### Review gate for Operate surfaces

Flag on sight: decorative motion that conveys no state · inconsistent component vocabulary across screens · display faces in UI labels, buttons, or data · reinvented standard affordances (custom scrollbars, odd form controls, non-standard modals) for flavour · full-saturation accent on inactive states · a modal reached for first, where inline or progressive disclosure was never tried · an orchestrated entrance on a surface the user opens dozens of times a day.
