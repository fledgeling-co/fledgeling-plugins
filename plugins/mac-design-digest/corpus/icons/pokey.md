# Icon: Pokey

- **Era:** custom (iOS-illustrative sticker mascot; borrows the Big-Sur "single object on an orange sky-ramp") · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply — `icon.png`, **400×400** web/iOS render (SHA-1 `36418482`). Category: Communication. App: Pokey — "Turn your cursor into the most memorable thing on the call" (a screen-share cursor enhancer; website pokeyapp.com).
- **Resolution caveat:** only a 400px render, not the 1024 master. The glove's bevel/emboss shading and the soft baked drop-shadow are present but coarse — edge treatment is `(estimated)`, not `(measured)`. This is a **pre-masked iOS-style asset**: the rounded-rect corners are baked into the PNG (transparent outside), not a full-bleed square left for the system to mask.

| Dimension | Reading |
|---|---|
| Background | Orange **ramp** ~**#FF9A4C (top) → #FA7324 (bottom)** — light-warm-orange at top darkening toward the base (Big-Sur "sky logic"), with a faint lighter radial lift behind the hand (~#FF913F). Fills the full 400px canvas edge-to-edge inside a baked ~115px corner radius (~29% — an iOS superellipse, not the macOS squircle inset) |
| Glyph | **Mascot** — a white four-fingered cartoon glove (the classic Mickey-Mouse / pointer-cursor hand), index finger raised up-left, emerging from a striped black wrist-cuff and a black sleeve. White fill ~#FFFFFF highlight → grey ~#D7D7D7 lower shade, wrapped in a heavy uniform black keyline. Positioned diagonally, anchored to the bottom-right corner; not optically centred |
| Overlay device | **None** — the hand *is* the subject; no tool crosses a base glyph. The diagonal is the gesture itself, not an overlaid instrument |
| Light model | Soft top / top-left key: glove carries an embossed bevel (top-left highlight → bottom-right grey), a short baked drop-shadow falls down-right, and the bg ramp lightens toward the top — roughly one consistent source. The **baked** shadow/bevel (rather than system-supplied) is the skeuomorphic/iOS tell |
| Layer stack | (baked rounded-rect + transparent corners) → orange gradient field → soft baked drop-shadow → white beveled glove w/ heavy black keyline → striped black wrist-cuff → black sleeve/forearm exiting bottom-right |
| Palette economy | **One** hue family (orange ramp) + neutral glyph (white→grey→black). No separate saturated accent — the orange field is the only chroma; the glyph is achromatic. Passes ≤2-hue economy easily |

## Signature devices
- **The pointer-cursor made flesh.** The white four-fingered glove is the literal old-school "pointing hand" cursor rendered as a cartoon hand — honest subject-mining: the app *is* a cursor enhancer, and the icon shows you the cursor. The metaphor equals the product (cf. Alcove's framed-recess).
- **Heavy comic keyline.** A thick uniform black outline around the whole glyph — a sticker/cartoon register, not a macOS-native material. It is what carries the figure at every size (the white fill alone would dissolve into the orange without it).
- **Diagonal reach from the corner.** The sleeve is anchored to the bottom-right edge and the arm rises across the canvas to a fingertip near centre — a dynamic, kinetic composition rather than a centred front-facing object. Committed direction (motion, "poking"), not template-default.
- **Striped cuff detail.** The ribbed black wrist-band is the one piece of fine detail; it's the first thing to smear at 16px.

## Failures
- **#1 Mask discipline — FAIL.** The corner radius (~115px on 400 ≈ 29%) is **baked into the artwork** with transparent corners, plus a **baked soft drop-shadow and bevel** on the glove. macOS 26 wants a full-bleed unmasked square with no baked corner/shadow/bevel/gloss (the system supplies all of those). This is an iOS/web app-icon ported straight across — a non-negotiable check (#1–#4) and it misses.
- **#10 Variant robustness — FAIL.** Single baked PNG, not layered Icon Composer authoring. Identity leans on the orange field; in mono/tinted/clear renders the orange (the only chroma) drops away and a white-glove-on-neutral would have to hold alone — no evidence it was designed for dark/tinted/mono. Not authored as light/dark/mono layers.

## Soft passes (flagged for synthesis)
- **#2 Grid adherence.** Deliberately off-centre — the hand mass reads fine and the diagonal is intentional, but the sleeve bleeds to the bottom-right edge/corner and the subject sits off the optical circle. Reads as a signature move, not a mistake, so a pass — flagged because it isn't grid-centred.
- **#3 Silhouette test.** Filled solid black, the outer contour is a lumpy hand-on-a-stalk — nameable as "a hand," but the *pointing* gesture and the glove-vs-cuff separation are defined by the white fill + internal keyline, both of which a pure-black silhouette discards. Nameable but identity-thin in silhouette.
- **#4 16px squint.** Survives as a white blob + dark stalk on orange (contrast holds), but the specific pointing gesture and the ribbed cuff smear; you read "white shape on orange," not "pointer hand." Legible, low-differentiation.
- **#9 Era coherence.** Consistent as a *custom* concept, but hybrid: a clean modern gradient field under a heavily-outlined, bevel-embossed cartoon glove — a flat-field convention married to a skeuo-illustrative glyph, belonging to no single macOS system era.

## Rubric ledger
| # | Check | Result |
|---|---|---|
| 1 | Mask discipline | **FAIL** (baked corner + baked shadow/bevel; iOS-ported) |
| 2 | Grid adherence | soft pass (intentional off-centre; sleeve bleeds to corner) |
| 3 | Silhouette | soft pass (nameable hand, thin gesture in solid black) |
| 4 | 16px squint | soft pass (blob survives, gesture/cuff smear) |
| 5 | Single light model | pass (consistent top/top-left key) |
| 6 | Palette economy | pass (one orange hue + neutral glyph) |
| 7 | Figure-ground contrast | pass (white+black keyline on orange, very high, survives grayscale) |
| 8 | Depth coherence | pass (bg → shadow → glove → cuff → sleeve, ordered) |
| 9 | Era coherence | soft pass (custom hybrid: flat field + skeuo glyph) |
| 10 | Variant robustness | **FAIL** (single baked PNG, orange-dependent identity) |
| 11 | Personality | pass (the cursor-glove is a strong, product-true device) |
| 12 | No-text | pass |

**Total: 10/12, 2 failures (#1, #10).** Both soft-pass-heavy on the four Dock-critical checks (#1 fails outright, #2–#4 are soft) — the icon is charming at hero size but engineered as an iOS sticker, not a macOS-native mark.

## Rhymes with (hint only — for icon-cluster synthesis)
- **Cartoon-mascot / sticker icons with a heavy black keyline on a single-hue gradient** — the Duolingo-adjacent illustrative register, hand/emoji-glyph app icons. Executed in an iOS-illustrative style rather than macOS-native.
- The Big-Sur **"single centred object on a warm sky-ramp"** family (light-top → dark-bottom orange), but here the object is off-centre and diagonal. Style-family guess: **"kinetic cartoon-glyph on orange ramp."** Palette-family rhyme: single-hue **orange** ramps (#FF9A4C→#FA7324).

## Brand-context note (cover coherence)
Cover uses the **same** orange ramp (deeper: ~#F26A1F→#FF8A3C) and the identical white-glove-black-outline hand, now mid-"poke" with hand-drawn black action-lines radiating from the fingertip (the "click"). Palette coherence between icon and cover is tight — one orange, one glove, one black — so the brand is disciplined and recognisable. The cover's kinetic burst-lines make explicit the *poke/click* energy that the icon compresses into a static diagonal. This is a coherent single-palette brand; its weakness is platform fit (iOS-style mark on a Mac shelf), not identity.
