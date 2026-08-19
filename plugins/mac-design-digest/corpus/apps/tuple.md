# Tuple — profile

- **Source:** macapp.supply (`cover.jpg`, SHA-1 `23b46164`) · **Surfaces digested:** 1 — marketing cover composite containing a partial in-session view · **Last updated:** 2026-07-19
- **One-sentence identity:** Figma-multiplayer's collaborator-color presence system applied to remote screen control — a native pair-programming HUD that humanizes a technical activity with pastel name pills and hand-drawn annotations.
- **Cluster:** unassigned (candidate: "friendly-pro presence tools")
- **Lineage:** native (low confidence) — Tuple is a known AppKit-native macOS + Windows app; the only genuinely-Tuple chrome visible (the floating annotation toolbar) reads native, but the input is a marketing composite, not a raw window capture, so lineage cannot be confirmed from pixels here.
- **Era (chrome):** custom / unknown — the visible Tuple surface is a floating HUD control bar, not standard window chrome; no glass, sidebar, or genuine traffic-light evidence to date it. No Liquid-Glass evidence either way — `(insufficient-evidence)`.

> **Provenance warning.** `cover.jpg` is a 1200×630 OG marketing card. The **left half** is pure brand evidence (wordmark, logo, headline on white). The **right half** is a stylized composite: a mocked remote macOS desktop (abstract Sequoia-style wallpaper, an Apple menu bar, a `PaidUsersList.tsx` code editor with real traffic lights) that represents *the guest's shared screen* — **not Tuple's own UI** — with Tuple's overlay layer drawn on top (annotation toolbar, participant name pills, remote cursors, freehand annotation). Only the overlay layer + the wordmark are Tuple design evidence. The outer window's traffic lights are stylized flat grey (illustration, not a real focused window). The app is rendered at an unknown marketing scale, so **no control size may be derived in points** from this image.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/primary (indigo) | `#5F52D5` (measured)(inferred) | | logo mark fill; violet-indigo, warmer/more saturated than system Blue `#0088FF` — an app brand hue, not the system accent |
| brand/logo-back-layer | `#CDC8F1` (measured)(inferred) | | pale lavender offset panel behind the indigo mark — the "two overlapping screens / pairing" depth device |
| brand/wordmark | "Tuple", heavy bold grotesque, near-black warm (~`#1C1C24`) (estimated)(inferred) | | tight, high-weight geometric-grotesque display face; not SF — a branded wordmark |
| brand/bg | `#FEFEFE` near-white (measured)(inferred) | | left marketing panel |
| identity/mike (blue) | fill `#D8EAF8`, label ~`#3E7CB1` (estimated)(inferred) | | participant pill: pale-blue tinted fill + saturated same-hue label |
| identity/paul (rust) | fill ~`#F6E7DC` peach, label ~`#BC5B3E` rust (estimated)(inferred) | | Paul's freehand annotation squiggle uses the same rust — per-person hue ties pill → cursor → annotation |
| identity/sarah (indigo) | fill `#D6D7F5`, label ~`#6E62D8` (estimated)(inferred) | | pale-lavender pill; note it echoes the brand indigo |
| badge/shape | capsule (radius = height/2), thin same-hue border, soft drop shadow (estimated)(inferred) | | floating-over-content elevation is legitimate — pills sit on the shared screen, not in a content pane |
| toolbar/tools | borderless monochrome grey glyphs (~`#8C8C8C`), ~6 items (estimated)(inferred) | | arrow · multi-cursor · hand-pointer · freehand-draw · "AI"/text · pen-in-stepper-pill |
| toolbar/selection | flat inset light-grey rounded-rect fill (radius ~6px at render scale) (estimated)(inferred) | | active tool (freehand-draw) highlighted — native selection grammar, not a saturated capsule |
| toolbar/pen-control | bordered rounded-rect pill with pen glyph + up/down stepper chevrons (measured)(inferred) | | reads as a pull-down/stepper group — one grouped control set apart from the free tools |

## Layout skeletons

**Marketing cover (1200×630).** Two-column split. Left column (~0–540px): logo mark + "Tuple" wordmark as a lockup near vertical center-top, then a 4-line headline in heavy grotesque ("The best remote pair programming app on macOS and Windows"), left-aligned, generous leading, on near-white. Right column (~560–1200px, bleeds off the right edge): a rounded app window, cropped. Top strip = Tuple's floating annotation toolbar (trailing-aligned tool cluster). Body = the shared remote screen (menu bar + wallpaper + a centered `PaidUsersList.tsx` code editor, lines 1–18). Tuple overlay drawn over the body: three participant name pills (Mike top-right, Paul mid, Sarah lower) pinned to their live cursor/I-beam positions, plus one rust freehand underline annotation on code line 6.

**Genuine Tuple surface (the overlay system).** A HUD, not a window: (1) a trailing floating toolbar of monochrome annotation tools with one active-tool highlight and one grouped stepper control; (2) a presence layer of capsule name-pills + colored remote cursors + freehand ink, all keyed to a per-participant hue.

## Signature moves
- **[GOLDEN-NUGGET] Per-participant identity color as a whole-cloth presence system.** Each collaborator owns one pastel hue that binds their name pill, their live cursor/I-beam, and their freehand annotations into a single legible identity — Paul's rust squiggle under line 6 reads as *Paul's* before you read the name. Presence is made pre-attentively locatable (Von Restorff): you find "who is where" by color, then confirm by label. This is the app's entire character in one decision — it turns cold remote-control into visible co-presence. Peer: Figma multiplayer cursors; the choice to soften the hues to pastel tints (not saturated) is what makes a pro dev tool feel human.
- **Freehand annotation over live screen as a first-class tool.** The toolbar's selected mode is the scribble/draw tool, and the composite foregrounds a hand-drawn underline — pointing at code by *drawing on it* rather than by moving a shared cursor. Humanizes the act of "look here."

## Defects
- **Contrast Dilution risk (low confidence, marketing render) — same-hue tinted pills.** Each name pill pairs a pale tint fill with a saturated *same-hue* label (rust-on-peach, blue-on-pale-blue). Rust-on-peach and blue-on-pale-blue plausibly fall below the 4.5:1 text floor. Mitigated in-product by the label always co-existing with a distinct cursor position, and color is never the *sole* signal (the name text is present) — so this is a WCAG-contrast note, not a color-alone failure. Verify against real in-app colors before treating as canon.
- **Not a product defect — flagged for honesty:** the outer window's flat grey traffic lights are marketing illustration, not a genuine focused-window frame. The real product's chrome was not shown.

## Rubric history
| Surface | Score | Failures / n-a |
|---|---|---|
| cover composite (Tuple overlay UI) | 7/14 passable, low-confidence | #9 text-contrast borderline (same-hue pills); #4–6, #12–14 **n/a** (no body copy, inputs, or focus states in the overlay UI); #1 grid **n/a** (unknown marketing scale) |

**Native-tells audit (Tuple overlay):** 6/10 clear passes, 4 n/a. PASS: #2 no glass abuse (opaque HUD), #3 selection = flat inset rounded fill (not saturated capsule), #6 identity colors correctly separated from a single accent (12-hue-style per-person palette), #7 one active tool per view, #9 toolbar = borderless grouped monochrome symbols. PARTIAL: #1 lineage native (low conf — composite), #10 real chrome (outer frame is faked illustration). N/A: #4 sidebar headers, #5 density-in-pt, #8 concentric corners (unverifiable at this scale).
