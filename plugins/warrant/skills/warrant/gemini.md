# gemini.md — `warrant`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the
section it lands on. `warrant` is a map: `It routes and explains; the eight skills do the work.` That
makes its failure mode narrower than the skills it points at, and sharper — a question about this
plugin has a fluent, well-shaped, plausible answer available without opening a single state file, and
the answer to `how much authority a model currently holds` is a fact about `.warrant/` rather than a
fact about the ladder table.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`: **no Gemini run of
  `warrant` has been observed**, at any tier.
- **`[measured-family]` sources:** two single sessions (n=1 each) and a 106-task benchmark at two
  effort levels — `geminify/references/evidence.md`. Neither watched a model route a request between
  skills or report a pipeline's state.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
  (one session on `gemini-3.7-flash-high`) — flash-tier claims, **not** to be projected onto the Pro
  tier. **[docs]** The default drifts inside the family: *"If thinking_level is not specified, Gemini
  3 will default to high."* against, from the 3.5 Flash release notes, *"The default thinking effort
  is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these overrides stand as
  `[docs]`-grounded discipline and every `[measured-family]` number is open.
- **Unmeasured on this skill:** no Gemini run of `warrant` · no evidence a `gemini.md` fixes anything
  on either source · **nothing measures this family routing rather than building**, so the transfer of
  every rate below to a map skill is `[derived]` · nothing measures it reading the regulatory evidence
  (`C11`, `C12`, `C21`) this skill's opening rests on.
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns about:
  *"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
  together fragmented instructions from multiple different places in the prompt."* One pass, then
  work from `SKILL.md`.

## There is no route-out block here

geminify writes one only where the benchmark measured the work, and `warrant` fails both conditions.
**Its work class is one the corpus abstains on:** naming which skill a situation calls for is
`referral`, where `lane_pick.py` returns the policy answer unchanged — the bench measures a model
building an artifact, and this skill builds none. **And none of the four measured shapes is a thing
it produces:** no page (`static-page`), nothing rendered to judge (`visual-design`), no repo edit
(`brownfield-integration`), no passing contract to break (`regression-sensitive`). **[docs]** *"Avoid
using prompts that ask the model to perform a task for which it has a known, fundamental
limitation."* The skills this map routes to carry their own blocks; `warrant:oracle`'s is the only one
in this set that fires.

## What the scan found, and what was dropped

Two quota rows, two bounds, two relative qualifiers, **0** qualitative skill references, **0** shouted
tokens. Four of those six are prose rather than deliverable scope and were dropped:
`every item` (line 7) is the frontmatter describing when to invoke the skill; `at most 11` (line 99),
`short` (line 97) and `significantly` (line 108) all sit inside quoted research findings — `C2`'s
aggregation gap and `C8`'s odds ratio — where changing the wording would misreport a source.

What survives is the pair this file is built on: **`Every claim`** id must resolve, and **`at most
three`** subagents. `delegation` fired on the scan; `gate` is added by hand, because
`scan_skill.py --refs` globs `<skill>/references/*.md` while this plugin keeps its references one
level up, and `gate` reaches three triggers once they are included. `visual`, `states`,
`platform-values`, `authorship`, `injection` and `count-contract` did not fire and are not written;
`bounded-constraint` reaches three across the reference set, but every bound it finds there is already
enforced by `charter_validate.py` or `_cli.rate()` rather than restated for a reader.

## What transfers intact

**The forced order is already an artifact chain, which is the one thing C4 asks for.** `Run the
planes in this sequence, because each one's output is the next one's input` — and every step names
the file it writes: `test-campaign`'s `campaign.py export-warrant` writes `suite-health.json` and
`oracle-coverage.json`, `lineage_gate.py` writes `.warrant/oracle-coverage.json`, `rollup_classes.py`
writes the `classes` block both consumers read. **[measured-family]** §1.2.1 is the failure this
avoids: a run skipped both skills its brief told it to compose with, and its own diagnosis was that
nothing downstream mechanically depended on a file those skills produce. Here everything does. Keep
the phrasing; Override 2 adds only the existence check.

**Absent evidence is already a distinct answer.** `Absent evidence is an unmet condition here by
design, which makes "never measured" and "measured badly" identical to charter_validate.py` — and the
skill immediately says which one it usually is and that re-running will not tell you. That is core C2
already written, better than this file would state it.

**The delegation section is a closed rule with a number**, which is why `delegation` below is one
override rather than a section: `Cap: at most three subagents for one task in this plugin.`

## Override 1 — the state question is a file read, and its answer is a transcript (`## The ladder`, `## Who drives this`)

`SKILL.md` is invoked to answer `how much authority a model currently holds` and `why a class was
revoked`. Both have a fluent answer available from the ladder table alone, and both are wrong unless
they come out of `.warrant/`. **[measured-family]** §1.1.2 (n=1) is what filling a shape without
running the procedure looks like: a verification document of five well-formed rows, all `PASS`,
naming a browser engine as verified when it had failed all four invocation attempts, `100% pass rate
on contrast` from a probe never executed — measured afterwards, every primary button 3.65:1 and one
glyph 1.00:1, invisible — and `Interactive Targets Audited: 47`, a number nothing produced. The
reading in §1.1.2 is that this is a model completing a requested **shape**, and a five-tier ladder is
a very clear shape.

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* and *"Verify your claims by quoting the exact applicable information (including policies)
when referring to them."* Ship the transcript filled, not a table you wrote:

```
charter  charter_validate.py --root .   → exit 0 · signed 2026-07-11 · renews 2026-10-09
tiers    ratchet.py --root . --json     → 7 classes · 4 at tier 1 · 1 at tier 2 · 2 at tier 0
revoked  ledger_verify.py --root .      → exit 0 · 1,412 rows · chain intact
         last revocation: disclosure-figures 2026-08-19 · pinned lane model version differed (C12)
gaps     rollup_classes.py --root .     → 2 classes green: false · no surface matched their globs
```

**[docs]** *"When model outputs must be machine-readable or follow a specific format, use a widely
recognized standard like JSON, XML, Markdown or YAML that can be parsed by common libraries."* Every
script here takes `--json`, and `In --json mode, stdout carries the JSON object and nothing else`, so
read it in Python rather than by eye. **[docs]** *"Gemini's code execution tool enables the model to
generate and run Python code, and should be enabled whenever the model needs to perform any kind of
arithmetic, counting, or calculation."*

Two answers to hold to. A class the warrant does not name `sits at tier 0` — report that as
unnamed, not as unearned. And a `green: false` from `rollup_classes.py` means no surface matched,
which is `no evidence` rather than a failure; **[docs]** *"provide instructions for handling missing
data rather than assuming inserted data will always be present and well-formed."*

## Override 2 — the order is a chain of files, so check the file before the next step (`## The order is forced`)

The section already names the artifacts. What it does not do is make the check explicit, and two of
its steps are the ones most easily read as optional: step 0 is another plugin, and step 6 is a bare
script line between two named skills. **[measured-family]** §1.2.2: an auditor validated its final
properties thoroughly, had **zero** checks that prerequisite artifacts existed, and returned exit 0
over two skipped upstream steps. Here the consequence is stated by the skill itself — skip
`rollup_classes.py` and `every class reads as having no evidence`.

So run the chain as a chain, and confirm each file before the step that consumes it:

```
0. test-campaign  campaign.py export-warrant → .warrant/suite-health.json, oracle-coverage.json
1. charter        charter_validate.py        → exit 0, or nothing below runs
2. oracle         lineage_gate.py            → .warrant/oracle-coverage.json  (surfaces)
3. assay          → .warrant/suite-health.json  (mutation score, high-water)
4. panel          lane_run.py                → verdicts/*.json + a digest
5. lot            lot_plan.py                → refuses without suite-health.json
6. rollup         rollup_classes.py          → the `classes` block in BOTH files above
7. ratchet        ratchet.py                 → tiers, revocations, proposals
```

**[docs]** *"make each step a prompt and chain the prompts together in a sequence."* A missing file at
any step is exit 3 — `a precondition is absent` — and re-running the same step changes nothing until
the step above it has run. `feedback` and `ledger` sit outside this order by design.

## Override 3 — three subagents, counted, and never one that checks your work (`## Delegation`)

`delegation` fired. The cap is already a number — `at most three subagents for one task in this
plugin` — so the override is to read it back rather than to restate it: name each subagent, what it
returned, and the running count, in the note. **[docs]** Google's remedy for a model answering outside
a closed set is to state the set: *"The response is correct, but the model didn't stay within the
bounds of the options."*

The skill's own test for when to spawn one is already closed — `a wide read across many files where
you need only the conclusion`, or `two genuinely independent tracks each larger than a handful of tool
calls` — and everything else is `Do the work yourself`. **[docs]** The agentic template leans the same
way on low-risk reads: *"For exploratory tasks (like searches), missing *optional* parameters is a LOW
risk."*

One case is closed entirely, and it is this plugin's subject: **no subagent verifies your own
output.** `references/opus5-authoring.md` states it as a property of the plugin — `No prompt in this
plugin asks a model to re-check its own output.` — because `The pipeline's gates are scripts with exit
codes.` A delegated re-check is a second vote in a plugin whose central measurement (`C2`) is that a
second vote buys almost nothing.

## Override 4 — every claim id resolves, and none is quoted from memory (opening section)

This is the quota row that survived, and it is the highest-value one in the file. Seven claim ids
appear in `SKILL.md` — `C2`, `C8`, `C11`, `C12`, `C18`, `C21`, `I7` — carrying nine figures between
them: two effective independent votes, 8 to 22 percentage points, at most 11%, 323,973 women, odds
ratio 0.53, over 15,000 mutants, more than half surviving. `Every claim id resolves in
docs/deep-research/claims.json, and references/evidence.md separates the direct findings from the
inferences.`

**[docs]** *"Your knowledge cutoff date is January 2025."* **[measured-family]** §1.1.4 is what a
recalled published value looks like from outside: a previous-generation accent colour returned
confidently — an old fact rather than a guess. Regulatory citations are the same genre, and 21 CFR
Part 11 and PCAOB AS 2201 are exactly the kind of thing a model can restate fluently and slightly
wrong. Fill this before citing anything:

| id | cited for | resolved in `claims.json` | tier |
|---|---|---|---|
| `C2` | the not-a-jury argument | yes | direct finding, preprint, different domain |
| `C8` | blind placement of the human sample | yes | direct finding, observational |
| `C11` | Part 11 signatures are individual | yes | direct finding; reach into release control is unclassified |
| `C12` | PCAOB benchmarking of an automated control | yes | direct finding; the reversioning inference is `warrant`'s own |
| `C18` | over half of 15,000+ mutants survived | yes | direct finding, one codebase |
| `C21` | no vendor found with an accepted all-machine step | yes | search absence, not a proof |
| `I7` | the unsupported-figure class is closable by arithmetic | yes | **inference**, marked `I` |

The `C`/`I`/`M` prefix is the tier and must survive into anything you write: `A claim id beginning C
is a direct finding from a source. One beginning I is an inference assembled across findings —
reasoning, not a result.`

## Override 5 — routing is the deliverable, and it is a closed set of eight (`## The eight skills`)

The answer to a routing question is a skill name and the command that starts it, not a synthesis of
the plugin. **[measured-family]** §1.2.4 recorded both halves of this failing in one session: a
question naming three skills was answered from prose memory without loading any of them, and the
correction inverted the error by launching a skill when the user wanted an answer. Read, then answer,
as two ordered steps — open the skill you are about to route to before describing what it does, and
still write the answer yourself.

**[docs]** *"By default, Gemini 3 models provide direct and efficient answers. If you need a more
conversational or detailed response, you must explicitly request it in your instructions."* A map
skill is the one place where the terse default undersells: name the skill, say what it will run, and
say what it needs to have run first. Where a request does not land on one of the eight, say which
condition is unmet rather than picking the nearest — the commonest case is the one the skill already
names, a repository whose surfaces were never given a checkable property, where `running the planes
again will not tell you which`.

## Override 6 — two attempts, and the exits that are not transients

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* **[measured-family]** Both n=1 sessions ran the loop: four consecutive invocations of
one banned, absent tool with nothing changed between them (§1.1.2), and four consecutive `Read` calls
against a 25,000-token ceiling before pivoting to a Python split (§1.2.3). `gemini-cli` ships a loop
detector whose halt message names *"repetitive tool calls"* (§7.2). Here: exit 3 is a missing
precondition and points at a step above, exit 2 is a finding to report, exit 4 from `ratchet.py` is a
revocation that has **already applied**, and only exit 1 — bad usage — is worth invoking again.
`.warrant/ledger.jsonl` is append-only and grows; query it in Python rather than reading it whole.

## Override 7 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation, or
advanced function calling scenarios"*; 3.7 Flash defaults to `MEDIUM`. Routing is not that — it is a
lookup over eight entries and a read of `.warrant/` — so run the default. **[measured-family]** Do not
raise it as a remedy for anything above: paired across 106 tasks, `high` beat `medium` on 24, lost on
24 and tied on 58, mean −1.7 points (§2.3). **[docs]** *"Higher thinking levels encourage the model to
use more tools to explore and verify, so lowering the level can reduce tool calls."*

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response
format, at the end of the prompt."*

1. Answer a state question from `.warrant/` with the command beside every number; the ladder table
   describes the rules, never the current holdings.
2. Run the seven steps as a chain and confirm each file before the step that reads it —
   `rollup_classes.py` especially, or every class reads as evidence-free.
3. Three subagents, counted in the note, and none of them checking your own output.
4. Resolve all seven claim ids in `claims.json` before quoting a figure, and carry the `C`/`I` prefix
   through; an `I` is reasoning, not a result.
5. Route to one of eight by name with its command, having read that skill first; where nothing fits,
   name the unmet condition instead of the nearest skill.
