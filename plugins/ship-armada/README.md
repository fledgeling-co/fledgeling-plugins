# ship-armada

The portfolio orchestrator: manages **every project in `~/Dev` as one portfolio**, sitting above `ship-fleet` (one repo's backlog) and `ship-feature` (one feature).

```
ship-armada → ship-fleet → ship-feature → stage skills
     ↘ armada-sync (manifest maintenance, runs with or without the armada)
```

Its memory is `~/Dev/ARMADA.md` (the manifest of record: index, groups, opportunities register, campaigns ledger, per-project entries) plus `~/Dev/CLAUDE.md` (portfolio operating rules). Four modes: **survey** (what's happening), **plan** (turn opportunities into campaigns), **dispatch** (run fleets, ≤3 projects concurrent), **daemon** (recurring loop that proposes; executes only user-approved campaigns).

Runners are Claude Opus (`claude-opus-5`); runner prompts follow the Opus 5 platform guidance (complete spec up front, explicit scope, no verification scaffolding, capped delegation, calm trigger language).

See `skills/ship-armada/SKILL.md` and `references/manifest.md` (manifest format + full-survey rebuild).
