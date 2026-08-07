# The launch pipeline — from scaffolded to launch-ready

Runs after `scaffold.sh` reports green. The scaffold gives you a working shell; this pipeline gives it substance: researched context, a triaged-ready feature backlog, comprehensive mocks, and a marketing site. Phases R and B start together (research runs in the background while you work); D and M need R's output, so order is R∥B → O → D → M → L. Report progress at each phase boundary.

Deep research is the grounding layer for three consumers: the **feature briefs**, the **OVERVIEW.md**, and the **marketing site's decisions and content**. Nothing in those three states a market claim the research or the owner didn't supply.

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

From the idea and interview answers, write the first briefs into `docs/features-to-triage/` using `BRIEF-TEMPLATE.md` (name: `<ID_PREFIX>-<slug>.md`), and add index rows to its README. Seed only what the owner actually described plus the structural certainties (e.g. "port the marketing mock into apps/web" is always the first web brief once Phase M runs). 5–12 briefs is the usual seed; don't pad.

**After Phase R lands**, revisit: revise briefs the research contradicts, add the briefs the research surfaces (competitor table-stakes, gaps worth owning), and cite the report + section in each brief's **Source** line. Ledger IDs stay unallocated — triage owns that write.

The generated CLAUDE.md carries the standing rule: **every future feature request lands as a brief here first**, then `ship-feature` (one) or `ship-fleet` (backlog) runs on it.

## Phase O — overview + marketing features

Fill `OVERVIEW.md` (positioning, audience, problem, market context) and `docs/MARKETING-FEATURES.md` (feature→benefit→proof rows for what the scaffold already ships, e.g. sign-in; pricing recommendation grounded in the research's competitor pricing, marked as recommendation until the owner confirms). Research-derived claims cite their report inline. Both files carry keep-current rules in CLAUDE.md — write them as if they'll be read in six months, because they will.

## Phase D — design: mocks for every surface

Ground rules: mocks are standalone HTML in `design/mocks/html/` (the pipeline's source of truth for build fidelity); every screen gets its **empty, loading, and error states**, not just the happy path; menus, modals, and sheets are mocked as their own frames or interactive states.

- **`design-craft`** authors the visual system and the mock set for each surface (web app screens, admin, marketing components). If the interview captured a `--design-ref`, bootstrap DESIGN.md from it first (design-md-from-website).
- **`ux-craft`** passes every flow: navigation, forms, onboarding, sign-in (the scaffolded /login flow is a real screen — mock it properly), return paths on every pushed view.
- **`mac-design-studio`** owns the native side: macOS window (or menu-bar) design, iOS/iPad screens, and the **app icon** — 2–3 directions.
- **Icons:** generate the vector artwork with **media-gen-pro** (`svg: true` — real SVG via Arrow, never a raster imitating one) into `design/icon/`, then complete `design/icon/audit.html` (scaffolded from the portfolio's audit template, sizes 128/64/**48**/32/16 + tinted + silhouette) — one `.row` section per direction. The audit is how a direction is chosen; don't skip to a single icon.
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
