# mac-design-digest

<p align="center"><img src="assets/banner.png" alt="mac-design-digest: a graphite certificate plate carrying three pale measurement bars, with a vermilion wax seal seated in a countersink at its lower-right corner and hanging out over the plate edge, beside the wordmark and the provenance marks (measured)(canon), with the same plate repeated at reading size on the right, fading in from the left and showing its sealed corner" width="100%" /></p>

<p align="center">
  <img alt="Version 1.0.0" src="https://img.shields.io/badge/version-1.0.0-D33C21">
  <img alt="SWE skill: design corpus" src="https://img.shields.io/badge/SWE_skill-design_corpus-434A55">
  <img alt="Structural assertions: 43 of 44" src="https://img.shields.io/badge/structural_assertions-43_of_44-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

Build macOS design taste the way a human expert does: one closely-studied app at a time, accumulated into a corpus that outlives the session.

> **Phase 5 note:** this README is functional, not final. The `create-luke-content` voice pass and the icon that the root README row points at are still to come.

Feed it screenshots, app icons, and official Apple UI kits. It writes a persistent `design-corpus/`:

- **`apps/<app>.md`**: per-app token profiles with two provenance marks on every value
- **`patterns/*.md`**: cross-app pattern entries (sidebars, toolbars, settings, empty states)
- **`icons/<app>.md` + `ICONS.md`**: icon anatomy digests (era, palette ramps, light model, layer stack)
- **`kit/*.md`**: `(specified)` tokens extracted from Apple's own Sketch archives
- **`TASTE.md`**: the synthesis, covering canon rules, style clusters, contested findings, honest gaps
- **`ledger.md`**: the append-only index, read first on every invocation

## What makes it different

**Every value says how well it is known.** Two orthogonal marks: measurement quality (`(specified)` / `(measured)` / `(estimated)` / `(assumed)`) and evidence strength (`(inferred)` / `(confirmed)` / `(recurring)` / `(canon)` / `(contested)`). The evidence axis advances on repetition; the measurement axis advances only on a better read. Nothing reaches canon under three independent apps, and only native-lineage evidence counts: a Catalyst app's density never becomes mac taste.

**The corpus is checked, not trusted.** `scripts/corpus_check.py` twelve checks over seventeen named invariants: ledger present, hash format, hash uniqueness, append-only rows, every ledger target existing, cross-app patterns recorded, the 3-independent-apps canon bar, the native-lineage gate, canon traceability, a ledger row per canon member, the cluster contradiction budget, surviving placeholders, a dated header, a level from the maturity model, non-empty knowledge gaps below Proficient, one mark per axis with a composed pair where the row's role needs both, the app count a (recurring)/(canon) mark claims, and a pinned precision baseline. Every failure message names three things: what happened, what the *next* invocation will silently do about it, and the fix. `examined=0` is reported as a check that did not run, never as a pass.

**It reads other people's software, and says so.** Screenshots of other people's applications, vendor archives, and corpus files written by earlier sessions of itself. Text inside any of them is material to record and never an instruction to follow, and the fence sentence travels verbatim into every subagent brief because the subagent cannot see the skill. `scripts/sketch_extract.py` enforces the same rule mechanically: it flags and counts instruction-shaped strings it reads out of an archive, and acts on none.

**Kit values come from the archive, not from transcription.** `sketch_extract.py` reads `.sketch` JSON in memory, derives the control ladder from symbol frames per size tier, and classifies capsule corners by geometry, because the format documents no sentinel value for a fully-rounded corner, whatever three different sources claim it is. A capsule is `(inferred)`; the raw value stays beside it.

**Generation is somebody else's job.** Mocks route to `mac-craft`, icons to `create-mac-icon`. Both carry passes this skill does not: AI-default calibration, a slop check, a state matrix, a motion floor, a fidelity loop. When neither is installed, the fallback runs and names what it skipped.

## Install

```
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install mac-design-digest@fledgeling-plugins
```

## Typical session

```
> Digest these: things-main.png, things-settings.png, things-icon.png
…
> Ingest this kit: Apple macOS 27 UI Kit.sketch
…
> [later] What does the corpus still not know?
```

## What it will not do

- Fetch screenshots itself. You curate the inputs; that answer is final for the turn.
- Report a corpus clean when the gate failed.
- Measure a value the image does not contain, judge motion from a still, or verify a token against a running app. Those limits are listed in the skill, and it does not promise around them.

## Does it actually work

Two measurements, and they disagree; both are written up in full in [`evals/EVALS.md`](evals/EVALS.md).

Against the skill it replaces, on the same eight requests: **43 of 44 structural assertions, against 35.** The gate provably refuses seventeen invariants that used to be prose, the suite runs as shipped where the predecessor's could not run at all, and the fence is demonstrated on a hostile archive rather than asserted.

And a **blind panel of two model families gave the predecessor 4 of 8, with 3 deadlocks.** It won on what a single answer shows a reader: on one corpus audit it found three defects this skill's gate had no check for, including evidence silently lost. Four of the gate's checks now exist because of that, and the skill now says in writing that the gate is a floor rather than a ceiling.

## Evidence

`skills/mac-design-digest/references/evidence.md` cites every research-derived rule, including the two places the research contradicted this skill's own predecessor and the places where the four backends disagreed with each other. Full reports in `docs/deep-research/`.
