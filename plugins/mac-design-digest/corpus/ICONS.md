# ICONS.md — icon corpus synthesis

> Load when designing a mac app icon. Corpus: **134 icons** (macapp.supply digests). Updated 2026-07-19. Corpus level: **Proficient** (icons only; no UI cross-check needed to design a mark).
>
> **Lineage caveat, load-bearing:** icon observations carry no framework-lineage field, so `nativeCount = 0`. Nothing here is promoted to *macOS native canon* the way `TASTE.md` UI rules are — these are **icon-level** canon (≥3 independent icons, none contradicting) and **candidate/recurring** style families. Hue families are DERIVED (HSV bucketing of observer-recorded hex). Most sources were 100–540px web renders, a few native 1024 masters; fine specular/gradient detail is `(estimated)` unless a master was seen. Raycast (4/12) is a corrupted/upscaled thumbnail per its own digest — **excluded from all canon and family counts below where it would pollute**.

## Era distribution — and what it teaches

| era | n | share | reading |
|---|---|---|---|
| big-sur | 61 | 46% | front-facing object/glyph on a gradient squircle, top-down baked light, micro-shadows — the 2020 idiom |
| custom | 38 | 28% | off-platform / web-first / brand-mark tiles that commit to **no** mac era (Electron/Figma/Blender exports) |
| liquid-glass | 16 | **12%** | the only cohort dressed in the current (macOS 26/27) glass idiom — and half-hearted (see #10) |
| skeuomorphic-quote | 13 | 10% | deliberate pre-Yosemite object quotes (photoreal keycaps, dials, leather) rendered in a modern squircle |
| flat-transition | 6 | 4% | flat marks mid-migration, neither Big Sur depth nor glass |

**The lag is the story.** Big Sur + skeuomorphic-quote = **74/134 (55%)** are pre-Liquid-Glass idioms; add flat-transition and it is 80 (60%). Only **12% wear the current era's clothes**, and even those mostly bake the glass into a flat raster rather than authoring system layers. A generated 2026 mac icon that adopts real Icon Composer layer discipline is, on this evidence, ahead of ~88% of the shipping field. The corpus teaches the *legacy* vocabulary richly (object tiles, tool-at-an-angle, glossy material) and the *target* vocabulary thinly — so design the target deliberately, don't imitate the mode.

Rubric health: min 4 / median 11 / mean 10.32 / max 12 (n=134). 15 icons ship clean (no failures); 119 carry ≥1.

## Recurring palette families (hex ramps + members)

Derived hue tallies across all recorded hex (bg + glyph + accent): white/near-white 180 · blue 169 · grey/silver 105 · indigo/violet 102 · black/near-black 85 · orange 71 · red 68 · yellow 60. Blue + indigo/violet dominate chromatic choice; white/charcoal/grey dominate grounds.

- **Electric blue** `#37D0FE → #0088FF → #0054EB` (light→core→deep; kit Blue `#0088FF`). Members: 1password, cleanshot-x, canary-mail, picmal (`#1B5BFF→#CBDEFF→#F2F6FF`), supaste, cachesweep, vocal-notes, slashit-app (cobalt), unfumble (azure→indigo), textsniper (cyan→violet). The category-default utility hue.
- **Indigo / violet** `#6D7CFF → #6155F5 → #3A2E8C` (kit Indigo `#6155F5`). Members: tuple, obsidian, screen-studio, usage, uninstally, presentify, revone, room-service, purge. The **AI-agent sub-ramp** (violet→blue glass): codex, inkline-text-editor, maestri, mailtwin (pink→violet), lookaway, mac-4-breakfast.
- **White / cream ground** `#FFFFFF · #FBF3E7 · #FFFBF3` (flat pale field, object floats). Members: notion, codex, dia, waterlemon, mymind, mole, tono, klack, caesura, hejour. The logomark / clay-object register.
- **Charcoal / near-black ground** `#2D2D30 → #0F1012` (top-lit vignette) / flat `#13120B`. Members: cursor, unfold, glaze, sero, prostir-zvuku, atlas, cooldock, wallspace, toplify, subscription-day, onlook, noticky, screen-charm. The dark-premium / emissive stage.
- **Monochrome metal** `#E8EAEE → #A6B1C2 → #565B65` (silver-on-charcoal, zero hue). Members: looq-preview, framer, creos, orbs, fello-ai, sessionwatcher, pieoneer, macusb, liqoria, coreviz-studio. Reads pro / menu-bar-native.
- **Warm accent** (orange/red/yellow, usually a single bounded jewel). Members: folder-hub (amber→black), macwall (red sun), hora-calendar (coral), fantastical (red band), foldervitrine (orange sun in cool frost), minarah (gold finial), tokens-4-breakfast (amber-orange), lookaway (pink→peach).
- **Acid green / lime** (rare, high-commitment brand). Members: ayron-time-tracker (`#C6F04C`+black), leafy-vocabulary (highlighter green), slapmac (green drench), super-shortcuts `#1F9D6F`, mac-4-breakfast.

## Recurring devices (with members)

Device-motif keyword frequency: glass/refraction 44 · subject-mined literal object 35 · concentric/radial 30 · device/hardware portrait 30 · monogram/letterform fusion 26 · diagonal-tool overlay 25 · mascot/face 25 · emissive glow focal 23 · double-read/pun glyph 21 · negative-space cut 16.

- **Diagonal tool-at-an-angle** (Apple TextEdit/Preview lineage): cleanmymac, uninstally (broom), deskminder (needle), spacepeek (loupe handle), macusb, dropadoo (paperclip), sweeper.
- **Concentric / radial** (ring, dial, aperture, spinner): 1password (vault dial), radial, orbs, hilium, coreviz-studio, code-meter (gauge), room-service (washer), screen-studio (record ring), pieoneer (pie aperture).
- **Notch / screen / device portrait**: agentpeek, droppy, folder-hub, dynamiclake, tellie, alcove, corner-time, healthynotch, codeshot.
- **Double-read / name-as-image pun**: 1password (1=keyhole), finbar (fin+bar), caesura (// pause), ajar (lid=arrow), waterlemon (watermelon in lemon-yellow), backdrop (a drop), maestri (prompt=face), tokens-4-breakfast (token=coin), mux (fork).
- **Negative-space cut**: hoolo (owl), mole (anatomy), compresto (pinch waist), notion (label plate), atlas (radial burst), resurf (R knockout), hejour (checkmark).
- **Emissive glow focal (self-lit)**: dropzone, onlook, sero, screen-studio, noticky, lookaway, usage, viaduct, prostir-zvuku (23 total).

## Icon canon (≥3 independent icons, none contradicting)

| Rule | Evidence | Members (sample) |
|---|---|---|
| **Subject-mine, don't stock-glyph.** The strongest marks draw the app's literal noun/verb, not a generic category symbol. | 35+ icons; the whole top of the rubric | cleanshot-x (capture-as-peel), unfold (spacebar key), klack/keeby (keycap), mole (digging claw), spacepeek (ring-as-lens), 1password (numeral-keyhole), minarah (minaret), viaduct (arch), sweeper (trash), soulver (domain keypad) |
| **Palette economy: ≤2 hue families, accent bounded or absent.** Monochrome or single-hue-plus-one-jewel is the disciplined majority. | 66/134 carry **no accent at all**; "monochrome" is the #1 adjective (19) | cursor, unfold, compresto, coreviz-studio, framer, fello-ai, satu, voiceos, mural, prostir-zvuku, cooldock |
| **Identity must survive a two-value silhouette.** Top scorers read filled-black; the failures collapse to a plain squircle. | #3 failed by 26 icons (the anti-case); 12/12 scorers all pass | passes: klack, unfold, mole, coreviz-studio, mural, notion / fails: cleanshot-x, alcove, fantastical, drivemosaic |
| **Top-down soft light + baked micro-shadow — the model wherever light is modeled, not everywhere.** From top(-left) with a short contact shadow. It is the *plurality* (36% of all 134) and the dominant read among light-modeling icons (~72%), **not** a universal default — the 18-member Dark-Field Emissive cluster deliberately inverts it to self-lit ground (a scoped contra-current; see cluster 4). | 48 "top-down soft + specular" + 19 specular-only = **67/134** top-lit ≈ **72% of the 93 light-modeling icons**; 41 flat/null and 23 self-lit emissive sit outside the rule | 1password, keeby, klack, radial, sessionwatcher, deskminder, presentify |
| **Name-as-image double-reads reward the squint.** A glyph that is simultaneously the name and the function outperforms a decorated letter. | 21 double-read/pun glyphs, none contradicting | 1password, finbar, caesura, ajar, waterlemon, maestri, mux, backdrop |

*Contested (both readings held):* **squircle vs. free object** — most icons commit to the system squircle full-bleed, but the photoreal-object family deliberately refuses it and ships a transparent free silhouette (klack, keeby, compressor, waterlemon, grape). Neither is wrong; it tracks the skeuomorphic-quote cluster boundary.

## The #10 epidemic — variant robustness (the era's defining gap)

**102/134 icons (76%) hard-fail check #10** (Liquid-Glass variant robustness: does the mark survive Default/Dark/Clear/Tinted system renders?). The remaining 32 only **soft-pass** — **zero icons cleanly pass**. The failure even reaches the current cohort: **6 of the 16 liquid-glass-era icons fail #10**.

**One root cause, repeated across digests:** the delivered art is a **flat, pre-masked raster** — a single baked PNG (corners already alpha-cut, shadow/rim baked in), with identity carried by a **colour relationship** rather than **separable Icon Composer layers**. Tint or de-colour it and the relationship collapses (cleanshot-x's blue-vs-charcoal peel; dia's spectrum *is* the identity; every glow-on-black emissive mark). macapp.supply serving web renders inflates this, but the digests confirm most masters are genuinely single-layer.

**Design implication (the corpus's most actionable lesson):** author the mark as **2–4 real layers** (background / mid / foreground / optional highlight) whose read survives when the system flattens hue to a monochrome tint — carry identity in **shape + value**, let colour be the last 10%. This one discipline would lift more icons than any composition change.

## Icon style clusters (candidate/recurring — promotable only with lineage the icon layer lacks)

> **Reading the `~N` counts (transparency):** each `~N` is the *estimated cluster population* — icons assignable to the cluster — not the count of slugs printed below it. Clusters overlap (e.g. dropzone/sero/screen-studio sit in more than one), so the populations sum past 134 by design. Each block lists only representative **exemplars** (the `…`/`+` markers are non-exhaustive), so `~N` cannot be reconstructed from the visible slugs — it rests on the per-icon observations, not on this file. For audit: the **named-exemplar** counts actually shown per block are 17 / 13 / 15 / 16 / 12 / 11 / 8 / 7 (clusters 1–8), against asserted populations of ~55 / ~35 / ~20 / ~18 / ~21 / ~17 / ~18 / ~8.

### 1. Big-Sur Object Tile — *"a photoreal or clay noun on a gradient squircle"* (peers: classic Preview, Pixelmator)
- **Members (~55):** skeuomorphic/photoreal (bartender-6, cleanmymac, code-meter, codeshot, letterboxx, zipic…) + 3D-clay (compressor, minarah, mymind, presentify, revone, waterlemon) + single-object-on-gradient (autoshelf, glyph, macrest, soulver, walltune).
- **Signature:** front-facing object, top-down baked light, glossy/candy or matte-clay material, contact shadow, one saturated field.
- **Do:** subject-mine the object; keep one hue field + one accent. **Don't:** ship it flat-baked — this cluster is the heart of the #10 failure.

### 2. Liquid-Glass Frosted Object — *"a saturated glass lens floating on a frosted slab"* (peers: macOS 26 system apps, textsniper)
- **Members (~35):** ajar, codex, dropzone, finbar, foldervitrine, room-service, sero, spacepeek, textsniper, mux + AI violet→blue glass-blob (cursor, inkline, maestri).
- **Signature:** translucency, specular top-rim, refraction tint, frosted ground; often a glass glyph over a paler slab.
- **Do:** actually separate the glass layer from its ground so tinted/dark variants hold. **Don't:** fake it as one baked gradient (the trap 6/16 fell into).

### 3. Flat Monochrome Logomark — *"the brand mark, verbatim, zero-to-one hue"* (peers: Vercel, Linear, Notion)
- **Members (~20):** atlas, compresto, coreviz-studio, cursor, hoolo, notion, notion-calendar, satu, voiceos, mural, hora-calendar + flat two-tone (bauhaus-clock, caesura, mole, super-shortcuts).
- **Signature:** keyline-as-depth, negative-space cut, ~18–21:1 contrast, no material.
- **Do:** lean on silhouette and counter-space (this cluster passes **#3** cleanly — 0/15 members fail it, the best #3 record in the corpus). **Don't:** forget the shipping white/dark field — several assets arrive field-less.
- **#10 caveat (measurement honesty):** strong silhouette does **not** buy tint-robustness here. 14/15 members **hard-fail #10** (only caesura soft-passes) — a 7% soft-pass rate vs. the 24% corpus baseline, i.e. this cluster fails #10 *worse* than average, not best. The marks ship as flat one-layer rasters, so a mono logomark only *becomes* tint-robust once authored as real layers — that is a composition claim (it *would* survive tint if layered), not the scored #10 outcome it currently earns.

### 4. Dark-Field Emissive — *"a glow-on-black focal that lights its own ground"* (peers: Arc, Raycast's true mark, Siri orb)
- **Members (~18):** backdrop, dropzone, lookaway, noticky, onlook, screen-studio, sero, usage, viaduct + spectrum-blob (dia, heatscope, prostir-zvuku) + charcoal single-white-glyph (cooldock, radial, toplify, wallspace).
- **Signature:** near-black vignette stage, self-lit focal, single warm or violet accent, nocturnal.
- **Do:** one luminous focal, ruthless restraint. **Don't:** rely on the glow surviving a mono tint — pair it with a shape.

### 5. Mascot / Character — *"a personified creature or face carries the brand"* (peers: Bartender, Duolingo-adjacent)
- **Members (~21):** agentpeek, bartender-6, claude-notch-usage-companion, glance, keeby, mole, mymind, pokey, tono, zush, slapmac, waterlemon.
- **Signature:** eyes/face as focal, friendly, warmth over utility; the mascot rarely states function.
- **Do:** give it a catchlight and a readable silhouette. **Don't:** let charm cost legibility at 16px.

### 6. Device-Portrait / Notch-Screen — *"the Mac hardware itself is the subject"* (peers: menu-bar utilities)
- **Members (~17):** agentpeek, alcove, corner-time, codeshot, droppy, dynamiclake, folder-hub, healthynotch, maestri, tellie, mjsfx.
- **Signature:** notch cutout, screen-in-bezel, rounded-top "the squircle IS the display", bottom-up screen glow.
- **Do:** quote the notch/screen literally — it reads instantly. **Don't:** over-detail the bezel; it vanishes small.

### 7. Big-Sur Diagonal-Tool / Cleaner — *"a maintenance tool crosses the plane at an angle"* (peers: TextEdit, CleanMyMac)
- **Members (~18):** cleanmymac, uninstally, deskminder, spacepeek, macusb, dropadoo, sweeper, cachesweep (sparkle-clean).
- **Signature:** tool-at-an-angle overlay, sparkle trail, saturated field, single white glyph.
- **Do:** use it when the verb is "act on files". **Don't:** default to it — it is the most template-worn move in the corpus.

### 8. Data-Viz / Ring-Chart Emblem — *"the app's own chart becomes the mark"* (peers: Activity Monitor, Disk utilities)
- **Members (~8):** code-meter (gauge), drivemosaic (treemap), nox, sessionwatcher (bars), spacepeek (donut), subscription-day (radar), radial (spinner).
- **Signature:** in-product artifact quoted at icon scale, category-colour encoding, concentric geometry.
- **Do:** quote the exact object the user will use. **Don't:** carry a legend of hues that smears at 16px (#6 risk).

## Device bank — best subject-mined glyph ideas (slug — device)

- **1password** — numeral-as-keyhole (the brand "1" IS the lock slot) + concentric vault dial
- **unfold** — the spacebar key debossed as a ⊔ well (the Quick Look *gesture*, not a file/eye)
- **cleanshot-x** — capture-as-peel (screenshot lifted off the desktop as a physical sheet)
- **mole** — digging-claw forepaw as the one detail that means "digs through your disk"
- **spacepeek** — ring-as-lens (disk-usage donut doubles as the magnifier)
- **finbar** — shark "fin" + menu "bar"; waterline doubles as a selected list-row
- **caesura** — the // musical pause mark IS the name, function, and typographic origin
- **maestri** — terminal prompt reimagined as a winking face (`>` eye, `|` cursor eye)
- **mux** — fork junction where cap shape carries meaning (arrowhead = redirect, foot = stay)
- **soulver** — 2×2 keypad of `$ % clock =` spells the feature set as glyphs
- **tokens-4-breakfast** — a coin that is both "tokens for breakfast" and "token = currency"
- **codex** — terminal `>_` knocked out of a glass cloud (cloud agent + CLI in one move)
- **ajar** — laptop lid at an angle that also reads as an upward arrow / light rising
- **waterlemon** — watermelon slice rendered in lemon-yellow (the name made visual)
- **open-screen-shot** — descending dots resolving into a down-arrow = "scrolling screenshot"
- **sweeper** — macOS Trash silhouette overflowing with the colourful apps it discards
- **klack** — a literal 3D mechanical keycap with a diegetic "K" molded into the top face
- **hoolo** — an owl built entirely from negative-space cuts; the "oo" doubles as eyes
- **walltune** — a wallpaper physically unrolling to reveal the vibrant field beneath
- **shake-it-on** — a mouse-jiggler drawn as maracas, the macOS cursor shaken as a prop
- **screen-studio** — a luminous record-ring that is also the lens aperture "O"
- **compresto** — compression drawn as an inward pinch to a hollow negative-space waist

## Design-mode checklist (icons)

1. **Pick era deliberately, not by imitation.** The corpus is 55% pre-glass — choose Liquid-Glass layer discipline on purpose (you'll beat 88% of the field), or quote an older idiom knowingly.
2. **Choose the cluster by function:** act-on-files → Diagonal-Tool; brand-led app → Flat Monochrome Logomark; utility/menu-bar → Big-Sur Object Tile or Dark-Field Emissive; hardware subject → Device-Portrait; data app → Ring-Chart Emblem; personality-led → Mascot; current-era hero → Liquid-Glass Frosted Object.
3. **Subject-mine first.** Draw the app's literal noun or verb (device bank for ideas) before reaching for a stock category glyph.
4. **Sketch the silhouette; run the 16px squint + the solid-black fill test.** If identity dies when filled black (#3) or smeared to menu-bar size (#4), rework shape/value before colour.
5. **Set palette economy:** ≤2 hue families + one bounded accent (or none). Pick a ramp from the families above.
6. **Author real layers for #10.** Build background / mid / foreground (/ highlight) so the mark survives Default/Dark/Clear/**Tinted** — carry identity in shape+value, colour last. This is the single highest-leverage step; 76% of the corpus fails here.
7. **Audit against the 12-point icon rubric; report the score and every #10 liability honestly.**
