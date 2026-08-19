# Sero — profile

- **Source:** macapp.supply (cover.png marketing composite; no discrete screenshots supplied) · **Surfaces digested:** main window (three-pane reader + assistant), dark mode · **Last updated:** 2026-07-19
- **One-sentence identity:** A Raycast-dark, Linear-adjacent Electron/webview wrapper for local-AI document analysis — a three-pane "source list / light document card / assistant chat" reader whose polish is entirely of the web-SaaS idiom, not the Mac's.
- **Cluster:** unassigned → suggested non-native cluster `electron-ai-dark` (kept OUT of macOS canon)
- **Lineage:** web-electron (high) — judged from the body, not the frame; the traffic-light frame reads genuine but everything inside is web-component grammar
- **Era (chrome):** custom (app-drawn dark chrome mimicking current macOS dark, no native material system)

## Provenance / measurement caveat

The only asset is a **1200×630 marketing composite** (blue gradient backdrop, "Search with Zero Resistance" headline, "Download Sero" pill, floating AI-orb icon). The app **window** inside it is the design evidence; the backdrop/headline/pill are brand evidence. The window is rendered **below 1:1** inside the canvas — there is **no clean @2x**, so every pixel/pt value below is `(estimated)` with wide ranges and low precision. Colours are clean sRGB samples and are more trustworthy than the geometry.

## Lineage tells (why web-electron, high confidence)

Density can't be measured precisely here, so lineage rests on grammar, and the grammar is unambiguous:
1. **Brand wordmark "sero" in the toolbar top-left** — native toolbars carry borderless symbols, never an app wordmark.
2. **Two filled marketing pills in the toolbar** ("How it works" white-filled + "Open Document" blue-filled) — native toolbars use borderless monochrome SF Symbols with one trailing primary.
3. **In-app dark-mode toggle** (moon icon in toolbar) — native apps follow system appearance; an app-owned light/dark switch is a web tell.
4. **Tracked-UPPERCASE content section headers** ("STRENGTHS / ISSUES / RECOMMENDATIONS") — native uses sentence/title case. (The *sidebar* headers "Active"/"Recent" are correctly title-case — the one native-correct detail.)
5. **Colored-left-border callout cards with severity chips** (Critical / Major / Minor) — a web component-library pattern.
6. **iMessage-style right-aligned blue "sent" bubble** ("Find important sections") in the assistant pane — web chat mimicry.
7. **Light document card floating on a dark canvas** — a rendered-page-in-a-card, not a native content list/table.
8. **Composed titlebar with a status subtitle** (centered "…report.pdf" over "● Ready") — a custom web titlebar, not the native single-title toolbar.

Corpus treatment: profiled, but **non-native — its properties are recorded as tells + corrections and are excluded from macOS canon and native style clusters.**

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/chrome-toolbar | `#0E1012` (measured)(inferred) | | near-black toolbar |
| bg/sidebar | `#000000` (measured)(inferred) | | **pure black** — dark-mode anti-pattern (HIG: avoid pure black, use elevated grays) |
| bg/assistant-pane | `#1A1C1E` (measured)(inferred) | | third distinct dark value — no coherent single elevation ramp across the three panes |
| bg/document-card | `#FFFFFF` (measured)(inferred) | | pure-white light "page" on dark canvas; dark-gray body text |
| accent/primary | `#0A84FF` (measured)(inferred) | | system-blue-*adjacent* (Big Sur-era iOS blue), NOT the macOS 27 kit blue `#0091FF` dark; used as a brand colour across wordmark o-dot, both CTAs, chat bubble, selection |
| selection/sidebar-fill | `~#112D4B` navy translucent + faint blue border, blue label (measured)(inferred) | | custom bordered navy fill — NOT the native flat inset accent selection (visible border is the tell) |
| status/ready | green dot `~#30D158` + gray label (estimated)(inferred) | | status paired with glyph (correct) |
| severity/critical | pink chip on pink tint (estimated)(inferred) | | pink-on-pink text likely <4.5:1 |
| severity/major | orange chip on orange tint (estimated)(inferred) | | |
| severity/minor | yellow chip on yellow tint (estimated)(inferred) | | yellow-on-yellow text likely <4.5:1 |
| finding-bar/strengths | green vertical rule `~#34C759` (estimated)(inferred) | | |
| finding-bar/issues | orange vertical rule (estimated)(inferred) | | |
| finding-bar/recommendations | blue vertical rule (estimated)(inferred) | | |
| type/body | ~13–14px equiv, reads web-generous (estimated)(inferred) | | cannot confirm 13pt native body from downscaled composite |
| type/section-header | ~11px tracked uppercase, secondary gray (estimated)(inferred) | | web tell |
| radius/card | ~8–10px (estimated)(inferred) | | callout cards + chat bubble |
| radius/pill | capsule (estimated)(inferred) | | toolbar CTAs, sidebar selection, chat send |
| chrome/sidebar | ~210px wide, full-height, opaque (not vibrancy) (estimated)(inferred) | | narrower than kit's 256pt example; flat opaque, no material |

## Layout skeletons

**Main window — three-pane, dark.** Unified single-row toolbar (≈40–52pt-equiv): leading brand wordmark `sero` · centered document title with a `● Ready` status subtitle · trailing cluster of two filled pills (How it works / Open Document) + gear + dark-mode moon. Below, three columns:
- **Left source list (~210px):** title-case section headers `Active` / `Recent`; one selected row (navy bordered fill, blue label, doc glyph) under Active; three recent `.pdf` rows; a trash affordance in the Recent header. Pure-black background.
- **Center reader (flex):** a pure-white document card floated on the dark canvas, holding an analysis report — `STRENGTHS` (green rule, dot-bulleted cards, "· Aligns with:" metadata), `ISSUES` (orange rule, cards with Critical/Major/Minor chips, "· Violates:" metadata), `RECOMMENDATIONS` (blue rule).
- **Right assistant (~240px):** `Assistant` header + trash; a right-aligned blue user bubble; a dark structured response card ("Page N Highlights"); a bottom composer field "Ask about this document…" with a circular ↑ send.

## Signature moves
- **The dual "report card" language:** a UX audit rendered as colour-coded, left-ruled finding cards (green strengths / orange issues / blue recommendations) with Critical-Major-Minor severity chips, **mirrored** by the assistant's structured "Page N Highlights" text summary. It is a coherent, purposeful information design for surfacing an analysis — genuinely the app's character — but it is a *web* signature (component-library callouts + chat), not transferable mac taste.
- **AI-orb brand through-line:** the luminous blue→lavender ring of the app icon is echoed in the wordmark's glowing `o` — a small, consistent identity hook.
- Honest verdict: **competent-but-web.** A polished dark AI-assistant wrapper in the 2025 "dark neutral + electric blue" idiom; strong first-impression gloss, thoroughly non-native.

## Defects
- **Focal Collision** → two filled pills adjacent in the toolbar (white "How it works" + blue "Open Document") → canon: one filled primary per region, the other ghost/text.
- **Contrast Dilution (mild)** → severity chip text pink-on-pink / yellow-on-yellow (likely <4.5:1); "Aligns with / Violates" metadata not de-emphasized from body → canon: label tier to secondary, chips carry a glyph + ≥4.5:1 text.
- **Pure-black dark surfaces** → sidebar `#000000` and three unrelated dark values across panes → HIG dark-mode correction: avoid pure black, build one elevated tonal ramp.
- **Non-native selection** → bordered navy fill vs. the flat inset accent fill → native correction: flat inset rounded fill, accent-tinted label, no border.
- **Faint card borders** → ~1px near-white hairlines on the white document card likely <3:1 (#10).

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (dark) | 10/14 | #8 focal collision (2 filled toolbar pills); #9 severity-chip text contrast (pink/yellow on tint <4.5:1); #10 card-border contrast (~1px hairline <3:1); #6 marginal (content-doc lines ~75–85ch) |
| main window — native-tells audit | 3/10 | fails #1 lineage(web) · #2 no native material system · #3 bordered non-native selection · #5 web-generous density / marketing pills · #6 accent not system-bound (brand-splashed blue) · #7 two prominent actions · #9 toolbar wordmark+filled pills not borderless symbols. passes #4 (sidebar headers title-case) · #8 (no obvious concentric violation, soft) · #10 (genuine traffic lights) |
