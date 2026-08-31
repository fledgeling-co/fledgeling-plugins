# Generate Variations: Produce 3+ Design Options

Produce multiple distinct design variations of a screen, component, or flow so the user can mix and match the strongest pieces. Use this when the user asks for options, alternatives, "different takes," or "show me a few."

**Variations are the cheapest path to good design.** A single design is one bet. Three variations let the user reject what they don't want and combine what they do.

## Phase 1: Establish the baseline

Confirm:

- **What is being varied.** A single screen, a component, a whole flow, a visual treatment? Scope determines how many variations are useful.
- **Existing design context.** Is there a UI kit, design system, or reference design? Variations should still root in that context unless explicitly asked to break free.
- **Number of variations.** Default to 3 if unspecified. 5–6 is a healthy ceiling — more than that and the user can't hold them all in mind.
- **Axis preference.** Does the user care most about visuals, interactions, layout, or copy/tone? You can vary on multiple axes, but knowing the priority helps you weight the explorations.

## Phase 2: Lock the identity before picking axes

**When the variations sit on an existing surface, the brand is already chosen — the job is variation *within* identity, not selection *between* identities.** The worst failure of a variation round is three off-brand options the user cannot accept, so this phase runs first and doesn't get skipped.

Write **one sentence** recording what is actually on screen, from DESIGN.md's visual fields, the CSS custom properties (the de-facto tokens), the computed styles on the target and its parent, and the visual rhetoric of its siblings: dominant surface and accent colour as **real values**, the loaded font pairing, layout topology (stacked / side-by-side / grid / asymmetric / overlay), surface treatment (corners, borders, shadows, decoration density), and the voice tone read off the copy. Be specific, skip an axis rather than invent one, and **don't name an aesthetic family** — a family is a conclusion, not data, and naming one licenses drift toward what that family usually looks like. A missing DESIGN.md is never an excuse; the identity is in the code.

This sentence is the **identity lock**. Every variation has to read as the same brand standing next to the others.

### Default mode vs departure mode

- **Default** preserves the identity and varies expression within it. Right for roughly nine rounds in ten.
- **Departure** rejects the identity. Trigger it **only** on the user's explicit ask in the current request — "redesign this", "rebuild from scratch", "something completely different". A stale note or an old critique is not authorization.

Unsure means default, and the reason is asymmetric risk: a wrong default costs three on-brand options that feel similar, which the next round recovers from; a wrong departure costs three off-brand options, which it doesn't.

Greenfield work with no incumbent surface skips this phase and runs `frontend-aesthetic-direction.md` instead.

## Phase 3: Pick the axes

Common variation dimensions — pick 2–4 to vary across:

- **Visual treatment** — color tone (warm / cool / neutral), density, shadow style, border radius, type weight
- **Aesthetic family** — pull directions from different *groups* of `aesthetic-worlds.md` (grids, quiet-human, tools, motion-raw, genre), not three rows from one group. The short range map in `frontend-aesthetic-direction.md` is the fallback when you have not opened the worlds table
- **Layout** — centered vs asymmetric, single-column vs multi-column, full-bleed vs inset, grid-heavy vs flowing
- **Interaction model** — single page vs multi-step, modal vs inline, hover-revealed vs always-visible
- **Motion & depth** — quiet vs one orchestrated entrance vs scroll-driven; flat vs textured vs dimensional (`motion-design.md`, `depth-and-3d.md`)
- **Information hierarchy** — what's elevated, what's secondary
- **Tone** — minimal / formal / playful / expressive / editorial
- **Component style** — filled vs ghost buttons, cards with shadows vs flat, rounded vs sharp

**Vary the structure first; colour buys the least.** Measured across 120 interfaces from five generative UI tools over 24 tasks (*Design Theater*, arXiv 2607.22928): generated designs **converge in visual appearance and layout organisation while their colour choices already vary the most**. So a round that differentiates on palette is differentiating along the one axis that was never collapsed, which is why three colour-worlds can still read as one design. Spend the round on **layout topology, structural decomposition, density and hierarchy** — the axes where the collapse actually is — and treat colour strategy as the fourth choice rather than the first.

**In default mode, each variation commits to a different *primary* axis, drawn from these six:** **hierarchy** (which element commands the eye) · **layout topology** (stacked / side-by-side / grid / asymmetric / overlay) · **typographic system** (pairing logic, scale ratio, case and weight — within the faces already loaded) · **colour strategy** (which existing palette role carries the surface: Restrained / Committed / Full palette / Drenched, existing tokens only) · **density** (minimal / comfortable / dense) · **structural decomposition** (merge, split, progressive disclosure). Three variations, three *different* primary axes — the same brand seen from three angles. New fonts, new hues, and new aesthetic-family signals belong to departure mode only.

**In departure mode**, anchor each variation to a different aesthetic direction *derived from the brand*, never a fixed catalogue: read the product's personality, derive physical or material experiences that embody it, and from those derive three directions genuinely different from each other and from the current surface. Each one names a real-world referent in a concrete sentence ("a museum exhibition label system"), not an adjective pair ("clean and minimal"). Reject any direction whose rationale would fit a neighbouring product unchanged.

Within a chosen brand, variations **remix the brand's own visual DNA**: play with scale, fills, texture, visual rhythm, layering, novel layouts, and type treatments built from the same tokens. The goal isn't the one perfect option — it's atomic variations the user can mix and match.

For each variation, write down which axis (or axes) you're flexing. This makes the comparison legible to the user.

**When the round has an intent, vary along that intent's own dimension** — three takes on the same lever is one variation:

| Intent | Each variation differs by |
|---|---|
| Bolder | which dimension is amplified — scale / saturation / structural change |
| Quieter | which dimension pulls back — colour / ornament / spacing |
| Distill | which class of excess is removed — visual noise / redundant content / nested structure |
| Polish | which refinement axis — rhythm / hierarchy / micro-detail |
| Typeset | a different pairing **and** a different scale ratio |
| Colorize | a different hue family; vary chroma and contrast strategy too |
| Layout | a different structural arrangement, never spacing tweaks |
| Adapt | a different target context — mobile-first / tablet / desktop / print or low-data |
| Animate | a different motion vocabulary — cascade stagger / clip wipe / scale-and-focus / morph / parallax |
| Delight | a different flavour of personality — micro-interaction / typographic surprise / illustrated accent / easter egg |

## Phase 4: Build with intent — basic to bold

Order matters. Start with the most by-the-book, end with the most novel:

1. **Variation 1 — by the book.** Matches existing patterns and conventions. The "safe" option — the user knows it works because it looks like things that already work.
2. **Variation 2 — refined.** Takes the safe option and pushes one or two dimensions — bolder type, a more confident layout, a more expressive color choice. This is often the user's actual pick.
3. **Variation 3 — novel.** A genuinely different take — an unconventional layout, a strong visual metaphor, an unexpected interaction, a daring aesthetic. The user may not pick it, but it stretches the conversation and surfaces preferences they didn't know they had.
4. **Variation 4–6 (if requested).** Hybrid points along the spectrum, or a wildcard on a different axis.

**Cover both ends.** Three "safe" variations waste the user's time; three "wild" ones feel like you didn't take the brief seriously.

## Phase 5: Vary substantively, not cosmetically

A variation is not "the same design with a different color." Each should differ on something that actually matters:

✅ Differ in: layout, hierarchy, what's primary vs secondary, type system, density, interaction approach, copy strategy
❌ Same except: button color, accent shade, shadow opacity

If two variations are too close, drop one and replace it with a more substantive alternative. The user should be able to articulate the difference between any two variations in one sentence.

**Specify each variation concretely before building it** — distinct palette family, distinct type pairing, distinct layout skeleton, written down per variation. Variety must be designed, not hoped for: left unspecified, variations drift toward one default look (typically the warm-editorial house style). For the novel variation, deliberately pick something off-distribution and interesting.

### The squint test — run it before you build

**Default mode.** Compare each planned variation against the Phase 2 identity lock: palette drift, type-voice drift, or changed rhetoric means it crossed into departure by accident — rework it. Then confirm three *different* primary axes. Three "slightly tighter density" variations is one variation with rounding error.

**Departure mode — two passes, family before sentence.** *Family pass:* label each variation with a concrete family of your own choosing; shared or interchangeable labels mean rework. *Sentence pass:* write the three one-line descriptions side by side; any two that rhyme mean rework. When the primary axis is colour or theme, the trio must not share theme plus dominant hue — three colour worlds, not three shades of one.

## Phase 6: Present in a single file

Put all variations in **one file** (SKILL.md §18) — live comparison is far more useful. Two patterns:

- **Side-by-side canvas** for static variations — a single HTML page with a CSS-grid of labeled cells, one variation per cell (the snippet is in SKILL.md §18). Good when the variations differ structurally.
- **Tweaks** when the variations share most of the structure and differ on a few axes (color, type, density, a layout toggle) — expose those axes in a floating panel so the user flips between them live. See `make-tweakable.md`.

For a flow or multi-screen variation, build each variation as a small storyboard within the canvas.

## Phase 7: Annotate

For each variation, add a short caption (one or two sentences):

```
Variation 1 — Conventional. Centered hero, single CTA, high contrast.
Variation 2 — Refined. Same structure, expressive headline type, warmer palette.
Variation 3 — Editorial. Asymmetric layout, large pull quote, slow scroll-driven reveals.
```

The captions are a thinking tool — they force you to articulate what makes each variation distinct. If you can't write a clear caption, the variation isn't distinct enough.

**An option keeps its number and its name for the life of the conversation.** Once something is "Variation 2" or "Editorial", it stays that on every later round, in every reply, and in the file — even when round two drops one, adds one, or reorders them by preference. Renumbering is the cheapest way to lose a decision the user already made: they said "go with 2", and after a silent renumber nobody can tell which 2 that was.

## Phase 8: Recommend

End with a clear recommendation. The user is the decider, but a designer offers an opinion:

- "Variation 2 is my pick — it keeps the safety of Variation 1 but adds visual confidence."
- "Variation 3 is the most interesting bet, but higher risk for a customer-facing landing page."
- "Variations 1 and 2 are close — pick based on whether you want neutral or warm."

Be direct. Don't hedge by saying all options are equally good. They aren't.

## Phase 9: Hand off

After the user picks (or asks for another round), suggest the next step: a single-direction iteration to refine the chosen variation; a second variation round on a different axis; `make-a-prototype` to take a chosen variation to interactive; or `polish-pass` if they're ready to ship the chosen variation.
