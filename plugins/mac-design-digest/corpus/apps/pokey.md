# Pokey — profile

- **Source:** macapp.supply (cover + icon only; no UI screenshots supplied) · **Surfaces digested:** none — marketing cover + app icon only · **Last updated:** 2026-07-19
- **One-sentence identity:** A 1930s rubber-hose cartoon glove (Cuphead / classic-Mickey lineage) recast as your macOS pointer — a loud, single-hue orange consumer brand built to make the cursor "the most memorable thing on the call," of which no actual app UI has yet been seen.
- **Cluster:** unassigned — brand/icon evidence only; not a member of any macOS-native UI cluster (no native surface observed).
- **Lineage:** unknown (low) — **no app UI surface was supplied**, so framework lineage cannot be classified. Do not infer native/Catalyst/Electron from a brand illustration. Brand evidence never feeds macOS canon regardless.
- **Era (chrome):** unknown — no window chrome present in either image. (Icon rendering reads legacy-glossy, see Signature moves, but that is icon-era, not chrome-era, evidence.)

## What was actually supplied (honesty note — read first)

Two files, **neither of which is a macOS UI screenshot**:

1. `cover.jpg` (1024×630) — a **marketing/brand illustration**: a vertical orange gradient backdrop with a white-gloved, four-fingered cartoon hand (index finger raised) surrounded by comic-book "impact" speed-lines radiating from the fingertip. No device frame, no window, no traffic lights, no controls, no text. This is 100% brand evidence; there is no design-system evidence to extract and none of the 14-point UI rubric or 10-point native-tells audit is applicable to it. Grading a brand illustration on grid-adherence / input-height / focus-appearance would be a category error and is deliberately **not** done.
2. `icon.png` (400×400) — the **app icon** (icon evidence, formally Workflow B; recorded here only at brand level because this pass is Workflow A). A proper 12-point icon digest is warranted as a follow-up.

**The corpus therefore learns Pokey's brand, not Pokey's UI.** What kind of app it is (the tagline and Communication category strongly imply a cursor-highlight / presentation-overlay utility, most likely a menu-bar extra) is **inference, not evidence** — its real surfaces (menu-bar popover, settings, the cursor overlay itself) remain entirely unseen.

## Tokens

All values below are **brand tokens**, not UI/design-system tokens. They describe the marketing mark and the icon; none describe a shipping interface.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/orange-gradient-top | #FA872E → #F56D15 | (measured)(inferred) | cover backdrop, upper region; warm mid-orange |
| brand/orange-gradient-bottom | ~#EB5A0D (#EB590C–#EB5C0E) | (measured)(inferred) | cover backdrop, lower region; deeper, redder |
| brand/orange-icon-top | #FF9A4C | (measured)(inferred) | icon tile, top; lighter/brighter than cover |
| brand/orange-icon-bottom | #FA7324 | (measured)(inferred) | icon tile, bottom |
| brand/orange-vs-system | system Orange family (kit Light #FF8D28 / Dark #FF9230) | (measured)(inferred) | brand orange lives in the same hue family but is rendered as a warm top→bottom gradient and pushed deeper at the base — not the flat system swatch |
| brand/glove-fill | #FFFFFF | (measured)(inferred) | cartoon glove, both assets |
| brand/keyline | #000000 heavy | (measured)(inferred) | thick black outline on glove + sleeve; the illustration's defining stroke |
| brand/sleeve | #000000 | (measured)(inferred) | forearm bleeding off the bottom edge (icon) / lower-right (cover) |
| color-strategy | drenched single-hue (cover) | (estimated)(inferred) | the surface *is* the color — orange carries ~100% of the cover |
| icon/tile-shape | full-bleed rounded-rect (iOS/legacy squircle) | (estimated)(inferred) | motif bleeds off the tile edge; not a centered-glyph-on-material composition |
| chrome/* | — | — | no window chrome supplied; every chrome token is a knowledge gap |

## Layout skeletons

**None.** No UI surface was supplied, so there is no region layout to record. (Cover composition, for reference only: single centred motif, off-centre to the right, fingertip at optical upper-third, impact-rays radiating from the fingertip — a poster composition, not an interface.)

## Signature moves

- **[GOLDEN-NUGGET] The cursor as mascot.** The whole brand is a visual pun: the classic white four-fingered cartoon glove — the universal "pointing hand" of 1930s animation (Mickey) and its modern revival (Cuphead) — literally *is* the macOS pointer the app enhances. Product function and brand mark are the same object. This is the app's entire identity in one decision.
- **Comic "impact" speed-lines around the fingertip** (cover) — encodes the product promise (attention capture / "look here") pictorially: the cursor is the thing that pops. Directly maps to the product's Von Restorff / peripheral-motion premise.
- **Heavy black keyline + rubber-hose curves** — a deliberate retro-cartoon rendering (thick uniform outline, bulbous glove, gloss), committing hard to a playful register rather than a flat modern app-mark.
- **Icon reads legacy-glossy, not Liquid Glass.** The icon glove carries a beveled specular sheen (highlight upper-left, soft drop shadow) under a dark keyline, and the motif bleeds full-tile — a pre-Big-Sur skeuomorphic-glossy treatment, **not** Icon Composer's layered-on-material grammar and not the current centered-glyph convention. Recorded as a signature/era observation for a later icon digest, not scored here.

## Defects

- **No UI-surface defects can be logged** — nothing gradable was supplied. This is a *coverage* gap, not a quality verdict; do not read the absence of logged defects as a clean bill of health.
- (Icon-level, provisional, pending a real Workflow B digest) the full-bleed glossy treatment and off-centre motif would likely miss current macOS icon conventions (centred glyph, layered material, no baked gloss) — flagged, not scored.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| — (no UI surface supplied) | n/a | 14-point rubric and 10-point native audit not run — no interface present in either image; brand illustration + icon are out of rubric scope |

## Knowledge gaps (what a future pass must bring)

Everything that matters about this app's *interface* is missing: the menu-bar popover/extra, any settings/preferences surface, the cursor-overlay UI itself, light/dark handling, window chrome, control density, framework lineage. Bring one real screenshot of any Pokey surface and this profile becomes a genuine UI digest instead of a brand record.
