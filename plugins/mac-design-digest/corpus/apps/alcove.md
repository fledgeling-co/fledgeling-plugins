# Alcove — profile

- **Source:** macapp.supply (`tryalcove.com`) · **Surfaces digested:** collapsed notch island, "locked" state (1 surface, 1 state, from marketing cover) · **Last updated:** 2026-07-19
- **One-sentence identity:** The iPhone Dynamic Island transplanted onto the MacBook notch — a true-black bezel-merging island in the register of NotchNook / DynamicLake / Boring Notch, not a native-chrome Mac app.
- **Cluster:** unassigned — opens a candidate "notch-island / iOS-transplant utility" cluster (sole member; mostly excluded from macOS canon, see Lineage).
- **Lineage:** native (med) — the *runtime* is almost certainly a native borderless-overlay utility (the notch-island category is native-Swift-dominated; a bezel-merged always-on-top notch overlay is not an Electron idiom). BUT the **visible surface uses zero native macOS controls or chrome by explicit intent** — it is bespoke iOS Dynamic Island trade dress. Per the lineage gate, this visible grammar (true-black capsule, iOS island shape, no system accent) is recorded as tells + corrections and **never feeds macOS canon or native clusters**.
- **Era (chrome):** custom — not Liquid Glass, not native chrome. True-black opaque material (iOS OLED / Dynamic Island philosophy) chosen to fuse software with the physical black notch/bezel, not the macOS-27 lensing-glass material.

> **Evidence caveat:** the only app UI is the window *inside a marketing composite* (`cover.png`, 2400×1260) — a stylized product render, not a captured screenshot. Scale is unknowable, so all island metrics are ratios/estimates at low confidence. Everything outside the device frame (cream backdrop, headline, pink highlighter, "Mac" badge, icon+wordmark lockup) is **brand evidence** and is kept separate from app-UI tokens below.

## Tokens

### App UI — the notch island (all `(estimated)(inferred)` — single stylized render)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| island/fill | true black ~#080808, opaque | (estimated)(inferred) | Not Liquid Glass; iOS Dynamic Island true-black to merge with the physical notch/bezel |
| island/shape | rounded-rect, aspect ~3:1 (w:h) | (estimated)(inferred) | Collapsed/compact state; visually echoes iPhone's ~126×37pt collapsed island proportion |
| island/radius | ~0.28–0.32 × height (rounded-rect, **not** full capsule) | (estimated)(inferred) | Corners read softer than a native search-field capsule but short of height/2 |
| island/glyph | white monochrome SF Symbol (`lock.fill`), left-inset | (estimated)(inferred) | Single status glyph; screen-locked / privacy state |
| island/glyph-color | #FFFFFF | (estimated)(inferred) | Monochrome; **no system accent used** — a non-native choice (see Defects) |
| island/position | centered at screen top, floating just below the top edge in the notch zone | (estimated)(inferred) | Occupies the menu-bar/notch region — the product premise |

### Brand (marketing composite — NOT app-UI tokens, kept separate)
| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/backdrop | warm cream ~#FBEFE0 | (estimated)(inferred) | Product-launch register, not the app surface |
| brand/headline | bold grotesk (Helvetica Now / SF Pro Display Bold class), near-black ~#1A1A1A | (estimated)(inferred) | Apple-keynote-mimetic typography |
| brand/highlight | pink marker-swipe ~#F7B8C4 behind "Mac" | (estimated)(inferred) | Highlighter emphasis device |
| brand/badge | "🍎 Mac" pill on cream, ~#F1E6D6 fill | (estimated)(inferred) | Platform badge |
| icon/aura-gradient | vertical indigo→magenta→pink (~#5B2A9E → ~#A03BC8 → ~#F0A6D8) inside a thick black squircle bezel | (estimated)(inferred) | The icon depicts the product: a display bezel glowing from within (the island's content aura). Rhymes with the app's purple wallpaper and the pink headline highlight |

## Layout skeletons

**Collapsed notch island (cover.png):** desktop wallpaper fills the frame (macOS Monterey purple/indigo gradient — the *user's desktop*, not app chrome). A single true-black rounded-rect island floats horizontally-centered at the top edge, in the notch zone. Interior: one white status glyph, left-aligned within the island's left inset; remaining island width is empty (reserved for the expanded/live-activity content this collapsed state hides). No traffic lights, no toolbar, no sidebar, no window frame — the island is the entire visible app.

## Signature moves
- **[GOLDEN-NUGGET] The whole app is one signature: import the iPhone Dynamic Island onto the Mac notch.** The load-bearing decision is the *true-black opaque* material — the island fuses with the physical black notch/display bezel so hardware and software read as a single continuous object (Gestalt figure-ground closure). This is the exact perceptual trick iPhone uses with its OLED cutout; Alcove borrows both the material and the collapsed-island proportion (~3:1). Everything else (the lock glyph, the compact state) is in service of that illusion.
- **[GOLDEN-NUGGET] The icon is the product, literally.** A thick black rounded-square bezel enclosing a vertical purple→magenta→pink glow — an abstraction of the display bezel lit from within by the island's content. The app's own overlay becomes its brand mark; the aura hue is reused as the marketing highlight and demo wallpaper for one coherent identity.

## Defects
- **Deliberate non-native surface (signature, not anti-pattern) — excluded from macOS canon.** By HIG `branding.md` / `the-menu-bar.md` the letter of the law is violated: custom UI occupies the menu-bar/notch zone, the user's chosen accent color is ignored (monochrome white glyph), and no native control grammar is used. Per defect-vs-signature (persona §2.3) this is *systematic + purposeful + accessible* and is the category convention for notch utilities → recorded as a **signature move**, but its grammar must never be learned as "mac taste."
- **Accent binding absent.** The island ignores `controlAccentColor`. Defensible for a true-black island (a tint would break the bezel-merge), but noted as the one place a native reading would differ.
- **Evidence poverty (not the app's fault):** one surface, one state, from a marketing render — grid adherence, real pt sizes, expanded/live states, dark-vs-light-desktop behavior, and any settings/onboarding surface are all unseen. The bezel-merge illusion is sold against a dark purple wallpaper; its robustness on a light desktop is unknown.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| collapsed notch island (light-composite) | 4/4 applicable (10 of 14 N/A — single-element surface) | Applicable checks pass: #8 action singularity (one glyph), #9/#10 contrast (white on true-black >15:1), #11 Fitts (large island target). N/A: #1–#7, #12–#14 (no grid reference, no type, no inputs, no multi-element hierarchy in a marketing render) |
| — native-tells audit | 1/10 (mostly N/A — intentionally non-native) | #1 native lineage unconfirmable from surface · #2 no glass, true-black overlay (custom) · #5 not native density (iOS island) · #6 no system-accent binding · #10 custom overlay occupies system chrome zone by design. #3/#4/#8/#9 N/A (no selection/sidebar/nesting/toolbar). #7 trivially passes |
