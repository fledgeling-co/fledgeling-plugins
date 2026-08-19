# WallTune — profile

- **Source:** macapp.supply · **Surfaces digested:** 1 (cover marketing composite containing the app window — immersive media browser, dark) · **Last updated:** 2026-07-19
- **One-sentence identity:** Apple TV app's cinematic "art-is-the-interface" featured hero, transplanted onto a wallpaper gallery whose one differentiating hook is that the background follows your Focus Mode.
- **Cluster:** unassigned (candidate: *immersive-media-gallery* — consumer personalization utilities where content art fills the frame and chrome recedes)
- **Lineage:** native (**low** confidence) — real macOS traffic-light frame, but the body is *custom immersive chrome* (no standard toolbar, floating capsule control bar) that a single marketing render cannot separate from a well-built Electron media app. Non-native evidence excluded from macOS canon regardless.
- **Era (chrome):** liquid-glass-adjacent / modern (med) — floating dark translucent capsule bar and capsule controls read as the macOS 26 idiom, but sitting on a bespoke content layer, so glass-discipline can't be strictly audited.

> **Evidence caveat (load-bearing):** this is a **marketing cover**, not a real screenshot. The left half (wordmark, serif-italic headline, terracotta gradient, "Download for free" ghost button) is **brand evidence**; the right-half window is genuine app-UI evidence but is **scaled down** inside the composite, so all absolute pt values are `(estimated)` with wide ranges and the proportional readings (selection colour, hierarchy ladder, layout topology) are more trustworthy than the numbers. The floating **"Gaming / Active" pill** is a *composited* stylised system notification (light material over the dark window), not a real element of the app window — it illustrates the Focus-Mode hook.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/brand-canvas | `#1A1A1A` near-black | (measured)(inferred) | marketing backdrop; app window content is full-bleed art, so its own base bg is not independently visible |
| brand/warm-gradient | terracotta `#A6643C` rising into black | (measured)(inferred) | brand backdrop only — NOT app chrome; do not read as a window material |
| accent/system-blue | `~#0C7DFE` ≈ system Blue (kit `#0088FF`/`#0091FF`) | (measured)(inferred) | on the Focus switch track + "Active" label; the app's *system-integration* accent |
| label/active-tint | `~#7FAAF3` blue | (measured)(inferred) | "Active" subtitle on the Focus pill |
| selection/in-app | pure-white capsule fill, dark text | (estimated)(inferred) | segmented "Videos" selected — **not** accent-tinted (see Signature) |
| control/segmented-track | dark translucent capsule, `~#26333F` | (estimated)(inferred) | floating bottom-right bar |
| radius/media-card | `~10–12px` relative | (estimated)(inferred) | grid thumbnails |
| radius/floating-bar | capsule (height/2) | (estimated)(inferred) | search + segmented bar |
| radius/window | rounded, small–medium; concentric stepping unverifiable | (estimated)(inferred) | top-left corner visible over content |
| type/eyebrow | tracked UPPERCASE micro-label ("FEATURED"), tertiary white | (estimated)(inferred) | hero eyebrow — media-app idiom, not a sidebar header |
| type/hero-title | large bold sans ("Jinx") | (estimated)(inferred) | primary label |
| type/metadata | small secondary, mid-dot separated ("by WallTune · 1,920 × 1,080") | (estimated)(inferred) | de-emphasised |
| chrome/window | full-bleed immersive; traffic lights float over content; **no standard toolbar** | (measured)(inferred) | genuine red/yellow/green cluster, correct order |
| control/pagination | dark capsule pill "1 / 8" + prev/next chevrons, bottom-right of hero | (estimated)(inferred) | carousel affordance |
| card/meta-overlay | source label ("WallTune") + like-count (♡ n) over art | (measured)(inferred) | community/popularity signal |
| brand/wordmark | lowercase "walltune", bold grotesk, icon at left | (measured) | marketing lockup |
| brand/headline | bold grotesk + **serif-italic accent** on "your focus." | (measured) | marketing only — editorial flourish, not in-app type |

## Layout skeletons

**App window — immersive media browser (dark):**
- **Featured hero** (top ~50–55% of window height): full-bleed video wallpaper; bottom-anchored dark gradient scrim carries a left-aligned stack — eyebrow ("FEATURED") → large title ("Jinx") → metadata ("by WallTune · 1,920 × 1,080"). Bottom-right of hero: pagination pill "1 / 8" with prev/next chevrons.
- **Card grid** (below hero): ~3-column rounded media cards (≈2.5 visible before right crop), each full-bleed thumbnail with a bottom overlay = source label + like-count. Even gutters (~16px relative), left edge shares the hero's left axis.
- **Floating control capsule** (bottom-right, over content): search-magnifier icon + Images/Videos segmented toggle, capsule-shaped dark translucent — a *floating* bar, not a docked bottom strip.
- No sidebar, no visible top toolbar — navigation/scope live entirely in the floating capsule.

## Signature moves
- **Interface-disappears immersion:** the wallpaper art *is* the entire canvas; chrome is distilled to one floating capsule plus a bottom gradient scrim. Systematic and purposeful for a personalization tool whose whole value is visual — this is the app's character, closest peer being Apple's TV/Music immersive featured views.
- **White-not-accent selection:** the selected segment ("Videos") is a neutral **white** capsule rather than an accent-tinted fill. On a dark art canvas, white is the highest-contrast neutral and it *reserves the accent budget* for the art and the single blue system-integration moment. Reads as a deliberate house rule (echoes the white "Download for free" ghost button), not a defect — but it is a real deviation from native selection grammar, so it does not feed macOS canon.
- **Focus-Mode binding as the soul:** the composited "Gaming / Active" pill states the product thesis — the wallpaper reacts to macOS Focus Mode. The one place the boldness budget is spent (system blue) is the feature that differentiates the app.

## Defects
- **Native-tells deviation — scope in a floating bar, not the toolbar:** Images/Videos is a bottom floating segmented control; HIG puts in-view scope in the toolbar. Systematic + genre-appropriate (immersive media apps legitimately float controls), so recorded as a native-fidelity deviation, not a taxonomy anti-pattern — but it lowers the native-tells score.
- **Selection not accent-bound** (native-tells #3/#6): see Signature — deliberate, but a genuine departure from the native selection/accent grammar.
- **Contrast risk (estimated):** dim "by WallTune" metadata and the dark segmented track sit over bright/busy art in places → possible UI-contrast <3:1 and text-contrast dilution at those spots. Cannot be verified on a scaled marketing render; flag, don't assert.
- **Tracked-UPPERCASE "FEATURED" eyebrow:** a web/marketing tell under the native grammar's sidebar-header rule — but this is a hero eyebrow, which Apple's own media apps use; a note, not a defect.

## Rubric history
| Surface | Score | Failures / notes |
|---|---|---|
| App window (immersive media browser, dark) | ~10/14 (estimated) | #9 text-contrast (dim metadata over art — risk, est.) · #10 UI-contrast (dark track over bright art — risk, est.) · #5/#6/#12/#13/#14 n/a (no running text, no text inputs, no visible focus state) · #1–#4,#7,#8 pass on proportional evidence |
| Native-tells | ~4/10 (heavy uncertainty) | Pass: #2 glass on floating chrome / content opaque (est), #7 one prominent action, #10 genuine traffic lights, #8 corners (est). Fail-as-native: #3 selection not accent fill, #9 scope not in toolbar. Unknown: #1 lineage (custom chrome), #4 headers (no sidebar; tracked-caps eyebrow present), #5 density (scaled render), #6 accent binding (split: blue for system-integration, white in-app). **Caveat:** on an intentionally immersive media app several "fails" are legitimate genre deviations — the score understates the app's polish. |
