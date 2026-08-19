# Notion — profile

- **Source:** macapp.supply (cover only; no dedicated UI shots) · **Surfaces digested:** 1 — main window (AI meeting-note view), light, shown in a marketing perspective render · **Last updated:** 2026-07-19
- **One-sentence identity:** A document-first workspace that deletes the platform's material system — Linear's structural calm and Craft's blank-page focus, but rendered in a deliberately accent-free monochrome with hand-drawn illustration warmth instead of native vibrancy.
- **Cluster:** unassigned (candidate: "monochrome-workspace" — neutral-canvas productivity)
- **Lineage:** web-electron (high) — publicly a React/Electron cross-platform app; tells corroborate (see below). **Non-native: contributes contrast evidence only, never macOS canon.**
- **Era (chrome):** custom (own web design language; no Liquid Glass, no Big Sur material ramp — flat white canvas with a real Electron window frame)

## Provenance caveat

The only app UI available is the app window composited into the marketing cover, **rendered in 3D perspective** (rotated, receding right). The window is not axis-aligned, so no clean pixel measurement or retina scale is recoverable. Every metric below is `(estimated)` with a wide range and is additionally softened by JPEG compression. Type sizes are relative reads, not absolute px. No settings/empty/onboarding/dark surfaces, no forms, no paragraph text — large parts of both rubrics are N/A for lack of surface content.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | `#FFFFFF` pure white (estimated)(inferred) | | content + sidebar both near-white; no tonal elevation between them |
| type/title | ~24–28px, bold, near-black (estimated)(inferred) | | "Stand-up" document title; humanist sans |
| type/body | ~15–16px web scale (estimated)(inferred) | | sidebar rows; **not** 13pt macOS body — a density tell |
| type/section-header | ~13px, semibold, mid-gray, **sentence case** (estimated)(inferred) | | "Meetings" / "Teamspaces" — NOT tracked uppercase (native-correct casing) |
| label/primary | near-black `#1A1A1A`-class (estimated)(inferred) | | selected/active text |
| label/secondary | mid-gray, ~50% (estimated)(inferred) | | "No upcoming events", icon labels |
| label/tertiary | light-gray, reads ~30% (estimated)(inferred) | | "View all", "@Today" mention — contrast-risk (see Defects) |
| accent/system | **absent** (inferred) | | no system-accent binding anywhere; selection is neutral gray, not tinted |
| color/status | tinted red — light-pink fill + red glyph/label (estimated)(inferred) | | "● Stop" record button; the only saturated action in view |
| select/fill | flat light-gray rounded fill, ~8–10px radius (estimated)(inferred) | | "Home" row and "Notes" tab share one selection grammar |
| radius/pill | ~8px soft rounded on selection + Stop button (estimated)(inferred) | | not full capsule; not the kit's capsule bezel |
| icon/style | monochrome line icons, uniform ~1.5px stroke (estimated)(confirmed) | | chat/calendar/inbox/search strip + row-leading glyphs |
| chrome/traffic-lights | monochrome **grey** dots (estimated)(inferred) | | inactive-window render or Notion's custom grey — not the colored cluster |
| chrome/sidebar | left source list, full-height, same white as content (estimated)(inferred) | | horizontal icon strip below "Home" is a web pattern, not native |

## Layout skeletons

**Main window (meeting-note view), light, perspective render**
- Left **source list** (own white, no vibrancy): header block = selected "Home" row (house glyph + label in gray pill) followed by a *horizontal* icon strip (chat, calendar, inbox, search) — a web navigation pattern, not the native vertical source list. Below: labeled sections "Meetings" (items: No upcoming events / New AI meeting note / View all) and "Teamspaces" (Company OS), each row = leading line-icon + label, generous row height.
- **Content area**: document title "Stand-up @Today" (bold black + gray mention). Inline sub-toolbar = a three-item tab group (Summary / **Notes** selected / Transcript, each icon+label), then an audio waveform, a pause glyph, a tinted-red "Stop" button, and a "…" overflow — an in-content AI recording bar.
- **Content top-right cluster** (from full cover): "…1d ago" · stacked collaborator avatars · "Share" text button · comment glyph · star glyph · "…" overflow.
- Alignment: sidebar and content resolve to clean left axes; grouping via labeled sections with proximity (header sits nearer its own items; larger gap before the next section).

## Signature moves

- **[GOLDEN-NUGGET] Grayscale-except-for-meaning.** The entire interface is monochrome: structure, selection, nav and typography are all neutral gray/black — the system accent is refused outright. Color appears only when it *means* something — tinted red for the live recording/Stop control, blue for the Company OS identity icon, the multi-hue rings around persona avatars. This is Von Restorff enforced at the design-system level: with the field kept colorless, the one red control is impossible to miss.
- **[GOLDEN-NUGGET] Platform-material erasure as document-first ideology.** Sidebar and canvas share one pure white; there is no vibrancy, no tonal elevation, no glass, no chrome depth. The blank page *is* the aesthetic — the OS is deliberately made to vanish so the document dominates. Native fidelity is not the goal; a consistent cross-platform blank canvas is.
- **Hand-drawn illustration warmth** offsets the utilitarian monochrome: the black-and-white character faces (agents/collaborators) with colored rings are the brand's single source of personality against an otherwise Swiss-neutral surface.

## Defects

Recorded as **lineage tells + native corrections** (Electron → excluded from macOS canon), not as "fix-me" defects unless native feel were the goal:
- **Accent-binding absence** → selection/nav use neutral gray with black text; native grammar tints the glyph/text with `controlAccentColor`. Correction: bind selection + focus + one primary action to the system accent.
- **Non-native sidebar icon strip** → horizontal chat/calendar/inbox/search row inside the source-list header is a web pattern; native puts navigation vertically in the list or in the toolbar.
- **Web density** → ~15–16px body and generous rows vs the 13pt body / 24–28pt control ladder of macOS 27.
- **Grey traffic lights** → rendered monochrome (inactive or custom); genuine focused chrome shows the colored cluster.

Genuine cross-platform anti-pattern (applies regardless of lineage):
- **Contrast Dilution (mild)** → the lightest tertiary labels ("View all", the "@Today" mention) read ~3–3.5:1 on white (estimated, perspective + JPEG) — below the 4.5:1 text floor. Mid-gray line icons sit near the 3:1 non-text floor.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| main window (perspective render) | 11/14 | #9 tertiary gray labels ~3–3.5:1 (est.); #10 mid-gray icons ~3:1 borderline. (#5,#6,#12,#13,#14 N/A — no paragraph/forms/focus state in a static marketing render.) |

**Native-tells audit: 2/10.** Passes: #4 sidebar headers sentence-case system font; #7 one prominent action (tinted Stop) with quiet Share. Fails: #1 Electron not AppKit; #2/no material system (flat, not a defect but non-native); #3 selection fill present but text neutral, not accent-tinted; #5 web density; #6 no accent binding; #10 grey/monochrome traffic lights. #8/#9 N/A (perspective precludes corner + toolbar-group verification).
