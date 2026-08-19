# Onlook — profile

- **Source:** macapp.supply (onlook.cam) · **Surfaces digested:** marketing cover composite + app icon — **no native app UI provided** · **Last updated:** 2026-07-19
- **One-sentence identity:** A menu-bar Ring-camera viewer whose entire brand is a warm chiaroscuro reframe of home security — a glowing open-doorway icon and SF Pro cream text on a drenched amber-to-black ground, inverting the cold blue/night-vision cliché of surveillance into "someone left the light on for you"; atmospheric indie-utility marketing, not a shipped-UI surface.
- **Cluster:** unassigned (no native UI evidence to cluster on)
- **Lineage:** unknown (low) — the app is a Mac menu-bar utility (tagline "Ring cameras in your Mac menu bar"), near-certainly an AppKit `NSMenuBarExtra` / native SwiftUI popover, but **not one pixel of app chrome is shown**. The only rendered surface is a marketing composite. Nothing here feeds macOS canon.
- **Era (chrome):** unknown — no window chrome shown. Icon reads **Big Sur / modern squircle era**, but is an *emissive single-scene* icon (a lit doorway rendered in perspective) rather than a flat centered glyph; a small render cannot separate Big Sur material from a soft-glow Liquid-Glass treatment.

## What is (and isn't) in the inputs

Two images, zero app UI:
- **`cover.jpg` (1200×630)** — an **OG-image-aspect marketing composite**, not an app screenshot. Drenched dark warm ground (near-black `#080000` top → warm amber glow `#39290F` bottom-center), the app icon rendered centered, and a two-line SF Pro headline. This is *brand evidence*, analysed below; it is **not native macOS UI** and is excluded from macOS canon and clusters.
- **`icon.webp` (102×102)** — the app icon, recorded as identity/brand evidence (this is Workflow A, so no full 12-point icon digest; a proper icon digest belongs in `icons/onlook.md` under Workflow B).

The app's actual UI — a menu-bar-extra popover with a Ring-camera feed grid, near-certainly — was not supplied. **The corpus cannot yet say anything about how Onlook's UI looks or whether it reads native.**

## Tokens

Brand/marketing tokens (composite surface — never promote to macOS canon):

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/bg-top | `#080000` near-black, warm-tinted | (measured)(inferred) | ground at top; warm-black, not pure `#000` |
| brand/bg-glow | `#39290F` warm amber-brown | (measured)(inferred) | bottom-center bloom; the surface *is* the colour (drenched strategy) |
| brand/bg-edge | `#0C0401`–`#090401` | (measured)(inferred) | lower corners / mid ground — deep warm shadow |
| brand/ink-headline | `#F2E8CF` warm cream | (measured)(inferred) | headline; ~16–17:1 on the near-black ground — very high contrast |
| brand/ink-warm-accent | shifts toward `#F5E6A0`-class yellow on lower/right words | (estimated)(inferred) | the headline carries a warm gradient — "bar." reads more yellow than "Ring"; type sits *inside* the light field |
| brand/type | SF Pro (Display), Regular weight, sentence case, terminal period | (estimated)(inferred) | system grotesque; macOS context → SF Pro over Inter. Restrained, native-voiced brand |
| icon/bg | warm graphite-to-black squircle, `#262721`-class body with warm vignette | (measured)(inferred) | dark surround, not gradient-plane; the frame recedes to black at the corners |
| icon/light-source | pale luminous door `#F4FFB0`-class (near-white warm-green highlight) | (measured)(inferred) | the light IS the subject — emissive centre, soft bloom into surround |
| icon/floor | warm amber trapezoid `#AB7549`-class in perspective | (measured)(inferred) | light spilling forward onto a floor; establishes depth / a physical doorway |
| icon/shape | rounded squircle, single centered scene, no overlay device | (measured)(inferred) | Big Sur-era grammar; painterly emissive scene, not a flat glyph |

## Layout skeletons

**cover.jpg — marketing composite, dark, ~2× export (illustrative).** Single centered vertical axis: the app-icon squircle sits in the upper third, then a large gap, then a two-line headline ("Ring cameras in / your Mac menu bar.") centered beneath it, both lines one size / one weight, tight display leading (~1.1–1.2). Radial/vertical light: near-black top corners, a warm amber bloom rising from bottom-center that both grounds the composition and back-lights the type. No CTA, no wordmark, no chrome — one icon, one sentence, one light source. Loose, poster-like, hushed density.

**App UI:** none provided — skeleton unknown.

## Signature moves

- **[GOLDEN-NUGGET] The warm-light reframe of home security.** Ring/camera/security marketing is conventionally cold — night-vision green, clinical blue, alarm red, a lens staring back. Onlook inverts the entire temperature: a glowing *open doorway* spilling warm light onto a floor, on a drenched amber-black ground, with cream type. The icon is the emotional opposite of a surveillance lens — it reads "home / presence / a light left on," not "you are being watched." That inversion is carried consistently across background, icon, and type temperature, and it is the whole memorable budget of the brand. Systematic + purposeful → signature.
- **[GOLDEN-NUGGET] Type inside the light field.** The headline isn't a flat cream overlay: it carries a subtle warm gradient (cooler cream on "Ring", warmer yellow by "bar.") so the words appear lit *by* the same amber bloom rather than floating on top of it. A small, deliberate integration of type into the scene's lighting.
- **Emissive single-scene icon.** Unlike the corpus's common gradient-squircle-plus-centered-glyph grammar (e.g. Ajar), Onlook's icon is a painterly *scene* — a doorway rendered in perspective with the light source as the subject and warm floor-glow establishing depth. Reads unmistakably at small size as "light through an open door."

## Defects

- **No true design defect observable** — the composite is internally coherent (one axis, one light source, one type size, high-contrast type). This is a *marketing* surface, not the product.
- **Corpus-input gap (not an app defect):** the submission ships a marketing composite where a native app UI screenshot belongs — almost all brand evidence, essentially no product evidence. Onlook's native fidelity is entirely unmeasured.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| cover.jpg (marketing composite — NOT native UI) | applicable checks pass (~7/7); #1,#7,#8,#10,#11,#12,#13,#14 N/A | #2 alignment pass (single centered axis) · #9 text-contrast pass strongly (cream `#F2E8CF` on `#080000` ≈ 16–17:1); no CTA/inputs/borders to score |
| native app UI | — | not provided; cannot score |

**Native-tells audit:** N/A on every point — `cover.jpg` has no toolbar, sidebar, traffic lights, selection grammar, or native controls to audit. The app's native fidelity is **unmeasured**. If the menu-bar popover UI is later supplied, re-digest to actually place this app.
