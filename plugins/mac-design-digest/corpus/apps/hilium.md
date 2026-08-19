# Hilium — profile

- **Source:** macapp.supply (meta) · **Surfaces digested:** 1 marketing composite containing 1 iOS companion-app screen (remote/trackpad control surface), dark · **Last updated:** 2026-07-19
- **One-sentence identity:** A "black-remote-control-surface" — iOS Control Center's recessive dark capsule grammar turned into a Mac trackpad/remote, with a single blue→green volume gradient as the only chromatic event. Peers: iOS Control Center dark sheet, the Apple TV Remote tile, Rogue Amoeba control panels.
- **Cluster:** unassigned (no macOS surface to cluster; iOS contrast evidence only)
- **Lineage:** unknown for the macOS product (**never shown**); the sole depicted UI is a genuine **iOS / iPhone** app screen (low confidence it says anything about the Mac app) — iOS evidence is contrast-only and never feeds macOS canon
- **Era (chrome):** unknown (no macOS chrome depicted). The iOS surface reads as current iOS 26 dark (Liquid-Glass-adjacent dark capsules), but that is not a macOS-era signal.

> **Digest honesty flag.** The provided images are a **marketing cover** (device-in-space on a black stage) and an **app icon** — no macOS window, sidebar, toolbar, or settings surface appears anywhere. The one interactive UI shown lives inside an iPhone frame and is therefore iOS. This profile records that UI and the brand/marketing evidence honestly, but it teaches the corpus **nothing about Hilium's macOS design** (the Mac side is presumably a menu-bar/receiver helper, undepicted). Additionally the phone is 3D-tilted and foreshortened, so every in-app measurement is `(estimated)` with wide ranges — semantics are trustworthy, pixels are not.

## Tokens

Provenance is capped at `(estimated)(inferred)` throughout: single surface, perspective distortion, iOS not macOS. Marketing/brand tokens are marked `brand`.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/stage (marketing) | #020202 → #0A0A0A near-black, faint concentric radar-ring vignette | (measured)(inferred) brand | Backdrop of the cover composite; rings echo the logo burst |
| bg/canvas (app) | near-pure black ~#000–#0A0A0A | (estimated)(inferred) | iOS remote surface ground |
| texture/trackpad | subtle dotted-grid on black | (estimated)(inferred) | Marks the touch/trackpad zone; the surface's one texture |
| control/fill | dark translucent gray capsules/circles, ~1 step above black | (estimated)(inferred) | Volume track, device chip, back/keyboard buttons; **low separation from canvas — see Defects** |
| accent/active | volume fill blue→green horizontal gradient (~#3B82F6 → #34C759-ish) | (estimated)(inferred) | The single chromatic event in the whole UI; Von Restorff moment |
| type/value | "42%" white ~15–17pt-class, "MacBook Pro" white ~15–16pt-class | (estimated)(inferred) | SF-class sans; only text in the app UI |
| radius/controls | capsule (device chip, volume track) + full-circle (back, keyboard) | (estimated)(inferred) | Pill-everything; consistent |
| icon/app-strip | 5 visible squircle app icons (Finder/Safari/Clock/Calendar/Mail), colorful | (measured)(inferred) | Represents the Mac's running apps; Finder carries a tiny close ✕ badge |
| type/headline (marketing) | ~64–72px off-white #E5E5E5 grotesk, semibold, 2 lines, tight leading | (estimated)(inferred) brand | "Turn your iPhone into a Mac trackpad"; SF Pro Display-class |
| type/subhead (marketing) | ~24–28px mid-gray secondary | (estimated)(inferred) brand | De-emphasized supporting line |
| brand/logomark | white radial "tap-burst" spokes (no arrow), monochrome | (measured)(inferred) brand | Bottom-left of cover; matches icon glyph |
| icon/bg | cyan→blue diagonal gradient #00D3FF → #00E5FD → #009DFB | (measured)(inferred) brand | iOS-style rounded-square (~22% radius), flat single-layer, no macOS layered-glass depth |
| icon/glyph | white radial burst + cursor arrow pointing to center | (estimated)(inferred) brand | "tap ripple + pointer" = the control-gesture metaphor |

## Layout skeletons

**iOS remote / trackpad surface (only interactive UI shown, foreshortened):**
Top: iOS status bar (9:41 / cellular / wifi / battery). Below it a large dark **trackpad zone** filling the upper ~60% of the screen, marked only by a faint dotted grid and a central handle pill. Beneath the trackpad, a horizontal **running-apps strip** of ~5 colorful squircle icons (Mac's open apps; leading icon has a close ✕ badge). Below that a full-width **volume control**: leading speaker glyph → capsule track with a blue→green gradient fill (~42%) → trailing "42%" label. Bottom **action bar** of three elements evenly distributed: circular back "‹" button (leading) · wide "MacBook Pro" device-selector capsule (center) · circular keyboard button (trailing). All controls dark-translucent; the only saturation is the volume gradient + the borrowed app-icon colors.

**Marketing composite (the cover itself — brand, not app):**
Left-aligned text column on a black stage: two-line off-white headline + gray subhead + small white logomark bottom-left. Right half: an iPhone floated at a 3D tilt with drop shadow, faint concentric radar rings behind it (logo motif at scale). Classic indie app-launch "device-in-space" template.

## Signature moves
- **[GOLDEN-NUGGET] The black control-stage.** A near-pure-black canvas where the dotted trackpad texture and one blue→green volume gradient are the *only* visual events; every actionable control is a dark-translucent capsule that deliberately recedes. The design makes itself disappear so the Mac being controlled (its colorful app icons, its name) is the figure and the phone is the ground. This is a real, systematic taste choice — a "remote should vanish in your hand" posture — even though it lives on iOS and cannot feed macOS canon.
- **Radar-ring / tap-burst motif carried from logo → backdrop.** The concentric rings behind the phone and the radial-spoke logomark are the same idea (a tap/click rippling outward), tying brand to the gesture-control premise.

## Defects
- **Contrast Dilution / low UI contrast (iOS surface).** The dark-gray control fills (back button, keyboard button, device chip, volume track) sit only ~1 tonal step above the near-black canvas — non-text separation likely <3:1. On a real device the black stage is elegant but the affordance edges risk vanishing; canon (and WCAG 3:1 non-text) would firm the control fills or add a hairline. Flagged, not confirmed (perspective + JPEG compression).
- **Target Starvation risk.** The close "✕" badge on the Finder icon is a tiny glyph on an already-small icon — a sub-24px tap target if literal. Mockup detail, noted.
- **Digest limitation, not an app defect:** the cover foreshortens the phone so heavily that most of the actual UI is unmeasurable and the macOS product is entirely absent — marketing chosen over design evidence.

## Rubric history
| Surface | Score | Failures / notes |
|---|---|---|
| iOS remote surface (contrast evidence) | ~9/14 applicable (many N/A) | #10 UI contrast (dark controls on black, <3:1 risk); #5/#6/#13/#14 N/A (no body text, no forms, touch UI); grid (#1) unverifiable under 3D perspective |
| Native-tells audit (macOS) | ~1/10 — category mismatch | Not a macOS surface: #1 lineage fails (iOS), #2–#10 N/A. Low score is "wrong platform," NOT a quality verdict. |
