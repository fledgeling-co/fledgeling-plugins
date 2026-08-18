# Design System Author: Build a Reusable System Folder

Author a design system as a folder on disk — tokens, components, UI kits, guidelines, assets, and a readme — from scratch or from provided context (codebase, brand guide, Figma exports, decks). Use this when the user asks to *create* a design system or UI kit as a durable, reusable deliverable.

This is the sibling of `design-system-extract.md`: **extract mines what already exists into a tokens file; author builds the whole system deliberately** — tokens plus components plus documentation plus a brand voice. If the user only needs tokens pulled from a source, use extract; if they need a system other projects (and agents) can design against, use this.

**A design system is documentation as much as CSS.** The folder must let a future agent — with none of your current context — produce on-brand work. Every undocumented decision is a decision that future work will get wrong.

## Phase 1: Explore and lay out the folder

Read the provided material (codebase, brand assets, decks — copy key assets and text to disk as you go). Screenshots are lossy — code or Figma data is the source of truth; use screenshots only as a high-level guide. Then create the layout:

- `tokens/` — CSS custom properties, one file per concern (`colors.css`, `typography.css`, `spacing.css`, …)
- `components/<group>/` — reusable UI primitives (e.g. `forms/`, `feedback/`, `navigation/`; a single `core/` is fine for a small set)
- `ui_kits/<product>/` — full-screen recreations of real product views, one directory per product/surface
- `guidelines/` — foundation specimen cards and deeper-dive prose
- `assets/` — logos, icons, illustrations, imagery, font files
- `readme.md` (root) — the design guide and manifest
- `styles.css` (root) — **`@import` lines only**, never inline rules: the single entry point a consumer links. Keeping it imports-only means adding a concern never touches the entry point, and the import list *is* the table of contents.

Record every source you were given (repo paths, Figma links, file names) in `readme.md` — the reader may have access even if you assume they don't.

## Phase 2: Tokens — base values AND semantic aliases

Write the token files with both layers: base values (`--gray-9`, `--font-serif-display`) and semantic aliases (`--text-body: var(--gray-9)`, `--surface-card`). Base values make the scale visible; semantic aliases are what components reference, so a rebrand edits one layer without touching components. Copy webfont files into `assets/` and write `@font-face` rules in a token-layer CSS file. **Missing font files:** find the nearest Google Fonts match, use it, and flag the substitution to the user with a request for the real files — a silent stand-in becomes permanent.

## Phase 3: Interrogate the brand into `readme.md`

Answer ALL of these — an unanswered question is a decision the next agent will invent.

**CONTENT FUNDAMENTALS:** How is copy written? Tone (formal/warm/terse)? Casing (sentence case vs Title Case, and where)? "I" vs "you"? Emoji — ever, and where? The overall vibe? Include specific real examples of on-brand copy, not adjectives alone.

**VISUAL FOUNDATIONS:** Colors, type, spacing — and then the questions that actually distinguish brands: What do backgrounds do (images? full-bleed? illustration? repeating patterns/textures? gradients?)? Animation (which easing? fades? bounces? none?)? Hover states (opacity, darker, lighter?) and press states (color shift? shrink?)? Borders? Inner/outer shadow systems? Protection gradients vs capsules over imagery? Use of transparency and blur — when? The color vibe of imagery (warm? cool? b&w? grain?)? Corner radii? What does a card look like (shadow, rounding, border)? Answer every one; add anything else you observed.

**USAGE RULES, not adjectives.** Wherever the system constrains something, write the constraint as an enforceable rule a reviewer can check mechanically: a frequency ("one accent moment per ~600vh"), a role ban ("mustard is never a CTA — it is jewelry"), a forbidden value ("pure white only as inverse text in the dark panel; pure black is forbidden — the darkest value is the ink token"). "Use sparingly" is a decision deferred to the next agent; a rule is a decision made.

## Phase 4: Foundation specimen cards

Create many small HTML specimen files in `guidelines/` — target ~700×150px each, and **split at the sub-concept level**: separate cards for primary vs neutral vs semantic colors; display vs body vs mono type; spacing tokens vs spacing-in-use. A typical set is 12–20+ cards; err toward more small cards, not fewer dense ones — small specimens are scannable and diff-able. No titles or framing inside the card (name the file instead); just the swatches/specimens. Each card links the real `../styles.css` so it renders from live tokens — a specimen with hardcoded values silently drifts from the system it documents.

## Phase 5: Iconography — copy, never draw

Add an ICONOGRAPHY section to `readme.md`: which icon system, icon font, or SVG set the brand uses; whether emoji or unicode glyphs ever appear. Then, in strict preference order: (1) **copy the codebase's own icons** (font/sprite/SVGs) into `assets/`; (2) if the set is CDN-available (Lucide, Heroicons, …), link it from CDN; (3) otherwise substitute the closest CDN match — same stroke weight, same fill style — and **FLAG the substitution**. **Never draw your own SVGs** — hand-rolled icons are the fastest tell of an off-brand system. Avoid *reading* SVG file contents (a waste of context): copy them programmatically and reference by path.

## Phase 6: Components

For each primitive (Button, Input, Select, Checkbox, Switch, Card, Badge, Tag, Avatar, Tabs, Dialog, Toast, Tooltip, …), grouped by concern, author three things:

1. **The implementation** — self-contained, styled exclusively via the token custom properties (no hardcoded values, no external packages). Match the consuming stack: plain HTML/CSS/JS component patterns for artifact work, or JSX if the target codebase is React.
2. **A props/API contract** — a `<Name>.d.ts` (or equivalent typed interface) documenting every prop/variant/state. The contract is what lets another agent use the component without reading its source.
3. **`<Name>.prompt.md`** — first line: one sentence of *what it is and when to use it*; then a small usage example; then notable variants and props. This is the file a future agent reads first.

Add a demo HTML per group showing key states densely — primary/secondary/ghost, sizes, disabled, with-icon — not a single default render.

### When the job is an inventory rather than a build

"Identify the reusable parts" / "build a component library" from a finished page or flow is this phase run as a *read*: walk the surface section by section and, for each visual element, ask whether the pattern appears more than once, whether it could reasonably appear elsewhere, whether it has variants, and whether it has states. Any yes makes it a candidate. Write the inventory to `component-inventory.md` — one section per component with the name (short, conventional: `Button`, `EmptyState`, `FormField`), a one-sentence purpose, variants, sizes, states, the tokens it references, what it composes from, accessibility notes, and at least one do and one don't. The primitive list above is the checklist; do not re-derive a generic atomic-design taxonomy, which is the one thing a competent model produces unaided and the one thing an inventory does not need.

**The gaps are the deliverable, not a footnote.** Walking a real surface always turns up four kinds, and each is work the user now knows about:

- **Inconsistencies** — three slightly-different button styles where one should serve. Flag and recommend the canonical version, and weight a *near*-miss as more severe than a far one: a value within ~5% of an existing token reads as "almost right, therefore wrong" (colour perception is non-linear), where a clearly different value might be deliberate.
- **Missing states** — a component with hover but no focus, or no disabled state. Absence is invisible in a screenshot, which is why it survives to the inventory.
- **Missing variants** — a design with delete actions and only primary buttons needs a destructive variant; name it rather than inventing it silently.
- **Off-scale values** — spacing or sizes outside the established scale. Flag and snap — **unless the surface is a matched system**, where the resolved value is data and snapping it breaks the match (SKILL.md §4).

Then recommend the next step: `design-system-extract.md` if tokens do not exist yet, building the primitives as code per Phase 6 above, or `polish-pass.md` on each component so they hold up at the atomic level.

## Phase 7: UI kits — replicate, never invent

For each product, build 3–5 core screens in `ui_kits/<product>/` as high-fidelity, lightly interactive click-through recreations (login, main view, settings, …). Rules:

- **Compose the primitives from Phase 6** — never re-implement Button inside a kit; the kit is proof the primitives suffice.
- **Pixel-perfect to the source.** Code or Figma data is truth; screenshots are lossy reference only.
- **Never invent.** The job is replication. If a section isn't in the source material, omit it or leave it purposely blank with a visible disclaimer — an invented section poisons the kit as a reference.
- Iterate visually 1–2× against the source before calling a screen done.

## Phase 8: Finish — index, SKILL.md, verify

- Add a short index to `readme.md`: a manifest of the root folder plus the list of components and UI kits.
- **Emit a portable `DESIGN.md`** at the folder root in the 9-section library shape (Visual Theme & Atmosphere / Color / Typography / Spacing & Grid / Layout & Composition / Components / Motion & Interaction / Voice & Brand / Anti-patterns, opening with an H1 title + `> Category:` line) — a condensed, prose distillation of the readme that other design tools and DESIGN.md-driven agents can consume directly. The readme is the system's manual; the DESIGN.md is its passport.
- **Write a `SKILL.md`** at the folder root so the system is itself an installable Agent Skill:

```
---
name: {brand}-design
description: Use this skill to generate well-branded interfaces and assets for {brand}. Contains design guidelines, tokens, fonts, assets, and UI kit components.
user-invocable: true
---

Read readme.md in this skill and explore the available files. For visual
artifacts (mocks, decks, prototypes), copy assets out and build static HTML.
For production code, use the tokens and rules here to design on-brand.
```

- Verify: open a specimen card, a component demo, and a kit screen in a browser; confirm tokens resolve, fonts load, no console errors.
- Report caveats only (substituted fonts/icons, inaccessible sources, blank-by-design sections) and end with a clear ask for what the user should review to iterate toward perfect.
