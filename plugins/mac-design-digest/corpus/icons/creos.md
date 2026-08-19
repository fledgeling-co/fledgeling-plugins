# Icon: CREOS

- **Era:** Custom (3D chrome-emblem render; quotes skeuomorphic *material*, not the Mac skeuomorphic era) · **Rubric:** 9/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/creos/icon.png`, 512×512, alpha) · **Category:** Productivity · **App:** "a second brain for creators — saves in, content out"

| Dimension | Reading |
|---|---|
| Background | Flat pure black — `#000000` field with faint `#050505` render noise; delivered as a pre-masked rounded-rect inset ~10% on transparency |
| Glyph | Abstract emblem reading as an angular checkmark / **C-monogram** fused with a tapering blade; full-grayscale polished chrome, optically centred in the black field, slight diagonal (lower-left → upper-right) bias from the blade |
| Overlay device | None — the emblem *is* the whole subject; no tool crossing the field |
| Light model | Environmental studio lighting, key from upper-left; photoreal reflective chrome with blown-out `#FFFFFF` specular edges and a faint **mirror-floor reflection** beneath the glyph. Not the flat top-down bake of Big Sur, not Liquid Glass's system specular — a bespoke 3D render |
| Layer stack | (back→front) 1. black squircle field · 2. mirror-floor reflection of glyph · 3. chrome 3D body (beveled hollow loop + tapering blade + top lightning-spike terminal) · 4. baked edge/specular highlights |
| Palette economy | One "hue" family only — none. Fully desaturated: black void + grayscale chrome ramp `#2A2A2A → #939393 → #E8E8E8 → #FFFFFF`. Zero accent; contrast >10:1 |

## Signature devices
- **Polished-chrome 3D emblem** — photoreal reflective metal, the single committed move; automotive-marque / crypto-token register, executed fully (bevels, refraction on inner faces, blown specular).
- **Mirror-floor reflection** — the glyph reflected on the black floor beneath it, gradient-faded. A 3D-render / web-graphic depth device rather than a baked Mac micro-shadow.
- **Pure-black void field** — maximises chrome pop; the black *is* the material's whole context, which is also its variant-robustness weakness (see Failures).
- **Ambiguous-but-distinctive form** — hollow angular loop + long tapering blade + lightning-spike terminal; reads as checkmark, "C", and chevron at once. Personality is high; nameability is soft.

## Failures
- **#1 Mask discipline (FAIL):** asset ships as a black rounded-rect *baked* on transparency, inset ~10% with its own corner radius (first opaque pixel at x≈50/512) — not full-bleed square art for the system to mask. Squircle-in-squircle / corner-mismatch risk on macOS 26. *(Caveat: partly attributable to a macapp.supply pre-render — see notes.)*
- **#4 16px squint test (FAIL):** at 16px the chrome bevels and hollow centre collapse to a muddy light blob; micro-highlights become noise. Reads acceptably at 32px, fails at menu-bar/Spotlight size. Both #1 and #4 sit in the non-negotiable 1–4 band.
- **#10 Variant robustness (FAIL):** composition depends entirely on the pure-black background for the chrome to read; there is no Icon Composer layer structure and no tint-safe glyph. Would collapse in light / clear / tinted renders — a chrome-on-black bitmap cannot retint.

## Soft passes (flagged for synthesis)
- **#3 Silhouette:** filled solid, the form is nameable but tri-stable (checkmark / C / chevron) — distinctive yet not instantly one thing.
- **#8 Depth coherence:** internally coherent, but the mirror-floor reflection is a render device, not a Mac-native baked shadow.
- **#9 Era coherence:** all devices belong to one language (chrome-emblem render) so it is *internally* consistent — but that language is off-platform for a macOS icon; it quotes no Mac era.

## Subject & brand coherence
- **Subject communication (weak):** the app is a creator "second brain" (save clips in, content out). The icon communicates *none* of that — it reads as a luxury marque / approval checkmark. Committed direction, absent subject-mining.
- **Brand coherence (strong):** the cover pairs this exact chrome glyph (small) with a white bold rounded-sans "CREOS" wordmark on near-black. Black + chrome + white is the real identity; the icon renders it faithfully.

## Rhymes with
- Off-corpus family: **chrome 3D emblem / metallic-on-black logo renders** — crypto & web3 token marks, gaming-clan crests, automotive marque badges, 3D-rendered SaaS logos. Does not rhyme with any Mac-native icon era. Nearest in-corpus neighbours would be any other dark-field metallic icons (candidate for a "metallic-void" micro-cluster if ≥3 accumulate).
