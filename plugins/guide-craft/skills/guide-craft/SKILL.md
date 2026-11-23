---
name: guide-craft
description: Build a season guide for a live-service game, shipping a multi-page static website and a native iPhone app from one dataset, with interactive tools, tactile shaders, a live voice guide, and narrated briefings, then deploying to Vercel and TestFlight and iterating with the owner. Use when asked for a season guide, companion app, meta tracker, or field guide for a game's current season ("make a season guide for <game>", "a companion app for this season", "what's the meta, as an app"), or when an existing guide needs a balance update or new season folded in. Supports shooters, hero shooters, battle royales, card games, racing, sports, action role-playing games, and fighting games. Carries the complete research, content, statistical provenance, App Store compliance, and polish blueprint distilled from both MW4 Season 1 sessions (17 to 23 November 2026) plus cross-genre API and policy research across eight genres. Not for a single static article, and not for building a game.
---

# Guide Craft

A season guide answers one question for a player between matches: **what is strong right now, and what should I do about it?** Everything in the product supports getting that answer in two taps, with sources and provenance badges proving why it can be trusted.

This skill reproduces the full research depth, content breadth, and multi-surface polish of the Call of Duty: Modern Warfare 4 (MW4) Season 1 build (17 to 23 November 2026: 16 web pages, 5 native iOS tabs plus full-screen voice, 7 interactive widgets, 4 bespoke Metal/WebGL shaders, 250 resolved sources, 62-defect audit, ~40 owner rounds, and 14 TestFlight builds), generalised across eight live-service genres with cross-genre official API, statistical validity, and App Store IP rules from a three-family research corpus in `docs/deep-research/`. Load the four stage playbooks in `references/` when entering their stages; measured figures and source provenance sit in `references/evidence.md`. Four deterministic gate scripts ship in `scripts/`.

Deliver the surfaces the owner asks for, at the scope intended. Each delivery surface (website, iOS app, live voice guide, narrated briefings, opening shaders, custom app icon) is optional; the single dataset, primary-source research bar, and compliance gate are required for any surface you ship.

## Terms used in this file

- **Brief**: the home page of the website and tab 1 of the app, structured as a season briefing.
- **Meta pick**: the weapon, hero, deck, build, car, or fighter that current evidence marks strongest for a role.
- **Balance update**: a publisher patch changing gameplay numbers (avoid labels colliding with game systems, such as `"weapon pass"` reading like `"battle pass"`).
- **Provenance badge**: a mandatory label naming how a metric was obtained: `official_telemetry`, `ladder_snapshot`, `pc_opt_in_tracker`, `lab_measurement`, or `editorial`.
- **Source id**: `r1` through `rN`, one identifier per source, cited inline as `[[rN]]` and resolved at build time.
- **Season strip**: the status bar showing current season day, official start date, and end date (or `"expected"` when unannounced).
- **Voice guide**: the out-of-match spoken assistant in the app and on the site (Overwatch in MW4).
- **Delegation**: the live voice model handing a deep question to a fast text model holding the full guide.
- **PC**: Windows gaming personal computer, in scope only when graphics settings or frame-rate estimates are requested.
- **Acronyms**: **AI** (Artificial Intelligence), **API** (Application Programming Interface), **CLI** (Command-Line Interface), **CSS** (Cascading Style Sheets), **DNS** (Domain Name System), **FPS** (Frames Per Second), **GPT** (Generative Pre-trained Transformer), **GPU** (Graphics Processing Unit), **HTML** (HyperText Markup Language), **HTTP** (Hypertext Transfer Protocol), **HUD** (Heads-Up Display), **JSON** (JavaScript Object Notation), **MCP** (Model Context Protocol), **MMO** (Massively Multiplayer Online game), **MOBA** (Multiplayer Online Battle Arena), **OFL** (Open Font License), **PRD** (Product Requirements Document), **RPG** (Role-Playing Game), **SVG** (Scalable Vector Graphics), **TTK** (Time to Kill), **UDP** (User Datagram Protocol), **UI** (User Interface), **URL** (Uniform Resource Locator), **UX** (User Experience), **VRAM** (Video Random Access Memory), **WebGL** (Web Graphics Library).

## Output format

Return three deliverables for a full build, or the subset matching requested surfaces:

1. **Git repository** with one data source feeding all surfaces: `build/` (dataset, scraped caches, website generator), `guide/` (generated HTML, hand-written CSS/JavaScript, explainer media), `assets/` (renders, cutouts, icons, map art), `ios/` (XcodeGen `project.yml`, `export_data.py`, `DESIGN.md`, SwiftUI/Metal sources, tests), `web/` (Vercel voice/API proxy routes, shared guide/voice libraries, audio/probe scripts, tests), `audio/` (hash-cached source clips, mixed outputs, manifest), `docs/` (overview, PRD, AI model usage, deployment, read-only `deep-research/` and `transcripts*/`), and `design/icon/` (generated takes, 1024 px master, provenance `README.md`).
2. **Deployed surfaces**: a live production website URL verified with cache-busted HTTP checks, and a `VALID` TestFlight build in the owner's internal tester group.
3. **Owner round reply** (2 to 6 lines of plain prose, or a refreshed `STATUS.html` plus 2 lines via `status-update:status-update` for portfolio projects): what changed in player-visible terms, where it is live, which checks ran, what could not be verified on this host, and any single item waiting on the owner.

## Twelve decisions that shape the product

1. **Open on the season briefing, and split into a multi-page site.** Lead with current meta, how the season plays, player sentiment, favourite maps, and news. A single three-reading dossier grew to 40,834 px desktop / 77,118 px mobile; gamers need a multi-page brief site with settings and calculators on dedicated pages/tabs. Launch the app on tab 1 (`Brief`) without persisting the last tab.
2. **Choose the compliant data plane for the genre.** Never build a universal scraper or embed publisher API keys in an iOS binary. Use one of four compliant tiers: backend-proxied official OAuth/keyed REST APIs, client-side clipboard codecs plus local 60 Hz UDP telemetry, MediaWiki Cargo community wikis, or clean-room editorial plus empirical lab tests when no match API exists.
3. **One dataset feeds all three surfaces.** One generator produces the website HTML, exports `guide.json` for iOS and the voice backend, and drives narration scripts. Compute recommendations and item counts dynamically so counts never drift.
4. **Hit the research and statistical validity bar before building.** Count independent publishers (`scripts/audit_sources.py`: 1 vote per YouTube channel, 1 per publisher, cloned stat sites collapsed to 1, automated runs 0). Target `>=2` independent publishers per core call and 0 `low confidence` core classes. For telemetry win rates, attach a provenance badge plus rank bracket and sample `n`, partition by `(client_version, balance_hotfix_timestamp)`, adjust for rank-bracket/72-hour lookahead skew, and sort by 95% Wilson lower bound with `n >= 50`.
5. **Split copy by surface from the same row.** Web and voice lookup carry full evidentiary prose (`why`, creator counts, stat-site ranks); the mobile app states what a pick does in 1 to 2 sentences (`brief`) with one deduplicated `PageSources` control per page or section. Pair every clipboard build/deck code with a visual slot-by-slot card on mobile so console players do not have to type 14-character strings.
6. **Mirror exact in-game menu structure and vocabulary.** Use the game's real settings tabs and labels, independent per-area sliders, and purpose-named presets (`Max detail`, `All-rounder`, `Lean`, `Ranked`, `Max FPS`, never `"Looks great"`). Sweep variant phrases when renaming colliding terms.
7. **Ground season dates in publisher announcements.** Mark unannounced end dates `"expected"` (`endConfirmed: false`) with estimator source, compute live progress in the publisher's timezone, and keep a static build-day CSS fallback.
8. **Isolate gameplay modes, anti-cheat rules, and out-of-match voice boundaries.** Strip campaign presets, campaign-only sliders, and sister-mode notes from core multiplayer tables. Exclude modded upscalers, library swaps, ReShade, injectors, and client memory reads. Keep live voice assistants strictly out-of-match (or 60 Hz local UDP sim-racing telemetry), never tracking enemy cooldowns or dictating live PvP decisions.
9. **Use a briefing-first voice guide.** Pack a ~10,700-token `liveBriefing()` inside GPT-Live's `session.instructions` (under its 16,384-token cap, gated by `scripts/check_briefing.py`) so routine questions answer in ~0.1 s instead of ~3.3 s, delegating only omitted depth to Haiku.
10. **Clear Apple 4.1(c), 4.2, 5.2 and publisher IP rules before naming or monetizing.** Run `scripts/check_compliance.py` before creating an App Store record: default to an original ownable app name and original icon (avoiding publisher trademarks in the app name and studio-lookalike AI icons), ship genuine native utility rather than a WebView wrapper, match the publisher's exact disclaimer and monetization rules (Riot, Blizzard, Bungie, EA, Capcom, GGG, Valve, Epic, Activision differ sharply), and never place ads in voice responses or game overlays.
11. **Data decides meta picks; the owner decides taste.** Bring numbers for picks and probability pushbacks instead of polling the owner. Route name, narrator voice, live voice, icon, spend, and publication through `clarify:clarify` with 2 to 7 concrete samples.
12. **Gate invariants with bundled scripts and visual contact sheets.** Run `scripts/check_html.py`, `scripts/audit_sources.py`, `scripts/check_briefing.py`, `scripts/check_compliance.py`, 2 to 4 s standalone `swiftc` JSON decoding, Scribe transcripts, 4-pass browser scroll captures, and simulator contact sheets on every round.

## Adapting to the genre

Keep the section order and interactive architecture; swap the nouns, codecs, and data plane for what the game actually has.

| Section | Shooter (MW4) | Hero shooter / MOBA | Battle royale | Card / autobattler | Racing | Sports | Action RPG / MMO | Fighting |
|---|---|---|---|---|---|---|---|---|
| Primary data plane | clean-room lab + patch notes | Riot / OpenDota official API | PUBG API or clean-room lab | Battle.net / Riot TFT / deckstrings | iRacing OAuth / 60 Hz UDP | closed partner API or editorial | PoE / Battle.net OAuth + ladder | MediaWiki Cargo frame wikis |
| Share artifact | 14-char Gunsmith code + 5-slot card | item/rune order list | loadout code + 5-slot card | Base64 varint deckstring | car setup notes | squad / tactics card | PoB Base64 zlib XML / WoW talent string | move notation / combo route |
| Meta picks | gun per class + build | hero per role + build | weapon pair + drop | deck archetype + list | car per class + tune | team / formation + tactics | build per class + gear | character + key moves |
| Detail page | build, unlocks, TTK by range | abilities, counters, bracket WR/PR/BR | weapon stats, rotations | card list, mulligan, IWD/matchups | tune values, lap delta | ratings, SBC/market toggle | skill tree, gear, clear speed | frame data, Classic/Modern splits |
| Mechanics explainer | netcode / bullet-sponge timeline | damage / crowd-control simulator | zone / rotation timing | Monte Carlo combat / draw odds | slip-angle / tyre-wear curve | stamina / chemistry math | damage-bucket calculator | frame-trap / gap timeline |
| Maps | layout, hills, spawns | map pool, objectives | drop zones, circle pulls | board or omit | tracks, lines, braking | stadiums, conditions | zones, bosses | stages |
| Settings | graphics sliders, GPU estimator, HUD | graphics, controls, binds | graphics, audio, controller | omit | wheel, assists, camera | controls, camera | graphics, keybinds | input delay, display |
| Sentiment & news | Steam/Reddit + balance updates | same + pro scene + hotfixes | same + map changes | same + server hotfixes + bans | same + track drops | same + roster updates | same + league mechanic | same + fighter patches |

Omit graphics settings for console-only or mobile-only games, and omit hardware estimators unless the game runs on PC.

## Inputs to confirm first

Confirm these 6 inputs in one round through `clarify:clarify` (linting JSON with `scripts/lint_questions.py`), then record them in `CLAUDE.md`:

1. Game title, publisher, target platforms, and exact modes covered (determines data plane and publisher IP/monetization rules).
2. Official season start date with publisher URL, and whether an official end date exists.
3. Whether graphics settings, PC hardware estimates, and handheld/laptop benchmarks are in scope.
4. Which of the 6 delivery surfaces to build: static website, native iPhone app, live voice assistant, narrated audio briefings, opening shader animation, and custom app icon.
5. Monetization posture (free, web ads, or subscriptions: gated against the publisher's policy) and monthly spend ceiling for generated imagery, audio, and live voice sessions.
6. Hosting account and custom domain, plus Apple developer profile and team (read `~/.config/app-store-connect/accounts.md` first).

## Stage 1: Set up the project

- Apply the matching parts of `create-swe-project:create-swe-project`: `CLAUDE.md` (`AGENTS.md` symlinked to it), `OVERVIEW.md`, `PRD.md`, `docs/AI-MODEL-USAGE.md`, `docs/DEPLOYMENT.md`, unit/UI test targets, and git.
- Load `opus-5-guide` before writing instruction files, write instruction files through `agent-voice:agent-voice`, and qualify skill names as `plugin:skill` (or exact command name like `opus-5-guide`). For prose under a human byline, route through that person's voice skill (such as `create-luke-content:create-luke-content`).
- Take a pre-edit tarball backup or baseline commit before refactoring an existing guide.
- Register the project via `armada-sync:armada-sync` and keep `STATUS.html` synced via `status-update:status-update` when it sits in the owner's portfolio.
- Keep secrets in gitignored `web/.env.local` and `ios/Secrets.xcconfig` (escape URL slashes as `/$()/` in `.xcconfig`) or the owner's secrets broker; compare keys by SHA-256 digest and never print values. Commit locally after each stage; push only when asked.

## Stage 2: Research, scrape, audit and hit the confidence bar

Load `references/research-playbook.md` and `references/cross-genre-apis-and-compliance.md` before running this stage.

1. **Confirm the legal data plane first:** check the publisher's API portal, rate limits, TTL caps, and fan-content policy in `references/cross-genre-apis-and-compliance.md` before scraping or registering keys.
2. **Diverge first (`trawl:trawl`):** run 5 parallel divergent frames before writing briefs to surface non-obvious angles (temporal artefacts, CPU knees, frame-gen latency floors, anti-cheat mod boundaries, hotfix version traps).
3. **Triangulate across 5 source tiers and 10 tracks:** publisher notes and launch art blogs -> official telemetry or lab/firing-range measurements -> dated stat sites (embedded JSON/SSR) or Cargo wikis -> YouTube transcripts spanning both meta channels and frame-counting testers (plus chapter-guided 2–3 s overlay frame grabs for silent benchmarks) -> 200 to 500+ post-launch Steam reviews and subreddit threads.
4. **Deduplicate, audit, and upgrade confidence:** run `scripts/audit_sources.py` and the 10-class content audit (collapsing cloned stat sites, separating per-match vs per-player anti-cheat math, correcting rank-bracket lookahead and low-sample skew, testing visibility alongside FPS cost). Trigger a Round-2 class-by-class deep dive whenever any core class remains at `low confidence`.
5. **Update after patches with two file-fenced agents:** Agent 1 (read-only) writes the `(file, table, current, replacement)` change list plus `AS_AT` set to newest patch read; Agent 2 (fenced strictly to generator files) applies it and centrally overrides stale build-card kill times.

## Stage 3: Build the single-source dataset, calibrated models and gates

Load `references/page-and-app-blueprints.md` and `references/cross-genre-apis-and-compliance.md` for exact row shapes, build/deckstring codecs, statistical smoothing, and the calibrated damped FPS formula (`DAMP ≈ 0.55–0.575`, 6% mean error across 11 checks).

- Feed 100% of web pages, `ios/FieldGuide/Resources/guide.json`, `web/data/guide.json`, and voice/narration generators from `build/build.py` + `build/site.py` + `ios/export_data.py` via one `scripts/build-web.sh`. Keep all publisher API keys on backend proxy routes, never inside the iOS bundle.
- Keep `guide.json` strictly additive (`Optional` fields in Swift), export untested numeric cells as `null` (never `""`), strip `<sup>` tags before generic HTML stripping, partition telemetry by `(client_version, balance_hotfix_timestamp)`, and derive item counts dynamically from `guide.json`.
- Gate every build on: `scripts/check_html.py` (nested `<a>`, digit-leading ids, missing images, unresolved `[[rN]]`), `scripts/audit_sources.py` (unresolved ids, deduplicated publisher counts, zero low-confidence core picks, Wilson lower bound and `n >= 50` floors), page-existence assertions, and a 2 to 4 s standalone macOS `swiftc` `guide.json` decode harness.

## Stage 4: Author the full multi-page site, 5-tab app and 7 interactive tools

Load `references/page-and-app-blueprints.md` for the complete blueprint of every page, iOS tab, interactive widget, copy rule, Duo fold layout, and the 6-surface Empty/Ideal/Overflow/Error state matrix.

- **Website (16 pages grouped into 5 JS-free `<details>` nav menus + phone sheet):** Season Briefing (`index`), Interactive Settings Workbench, Frame Rates & Card Advisor, Secondary GPU Vendor page, Portable/Handhelds & Laptops, Upscalers Comparison, Meta Picks / Arsenal, Complete Loadouts / Kits, Pros & Streamers, Combat/Controls/Audio/HUD, Signature Mechanics Explainer, Tips & Movement, Maps / Tracks, Integrity / Cheating, Players Say, and Auditable Sources. Omit PC hardware pages on console/mobile titles.
- **iOS app (5 tabs + full-screen Voice cover + persistent search + mini-player accessory):** `Brief` (7-block season briefing matching web home with a patch+hotfix freshness pill), `Arsenal` (cutout weapon/item cards, play-style switcher, inspect plate, visual build + copyable share code, TTK/stat chart), `Settings`, `Field` (maps with 3D table, mechanics calculator, tips, pros), `Intel` (integrity odds calculator, players say, searchable sources, launch-sound settings), plus non-scrolling `VoiceScreen` and top-centre `CommsStrip` / `CommsLog`.
- **Seven interactive tools (progressive-enhancement on web, native SwiftUI on iOS):** (1) 6-area Settings Workbench with presets & clipboard copy, (2) Best-Settings-For-Your-Card Advisor, (3) Play-Style Switcher + scrubbable TTK/Matchup Chart + Agreement Matrix + build/deckstring codec, (4) 3D Tactile Inspect Plate, (5) Interactive 3D Map Table, (6) Three-Clock Mechanics/Netcode Timeline Simulator + Fight-Length Calculator, (7) Interactive Integrity / Lobby-Odds Calculator & Curve.

## Stage 5: Craft the visual system, tactile interactions, shaders and icon

Load `references/polish-and-ship-playbook.md` for exact token recipes, shader mechanics, Mobbin extraction steps, icon rubric, and web/iOS layout traps.

- **Design craft & Mobbin (`design-craft:design-craft`, `ux-craft:ux-craft`, `duo-craft:duo-craft`):** adopt visitor mode **Read, with Operate habits**. Trawl Mobbin across 4 UI archetypes (readout spec sheet, split-view reading guide, ranked tier list, settings), documenting a **Take / Leave** table in `ios/DESIGN.md`. Derive a game-native palette with a 4-step shadowless tonal surface ramp (`bg`, `bg2`, `panel`, `panel2`), hairlines, 4 pt spacing grid, 4 pt/8 pt square-edged corners, 3 bundled OFL fonts (condensed uppercase display, humanist sans body, tabular mono figures), a strict **2-hot-accent-per-screen cap**, dedicated measured-figure colour, and shape+word status marks. Explicitly exclude purple/neon gradients, cream/off-white editorial defaults, glass cards on content panels (system Liquid Glass stays on tab bar/toolbars/mini player only), emoji, rainbow tier-letter badges, drop shadows, publisher marks, and self-awarded `"verified"` badges.
- **Tactile iOS motion, shaders & haptics:** build 4 stitchable SwiftUI Metal shaders receiving palette colours from `Theme.swift` (`uplink` launch iris reveal, `commsOrb` audio-reactive comms scope, `benchGrid` tilt-lit bench, `scanReveal` chromatic title sweep). Pair with attitude-relative `CoreMotion` `MotionTilt`, `InspectPlate` (Vision foreground cutouts via `scripts/lift-guns.sh`, dynamic shadow, specular metal glint, UIKit `HorizontalPan`), 3D Map Table (50° layback, drag/pinch/double-tap), `.contentTransition(.numericText())` rolling figures, `revealOnScroll()` `scrollTransition`, scrubbable Swift Charts, and purposeful haptics.
- **Web motion, data viz & icon (`dataviz`, `visualization:visualization`, `motion-craft:motion-craft`, `create-website:create-website`, `create-mac-icon:create-mac-icon`):** mirror `uplink` as a once-per-session WebGL opening boot + hero layer with 3D-racked WebP cutouts (1 full-strength render at 390 px), gated by `scroll_capture.mjs` (4 passes). Build inline dark SVG charts (polylines, `<=5` series, `3:1` mark contrast, no radar charts) and GSAP scrubbable timeline explainers with reduced-motion fallbacks. Generate 6 original, non-impersonating icon takes across 2 directions via `media-gen-pro` (GPT Image 2.6 Flare), judge at 280/64/40/32/29/16 px + greyscale against the 12-point rubric (`>=10/12`, 0 failures on checks 1 to 4), and reuse as favicon and touch icon.

## Stage 6: Build the two-tier live voice guide

Load `references/polish-and-ship-playbook.md` for AI Gateway auth, AI SDK v7 syntax, Haiku tuning, Swift 6 `nonisolated` microphone tap code, and security controls.

- Pair `openai/gpt-live-1.1` (WebSocket + client delegation via Vercel AI Gateway, monthly-capped `AI_GATEWAY_API_KEY`, server-controlled `audio.output.voice`, `<50,000`-char `liveBriefing()` in `session.instructions` gated by `scripts/check_briefing.py`, 500-token `thinking.append` screen context) with prompt-cached `anthropic/claude-haiku-5.5` (`maxOutputTokens: 400`, thinking disabled, `<=70` words, first-person prompt) for omitted depth.
- Keep voice assistance strictly out-of-match (or local 60 Hz UDP sim-racing telemetry) with zero ads in voice responses and zero cloned character/actor voices. Wait up to 2 s (`400 ms` quiet) for `input_transcript.delta` before delegating, normalize speech-recognition numbers, inject matched hardware lines with explicit `reachable`/`NOT reachable` phrasing, test via mic-less `voice-probe.ts` measuring `afterResult`, and arm the iOS microphone tap against Swift 6 audio-thread crashes via offline `AVAudioEngine` rendering.

## Stage 7: Produce narrated briefings, launch radio comms and blind audio QA

Load `references/polish-and-ship-playbook.md` for exact ElevenLabs pricing, ffmpeg radio filter chain, and playback scrubber rules.

- Generate hash-cached briefings (`brief-season`, per-class, per-map), a two-voice muffled launch radio exchange over a custom music sting (`450–2700 Hz`, `tanh(3.2)`, 9-bit `acrusher`, sidechain ducking, `-16 LUFS`), and broadband push-to-talk channel clicks (`gen-audio.mjs`). Defer the full narration batch until after Stage 2's audit; run `--dry` and report cost first.
- Verify every generated clip without ears using 4 checks: `elevenlabs/scribe-v2` transcription, `ffmpeg` loudness/waveform PNGs, `google/gemini-3.8-flash` mix critique (`maxOutputTokens: 3000`), and Python/NumPy spectral flatness plus pitch, while letting the owner choose narrator and live voices by ear from audio samples.
- Drive app progress with a 10 Hz observed `position` clock, UIKit sideways-gated `Scrubber` (`hitHeight: 18` in mini player), `.ambient` for auto launch comms vs `.playback` + Stop + captions for user-tapped replay, and verify web seeking on HTTP `206` Range-capable hosting.

## Stage 8: Ship to web and TestFlight

Load `references/polish-and-ship-playbook.md` and `references/cross-genre-apis-and-compliance.md` for Vercel, Namecheap, `provision-app.sh`, `asc`, and App Store compliance commands.

- Build via `scripts/build-web.sh`, run `scripts/check_html.py`, deploy with `vercel deploy --prod --scope <team> --yes`, verify previews via `vercel curl` and production via `?x=$RANDOM`, and configure `MW4APIBase` + `MW4APIFallback` in `Secrets.xcconfig` so TestFlight works pre-DNS.
- Run `scripts/check_compliance.py` on the app release manifest before creating any App Store record: verify original naming under Apple 4.1(c), 30-character name/subtitle caps, required publisher disclaimer, compliant monetization, and zero unlicensed game art in App Store screenshots.
- Ship iOS builds through `app-store-connect:app-store-connect` (`accounts.md`, `CURRENT_PROJECT_VERSION` bump, `xcodegen`, manual signing, `PlistBuddy` `CFBundleDisplayName` check, `asc builds upload --locale en-US --test-notes`, verify `VALID`, group builds via `--group-id`, tester `INVITED` status), survey category collisions via the iTunes Search API before proposing 2 names through `clarify:clarify`, and ship a dismissible `"Coming soon to the App Store"` web banner until release.

## Stage 9: Verify visually and iterate with the owner

Load `references/polish-and-ship-playbook.md` for the full test inventory, Duo multi-display/Device Hub protocol, browser/linter checklists, macOS zsh hygiene, and the 22-row consolidated failure-mode table.

- **Visual critique loop:** never declare a screen done from unit tests alone. After every UI or content change, capture all web pages at `1440 px` and `390 px` plus `javaScriptEnabled: false` (probing inner `.tblwrap` widths, running `ux-lint.py --static`, `design-lint.py guide/site.css`, computed WCAG contrast, and 4-pass `scroll_capture.mjs`), and capture simulator tours (`--display=1`/`3` + `-split` + `magick montage`/`ffmpeg hstack` sheets + `recordVideo` launch clips) with Mac audio muted. Open every sheet, fix wrapping, clipping, contrast, and phrasing defects before showing the owner, then ship web + TestFlight, commit locally, refresh `armada-sync:armada-sync` and `status-update:status-update`, and reply in 2 to 6 lines.

## Bundled deterministic scripts (`scripts/`)

Run all four gates on every release; each ships a `--self-test` suite verifying both failing and passing fixtures:

- `python3 scripts/check_html.py <guide_dir>`: catches nested `<a>` links, digit-leading ids, unresolved `[[rN]]` tokens, and missing local image assets.
- `python3 scripts/audit_sources.py <audit.json>`: verifies source resolution, independent-publisher deduplication, zero low-confidence core picks, rank/patch telemetry tags, `n >= 50` floors, and 95% Wilson lower bounds.
- `python3 scripts/check_briefing.py --briefing <txt> --entities <json>`: enforces GPT-Live's `<50,000`-char / `<14,000`-token ceiling and 100% entity retention.
- `python3 scripts/check_compliance.py <release-manifest.json>`: checks Apple 4.1(c)/5.2.1/5.2.2, 30-char name/subtitle limits, required/forbidden publisher disclaimers, monetization legality, binary key isolation, and memory-read bans across 9 major publishers.

## Skills and tools by stage

| Stage | Skill or tool | Role in MW4 / cross-genre builds |
|---|---|---|
| Setup | `create-swe-project:create-swe-project` | `CLAUDE.md`, `OVERVIEW.md`, `PRD.md`, `docs/`, test targets, git |
| Setup | `opus-5-guide`, `agent-voice:agent-voice`, `create-luke-content:create-luke-content` | Instruction files linted against current guidance; owner-byline voice lint where requested |
| Setup | `armada-sync:armada-sync`, `status-update:status-update` | Portfolio manifest entry and living `STATUS.html` dashboard refreshes |
| Research | `dossier-report:dossier-report`, `trawl:trawl`, Dossier MCP | Phase 0 divergent framing (5 frames), claim-graph discipline, multi-backend CLI/API panels |
| Research | `WebSearch`, `WebFetch`, `agent-browser`, `yt-dlp`, `curl` + Chrome UA, `ffmpeg`/`magick` | Official patch notes and blog art, official APIs, Cargo wikis, Steam/Reddit feeds, YouTube VTT transcripts, overlay frame grabs |
| Research | File-fenced subagents / parallel CLI extractors (`codex exec`, `grok -p`) | Round 1/2 class research tracks, 62-defect content audit, patch change list, generator-only apply pass |
| Design | `design-craft:design-craft`, `ux-craft:ux-craft`, Mobbin MCP | Web and iOS visual/navigation systems, Mobbin Take/Leave sheets, `ios/DESIGN.md`, `ux-lint.py`, `design-lint.py` |
| Design | `dataviz`, `visualization:visualization`, `motion-craft:motion-craft` | TTK charts, agreement matrices, scrubbable timeline explainers (GSAP + reduced-motion), optional film |
| Design | `duo-craft:duo-craft` | Foldable iPhone Duo split-pane layout (`UIView.reservedRegions`, `UIHingeInteraction`, 6-of-9 pose matrix) |
| Design | `create-website:create-website` | WebGL opening shader rules (`hero-media.md`) and 4-pass `scroll_capture.mjs` |
| Design | `create-mac-icon:create-mac-icon` + `media-gen-pro` | Direction catalogue, dark corpus references, 12-point rubric, 6 GPT Image 2.6 Flare takes, explainer video |
| Voice | Vercel AI Gateway (`openai/gpt-live-1.1`, `anthropic/claude-haiku-5.5`), `braindump:braindump` | Out-of-match live WebSocket voice, cached delegation, briefing retention-test discipline |
| Audio | Vercel AI Gateway (`elevenlabs/eleven-v4`, `eleven-flash-v2.5`, `sound-effects-v2`, `music-v2.5`, `scribe-v2`), `google/gemini-3.8-flash`, `ffmpeg` | Hash-cached narration, radio comms mix, Scribe, Gemini, and audio-signal blind QA |
| Ship | Vercel CLI (`vercel deploy`, `vercel curl`, `vercel logs`) | Production website, API proxy routes, preview checks, and voice serverless routes |
| Ship | `app-store-connect:app-store-connect` (`asc`, `provision-app.sh`), XcodeGen, `PlistBuddy` | Bundle/app record, manual signing archive, compliant store listing metadata, TestFlight builds |
| Verify | Bundled `scripts/*.py`, XCTest, standalone `swiftc` harness, Playwright Chromium, `agent-browser`, `xcrun simctl` | Mechanical HTML/source/briefing/compliance gates, 9 unit + 5 UI tests, 2–4 s decode gate, desktop/mobile sweeps, Duo and video captures |
| Iterate | `clarify:clarify` (`lint_questions.py`, `AskUserQuestion`) | Owner choices for app name, narrator, live voice, banner destination, Device Hub control, and scope |

## Constraints

- **Unofficial and compliant, always.** Exclude publisher logos, trademarks in the app name (Apple 4.1(c)), unlicensed game art in App Store screenshots, and voice cloning; pass `scripts/check_compliance.py` before shipping.
- **Confirm before spending or publishing.** Report estimated costs before billed generation or paid research, and get an explicit yes from the owner before creating permanent App Store records (unless TestFlight deployment already authorized it), submitting to App Review, enabling public beta, releasing, buying a domain, driving Device Hub mouse input, or pushing git commits.
- **Cap write-capable delegation at 2 background agents.** Keep code edits in the main session or a single file-fenced generator subagent instructed to finish the full change list without stopping early; inspect diffs and re-run gates yourself before committing. Probe 1 read-only CLI extraction lane before fanning out transcript jobs.
- **Keep secrets out of git, binaries, and logs.** Never commit `.env.local` or `Secrets.xcconfig`, never embed publisher API keys in iOS binaries, never print credentials, and compare environment keys by SHA-256 digest.
- **Report in the owner's words.** Name the screen and what a player sees rather than internal test names, and state plainly what could not be checked on the current machine.
