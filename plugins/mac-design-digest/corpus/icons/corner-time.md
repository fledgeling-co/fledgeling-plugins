# Icon: Corner Time

- **Era:** Big Sur unified (front-facing squircle, top-down light, no glass) · **Rubric:** 9/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`sources/corner-time/icon.png`, SHA-1 `02e07538`) · **Category:** Utility
- **What the app does:** always-visible corner clock for fullscreen / hidden-menu-bar. The icon depicts exactly that — subject communication is total and literal.

| Dimension | Reading |
|---|---|
| Background | Silver body **ramp #EAEAEA → #D2D2D2** (measured), vertical, light-under-bar → darker-at-base; flat left-to-right (#E0E0E0 across, measured) |
| Glyph | **Scene**, not a glyph: a depicted screen. Full-bleed black menu-bar band (`#0A0100` ≈ #000000, measured) spanning the squircle top; white `09:41` numerals (`#FFFFFF`, measured) pinned top-right of the band |
| Overlay device | None — the clock is baked into the scene, not a tool/badge/frame crossing a separate field |
| Light model | Soft top-down; subtle vertical luminance ramp on the body; flat black header (no lighting); **no specular / refraction / translucency**; short baked drop shadow under the squircle (render composite) |
| Layer stack | back → front: silver body ramp → black menu-bar band (top, full-bleed) → white `09:41` numerals (top-right) · plus baked squircle mask + drop shadow at composite level |
| Palette economy | **Zero hue** — pure greyscale (black / white / silver ramp). No saturated accent anywhere. Economical to the point of austerity |

## Signature devices

- **Self-referential product depiction** `[GOLDEN-NUGGET]` — the icon *is* the app's on-screen output: a screen showing a corner clock. Nameable, honest, on-the-nose. The committed idea; the personality lives entirely here.
- **Full-bleed field** — art bleeds to the mask edge; the whole squircle reads as a display, the black band following the top curve. No inset background field + centred glyph (breaks the Big-Sur "tool-on-a-field" convention deliberately).
- **Corner-anchored clock** — the numerals sit in the top-right corner, echoing both the app name ("Corner Time") and its function. Intentional asymmetry.

## Failures

- **#3 Silhouette test — FAIL.** Filled solid black, the icon is a featureless squircle. Subject is carried entirely by internal light/dark contrast (black band vs silver body), zero shape identity. Nothing nameable survives a solid-black fill.
- **#10 Variant robustness — FAIL.** A fixed greyscale render (no Icon Composer layers). A hard black band + white numerals over silver body gives tinted/clear modes nothing to grab; monochrome art with a fixed dark region won't adapt gracefully to dark/tinted appearances.
- **#12 No-text check — FAIL.** Contains baked literal numerals `09:41` (Apple's canonical demo time) and is essentially a UI/menu-bar depiction — both are explicit no-text-check violations. The numerals *are* the subject, but the rubric is strict: text in an icon smears and here doubles as a UI screenshot.

## Soft passes (flag, not fail)

- **#1 Mask discipline (soft).** Composition is designed for the squircle and fights nothing — but the PNG ships a **baked-in squircle mask** (alpha-0 corners) **+ baked drop shadow**, i.e. an iOS/web-render composite, not the unmasked square layers macOS 26 / Icon Composer expects. Can't tell whether the source authored it correctly or only this render is composited.
- **#2 Grid adherence (soft).** No centred glyph to grid — it's a full-bleed field, so safe-zone logic applies to the field (clean). But the mark is **top-heavy and right-weighted** (dark band + corner numerals up top, empty silver below); optical centre of mass sits high.
- **#4 16px squint test (soft).** The dark-band-on-light-body gestalt survives at menu-bar size and stays distinguishable in the Dock — but the `09:41` digits, the actual subject, smear to an illegible speck. The icon reads as "a card with a dark title bar," not "a clock," when small.

## Passing checks (evidence)

- **#5 Single light model** — one soft top-down ramp across the body; no mixed lighting.
- **#6 Palette economy** — greyscale only, ≤2 "hue" families trivially (zero hue); no competing accents.
- **#7 Figure-ground contrast** — black band vs white numerals ≈ 21:1; band vs silver body high; survives grayscale (it is grayscale).
- **#8 Depth coherence** — layers ordered sensibly (body → band → text); baked shadow consistent with top-down light; near-flat but non-conflicting.
- **#9 Era coherence** — consistent Big-Sur-unified language throughout (squircle, front-facing, subtle top-down gradient). No era-mixing. Flag: it does **not** adopt Liquid Glass, so reads slightly dated on macOS 26.
- **#11 Personality** — the self-referential depiction is a genuine nameable device; not a generic glyph-on-gradient.

## Aesthetic read (direction vocabulary)

A **committed idea executed at template fidelity**. The idea — "draw the app's own output as the icon" — is a real, subject-mined choice (literal utility honesty). The execution is anonymous: no accent, no material craft, no craft in the ramp; it reads as a competent placeholder render rather than a lovingly-built mark. Committed adjectives: **literal, austere, monochrome**. This is the austere end of Swiss reduction (near-white, near-black, no colour) collided with a literal-UI utility metaphor — decisive about *what* to show, indifferent about *how*.

## Brand coherence note

The app cover (`cover.png`) is Sonoma-blue wallpaper + cyan `Corner Time` wordmark; the settings window is dark-mode blue. The **icon carries none of that blue** — pure greyscale. Icon↔brand palette are incoherent: the icon could belong to any monochrome utility. A single restrained accent (e.g. tinting the band or a coloured clock) would tie it to the brand and give tinted-mode something to work with.

## Rhymes with

- Monochrome / greyscale utility icons (menu-bar tools, screenshot/display utilities) — style family: **austere greyscale utility, Big-Sur-era, literal-UI-depiction**.
- Hint only — no other icons digested yet; revisit when a second monochrome-utility or literal-product-depiction icon lands to test whether "self-referential UI depiction" is a recurring device.
