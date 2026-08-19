# Icon: Codex

- **Era:** Liquid Glass (transitional — glass idiom with baked specular; see caveat) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (OpenAI Codex, Dev). Icon render is 204×204 webp — a resized web asset, **not** the 1024 master. All px/positional reads are `(estimated)` at low res; hex sampled from the 204px render.

| Dimension | Reading |
|---|---|
| Background | Flat near-white field, faint cool-lilac cast — `#FEFEFE` (top) → `#F1F1F1` (bottom), mid `#EDF0FA`. A whisper of a glass rim highlight around the squircle. |
| Glyph | Compound: a scalloped **glass cloud** (object) carrying an inlaid terminal prompt `>_`. Cloud gradient runs lavender-pink crown → periwinkle → electric indigo base: `#C3AFFE` → `#A091FF` → `#769CFF` → `#5D7CFE` → `#3333FF`. The `>_` is light/white ink (knockout), reading `#D9E2FF`→white, rounded stroke terminals. Optically centred, sitting slightly high; occupies ~central 65% of the canvas (good safe-zone margins). |
| Overlay device | Other — a mono glyph *inlaid/knocked out of* the cloud object (not a diagonal tool, badge, or frame). |
| Light model | Single top-down / front environmental-glass source: pink-lavender specular bloom at the cloud's crown, gradient darkening to electric indigo at the base, one soft short micro-shadow under the cloud on the white field. Coherent. |
| Layer stack | (back→front) 1. near-white squircle field w/ faint glass rim → 2. soft cloud micro-shadow → 3. translucent violet→blue glass cloud (scalloped) with baked internal gradient + crown specular → 4. white/light `>_` terminal glyph on the cloud. |
| Palette economy | One extended violet→blue ramp (adjacent hues, indigo family) + white field + white glyph knockout. Zero competing accents; saturation reserved entirely for the cloud (the focal object). Clean. |

## Signature devices
- **[GOLDEN-NUGGET] Terminal prompt knocked out of a glass cloud** — the whole concept in one move: cloud (cloud-compute / autonomous agent) fused with `>_` (CLI/terminal). Communicates "a coding agent that runs in the cloud" without text. This is committed direction, not template glyph-on-gradient.
- **Crown specular as a pink-lavender bloom** — the light source reads as a warm pink highlight sitting on a cool blue-violet glass body; the hue-shift (pink light, blue mass) is what sells the glass material.
- **White-field ground, not a saturated background** — inverts the usual saturated-bg + light-glyph convention: the glass object floats on near-white. Distinctive in a Dock full of filled-gradient squircles; also the source of the variant fragility below.
- **Rounded stroke terminals on the `>_`** — soft, friendly CLI rather than a hard monospace prompt; matches the pillowy cloud.

## Failures
- **#4 16px squint (soft-fail).** The thin, light `>_` strokes sit on a mid-value gradient cloud and smear to illegible at menu-bar/Spotlight size — at 16px the icon survives only as a distinctive *blue blob in white*, and its entire terminal concept drops out. Structural (thin stroke + light-on-gradient + glyph small within cloud), not merely a render artifact — though the double-downscaled 204px source lowers confidence; the true 1024 master would fare somewhat better.

### Soft passes (counted as passes, flagged)
- **#3 Silhouette.** Filled solid black it reads as a lumpy round blob — nameable as "a cloud," but the *all-around* scallop (clouds are flat-bottomed) invites a competing "flower/burst/thought-bubble" read. The `>_`, being a knockout, vanishes in pure silhouette, so subject identity rides entirely on the glyph at any size where the glyph is legible — and on color/shape where it isn't.
- **#10 Variant robustness.** The composition is built on the white ground: a white-ink glyph over a translucent cloud over a near-white field. Dark/clear/tinted renders are unverified from this single static webp, and the white-knockout glyph is the fragile element (nothing anchors it if the ground inverts). Concern, not a confirmed failure.
- **#2 Grid adherence.** Optical centring and safe-zone margins look right, but the true Apple grid can't be overlaid on a 204px render — `(estimated)`.

## Rhymes with
- Current-wave **AI/agent app icons** using violet→blue gradient glass blobs on light grounds (the LLM-era lavender-to-electric-blue ramp).
- **Big-Sur/Liquid-Glass dev-tool icons that inlay a mono glyph into a glass object** (the "tool/glyph on a front-plane object" tradition, here a cloud instead of a tilted card).
- **Cloud-motif + CLI-glyph** terminal/agent icons — style family: *glass-object-on-light-ground, indigo AI gradient*. (Hint for synthesis — confirm against ≥3 independent icons before any canon.)
