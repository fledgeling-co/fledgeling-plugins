# Icon Directions — choosable recipes for generating a mac app icon

Distilled from **three corpora**: the original 134 macapp.supply digests (`ICONS.md`, in the sibling `mac-design-studio` skill — not bundled here), the **500 most recent macosicongallery.com icons** (2022-02 → 2026-07), and **32 ground-truth macOS 26 "Tahoe" captures** of Apple's own system set + current-idiom third parties. What is bundled: `corpus/` (read `corpus/SYNTHESIS.md` for the aggregate and what it retains from the two corpora whose images were dropped; `corpus/apple-2026.md` for the Tahoe answer key; `corpus/apple-2026/` holds the 32 ground-truth captures at ~512px, usable as raster-engine style references). Each **direction** is a style family made buildable: commit to ONE per icon — from this catalogue, a hybrid, or a novel composition the subject earns (declare a novel one with the same rigour: palette recipe, composition recipe, light model, #10 layering plan). Canvas is always 1024×1024 full-bleed; the system applies the squircle mask + drop shadow — design inside the mask, never bake corners or shadow.

> **Calibration flags:** the corpus's template-default is the **stock-glyph-on-blue/indigo ramp** — technically clean, communicates nothing (the `sparkles`-on-indigo problem: it says "AI app", not *this* app). Blue/indigo grounds need positive justification, and the glyph must name this subject, not its category. The glyph idea comes from subject-mining (the device bank below), never from the SF Symbols default set alone.

**The corpus's one load-bearing lesson (read before choosing anything):** 76% of shipping icons hard-fail variant robustness (rubric #10) because they ship a *flat pre-masked raster* — identity carried by a colour relationship that dies under Dark/Clear/Tinted. Every recipe below therefore ends in a **#10 layering clause**: author 2–4 real layers (background / mid / foreground / optional highlight), carry identity in **shape + value**, let colour be the last 10%. Do this and you beat ~88% of the field on the current era's defining gap.

**The lag is confirmed at 4× the sample.** In the 500-icon gallery census, liquid-glass is 0% of 2022–2024 icons, spikes to 64% only in the Nov-2025 system-release wave (Apple's own set), and falls back to ~16% across 2026 indies. Apple has fully moved; third parties have not. Authentic Tahoe grammar remains the single cheapest way to look ahead of the shipping field.

---

## The Tahoe gel-glass grammar — the current era's answer key

Learned from the 32 Apple/system captures (`corpus/apple-2026.md`) and confirmed by the Nov-2025 wave in the gallery census. These nine tells are what separates a real macOS 26 icon from a Big Sur re-tread — apply them whenever the chosen direction is current-era:

1. **The tile is a cushion, not a print.** Every ground — porcelain or saturated — carries a subtle inner rim light around the perimeter and a gentle edge vignette. A dead-flat background is instantly previous-era.
2. **Two ground registers dominate.** (a) **Porcelain near-white** (`#FAFAFB`-ish) carrying a colored gel object with a soft cast shadow — Safari, Photos, News, Slack, Find My, Home. (b) **Saturated single-hue vertical-gradient gel tile** carrying a **white frosted glyph** — Mail, App Store, Weather, Keynote. Dark charcoal is the pro/system minority register (Passwords, Icon Composer, Activity Monitor). Pick one register and commit.
3. **Glyphs are poured, not drawn.** The default material is soft-extruded translucent gel/resin: generous rounded corners, a soft top-edge highlight, faint inner glow, small soft drop shadow. Flat brand marks get **re-materialised, not redrawn** (News N, Slack pinwheel, the iWork set) — silhouette untouched, material swapped.
4. **White is a material.** A white glyph is frosted glass/porcelain — the ground's hue visibly bleeds through its thinner areas, with fold/emboss shading. Flat `#FFFFFF` with no ground-bounce is the batch-04 warning: *white-on-hue without translucency cues = flat Big Sur re-tread.* The cues ARE the era.
5. **Authored overlap is the signature craft moment.** Wherever two shapes cross, hue visibly blends — multiplying darker (Photos petals) or additively lightening (QuickTime's Q, Shortcuts' diamonds, App Store's sticks, Weather's sun-through-cloud). This bleed-through is precisely what a baked flat raster cannot fake under system tinting — authoring it forces the layer discipline #10 demands.
6. **One soft top light, zero hard speculars.** Depth = rim highlights + soft AO. The sanctioned second light is an **emissive interior under glass** (Siri orb, Tips bulb, Home's inner glow, Activity Monitor's neon trace).
7. **3D miniatures survive, softened.** Object icons (loupe, tower, calculator, binoculars, podium) persist as toy-scale renders in matte-satin/clay with real contact shadows — never chrome-gloss, one clearly-lit object.
8. **Sanctioned garnish:** micro diegetic engraved text as an easter egg (Mail's "Apple Park, California 95014", "PREVIEW 10×") — sub-legible, on an object, never a headline; ultra-low-contrast patterned grounds (Xcode's blueprint grid, sparkle stars); edge-bleed devices that treat the mask as a physical boundary (Contacts' index tabs, a tile-as-machine slot).
9. **Radical flat abstraction is legal when the silhouette is iconic** (Calendar's dot-matrix, Notes, Clock) — but must still sit on a cushion tile.

**Composition constants:** one focal object at ~55–65% tile width, optically centred (or a deliberate offset badge, à la Maps); concentric radii; palette economy unchanged — porcelain + one gel hue family, or saturated tile + white frost; multi-hue only when the brand/domain IS multi-hue, then quarantined inside one shape.

---

## The 8 directions

### 1. Object Tile (Big-Sur descendant)
**Essence:** a photoreal or clay *noun* front-facing on a gradient squircle. The heart of the corpus (~55 icons) and the heart of the #10 failure.
**Exemplars:** cleanmymac (magenta iMac), waterlemon (candy fruit), soulver, presentify, minarah, revone, mymind.
**Palette recipe:** one saturated hue field + one bounded accent. Field ramp light-at-top→darker-bottom within a single hue, e.g. periwinkle `#F3EDFF→#D8CCF5`; reserve the saturated accent (`#EC2DCB` magenta) for the focal object only.
**Composition:** background = single-hue sky ramp (or flat white plate, à la waterlemon) → glyph = the app's literal object, front-facing, top-down baked soft light with a short contact shadow and a modest specular sheen → overlay = none (add a diagonal tool only if the verb is "act on files" → use Direction 7 instead). **Era:** Big Sur; **light:** top-down soft, one source.
**When to choose:** the app has a concrete physical noun and a warm/consumer personality.
**Do:** subject-mine the object; keep ≤2 hue families. **Don't:** float bright-on-white without a darker rim (waterlemon fails #7 at 1.4:1); don't bake gloss as your identity.
**Tahoe-softening (to keep this direction current):** swap candy gloss for matte-satin/clay, give the object a real contact shadow, and put it on a cushion tile — the 3D-miniature idiom survives the era change only in soft materials (the loupe/tower/calculator captures; parcel, The Unarchiver). Hard gloss sweeps, lens flares, and chrome now read as instant era-markers for "old".
**#10:** separate object / field / contact-shadow / specular into layers; make the object's silhouette + internal value read when hue flattens to a mono tint — do not let the field colour be the only thing distinguishing figure from ground.

### 2. Tahoe Gel-Glass (Liquid-Glass, the target era — now with the answer key)
**Essence:** the current system idiom, per the grammar section above. Two committed sub-registers plus a dark variant; all three live or die on *authored translucency*.
**Exemplars:** system ground truth: Mail, App Store, Shortcuts, Photos, Weather, Safari, Finder, Contacts, Game Center, Configurator; third parties who got there: darkroom, elytra, mindnode, dropzone-5, multi, mercury-weather, WhisperType; earlier AI sub-ramp: codex, cursor, inkline, maestri.
**Sub-register (a) — porcelain + gel object:** near-white cushion tile `#FEFEFE→#F1F1F1` with faint rim + vignette → one colored soft-gel object (or re-materialised brand mark) with top-edge highlight, inner glow, soft cast shadow. Where the object's shapes overlap, hues visibly blend. (Safari, News, Slack, iA Writer, CleanMyMac, copilot, parcel.)
**Sub-register (b) — saturated tile + white frost:** single-hue vertical-gradient gel tile (e.g. blue `#4B8DF8→#2E6BF0`, violet, coral) → white **frosted** glyph whose thinner areas let the ground hue bleed through, with fold/emboss shading and a soft drop shadow. Never flat `#FFFFFF`. (Mail, App Store, Weather, Keynote, Messages formula.)
**Sub-register (c) — dark glass:** charcoal/near-navy cushion tile → tinted translucent glass objects with strong rim light, or an emissive interior under glass. (Passwords, Icon Composer, Activity Monitor, the sticker/butterfly captures.)
**Palette recipe:** one hue family per icon, differentiated by luminance/opacity — Apple's 26 set is strictly tone-on-tone. The AI violet→blue ramp (`#C3AFFE→#A091FF→#5D7CFE→#3333FF` with a warm crown bloom) remains legitimate but is now the *most* template-worn glass move — justify it.
**Era:** Liquid Glass; **light:** one soft top light, rim highlights + soft AO, optional emissive interior; zero hard speculars.
**When to choose:** any current-era hero icon; the default when the brief says "make it feel native to macOS 26".
**Do:** author the overlap blends for real; give white objects ground-hue bounce; keep the tile a cushion. **Don't:** bake it as one gradient (the trap 6/16 glass-era icons fell into); don't ship white-on-hue with no translucency cues (batch-04's named failure); don't let a thin light-on-gradient glyph be the whole read (codex smears at 16px).
**#10:** this direction can *actually pass* when authored right — ground slab / gel glyph / highlight+bloom as separate planes over a swappable ground. The 32 Apple captures all decompose this way; that is why they survive Dark/Clear/Tinted.

### 3. Monochrome Logomark (era-agnostic brand mark)
**Essence:** the brand mark verbatim, zero-to-one hue, silhouette does all the work.
**Exemplars:** notion (N-block), coreviz-studio (hex-nut), cursor, atlas, compresto, mole, caesura, hoolo.
**Palette recipe:** achromatic or one hue. Two tones only — off-white `#F8F8F8` on `#000000` (~19:1), or ink-on-paper `#000` on `#FFF`. No gradient, no accent.
**Composition:** background = flat field (commit to shipping WHITE or BLACK — several corpus assets arrive field-less and float in the Dock) → glyph = negative-space cut or keyline-as-depth mark, optically centred with safe-zone margin → overlay = none. **Era:** custom/flat; **light:** none (flat is internally consistent).
**When to choose:** strong existing brand mark; austere/pro/developer personality; Vercel/Linear/Notion register.
**Do:** lean on counter-space and silhouette (this family passes #3 cleanly — 0/15 fail it). **Don't:** ship field-less; don't rely on a strong silhouette to buy #10 — it does NOT (14/15 members hard-fail #10).
**#10:** the honesty trap — a mono mark is only tint-robust once *authored as layers*. Ship an explicit dark variant + a tint-safe layer where the glyph is a filled shape (not a white-on-black knockout that inverts to invisible on a light tint).

### 4. Dark-Field Emissive (nocturnal focal)
**Essence:** a glow-on-black focal that lights its own ground. Deliberately inverts the top-down-light majority.
**Exemplars:** sero (emissive ring), dropzone, onlook, screen-studio, usage, viaduct, backdrop; spectrum-blob: dia, prostir-zvuku.
**Palette recipe:** near-black cool ground `#161616→#14283C` + ONE adjacent-hue emissive sweep. Sero's conic: electric blue `#189FFC` → pale lavender `#E1D1FF`. Warm alt: amber→red. Saturation lives entirely in the focal.
**Composition:** background = near-black vignetted void → glyph = a single self-luminous focal (ring/aperture/orb) blooming a halo into the black → overlay = none; add a radial center vignette for cheap depth. **Era:** custom dark emblem; **light:** emissive (the glyph IS the source), no scene light.
**When to choose:** AI/utility/menu-bar app; premium nocturnal personality; single strong focal shape.
**Do:** one luminous focal, ruthless restraint; pair the glow with a *carrying shape* (sero passes #10 where alcove fails — because the ring silhouette survives tinting, the glow drama doesn't need to).
**Don't:** rely on the glow surviving a mono tint; don't let the black ground be load-bearing for the read.
**#10:** carry identity in the focal's shape+value, treat the bloom as a top highlight layer that can drop out. Verify the mark still names itself as a flat tinted glyph on a light ground.

### 5. Character Mascot (personality-led)
**Essence:** a personified creature or face carries the brand; warmth over utility.
**Exemplars:** keeby, mole, tono, pokey, zush, bartender-6, glance, slapmac.
**Palette recipe:** friendly 2-hue — a warm body hue + a darker feature accent; or monochrome body + single warm focal (klack's ivory-on-black). Keep the eye/catchlight the brightest value.
**Composition:** background = soft field or transparent → glyph = the mascot with eyes/face as focal, readable silhouette, one catchlight → overlay = none. **Era:** Big Sur clay or skeuomorphic-quote; **light:** soft top-left studio, short AO pool.
**When to choose:** consumer/playful app where personality sells harder than function; the mascot need not state the verb.
**Do:** give it a catchlight and a silhouette that survives filled-black. **Don't:** let charm cost 16px legibility (a molded monogram like klack's "K" smears — recovers only by 32px).
**#10:** layer body / features / catchlight; ensure the face reads as shape+value under tint. A photoreal near-black render (klack) hard-fails #10 and #1 — if you need system-safety, pair it with a proper masked squircle variant.

### 6. Device Portrait (the Mac hardware IS the subject)
**Essence:** the notch, screen, or bezel quoted literally — reads instantly for menu-bar utilities.
**Exemplars:** alcove, dynamiclake, healthynotch, folder-hub, corner-time, tellie, droppy, codeshot.
**Palette recipe:** dark bezel `#0F1012` + a bottom-up screen glow (single hue) as the only chroma; or a cool device-silver. Screen content is the accent, bezel is neutral.
**Composition:** background = the squircle IS the display, or a device sits front-facing → glyph = notch cutout / screen-in-bezel with a bottom-up screen glow → overlay = optional badge. **Era:** Big Sur / Liquid Glass; **light:** screen-emissive from below + soft top rim.
**When to choose:** the app acts on the Mac's hardware (notch, menu bar, display, dock).
**Do:** quote the notch/screen literally. **Don't:** over-detail the bezel — it vanishes small (alcove fails #3 and #10 by leaning on the gradient field, not a shape).
**#10:** the device outline is your carrying shape — keep it a real filled silhouette layer; let the screen glow be a droppable highlight, not the identity.

### 7. Diagonal Tool (Big-Sur cleaner/maintenance)
**Essence:** a maintenance tool crosses the plane at an angle — Apple's TextEdit/Preview grammar.
**Exemplars:** cleanmymac (chrome arm), uninstally (broom), deskminder (needle), sweeper, macusb, dropadoo (paperclip).
**Palette recipe:** one saturated field + a chrome/metal tool ramp `#EDEBF4→#DAD5EE→#C1BED9` that picks up the field's cast + optional sparkle-trail whites.
**Composition:** background = saturated hue field → glyph = single white/object glyph → overlay = a tool laid corner-to-corner (top-left→lower-right), the verb of the app. **Era:** Big Sur; **light:** top/top-left soft, bright tool top-edges.
**When to choose:** ONLY when the verb is literally "act on / clean / fix files." 
**Do:** use the tool as the verb. **Don't:** default to this — it is the most template-worn move in the corpus; thin tool arms smear at 16px and the maintenance metaphor is silhouette-fragile (cleanmymac loses the verb at Dock size).
**#10:** layer field / object / tool / sparkle; the tool must read as shape under tint, not as a specular highlight that disappears.

### 8. Instrument Emblem (data-viz / ring-chart)
**Essence:** the app's own chart or gauge becomes the mark — concentric geometry, category colour.
**Exemplars:** code-meter (gauge), sessionwatcher (bars), spacepeek (donut-as-lens), subscription-day (radar), radial (spinner), pieoneer (pie).
**Palette recipe:** neutral ground + a bounded 1–2 hue encoding. Resist a full legend of hues (smears at 16px, fails #6/#7).
**Composition:** background = flat or subtle ground → glyph = the exact in-product artifact (ring/gauge/bars) at icon scale, concentric → overlay = none. **Era:** Big Sur or flat; **light:** flat or soft top-down.
**When to choose:** monitoring/analytics/disk/time apps where the product's own visualization is iconic.
**Do:** quote the exact object the user will use; double-read it (spacepeek's donut = disk-usage = magnifier lens). **Don't:** carry >2 chart hues; don't let fine tick detail define the read.
**#10:** the ring/gauge silhouette is the carrier — keep it a filled-shape layer; encode data by value/position, not by hue alone, so a tint preserves it.

---

## Picker — app subject/personality → candidate directions

| App is… | Primary | Alt |
|---|---|---|
| Act-on-files / cleaner / installer | 7 Diagonal Tool | 1 Object Tile |
| Strong existing brand mark | 3 Monochrome Logomark | 2 Tahoe Gel-Glass (re-materialise it) |
| AI / agent / dev current-era hero | 2 Tahoe Gel-Glass | 4 Dark-Field Emissive |
| Menu-bar / notch / display utility | 6 Device Portrait | 4 Dark-Field Emissive |
| Monitoring / analytics / disk / time | 8 Instrument Emblem | 4 Dark-Field Emissive |
| Consumer with a physical noun | 1 Object Tile | 5 Character Mascot |
| Personality-led / playful | 5 Character Mascot | 1 Object Tile |
| Premium / nocturnal / pro utility | 4 Dark-Field Emissive | 3 Monochrome Logomark |
| Pro / silver / menu-bar-native (palette overlay) | any + Monochrome-metal ramp `#E8EAEE→#A6B1C2→#565B65` | — |

---

## The 12-point rubric — delivery bar ≥10/12, checks 1–4 non-negotiable

1. **Mask discipline** — designed for the squircle; no baked corners/shadow. *(non-negotiable)*
2. **Grid adherence** — optically centred, safe-zone margins; wide glyph→inner square, round→larger circle. *(non-negotiable)*
3. **Silhouette test** — nameable filled solid black. *(non-negotiable — 26 icons fail here)*
4. **16px squint** — survives menu-bar/Spotlight; no detail smear. *(non-negotiable)*
5. Single light model — one source/direction (or deliberately none).
6. Palette economy — ≤2 hue families + ramps; accent reserved for focal.
7. Figure-ground — glyph vs ground ≥3:1; survives grayscale.
8. Depth coherence — planes ordered, shadows match light, no z-fight.
9. Era coherence — one era's language (or a knowing quotation).
10. **Variant robustness** — survives Default/Dark/Clear/Tinted; identity not hostage to one bg colour. *(76% fail — the highest-leverage fix)*
11. Personality — ≥1 nameable device beyond glyph-on-gradient.
12. No-text — no words/screenshots/photos (diegetic monogram OK).

Bar: **≥10/12 with zero failures on 1–4.** Report the score and every #10 liability honestly. `scripts/audit_sheet.py check` now verifies mechanically that a score and this bar appear on the sheet, so an unscored sheet fails the gate instead of passing quietly.

---

## Device bank — 15 subject-mining glyph strategies (strategy, not app-copy)

Draw the app's literal noun/verb before reaching for a stock category glyph. Generalised moves from the corpus:

1. **Numeral/letter-as-object** — the brand initial IS the functional shape (1password: "1" = keyhole slot).
2. **Gesture-as-glyph** — draw the interaction, not the file (unfold: the spacebar key as a debossed ⊔ well).
3. **Result-as-physical-object** — the output lifted as a tangible thing (cleanshot: screenshot peeled off the desktop).
4. **One anatomical detail that means the verb** — a single body part carries "digs/grabs/points" (mole: the digging claw).
5. **Dual-function primitive** — one shape reads as two product concepts (sero: ring = O = zero = lens/portal).
6. **Waterline / fill-level as data** — a boundary doubles as a selected row or level (finbar: fin + waterline = list-row).
7. **Punctuation-as-identity** — the name's typographic mark IS the function (caesura: // = pause).
8. **Prompt-as-face** — CLI glyphs re-read as an emoticon (maestri: `>` eye + `|` cursor eye = winking agent).
9. **Junction/fork where cap-shape carries meaning** — arrowhead vs foot encodes redirect vs stay (mux).
10. **Micro-keypad spelling the feature set** — a 2×2 of domain glyphs (soulver: `$ % clock =`).
11. **Glyph knocked out of a material object** — CLI/prompt inlaid into a glass cloud (codex: cloud-compute + terminal).
12. **Colour/shape mismatch as the name** — the pun lives in one wrong attribute (waterlemon: melon shape, lemon colour).
13. **Descending elements resolving into a direction** — motion implied by a sequence (open-screen-shot: dots → down-arrow = scrolling capture).
14. **Container overflowing with what it manages** — the vessel plus its contents (sweeper: Trash overflowing with discarded apps).
15. **Diegetic molded monogram** — the initial molded INTO a rendered object, catching its light (klack: "K" in the keycap), never typeset over it.

Extended bank (for variety across sessions): **the app's in-product artifact at icon scale** (gauge, treemap, radar); **hardware quotation** (notch, screen, bezel as the subject); **the appliance being serviced** (draw the Mac, not "clean"); **negative-space creature** (hoolo: owl from cuts, "oo" = eyes); **material unrolling to reveal** (walltune: wallpaper peeling); **everyday prop standing in for the verb** (shake-it-on: cursor as maracas); **architectural noun** (viaduct: arch, minarah: minaret); **coin/token doubling as currency AND name** (tokens-4-breakfast).

New from the 532-icon corpus (2026-08):

16. **The icon performs the verb** — the composition physically enacts the app's function (CleanShot X: the page-curl IS the capture; PDF Squeezer: a machine squeezing the format; unfolder: 3D shapes in, papercraft nets out; CleanMyMac: the wiped-glass streak performs "clean").
17. **Tile-as-machine with a diegetic aperture** — the squircle is the device, with a real slot/opening cut into it that the content emerges from (the photo-strip printer capture; The Unarchiver's drawer).
18. **Edge-bleed physicality** — an element deliberately cut by the mask so the tile reads as a physical object (Contacts' rainbow index tabs bleeding off the right edge).
19. **Re-materialised brand mark** — keep a flat logo's silhouette exactly, re-pour it in gel/frost (News, Slack, the iWork set; the upgrade path for any existing flat mark).
20. **Data-as-glyph abstraction** — the content reduced to its minimal data pattern with one accent datum (Calendar's dot-matrix month with a single red "today" dot; TablePlus's facet-planes).
21. **Overlap-as-identity** — two translucent primitives whose blend zone IS the mark (Shortcuts' diamonds, Photos' petals, Game Center's bubbles, mindnode).
22. **Emissive interior under glass** — a glowing core inside a translucent shell as the second light source (Siri orb, Tips bulb, Home's nested glow, elytra's amber core, dropzone-5).
23. **Fold/self-shadow ribbon** — a flat mark given 3D presence by one fold with a darker inner face (Infuse's play-ribbon).
24. **UI-primitive-as-mark** — own one interface primitive outright (iA Writer's caret; Reminders' list-rows; copilot's arrow).
25. **X-ray technical drawing** — monochrome line-art with translucent internals, engineering-diagram register (flighty's airliner).
26. **Material pun** — the name/function told entirely in material physics (Couverture's chocolate drip viscosity; pasta's glossy pasta "P"; PixelGriddle's waffle-iron grid; betterzip's bound bundle).

---

## Anti-sameness rules (vary across a session)

When generating multiple icons in one session, actively diversify — the corpus's failure mode is templated sameness:

- **Vary the direction.** Don't ship three Object Tiles or three violet-glass AI blobs. Rotate families across the picker.
- **Vary the palette family.** Blue + indigo/violet dominate the corpus (271 of recorded chromatic hits) — deliberately reach for the under-used ramps: warm accent (amber/coral), acid-green (`#C6F04C`), monochrome-metal, ink-on-paper. Don't let every icon land on electric blue.
- **Vary the glyph type.** Alternate object / mascot / monogram / abstract-emblem / device-portrait — not all literal-object, not all letterform.
- **Vary the ground.** Mix saturated-field, near-white-float, and near-black-emissive so a set doesn't read as one gradient family.
- **Vary the era knowingly.** Prefer Liquid-Glass layer discipline for current-era heroes, but a deliberate Big-Sur or skeuomorphic quote is legitimate when the personality demands it — just commit, don't drift.
- **Never repeat the diagonal-tool default** across a session — it is the single most worn move; use it once, for the one app whose verb is literally "act on files."

---

## Failure-mode anti-checklist (from 500 gallery icons — audit against before delivery)

The ten recurring ways shipping icons fail (full evidence: `corpus/SYNTHESIS.md`):

1. Template genericism — saturated gradient + stock gel glyph/checkmark/magnifier/wrench, nothing ownable.
2. White-on-hue with no translucency cues — the flat Big Sur re-tread masquerading as Tahoe.
3. Tone-on-tone silhouette collapse — glyph hue too close to ground; dies in grayscale.
4. Baked text, wordmarks, screenshots, data tables — dead at Dock sizes (only sub-legible diegetic engraving is sanctioned).
5. Metaphor pile-ups — 3+ props/ideas per tile that never resolve into one object.
6. Legacy-era drag — hard gloss sweeps, lens flares, Aqua glass, metal bevel frames, page curls, freeform overhangs.
7. Photo texture / game key-art that bakes to mud at 32px, with zero macOS grammar.
8. Apple-template mimicry (blueprint dev costume, iWork look) or sibling-SKU non-differentiation with nothing owned.
9. Unearned rainbow — multi-hue without data/colour-domain semantics; when earned, quarantine it inside one shape.
10. Flat pre-masked raster delivery — identity as a colour relationship that dies under Dark/Clear/Tinted.

**Where a gate could take over, and where it can't.** Three of these are mechanical and nothing currently checks them: #4 is a `<text>`/`<tspan>` scan of the SVG master, #3 is a grayscale figure-ground ratio on the render, and the blue/indigo template default flagged at the top of this file is a hue histogram over the ground pixels. The rest — genericism (#1), metaphor pile-ups (#5), template mimicry (#8), whether a rainbow is earned (#9) — are judgments about whether the composition *means* anything, and need an eye or a panel. Those three are the cheap wins for anyone extending the gates; scoring the others mechanically would be scoring the wrong thing.

---

## Generation pipeline — three engines, multiple variations (never ship a single take)

An icon commission produces a **variation set**, not one artifact. One shared design spec, rendered through three different engines whose strengths differ — then a judged contact sheet. The spec comes first so variations are takes on one committed idea, not three random ideas.

**Step 0 — the shared spec.** Direction (from this catalogue), subject-mined glyph device, silhouette description, ground register, palette hexes, light model, and the #10 layer plan (background / mid / foreground / highlight). Optionally add 1–2 spec-level alternates in a *different* direction when the user wants genuine options — that multiplies the set, it never replaces the per-engine takes.

**Engine A — hand-authored layered SVG (this model; always produce this one).**
Write the SVG yourself, 1024×1024, one `<g>` per layer named `bg` / `mid` / `fg` / `highlight` so it maps 1:1 onto Icon Composer layers.
- *Strengths:* exact geometry and optical centring, true layer separation (#10 robustness by construction), deterministic palette hexes, editable forever. This is the **canonical master** — whatever wins the look, the shipped deliverable is this file matched to it.
- *Tahoe material simulation in SVG:* cushion tile = radial gradient + a 1–2% inner white stroke ring; frosted glyph = white fill at 78–92% opacity over the ground with a soft `feGaussianBlur` inner bloom; overlap blends = literal overlapping semi-opaque shapes (let the renderer do the multiply); rim light = short arc strokes with linear gradients; contact shadow = blurred ellipse at 10–18% black. Keep filters simple — renderers vary.

**Engine B — media-gen-pro vector (`svg: true`, Arrow).**
A real, editable SVG generated from a text brief — an independent vector take you didn't draft.
- *Brief it with:* the spec verbatim — direction essence, glyph device, palette hexes, ground register — plus: "1024×1024 app-icon artwork, full-bleed square, squircle-safe margins, no baked corner radius, no baked drop shadow, layered shapes".
- *Strengths:* organic curves and shape ideas outside your drafting habits; still vector, so salvageable parts can be merged into the Engine A master.

**Engine C — media-gen-pro raster (default model = GPT Image; the material-realism engine).**
One or two raster takes for the gel/frost/glass rendering no vector engine matches.
- *Steer it with reference images:* pass `referenceImages` — 2–4 corpus exemplars from `references/corpus/apple-2026/` in the **same ground register** as the spec (e.g. porcelain register → `apple-2026/apple-23.png` Safari + `apple-28.png` Photos; saturated-tile register → `apple-01.png` Mail + `apple-14.png` App Store; dark register → the sticker/butterfly captures). This is how the Tahoe material language actually transfers.
- *Prompt in prose* (media-gen-pro craft rules): subject first, then material ("soft-extruded translucent gel, frosted white glyph with the ground's hue bleeding through, one soft top light, rim highlights, soft contact shadow, no hard speculars"), composition ("single focal object, ~60% of tile, optically centred"), and "flat square full-bleed artwork, no rounded-corner mask, no baked drop shadow, no text".
- *Caveats:* billed per image; the output is a **flat raster** — it is the hero preview and material target, never the shipped master (it re-creates failure mode #10 if shipped as-is). If a raster take wins the look, rebuild its material language into the Engine A layered SVG.

**Step 4 — contact sheet + judgment, delivered as `audit.html`.** Render every take with `python3 scripts/audit_sheet.py render <dir>`: a 1024 hero plus 2x retina sources at **256 / 128 / 96 / 64 / 32**, displayed at **128 / 64 / 48 / 32 / 16 css px** — 1x renders read blurred on retina screens, and the 16px cell is paired with a pixelated ×6 magnification of the same render. **The 48px row is not optional:** a Finder list row and a plugin-marketplace tile both render there, and an icon that survives 128 and 16 can still collapse in between. Write a self-contained **`audit.html`** into the assets/deliverables directory (start from `assets/icon-audit-template.html`): one row per take showing its renders beside its 12-point rubric score and a one-line verdict, losing takes included with the reason they lost, and a recommendation block naming the shipping take and its known liabilities. The same script's `check` subcommand gates the finished sheet — it is the mechanical half of this step, and it reads the sheet, so a sheet that was never written cannot pass it. Audit silhouette and small-size legibility on the actual renders, not imagination. Presenting scores in chat without writing the artifact does not satisfy this step — the sheet is what the user reviews later and what the next iteration diffs against. Then deliver the layered SVG master (+ the raster hero and the Arrow take as alternates). Minimum set: 3 takes (A + B + C); typical: 4–6 across two spec alternates. Under a constrained run, shrink per-engine iteration counts before ever dropping an engine or the sheet; missing engines or a missing `audit.html` make the commission incomplete unless the user explicitly waived them.
