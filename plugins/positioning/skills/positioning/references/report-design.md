# The designed report — one HTML surface, gated before it ships

Markdown carries the argument. The HTML carries the decision — it is what gets
opened in a meeting, scrolled through on a phone, and sent to a co-founder. The
predecessor shipped a decision page as a template to "adapt", with no gate on
what came out the other side, and the style guidance was one paragraph at the
bottom of the SKILL.

## Route the design, don't improvise it

**`/design-craft:design-craft` is the visual authority and
`/ux-craft:ux-craft` is the UX authority.** Load both. They are a standing pair,
not alternatives: ux-craft decides the flow, the states, the reading order and
the words; design-craft decides the type, the colour, the elevation, the motion
and the anti-slop pass. Never let visual polish override a usability call.

Two things to hand them that they cannot derive:

- **The brand.** If the project has a `DESIGN.md` (or `design.md`, or a token
  file, or a brand guideline), read it and build to it — that is the whole point
  of the file existing. Where none exists, author one. `design-craft` carries
  `design-system-author.md` for exactly this, and the authored system is written
  to `docs/positioning/DESIGN.md` so the next run and the next artifact use the
  same one rather than inventing a second.
- **The subject.** A positioning report about a logistics product and one about
  a developer tool should not look the same. The palette, the imagery and the
  type are mined from the product's own category, and the run says in one line
  what it mined and what it deliberately left.

## What the surface actually is

One self-contained HTML page at `docs/positioning/positioning-report.html`,
beside the nine markdown reports rather than in a directory of its own, with
these sections in this order:

1. **The recommendation**, above the fold, quotable.
2. **The shortlist**, side by side, comparable at a glance.
3. **Feel the copy** — each territory's hero rendered as it would actually
   appear, at real type sizes. This is the section that changes minds, because a
   hero line in a table reads differently from a hero line set as a hero.
4. **The evidence** — the claim register, filterable, each row showing its
   confidence and its independent-domain count.
5. **The decision instrument** — see `decision-aid.md`. Not a naive weighted
   scorer.
6. **What has to be true**, and the pre-commitment tests.

## Motion, 3D and imagery — each with a reason to exist

**GSAP** for the scroll-driven passages: the shortlist comparison that pins
while the four axes swap, the value-curve that draws as it enters. Load it per design-craft's own
`gsap-motion` reference — pinned CDN with SRI for a served
or local page, inlined source for a published Artifact, because an Artifact's
CSP blocks every external origin silently and the page ships motionless with
nothing in the console to say so. Entrance motion is `gsap.from`, never
`gsap.to`. `prefers-reduced-motion` gets a real static layout, not a fast one.

**Three.js** only at rung 6 of `design-craft`'s depth ladder — when the 3D
object *is* the content and rungs 1–5 cannot fake it. On a positioning report
there is exactly one honest candidate: the **strategy canvas as a dimensional
surface**, where the competing value curves are read against each other and the
uncontested space is a visible volume rather than a gap between lines. If the
canvas is better as a flat annotated SVG — and for four factors it usually is —
build the SVG and say the rung was not needed. A WebGL hero on a document nobody
asked to be impressed by is the 3D version of a rainbow gradient.

**media-gen-pro** for imagery the design genuinely needs: a category-mined
texture, an editorial header image, a scene that carries the enemy metaphor.
Never for diagrams. Diagrams are mermaid or hand-authored SVG — native, legible
in both themes, maintainable, and correct. An image of a chart is a chart nobody
can fix.

**The figure is in the DOM before anything runs.** Charts are inline SVG or a
table, computed at build time. A chart drawn at runtime is absent with
JavaScript off, absent in print, and absent in the PDF that gets forwarded.

## Then gate it

Run **`/design-review:design-review`** on the rendered page before it goes to
the user. Not as a formality — it is the pass that catches what the building
session cannot see, and its own evidence file documents a review that went green
on a broken layout because only the WCAG gates ran.

Enumerate the surfaces first: the report page is one surface, plus one row for
shared chrome, plus one row per interactive state that changes what is on screen
(the decision instrument at rest and after weighting, the evidence table
filtered, reduced-motion). `scripts/worklist.py check` exits non-zero while any
cell is open, and that exit code is what "the review is finished" means.

Take the findings back into the page and re-run. A Tier 1 finding blocks; a Tier
3 finding is recorded in the delivery note and left alone if the user's time is
better spent elsewhere. Say which happened.

## Look at it

Serve the page, open it, read the render. `design-craft`'s rule is the one that
matters here: rendering an image is not seeing one — a screenshot enters your
knowledge only when you open it. Ask each capture "what is wrong with this?"
rather than "is this done?", because the same pixels answer those two questions
differently.

Then, because this is a finished artifact for a human:
`open -a "Google Chrome" docs/positioning/positioning-report.html`, and one
sentence saying what to look at.
