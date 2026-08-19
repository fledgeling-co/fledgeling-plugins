# HealthyNotch — profile

- **Source:** macapp.supply (`healthynotch.com`) · **Surfaces digested:** notch dropdown HUD dashboard (dark, shot-2); two notch reminder banners (dark, shot-3/shot-4 top strips); marketing composites (cover + shot-1, brand evidence only) · **Last updated:** 2026-07-19
- **One-sentence identity:** A wellness-nag HUD mounted on the MacBook notch — in the NotchNook / Alcove / DynamicLake genre — but themed as an 8-bit arcade cabinet: pixel-art heart, neon-on-black metrics, and a gentle humane voice instead of clinical health charts.
- **Cluster:** unassigned — fits the corpus's emerging `notch-hud / dynamic-island-genre` candidate (peers: Alcove, DynamicLake, Claude Notch Usage Companion). Its retro-pixel theme differentiates it from the pure iOS-Dynamic-Island-clone members.
- **Lineage:** native (high) — the notch-HUD form factor is native-only: a borderless always-on-top NSPanel/SwiftUI overlay positioned around the physical notch (no Electron app can morph a pill out of the notch bezel). BUT the visible grammar is **fully custom-drawn** (opaque true-black HUD, neon identity hues, pixel-art glyphs, tracked-uppercase labels) — zero standard AppKit chrome/controls. Per the lineage gate, this bespoke grammar is recorded as tells + corrections and does **not** feed macOS native canon or clusters.
- **Era (chrome):** custom — opaque near-black fill (not Liquid Glass, not vibrancy, not NSVisualEffectView). The black is a purposeful design choice: the panel fuses with the physical black notch/bezel, so glass would break the illusion. Absence of glass here is legitimate, not a defect.

> **Evidence caveat:** shot-1 and cover are marketing composites (glass card + headline over a Tahoe-style gradient wallpaper) with **no app UI** — brand evidence only. shot-3 and shot-4 are marketing composites whose **top strip** carries a genuine notch banner (the app UI); the lower two-thirds is the same composite treatment. Only shot-2 is a (near-)full app surface. All three composites are 1270×760 renders at an **indeterminate scale** — treat every pt value below as `(estimated)` with wide ranges; trust the *proportions and hierarchy*, not the absolute point sizes.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/panel | near-black `#0A0A0B`–`#101012`, opaque | (estimated)(confirmed) | HUD dropdown + notch banners; appearance-independent OLED-black, fuses with notch |
| radius/panel | ~28–34px bottom corners (top flush to screen edge) | (estimated)(confirmed) | large rounded-rect that morphs down from the notch; banners share the shape at smaller size |
| radius/button | ~10–12px (gear, "+" log button) | (estimated)(inferred) | translucent-fill rounded squares |
| radius/status-glyph | ~18–22px squircle outline | (estimated)(inferred) | mint "mood face" container |
| radius/progress-bar | capsule (~3px half-height) | (estimated)(confirmed) | all three metric bars |
| fill/button | white ~8–12% translucent | (estimated)(confirmed) | gear + "+" buttons; recessive, non-CTA |
| type/status-name | reads Title2-Bold (~17px), white | (estimated)(inferred) | "Balanced" |
| type/status-subtitle | reads Body (~13px) Regular, white ~50–55% | (estimated)(inferred) | "Nice and steady today" — de-emphasis tier |
| type/metric-value | reads Title1-class Bold (~26–30px), white | (estimated)(confirmed) | "1.2/2L", "4/6", "5/8" — value dominates label |
| type/metric-label | reads Caption/Footnote (~10–11px), **tracked-uppercase**, white ~40–50% | (estimated)(confirmed) | WATER / BREAKS / MOVEMENT — non-native tell, see Defects |
| type/banner-title | reads Headline-Bold (~15px), white | (estimated)(confirmed) | "Move that body", "Thirsty yet?" |
| accent/water | neon cyan `~#20C8F0` | (estimated)(confirmed) | droplet glyph + progress fill + pixel-droplet banner glyph |
| accent/breaks | vivid green `~#2FD855` | (estimated)(confirmed) | check-circle + progress fill |
| accent/movement | vivid orange `~#FF9A20` | (estimated)(confirmed) | walking-figure + progress fill + pixel-equalizer banner glyph |
| accent/balance | neon mint `~#3EE0C0` | (estimated)(inferred) | status "mood face" glyph stroke |
| track/progress | white ~10% on black | (estimated)(confirmed) | unfilled bar remainder; sits <3:1 (recessive by design) |
| divider/hairline | white ~8% | (estimated)(confirmed) | header→metrics separator + inter-column verticals; <3:1 |
| brand/headline (composite) | bold geometric sans (reads SF Pro Display Bold), white | (estimated)(inferred) | marketing only — NOT an app token |
| brand/wallpaper (composite) | flowing blue→teal→cream gradient (Tahoe-style) | (estimated) | marketing backdrop only |

## Layout skeletons

**Notch dropdown HUD (shot-2)** — a single opaque rounded panel morphing down from the notch, ~910px wide in a 1270px render (~0.7 of frame width). Two stacked regions:
- *Header row:* leading status "mood face" glyph (mint squircle outline, pixel-dot smile) → title/subtitle stack ("Balanced" bold over "Nice and steady today" gray) → large flexible gap → trailing gear button (translucent rounded square). ~16–20px internal padding. A full-width hairline divider closes the region.
- *Metrics row:* three equal-width columns split by 1px vertical hairlines. Each column is a top-aligned stack: [colored glyph + tracked-uppercase label] → large white value → capsule progress bar (colored fill on dark track). The WATER column carries an extra trailing "+" button inline with its label (quick-log affordance). Within-group gaps (icon↔label, label↔value, value↔bar) are tight; between-column separation is a divider + margin — Gestalt proximity holds.

**Notch reminder banner (shot-3/shot-4)** — a compact black pill emerging from the notch, top flush to the screen edge, ~20px bottom corners. One row: leading bold-white title (playful copy) → flexible gap → trailing pixel-art metric glyph (orange 8-bit equalizer for movement; blue dot-matrix droplet for water). A transient nudge, not a panel.

## Signature moves

- **[GOLDEN-NUGGET] The notch is the product surface.** Reminders emerge as pills from the physical notch and the full dashboard drops down from it — the app's entire UX premise is "right where you already look" (its own subhead). Opaque true-black is chosen deliberately to fuse software with the bezel; glass would destroy the conceit. Systematic across every surface.
- **[GOLDEN-NUGGET] An 8-bit theme carried edge to edge.** Pixel-art heart app icon → pixel-dot "mood face" status glyph → pixel-art banner glyphs (equalizer bars, dot-matrix droplet). A consistent retro-arcade motif that gives a nagging health tool warmth and whimsy instead of clinical gauges — its differentiator within the notch genre.
- **Per-metric identity hue + value-dominant hierarchy.** Each metric owns a neon hue (cyan water / green breaks / orange movement / mint balance); value is set large-white, label small-gray-tracked. Activity-ring logic without the rings — and each hue is always paired with a glyph and label, never color alone.
- **Humane micro-voice.** "Thirsty yet?", "Move that body", "Nice and steady today", "before it starts complaining" — gentle, personified copy that softens interruption, matching the tagline "Work shouldn't cost you your health."

## Defects

- **Tracked-uppercase micro-labels (mild non-native tell).** WATER / BREAKS / MOVEMENT are letter-spaced caps — the web/iOS-widget convention, where AppKit grammar is sentence-case. Systematic and compact-purposeful (glanceable HUD), so it reads more as genre styling than error, but it leans the app slightly further from native than its notch-genre peers (the Claude Notch companion, by contrast, was noted for *avoiding* tracked-uppercase). Corrective: sentence-case or small-caps at native tracking if native feel were the goal — but the arcade theme arguably earns it.
- **Recessive non-text contrast (minor).** Hairline dividers (white ~8%) and progress-bar tracks (white ~10%) sit below the 3:1 non-text floor. Intentional recession, not amateurism — but a hair more track contrast would keep the "remaining" portion legible at peripheral glance.
- No hard cross-platform anti-pattern present: spacing reads on-grid, hierarchy is strong (value > label), no Focal Collision (gear/"+" are quiet, no competing saturated CTAs), no Proximity Failure.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| notch dropdown HUD (shot-2) | 12/14 | #10 non-text contrast (dividers/tracks <3:1); #6/#12 n/a (no prose/inputs); #14 focus state unseen |
| notch reminder banner (shot-3/shot-4) | 11/14 | #4/#5 n/a (single element); #6/#11–14 n/a (no components/inputs/focus); minimal by design — scored on what applies |

**Native-tells audit (shot-2, HUD):** ~7/10 applicable-pass. The genre exempts most chrome checks — no traffic lights (correct for a floating HUD), no toolbar, no sidebar, no glass required (opaque black legitimate), no list selection. Real dings: tracked-uppercase labels (the sentence-case-headers analog), and the fully-custom control grammar (no standard AppKit controls, by explicit design). Passes: concentric corners (panel > glyph > buttons > capsule bars), identity-color discipline (hue always paired with glyph+label), one quiet primary action, native-only runtime.
