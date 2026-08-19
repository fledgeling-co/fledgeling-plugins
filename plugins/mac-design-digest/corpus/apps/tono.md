# Tono — profile

- **Source:** macapp.supply (`sources/tono/`, cover.png + icon.png) · **Surfaces digested:** menu-bar-extra popover (light) · **Last updated:** 2026-07-19
- **One-sentence identity:** a photo-first menu-bar wallpaper picker whose chrome is deliberately desaturated — translucent sage material + black/white capsules — so the wallpaper is the only color on screen; Apple's Wallpaper settings crossed with an indie black-pill utility (Raycast-adjacent button language).
- **Cluster:** unassigned (candidate: "content-deferential utility" / photographic menu-bar tools)
- **Lineage:** native (med) — SF Symbols, vibrancy material, capsule bezels, menu-bar-extra form factor all read AppKit/SwiftUI. Cannot fully exclude a well-built Electron/Tauri menu-bar app from one composite, but no web tells present (no kebab menus, no tracked-uppercase, no pointer-hand). Non-native evidence would never feed macOS canon regardless.
- **Era (chrome):** Liquid Glass-era intent (low-med) — capsule buttons are the era's default bezel (Big Sur used 5–6pt rounded rects), large translucent tinted panel, soft large radii. From a single light-mode composite I *cannot* confirm true Liquid Glass lensing vs. plain Big Sur vibrancy (dark-mode-humility rule applies to material identification). Controls are app-custom, not stock system buttons.

## Source caveat

The only evidence is a **marketing composite**: the app popover floats over a deliberately-blurred green-foliage desktop chosen to demonstrate material translucency. The green cast on the panel is the backdrop bleeding through a light neutral vibrancy material — **not** an intrinsically green panel. Window scale is unverifiable; measurements below assume ~@2x render and carry wide ranges. All tokens are `(estimated)(inferred)` — one surface, composite provenance.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| window/type | menu-bar-extra popover, ~340–380pt wide | (estimated)(inferred) | single vertical stack; no traffic lights (correct for popover) |
| bg/panel-material | light neutral vibrancy/glass, reads sage over green desktop; ~1pt light hairline edge | (estimated)(inferred) | translucent — desktop visibly muted through it; floating-chrome-only glass (legit) |
| radius/panel | ~20–24pt | (estimated)(inferred) | large soft corner |
| radius/hero-image | ~14–16pt | (estimated)(inferred) | near-concentric with panel (ideal ~11pt), slightly loose |
| radius/thumbnail | ~14–16pt | (estimated)(inferred) | matches hero radius |
| radius/button | capsule (height/2) | (estimated)(inferred) | era signature; app-custom fill |
| control/primary-btn | black filled capsule (~#1C1C1E), white label, ~30pt tall | (estimated)(inferred) | "设为壁纸" (Set as wallpaper), trailing — most-contrast element on light panel |
| control/secondary-btn | white filled capsule, dark label, ~30pt tall, equal size to primary | (estimated)(inferred) | "换张" (Shuffle) — iso-sized filled, see Defects |
| icon/utility | monochrome dark-gray SF Symbols, ~18–20pt glyph | (estimated)(inferred) | gear / arrow.down / arrow.counterclockwise, borderless, leading in action bar |
| identity/favorite | coral-red filled heart ~#F0596A (≈ system Pink), no button chrome | (estimated)(inferred) | correctly a separate identity hue, paired with a glyph; floats on the hero |
| selection/thumbnail | faint low-contrast light ring (~1.5–2pt) | (estimated)(inferred) | marks current wallpaper; NOT accent-tinted inset — weak, non-standard |
| space/panel-padding | ~10–12pt | (estimated)(inferred) | consistent inset for hero, thumb-row, action bar (shared axes) |
| space/thumbnail-gap | ~10pt | (estimated)(inferred) | between-section gaps only marginally larger |
| type/button-label | ~13–15pt system (PingFang SC), medium weight | (estimated)(inferred) | Chinese localization |
| type/attribution | ~11–12pt white, source/author links underlined | (estimated)(inferred) | "照片作者 … 来自 …", connector words lighter than links |
| accent/system-blue | **absent** | (inferred) | app substitutes black primary + neutral selection for the system accent — see Signature |

**Brand note (icon.png, not scored — Workflow A only):** American-robin illustration (matte-black head/back with soft directional shading, saturated red breast, yellow beak) on a warm cream (~#F5F1E8) Big-Sur-era squircle, flat vector + soft contact shadow. **Warm, characterful, illustrative** — a deliberate temperature/personality *contrast* with the cool, neutral, photographic UI. Flag for synthesis: brand mark and app chrome do not share a palette family.

## Layout skeletons

**Menu-bar-extra popover (light):** single vertical stack inside a translucent ~22pt-radius shell, ~11pt padding.
1. **Hero** — full-width featured wallpaper, ~14–16pt radius, ~3:2 landscape. Overlays: top-right filled red heart (favorite, no chrome); bottom-left attribution text (white, author + Unsplash source, links underlined).
2. **Thumbnail strip** — 4 equal rounded (~14–16pt) images, ~10pt gaps, evenly distributed on the panel's left/right axes; current item = faint light ring.
3. **Action bar** — leading cluster of 3 borderless monochrome SF Symbols (settings / download / refresh); trailing pair of equal capsule buttons (white 换张 · black 设为壁纸). Trailing-primary placement is correct.

## Signature moves

- **[GOLDEN-NUGGET] Content-deferential monochrome chrome.** The app refuses the system accent entirely: primary action is a *black* capsule, secondary is *white*, selection is a neutral ring, utility glyphs are gray. The single saturated element in the whole UI is the wallpaper photo (plus the one red favorite heart). For a wallpaper picker this is purposeful and systematic — the chrome gets out of the photo's way. It is also a real trade-off: it overrides the user's chosen accent (native grammar wants selection/primary bound to `controlAccentColor`). Signature, not defect — internally consistent, and the identity hue (heart) is correctly separated and glyph-paired.
- **Chromeless favorite.** The red heart sits directly on the image with no button background — a light, content-first affordance.
- **Material as message.** The translucent popover lets the live desktop bleed through, quietly reinforcing "this is about *your* screen."

## Defects

- **Iso-styled competing actions (mild)** — 换张 and 设为壁纸 are two equal-size filled capsules. Native grammar and hierarchy discipline want one prominent action + one recessive (outline/text). Partly mitigated: black-on-light-panel gives 设为壁纸 clear primacy over the white capsule, and trailing placement is correct — but same size + both filled weakens the first-glance read. Canon fix: keep 设为壁纸 filled; demote 换张 to outline or tinted.
- **Contrast Dilution risk (#9)** — attribution text is white over a variable photo with no guaranteed scrim; legibility is image-dependent and can drop below 4.5:1 over light image regions. Canon fix: a subtle bottom gradient scrim.
- **Weak selection affordance (#10)** — the current-wallpaper ring is very low contrast and non-standard (not the accent-tinted inset fill). Easy to miss which thumbnail is active.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| menu-bar-extra popover (light) | 12/14 · native 7/10 | #9 attribution text over photo, no scrim · #10 thumbnail selection ring / gray icons low contrast · native #3 selection not accent-inset · native #7 two prominent filled capsules (#14 focus & #4 sidebar n/a; native #6 accent-override recorded as signature) |
