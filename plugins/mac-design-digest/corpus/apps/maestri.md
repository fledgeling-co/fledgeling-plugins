# Maestri — profile

- **Source:** macapp.supply (cover.png only — no discrete screenshots supplied) · **Surfaces digested:** main window / infinite canvas (light) · **Last updated:** 2026-07-19
- **One-sentence identity:** Apple Freeform's native spatial canvas repurposed as an AI-agent orchestration board — live terminal sessions, notes, code diffs, and web captures become movable nodes wired into a colour-coded pipeline, all under restrained Liquid Glass chrome (peers: Freeform, Muse, Warp).
- **Cluster:** unassigned (opens a candidate "spatial-canvas / native workspace" cluster — sole member; do not promote)
- **Lineage:** native (high) — Liquid Glass container-morphed toolbar, borderless SF Symbols, accent-tinted active tool, coloured traffic lights, 13pt-class title-pill text, macOS document proxy pill. Unmistakably a macOS 26/27 AppKit/SwiftUI app; not Electron (container-morphing glass groups are the tell).
- **Era (chrome):** Liquid Glass native (macOS 26/27)

> **Evidence caveat:** the only asset is a marketing cover — the app is captured (~2x), composited into a 14″ MacBook Pro device frame (notch visible) at slightly-under-2x scale, and the **canvas is deliberately zoomed out** to show "the big picture," so node content renders tiny. Structural/grammar evidence (chrome archetype, glass discipline, control vocabulary, node model) is reliable; per-pixel token values are `(estimated)` with wide ranges. No settings, dark-mode, empty-state, or form surfaces seen.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/canvas | #FFFFFF–#FCFCFD (estimated)(inferred) | | infinite canvas, light mode; opaque content layer (correct glass discipline) |
| canvas/grid | ~1px hairline graph grid, light gray ~#00000008–0E (estimated)(inferred) | | fine dot/line "graph paper" lattice — the canvas's spatial affordance |
| chrome/toolbar | unified Liquid Glass, XL-tier (36pt-class) controls, ~52–72pt band (estimated)(inferred) | | borderless mono SF Symbols in ≥3 container-morphed glass groups |
| toolbar/group | continuous glass capsule, capsule bezel (estimated)(inferred) | | adjacent tool symbols share one refractive edge — kit "container morphing" |
| title/proxy-pill | glass capsule, app-icon glyph + "Maestri macOS App" ~13pt Semibold (estimated)(inferred) | | macOS document/proxy pill in titlebar centre-left |
| accent/active-tool | system blue ~#0088FF (estimated)(inferred) | | pointer tool is the ONE tinted symbol; all other tools monochrome |
| type/ui | 13pt-class SF Pro (title pill, card headers) (estimated)(inferred) | | matches kit Body 13pt |
| type/node-mono | fixed-width mono (terminal + code nodes) (measured)(confirmed) | | terminals & code editors render their own mono; product-native to the subject |
| node/card-radius | ~6–8px (estimated)(inferred) | | canvas node chrome — small radius, not capsule |
| node/header | ~22–24pt compact bar: status glyph (lead) + title + ✕ (trail) (estimated)(inferred) | | custom node chrome, not standard NSWindow traffic lights |
| node/border | ~1px very-light gray hairline (estimated)(inferred) | | soft — borderline #10 UI-contrast on white |
| connector | dashed gray bezier curves between nodes (measured)(confirmed) | | the "flow" wiring — hand-drawn pipeline aesthetic |
| stage-label | tracked UPPERCASE + dashed rule, category-hued (measured)(confirmed) | | BUILD=blue · CREATE=green · Refine=red · Review=purple |
| category/palette | blue/green/red/purple identity hues from system 12-hue set (estimated)(confirmed) | | per-swimlane identity colour — separate from the app accent (correct) |

**Brand evidence (backdrop — NOT app UI; never feeds macOS canon):**

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/backdrop | lavender→white vertical gradient (estimated) | | cover ground |
| brand/texture | scattered monospace glyph field (`0`, `<`, chevrons, em-dashes) (measured) | | code/binary motif — "developer" signalling |
| brand/display | heavy geometric grotesque, near-black, tight ("Every agent. One canvas." / "See the big picture") (estimated) | | rounded-terminal display face |
| brand/body | monospace typewriter face for sub-copy (measured) | | deliberate display-grotesque + mono pairing |
| brand/icon | Liquid-Glass layered terminal-window icon: indigo/purple gradient, `>_` prompt with a `:)` smiley (estimated) | | NOT digested as icon (Workflow A only) — recorded as brand evidence |

## Layout skeletons

**Main window — infinite spatial canvas (single surface seen):**
- **Top:** one unified Liquid Glass toolbar spanning full width. Three logical regions:
  - *Leading identity cluster* — traffic lights · sidebar-toggle (glass pill) · document proxy pill (app-icon glyph + "Maestri macOS App").
  - *Centre tool cluster* — one continuous glass capsule holding ~8 borderless SF Symbols: pointer (accent-tinted, active) · terminal `>_` · note/list · paperclip · folder · globe · "Aa" type · pen/mask circle. This is the node-creation / tool palette.
  - *Trailing action cluster* — `{}` code pill · hammer+chevron (build/run split) · share · `»` overflow.
- **Body:** full-bleed opaque white canvas with a fine graph-paper grid. Heterogeneous nodes float freely, each with its own compact header (status glyph · title · ✕): terminal sessions (Claude Code, opencode), code editors (diff-coloured), yellow legal-pad notes, web/browser captures (GitHub, Setapp, Apple Developer), phone-frame captures, and free text nodes.
- **Overlay structure:** nodes are wired by dashed grey bezier connectors into a left→right pipeline; **colour-coded UPPERCASE stage labels with dashed rules** act as swimlane markers (BUILD → CREATE → Refine → Review). No persistent sidebar or inspector shown (sidebar-toggle present but collapsed).

## Signature moves
- **[GOLDEN-NUGGET] The product thesis rendered as the UI: one infinite canvas where every heterogeneous artefact — live agent terminals, code diffs, notes, and web captures — is a co-equal movable node.** The chrome is deliberately quiet native Liquid Glass so the spatial content is the entire experience. "Every agent. One canvas." is literal.
- **[GOLDEN-NUGGET] Live PTY/agent sessions as first-class canvas nodes.** Claude Code and opencode run *inside* cards (real CLI banners, cursors, status footers), not screenshots of them — the terminal is embedded, spatialised, and wired into a flow.
- **Colour-coded pipeline swimlanes.** Stage labels (BUILD/CREATE/Refine/Review) each take a distinct system identity hue and a dashed connector rule, giving the freeform canvas a legible left-to-right process spine without imposing rigid lanes. The category hues are correctly kept separate from the single app accent (the blue pointer tool).
- **Textbook Jakob's Law split:** conventional about the interface (stock macOS Liquid Glass chrome, real proxy pill, system accent), innovative about the product (the canvas model). The app "disappears" so the work shows.

## Defects
- None systematic. One soft flag: **node border hairlines (~1px, very light gray) sit near the #10 UI-contrast floor on white** — likely fine in-app at working zoom, unverifiable from a zoomed-out composite. Not recorded as an anti-pattern.
- Not defects, just unobservable from this asset: focus-appearance (#14), input height (#12), label proximity (#13) — no forms/inputs in view; dark mode unseen.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main canvas (light) | 12/14 | #14 focus state unobservable (static composite); #12/#13 N/A (no form inputs); #10 node hairline borders borderline on white |
| native-tells | 9/10 | #4 N/A (sidebar collapsed — headers not shown) |
