# Hoolo — profile

- **Source:** macapp.supply (meta.json + cover.webp + icon.png) · **Surfaces digested:** 1 — main window / Rules list, light (embedded in the marketing cover) · **Last updated:** 2026-07-19
- **One-sentence identity:** AutoShelf's brand-accent file-rules utility, rotated from orange-red to a breezy green-and-amber — a "reversible cleanup" organizer whose signature is color-coding each rule's chain behavior (green = keep matching, amber = stop) rather than any native selection grammar.
- **Cluster:** unassigned (proposed hint: *file-rules utility (brand-accent)*) — pairs with **AutoShelf** as a candidate 2-member cluster (both: rules list, per-row status toggle, brand hue replacing the system accent, inset card rows, marketing-cover-embedded window). Two direct peers is `(recurring)`, not yet canon.
- **Lineage:** **web-electron (low confidence)** — genuinely ambiguous with heavily-custom SwiftUI. The window *frame* is convincing (coloured traffic lights, a real unified toolbar of borderless monochrome SF-Symbol-style glyphs, a trailing gear = Settings, a share tray glyph), but the *body* reads non-native: inset rounded-rect card rows on a faintly tinted canvas, green iOS-`UISwitch`-style capsule toggles, and **colored interactive text** ("Continue Matching Later Rules" in green / "Stop After Match" in amber) standing in for native pop-up buttons. Judge lineage from the body: this does not read AppKit-native. Whichever way it lands (Electron vs custom SwiftUI-multiplatform), its non-native idioms are recorded as **tells + corrections and must never feed macOS canon.**
- **Era (chrome):** **custom** contemporary flat (brand-styled, 2023+). **No Liquid Glass** — chrome and cards are flat opaque, no lensing/edge-bending, no glass grouping (legitimate absence for a utility, not a defect). Does not track the macOS 27 material system.

## What was actually supplied (honesty note)

No `shot-*` files were provided (gallery empty). The only UI evidence is inside the **3098×1998 marketing cover** (`cover.webp` → converted via `sips -s format png`). The cover is a composite of **two designed things that must not be conflated**:

1. **The website landing page** (brand evidence, web) — a soft-focus **blue-sky + wildflowers** photographic backdrop, a floating translucent-white **glassy capsule nav pill** (Hoolo lockup · Overview/Safety/Pricing/Rules/FAQ/Update · language picker · a saturated green "Early Bird · 20% Off" pill), a heavy near-black grotesk **display headline** with two words knocked into brand green ("clean", part of "reversible") and one into amber ("quiet", part of "reversible"), and a black **"Download for Mac"** capsule CTA. This is a consumer-warm marketing surface, not the app.
2. **The app window** (the design evidence), embedded lower-center, bleeding off the bottom of the composite.

**Scale is indeterminate.** The window sits at an unknown scale inside the composite; a traffic-light estimate implies roughly ~1.2 px/pt but is unreliable off a soft render. **Therefore no absolute pt sizes are asserted below** — tokens are proportional/relative and marked `(estimated)` or `(assumed)` with wide error bars. Marketing copy ("watches the folders that get messy first… keeps risky cleanup reviewable before files move") is context, not evidence.

## Tokens

All values `(estimated)(inferred)` unless noted — one exposure, indeterminate scale, single app. App-UI tokens first; brand/web tokens flagged separately and excluded from any native reading.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/window-content | very light warm gray ~#F3F3F4 | (estimated)(inferred) | content canvas, light mode; cards sit a step lighter |
| bg/rule-card | near-white ~#FBFBFC with a soft shadow/hairline | (estimated)(inferred) | each rule is an inset rounded card, not a flat list row |
| accent/brand-green | ~#3FB977 / #45C07E green | (estimated)(inferred) | THE app accent — toggle "on" track + the "Continue Matching Later Rules" menu text/glyph; replaces the system accent. Matches the website's green display words |
| status/amber | ~#E8912E / #EF9A3A amber-orange | (estimated)(inferred) | the "Stop After Match" menu text + target glyph; a second reserved hue for rule-chain state |
| action/pin-blue | ~#2F7DF6 system-blue-ish | (estimated)(inferred) | filled tilted-pushpin per row (pin/prioritize) |
| action/trash-red | ~#E5533B red | (estimated)(inferred) | outline trash/delete per row |
| control/status-toggle | green capsule `UISwitch`-style, knob RIGHT = on | (estimated)(inferred) | iOS switch grammar (green track), not NSSwitch/accent; every visible rule is on |
| control/chain-menu | colored **text** + leading glyph + chevron-down (green "Continue Matching Later Rules" / amber "Stop After Match") | (estimated)(inferred) | a pull-down styled as bare colored text — non-native (native = bordered pop-up button); doubles as at-a-glance rule-chain state |
| type/row-title | bold, primary near-black (~85–100%), ~Body/Headline-emphasized class | (estimated)(inferred) | e.g. "Screenshot Organization"; family reads SF Pro **or Inter** — cannot disambiguate |
| type/toolbar-label | medium, primary, beside each toolbar glyph | (estimated)(inferred) | "Trash Cleanup / Add Rule / Choose Folder / Scan / Logs Panel" |
| type/secondary | gray secondary — "8 rules, 8 enabled" + section label "快捷模板" | (estimated)(inferred) | de-emphasis carried by color; section label is Chinese (localized build) |
| icon/toolbar-symbols | borderless monochrome SF-Symbol-style: trash / plus / folder / clockwise-arrow (Scan) / history-clock (Logs) / import-tray / share-tray / gearshape | (estimated)(inferred) | the strongest native-affiliation signal in the whole surface |
| list/grouping | inset rounded-rect cards per rule on tinted canvas, even vertical gaps | (estimated)(inferred) | iOS/web card-list idiom, not a flat AppKit list/table with hairline separators |
| chips/templates | borderless icon+label row (Screenshot Archive · PDF Archive · Installer Archive · Large File Review · Duplicate File Review · Screenshot App Pipeline · Downloaded Receipt Archive · Screen Recording Archive · Temporary File Quarantine), faint vertical dividers | (estimated)(inferred) | quick-start "快捷模板" template strip above the rule list |
| chrome/traffic-lights | coloured red/yellow/green = focused window | (estimated)(inferred) | genuine macOS chrome |
| chrome/toolbar | unified single-row: leading "8 rules, 8 enabled" status · trailing action group (5 icon+label) · far-trailing icon-only cluster (import/share/gear) | (estimated)(inferred) | reads native in construction; no single filled primary (fine for a utility) |
| cover/dimensions | 3098×1998 marketing composite (~1.55:1) | (measured)(inferred) | website hero + embedded app window; app window bleeds off bottom |
| brand/nav-pill (web) | translucent frosted-white capsule, blurred, floating | (estimated)(inferred) | **brand/web only** — a glassy nav, not app chrome; do not read as macOS material |
| brand/display (web) | heavy near-black grotesk headline, green + amber colored words | (estimated)(inferred) | **brand/web only** |
| brand/palette (web) | sky-blue photo ground, brand green, amber, near-black | (estimated)(inferred) | **brand/web only** — consumer-warm, organic |

## Layout skeletons

**Main window — Rules list (light).** Single-pane content window (no visible sidebar); the whole surface is chrome-over-list.

- *Toolbar (unified, one row):* leading — traffic lights, then a gray **"8 rules, 8 enabled"** status label. Trailing — a group of five `[SF-Symbol · label]` actions: **Trash Cleanup · + Add Rule · Choose Folder · Scan · Logs Panel**, then a far-trailing icon-only cluster: **import-tray · share-tray · gearshape (Settings)**. Borderless, monochrome, evenly spaced — correct macOS toolbar grammar.
- *Template strip:* a gray section label **"快捷模板"** (quick templates) above a single horizontal row of borderless **icon+label chips** (nine visible), faint vertical dividers between them — a quick-start rail for common rules.
- *Rule list:* a vertical stack of **inset rounded cards**, one per rule (Screenshot Organization / PDF Import to Documents / Centralized Archiving / Certificate Files Archiving…), even gaps. Row anatomy, left→right on shared column axes: `[bold rule title] … [small hand/interaction glyph] [chain-behavior menu — green "Continue Matching Later Rules ⌄" OR amber "Stop After Match ⌄"] [blue pin] [red trash] [green toggle]`. The trailing control cluster right-aligns consistently across every row; the list bleeds off the bottom of the composite.

## Signature moves

- **[GOLDEN-NUGGET] Rule-chain state as color-coded flow language.** Each rule's *matching behavior* — the one genuinely confusing concept in a rules engine (does processing continue to later rules, or stop here?) — is encoded as colored text: **green "Continue Matching Later Rules"** (flow continues) vs **amber "Stop After Match"** (flow halts). Green reads "go", amber reads "stop"; the whole rule chain's logic is scannable down the right rail without opening anything. It's the app's cleverest choice — and it's spent, non-natively, as bare colored menu text (a native pop-up button would be quieter but wouldn't glow the state).
- **[GOLDEN-NUGGET] Reversibility surfaced in the chrome.** The toolbar leads a safety story: **Trash Cleanup**, **Scan** (dry-run), **Logs Panel** (audit trail), plus a per-row **pin** — the "keeps risky cleanup reviewable before files move" promise made physical in the top bar. For a tool that *moves and deletes a user's files*, putting the undo/review affordances in the most prominent chrome is a real trust decision, not decoration.
- **Brand hue owns the accent.** One green (~#3FB977) does the identity work — the toggle "on" state and the primary chain-menu — echoing the website's green display words. Deliberate and consistent, but it replaces the user's system accent (see Defects).

## Defects

- **Reserved-color overload per row** (rubric #8 / hierarchy-rhythm "cap ~3 reserved roles per surface") → each rule row stacks **four** meaning-bearing colors — green toggle, green/amber chain menu, blue pin, red trash — all competing in one ~row-height band. The green/amber flow-coding is the idea worth protecting; the saturated blue pin and red trash beside it dilute the very von-Restorff pop the color-coding depends on. *Correction:* keep green/amber for chain state; demote pin + trash to monochrome secondary glyphs that colorize only on hover.
- **Low-contrast interactive text** (rubric #9) → the light-**green** "Continue Matching Later Rules" and **amber** "Stop After Match" are *controls you must read*, set as thin colored text on near-white — both likely land well under 4.5:1 (light green ~2:1 `(estimated)`). A menu label failing text contrast is a real accessibility miss. *Correction:* darken the text hues (or pair color with a bordered/filled chip that carries the contrast) so the state survives at AA.
- **Non-system accent binding** (native tell #6) → brand green replaces the user's `controlAccentColor` for the toggle + primary menu, and amber acts as a second reserved hue not separated from the accent. Internally consistent house style (defect/signature boundary), recorded as tell + correction. *Native correction:* bind toggles/focus to the system accent; keep green/amber strictly for rule-chain *semantics*, not chrome.
- **Inset-grouped card list as primary content** (native tell #1/#5) → rules render as rounded cards on a tinted canvas with tall padding — an iOS/web idiom where native macOS would use a **flat list/table on one opaque surface** with hairline separators and compact desktop row density. Part of the web/non-native picture.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| main window / Rules list (light) | 11/14 | #8 four reserved-meaning colors compete per rule row (color overload); #9 green/amber chain-menu **text** likely <4.5:1 on white `(estimated)`. Pass: grid regularity, container alignment, gestalt proximity, modular scale, de-emphasis (gray secondary), UI-contrast on toggles/toolbar, Fitts (desktop calibration, with small pin/trash noted). N/A: #5/#6 line-height & measure (no paragraphs in-app), #12/#13 no text inputs or form label pairs visible, #14 no focus state in a static shot. |
| — native-tells audit | 5/10 | #1 body reads web/non-native (inset cards, green `UISwitch` toggles, colored-text menus); #5 non-native inset-card density; #6 brand green + amber replace the system accent. Pass: #2 no glass abuse (flat, legitimate), #7 toolbar restraint (no rogue primary), #8 corners rounded/no obvious concentricity violation, #9 borderless grouped SF-Symbol toolbar reads native, #10 genuine coloured traffic lights + real unified toolbar frame. N/A: #3 no selection state visible, #4 no sidebar. |

## Knowledge gap this app leaves open

One surface, one mode (light), indeterminate scale, marketing-embedded. To place Hoolo the corpus needs: a **clean orthogonal screenshot** (to promote estimated tokens toward measured and settle the SF-Pro-vs-Inter question that would decide web-vs-native), a **settings or rule-editor surface** (the form grammar is the strongest remaining lineage tell), **dark mode**, and the advertised **menu-bar extra** + **HTML report** surfaces named in the marketing chips. Lineage stays web-electron/low-confidence until a form or AX-inspectable surface settles it. With AutoShelf, this is the second brand-accent file-rules utility — one more would open a real cluster.
