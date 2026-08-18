# Layout specs — geometry, hierarchy and UX per template

One block for all 200 templates in `template-catalogue.md`. Produced by running design-craft and
ux-craft over each family, fitting every layout to the fixed 1280×720 frame.

**Every number in this file is in 1280×720 units.** Multiply by 1.5 for a 1920×1080 HTML deck —
this frame targets the JSON canvas, and the rest of the skill authors larger, so a `96` here is the
`143` that `investor-relations.md` calls the AGM floor. They are the same rule in two unit systems.

**Read this file by template id, never whole.** It is ~1,844 lines, so a full read costs about 30k
tokens to obtain a 9-line block — which is the over-reading `diolog-templates.md` measures and
forbids, and a rule that expensive to follow is a rule that gets skipped. Instead:

```bash
grep -n -A9 '^### kpi-row-3up' references/layout-specs.md
```

then `Read` with `offset`/`limit` if the block runs longer than the grep window. This is why the file
stays alphabetical and in one piece: a grep-by-id lookup works here and would not across 27 family
files, and splitting it would reinvent the discovery sweep the skill forbids.

Read the block for a template before you author with it. `zones` is the geometry intent, not a
binding coordinate set — a template expands server-side, and a hand-authored slide following the
same zones will sit correctly beside a templated one.

Colour is expressed as a **role** (`accent`, `neutral`, `muted`, `ground`) because templates carry
no colour and no font; the theme resolves those.

**`caps` overrides the catalogue.** Where a block says the stated `max N` is wrong, the block is
right — it was measured against the frame. The catalogue's caps were mostly authored from intent.

---

### cover-title
- **zones** — `title x80 y280 w960 h128 · subtitle x80 y424 w800 h56 · date x80 y600 w480 h24 · accent rule x80 y240 w96 h4 · base band y656–720 held clear`
- **focal** — the title. Scale (72 against a 24 subtitle) + spacing (128px of dedicated block with 112px of clear ground above it) + position (sits on the upper-third optical anchor, not the vertical centre — a mathematically centred title reads as a default).
- **type** — `title: display (72) · subtitle: body (24) · date: caption (18)`
- **accent** — the 96×4 rule above the title. Nothing else on the slide takes colour, including the title itself.
- **ux** — names the deck and dates it so the room knows what it is watching before the presenter says a word.
- **avoid** — reusing it mid-deck as a divider; it has no numbering and no ground change, so it reads as a restart rather than a section break. Also don't let the subtitle paraphrase the title — one of the two is then filler.
- **caps** — no list slots, so no `max` applies. The real ceiling is the title at ~48 characters (two lines at 72px across 960); past that the renderer's fit check forces a third line and the 240 rule collides with it.

### cover-image-bleed
- **zones** — `image full-bleed x0 y0 w1280 h720 · scrim x0 y360 w1280 h360 (ground→transparent, bottom-anchored) · title x80 y456 w896 h112 · subtitle x80 y584 w768 h48 · base band y656–720 held clear`
- **focal** — the title. Scale (64) + colour contrast against the scrim (the only high-contrast pairing on the slide) + position (bottom-left, deliberately placed over the photograph's quietest quadrant).
- **type** — `title: display (64) · subtitle: body (24)`
- **accent** — none. The photograph is already the colour event; an accent laid over it competes with the asset you chose the template for.
- **ux** — opens on real evidence — a site, a plant, a product in use — so the first impression is the company's physical reality rather than its typography.
- **avoid** — a photograph with detail or high contrast in the lower-left band. If the image has no quiet quadrant, the scrim has to get heavy enough to destroy the photo — use cover-title instead.
- **caps** — no list slots. Practical ceiling: title ≤ ~40 characters (two lines at 64px across 896), because a third line pushes into the 656 base band.

### cover-logo-band
- **zones** — `title x80 y264 w960 h112 · date x80 y400 w640 h24 · hairline x80 y552 w1120 h1 · logo.1 x80 y592 h64 (max-w 320) · logo.2 x440 y592 h64 (max-w 320) · base band y672–720 held clear`
- **focal** — the title. Scale (64 against 64-tall logo marks that sit at ~24px optical cap-height) + position (upper block, alone) + the hairline, which explicitly demotes everything below it to a footer band. Co-branding is a fact to state, not the slide's subject.
- **type** — `title: display (64) · date: caption (18)`
- **accent** — none. Two marks already introduce two brand colours; a third is noise and will clash with at least one of them.
- **ux** — declares a joint venture or co-presented deck and gives both parties their mark without ranking one above the other.
- **avoid** — matching the two logos by bounding box. Match them optically on cap-height or x-height instead, or a wordmark next to a monogram renders at twice the apparent size and looks like a hierarchy nobody agreed to.
- **caps** — no `max` stated; two logos is the structural ceiling for the 320-wide slots at 32px gutters. A third partner needs a dedicated partner-strip layout, not a squeeze.

### cover-statement
- **zones** — `statement x120 y200 w1040 h320 · attribution x120 y560 w640 h24 · base band y656–720 held clear`
- **focal** — the statement. Scale (56 against an 18 attribution) + measure (held to ~45 characters per line, three lines maximum) + spacing (320px of dedicated block, nothing above it at all).
- **type** — `statement: display (56) · attribution: caption (18)`
- **accent** — one word or clause inside the statement, set in the accent colour. Never the whole line — that is a colour choice, not emphasis.
- **ux** — opens a thesis-led investor day with the argument itself, so the room is oriented to a claim rather than to a company name they already know.
- **avoid** — a statement past ~140 characters. The renderer drops it below 40px to fit and the slide silently becomes a paragraph, which is the one thing this template exists not to be.
- **caps** — no list slots. The ~140-character ceiling is the real cap and should be stated in the catalogue row, because the fit check passes long text at a size that defeats the template.

### section-numbered
- **zones** — `number x80 y216 w240 h200 · hairline x80 y456 w1120 h2 · title x80 y496 w1040 h72 · base band y656–720 held clear`
- **focal** — deliberate promotion: the **number**, not the title. Scale (160 against 44), weight, and its own 240-wide column with 856px of empty ground beside it. The number is the navigational fact the audience needs ("we are in part three"); the title is merely its label.
- **type** — `number: display (160) · title: title (44)`
- **accent** — the number. The rule and the title stay neutral.
- **ux** — resets attention between sections and tells the room how far through the deck they are, which is the single cheapest way to stop people wondering how long this will take.
- **avoid** — using it every three or four slides. A divider that appears constantly stops dividing anything and just adds slides.
- **caps** — no list slots. One live risk: `number` is a `text` slot rendered at 160px with ≤14 characters, which may trip the deck-level "headline figure authored as text must be a stat" floor. If the gate flags it, the fix is to make it read as an ordinal (`Part 03`) rather than converting a section marker into a stat.

### section-image
- **zones** — `image full-bleed x0 y0 w1280 h720 · ground panel x0 y400 w1280 h320 (or left panel x0 y0 w512 h720) · title x80 y488 w800 h96 · base band y656–720 held clear`
- **focal** — the image. Area (the full frame) + position (it is the ground, not an element on the ground). The title is promoted to a clear second by giving it the only opaque panel on the slide — enclosure, not scale, is what wins it.
- **type** — `title: display (56)`
- **accent** — none. A section break is a pause, not an argument; there is nothing here to point at.
- **ux** — hands the section break to a real image when the visual carries more meaning than a section number would.
- **avoid** — reusing the same photograph across two dividers. Repeated imagery makes the deck feel short of assets, which reads as short of substance.
- **caps** — no list slots. Title ≤ ~30 characters (one line at 56px in the panel); a wrapping section title undercuts the whole point of a break.

### agenda-list
- **zones** — `title x80 y64 w1120 h64 · index numerals x80 w48 · item text x144 w800 · rows from y176, pitch 56, 8 rows to y624 · base band y656–720 held clear`
- **focal** — the title. Eight identical rows carry more visual mass than any one of them, so the title wins on scale (44 against 24) + spacing (the 48px clear band below it, which no row gets) + weight. Every row is held identical on purpose so the list reads as one object rather than eight competitors.
- **type** — `title: title (44) · items: body (24) · index numerals: label (20)`
- **accent** — none. An agenda has no argument to point at. The one exception: if the deck marks the live section as it progresses, that marker is the slide's single accent and nothing else takes colour.
- **ux** — sets expectations for the next thirty minutes so the audience stops silently budgeting their attention and starts spending it.
- **avoid** — sub-bullets under an agenda item. That is a contents page, and it tells the room the deck is long before you have earned the patience.
- **caps** — `max 8` is right but only just, and only for single-line items: 8 rows × 56 pitch = 448 in the 448px band from y176 to y624. Any item that wraps to two lines needs pitch 88 and the real cap drops to 5. Recommend the catalogue read `max 8 (one line each; max 5 if any item wraps)`.

### statement-hero
- **zones** — `statement x120 y176 w1040 h368, optically centred within the block · base band y656–720 held clear · no other zone exists`
- **focal** — the statement, uncontested. Scale (72) + total isolation (no title, no footer, no second element of any kind) + measure held to ~40 characters per line so the eye reads it as a shape rather than scanning it.
- **type** — `statement: display (72), line-height 1.1`
- **accent** — one clause inside the sentence. The template's whole mechanism is that nothing else is present, so a second accent has nowhere to hide.
- **ux** — gives one idea the room's full attention for the ten seconds a presenter needs to land it, with no competing surface to look at.
- **avoid** — more than ~120 characters, and more than two of these in a deck. The effect is entirely scarcity-based: the third one is just a big font.
- **caps** — no list slots. The ~120-character ceiling should be stated, because a 200-character statement passes the fit check at 48px and quietly becomes statement-support without the supporting structure.

### statement-support
- **zones** — `statement x80 y136 w960 h192 · hairline x80 y376 w1120 h1 · support columns x80/x464/x848 w352 gap 32, y416 h160 · base band y656–720 held clear`
- **focal** — the statement. Scale (56 against 24) + position (above the rule, which acts as a hard hierarchy boundary rather than decoration) + spacing (192px block, 80px of clear ground beneath it before the rule).
- **type** — `statement: display (56) · support items: body (24)`
- **accent** — one clause inside the statement. The three support columns stay neutral; colouring them would make three peers argue with the claim they exist to serve.
- **ux** — states a claim and immediately gives the audience the two or three legs it stands on, so the claim survives the first sceptical question.
- **avoid** — support lines that restate the statement in other words. Each one must add a fact the statement does not contain, or it is filler with a column around it.
- **caps** — `max 3` is right and matches the geometry exactly: three 352-wide columns fill 1120 at a 32 gutter. A fourth drops each column to 256 and the support text wraps to five lines in a 160-tall box.

### lead-bullets
- **zones** — `title x80 y64 w1120 h64 · lead x80 y152 w896 h48 · bullets x80 y240 w960, pitch 64, 6 rows to y624 · base band y656–720 held clear`
- **focal** — the title. Scale (44 against 24) + spacing (the 48px band under it that no bullet gets) + position (full-width, above a left-indented list that is visibly subordinate).
- **type** — `title: title (44) · lead: body (26) · bullets: body (24) · bullet markers: body (24), muted`
- **accent** — none by default. If exactly one bullet is the point, that bullet's marker takes the accent and nothing else does — but then question whether the other five earn their place at all.
- **ux** — the workhorse content slide: a claim, one framing line, then the evidence in scannable order.
- **avoid** — using it for everything. Four of these consecutively and the deck has become a document being read aloud. Also never put a headline figure in a bullet — a figure at body size is invisible, and the deck-level floor will flag it as a stat authored as text.
- **caps** — `max 6` holds only at one line per bullet (6 × 64 = 384, filling the y240–y624 band exactly). Two-line bullets need pitch 96 and the real cap is 4. Recommend `max 6 (max 4 if any bullet wraps)`.

### two-column-text
- **zones** — `title x80 y64 w1120 h64 · divider x640 y176 w1 h432 · left.heading x80 y176 w512 h40 · left.body x80 y232 w512 h376 · right.heading x688 y176 w512 h40 · right.body x688 y232 w512 h376 · base band y656–720 held clear`
- **focal** — the two columns are co-equal by design, so the **title** is promoted. Scale (44 against 28 headings) + position (the only element crossing the divider, spanning the full 1120). If the title cannot carry the argument on its own, this is the wrong template — the layout has deliberately given up the ability to prefer one side.
- **type** — `title: title (44) · column headings: heading (28) · column bodies: body (24)`
- **accent** — none. Colouring one column tells the room which side wins, which is exactly what a balanced comparison must not do. If one side does win, use problem-solution or before-after.
- **ux** — sets two themes or two options side by side so the audience compares on their own terms rather than being led.
- **avoid** — unequal copy lengths. A 380-character left against a 60-character right reads as an unfinished slide, not as a considered asymmetry.
- **caps** — no `max`; the fit ceiling is ~400 characters per body (36 chars/line × 11 lines at 24px in a 512×376 box). Past that, split the slide.

### three-point
- **zones** — `title x80 y64 w1120 h64 · columns x80/x464/x848 w352 gap 32 · point headings y200 h64 · point bodies y280 h280 to y560 · base band y656–720 held clear`
- **focal** — the title. Scale (44 against 28) + spacing (48px clear band below it) + the shared column rhythm, which demotes each point to a peer by construction. Three identical columns cannot contain a focal point; the argument has to live in the title.
- **type** — `title: title (44) · point headings: heading (28) · point bodies: body (20)`
- **accent** — none. One shared device repeated three times is decoration, not emphasis. If one pillar genuinely is the argument, promote it with weight and give the accent to that heading alone.
- **ux** — the strategy-pillars slide: three reasons to believe, given equal standing so the audience does not assume a ranking you did not intend.
- **avoid** — ragged column bottoms. Bodies of wildly different length read as broken rather than varied; trim to within a line of each other.
- **caps** — three is structural, not a `max`. A fourth column drops each to 256 wide, at which point 28px headings wrap and the columns stop aligning. If you have four points, they are a kpi-grid-2x2 or two slides.

### quote-pull
- **zones** — `decorative quotation glyph x80 y136 (behind, muted) · quote x120 y176 w1040 h288 · attribution x120 y512 w640 h48 · base band y656–720 held clear`
- **focal** — the quote. Scale (48 against a 20 attribution) + isolation (nothing else on the slide but its own attribution) + measure (~50 characters per line, four lines maximum).
- **type** — `quote: display (48), line-height 1.25 · attribution: label (20)`
- **accent** — the decorative quotation glyph, at a muted tint, sitting behind the text. That is the slide's one colour event; the quote itself stays in the neutral text role.
- **ux** — lets a third party — a CEO, an analyst, a customer — make the claim, which lands differently from the company making it about itself.
- **avoid** — quoting the person standing in the room presenting. It converts a credibility device into a self-citation, which is worse than saying the same thing in plain body copy.
- **caps** — no list slots. Quote ≤ ~200 characters (four lines at 48px across 1040); longer and the renderer drops it toward 36px, where it stops reading as a quotation and starts reading as a paragraph in quotes.

### quote-portrait
- **zones** — `image x0 y0 w448 h720 full-bleed left · quote x528 y176 w672 h288 · attribution x528 y512 w512 h48 · base band y656–720 held clear`
- **focal** — deliberate promotion: the **quote**, not the face. A 448×720 portrait wins on area by default, so the quote is promoted on scale (40 against the portrait's silent presence), weight, and the whole right field with 176px of top clearance. Crop the portrait so the subject's eyeline points into the text — gaze direction is a hierarchy vector the layout gets for free.
- **type** — `quote: display (40) · attribution: label (20)`
- **accent** — none. A face is already the most salient object a human can be shown; adding an accent creates a third competitor on a two-element slide.
- **ux** — attributes a claim to a specific human when the credibility rides on exactly who said it.
- **avoid** — a low-resolution, badly-lit, or stock-looking portrait. It converts a credibility play into a trust cost, and the audience registers it faster than they read the quote.
- **caps** — no list slots. Quote ≤ ~160 characters (five lines at 40px across 672). This is a shorter ceiling than quote-pull, because the portrait takes 35% of the width.

### problem-solution
- **zones** — `title x80 y64 w1120 h64 · problem panel x80 y176 w544 h432 · solution panel x656 y176 w544 h432 · panel headings y208 h40 · panel bodies y264 h304 · base band y656–720 held clear`
- **focal** — deliberate promotion: the **solution** panel. Colour (it holds the slide's only accent) + ground contrast (the problem sits on the flat slide ground, the solution on a tinted panel) + heading weight. Left-to-right reading order already hands the problem first position; the promotion stops it also winning attention.
- **type** — `title: title (44) · panel headings: heading (28) · panel bodies: body (24)`
- **accent** — the solution heading, or its panel ground at a low tint — one or the other, never both.
- **ux** — frames a strategic response so the action reads as a consequence of a diagnosed problem, not as an initiative that appeared from nowhere.
- **avoid** — writing the problem more vividly than the solution, which is the default failure and leaves the room remembering the problem. And do not use it when the problem is not actually resolved — a solution stated in future tense on this layout reads as a promise the deck has already claimed to have kept.
- **caps** — no `max`; each body fits ~460 characters at 24px in a 544×304 box, but stay under ~380 or the panels stop scanning. Past that, the pair is two slides.

### before-after
- **zones** — `title x80 y64 w1120 h64 · before panel x80 y176 w512 h400 · connector band x592 y176 w96 h400 · after panel x688 y176 w512 h400 · state headings y208 h48 · bodies y272 h280 · base band y656–720 held clear`
- **focal** — the **after** state. Colour (the only accent on the slide) + weight (its heading runs one step heavier than the before heading) + ground contrast on the panel. The before panel is deliberately muted; a transformation slide where both states look equally alive has not stated a direction.
- **type** — `title: title (44) · state headings: heading (32) · bodies: body (24)`
- **accent** — the after heading. The connector between panels stays neutral — an accented arrow spends the accent on a piece of punctuation.
- **ux** — states a turnaround as two readable states rather than as a narrative the audience has to assemble from prose.
- **avoid** — using it when the two states are not period-bounded. Without a stated period on each panel the "before" is unfalsifiable, and a sceptical investor will read it as selective framing rather than progress.
- **caps** — no `max`. Both bodies are optional: with both omitted, headings step up to 40 and the panels shrink to h200 at y264, which is the stronger version of this slide. Two-line headings need the h400 panels back.

### kpi-hero
- **zones** — `title x80 y96 w1120 h48 (optional) · kpi.1 value x80 y216 w1120 h240 · kpi.1 label x80 y480 w1120 h40 · footnote x80 y632 w1120 h24 · base band y656–720`
- **focal** — the value. Scale (120 against a 24 label) + weight + colour + 240px of dedicated block with nothing beside it. Four vectors, because this template's entire proposition is that one number gets everything.
- **type** — `title: heading (28) · kpi.value: display (120, renderer-derived) · kpi.label: body (24) · footnote: caption (18)`
- **accent** — the value.
- **ux** — makes one number the whole message when the number is genuinely the news, and forces the presenter to say the one sentence around it.
- **avoid** — a value that needs its caveat to be true. The footnote renders at 18px and is unreadable from the back of a room, so anything load-bearing in it is effectively not on the slide.
- **caps** — the `≤14 characters` stat contract is correct here and this is the only KPI template where the full 14 is safe: the renderer's own arithmetic gives `min(120, 240×0.72, (1120/(14×0.62))×0.94) = 120`, so even a 14-character figure renders at the full display step.

### kpi-row-2up
- **zones** — `title x80 y64 w1120 h64 · columns x80/x656 w544 gap 32 · value y240 h144 · label y400 h48 · optional column hairline x624 y240 h208 · footnote x80 y632 w1120 h24 · base band y656–720`
- **focal** — a pair is co-equal by geometry, so the **title** carries the argument: scale (44 against 24 labels) + full-width position + the 112px clear band before the values. If one of the two figures is genuinely the headline, promote that one with the accent and leave the other neutral — but then say so, because an accented pair has no focal point at all.
- **type** — `title: title (44) · kpi.value: display (96, renderer-derived) · kpi.label: body (24) · footnote: caption (18)`
- **accent** — one of the two values, or none. Never both.
- **ux** — puts two headline figures side by side when the pair is the story — revenue and margin, volume and price — so the relationship is visible without a sentence.
- **avoid** — two figures with no relationship to each other. That is two slides wearing one title, and the audience will spend the slide looking for the link.
- **caps** — `≤14 chars` is contractual but misleading at this width. A 544-wide box renders 8 characters at ~96px and 14 characters at ~59px — smaller than the 44px title beside it. Cap 2-up figures at **8 characters** and the stated max becomes honest.

### kpi-row-3up
- **zones** — `title x80 y64 w1120 h64 · columns x80/x464/x848 w352 gap 32 · value y248 h128 · label y392 h48 · footnote x80 y632 w1120 h24 · base band y656–720`
- **focal** — the value row read as one object. It beats the title on scale (88 against 44) + weight + the 120px clear band above it; the title is a clear second. If one figure is the news, it takes the accent and becomes the focal point on its own, with the other two neutral.
- **type** — `title: title (44) · kpi.value: display (88, renderer-derived) · kpi.label: body (24) · footnote: caption (18)`
- **accent** — one value, or none.
- **ux** — the standard results row: the three numbers the market will quote back at you tomorrow.
- **avoid** — padding to three when only two figures are real. `kpi.3` is optional precisely so the layout closes up to a two-column row; inventing a third metric to fill the gap is the most common honesty failure on a results deck.
- **caps** — three is right for the geometry, but the figure length is not: 352-wide holds ~6 characters at 88px (`$48.2m`, `+12.4%`), and 14 characters self-shrinks to ~38px, below the title. Cap 3-up figures at **6–7 characters**.

### kpi-row-4up
- **zones** — `title x80 y64 w1120 h64 · columns x80/x368/x656/x944 w256 gap 32 · value y256 h112 · label y384 h64 (two lines) · footnote x80 y632 w1120 h24 · base band y656–720`
- **focal** — the four-value band, held rigorously identical, with the **title** carrying the claim on scale (44 against 20 labels) + the 128px clear band + full-width position. Promoting one of four at this density breaks the scan without reading as emphasis — if one figure is the point, use kpi-row-3up and drop the weakest.
- **type** — `title: title (44) · kpi.value: display (56, renderer-derived) · kpi.label: label (20) · footnote: caption (18)`
- **accent** — none. Four figures with one coloured reads as a rendering error rather than a hierarchy.
- **ux** — the dense results summary for an audience that wants the full scorecard visible at once rather than paged.
- **avoid** — using it as the deck's first metrics slide. Four figures at 56px is a reference table; the audience needs the headline before the scorecard.
- **caps** — `≤14 chars` is wrong for this geometry and should be overridden in the catalogue row. A 256-wide box renders 7 characters at ~56px, 8 at ~48px, and 14 at ~28px — smaller than the labels beside it. State **≤7 characters** for 4-up.

### kpi-grid-2x2
- **zones** — `title x80 y64 w1120 h64 · cells x80/x656 w544 · rows y176 h192 and y400 h192 · value at cell top h128 · label beneath h48 · base band y592–720 held clear (no footnote slot)`
- **focal** — the top-left cell. Position (reading-order first in a symmetric grid) + colour (it holds the only accent). Those are the only two vectors available, because all four cells are geometrically identical by design.
- **type** — `title: title (44) · kpi.value: display (88, renderer-derived) · kpi.label: body (24)`
- **accent** — the top-left value.
- **ux** — four metrics whose labels are too long for a row — "Underlying EBITDA margin" simply will not fit a 256-wide 4-up column.
- **avoid** — reaching for it as "4-up with better spacing". The grid exists for label length; if the labels are short, a row scans faster and this layout wastes 128px of vertical ground.
- **caps** — four is right and the 544-wide cells hold a 9-character figure at 88px, which is the most generous of the KPI grids. The real gap is the missing `footnote:text?` slot: any figure needing a caveat has nowhere to put it here, so either add the slot or route the slide to kpi-row-4up.

### kpi-grid-2x3
- **zones** — `title x80 y64 w1120 h64 · columns x80/x464/x848 w352 gap 32 · rows y176 h192 and y400 h192 · value h120 · label h56 · base band y592–720 held clear`
- **focal** — the title, by necessity. Six identical cells cannot contain a focal point, so the title takes scale (44 against 20) + the 48px clear band + full-width position against the gridded field beneath it.
- **type** — `title: title (44) · kpi.value: display (64, renderer-derived) · kpi.label: label (20)`
- **accent** — none. Six cells with one coloured is a lottery ticket rather than a hierarchy — nobody can tell why that one won.
- **ux** — the divisional or quarterly scorecard: everything on one page for a management audience that already knows what each metric means.
- **avoid** — showing it to an audience hearing these numbers for the first time. Six figures at 64px is a handout, and a presenter reading it aloud will lose the room by the fourth.
- **caps** — six is the correct geometric ceiling and a seventh does not fit at any legible size. Figures cap at **8 characters** at 64px in a 352-wide cell. A seventh metric means kpi-table-compact.

### kpi-delta-row
- **zones** — `title x80 y64 w1120 h64 · periods x80 y136 w1120 h32 · columns x80/x464/x848 w352 gap 32 · value y248 h120 · delta chip y384 h40 · label y440 h48 · footnote x80 y632 w1120 h24 · base band y656–720`
- **focal** — deliberate promotion: the **delta**, not the value. This is the one KPI template where the movement is the message, so the delta wins on colour + shape (an enclosed chip, the only enclosed object on the slide) + a directional glyph, while the value keeps scale but stays neutral.
- **type** — `title: title (44) · periods: label (20) · kpi.value: display (80, renderer-derived) · delta: heading (28) · kpi.label: body (24) · footnote: caption (18)`
- **accent** — the single delta that carries the argument. The other two chips use the glyph and a neutral tint. Colouring all three spends the accent three times and it stops meaning anything. Encode direction with `▲`/`▼` and the sign as well as tint, never colour alone.
- **ux** — shows period-on-period movement so the audience reads direction and magnitude of change, not just level.
- **avoid** — colouring a delta green because it is positive when the metric being up is bad (cost, gearing, days sales outstanding). Direction and desirability are different axes, and the projector will flatten your careful red/green anyway.
- **caps** — three is right. 352-wide caps the figure at ~6 characters at 80px, and the delta string must also stay ≤6 (`+12.4%`). A 4-up delta row does not fit — below 256 wide the chip and the label collide.

### kpi-sparkline
- **zones** — `title x80 y64 w1120 h64 · columns x80/x464/x848 w352 gap 32 · value y216 h112 · sparkline y344 w352 h72 · label y440 h48 · footnote x80 y632 w1120 h24 · base band y656–720`
- **focal** — the value row. Scale (88 against a 72-tall sparkline with no axis and no labels) + weight. The sparklines are deliberately subordinate — single stroke, no gridlines, no axis — because they qualify the figure rather than compete with it.
- **type** — `title: title (44) · kpi.value: display (88, renderer-derived) · kpi.label: body (24) · footnote: caption (18)`
- **accent** — none on the figures. All three sparks share one neutral stroke; if a single trend is the point, that one spark takes the accent and the other two go muted.
- **ux** — answers "and which way is it going?" without spending a whole chart slide on a question that takes 72px to settle.
- **avoid** — a sparkline with fewer than ~6 points, which reads as a zigzag rather than a trend, and any sparkline on a truncated axis — an unlabelled micro-chart with a hidden zero is the easiest place in a deck to mislead by accident.
- **caps** — three columns, figures ≤6 characters at 88px. The spark slots are individually optional, but two sparks across three figures reads as missing data rather than as an editorial choice — supply all three or none.

### kpi-chart-right
- **zones** — `title x80 y64 w1120 h64 · KPI stack x80 y176 w384, three rows at pitch 144 (value h88, label h40) · divider x512 y176 w1 h432 · chart x576 y176 w624 h400 · source x576 y600 w624 h24 · base band y656–720`
- **focal** — deliberate promotion: the **KPI stack**, not the chart. The chart wins on area (624×400), so the figures are promoted on scale (72 against 18px axis labels) + weight + left-column reading position. The chart is the evidence; the figures are the claim, and the claim goes first.
- **type** — `title: title (44) · kpi.value: display (72, renderer-derived) · kpi.label: label (20) · chart axis: label (18) · source: caption (18)`
- **accent** — the chart's single primary series. The figures stay neutral, so the accent is doing one job: telling you which line produced them.
- **ux** — pairs the numbers the audience will quote with the trend that produced them, so the figure and its trajectory are read in one movement instead of across two slides.
- **avoid** — more than two series in the 624-wide plot. At that width a legend eats the plot area and the chart stops being readable at distance, which defeats the pairing.
- **caps** — three KPIs is the correct ceiling for a 432-tall stack at 144 pitch; figures cap at **8 characters** at 72px in a 384-wide box. `kpi.3` being optional is right — two figures on this layout reads fine.

### kpi-progress
- **zones** — `title x80 y64 w1120 h64 · rows at y176/y320/y464, pitch 144 · per row: label x80 w288 h32 · track x400 (row y+24) w528 h16 with fill and target tick · value x960 w240 h56 right-aligned · footnote x80 y632 w1120 h24 · base band y656–720`
- **focal** — the value column. Scale (56 against 24 labels) + weight + alignment (a right-aligned numeric column reads as one scannable stack rather than three separate numbers). The tracks carry the comparison but stay muted.
- **type** — `title: title (44) · row label: body (24) · kpi.value: heading (56) · target caption: caption (18) · footnote: caption (18)`
- **accent** — the single metric that is materially ahead of or behind guidance. Fills and target ticks on the other rows stay neutral; colouring all three fills spends the accent three times.
- **ux** — tracks delivery against stated guidance so the audience can see the gap for themselves instead of being told there isn't one.
- **avoid** — a track with no visible target marker. A progress bar without a target is a bar chart pretending to be accountability, and it is the fastest way to lose an analyst's trust on an otherwise honest slide.
- **caps** — three rows at 144 pitch fills the y176–y608 band; a fourth needs pitch 108 and drops the value below 44px. The catalogue's `kpi.1!` + two optionals is correct — cap at 3 and do not extend it.

### kpi-table-compact
- **zones** — `title x80 y64 w1120 h64 · header row x80 y176 w1120 h40 · rule under header at y216 · body rows from y224 at pitch 48, 8 rows to y608 · footnote x80 y632 w1120 h24 · base band y656–720`
- **focal** — the title. A table has no single cell worth promoting, so the title takes scale (44 against 24) + the 48px clear band + full-width position. Inside the table, the value column is right-aligned with tabular figures and one weight step up, so it reads as a column rather than as eight loose numbers.
- **type** — `title: title (44) · header: label (18), caps, tracked +0.06em · row label: body (24) · row value: body (24), tabular, right-aligned · footnote: caption (18)`
- **accent** — the header rule, or one highlighted row. Never both, and never a coloured column — a coloured column says "read this one" about a template whose job is to show all of them.
- **ux** — carries more metrics than a grid holds without shrinking type below the legibility floor, which is the honest alternative to cramming a 2x3 grid.
- **avoid** — reaching for it because the numbers feel boring. A table put in front of an audience seeing the figures for the first time is a handout being projected; if it matters, pull the two figures that matter onto a kpi-row-2up.
- **caps** — no `max` is stated and this is exactly the template the frame check catches: 8 body rows at pitch 48 ends at y608, and a 9th row runs into the footnote band and off the 720 frame. **Add `max 8` to the catalogue row** (7 if the footnote wraps to two lines).

### chart-bleed
- **zones** — `title x80 y56 w1120 h48 (optional) · plot x64 y136 w1152 h456 · axis labels inside the plot band · source x64 y632 w1152 h24 · base band y656–720`
- **focal** — the plot. Area (1152×456, ~70% of the frame) + isolation (nothing competes with it) + the single accent on the primary series.
- **type** — `title: heading (32) · direct series labels: label (20) · axis labels: label (18) · source: caption (18)`
- **accent** — the primary series. Every other series drops to neutral tints.
- **ux** — hands the whole slide to one chart when the *shape* of the data is itself the argument and a sentence would only paraphrase it.
- **avoid** — using it with the title omitted when the shape is not self-evident. A bleed chart with no stated point makes the audience do the interpretive work, and they will each reach a different conclusion — if they need help, use chart-takeaway.
- **caps** — no list slots. Cap at 4 series and label them directly at the line ends; a legend costs 40px of plot height and forces a colour-matching task on a projected slide.

### chart-takeaway
- **zones** — `title x80 y56 w1120 h48 · takeaway x80 y120 w1120 h72 · hairline x80 y216 w1120 h1 · plot x80 y248 w1120 h352 · source x80 y632 w1120 h24 · base band y656–720`
- **focal** — deliberate promotion: the **takeaway**, not the chart. The chart wins on area, so the takeaway is promoted on scale (36 against 18px axis labels) + weight + position above the dividing rule, while the title is demoted to a tracked-caps eyebrow. The chart is the proof; the sentence is the point, and the point goes first.
- **type** — `title: label (20), caps, tracked +0.08em · takeaway: display (36) · axis labels: label (18) · source: caption (18)`
- **accent** — the series or segment the takeaway actually names. Nothing else.
- **ux** — states the "so what" so the audience does not have to derive it — the single highest-value move available on any data slide, and the one most decks skip.
- **avoid** — a takeaway that describes the chart ("revenue rose in every quarter") instead of interpreting it ("growth is now coming from services, not volume"). A description is redundant with the picture; an interpretation is the reason the slide exists.
- **caps** — no list slots. Takeaway ≤ ~110 characters (two lines at 36px across 1120). A three-line takeaway is a paragraph, and it steals the 32px gap the rule needs to read as a boundary.

### chart-callouts
- **zones** — `title x80 y64 w1120 h64 · plot x80 y176 w800 h424 · callout rail x912 y176 w288, three blocks h112 at gap 40 · leader lines from rail to the marked points · source x80 y632 w1120 h24 · base band y656–720`
- **focal** — the primary marked point on the plot: a filled marker plus its leader line. Colour + shape (the only filled marker against neutral rings) — the callout text is that point's label, not the focal element.
- **type** — `title: title (44) · callout headings: label (20) · callout bodies: body (18) · axis labels: label (18) · source: caption (18)`
- **accent** — one marked point and its matching callout heading. The other two markers are neutral rings; three accented markers is decoration and the eye picks one at random.
- **ux** — points at the specific moments in a series that need explaining — an inflection, an acquisition, a one-off — so the presenter is not narrating coordinates.
- **avoid** — callouts that restate the axis ("Q3 2025", "the peak"). A callout earns its 288-wide block only by explaining a *cause* the chart cannot show.
- **caps** — `max 3` is right: three 112-tall blocks at 40px gaps total 416 in the 424-tall rail. A fourth forces bodies below 18px, which breaks the legibility floor rather than merely looking tight.

### chart-bar-v
- **zones** — `title x80 y64 w1120 h64 · plot x80 y176 w1120 h400 · category labels y584 h32 (single line, horizontal) · source x80 y632 w1120 h24 · base band y656–720`
- **focal** — one bar — the tallest, or the one the title is about. Bar height is set by the data, so the hierarchy has to come from colour + a direct value label placed above that bar and no other.
- **type** — `title: title (44) · value label on the accented bar: label (20) · category labels: label (18) · source: caption (18)`
- **accent** — the single bar the title names. All others neutral.
- **ux** — compares magnitudes across a small set of categories where the ranking, not the trend, is the message.
- **avoid** — a truncated value axis. On a comparison chart that is a defect rather than a style choice — the bar heights are the entire encoding, and clipping the baseline manufactures a difference that is not in the data.
- **caps** — no list slots. ~8 bars at 1120 wide (96 bar, 48 gap) before category labels start to collide at 18px. Past 8, or with any label needing rotation, switch to chart-bar-h.

### chart-bar-h
- **zones** — `title x80 y64 w1120 h64 · category labels x80 w320, right-aligned to the bar origin · bar field x424 y176 w776 h424, row pitch 48, up to 8 rows · value labels at the bar end · source x80 y632 w1120 h24 · base band y656–720`
- **focal** — the top bar. Position (a descending ranking puts first place first, which is the strongest position on the slide) + colour. Always sort descending: an unsorted ranking has no focal point at all and the audience reads it as a list.
- **type** — `title: title (44) · category labels: body (24) · value labels: label (20) · source: caption (18)`
- **accent** — the bar the slide is about — usually the company's own, which is often not the top one. That is the honest use of this template.
- **ux** — ranks a peer set or a category list where the labels are words rather than dates, so long names read straight without rotation.
- **avoid** — leaving it unsorted, and hiding your own bar in a neutral tint when the whole point is where you sit in the ranking. Both read as evasion to an audience that came to find exactly that bar.
- **caps** — no list slots. 8 rows at pitch 48 sits comfortably in the 424 band; 12 rows at pitch 32 with 18px labels is the hard ceiling before the bars become hairlines.

### chart-line
- **zones** — `title x80 y64 w1120 h64 · plot x80 y176 w1120 h400 · direct series labels at each line's right terminus, inside the plot · x-axis y584 h24 · source x80 y632 w1120 h24 · base band y656–720`
- **focal** — the primary series. Colour + stroke weight (2px against 1px neutrals) + a direct end-label at its terminus. Three vectors before the data does any work, which is what keeps the slide readable when the primary line is not the highest one.
- **type** — `title: title (44) · series end-labels: label (20) · axis labels: label (18) · source: caption (18)`
- **accent** — the primary series stroke and its end-label.
- **ux** — shows a quantity moving through time — share price, output, headcount — where direction matters more than any individual level.
- **avoid** — more than four series, and any legend where direct end-labels fit. A legend converts reading into a colour-matching task performed at distance, which is where projected decks lose their audience.
- **caps** — no list slots. Four series maximum at 1120 wide; a fifth means charts-2up or small multiples, not a thinner stroke.

### chart-area
- **zones** — `title x80 y64 w1120 h64 · plot x80 y176 w1120 h400 · band labels set inside the thickest part of each band · x-axis y584 h24 · source x80 y632 w1120 h24 · base band y656–720`
- **focal** — the band that is growing or shrinking. Colour (the accent, against neutral tints for every other band) + weight on its in-band label.
- **type** — `title: title (44) · band labels: label (20) · axis labels: label (18) · source: caption (18)`
- **accent** — the one band the title names.
- **ux** — shows composition changing over time — mix shift, segment contribution — where the whole matters as much as any part.
- **avoid** — stacking more than 5 bands, and mixing percentages with absolutes on one plot. If the audience needs to read individual values rather than see the shift, this is a chart-line or a table.
- **caps** — no list slots. 5 bands is the ceiling: below that thickness an in-band label will not fit, and once you fall back to a legend the template has lost the advantage it had over chart-line.

### chart-waterfall
- **zones** — `title x80 y64 w1120 h64 · plot x80 y176 w1120 h368 · connector lines between bar tops · delta labels above or below each bar · category labels y560 h48 (two lines permitted) · source x80 y632 w1120 h24 · base band y656–720`
- **focal** — the closing bar. Position (terminal, and one of only two bars grounded on the baseline) + colour + a heavier value label. The result is the point; the steps are how you got there.
- **type** — `title: title (44) · opening and closing labels: heading (28) · delta labels: label (20) · category labels: label (18) · source: caption (18)`
- **accent** — the closing bar. Distinguish increases from decreases by **direction and sign**, not by a red/green pair — pair any tint with the `+`/`−` so the bridge survives projection gamma and colour-vision deficiency.
- **ux** — explains how a figure moved from A to B and attributes each step, which no pair of bars can do.
- **avoid** — a bridge that does not reconcile. Someone in the room will add the steps up, and a waterfall that misses its own closing figure costs more credibility than the slide was worth.
- **caps** — no list slots. Opener + 6 steps + closer = 8 bars at 1120 wide (96 bar, 48 gap). Beyond that, group the small movements into a single "other" step rather than thinning the bars.

### chart-donut
- **zones** — `title x80 y64 w1120 h64 · donut cx400 cy400, r-outer 200, r-inner 128 · centre figure inside the hole (≤6 characters) · label rail x672 y224 w528, six rows at pitch 48 · source x80 y632 w1120 h24 · base band y656–720`
- **focal** — the centre figure (the total) where one is supplied, otherwise the largest segment. Scale (56 against 20px rail labels) + enclosure (it sits inside the ring, the strongest containment cue available on a slide).
- **type** — `title: title (44) · centre figure: display (56) · centre caption: caption (18) · rail labels: body (20) · rail values: body (20), tabular, right-aligned · source: caption (18)`
- **accent** — the one segment the title names. The remaining segments step through neutral tints, ordered largest-first clockwise from twelve o'clock.
- **ux** — shows share of a total when the audience needs "how much of the whole", not "how much".
- **avoid** — putting two donuts side by side to show change. Humans compare angles badly and area worse; a change in composition is a stacked bar or chart-area. Also avoid any segment under ~5% — it becomes a sliver whose label cannot reach it.
- **caps** — six segments is right and is a hard ceiling: six 48-pitch rail rows fill the 288px band exactly, and a seventh both overruns the rail and produces a segment too thin to label. Keep `six segments at most` as stated.

### chart-combo
- **zones** — `title x80 y64 w1120 h64 · plot x80 y176 w1120 h400 · left axis (volume bars) x80 w64 · right axis (rate line) x1136 w64 · a unit caption at the top of each axis · x-axis y584 h24 · source x80 y632 w1120 h24 · base band y656–720`
- **focal** — the rate line. Colour + stroke weight against flat neutral bars + a direct end-label. The bars are context, the line is the argument — if it is the other way round, this is the wrong template and you want chart-bar-v.
- **type** — `title: title (44) · line end-label: label (20) · axis unit captions: label (18) · axis values: label (18) · source: caption (18)`
- **accent** — the line.
- **ux** — puts a volume series and a rate on one plot when the *relationship* between them is the point — units against margin, visits against conversion.
- **avoid** — a dual axis chosen to make two unrelated series appear correlated. It is the most-abused chart form in an investor deck: both axes must start at zero and both units must be captioned, or the correlation is something you manufactured with axis scaling.
- **caps** — no list slots. Exactly two series — one bar set, one line. A second line on the right axis makes the slide unreadable at distance; use charts-2up.

### charts-2up
- **zones** — title `64,48 1152×72` · chart-L `64,152 560×456` (label strip `560×32` on top, plot `560×408`) · chart-R `656,152 560×456` (same internal split) · source `64,624 1152×32`. Gutter 32, margins 64.
- **focal** — chart-L. Two equal boxes give geometry no vote, so promotion is by **colour** (chart-L carries the accented series, chart-R is entirely `neutral`/`muted`) + **weight** (chart-L label 20/600, chart-R label 20/450) + **position** (first in reading order). Promoted left because the title's claim is normally proved by one chart and *qualified* by the other; the prover goes first.
- **type** — title→40/600 · chart label→20 (L 600, R 450) · axis tick→18/450 `muted` · direct series label→18/550 · source→18/450 `muted`.
- **accent** — one series inside chart-L. Chart-R gets none.
- **ux** — Proves a single claim by showing the same fact from two angles at once, so the audience never has to hold slide N in memory while looking at slide N+1.
- **avoid** — Two unrelated charts. If the title needs the word "and", these are two slides; a 2-up with no shared claim just halves both charts' legibility.
- **caps** — No `max N` stated and none needed, but 560px of plot caps each side at ≤4 series and ≤8 categories before tick labels rotate. Add that as a note rather than a slot cap.

### charts-4up
- **zones** — title `64,48 1152×72` · 2×2 grid in `64,152 1152×456`: cells `560×212` at `(64,152) (656,152) (64,396) (656,396)`, gutters 32 · each cell = label `560×24` + plot `560×188` · source `64,624 1152×32`.
- **focal** — top-left cell. **Position** (first cell of a Z-scan) + **colour** (only this cell's series takes the accent) + **weight** (its label 20/600 against 20/450). A 188px plot cannot win on scale, so scale is deliberately not a vector here — all four plots stay identical in size, which is what makes the grid scannable.
- **type** — title→40/600 · cell label→20 · min/max endpoint label→18/450 · source→18/450 `muted`. No axis furniture below 18 means no tick ladders: label only the first and last point.
- **accent** — one series in the top-left cell.
- **ux** — A divisional scoreboard: four trends compared for *shape*, not read for *value*. The audience leaves with "three up, one down", not with numbers.
- **avoid** — Treating it as four readable charts. At 188px tall a legend, a gridline set, or a second series makes all four unreadable at once. If any single chart needs to be read, it belongs on its own slide.
- **caps** — `chart.3`/`chart.4` optional is right, but the 3-filled case must re-flow to one row of three at `368×456` rather than leaving a hole in the grid — a 2×2 with an empty quadrant reads as missing data, not as three divisions.

### chart-table
- **zones** — title `64,48 1152×72` · chart `64,152 688×456` · table `784,152 432×456` (header row 48, body rows 44) · source `64,624 1152×32`. 32 gutter between chart and table.
- **focal** — the chart. **Scale** (688 vs 432 — a 1.6× width ratio) + **position** (left) + **colour** (the only accented object on the slide is in the plot). The table is demoted on purpose: hairline rules, `muted` header, no fills.
- **type** — title→40/600 · table column header→18/550 caps tracked 0.08em `muted` · table cell→18/450, numerals tabular-lining and right-aligned · direct series label→18/550 · source→18/450 `muted`.
- **accent** — one series in the chart. Never also a table row: two accents across a chart/table pair make the audience hunt for the correspondence that isn't there.
- **ux** — Lets a sceptical reader audit the shape they were just shown, on the same slide, without a "detail in the appendix" promise nobody follows up.
- **avoid** — A table that restates every plotted point. The table earns its 432px only by carrying what the chart cannot — absolute values behind an indexed line, or the base the percentages sit on.
- **caps** — No row cap stated. 432×456 with a 48px header holds **9 body rows** geometrically at 18px/44px; set the editorial cap at **7**, and only 2 columns (label 240 + value 192) or 3 very narrow ones.

### chart-kpis
- **zones** — title `64,48 1152×72` · chart `64,152 832×456` · KPI rail `928,152 288×456` = three blocks `288×136` at y152/y312/y472, gaps 24 · each block = value `288×64` + label `288×32` under it · source `64,624 1152×32`.
- **focal** — KPI 1's value. **Scale** (44 against a 20px body — the largest thing on the slide) + **colour** (the only accent) + **spacing** (a 288px column of its own, isolated from the plot by a 32px gutter). Promoted over the chart because a stat rail exists to make the number the takeaway; if the deck's claim is a *shape* rather than a figure, invert it — accent the series, set all three KPI values `neutral`, and say so.
- **type** — title→40/600 · KPI value→44/600 (`stat` slot, not `text`) · KPI label→18/510 `muted` caps tracked 0.08em · axis tick→18/450 `muted` · source→18/450 `muted`.
- **accent** — KPI 1's value only.
- **ux** — Anchors a trend to the two or three figures it produced, so the chart and the guidance language in the CEO's script are the same object.
- **avoid** — Long stat values. In a 288px box at 44px the fit arithmetic (`len × size × 0.62 ≤ box.w`) caps the value at **10 characters**, not the contract's 14. `$1,284.6m` fits; `3,000sqm p.a.` does not and will wrap mid-figure.
- **caps** — `kpi.3` optional is right. With two filled, centre the pair vertically in the rail (blocks at y216/y376) rather than stacking from the top and leaving 160px of dead rail.

### chart-legend-panel
- **zones** — title `64,48 1152×72` · chart `64,152 800×456` · legend panel `896,152 320×456` = 6 rows `320×64`, gaps 8 (424 used, 32 top pad) · each row = swatch `16×16` + name + one note line · source `64,624 1152×32`.
- **focal** — the accented series **and its legend row read as one object**. **Colour** (the one accent, appearing in the plot and repeated in its swatch) + **weight** (that row's name at 20/600, the other five at 20/450) + **spacing** (16px extra above and below that row). The pairing is the point: the eye lands on the coloured line, then travels once to the explanation.
- **type** — title→40/600 · legend name→20 · legend note→18/450 `muted`, ≤34 chars per line at 320px · axis tick→18/450 `muted` · source→18/450 `muted`.
- **accent** — one legend row plus its series (one object, counted once). The other five swatches are steps on a `neutral`/`muted` ramp differentiated by position in the list, never by five saturated hues.
- **ux** — Buys explanation space for series whose names alone don't carry meaning — cohort labels, tranche names, scheme codes.
- **avoid** — Reaching for it when direct end-of-line labels would fit. A legend charges a recall tax on every glance; only pay it when each series needs a sentence the plot has no room for.
- **caps** — `max 6` is right. 7 rows at 64px overflow the panel; if you have 7 series the chart is already past what a 800px plot separates.

### segment-3up
- **zones** — title `64,48 1152×72` · three cells `368×456` at `(64,152) (456,152) (848,152)`, gutters 24 · each cell = label `368×32` + plot `368×400` + optional total `368×24` · source `64,624 1152×32`.
- **focal** — the leftmost segment. **Colour** (its series accented, the other two `neutral`) + **weight** (label 20/550 vs 20/450) + **position**. Ordering is load-bearing: sort segments descending by size so the promoted cell is also the largest, and the two hierarchy vectors point the same way as the data. If the title names a different division, move the accent and re-sort.
- **type** — title→40/600 · segment label→20 · segment total→20/600 (or a `stat` if it belongs on the type ramp above body) · axis tick→18/450 `muted` · source→18/450 `muted`.
- **accent** — one segment's series.
- **ux** — Splits one number three ways while keeping the three splits directly comparable, which a stacked chart makes impossible.
- **avoid** — Three cells that don't share an axis maximum, or three different chart forms. Comparison across cells is only honest when the encoding, the scale, and the y-range are identical; independently-scaled panels are the most common lie in a divisional deck.
- **caps** — Fixed 3, all required — correct. Don't force a fourth by narrowing to 276px; that's `charts-4up`.

### variance-bridge
- **zones** — title `64,48 1152×72` · bridge plot `64,152 800×400` (zero baseline at y=~400, bars 72–96 wide, connectors 1px) · notes rail `896,152 320×400` = 4 rows `320×88`, gaps 16 · source `64,624 1152×32`.
- **focal** — the closing bar. **Position** (the terminus — a bridge is read left to right and the eye stops at the last column) + **colour** (the single accent) + **scale** (it is a full-height column against the increments' partial bars).
- **type** — title→40/600 · bar value label→20/600 · category label→18/550, two lines allowed at 96px wide · note→18/450 `muted` · source→18/450 `muted`.
- **accent** — the closing bar only. Increments and decrements are separated by **position relative to the baseline plus a signed value label**, using two `neutral` steps — never a red/green pair, which a projector's gamma flattens and ~8% of men can't split.
- **ux** — Names every moving part between two numbers, so "EBITDA fell $4m" becomes an argument with four attributable causes.
- **avoid** — A truncated value axis. On a waterfall the bar heights *are* the quantities; a non-zero baseline isn't a style choice, it's a misstatement. If the movements are tiny against the base, add a broken-scale inset or change templates.
- **caps** — `notes max 4` is right for a 320×400 rail; ≤90 characters per note at 18px.

### table-simple
- **zones** — title `64,48 1152×72` · table `64,152 1152×456`: header row 48, body rows 44, full-width hairline under the header only · footnote `64,624 1152×32`.
- **focal** — the title, by default. A table with no highlight slot has no internal focal, and pretending otherwise produces a slide the eye grazes. Vectors: **scale** (40 against an 18px cell — a 2.2× step) + **spacing** (72px title band with a 32px gap to the header). The table is a supporting exhibit, and the title must therefore carry the whole claim as a sentence, not a noun phrase.
- **type** — title→40/600 · column header→18/550 caps tracked 0.08em `muted` · cell→18/450 (16 is the absolute floor; use it only to save a column, never a row) · numerals tabular-lining, right-aligned, decimals aligned · footnote→18/450 `muted`.
- **accent** — none. That is the template's contract.
- **ux** — Presents reference material the audience will look *up* rather than look *at* — fee schedules, definitions, register extracts.
- **avoid** — Using it when one row matters. The moment a row is the point, this template forces the presenter to say "third row down", which is the interface failing. Switch to `table-highlight`.
- **caps** — No cap stated; that's the gap. Geometry holds **9 body rows** at 18/44px; set the cap at **8**. Past that, split across two slides or plot it.

### table-totals
- **zones** — title `64,48 1152×72` · body table `64,152 1152×360` (header 48 + 7 rows × 44) · separator rule `64,520 1152×2` · totals band `64,528 1152×80` (1–2 rows at 48, 16px extra leading above) · footnote `64,624 1152×32`.
- **focal** — the total line. **Weight** (600 against the body's 450) + **spacing** (a 2px rule plus 16px of air that no body row gets) + **colour** (the accent). Three vectors, which is what lets the total survive a long label pushing its size down.
- **type** — title→40/600 · column header→18/550 caps tracked 0.08em `muted` · cell→18/450 · total row→20/600 · footnote→18/450 `muted`.
- **accent** — the total row's figures only — not the header band, and not the whole row's ground.
- **ux** — Makes the sum the destination of the slide, so the audience reads the components as a route to a number they already know is coming.
- **avoid** — Stacking subtotal + total + adjusted total. Three summary lines mean no focal; cap at two and accent only the last, or the slide argues with itself about which number is the answer.
- **caps** — No cap stated. With the totals band reserved, geometry holds **7 body rows**; set the cap at **6 body + 2 total**.

### table-3period
- **zones** — title `64,48 1152×72` · table `64,152 1152×456`: label column `432`, three period columns `240` each · header 48, body rows 44 · current-period column carries a `muted` ground tint running the full table height · footnote `64,624 1152×32`.
- **focal** — the current-period column. **Position** (rightmost — the terminus of a left-to-right period read) + **colour** (its header label is the accent) + **weight** (that column's figures at 18/600 against 18/450). The column tint is `muted`, not `accent`, so the whole column reads as one promoted object with exactly one accented mark inside it.
- **type** — title→40/600 · period header→18/550 caps tracked 0.08em (current period 18/600 `accent`) · row label→18/450 · figure→18/450, current period 18/600, all tabular-lining and right-aligned · footnote→18/450 `muted`.
- **accent** — the current-period header label. One mark.
- **ux** — Lets the audience compute the trend themselves in one glance, which is more persuasive than being told it.
- **avoid** — A fourth period. At 4 columns the width drops to 180px and figures with a currency symbol and a decimal start wrapping; a four-period comparison is a chart.
- **caps** — `periods max 3` is right and geometrically load-bearing. Row cap is missing: state **max 8 body rows** (9 is the geometric ceiling).

### table-highlight
- **zones** — title `64,48 1152×72` · table `64,152 1152×456`: header 48, body rows 44, highlighted row 52 with 8px extra internal padding · footnote `64,624 1152×32`.
- **focal** — the highlighted row. **Colour** (accent ground across the full row width) + **weight** (18/600 against 18/450) + **scale/spacing** (row height 52 against 44). The extra 8px matters more than it sounds: it is what makes the row survive being one of nine near-identical bands.
- **type** — title→40/600 · column header→18/550 caps tracked 0.08em `muted` · cell→18/450 · highlighted cell→18/600 · footnote→18/450 `muted`.
- **accent** — the one row, full-bleed to the table's measure. Not a coloured header band — a tinted header promotes the *labels*, which are the least important text on the slide.
- **ux** — Answers "which line should I be looking at?" before the presenter says it, which is the only reason a table belongs in a deck at all.
- **avoid** — Highlighting a row the title doesn't explain. An accented row with a neutral title makes the audience reverse-engineer why it's lit — the interface asking the user to think, which is the failure this whole family exists to prevent. One highlight, always; two makes both invisible.
- **caps** — No row cap stated. **Max 8 body rows** (9 geometric). Fewer is better here — the highlight's contrast against the set weakens as the set grows.

### table-income
- **zones** — title `64,48 1152×72` · table `64,152 1152×448`: label column `432` + four numeric columns `180` · header 48, body rows 44, subtotal rows 48 with a 1px rule above · mandatory footnote `64,616 1152×64` (two lines at 18px).
- **focal** — the statutory result line (NPAT, or whichever line the title names). **Weight** (20/600 against 18/450) + **spacing** (a 2px rule and 16px of air) + **colour** (the accent). Every subtotal above it uses a 1px `muted` rule and no weight change, so only one line reads as a destination.
- **type** — title→40/600 · column header→18/550 caps tracked 0.08em `muted` · line item→18/450 · subtotal→18/550 · result line→20/600 · variance column→18/450 with a signed prefix, sign never carried by colour alone · footnote→18/450 `muted`.
- **accent** — the result line's figure.
- **ux** — The single slide a results call is built around; it must be readable by someone half-listening on a phone, which is why the line count matters more than the completeness.
- **avoid** — Reproducing the statutory P&L. A slide is not the accounts — aggregate to the ~7 lines that move the story and let the footnote point at the filed statements. Reaching for a smaller cell size to fit more lines is the failure mode: 16px on a projected income statement is where the audience stops reading.
- **caps** — No cap stated, and the CAVEAT footnote eats 64px. State **max 7 body rows + 2 subtotals**; 9 total row slots is the geometric ceiling.

### table-balance
- **zones** — title `64,48 1152×72` · table `64,152 1152×448`: label column `528` (section headers and 24px indents live here) + 2–3 numeric columns `208` · header 48, section header rows 40 `muted`, body rows 44 · mandatory footnote `64,616 1152×64`.
- **focal** — the net position line (net assets, or net debt if that's the argument). **Weight** (20/600) + **spacing** (2px rule + 16px air) + **colour** (accent). Position is deliberately *not* a vector — the net line sits where the accounting puts it, so the other three have to do the work.
- **type** — title→40/600 · section header→18/550 caps tracked 0.08em `muted` · line item→18/450 · indent step 24px, maximum 2 levels · net line→20/600 · footnote→18/450 `muted`.
- **accent** — the net position figure.
- **ux** — Establishes capacity: what the company owns, owes, and has left to fund the plan with.
- **avoid** — Three levels of indent. At 18px a 16px indent step is invisible and a third level is indistinguishable from the second — collapse to two levels and 24px steps, or the hierarchy the indent is asserting simply isn't perceptible from the fourth row of a boardroom.
- **caps** — No cap stated. **Max 6 body rows + 3 section headers + 1 net line** = 10 row slots, which is the ceiling once the CAVEAT footnote is reserved.

### table-cashflow
- **zones** — title `64,48 1152×72` · table `64,152 1152×448`: label column `528` + 2–3 numeric columns `208` · three section headers (operating / investing / financing) at 40px `muted`, body rows 44, closing line 48 · mandatory footnote `64,616 1152×64`.
- **focal** — the closing cash (or free cash flow) line. **Weight** (20/600) + **spacing** (2px rule, 16px air) + **colour** (accent). Same treatment as `table-income`'s result line on purpose — a deck that accents its result line and its cash line identically teaches the audience where to look by slide three.
- **type** — title→40/600 · section header→18/550 caps tracked 0.08em `muted` · line item→18/450 · closing line→20/600 · footnote→18/450 `muted`.
- **accent** — the closing figure.
- **ux** — Carries the "the profit is real" argument: it reconciles the reported result to cash actually generated.
- **avoid** — Using it when the *movement* is the story. A table shows the components; it cannot show that the movement was driven by one item. If the point is attribution, that's `variance-bridge` — and using both wastes a slide.
- **caps** — No cap stated. **Max 6 body rows + 3 section headers + 1 closing line**.

### timeline-h
- **zones** — title `64,48 1152×72` · axis rule at `y=400`, spanning 32px past the first and last node only · 6 node columns of `192` on a 1152 measure, centres at x160/352/544/736/928/1120 · date labels `176×32` above the axis (baseline y352) · event blocks `176×120` below (y432–552) · no source slot.
- **focal** — one node, defaulting to the rightmost (a company history terminates in *now*, and the terminus is where the eye already stops). **Scale** (16px dot against 8px dots) + **colour** (accent fill) + **weight** (its labels one weight step up). Move it if the title names an earlier event.
- **type** — title→40/600 · date→20/550 tabular-lining · event heading→20/600, ~16 chars per line at 176px · event detail→18/450 `muted`, two lines maximum · axis rule 2px `muted`.
- **accent** — the one promoted node and its date.
- **ux** — Compresses a decade into one glance so the audience gets duration and sequence without reading a single sentence.
- **avoid** — Spacing nodes proportionally to their real dates. Real chronology clusters — three events in 2024 and one in 2011 collapse into an unreadable pile at one end. Even spacing is the honest read of *sequence*; if elapsed time is the point, label the gaps.
- **caps** — `max 6` is right; 176px per block is the width floor. Degrading: with 3 events use 3 columns of 384 (centres x256/640/1024) and let the blocks grow — never keep 6 slots and leave three empty. The axis rule always stops 32px past the outer nodes, so it never runs into whitespace, which is the single tell that makes a short timeline look broken.

### timeline-v
- **zones** — title `64,48 1152×72` · date gutter `64,152 96×456` (right-aligned) · vertical rule at `x=176`, running from the first node's centre to the last node's centre only · nodes on the rule · content column `216,152 1000×456` · 6 rows of 72 (gap 8) or fewer rows grown to fill.
- **focal** — the first entry. **Position** (top-left, the LTR entry point) + **weight** (its heading 20/600 against 20/550) + **spacing** (16px extra below it, separating it from the run). If the title names a later entry, move the accent there and let position stay with the first — the two vectors splitting is acceptable here because the rule visually chains them.
- **type** — title→40/600 · date→20/550 tabular-lining, right-aligned · entry heading→20/600 · entry sentence→18/450 `muted`, ~97 chars per line at 1000px · rule 2px `muted`, nodes 10px.
- **accent** — one node plus its date.
- **ux** — The form you choose when each entry needs a sentence; the vertical axis buys line length that a horizontal timeline cannot.
- **avoid** — Using it for entries that are just labels. Six one-word events down a 1000px column is 90% whitespace and reads as a padded list — that's `timeline-h`.
- **caps** — `max 6` is right but tight: at 6 rows each entry gets a heading plus exactly one line. Degrading: 4 events → 112px rows and two lines of detail each; 3 → 144px rows. The rule must shorten to span first-node-centre to last-node-centre at every count; a rule running past the final node into empty space is the broken tell.

### roadmap-quarters
- **zones** — title `64,48 1152×72` · four columns `264×456` at x64/x360/x656/x952, gutters 32 · each column = quarter header band `264×48` + items area `264×392` holding 4 items of `264×88`, gaps 8 · current quarter's column carries a `muted` ground the full 456 · no source slot.
- **focal** — the nearest quarter's column. **Colour** (its header label is the accent, its ground is `muted`) + **position** (leftmost) + **weight** (header 20/600 against 20/550). Promoted because roadmap credibility is bought with what ships next, not with what's promised in Q4; if the deck's argument is a later milestone, move the promotion and make the title say why.
- **type** — title→40/600 · quarter header→20/550 caps tracked 0.08em (current 20/600 `accent`) · item→20/450, ~24 chars per line at 264px, two lines maximum · no third level.
- **accent** — the current quarter's header label.
- **ux** — Converts a delivery plan into four commitments the audience can hold, which is what makes a roadmap slide answerable at Q&A.
- **avoid** — Four equally-full columns of equally-weighted bullets. Sixteen same-size phrases is a backlog dump, and the audience correctly reads it as "nothing has been prioritised". Density should decrease left to right — near quarters specific, far quarters thematic — which is also the honest representation of certainty.
- **caps** — `max 4` per column is geometrically right and editorially generous; ≤3 is the number a room retains. Degrading: an empty quarter keeps its header band and shows nothing — a labelled empty column is an honest statement about a delivery gap; deleting the column silently misrepresents the horizon.

### milestone-check
- **zones** — title `64,48 1152×72` · delivered panel `64,152 560×456` · next panel `656,152 560×456`, 32 gutter, 1px `muted` divider rule at x=640 · each panel = heading band `560×48` + 5 rows of `560×72`, gaps 8 · row = glyph `24×24` + text `496×...`.
- **focal** — the delivered panel's heading. Two co-equal panels, and I promoted **delivered**: this slide's job is credibility, and credibility is entirely a function of the left column — the right column is only worth reading if the left one is believed. Vectors: **colour** (the heading is the only accent) + **position** (left) + **weight** (20/600 against the right panel's 20/550). For a forward-looking raise deck, swap the promotion and say so in the title.
- **type** — title→40/600 · panel heading→20 (`delivered` 600 `accent`, `next` 550 `neutral`) · item→20/450, ~40 chars per line at 496px, two lines maximum · glyphs 24px, `muted` on both sides.
- **accent** — the delivered panel's heading only. Not the five check glyphs — five accented marks is decoration and destroys the single-focal rule.
- **ux** — Puts the promise and the receipt on the same slide, which is the only format in which a milestone claim is checkable in real time.
- **avoid** — Wildly unequal counts. 5 delivered against 1 next reads as an empty pipeline; 1 against 5 reads as nothing shipped. Keep within ±2 or reframe the slide.
- **caps** — `max 5` each side is right (5×72+48 = 408 in a 456 panel). Degrading: with 3+3 grow rows to 120 and gain a second line — but **both panels keep their full 456 height**. Panels shrinking to their content produce two different-height boxes across a vertical gutter, which is the single most obvious "broken" tell in this family.

### phase-stepper
- **zones** — title `64,48 1152×72` · stepper band `64,288 1152×160` (vertically centred in the content area) · 5 blocks `224×144` at x64/x296/x528/x760/x992, gaps 8 · 2px connector rule at `y=360` running behind the gaps only · current block `224×160` (16px taller, breaking the band top and bottom by 8) · no source slot.
- **focal** — the current phase block. **Colour** (accent ground, the only filled block) + **scale** (160 tall against 144) + **weight** (its name 20/600 against 20/550). Three vectors, which is what lets the current phase stay obvious even when its name is the longest.
- **type** — title→40/600 · phase number→18/550 caps tracked 0.08em `muted` · phase name→20/600 current, 20/550 others, ~18 chars per line at 224px, two lines maximum · connector 2px `muted`.
- **accent** — the current phase block's ground.
- **ux** — States progress against a stage-gated plan in a form the audience can't misread as "nearly done".
- **avoid** — Interlocking chevrons. The classic stepper defect is a chevron point overlapping the next block's first character; flat blocks with an 8px gap and a separate connector rule are structurally immune. Also avoid phase names longer than two words — 224px cannot hold three.
- **caps** — `max 5` is right. Degrading: 3 phases become 3 blocks of `378` on the same band, still spanning the full 1152 measure. A stepper is a proportion of a whole, so equal division is honest at any count — but 3 blocks left at 224 with dead space at the right reads as two missing phases, which is a factual misstatement.

### gantt-lite
- **zones** — title `64,48 1152×72` · period header row `336,152 880×40` (4 periods of 220) · stream label column `64,192 264×392` · plot `336,192 880×392` with vertical 1px `muted` gridlines at each period boundary running the full plot height · 5 stream rows of `72`, gaps 8 · bars `24` tall, centred in their row, snapped to a 110px half-period grid · footnote `64,624 1152×32`.
- **focal** — the critical-path bar. **Scale** (it is the longest bar on the slide) + **colour** (the only accent) + **weight** (its stream label at 20/600 against 20/450).
- **type** — title→40/600 · period header→18/550 caps tracked 0.08em `muted` · stream label→20/450, ~26 chars per line at 264px, two lines maximum · in-bar or end-of-bar annotation→18/550 · footnote→18/450 `muted`.
- **accent** — one bar.
- **ux** — Shows that two workstreams overlap — which is the only thing a slide-scale Gantt can honestly claim.
- **avoid** — Bars snapped to arbitrary pixel positions. If the grid is quarters, a bar either fills a quarter or half of one; anything between implies a precision the plan doesn't have. And the moment it needs dependency arrows or % complete it belongs in a document, not on a slide.
- **caps** — `streams max 5` × `periods max 4` is right and shouldn't be raised: 6 rows need 472px against 456 available. Degrading: 3 streams grow to 120px rows and the band re-centres vertically; the vertical period gridlines always run the full plot height regardless of row count, so a short chart never looks half-empty.

### catalyst-calendar
- **zones** — title `64,48 1152×72` · table `64,152 1152×456`: date `224` · event `640` · status/category `288` · header 48, body rows 44 · mandatory-in-practice footnote `64,624 1152×32` (forward-looking-statements caveat).
- **focal** — the nearest dated catalyst, i.e. the top row. **Position** (rows are sorted ascending by date, so the nearest is the first thing read) + **colour** (its date cell is the accent) + **weight** (that row's date at 18/600).
- **type** — title→40/600 · column header→18/550 caps tracked 0.08em `muted` · date→18/550 tabular-lining, one format across every row · event→18/450 · status→18/450 `muted` · footnote→18/450 `muted`.
- **accent** — the nearest catalyst's date. One cell.
- **ux** — Gives an investor audience the dates to diarise, which is the most concretely useful thing an IR deck can hand over.
- **avoid** — Mixing hard dates with "H2 FY26, TBC". An undated row is a forward-looking statement without a date — exactly what the footnote exists to caveat — and it also breaks the date column's scan, which was the template's only reason to exist. Put undated items in a separate list or drop them.
- **caps** — No cap stated. **Max 7 rows** (9 is geometric). Past 7 it stops being a set of catalysts and becomes a schedule, and nobody diarises a schedule from a slide.

### history-arc
- **zones** — title `64,48 1152×72` · arc band `64,200 1152×360` · 5 beat cells `224×360` at x64/x296/x528/x760/x992, gaps 8 · beat centres stepped along a shallow curve (y offsets 0/-32/-48/-32/0 from a `y=440` baseline) · connector drawn between node centres only · no source slot.
- **focal** — the final beat. **Position** (the arc terminates in the present, and the eye follows the curve to its end) + **colour** (accent node) + **scale** (its year set one step up, 32 against 28).
- **type** — title→40/600 · year→28/600 tabular-lining · beat heading→20/600, ~18 chars per line at 224px · beat detail→18/450 `muted`, two lines maximum.
- **accent** — the final beat's node and year.
- **ux** — Tells a causal story in five beats — each one made possible by the last — rather than listing five things that happened.
- **avoid** — Beats that aren't a chain. A history arc asserts causation by its shape; a set of unconnected events dressed in an arc is a claim the content doesn't support. Also note the slot limitation: **the years live inside `events` list text, so they can never be `stat` slots** — they will not take the accent colour and will not be sized to a box. If the years are the point, hand-author the slide or pick a stat-bearing template.
- **caps** — `max 5` is right; the curve stops reading as a shape past 5 nodes (that's `timeline-h`). Degrading: 3 beats become 3 cells of `378` with y offsets 0/-48/0 — the arc must be redrawn across the actual node count, never left as a 5-point curve with two nodes missing.

### cols-3-icon
- **zones** — title `64,48 1152×72` · three cells `368×400` at `(64,176) (456,176) (848,176)`, gutters 24 · each cell = icon `48×48` at y176 + heading `368×64` at y248 + body `368×112` at y328 · no source slot.
- **focal** — the title. Three parallel concepts are, by contract, co-equal — so the focal moves up a level to the claim they support. **Scale** (40 against a 24px heading) + **spacing** (72px band with a 32px gap below) + **position**. If one column genuinely must win, this is the wrong template.
- **type** — title→40/600 · column heading→24/600, two lines maximum · body→20/450, ~30 chars per line at 368px, three lines (~90 chars) · icons 48px, 2px stroke, `muted`.
- **accent** — none by default. Three accented icons is decoration; one accented icon among three creates a hierarchy the content doesn't claim. If the title needs colour, take one hairline rule under it and spend the budget there.
- **ux** — Asserts that a claim rests on exactly three things, and that they are of the same kind — the parallelism is the argument.
- **avoid** — Icons that restate their heading (a lightbulb beside "Innovation"). A decorative icon costs 48px of attention and returns nothing; the slot is optional, so drop it rather than fill it. Also: headings must be grammatically parallel, or the three stop reading as a set.
- **caps** — Fixed 3, correct. Body copy at ~90 characters is the real cap — past that the cells' baselines break and the row stops aligning.

### cols-4-icon
- **zones** — title `64,48 1152×72` · four cells `264×400` at x64/x360/x656/x952, gutters 32 · each cell = icon `48×48` at y176 + heading `264×64` at y248 + body `264×112` at y328 · no source slot.
- **focal** — the title. Same reasoning as `cols-3-icon`: co-equal by contract. **Scale** + **spacing** + **position**.
- **type** — title→40/600 · column heading→24/600, ≤2 words or it wraps to three lines · body→20/450, ~21 chars per line at 264px, four lines (~84 chars) · icons 48px `muted`.
- **accent** — none.
- **ux** — The maximum number of parallel concepts a 1280 canvas holds legibly side by side.
- **avoid** — Padding a fourth column because the template has four slots. Three real pillars and one invented one is the most common filler tell in a strategy deck, and the invented column is always the vaguest — the audience finds it instantly. Also watch heading wrap: at 264px a three-line heading in one column breaks the row's shared baseline, which reads as broken rather than varied.
- **caps** — Fixed 4, correct, and it is the ceiling — five concepts need two rows or a list, not 208px columns.

### matrix-2x2
- **zones** — title `64,48 1152×72` · plot `288,160 704×416` (four quadrants of `352×208`) · y-axis label rotated in `64,160 56×416` · x-axis label `288,600 704×32` · quadrant labels inset 24px from their quadrant's outer corner · 2px `muted` axis cross through the plot centre.
- **focal** — the occupied quadrant. **Colour** (accent ground on that one cell) + **weight** (its label 24/600 against the others' 20/450) + **scale** (its label one step up). A 2×2 with four evenly-treated quadrants is a framework, not an argument — the slide's job is to say which cell you are in.
- **type** — title→40/600 · axis label→18/550 caps tracked 0.08em `muted` · quadrant label→20/450, occupied quadrant 24/600, ≤4 words (~29 chars) at 352px · never below 18.
- **accent** — the occupied quadrant's ground.
- **ux** — Positions the company against two variables the audience already believes matter, so the conclusion feels derived rather than asserted.
- **avoid** — Axes whose direction isn't stated. Each axis is a **single** text slot, so it must encode direction itself ("Increasing scale →", not "Scale"). An unpolarised axis makes all four quadrants ambiguous, and the audience quietly stops trusting the frame.
- **caps** — Fixed 4 quadrants, correct. The real cap is the label length: 4 words per quadrant at 352px.

### funnel
- **zones** — title `64,48 1152×72` · funnel `320,152 640×432`: 5 bands of `80`, gaps 8, widths tapering `640 → 384` in 64px steps, each band centred on x=640 · labels inside their band · optional value right-aligned inside · no source slot.
- **focal** — the terminal band. **Position** (the taper's destination — the shape itself points there) + **colour** (accent fill) + **weight** (20/600 against 20/450).
- **type** — title→40/600 · stage label→20/600 terminal, 20/550 others, ~30 chars at the narrowest 384px band · value→20/600 tabular-lining · never below 18.
- **accent** — the terminal band.
- **ux** — Shows narrowing — pipeline to close, resource to reserve — where the *rate* of narrowing is the message.
- **avoid** — A decorative taper beside real numbers. If the band widths aren't proportional to the values printed on them, the shape contradicts the data and the slide is a misstatement. When the numbers don't taper, use `process-arrows`. Note the geometry: the taper must stop at **384px**, not at a point — a band narrower than that can't hold a legible label at 18px, which is why funnels that taper to nothing always end in a label floating outside the shape.
- **caps** — `max 5` is right. Degrading: 3 stages become bands of 136 tapering 640→448 over 3 steps — keep the taper *angle* roughly constant so a short funnel still reads as a funnel rather than as three stacked bars.

### pyramid
- **zones** — title `64,48 1152×72` · pyramid `320,176 640×408`: 4 tiers of `96`, gaps 8, widths `256 / 384 / 512 / 640` apex-to-base, each centred on x=640 · labels inside their tier, centred · no source slot.
- **focal** — the apex. **Position** (top, and a pyramid is read apex-first because the shape converges there) + **colour** (accent fill) + **weight** (20/600 against 20/550). Accenting the base contradicts the form — the shape already says the apex is the point.
- **type** — title→40/600 · apex label→20/600, ~20 chars at 256px (set it outside to the right at 18/550 if longer) · tier labels→20/550, ~28–50 chars depending on tier · never below 18.
- **accent** — the apex tier.
- **ux** — Asserts nesting: each tier rests on and is enabled by the one below it.
- **avoid** — Using it for a process. A pyramid is a containment and dependency shape, not a sequence; steps belong in `process-arrows`. And if the tiers *don't* nest — if they're just four ranked items — the shape is making a structural claim the content can't back.
- **caps** — `max 4` is right. A 5th tier drops the apex to ~128px, which cannot hold a label at 18px. Degrading: 3 tiers at 136 tall, widths 288/464/640 — the base always stays at 640 so the silhouette is constant across the deck.

### process-arrows
- **zones** — title `64,48 1152×72` · band `72,288 1136×144` · 6 blocks `176×144` at x72/x264/x456/x648/x840/x1032, gaps 16 · a 2px `muted` connector with a small chevron terminal drawn **in the 16px gap only**, never overlapping a block · no source slot.
- **focal** — the final step. **Position** (the terminus of the arrow chain) + **colour** (accent ground) + **weight** (20/600 against 20/550). If the title names a different step as the bottleneck, move all three there together.
- **type** — title→40/600 · step number→18/550 caps tracked 0.08em `muted` · step label→20/600 final, 20/550 others, ~14 chars per line at 176px, three lines maximum · never below 18.
- **accent** — the final step's ground.
- **ux** — Establishes that a sequence exists and has a fixed number of steps, so later slides can refer to "step 3" without re-explaining.
- **avoid** — Arrow heads that bite into the next block's text. Draw the connector in the gap, never over a block. The deeper problem at max: six steps of three words is eighteen items the room must hold in one glance, which is well past a working-memory budget of about four chunks. Four steps is the number people retain.
- **caps** — `max 6` is the correct *geometric* ceiling (176px is the label-width floor), but it is editorially too generous — flag 4 as the recommended maximum in authoring guidance while leaving the slot cap at 6.

### hub-spoke
- **zones** — title `64,48 1152×72` · canvas `64,152 1152×456`, hub centred at `(640, 396)` · hub circle `208` diameter · 6 spoke chips `208×88` on a `192` radius, angles evenly divided by spoke count (6 → every 60° starting at 0°) · 2px `muted` connectors drawn from the hub edge to the chip edge, never passing under a chip.
- **focal** — the hub. **Scale** (a 208px circle against 208×88 chips) + **position** (optical centre) + **colour** (the accent ground). The form only works if the centre wins; a hub that reads as a seventh peer defeats the template.
- **type** — title→40/600 · hub label→24/600, ~14 chars per line at 208px, two lines · spoke label→20/550, ~17 chars per line, two lines · never below 18.
- **accent** — the hub's ground.
- **ux** — Claims that several things all relate to one centre and *not* to each other — the negative claim is as load-bearing as the positive one.
- **avoid** — Using it for anything ordered or hierarchical. Spokes are peers with no sequence; if there's an order, the ring silently denies it. Also avoid connectors routed under chips — a line emerging from behind a box implies a relationship between chips that the model rules out.
- **caps** — `max 6` is right; 8 chips at 208 wide collide on a 192 radius. Degrading: **always redistribute angles by count** — 3 spokes sit at 90°/210°/330°, not in three of six fixed slots. A ring with holes in it is the tell that makes a small hub-spoke look broken.

### org-chart
- **zones** — title `64,48 1152×72` · root `512,168 256×80` · level-2 `256,312` and `768,312`, each `256×80` · level-3 four boxes `224×80` at x64/x368/x672/x976, y456 · connectors: 32px vertical drops into horizontal buses at `y=280` and `y=424`, 2px `muted` · no source slot.
- **focal** — the root node. **Position** (top-centre, the only symmetric object) + **colour** (accent ground, the only filled box) + **scale** (256 wide against level-3's 224, with more internal padding).
- **type** — title→40/600 · root label→24/600 · level-2 label→20/600 · level-3 name→20/600 with role→18/450 `muted` beneath, ~18 chars per line at 224px · never below 18.
- **accent** — the root node.
- **ux** — Answers "what exactly am I buying a share of" for a group with subsidiaries, JVs, or a listed parent and unlisted operating entities.
- **avoid** — Using it as a headcount map. Three levels and seven nodes is a *structure* slide; a real org chart belongs in a document. And never let an entity name wrap mid-word at 224px — abbreviate the entity, never the person.
- **caps** — `level3 max 4` is right at 224px. `level2 max 2` is **tighter than the geometry allows**: three level-2 boxes at 256 wide fit comfortably (3×256 + 2×64 = 896 inside 1152), and a three-subsidiary group structure is common — raise it to **max 3**, keeping level-3 at 4 (at 3 parents, 6 leaves would force 176px boxes, which is below the label floor).

### people-3up
- **zones** — title `64,48 1152×72` · three cells `368` wide at x64/x456/x848, gutters 24 · photo `368×368` at y152 · name `368×40` at y544 · role `368×32` at y584 · no source slot.
- **focal** — the title. Three portraits at identical size are a **set**, and the set is the message; there is no internal focal by design. Vectors on the title: **scale** (40 against 24) + **spacing** (72px band, 32px gap) + **position**.
- **type** — title→40/600 · name→24/600, ~24 chars at 368px · role→18/510 `muted` caps tracked 0.08em, two lines maximum · never below 18.
- **accent** — none. Accenting one face in a three-up invents a ranking among executives — a political error as much as a design one. If one person *is* the news, that's `bio-single`.
- **ux** — Puts faces to the names the audience will meet on the call, which measurably raises trust in the words that follow.
- **avoid** — Mixed photo treatments. Different crops, backgrounds, or one colour shot among two mono breaks the set instantly. Normalise: head-and-shoulders, eyeline at the same fraction of the frame in all three, one background treatment.
- **caps** — `person.3` optional. With two filled, re-compose as two cells of 560 rather than leaving a hole at the right — an empty third cell reads as a departure nobody announced.

### people-4up
- **zones** — title `64,48 1152×72` · four cells `264` wide at x64/x360/x656/x952, gutters 32 · block vertically centred: photo `264×264` at y196 · name `264×40` at y476 · role `264×64` at y520 · no source slot.
- **focal** — the title. Same set logic as `people-3up`. **Scale** + **spacing** + **position**.
- **type** — title→40/600 · name→24/600, ~19 chars at 264px · role→18/510 `muted` caps tracked 0.08em, two lines maximum (~28 chars per line) · never below 18.
- **accent** — none.
- **ux** — The standard leadership slide: four faces, four names, four roles, no hierarchy asserted.
- **avoid** — Long role strings. "Chief Operating Officer & Company Secretary" wraps to three lines at 264px and breaks the row's shared baseline while the other three sit at two. Pick one abbreviation convention (COO / CFO) and apply it to all four, or shorten every role.
- **caps** — `person.3`/`person.4` optional. With three filled, use `people-3up` — three 264px cells with 288px of dead space at the right is worse than three 368px cells.

### people-6up
- **zones** — title `64,48 1152×72` · 3×2 grid: cells `368×216` at x64/x456/x848 × y152/y392, gutters 24 · each cell = circular photo `152` at the cell's left, text block `192` wide beside it: name `192×32`, role `192×48` · no source slot.
- **focal** — the title. Six equal faces; the set is the message. **Scale** + **spacing** + **position**.
- **type** — title→40/600 · name→20/600, ~16 chars at 192px · role→18/450 `muted`, two lines · never below 18. This is the family's density floor — a seventh face would push names below 18.
- **accent** — none.
- **ux** — Shows a full board or executive team as a complete group, where completeness is the claim.
- **avoid** — Shrinking to fit a seventh. A board of seven on a six-slot grid either drops someone (a governance-optics error the audience will notice) or breaks the type floor. Split across two slides instead — and never mix background treatments across six photos, which is where a large set falls apart first.
- **caps** — `max 6` is right. With 5, **left-align the widow row** (two cells at x64 and x456) — centring the remainder breaks the column grid and is the visual tell. With 4 or fewer, use `people-4up`.

### bio-single
- **zones** — no title slot: photo `64,96 456×528` · text column `584,136 632×...`: name `632×56` at y136, role `632×32` at y208, 2px rule `632×2` at y264, bio `632×250` from y296 · nothing below y624.
- **focal** — the name. **Scale** (44 against a 20px bio — the largest thing on the slide, and the template gives it no title to compete with) + **weight** (600 against 450) + **spacing** (32px of air above the rule that nothing else gets). The name *is* the title here; that is the whole design of this template.
- **type** — name→44/600 · role→24/510 `muted` caps tracked 0.08em · bio→20/450, ~54 chars per line at 632px, up to 10 lines · never below 18.
- **accent** — the 2px rule under the role, or nothing. One hairline is the entire colour budget on a slide whose subject is a person.
- **ux** — Gives a new appointment or key hire the weight of a whole slide, which is itself the signal — the format says "this matters" before a word is read.
- **avoid** — A bio that runs long. The fit arithmetic allows ~540 characters in `632×250`; the design cap is **~420**, about three sentences. Past that it stops being a slide and becomes a page nobody finishes. Also avoid a landscape crop in a portrait slot — a 456×528 box wants a portrait frame, and a stretched or letterboxed headshot undoes the slide's own claim about the person's importance.
- **caps** — No list slots, so no `max N`. The cap that's missing is the bio's character ceiling: state **~420 characters**.

### board-grid
- **zones** — title `64,48 1152×72` · photo row: four cells `264` wide at x64/x360/x656/x952, circular photo `128` at y144, name `264×32` at y288, role `264×28` at y316 · table `64,372 1152×280`: header 44, four body rows of 48 · footnote/source line optional at `64,664`.
- **focal** — the photo row. Two co-equal blocks compete, and I promoted the **faces**: faces are pre-attentive — the eye finds them before it parses a single table cell, so fighting that with a heavier table only produces a slide where nothing wins. Vectors: **position** (above) + **scale** (128px circles against 18px rows) + **spacing** (a 32px gap and no rules, against the table's ruled bands). The table is deliberately quiet: 18/450, hairlines, no fills.
- **type** — title→40/600 · name→20/600 · role→18/450 `muted` · table column header→18/550 caps tracked 0.08em `muted` · table cell→18/450, dates tabular-lining · footnote→18/450 `muted`.
- **accent** — none by default. A governance slide that ranks its directors with colour is making a statement it doesn't intend. If one mark is unavoidable, put it on the chair's role label — never on a photo.
- **ux** — Carries the governance section: who the directors are, and the tenure/committee facts a governance-focused holder actually checks.
- **avoid** — A mismatch between the faces and the rows. Four photos above seven table rows implies three directors weren't worth a picture, which is exactly the optics a governance slide exists to avoid. Keep the table to the same people shown, or split.
- **caps** — `table.rows` has no cap, and with the photo row reserved the geometry holds **4 body rows**. State that. A board of 7+ needs `people-6up` plus a separate `table-simple`, not a compressed grid.

### advisor-strip
- **zones** — title `64,48 1152×72` · logo grid `64,200 1152×320`: 2 rows × 4 cells of `264×144`, gutters 32/32 · each mark bounded to `176×72` and optically centred in its cell · no source slot.
- **focal** — the title. Every mark is deliberately co-equal — that is this template's entire contract — so nothing inside the grid may win. Vectors on the title: **scale** (40 against the marks' ~72px optical height) + **spacing** (a 72px band with 80px of air above the grid) + **position**.
- **type** — title→40/600 · optional caption→18/450 `muted`. No type inside the grid; the marks carry their own.
- **accent** — none. Logos arrive with their own brand colours, so an accent here would be the slide's ninth colour. If the set clashes badly, render every mark in a single `neutral` — but that is a trademark-usage question as much as a design one, so flag it rather than deciding silently.
- **ux** — Borrows credibility by association: named advisors, brokers and partners shown as a set the audience already trusts.
- **avoid** — Normalising by bounding box. A wide wordmark and a compact roundel scaled to the same box width look wildly different in weight, and the grid reads as sloppy. Normalise by **optical area**. Second failure: mixing tiers — a tier-1 bank beside a local supplier makes an equivalence claim the audience will discount both for.
- **caps** — `max 8` is right for 2×4. With 5–7, keep the four-column grid and **left-align the second row** — centring the remainder breaks the column grid. With 4 or fewer, use a single row at y320.

### image-bleed-caption
- **zones** — `photo 0,0,1280,720` (full bleed) · `scrim 0,472,1280,248` (bottom-anchored, transparent→ground, no hard edge) · `caption 64,600,896,64` sitting inside the scrim · bottom margin 56.
- **focal** — the photograph's subject. Wins on **scale** (it is the entire 1280×720 frame), **isolation** (no competing element above y=472) and **position** (subject placed on the upper-left third, where the eye lands first in LTR). The caption is deliberately last: small, low, single line.
- **type** — `caption→24/1.35` (single line preferred, two absolute max) · nothing else on the slide.
- **accent** — `none`. A photo slide spends its impact on the image; an accent on the caption would compete with the subject and there is nothing else to mark. Caption sits `neutral` on the scrim.
- **ux** — Lets a real asset (site, plant, product, people) do the arguing, with one line of context so the audience knows what they are looking at.
- **avoid** — Do not use it for a photo whose subject sits in the bottom-left; the scrim will bury it and the caption will sit on the thing you wanted seen. Crop-check before choosing this template rather than after.
- **caps** — No list slots. Caption should be capped at ~90 characters: `perLine = 896/(24*0.58) ≈ 64`, two lines max inside a 64px box. Longer copy belongs on `image-left`.
- **image treatment** — **aspect-fill**, centre-weighted, subject kept inside a 1152×592 safe area so the bleed can crop 64px on every side without losing it. **Text protection = scrim**, fixed at `0,472,1280,248`, always present, never chosen per slide — a scrim that appears only on "dark photos" produces two different-looking slides in one run.

### image-left
- **zones** — `photo 0,0,552,720` (full-height bleed, flush to the left edge) · `text column 616,0,600,720` with `title 616,216,600,128` and `body 616,368,600,224` · gutter 64 between photo edge (552) and text (616) · right margin 64.
- **focal** — the title. Wins on **scale** (56 against 22 body), **weight** (600 against 400) and **spacing** (128px of room above it, 24 below). The photo is large but soft-edged and mid-tone; the title is the only hard, high-contrast mark in the text column.
- **type** — `title→56/1.1` · `body→22/1.5` · optional eyebrow if the theme has one `→18` caps, tracked 0.08em.
- **accent** — one short rule or the eyebrow above the title at `616,168,64,4`. Nothing else on the slide takes it.
- **ux** — Pairs one visual proof with the claim it supports, so the audience reads the sentence and verifies it in the same glance.
- **avoid** — Do not use it when the body copy runs past ~420 characters (`perLine = 600/(22*0.58) ≈ 47`, `lines = 224/(22*1.5) ≈ 6` → capacity ≈ 282, gate limit ≈ 324). Longer argument needs a text-only template; squeezing it here drops the body below 18 and breaks the floor.
- **caps** — No list slots. Body cap ≈ 300 characters as computed above; state it rather than discovering it at the gate.
- **image treatment** — **aspect-fill** into 552×720 (a 0.77 portrait crop — check the subject survives a tall crop before choosing this over `image-bleed-caption`). **Text protection = reserved zone**: no text ever sits on the photo, so no scrim and no card exist on this template. That is the whole point of the split.

### image-right
- **zones** — mirror of `image-left`: `photo 728,0,552,720` · `text column 64,0,600,720` with `title 64,216,600,128` and `body 64,368,600,224` · gutter 64 (664→728) · left margin 64.
- **focal** — the title, same two vectors (**scale** 56 vs 22, **weight** 600 vs 400) plus **position** — in a mirrored slide the text now occupies the LTR entry corner, so it reads before the image rather than after it.
- **type** — identical to `image-left`: `title→56/1.1` · `body→22/1.5` · eyebrow `→18` tracked.
- **accent** — the rule/eyebrow at `64,168,64,4`. Once only.
- **ux** — Same job as `image-left`, alternated across a run of slides so a three- or four-slide photo sequence has rhythm instead of reading as one repeated layout.
- **avoid** — Do not alternate for its own sake. If the photos in the run all have their subject on the same side, forcing a mirror puts the subject in the gutter. Mirror the layout only when the imagery supports it.
- **caps** — Same body cap ≈ 300 characters. Keep it identical to `image-left` so an author swapping between the two never has to re-edit copy.
- **image treatment** — **aspect-fill** into 552×720; **text protection = reserved zone** (text never touches the photo).

### image-grid-2x2
- **zones** — `title 64,56,1152,72` · four tiles on a 2×2 grid, cell 560×216, column gap 32, row gap 56: `tile1 64,152,560,216` / `tile2 656,152,560,216` / `tile3 64,424,560,216` / `tile4 656,424,560,216` · each caption in a reserved strip directly under its tile: `cap1 64,376,560,24` / `cap2 656,376,560,24` / `cap3 64,648,560,24` / `cap4 656,648,560,24` · bottom margin 48.
- **focal** — the **set**, read as one object, not any single tile. It wins on **scale** (the grid occupies 1152×520, ~65% of the canvas), **repetition** (four identical cells read as a single unit) and **position** (it sits directly under the only title). No tile is promoted — promoting one would turn the slide into an `image-left`.
- **type** — `title→32` · `caption→18/1.3`, single line, sentence case. Captions are labels, not sentences.
- **accent** — `none`. Four tiles cannot share one accent, and marking one tile makes the other three read as rejected. Leave the whole grid `neutral`.
- **ux** — Shows breadth — a portfolio, a site list, a product range — where the argument is "there are several of these", not "look at this one".
- **avoid** — Do not use it when only two or three images exist. The optional slots drop out and the layout closes up, but a 2×2 grid with a hole reads as missing content; use `image-strip-3up` instead.
- **caps** — Fixed at 4; correct for the geometry — a 3×2 at this canvas gives 368×216 tiles with 18px captions at ~35 characters, which is a contact sheet, not a slide. Caption cap ≈ 55 characters (`perLine = 560/(18*0.58) ≈ 53`, one line).
- **image treatment** — **aspect-fill** into 560×216 (2.6:1 — a deliberately cinematic crop; tall subjects will lose head and feet, so screen the set first). **Text protection = reserved zone**: captions live off the image in their own strip. Never overlay a caption on a tile this small.

### image-strip-3up
- **zones** — `title 64,56,1152,72` · three panels, cell 368×296, gap 24: `panel1 64,192,368,296` / `panel2 456,192,368,296` / `panel3 848,192,368,296` · captions in reserved strips: `cap1 64,504,368,56` / `cap2 456,504,368,56` / `cap3 848,504,368,56` · bottom margin 160 (deliberate — the strip floats above a quiet base).
- **focal** — the middle panel when the slide is a *comparison*; the left panel when it is a *sequence*. Either way the winner takes **position** (centre or LTR-first) plus **spacing** (the deliberate 160px of empty ground below the strip pulls the eye up into it). Do not add a second vector by enlarging one panel — the equal cells are what make it read as a comparison.
- **type** — `title→32` · `caption→20/1.35`, up to two lines.
- **accent** — one caption's leading label (e.g. the "after" or "recommended" panel) may take the accent — but only when the slide has a directional argument. In a neutral three-way set: `none`.
- **ux** — Puts three states side by side so the audience does the comparison themselves rather than being told the difference.
- **avoid** — Do not use it for three unrelated images. Three panels in a row is a strong implicit claim of sequence or equivalence; unrelated content makes the audience hunt for a relationship that isn't there.
- **caps** — Fixed at 3; correct. A fourth panel at this canvas drops the cell to 270px wide, which cannot carry a legible caption at 20. Caption cap ≈ 70 characters (`perLine = 368/(20*0.58) ≈ 31`, two lines).
- **image treatment** — **aspect-fill** into 368×296 (1.24 portrait-ish). **Text protection = reserved zone** below each panel. Panels must all be filled to the same crop rule; three different crops in one strip destroys the comparison.

### image-stat-overlay
- **zones** — `photo 0,0,1280,720` (full bleed) · `stat card 64,368,576,248`, opaque `ground`, radius per theme, holding `value 96,408,512,120` and `label 96,544,512,32` · `caption 64,648,896,32` on a bottom scrim `0,608,1280,112` · bottom margin 40.
- **focal** — the stat value. Wins on **scale** (96–112px against everything else on the slide), **colour** (it is the one accented mark), **isolation** (it sits on its own opaque card, cut out of the photograph) and **position** (left third, on the entry diagonal). Four vectors is intentional here — the photograph is a loud competitor.
- **type** — `stat.value→96` (auto-sized down by the renderer; the 512px inner width holds ~8 characters at 96) · `stat.label→20` caps, tracked 0.08em · `caption→18/1.35`.
- **accent** — the stat value, and only the value. The label stays `muted-on-ground`, the caption `neutral`.
- **ux** — Welds one number to the physical thing it describes, so the figure lands as evidence rather than as a claim on a chart.
- **avoid** — Do not use it for a figure that needs a comparator or a trend. A single number on a photograph has nowhere to put "vs prior period"; that belongs on `share-price` or a KPI row.
- **caps** — `stat.value` ≤ 14 characters by contract, but the 512px card interior tightens it: at the theme's 96 step, `512/(96*0.62) ≈ 8` characters. Recommend narrowing the documented guidance to **≤8 characters** for this template specifically, or widening the card to 704.
- **image treatment** — **aspect-fill**, with the subject composed into the *right* half (x 640–1280) so the stat card lands on quiet ground. **Text protection = card** for the stat (an opaque plate, because a number must never be read through a photograph) **plus a scrim** for the caption only. Both are fixed geometry — never decided per slide.

### map-pins
- **zones** — `title 64,56,1152,72` · `map 64,152,768,512` · `pin list 880,152,336,336`, six rows at 56 (`row n` at `y = 152 + 56n`), each row = pin marker 24×24 at x=880 + label from x=920 · bottom margin 56.
- **focal** — the map. Wins on **scale** (768×512 is 43% of the canvas), **position** (left, LTR entry) and **density** (the pin list beside it is deliberately sparse, 56px rows with air). The list reads as index, the map as subject.
- **type** — `title→32` · `pin label→20/1.2` · optional sub-label `→18 muted`.
- **accent** — the pin markers, as one set (they are one semantic class, so this counts as a single accent placement). Nothing else on the slide is accented — not the title, not the list labels.
- **ux** — Answers "where do you actually operate" in one glance, with the named list doing the work a hover state would do in a product.
- **avoid** — Do not use it when the sites are geographically clustered to the point of overlap at this scale. Two pins 6px apart read as one; use a table or an inset instead of shrinking the markers.
- **caps** — `pins max 6` is exactly right: `6 × 56 = 336px`, which fits the 512px map band with air to spare and leaves each label 336px at 20 (~28 characters). A 7th pin either compresses rows below the 44px touch/read rhythm or pushes the list past the map's bottom edge.
- **image treatment** — **aspect-fit**, not fill. A map is information, not atmosphere: cropping it removes geography and can silently drop a pinned site outside the frame. Letterbox inside 768×512 on the theme's `muted` ground. **Text protection = reserved zone** — every label sits in the right-hand column, off the map. Pin markers may sit on the map; words may not.

### share-price
- **zones** — `title 64,56,1152,72` · `KPI row 64,152,1152,144` as three cells of 368 with 24 gaps (`x = 64 / 456 / 848`) · `chart 64,320,1152,288` · `source strip 64,632,1152,48`.
- **focal** — `kpi.1` (the last price or the period move). Wins on **scale** (72px value against 20px labels and 18px axis type), **position** (top-left of the KPI row, first thing after the title) and **spacing** (144px band with the chart held 24px clear below).
- **type** — `title→32` · `stat.value→72` · `stat.label→20` caps tracked 0.08em · `chart axis/series labels→18` · `source→18`.
- **accent** — the primary price series line in the chart. `kpi.1` wins on scale and position instead, so the accent is not spent twice. Secondary series (index, volume) stay `muted`.
- **ux** — The standing "how has the stock done" slide: gives the number the room wants and the shape the number came from, in one frame.
- **avoid** — Do not truncate the value axis to dramatise a move. On the most-screenshotted slide in an IR deck, a chopped axis is a credibility defect, not a styling choice.
- **caps** — No list caps. 3 KPIs is the ceiling for this geometry: at 4-up the cell drops to 270px and a 72px value holds only ~6 characters, so `$1,234.5m` wraps mid-figure. Keep `kpi.3` optional and never extend to 4.
- **source** — `source:text!` renders in the strip at `64,632,1152,48`, 18px, `neutral` (not `muted`), left-aligned on the same left margin as the title so it reads as part of the slide rather than as chrome. It must clear ≥4.5:1 against the ground. It is legible, not hidden: a source line small enough to need a squint is the same defect as no source line.

### capital-structure
- **zones** — `title 64,56,1152,72` · `table 64,152,680,456` (header 56 + rows 48) · `chart 776,152,440,368` (stacked bar or donut of the same composition) · `footnote 64,632,1152,48`.
- **focal** — the table's total / fully-diluted row. Wins on **weight** (600 against 400 in the body rows), **spacing** (a 16px rule and 8px of extra padding above it) and **position** (last row, where a reader lands after scanning the column). The chart restates, it does not compete.
- **type** — `title→32` · `table header→20` caps tracked 0.06em · `table cell→20` · `chart labels→18` · `footnote→18`.
- **accent** — the total row's figure (or the equivalent segment in the chart — one, not both).
- **ux** — Puts every claim on the equity in one frame so a reader can compute dilution themselves instead of asking for it.
- **avoid** — Do not use it as the dilution story for a raise. It shows the register as at a date; the before/after argument belongs on `cap-table-prepost` or `dilution-waterfall`.
- **caps** — No list caps. Table cap = header + **8 body rows** (`56 + 8×48 = 440 ≤ 456`). A 9th row runs to y=656 and collides with the footnote strip — the measured failure mode where the overflowed rows and the footnote both vanish from the render. Split to a second slide instead.

### register-breakdown
- **zones** — `title 64,56,1152,72` · `table 64,152,680,456` · `chart 776,152,440,368` (composition donut or 100% bar) · `source strip 64,632,1152,48`.
- **focal** — the largest holder band — the top row of the table and its matching chart segment read as one mark. Wins on **scale** (largest segment), **colour** (the single accent) and **position** (first row / 12-o'clock segment start).
- **type** — `title→32` · `table header→20` caps tracked · `table cell→20` · `chart labels→18` (direct-labelled, no separate legend) · `source→18`.
- **accent** — the largest ownership band, marked once — either the chart segment or the table row, not both. Pair it with a direct label so the meaning does not rest on colour alone.
- **ux** — Answers "who owns this company" with the concentration visible rather than described.
- **avoid** — Do not use it for a register with a long tail of near-equal holders; a donut of twelve 8% slices communicates nothing. Aggregate to Top 20 / institutional / retail / board and use the table for the detail.
- **caps** — No list caps. Table cap = header + **8 body rows** (same 440/456 arithmetic as `capital-structure`). Chart series cap 6 segments — beyond that direct labels at 18px cannot be placed without collision.
- **source** — `source:text!` in the `64,632,1152,48` strip at 18px `neutral`, naming the registry and the as-at date. Registry data is third-party and dated; an undated register breakdown is a compliance problem, not a design one. Legible at 18, not shrunk to fit.

### dividend-history
- **zones** — `title 64,56,1152,72` · `table 64,152,624,456` (period / DPS / franking / payment date) · `chart 720,152,496,368` (column series, one bar per period) · `footnote 64,632,1152,48`.
- **focal** — the most recent period's bar in the chart. Wins on **position** (rightmost, where a time series ends and the eye stops), **colour** (the one accent) and **scale** if it is also the largest. Two vectors hold even when it is not the tallest bar.
- **type** — `title→32` · `table header→20` caps tracked · `table cell→20` · `chart value labels→18`, direct on the bars · `footnote→18`.
- **accent** — the latest-period bar. Prior periods stay `muted`.
- **ux** — Shows income investors the payment record and its direction in the order they ask for it: how much, how often, when.
- **avoid** — Do not use it when the record is short or interrupted. Three bars with a gap invites the question the slide was meant to close; state the policy in text instead.
- **caps** — No list caps. Table cap = header + **8 body rows**. Chart cap ≈ 12 columns: `496/12 ≈ 41px` per bar, which is the floor for a legible 18px direct value label rotated or stacked. Beyond 12 periods, drop the labels or narrow the window.

### guidance-actual
- **zones** — `title 64,56,1152,72` · `KPI pair 64,152,1152,144` as two cells of 564 with a 24 gap (`x = 64 / 652`) — guidance and actual, or actual and variance · `chart 64,320,1152,288` (paired columns, guidance vs actual per period) · `footnote 64,632,1152,48` — **mandatory**.
- **focal** — the variance figure. Wins on **scale** (96px value in a 564px cell), **colour** (the single accent) and **position** (right cell, read last, which is where a delivery argument should land). Pair the accent with an explicit `+`/`−` glyph and the word "vs guidance" so the result is not encoded in colour alone.
- **type** — `title→32` · `stat.value→96` · `stat.label→20` caps tracked · `chart labels→18` · `footnote→18`.
- **accent** — the variance stat value. The chart's guidance series stays `muted`, the actual series `neutral-strong`.
- **ux** — The delivery record: shows whether the company did what it said it would, without making the audience do the subtraction.
- **avoid** — Do not use it when the answer is a miss you are not prepared to name in the title. A slide that shows a miss under a neutral title reads as evasion; the most scrutinised slide in the deck is the wrong place to be coy.
- **caps** — No list caps. 2 KPIs is right; a third at 368px drops the value to 72 and weakens the focal. **Slot gap worth fixing:** `footnote:text?` is optional in the catalogue while the `[CAVEAT]` marking makes it mandatory. Either make it `footnote:text!` or accept that authors will omit the caveat and the gate will not catch it.
- **caveat** — The mandatory footnote sits in the `64,632,1152,48` strip at 18px `neutral` — the same strip a source line uses, on the same left margin, ≥4.5:1 against the ground. Two lines maximum (`perLine = 1152/(18*0.58) ≈ 110`). It states the guidance basis and the as-at date. It is legible at reading distance, not a hairline at the frame edge.

### peer-comparison
- **zones** — `title 64,56,1152,72` · `table 64,152,1152,456` full width when no chart (header 56 + 8 rows at 48) — or `table 64,152,680,456` + `chart 776,152,440,368` when a chart is bound · `source strip 64,632,1152,48`.
- **focal** — the company's own row. Wins on **weight** (600 against 400 in peer rows), **colour** (the one accent, as a row tint or a 4px leading marker) and **position** (pinned to the top row rather than sorted into the middle of the peer set).
- **type** — `title→32` · `table header→20` caps tracked 0.06em · `table cell→20`, figures tabular-lining and right-aligned · `chart labels→18` · `source→18`.
- **accent** — the own-company row marker. Every peer row stays `neutral`. Never accent a favourable metric column as well — that is the accent spent twice and it reads as thumb-on-scale.
- **ux** — Places the company in a named peer set so relative valuation is checkable rather than asserted.
- **avoid** — Do not curate the peer set to flatter. A set the audience does not recognise as fair costs more credibility than the comparison buys, and analysts will name the omission in Q&A.
- **caps** — No list caps. Table cap = header + **8 body rows** — which means **7 peers plus the company**. That is a defensible peer set; if the real set is larger, cut to the 7 most-cited rather than shrinking rows below 48px.
- **source** — `source:text!` in the `64,632,1152,48` strip at 18px `neutral`, naming the data provider, the metric basis (e.g. consensus vs reported) and the as-at date. It carries the burden of the whole slide, so it is set at the same size as any other footnote and never demoted to `muted` grey.

### analyst-coverage
- **zones** — `title 64,56,1152,72` · `table 64,152,1152,456` full width, four columns (broker / analyst / recommendation / target), header 56 + 8 rows at 48 · `source strip 64,632,1152,48`.
- **focal** — the target-price column. Wins on **position** (rightmost column, the terminal scan position for a left-to-right table), **weight** (600 on the figures against 400 elsewhere) and **alignment** (right-aligned tabular figures form a single vertical edge the eye follows down).
- **type** — `title→32` · `table header→20` caps tracked 0.06em · `table cell→20`, targets tabular-lining right-aligned · `source→18`.
- **accent** — the consensus / mean target, if a summary row exists. If the table is brokers only: `none`. Do not accent individual recommendations — colour-coding buy/hold/sell on this slide is both meaning-in-colour-alone and an implicit endorsement.
- **ux** — Shows the audience who is publishing on the stock and where the street sits, without the company appearing to endorse any of it.
- **avoid** — Do not use it to show only the favourable coverage. A partial list of brokers is worse than no slide; if the full set cannot be shown, show none.
- **caps** — No list caps. Table cap = header + **8 body rows** with the source strip in place. This is genuinely tight for a well-covered stock — recommend the theme allow a 44px row on this template specifically (header 56 + 10 rows = 496, still inside the 456→504 band if the footnote strip is dropped, which it cannot be here). Otherwise split coverage across two slides rather than compressing.
- **source** — `source:text!` in the `64,632,1152,48` strip at 18px `neutral`, naming the compiler and the as-at date, plus the standing disclaimer that the views are the analysts' own. Legible and on the slide — not moved to a notes field.

### esg-metrics
- **zones** — `title 64,56,1152,72` · `KPI row 64,152,1152,144` as four cells of 270 with 24 gaps (`x = 64 / 358 / 652 / 946`) · `chart 64,320,1152,288` (single trend series) · `footnote 64,632,1152,48`.
- **focal** — `kpi.1`. Wins on **position** (leftmost of the four, first in the LTR scan), **spacing** (the row sits alone in its 144px band) and **colour** if the theme marks the lead metric. At four-up the cells are equal by design, so the accent is what breaks the tie.
- **type** — `title→32` · `stat.value→56` (a 270px cell holds ~7 characters at 56: `270/(56*0.62) ≈ 7.8`) · `stat.label→18` caps tracked 0.08em, two lines allowed · `chart labels→18` · `footnote→18`.
- **accent** — `kpi.1`'s value, or the chart's trend line — one, not both. Default to the trend line when the slide's argument is direction rather than level.
- **ux** — Gives the ESG section four hard measures and one direction, so it reads as reported performance rather than as narrative.
- **avoid** — Do not use it with four metrics on four different bases (intensity, absolute, rate, index) and no unit labels. Four unlabelled numbers side by side invite the reader to compare things that are not comparable.
- **caps** — 4 KPIs is the ceiling for this geometry — the 270px cell already forces `stat.value` down to 56 and caps the figure at ~7 characters. Do not extend to 5. `stat.label` at 18 across 270px holds ~26 characters per line; keep labels to two lines.

### safety-stats
- **zones** — `title 64,56,1152,72` · `KPI row 64,152,1152,144` as three cells of 368 with 24 gaps (`x = 64 / 456 / 848`) · `chart 64,320,1152,288` (TRIFR/LTIFR trend, `chartSeries!`) · `footnote 64,632,1152,48`.
- **focal** — `kpi.1` (current TRIFR). Wins on **scale** (72px value against 20px labels), **position** (first cell) and **spacing** (its band is otherwise empty). The trend chart is the supporting evidence, not the headline.
- **type** — `title→32` · `stat.value→72` · `stat.label→20` caps tracked 0.08em · `chart axis/series labels→18` · `footnote→18`.
- **accent** — the trend line in the chart. The KPI values stay `neutral-strong` and win on scale — spending the accent on both the number and the line is the most common way this slide ends up with two focal points.
- **ux** — Reports the safety record with its direction attached, which is what the metric is actually for.
- **avoid** — Do not use a truncated or inverted axis to make a worsening trend look flat. Safety data is audited elsewhere; a cosmetic axis on this slide is the fastest available credibility loss.
- **caps** — No list caps. 3 KPIs is right for 368px cells at 72px values (~8 characters). Chart cap ≈ 12 periods across 1152px. Never encode "improving/worsening" in red/green alone — pair with an arrow glyph and the word, per the colour rule.

### production-summary
- **zones** — `title 64,56,1152,72` · `table 64,152,680,456` (product / period / prior / variance) · `chart 776,152,440,368` (paired columns, period vs prior) · `footnote 64,632,1152,48`.
- **focal** — the variance column in the table. Wins on **weight** (600 against 400), **alignment** (right-aligned tabular figures forming one vertical edge) and **colour** (the single accent applied to the column's values, paired with `+`/`−` glyphs so direction is not colour-only).
- **type** — `title→32` · `table header→20` caps tracked 0.06em · `table cell→20` tabular-lining · `chart labels→18` · `footnote→18`.
- **accent** — the variance column's figures, as one set. The chart stays two-tone `neutral`/`muted`.
- **ux** — Shows what was produced against what was produced last time, with the delta already computed for the reader.
- **avoid** — Do not use it when units differ per row without a unit column. Tonnes beside ounces beside megalitres in one unlabelled figure column is the failure mode; give units their own column at 20px.
- **caps** — No list caps. Table cap = header + **8 body rows**. If the product set genuinely exceeds 8, group to categories on this slide and put the full schedule in the appendix — do not drop the row height below 48, which is the floor for a 20px cell with breathing room.

### disclaimer-full
- **zones** — `title 64,56,1152,64` · two body columns, `col1 64,152,552,512` and `col2 664,152,552,512`, gutter 48 (616→664) · bottom margin 56. No footer, no accent bar, no logo — the page is the content.
- **focal** — the title. Wins on **scale** (40 against 14–16 body) and **isolation** (it is the only element outside the two body columns). This is the one template where the focal is deliberately weak — a disclaimer that competes for attention has been designed wrong.
- **type** — `title→40/1.15` · `body→16/1.45` preferred, **14/1.5 floor** for genuinely long statutory text. 14 is the legal-disclaimer exception and applies here and on `forward-looking` only.
- **accent** — `none`. Never accent a disclaimer; emphasis inside legal text changes its meaning.
- **ux** — Carries the mandatory legal page in a form a reader could actually read if they chose to, rather than as a grey block that admits it expects not to be read.
- **avoid** — Do not shrink type below 14 to fit a long disclaimer on one slide. Split across two slides (`Disclaimer 1 of 2`) instead — an unreadable disclaimer is a compliance risk dressed as a layout solution.
- **caps** — No list caps. Capacity at 14/1.45 in a 552×512 column: `perLine = 552/(14*0.58) ≈ 68`, `lines = 512/(14*1.45) ≈ 25` → ~1,700 characters per column, **~3,400 characters per slide**. At the preferred 16/1.45: ~1,290 per column, **~2,580 per slide**. Past that, split the slide.
- **legibility** — 14px on a 1280×720 canvas is ~21px at 1920 projection and is the documented floor, not a target. Set it `neutral` on `ground` at ≥4.5:1; a muted grey disclaimer fails contrast and reads as concealment.

### forward-looking
- **zones** — `title 64,56,1152,64` · `body 64,152,760,504` — a single column held to a readable measure, not full width · right band `856,152,360,504` left empty on purpose · bottom margin 64.
- **focal** — the title. **Scale** (40 against 18) and **position** (top-left, alone above a single narrow column). Same deliberate restraint as `disclaimer-full`.
- **type** — `title→40/1.15` · `body→18/1.5`. This statement is shorter than a full disclaimer, so it stays at 18 rather than dropping to the 14 legal floor. Use 14 only if the statement genuinely will not fit.
- **accent** — `none`.
- **ux** — Puts the forward-looking-statements qualification in front of the audience *before* the guidance slides it governs, in one readable column.
- **avoid** — Do not merge it into `disclaimer-full`. A forward-looking statement placed after 3,000 characters of general disclaimer is functionally not given; it needs its own slide near the front.
- **caps** — No list caps. Capacity at 18/1.5 in 760×504: `perLine = 760/(18*0.58) ≈ 72`, `lines = 504/(18*1.5) ≈ 18` → **~1,300 characters**. The empty right band is the release valve — widen the column to 1152 (→ ~2,000 characters) only if the statement demands it, accepting the longer measure.
- **legibility** — 18/1.5 at a 72-character measure is inside the readable band. Set `neutral` on `ground`, ≥4.5:1. Do not centre it; centred legal text at this length is unreadable.

### contact
- **zones** — `title 64,56,1152,72` · four contact cards on one row, 264 wide with 32 gaps (`x = 64 / 360 / 656 / 952`), `y 248, h 200` · `logo 64,600,200,64` bottom-left, aspect-fit · bottom margin 56.
- **focal** — the primary contact card (`contacts[0]`). Wins on **position** (leftmost, LTR-first), **weight** (name at 600 against role/detail at 400) and **colour** if the theme marks the primary. The four cards are otherwise equal by design.
- **type** — `contact name→24/1.2` · `contact role→18` · `contact detail (email/phone)→18/1.4`, never below 18 — a phone number nobody can read is the one failure this slide cannot survive.
- **accent** — the primary contact's name, or the email addresses as one set. One or the other.
- **ux** — Closes the deck by telling the room exactly who to call and about what, so the follow-up question has an address.
- **avoid** — Do not use it with a generic `investors@` inbox and nothing else. A named human with a role is the entire value of the slide; a shared mailbox belongs in the footer.
- **caps** — `contacts max 4` is right: `4 × 264 + 3 × 32 = 1152` exactly. A fifth card drops the cell to 208px, where a long email address (~30 characters at 18 needs ~313px) wraps mid-address. If five contacts are genuinely needed, go 2×2 at 560 wide and drop the logo.

### thank-you
- **zones** — `title 64,296,1152,112` · `subtitle 64,432,760,48` · optional theme device (rule, mark) at `64,240,64,4` · everything else empty. Vertical centre of mass sits slightly above the true middle (title baseline near y=380), which reads as composed rather than as content that fell to the centre.
- **focal** — the title. Wins on **scale** (88 against 24), **spacing** (240px of clear ground above it, 24 below) and **isolation** (it is one of two marks on the slide).
- **type** — `title→88/1.05`, tracked −0.02em (display type at this size needs negative tracking; the floor is −0.04em) · `subtitle→24/1.4`.
- **accent** — the rule/device above the title, or `none`. Not the title itself — a full-bleed accent word is the drenched strategy and only belongs here if the whole deck committed to it.
- **ux** — Gives the deck a deliberate ending so the last thing on screen is a chosen frame, not whatever slide the presenter stopped on.
- **avoid** — Do not use it as the terminal slide of a live session. `contact` or `qa` should hold the screen while the room talks; a "Thank you" left up for 20 minutes of Q&A wastes the most-viewed frame in the deck.
- **caps** — No list caps. Title cap ~28 characters at 88 (`1152/(88*0.62) ≈ 21` per line, two lines max). Subtitle cap ~110 characters.

### qa
- **zones** — **without image:** `title 64,296,1152,112`, same composition as `thank-you`. **With image:** `photo 640,0,640,720` (right half, full-height bleed) and `title 64,296,512,112` in the reserved left half; text never crosses x=576.
- **focal** — the title. **Scale** (88 against nothing else) and **isolation** (single mark on its ground). With the image bound, add **position** — the title holds the LTR entry half while the photo holds the exit half.
- **type** — `title→88/1.05` tracked −0.02em. No body type on this slide.
- **accent** — `none`. This slide is a holding frame; an accent on it is decoration with no argument to carry.
- **ux** — Holds the screen while the room asks questions, signalling that the presentation has stopped and the conversation has started.
- **avoid** — Do not put the agenda, a recap, or contact details on it. This slide is on screen the longest of any in the deck and the temptation is to make it work harder; a busy Q&A slide competes with the person answering.
- **caps** — No list caps. Title cap ~20 characters at 88 in the 512px half-width box (`512/(88*0.62) ≈ 9` per line — "Questions" fits, "Questions & Answers" needs two lines or the full-width variant).
- **image treatment** — **aspect-fill** into 640×720 (0.89, near-square). **Text protection = reserved zone**: the title lives in the left half, off the photograph entirely. No scrim and no card exist on this template — if the photo needs to bleed full-width, that is `image-bleed-caption`, not this.

### appendix-divider
- **zones** — full-bleed section ground `0,0,1280,720` (a distinct ground from the content slides — this is one of the templates that supplies the deck's required ground variation) · `title 64,464,1152,80` · `subtitle 64,560,760,40` · optional index number `64,392,200,48`.
- **focal** — the title. Wins on **scale** (72 against 20), **position** (low-left, a deliberate break from the top-left title position every content slide uses) and **colour** (it sits on an inverted ground, so it is the highest-contrast mark in the frame).
- **type** — `title→72/1.1` tracked −0.02em · `subtitle→20/1.4` · index number `→48` if used.
- **accent** — the index number, or `none`. The inverted ground is already doing the marking work; adding an accent on top of a drenched ground is the accent spent twice.
- **ux** — Tells the audience the argument has ended and reference material has started, so nobody mistakes an appendix chart for a headline claim.
- **avoid** — Do not use it as a general section break mid-argument if the deck already has a section-break template. Two divider styles in one deck reads as inconsistency, not variety.
- **caps** — No list caps. Title cap ~50 characters (`1152/(72*0.62) ≈ 25` per line, two lines). Subtitle cap ~140 characters at 20 over 760px.

### live-price
- **zones** — `title 64,56,1152,72` · `widget frame 240,152,800,440` — centred, fixed, reserved whether or not the widget resolves · `caption 64,624,1152,40`.
- **focal** — the live price inside the widget. Wins on **scale** (the widget's own headline figure is the largest mark on the slide), **position** (optically centred in the frame) and **isolation** (a bordered frame on otherwise empty ground).
- **type** — `title→32` · `caption→20/1.35` · widget-internal type is the widget's, but the frame must be sized so its headline value renders ≥72 and its labels ≥18 at 1280×720.
- **accent** — the widget frame's border or the live-state indicator dot — one mark, not both. If the widget renders its own accent internally, the frame stays `neutral` and the accent is spent inside the widget.
- **ux** — Shows the room the market's live view of the company during an investor day or AGM, which is the one thing a static deck cannot claim.
- **avoid** — Do not use it when the market is closed or the session is pre-recorded. A live-price widget showing a stale close, with no indication it is stale, is worse than a chart.
- **caps** — No list caps. The 800×440 frame is the minimum that carries a ≥72px figure plus labels; do not shrink it to fit a second element on the slide.
- **failure behaviour** — The frame is **reserved geometry**: on load failure, timeout, or market-closed, the layout does not reflow and the box does not collapse. It renders a static fallback inside the same 800×440 box — last-known price, the explicit as-at timestamp, and a `muted` "Live data unavailable" label at 20px — and the caption stays put. Never a blank frame, never a raw error string, never a slide that silently re-centres the caption because the widget vanished.

### live-poll
- **zones** — `title 64,56,1152,72` (carries the question) · `widget frame 64,160,832,456` — results bars, left-weighted · `join panel 928,160,288,456` holding a QR code at `960,192,224,224` and a short join URL at `928,440,288,64` · `caption 64,640,1152,40`.
- **focal** — the leading result bar. Wins on **scale** (longest bar), **colour** (the single accent) and **position** (top of the stack). Before votes arrive the focal falls back to the QR panel, which is correct — at that moment the job is to get people to vote.
- **type** — `title→32/1.2` (the question, up to two lines) · `option label→20` · `percentage→24` · `join URL→24` · `caption→18`.
- **accent** — the leading bar. Every other bar `muted`. Do not also accent the QR panel.
- **ux** — Turns the room into data in real time, so the next slide can respond to what the audience actually thinks.
- **avoid** — Do not use it for a question with more than 5 options: `456/5 ≈ 91px` per row is the floor for a 24px percentage beside a 20px label. Six options force the labels below 18.
- **caps** — No list caps in the contract, but the widget config should cap at **5 options** for this geometry. State it in the config rather than discovering it on stage.
- **failure behaviour** — The 832×456 frame is reserved. On failure it renders the question restated at 32 with a `muted` "Results will be shown live" line and the QR/URL panel **still live** at full size, because the join path and the results path fail independently — losing the results display must not lose the ability to vote. If the poll service is down entirely, the panel shows the join URL as plain readable text at 24 so the presenter can read it aloud. No reflow, no collapsed box.

### live-qa
- **zones** — `title 64,56,1152,72` · `question feed 64,160,832,456` — up to 5 rows at 88 with 8px gaps · `submit panel 928,160,288,456` with QR at `960,192,224,224` and short URL at `928,440,288,64` · `caption 64,640,1152,40`.
- **focal** — the top question in the feed. Wins on **position** (first row), **scale** (rendered at 24 against 20 for the rest) and **spacing** (16px extra padding above it, separating it from the queue).
- **type** — `title→32` · `top question→24/1.35` · `queued questions→20/1.35` · `asker attribution→18 muted` · `join URL→24` · `caption→18`.
- **accent** — the top question's row marker. The queue stays `neutral`.
- **ux** — Surfaces the room's actual questions so the session answers what was asked rather than what was anticipated.
- **avoid** — Do not use it without a moderation step configured. An unmoderated live feed projected at an AGM is a governance incident waiting for one bad submission.
- **caps** — No list caps in the contract; the geometry caps the visible feed at **5 questions** (`5 × 88 + 4 × 8 = 472`, just over the 456 band — so **5 rows at 80** or 4 rows at 88). Recommend documenting **5 visible rows at 80px** with the remainder held in the queue.
- **failure behaviour** — The 832×456 feed frame is reserved. On failure it renders a `muted` "Questions are being collected" line at 24 centred in the frame, with the submit panel still showing the QR and readable URL — collection continues even when the display does not. If submission itself is down, the panel switches to a plain-text fallback channel (the caption slot's email/handle) at 24. Layout is identical in both states; nothing moves.

### live-ticker
- **zones** — `title 64,56,1152,72` · `ticker band 0,296,1280,128` — full-bleed horizontal strip, the only full-bleed element on the slide · `caption 64,472,1152,40` · large empty ground above and below the band by design.
- **focal** — the ticker's live figure. Wins on **scale** (96px inside a 128px band), **isolation** (a full-bleed strip cutting the slide, with nothing else on its line) and **colour** (the band's ground inverts against the slide's).
- **type** — `title→32` · `ticker value→96` · `ticker label→20` caps tracked 0.08em · `caption→18/1.35`.
- **accent** — the ticker value. Nothing else on the slide takes colour.
- **ux** — Keeps one number honest and current while the deck sits on screen, so the figure is never a claim about a moment that has passed.
- **avoid** — Do not use it for a figure that does not actually move during the session. A "live" ticker showing an unchanged number for an hour trains the room to ignore it — and to wonder what else in the deck is decorative.
- **caps** — No list caps. Value cap ~13 characters at 96 across the 1152px inner band, but the visual argument breaks past ~8; keep it to a single figure with a unit.
- **failure behaviour** — The 1280×128 band is reserved and always renders. On failure it holds the last-known value with an explicit "as at HH:MM" label at 20 and drops the live indicator, so a stale number is never presented as current. If there is no last-known value, the band renders the label alone at 32 with a `muted` "Updating" state — the band never collapses, because a full-bleed strip disappearing would leave the title and caption 176px apart with a hole between them.

### offer-details
- **zones** — `title 64,56,1152,72` · `table 240,152,800,456` — narrowed and centred, because a terms table with two columns across 1152px puts 900px of white between label and value · `footnote 64,632,1152,48` — **mandatory**.
- **focal** — the offer price row. Wins on **weight** (600 against 400), **scale** (its value set one step up, 28 against 20) and **position** (first body row, directly under the header rule).
- **type** — `title→32` · `table header→20` caps tracked 0.06em · `table cell→20` · `offer price value→28` · `footnote→18`.
- **accent** — the offer price value. Every other row `neutral` — accenting the discount as well is the accent spent twice and reads as selling rather than disclosing.
- **ux** — States the terms of the raise in one checkable frame: price, size, ratio, record date, structure.
- **avoid** — Do not use it to present the price without the basis (discount to last close / to TERP, and which). A price with no reference point is the single most-queried omission on this slide.
- **caps** — No list caps. Table cap = header + **8 body rows** at 800px wide. **Slot gap worth fixing:** `footnote:text?` is optional while the `[CAVEAT]` marking makes it mandatory — recommend `footnote:text!` on every `[CAVEAT]` template, matching how `[SOURCE]` templates already require `source:text!`.
- **caveat** — The mandatory footnote sits in the `64,632,1152,48` strip at 18px `neutral` on the title's left margin, ≥4.5:1, up to two lines (~110 characters per line). It carries the not-an-offer / jurisdiction / full-terms-in-the-offer-document qualification. Legible at reading distance — this is the slide where a hidden caveat is an actual legal exposure, not a styling preference.

### use-of-funds
- **zones** — `title 64,56,1152,72` · `chart 64,160,480,448` (donut or 100% stacked bar, direct-labelled) · `table 592,152,624,456` (application / amount / % of raise) · `footnote 64,632,1152,48`.
- **focal** — the largest allocation — its chart segment and its table row read as one mark. Wins on **scale** (largest segment), **colour** (the single accent) and **position** (segment starting at 12 o'clock, row pinned first).
- **type** — `title→32` · `chart segment labels→18` direct on or beside the segment, no separate legend · `table header→20` caps tracked · `table cell→20` · `footnote→18`.
- **accent** — the largest allocation, marked once — segment or row, not both. Pair with a direct label so the largest slice is identifiable without colour.
- **ux** — Answers the first question every investor asks about a raise — where does the money go — with the proportions visible rather than listed.
- **avoid** — Do not let "general working capital" be the largest segment. If it is, the slide is telling the audience the raise has no plan; restructure the categories or expect the question.
- **caps** — No list caps. Table cap = header + **8 body rows**. Chart cap **6 segments** — below 6% of a 480px donut a direct label at 18 cannot be placed without a leader line, and leader lines at this size collide. Aggregate the tail into "Other" with the detail in the table.

### sources-and-uses
- **zones** — `title 64,56,1152,72` · `sources table 64,152,552,456` and `uses table 664,152,552,456`, gutter 48 (616→664) · `footnote 64,632,1152,48`.
- **focal** — the two totals, read as one mark because they must be equal. Wins on **weight** (600 against 400), **position** (bottom row of each table, on the same Y baseline — the shared baseline is what makes them read as a single statement) and **spacing** (a 16px rule and 8px extra padding above both).
- **type** — `title→32` · `column header→20` caps tracked 0.06em · `table cell→20` tabular-lining right-aligned · `total row→24` · `footnote→18`.
- **accent** — the matched total figures, as one set (both totals take it together — they are one semantic mark, and accenting only one would imply they differ).
- **ux** — Shows the funding structure from both sides at once so a reader can verify the balance rather than take it on trust.
- **avoid** — Do not use it when the two sides do not actually balance. The layout's entire argument is the equality; an unbalanced sources-and-uses slide destroys more credibility than it discloses.
- **caps** — No list caps. Cap = header + **8 body rows per side**, and the two tables must be padded to the same row count so the total rows land on the same Y. Unequal row counts break the shared baseline that carries the focal.

### cap-table-prepost
- **zones** — `title 64,56,1152,72` · `pre table 64,168,536,440` under a `pre label 64,128,536,32` · `post table 680,168,536,440` under a `post label 680,128,536,32` · a centred delta marker (arrow or "→") at `600,360,80,32` in the 80px gutter (600→680) · bottom strip `64,632,1152,48` reserved for the mandatory caveat.
- **focal** — the post-raise ownership percentage of the existing holders — i.e. the dilution. Wins on **position** (right table, read second, which is where a before/after argument resolves), **colour** (the single accent) and **weight** (600 against 400). The delta marker in the gutter directs the eye across.
- **type** — `title→32` · `pre/post labels→20` caps tracked 0.08em · `table header→20` · `table cell→20` tabular-lining · `caveat→18`.
- **accent** — the diluted percentage in the post table. Not the delta marker, not the pre table.
- **ux** — Makes dilution explicit and side-by-side rather than described in a sentence nobody will re-read.
- **avoid** — Do not use it when pre and post have different row sets. The comparison only works when every row exists on both sides; a row that appears only post-raise must still be shown pre-raise at zero.
- **caps** — No list caps. Cap = header + **8 body rows per side**, padded to equal counts so rows align across the gutter (misaligned rows across a before/after pair read as broken, not varied). **Slot gap worth fixing — this one is real:** the template is `[CAVEAT]` but has **no `footnote` slot at all** (`title` · `pre.rows` · `post.rows` only). The mandatory footnote has nowhere to bind. Add `footnote:text!`.
- **caveat** — Reserve `64,632,1152,48` at 18px `neutral` for it regardless, and bind it once the slot exists. It states the illustrative basis, the assumed take-up, and that actual dilution depends on final allocation. Legible at 18 on the title's left margin — a dilution caveat set as a hairline is exactly the disclosure a regulator reads first.

### dilution-waterfall
- **zones** — `title 64,56,1152,72` · `chart 64,168,1152,376` (waterfall: opening shares → each issue step → closing shares, direct value labels above each bar) · `takeaway 64,568,896,56` — one sentence, set as a statement not a caption · `footnote strip 64,640,1152,40`.
- **focal** — the closing (post-raise) bar. Wins on **scale** (tallest bar by construction), **position** (rightmost, where a waterfall terminates and the eye stops) and **colour** (the single accent).
- **type** — `title→32` · `bar value labels→20` direct above each bar · `step labels→18` below the axis, two lines allowed · `takeaway→24/1.35` · `footnote→18`.
- **accent** — the closing bar. Every intermediate step `neutral`, the opening bar `muted`.
- **ux** — Steps the audience through exactly how the share count gets from where it is to where it will be, so dilution is arithmetic rather than assertion.
- **avoid** — Do not use it with more than 6 steps. `1152/6 ≈ 192px` per bar is already the floor for an 18px two-line step label; a 7-step waterfall forces the labels to rotate, and rotated labels at 18 on a projector are unreadable.
- **caps** — No list caps. Chart cap **6 steps** (opening + 4 movements + closing). **Slot gap worth fixing:** `[CAVEAT]` but the only text slot below the chart is `takeaway:text?` — a takeaway is a claim, not a caveat, and the two must not share a slot. Add `footnote:text!` and keep `takeaway` for the argument.
- **caveat** — Reserve `64,640,1152,40` at 18px `neutral` for the mandatory footnote (assumed take-up, options/rights treatment, illustrative basis). It sits below the takeaway on the same left margin, legible, not folded into the takeaway sentence.

### raise-timeline
- **zones** — `title 64,56,1152,72` · horizontal axis rule at `64,368,1152,2` · six event nodes on the rule at `x = 64 / 288 / 512 / 736 / 960 / 1184`, marker 16×16 centred on the rule · `date labels` above the rule in `y 280..352` boxes 192 wide · `event labels` below in `y 392..488` boxes 192 wide, up to three lines · `footnote strip 64,632,1152,48`.
- **focal** — the record date node (or the close, depending on the audience). Wins on **scale** (a 24px marker against 16px for the rest), **colour** (the single accent) and **weight** (its label at 600 against 400). One node is promoted; the others are equal.
- **type** — `title→32` · `date→20` weight 550 · `event label→18/1.3`, up to three lines · `footnote→18`.
- **accent** — the promoted node's marker and its date, as one mark.
- **ux** — Gives holders the dates they have to act on, in the order they arrive, so nobody misses a record date because it was buried in a paragraph.
- **avoid** — Do not use it for indicative dates without saying so. A timeline reads as commitment; an unlabelled indicative timeline is the most common source of "you said the 14th" complaints.
- **caps** — `events max 6` is right and is a hard geometric ceiling: `1152/6 = 192px` per node, which at 18px holds ~18 characters per line over three lines (~54 characters per event). A 7th node drops the column to 164px and forces two-line dates. Do not raise the cap; split a longer schedule into "Offer" and "Settlement" slides.
- **caveat** — `[CAVEAT]` template with **no `footnote` slot** (`title` · `events` only). Reserve `64,632,1152,48` at 18px `neutral` for the mandatory "dates are indicative and subject to change / ASX Listing Rules" line and add `footnote:text!` to the contract. On a dates slide this caveat is the whole legal point of the footnote — it cannot be optional.

### cornerstone-support
- **zones** — `title 64,56,1152,72` · `commitment 64,152,1152,120` — the headline commitment figure and its sentence, given its own band · `investor grid 64,304,1152,288` as 3 columns × 2 rows, cell 368×136, gaps 24/16 (`x = 64 / 456 / 848`, `y = 304 / 456`) · `source strip 64,632,1152,48`.
- **focal** — the commitment figure in the top band. Wins on **scale** (72px against 24 for investor names), **position** (above the grid, first after the title) and **spacing** (a 120px band with 32px clear below). The named investors are the evidence; the total is the claim.
- **type** — `title→32` · `commitment figure→72` · `commitment sentence→24/1.4` · `investor name→24` · `investor descriptor→18 muted` · `source→18`.
- **accent** — the commitment figure. Investor names stay `neutral` — accenting a named third party reads as the company styling someone else's endorsement.
- **ux** — Shows that credible money has already committed, which is the strongest available signal to the investors being asked next.
- **avoid** — Do not name an investor who has not consented in writing to be named. This is the one template where the failure mode is a legal one, not a design one.
- **caps** — `investors max 6` is right for the 3×2 grid at 368×136 — a name at 24 gets ~24 characters per line with room for a descriptor. A 4×2 grid would drop cells to 270px and force institutional names to wrap awkwardly. Keep 6.
- **source** — `source:text!` in the `64,632,1152,48` strip at 18px `neutral`, recording that commitments are subject to definitive documentation and naming the as-at date. It is legible on the slide, not deferred to the appendix — an uncaveated cornerstone claim is the exact shape of a misleading statement.

### valuation-bridge
- **zones** — `title 64,56,1152,72` · `chart 64,160,704,448` (waterfall: pre-money → each step → post-money) · `table 792,160,424,448` (the same steps as figures) · `footnote 64,632,1152,48`.
- **focal** — the post-money bar. Wins on **position** (rightmost terminal bar), **scale** (tallest by construction) and **colour** (the single accent).
- **type** — `title→32` · `bar value labels→18` direct · `step labels→18` below axis · `table header→20` caps tracked · `table cell→20` · `footnote→18`.
- **accent** — the post-money bar (or its table row — one, not both).
- **ux** — Names every step between pre-money and post-money so the valuation is a construction the audience can follow rather than a number to accept.
- **avoid** — Do not use it when a step is an unexplained adjustment. A waterfall with a "other/adjustments" bar carrying meaningful value is the version of this slide that generates more questions than it answers.
- **caps** — No list caps. Chart cap **5 steps** in a 704px plot (`704/5 ≈ 140px` per bar — the floor for an 18px two-line label). Table cap = header + **8 body rows** in 424px width. **Slot gap:** `footnote:text?` optional under a `[CAVEAT]` marking — should be `footnote:text!`.
- **caveat** — The mandatory footnote sits in the `64,632,1152,48` strip at 18px `neutral`, stating the valuation basis and that it is illustrative. Full width, up to two lines, legible on the title's left margin — never set in `muted` grey, which on a tinted ground is the most common contrast failure in generated decks.

### comparable-transactions
- **zones** — `title 64,56,1152,72` · `table 64,152,1152,456` full width, five to six columns (date / target / acquirer / consideration / multiple / premium), header 56 + 8 rows at 48 · `source strip 64,632,1152,48`.
- **focal** — the multiple column. Wins on **position** (the terminal analytic column, right-aligned), **weight** (600 on the figures) and **alignment** (tabular-lining figures forming one vertical edge). If a median row exists, it takes the focal instead, on weight + a separating rule above it.
- **type** — `title→32` · `table header→20` caps tracked 0.06em, two lines allowed for long column names · `table cell→20`, figures tabular-lining right-aligned, text columns left-aligned · `source→18`.
- **accent** — the median (or mean) row, if present. If the table is transactions only: `none` — accenting a favourable precedent is thumb-on-scale.
- **ux** — Frames the deal or raise against what the market has actually paid for comparable assets, so the pricing has a precedent rather than a rationale.
- **avoid** — Do not use it with fewer than four transactions. Three precedents is an anecdote, and a median of three invites the question of what was excluded.
- **caps** — No list caps. Table cap = header + **8 body rows** with the source strip in place — so 7 transactions plus a median row, or 8 transactions with the median in the footnote. Six columns across 1152px gives ~192px each; target and acquirer names longer than ~18 characters at 20 will need abbreviating, which should be done in the data, not by shrinking type.
- **source** — `source:text!` in the `64,632,1152,48` strip at 18px `neutral`, naming the data provider, the screen criteria, and the as-at date. The screen criteria matter more than the provider here — an unstated selection rule is what makes a comparables table arguable. Legible at 18, not compressed to fit another row.

### subscription-summary
- **zones** — `title 64,56,1152,72` · `KPI row 64,152,1152,144` as three cells of 368 with 24 gaps (`x = 64 / 456 / 848`) — raised / take-up / scale-back · `table 64,320,1152,288` (allocation by holder class), header 56 + 4 rows at 48 · `footnote 64,632,1152,48`.
- **focal** — `kpi.1`, the amount raised. Wins on **scale** (72px against 20px labels), **position** (first cell, top-left of the row) and **spacing** (the KPI band sits alone with 24px clear above the table).
- **type** — `title→32` · `stat.value→72` · `stat.label→20` caps tracked 0.08em · `table header→20` caps tracked · `table cell→20` · `footnote→18`.
- **accent** — the take-up percentage (`kpi.2`), because that is the slide's actual argument — the raise amount was already known. `kpi.1` wins the focal on scale and position without the accent.
- **ux** — Reports how the raise actually landed — how much, from whom, and who got scaled back — so holders learn the outcome from the company rather than from their broker.
- **avoid** — Do not use it to report a shortfall without naming the shortfall. A "subscription summary" that omits the underwritten portion or the unsubscribed balance reads as a result being managed.
- **caps** — No list caps. 3 KPIs is right at 368px cells (72px values, ~8 characters). Table cap with the KPI row in place = header + **4 body rows** (`56 + 4×48 = 248 ≤ 288`) — materially tighter than the 8 rows a table-only template gets. Recommend the catalogue state this: on any KPI-row + table template, the table cap halves.

### escrow-schedule
- **zones** — `title 64,56,1152,72` · `table 64,152,1152,456` full width (holder class / securities / % of issued / release date / condition), header 56 + 8 rows at 48 · `footnote 64,632,1152,48`.
- **focal** — the release-date column. Wins on **position** (the column the audience came for, placed at the terminal right), **weight** (600 on the dates) and **alignment** (a single right-edge column of dates the eye can run down).
- **type** — `title→32` · `table header→20` caps tracked 0.06em · `table cell→20`, dates and percentages tabular-lining · `footnote→18`.
- **accent** — the nearest release date row. Everything further out stays `neutral` — that row is the only one that changes anyone's behaviour this quarter.
- **ux** — Tells the market exactly when restricted stock becomes free, so the overhang is a known date rather than a rumour.
- **avoid** — Do not use it with release dates expressed only as conditions ("on satisfaction of milestone X"). A schedule with no dates is a list; if the dates are genuinely conditional, give both a condition column and an earliest-possible date.
- **caps** — No list caps. Table cap = header + **8 body rows**. Five columns across 1152px gives ~230px each, comfortable at 20. **Slot gap:** `footnote:text?` optional under a `[CAVEAT]` marking — should be `footnote:text!`.
- **caveat** — The mandatory footnote sits in the `64,632,1152,48` strip at 18px `neutral`, stating the ASX Listing Rule basis and that dates are subject to the escrow deeds. Two lines maximum, on the title's left margin, ≥4.5:1 — legible, because this is the caveat that qualifies every date above it.

### pathway-to-listing
- **zones** — `title 64,56,1152,72` · five phase columns of 216 with 18px gaps (`x = 64 / 298 / 532 / 766 / 1000`), `y 200, h 320` · a connecting rule at `64,192,1152,2` running behind the phase heads · status marker 24×24 at the top of each column on the rule · `footnote strip 64,632,1152,48`.
- **focal** — the current phase column. Wins on **colour** (the single accent on its status marker and heading), **weight** (heading at 600 against 400 for the others) and **position** — the completed phases behind it are `muted`, so it is the first non-dimmed column in the LTR scan. Never encode completed/current/remaining in colour alone: use a filled / half / hollow marker shape as well.
- **type** — `title→32` · `phase heading→24/1.2` · `phase detail→18/1.35`, up to five lines · `phase status label→18` caps tracked 0.08em · `footnote→18`.
- **accent** — the current phase's status marker and heading, as one mark.
- **ux** — Shows a pre-IPO audience what has already been done and what is left, so readiness is a position on a path rather than a promise.
- **avoid** — Do not use it when three of five phases are still open. A pathway slide that is mostly ahead of you argues the opposite of what it intends; use a milestones list without the progress framing.
- **caps** — `phases max 5` is right and is the geometric ceiling: `216px` per column at 18 holds ~20 characters per line. A 6th phase drops the column to 178px (~17 characters) and the phase headings at 24 start breaking mid-word. Keep 5.
- **caveat** — `[CAVEAT]` template with **no `footnote` slot** (`title` · `phases` only). Reserve `64,632,1152,48` at 18px `neutral` for the mandatory "indicative timetable, subject to regulatory approval and market conditions — no assurance the listing will proceed" line, and add `footnote:text!` to the contract. On a pre-IPO slide this is the most legally load-bearing sentence on the page and it currently has nowhere to go.

### agm-agenda
- **zones** — title `64,64,1152,80`; 2px rule at `y=168` spanning `64→1216`; index gutter `64,200,48,400`; item column `120,200,832,400` (10 rows, 40 pitch); right `256px` deliberately empty as the slide's only air.
- **focal** — the title word. Wins on scale (48 against 24 body, 2×) and spacing (80px of clearance beneath it, wider than any inter-item gap), reinforced by top-left position. The list is explicitly not the focal — it is a menu, read at leisure.
- **type** — title 48/600 → item 24/450 → index numeral 18/550 caps-tracked +0.08em.
- **accent** — the rule under the title. One element, one use.
- **ux** — gives the room the shape of the meeting before anything is put to a vote.
- **avoid** — not a running position indicator; it has no current-item state. Use `agenda-progress` for that.
- **caps** — `max 10` fits geometrically (10 × 40 pitch bottoms out at `y=600`), but 10 items at 24px is a wall from the back of a room. Keep the hard max at 10, treat 8 as the working ceiling.

### resolutions-list
- **zones** — title `64,56,1152,64`; table `64,152,1152,448` (header 56 + 7 rows @ 56); columns resolution-no `112` / resolution name `560` / board recommendation `240` / notes `240`; footnote `64,624,1152,40`.
- **focal** — the resolution-name column. Wins on width (560, half the table), weight (550 against 450 in every other cell) and position (leftmost text column, so every other column is read relative to it).
- **type** — title 36/600 → column head 18caps/550 +0.08em → resolution name 20/550 → cell 18/450 (16 hard floor) → footnote 18/400 muted.
- **accent** — none. Colour on one resolution row reads as endorsement, which is a governance claim the template has no right to make.
- **ux** — lets a holder find the resolution they care about, and how the board frames it, before the poll opens.
- **avoid** — do not use for outcomes; results belong in `proxy-results`. And never accent a row.
- **caps** — 7 body rows is the geometric ceiling at 56 pitch. `footnote:text?` is optional in the slot list but the `[CAVEAT]` marking requires it — the contract should be `footnote:text!`.

### proxy-results
- **zones** — title `64,56,1152,56`; chart `64,144,672,400` (100% stacked horizontal bars, one per resolution, direct-labelled, 0–100 axis); table `768,144,448,392` (header 56 + 7 rows @ 48); source `64,624,1152,32`.
- **focal** — the single resolution with the lowest "for" percentage. Wins on accent (the only coloured segment on the slide), on scale (its bar is the widest object in a 672px field) and on position (first in the LTR read).
- **type** — title 36/600 → direct percentage label 24/600 → series label 18/500 → cell 18/450 (16 floor) → source 18/400 muted.
- **accent** — the against/abstain segment of that one lowest bar. Everywhere else, for/against is carried by position and label, never by colour alone.
- **ux** — shows how the register already voted, before the room is asked.
- **avoid** — never truncate the percentage axis; the 0–100 span is the whole point. Do not drop abstentions because they are small.
- **caps** — table 7 rows. Source line is mandatory and sits full-width at `y=624`, 18px, clear of the table's `y=536` bottom by 88px — legible, never a hairline caption.

### chair-address
- **zones** — photo full-bleed left `0,0,448,720`; title `512,96,640,96`; attribution `512,200,640,32`; body `512,256,640,360` (24/1.5 ≈ 44 chars per line, 10 lines). Photo absent → body column re-anchors to `64,256,1000,360` and the left third becomes flat ground.
- **focal** — the address's opening claim, set as the title. Wins on scale (40 against 24 body), on colour role (full-strength `neutral` while the body sits `muted`) and on the photo's vertical edge acting as a rule pointing into it.
- **type** — title 40/600 → attribution 18caps/550 +0.08em → body 24/450, line-height 1.5.
- **accent** — none. A portrait plus an accent is two things competing for a slide with one job.
- **ux** — carries the chair's framing of the year in the words the market will quote back.
- **avoid** — not a transcript. The box holds ~440 characters; the rest is spoken.
- **caps** — no cap stated on `body`. It needs one: ~440 characters at 24px in `640,360`. Add `body` max ≈ 440 chars to the contract.

### ceo-address
- **zones** — mirror of `chair-address`: photo `832,0,448,720`; title `64,96,640,96`; attribution `64,200,640,32`; body `64,256,640,360`. The mirror is deliberate — the two addresses read as a pair without reading as a repeat.
- **focal** — the opening claim as title. Same vectors: scale (40 vs 24), colour role (`neutral` title against `muted` body), plus the photo edge on the opposite side closing the composition inward.
- **type** — title 40/600 → attribution 18caps/550 +0.08em → body 24/450 at 1.5.
- **accent** — none.
- **ux** — gives the operating narrative a face and a single quotable line.
- **avoid** — do not run chair and CEO on the same side of the canvas; identical geometry back-to-back reads as a rendering fault.
- **caps** — same missing `body` cap as `chair-address`: ~440 chars.

### voting-instructions
- **zones** — title `64,72,896,72`; three steps stacked `64,208,736,336` (3 rows @ 112); QR `864,208,288,288`; QR caption `864,512,288,32`. QR absent → steps widen to `64,208,1000,336`.
- **focal** — the QR block. Wins on scale (288² is the largest single object), position (isolated in the right column behind a 128px gutter) and spacing (nothing else occupies its quadrant). QR absent → focal falls to step 1's numeral, promoted to 40/600.
- **type** — title 36/600 → step numeral 32/600 → step text 24/450 → QR caption 18/450.
- **accent** — the QR frame. Once. Step numerals stay neutral.
- **ux** — gets a holder from "I am in the room" to "my vote is lodged" without asking a question aloud.
- **avoid** — not a procedures manual. Three steps means three; a fourth means the process needs fixing, not a slide.
- **caps** — `max 3` is right. Each step gets 112px, which is two lines at 24px — enough for one instruction, not enough for a caveat.

### remuneration-summary
- **zones** — title `64,56,1152,56`; chart `64,152,544,384` (fixed vs at-risk, stacked, max 3 series); table `656,152,560,384` (header 56 + 5 rows @ 64); source `64,624,1152,32`. Split intentionally differs from `proxy-results` so the two AGM chart-plus-table slides do not render as the same slide twice.
- **focal** — the largest total-remuneration bar. Wins on scale (tallest element in the chart field), weight (its direct label at 600 while the rest sit 450) and accent.
- **type** — title 36/600 → direct value label 24/600 → axis/series label 18/500 → cell 18/450 (16 floor) → source 18/400 muted.
- **accent** — that one bar's at-risk segment. Fixed vs at-risk is otherwise separated by position and label.
- **ux** — puts the remuneration report's numbers on the wall before the discussion the law requires.
- **avoid** — never omit the statutory total in favour of a "realised pay" figure alone; the two must sit in the same table.
- **caps** — table 5 rows, chart ≤3 series. More series and the 544px plot loses direct labelling and needs a legend, which is worse.

### director-election
- **zones** — portrait `64,64,384,480` (4:5); name `496,96,720,64`; role `496,168,720,32`; tenure chip `496,216,240,40`; bio `496,280,688,264` (22/1.5 ≈ 52 chars/line, 8 lines ≈ 416 chars).
- **focal** — the candidate's name. Wins on scale (44/600 against 22 body), position (top of the text column, aligned to the portrait's upper third where the face sits) and spacing (32px clear above and below, more than any other gap).
- **type** — name 44/600 → role 24/500 → tenure chip 18caps/550 +0.08em → bio 22/450 at 1.5.
- **accent** — the tenure chip. One use, and it is the fact holders actually scan for.
- **ux** — lets a holder decide one candidate, on the record, in the time it takes to read a paragraph.
- **avoid** — never grid five candidates onto one slide. An election is per-person; a grid invites comparison the ballot does not offer.
- **caps** — bio ~416 chars. Longer text drops below 22px and breaks the 18px floor by the third resize.

### quarterly-highlights
- **zones** — title `64,64,1152,64`; KPI row `64,176,1152,224` (4 cells @ 264, 32 gutters); rule `y=432`; bullets `64,464,1000,176` (4 rows @ 44).
- **focal** — `kpi.1`'s value. Wins on scale (80/600 against 22 body), accent (the only coloured element) and position (first cell, top-left of the row).
- **type** — title 36/600 → KPI label 18caps/550 +0.08em → KPI value 80/600 → delta 20/500 → bullet 22/450.
- **accent** — `kpi.1` value or its delta marker. One.
- **ux** — hands the quarter to a reader in four numbers before a word of narrative.
- **avoid** — do not fill all four KPI slots to look complete. The optionals exist so three real figures beat four padded ones; a weak fourth dilutes the first.
- **caps** — `max 4` KPI is right, with a constraint the catalogue does not state: at 264px a stat only clears comfortable size up to ~8 characters (renderer arithmetic gives ~67px at 6 chars, ~29px at 14). Figures longer than 8 characters must use three cells at 362, not four.

### 4c-cash-summary
- **zones** — title `64,56,1152,56`; KPI pair stacked `64,144,544,224` (2 cells @ 112); table `656,144,560,448` (header 56 + 7 rows @ 56); footnote `64,624,1152,40`, full width, clear of the table's `y=592` bottom.
- **focal** — `kpi.1`, cash at quarter end. Wins on scale (72/600), accent, and isolation — it is the only object in the top-left quadrant.
- **type** — title 36/600 → KPI label 18caps/550 +0.08em → KPI value 72/600 → cell 18/450 (16 floor) → footnote 18/400 muted.
- **accent** — the closing-cash value. Once.
- **ux** — puts the 4C's two numbers that matter next to the reconciliation that produced them.
- **avoid** — quarters-of-runway is a derived figure; showing it without the basis in the footnote turns arithmetic into a promise.
- **caps** — table 7 rows. The template is marked `[CAVEAT]` but carries **no footnote slot at all** — the contract needs `footnote:text!` or the mandatory caveat has nowhere legible to go. Reserved band above.

### activities-summary
- **zones** — title `64,64,768,64`; bullets `64,176,672,400` (5 rows @ 80); image.1 `800,160,416,228`; image.2 `800,412,416,228`. Both images absent → bullets widen to `64,176,1000,400` at 88 pitch.
- **focal** — bullet 1, promoted to a lead line at 28/550 while bullets 2–5 sit at 22/450. Wins on scale, weight, and 32px of extra clearance beneath it that no other row gets.
- **type** — title 36/600 → lead bullet 28/550 → bullet 22/450 → image caption 18/450.
- **accent** — the lead bullet's marker only. The other four markers are neutral.
- **ux** — tells the operational story of a quarter with evidence beside it rather than after it.
- **avoid** — not a photo gallery. Each image must illustrate a named bullet; unlabelled site photography is decoration and reads as padding.
- **caps** — `max 5` fits at 80 pitch (two lines at 22px each). Six drops the pitch to 64 and single-line bullets start truncating.

### production-vs-guidance
- **zones** — title `64,56,1152,56`; KPI strip `64,136,1152,136` (3 cells @ 362, 32 gutters); chart `64,304,1152,288` with the guidance band drawn as a labelled reference band, not a legend entry; footnote `64,624,1152,40`.
- **focal** — the variance figure in `kpi.1` (actual against guidance). Wins on scale (72/600 in a 362 box), accent (sole coloured element), and position (first cell, top-left of the strip).
- **type** — title 36/600 → KPI label 18caps/550 +0.08em → KPI value 72/600 → chart direct label 20/550 → footnote 18/400 muted.
- **accent** — the variance value. If the variance is a miss, it still takes the accent — the accent marks salience, not good news.
- **ux** — shows delivery against the number the market is already holding you to.
- **avoid** — never rebase the value axis so a miss reads as a hit. That is a defect, not a chart style.
- **caps** — 3 KPI at 362 is generous and correct. `footnote:text?` should be `footnote:text!` given the `[CAVEAT]` marking.

### exploration-update
- **zones** — title `64,56,1152,56`; table `64,144,1152,448` (header 56 + 7 rows @ 56); columns prospect `288` / activity `320` / result `320` / next step `224`; source `64,624,1152,32`.
- **focal** — one result cell: the intercept or assay the slide exists for. Wins on weight (600 against 450 in every sibling cell), scale (that cell set one step up at 24 against 18) and accent.
- **type** — title 36/600 → column head 18caps/550 +0.08em → cell 18/450 (16 floor) → highlighted result 24/600 → source 18/400 muted.
- **accent** — that single result cell. Once.
- **ux** — answers "where did you drill, what did you find, what happens next" in one pass.
- **avoid** — never show the good hole without the hole list. If there is only one result, use a stat template and say so plainly.
- **caps** — 7 body rows at 56 pitch. Source line mandatory, full width at `y=624`, 88px clear of the table bottom.

### milestones-quarter
- **zones** — title `64,56,1152,56`; vertical hairline `x=640`, `y=160→600`; delivered `64,160,512,432` (head at 160, rows from 208 @ 72); next `704,160,512,432` (same rhythm).
- **focal** — the delivered column as a block, entered at its first row. Wins on position (left, first in LTR), weight (delivered items 550, next items 450 muted) and colour role (`neutral` vs `muted`) — the past is verified, the future is not, and the type says so.
- **type** — column head 18caps/550 +0.08em → delivered item 22/550 → next item 22/450 muted → title 36/600.
- **accent** — none. The left/right split already carries the meaning; accenting one milestone asserts a ranking the template does not have.
- **ux** — closes the quarter and opens the next one on the same surface, so drift is visible.
- **avoid** — do not date a "next" item unless it is committed. An implied date becomes guidance the moment the deck is lodged.
- **caps** — 5/5 at 72 pitch fits. Asymmetric fills (3 delivered, 5 next) are correct behaviour, not a gap to pad.

### tenement-map
- **zones** — map `416,56,800,560`; title `64,72,320,120`; legend `64,224,320,336` (6 rows @ 56, 20px swatch at `x=64`, label from `x=96`); source `64,624,1152,32` running under both columns.
- **focal** — the map. Wins on scale (62% of the canvas), position (occupying the optical centre-right) and by being the only image on the slide.
- **type** — title 32/600 → legend label 18/450 → map annotation 18/500 → source 18/400 muted.
- **accent** — one parcel: the tenement the slide is about, filled. Every other holding is a neutral outline. The matching legend row takes 550 weight, not a second colour.
- **ux** — makes the land position legible to someone who has never seen the licence numbers before.
- **avoid** — never render without a scale bar and a north arrow, and never without the register name and as-at date in the source line. Without those it is an illustration.
- **caps** — legend `max 6` at 56 pitch fits 336. More than six and you are mapping a portfolio, not a project — split the slide.

### drilling-results
- **zones** — title `64,56,1152,56`; table `64,144,1152,392` (header 56 + 6 rows @ 56); columns hole ID `160` / from-to `192` / interval `160` / grade `192` / coordinates `224` / comment `224`; two-line band `64,560,1152,88` — line 1 source 18/450, line 2 the JORC/competent-person caveat 18/400 muted, both left-aligned at `x=64`.
- **focal** — the single best intercept cell. Wins on weight (600 against 450), scale (24 against 18 siblings) and accent.
- **type** — title 36/600 → column head 18caps/550 +0.08em → cell 18/450 (16 hard floor) → highlighted intercept 24/600 → source 18/450 → caveat 18/400 muted.
- **accent** — that one intercept. Once.
- **ux** — reports assays in the form a technical reader can check rather than the form marketing prefers.
- **avoid** — never present the best intercept without the full hole list on the same slide. Cherry-picking is the exact failure this table exists to prevent.
- **caps** — 6 body rows. A full assay table is an annexure, not a slide. `[SOURCE CAVEAT]` but the slot list carries only `source:text!` — add `footnote:text!` for the caveat; the 88px band above reserves room for both lines.

### resource-reserve-table
- **zones** — title `64,56,1152,56`; table `64,144,1152,448` (header 56 + 5 rows @ 64 + total row 72, with a 2px rule above the total); columns category `256` / tonnes `224` / grade `224` / contained metal `224` / classification `224`; band `64,600,1152,72` for source line and JORC caveat.
- **focal** — the total row's contained-metal figure. Wins on weight (600), scale (24 against 18 cells), the 2px rule isolating the row, and terminal position at the table's foot.
- **type** — title 36/600 → column head 18caps/550 +0.08em → cell 18/450 (16 floor) → total 24/600 → source 18/450 → caveat 18/400 muted.
- **accent** — the total row's rule. Not the figure — the figure already wins on three vectors, and doubling up spends the accent on a fight already over.
- **ux** — states the estimate in the categories that make it a JORC estimate rather than a number.
- **avoid** — never collapse measured/indicated/inferred into one figure without the classification column. The category is what makes the number mean anything.
- **caps** — 5 category rows plus one total. Same missing `footnote` slot as `drilling-results` despite the `[CAVEAT]` marking.

### clinical-pipeline
- **zones** — title `64,56,1152,56`; phase column heads `64,152,1152,40` (4 columns @ 264, 32 gutters); programme rows `64,200,1152,400` (5 rows @ 80), each a bar starting at column 1 and ending at the phase actually entered, label set inside the bar's left; footnote `64,624,1152,40`.
- **focal** — the most advanced programme's bar. Wins on position (the only bar crossing into the final column), scale (longest object on the slide) and accent.
- **type** — title 36/600 → phase head 18caps/550 +0.08em → programme label 20/550 → phase-detail caption 18/450 → footnote 18/400 muted.
- **accent** — the lead bar's terminal segment. Once.
- **ux** — shows where each programme actually is, in the vocabulary regulators and specialists share.
- **avoid** — never let a bar imply a phase it has not entered. The footnote must define what "in phase N" means here — enrolled, dosed, first-patient-in are three different claims.
- **caps** — 4 phases × 5 programmes is the ceiling; 6 programmes at 80 pitch overruns the footnote band. Marked `[CAVEAT]` with **no footnote slot** — add `footnote:text!`.

### regulatory-milestones
- **zones** — title `64,56,1152,56`; axis `64,392,1152,2`; 5 nodes at 288 intervals from `x=176`; labels alternate above `256,y=256..376` and below `y=408..528` to keep 20px text from colliding; footnote `64,624,1152,40`.
- **focal** — the current position node. Wins on accent, on scale (24px marker against 16px siblings), on weight (its label 550 against 450) and on a vertical tick dropping to a "current" tag — four vectors, because on a timeline the eye otherwise defaults to the leftmost node.
- **type** — title 36/600 → node label 20/450 → current-node label 20/550 → date 18/500 → footnote 18/400 muted.
- **accent** — the current node and its tick, read as one mark.
- **ux** — locates the company on an approval pathway the audience only half knows.
- **avoid** — do not imply dates you do not hold. An undated future node must read as sequence, not schedule, and the footnote must state that approval timing is not within the company's control.
- **caps** — `max 5` at 288 spacing is correct; 6 collides labels at 20px. `[CAVEAT]` with **no footnote slot** — add `footnote:text!`.

### project-economics
- **zones** — title `64,56,1152,56`; KPI column `64,136,352,384` (4 cells @ 96); chart `448,136,768,384`; band `64,584,1152,72` — source line 18/450 then study caveat 18/400 muted.
- **focal** — NPV in `kpi.1`. Wins on scale (64/600 in a 352 box), accent, position (top-left, first read) and isolation from the chart by a 32px gutter.
- **type** — title 36/600 → KPI label 18caps/550 +0.08em → KPI value 64/600 → chart direct label 20/550 → source 18/450 → caveat 18/400 muted.
- **accent** — the NPV value. Once. IRR and payback stay neutral.
- **ux** — puts the study's four output numbers where a capital allocator looks first, with the sensitivity chart beside them.
- **avoid** — a study result is not a forecast. The caveat must name the study level (scoping / PFS / DFS) and its accuracy band, and NPV without its discount rate is not a number.
- **caps** — 4 stacked KPI at 96 pitch fits, and 352 width comfortably carries a 14-character figure (~38px). `[SOURCE CAVEAT]` with no `footnote` slot — the band reserves 72px for both lines; add `footnote:text!`.

### offtake-summary
- **zones** — title `64,56,1152,56`; table `64,144,1152,456` (header 56 + 6 rows @ 56 + total row 64, 2px rule above total); columns counterparty `288` / product `192` / volume `192` / term `192` / expiry `160` / status `128`; source `64,624,1152,32`.
- **focal** — the total contracted-volume figure in the total row. Wins on weight (600), the rule above it, and terminal position at the foot of a column of smaller values.
- **type** — title 36/600 → column head 18caps/550 +0.08em → cell 18/450 (16 floor) → total 24/600 → source 18/400 muted.
- **accent** — the total. Once.
- **ux** — shows how much of production is already sold, and until when.
- **avoid** — never name a counterparty without consent, and never drop the expiry column. An offtake with no end date reads as perpetual, which is the single most misleading omission available here.
- **caps** — 6 body rows plus total at 56 pitch. Seven would push the total row under the source band.

### plant-throughput
- **zones** — title `64,56,1152,56`; KPI strip `64,136,1152,152` (3 cells @ 362); chart `64,320,1152,272` with nameplate as a labelled horizontal reference line, direct-labelled at its right end; footnote `64,624,1152,40`.
- **focal** — the utilisation-against-nameplate KPI. Wins on scale (72/600), accent and first-cell position.
- **type** — title 36/600 → KPI label 18caps/550 +0.08em → KPI value 72/600 → reference-line label 18/550 → footnote 18/400 muted.
- **accent** — the utilisation value. Once. The nameplate line stays neutral — it is the benchmark, not the news.
- **ux** — shows whether the plant is doing what it was built to do, over enough periods to be honest.
- **avoid** — do not annualise one good month. The footnote must state basis: actual against run-rate.
- **caps** — 3 KPI is right for the geometry and for the metric set (throughput, utilisation, recovery).

### sensitivity-table
- **zones** — x-variable label `64,120,1152,32` (18caps); matrix `64,152,1136,392` (header 56 + 6 rows @ 56; label column 224 + 6 data columns @ 152); y-variable label rotated in the `24,152,40,392` gutter; footnote `64,624,1152,40`.
- **focal** — the base-case cell at the matrix centre. Wins on weight (600 against 450), a 2px outline no other cell carries, and accent. Position alone would not do it — the eye lands top-left in a grid, so the cell needs the outline to pull it.
- **type** — axis labels 18caps/550 +0.08em → column/row head 18/550 → data cell 20/450 → footnote 18/400 muted.
- **accent** — the base-case cell. Once.
- **ux** — shows how much the answer moves when the two inputs people argue about move.
- **avoid** — do not heat-map the grid by value. Shading reads as likelihood; this matrix shows arithmetic, not probability. The footnote must state that variables move one at a time with all else held.
- **caps** — 6×6 is the geometric ceiling: a 7th column drops cells to ~130px and figures wrap mid-number. `footnote:text?` should be `footnote:text!` under `[CAVEAT]`.

### scenario-3case
- **zones** — title `64,56,1152,56`; table `64,152,672,392` (header 56 + 6 metric rows @ 56; case columns are the table's columns); chart `768,152,448,392`. Chart absent → table widens to `64,152,1152,392` with column widths scaled proportionally. Footnote band reserved `64,616,1152,48`.
- **focal** — the base-case column. Wins on accent (its column ground tinted once, the slide's only colour), weight (600 against 450 in low and high) and centre position between two equals.
- **type** — title 36/600 → case head 20caps/550 +0.08em → metric label 18/450 → value cell 20/550 (16 floor) → footnote 18/400 muted.
- **accent** — the base column's tinted ground. Once — and note that the tint is the accent, so the base figures themselves stay neutral.
- **ux** — puts a range on the table without pretending any one number is the answer.
- **avoid** — never label these "forecast", and do not make low and high symmetric for neatness when the drivers are not.
- **caps** — 3 cases is fixed by the name; 6 metric rows is the geometric ceiling at 56 pitch. Marked `[CAVEAT]` with **no footnote slot** — add `footnote:text!`; the 48px band at `y=616` is reserved for it.

### assumptions-list
- **zones** — title `64,56,1152,56`; column A `64,152,544,448` (4 rows @ 112); column B `672,152,544,448` (4 rows @ 112). Each row: assumption text 20/450 left (~90 chars in 544), value right-aligned 24/550.
- **focal** — the title. Deliberate: the eight assumptions are rendered as equals, because promoting one tells the audience which seven they may skip. The title wins on scale (36 against 20) and on 96px of clearance above the first row.
- **type** — title 36/600 → assumption 20/450 → assumption value 24/550 → column rule label 18caps/550 +0.08em.
- **accent** — none, and this is a design decision rather than an omission. An accented assumption is an argument, and this slide's job is to be checkable.
- **ux** — makes every number elsewhere in the deck defensible by naming what it rests on.
- **avoid** — do not use it to bury the assumption that actually moves the answer. If one dominates, that belongs in `assumption-load-bearing`, not row six of eight.
- **caps** — `max 8` fits (two columns × 4 @ 112 pitch) and is also the comprehension ceiling. Nine would drop pitch below the two-line requirement.

### valuation-range
- **zones** — title `64,56,1152,56`; range band `64,176,1152,200` (horizontal band, ticks at low / mid / high); three KPI cells pinned under their ticks `64,416,256,144`, `512,416,256,144`, `960,416,256,144`; band `64,592,1152,72` — source 18/450 then caveat 18/400 muted.
- **focal** — the midpoint figure. Wins on scale (72/600 against 44/550 at the ends), position (centre, vertically locked to the mid tick) and accent on the mid tick alone.
- **type** — title 36/600 → range label 18caps/550 +0.08em → mid value 72/600 → end values 44/550 → driver caption 18/450 → source 18/450 → caveat 18/400 muted.
- **accent** — the mid tick. Once; the two end ticks are neutral.
- **ux** — states a valuation as a range with its ends explained, which is the only honest form for one.
- **avoid** — never render the range without naming what drives each end; a range with no drivers is a hedge. A broker or consensus range needs its source and as-at date or it reads as the company's own view.
- **caps** — 3 KPI maps exactly to low/mid/high. Do not add a fourth. `[SOURCE CAVEAT]` with no `footnote` slot — add `footnote:text!`; band reserved above.

### break-even
- **zones** — title `64,56,1152,56`; chart `64,152,768,400` with the crossing point marked by a 12px node and a leader running right; takeaway `880,200,336,240` (28/550, ~180 chars); footnote `64,624,1152,40`.
- **focal** — the crossing point. Wins on accent (the only coloured mark on the slide), on position (the convergence the eye finds without help) and on a direct label at 24/600 that no other chart point carries.
- **type** — title 36/600 → takeaway 28/550 → crossing label 24/600 → axis label 18/500 → footnote 18/400 muted.
- **accent** — the crossing node and its label, read as one mark.
- **ux** — names the volume or price at which the economics turn, and says it in words beside the chart.
- **avoid** — do not extend either line past the data you hold. If an extrapolated region is shown it must be visually distinct (dashed) — and the takeaway must state the level, not just the period.
- **caps** — takeaway ~180 chars at 28px in `336,240`. Marked `[CAVEAT]` with **no footnote slot** — add `footnote:text!`; the `y=624` band is reserved.

### risk-matrix
- **zones** — title `64,56,768,56`; plot `256,136,720,480` (5×5 or 3×3 grid); y-axis label rotated in `192,136,48,480`; x-axis label `256,624,720,32`; numbered key `1008,136,208,480` (6 rows @ 80). Risk items plot as 40px numbered nodes.
- **focal** — the node in the highest likelihood × highest impact cell. Wins on accent, on scale (that node one step larger at 48px) and on position (the corner the eye is trained to check first on a 2×2 logic).
- **type** — title 36/600 → axis label 18caps/550 +0.08em → node numeral 22/600 → key entry 18/450 → key numeral 18/600.
- **accent** — the top-right node. Once. Every other node is neutral with its number doing the identifying.
- **ux** — turns a risk register into something a board can argue about in the time available.
- **avoid** — never let colour alone carry severity. Number every node and repeat the number in the key; a projector will flatten a red/amber distinction anyway.
- **caps** — `max 6` is right; nodes cluster in the top-right cell, and a seventh overlaps at 40px. The 208px key caps risk names at ~24 characters — enforce it or key entries wrap into their neighbours.

### decision-request
- **zones** — decision statement `64,64,896,136` (2 lines at 36); decide-by chip `992,64,224,96` (18caps label + 32/600 date), the only element in the top-right quadrant and in the identical position across the whole family; options table `64,232,672,288` (header 56 + 4 rows @ 56, do-nothing included as a row); recommendation card `768,232,448,288` on a tinted ground with a 2px rule above it — not a left border; rationale inside that card from `y=392`; unlocks `64,552,1152,64` as one line at 22/500.
- **focal** — the decision statement. Wins on scale (36 against 20 body, the only text above 24), position (top-left, first read), spacing (32px of air beneath a 136px band) and by being the only full-width element on the slide. Four vectors, because on a slide dense with options the ask is the thing most easily lost.
- **type** — decision 36/600 → decide-by date 32/600 → decide-by label 18caps/550 +0.08em → recommendation 24/550 → options head 18caps/550 → options cell 18/450 (16 floor) → rationale 20/450 → unlocks 22/500.
- **accent** — the recommendation card's ground. Once. The matching options row is marked by weight (550) and a leading rule, never by a second use of colour.
- **ux** — states what the board is being asked to decide, what the alternatives cost, what is recommended, and when the answer is needed.
- **avoid** — do not omit the do-nothing option. A three-option table of things that all cost money is not a decision, it is a budget request wearing a decision's layout.
- **caps** — `max 4` options fits exactly (288 = header 56 + 4 × 56) and four including do-nothing is the real ceiling for a slide someone must decide from. Decision text ≤ ~150 chars at 36px in `896,136`.

### consequence-fork
- **zones** — premise `64,64,1152,96` (32/550, full width); divider hairline `x=640, y=192→560`; path A `64,208,512,352`; path B `704,208,512,352` — each carrying label 24caps at `y=208`, stat at `y=264`, outcome `,392,512,136`; footer bar `64,592,1152,56` with owner left and decide-by right.
- **focal** — the premise. Wins on scale (32 against 22 outcome text), on full-width position at the top, and on spacing (48px clear of both path columns). Deliberately *not* either path: the two paths must stay geometrically and typographically identical, or the slide has decided for the audience before it is asked.
- **type** — premise 32/550 → path label 24caps/550 +0.08em → path stat 72/600 → outcome 22/450 → owner 20/500 → decide-by 24/600.
- **accent** — the decide-by chip in the footer, and nothing else. If `decideBy` is absent, `none` — no accent may land on a path.
- **ux** — makes two futures comparable at a glance so the room argues about consequences rather than framing.
- **avoid** — do not use it when the choice is already made. A fork that visually favours one path is `decision-request` in costume, and the audience will read the tilt before the text.
- **caps** — two paths is structural. Outcome ~200 chars per side at 22px in `512,136`. The decide-by chip sits bottom-right at 24/600 — findable in under two seconds because it is the only figure-weight item below the divider.

### routing-alternatives
- **zones** — origin node `64,328,192,128`; destination node `1024,328,192,128`; three path lanes `272,176,736,128`, `272,328,736,128`, `272,480,736,128` (152 pitch); each lane: path label 22/550 left, then cost / time / risk cells at 20/450, with 18caps column heads on the top lane only.
- **focal** — the chosen path's lane. Wins on accent (its lane ground tinted, once), weight (550 against 450 in rejected lanes) and scale (that lane's label one step up at 26). Position is deliberately not a vector — the chosen lane is not always the middle one.
- **type** — origin/destination 24/550 → column head 18caps/550 +0.08em → path label 22/550 (chosen 26/600) → metric cell 20/450.
- **accent** — the chosen lane's ground. Once.
- **ux** — shows that the route taken was chosen against real alternatives with real numbers, not assumed.
- **avoid** — do not render rejected routes as greyed ghosts. Muted is fine; illegible is dishonest, and the numbers on a rejected path are the entire evidence that a choice happened.
- **caps** — `max 3` is the geometric ceiling at 152 pitch. Four drops lanes to 96px and the three metric cells stack instead of sitting in a row.

### last-mile-so-what
- **zones** — finding `64,96,1152,240` (48/600, up to 3 lines); 2px rule `y=384` full width; delivery row `64,432,1152,176` as three cells — audience `64,432,352,176`, action `448,432,448,176`, by `944,432,272,176`; each with an 18caps label at `y=432` and its value from `y=472`.
- **focal** — the finding. Wins on scale (48, more than twice anything else), position (top, full width) and spacing (the rule plus 96px of air separating it from everything below).
- **type** — finding 48/600 → cell label 18caps/550 +0.08em → audience 28/550 → action 28/550 → by 36/600.
- **accent** — the `by` value. Once — and it doubles as the two-second deadline: it is the rightmost, terminal cell, the only figure-weight item in the row, set one step above its siblings.
- **ux** — converts a finding into a named person doing a named thing by a named date.
- **avoid** — do not restate the finding in the action cell. The finding is what is true; the action is what someone does. If they are the same sentence, the slide has no last mile.
- **caps** — no cap stated on `finding`; the contract arithmetic gives ~164 characters at 48px in `1152,240`, so set ~150. Longer copy should drop to 40px rather than wrap to four lines.

### decision-queue-depth
- **zones** — title `64,56,768,56`; table `64,152,1152,440` (header 56 + 6 rows @ 64, sorted oldest first); columns decision `448` / owner `208` / days waiting `160` / blocked by `192` / decide by `144`.
- **focal** — the top row's days-waiting cell. Wins on accent, on weight (600 against 450), and on position (first data row, because the sort guarantees the oldest sits there).
- **type** — title 36/600 → column head 18caps/550 +0.08em → decision cell 20/450 → days-waiting 24/600 → decide-by 20/600 → other cells 18/450 (16 floor).
- **accent** — the oldest row's days-waiting figure. Once.
- **ux** — shows this audience what it is holding up, and for how long.
- **avoid** — not a status report. Every row must be a decision this room can take today; a row whose owner is not present belongs in a different deck.
- **caps** — `max 6` at 64 pitch fills `440` and leaves closing air; 7 rows reaches `y=592` with nothing left below it. Keep 6. Deadlines are findable because `decide by` is the last column, right-aligned, set at 600 — a vertical column of dates scans faster than dates buried in prose.

### handoff-baton
- **zones** — eyebrow 18caps `64,64,1152,32`; handsOver table `64,136,672,376` (header 56 + 5 rows @ 64); receiver `768,136,448,176`; nextAction `768,344,448,176`; ackLine `64,568,1152,48` with a signature rule beneath at `y=624`.
- **focal** — `nextAction`. Wins on scale (36/600, the largest type on the slide), accent, and terminal position at the end of the left-to-right handover the layout describes. `receiver` is its addressee at 32/550 — one step down, deliberately, so the slide reads "do this" rather than "here is a person".
- **type** — eyebrow 18caps/550 +0.08em → receiver 32/550 → nextAction 36/600 → handsOver head 18caps/550 → handsOver cell 18/450 (16 floor) → ackLine 20/450 muted.
- **accent** — `nextAction`. Once.
- **ux** — makes a handover an event with a named recipient rather than a deck that ends.
- **avoid** — never hand off to a role ("the finance team"). A baton passed to a group is a baton dropped.
- **caps** — 5 handsOver rows at 64 pitch fits `376`. **The template has no date slot**, so the deadline can only live inside `nextAction` prose and cannot be found in two seconds — the family's own rule. Add `by:text!` and pin it at `1024,344,192,80` at 32/600.

### ask-and-close
- **zones** — ask `64,120,1024,216` (56/600, ≤2 lines); 2px rule `y=376` full width; nextStep `64,416,672,96` (28/550); deadline `800,400,416,128` — 18caps label at `y=400`, date at 44/600 from `y=440`; contact `64,560,672,64` (20/450 muted).
- **focal** — the ask. Wins on scale (56, largest on the slide), position (upper-left, isolated by 120px of top margin) and colour role (the only full-strength `neutral`; next step and contact sit `muted`).
- **type** — ask 56/600 → deadline label 18caps/550 +0.08em → deadline 44/600 → nextStep 28/550 → contact 20/450 muted.
- **accent** — the deadline. Once — and it is the second-largest element on the slide, sitting on the same optical line as the next step, which is what makes it findable inside two seconds.
- **ux** — ends a persuasion deck with the thing being asked for and the date it is needed by.
- **avoid** — do not end on a thank-you or a logo; this template exists to replace that. And do not put two asks on it — an ask with options is `decision-request`.
- **caps** — ask ≤ ~90 chars at 56px in `1024,216` (contract arithmetic gives 93). Longer copy drops to 44px, giving ~150, rather than running to four lines. `deadline:text?` should be `deadline:text!` — a closing ask with no date is the failure mode this family was built to remove.

### claim-provenance-ledger
- **zones** — title `64,56,1152,56`; ledger `64,144,1152,440` (header 56 + 8 rows @ 48); columns claim `512` / source `288` / as-at `160` / preparer `112` / status `80`; source `64,624,1152,32`.
- **focal** — the first row whose source cell is empty or whose status is unverified. It wins by pattern-break — the single interruption in an otherwise perfectly regular ruled field — plus the accent and a heavier outline. If every row is sourced, the focal falls back to the title and the slide reads as a clean bill.
- **type** — title 36/600 → column head 18caps/550 +0.08em → claim cell 18/450 → source cell 18/450 → as-at 18/500 → status chip 18caps/550 → source line 18/400 muted.
- **accent** — the one unverified status chip. If all rows are verified, `none`.
- **ux** — puts every assertion the deck makes elsewhere in one place, next to whoever stands behind it.
- **avoid** — never merge source and as-at into one column. An undated source is the mechanism by which a stale figure survives into a new deck.
- **caps** — `max 8` at 48 pitch fills `440` exactly and is also the floor: 8 rows is the last count at which cells hold 18px without breaching the 16px table minimum. **How the geometry shames a gap:** every row's source cell is a ruled box with a visible baseline and a fixed 288px width, and every row renders a status chip — so an empty source is a drawn empty box, not whitespace, and a missing status is a hollow outline. The eye tracks straight from claim text across a column rule into a shape that is visibly unfilled. The layout cannot close up around an unsourced claim; the cells do not collapse.

### number-provenance
- **zones** — figure label 18caps `64,80,480,32`; figure `64,112,480,224` (stat, sized by the renderer up to 120px); derivation ladder `640,112,576,320` (4 steps @ 80; each step: operation 18/500 left, value 24/550 right, source tag 16/450 on a reserved baseline beneath); asAt `64,400,480,48`; source `64,624,1152,32`.
- **focal** — the figure. Wins on scale (up to 120px against 24 in the ladder), position (left, first read) and isolation (480×224 with nothing else in its quadrant).
- **type** — figure label 18caps/550 +0.08em → figure stat up to 120/600 → step operation 18/500 → step value 24/550 → step source tag 16/450 muted → asAt 20/450 → source 18/400 muted.
- **accent** — the figure. Once; the ladder stays neutral so it reads as working, not as argument.
- **ux** — shows how a derived number was arrived at, at the same moment the number is claimed.
- **avoid** — not for a figure lifted straight from the accounts. A one-step ladder is manufactured rigour and reads as such.
- **caps** — `max 4` steps at 80 pitch fits `320`; more than four is a reconciliation and belongs in `non-ifrs-reconciliation`. **How the geometry shames a gap:** each ladder step reserves a fixed 80px whether or not its source tag is filled, so an untagged step renders as a visible empty baseline directly beneath the number it produced. And the ladder occupies 45% of the canvas — the headline figure cannot be rendered by this template without the derivation beside it.

### non-ifrs-reconciliation
- **zones** — statutory `64,128,320,176` (18caps label + value); add-backs ladder `448,112,384,384` (header 48 + 6 rows @ 56, running rule down the right edge of the amounts); adjusted `896,128,320,176`; connector baseline `y=216` running `384→448` and `832→896`; definition band `64,560,1152,96` on a tinted ground, 18/450 across two lines.
- **focal** — the adjusted figure. Wins on terminal position (end of a left-to-right ladder the connectors draw) and accent, with the ladder's directional rule pointing at it. It is deliberately set at the *same* size and weight as the statutory figure, so scale is not a vector here — the slide must not imply the adjusted number is the bigger news.
- **type** — stat label 18caps/550 +0.08em → statutory 56/600 → adjusted 56/600 → add-back item 18/450 → add-back amount 20/550 → definition 18/450.
- **accent** — the adjusted figure. Once.
- **ux** — refuses to present an adjusted number without the ladder and the definition that make it checkable.
- **avoid** — never make the adjusted figure larger or bolder than the statutory one, and never let the definition be an adjective ("underlying performance"). It must be a formula, naming what is in and what is out.
- **caps** — `max 6` add-backs fits at 56 pitch, but six is itself a warning: past about four add-backs the adjusted number is an opinion. **How the geometry shames a gap:** the adjusted stat is horizontally locked to the right of the ladder — there is no arrangement in which it renders without the ladder occupying the middle third — and the definition band is a fixed 96px strip on a tinted ground, so an empty definition is a visible empty panel rather than a layout that closes up.

### restatement-diff
- **zones** — eyebrow 18caps `64,64,1152,32`; table `64,128,1152,416` (header 56 + 5 rows @ 72, sized for a reason sentence per row); columns line item `288` / prior `176` / restated `176` / delta `144` / reason `368`; effectiveDate `64,568,1152,64` with a 2px rule above — 18caps label then 32/600 date.
- **focal** — the largest delta cell. Wins on weight (600 against 450), scale (24 against 20 elsewhere) and accent. The delta column is also the only right-aligned numeric column, which sets it apart before any cell is read.
- **type** — eyebrow 18caps/550 +0.08em → column head 18caps/550 → line item 20/500 → prior/restated 20/450 → delta 24/600 → reason 18/450 → effectiveDate label 18caps/550 → effectiveDate 32/600.
- **accent** — the largest delta cell. Once.
- **ux** — makes a revision impossible to publish without saying what changed, by how much, why, and from when.
- **avoid** — do not restate quietly across successive decks. If the prior figure is not rendered at the same size as the restated one, this is a correction hiding as an update.
- **caps** — `max 5` at 72 pitch fits `416`. The reason column caps at ~70 characters (18px in `368,72`); enforce that or rows wrap into each other. **How the geometry shames a gap:** the reason column is 368px — a third of the table width — and each row's baseline rule runs the full 1152, so a blank reason renders as a third of a row visibly unanswered. There is also no layout branch without the `effectiveDate` band.

### what-changed-since
- **zones** — priorRef strip `64,64,1152,56` — 18caps "since" label then the reference and its date at 24/550; table `64,152,1152,392` (header 56 + 6 rows @ 56); columns item `320` / then `224` / now `224` / delta `112` / why `272`.
- **focal** — the largest mover in the delta column. Wins on accent, weight (600 against 450) and by being the only column carrying a directional marker (▲/▼ plus sign — a glyph and a sign, never colour alone).
- **type** — priorRef label 18caps/550 +0.08em → priorRef 24/550 → column head 18caps/550 → item 20/500 → then/now 20/450 → delta 22/600 → why 18/450 (16 floor).
- **accent** — the largest delta cell. Once.
- **ux** — makes drift between one pack and the next visible instead of leaving it to memory.
- **avoid** — do not list every line. Six is the cap because the slide's job is drift, not completeness — and never compare against an unnamed "last time"; `priorRef` must name the meeting and its date.
- **caps** — `max 6` at 56 pitch fits `392`. The `why` column at 272px caps reasons at ~50 characters; enforce it. **How the geometry shames a gap:** `priorRef` is a full-width strip above the table, not a caption — the comparison cannot render anonymously — and the `why` column is ruled per row, so an unexplained change is a drawn empty cell sitting beside a delta the audience can already read.

### returns-register
- **zones** — eyebrow 18caps `64,64,1152,32`; table `64,128,1152,440` (header 56 + 6 rows @ 64); columns commitment `384` / period made `144` / outcome `256` / variance reason `208` / status `160`; closing rule `y=592`.
- **focal** — the first `missed` status chip. Wins by pattern-break (the only filled or inverted chip in a column of outlines), by accent, and by weight (600 against 450 in every other cell).
- **type** — eyebrow 18caps/550 +0.08em → column head 18caps/550 → commitment 20/500 → outcome 20/450 → variance reason 18/450 (16 floor) → status chip 18caps/600.
- **accent** — the first missed chip. Once. If nothing was missed, `none`.
- **ux** — sets what was promised beside what came back, so a track record is a table rather than a claim.
- **avoid** — never populate it only with kept commitments. A register with no misses is marketing; if the period genuinely had none, say so in a commitment row rather than filtering rows out.
- **caps** — `max 6` at 64 pitch fits `440`. Recommend adding `tally:text?` at `64,592,1152,48` — kept-versus-missed counts are currently derivable only by counting chips. **How the geometry shames a gap:** every row renders a status chip regardless of outcome, so a promise with no result shows a hollow chip reading "open" — visibly not an answer — and the variance column is ruled, so an unexplained miss is a drawn blank next to it.

### definition-strip
- **zones** — eyebrow 18caps `64,64,1152,32`; column A `64,136,544,480` (3 entries @ 160); column B `672,136,544,480` (3 entries @ 160). Each entry: term 24/600, hairline beneath, then formula or inclusion rule 18/450 across two lines (~100 chars in 544).
- **focal** — the term the deck's headline figure depends on, set at 28/600 while the other five sit 24/550, with the accent on its formula line. Two vectors: scale and accent. If no single term dominates, keep all six equal and let the eyebrow carry the focal — a glossary where one entry shouts implies the rest are optional.
- **type** — eyebrow 18caps/550 +0.08em → term 24/600 (lead term 28/600) → formula 18/450.
- **accent** — the lead term's formula line. Once, or `none` when the six are genuinely co-equal.
- **ux** — pins the vocabulary the deck's numbers depend on before anyone argues about a figure that turns out to be a definition dispute.
- **avoid** — do not define terms the deck never uses. Six generic finance terms is padding; each term must appear in a figure elsewhere in the deck.
- **caps** — `max 6` at 160 pitch across two columns fits `480` and matches the comprehension ceiling for a reference strip. **How the geometry shames a gap:** each entry reserves a fixed 160px with a hairline between term and rule, so a term with no formula renders as a labelled empty half-cell — the definition's absence occupies exactly as much space as its presence would.

### range-not-point
- **zones** — metric/title `64,56 1152×56`; low block `64,272 256×152`; base block `512,232 256×192`; high block `960,272 256×152`; range band (16px rule, `128,440 → 1152,440`) with three ticks under the block centres at x=192 / 640 / 1088; driver strip `64,496 1152×64`; basis footnote `64,640 1152×32`.
- **focal** — the base figure. Scale (72 against 44 for low/high), position (centred on the band's midpoint, the only block on the vertical axis of the slide), colour (the one accented figure), spacing (its box is 40px taller and 40px deeper than its neighbours). Four vectors, so a long base value that drops to 56 still wins.
- **type** — title 40/600 · block labels 18 caps 0.08em · low+high stats 44 · base stat 72 (−0.02em) · driver label 18 caps · driver body 24 · basis 18.
- **accent** — the base stat and its tick on the band, read as one mark. Low and high stay neutral; muted for their labels.
- **ux** — Makes a forecast answerable as a band instead of inviting the audience to treat one number as fact.
- **avoid** — Do not use it when low/base/high are the same number dressed three ways; a band with no real spread reads as false precision and is worse than a plain stat.
- **caps** — No list slots. Cap `driver` at ~90 characters (24px across 1152 = ~82/line, 2 lines) and all three stats at 14 characters, or the 72px base wraps mid-figure.

### assumption-load-bearing
- **zones** — claim slab `64,72 1152×160` (bordered band, 32px inner padding); four assumption columns `64 / 360 / 656 / 952, 264 264×328` (gutter 32); inside each: state chip `+0,+0 264×32`, assumption body `+0,+48 264×180`, owner caption `+0,+272 264×32`; footer `64,640 1152×32`.
- **focal** — the claim slab. Scale (40 against 20 in the columns), spacing (a 160px band with nothing beside it), position (top, full width), weight (600 against 400). The columns are deliberately co-equal because ranking assumptions defeats the point of listing them.
- **type** — claim 40/600 (−0.02em) · state chip 18 caps 0.08em · assumption 20 · owner 18 muted.
- **accent** — the 8px×96 rule under the claim. State chips stay neutral: verified = filled square, estimated = half square, hollow square = assumed, each with its word — shape and fill carry the meaning, never colour.
- **ux** — Turns a confident claim into a visible dependency list, so the audience argues about the assumption rather than the conclusion.
- **avoid** — Do not accent the "assumed" chips to signal risk; four accented chips makes the slide read as an alarm and eats the accent budget the claim needs.
- **caps** — `max 4` is right: 4×264 is the narrowest column that holds 20px text at ~22 chars/line. With 2 or 3 rows the columns re-divide 1152 evenly (3 → 368, 2 → 560); do not centre 2 narrow columns and leave a hole.

### disconfirming-evidence
- **zones** — thesis label `64,64 416×24`; thesis panel `64,96 416×456`; vertical hairline `512,96 → 512,552`; counter rows `544,96 672×456`, four rows h=96 with 24 gutter (96 / 216 / 336 / 456); inside each: severity mark `+0,+0 32×32`, evidence line `+48,+0 624×48`, response line `+48,+52 624×44`; footer `64,640 1152×32`.
- **focal** — the thesis panel. Scale (32 against 20), spacing (it owns a third of the canvas for one sentence), position (left, first read in LTR). The counters are the payload but read second by design — you have to know what is being attacked.
- **type** — thesis label 18 caps 0.08em · thesis 32/450 · evidence 20/600 · response 18 muted · severity word 18 caps.
- **accent** — the 8px×96 rule above the thesis. Severity uses filled / half / hollow triangles plus the word, so the ranking survives greyscale and a projector's gamma.
- **ux** — Forces the strongest case against the argument onto the slide, where it can be answered, instead of into Q&A where it can't.
- **avoid** — Do not fill it with straw objections you can dismiss in four words; a row whose response is longer than its evidence is the tell that the audience will call.
- **caps** — `max 4` is right. A fifth row drops the pitch below 96 and the two-line response collapses to one, which is where the honesty goes.

### unknowns-register
- **zones** — title `64,56 1152×48`; header row `64,136 1152×40` with a 2px rule at y=176; six body rows `64,176 1152×64` (176 / 240 / 304 / 368 / 432 / 496, hairline separators, table ends 560); columns — unknown `64 w360`, why `440 w264`, would-resolve `720 w264`, by-when `1000 w128`, owner `1144 w72`; footer `64,640 1152×32`.
- **focal** — the leftmost column, read as one vertical block. Weight (20/600 against 18/400 in every other cell), position (first column, first read), colour (full-strength while the supporting cells sit one step muted). A table has no natural hero, so the hierarchy is built across a column rather than onto a cell.
- **type** — title 36/600 · header 18 caps 0.08em · unknown cell 20/600 · other cells 18 · footer 18.
- **accent** — the "Would resolve it" column header only. That is the column that converts an unknown into work; one header mark, nothing else on the slide.
- **ux** — Makes absence of evidence assignable, with an owner and a date, instead of leaving it as a shrug in the room.
- **avoid** — Do not use it as a risk register; risks have likelihoods and mitigations, unknowns have resolution actions, and merging them produces rows nobody owns.
- **caps** — `max 6` is right. Seven rows at 64 push the table to 624 and collide with the footer band, and the frame check does not catch a footer overlap.

### jit-assumptions
- **zones** — title `64,56 1152×48`; time axis rule `64,136 1152×2` with lane labels `64 / 456 / 848, 144 368×32`; three lanes `64 / 456 / 848, 192 368×408`; four cards per lane, h=88 gutter 16 (192 / 296 / 400 / 504, lane ends 592); card internals — assumption 20 at `+16,+12`, carrying cost + decay date 18 at `+16,+58`; footer `64,640 1152×32`.
- **focal** — the NOW lane. Position (leftmost on a left-to-right time axis), colour (its label and card grounds at full strength while SOON and LATER step down two tints), weight (its label 20/600 against 18/510). Three vectors, none of them size — the lanes stay the same width because they are the same kind of thing.
- **type** — title 36/600 · lane labels 20 caps 0.08em · card body 20 · card meta 18 muted.
- **accent** — the NOW lane header. Nothing inside a card takes colour.
- **ux** — Sequences assumptions by when each has to be resolved, so the room argues about the next one rather than all of them at once.
- **avoid** — Do not put an assumption in LATER that the current plan already depends on; the template's value is that the lane is a commitment about timing, and a mis-laned assumption is worse than an unsorted list.
- **caps** — `max 4` per lane is right (4×88 + 3×16 = 400 in a 408 lane). Lanes are independently optional, so a 4/2/0 shape renders honestly — do not pad LATER to fill the column.

### checkpoint-recap
- **zones** — kicker `64,64 1152×24`; you-are-here line `64,112 1152×136`; progress strip `72,336 1136×40` (five segments w=208, gutter 24, at x=72 / 304 / 536 / 768 / 1000), the active segment drawn `y=324 h=64`; segment labels `beneath each, y=400 w=208 h=48`; next beat `64,520 1152×64`; footer `64,656 1152×24`.
- **focal** — the you-are-here line. Scale (52 against 24 for the next beat and 18 for labels), position (top-left), weight (600), spacing (a 136px band to itself). The active segment is the second read via colour and its 24px height jump.
- **type** — kicker 18 caps 0.08em · you-are-here 52/600 (−0.02em) · segment labels 18 caps, active 20 · next label 18 caps · next body 24.
- **accent** — the active segment fill. Its height and its label weight repeat the signal, so it is not colour alone.
- **ux** — Gives a long deck a save point, so a distracted audience can re-enter the argument without asking where they are.
- **avoid** — Do not use it before the deck has earned it; a checkpoint at slide four reads as padding. One or two in a 30-slide deck, placed after the densest run.
- **caps** — `max 5` is right. Six segments drop to w=176 and the labels start truncating; if a deck genuinely has six sections, cut the labels to a single word rather than raising the cap.

### agenda-progress
- **zones** — title `64,56 768×48`; list `64,152 768×464`, seven rows h=56 gutter 8 (152 / 216 / 280 / 344 / 408 / 472 / 536), the current row rendered h=72; row internals — number chip `+0,+0 48×48`, item text `+80,+0 688×56`; position block `896,200 320×200` showing the current index over the row count, derived from `currentIndex` and the row count, not a new slot; footer `64,656 1152×24`.
- **focal** — the current agenda item. Scale (32 against 24), weight (600 against 450), colour (full strength while completed items sit at ~45% and upcoming items at ~70%), plus its filled number chip. Four vectors, so it survives a long item label.
- **type** — title 36/600 · numbers 18 caps · items 24, current 32 · position stat 64 · position label 18 caps.
- **accent** — the current item's number chip. The dimming ramp is neutral tint, not a second colour.
- **ux** — Answers "where are we and how much is left" without the presenter having to say it, which is the single most common interruption in a long pack.
- **avoid** — Do not dim completed items below 4.5:1 contrast; "done" is still readable content, and a projector will take another step of contrast off it.
- **caps** — `max 7` is right (7×56 + 48 = 440 inside 464). Eight would still fit geometrically but the slide stops reading as an agenda and starts reading as a list.

### attention-reset
- **zones** — full-bleed ground `0,0 1280×720`, inverted against the deck's content slides; phrase `160,240 960×240`, optically centred (mass centred at y≈336, above the geometric centre so it does not sit low); marker `64,656 1152×24` on the exact baseline every other slide's footer uses. No other elements.
- **focal** — the phrase, and nothing else. Scale (up to 96 against a deck whose body is 20–24), isolation (the only ink in 720px of height), ground inversion (colour). What makes it read as deliberate rather than unfinished is the frame furniture: the marker sits on the same baseline, at the same x, in the same size and tracking as every other slide's footer, and the phrase's margins are exact multiples of 8 from the same scale. An unfinished slide has neither. The ground flip is the second proof — a forgotten slide inherits the content ground, it does not invert it.
- **type** — phrase 72–96/600 at line-height 1.05, −0.02em, two lines maximum · marker 18 caps 0.08em.
- **accent** — none. The ground inversion is already doing the colour work; adding an accent turns it into a section cover.
- **ux** — Buys back attention after a dense run by giving the room one beat with nothing to process.
- **avoid** — Do not use it more than twice in a deck, and never where nothing dense preceded it — with no cognitive debt to pay off it reads as a slide someone forgot to fill.
- **caps** — No list slots. Cap the phrase at ~60 characters at 96px, ~90 at 72px. Longer and it stops being a reset and becomes an unformatted statement slide; the renderer should step 96 → 84 → 72 rather than wrap to three lines.

### speedrun-summary
- **zones** — title `64,48 1152×48`; rows `64,120 1152×504`, eight rows h=56 gutter 8 (120 / 184 / 248 / 312 / 376 / 440 / 504 / 568, ending exactly at 624); row internals — index `64 w64`, claim `144 w760`, figure `936 w280` right-aligned; footer `64,648 1152×32`.
- **focal** — the figure rail, read as one vertical mass rather than eight items. Scale (32 against 22 for claims), weight (600 against 450), position (a single hard right alignment edge that the eye tracks down). No individual row is promoted: this slide is built to be photographed and any promoted row biases what gets kept.
- **type** — title 28/600 · index 20 caps muted · claim 22/450 · figure 32/600.
- **accent** — none. Eight equal rows means any accent invents a priority the summary does not have, and this is the one slide where the audience's phone is the medium.
- **ux** — Compresses the whole argument to something a board member can photograph and re-read a week later without the deck.
- **avoid** — Do not use it as a closing slide when there is an ask; a summary that ends the deck buries the request. Follow it with `ask-and-close`.
- **caps** — `max 8` is right and is a hard ceiling: 8×56 + 7×8 = 504 fills the region exactly, and a ninth row breaks the frame.

### difficulty-ramp
- **zones** — title band suppressed (the surface line is the title); band 1 `64,96 1152×176` with label rail `64 w144` and body `224 w992`; band 2 `64,296 1152×152`, same rails; band 3 `64,472 1152×120`, body `224 w672` with `detailStat` right-aligned in `936,488 280×72`; hairline rules between bands at y=288 and y=464; footer `64,640 1152×32`.
- **focal** — the band-1 surface claim. Scale (40 against 28 and 20), spacing (the tallest band with the most internal padding), position (top), colour (full strength while bands 2 and 3 step down in tint). The type ramp is literally the depth ramp, so the hierarchy and the content are the same gesture.
- **type** — band labels 18 caps 0.08em · surface 40/600 (−0.02em) · mechanism 28/450 · detail 20 · detailStat 40/600 neutral.
- **accent** — the band-1 label chip. `detailStat` stays neutral so a 40px figure at the bottom-right cannot pull focus off the claim at the top-left.
- **ux** — Lets one slide serve three audiences at once, so the presenter stops where the room's appetite ends instead of guessing beforehand.
- **avoid** — Do not write three restatements of the same sentence at decreasing font sizes; each band must add a mechanism the one above did not contain, or the slide is a paragraph with rules through it.
- **caps** — No list slots. Cap surface at ~84 characters (2 lines at 40px across 992), mechanism at ~170, detail at ~230. `detailStat` is 14 characters like any stat.

### section-recap
- **zones** — kicker `64,64 1152×32`; section title `64,96 1152×64`; three columns `64 / 456 / 848, 224 368×360`; inside each: numeral `+0,+0 368×56`, established text `+0,+72 368×240`; footer `64,640 1152×32`.
- **focal** — the section title. Scale (40 against 24), position (top-left), weight (600 against 450), plus the accent rule beneath it. The three columns are deliberately co-equal — "the three things" only works if none of them is bigger.
- **type** — kicker 20 caps 0.08em · section 40/600 (−0.02em) · numerals 40/450 muted · established 24.
- **accent** — the 8px×96 rule under the section title. The 01/02/03 numerals stay muted neutral.
- **ux** — Closes a section by naming what was established, so the next section can build on it instead of re-arguing it.
- **avoid** — Do not restate the section's slide titles; a recap that lists topics rather than conclusions gives the audience nothing to carry forward.
- **caps** — `max 3` is right and should not rise. Four columns fall to w=272, which forces the body to 20 and breaks the "three things" claim the template is named for.

### objection-gate
- **zones** — label `64,56 1152×24`; objection `64,96 1152×160`; hairline `64,280 1152×2`; three condition columns `64 / 456 / 848, 312 368×216`, each with an index `+0,+0 368×24` and body `+0,+40 368×176`; evidence block `832,552 384×88` — stat left `832 w168`, note right `1016 w200`; slide marker `64,656 1152×24`.
- **focal** — the objection. Scale (44 against 22 for conditions and 36 for the evidence stat), position (top, full width, first read), spacing (160px band for one sentence). The evidence stat is deliberately smaller than the objection so it is found second, as the answer rather than the headline.
- **type** — label 18 caps 0.08em · objection 44/600 (−0.02em) · condition index 18 caps · condition body 22 · evidence stat 36/600 · evidence note 18.
- **accent** — the evidence stat. It is the only figure and the only thing on the slide that unlocks the gate; the objection carries its weight through scale, not colour.
- **ux** — States the objection in the audience's own words and names exactly what would settle it, which converts an argument into a test.
- **avoid** — Do not soften the objection into something easier to answer. If the wording is not one a sceptic would recognise as theirs, the slide reads as a set-up and costs more trust than it buys.
- **caps** — `max 3` conditions is right; 368-wide columns hold two lines of 22 comfortably. Note that `evidence` is optional — with it absent the block is removed and the conditions row re-centres in `312 → 560`, which is the correct honest render.

### failure-postmortem
- **zones** — label `64,56 832×24`; prior claim `64,88 832×112` with a 2px strike rule through the text's optical centre; miss stat `960,72 256×144`; hairline `64,232 1152×2`; causes panel `64,264 560×328` (header `+0,+0 560×32`, three rows h=88 gutter 16 at 296 / 400 / 504); repair panel `656,264 560×328`, same rhythm, each row carrying an owner caption; vertical hairline `624,264 → 624,592`; footer `64,640 1152×32`.
- **focal** — the miss stat. Scale (64, the largest thing on the slide), colour (the only accent), position (top-right, where the reading path from the struck claim terminates), weight (600). The struck prior claim is actively demoted — muted plus a strike rule — so the hierarchy is built by pushing down as well as up.
- **type** — labels 18 caps 0.08em · prior claim 32/450 muted, struck · miss stat 64/600 · panel headers 18 caps · cause and repair rows 20 · owner captions 18 muted.
- **accent** — the miss stat, and nothing else. Specifically not the repair column: an accented repair reads as spin and undoes the credibility the struck claim just bought.
- **ux** — Pays a credibility debt in public by naming the miss before anyone else does, which is what makes the next forecast on the same deck believable.
- **avoid** — Do not run it with more repair rows than cause rows; a postmortem that lists three fixes for one cause is a plan wearing a postmortem's clothes.
- **caps** — 3 and 3 are right. Four each drops rows to 64 and the two panels start reading as one table, which destroys the cause↔repair pairing that the side-by-side exists to show.

### faq-objections
- **zones** — title `64,56 1152×48`; grid `64,144 1152×472`, two columns w=560 gutter 32 (x=64 / 656), three cells per column h=144 gutter 16 (144 / 304 / 464, ending 608); cell internals — question `+16,+16 528×56`, answer `+16,+80 528×48`; footer `64,648 1152×32`.
- **focal** — the title. Scale (36 against 22), weight (600 against 450), spacing (an 88px gap above a dense six-cell field), plus the accent rule. No cell may be promoted — ranking anticipated questions tells the audience which one you are afraid of.
- **type** — title 36/600 · question 22/600 · answer 20/450 muted · footer 18.
- **accent** — the 8px×96 rule under the title. Q markers, if drawn, stay neutral.
- **ux** — Pre-empts the Q&A on the record, so the answers are the considered ones rather than the improvised ones.
- **avoid** — Do not use it for the objection that actually decides the deal; that one needs `objection-gate` with its resolving evidence. This template is for the six questions that would otherwise eat ten minutes.
- **caps** — `max 6` is right as a ceiling but 4 reads better. Eight cells would drop the pitch to 104 and force answers to a single line at 18, which is where they turn into slogans.

### conflict-disclosure
- **zones** — title `64,56 1152×48`; header row `64,144 1152×40` with a 2px rule at y=184; five body rows `64,192 1152×80` (192 / 272 / 352 / 432 / 512, hairlines, table ends 592); columns — party `64 w288`, relationship `368 w320`, interest `704 w320`, recusal `1040 w176`; mandatory caveat footnote `64,648 1152×48`, laid out **before** the rows so the table can never claim its space.
- **focal** — the interest column. Weight (20/600 against 18/450 elsewhere), colour (full-strength while party and relationship sit muted), ground (a faint tinted column band running the table's height). Three vectors, none of them the deck accent — this is the column the template exists to force, so it is emphasised without being editorialised.
- **type** — title 36/600 · header 18 caps 0.08em · party and relationship cells 18 · interest cell 20/600 · recusal 18 caps · caveat 18.
- **accent** — none. A disclosure table that accents anything reads as argument rather than record; the recusal marker is semantic (filled square + "Recused" / hollow square + "Not recused"), never colour alone.
- **ux** — Makes an interest impossible to omit by giving it a column, so the recommendation and its conflicts are read in the same glance.
- **avoid** — Do not render a recommendation slide without this one when an interest exists; the failure mode is not a bad-looking slide, it is a governance finding.
- **caps** — `max 5` is right and is lower than an ordinary table's for a reason: the mandatory caveat band takes 48px plus its 56px gap, and six 80px rows would eat it. If a sixth party exists, split across two slides rather than shrinking the rows.

### bottleneck-lane
- **zones** — title `64,56 1152×48`; stage names `80 / 272 / 464 / 656 / 848 / 1040, 200 160×40`; lane `80,248 1120×120` — six stage boxes w=160 pitch 192 (gutter 32), the constraint stage drawn `h=56` at y=280 instead of `h=120` at y=248; flow arrows in each 32px gutter on the lane's vertical midline y=308; throughput figures `beneath each box, 384 160×40`; loss callout `constraint-aligned, 456 384×96`, clamped so x stays within `64 … 832`, with a 2px orthogonal connector to the neck; footer `64,640 1152×32`.
- **focal** — the constricted stage. Shape (it is the one box that breaks a repeated rhythm — the strongest single isolation signal available in a row of identical marks), colour (the accent fill), scale (its throughput figure set at 36 against 28). Three vectors, and the shape one survives greyscale.
- **type** — title 36/600 · stage names 18 caps 0.08em · throughput figures 28/600, constraint 36 · loss callout 22.
- **accent** — the constraint stage's fill only. Its throughput figure wins on size and weight rather than taking a second dose of colour.
- **ux** — Names the constraint so the conversation is about one stage instead of about the whole pipeline.
- **avoid** — Do not draw two necks. A lane with two constraints has not been analysed yet, and the slide's entire value is that it commits to one.
- **caps** — `max 6` is right at w=160, but stage names must be ≤15 characters at 18px caps. Four stages is the comfortable read (w=264 after re-division); prefer it when the pipeline allows.

### batch-vs-flow
- **zones** — left panel `64,112 544×488`, right panel `672,112 544×488`, centre hairline `640,112 → 640,600`; per panel — label `+0,+16 544×40`; cadence band `+0,+88 544×120`: left draws three blocks w=96 h=64 at pitch 224 (x=64 / 288 / 512, filling 544 exactly), right draws twelve ticks w=16 h=64 at pitch 40 (456 wide, left-aligned); stats `+0,+248 544×200`, up to three rows h=56 gutter 8, label 18 caps left and value right-aligned; footer `64,640 1152×32`.
- **focal** — the cadence band, read as one comparison object across the divider. Position (the optical centre band of the slide), density contrast (three marks against twelve is the argument, rendered as geometry), colour (the only accented ink on the slide sits inside it). The panel labels and stats are subordinate at 24 and 32.
- **type** — panel labels 24 caps 0.08em · stat labels 18 caps · stat values 32/600 · footer 18.
- **accent** — the right-hand tick array. If the deck is arguing for batching instead, swap which cadence sits on the right rather than moving the accent — the accent always marks the advocated state, and the right-hand position always marks the destination.
- **ux** — Converts an abstract operating-model argument into two shapes the room can compare in one second, before any number is read.
- **avoid** — Do not use it when the two sides differ in more than cadence (different scope, different team, different period). The geometry claims like-for-like, so an unlike comparison is a lie the layout tells for you.
- **caps** — The catalogue sets no cap on `left.stats` / `right.stats`. **Set `max 3` on each.** Three 56px rows plus gutters fill the 200px stats region exactly; a fourth overflows into the footer band.

### unit-array
- **zones** — title `64,56 1152×48`; array region `64,200 768×384`; total stat `880,216 336×120`; unit label `880,360 336×64`; caption `880,456 336×96`; footer `64,640 1152×32`.
- **focal** — the total stat. Scale (72, the largest type on the slide), position (an isolated right rail against a dense left field), spacing (120px of its own), weight (600). Deliberately not colour — the accent is spent on the unit mark, which is what makes the array countable.
- **type** — title 36/600 · total stat 72 (−0.02em) · total label 20 caps 0.08em · unit label 22 · caption 18.
- **accent** — the single called-out unit mark (the first mark, top-left), at the same size as every other mark. Never larger: a bigger mark reads as a bigger value and turns a unit chart into an illustration.
- **ux** — Makes a large number countable, so the audience feels the magnitude instead of parsing digits.
- **avoid** — Do not use it for a number whose unit is not a real discrete thing (dollars, percentages, ratios). A unit array of "$4.2m" is decoration; a unit array of "450 sites" is data.
- **caps** — No list slots, but the geometry needs stating. **Marks are 16px squares on an 8px gutter (24px pitch), in a 30 × 15 grid = 450 marks, with an extra 16px gap after every 10th column and every 5th row so the array can be counted in tens.** Filled row-major, left to right, top to bottom. Above 450, step the mark down 16 → 12 → 8 (gutter = mark/2, floor 4); below 8px the marks stop resolving on a projector — use `waffle-share` or `scale-anchor` instead.

### waffle-share
- **zones** — title `64,56 1152×48`; waffle grid `88,152 472×472`; text rail `656,216 560×352` — filled stat `656,216 560×136`, label `656,368 560×80`, note `656,472 560×96`; footer `64,648 1152×32`.
- **focal** — the filled block. Colour (the filled cells are the only accented ink and form one contiguous mass), shape (a single readable boundary step rather than a scatter), position (left, first read). The stat is held at 72 rather than 96 precisely so the grid keeps the focal — the number labels the shape, it does not replace it.
- **type** — title 36/600 · filled stat 72/600 (−0.02em) · label 28 · note 20 · footer 18.
- **accent** — the filled cells, read as one mark. Empty cells are a muted ground with a hairline outline so the denominator stays visible and countable.
- **ux** — Makes a proportion countable, which is the only way an audience actually feels the difference between 12% and 30%.
- **avoid** — Do not use it for a value below 1% or one that needs a decimal; a waffle cell is a whole percentage point, and rounding 0.4% up to one filled cell is a misrepresentation. Use a stat template.
- **caps** — Fixed 100 cells: **40px cells on an 8px gutter (48px pitch), 10 × 10, 472×472 total.** Fill strictly row-major from the top-left so the boundary is one step. `filled` above 100 is not a share and must be refused rather than clamped.

### scale-anchor
- **zones** — title `64,56 1152×48`; label rail `64,152 256×320` (row labels right-aligned); zero rule `352,160 2×312` with a "0" label at `352,480`; bar tracks `352,x 704×h` — primary `352,176 704×64`, comparisons at `352,272 / 352,344 / 352,416`, each `704×48`; figure column `1072,x 144×h` right-aligned per row; primary stat `64,504 288×96`; mandatory source `64,648 1152×32`.
- **focal** — the primary bar and its stat, read as one row. Scale (64px stat against 22px comparison figures; 64px track against 48px), colour (the primary bar is the only accented fill), position (top of the stack, immediately under the title), weight. Four vectors.
- **type** — title 32/600 · row labels 18 caps 0.08em · primary stat 64/600 · comparison figures 22 · source 18 muted.
- **accent** — the primary bar's fill. The stat stays neutral so the accent lands on the encoding rather than on the digits.
- **ux** — Gives a bare figure the one thing that makes it interpretable: something at the same scale to sit beside it.
- **avoid** — Do not scale the bars independently or start the axis anywhere but zero. A shared zero-anchored scale is the entire mechanism; truncate it and the slide argues the opposite of what the numbers say.
- **caps** — `max 3` comparisons is right. Four fits geometrically (416 + 48 + 40 = 504) but a fourth named reference dilutes the anchor into a small bar chart, which is a different template.

### product-screens-3up
- **zones** — title `64,56 1152×48`; three frames `64 / 456 / 848, 152 368×352` (gutter 24), each a 1px-bordered slot on a neutral ground with device or browser chrome drawn **as part of the frame**; the shot aspect-FITs into the chrome's viewport rect with a 16px inset (336×320 usable) and letterboxes against the ground on its short axis; captions `64 / 456 / 848, 528 368×72`, **below the frames, never over a shot**; footer `64,640 1152×32`.
- **focal** — frame 1. Position (leftmost, and the first step in what is nearly always a sequence), colour (its caption numeral and frame hairline carry the accent). Frames stay identical in size — an unequal frame implies a ranking that a three-step sequence does not have.
- **type** — title 32/600 · caption numerals 18 caps 0.08em · captions 20/450 · footer 18.
- **accent** — the "01" numeral and hairline on frame 1. Nothing is drawn on the screenshots themselves.
- **ux** — Shows the product doing the thing, in the order a user would meet it, without asking the audience to read a UI at 19% scale.
- **avoid** — Do not use it for landscape desktop screenshots; a 1440-wide UI inside a 336px slot is a texture, not a screen. Portrait or phone shots suit 3-up; a desktop shot belongs in `screen-annotated`.
- **caps** — `max 3` is right and should not rise. With 2 shots the frames re-divide to `w=560, gutter 32`; with 1, use `screen-annotated`. Captions are optional but should be all-or-nothing — one captioned frame among three uncaptioned reads as a mistake.

### screen-annotated
- **zones** — title `64,56 1152×48`; image frame `64,136 768×480`, shot aspect-FIT with a 16px inset (736×448 usable), letterboxed against a neutral ground; numbered markers placed at target coordinates on the shot — 32px circled numerals with an 8px contrasting ring so they stay legible over any pixel; callout rail `880,136 336×480`, four rows h=96 gutter 24 (136 / 256 / 376 / 496), each with a numeral chip `+0,+0 32×32` and text `+56,+0 280×96`; leader lines drawn orthogonally, and only when a rail row and its marker are more than 120px apart vertically; footer `64,648 1152×32`.
- **focal** — the screenshot. Scale (768×480 is ~40% of the canvas), position (left, dominant), spacing (the rail is a third of its width). The markers are the second read and route the eye into the rail.
- **type** — title 32/600 · marker numerals 20/600 · rail numerals 18 caps · callout text 20/450 (≈24 chars/line, 3 lines) · footer 18.
- **accent** — the numbered markers and their matching rail chips, as one semantic mark set (numeral + ring). Nothing else on the slide takes colour. The numeral, not the colour, is the link between rail and shot, so it survives a colour-blind viewer and a washed-out projector.
- **ux** — Points at the exact region under discussion, so the room stops hunting the screenshot while the presenter talks.
- **avoid** — Do not set callout text on the screenshot. Text over UI collides with the UI's own text at every zoom level, and the shot stops being evidence.
- **caps** — `max 4` is right. A fifth row pushes the rail below the 96px pitch that 20px text over three lines needs, and five markers on one screen is a sign the screen needs splitting.

### before-after-screens
- **zones** — title `64,56 1152×48`; state labels `64 / 656, 104 560×32`, above the frames and never on a shot; two frames `64 / 656, 136 560×352` (gutter 32), **identical boxes regardless of source aspect**, each shot aspect-FIT with a 16px inset (528×320) and letterboxed; direction marker `624,296 32×32` in the gutter; summary `64,520 1152×96`; footer `64,648 1152×32`.
- **focal** — the "after" frame. Position (right, the destination of the reading path), colour (its label and frame hairline take the accent), and the "before" frame demoted a full contrast step in both its border and its label. Three vectors, one of them a demotion.
- **type** — title 32/600 · state labels 20 caps 0.08em · summary 24/450 (≈82 chars/line, 2 lines) · footer 18.
- **accent** — the "After" label plus its frame hairline, read as one mark.
- **ux** — Makes a UI change legible in one glance, which is the only way a non-user audience can judge whether it was worth doing.
- **avoid** — Do not crop or zoom the two shots differently. Different crops mean the comparison measures the crop, not the change, and it is the single most common way this slide misleads without anyone intending it.
- **caps** — Fixed at two images. Cap `summary` at ~160 characters; longer and it competes with the frames it is supposed to caption.

### architecture-blocks
- **zones** — title `64,56 1152×48`; four tier bands `64,136 / 64,256 / 64,376 / 64,496`, each `1152×96` with a 24px inter-tier gutter (last band ends 592); per band — tier label rail `+0,+0 176×96` (vertically centred), blocks `+192,+16 936×64`, up to five blocks w=168 gutter 24, left-aligned; connectors are 2px vertical rules in the inter-tier gutters between vertically adjacent block centres, never diagonal; note `64,608 896×48`; slide marker `1000,616 216×32`.
- **focal** — the top tier. Position (first read, and the user-facing layer), colour (full-strength ground while the tiers below step down one tint each), scale (its label 20 against 18). Three vectors.
- **type** — title 32/600 · tier labels 20 caps 0.08em (top tier), 18 caps below · block labels 18/510, two lines maximum · note 18 muted.
- **accent** — the top tier's label rail. Blocks and connectors stay neutral; an accented block in a diagram of equals implies a criticality the layout cannot substantiate.
- **ux** — Gives a non-engineering audience a mental model of the system in the ten seconds before the technical discussion starts.
- **avoid** — Do not use it as a real architecture diagram. Four tiers of labelled boxes with vertical connectors cannot express failover, async, or data direction; if those matter, the slide is a `sequence-flow` or a hand-authored diagram.
- **caps** — `max 4` tiers is right (a fifth 96px band plus gutter breaks the frame). **The catalogue sets no cap on blocks per tier — set 5** at w=168, and note that block labels must fit ~16 characters at 18px over two lines. Worth adding a `focusIndex:text?` so the emphasised tier is authored rather than always defaulting to the top.

### sequence-flow
- **zones** — title `64,56 1152×48`; step numeral gutter `64,216 48×384`; four actor lanes `128 / 408 / 688 / 968, 136 248×...` — headers as filled chips `y=136 h=56`, lane rules 2px vertical at the lane centres x=252 / 532 / 812 / 1092 running `y=208 → 600`; six step rows `128,216 1088×64` (216 / 280 / 344 / 408 / 472 / 536, ending 600), each drawing an arrow between its source and target lane centres at the row's mid-y with the step label set **above** the arrow, centred on the span; footer `64,648 1152×32`.
- **focal** — the actor header row. Position (top, and it answers "who is in this system" before any step matters), weight (20/600 caps on filled chips against 18/450 step labels), ground (the chips are the only filled shapes above the lanes). Three vectors. No individual step may be promoted, or the sequence reads as ranked rather than ordered.
- **type** — title 32/600 · actor names 20 caps 0.08em · step numerals 18 caps muted · step labels 18–20/450.
- **accent** — the final step's arrowhead. It is positionally determined (last row), it marks where the sequence lands, and it is the only mark on the slide that is not repeated.
- **ux** — Shows who does what in what order across a boundary, which is the question every integration conversation actually opens with.
- **avoid** — Do not use it for a flow with branches or retries. Six ordered arrows cannot render a conditional, and forcing one in produces a diagram that is wrong rather than simplified.
- **caps** — `max 4` actors / `max 6` steps are both right. Step labels must fit ~26 characters for an adjacent-lane hop (280px span at 18px) and ~55 for a two-lane hop. Five actors drops lanes to ~192 and forces actor names under 14 characters — keep 4.

### now-next-later
- **zones** — title `64,56 1152×48`; three columns `64 / 456 / 848, 136 368×464`; per column — header `+0,+0 368×48` with a rule beneath, four cards `+0,+64 368×88` at a 104px pitch (200 / 304 / 408 / 512, ending 600); card internals — item `+16,+12 336×48`, meta caption `+16,+58 336×22`; footer `64,648 1152×32`.
- **focal** — the NOW column. Position (leftmost, first read), colour (its header rule and card grounds at full strength, NEXT one tint down, LATER two), weight (its header 20/600 against 18/510). Three vectors, and column widths stay equal because the columns are the same kind of thing.
- **type** — title 32/600 · column headers 20 caps 0.08em · card items 20/450 (≈28 chars/line, 2 lines) · card meta 18 muted.
- **accent** — the NOW column's header rule only.
- **ux** — Communicates sequence without committing to dates, which is the honest shape for work that has not been scheduled.
- **avoid** — Do not put a date in a card. The template exists precisely because the work is not calendar-committed, and one date in the NOW column converts the whole slide into a roadmap you will be held to.
- **caps** — `max 4` per column is right (4×88 + 3×16 = 400 in a 464 region with the header). Columns are independently sized, so a 4/3/1 shape renders honestly — never pad LATER for symmetry, because the taper is information.

### release-notes
- **zones** — version `64,56 640×72`; date `880,72 336×32` right-aligned; rule `64,168 1152×2`; two group columns `64 / 656, 208 560×392`, three groups per column h=120 gutter 16 (208 / 344 / 480, ending 600); per group — category `+0,+0 560×32`, items `+0,+40 560×80`; footer `64,648 1152×32`.
- **focal** — the version number. Scale (48 against 20 for item text), weight (600), position (top-left), spacing (its own 72px band above a rule). Four vectors.
- **type** — version 48/600 (−0.02em) · date 18 caps 0.08em muted · category headers 18 caps 0.08em · items 20/450 · footer 18.
- **accent** — the version numeral itself. Categories and items stay neutral — six accented category headers is a rainbow, not a hierarchy.
- **ux** — Answers "what is actually in this release" in the shape engineers and customers both already read: version, date, grouped items.
- **avoid** — Do not use it as a demo substitute. Release notes list what shipped; if the audience needs to see the change, pair it with `before-after-screens` rather than describing pixels in a bullet.
- **caps** — `max 6` groups is right for the 2×3 grid; a seventh breaks the column. Each group's item text must fit ~150 characters at 20px in 560×80.

### incident-summary
- **zones** — title `64,56 768×88`; impact stat `880,64 336×96`; duration stat `880,168 336×64`; timeline rule `64,360 1152×2` with five nodes at x=64 / 352 / 640 / 928 / 1216 (16px dots), time labels `above, y=296 h=32` and event text `below, y=384 h=48 w=256` centred on each node — **the first and last labels left- and right-align to the frame instead of centring, or they overflow**; resolution band `64,488 1152×104` with a label `+0,-32`; footer `64,648 1152×32`.
- **focal** — the impact stat. Scale (56, largest on the slide), colour (the only accent), position (top-right rail, isolated from the timeline), weight (600). Four vectors.
- **type** — title 36/600, two lines maximum · stat labels 18 caps 0.08em · impact stat 56/600 · duration stat 40/450 · timeline times 18 caps · timeline events 20 · resolution 24.
- **accent** — the impact stat. Not the resolution band — an accented resolution reads as relief and undercuts the impact figure the audience came for.
- **ux** — Gives a review the three things it needs in one frame: how bad, how long, and what closed it.
- **avoid** — Do not order duration above impact. A postmortem that leads with "resolved in 40 minutes" before "12,400 users affected" reads as defensive, and the room stops believing the timeline.
- **caps** — `max 5` timeline nodes is right. Six drops the node pitch to ~230 and the 256px event labels collide; if the incident needs six beats, the extra ones belong in the written postmortem.

### metric-dashboard
- **zones** — title `64,56 1152×48`; 4 × 2 tile grid — tiles `64 / 360 / 656 / 952` × `144 / 384`, each `264×208` (column gutter 32, row gutter 32, grid ends 592); tile internals (24px padding) — label `+24,+24 216×24`, figure `+24,+64 216×56`, delta caption `+24,+128 216×22`, sparkline `+24,+152 216×40`; footer `64,640 1152×32`.
- **focal** — the title line carrying the period. Scale (36 against 44 stats that are spread across eight tiles and therefore read as a texture), colour (the accent rule beneath it is the only colour on the slide), spacing (an 88px gap above a dense field). The tiles are deliberately co-equal — this is the one place where the focal is legitimately the frame rather than the content.
- **type** — title 36/600 · tile labels 18 caps 0.08em · tile figures 44/600 · delta captions 18 · footer 18.
- **accent** — the rule under the title. **No tile is differentiated by colour**: all figures neutral, all sparklines the same weight, because a coloured tile in a dashboard reads as an alert the data may not support.
- **ux** — Gives a working review its standing scoreboard, so the discussion starts from the same eight numbers every time.
- **avoid** — Do not use it when one metric matters more than the others. A dashboard flattens by design; if there is a headline, it belongs in `stat-hero` or `scale-anchor` and the dashboard is the follow-on slide. Sparklines are shape-only (216×40, no axes, no gridlines, endpoint dot) and must never be read as comparable across tiles — each has its own units and range.
- **caps** — `max 8` is exactly right: 4 × 2 fills the grid. Six re-flows to 3 × 2 at w=368. Below five tiles, use a stat row instead — a half-empty dashboard reads as missing data.

### rag-status
- **zones** — title `64,56 1152×48`; header row `64,136 1152×40` with a 2px rule at y=176; seven rows `64,184 1152×56` (184 / 240 / … / 520, hairlines, table ends 576); columns — status mark `64 w96`, workstream `176 w352`, owner `552 w200`, note `776 w440`; legend `64,608 560×32`; footer `64,648 1152×32`.
- **focal** — the status column, read as one vertical rail of marks. Position (leftmost, aligned), scale (32px marks against 18–20px text), shape rhythm (the column of discs is the only repeated geometry on the slide). Three vectors, none of them the deck accent.
- **type** — title 36/600 · header 18 caps 0.08em · status letters 18 caps 0.08em · workstream 20/510 · owner and note 18 · legend 18.
- **accent** — none. RAG is its own semantic triad and a fourth colour would compete with it. **Each status carries three non-colour signals**: R = filled disc + letter "R", A = half-filled disc + "A", G = hollow disc + "G", with the legend spelling all three out. Colour is the redundant fourth layer, never the encoding.
- **ux** — Puts every workstream's state, owner and one-line reason on one surface, so a steering meeting spends its time on the reds.
- **avoid** — Do not run it with every row green. An all-green RAG has told the audience nothing and trains them to stop reading the slide in future packs.
- **caps** — `max 7` is right: 7×56 = 392 leaves room for the legend, which is not optional on this template.

### logo-wall
- **zones** — title `64,56 1152×48`; logo grid `72,144 1136×296` — 6 × 2 cells w=176 gutter 16 (x=72 / 264 / 456 / 648 / 840 / 1032), rows h=136 gutter 24 (y=144 / 304); each mark aspect-FITs inside a 24px inset (128×88 usable), optically centred; stat block `64,488 560×112`; caption `656,504 560×96`; footer `64,648 1152×32`. With `stat` absent both it and the caption are removed and the grid re-centres to `y=200 … 560`.
- **focal** — the stat block when present. Scale (64 against 18 captions), colour (the only accented ink against an all-greyscale grid), spacing (isolated below a rule), position. With no stat the grid becomes the focal by mass alone, which is the correct honest render for a pure credibility slide.
- **type** — title 32/600 · stat 64/600 · stat label 20 caps 0.08em · caption 20 · footer 18.
- **accent** — the stat figure, or none when it is absent. **All logos render in a single neutral monotone** — otherwise a customer's brand colour becomes the slide's accent and the deck loses its palette on one slide.
- **ux** — Buys credibility in the two seconds before the argument starts, by showing who already said yes.
- **avoid** — Do not pad the grid to twelve. Six recognisable marks beat twelve with four nobody knows, and the weak ones are what the audience will ask about.
- **caps** — `max 12` is right for 6 × 2. With 7–11 marks, keep the 6-column pitch and leave the last row short-and-left-aligned rather than re-centring a ragged row. With ≤6, use a single centred row at w=176. Optical normalisation matters more than the box: cap wordmark width at 128 and glyph height at 72, or a square logo will look twice the size of a wide one at the same box height.

### case-study
- **zones** — logo `64,56 224×64` (aspect-FIT, monotone); customer `64,144 1152×64` (moves to y=56 when no logo); two panels `64 / 656, 240 560×216` — label `+0,+0 560×32`, body `+0,+40 560×176`; outcomes rail `64,488 1152×128` on a tinted ground — three blocks `64 / 456 / 848, 488 368×128`; footer `64,648 1152×32`.
- **focal** — the first outcome figure. Scale (56 against 44 for outcomes 2–3 and 22 for body), colour (the only accent), position (leftmost of a tinted band that reads as one object), spacing. Four vectors. Row order is authored: outcome 1 is the headline result, so the author controls the ranking rather than the layout inventing one.
- **type** — customer 40/600 (−0.02em) · panel labels 18 caps 0.08em · situation and change 22/450 (≈43 chars/line, 6 lines) · outcome 1 stat 56/600, outcomes 2–3 44/600 · outcome labels 18 caps.
- **accent** — outcome 1's figure.
- **ux** — Gives one named customer's before, change and result in the order a sceptical buyer asks for them.
- **avoid** — Do not use it when the outcomes cannot be quantified. A case study whose results are adjectives is a `testimonial-grid`, and rendering it here promises a figure the slide cannot deliver.
- **caps** — `max 3` outcomes is right. `situation` and `change` cap at ~260 characters each; longer copy pushes the panels into the outcomes rail, which the frame check will not catch because it only compares elements to each other.

### testimonial-grid
- **zones** — lead quote column `64,152 448×448`; support columns `544 / 896, 152 320×448` (gutter 32); per column — quote mark `+0,+0 48×56`, quote body `+0,+64 w×256`, attribution pinned at `+0,+384`: name `w×28`, role `w×24`. **Attributions sit on a shared baseline (y=536) across all three columns regardless of quote length**; quote bodies top-align at y=216. Footer `64,648 1152×32`.
- **focal** — the lead quote. Scale (26 against 22), spacing (a 448-wide column against two at 320), colour (its quote mark is the one accented element). Three vectors. Three quotes at identical size is a wall of italic; a designed grid leads with one and the author orders the strongest first.
- **type** — quote marks 48 muted · lead quote 26/450 (≈29 chars/line) · support quotes 22/450 (≈25 chars/line) · attribution name 20/600 · attribution role 18 muted.
- **accent** — the lead quote's opening quote mark.
- **ux** — Puts three independent voices on one surface, which is what makes a claim read as a pattern rather than an anecdote.
- **avoid** — Do not run unattributed quotes. A quote with no name and role is worth less than no quote, because it invites the audience to assume you could not get permission.
- **caps** — `max 3` is right. Cap the lead at ~200 characters and the supports at ~150; a testimonial that needs more is a `case-study`. With 2 quotes, keep the lead asymmetry (672 / 448, gutter 32) rather than splitting evenly.

### pricing-tiers
- **zones** — title `64,56 1152×48`; four tier columns `64 / 360 / 656 / 952, 144 264×472`; per column — name `+0,+24 264×32`, price `+0,+72 264×64`, period `+0,+144 264×24`, rule `+0,+176`, inclusions `+0,+184 264×160` (up to 5 items at a 32px pitch), footnote `+0,+392 264×24`. The highlighted tier renders `y=128 h=496` — 16px taller top and bottom — with a 2px all-round border and a caps ribbon at `+0,-32`. Footer `64,648 1152×32`.
- **focal** — the highlighted tier. Scale (a card 32px taller than its neighbours; its price 56 against 48), colour (accent border and ground), weight, spacing (offset out of the row's baseline). Four vectors, three of them non-colour, so the recommendation survives greyscale printing. With `highlightIndex` absent, no card is raised and the focal falls to the price rail — four prices on one baseline at the largest type on the slide, which correctly reads as a comparison rather than a recommendation.
- **type** — title 32/600 · tier names 20 caps 0.08em · prices 48/600, highlighted 56 · period 18 muted · inclusions 20/450 (≈22 chars/line) · footnote 18.
- **accent** — the highlighted tier's border and ribbon, as one card. None when `highlightIndex` is absent.
- **ux** — Lets a buyer self-select in one glance and tells them which tier you think they are.
- **avoid** — Do not highlight the most expensive tier by default, and do not build a three-tier layout where the middle exists only as a decoy. Both fail the sincerity test: the highlighted tier must be the one most customers should actually choose.
- **caps** — `max 4` is right but tight — 264px forces inclusion lines to ~22 characters at 20px. Three tiers (w=368 after re-division) reads considerably better; prefer it when the pricing allows.

### feature-matrix
- **zones** — title `64,56 1152×48`; header `64,136 1152×56` with a 2px rule at y=192; feature-name column `64 w512`; four value columns at `584 / 744 / 904 / 1064`, each `w152` (160px pitch); eight rows `64,200 1152×48` (200 / 248 / … / 536, hairlines, table ends 584); legend `64,608 768×32`; footer `64,648 1152×32`.
- **focal** — the subject column (value column 1). Colour (full-strength while columns 2–4 sit muted), ground (a faint tinted band running the table's height), weight (its header 20/600 against 18/510). Three vectors, none applied to the marks themselves.
- **type** — title 32/600 · column headers 18 caps 0.08em (subject 20) · feature names 20/450 (≈44 chars/line, one line) · marks 18 caps · legend 18.
- **accent** — the subject column's header rule only. **The marks are semantic and never colour-coded**: full = filled disc + "✓", partial = half-filled disc + "Partial", none = a hairline dash. An empty cell is forbidden — it is ambiguous between "no" and "not assessed", and the audience will read whichever is worse for you.
- **ux** — Answers "what do we have that they don't" in the format buyers already know how to scan.
- **avoid** — Do not choose features that only you have. A matrix with a full column of ticks on your side and crosses everywhere else is read as selection bias, and the audience discounts the whole slide.
- **caps** — `max 8` features / `max 4` columns are both right; 8×48 = 384 fits, and column headers must hold ~14 characters at 18px caps. Worth adding a `subjectIndex:text?` so the emphasised column is authored rather than always defaulting to the first.

### competitive-position
- **zones** — title `64,56 1152×48`; plot `400,112 480×480` (square, non-negotiable — unequal axes weight one dimension over the other); quadrant cross 1px at x=640 / y=352, muted; y-axis label rotated at `344,232 32×240`, x-axis label `400,608 480×32`, with low/high pairs at each axis end at 18 muted; player marks — competitors 12px hollow discs with 18px muted labels, "us" a 24px filled disc with a 20/600 label; labels offset 12px right of their dot, flipping left when two players fall within 40px; numbered side rail `944,160 272×240` listing all six players to match the marks; mandatory source `64,648 1152×32`.
- **focal** — the "us" mark. Scale (24px against 12px), colour (the only accented mark), weight (its label 20/600 against 18/450), fill (the only solid disc in a field of outlines). Four vectors.
- **type** — title 32/600 · axis labels 18 caps 0.08em · axis end labels 18 muted · player labels 18, "us" 20/600 · rail 18 · source 18 muted.
- **accent** — the "us" mark and its label, as one mark.
- **ux** — Puts the competitive claim on two named, sourced dimensions where it can be argued with rather than asserted.
- **avoid** — Do not choose axes that put "us" top-right by construction. That is what the mandatory `source` slot exists to make checkable, and an unsourced positioning map is a self-portrait the audience has seen before.
- **caps** — `max 6` players is right. Beyond six, labels collide inside a 480×480 plot regardless of the offset-flip rule, and the numbered rail stops being a fallback and becomes the actual chart.

### market-sizing
- **zones** — title `64,56 1152×48`; nest `64,136 480×440` — three rectangles sharing the bottom-left corner at (64, 576), sides scaled by √(value / tam) so **area** is proportional; TAM = 480×440, SAM and SOM scaled from it; three text blocks `608,152 / 608,288 / 608,424`, each `608×120` — label 18 caps, figure, basis line 18, with a leader from each rectangle's top edge; mandatory source `64,648 1152×32`.
- **focal** — the SOM figure. Scale (56 against 44 for TAM and SAM), colour (the only accent, on both the figure and the innermost rectangle's fill — one semantic mark), weight. Scale runs against it in the nest (its rectangle is the smallest), which is exactly right: the shape shows how small the claim is, the type shows that it is the only claim being made.
- **type** — title 32/600 · tier labels 18 caps 0.08em · TAM and SAM 44/600 · SOM 56/600 · basis lines 18 · source 18 muted.
- **accent** — the SOM figure and its filled rectangle. TAM and SAM rectangles are outlines only.
- **ux** — Shows the addressable market and the company's actual claim on it at the same scale, so the audience can see the gap rather than being told about it.
- **avoid** — Do not draw the nest non-proportionally. Three similarly-sized boxes is the exact defect this template exists to prevent. Where SOM/TAM falls below 1/400 the innermost rectangle stops being drawable — render it at a stated minimum side and print the ratio as text rather than faking the geometry.
- **caps** — `max 3` basis rows is right and should stay **locked** at one per tier rather than being a free list; a basis row with no tier to attach to is an assumption with nowhere to land.

### unit-economics
- **zones** — title `64,56 1152×48`; ladder `64,136 832×424` — six rows h=64 gutter 8 (136 / 208 / 280 / 352 / 424 / 496, ending 560); per row — label `64 w320`, bar segment `400 w336` with length proportional to |value| and costs drawn leftward from a shared right edge, value `752 w144` right-aligned; contribution block `944,200 272×176`; payback block `944,400 272×120`; footer `64,648 1152×32`.
- **focal** — the contribution stat. Scale (64 against 22 for row values), colour (the only accent), position (the right rail, where the ladder terminates), spacing (its own isolated block). Four vectors.
- **type** — title 32/600 · row labels 20/450 · row values 22/600 · contribution stat 64/600 · contribution label 20 caps 0.08em · payback stat 40 · payback label 18 caps.
- **accent** — the contribution figure.
- **ux** — Shows whether a single unit makes money, and where the money goes on the way, in the order the audience will interrogate it.
- **avoid** — Do not mix per-unit and aggregate figures in the same ladder; the whole claim rests on every row being the same unit. If the ladder needs more than six lines, it is a P&L — use `budget-variance`.
- **caps** — `max 6` rows is right (6×64 + 40 = 424 exactly). Bar lengths share one scale across all rows, anchored at zero.

### cohort-retention
- **zones** — title `64,56 1152×48`; chart `64,136 832×440` — plot area `144,152 640×376`, y-axis labels `64,152 72×376`, x-axis labels `144,536 640×32`, end-label gutter `784,152 112×376`; gridlines at 0/25/50/75/100% as muted hairlines; curves direct-labelled at their right end, **no legend**; headline block `944,200 272×176`; note `944,416 272×136`; footer `64,648 1152×32`.
- **focal** — the headline stat. Scale (64 against 18px axis labels), position (isolated right rail against a dense plot), spacing (176px block with one figure in it). Three non-colour vectors, because the accent is spent inside the chart where it does the legibility work.
- **type** — title 32/600 · axis labels 18 · end labels 18, newest cohort 20/600 · headline stat 64/600 · headline label 20 caps 0.08em · note 18–20.
- **accent** — the newest cohort's curve and its end label. Older cohorts render in one neutral at decreasing opacity by age — **never six different hues**, which is the standard way this chart becomes unreadable.
- **ux** — Shows whether the product's retention is improving cohort over cohort, which is the only version of a retention number worth presenting.
- **avoid** — Do not truncate the y-axis to flatten the curves or plot cohorts of wildly different sizes at equal visual weight without stating n. Both make a declining chart look stable.
- **caps** — The catalogue sets no series cap. **Set `max 6` series.** Beyond six, curves are indistinguishable at 640px and the direct end-labels collide inside the 112px gutter, which forces a legend the template does not have.

### hiring-plan
- **zones** — title `64,56 1152×48`; header row `64,136 1152×40` with a 2px rule at y=176; seven rows `64,184 1152×56` (184 / 240 / … / 520, hairlines, table ends 576); columns — role `64 w384`, function `464 w224`, period `704 w176`, count `896 w128` right-aligned, status `1040 w176`; total row `64,584 1152×48` under a 2px rule, count summed from the rows (derived, not a new slot); footer `64,648 1152×32`.
- **focal** — the count rail terminating in the total. Position (a single right-aligned column the eye tracks down), scale (the total at 28 against 22 in the rows), weight (600), spacing (the 2px rule isolating the total). Four vectors. This is the column the audience is actually being asked to approve.
- **type** — title 36/600 · header 18 caps 0.08em · role 20/510 · function, period 18 · count 22/600, total 28/600 · status 18 caps.
- **accent** — the total headcount figure.
- **ux** — Turns "we need to hire" into a countable, ownable, dated request.
- **avoid** — Do not leave the status column unfilled. Approved / open / proposed is the only thing separating a plan from a wish, and its absence is what makes the slide unapprovable. Status uses a shape plus its word (filled square = approved, half = open, hollow = proposed), never colour alone.
- **caps** — `max 7` is right: 7×56 = 392 plus a 48px total row leaves the footer band intact.

### org-target-state
- **zones** — title `64,56 1152×48`; two panels `64 / 672, 136 544×...` with a 64px centre gutter (608 → 672); panel headers `+0,+0 544×48`; five rows each `+0,+64 544×64` at a 72px pitch (200 / 272 / 344 / 416 / 488, ending 552); change markers centred in the gutter at each paired row's mid-y, drawn only when rows pair 1:1; note `64,592 1152×48`; footer `64,656 1152×24`.
- **focal** — the target panel. Position (right, the destination of the reading path), colour (full-strength ground while the current panel sits one tint down), weight (its header 20/600 caps against the current panel's 18/510). Three vectors.
- **type** — panel headers 20 caps 0.08em (target), 18 caps (current) · row labels 20/450 · row values 18 right-aligned · change markers 18 · note 18 muted.
- **accent** — the target panel's header rule.
- **ux** — Shows the shape of the organisation you are asking for beside the one you have, so the delta is read rather than described.
- **avoid** — Do not pad the two panels to equal row counts. If the target has fewer units, show fewer — the asymmetry is the message, and a symmetrical render hides the consolidation you are proposing.
- **caps** — `max 5` each is right at a 72px pitch. Change markers are a shape plus a word (→ unchanged, + added, − removed), never colour alone.

### raci
- **zones** — title `64,56 1152×48`; header `64,144 1152×64` — workstream column `64 w432`, five person columns at `520 / 664 / 808 / 952 / 1096`, each `w120` (144px pitch), each header carrying a name over a role caption; 2px rule at y=216; six rows `64,224 1152×64` (224 / 288 / … / 544, hairlines, table ends 608); cells hold a 32px chip centred in the column; legend `64,624 768×32`; footer `64,664 1152×24`.
- **focal** — the pattern of "A" chips across the grid, read as one scatter. Fill (the A chips are the only solid ones), weight (22/600 against 18 for the rest), shape (chip treatment differs per letter). Three vectors. The grid's job is to make "exactly one A per row" visible at a glance, so the A's are what the eye should assemble.
- **type** — title 36/600 · person names 18/600, role captions 18 muted · workstream names 20/450 · RACI letters 22/600 · legend 18.
- **accent** — the A chips, as one semantic mark set. No deck accent appears elsewhere on the slide. Letter treatment carries the meaning without colour: A = filled chip, R = outlined chip, C = letter only, I = muted letter. **A blank cell renders a hairline dash** — never nothing, or "not involved" is indistinguishable from "not filled in".
- **ux** — Makes accountability unambiguous by forcing exactly one owner per workstream onto the record.
- **avoid** — Do not render two A's in a row. The grid makes it visible, which is the point, but shipping it means the accountability question was never actually answered.
- **caps** — `max 6` workstreams / `max 5` people are right. Six people would drop the pitch to 120 and force names under 9 characters, which defeats a grid whose entire content is names.

### budget-variance
- **zones** — title `64,56 1152×48`; header row `64,136 1152×40` with a 2px rule at y=176; seven rows `64,184 1152×56` (184 / 240 / … / 520, hairlines, table ends 576); columns — line item `64 w416`, budget `496 w176`, actual `688 w176`, variance `880 w176`, variance bar `1072 w144` diverging ±72px from a zero rule at x=1144; total row `64,584 1152×56` under a 2px rule; note `64,656 1152×32`.
- **focal** — the variance column and its bar rail, terminating in the total. Weight (variance figures 22/600 against 20/450 for budget and actual), ground (a faint tint on the variance column running the table height), alignment (a single right-aligned rail), shape (the bars' divergence pattern reads as one silhouette). Four vectors.
- **type** — title 36/600 · header 18 caps 0.08em · line items 20/450 · budget and actual 20 · variance 22/600 · total row 24/600 · note 18 muted.
- **accent** — the total variance figure, one cell.
- **ux** — Shows not just what missed but by how much and in which direction, in a form the audience can scan for the two lines that matter.
- **avoid** — Do not encode over/under in red and green alone. The bar's **direction from the zero rule** is the primary signal and a "+/−" prefix is the second; colour is the redundant third. And never show variance without the driver note — a number with no explanation is a fact, not an answer.
- **caps** — `max 7` rows plus the total is right (7×56 = 392, total 56, note band intact).

### spend-breakdown
- **zones** — title `64,56 1152×48`; total block `64,136 384×200` (isolated in its own quadrant — the whitespace beneath it is the hierarchy, not an unfilled slot); rows `512,136 704×424`, six rows h=64 gutter 8 (136 / 208 / 280 / 352 / 424 / 496, ending 560); row internals — category `512 w256`, amount `784 w136` right-aligned, share bar `936 w200` proportional to share, percentage `1152 w64` right-aligned; footer `64,648 1152×32`.
- **focal** — the total stat. Scale (72, the largest thing on the slide), colour (the only accent), position (top-left, first read), spacing (200px of quadrant for one figure). Four vectors.
- **type** — title 32/600 · total stat 72/600 (−0.02em) · total label 20 caps 0.08em · categories 20/450 · amounts 22/600 · percentages 18 · footer 18.
- **accent** — the total figure. Share bars are one neutral at a single weight — a six-colour spend chart is the standard failure of this slide.
- **ux** — Answers "where did it go" with the total anchored first, so every share below is read as a fraction of a known number.
- **avoid** — Do not render shares that do not sum to 100% or a total that does not equal the sum of the rows. If there is a remainder, name it as a row — an unexplained gap is the first thing a finance audience finds. The optional prior-period column is best drawn as a hairline tick on each bar at the prior share position, so the delta is read as distance rather than as a seventh column.
- **caps** — `max 6` rows is right at a 72px pitch. Beyond six categories the shares get small enough that the bars stop discriminating; roll the tail into a named "Other" row.

### capacity-vs-demand
- **zones** — title `64,56 1152×48`; chart `64,136 832×440` — plot `144,152 752×376`, y-axis labels `64,152 72×376`, x-axis labels `144,536 752×32`; up to eight period groups at an 88px pitch, each a 36px capacity bar (outline) and a 36px demand bar (filled) with an 8px intra-pair gap; shortfall periods marked by a hatched wedge between the two bars; gap block `944,200 272×160`; note `944,400 272×136`; footer `64,648 1152×32`.
- **focal** — the shortfall region in the chart. Shape (the only hatched fill on the slide), colour (the accent), scale (the largest single marked area). Present regardless of whether the optional `gap` stat is filled, so the focal never depends on an optional slot; the stat, when present, is the label for it at 56 neutral.
- **type** — title 32/600 · axis labels 18 · gap stat 56/600 · gap label 20 caps 0.08em · note 18–20.
- **accent** — the shortfall wedge.
- **ux** — Shows when the team runs out of room before the commitment is made, rather than after.
- **avoid** — Do not compare capacity and demand in different units (FTE against hours, sprints against tickets). Normalise before rendering — the paired-bar geometry asserts they are the same measure, and if they are not, the wedge is meaningless.
- **caps** — The catalogue sets no caps. **Set `max 8` periods and exactly 2 series.** Nine groups drops the pitch below 80 and the paired bars merge visually; a third series turns the shortfall wedge into an ambiguous overlap. The y-axis starts at zero, always.

### sources-slide
- **zones** — title `64,56 1152×48`; two columns `64 / 656, 136 560×440`, four rows each h=104 gutter 8 (136 / 248 / 360 / 472, ending 576); per row — superscript number `+0,+0 40×24`, title `+56,+0 504×56`, publisher and date `+56,+60 504×24`; retrieval / as-at note (the `source` slot) `64,624 1152×32`; slide marker `64,664 1152×24`.
- **focal** — the title. Scale (32 against 20), weight (600), spacing (an 80px gap above a quiet two-column field). Three vectors, none of them colour — this is the one slide in the deck that should carry the lowest visual energy, and a sources page that competes with the argument is a design error.
- **type** — title 32/600 · superscript numbers 20/600 · source titles 20/450 · publisher and date 18 muted · as-at note 18 muted.
- **accent** — none. A reference page is a record, and colour on it reads as emphasis nobody intended.
- **ux** — Lets any figure in the deck be traced to its origin, which is what makes the rest of the deck's numbers checkable rather than assertable.
- **avoid** — Do not renumber on reorder. The numbers must match the in-deck superscripts exactly; a source list whose numbering has drifted from the slides is worse than no source list, because it looks rigorous and is not.
- **caps** — `max 8` is right for 2 × 4. Beyond eight sources the deck needs an appendix, not a slide; cap each source title at ~100 characters over two lines at 20px in 504px.
