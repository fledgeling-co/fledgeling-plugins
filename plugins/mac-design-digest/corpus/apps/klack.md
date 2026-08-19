# Klack — profile

- **Source:** macapp.supply (marketing cover composite only — no in-app screenshots supplied) · **Surfaces digested:** menu-bar-extra control panel (light), sound-profile picker popover (dark) · **Last updated:** 2026-07-19
- **One-sentence identity:** a Control Center-idiom menu-bar utility that dresses audio presets as collectible mechanical-keyboard switches — Dato/One Thing's menu-bar economy given a boutique hardware-catalog personality.
- **Cluster:** unassigned (candidate: *boutique-menu-bar-utility* — sole member so far)
- **Lineage:** native (med confidence) — SF Pro throughout, 13pt-class body, macOS control metrics, Control-Center-style floating panels; but evidence is a rendered marketing composite, not a live screenshot, so lineage cannot be verified against a real window. No web/Electron tells (no 16px body, no tracked-uppercase headers, no kebab menus, arrow-cursor implied).
- **Era (chrome):** Liquid-Glass-adjacent (macOS 26 Tahoe) — warm translucent glass panels that lens the backdrop through, large corner radii, Control-Center panel grammar. The surrounding dark rounded-pill "menu bar" and `Sat 18:74` clock are **marketing composite dressing, not literal chrome** (18:74 is an impossible time — a mock giveaway).

## Tokens

All values are `(estimated)` — sampled from a compressed marketing render at unknown retina scale; ranges over false precision.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/backdrop | #FFF7ED warm cream | (estimated)(inferred) | cover backdrop — BRAND evidence, not app UI |
| brand/ink | #292524 warm near-black | (estimated)(confirmed) | wordmark, headline, light-panel title — one shared ink |
| brand/marker | #F0ABFC lilac highlight | (estimated)(inferred) | headline marker swipe under "sound" — brand only |
| accent/toggle-on | ~#10B98C–#12B886 teal-green | (estimated)(inferred) | master switch ON fill — a HOUSE accent, NOT system blue |
| panel/light-bg | #E9E2DB→#F5F0E8 warm off-white, radial gradient, translucent | (estimated)(inferred) | menu-bar-extra control panel; reads as light glass lensing the cream backdrop |
| panel/dark-bg | #2B2628 warm graphite, translucent | (estimated)(inferred) | sound-picker popover; vibrancy over purple wallpaper |
| text/primary (dark panel) | #FFF7ED warm white | (estimated)(confirmed) | row labels "Japanese Black" / "Crystal Purple" |
| text/primary (light panel) | #292524 | (estimated)(inferred) | "Klack" title, 17pt-class bold |
| text/secondary | #75706F warm gray (~50–55%) | (estimated)(confirmed) | "Sound", "Switches", "CherryMX™", "Everglide™" — section/field labels |
| slider/filled | ~#1C1C1E near-black | (estimated)(inferred) | filled portion of Sound slider is BLACK, not accent — house style |
| slider/track | ~#D8D4CC warm light gray | (estimated)(inferred) | unfilled track on light panel — low contrast (see Defects) |
| chip/identity-gray | #2D292A | (estimated)(inferred) | "+" add-chip for Japanese Black (a dark switch → dark chip) |
| chip/identity-purple | #EC9DF8 magenta-purple | (estimated)(inferred) | "+" add-chip for Crystal Purple — chip hue = the switch's colour |
| control/switch | capsule, cream knob, ~40×22 proportion | (estimated)(inferred) | matches macOS switch geometry; custom tint |
| control/play | translucent white circle (~15–20% fill), white ▶ glyph, ~28pt | (estimated)(inferred) | per-row audition button, trailing |
| radius/panel | large, ~14–18pt | (estimated)(inferred) | both panels; concentric with rounded chips inside |
| type/title | ~17pt SF Pro Bold (Title2-class) | (estimated)(inferred) | "Klack" |
| type/row-label | ~15pt SF Pro Medium (Title3/Body-class) | (estimated)(inferred) | sound names |
| type/section-header | ~13pt SF Pro Semibold, secondary colour, title case | (estimated)(confirmed) | correct macOS section-header grammar |

## Layout skeletons

**Menu-bar-extra control panel (light glass).** Single column, ~540px-region wide. Top row: leading bold title "Klack" | trailing master switch (green, ON), baseline-aligned. Hairline separator. Field block: left-aligned secondary label "Sound" over a full-width slider (black-filled left → cream knob → gray track). Hairline separator. Field block: secondary label "Switches" over a selectable list row (leading swatch, redacted label bar, trailing checkmark = current selection). Reads exactly as a Control Center module stack: toggle → slider → picker.

**Sound-profile picker popover (dark glass).** Single column list grouped by brand section. Section header (secondary gray, title case, "CherryMX™") → row(s). Each row: leading rounded-square "+" add-chip (fill = switch identity colour) · row label (warm-white, ~15pt) · trailing circular ▶ audition button. Full-width hairline separator between rows/sections. Generous ~44pt row height. Three aligned vertical axes: chip-left, label-left, play-right.

## Signature moves
- **[GOLDEN-NUGGET] Two-material mood split.** The app splits *choosing* sound from *using* sound across two materials: a dark, immersive warm-graphite catalog (where you browse ™-branded switches against an iridescent CD/vinyl wallpaper) vs a light, quick warm-cream control panel (where you toggle and set volume). One utility, two deliberately opposite moods — the picker sells, the panel serves.
- **[GOLDEN-NUGGET] Presets-as-hardware.** Audio profiles are named and coloured like physical products: "CherryMX™ Japanese Black", "Everglide™ Crystal Purple", each with a per-switch identity colour on its "+" chip. The whole personality is skeuomorphism-by-taxonomy — you're not picking a sound file, you're collecting switches.
- **Audition-before-commit rows.** Every row carries a leading "+" (add to library) *and* a trailing "▶" (preview). You hear the switch before adopting it — the interaction is built around the fact that a sound cannot be judged from its name.
- **Monochrome control theming with one warm-teal accent.** The slider fills black and the toggle turns a house teal rather than system blue — a committed, hardware-object palette (keycap black + one candy accent) instead of the platform accent.

## Defects
- **Accent not system-bound (native tell, not a defect per se).** Master toggle uses a brand teal, slider fill uses black — neither binds to `controlAccentColor`, and the two aren't even the same hue. Legitimate house style for a boutique menu-bar utility, but it means the app opts out of the user's chosen accent. Record as a lineage/brand tell, not canon.
- **Contrast Dilution (borderline) — UI contrast.** Slider unfilled track (~#D8D4CC) on the warm off-white panel (~#EFE9E1) is well under 3:1; the track edge is barely legible. Estimated from a compressed render — flag, don't assert.
- **Contrast (borderline) — secondary labels.** "Sound"/"Switches" (~#7?7?7? warm gray) on the light panel read ~3.5–4:1; fine as de-emphasis, marginal as 13pt text against WCAG 4.5:1. Estimated.
- **Marketing-mock artifacts (not app defects):** the "Switches" row shows skeleton/redacted bars; the pill menu bar and `18:74` clock are composite dressing. Excluded from real-UI judgement.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| menu-bar-extra control panel (light) | 11/14 | #9 secondary-label contrast borderline (est), #10 slider track <3:1 on warm panel (est), #14 focus state not evidenced (marketing render) |
| sound-profile picker popover (dark) | 12/14 | #10 translucent ▶ glyph contrast borderline (est), #14 focus state not evidenced |
| native-tells audit (combined) | 8/10 | #6 accent not system-bound (teal toggle + black slider, internally inconsistent); #3 selection grammar only shown as menu-checkmark, no inset-rounded list selection to verify |
