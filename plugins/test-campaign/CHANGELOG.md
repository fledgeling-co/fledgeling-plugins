# Changelog

All notable changes to the `test-campaign` plugin.

## 0.9.2 — 2026-08-20

The blind-mutation check from 0.9.0 was measuring itself. Run against a real suite it reported
26 blind tests of 32 mutating; four defects in the detector accounted for 19 of them, and each
one made the pass report a larger number, which reads as thoroughness rather than as a broken
instrument.

**`--reader` replaced the seven defaults instead of extending them.** `tuple(args.reader) or
DEFAULT_READERS` means a project naming one reader of its own silently loses `assert_eq`,
`get_telemetry` and the other five, so every test reading through them is reclassified blind.
The flag that exists to teach the detector about a project made it blinder, and the resulting
rise in the count is indistinguishable from a thorough pass. Both flags now extend; `--only`
replaces, for the case where the defaults genuinely do not apply.

**The mutator pattern had no left word boundary.** `re.escape("record") + r"\w*\s*\("` matches
`record` inside `job_record(`, so a test whose only "mutation" was constructing a fixture was
reported as mutating-and-blind. Anchored with `(?<![A-Za-z0-9_])`, which still fires on
`.record(` and no longer fires inside an identifier.

**Fixture helpers were counted as tests.** A helper like `log_with_two_jobs()` mutates and
returns, leaving its callers to do the reading — so it is blind by construction and its callers
are not. Counting it inflated the denominator (168 where 141 is true) and added a finding about
a function nobody wrote as a test. A function called more than once in its own file is now
treated as a helper and excluded.

**The vocabulary could only come from the command line.** A project has to re-pass its flags on
every invocation or silently get the defaults, and a CI job that forgets them reports a clean
sweep. `campaign.json` now carries a `blindVocabulary` block with `mutators`, `readers` and an
optional `only`, and the run prints which source it used and how many terms it holds.

**`strict-check.py` never learned `effect-witness`.** The rung was added to `campaign.py` in
0.9.0 and its `EFFECT_RUNGS` set was not — so the rung that most strongly proves the product
acted scored in the same bucket as "something rendered", and building a real witness moved the
strict score by nothing.

## 0.9.1 — 2026-08-20

Three defects in 0.9.0's own effect census, all found by running it against the campaign it was
written for. Each read as a clean result, which is the failure mode the census exists to catch.

**`witnessed` was a subtraction, not a count.** It computed
`len(effect_reqs) - len(unbacked) - len(vacuous)`, so a requirement declaring an external effect
and recorded `reported` — claimed, never witnessed, and correctly not blocked — was subtracted
into the witnessed total and reported as an effect somebody had seen. On the egress registry that
printed `witnessed=1` where the true figure is 0. It now counts the requirements that actually
have a passing case at `effect-witness`, and names the rest as `unwitnessed` with their evidence
class beside them.

**The census printed only after the full-run verdict.** It sat past the selective-run `return 0`,
so on this skill's own default scope it never printed at all — a registry with eight vacuous
requirements said nothing about any of them, and the only place the numbers existed was `--json`.
It now prints in the header, beside the requirement and surface counts, on every path including a
blocked one.

**An unrecognised effect class vanished instead of blocking.** `add` refuses one, but a registry
edited by hand never passes through `add`, and an unrecognised class then simply failed the
membership test and dropped out of the census — indistinguishable from a requirement claiming no
external effect. `check` now blocks on it and names the classes it accepts.

`references/effect-boundary.md` §3 said a requirement whose declared effect has no provider is
`contradicted` at phase 1, where §2 of the same file defines `vacuous` for exactly that case.
Corrected, with the distinction spelled out rather than assumed.

Gate tests 48 → 53. The five new ones prove each of the above fires on a fixture built to trip it
and clears when the fixture is corrected.

## 0.9.0 — 2026-08-20

A campaign closed 230 cases over a CI runner built around zero-trust network isolation, armed 220
of them, cleared every gate this plugin owned, and recorded REQ-001 — "runner communication is
outbound pull only over HTTPS/WSS on TCP 443" — as **observed**. A reviewer on a neighbouring
project then read the source: no HTTP client anywhere in the dependency tree, no line of
production code that spawns a subprocess, `tart`, `wsl.exe`, `pfctl` and `nft` never executed, no
mDNS, and a daemon that only ever binds loopback. The isolation engines are rule generators and
state machines. Every network guarantee in the inventory was true because nothing crosses the
boundary they describe.

Nothing was broken here either. **Arming mutates the system** — revert the behaviour an assertion
guards, watch the case go red — and that finds what a suite does not cover. Ball & Kupferman named
it as one of a pair in *Vacuity in Testing* (TAP 2008): mutating the system finds coverage gaps,
and mutating the **specification** finds guarantees that were never exercised at all. This plugin
had shipped one half of a known pair 220 times and the other half never. Beer, Ben-David, Eisner
& Rodeh put the base rate at "typically 20% of formulas are found to be trivially valid, and
trivial validity **always** points to a real problem" (FMSD 18(2), 2001).

The standard toolkit cannot see it either, which is why the gap survived a mature campaign.
`cargo mutants` mutates the code that exists, so a boundary nothing reaches has no mutants;
coverage counts lines executed by the suite, and a rule generator's lines all execute; and the
whole isolation stack — `pytest --disable-socket`, `WebMock.disable_net_connect!`,
`nock.disableNetConnect()` — asserts the *absence* of I/O, so a suite built on it cannot
distinguish "correctly outbound-only" from "never communicates".

Applying the same lens **in-process**, needing no new lane and no privilege, immediately surfaced
a live defect the 230-case campaign passed: `stop_runner` returns `true` twice for the same
runner and never removes it, `stop_all_runners` reports "Stopped 2 runners" with the count
unchanged at 2, and `restart_runtime` returns "…restarted successfully" having restarted nothing.
The case covering it sat at the `outcome` rung, and the outcome it asserted was the arrival of a
sentence.

### Added

- **`references/effect-boundary.md`** — the two directions of mutation, the effect census, why
  mutation testing and coverage are both blind to this, the `effect-witness` rung with its
  four-part causal witness, `--seed-strengthen`, and the two places the research panel disagreed
  about where the floor sits on a machine without root.
- **`vacuity-check.py`**, three exact passes and a control. **unclassed**: a requirement whose own
  words name an effect outside the process and carries no `effect` field — it over-flags on
  purpose, because a false positive costs one `"effect": "none"` and a false negative costs the
  campaign its central claim. **uncensused**: an effect class with no `provider` named in
  production source. **blind**: a test that calls a mutating verb and never reads the observable
  again, so it can only be asserting the call's own return value. On the campaign above that pass
  read 164 test functions and found **26 of 32 mutating tests blind**, five of them in a file
  named for the effect it was not measuring.
- **`--seed-strengthen`**, this plugin's own arming rule turned on its new gate: strengthen a
  requirement's declared constraint until the registry cannot satisfy it, require red, restore the
  registry byte-for-byte. A strengthened constraint that still clears proves the census reads
  nothing.
- **The `effect-witness` oracle rung.** A recorder the product does not control — a packet
  capture, `dtrace`/`strace`, a real listener's accept log, a process table, a sentinel file —
  plus the effect class and the count it saw. `campaign.py set` gained `--recorder`,
  `--effect-class` and `--effect-count`; a claim at this rung with no recorder, no class, or a
  count of zero blocks, because a witness that saw nothing is the condition being tested rather
  than the proof of it.
- **The `vacuous` requirement evidence class**, the fifth beside observed / reported /
  contradicted / unknown. A guarantee that holds because the capability it constrains never runs.
  It is a finding in the same way `contradicted` is, and it clears the gate: a correctly recorded
  `vacuous` is finished honest work, and blocking on it would mean no campaign over a partly-built
  product could ever go green. What blocks is the dishonest configuration — an external effect
  class, recorded `observed`, with no passing `effect-witness` case behind it.
- **Sweep M, reality boundary and vacuity**, in `references/sweeps.md`: census, reachability,
  witness, sabotage, strengthening and blind mutation, with a denominator on each. Two of the six
  cost nothing and need no privilege.
- **Fifteen gate tests**, each proving a new blocker fires on a fixture built to trip it and then
  clears when the fixture is fixed. 33 → 48 passing.

### Changed

- `SKILL.md` carries a fifth failure mode; phase 1 produces the effect census alongside the
  requirement inventory; phase 5's rung table gains `effect-witness`; phase 7 gains sweep M; the
  CHECKED test gains a campaign-level obligation that every requirement claiming an external
  effect is either witnessed or recorded `vacuous`.
- `references/coverage-model.md` gains an **effect boundary** axis (in-process · own process tree
  · kernel · host · network) and connects instrument vacuity to product vacuity — the same shape
  one level up.
- `references/project-comprehension.md` carries the fifth evidence class and the closed effect-class
  list.

### Not settled

The panel split on where the witness floor sits, and the disagreement is recorded rather than
resolved. One reading holds that nothing below a kernel-observed causal effect may be recorded
`observed`; another holds that a machine without root still has a real floor — a genuine loopback
listener logging its accepts, or a real spawned process writing a sentinel — and that setting the
bar at `dtrace` on every host means the rung goes unused. `references/effect-boundary.md` §5
carries both.

## 0.8.0 — 2026-08-20

A campaign published 20 surface captures and cleared every gate this plugin owned — every case
accounted for, 46 of 49 checked under the strict rule, every `-glass` lane proved and witnessed.
The captures were of three unrelated documents: a project status report, the mock browser's own
index page, and a design accessibility doc. Twenty files held **six distinct images**; four groups
of four were byte-identical. A flow step captioned "Open pairing QR code sheet" showed a
questionnaire about Apple developer credentials.

Nothing was broken. `attach-shots.py` binds a picture to a surface on a slug of its **filename**;
`evidence-page.py` rendered it with an `alt` taken from the label, so a wrong image arrived under
a right-sounding caption; `campaign.py check` ran its artifact and duplicate detectors over
`RASTER_RUNGS` case evidence only, and the `shot` field the page actually renders was inspected by
nothing. The gated part of the campaign was sound and the ungated part was the part people look
at.

### Added

- **`references/capture-lineage.md` and `capture-lineage.py`** — `warrant:oracle`'s lineage plane
  with *picture* substituted for *figure*. There, a displayed number without a `data-source-ref`
  is the defect the plane exists to find; here, a published capture without a recorded target is.
  Four passes, all exact, none needing a model: **unsourced** (no manifest entry, or no target),
  **untied** (the target does not resolve to the subject's route), **shared** (two subjects, one
  sha256, undeclared), **unjudged** (published with no `be-my-witness` verdict — this one ratchets
  rather than blocks, for the same reason `strict-check.py` ratchets).
- **`--seed-swap`**, the gate watched to fail. Swapping two subjects' manifest entries must turn
  the tie pass red; a swap that passes means the pass reads nothing and every verdict it ever
  issued is worthless. That is the campaign's own arming rule turned on its own gate.
- **Phase 8a** in `SKILL.md`, between the differential and publication.
- **A fourth failure mode** in the opening: publishing a picture of one thing under the name of
  another.
- **Twelve tests** in `tests/run.sh` covering every new blocker in both directions, plus the
  seeded swap and the manifest it borrows and restores.

### Changed

- **`campaign.py check` audits the published shots**, not only raster-rung case evidence. Three
  new blockers: a shot that is not a usable capture, a shot repeating another subject's picture,
  and a shot bound to its subject by filename alone. The verdict now prints the wall's distinct-image
  count beside its cell count, so a gallery that repeats itself says so on its face.
- **`attach-shots.py` refuses to write an attachment no capture manifest corroborates.**
  `--filename-only` proceeds and stamps `"shotProvenance": "filename"` into the inventory, so the
  weakness travels with the data rather than being forgotten at the next read.
- **`evidence-page.py` badges every rendered capture** with how its subject was established —
  *witnessed*, *manifest*, or *filename*. It also anchors a flow step on the step's **own** id
  rather than one recomputed from the loop index, which used to renumber every anchor after a
  reordered step and silently repoint links a reader had already shared.
- **`witness-worklist.py` demotes a reference that is not a raster.** The measured campaign
  reported 20 judgeable pairs, 0 blind, every reference an unrendered `.html` path and
  `evidence/shots/mock/` absent — the pair template had never run and `pairs.json` was
  hand-authored metadata describing captures nobody took. Reporting that as judgeable is what let
  the whole comparison be skipped without anything saying so.
- **`assets/capture-pairs.template.mjs` writes `captures.json` as it shoots**, recording the URL
  the browser *ended up at* rather than the one it was sent to — a redirect to a login page is
  exactly the capture that otherwise gets filed as the dashboard.

### Why the four passes are deterministic

`be-my-witness`'s `prescan.py` returns `isEvidence: true, settled: true`, exit 0 against the worst
capture in that campaign: a real, contentful, settled image of the wrong document. Image statistics
cannot answer the subject question, and frontier multimodal models reach roughly 40% recall on
fine-grained UI diffs. Provenance answers it, and only if it is recorded while the shutter is open.

## 0.7.0 — 2026-08-19

A campaign could measure a repository thoroughly and a `warrant` in the same repository would
still refuse every tier, because neither plugin could read the other's state. And a case nothing
could settle resolved to `inconclusive` alongside cases an instrument merely failed to measure,
which sent half the work to the place that cannot fix it.

### Added

- **`unoracled: <reason>`, split from `inconclusive`.** The two arrive looking identical and have
  opposite remedies: `inconclusive` is an instrument problem and wants a better instrument;
  `unoracled` is a specification problem, where nothing was ever named that a check could read,
  and no instrument helps. Both hold the gate. The distinction is not new — a screenshot-judging
  pass over fifty surfaces once returned inconclusive on all fifty and the record said the
  verdicts were "for want of a judge rather than for want of an oracle", then every tool
  downstream collapsed the two halves into one status.
- **Phase 6a, oracle construction**, and `references/oracle-construction.md` behind it: a
  four-rung ladder from a specification-sourced outcome assertion, through a metamorphic relation,
  through a property-based invariant, to a recorded permanent limit in structural terms. Stop at
  the first rung that holds. Metamorphic relations are the standard answer to the oracle problem
  and the reason an unoracled case is tractable without a baseline; the evidence for them is
  directional rather than sized, and the reference says so.
- **`campaign.py export-warrant <dir> --root <repo>`** — writes `.warrant/suite-health.json` (the
  armed ratio, the effect-rung passes, the campaign's own gate) and `.warrant/oracle-coverage.json`
  (per surface, keyed by file path so warrant's `rollup_classes.py` can match it against the
  warrant's class globs). Nothing is inferred: a campaign that measured little exports little and
  the warrant still refuses the tier, which is the outcome that should follow.

### Why the export keys by path

The first cut keyed `oracle-coverage.json` by surface id, which matched no glob and rolled up to
zero coverage on every class — indistinguishable from a campaign that measured nothing. Caught by
running the full chain rather than by reading the schema. `rollup_classes.py` reads a list of rows
carrying `file`, `figures`, `sourced` and `unsourced`, and the export now emits exactly that.

### Changed

- `unoracled` is counted separately in `check` and `report`, named with its remedy in the blocker
  list, and folded into `unavailable` in the observation coverage rather than into `deferred`.

### Evidence

The two constraints on generating an oracle are measured and both are in the reference: roughly
half of LLM-generated test plans duplicate existing cases (50.5% duplicates, 22.5% invalid, 27%
valuable and new), so generation runs against a cell from the coverage model rather than
free-form; and the model that wrote the code may not be its sole oracle, because generated tests
demonstrably validate faulty behaviour and code in context biases later generation toward
mutually consistent but incorrect implementation/test pairs.
