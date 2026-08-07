<p align="center">
  <img src="assets/banner.png" alt="Fledgeling: a cream fledgeling-bird mark on warm charcoal beside the wordmark, with the line: tools for people building from nothing" width="100%" />
</p>

<p align="center"><strong>Claude Code plugins from <a href="https://www.fledgeling.app">Fledgeling</a>.</strong><br />
Built and used daily by <a href="https://github.com/lprhodes">Luke Rhodes</a>; shipped when they've earned it.</p>

<p align="center">
  <img alt="6 plugins" src="https://img.shields.io/badge/plugins-6-C4622D">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-6B665D">
</p>

---

Fledgeling makes AI-native software for founders and developers; these are the Claude Code plugins that come out of building it. Each one exists because a real workflow needed it, and each carries its own README, evals or references where the work justified them.

## Installing

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
```

Then install what you want:

```text
/plugin install trawl@fledgeling-plugins
```

## The plugins

| | Plugin | In one line | |
|---|---|---|---|
| <img src="plugins/trawl/assets/icon-128.png" width="40" alt="" /> | **trawl** | Divergent ideation that converges on something you can ship; every design choice traces to measured research. | [README](plugins/trawl/README.md) |
| | **design-review** | The last pass before a human looks at AI-built UI: deterministic gates, then judged passes, on real renders. | [README](plugins/design-review/README.md) |
| | **slipway** | A complete, working new project from an idea: one interview, then scripts render the whole scaffold and launch pipeline. | [README](plugins/slipway/README.md) |
| | **ship-armada** | The portfolio-level orchestrator: reads the manifest, surveys every project, routes and dispatches work. | [README](plugins/ship-armada/README.md) |
| | **armada-sync** | The counterpart maintenance skill: keeps the portfolio manifest truthful after work happens anywhere. | [README](plugins/armada-sync/README.md) |
| | **compaction-quality** | Writes context-compaction summaries that survive being the only thing the next session has, and scores them. | [SKILL.md](plugins/compaction-quality/SKILL.md) |

### trawl

Ask a model an open-ended question and you get the answer everyone gets. Trawl spawns isolated thinkers under genuinely different frames, writes the obvious answer down first, and only recommends a creative pick that beats it blind on your stated problem. The whole design is receipts-first: structural evals (96.4% vs its predecessor's 49.0%), a four-judge blind panel, and the research corpus it was built from, all committed in the repo. [Read more →](plugins/trawl/README.md)

### design-review

AI-built UI ships with defects that pass every lint. This runs the deterministic gates first (accessibility, contrast, target size, motion, layout integrity), then judged passes over hierarchy, states, flows and system coherence, against real renders at a viewport matrix. Findings come severity-ranked with pasteable fixes and an explicit list of what was never checked. Works with Playwright, Puppeteer, chrome-devtools-mcp, agent-browser or claude-in-chrome; with none of them it says so rather than implying a page was seen. [Read more →](plugins/design-review/README.md)

### slipway

New projects die in setup. Slipway runs one front-loaded interview, then scripts render ~120 templates into a working monorepo: web app, auth, admin, native apps, testing harnesses, deploy config, env wiring, and a launch pipeline that runs deep research, seeds feature briefs, and mocks every surface. The LLM only interviews; scripts make the files. [Read more →](plugins/slipway/README.md)

### ship-armada and armada-sync

A portfolio of repos needs a layer above any one of them. Ship-armada reads the manifest of record, verifies it against git, then surveys, plans, routes single directives into the right project's pipeline, and dispatches per-repo backlogs. Armada-sync is the surgical counterpart: after work happens anywhere, it updates that one project's manifest entry and stops. [ship-armada →](plugins/ship-armada/README.md) · [armada-sync →](plugins/armada-sync/README.md)

### compaction-quality

When a session compacts, the summary becomes the only context the next session has; most summaries lose the corrections the user fought for. This writes summaries built on a 225-event measurement of what actually survives, and ships a deterministic scorer so regressions are caught rather than felt. [SKILL.md →](plugins/compaction-quality/SKILL.md)

> [!NOTE]
> Some plugins depend on each other by design: ship-armada dispatches through skills that live in a sibling marketplace, and armada-sync is the maintenance half of ship-armada. Each README states what it expects.

## Licence

MIT. Do what you like; attribution appreciated.

## Elsewhere

Fledgeling is [Luke Rhodes](https://www.linkedin.com/in/lukerhodes/), also co-founder of [Diolog](https://diolog.app).

[fledgeling.app](https://www.fledgeling.app) · [GitHub](https://github.com/lprhodes) · [X](https://x.com/lp_rhodes) · [LinkedIn](https://www.linkedin.com/in/lukerhodes/) · [hello@fledgeling.app](mailto:hello@fledgeling.app)
