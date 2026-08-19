# TASTE.md — macOS design corpus synthesis

> Load this file (plus the relevant cluster section and 1–2 app profiles) when generating a new macOS mock.
> **Corpus level: Proficient** — 209 surfaces / 134 apps / 13 in-file app-icon surfaces. Updated 2026-07-19.
> The level claim rests on the **native subset**: 66 native-lineage apps (49%), all with ≥1 scorable UI surface. Stable canon + clusters with identities exist; full Expert is withheld because only **16 of 66** native apps carry ≥2 surfaces (most are single hero/marketing renders), and settings/onboarding/light-mode-pro evidence is thin (see Gaps).

**Evidence honesty.** 109 apps have ≥1 scorable UI surface; **25 are marketing/brand-only** (tokens = brand/icon evidence, never UI canon). **46 apps (34%) are unknown-lineage** — real UI but unverifiable framework, so excluded from canon. Only `native` evidence feeds the canon below; `web-electron` (19) / `catalyst` (2) / `ios-on-mac` (1) feed Tells & the Non-native shelf. Native-audit (10-pt) median **7.0**, mean 6.16; rubric (14-pt) median **12.0** — the corpus skews competent, with a long tail of Contrast Dilution.

---

## Canon — universal
*(promoted only from ≥3 independent native apps, no contradiction. Every row cites members.)*

> **Independence caveat (auditability).** The observation JSONs carry no developer/vendor field, so "independent (same developer counts once)" rests on **distinct app identities**, not confirmed-distinct developers — it is not auditable from the digestion artifacts. No same-developer duplicate is evident by name among cited members (e.g. only one `-4-breakfast` app is cited), so no violation is known; the guarantee is weaker than the rule's wording implies.

| Rule | Values | Native members (count) | Since |
|---|---|---|---|
| **De-emphasis hierarchy survives grayscale** — 2–3 ink tiers do the work; colour is the last 10%. | primary ~**85%** ink · secondary ~**50–55%** · tertiary ~**25%** (matches kit Labels) | sketch, spacepeek, shake-it-on, hejour, bartender-6, purge, klack, grape, resurf, code-meter, raycast, caesura, fantastical, letterboxx, forma, claude-notch (16) | 2026-07 |
| **Single-accent economy** — exactly one saturated moment per view (one CTA / one selection / one datum); everything else neutral. | 1 accent budget per surface | compresto, open-timer, caesura, autoshelf, liqoria, mac-4-breakfast, satu, revone, room-service, tono, noticky, hejour, orbs, walltune, sketch (15) | 2026-07 |
| **Accent bound to interactive state** — the one accent lives on selection / focus / primary action, not scattered decoration; brand hue quarantined to icon+marketing. | selection+focus+primary share one hex | zipic, spacepeek, satu, letterboxx, glance, cachesweep, macusb, bartender-6, vocal-notes, compresto, keeby, screenlex, hora-calendar, resurf (14) | 2026-07 |
| **Card / container radius 10–14pt** | ~10–14pt (concentric: inner ≈ outer − 4) | spacepeek(12–14), viaduct(12), bartender-6(10–12), satu(10–12), resurf(12), forma(10–12), usage(10–12), room-service(10–12), code-meter(12–14), letterboxx(13) — 10 in-band; **macusb(14–16) sits mostly ABOVE the band, does not evidence the headline range** (11 cited) | 2026-07 |
| **Floating panel / popover radius 16–20pt** | ~16–20pt (aligns kit popover **20**) | cachesweep(16), open-timer(20), folder-hub(16–20), satu(16–18), purge(18–20), droppy(16–20), mac-4-breakfast(16–20), dropzone(16–20), tono(20–24) — 9 carry the band; **klack(14–18) and usage(12–16) fall BELOW the 16 lower bound**, do not evidence the headline range (11 cited) | 2026-07 |
| **Body type = 13pt SF Pro** (matches kit Body) | 13pt SF Pro Regular, lh ~16 | noticky, codeshot, sketch, finbar, shake-it-on, satu, mac-4-breakfast, resurf, hora-calendar, grape, fantastical, room-service, foldervitrine, code-meter, hejour (15) | 2026-07 |
| **Genuine native window chrome** — real traffic-light cluster (~68×14), colours on focus, mutes when inactive. *(Conclusion sound; "never faked dots" is the pattern, not proven-clean on every member — see note.)* | 68×14 cluster, ~12pt dots | clean screenshots: atlas, inkline, vocal-notes, glyph, canary-mail, autoshelf. **Traffic lights observed inside MARKETING COMPOSITES** (render, not clean capture): compresto, corner-time, room-service, hejour, macusb, satu (12) | 2026-07 |
| **Selection = inset rounded-rect fill** — the *geometry* (inset-rounded row/sidebar selection, kit sidebar/menu spec) is canon; the **neutral-flat grammar + radius-8 value** is only *(recurring)* — 2 clean apps. | geometry: inset-rounded ✓ · radius **8** = vocal-notes/grape only (caesura ~10, autoshelf ~10–12) | vocal-notes, grape *(clean neutral inset, r≈8)*; autoshelf, caesura *(inset-rounded geometry but **solid brand-hue fill** overriding the system accent — flagged native#3/#6 in their own obs)*; canary-mail *(**sidebar** conforms neutral #2C3235; message-list = saturated indigo card #2558C9, native#3)* (5) | 2026-07 |

Near-canon, **not** promoted (honest under-claim): **8/4pt spacing rhythm.** Native-audit spacing checks pass broadly, but explicit spacing tokens exist for only 5 native apps under 5 different names (noticky 16/8, deskminder 8, usage 15–16, tono 10–12, raycast). Treat base-8 as the *(assumed)* default per HIG/knowledge-base, not a corpus-measured canon.

**Corrections this pass (2026-07-19 audit).**
- **Rule 8 (selection fill):** `cachesweep` **removed** — its own observation logs a *trailing circular checkbox ~18–20pt* and failure `native#3 selection is trailing circular checkmark, not macOS inset-rounded accent fill`. It is a **counter-example**, not evidence (cited count 6→5). Of the survivors, only vocal-notes + grape cleanly evidence the *neutral flat, radius-8* grammar; autoshelf/caesura/canary-mail show the inset-rounded geometry but with brand-saturated fills that override the system accent — so the radius-8/neutral-flat specificity is now *(recurring)*, geometry stays canon.
- **Rule 4 / Rule 5:** two members each sit outside the headline band (see rows) — annotated in place, rules survive on their in-range members.

---

## Canon — macOS conventions
Ground truth: `kit/macos-27.md` `(specified)`. Corpus confirms/contests these:

- **Control ladder** Mn16 / Sm20 / **Rg24** / Lg28 / **XL36 (toolbars)**; push-button padding 16px. Native apps honour Rg-24 defaults; the frequent tell is *iOS density* (45pt buttons, 26pt checkboxes, ~40pt titles) in catalyst/ios-on-mac and 2 native apps — always logged as non-native.
- **Type** SF Pro, **13pt Body / 16 lh**; light primary **#000 @85%** (not pure black — kit avoids Contrast Dilution). 15/17/22/26pt title ramp. Reading-cluster apps deviate body **up** to 15–16pt on purpose (glance, viaduct item names) — density traded for legibility.
- **Chrome** titlebar 33pt; unified toolbar 52 (compact 40 / expanded 77); sidebar 256pt, rows 24/32/40, selection radius 8; menu rows 24, selection radius 8; popover radius 20; menu-bar-item selection 13 (capsule). Traffic-lights 68×14 at (9, 9.5).
- **Selection fill radius 8** confirmed by native selection grammar (above). **Separators** ~29% black — apps that drop below (8–15% hairlines) fail the 3:1 UI-contrast floor (the corpus's #1 defect).
- **Era (Liquid Glass)** capsule bezels; over-glass vibrant tiers; Scroll Edge Effect under floating toolbars; Active/Inactive states. Corpus glass exemplars: cachesweep, compresto, foldervitrine, liqoria, atlas, maestri. Watch **Glass-in-content** (3 apps) — glass belongs on chrome/floating layers, content stays opaque.

---

## Style clusters
*(9 native clusters + a non-native contrast shelf. Members are native unless the shelf.)*

### Menu-bar Instrument — a single NSMenu/popover *is* the app; restraint as identity. Peers: Bartender, Alfred, iStat Menus.
- **Members:** corner-time, finbar, klack, mac-4-breakfast, mux, open-timer, orbs, raycast, shake-it-on, tono, usage · **Audience:** pro/power utility
- **Identity tokens:** true-dark or graphite ground (#1A1A1C–#1E1E1E) · 13pt body · tabular/mono hero figures · single accent (often system blue, some withhold to white) · panel radius 16–20 · glanceable one-question layouts · per-metric identity hues (usage: #5953FD/#2A9CF9) · live telemetry rows
- **Do:** open by answering one question (mux: "what network am I on?"); promote the hero datum to ~36pt (cachesweep, open-timer); keep chrome invisible. **Don't:** add a titlebar/toolbar the menu doesn't need; scatter more than one saturated element.
- **Read for depth:** klack, open-timer, usage

### Warm-Editorial / Paper — writing & reading surfaces that recolour clinical utility into warm paper. Peers: Bear, iA Writer, Craft.
- **Members:** caesura, forma, glance, glyph, grape, hejour, letterboxx, noticky, vocal-notes · **Audience:** consumer/creative
- **Identity tokens:** warm off-white grounds (#F8F7F5 / #F3F3F0) or graphite; single warm accent (caesura terracotta #B35A3C, hejour lime, glyph steel-blue #5E9DC0) · body 13–16pt · de-emphasis via ONE grey token · monochrome ink controls (noticky) · dimmed inline markdown syntax (hejour, glyph) · calm all-lowercase or sentence-case labels
- **Do:** carry hierarchy by weight + one grey (caesura's #8A8073 for *all* secondary); reserve the accent for a single status (hejour's lime = done only). **Don't:** use the vivid system blue where a bookish muted accent fits; add editor chrome to a reading surface (glance).
- **Read for depth:** caesura, hejour, letterboxx

### Notch Native — the MacBook notch/Dynamic-Island as the entire surface. Peers: NotchNook, Boring Notch, Alcove.
- **Members:** alcove, claude-notch-usage-companion, deskminder, droppy, dynamiclake, folder-hub, healthynotch · **Audience:** consumer glanceable
- **Identity tokens:** **TRUE-BLACK opaque** (#000, appearance-independent) fusing software to bezel · panel bottom-corner radius 28–34 · monochrome + one status hue · glanceable count/countdown · iOS Live-Activity mental model · playful mascot/pixel themes (healthynotch 8-bit)
- **Do:** commit to pure black so the app disappears into the hardware; one glanceable value. **Don't:** use a translucent material here (breaks the bezel illusion); port iOS control sizing wholesale into any spawned window.
- **Read for depth:** alcove, droppy, healthynotch

### Liquid-Glass Translucent Utility — wallpaper-tinted glass sheets; drop-target/file utilities. Peers: iStat Menus, Yoink, Permute.
- **Members:** cachesweep, compresto, dropzone, foldervitrine, liqoria, spacepeek · **Audience:** consumer/pro utility
- **Identity tokens:** whole-window Liquid Glass tinting to wallpaper · one saturated action bar (compresto candy-blue w/ cyan label) · glass-pill metadata riding thumbnails · panel radius 16–20 · single-chroma discipline (liqoria: only the Spotify-green source badge) · grouped translucent toolbar clusters (dropzone)
- **Do:** let user content be the only saturation; float 3–4 glass islands over content (atlas-adjacent). **Don't:** put glass on content text (legibility); add a second accent.
- **Read for depth:** compresto, spacepeek, liqoria

### System-Idiom Utility — near-exact macOS shell adoption (Jakob's Law) as camouflage. Peers: System Settings, Ice.
- **Members:** bartender-6, codeshot, fantastical, maestri, purge · **Audience:** pro utility
- **Identity tokens:** stock Liquid Glass + real proxy pill + system accent · hero header card per settings pane (bartender-6) · grouped native forms · risk-tiered filter pills w/ live counts (purge) · reversibility copy ("moved to Trash") · innovation lives in *content*, not chrome (maestri canvas)
- **Do:** impersonate System Settings precisely, then earn distinctiveness through one purpose-built control (bartender-6 gradient editor). **Don't:** fake the chrome you're imitating; break the idiom you borrowed for familiarity.
- **Read for depth:** bartender-6, purge

### Terminal-Dark Instrument — nocturnal developer tools, instrument-panel density. Peers: Linear, Warp, iStat Menus.
- **Members:** code-meter, hora-calendar, inkline-text-editor, macusb, mole · **Audience:** developer/pro
- **Identity tokens:** near-black grounds (#0B0A0E–#1E1E1E), inverted-depth tonal stacks (inkline chrome>canvas>cards) · monospace metadata voice (mole, code-meter, ayron) · tracked-caps mono section labels · code-editor theming (Tokyo Night/Gruvbox) · per-event colour on the system 12-hue palette · two-hue discipline (hora: brand red owns marketing, system blue owns actions)
- **Do:** keep figure-ground within a few % (screen-studio #0C0D0F discipline); mono for instrument data only. **Don't:** let a fixed brand accent override every focus state (inkline's over-bound violet is logged as a mild defect).
- **Read for depth:** code-meter, hora-calendar

### Content-Forward Gallery — chromeless, content-is-the-interface browsers. Peers: Eagle, Cosmos, Apple Photos.
- **Members:** atlas, prostir-zvuku, supaste, walltune · **Audience:** creative
- **Identity tokens:** edge-to-edge imagery, chrome dissolved to floating glass islands · **zero-accent / white-not-blue selection** (atlas, walltune, orbs, prostir) · true-black or #111 void grounds turning thumbnails into lit objects (supaste) · personable centred window titles ("HELLO, ATLAS") · content is the only chroma
- **Do:** withhold the system accent so every thumbnail is figure against silent chrome; neutral white selection reticle. **Don't:** introduce app-owned colour that competes with user content.
- **Read for depth:** atlas, supaste

### Warm Consumer Utility — friendly Setapp-register tools; brand warmth over correct bones. Peers: One Sec, CleanShot X, Things.
- **Members:** autoshelf, keeby, lookaway, satu · **Audience:** consumer
- **Identity tokens:** one loud brand hue quarantined to icon (keeby orange), **system blue for actual controls** · whole-panel theming sets (satu default/cream/blue) · status-toggle-as-traffic-light (autoshelf green/red pill) · luminance-signalled CTA on tinted glass (lookaway) · rule-as-sentence subtitles · emotional de-escalation copy
- **Do:** quarantine the brand hue, bind interaction to system blue (keeby is the textbook case). **Don't:** override every control with the brand colour (shake-it-on's orange-on-all-controls is a logged tell).
- **Read for depth:** keeby, autoshelf

### Electric Accent (⚠ was "-Dark") — one hardcoded, deliberately-non-system accent carrying a neutral utility surface. Peers: DaisyDisk, Permute.
> **⚠ Coherence flag (near the red line).** The cluster was named "**-Dark**" on a **#171717 dark-ground** identity, but that ground is evidenced by **1 of 3 members**: `revone` only. `picmal` is **light mode** (bg #FFFFFF; its own `cluster_hint` = "electric-accent native utility (**light**)") and `radial` is **light mode** too. The naming token contradicts a majority of members — per persona §4.1 (no cluster contradicting >2 identity tokens) this approaches the split/rename line. The token that actually unifies all three is **the electric, hardcoded accent that is deliberately not system blue** (revone indigo #6155F5, picmal royal #1B5BFF), *not* the ground luminance. `picmal` is a **weak member** anyway — logged "competent-but-almost-anonymous / default AppKit table with a blue swap". At n=3 with one weak + one geometry-only member, treat as provisional; a 4th clean dark-ground app would re-earn the "-Dark" name, otherwise rename to "Electric Accent" and let ground luminance vary.
- **Members:** revone *(the only #171717 dark-ground exemplar)*, picmal *(light, weak)*, radial *(light, geometry-only)* · **Audience:** pro/creative *(smallest native cluster — 3, coherence-flagged)*
- **Identity tokens:** **one hardcoded non-system accent** (the load-bearing token) · ground luminance **varies** (revone #171717 dark; picmal/radial light) · neon w/ genuine bloom (revone indigo #6155F5 spline glow) · Fitts-optimal pie/radial layouts (radial) · one-accent discipline (revone: indigo chart + one green delta)
- **Do:** let a single electric accent carry the surface on a neutral ground (dark or light). **Don't:** ship the default AppKit table with only a blue swap (picmal is logged "competent-but-almost-anonymous"); **don't** rely on this cluster for a *dark-ground* recipe — only revone evidences it.
- **Read for depth:** revone *(radial for geometry only)*

### Non-native contrast shelf *(instructive, never seeds canon)*
- **web-electron exemplars:** 1password (faithful macOS selection-duality *in* Electron; periwinkle field-labels), superlist, notion-calendar, craft, obsidian, cursor. **Lesson:** great Electron work reproduces native selection grammar and de-emphasis by hand — study the *result*, attribute nothing to canon.
- **Brand/marketing-register (44 apps, 1 native):** ajar, creavit-studio, mailtwin, pixelcasso, sero, zush… — apple.com mimicry, editorial serif display, glossy gradients. **Brand-evidence-only:** palette + icon, never UI tokens.

---

## Signature move bank
*(the raw material of distinctiveness — slug → move)*

| Slug | Move |
|---|---|
| caesura | The name *is* the system: a `//` caesura mark = logo + selection + status; one terracotta #B35A3C everywhere |
| autoshelf | Status-toggle-as-traffic-light: per-row green(on)/red(off) pill doubles as enable indicator |
| autoshelf | Rule-as-sentence subtitle: metadata reads as plain English ("Extension is .dmg · Move to Trash") |
| atlas | Chromeless shell — UI dissolved into 4 floating Liquid Glass islands over edge-to-edge imagery |
| atlas | Personable centred window title ("HELLO, ATLAS" / "869 ITEMS") — Photos schema made warm |
| cachesweep | Scale-as-hierarchy hero: ~36pt "120.3 MB" reclaimable figure answers the one question pre-attentively |
| spacepeek | Quick Look disguise — presents as a native spacebar-invoked Finder panel; ⚡ throughput proof pill |
| fantastical | Brand-red as typographic jewelry (the YEAR, TODAY cap, now-line) never as a fill |
| fantastical | Agenda/DayTicker pane *replaces* the list-of-calendars source list |
| finbar | Quantified menu tree: live count pill on every branch ("File 38", "Edit 16") |
| finbar | App-icon-as-search-context: target app's icon in the field's leading slot instead of a magnifier |
| klack | Two-material mood split: dark immersive catalog to choose vs light control panel to use |
| klack | Audition-before-commit rows: every row pairs a leading "+" with a trailing "▶" preview |
| open-timer | Session sparkline — a 7-bar histogram turns a one-shot timer into a glanceable daily dashboard |
| mux | Entire product surface is a single native NSMenu — zero custom chrome; restraint as character |
| orbs | Wheel-as-spatial-memory launcher: fixed wedges + hold-flick-release; number badges as expert path |
| radial | Fitts-optimal pie menu — every item the same short distance from the invoke point |
| hejour | Day-as-document title: the date *is* the page title; monochrome-plus-one-lime for "done" only |
| hejour | Dimmed inline markdown syntax — `##` persists in tertiary grey while the heading renders bold |
| noticky | Monochrome ink controls on coloured paper — checkboxes drawn as black ink, colour = filing identity |
| glyph | Heading-level gutter badges (grey "H1"/"H3" tags in the left margin) |
| forma | Monospace-everything on graph paper — full drafting-table commitment; hand-drawn bezier connectors |
| letterboxx | Data-viz as the sole boldness budget over disciplined system-default chrome; unread = weight + dot |
| keeby | Brand hue quarantined to the icon; selection/focus/primary all bind to system blue #0A84FF |
| lookaway | Signals the primary action by **luminance**, not accent hue, on a wallpaper-tinted warm glass panel |
| mac-4-breakfast | Telemetry-as-identity: raw 14.5 W / 8575 mAh / 32.6 °C promoted to primary hero type |
| code-meter | The meter *is* the metaphor: pixel/bitmap display face + dial gauges; dual-window ring+bar per row |
| compresto | Wallpaper-tinted whole-window glass; one candy-blue Compress bar with a cyan (not white) label |
| dropzone | Drag-target tile-grid *is* the product (Launchpad/Stacks metaphor as file destinations) |
| vocal-notes | Correct two-level selection: solid accent-blue knockout-white in focused list WHILE sidebar stays inset-gray |
| usage | Fixed per-metric identity palette (indigo=disk, blue=cpu) instead of the system accent; split menu-bar/window personality |
| sketch | Floating capsule toolbar — grouped opaque-white pill clusters (≤4 by function) over the canvas |
| bartender-6 | Hero header card per settings pane (icon tile + LargeTitle + one-line description) titles each config chapter |
| supaste | Content-type-aware clip cards on a true-black gallery backdrop; counted collections as capsule tabs |
| purge | Risk-tiered taxonomy (Safe/Check-First/All) + "710 photos or 355 songs" tangible-equivalent chips |
| maestri | Infinite canvas of *live* PTY/agent sessions as first-class nodes; colour-coded pipeline swimlanes |
| dynamiclake | Concave shoulder morph — island top corners flare OUTWARD into the menu bar (inverse radius) |

---

## Tells & corrections
*(most frequent non-native tells → the native fix. Contrast Dilution alone appears in **72 apps** — the corpus's dominant defect, across all lineages.)*

| Tell | Native correction |
|---|---|
| **Contrast Dilution** — secondary text <4.5:1, dividers/borders 8–15% (<3:1) | 85/50/25 label tiers; separators to ~29%; dividers from Fills tiers to ≥3:1 |
| **Faked / custom traffic lights** — grey dot rings on a card that isn't a window | Real NSWindow cluster (68×14) that colours on focus, mutes when inactive |
| **iOS density** — 40pt titles, 66pt action cards, 45pt buttons, 26pt checkboxes | Rg-24 control ladder, 13pt body, 16px push-button padding |
| **Gradient-as-accent** — pink→violet→blue decorative fill standing in for the accent | Single flat `controlAccentColor`; brand gradient only in icon/marketing |
| **Accent not system-bound** — hardcoded brand green/red on every control | Bind selection/focus/primary to system accent; quarantine brand hue to the icon |
| **Tracked-uppercase section headers** at heading size | SF Pro Semibold sentence/title case (tracked tiny-caps *eyebrow* only — see Contested) |
| **In-window hamburger** instead of the menu bar | Real menu-bar commands; window chrome stays native |
| **Selection-grammar drift** — blue-translucent fill + blue label | Flat gray inset (unfocused) OR solid-accent knockout-white (focused), radius 8 |
| **Glass-in-content** — Liquid Glass material behind body text | Glass on chrome/floating layers only; content surfaces opaque |
| **Non-native modality** — centred floating modal | Top-anchored native sheet |

---

## Contested
*(native apps genuinely disagree — both readings recorded; splits track cluster lines.)*

| Question | Reading A | Reading B | Verdict |
|---|---|---|---|
| **Section-header grammar** | Tracked-UPPERCASE eyebrow (10–11px, tertiary): caesura, satu, autoshelf, room-service, mole, cachesweep, fantastical | Sentence/Title-case Semibold 13pt: sketch, klack, foldervitrine, dropzone, letterboxx, finbar, bartender-6, grape, mux | Both native. Tracked-caps is native **only** at tiny eyebrow size + tertiary colour; at heading size it becomes a web tell. |
| **Accent source** | System blue is the accent (majority default): zipic, spacepeek, satu, cachesweep, macusb, vocal-notes, keeby, fantastical | One owned hue OR accent-withheld: caesura(terracotta), revone(indigo), room-service(orange), picmal(royal), atlas/grape/orbs/walltune/prostir/tono (neutral white) | Tracks cluster lines: **Content-Forward Gallery** withholds accent; **Warm** clusters own one hue; utilities default to system blue. All keep the *single-accent* canon — only the source differs. |
| **Section elevation** | Borders-as-elevation, no shadow (room-service, canary tonal steps) | Tonal fill-step elevation (grape, inkline inverted stack) | Both valid; shadow-free is the majority. |

---

## Knowledge gaps
- **Settings surfaces: only 8 in the whole corpus.** Empty-state 18, **onboarding just 2**, table 5. The corpus can specify a hero window far better than a preferences pane, an empty state, or a first-run flow. Bring settings + onboarding surfaces for the dense-pro clusters.
- **Single-surface bias:** only 16 of 66 native apps have ≥2 scorable surfaces — most tokens are `(inferred)` from one hero/marketing render, which over-indexes on hero styling. Multi-surface digests would promote many `(inferred)` → `(confirmed)`.
- **Marketing-composite contamination:** 101 of 209 surfaces are marketing composites; 25 apps are brand-only. Their tokens are brand/icon evidence, not UI canon — flagged per-app.
- **Mode imbalance:** dark 123 vs light 84 — the corpus is **dark-heavy**. Light-mode dense-pro evidence (the hardest to get right) is the thinnest slice.
- **Unknown lineage 34% (46 apps):** real UI, unverifiable framework — held out of canon entirely. Framework-tell captures would recover some.
- **Window corner radius still `(unknown)`** from the kit (layer-style masked); few clean screenshot measurements exist.
- **Out of scope:** motion, hover, transitions, responsiveness — static evidence only.

---

## Design-mode checklist
1. **Pick a cluster by audience match** (state choice + runner-up). Menu-bar Instrument · Warm-Editorial · Notch Native · Liquid-Glass Utility · System-Idiom · Terminal-Dark · Content-Forward Gallery · Warm Consumer · Electric Accent *(coherence-flagged; was "-Dark")*.
2. **Inherit the cluster's identity tokens**; fill gaps from Canon (above); fill remaining from `kit/macos-27.md` then HIG defaults `(assumed)` and disclose.
3. Build the layout skeleton from the nearest `patterns/` entries (toolbar, sidebar, list, floating-panel, card-grid, empty-state, inspector).
4. **Enforce canon before flourish:** 85/50/25 hierarchy · one accent bound to interaction · card 10–14 / panel 16–20 · 13pt body · real traffic lights · inset-rounded selection *(radius 8 is the clean-example value, not proven canon)*.
5. Audit against the 14-point rubric (macOS calibration); the #1 failure to pre-empt is **Contrast Dilution** — check every secondary label ≥4.5:1 and every divider ≥3:1.
6. **Lookalike check:** if the result would pass as caesura, atlas, klack, hejour, bartender-6 or another digested app's screen, differentiate deliberately (persona §6: inspiration, not cloning).
