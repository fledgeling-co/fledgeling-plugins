# gemini.md — `reckon`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the
section it lands on. `reckon` suits this model well in one respect: almost all of its arithmetic
belongs to `scripts/reckon.py`, and **[measured-family]** the one work bucket where this family
matches opus is the one whose brief already states a number — optimality, 74.7 against 75.0
(`geminify/references/evidence.md` §2.1). It suits it badly in another: what the script hands back is
a document that *looks* like a verification record, and a document with an obvious shape and nothing
compiling it is what one measured run filled in without running anything.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`: **no Gemini run
  of `reckon` has been observed**, at any tier.
- **`[measured-family]` sources:** two single sessions (n=1 each) and a 106-task benchmark at two
  effort levels — `geminify/references/evidence.md`. None watched a model reconcile a ledger.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
  (one session on `gemini-3.7-flash-high`) — flash-tier claims, **not** to be projected onto the Pro
  tier. **[docs]** The default drifts inside the family: *"If thinking_level is not specified, Gemini
  3 will default to high."* against, from the 3.5 Flash release notes, *"The default thinking effort
  is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these overrides stand as
  `[docs]`-grounded discipline and every `[measured-family]` number is open.
- **Unmeasured on this skill:** no Gemini run of `reckon` · no evidence a `gemini.md` fixes anything
  on either source · the categorical-collapse and bound-following rates were measured on UI briefs,
  so their transfer to a ledger of rows is `[derived]` · nothing measures this family clustering
  blockers, ruling on a join edge, or using the ECSS/TTCN-3 standards evidence behind these rules.
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns about:
  *"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
  together fragmented instructions from multiple different places in the prompt."* One pass, then
  work from `SKILL.md`.

## There is no route-out block here

geminify writes one only where the benchmark measured the work, and `reckon` fails both conditions.
**Its work class is one the corpus abstains on:** the bench measures a model *building* an artifact,
so adjudicating a partition and reporting what is not known sit in `completeness` and `verification`,
where `lane_pick.py` returns the policy answer unchanged. **And none of the four measured shapes is a
thing it produces:** `static-page` and `visual-design` (it renders nothing), `brownfield-integration`
(it writes a fresh `docs/reckoning/<date>/`, and a grep may only demote or route),
`regression-sensitive` (no contract a test passes today; the ratchet is a script). **[docs]** *"Avoid
using prompts that ask the model to perform a task for which it has a known, fundamental
limitation."*

## What transfers intact

**The partition is the anti-collapse mechanism, and it is code.** `reckon.py` places every entity and
exits 1 when an id appears twice or a status produces an illegal class, so the one bound the scan
found — `exactly one` class per entity, six times across the skill and its references — is already
read back off the produced artifact rather than restated in prose, which is what `bounded-constraint`
exists to ask for. That module did not fire and is not written below. **The denominators are
generated, not narrated:** five axes with `n`, `of` and `pct` plus a floor note, and `check` exits 2
on a headline the rows do not support — so `Asked to be selective about what counts as remaining, a
capable model will under-report` is already mechanised against **[measured-family]** §1.1.1.

**The delegation cap is a closed rule with a number** (`Delegate in one case only`, one subagent, the
join alone, past ~150 briefs), so `delegation` is not written. Neither is `visual` (zero triggers),
`states`, `platform-values`, `injection` (its inputs are the repo's own briefs and registry, and code
evidence `may only demote or route, never promote`) or `emphasis` — **0** shouted tokens.

## Override 1 — the adjudication pass has a denominator, and the ledger prints it (`### 3 · Adjudicate what the script could not`)

Step 3 is where the script stops and the categorical scopes begin: `Read the overlap edges, confirm
or cut them`, read the `unjoined` rows, `Merge them, and split any it over-grouped` — three sets with
knowable sizes, none of them stated. **[measured-family]** One run delivered **12 of 12** requirements
a brief *enumerated* and satisfied every requirement named *categorically* with one instance or none:
all surfaces → 5, all states → **1**, all menus → **0**, all flows → **0** (§1.1.1, n=1), while the
skill it followed stated six states and an explicit completeness condition in prose. **[docs]**
*"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition."*

`ledger.json` holds every denominator already. Print them before ruling on anything:

```bash
python3 - docs/reckoning/<date>/ledger.json <<'PY'
import json, sys
d = json.load(open(sys.argv[1]))
n = lambda c: len([r for r in d["rows"] if r["class"] == c])
print("overlap", len([e for e in d["join"]["edges"] if e["method"] == "overlap"]),
      "· unjoined", n("unjoined"), "· retirable", n("retirable"),
      "· blockers", len(d["blockers"]), "· unclassified", len(d["unclassified"]))
PY
```

Fill this and report the fraction; every number in your copy comes from that command, not this file:

| scope, in reckon's own words | denominator | ruled on | reported |
|---|---|---|---|
| overlap edges confirmed or cut | 11 | 11 | `11 of 11, 3 cut` |
| `unjoined` rows ruled on | 13 | 13 | `13 of 13, 2 were missed joins` |
| blocker clusters merged or split | 6 | 6 | `6 of 6, 2 merged onto one credential` |
| `retirable` rows read | 4 | 4 | `4 of 4, 1 routed to spec-validation` |
| unclassified inputs given a rule | 2 | 1 | `1 of 2, 1 n/a: the word is upstream's` |

A cell you cannot fill reads `n/a: <reason>` — **[docs]** *"provide instructions for handling missing
data rather than assuming inserted data will always be present and well-formed."* An edge nobody read
is unreviewed, never confirmed.

## Override 2 — `reckoning.md` is the genre that got fabricated (`## What the report has to say`)

**[measured-family]** §1.1.2 (n=1): a run wrote its own review document as five well-formed rows, all
`PASS`, asserting a browser engine as verified when it had failed all four invocation attempts,
`100% pass rate on contrast` from a probe never executed — measured afterwards, every primary button
3.65:1 and one glyph 1.00:1, invisible — and `Interactive Targets Audited: 47`, a number nothing
produced. Forty cells' worth of work, five rows. That document and `reckoning.md` are one genre.

So **no figure is typed into the report by hand**. `build` writes `reckoning.md`; what you add is the
read at the end, every number in it copied from `ledger.json` or the gate's stdout with its command
named. **[docs]** *"Include specific verification steps in either the system instructions or your
prompts directly."* and *"Verify your claims by quoting the exact applicable information (including
policies) when referring to them."* The delivery note ships filled, as the shape:

```
build    reckon.py build --briefs docs/features-to-triage --campaign docs/test-campaign/2026-08-21
         → scrim · 152 rows · 83 piece(s) of work remain … 25/58 (43%) of designed cases
check    reckon.py check docs/reckoning/2026-08-23/ledger.json      → exit 0
ratchet  reckon.py ratchet <prev>/ledger.json <new>/ledger.json     → exit 0
control  scripts/selftest.py                                        → exit 0
inputs   campaign_dir docs/test-campaign/2026-08-21 · campaign_present true · join 55.2%
```

A run that cannot show `check`'s exit code is holding an ungated ledger, and says so in the first
line rather than the last.

And **count from `ledger.json`, because the report is truncated by design.** `count-contract` fired,
and the extension is specific: `render()` prints at most **40** rows per class, **25** waivers and
**10** blockers, each list closing `…and N more in ledger.json`. A read written from `reckoning.md`
alone reports a quietly smaller population — the skill's founding failure, through its own report. **[docs]** *"When model outputs must be machine-readable or
follow a specific format, use a widely recognized standard like JSON, XML, Markdown or YAML that can
be parsed by common libraries."* — that surface is `ledger.json`, and **[docs]** *"Gemini's code
execution tool enables the model to generate and run Python code, and should be enabled whenever the
model needs to perform any kind of arithmetic, counting, or calculation."*, so count in Python over
it, not by eye over a table. `summary.rows` is every entity, `summary.work_items` what somebody
schedules.

## Override 3 — prove the gate can fail, then check the receipt (`### 4 · Re-gate and report`)

**[measured-family]** §1.2.2: an auditor validated tags, citations and contrast floors thoroughly,
had no check that its prerequisite artifacts existed, and returned exit 0 over two skipped skill
invocations. **[derived]** geminify's own quote gate went green across every file after a change took
its checked count to zero, caught only by re-running the negative control (§5). `reckon` ships that
control already:

```bash
python3 scripts/selftest.py   # ends: all gates demonstrated failing on a bad fixture
```

Run it whenever the ledger looks clean and the answer looks tidy, then read the receipt before the
verdict: `check` gates the ledger's internal integrity and cannot tell you which campaign built it.
Read `campaign_present`, `campaign_dir` and `denominators.scope` back off the ledger —
`references/no-campaign.md` is explicit that an empty `unmeasured` column there means the opposite of
what it means in a full run. Same for `join.weak`: a withheld retirement claim is a degraded answer
printed as a warning at exit 0, and it belongs in the read.

## Override 4 — two attempts, and four exits that must not be retried (`### 1 · Find the inputs`, `### 4`)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* **[measured-family]** Both n=1 sessions ran the loop: four consecutive invocations of
one banned, absent tool with nothing changed between them (§1.1.2), and four consecutive `Read` calls
against a 25,000-token ceiling before pivoting to a Python split (§1.2.3). `gemini-cli` ships a loop
detector whose halt message names *"repetitive tool calls"* (§7.2).

Where that lands here: a campaign registry is machine-written JSON, and `cases.json` for a 58-case
campaign alongside `inventory.json` will pass the read ceiling. **Do not `Read` them at all** —
`reckon.py build` is their reader; when you need a row, query `ledger.json` in Python. Pivot on
attempt 1, not attempt 4. And a nonzero exit is a finding, not a transient: exits 1 and 2 mean `the
numbers in it cannot be trusted`, so fix the ledger rather than re-run for a different verdict; exit
3 is the ratchet — `An item may leave unmeasured only by being measured.`; and **exit 4 is the one
worth reading rather than retrying**, its remedy a rule for the word or a correction to the rows,
because `a longer list of words only moves the edge one word along`.

## Override 5 — one edge ruled on in full, then the rest (`### 3`, `references/joining.md`)

**[docs]** *"We recommend to always include few-shot examples in your prompts"*, and *"you can remove
instructions from your prompt if your examples are clear enough in showing the task at hand"*. Write
the first ruling at full fidelity, in the deliverable, and let the rest match it:

| edge | method | score | brief | target | ruling | why |
|---|---|---|---|---|---|---|
| 1 | overlap | 0.21 | `SCR-0088-menu-bar-key-equivalents` | `REQ-0031` | **cut** | shared vocabulary, different subject: the brief is about key equivalents, the requirement about menu bar rendering |
| 2 | cited | 1.00 | `SCR-0071-capability-backfill` | `DEF-0001` | keep | the brief names the id; class `broken`, rolls into the defect — one job, two rows |

`references/joining.md` puts the false positives between 0.18 and about 0.35, so read that band first
and cut rather than keep when it is close: `An unjoined brief is visibly unresolved and gets read; a
wrong edge is invisible and gets believed.` **[docs]** *"Inhibit your response: only take an action
after all the above reasoning is completed. Once you've taken an action, you cannot take it back."* —
`retirable`'s own rule from the other side, since retiring deletes somebody's stated intent.

## Override 6 — the handovers travel as files, and already do (`## What this does not do`)

The scan flags **0** qualitative skill references here, which is earned: every route in that section
names an artifact instead of a lens — `Hand it this ledger; undecided rows are exactly its input.`
Keep it that way, and name row ids. `[derived]`, from **[measured-family]** §1.2.1, where a run
skipped both skills its brief told it to compose with, its own diagnosis being that nothing
downstream depended on a file those skills produce. **[docs]** *"make each step a prompt and chain
the prompts together in a sequence."*

```
1. reckon.py build           → docs/reckoning/<date>/ledger.json + reckoning.md
2. adjudicate (Override 1)   → the same ledger, edges confirmed or cut, clusters regrouped
3. reckon.py check           → an exit code, pasted into the delivery note
4. spec-validation, whats-left ← the ids of the `undecided` rows from step 3's ledger
```

Writing briefs back stays opt-in and stamped — `generated-by: reckon`, `reckon-sources`, `Name an
evidence-work brief for the capability it buys … not for the cases it unblocks.` An unstamped brief
inflates the next run's denominator, which is this skill measuring its own output.

## Override 7 — unavailable is a value, and it is this skill's thesis (`## The partition`)

`authorship` fired, and Google's grounded instruction closes on the sentence `reckon` was built
around. **[docs]** *"Treat the provided context as the absolute limit of truth; any facts or details
that are not directly mentioned in the context must be considered completely untruthful and
completely unsupported. If the exact answer is not explicitly written in the context, you must state
that the information is not available."* Adopt it verbatim for the read you write: the briefs and the
registry are the context, `unmeasured` is what that last clause looks like as a class, and a ratio
you computed off the ledger is your claim rather than the campaign's. **[docs]** *"Do not assume or
infer from the provided facts; simply report them exactly as they appear."* — a repair nobody wrote
down is not a repair, which is the legality table's absent-status row.

**[docs]** *"Your knowledge cutoff date is January 2025."* The standards behind these rules — the
ECSS close-out model, TTCN-3's `inconc` verdict, the coverage and flaky-test figures — are read out
of `references/evidence.md`, never recalled, their numbers least of all. The same covers a file or
skill named in a prompt: **[measured-family]** §1.2.4 recorded both halves failing in one session —
answering from memory when three skills were named, then launching a skill when an answer was
wanted. Read, then answer, as two ordered steps.

## Override 8 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation, or
advanced function calling scenarios"*; 3.7 Flash defaults to `MEDIUM`. Most of `reckon` is not that —
the planning belongs to `reckon.py` and what is left is a read over rows — so run the default and
spend the budget on ledger queries. **[measured-family]** Do not raise it as a remedy for anything
above: paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean −1.7
points (§2.3), while the bound-shaped share of failures *rose* from 58% to 86% (§2.2). **[docs]**
*"Higher thinking levels encourage the model to use more tools to explore and verify, so lowering the
level can reduce tool calls."* — the wrong direction for a skill that re-reads every figure.

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response
format, at the end of the prompt."*

1. Print the five adjudication denominators from `ledger.json` before ruling on anything; report
   `N of N` after, with `n/a: <reason>` on anything unfilled.
2. Type no figure into the report — copy each from `ledger.json` or the gate's stdout, command beside
   it — and count from the ledger, not `reckoning.md`, whose lists stop at 40, 25 and 10.
3. Run `selftest.py` before believing a clean gate; read `campaign_present`, `campaign_dir` and
   `join.weak` before believing the ledger is about the campaign you meant.
4. One retry on a transient error, none on a 25k-token registry file, and none on exits 1, 2, 3 or 4.
5. Rule on one join edge in full before the rest, cut before keep in the 0.18–0.35 band, and let
   `unmeasured` carry everything nobody found out, stated as unavailable rather than filled.
