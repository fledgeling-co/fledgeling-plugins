# DriveMosaic — profile

- **Source:** macapp.supply · **Surfaces digested:** cover.png (marketing composite — app main-window depiction + web hero) · **Last updated:** 2026-07-19
- **One-sentence identity:** A DaisyDisk-genre treemap disk analyzer wearing the Linear/Vercel dark-hero costume — the disk drawn as a flush jewel-tile mosaic, but rendered (in marketing) in flat Tailwind-500 primaries rather than Apple's system palette.
- **Cluster:** unassigned (cluster hint: electric-dark-utility)
- **Lineage:** unknown (low) — the only UI artifact is a *drawn marketing depiction*, not a captured screenshot; it reveals no AppKit tells. Circumstantial evidence leans native-indie (a real macOS squircle app icon, single-platform "macOS 14+", $4.99 one-time — the indie-Mac-dev pattern; disk analyzers as a genre are overwhelmingly native: DaisyDisk, GrandPerspective). But the depicted palette is Tailwind and the chrome is recreated, so **nothing here may feed macOS canon** regardless.
- **Era (chrome):** unknown — the depiction is era-agnostic dark-flat: no Liquid Glass evidence (no glass, no scroll-edge effect, no capsule bezels), and no legacy-native tells (no hard 1px opaque dividers, no bezeled controls) either. There are almost no native controls to date it.

## Evidence provenance caveat (read first)

`cover.png` is a **1200×630 web OG composite**, not an app screenshot. It has two zones that must not be conflated:
- **Brand zone (left):** near-black hero backdrop, wordmark, a bold grotesk headline with a gradient-accent word, a muted body paragraph, and three web-style pills. This is *marketing/brand* evidence.
- **App-window depiction (right):** a drawn macOS window (traffic lights + centered title + treemap body). This is the *design evidence* — but it is a stylized rendering. Two proofs it is drawn, not captured: (1) the traffic-light hexes are dimmed approximations (`#E95750/#E8AC2A/#25B73B`) rather than Apple's exact `#FF5F57/#FEBC2E/#28C840`; (2) the tile palette is pixel-exact Tailwind-500. Treat window tokens as describing the *depiction*; the shipping app's real rendering is unconfirmed (and per the icon, likely different — see Defects).

## Tokens

### App-window depiction (treemap)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window | `#0B0B10`–`#0D0D13` near-black | (measured)(inferred) | window content + inter-tile gap colour; slight blue cast |
| chrome/titlebar | ~35px, Default style, centered title | (estimated)(inferred) | ≈ kit's 33pt Default titlebar — a competent recreation |
| chrome/traffic-lights | ~10px dots, ~16px pitch, ~46px cluster, inset ~11px | (estimated)(inferred) | **cluster ~46px vs kit 68×14** and dimmed hexes → drawn, not native |
| treemap/gap | ~2px, window-bg fill | (measured)(inferred) | uniform hairline gaps, H and V |
| treemap/tile-radius | ~6–8px | (estimated)(inferred) | softly rounded tiles |
| treemap/inset | 0px (full-bleed to window edge and to titlebar) | (measured)(inferred) | no content padding; tiles butt the titlebar |
| title/text | `#3D3D44` on `#0B0B10` ≈ 1.8:1 | (measured)(inferred) | **fails 4.5:1 — see Defects (Contrast Dilution)** |

### Treemap palette — exact Tailwind CSS 500 swatches (NOT Apple system colours)
| Tile | Value | Tailwind name | macOS-27 equivalent (kit) |
|---|---|---|---|
| indigo (largest) | `#6366F1` (measured) | indigo-500 | kit Indigo `#6155F5` — close but distinct |
| violet | `#8B5CF6` (measured) | violet-500 | — |
| purple | `#A855F7` (measured) | purple-500 | kit Purple `#CB30E0` |
| pink | `#EC4899` (measured) | pink-500 | kit Pink `#FF2D55` |
| red | `#EF4444` (measured) | red-500 | kit Red `#FF383C` |
| orange | `#F97316` (measured) | orange-500 | kit Orange `#FF8D28` |
| yellow | `#EAB308` (measured) | yellow-500 | kit Yellow `#FFCC00` |
| green | `#22C55E` (measured) | green-500 | kit Green `#34C759` |
| teal | `#14B8A6` (measured) | teal-500 | kit Teal `#00C3D0` |
| blue | `#3B82F6` (measured) | blue-500 | kit Blue `#0088FF` |

10/10 tiles are pixel-exact Tailwind-500; **0/10** match the Apple system palette. Decisive non-native colour tell. For a native mock, these would be sourced from the 12-hue system palette (per-item identity colours, like calendar dots / chart series) — legitimate as identity hues, but from the system set, not Tailwind.

### Brand zone (web hero — brand evidence, NOT app tokens)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/hero | `#0A0A0F` → `#0F0F1D` radial | (measured) | near-black + subtle indigo glow behind window |
| accent/gradient-word | indigo→violet (~`#6366F1`) | (estimated) | "eating your" set in accent within the headline |
| headline | heavy grotesk, ~52px, white | (estimated) | Inter/Geist-class |
| pill/pro | indigo-tinted fill `#271C43` bg / `#8B7FD6`-ish text | (measured) | "Pro — $4.99" |
| pill/onetime | emerald-tinted `#162B2D` bg / green text | (measured) | "One-time purchase" |
| pill/macos | zinc ghost, text `#71717A` | (measured) | "macOS 14+" |

## Layout skeletons

**cover.png — marketing composite (dark).** Two-column OG layout. Left column (~0–55%): vertical stack — wordmark (mosaic glyph + "DriveMosaic"), two-line headline, 3-line body, then a horizontal 3-pill CTA row. Right column (~55–95%): a floating macOS window, ~477×374px depiction. Window = Default titlebar (traffic lights leading, "DriveMosaic" centered) + full-bleed **squarified treemap** filling the content area: one dominant indigo block (~40% area, left, spanning the top two rows), a top strip (violet / pink / narrow orange), a middle strip (teal / blue), a bottom strip (green / purple / yellow / red). Tiles separated by ~2px near-black gaps; size encodes bytes. Zero content padding — the mosaic bleeds to every window edge including under the titlebar.

## Signature moves
- **[GOLDEN-NUGGET] Name-as-interface.** The product *is* its visualization: "DriveMosaic" → a literal mosaic of gap-separated, softly-rounded, jewel-saturated tiles sized by file weight, full-bleed to the window. The app icon repeats the exact same motif (a treemap in a squircle). Signature identity is total and self-consistent across icon + UI + name — the one memorable element is unmistakable.
- **Size-as-hierarchy done right.** Within the mosaic there is no colour de-emphasis (all tiles full-saturation) — and that is *correct*, not a Focal Collision: a treemap encodes magnitude in area, so the largest tile (indigo, ~40%) is the pre-attentive focal point and also literally "the biggest space hog." The visual peak equals the actionable insight. This is the app's whole job resolved in one geometry.

## Defects
- **Contrast Dilution** → window title `#3D3D44` on `#0B0B10` ≈ 1.8:1, effectively invisible → canon: macOS Default titlebar titles use primary-label (85% black / white); a dark-mode title wants secondary-label white `#FFFFFF`@55%, not near-black-on-near-black.
- **Non-Apple palette (tell, not a rubric anti-pattern)** → treemap is Tailwind-500 throughout → for macOS fidelity, identity hues come from the 12-hue system palette. Recorded as a tell + correction; excluded from canon.
- **Icon⇄cover palette contradiction (flag for synthesis)** → the *app icon* renders the same treemap in a **muted, hand-tuned, bevelled** palette (dusty mauve, sage, muted teal, olive, terracotta, tan, ochre — each tile with a soft top-edge highlight / matte fill), a genuinely tasteful painterly set. The *cover window* renders it in flat, maximally-saturated Tailwind primaries with no bevel. The two artifacts disagree on the product's actual look. Likely the cover is an idealized/quick marketing render and the real app is closer to the (more considered) icon — but from these two inputs alone it's unresolved. Bring a real screenshot to settle it.
- **Information-scent gap (UX, static)** → tiles carry colour identity but **no labels, sizes, or legend** → in the still you cannot tell *what* the big indigo block is (Pirolli & Card information scent); a disk analyzer lives on quickly reading which folder is the hog. Presumably resolved by hover/selection (out of static scope) — noted, not scored.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| cover — app-window depiction (dark) | 11/14 | #9 title contrast ≈1.8:1. (#4–6, #12–14 N/A — a treemap has no type ramp, paragraphs, inputs, or form labels; #1 grid N/A — tile sizes are data-driven by design.) |
| cover — native-tells audit | 3/10 | native #1 Tailwind palette (non-native); native #10 drawn traffic lights (dimmed hexes, ~46px cluster vs 68px kit). Most checks (selection, sidebar, toolbar, accent-binding, dialog grammar) N/A — no such surfaces present. |
