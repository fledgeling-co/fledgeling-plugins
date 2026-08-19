# Cursor — profile

- **Source:** macapp.supply · **Surfaces digested:** cover.png (brand lockup — **no app UI window present**) · **Last updated:** 2026-07-19
- **One-sentence identity:** *Not determinable from the supplied evidence* — the only image is a marketing brand lockup; no app surface was provided to profile. (Product-knowledge prior, not image evidence: Cursor is an Electron VS Code fork AI code editor, peer to Zed / VS Code / Windsurf.)
- **Cluster:** unassigned — cannot assign without a UI surface
- **Lineage:** web-electron (**low confidence — external product-knowledge prior, NOT derived from the cover**, which contains zero UI). Per persona rule, lineage must be judged from a UI *body*; none exists here, so this classification carries no evidentiary weight for canon and Cursor contributes **no** macOS-native evidence.
- **Era (chrome):** unknown — no window chrome, toolbar, or content visible

## Evidence caveat

The macapp.supply payload for Cursor is a **cover + icon only** (empty `gallery`, no `shot-*` files). The cover is a pure brand composite: an off-white logo lockup centred on a warm near-black field, no device frame, no app screenshot inside it. Per the skill's cover rule, only the **brand layer** is analysable here; there is no app-window layer to extract. Consequently **no UI rubric, no native-tells audit, and no layout skeleton can be produced** — those require an actual surface. Everything below is brand evidence, marked as such, and must never feed macOS UI canon or style clusters.

## Tokens (brand evidence only — from cover.png)

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/bg-cover | `#14120B` — warm near-black (R20 G18 B11) | (measured)(inferred) | Distinctly warm/brown-ward, **not** neutral #000 or blue-black; unusual restraint for a dev-tool brand |
| brand/logo-fill | `#EDECEC` — off-white | (measured)(inferred) | Slightly warm-neutral, not pure #FFF — monochrome lockup, single ink |
| brand/palette-economy | 2 values total (1 ground + 1 ink) | (measured)(inferred) | Maximally restrained; no accent hue in the lockup |
| brand/wordmark-face | Extended geometric techno-grotesk, wide tracking, monoline stroke, squared counters w/ softened outer corners (Eurostile Extended / Michroma / Bank-Gothic-adjacent class) | (estimated)(inferred) | Reads industrial/hardware-tech, not warm/humanist; likely a custom or customised face |
| brand/mark | Rounded-edge isometric cube (hex silhouette) with negative-space **downward cursor/arrow** carved through the top + front faces | (estimated)(inferred) | The literal "cursor" pun sits inside a "cube/block/build" container; corners are soft-rounded, not sharp |

## Layout skeletons

None — no UI surface was provided. (Cover composition: single horizontally-centred logo lockup, mark left of wordmark, on a full-bleed flat ground. This is brand layout, not app layout.)

## Signature moves

- **[GOLDEN-NUGGET — brand, not UI]** *Cube-as-cursor negative space:* the mark hides a downward pointer inside an isometric cube via cut-out geometry — one shape carries both "3D block/build" and "cursor," the product's whole thesis in a single glyph. Systematic and purposeful *as branding*; cannot be promoted as UI taste.
- **[brand]** *Warm near-black ground (`#14120B`, not neutral):* a deliberate temperature choice against the dev-tool default of blue-black/neutral graphite. Worth watching for whether it recurs in an actual Cursor UI surface (would corroborate a warm-dark house style) — currently single-data-point, uncorroborated.

## Defects

- None assessable — a brand lockup cannot fail the UI rubric or the native-tells audit (category mismatch). Not recording pseudo-defects against a non-UI surface.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| cover.png (brand lockup) | N/A — not a UI surface | 14-point UI rubric and 10-point native-tells audit both inapplicable; no window chrome, controls, type ramp, or content to measure |

## What would move this profile forward

Need ≥1 real Cursor **app window** screenshot (editor + sidebar + AI panel, ideally light *and* dark) to: (1) confirm/refute the web-electron lineage from the body, (2) run both rubrics, (3) test whether the warm-black brand temperature carries into the product chrome. Until then Cursor is a brand digest, not a UI digest.
