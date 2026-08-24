# gemini.md — harbourmaster

Read this once, top to bottom, then read `SKILL.md` in full. Nothing here changes which plane work
belongs on or how a berth is taken — it changes what counts as *deciding*, and what counts as
*checking*.

harbourmaster is unusual among geminify's targets: most of its requirements are already numbers —
five planes, four verdicts, 80% of core count, multipliers of 1.00/0.85/0.50/0.25, 20 GiB,
90% swap, a 60 s dwell, a 180 s clear. **[docs]** That is what the health checklist asks for
under **Ambiguity**: "Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition. Instead, provide objective constraints". So the usual work — converting categorical
scopes into counts — is mostly done here. What is *not* done is the part where a number gets read
back, and this skill's whole output is a measurement handed to a caller: one nobody took reads
exactly like one that was.

## Epistemic status

**Tiers used:** `[docs]`, quoted verbatim and gate-checked; `[measured-family]`, Gemini runs of
*other* work — two single sessions (n=1 each) plus a 106-task benchmark scoring
`gemini-3.7-flash` against `claude-opus-5`; and `[derived]`. No `[measured-here]`.

**The tier this evidence is about.** Every measured claim below is flash-tier —
`gemini-3.7-flash`, plus two sessions on `gemini-3.7-flash-high`. None is measured on the Pro tier
and none may be projected there; on Pro these overrides stand as `[docs]`-grounded discipline while
every rate is open. Defaults drift too: **[docs]** "If thinking_level is not specified, Gemini 3
will default to high", then, from the 3.5 Flash notes, "The default thinking effort is now medium".

**Unmeasured on this skill:** no Gemini run of harbourmaster at all — no routing decision, no
berth read, no integration edit. No evidence a `gemini.md` fixes anything on any target, since no
run has been measured with one against the same work without one. And nothing in either source
covers a model *deciding* rather than building, this skill's primary output — so the rates below
bound the C9 lane and say nothing about the plane table.

**[docs]** A conditional side-file is itself the **Conflicting internal references** shape:
"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
together fragmented instructions". Hence one pass, and every override names where it lands.

## Route this skill's own work out, where it should be (C9)

The core work — choosing a plane, reading pressure, naming a weight — is **judgement**, and the
corpus behind this file measures a model *building*, so it gets no route-out row; abstaining is
honest when the evidence is about a different question. One lane does build: `Calling this from
another skill` and `references/integration.md` edit a caller's existing loop — ship-fleet's fixed
slot count becomes a `berths.py` read — a brownfield edit to a repo whose loop passes today.

| shape | when it applies here |
|---|---|
| `brownfield-integration` | editing a caller's runner loop or build step to take berths |
| `regression-sensitive` | that loop works today and must keep working after the edit |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

**[docs]** Under **Task outside of model capabilities**: "Avoid using prompts that ask the
model to perform a task for which it has a known, fundamental limitation."

**[measured-family]** On the benchmark's brownfield bucket (28 tasks) `gemini-3.7-flash` scored
16.1 at `medium` against opus's 46.4, with a hard zero on 79% of decided rows; a same-scaffold
control puts it at the bottom of a cohort spanning 20 to 65 points, so that is an upper bound. Rows
omitted: `static-page` (this skill authors no self-contained page) and `visual-design` (it renders
nothing). Where no lane is available, do the work and treat the wiring edit as the part to distrust.

## O1. Probe every plane, not the first that fits

**Lands on** `Route first` and `references/routing.md` — "Take the one whose resource is least
scarce at that moment, measured rather than assumed", which names a probe per plane. The failure
guarded is not choosing wrongly; it is answering after checking one thing.

| plane | probe | ran | answer | verdict |
|---|---|---|---|---|
| this Mac | `scripts/pressure.py` | yes | `overall: busy`, disk 72 GiB | 10 berths, 6 held → 4 free |
| errand node | `anvil errand --check` | yes | `denied errand_ticket_unavailable` | unavailable |
| proctor | read the foreground queue | n/a | no native app in this work | — |
| defer | `lane_pick.py --report` | yes | fable clear, codex at limit | one lane open |
| subagents | none needed | n/a | nothing to search | — |

Report the fraction: `5 of 5 planes assessed, 2 n/a with reasons`. A plane skipped without a reason
is a plane you did not consider. **[docs]** The `n/a` cell is Google's own remedy for the
underspecified case: "provide instructions for handling missing data rather than assuming inserted
data will always be present".

**[measured-family]** In the run this file's family evidence comes from, every *enumerated*
requirement was delivered — twelve named features, all present — while every requirement named
*categorically* landed once or not at all: all surfaces → 5, all states → 1, all menus → 0.
Five named planes is an enumeration; "consider the planes" is not. Weight likewise comes from
`references/admission.md`: 1 for a unit test, 2 for a runner, 4 for a suite, 6–8 for a full build.

## O2. Exit 75 is a retry ceiling, and the skill already wrote it

**Lands on** `Then admit`, which states it twice: "Do not loop on the call", and "A call that
blocks past a tool timeout becomes a retry storm, which is worse than the queue it was trying to
be." **[docs]** From the agentic template's persistence rule: "On *other* errors, you must change
your strategy or arguments, not repeat the same failed call."

**[measured-family]** Two sessions, each looping instead of pivoting: four consecutive `Read`
calls against a 25 000-token ceiling before switching to a Python split, and four invocations of a
tool banned by the repo and absent from the machine, failing every time.

| result | attempts | what to do instead |
|---|---|---|
| 75 with `hard_gate` | 0 | stop scheduling; hand disk to `mac-doctor` |
| 75 without | 1, after `retry_after_sec` | do other work between — never a tight loop |
| 64 | 0 | fix the weight; impossible at any pressure |
| any other code | 0 | it is the workload's — read the workload's output |

The ceiling covers hard capacity errors anywhere in the run: on the *first* `File content exceeds
maximum allowed tokens`, pivot to chunking or a line-ranged read, not a tweaked offset.

## O3. Paste the reading; a verdict with no command above it is a claim

**Lands on** `Pressure, and what it changes`, `Thermal`, `The ledger`. **[docs]** Verification
is something the prompt has to contain: "Include specific verification steps in either the system
instructions or your prompts directly", and "Verify your claims by quoting the exact applicable
information".

**[measured-family]** Where that scaffolding was absent the vacuum filled: a review with five
well-formed `PASS` rows naming a CDP harness that failed all four invocation attempts and never ran,
a "100% pass rate on contrast" from a probe never executed — measured afterwards at 3.65:1 on every
primary button, one glyph at 1.00:1 — and an audited count of 47 that nothing produced. Say that
this reverses the house style: removing verification scaffolding is right for a model that
over-verifies, and inheriting that removal here is the defect. The skill supplies the shape for an
absent reading — "Without that grant this lane reports `unobservable` and changes nothing — which is
the honest answer, not a claim that the machine is cool." Ship the note filled:

```
pressure   scripts/pressure.py         → overall "busy", disk 72 GiB, swap 3.7/5.1 GB  0.36 s
berths     scripts/berths.py           → ceiling 10, in_use 6, available 4
thermal    scripts/thermal.py --check  → unobservable (no passwordless powermetrics)
decision   local plane, weight 4       → governor-run exit 0
3 readings taken, 1 unobservable and named. No verdict reported without its line.
```

Occupancy is read back from the locks and never stored, so never report a remembered berth count;
and `unknown` is not `healthy` — it "carries the same multiplier as `critical` (0.25)".

## O4. Route and admit are two phases, with an artifact between them

**[docs]** The remedy for an overloaded pass: "make each step a prompt and chain the prompts
together in a sequence." **[measured-family]** Where composition was phrased as a standard rather
than a step whose output a later step consumes, both invocations were skipped, and the run's own
diagnosis named the mechanism: nothing downstream depended on a file only those steps produce. The
scan found **no** qualitative skill references here — `mac-doctor`, `defer` and `proctor` are scope
fences — so the conversion applies to this skill's own stages instead:

1. Probe → the O1 ledger, written out before any decision sentence.
2. Decide → cite rows by name; plane and weight each trace to a cell.
3. Admit → `governor-run --weight <that cell> --project <repo> --label <what>`.
4. Record → `scripts/ledger.py` writes `~/Dev/FLEET.md`, the concrete artifact that makes the
   chain mechanical; a refill re-reads `scripts/berths.py` — the skill's own "re-read on every
   refill rather than once at the top" — and never reuses step 1's number.

## O5. `gate` — the scripts are the answer, and their surface is checkable

**Module fired:** `gate`, 5 triggers — `berths.py`, `pressure.py`, `thermal.py`, `demote.py`,
`governor-run`, plus `scripts/selftest.sh` and `tests/run.sh`. **[docs]** "use a widely recognized
standard like JSON, XML, Markdown or YAML". These emit JSON; quote it, and print the denominator.

**A flag the script does not define is a refusal, not silence.** `berths.py` parses only `--quiet`;
any other argument exits 2 and names itself. It used to be silence — an unknown flag spawned a
one-shot read that exited 0 with no lock held and nothing recorded. That happened here once, which
is why `tests/check_surface.py` exists and why the read scripts now refuse. Read the surface before
invoking — and note claims are `governor-run`'s alone: `berths.py` reads, it never takes.

| script | flags it defines |
|---|---|
| `berths.py` | `--quiet` |
| `pressure.py` | `--max-age`, `--fresh`, `--no-cache` |
| `governor-run` | `--weight`, `--project`, `--label`, `--wait`, `--qos`, `--dry-run` |
| `demote.py` | `--apply`, `--min-cpu`, `--max`, `--include-agents`, `--restore` |
| `thermal.py` | `--duration`, `--check` |

**Prove the gate can fail before trusting it passing.** `tests/run.sh` already builds a fixture
designed to trip each direction and confirms it fires before trusting a clean tree, and
`selftest.sh` targets the properties that "fail SILENTLY — where the governor keeps reporting
success while governing nothing". **[measured-here]** On geminify's own quote gate, a one-line
change took the checked count to zero and turned every file green, negative control included —
caught only because the control was re-run rather than assumed.

## O6. `delegation` — keep the cap, take the probe over the question

**Module fired:** `delegation`, 5 triggers. The cap is already written: "cap that fan-out at four;
a berth check and a routing decision need none." **[docs]** The five planes are a closed set, and
the remedy for an answer that strays outside the offered options is structural: "you can rephrase
the instructions as a multiple choice question and ask the model to choose an option." Answer with
one of the five, named. And on acting rather than asking: "Prefer calling the tool with the
available information over asking the user" — `anvil errand --check` changes nothing and answers in
one call, so run it rather than asking whether the node is up.

**The advice has two parts under `tiered`.** The skill names a sixth resource with no plane and no
meter — the conductor's attention — whose constraint "will not appear in any reading this skill
produces". A fleet-width answer there is a two-cell deliverable, the berth number and the attention
caveat, reported `2 of 2`. **[measured-family]** O1's categorical collapse in different clothes.

## O7. Read the value; do not recall it

**[docs]** "The knowledge cutoff date for Gemini 3.7 Flash is March 2026" — with older domains
still at the January 2025 floor — and the remedy: grounding "should be enabled whenever the model
may need to know obscure or recent facts". **[measured-family]** What a stale floor looks like from
outside: Windows 10's `#0078D4` accent on a Windows 11 app — a previous-generation published value
returned confidently, among eight metric errors in one artifact.

Here that lands on `Thermal`: `powermode` is `0` Automatic, `1` Low Power, `2` High Power, and
`pmset -g custom` reports per power source, so the wrong branch reports a mode the machine is not
in. Read these from `references/thermal.md` or `pmset`, and the frequency ladder's top inline from
`powermetrics`, since it is per-SKU.

**Read, then answer — two ordered steps.** When a prompt names a file or a skill
(`references/routing.md`, `defer`, `proctor`), load it and then answer. **[measured-family]** Asked
a question naming three skills, one run answered from memory without loading any; asked to fix that,
it launched a skill instead of answering. Neither step substitutes for the other.

## O8. `thinking_level`, written as what it is for

**[docs]** "suitable for complex prompts requiring deep reasoning, such as multi-step planning,
verified code generation". A routing decision is a short lookup against three probe outputs, which
is not that; the C9 integration lane is, and that is where `HIGH` is what Google describes — uplift
unmeasured on this corpus. **[measured-family]** Paired across 106 tasks, `high` beat `medium` on
24, lost on 24 and tied on 58, mean −1.7 points, so raising the level is not the remedy for anything
in O1–O7.

**[docs]** And one coupling: "Higher thinking levels encourage the model to use more tools to
explore and verify, so lowering the level can reduce tool calls." Fewer tool calls is the wrong
direction here; do not lower the level to save on probes.

## What transfers intact

- **The plane table** — five named rows, each with the resource it spends.
- **Every threshold is already a number** — 80% of cores, the four multipliers, 20 GiB, 90% swap,
  60 s dwell, 180 s clear. **[measured-family]** That is the one bucket where the benchmark gap
  closes: where the brief states a bound, 74.7 against opus's 75.0.
- **The exit-code contract** (75 with and without `hard_gate`, 64, other) — a closed set with a
  response per code, already O6's multiple-choice shape.
- **Refusal kinds over sentences**, and **"A berth report is two lines, not a table"**.
  **[docs]** "By default, Gemini 3 models provide direct and efficient answers." Brevity trims
  preamble, never O3's readings.
- **The scope fence** — a hand-off list rather than a lens, so O4's conversion does not apply.

## What was not written, and why

The scan read 671 lines across `SKILL.md` and five references. Two modules cleared the three-trigger
threshold — `gate` (5) and `delegation` (5) — and both are written; the other eight did not fire and
none is written (`visual`, `states`, `platform-values`, `authorship`, `injection`,
`bounded-constraint`, `count-contract`, `emphasis`). The nearest miss is `platform-values`, which O7
carries instead, because those values are read from the skill's own references rather than recalled
from an external design system. Four of the scan's five candidate rows are prose rather than
deliverable scope and were dropped: the quota row at `SKILL.md:154`, the bounds at `SKILL.md:34`
and `references/thermal.md:24`, and the relative qualifier at `SKILL.md:221`. The survivor is the
weight table at `SKILL.md:94`, folded into O1 rather than given a bound ledger of its own —
`bounded-constraint` did not fire, and a module written for one row is the same defect as a module
fired on a skill it does not fit.
