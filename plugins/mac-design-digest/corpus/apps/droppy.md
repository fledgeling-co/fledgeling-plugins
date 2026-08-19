# Droppy — profile

- **Source:** macapp.supply (getdroppy.app) · **Surfaces digested:** cover — notch HUD (Now Playing media widget + "Playing Next" queue + detached glass launcher pill), dark · **Last updated:** 2026-07-19
- **One-sentence identity:** iPhone's Dynamic Island transplanted onto the Mac notch — Control Center's dark-glass Now Playing given a detached Liquid-Glass launcher, in the NotchNook / Boring Notch / MediaMate genre.
- **Cluster:** unassigned (proposed: `notch-hud-ambient` / dark-glass system-adjacent utility)
- **Lineage:** native — custom-drawn SwiftUI HUD (med confidence: SF Symbols set, Liquid-Glass launcher with container morphing, true-black material; no AppKit window chrome because it is a floating HUD, not a window)
- **Era (chrome):** Liquid Glass native (macOS 26+ "Tahoe/27") — glass launcher pill + scroll-under material behaviour
- **Provenance caveat:** the cover is a real-desktop screenshot (the app over the user's coastline wallpaper), NOT a device-frame marketing composite — so the panel and pill are genuine design evidence. But the capture scale is ambiguous (1816×568 crop, not a full logical screen), so all geometry/type is `(estimated)` with wide ranges; only sampled hex values are `(measured)`.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/panel (opaque zone) | `#000000` true black | (measured)(inferred) | top of the notch HUD reads pure 0,0,0 |
| bg/panel (glass edge) | dark translucent; samples `rgb(33,44,49)` teal over water wallpaper | (measured)(inferred) | lower panel dissolves to translucent glass — wallpaper bleeds through; floating-chrome glass, legitimate |
| text/primary | near-white `~#EBEBEB→#FFFFFF` | (measured)(inferred) | now-playing + queue titles; very high contrast on black |
| text/secondary | `#717171` (~44% white) | (measured)(inferred) | artist names + "Playing Next" header; ≈4.2:1 on black — borderline < 4.5:1, see Defects |
| progress/fill | `#EEEEEE` | (measured)(inferred) | elapsed portion of scrubber |
| progress/track | `#2F2F2D` | (measured)(inferred) | unplayed track, dark neutral |
| accent/source-badge | `#E54C58` Apple-Music red | (measured)(inferred) | source-app identity badge on album art — paired with meaning (which app is playing), NOT the app's own accent |
| pill/launcher-material | translucent Liquid Glass; wallpaper visible through it (sampled `rgb(166,147,104)` = sand passthrough) | (measured)(inferred) | detached capsule + separate rounded-square; both floating over desktop, no glass-on-glass |
| selection/fill | lighter translucent inset rounded-rect behind the selected `house.fill` glyph | (estimated)(inferred) | inset-fill selection grammar present; glyph is neutral white, NOT accent-tinted |
| radius/panel | large, ~16–20pt bottom corners | (estimated)(inferred) | flush to notch at top; only bottom corners rounded |
| radius/album-art | ~10–12px | (estimated)(inferred) | 1:1 artwork, concentric (< panel radius) |
| radius/launcher | capsule (pill) + rounded-square module | (estimated)(inferred) | matches macOS-27 capsule bezel convention |
| type/title (now playing) | Title1-class, ~20–24pt Bold | (estimated)(inferred) | glanceable HUD scale — larger than 13pt body on purpose (cap-height ≈1.6× the queue title) |
| type/queue-title | Title3-class, ~15pt Semibold/Bold | (estimated)(inferred) | cap-height ~22px in-frame |
| type/secondary | ~12–13pt Regular, gray | (estimated)(inferred) | artist rows + section header |
| symbols | SF Symbols, filled: `pause.fill` `backward.fill` `forward.fill` `list.bullet` `airplayaudio` `house.fill` `tray` `square.grid.2x2` `calendar` | (estimated)(inferred) | monochrome, native symbol set |

## Layout skeletons

**Surface — Notch HUD (Now Playing + queue), dark, floating.** Dark panel anchored flush to the notch cutout at top; only the two bottom corners round off (~16–20pt). Two-column split divided by a thin (~1px) vertical rule:
- **Left column (~55%):** header row = [album art 1:1 rounded ~10px, with a small red Apple-Music source badge over its bottom-right] + [title Bold / artist secondary, stacked, tight]. Below, a full-width scrubber = [elapsed `1:56` · light-fill track on dark · remaining `-1:07`]. Below that, a transport row = [queue-list button in a translucent rounded-square · `backward.fill` · **`pause.fill` centered and largest, bare glyph (no button chrome)** · `forward.fill` · `airplayaudio` trailing].
- **Right column (~45%):** "Playing Next" header (secondary color, title case) over a vertical queue list; each row = [art ~48px rounded + title Bold / artist secondary + trailing reorder handle `line.3.horizontal`]. Titles hard-clip at the panel's right edge (see Defects).
- **Detached below the panel, centered:** a Liquid-Glass **capsule launcher** = [`house.fill` selected (inset fill) | `tray` | `square.grid.2x2`] and, separated by a gap, a distinct glass **rounded-square** module = [`calendar` with a clock badge]. Two independent floating-glass modules, not one bar.

## Signature moves
- **[GOLDEN-NUGGET] Colonizes the notch dead-zone as the primary interactive surface** — the whole product. It borrows the iPhone Dynamic Island / Control-Center Now-Playing schema wholesale (Jakob's Law: users arrive pre-trained), so a Mac-first paradigm reads as instantly familiar. The screen's top edge is an infinite-depth Fitts target; parking a HUD there is a deliberate acquisition win.
- **[GOLDEN-NUGGET] Album art is the only chroma.** The HUD is monochrome on true black; the sole saturated elements are the artwork and the one red source badge (Von Restorff — the badge is the "which app" signal precisely because nothing else is colored). No user-accent binding is spent.
- **Two floating modules, not one bar.** The ambient-status panel (notch) and the navigation launcher (pill) are separate floating-glass surfaces. The launcher itself is one continuous glass capsule (three icons share a refractive edge = container morphing) with the calendar broken out as its own module — correct glass grammar, no glass-on-glass.
- **Concept-as-icon:** the app icon depicts the MacBook notch itself — a heavy black bezel with the notch cutout, wrapping a glowing blue concave "pillow" interior. The product's entire thesis in one object. (Recorded here as brand context; not digested under the icon workflow.)

## Defects
- **Truncation without ellipsis/fade (low confidence — may be marketing framing):** queue titles clip hard at the panel's right content edge ("Lotje (Lil Kleine Remi…", "Roeland Beelen & Lil Kle…") with no `…` or gradient fade. Canon would truncate with an ellipsis or a trailing scroll-edge fade.
- **Contrast Dilution (mild):** secondary label gray `#717171` on true black ≈ 4.2:1 — just under the 4.5:1 AA floor for the smallest labels (artist rows, "Playing Next"). Canon secondary-on-dark is `#FFFFFF`@55% ≈ `#8C8C8C` for ≥4.5:1. The larger now-playing/queue titles clear it easily; only the small metadata is marginal.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| notch HUD (Now Playing + queue + launcher), dark | 12/14 | #9 secondary label #717171 ≈4.2:1 < 4.5:1 (small metadata only); #6 line-length n/a but titles hard-truncate without ellipsis |
| — native-tells | 8/10 | #5 density runs glanceable-large not 13pt (HUD convention, not a defect); #6 accent not bound — neutral monochrome, no user-accent on selection/primary |
