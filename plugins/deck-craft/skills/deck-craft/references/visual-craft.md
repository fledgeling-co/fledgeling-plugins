# Visual craft for decks — direction, type, colour, hierarchy

Everything needed to make a deck look designed rather than generated. Self-contained: no other skill required.

## 1. Ground it in what exists before inventing anything

A deck rooted in real context beats one invented from taste. Before drawing, look for, in this order:

1. **A `DESIGN.md` / design-language spec** in the project root or supplied by the user. Binding, not inspiration. Build from its tokens; never guess a `var(--*)` name, because an unresolved custom property silently falls back and the slide renders in the wrong colour with no error.
2. **A token file** — `tokens.css`, `theme.ts`, `_variables.scss`, or a `theme.tokens` block in a deck JSON. Lift exact hex values, exact font stacks, exact radii and spacing steps. Approximating a brand colour by eye is the most visible failure a branded deck has.
3. **An existing codebase or product UI.** Read the source rather than a screenshot when both exist — you reproduce an interface far more faithfully from code.
4. **Prior decks from the same company.** Match the footer treatment, the section-break pattern, the chart style. A deck that looks like the last one is doing brand work.

Only when none of that exists do you author a direction from scratch (§2). If a brand plainly exists but wasn't supplied, ask for it rather than inventing one.

**Say in one line what you matched**, before the first slide: *"matching `packages/ui` — Söhne, 6px radii, slate and indigo tokens, 34px body on a 1920 canvas"*. It takes a sentence and it is the only way the user can catch you having matched the wrong thing before twelve slides are built on it.

**And when a genuine search finds nothing, say that you looked.** The two sentences are different claims: "no design system was supplied" and "I searched the project root, the token filenames above, `design-system/` and `ui/`, and the screens nearest this deck, and found none, so I authored the direction in §2" — the second one is checkable. A silent fallback to an invented direction reads exactly like a matched one.

**Consuming a `DESIGN.md` well.** Take the palette roles (not just the hexes — which colour is *primary*, which is *accent*, which is background), the type ramp with its weights, the spacing scale, the radius scale, and any stated do/don'ts. Map them onto the deck's own scale: a web design system's 16px body becomes 34px on a 1920 canvas, but the *ratios* between its steps carry over. Where the system is silent (decks usually need display sizes a web system never defines), extend it in its own logic rather than importing a different system's values.

## 2. When there's no brand: commit a direction

Mocking a deck without committing to an aesthetic is the fastest path to template output. Pin down the subject, the audience, and the deck's single job — then mine the *subject's own world* for the design language. A mining company's deck can take its palette from ore and steel; a legal-tech deck from paper stock and rule lines. Subject-derived choices are where distinctiveness actually comes from; generic "modern, professional" is where it dies.

**Name the rut before you shortlist.** Two things are ruled out before any candidate: the deck this occasion always ships, and its predictable opposite. "Board pack → navy, grey, Arial" is the first; "board pack but not navy → near-black with one accent" is the second, and it is exactly as reflexive. Write both down and keep both off the list. If the brief paints its own picture — a company name, a campaign line, a governing metaphor — its literal reading joins the rut: spend at most one candidate on it.

Then derive several candidates from the audience's own world, and check the spread: **the candidates must span at least three material families**. The audience's world includes its graphic and screen traditions, not only its physical objects — the notation, filings, publications, instruments and identity programs it reads daily. A drilling-services audience knows core trays, survey plots, hi-vis, and the AS/NZS spec sheet; that is four families, and a list of four ore-coloured palettes is one. Near-duplicates count once.

**Then don't take your top-ranked candidate by default.** Rank them, and treat the top one with suspicion: it is what every run on this brief produces, which is the outcome the whole procedure exists to avoid. Build a lower-ranked one unless the top is forced by product truth or an explicit brief constraint, and say which rank you took. Taste is never grounds for climbing back up; a factual failure — it can't carry the subject, the assets don't exist — is.

`direction-index.md` is evidence for this step, not a menu to shop: shortlist against the candidates you derived, don't let the table generate them.

Commit on three axes and state them:

- **Scheme** — light paper / dark canvas. Not "dark because tools look cool dark". Write one sentence of physical scene: who is watching this, in what room, on what screen, at what time. If the sentence doesn't force the answer, add detail until it does.
- **Formality** — boardroom ↔ zine.
- **Density** — airy manifesto ↔ data-heavy working deck.

Then declare two things and hold them: **one signature element** (the thing the deck will be remembered by — a full-bleed section break, a recurring rule, a distinctive numeral treatment) and **one justified risk**. Spend the boldness there and keep everything around it quiet. Not taking a risk is itself a risk: "competent but anonymous" is the failure mode of every deck that got no complaints and changed no minds.

**The swap test.** Imagine a neighbouring brief — a different company in the same sector. Would your direction fit it unchanged? Any axis that transfers untouched is a default, not a choice. Revise that axis. Then run it one tier deeper: could someone guess your direction from the occasion *plus the rut you named*? That is the second-order reflex, and it is still a reflex.

### The standing exit — the convention, played straight

Every direction round carries one permanent alternative: **the category standard, executed at full fidelity.** The conventional board deck. The house results template. It is the user's door and never your recommendation — don't argue for it, don't weigh it against the committed direction, don't let it soften the other options.

This matters more for decks than for most artifacts. Board, regulatory and results audiences legitimately want the convention, and without an explicit door they have to fight the anti-slop rules to ask for it. When they take it, convention *becomes* the commitment: ask once for two or three decks this should sit alongside, make their craft level the bar, and execute the canon at full fidelity — no irony, no smuggled quirk, no "elevated" version of it.

### Write the direction down where the build can see it

A direction declared only in conversation drifts by slide 9. Write it into the artifact as five short blocks, ≤150 words — an HTML comment at the top of the file for an HTML deck, `x.diolog.direction` for a JSON one:

- **THESIS** — the one idea this deck owns, and the occasion's default arrangement it refuses.
- **OWN-WORLD** — palette, type ramp and surface language, specific enough to recognise with all content removed. Real values, not adjectives.
- **STORY** — what the audience understands, believes, and does.
- **COVER** — the exact composition of slide 1: what is where, at what scale.
- **FORM** — the candidate taken, its rank on your list, and why that one.

If a block reads like a mood, the direction isn't decided yet. "Serious and confident" is not an OWN-WORLD; `#12171C` ground, bone paper, one signal-orange accent, Söhne over a condensed grotesk, hairline rules and no radius is. `deck-review.md`'s delivery pass audits the finished deck against these blocks promise by promise, so a block that can't be checked is a block that won't be.

## 3. Typography

**One or two families.** Pair on a contrast axis — serif + sans, geometric + humanist, display + text — or use one family across several weights. Two similar-but-different sans faces read as a mistake, not a pairing.

**A scale, and only the scale.** Define display / title / subtitle / body / caption as tokens and use nothing else. Arbitrary sizes (`37px` beside a 34px body) are the clearest tell of a deck assembled slide by slide rather than designed.

**Sizes for distance.** On 1920×1080: body ≥24px and ideally 32px+; headlines 60–96px. Scale ~0.67 for 1280×720. A user naming a size means points — `px = pt × 1.333`.

**Track deliberately.** ALL-CAPS labels need `letter-spacing: 0.06–0.1em` or the counters collide. Display type ≥48px needs −0.02 to −0.03em, with a hard floor of −0.04em — tighter and letters touch, which reads cramped rather than designed. Body stays at 0. Untracked caps and untracked display are the two most reliable typographic tells.

**Leading and measure.** Display at line-height 1.0–1.2; body at 1.4–1.5 on slides (tighter than web, because lines are shorter and the reader is further away). Cap body lines at ~45–60 characters — a full-width line of 34px text on a 1920 canvas is unreadable at distance.

**Never letter-space or italicise Arabic or Hebrew** — neither script has an italic tradition and spacing breaks cursive joining.

**Avoid the attractors.** Space Grotesk, Inter, Roboto, Arial, bare system stacks, and the silent serif-display defaults (Fraunces, Playfair, Georgia-as-display). Each is fine when chosen; each is a tell when it arrives by gravity. The test: one sentence defending the choice that mentions this deck's subject.

## 4. Colour

**Extract when a brand exists** (§1). Otherwise build a small palette in `oklch()` so hues stay harmonically related:

```
--a: oklch(50% 0.15 250);  --b: oklch(50% 0.15 200);  --c: oklch(50% 0.15 280);
```

**Three to five colours across the whole deck**, plus tints. Limit backgrounds to 1–2; a section break may take a third.

**Count hue families, not swatches, and count them across the deck rather than per slide.** The failure never looks like a palette decision: a status chip takes green for *done*, another takes blue for *in progress*, a delta chip takes green for *up*, and the deck is carrying three hues while every slide in isolation looked disciplined. Measured on two decks from one brief and one brand spec: **1 hue family against 3** — and the three-hue deck's own stylesheet declared the same "one accent" rule in a comment. Semantic colours earn their place on genuine state, always paired with an icon or a word; a status column that reads correctly in greyscale never needed the hue. `deck-preflight.js` reports `hueFamilies`.

**Pick a strategy, don't drift into one.** *Restrained* — tinted neutrals plus one accent under ~10% of pixels; the default for data decks. *Committed* — one saturated colour carrying 30–60% of the surface; identity decks. *Drenched* — the slide is the colour; covers and section breaks. Defaulting to Restrained without deciding is how timid, evenly-grey decks happen.

**Spend the accent once per slide.** One thing matters; give it the colour. An accent on four elements is decoration. The measurable form: two decks from one brief averaged **1.8 accent marks per slide against 3.7, peaking at 3 against 7**. Seven marks on a cover — eyebrow, half the headline, a rule, two pills, a progress bar, a button — is not a bold cover; it is a cover with no focal point, because everything shouting is the same as nothing shouting.

**Three places the budget goes without anyone deciding**, all measured on one deck. A data table whose column headers are set in the accent spends it four times before the slide has said anything — move the colour to the 2px rule beneath the headers, which keeps the structural signal and returns the whole budget. A set of status marks spends one per row; charcoal marks distinguished by fill weight, glyph and word read correctly in greyscale and leave the accent for the one thing the slide is actually about. And a numeral chip on every card in a six-card grid is six — those are labels, so `ink-muted` is the right colour and the eye still finds them. Count in the rendered capture rather than in the stylesheet: an automated check that walks only text-bearing leaves scores filled bars, rules, tracks and dots at zero while the eye counts every one of them — which is why `deck-preflight.js` counts drawn marks alongside text ones as of 18 Aug 2026, reporting `textMarks` and `drawnMarks` separately so a slide that is over budget on geometry rather than on type says so.

**Tone the neutrals.** `#FAFAFA` / `#1A1A1A` rather than pure `#FFFFFF` on `#000000` — pure black-on-white is harsh projected and reads unfinished.

**Never encode meaning in colour alone.** Pair with position, label, or shape. Roughly 8% of men have a colour-vision deficiency, and a projector's gamma will flatten your careful red/green distinction anyway.

**Contrast floor:** body text ≥4.5:1 against its background, large text (≥24px bold / ≥32px) ≥3:1. Projection loses contrast — a pairing that passes marginally on your monitor fails in a bright room. Check the muted roles specifically: mid-grey captions on a tinted near-white ground are the most common failure in generated decks.

**Dual-theme contrast on dark bands:** When alternating between light paper and dark canvas sections (`#2E2B2B` / `#181717`), a primary brand colour chosen against light backgrounds will fail AA contrast on dark grounds. Always define a dedicated lifted accent token (e.g. `--color-primary-on-dark: #FF5A5F` against `#2E2B2B`). Use translucent pill backgrounds (`rgba(255,255,255,0.12)` or `rgba(color, 0.15)`) with high-contrast text (`#4ADE80`, `#60A5FA`). Badges placed directly over photographic scrims must use a solid brand background with bold white text.

## 5. Hierarchy and rhythm

**Hierarchy is built from five vectors, not size alone:** scale, weight, colour, spacing (more room = more important), and position. The dominant element needs at least two working the same direction — size-only hierarchy collapses the moment a long headline forces the size down.

Two failure modes, and their fixes: **flat** (everything at similar weight; steps under ~1.25× with no compensating jump) → increase contrast on two vectors. **Noise** (several elements competing as co-primaries; everything bold or accented) → promote one deliberately and demote the rest, including things that feel important. Hierarchy is relative; something has to lose.

**Three weights is plenty:** body (400/450), UI and labels (510/550), headlines (590/600). Weight should jump between levels, not step — a regular→medium→semibold→bold ladder reads as a default scale rather than an authored one.

**Rhythm is repetition with deliberate variation.** All spacing snaps to one scale (multiples of 8 at deck sizes) — **unless you are matching a system whose own scale is not 8-based**, in which case its scale wins and rounding to yours is the defect. This rule is for authoring from scratch; a matched system's steps are lifted exactly, like its colours. Repeated elements sit in identical positions slide to slide. Then break the pattern once or twice for emphasis — a page that varies every slide is chaos; one that never varies is a list.

**Value outranks label.** On a stat, "$48.2m" is larger and heavier than "Revenue". The label whispers; the number speaks.

**Cross-slide discipline.** Section headers look identical to each other. Card groups align across columns — titles at the same Y, footers pinned to the same line — because misaligned baselines across side-by-side cards read as broken rather than varied.

**A list laid out as a grid needs its rhythm from `row-gap`, not from item margins.** `li:first-child { margin-top: 0 }` zeroes only the DOM-first item, so in a two-column grid the second column's first row keeps its margin and sits a full gap below its neighbour — a misalignment that looks like a rendering fault and is arithmetic. Zero every item's margin in grid mode and let `gap: 22px 72px` carry both axes. The general form: when a rule keys off document order but the layout is two-dimensional, the rule and the layout disagree about which item is first.

## 6. Anti-slop

Each rule leads with the move to make; the trailing clause names what to avoid.

- **Flat colour by default.** If a gradient is needed: two stops, low contrast, same hue family. Avoid rainbow, neon-on-neon, and 3+ stop gradients — and the purple-to-pink hero especially.
- **No emoji** unless the brand uses them or the emoji is functional. 🚀 📈 ✅ sprinkled for colour is the single fastest way to make a deck look generated.
- **Real photography, professional illustration, or an established icon set** (Feather, Material, Phosphor, Heroicons). Avoid hand-drawn SVG of people, scenes, or abstract concepts. With no asset, use an honest placeholder — a striped ground with a monospace label naming the asset and its dimensions. A placeholder shows intent; a weak illustration shows you didn't have the asset.
- **This bans SVG imitating pictures; it never bans SVG doing geometry.** Rules, hairlines, drawn marks, flat shape systems, diagrams with countable elements, and the accent devices `layout-specs.md` specifies are first-class deck material. The line: geometry is what you can specify exactly; a shaded, perspectived or figure-bearing drawing is a *picture* even in line-art style, and pictures get sourced, generated, or honestly placeheld.
- **No imitation material.** CSS bevels, embossing, faux letterpress, fake foil, stamped-metal and chalk effects standing in for a material the slide never actually renders read as machine-made faster than any other tell — and decks reach for them more than web pages do, usually on a cover. Either the material is a real asset or the surface is honestly flat. A gradient standing where a texture belongs ships the gradient.
- **Depth with an offset and a soft blur, from one light source.** A zero-offset coloured halo is paint, not elevation; a hard offset block shadow (`4px 4px 0`) is a costume that only a genuinely neobrutalist direction earns.
- **Backgrounds with intent.** A flat toned ground, one photograph, or one geometric device. Avoid the default corporate wash: blue-purple gradient, faint hex grid, floating translucent circles.
- **Vary the module, not just its contents.** Reaching for the same 3-or-4-across bordered card row on slide after slide is the strongest single tell of generated layout, and it is invisible while you build because each slide's grid was a reasonable local choice. Measured: seven of twelve slides on one deck were an identical card row; the comparison deck used stat tiles, an editorial photo split, a data table, a progress matrix, a milestone grid, a shared-scale bar pair and a full-bleed photograph across the same twelve. Before building a card row, ask what this slide's content actually *is* — a comparison, a sequence, a matrix, a single figure — and let that pick the module.
- **Card discipline.** Separate with a thin all-round border, a subtle shadow, or background contrast. **Never use `border-left: 4px solid` on generic cards, quotes, or metric tiles** — reserve left borders strictly for genuine system warnings or semantic alert banners. On quotes and leadership cards, use **top accent rules** (`border-top: 4px–6px solid var(--primary)`), subtle background contrast, and role chips instead.
- **Asymmetric Editorial Layouts.** Move beyond identical card grids: pair a full-height editorial photograph on one half of the slide (`grid-template-columns: 1.06fr 0.94fr` or `.92fr 1.08fr`) with an overlaid gradient scrim and a zero-based chart/bullet list on the other half. Full-height imagery grounds the slide in reality.
- **Brand Geometric Signatures.** Translate the subject's physical and industrial world into authored CSS geometry:
  - Custom list bullets using SVG/CSS polygon clip-paths (e.g. chevron marks `clip-path: polygon(...)`) instead of generic round bullet dots.
  - Heavy grounding accent rules (`.rule` e.g. `width: 96px; height: 8px; background: var(--primary)`) at the top of headers, evoking structural beams or rule lines.
  - Section divider bands (`.chev-band` with angled `clip-path: polygon(...)`) separating content zones.
- **Charts show the point.** Cut every series and column that doesn't support the slide's claim. Avoid 3D, avoid gratuitous legends where direct labels work, and never truncate a value axis on a comparison — that's a defect, not a style.


## 7. Accessibility & Typography Floors

Not an add-on; on a projector it's just legibility. Contrast per §4. Never encode by colour alone. Keep interactive affordances (in an HTML deck: nav, links) keyboard-reachable with a visible focus ring — `:focus-visible { outline: 2px solid …; outline-offset: 2px }`, never `outline: none` with no replacement. Respect `prefers-reduced-motion`: under it, builds apply instantly but keep their click steps, because build order is content rather than decoration. Meaningful images get alt text; decorative ones get `alt=""`.

**Two-Tier Typographic Scale on 1920×1080 Canvas:**
- **Primary Content Floor (≥24px, ideally 28px–34px+):** Body prose, slide titles (68px–104px), lead paragraphs (32px–40px), hero stats (56px–96px), chart values (28px–38px).
- **Auxiliary/Accessory Floor (≥18px–20px):** Eyebrow category overlines (18px uppercase tracking `0.12–0.14em`), tabular data table cells (20px), chart axis sub-labels (20px–23px), stat descriptive notes (20px), and statutory footnotes/timestamps (20px). Do not artificially inflate 18px eyebrows or legal footnotes to 24px; doing so compresses visual hierarchy and makes metadata compete with body copy.

## 8. The last look

Before delivering, remove one thing. Review rounds accrete — a rule here, a badge there, a second accent that crept in. Find the element the deck doesn't need and cut it. If you genuinely can't find one, ship.

The reliable place to find it is a **hero numeral standing for something that isn't a metric**. A stat tile reading `3` over "Jurisdictions" borrows the visual weight the deck reserves for its financial figures and spends it on a count of countries — it is a fact wearing a metric's clothes, and it is the element a sceptical reader questions first. Cut the tile, fold the fact into the prose beside it, and nothing is lost but the borrowed authority.


## Provenance on a slide

A deck has no place to hang a marker, so the contract has to be carried by composition. Three
rules, all learned on an ASX-derived deck:

- **Every number on a slide traces to the source document.** If it is not in the source, it is
  not on the slide. There is no "roughly" on a slide a board will read as a statement.
- **NEVER depict a real named person with a generated AI photograph.** Fabricating an AI likeness for a real named executive, board director, CEO, or key personnel produces uncanny visual artifacts (distorted hands, synthetic attire, hallucinated background text) and destroys deck credibility. On leadership and governance slides:
  - Use **structured typographic credential cards** (Degree, Professional Body e.g. AusIMM / AICD / CPA, Prior Executive Track Record, Board Sub-Committees).
  - Use authentic company facility/infrastructure photography or corporate insignias.
  - A clean typographic credential card outranks a fabricated synthetic portrait 100% of the time.
- **Precision is a claim.** If the source says a quarter, the slide says a quarter. Inventing a
  date or a decimal to make a chart tidier fabricates specificity the record does not support.

If a deck and a data-driven surface are built from the same material, the surface's provenance
model is the better source: read `ux-craft/references/data-provenance.md` and carry its three
states into what you choose to put on a slide.

