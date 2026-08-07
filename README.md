<p align="center">
  <img src="assets/banner.png" alt="Fledgeling: a cream fledgeling-bird mark on warm charcoal beside the wordmark, with the line: tools for people building from nothing" width="100%" />
</p>

<p align="center"><strong>SWE Skills from <a href="https://www.fledgeling.app">Fledgeling</a>.</strong><br />
Built and used daily by <a href="https://github.com/lprhodes">Luke Rhodes</a>; shipped when they've earned it.</p>

<p align="center">
  <img alt="6 skills" src="https://img.shields.io/badge/skills-6-C4622D">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-6B665D">
</p>

---

Fledgeling makes AI-native software for founders and developers; these are the SWE skills that come out of building it. Each one exists because a real workflow needed it, and each carries its own README, evals or references where the work justified them. Every icon below came through the same three-engine design pipeline with its audit sheet committed beside it.

## Installing

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
```

Then install what you want:

```text
/plugin install trawl@fledgeling-plugins
```

## The skills

| | Skill | |
|---|---|---|
| <a href="plugins/trawl/README.md"><img src="plugins/trawl/assets/icon-256.png" width="96" alt="" /></a> | **[trawl](plugins/trawl/README.md)**<br />Divergent ideation that converges on something you can ship. Isolated thinkers under genuinely different frames, the obvious answer written down first, and a creative pick recommended only when it beats that answer blind. Receipts committed: structural evals (96.4% vs its predecessor's 49.0%), a four-judge blind panel, and the research corpus it was built from. | [README →](plugins/trawl/README.md) |
| <a href="plugins/design-review/README.md"><img src="plugins/design-review/assets/icon-256.png" width="96" alt="" /></a> | **[design-review](plugins/design-review/README.md)**<br />The last pass before a human looks at AI-built UI. Deterministic gates first (accessibility, contrast, target size, motion, layout integrity), then judged passes over hierarchy, states, flows and system coherence, on real renders at a viewport matrix. Findings come severity-ranked with pasteable fixes and an explicit list of what was never checked. | [README →](plugins/design-review/README.md) |
| <a href="plugins/create-swe-project/README.md"><img src="plugins/create-swe-project/assets/icon-256.png" width="96" alt="" /></a> | **[create-swe-project](plugins/create-swe-project/README.md)**<br />A complete, working new project from an idea. One front-loaded interview, then scripts render the whole scaffold: monorepo, auth, admin, native apps, testing harnesses, deploy config, and a launch pipeline that researches, seeds feature briefs and mocks every surface. The LLM only interviews; scripts make the files. | [README →](plugins/create-swe-project/README.md) |
| <a href="plugins/ship-armada/README.md"><img src="plugins/ship-armada/assets/icon-256.png" width="96" alt="" /></a> | **[ship-armada](plugins/ship-armada/README.md)**<br />The portfolio-level orchestrator. Reads the manifest of record, verifies it against git, then surveys, plans, routes single directives into the right project's pipeline, and dispatches per-repo backlogs as dependency-ordered campaigns with capped concurrency. | [README →](plugins/ship-armada/README.md) |
| <a href="plugins/armada-sync/README.md"><img src="plugins/armada-sync/assets/icon-256.png" width="96" alt="" /></a> | **[armada-sync](plugins/armada-sync/README.md)**<br />The surgical counterpart to ship-armada: after work happens anywhere in the portfolio, it updates that one project's manifest entry, stamps it fresh, and stops. The smallest skill here, on purpose. | [README →](plugins/armada-sync/README.md) |
| <a href="plugins/compaction-quality/README.md"><img src="plugins/compaction-quality/assets/icon-256.png" width="96" alt="" /></a> | **[compaction-quality](plugins/compaction-quality/README.md)**<br />Writes context-compaction summaries that survive being the only thing the next session has, built on a 225-event measurement of what actually gets lost (five user corrections per session; four die). Ships a deterministic scorer so a good summary is a number, not a feeling. | [README →](plugins/compaction-quality/README.md) |

> [!NOTE]
> Some skills depend on each other by design: ship-armada dispatches through skills that live in a sibling marketplace, and armada-sync is the maintenance half of ship-armada. Each README states what it expects.

## Licence

MIT. Do what you like; attribution appreciated.

## Elsewhere

Fledgeling is [Luke Rhodes](https://www.linkedin.com/in/lukerhodes/), also co-founder of [Diolog](https://diolog.app).

[fledgeling.app](https://www.fledgeling.app) · [GitHub](https://github.com/lprhodes) · [X](https://x.com/lp_rhodes) · [LinkedIn](https://www.linkedin.com/in/lukerhodes/) · [hello@fledgeling.app](mailto:hello@fledgeling.app)
