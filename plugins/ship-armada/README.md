# ship-armada

The portfolio orchestrator: manages **every project in `~/Dev` as one portfolio**, sitting above `ship-fleet` (one repo's backlog) and `ship-feature` (one feature).

```
ship-armada → ship-fleet → ship-feature → stage skills
     ↘ armada-sync (manifest maintenance, runs with or without the armada)
```

Its memory is `~/Dev/ARMADA.md` (the manifest of record: index, groups, opportunities register, campaigns ledger, per-project entries) plus `~/Dev/CLAUDE.md` (portfolio operating rules). Five modes: **survey** (what's happening), **plan** (turn opportunities into campaigns), **route** (land one directive — "research feature X and incorporate it into <project>" — as research + a features-to-triage brief + an ORCHESTRATOR.md inbox row the project's active fleet picks up, or a new ship-fleet run when approved), **dispatch** (run fleets, ≤3 projects concurrent), **daemon** (recurring loop that proposes; executes only user-approved campaigns).

The skill is written to double as the **system prompt of a standing master-orchestrator agent** (e.g. a perch-hosted daemon): directives are classified into modes, assumptions are recorded in the artifacts instead of asked as questions, and ARMADA.md carries all surviving state.

Runners are Claude Opus (`claude-opus-5`); runner prompts follow the Opus 5 platform guidance (complete spec up front, explicit scope, no verification scaffolding, capped delegation, calm trigger language).

See `skills/ship-armada/SKILL.md` and `references/manifest.md` (manifest format + full-survey rebuild).
