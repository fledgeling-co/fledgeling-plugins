# gemini.md — `reckon`

Read this once, then read `SKILL.md` and follow it with the overrides below; each names the section it lands on.
`reckon` suits this model in one respect: almost all of its arithmetic belongs to `scripts/reckon.py`, and
**[measured-family]** the one work bucket where this family matches opus is the one whose brief already states a
number — optimality, 74.7 against 75.0 (§2.1). It suits it badly in two: what the script hands back is a document that
*looks* like a verification record, which is what one measured run filled in without running anything, and that
document now carries a schedule made of bounds — `always a range and never a number`, `never a schedule implying a
speedup better than the 4.0x ever observed` — the shape this family exceeds while delivering everything else asked
for.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`: **no Gemini run of `reckon` has
  been observed**, at any tier. The `[measured-family]` sources, cited by § below, are two single sessions (n=1 each)
  and a 106-task benchmark at two effort levels — `geminify/references/evidence.md`. None watched a model reconcile a
  ledger.
- **The tier the evidence is about.** Every rate below was observed on `gemini-3.7-flash` (one session on
  `gemini-3.7-flash-high`) — flash-tier claims, **not** to be projected onto Pro, where the default itself drifts.
  **[docs]** *"If thinking_level is not specified, Gemini 3 will default to high."* against, from the 3.5 Flash
  release notes, *"The default thinking effort is now medium, changed from high in Gemini 3 Flash Preview."* On Pro
  every `[measured-family]` number below is open.
- **Unmeasured on this skill:** no Gemini run of `reckon` · no evidence a `gemini.md` fixes anything on either source
  · the categorical-collapse and bound-following rates were measured on UI briefs, so their transfer to a ledger of
  rows and a wave schedule is `[derived]` · nothing measures this family clustering blockers, ruling on a join edge,
  narrating a duration range, or using the ECSS/TTCN-3 standards evidence behind these rules.
- **No route-out block, and why.** The bench measures a model *building* an artifact, so adjudicating a partition sits
  in `completeness` and `verification`, where `lane_pick.py` returns the policy answer unchanged — and no measured
  shape is one this skill produces: `reckoning.html` is emitted by `render_html` from `ledger.json`, which is also why
  `visual` did not fire on a skill shipping an HTML board, and the ratchet is a script rather than a contract a test
  holds. **[docs]** *"Avoid using prompts that ask the model to perform a task for which it has a known, fundamental
  limitation."*
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns about: *"Avoid writing
  a prompt with non-linear logic or conditionals that require the model to piece together fragmented instructions from
  multiple different places in the prompt."* One pass, then `SKILL.md`.

## What transfers intact

**The partition is the anti-collapse mechanism, and it is code.** `reckon.py` places every entity and exits 1 when an
id appears twice or a status produces an illegal class, so the bound the scan found six times — `exactly one` class
per entity — is read back off the produced artifact rather than restated in prose. The schedule is conserved the same
way: `gate()` refuses an item in two waves, an item in no wave and on no decision list, and a project total that is
not the sum of its waves. **The denominators are generated, not narrated** — five axes with `n`, `of` and `pct` plus a
floor note, and `check` exits 2 on a headline the rows do not support, so `Asked to be selective about what counts as
remaining, a capable model will under-report` is mechanised. **The delegation cap is closed and numbered**: the main
context, one subagent, the join alone, past roughly 150 briefs.

Not written below: `visual`, `states`, `platform-values`, `injection` and `emphasis` — **0** shouted tokens. Six of
the scan's 15 quota rows are prose and were dropped; the six that remain are mechanised. **The real categorical scopes
are the imperatives in steps 3 and 4, which the regex cannot see** — `Read the overlap edges, confirm or cut them`,
`Merge them, and split any it over-grouped`, `Cut the inferred ones you disagree with`.

## Override 1 — the adjudication passes have a denominator, and the ledger prints it (`### 3`, `### 4`)

**[measured-family]** One run delivered **12 of 12** requirements a brief *enumerated* and satisfied every requirement
named *categorically* with one instance or none: all surfaces → 5, all states → **1**, all menus → **0**, all flows →
**0** (§1.1.1, n=1), while the skill it followed stated six states and an explicit completeness condition in prose.
**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition."*
`ledger.json` holds every denominator already:

```bash
python3 - <out>/ledger.json <<'PY'
import json, sys
d = json.load(open(sys.argv[1])); s = d.get("schedule") or {}; R = d["rows"]
c = lambda k: sum(1 for r in R if r["class"] == k)
m = lambda xs, k: sum(1 for x in xs if x["method"] == k)
print("overlap", m(d["join"]["edges"], "overlap"), "unjoined", c("unjoined"), "retirable", c("retirable"),
      "blockers", len(d["blockers"]), "unclassified", len(d["unclassified"]),
      "inferred", m(s.get("edges", []), "inferred"), "tiers", sum(1 for r in R if r.get("estimate")))
PY
```

Fill this and report the fraction; every number in your copy comes from that command, not this file:

| scope, in reckon's own words | denominator | ruled on | reported |
|---|---|---|---|
| overlap edges confirmed or cut | 11 | 11 | `11 of 11, 3 cut` |
| `unjoined` rows ruled on | 13 | 13 | `13 of 13, 2 were missed joins` |
| blocker clusters merged or split | 6 | 6 | `6 of 6, 2 merged onto one credential` |
| `retirable` rows read for the scope-narrowing trap | 4 | 4 | `4 of 4, 1 → undecided: outer daemon deferred` |
| `inferred` edges kept or cut | 9 | 9 | `9 of 9, 2 cut` |
| tiers checked against what you know | 21 | 21 | `21 of 21, 3 retiered, re-gated exit 0` |
| unclassified inputs given a rule | 2 | 1 | `1 of 2, 1 n/a: the word is upstream's` |

A cell you cannot fill reads `n/a: <reason>` — **[docs]** *"provide instructions for handling missing data rather than
assuming inserted data will always be present and well-formed."* The `retirable` row is the pass most easily lost:
`The scope-narrowing trap` asks whether `the brief's full acceptance sketch was satisfied or merely its narrowed
in-tree subset` — a second question per row, not a re-read of the first.

## Override 2 — `reckoning.md` is the genre that got fabricated (`## What the report has to say`)

**[measured-family]** §1.1.2 (n=1): a run wrote its own review document as five well-formed rows, all `PASS`,
asserting a browser engine as verified when it had failed all four invocation attempts, `100% pass rate on contrast`
from a probe never executed — measured afterwards, every primary button was 3.65:1 and one glyph 1.00:1, invisible —
and `Interactive Targets Audited: 47`, produced by nothing.

So **no figure is typed into the report by hand**. `build` writes all three artifacts; what you add is the read at the
end, every number copied from `ledger.json` or the gate's stdout with its command beside it. **[docs]** *"Include
specific verification steps in either the system instructions or your prompts directly."* and *"Verify your claims by
quoting the exact applicable information (including policies) when referring to them."* The delivery note ships
filled, as the shape:

```
build    reckon.py build --briefs docs/features-to-triage --campaign docs/test-campaign/2026-08-21
         → scrim · 152 rows · 83 piece(s) of work remain … 25/58 (43%) of designed cases
         → wrote ledger.json, reckoning.md, reckoning.html in docs/reckoning/2026-09-01
check    reckon.py check <out>/ledger.json  → 152 rows · … · gate: clean, exit 0
ratchet  reckon.py ratchet <prev> <new>     → ratchet: clean, exit 0 · selftest.py → exit 0
inputs   campaign_dir docs/test-campaign/2026-08-21 · campaign_present true · join 55.2%
schedule 6 waves · max_concurrency 8 · project 41–214 min · speedup 3.6x
```

A run that cannot show `check`'s exit code is holding an ungated ledger, and says so in the first line rather than the
last. And **count from `ledger.json`, because both reports are truncated by design**: `count-contract` fired, and
`render()` prints at most **40** rows per class, **40** edges, **25** waivers, **25** decisions, **25** unmeasured
requirements and **10** blockers, while `render_html` stops at **12**. A read written from `reckoning.md` alone
reports a quietly smaller population — the skill's founding failure, through its own report — so count in Python,
which **[docs]** is what Google says the tool is for: *"should be enabled whenever the model needs to perform any kind
of arithmetic, counting, or calculation."*

## Override 3 — every duration is a bound, and the bounds are in the ledger (`## Waves…`, `### 4`)

`bounded-constraint` fired here for the first time, and the schedule is why. **[measured-family]** §2.2: of this
family's failing UI assertions, **58%** at `medium` and **86%** at `high` stated a bound rather than asking for a
thing, against **8%** for opus and **6%** for the OpenAI lane — and one rule, `has exactly one soft elevation shadow`,
failed on *every instance in its set* on a run that passed 37 of its 39 other assertions. Bounds get exceeded while
everything asked for is delivered. **[docs]** Google treats these as a component in their own right — *"Restrictions
on what the model must adhere to when generating a response, including what the model can and can't do."* So the
ledger below is that component, with values in it, each row naming the `ledger.json` field that supplies its own:

| bound, in reckon's own words | readback | observed | within? |
|---|---|---|---|
| `always a range and never a number` | rows whose `low_min == high_min` | `[]` | yes |
| a speedup no better than the `4.0x ever observed` | `schedule.project.speedup` | `3.6` | yes |
| `Decision work is never scheduled` | rows with an estimate and `kind: decision-work` | `[]` | yes |
| a wave past the ceiling widens its upper bound | `waves[].n > max_concurrency`, `bound_by` | wave 3, `n=11`, `capacity` | yes — note printed |
| `do not narrow a printed range to a point when you talk about it` | your own prose | `41–214 min`, twice, no midpoint | yes |
| a retiered row is re-gated | `check` after editing `ledger.json` | 3 retiered, `gate: clean` exit 0 | yes |

The last two rows matter most, because nothing else reads them. `### 4` invites you to `change its tier in ledger.json
and re-gate`, this tool's one sanctioned edit of its own gated artifact, so an edit made and not re-gated is §1.1.2
wearing the gate's name. And a range collapsed in prose is caught by no exit code at all: `41–214 min` narrated as
*about two hours* violates the bound where the script cannot see. **[docs]** *"Ensure that all requirements,
constraints, options, and preferences are exhaustively incorporated into your plan."*

## Override 4 — prove the gate can fail, read the receipt, do not retry an exit (`### 5`, `### 1`)

**[measured-family]** §1.2.2: an auditor validated tags, citations and contrast floors thoroughly, had no check that
its prerequisite artifacts existed, and returned exit 0 over two skipped skill invocations. **[derived]** geminify's
own quote gate went green across every file after a change took its checked count to zero, caught only by re-running
the negative control (§5). `reckon` ships that control — `python3 scripts/selftest.py`, which demonstrates each gate
failing on a bad fixture. Run it whenever the ledger looks clean, then read the receipt, because `check` gates
internal integrity and cannot say which campaign built it: `campaign_present`, `campaign_dir`, `denominators.scope`,
and `join.weak`, a degraded answer printed as a warning at exit 0. An empty `unmeasured` column means the opposite in
a run with no campaign, and `references/no-campaign.md` is explicit about it.

**The two claims the gate deliberately does not hold.** A requirement now leaves `unmeasured` on `backed_by`, `the ids
of the passing cases citing it`, not on its own evidence word — because one session moved eight requirements to
`observed` with no case having run in between, in the same session that `carried the brief join from 6.2% to 100% by
writing requirement: citations into 81 briefs`, and both `check` and `ratchet` exited 0. That is a document edited to
satisfy the tool: §1.1.2's shape in this skill's own vocabulary. The join is still ungated, so compare the `cited`
edge count against the adjudicated case count before believing a join percentage that moved far in one run — and never
write a citation into a brief mid-reckoning.

**And a nonzero exit is a finding, not a transient.** **[docs]** *"On *other* errors, you must change your strategy or
arguments, not repeat the same failed call."* **[measured-family]** Both n=1 sessions ran the loop — four invocations
of one banned, absent tool with nothing changed between them (§1.1.2), and four `Read` calls against a 25,000-token
ceiling before pivoting to Python (§1.2.3). So do not `Read` `cases.json` or `inventory.json` at all; `reckon.py
build` is their reader. Exits 1 and 2 mean `the numbers in it cannot be trusted`, so fix the ledger rather than re-run
for a different verdict; exit 3 is the ratchet — `An item may leave unmeasured only by being measured.`; **exit 4 is
worth reading rather than retrying**, because `a longer list of words only moves the edge one word along`.

## Override 5 — one edge ruled on in full, then the rest (`### 3`, `references/joining.md`)

**[docs]** *"We recommend to always include few-shot examples in your prompts"*, and *"you can remove instructions
from your prompt if your examples are clear enough in showing the task at hand"*. So write the first ruling at full
fidelity, in the deliverable, and let the rest match it:

| edge | method | score | brief | target | ruling | why |
|---|---|---|---|---|---|---|
| 1 | overlap | 0.21 | `SCR-0088-menu-bar-key-equivalents` | `REQ-0031` | **cut** | shared vocabulary, different subject: the brief is about key equivalents, the requirement about menu bar rendering |
| 2 | cited | 1.00 | `SCR-0071-capability-backfill` | `DEF-0001` | keep | the brief names the id; class `broken`, rolls into the defect — one job, two rows |

`references/joining.md` puts the false positives between 0.18 and about 0.35, so read that band first and cut rather
than keep when it is close: `An unjoined brief is visibly unresolved and gets read; a wrong edge is invisible and gets
believed.` **[docs]** *"Inhibit your response: only take an action after all the above reasoning is completed. Once
you've taken an action, you cannot take it back."* — `retirable`'s own rule from the other side, since retiring
deletes somebody's stated intent.

## Override 6 — the handovers travel as files, and already do (`## What this does not do`)

The scan flags **0** qualitative skill references here, which is earned: every route in that section names an artifact
instead of a lens — `Hand it docs/reckoning/<date>/ledger.json directly`, with the class each downstream skill
consumes spelled out. Keep it that way, and name row ids. `[derived]`, from **[measured-family]** §1.2.1, where a run
skipped both skills its brief named because nothing downstream depended on a file they produce. **[docs]** *"make each
step a prompt and chain the prompts together in a sequence."*

```
1. reckon.py build  → <out>/{ledger.json, reckoning.md, reckoning.html}
2. adjudicate (Overrides 1, 3)  → the same ledger, edges cut and tiers set
3. reckon.py check  → an exit code, pasted into the delivery note
4. spec-validation, whats-left  ← the `undecided` row ids from step 3's ledger
```

`delegation` fired on four hits and needs one line, because the schedule prints a number that reads like permission:
`max_concurrency` is how many agents `ship-fleet` may run over this ledger *later*, not how many subagents this run
may spawn. This run stays in the main context.

## Override 7 — unavailable is a value, and it is this skill's thesis (`## The partition`)

`authorship` fired, and Google's grounded instruction closes on the sentence `reckon` was built around. **[docs]**
*"Treat the provided context as the absolute limit of truth; any facts or details that are not directly mentioned in
the context must be considered completely untruthful and completely unsupported. If the exact answer is not explicitly
written in the context, you must state that the information is not available."* Adopt it verbatim for the read you
write: the briefs and the registry are the context, `unmeasured` is what that last clause looks like as a class, and a
ratio you computed off the ledger is your claim rather than the campaign's. **[docs]** *"Do not assume or infer from
the provided facts; simply report them exactly as they appear."* — an outer capability nobody built is not built
because an in-tree test passed.

**[docs]** *"Your knowledge cutoff date is January 2025."* The ECSS close-out model, TTCN-3's `inconc` verdict and the
1,842-run duration corpus are read out of `references/evidence.md` and `references/estimation.md`, never recalled — as
is any file a prompt names: **[measured-family]** §1.2.4 recorded both halves failing in one session, answering from
memory when three skills were named, then launching a skill when an answer was wanted.

## Override 8 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation, or advanced function
calling scenarios"*; 3.7 Flash defaults to `MEDIUM`. Most of `reckon` is not that — the planning belongs to
`reckon.py`, waves included — so run the default and spend the budget on ledger queries. **[measured-family]** Do not
raise it as a remedy for anything above: paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on
58, mean −1.7 points (§2.3), while the bound-shaped share of failures *rose* from 58% to 86% (§2.2).

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response format, at the
end of the prompt."*

1. Print the seven denominators and the six bounds off `ledger.json` before ruling on anything, report `N of N` after
   with `n/a: <reason>` on anything unfilled, and count the scope-narrowing read of each `retirable` row as its own
   pass.
2. Type no figure into the report: copy each from `ledger.json` or the gate's stdout with the command beside it, and
   count from the ledger, whose rendered lists stop at 40, 25, 12 and 10.
3. No collapsed range, no priced decision row, speedup within 4.0x, no printed range narrowed to a point in your own
   prose, and a re-gate after any tier you edit.
4. Run `selftest.py` before believing a clean gate; read `campaign_present`, `campaign_dir`, `join.weak` and
   `backed_by` before believing the ledger is about the campaign you meant; never write a citation into a brief
   mid-reckoning; one retry on a transient error and none on exits 1, 2, 3 or 4; and rule on one join edge in full
   first, cutting rather than keeping in the 0.18–0.35 band.
