# Icon: AgentPeek

- **Era:** Big Sur unified (front-facing squircle, flat matte glyph, baked soft drop-shadow — **not** Liquid Glass) · **Rubric:** 10/12 (2 failures, 2 soft passes) · **Digested:** 2026-07-19
- **Source:** macapp.supply web renders. `icon.webp` is 102×102px **with a transparent background** (the glyph-only cutout / foreground layer, not the tile). The shipped composition — white squircle tile + black glyph — is only legible from `cover.jpg` (icon rendered ~165px, JPEG-compressed). No 1024 master; all hex/geometry `(estimated)` from small renders.

| Dimension | Reading |
|---|---|
| Background | Flat **pure white** `#FFFFFF` squircle tile (read from cover; the webp itself ships the glyph on transparency). No ramp, no vignette, no texture (estimated) |
| Glyph | **Mascot** — the MacBook **notch given a face**. A flat black `#000000` body: a wide flat top bar with two rounded horizontal flanges (the notch's "shoulders") dropping into a rounded U/bell. Inside sit two white knockout **cartoon eyes** (`#FFFFFF` ovals) with dark pupils, tiny sparkle highlights, and thin arched eyebrows — a "peeking" expression. Optically near-centre; visual mass sits slightly low (bell body) while the flanges reach wide toward the safe-zone edges (estimated) |
| Overlay device | None — single centred character, no diagonal tool, no badge, no frame |
| Light model | Soft ambient / top-down: one diffuse **gray drop-shadow halo** (`~#8C8C93`) rings the black glyph and lifts it off the white tile; eye sparkles imply an upper light; the glyph body itself is flat, unshaded black (estimated) |
| Layer stack | white squircle tile → soft gray ambient drop-shadow → black notch-body glyph → white knockout eyes → dark pupils + sparkle highlights + eyebrow arcs (front) |
| Palette economy | **Achromatic** — 0 hue families. Black glyph + white ground/eyes + one gray shadow. No accent, no saturation anywhere. Maximal figure-ground (~21:1) by monochrome default rather than reserved-accent discipline |

## Signature devices
- **Notch-as-mascot** — the app's whole subject (it lives in the MacBook notch: *"your coding agents, in the Mac notch"*) *is* the icon. The literal notch silhouette is personified rather than an abstract glyph drawn about it. Subject-mining taken all the way to the literal object. `[GOLDEN-NUGGET]`
- **Negative-space googly eyes** — the face is built entirely from white knockouts in the black body (pupils + pinpoint sparkle highlights + thin eyebrow arcs), giving a deadpan "peeking" character with zero added color. The personality budget is spent on two eyes and nothing else.
- **Baked soft-shadow lift** — a single diffuse gray halo does all the depth work; the icon is otherwise perfectly flat. Big-Sur-era habit (a shadow the Liquid Glass system would rather apply itself).

## Failures
- **#3 silhouette test** — the identity is carried by the *white knockout eyes*, which vanish when the shape is filled solid black. The bare silhouette is an ambiguous notch/anvil/bell blob, not instantly nameable as a creature. The character dies in silhouette because its face is negative space, not separate shapes.
- **#10 variant robustness** — the composition is wholly dependent on the white ground: a black glyph with white-knockout eyes only works over white. There is no authored layered/appearance-aware construction, so macOS 26 Dark / Clear / Tinted renders would collapse it (black glyph on a dark or tinted ground disappears; the eyes need a black fill under them). Not forward-compatible with Liquid Glass tinting without an invert/redesign.

## Soft passes (borderline — scored pass, flagged for synthesis)
- **#2 grid adherence** — reads centred, but the visual mass is bottom-heavy (bell body) while the top flanges push wide toward the safe zone. Optically acceptable, not textbook-centred.
- **#4 16px squint** — the high-contrast black-on-white silhouette survives to menu-bar size, but the eye detail (pupils, sparkles, eyebrows) smears below ~32px into "a blob with two dots." The face-in-notch reading holds enough to pass because the app itself lives in the notch, so a tiny face there is on-brand.

## Rhymes with
- *(hint only)* Flat **monochrome mascot** icons where a UI element or object is personified with cartoon eyes — the "cute creature peeking" family rather than the diagonal-tool (TextEdit/Preview) or concentric-badge (1Password) families. Also rhymes with black-glyph-on-white menu-bar/notch utility marks. A face-in-negative-space, achromatic, subject-literal icon. Confirm against future digests before clustering.

## Provenance / caveats
- All hex `(estimated)` from ≤165px renders; `(inferred)` — single icon, single source.
- The webp's transparent background means it *might* be authored as a separate foreground layer (weak positive signal toward layered construction) — but no dark/tinted variant is shown, and the white ground is essential to the reading, so #10 still fails on evidence.
- Mask corner radius unmeasurable at this resolution.
- **Brand-coherence with `cover.jpg`:** strong and deliberate. The cover reuses the exact icon (same black notch-face) on the same white tile, floats it over a **black→silver liquid-metal blurred field**, and sets the wordmark "AgentPeek" in a white SF-style sans. The cover's grayscale palette (`#0A0A0C` black → `#9B9EA5` silver) is the icon's monochrome extended into an environment — the whole brand commits to achromatic. The one thing the icon does *not* borrow from the cover is that metallic ground; the icon stays flat white.
- **Era-lag note for synthesis:** like 1Password, AgentPeek ships a flat Big-Sur-era icon in the Liquid Glass era — more evidence that shipping third-party dev/utility icons lag the current icon language.
