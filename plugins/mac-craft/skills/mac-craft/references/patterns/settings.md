# Pattern: settings

Cross-app synthesis of the Settings/Preferences surface. All 8 pattern members are native lineage (`settings` pattern = 8 native / 8). Kit floor: `kit/macos-27.md` — Settings uses the grouped-form idiom; sidebar row selection radius **8**, section headers 18–20, controls at the 24pt Rg tier, capsule as the default bezel; light primary text **85% black**, secondary 50%.

## Evidence

| App | Surface | Key values | Provenance |
|---|---|---|---|
| Bartender 6 | split-view settings (dark) | System-Settings clone: source-list sidebar (solid-accent selection r8) + scrolling detail of **grouped inset rounded cards** (r~10–12) of label-left / control-right rows w/ inset hairlines; **hero header card per pane** (icon tile + LargeTitle-class title + one-line description); section headers 13pt Semibold Title Case | (estimated)(confirmed) |
| Inkline | separate settings window (dark) | left nav sidebar (search field + 10 SF-Symbol destinations, ~32pt Medium rows) + right scroll of **outlined section-cards** (r~10–12), each Title2 header + secondary description + native pop-ups (double chevron) + **one filled-violet primary** with quiet/disabled siblings | (estimated)(inferred) |
| Shake it On | grouped Form (dark) | SwiftUI grouped `Form`: **bold Title-Case section header** (flush left) → one rounded inset group `#222` of full-width rows w/ hairline separators → optional tertiary caption; radio pair + `Toggle` rows; disabled minimize/zoom greyed | (measured/estimated)(confirmed) |
| Corner Time | settings window (dark) | ~299px portrait; shared ~20px inset axis; **WYSIWYG live-preview card** (r~12) → segmented pane switch (Format/Style/General) → **inset-grouped settings card** (r~14) of 4 `label…switch` rows w/ faint left-inset hairlines; native capsule switches; row ~52pt | (estimated)(inferred) |
| Zipic | Pro pane (light) | native **preferences tab bar** (icon-over-label ×4, selected = rounded fill + accent); **one-setting-per-card** grouped white rounded cards (r~10–12), each leading SF Symbol + bold Title-Case header + control; disabled minimize/zoom greyed | (estimated)(confirmed) |
| Presentify | Cursor pane (light) | classic AppKit `NSToolbar` **icon-over-label tab bar** (General/Annotate/Cursor/Shortcuts/About); grouped form rows = `[primary label / secondary one-sentence description]` left + right-aligned control (sliders); section header "Spotlight" secondary | (estimated)(confirmed) |
| Satu | Options window (light/cream) | **custom 4-segment tab bar** (icon over **tracked-uppercase** label — flagged defect); tracked-uppercase accent-blue section headers (flagged); grouped rounded cards, 28px circular blue icon chips, title+subtitle + trailing accent switch | (estimated)(inferred) |
| macUSB | wizard + config modal (dark) | full-width rounded cards ~30px margins; **centred rule-label section headers** (flagged non-native); iOS-scale controls (~45pt buttons, ~26pt checkboxes — flagged); floating centred modal (flagged, not a sheet) | (estimated)(confirmed) |

## Converged rules

- **Settings is a grouped-form: section header → inset rounded card (r~10–14) of `label-left / control-right` rows separated by inset hairlines** — apps: Bartender 6, Inkline, Shake it On, Corner Time, Zipic, Presentify, Satu — **(canon)**. Between-section gaps exceed within-group row gaps (Gestalt proximity).
- **Controls right-aligned on a shared axis; labels left on a shared axis** — apps: Bartender, Shake it On, Corner Time, Presentify, Compresto(form), Zipic — **(canon)**.
- **One filled primary per dialog/pane; siblings are quiet or disabled-but-visible** — apps: Inkline (filled-violet Save + quiet Delete/Apply), Shake it On, macUSB(operation-confirm) — **(recurring→canon)**. Disabled controls stay dimmed-in-place, never hidden (Bartender, Shake it On, Inkline).
- **Settings-window traffic lights: minimize/zoom greyed/disabled** (the correct macOS settings-window tell) — apps: Zipic, Shake it On, Corner Time, Satu — **(canon)**.
- **Native controls throughout: capsule switches (blue-on/grey-off), pop-up buttons with the double up/down chevron, square checkboxes, segmented pickers** — apps: Bartender, Inkline, Corner Time, Zipic, Presentify, Shake it On, Compresto — **(canon)**.
- **Two-tier rows for consumer utilities: bold primary label over a one-sentence secondary description** — apps: Presentify, Satu, Zipic, Compresto — **(recurring)**; trades density for recognition-over-recall, appropriate for configure-once utilities.

## Divergences

- **Navigation model.** A real **sidebar** (Bartender System-Settings clone, Inkline) vs a **preferences tab bar** — classic AppKit icon-over-label `NSToolbar` (Presentify, Zipic) vs a **segmented/custom tab bar** (Corner Time, Satu). The kit note "a toolbar is not a tab bar" makes the segmented-as-nav choice a soft native quibble (Corner Time's `Picker(.segmented)` is an accepted small-window idiom; Satu's tracked-uppercase custom pill group is flagged).
- **Section-header grammar splits along lineage confidence.** Native-correct **sentence/Title-Case system-font secondary** headers: Bartender, Shake it On, Presentify, Zipic, Inkline. **Tracked-uppercase / centred-rule** headers: Satu (tracked-uppercase accent), macUSB (centred rule-labels) — both flagged as native-tell defects (Satu heavily re-skinned; macUSB iOS-idiom).
- **Card density.** Many-rows-per-card (Bartender, stock System Settings register) vs **one-setting-per-card** (Zipic, spacious consumer-warm register). Density choice tracking pro-config vs consumer audience.
- **Signature flourish: the hero/preview card.** Bartender titles every pane with an elevated hero card; Corner Time renders a live WYSIWYG preview above the toggles that shape it. Both are `[GOLDEN-NUGGET]` orientation devices layered onto the stock grouped form.

## Generation guidance

- **Structure:** either a real settings **sidebar** (Medium 32pt rows, selection r8) for a many-pane app, or an AppKit-style **preferences tab bar** (icon-over-label, normal-case labels) for ≤5 panes. Avoid a segmented control as primary nav for anything but a tiny window.
- **Body:** vertical stack of **inset rounded grouped cards** (radius 10–14). Each group = a **sentence/Title-Case, secondary-grey, system-font** header, then rows of `label-left / control-right` separated by inset hairlines. Never tracked uppercase, never centred rule-labels.
- **Alignment:** all labels on one left axis, all controls on one right axis. Between-section gap > intra-group row gap.
- **Controls:** native capsule switches (blue-on/grey-off), pop-up buttons with the double up/down chevron for pick-a-value, square checkboxes for multi-select, sliders right-aligned. Bind the on-state to the user's system accent, not a brand hex.
- **Actions:** at most one filled primary per pane (Inkline's filled-violet Save reference — but use the *system* accent); keep Delete/secondary quiet or disabled-but-visible.
- **Window chrome:** grey out minimize/zoom (settings-window convention); keep primary text at 85%-black (light) and secondaries at the 50%/55% tiers so a group caption still clears ~4.5:1 — the recurring miss is tertiary captions dropping under the text floor.
- **Optional signature:** a per-pane hero card or a live WYSIWYG preview above the controls (Bartender / Corner Time) is a strong orientation move for a config-dense app — layer it on top of, not instead of, the grouped form.
