# Icon: FolderVitrine

- **Era:** Liquid Glass (clear/frosted variant, macOS 26 Tahoe+) · **Rubric:** 10/12 (2 soft passes, 2 failures) · **Digested:** 2026-07-19
- **Source:** macapp.supply / user · **Subject:** Utility — "Beautiful folder Quick Look for Mac" (a glass panel that previews a folder's media contents)
- **Resolution caveat:** the source is a **1200×630 JPEG web render** (App-Store-OG style), the icon centred at ~360×360px effective on a `#F8F8F8` plate — **not** a native 1024 export. Edge specular, refraction and micro-shadows are JPEG-softened; every hex below is `(estimated)` off a compressed render, not a clean PNG. The 16px/32px squint tests were run on the upsampled 360px crop — but the failure they surface is **structural** (pale-on-pale), so it holds at any source resolution.

| Dimension | Reading |
|---|---|
| Background | Frosted-white squircle, faint cool tint: `#FEFEFE` (top) → `#EFF6FF` (lower body) `(estimated)`. Not a saturated field — this is a **clear-glass base**, near-white, with a crisp `#FFFFFF` specular on the upper-right rim |
| Glyph | **Translucent blue-glass folder** (back body + front flap), own top-down ramp `#E6F4FF` (flap top) → `#D0EBFC` (mid) → `#82D3FF` (deepest pool at base) `(estimated)`. Optically centred horizontally; mass sits low, baseline crowds the lower third, photo card lifts weight back up |
| Overlay device | **Protruding content card** — a translucent white photo/media card (`#F6F9FE`) sandwiched between the folder's back and front planes, bearing the classic image-placeholder glyph: a warm sun dot + two blue mountain triangles (`#AAE1FF`). Not a diagonal tool / badge / frame — a "folder revealing its contents" motif |
| Light model | Soft top-down / environmental glass. Base glows uniformly frosted; folder ramps light-top → blue-pool-base; single white specular on upper-right squircle edge; internal shadows very short/soft (the drop shadow in the render is macapp.supply's, not the icon's) |
| Layer stack | 1) frosted-white squircle base (translucent, faint inner glow) → 2) folder back panel (pale blue glass) → 3) photo/media card (white glass + sun/mountain glyph) → 4) folder front flap (pale→sky-blue glass, half-covering the card) |
| Palette economy | One hue family (blue) + neutral frost base + **one** warm jewel (the sun, `~#FFDFAE`). ≤2 hues, accent reserved for the single focal detail. Exemplary economy |

## Signature devices
- **Glass vitrine** `[GOLDEN-NUGGET]` — the frosted squircle reads as a display case housing a translucent folder; the name (*vitrine* = display cabinet) is rendered literally as a glass box you look *into*. Strong subject-mining for a folder-preview utility.
- **Folder-that-previews-its-media** `[GOLDEN-NUGGET]` — the photo card poking out is the app's actual function (Quick Look of a folder's images) compressed into one shape. The icon communicates the subject, not just "a folder".
- **Single warm jewel in an all-cool frost** — the orange sun is the only saturated point in an otherwise monochrome-blue-on-white composition; it is jewelry, not a CTA. It's also the only element that survives the 16px squint (see Failures) — accidentally the icon's one legibility anchor.
- **Double-plane folder with sandwiched card** — back body + front flap rendered as two stacked glass planes with the content card correctly z-ordered between them. Clean glass depth, no z-fighting.

## Failures
- **#4 16px squint — FAIL (non-negotiable).** At 16px the whole icon collapses to a **featureless pale-blue frosted square** — folder, card, sun and mountains all smear into one blob with a faint blue pool at the base. At 32px a faint mountain hint + the tiny orange sun dot survive, but the folder shape is still not readable. Fails Dock-small / Spotlight / menu-bar duty.
- **#7 Figure-ground contrast — FAIL.** Folder (`#D0EBFC`) against base (`#FEFEFE`) is far under the 3:1 floor; the deepest folder blue only reaches `#82D3FF`. In grayscale the folder nearly vanishes into the base. This is the **root cause** of the #4 failure — the icon is defined by translucency and faint edges, never by contrast.

**Soft passes** (scored as pass, flagged for synthesis):
- **#2 Grid** — folder mass is base-heavy and sits below the geometric centre; the protruding card rebalances it upward so the composite *reads* centred, but it isn't geometrically centred.
- **#10 Variant robustness** — the composition leans entirely on the near-white light backdrop for its faint edges. Because the folder is defined by translucency + low-saturation blue rather than a solid colour, dark/clear/tinted renders risk flattening the folder further into the base. No layered source to verify; a tinted-mode contrast collapse can't be ruled out. Honest concern, not a clean pass.

Clean passes: **#1** mask (proper full-bleed squircle, no corner fighting) · **#3** silhouette (folder-with-protruding-card is nameable *at full size* — the shape is conventional even though contrast doesn't carry it) · **#5** single light model · **#6** palette economy · **#8** depth coherence · **#9** era coherence (consistent Liquid-Glass clear-frost language) · **#11** personality (the vitrine + media-card motif is well beyond glyph-on-gradient) · **#12** no-text (the photo card is an illustrated placeholder, not a real photo or UI screenshot).

## Rhymes with
- **Clear-glass Liquid-Glass icons** taken to full translucency — near-monochrome frost + a single warm jewel. Folder-utility icons in the Big-Sur folder-object lineage (Finder/Preview-adjacent) but rendered as frosted glass rather than opaque plastic. (Hint only — no ≥3-icon cluster asserted; synthesis owns clustering.)

## Cross-icon / brand notes
- **Palette coherence with cover:** the cover shows a frosted-blue glass panel on a blue wallpaper with an **orange→blue progress bar** as its one warm accent. The icon mirrors this exactly — blue glass + one orange jewel (the sun). Brand = frosted-blue glass with a single warm accent; icon and product read as one system. Strong coherence.
- **The cautionary lesson:** this is a *beautiful-at-1024, illegible-at-16* icon. The clear-glass aesthetic that makes the cover panel elegant becomes a contrast failure when the same pale-on-pale treatment is asked to survive Dock and menu-bar duty. Committing to full frost cost the icon checks #4 and #7 — the two the system will actually enforce.
