# Positioning, Ideation & Pricing Architecture

This guide details the strategic product positioning for home network admins and gamers, ideation workflows, and dual-model pricing architecture.

---

## 0. Positioning Document Audit & Discovery Protocol

Before drafting marketing copy, establishing category labels, or finalizing pricing hooks:
1. **Audit `docs/positioning/`**: Check if `docs/positioning/00-decision.md` or `docs/positioning/10-territory-*.md` exists.
2. **Invoke `/positioning:positioning` if Missing**: If no positioning documents exist in `docs/positioning/`, trigger the `positioning` skill (`/positioning:positioning`). It runs Dossier deep-research panels (free CLI + paid API), tests candidate territories under trawl frames, enforces shipped-truth bindings in a claim ledger, and produces the complete 9-document report suite and interactive decision aid in `docs/positioning/`.
3. **Anchor to Decision of Record**: Extract the recommended territory, the single word to own, the named enemy, and the beachhead persona from `docs/positioning/00-decision.md` and use them as the immutable baseline for all copy generation.

---

## 1. Target Personas & Core Messaging Hooks

### Persona A: The Sovereign Home Network Admin
- **Mindset**: Values local sovereignty, hardware telemetry, deterministic routing, zero cloud lock-in, and zero trust.
- **Pain Points**: Enterprise tools are bloated, subscription-heavy, and push opaque SaaS telemetry; FOSS scripts are brittle and lack polish.
- **Core Hook**: *"Your network, your hardware, zero opaque cloud intermediaries. Enterprise-grade packet inspection and telemetry with the elegance of a native desktop app."*

### Persona B: The Competitive Gamer & Low-Latency Enthusiast
- **Mindset**: Obsessed with packet jitter, bufferbloat reduction, tick-rate stability, and cross-device telemetry.
- **Pain Points**: VPNs increase ping; background bloat causes frame spikes; router UIs are slow and clunky.
- **Core Hook**: *"Sub-millisecond route optimization, zero bloat, and instantaneous hardware telemetry across your rig, handheld, and phone."*

---

## 2. Ideation & Inspiration Workflows

### 1. Divergent Feature & Angle Ideation via `/trawl:trawl`
Run `/trawl:trawl` to extract sharp technical hooks from prior projects and user discussions:
- Hardware-accelerated eBPF / DPDK packet paths.
- Local AI anomaly detection with Bring-Your-Own-Key (BYOK).
- Custom latency heatmaps and hop-by-hop visual traceroutes.

### 2. UI Inspiration via Mobbin MCP
Search Mobbin via router MCP:
- Use `mcp__router__mobbin__search_screens` with queries: `"network monitoring"`, `"analytics dashboard"`, `"gaming hardware companion"`, `"dark mode telemetry"`.
- Use `mcp__router__mobbin__search_flows` with queries: `"byok onboarding"`, `"self-hosted configuration"`.

---

## 3. Dual Pricing Architecture

| Model | Price | Target Audience | What's Included |
|---|---|---|---|
| **Self-Hosted / BYOK** | **$9.99** (Perpetual) | Home lab enthusiasts, VPS owners, privacy purists | Unlimited self-hosted node deployment (Docker/bare metal), Bring Your Own AI Key (OpenAI/Anthropic/Ollama), local storage, lifetime client updates. |
| **Managed Cloud SaaS** | **$4.99 / mo** | Gamers, mobile power users, quick setup | Automated encrypted relay tunnels, managed zero-trust mesh, cloud backup, 100k monthly AI anomaly credits, instant multi-device sync. |

---

## 4. Copywriting Guidelines (Luke Voice Rules)

All marketing copy must be generated through `/create-luke-content:create-luke-content`:
1. **Direct and grounded**: Say what the software does in the first sentence.
2. **Zero fluff**: No "revolutionary", "game-changing", "next-gen AI superpower", or "seamless experience".
3. **No em dashes (`—`)**: Use standard punctuation (colons, parentheses, or separate sentences).
4. **Honest technical specifications**: State exact port protocols, supported OS versions, memory footprint, and local encryption specs.
