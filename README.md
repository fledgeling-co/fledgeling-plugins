<p align="center">
  <img src="assets/banner.png" alt="Fledgeling: a cream fledgeling-bird mark on warm charcoal beside the wordmark, with the line: tools for people building from nothing" width="100%" />
</p>

<p align="center"><strong>SWE Skills from <a href="https://www.fledgeling.app">Fledgeling</a>.</strong><br />
Built and used daily by <a href="https://github.com/lprhodes">Luke Rhodes</a>; shipped when they've earned it.</p>

<p align="center">
  <img alt="9 skills" src="https://img.shields.io/badge/skills-9-C4622D">
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

<a href="plugins/trawl/README.md"><img src="plugins/trawl/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [trawl](plugins/trawl/README.md)

Divergent ideation that converges on something you can ship. Isolated thinkers under genuinely different frames, the obvious answer written down first, and a creative pick recommended only when it beats that answer blind. Receipts committed: structural evals (96.4% vs its predecessor's 49.0%), a four-judge blind panel, and the research corpus it was built from.

<br clear="left" />

<a href="plugins/design-review/README.md"><img src="plugins/design-review/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [design-review](plugins/design-review/README.md)

The last pass before a human looks at AI-built UI. Deterministic gates first (accessibility, contrast, target size, motion, layout integrity), then judged passes over hierarchy, states, flows and system coherence, on real renders at a viewport matrix. Findings come severity-ranked with pasteable fixes and an explicit list of what was never checked.

<br clear="left" />

<a href="plugins/create-swe-project/README.md"><img src="plugins/create-swe-project/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-swe-project](plugins/create-swe-project/README.md)

A complete, working new project from an idea. One front-loaded interview, then scripts render the whole scaffold: monorepo, auth, admin, native apps, testing harnesses, deploy config, and a launch pipeline that researches, seeds feature briefs and mocks every surface. The LLM only interviews; scripts make the files.

<br clear="left" />

<a href="plugins/ship-armada/README.md"><img src="plugins/ship-armada/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [ship-armada](plugins/ship-armada/README.md)

The portfolio-level orchestrator. Reads the manifest of record, verifies it against git, then surveys, plans, routes single directives into the right project's pipeline, and dispatches per-repo backlogs as dependency-ordered campaigns with capped concurrency.

<br clear="left" />

<a href="plugins/armada-sync/README.md"><img src="plugins/armada-sync/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [armada-sync](plugins/armada-sync/README.md)

The surgical counterpart to ship-armada: after work happens anywhere in the portfolio, it updates that one project's manifest entry, stamps it fresh, and stops. The smallest skill here, on purpose.

<br clear="left" />

<a href="plugins/compaction-quality/README.md"><img src="plugins/compaction-quality/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [compaction-quality](plugins/compaction-quality/README.md)

Writes context-compaction summaries that survive being the only thing the next session has. Rebuilt on four research reports and a fresh measurement across 121 real compaction events: rejected approaches survive at 0.3%, and standing constraints at somewhere between a third and a half depending on the sample. Ships a deterministic scorer and a head-to-head benchmark against the built-in /compact whose baseline arm costs nothing.

<br clear="left" />

<a href="plugins/improve-skill/README.md"><img src="plugins/improve-skill/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [improve-skill](plugins/improve-skill/README.md)

The pipeline that built half this marketplace, as a skill. Point it at an existing skill plus your complaints; it runs paid and free deep research, rebuilds the skill with every change traced to evidence, proves the rebuild with comparative evals and a blind multi-family judge panel, then ships the full brand treatment. You choose the name and the icon concept before anything gets generated.

<br clear="left" />

<a href="plugins/create-skill/README.md"><img src="plugins/create-skill/assets/icon-c1-256.png" align="left" width="110" alt="" /></a>

### [create-skill](plugins/create-skill/README.md)

The sibling of improve-skill, for when there is nothing to improve yet. It interviews you properly first, because an unstated intention is the usual reason a new skill misses, then researches the domain, builds through skill-creator with every rule traced to evidence, and proves it against the honest baseline: the same prompts with no skill at all.

<br clear="left" />

<a href="plugins/create-mac-icon/README.md"><img src="plugins/create-mac-icon/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [create-mac-icon](plugins/create-mac-icon/README.md)

macOS app icons, measured against the reference instead of eyeballed. A direction catalogue distilled from 532 real icons, three generation engines with a written audit sheet, then a scoring harness that iterates the shipped SVG against the winning raster at five sizes until the material matches. Every confirmed construction feeds a recipe library, so it gets better with each commission.

<br clear="left" />

<a href="plugins/dossier-report/README.md"><img src="plugins/dossier-report/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [dossier-report](plugins/dossier-report/README.md)

A research question in, one published page out. It runs a paid and free research panel, reads every report end to end rather than the merged summary, turns the corpus into a list of claims with sources attached, then designs the page from scratch around its own subject so consecutive pages do not converge on one look. Every claim carries a citation you can open, and the build fails on one that does not resolve.

<a href="plugins/mac-doctor/README.md"><img src="plugins/mac-doctor/assets/icon-256.png" align="left" width="110" alt="" /></a>

### [mac-doctor](plugins/mac-doctor/README.md)

Your Mac did not fill up because of one thing, it filled up because a hundred reasonable defaults each left something behind and nobody was counting. Five scheduled jobs, from every fifteen minutes to weekly, with what each may do on its own widening as the gap between runs grows. Running low makes it check sooner, never delete more. The interesting part is what it refuses: a worktree needs three separate proofs before it is touched, and on the machine it was built for it declined to remove a single one of 620 GB.

<br clear="left" />

> [!NOTE]
> Some skills depend on each other by design: ship-armada dispatches through skills that live in a sibling marketplace, and armada-sync is the maintenance half of ship-armada. Each README states what it expects.

## Licence

MIT. Do what you like; attribution appreciated.

## Elsewhere

Fledgeling is [Luke Rhodes](https://www.linkedin.com/in/lukerhodes/), also co-founder of [Diolog](https://diolog.app).

[fledgeling.app](https://www.fledgeling.app) · [GitHub](https://github.com/lprhodes) · [X](https://x.com/lp_rhodes) · [LinkedIn](https://www.linkedin.com/in/lukerhodes/) · [hello@fledgeling.app](mailto:hello@fledgeling.app)
