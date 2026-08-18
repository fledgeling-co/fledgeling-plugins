# Pattern: menu-bar-extra

Cross-app synthesis of the `MenuBarExtra` surface — status-item menus, rich popovers, and notch-anchored panels. Native-lineage evidence only. Kit floor: `kit/macos-27.md` — menu-bar item selection **13pt radius (on 25pt), capsule**; menu item selection radius **8** (on 24pt rows); Popover body radius **20**; menu rows Regular **24pt**; Dock/menu-bar app icons 72×72.

## Evidence

| App | Surface | Key values | Provenance |
|---|---|---|---|
| Keeby | menu + profile panel (dark, Tahoe) | dark glass panel ~160–170px, r~16–20; **menu selection = full-width accent-blue inset fill r~8**; sentence-case secondary section headers (Control/Configure); ~24pt menu rows, icon-leading single-line; brand orange quarantined to icon, selection binds **system** blue; "Soon" status pills on disabled rows | (estimated)(inferred) |
| Klack | control panel + picker (light/dark glass) | Control-Center module stack (toggle → slider → picker); ~44pt picker rows: leading identity-colour "+" chip + label + trailing ▶ audition; title-case secondary section headers; house-teal toggle + black slider (accent not system-bound, flagged) | (estimated)(inferred) |
| Satu | popover (light/cream) | ~340–370px rounded panel r~16–18; full-width task-header card + flush disclosure list (`label` left / secondary value right / trailing `>` chevron — flagged iOS); large lofi "vibe" art card; green "Done" = the one saturated action | (estimated)(confirmed) |
| Cachesweep | rich panel (dark glass, Tahoe) | ~340pt Liquid-Glass popover r~16, wallpaper-tinted; header (sparkle glyph + wordmark + refresh); **giant `120.3 MB` hero metric ~36pt**; full-width capsule "Clean Selected" (XL 36pt); tracked-uppercase section headers (flagged); trailing circular checkbox selection (flagged iOS); live green ▲-delta feed | (estimated)(inferred) |
| Dropzone | launcher panel (light vibrancy) | ~443pt translucent popover r~16–20, up-caret anchored to status icon; toolbar row (grouped `+`/collapse container, centred pop-up, grouped window/gear); **5-col ~64pt tile grid** in sentence/title-case sections; menu-bar item selection r~13 | (estimated)(inferred) |
| Open Timer | popover (dark) | ~297×283 opaque **navy card** (hardcoded brand surface, flagged), r~20, no beak; oversized tabular time hero ~48–52px; 7-bar session sparkline; single accent action (pause) | (estimated)(inferred) |
| Mac 4 Breakfast | panel (dark) | ~330–360pt borderless popover r~16–20; segmented tab-bar primary nav (solid-blue fill — flagged); hero status row + charge card + key/value health table; status triad blue=selection, green=good, orange=cost | (estimated)(inferred) |
| Purge | popover (dark) | r~18–20 translucent panel, rounded status-item highlight; header (bold value + secondary), hairline divider, ~50px action rows (2× native menu-item height → window-style popover, not `NSMenu`) | (estimated)(confirmed) |
| Hora Calendar | "ends in Xm" popover (dark) | status item countdown → popover: time-stamped event rows + ALL-DAY badges + coloured Join pills; "Tomorrow" section; bottom Focus 25:00 pomodoro strip | (estimated)(confirmed) |

## Converged rules

- **Two form factors: a thin `NSMenu`-style menu (~24pt rows, selection r8) and a rich window-style popover (~300–450pt wide, r~16–20)** — apps: Keeby (menu), Klack, Satu, Cachesweep, Dropzone, Purge, Mac 4 Breakfast (popovers) — **(canon)**. Rich popovers run ~2× the native menu-item height and carry cards/controls a plain menu can't.
- **No traffic lights / no titlebar — the panel is floating chrome, anchored to its status item (often with an up-caret)** — apps: Dropzone (up-caret), Cachesweep (caret), Open Timer, Mac 4 Breakfast, Satu — **(canon)**.
- **Popover corner radius ~16–20 (near the kit's specified Popover body 20)** — apps: Keeby, Satu, Cachesweep, Dropzone, Purge, Open Timer, Mac 4 Breakfast — **(canon)**.
- **A single dominant hero readout answers the one glance-question, scale-as-hierarchy** — apps: Cachesweep (`120.3 MB` ~36pt), Open Timer (oversized time), Mac 4 Breakfast (hero status + %) — **(recurring→canon)**; the panel's whole job is a one-second glance.
- **Exactly one saturated action; everything else neutral/monochrome** — apps: Cachesweep (one capsule CTA), Open Timer (pause only), Satu (green Done), Keeby (one system-blue selected item) — **(canon)**.
- **Menu/list selection binds a full-width accent fill (menus r13-capsule on the bar, r8 inside)** — apps: Keeby (r8 accent fill), Dropzone (r13 menu-bar selection), Klack (checkmark current-selection) — **(recurring)**.

## Divergences

- **Panel material.** Native adaptive glass/vibrancy that tints to the wallpaper (Cachesweep, Dropzone, Keeby, Klack, Tono) vs a **hardcoded opaque brand surface** (Open Timer navy, DeskMinder green) — the hardcoded-surface reading is the flagged non-native tell (fixed accent + brand fill instead of `NSVisualEffectView` + `controlAccentColor`).
- **Section-header grammar.** Sentence/title-case secondary (Keeby, Klack, Dropzone, Hora menu-bar) vs **tracked-uppercase** (Cachesweep `LIVE ACTIVITY`, Satu) — the same lineage tell as everywhere else.
- **Selection / row affordance.** Native accent inset fill (Keeby) vs **iOS idioms**: trailing circular checkmark toggles (Cachesweep), per-row `>` disclosure chevrons (Satu), segmented-control-as-nav (Mac 4 Breakfast) — recurring SwiftUI-multiplatform tells, excluded from macOS canon.
- **Notch sub-family.** A distinct group anchors to the display notch rather than the menu bar (Folder Hub file-drawer, DeskMinder live-activity pill, Alcove/DynamicLake) — wide-short panels that transpose a sidebar into horizontal tabs and often import iOS Live-Activity grammar; recorded as a related-but-separate register (see floating-panel.md).

## Generation guidance

- **Choose the form factor:** a thin `NSMenu` (24pt rows, r8 selection, sentence-case section headers, leading SF Symbol) for a quick command list; a **window-style popover** (~340pt wide, radius ~18) for a rich glanceable dashboard.
- **Chrome:** no traffic lights, no titlebar. Anchor to the status item (add the up-caret). Use `NSVisualEffectView` menu/popover material so the panel tints to the desktop — do **not** hardcode a brand-colour surface (Open Timer's navy / DeskMinder's green are the flagged misses).
- **Hierarchy:** lead with one dominant hero readout (the number/time the user opened the panel to see) sized ~34–48pt; everything else defers. Section headers sentence/title-case, secondary-grey — never tracked uppercase.
- **Action economy:** exactly one saturated element as the primary action (a full-width capsule at the XL 36pt tier), plus optionally one reserved identity/status hue (always glyph-paired). Everything else monochrome.
- **Selection:** full-width accent inset fill (r8 inside the panel; r13 capsule for the menu-bar item itself). Avoid trailing circular checkmarks and per-row `>` chevrons (iOS tells).
- **Accent discipline:** bind selection + the one action to the user's `controlAccentColor`; keep a loud brand hue quarantined to the icon (Keeby is the reference — orange icon, system-blue UI).
- **Contrast watch:** secondary/tertiary text over translucent glass frequently drops below 4.5:1 — seat critical secondary text at ≥55% white or on a higher-opacity zone.
