# Canary Mail — profile

- **Source:** macapp.supply (`cover.png`, SHA-1 `aab493c8`) · **Surfaces digested:** three-pane main window (dark) — from the app window inside a marketing composite · **Last updated:** 2026-07-19
- **One-sentence identity:** Spark/Airmail's saturated cross-platform email language grafted onto a genuinely native macOS 26 shell — AI surfaced as a first-class, always-visible reading affordance.
- **Cluster:** unassigned (candidate: *prosumer-email-dark* — dark neutral ramp + one electric blue accent + avatar-forward rows)
- **Lineage:** native (med confidence) — real traffic lights, glass-grouped capsule toolbar with monochrome SF Symbols, textbook macOS source list with sentence-case headers and neutral inset selection. Content panes carry a custom, iOS-leaning brand skin (saturated selection card, avatar rows, card-thread reading view) layered on native chrome. Not Electron: the container-morphed glass toolbar groups read as real AppKit chrome.
- **Era (chrome):** Liquid Glass native (macOS 26/Tahoe) — evidenced by the rounded-capsule glass button *groups* (container morphing) in the toolbar. Glass hard to confirm in a marketing still; the grouped-capsule chrome is the tell.

## Scale note
Marketing render measured at **~1.67×** (traffic-light dot = 20px → native 12pt). All pt values below are render-px ÷ 1.67, hence `(estimated)` with wide bands. Flat fill hexes are clean `(measured)`.

## Tokens

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/sidebar | `#1B2124` (measured)(inferred) | | darkest pane, faint cool tint |
| bg/list | `#212A2E` (measured)(inferred) | | mid pane, faint cool tint — lightest of the three |
| bg/readpane | `#1E1E1E` (measured)(inferred) | | pure neutral; **matches kit dark window bg `#1E1E1E` exactly** |
| surface/card-readpane | `~#2A2A2A–#323232` (measured)(inferred) | | message + attachment cards, elevated neutral |
| sel/sidebar-fill | `#2C3235` (measured)(inferred) | | **native grammar** — flat neutral inset rounded fill |
| sel/list-card | `#2558C9` (measured)(inferred) | | **house style** — saturated indigo filled card, white text (Spark/Airmail-class) |
| accent/azure | `#0093FF` / glyphs `#0090FA` (measured)(inferred) | | filter-selected pill + sidebar glyph tint; ≈ kit system blue `#0091FF` dark |
| accent/indigo | `#2558C9` (measured)(inferred) | | list selection — a *second* blue, distinct hue from azure accent (see Defects) |
| identity/pip-magenta | `#FF00C3` (measured)(inferred) | | per-account unread pip (Sarrah) |
| identity/pip-cyan | `~#0AC2E8` (estimated)(inferred) | | per-account pip (Support) |
| status/pdf-red | `#D1291F` (measured)(inferred) | | attachment-type glyph |
| text/primary | `~#DFDFE0` (measured)(inferred) | | near-white on dark, contrast >12:1 |
| text/secondary | mid-gray (estimated)(inferred) | | counts, "To:", "63 KB", section headers |
| type/subject-header | ~22–24pt Bold (estimated)(inferred) | | reading-pane conversation title (Title1/near-LargeTitle) |
| type/body-read | ~13–15pt Regular (estimated)(inferred) | | email body; reads native-plausible, not iOS 17pt |
| radius/card | ~12–14px render → ~7–8pt (estimated)(inferred) | | list card + summarize card + attachment chip |
| radius/pill | capsule (estimated)(inferred) | | filter chips, toolbar button groups |
| chrome/sidebar | ~140pt wide, full-height, source list (estimated)(inferred) | | **compact** — narrower than kit's 256pt example |
| chrome/traffic-lights | 12pt dots, coloured (window focused) (measured)(inferred) | | genuine, top-left |
| toolbar/groups | glass capsule button groups, borderless SF Symbols (measured)(inferred) | | list region: 1 group of 3; read region: 4 groups |

## Layout skeletons

**Three-pane main window (dark):**
- **Sidebar (~140pt, `#1B2124`):** account header ("Sarrah", gray semibold + magenta pip) → Inbox (selected: neutral inset fill, blue inbox glyph, "2904" count trailing) / Sent Mail / Labels ⌄ / More ⌄ → section header "Favorites" → second account "Support" (+cyan pip) → Inbox / Assigned / Mentions / Analytics (all blue glyphs) → bottom status footer "Last updated 12:40 pm" + spinner. Sentence/title-case headers throughout.
- **Message list (`#212A2E`):** horizontal filter chip row (All [azure-filled] / Primary / Promotions / Social / Updates…, scrolls) → rows of `avatar circle + sender (bold) + greeked subject/preview bars`; the selected row swaps to a **saturated indigo filled card** with real sender/subject/truncated preview.
- **Reading pane (`#1E1E1E`):** large bold subject header → full-width **"Summarize this conversation"** AI card (blue sparkle glyph) → message cards: `avatar + sender + paperclip · To: recipient ⌐ · 1px rule · attachment chip (red PDF glyph, name, size) · body · "Sent from Canary" (blue link)`; quoted thread below.
- Toolbar spans all panes: [traffic lights][sidebar-toggle] · list region {✓ · sparkle-AI · summary} · divider · read region {compose} {reply/reply-all/forward} {snooze/pin/⋯} {search}.

## Signature moves
- **[GOLDEN-NUGGET] AI as a persistent, full-width inline reading affordance** — "Summarize this conversation" sits at the top of every thread (plus a sparkle action in the list toolbar), not buried in a menu. The whole product thesis stated in one always-visible card.
- **Saturated indigo selection card** (`#2558C9`, white text) — the active thread is the single Von-Restorff "different thing"; strong pre-attentive pop against the muted panes. Systematic within the list and accessible → a signature, not a defect (its *inconsistency with the sidebar's* selection is the defect).
- **Triple-tone pane elevation without borders** (sidebar `#1B2124` → list `#212A2E` → read `#1E1E1E`) — depth by tonal steps, no dividers.
- **Avatar/memoji-forward list rows** — a consumer-social warmth uncommon in pro mail chrome.

## Defects
- **Inconsistent selection grammar** → sidebar uses native flat neutral inset fill (`#2C3235`) while the message list uses a saturated indigo filled card (`#2558C9`). Two selection languages in one window; canon wants one flat accent-tinted inset fill everywhere.
- **Two-blue accent split** → list selection indigo `#2558C9` vs filter/glyph azure `#0093FF`/`#0090FA`. Near-miss hue deviation (perception flags small differences hardest); accent should bind to one hue.
- **Line Length Fatigue (potential)** → reading-pane body appears to run full-width with no ~65ch readable-content cap; the composite crops the line off-edge, so the real measure is longer still. Flag pending an un-cropped shot.
- **Pane tone-temperature drift** → sidebar/list carry a faint cool tint; reading pane is pure neutral `#1E1E1E`. Minor.

## Aesthetic
- **Adjectives:** saturated · avatar-social · AI-forward.
- **Direction:** neo-grotesque product (dark neutral ramp + one electric accent) warmed toward consumer-social by avatar rows, rounded cards, and a saturated selection — not the restrained Linear register.
- **Peers:** Spark, Newton Mail, Airmail (the saturated-blue selected card is their shared dialect); Superhuman for the speed-tool chrome, but Canary is warmer/more coloured.
- **Audience:** consumer-utility tipping to prosumer (AI, Assigned, Mentions, Analytics = team/pro features).

## Psychology
- **Von Restorff / signal-detection** — saturated selection card makes the active thread the one different element; used well.
- **Fogg reduction** — "Summarize this conversation" reduces reading effort; AI as an ability-lever, not motivation copy.
- **Jakob's Law** — canonical three-pane mail layout matches trained expectations.
- **Miller/Cowan chunking + progressive disclosure** — sidebar chunked into account sections; Labels ⌄ / More ⌄ / See More collapse depth.
- **Hick's Law (mild tension)** — deep sidebar + 5+ filter chips is high option-density; acceptable as an expert workspace (option density is a feature there), but a lot to scan.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| main window (dark, three-pane) | 13/14 | #6 line length (reading body full-width, no ~65ch cap — composite-cropped, likely worse). #14 focus not assessable in a static render. |
| main window — native-tells | 9/10 | #3 selection grammar (list = saturated indigo card, not native flat inset fill; sidebar conforms). |
