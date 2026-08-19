# Pattern: floating-panel

Cross-app synthesis of floating panels — Quick Look-style preview panels, HUD command palettes, floating tool bars, notch-anchored drawers, and glass islands over content. These are surfaces that are *legitimately all chrome* (no window body, no traffic lights), so they are judged against popover/panel grammar, not window grammar. Native-lineage evidence only. Kit floor: `kit/macos-27.md` — Popover body radius **20**; HUD/panel is "a darker, translucent variant for media-oriented or immersive apps."

## Evidence

| App | Surface | Key values | Provenance |
|---|---|---|---|
| FolderVitrine | folder preview panel (light, Tahoe) | ~878×580pt, r~20–24; **translucent Liquid Glass, wallpaper-tinting**; close/dismiss ✕/⊘ circles top-left + share top-right (Quick Look chrome, **no traffic lights**); 2-col body (preview-stack collage + data column); content-on-glass flagged | (measured)(inferred) |
| SpacePeek | Quick Look folder panel (light, Tahoe) | translucent whole-window vibrancy; ✕/⊘ circular buttons top-left (not traffic lights); r~14–16 window / r~12–14 card / capsule pills; hero total + donut + tinted-wash list; segmented Overview\|Contents | (estimated)(inferred) |
| Atlas | gallery islands (light, Tahoe) | **chromeless** — four floating glass islands over edge-to-edge content: traffic-light glass capsule + sidebar-toggle square (top-left), centred title, dark-glass segmented switcher (bottom-center), circular import button (bottom-right); each island one continuous glass edge; content opaque w/ soft shadow | (estimated)(inferred) |
| Raycast | command-palette HUD (dark) | full-bleed near-black translucent HUD, r~10–12, **no titlebar/traffic lights**; search text with no field chrome + leading back-button; two-pane list+inspector (35/65) inside the palette; ~40–48pt rows; **neutral (accent-suppressed) selection** | (measured)(inferred) |
| Orbs | radial launcher HUD (dark, Tahoe) | frameless radial canvas; **Clear-glass centre hub** (desktop lensed through), dark-glass wedges; solid-white "aim" selection (not accent); labels carry a dark text-halo scrim for legibility over any wallpaper | (estimated)(inferred) |
| Presentify | annotation tool bar (over any app) | single horizontal **near-black opaque capsule** (~#0B0B0E), r~8–10, drag-handle + colour swatches + dividers + tool cluster; opaque (not glass) deliberately, to stay legible over any background | (estimated)(inferred) |
| Dropzone | launcher popover (light vibrancy) | ~443pt translucent panel, r~16–20, up-caret anchored; grouped-control containers; 5-col tile grid | (estimated)(inferred) |
| Klack | Control-Center panels (light+dark glass) | two-material split: warm-cream light control panel + warm-graphite dark picker popover, r~14–18; translucent, wallpaper-lensed | (estimated)(inferred) |
| Folder Hub | notch file-drawer (light) | wide-short popover anchored to notch, r~16–20, **no traffic lights**; source-list transposed into horizontal top-tabs (form-factor concession); Finder icon grid; neutral-grey selection | (estimated)(inferred) |
| macUSB | install-config modal (dark) | **floating centred rounded card** (flagged — native modality is a top-anchored sheet, not a centred dialog); dimmed backdrop; ~26pt checkboxes + focus-ring field + trailing capsule Done | (measured)(confirmed) |

## Converged rules

- **A floating panel legitimately has no traffic lights / no titlebar; its chrome is Quick-Look-style (✕/⊘ close-dismiss top-left, share top-right) or none at all** — apps: FolderVitrine, SpacePeek, Raycast, Orbs, Atlas islands, Dropzone, Folder Hub — **(canon)**.
- **Panel corner radius is large, popover-class ~16–24 (near the kit's specified 20)** — apps: FolderVitrine (20–24), SpacePeek (14–16), Dropzone (16–20), Klack (14–18), Folder Hub (16–20), Open Timer (20) — **(canon)**.
- **The panel material is translucent glass/vibrancy that tints to the wallpaper behind it** — apps: FolderVitrine, SpacePeek, Cachesweep, Dropzone, Klack, Atlas islands — **(canon)** for Liquid-Glass-era; the deliberate exception is an *opaque* panel where legibility-over-anything demands it (Presentify's near-black tool capsule).
- **Grouped controls share one continuous glass container per cluster (container morphing)** — apps: Atlas (each island one edge), Dropzone (leading/trailing grouped pills), FolderVitrine — **(recurring→canon)**.
- **HUD launchers suppress chrome to a full-bleed translucent stage and enlarge rows/targets** — apps: Raycast (~40–48pt rows, no field chrome), Orbs (radial wedges as huge Fitts targets) — **(recurring)**; both are the ⌘K command-palette register, not an AppKit list window.

## Divergences

- **Content-on-glass discipline.** Clean: Atlas keeps every content item opaque with its own shadow, glass only on the four islands. Compromised: FolderVitrine, SpacePeek, Compresto seat lists/text *on* the translucent panel — flagged glass-in-content (softened for genuine transient Quick Look panels, where the whole surface is arguably floating chrome, but the scrollable list within is still content and should sit on an opaque fill).
- **Selection on a HUD.** Native accent-inset (rare here) vs deliberate **accent-suppressed / white-aim** selection (Raycast neutral grey, Orbs solid-white reticle) — a systematic signature of the launcher/HUD register that keeps the stage chromatically silent so content carries colour; costs the selection its contrast (Raycast's ~1.3:1 selection is the logged tradeoff).
- **Modal grammar.** A native modal should be a **top-anchored sheet**; macUSB's floating **centred** dialog is the recurring iOS/web tell.
- **Notch-anchored sub-family.** Folder Hub / DeskMinder / Alcove / DynamicLake dwell on the display notch, transpose sidebars into horizontal tabs, and often import iOS Live-Activity grammar — a coherent but non-canonical register (brand-tinted material, fixed accent).
- **Contrast over translucency** is the recurring cost across the whole pattern (FolderVitrine dividers ~1:1 on glass, SpacePeek tertiary %, Cachesweep secondary text) — glass over an arbitrary desktop is the worst case for secondary text and hairlines.

## Generation guidance

- **Chrome:** no traffic lights, no titlebar. For a preview/utility panel use Quick-Look chrome (✕ + ⊘ circles top-left, share top-right). For a launcher, use no chrome at all beyond a leading back-button.
- **Material + radius:** translucent Liquid Glass (`NSVisualEffectView`) that tints to the wallpaper, corner radius ~20 (popover-class). Use an *opaque* panel only when legibility over arbitrary content demands it (annotation/overlay tools → near-black opaque capsule).
- **Glass discipline (the cardinal rule):** glass lives on the *floating layer only*. Every list, table, card, and text block sits on an **opaque (or high-opacity) content fill**, never directly on the glass. Group controls into continuous glass containers (container morphing), each with soft interior dividers.
- **HUD launchers:** full-bleed translucent stage, search text set directly on the panel (no field chrome), generous ~40–48pt rows. If you suppress the accent for a silent stage (Raycast/Orbs register), still give selection a ≥3:1 contrast shift (accent-tinted text or a firmer fill) — the recurring miss is a sub-2:1 selection state in a keyboard-driven launcher.
- **Legibility over any desktop:** give panel text a subtle dark scrim/halo (Orbs) or seat secondary text on an opaque zone; verify secondary ≥4.5:1 and hairlines ≥3:1 against the *lightest* wallpaper the panel might float over, not just the demo one.
- **Modals:** anchor a sheet to the window's top edge; do not float a centred dialog (macUSB miss).
