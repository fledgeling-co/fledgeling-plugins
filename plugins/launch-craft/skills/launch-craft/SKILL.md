---
name: launch-craft
description: >-
  Conduct end-to-end product synthesis, positioning, and high-fidelity launch site creation for any project. Takes raw briefs in docs/features-to-triage/, mock HTML, and application source code, and executes a 4-phase pipeline: (1) Synthesizes and updates OVERVIEW.md and PRD.md using Gemini 3.7 Flash High via agy with complete feature traceability; (2) Grounds product positioning for home network admins and gamers, ideates hooks via /trawl, draws patterns from Mobbin MCP, and drafts authentic copy in Luke Rhodes' voice via /create-luke-content with dual pricing ($9.99 self-hosted/BYOK vs $4.99/mo hosted); (3) Crafts an interactive marketing website via /design-craft and /ux-craft utilizing GSAP scroll timelines, Three.js 3D telemetry canvases, interactive mock UI slices, and 5-platform badges (Windows, Mac, Linux, iOS, iPadOS); (4) Enforces deterministic WCAG, contrast, and visual conformance gates. Use whenever you need to synthesize project truth into PRDs and launch a bespoke, highly creative interactive marketing site — "build a launch site for this repo", "generate marketing website and update PRD", "launch-craft", "create product landing page with GSAP and Three.js".
---

# launch-craft — Product Synthesis & Interactive Launch Conductor

`launch-craft` bridges the gap between raw codebase reality, structured product documentation, and high-converting, creative marketing sites. It conducts a deterministic 4-phase pipeline:

```
[Raw Briefs / Code / Mocks]
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Gemini Document Synthesis (agy / Perch)            │
│   • Scans docs/features-to-triage/*.md, app code, mocks     │
│   • Runs gemini-3.7-flash-high via agy                      │
│   • Emits updated, trace-verified OVERVIEW.md & PRD.md      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 2: Positioning, Ideation & Authentic Copywriting      │
│   • Target: Home network admins & Gamers                    │
│   • Dual pricing: $9.99 BYOK/self-hosted · $4.99/mo SaaS    │
│   • Patterns via Mobbin MCP · Ideation via /trawl           │
│   • Copy drafted via /create-luke-content (Luke voice)      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 3: Interactive Marketing Site Crafting                │
│   • Design & UX via /design-craft & /ux-craft               │
│   • GSAP scroll timelines & micro-interactions              │
│   • Three.js 3D telemetry/topology hero canvas              │
│   • Interactive mock UI slices (network & latency toggles)  │
│   • 5-Platform badges (Windows, Mac, iPad, iPhone, Linux)   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Phase 4: Deterministic Validation & Conformance Gates       │
│   • Structural trace & markdown schema checks               │
│   • Contrast (WCAG AA/AAA), layout bounds, asset checks     │
│   • Exit 0 verification & artifact export                   │
└─────────────────────────────────────────────────────────────┘
```

**Running as a Gemini model?** Read `gemini.md` in this directory first, then follow this file with the overrides it names. It provides explicit enumeration bounds, execution ledgers, and chained file prerequisites. Other models skip it.

---

## Phase 1 — Project & Backlog Synthesis (Gemini 3.7 Flash High)

Synthesize all scattered project intelligence into single sources of truth (`OVERVIEW.md` and `PRD.md`).

1. **Discover all project artifacts**:
   - Backlog briefs: `docs/features-to-triage/*.md`
   - Feature plans & specs: `docs/plans/*.md`, `docs/specs/*.md`
   - Existing mock UI: `design/mocks/html/*.html`, `mocks/*.html`
   - Application source code: `src/`, `apps/`, `packages/`, config files.

2. **Execute Gemini 3.7 Flash High via `agy`**:
   - Run synthesis via `<skill-dir>/scripts/run_synthesis.py` or invoke `agy` directly from `/tmp` with `--new-project` (per global CLAUDE.md guidelines to prevent cwd context leaks):
   ```bash
   perl -e 'alarm shift @ARGV; exec @ARGV' 900 agy --new-project --model gemini-3.7-flash-high -p "<prompt>" > /tmp/synthesis.md 2>/tmp/synthesis.log
   ```
3. **Generate and Commit Artifacts**:
   - **`OVERVIEW.md`**: Executive summary, system architecture, core tech stack, active modules, and repository layout.
   - **`PRD.md`**: Comprehensive product requirements, target personas, feature matrix partitioned by status (Built / In Progress / Triaged / Backlog), API contracts, and non-functional requirements.
   - Every triaged feature in `docs/features-to-triage/*.md` must have an explicit traceable requirement in `PRD.md`.

---

## Phase 2 — Positioning, Ideation & Authentic Copywriting

Ground the product's market stance, ideate compelling differentiators, and write authentic marketing copy.

1. **Target Audience & Positioning**:
   - Primary: **Home Network Administrators** (demanding granular traffic observability, local control, custom DNS/VPN routing, self-hosted telemetry).
   - Secondary: **Gamers & Power Users** (demanding ultra-low ping, bufferbloat reduction, zero telemetry lag, hardware-accelerated routing).
   - Position against bloated enterprise tools and fragile CLI scripts: fast, beautiful, sovereign, and cross-platform.

2. **Pricing Structure**:
   - **$9.99 Perpetual / One-Time**: Bring Your Own Cloud (BYOK), self-hosted VPS/Docker, pay-as-you-go AI credits, lifetime client updates.
   - **$4.99 / Month Hosted SaaS**: Fully managed cloud relay, automated encrypted backups, turnkey zero-trust tunneling, included monthly AI credit allowance.

3. **Inspiration & Ideation**:
   - Search Mobbin MCP (`mcp__router__mobbin__search_screens` / `search_flows`) via router MCP for world-class onboarding and telemetry interfaces.
   - Invoke `/trawl:trawl` to extract sharp technical hooks, gamer pain points, and networking tropes.
   - Optional: leverage `mcp__router__media-gen-pro` for bespoke dark-mode textures, hardware renders, or backdrop assets.

4. **Draft Copy in Luke Rhodes' Voice**:
   - Route all site headlines, feature cards, technical specs, platform callouts, and FAQs through `/create-luke-content:create-luke-content` (marketing persona).
   - Enforce the Luke voice rules: authentic, technical, direct, zero AI slop, no breathless hyperbole, no em dashes (`—`).

---

## Phase 3 — Interactive Marketing Site Crafting (`design-craft` + `ux-craft`)

Build a bespoke, high-craft, interactive marketing website that refuses generic SaaS templates.

1. **Invoke Design & UX Authorities**:
   - Load `/design-craft:design-craft` for typography, color hierarchies, elevation, and layout discipline.
   - Load `/ux-craft:ux-craft` for information density, keyboard navigation, scan paths, and micro-copy ergonomics.

2. **Interactive 3D Hero (Three.js)**:
   - Embed an interactive WebGL Three.js canvas in the hero section: dynamic particle network topology, real-time ping mesh, or interactive orbital node constellation responding smoothly to pointer movement.
   - Fallback graceful CSS animation if WebGL is unavailable; ensure 60fps performance without CPU burn.

3. **Motion Choreography (GSAP & ScrollTrigger)**:
   - Choreograph scroll-driven reveals, telemetry counters, and sticky pinned comparison sections using GSAP.
   - Support `prefers-reduced-motion` with clean static layouts.

4. **Interactive Mock UI Feature Slices**:
   - Provide live, clickable UI slice widgets directly in the page:
     - *Packet / Flow Inspector*: Live filtering and latency timeline slider.
     - *BYOK vs Hosted Toggle*: Real-time cost & feature calculator.
     - *Platform Matrix Switcher*: Interactive preview switcher demonstrating native UI on **Windows**, **Mac**, **iPad**, **iPhone**, and **Linux**.

5. **5-Platform Badges & System Requirements**:
   - Prominently feature native client support across Windows (10/11), macOS (Apple Silicon & Intel), iPadOS, iOS, and Linux (AppImage / deb / rpm / AUR).

---

## Phase 4 — Deterministic Validation & Conformance Gates

Validate every generated artifact against deterministic quality criteria.

1. **Document Completeness Check**:
   - Ensure all `docs/features-to-triage/*.md` files trace directly into `PRD.md`.
   - Verify `OVERVIEW.md` accurately reflects repository structure and technology stack.

2. **Site Conformance & Accessibility Gate**:
   - Run `<skill-dir>/scripts/validate_site.py <site-path>`:
     - Assert WCAG AA contrast on all text elements (>4.5:1 for body, >3:1 for large text/headings).
     - Assert zero em dashes (`—`) across all copy.
     - Assert responsive layout integrity (no horizontal scrollbar on body from 320px to 2560px).
     - Assert all external scripts (GSAP, Three.js, fonts) resolve cleanly with fallbacks.

3. **Preview Deliverables**:
   - Open generated marketing site: `open -a "Google Chrome" <marketing-site.html>` or reveal generated markdown: `open -R OVERVIEW.md PRD.md`.

---

## Reference Guides

- `references/synthesis-protocol.md` — Gemini extraction prompts, schema constraints, and trace matrix.
- `references/positioning-and-pricing.md` — Personas, gamer/admin messaging angles, and dual pricing mechanics.
- `references/site-craft-and-gsap.md` — Three.js particle setup, GSAP timeline choreography, and interactive slice components.
- `references/evidence.md` — Empirical citations, benchmark comparisons, and design rationale.
