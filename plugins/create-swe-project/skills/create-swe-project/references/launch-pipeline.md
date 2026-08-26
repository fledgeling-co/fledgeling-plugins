# The launch pipeline — from scaffolded to launch-ready

Runs after `scaffold.sh` reports green. The scaffold gives you a working shell; this pipeline gives it substance: positioning & market grounding, researched context, a triaged-ready feature backlog, comprehensive technical PRD & OVERVIEW documentation, comprehensive mocks, and a marketing site. Phases P, R and B start together (positioning audit and research run in the background while you work); O synthesizes PRD.md + OVERVIEW.md; D and M build design and marketing from verified ground truth. Order is P∥R∥B → O → D → M → L. Report progress at each phase boundary.

Deep research and positioning are the grounding layers for four consumers: the **feature briefs**, the **PRD.md**, the **OVERVIEW.md**, and the **marketing site's decisions and content**. Nothing in those four states a market claim the research or the owner didn't supply.

## Phase P — positioning audit & market grounding

Before establishing marketing hooks, category labels, or product scope:
1. **Audit `docs/positioning/`**: Check if `docs/positioning/00-decision.md` or `docs/positioning/10-territory-*.md` exists.
2. **Invoke `/positioning:positioning` if Missing**: If no positioning documents exist in `docs/positioning/`, execute the `positioning` skill (`/positioning:positioning`). It runs Dossier deep-research panels (free CLI + paid API), discovers customer pain points and competitor lines, evaluates candidate territories under trawl frames, tests product-truth claimability, and writes the 9-document report suite and interactive decision surface to `docs/positioning/`.
3. **Anchor to Decision of Record**: Read the recommended territory, hero line, category frame, and target beachhead from `docs/positioning/00-decision.md` as the authoritative source of truth for `PRD.md`, `OVERVIEW.md`, and all marketing copy.

## Phase R — deep research (starts first, runs in the background)

Decide 0–2 Dossier queries from the idea:

- **Competitive/market** (archetype `competitive`) — when the product enters an existing space: who else does this, what they charge, what users complain about, the gap. Almost every product idea warrants this one.
- **Technical** (archetype `technical`) — only when the domain has real unknowns (a hardware API, a protocol, a regulated space). Skip for stacks the templates already encode.

Lanes: the **free CLI panel is the default** (`research_plan` shows it; local-claude/codex lanes cost nothing). **Ask the user before any paid backend joins** — it's their money; present the plan's cost band and let them choose free-only vs full panel. Then `research_start` and **carry on with Phase B — do not block on the run** (4–20 min).

When the panel settles:

1. **Read every report in full.** Not outlines, not the merged coverage-diff — the full report files (`~/.dossier-research-mcp/reports/<runId>.md`). An outline gives every heading and no content; a merge diff lists claims without evidence. This rule exists because skipping it was a real mistake this skill's own design nearly shipped with.
2. `research_export` each run into `docs/deep-research/` (with sources), so the project owns its evidence.
3. Optionally `research_verify_citations` on the run whose claims will drive pricing or positioning.

## Phase B — seed the feature backlog (immediately, from the owner's context)

From the idea and interview answers, write the first briefs into `docs/features-to-triage/` using `BRIEF-TEMPLATE.md` (name: `<slug>.md`), and add index rows to its README. The template is the format the `intake` skill writes, so a brief seeded here and a brief intake adds later read the same. Seed only what the owner actually described plus the structural certainties (e.g. "port the marketing mock into apps/web" is always the first web brief once Phase M runs). 5–12 briefs is the usual seed; don't pad.

**After Phase R lands**, revisit: revise briefs the research contradicts, add the briefs the research surfaces (competitor table-stakes, gaps worth owning), and cite the exported report on each brief's `research:` line. A brief the research surfaced rather than the owner asking for it carries `proposed-by-ai: true`, so the owner vetoes an idea by deleting the file instead of answering a question. Ledger IDs stay unallocated — triage owns that write.

The generated CLAUDE.md carries the standing rule: **every future feature request lands as a brief here first**, then `ship-feature` (one) or `ship-fleet` (backlog) runs on it.

## Phase O — technical PRD, overview & marketing features

Generate and maintain the core product source-of-truth documents:

1. **`PRD.md` (Comprehensive Technical Requirements Document)**:
   - Must cover **ALL** feature briefs in `docs/features-to-triage/*.md` with complete traceability.
   - Include: Product Overview & Strategic Goals, Target Personas & User Journeys, Feature Traceability Matrix (mapping every brief to Req ID, target surface, status [Triaged/Backlog/In Progress/Built], user story, and core acceptance criteria), System Architecture & API/Data Contracts, Non-Functional Requirements (Performance, Security, Accessibility, Reliability), and Release Criteria.
   - Every seeded brief in `docs/features-to-triage/*.md` must trace to an explicit requirement row.

2. **`OVERVIEW.md`**:
   - System overview: Mission, target audience, core problem, solution architecture with Mermaid diagram, surfaces/modules map, and market context cited from `docs/positioning/` or `docs/deep-research/`.
   - Positioning in one line: taken directly from `docs/positioning/00-decision.md`.

3. **`docs/MARKETING-FEATURES.md`**:
   - Feature→benefit→proof rows for what the scaffold already ships (e.g. sign-in, tokens, Caddy, native apps); pricing recommendation grounded in competitor research and Phase O½ rules. Both files carry keep-current rules in CLAUDE.md.

## Phase D — design: mocks for every surface

Ground rules: mocks are standalone HTML in `design/mocks/html/` (the pipeline's source of truth for build fidelity); every screen gets its **empty, loading, and error states**, not just the happy path; menus, modals, and sheets are mocked as their own frames or interactive states.

- **`design-craft`** authors the visual system and the mock set for each surface (web app screens, admin, marketing components). If the interview captured a `--design-ref`, bootstrap DESIGN.md from it first (design-md-from-website).
- **Reference trawl before the direction is committed** (`design-craft` → `plugins/design-craft/skills/design-craft/references/mobbin-trawl.md`): two or three aimed Mobbin searches per surface family, images opened, and a took/left ledger recorded in `INDEX.md`. A direction derived only from memory converges on the category's default shape, which is what "bland", "boring" and "the layouts are terrible" name when they arrive as feedback. Mobbin not installed is a one-line note in the phase report.
- **`ux-craft`** passes every flow: navigation, forms, onboarding, sign-in (the scaffolded /login flow is a real screen — mock it properly), return paths on every pushed view.
- **`mac-design-studio`** owns the native side: macOS window (or menu-bar) design and iOS/iPad screens. It routes icon work onward (below) rather than doing it itself.
- **Icons: hand the whole commission to `create-mac-icon`.** Invoke that skill, or brief one agent to read its SKILL.md and follow it, passing the app's subject, its three committed adjectives, and any brand colour constraint. It owns the direction pick from its 532-icon corpus catalogue, the subject-mined glyph, all three engines, the fidelity loop that scores the shipped SVG against the winning raster at five sizes, and the `audit.html` written from its own template.

  A bare `media-gen-pro` call plus a hand-rolled contact sheet is **not** this step. That shortcut skips the corpus, the 12-point rubric, the loop and the recipe library, and it produces the icons the owner described as "really basic compared to all of the macos icons". `media-gen-pro` with `svg: true` is Engine B *inside* the pipeline, alongside the hand-authored layered master and the corpus-referenced raster — a stage, not the whole of it.

  Deliverables into `design/icon/`: the layered SVG master plus its build script, the alternates, the retina renders under `audit-renders/`, and `audit.html` — one row per take, losers scored and kept, sizes 128 / 64 / **48** / 32 / 16 css px from 256 / 128 / 96 / 64 / 32 sources, plus tinted and silhouette. Every take shares one outer silhouette from `squircle-path.txt`.

  Then gate it mechanically and look at it:

  ```bash
  python3 <create-mac-icon>/skills/create-mac-icon/scripts/audit_sheet.py check design/icon   # exit 0 required
  ```

  followed by serving `design/icon/audit.html` and reading it. The script proves the sheet exists, is filled in, and that every image resolves; only opening it proves the icons are good. The audit is how a direction gets chosen — never skip to a single icon.

  `create-mac-icon` absent: say so in the phase report, fall back to `mac-design-studio`'s icon section, and note that the master ships unmeasured against any reference.
- Inventory before authoring: list every screen/flow/state as a checklist in `design/mocks/html/INDEX.md`, then work through it. A mock set without an inventory silently drops states.

## Phase O½ — pricing decisions (evidence, not vibes)

The pricing recommendation in `docs/MARKETING-FEATURES.md` follows the researched decision table, then the owner confirms:

| Product state | Mechanic |
|---|---|
| Unvalidated idea | Waitlist **with a referral loop** — the scaffolded `waitlist` module ships exactly this (`/waitlist`, referral codes, queue-jumping) (bare email capture converts ~1-2%; referral-powered lists report 15-25%) — or skip the waitlist for a build-in-public launch |
| Working SaaS, fast time-to-value | Free trial primary (opt-in ~9%, card-required ~31% at lower volume), prices published — hidden pricing eliminates ~43% of buyers |
| Mac pro/utility app | Direct sale (Paddle/Stripe MoR): one-time price + 1 year of updates + optional renewal — the CleanShot/Sketch pattern |
| iOS consumer app | App Store: trial paywall + annual "most popular" + lifetime anchor; hard paywalls convert ~5x freemium but refund higher |

Native-app channel decisions (IAP vs external purchase vs direct sale, region flux, MAS sandbox) follow `references/apple-commercialization.md` — walk the tree before writing native pricing copy. Card rules with evidence behind them: **3 tiers max**, exactly one visually dominant "most popular" (highlighting two backfires), annual pre-selected with "2 months free", real strike-through anchors fine (numerical anchoring replicates; decoy-tier tricks don't). Apple external-purchase-link economics are legally in flux — never bake channel-fee claims into copy.

## Phase M — the marketing site

A **premium single-page site** at `design/marketing/index.html` (standalone; porting it into `apps/web` becomes a P0 brief). Three skills in concert:

- **`create-luke-content`** (marketing register) writes every word: hero, feature sections from `docs/MARKETING-FEATURES.md`, honest caveats, and the **pricing section** using Phase O's recommendation. Copy is grounded in OVERVIEW.md + the research; no invented claims, no hype adjectives; run its voice lint on the copy.
- **`design-craft` + `ux-craft`** build it: gsap (ScrollTrigger reveals, staggered load) + three.js where it earns its place (one hero moment beats scattered effects) + micro-interactions throughout (hover states, magnetic buttons, scroll progress); **interactive app-UI mock slices** — lift real frames from Phase D's mocks and make them respond (a working toggle, a typed-in field), because a live slice sells better than a screenshot; sticky header with **Log in / Sign up** linking to the web app's `/login`; pricing cards wired to the same.
- **media-gen-pro** supplies the imagery: hero/section images (and video stills where motion helps) generated to `design/marketing/assets/` and referenced relatively. Charts/UI/anything with exact text stays hand-built — image models garble text.

**The quality bar (from the research — treat as gates, not aspirations):**

- **Zero slop tells.** The Krebs study scored 1,590 launch pages against deterministic AI-design tells; avoid every one: Inter/Geist/Space Grotesk as the whole identity, a single serif-italic accent word in the hero, "VibeCode purple", permanent dark mode with grey body text, gradient glows, centered hero + pill badge above the H1, colored card borders, identical icon-topped feature-card grids, 1-2-3 numbered steps, stat banner rows. design-craft's anti-slop machinery owns this; design-review confirms it.
- **Performance is the proven conversion lever** (the only rigorous datum: 1s LCP improvement → +13% conversions). Gate: LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1; three.js **out of the critical path** (dynamic import after first paint, static fallback, DPR capped, rendering suspended off-screen); `prefers-reduced-motion` produces a genuinely static page; **native scroll preserved** — scrolljacking is the most-hated pattern on the open web. Canvas image-sequence beats `<video>` for scroll-scrubbed product shots.
- **JS budget, from measured exemplars** (2026-08-07 teardown, transferred bytes): Linear 153KB across 27 chunks, CleanShot 189KB, Raycast 577KB, Family (WebGL-maximal) 1.4MB. Default budget: **≤300KB** — between the lean exemplars and Raycast. A deliberate cinematic mode may spend more only if the CWV gates still pass on mobile.
- **Motion A/B instrumentation** (the field has no honest animation-conversion data — the first launch can produce a better datum than anything published): build the page with a motion switch (`?motion=off` sets `data-motion="off"`, also honoured by `prefers-reduced-motion`), attach the active `motion_variant` to every analytics event, and note the experiment in docs/LAUNCH.md so a 50/50 split can run at launch.
- **Motion argues the product, selectively.** One authored hero moment and one pinned product narrative showing 2-3 real state changes beat effects everywhere ("mastering delight is mastering selective emphasis"). Animation-for-decoration reads as cheap; the interactive mock slice is the differentiator (only ~4% of SaaS sites embed one).
- **Structure:** hero proof-moment → proof strip (nothing invented) → pinned product narrative → interactive slice → fewer, richer feature modules → pricing (Phase O½ rules) → dependable footer. One conversion action per viewport.

Quality gate: run `design-review` over the finished page before calling Phase M done.

## Phase L — launch operations pack

The research's clearest finding: the "launch mile" is what every idea-to-launch tool skips, and it stays human-owned — the pipeline's job is to make the human's part small and well-informed. Fill `docs/LAUNCH.md` (scaffolded skeleton):

- **Domain**: check availability for the codename with the namecheap MCP (`check_domain_availability` — read-only, free) and record candidates; purchase stays a human action.
- **Legal**: draft privacy policy + terms stubs (Apple requires a privacy-policy URL for any App Store submission); publication is a human approval.
- **App Store kit** (native modules): name/subtitle options via create-luke-content, a screenshot shot-list mapped to Phase D mocks, the privacy-data inventory, review-account notes. Submission is human.
- **Analytics event schema**: the funnel events worth instrumenting (CTA click → signup → activation → paywall view → trial start → paid), so measurement exists from day one.
- **Waitlist/launch mechanics**: per the Phase O½ table; a referral loop is the most under-used lever.

Nothing in this phase creates accounts, spends money, or publishes — it prepares, and the checklist says exactly what the owner runs.

## Wrap-up

- Commit per phase (the scaffold committed phase 0; commit R+B, O, D, M, L separately so each is reviewable).
- Update the ARMADA manifest entry (armada-sync) — the project now has briefs, research, mocks, and a marketing mock worth listing.
- Report: what was researched (and what it changed), the brief count, the mock inventory coverage, and the marketing page path — plus what's deliberately deferred to the pipeline.
