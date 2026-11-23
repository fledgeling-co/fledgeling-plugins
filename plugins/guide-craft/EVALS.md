# guide-craft: evaluation

**Live with-skill versus no-skill A/B runs haven't been run for v1.0.0.** On 23 November 2026, during Phase 0 of building this plugin, we picked "Self-test scripts, skip A/B" alongside a paid cross-genre Dossier research pass. So this release ships with mechanically verified gate scripts, a verified three-family research corpus, and production-measured rules from the MW4 Season 1 Field Guide, but it doesn't carry a head-to-head agent benchmark or blind panel score yet.

Everything below separates what we actually ran and verified from what's still untested.

## Layer 1: mechanical self-tests (verified)

Each script in `skills/guide-craft/scripts/` has a `--self-test` mode that runs against clean fixtures and deliberately broken ones. All four use standard Python 3 with zero third-party packages and exited `0` on 23 November 2026.

| Script | What it checks | Clean fixture | Faulted fixtures caught | Exit code |
|---|---|---|---|---|
| `check_html.py` | Nested `<a>` tags, digit-starting DOM IDs, broken `#fragment` links, stray `<` text | 0 errors | 4 / 4 fault classes | `0` |
| `audit_sources.py` | Unresolved `[[rN]]` IDs, bare-domain URLs, publisher dedup, `n < 50` floor, Wilson 95% lower bound, datamine vs lab split | 0 errors | 6 / 6 fault classes | `0` |
| `check_briefing.py` | Voice briefing byte ceiling, entity retention across guide items, zero-denominator guard | OK | Overflow, entity drop, and zero-cap fixtures | `0` |
| `check_compliance.py` | Apple 4.1(c)/4.2/5.2 rules plus nine publisher policies (Riot, Capcom, Bungie, Blizzard, Valve, Wargaming, GGG, PUBG, iRacing) | Clean Riot manifest | 9 / 8 Capcom IP/ad/hitbox faults and Bungie ad fault | `0` |

Two real defects turned up during these checks and were fixed before shipping. First, `check_compliance.py` originally rejected Riot's own verbatim disclaimer ("Riot Games does not endorse or sponsor this project") because the regex only checked for "unofficial" and "not affiliated". Adding "does not endorse" and "isn't affiliated" cleared that false positive without loosening missing-disclaimer checks. Second, `scripts/check_skill_references.py` caught retired skill IDs (`anthropic-skills:deep-research` and `anthropic-skills:chrome-browser`) carried over from an earlier draft; both were replaced with live tool names (`dossier`, `agent-browser`, `obscura`).

## Evidence behind the rules (verified)

The rules in `skills/guide-craft/references/evidence.md` come from two sources.

First, direct measurements (`O1` to `O11`, `C1` to `C6`) from building and auditing the MW4 Season 1 web guide (`mw4.fledgeling.app`), SwiftUI iOS app (`app.fledgeling.fieldguide`), and Overwatch GPT-Live voice endpoint across two recorded sessions (`34766ed0` and `a54ba008`/`f66084b1`). Those sessions produced the HTML nesting gate, the briefing-first voice architecture, the Scribe TTS loop, and the datamine-versus-lab split (where TAQ-V datamined at 513 RPM but frame-tested at 361 RPM).

Second, a three-family Deep Research pass archived in `docs/deep-research/` on 23 November 2026, covering APIs, codecs, stats bias, and publisher rules across eight game genres.

| Research member | How it ran | Citation check | Status |
|---|---|---|---|
| Gemini Deep Research | Run by Luke on Gemini web (`cross-genre-gemini.md`, base64 chart blobs stripped) | Primary portal and Apple Guideline URLs spot-checked | Archived and used |
| xAI (`dr_1c8927393675f6c2`) | Paid Dossier API run | `research_verify_citations`: 38 / 47 live, 0 dead, 9 blocked by publisher firewalls | Archived and used |
| Perplexity (`dr_f6421164959dee4e`) | Paid Dossier API run | `research_verify_citations`: caught 2 dead URLs (`bungie.net/Platform/Destiny2\`` and `api.steampowered.com/`) and 1 malformed URL (`partner.steam-api.com\``) | Archived; bad URLs dropped |

All five local CLI Dossier backends (Codex, Claude CLI, Antigravity, Cursor, Grok CLI) failed `research_doctor` search probes on 23 November 2026 (usage-limited, unsigned, or returning zero URLs). That's why Phase 0 approved the paid API panel instead of running locally for free.

## Spend record

| Item | Cost | Notes |
|---|---|---|
| Dossier Phase 1 panel (Perplexity + xAI) | `$3.20` | Reported by `research_budget` |
| Gemini Deep Research | `$0.00` (subscription) | Run on Gemini web and supplied directly |
| Icon commission (`media-gen-pro`: 1 Arrow SVG + 2 Flare rasters) | 3 billed image calls | Hand-authored SVG master (`build_icon.py`) shipped at 11 / 12 in `assets/audit.html` |
| Live A/B agent runs | `$0.00` | Skipped per Phase 0 choice |

## Layer 2: what isn't proved yet (ready to run)

`evals/evals.json` holds seven cross-genre prompts with checkable assertions ready to run with the skill against a bare baseline, then judge blind across `claude`, `meta`, and `xai` (excluding the generator's own family).

| # | Task | Genre | What it checks |
|---|---|---|---|
| 1 | FPS season guide with closed API | Shooter | Multi-page guide, clean-room provenance, datamine vs frame-test split, `check_html.py` and `audit_sources.py` |
| 2 | MOBA patch companion | League / TFT | Backend Riot proxy (no keys in iOS binary), pre-match tier subtraction, TFT Augment win-rate ban, no overlay ads |
| 3 | Fighting-game frame-data app (adversarial) | Street Fighter 6 | Refusing paywall ads and live hitbox overlays per Capcom's rules, querying SuperCombo Cargo instead |
| 4 | CCG meta deck tracker | Hearthstone / MTG Arena | Client-side Base64 varint deckstring codec, hotfix timestamp partitioning, 17Lands opt-in skew note |
| 5 | ARPG league build guide | Path of Exile 1 & 2 | PoB XML and PoE2 `.build` JSON codecs, dynamic `X-Rate-Limit-*` pacing, 5-minute public stash delay |
| 6 | Sim-racing telemetry companion | F1 25 / iRacing | Local 60 Hz UDP port 20777 listener, iRacing affirmative consent, no cloud-scrape leakage |
| 7 | Briefing-first voice companion | Cross-genre voice | Compact plain-text briefing verified by `check_briefing.py`, session minute caps, Scribe blind QA |

Until those seven pairs run against a bare model and pass blind multi-family judging, treat `guide-craft`'s runtime lift and token overhead as unmeasured. The deterministic gate scripts and compliance checks are proved today; live agent adherence isn't.

## Recorded user checkpoints

Phase 0 (23 November 2026) approved buying the paid Dossier panel (paired with Luke's Gemini Deep Research export) and self-testing the scripts while skipping live A/B runs. Phase 4 (23 November 2026) picked the plugin name `guide-craft` and the `Folio and season tab` porcelain gel-glass icon direction.
