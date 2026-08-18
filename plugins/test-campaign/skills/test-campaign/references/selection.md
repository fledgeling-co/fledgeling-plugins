# Selection — which cases this run actually needs

A campaign that runs everything every time gets run less often, then stops being
run at all. That is the failure this file exists for, and it is worse than the one
it risks: a forty-minute gate on a five-minute change is a gate somebody switches
off, and a switched-off gate catches nothing. So a run **selects**, and covering
everything is a decision somebody made rather than a default nobody chose.

That inversion sits uncomfortably close to this skill's first failure mode —
*covering a subset and reporting it as the whole* — and the discomfort is the
point. Selection is only distinguishable from silent narrowing by three things,
all mechanical:

1. The scope is **declared** before the run, with a basis another person could
   reproduce.
2. Every case the run did not select is **carried** with that basis attached, so
   the ledger says "not run this time, unchanged since X" rather than "pass".
3. The verdict **names its own scope**, so a selective green cannot be read as a
   full one.

Miss any of the three and this is the narrowing failure wearing better clothes.

---

## 1 · The decision ladder

Three rungs. The first that applies decides, and the choice is recorded in
`run.decidedBy` so a reader knows which rung fired.

**Rung 1 — somebody asked.** "Run everything", "full regression", "all the
gates", "check the whole app". Full run, no inference, no argument. Equally: a
request scoped to one feature is a request for a selective run, and answering it
with the whole suite is not generosity, it is forty minutes of somebody's
afternoon.

**Rung 2 — the model running the campaign infers it.** You are the one holding
the diff and the context, so this is your call to make rather than a flag to wait
for. Infer a full run when:

- a lockfile, dependency manifest, build config, CI config or toolchain version
  moved — the blast radius of a dependency bump is the whole application, and no
  file-level mapping models it
- a shared component, design token, global stylesheet, theme, layout shell,
  router, auth guard or i18n bundle changed — a change with no local blast radius
  reaches surfaces that do not mention it
- the previous run failed, or was itself selective and left the failure carried
- the target environment is new to the campaign, or the base URL, tenant or
  backend changed
- a release, tag, deploy or migration is what prompted the run
- the diff is a wide refactor: many files, mostly small, no single feature

Otherwise infer selective. **Say which you inferred and why, in the reply.** An
inference nobody can see is an assumption.

**Rung 3 — default.** Selective, against the last full run.

---

## 2 · The always-run floor

Change-to-test mapping is a heuristic, and it is unsafe in the specific sense
that matters: the case it wrongly drops is indistinguishable from the case that
passed. Genuinely safe selection needs a dependency graph the harness maintains;
a glob from changed paths to test files does not have one. So a floor exists, and
selection may never reach below it.

**Always runs, every run, whatever the diff:**

- **Every `critical` flow's effect-rung case.** A critical flow promises an
  effect; carrying that promise forward is exactly what nobody should trust a
  heuristic with. `campaign.py carry` refuses to carry these and reports them as
  `protected`; `check` blocks if one was carried some other way.
- **The gate's own checks.** A selection that can silently disable the thing
  measuring it is not a selection.
- **Anything in the blast radius** as derived in §3, including transitively.
- **Whatever the harness cannot map.** A test the mapping cannot place runs. The
  default for unknown is *include*, never *exclude* — an unmappable test that
  gets dropped is the silent case again.

A floor that is small enough to run on every commit is a design constraint on the
campaign, not an afterthought. If the floor takes forty minutes, the floor is the
problem.

---

## 3 · Deriving the blast radius

This skill already builds the mapping that makes selection possible, which is the
reason selection belongs here rather than in the harness alone: the surface map
says where each surface lives, the component axis says which surfaces a component
appears on, and every case names its requirement, surface, flow and cell.

From a changed path, walk outward and stop at the first honest answer:

| changed | selects |
|---|---|
| a surface's own view/route files | that surface's cases, and every flow whose steps name it |
| a component | every surface the component atlas places it on — this is why components are their own axis |
| a shared style, token or theme | full run (§1 rung 2) |
| an API handler or schema | the cases whose data-shape cell touches it, plus every flow that writes through it |
| a test file only | that test, plus proof it still bites (§4) |
| docs, PRD, design of record | the requirement trace and the differential, not the whole suite |
| anything the map does not place | full run, and a finding that the map has a hole |

Record the derivation, not just its result. `--basis "changed: src/pricing/**,
packages/ui/Button.tsx since v2.3.1 → SURF-004, SURF-011, FLOW-002"` is
reproducible. `--basis "pricing changes"` is a summary of a decision nobody can
re-check.

---

## 4 · The ledger contract

```bash
python3 $S/campaign.py scope <dir> --full --max-full-age-days 14 \
    --decided-by "user asked for every gate"

python3 $S/campaign.py scope <dir> --selective \
    --basis "changed: src/pricing/** since v2.3.1 → SURF-004, FLOW-002" \
    --decided-by "default (nothing asked for a full run)"
python3 $S/campaign.py carry <dir> --ran CASE-0117 --ran CASE-0118 \
    --basis "unchanged since v2.3.1"
```

`unselected` is its own state and not a kind of `skip`. A `skip` says this case
should not run; `unselected` says it did not run *this time* and its previous
verdict is carried. Each carried case keeps `carriedFrom` — the result being
carried — and `selectionBasis`.

`check` then blocks on:

- a selective run with no basis, or with no recorded `lastFullRun` to carry from
- a carried case naming no basis
- a critical flow whose every effect case was carried
- a `lastFullRun` older than `maxFullRunAgeDays`

and its verdict line prints `SELECTIVE — ran 12/225 cases, carried 213`, the
basis, and how many days old the full result is. **A selective run still exits 0
when it is internally complete**, deliberately: a gate that can never go green
gets marked non-blocking within a week, and then it is another switched-off gate.
What it must never do is print the same sentence a full run prints.

**Freshness is the number that decays.** A carried pass is evidence about the
code as it was at `lastFullRun`, not as it is now. That is why the age is on the
verdict line and why the bound is a blocker rather than a warning — twelve
consecutive selective runs are a full suite nobody has executed in a fortnight.

**A changed test proves nothing until it is watched to fail.** When the diff is
the test rather than the code, selecting it is not enough: re-arm it. An assertion
edited and then passed is the one place selection can manufacture a green.

---

## 5 · Existing suites and existing gates

A project that already has tests almost always runs all of them on every commit,
and the same inversion applies. Mirror what is there; never impose a parallel
selection mechanism beside one the harness already has.

**First, find out whether the harness selects natively**, and verify the flag
against the installed version rather than this list, which goes stale: Jest
(`--onlyChanged`, `--changedSince`), Vitest (`--changed`), Playwright
(`--only-changed`), pytest (`pytest-testmon` for change mapping; `--lf` is
last-failed, which is a different thing), Nx (`affected`), Turborepo (`--filter`
with a git range), Bazel (affected targets by query), Gradle and Go (per-target
caching, automatic). Run its `--help`; a flag that does not exist fails in a way
that looks like a clean selective run of nothing.

**Where the harness selects natively**, wrap it rather than replace it: take its
selected set as the `--ran` list, and put this file's discipline around it — the
declared basis, the carried cases, the floor, the staleness bound. The harness
knows the dependency graph better than a glob does; it does not know which of
your flows is critical.

**Where it does not**, select at the campaign layer using §3, and say so in the
ledger — a campaign-layer selection over a harness with no dependency graph is
coarser, and the floor carries more weight as a result.

**Then audit the existing gates the same way.** For each CI job, pre-commit hook
and pre-push hook, establish what it runs and on what trigger, and convert it to
the ladder: selective by default, full on the rung-2 triggers, full on a
schedule that satisfies the staleness bound. Two things to look for while you are
in there, because both are common and both are this skill's own failure modes:

- **A gate that runs everything on every commit and is therefore skipped.** Look
  for `--no-verify` in the shell history, `[skip ci]` in commit messages, or a
  required check that somebody made optional. That is the switched-off gate, and
  selection is the fix.
- **A gate that already selects but does not say so.** Far more dangerous. It
  reports a green with no scope, no basis and no denominator, so a partial run
  reads as a full one — which is the narrowing failure already in production.
  Fixing its output matters more than fixing its selection.

Report what you changed per gate, and what each one now runs on which trigger.
An existing gate you left alone is a stated decision, not an omission.
