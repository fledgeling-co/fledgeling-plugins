# VoiceOS — profile

- **Source:** macapp.supply (meta.json + cover + icon) · **Surfaces digested:** none (marketing cover + app icon only — no app UI window) · **Last updated:** 2026-07-19
- **One-sentence identity:** An Apple-marketing-clean voice-control utility whose *brand* reads like a Superhuman/Raycast landing page — one electric-blue accent word on near-white, a monochrome mark — but whose *actual app UI is entirely unseen*.
- **Cluster:** unassigned (no UI evidence to place)
- **Lineage:** unknown (low) — **no application window is present in any supplied image**; framework lineage is genuinely unknowable, do not infer it from marketing typography
- **Era (chrome):** unknown — the app icon is a Big Sur-era squircle material tile, but a tile render is not chrome evidence

## What was actually supplied

Two images, neither a UI screenshot:
1. **cover.png (1200×630)** — a social/OG marketing composite: left half a display headline "**Voice** is your new keyboard" (the word "Voice" in electric blue, the rest pure black) on a flat `#F8F8F8` ground; right half a soft rounded-rect card holding a diagonal arc of third-party app icons (Slack, Google Sheets, Notion, VS Code, a black gem/Linear-class, ChatGPT, a red starburst app) with the black **VO** logo mark (down-triangle + filled circle) seated bottom-right. No window chrome, no traffic lights, no toolbar/sidebar/content — **not app UI**.
2. **icon.webp (204×204)** — the app tile: charcoal-black `VO` glyph (flat down-triangle + softly-sphered circle) on a white→`#F0F0F0` top-lit gradient. Recorded here as brand evidence only; a full icon digest (Workflow B) was out of scope for this pass.

The tagline ("Use your voice to control apps and get work done 10× faster") and the app-collage confirm the product is a **voice-control / dictation utility** — most plausibly a menu-bar extra or floating dictation panel — but no such surface was provided, so that stays a positioning inference, not a design reading.

## Tokens

All values below are **brand-layer** (marketing graphic + icon), **not native-UI tokens** — none may feed macOS canon.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/accent-blue | `#126FF6` (measured)(inferred) | | the "Voice" word; more saturated/bluer than kit system Blue `#0088FF` — a chosen brand electric-blue, not the platform accent |
| brand/ink | `#000000` (measured)(inferred) | | headline body text — pure black (marketing licence; native primary text is 85% black per kit) |
| brand/logo-black | `#0D0D0D` (measured)(inferred) | | VO mark on cover |
| brand/bg-marketing | `#F8F8F8` (measured)(inferred) | | flat achromatic light ground — cooler/plainer than apple.com `#F5F5F7` |
| brand/card-fill | `#F4F6F9`→`#EDEFF1` (measured)(inferred) | | faintly cool blue-gray app-collage card, soft diffuse shadow |
| brand/headline-type | ~72–80px, Bold, geometric-humanist sans (SF Pro Display-class) (estimated)(inferred) | | two-line display; single-weight, no serif pairing |
| icon/tile-bg | white → `#F0F0F0` top-lit gradient (measured)(inferred) | | Big Sur-era material tile, slight warm-neutral |
| icon/glyph | charcoal-black `#292929`; circle softly shaded (edge `#151515`) (measured)(inferred) | | flat triangle + subtly-spherical circle = the only depth cue |

## Layout skeletons

None — no app surface was supplied. The cover is a two-zone marketing composite (left: type stack; right: illustrative app-collage card), not an interface.

## Signature moves

- **Monochrome geometric mark from two primitives** — a down-pointing triangle ("V") + a filled circle ("O"), the circle given a whisper of spherical shading while the triangle stays flat. The entire brand depth budget spent on one edge of one shape. Restrained and memorable; reads at Dock size.
- **One-word accent** — exactly one blue word ("Voice") in an otherwise pure-black headline. Von Restorff isolation doing the brand's whole color job.
- **App-collage arc** — the "works inside the tools you already use" trope executed as a fanned diagonal of recognizable third-party icons; a positioning device, not an interface pattern.

## Defects

- None assignable. **No UI surface exists to audit** — running the 14-point rubric or 10-point native-tells audit would be fabrication. (Marketing's pure-`#000` headline is max-contrast display licence, not Contrast Dilution.)

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| (none — marketing cover + icon only) | n/a | No native macOS window supplied; nothing to score |
