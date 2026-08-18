# EVALS: what was measured, and what was not

Written for someone deciding whether to trust this skill, not for someone who already
believes it. The numbers below are small. They are reported with their limits attached,
because a skill that overstates its evidence is exactly the failure it exists to prevent.

## The brief this was built against

Recorded before the build, so later phases have something to drift against.

| | |
| --- | --- |
| **Trigger** | Someone wants agent-authored text to read better, or is about to write an instruction file another model will execute. |
| **Output** | A drafted or revised piece in one of seven registers, plus two to four lines saying what was routed, cut and linted. |
| **Audience** | Split, and that split is the skill's whole design: five registers are read by a person, two by a model. |
| **Done** | The piece passes the lint's hard checks for its register, carries every fact the task supplied, and invents nothing the task did not. |
| **Never** | Reduce the amount of work done rather than the amount written. Claim a check that did not run. Weaken a rule to make a draft pass. |
| **Checkability** | Mostly objective. Closing flourishes, self-congratulation, preamble openers, unmeasurable qualifiers, uncounted scope, pressure language and misplaced verification scaffolding are all string- or pattern-checkable, which is why the evals below are deterministic rather than judged. |
| **Routes to** | `create-voice-persona` for a human voice built from writing samples; `geminify` for retrofitting a whole existing skill to Gemini; `create-skill` and `improve-skill` for authoring pipelines. This skill writes prose; those build artifacts. |
| **Cost** | No metered API spend at run time. The evals below spent CLI-lane calls on a subscription, no dollar cost. |

**Where the brief came from.** One question reached the user through `AskUserQuestion` (whether
the skill should cover instruction files as well as human-read output; they chose to include
them). One clarification arrived unprompted mid-build ("the intent is for the agent-voice to be
a better voice for content in claude code and other harnesses"), and it superseded a three-lane
referral that had converged on a different reading. That referral is recorded under **Referrals**
below, including the lane that failed and the one whose output was discarded.

---

## What was run

### 1. A no-skill baseline, deterministically scored

Three tasks, two arms each. Arm A is the bare task. Arm B is the same task with
`references/agent-voice.md` plus the matching register file prepended, task last. Both arms
scored by `scripts/agent_voice_lint.py` at the register's own format key, which is a fixed
program rather than a judge.

Generation lane: `agy --model gemini-3.7-flash-high`, run from a directory with no project
instructions. Prompts and outputs are in `evals/runs/`.

| Task | Register | Arm | Hard failures | Advisories | Non-empty lines |
| --- | --- | --- | --- | --- | --- |
| 1 | `reply`, is this retry logic idempotent? | no skill | 0 | 1 | 5 |
| 1 | | **skill** | **0** | **0** | **2** |
| 2 | `skill`, write a SKILL.md section on checking UI states | no skill | **1** | 2 | 52 |
| 2 | | **skill** | **0** | 3 | **23** |
| 3 | `report`, report on this work | no skill | **1** | 3 | 20 |
| 3 | | **skill** | **0** | **0** | **3** |
| **Total** | | no skill | **2** | 6 | 77 |
| | | **skill** | **0** | **3** | **28** |

The two baseline hard failures were the ones the skill's central claims predict: an **uncounted
categorical scope** in the instruction file, and a **preamble opener** on the report ("Here is a
summary of the rate limiting implementation…").

### 2. Shorter, or shorter and worse?

The measured trap this whole skill is built around is that a terseness instruction makes the
agent do less rather than say less. So length alone is not a result. Task 3's log states twelve
discrete facts; a mechanical check for each:

| | Facts kept | Lines | Invented artifacts |
| --- | --- | --- | --- |
| no skill | 12 / 12 | 20 | fabricated `file:///` links, an unrequested "Recommended Next Steps" section, LaTeX (`$N \times 100$`) in a terminal report |
| **skill** | **12 / 12** | **3** | **none** |

Identical coverage at 15% of the length, and three invented artifacts gone. The baseline turned
one observation from the log ("`admin.ts` has no rate limiting; left it") into a recommendation
the log did not make; the skill arm reported it as the fact it was.

**This is one task.** It is enough to show the skill is not trading content for brevity on this
task. It is not enough to show it never does.

### 3. Mechanical verification

`./scripts/check_package.sh` runs all four and exits 0 only when all pass.

| Check | What it covers | Result |
| --- | --- | --- |
| `agent_voice_lint.py --self-test` | 18 fixtures: 9 asserting the lint fires, 4 asserting it stays quiet on clean text, 5 regressions for false positives found during the build | 18 passed |
| `check_examples.sh` | Every `<output>` block in the seven register files, linted at that register's format | 14 clean |
| Shipped files | SKILL.md and the rule files at `skill`; `evidence.md` and the field guide at `doc` | 10 clean |
| `verify_quotes.py` | Every span attributed to `[Anthropic]` or `[Google]`, checked verbatim against the four source documents | 82 verified, 0 unverified |

---

## What the gates caught during the build

Recorded because a gate that never fired is not evidence that it works.

1. **A dropped comma inside a verbatim vendor quote.** The Gemini source reads
   `(e.g., <context>, <task>)`; two files had `(e.g. <context>, <task>)`. `verify_quotes.py`
   found it. A sibling skill in this repository previously shipped three of its own sentences
   attributed to Google, which is why that script exists.
2. **Five citations whose words were the source's but whose sentence boundaries were mine**:
   a bolded heading joined to its bullet body with punctuation I added. Rewritten to quote
   contiguous runs, with elisions marked.
3. **An unmeasurable qualifier in the skill's own worked example** ("it is reasonable to say so
   and ask"). `check_examples.sh` caught it. The example was fixed rather than the rule
   weakened, because a worked example steers generation harder than the rule beside it.
4. **A regex bug that silenced the categorical check.** A greedy two-word capture swallowed the
   conjunction in "capture all screens and record…", read the result as singular, and skipped
   the line. Found by a fixture that should have failed and did not.

Each of 1, 3 and 4 now has a permanent fixture or check.

## Defects the build introduced into the lint, and the trade taken

Four false positives surfaced while running the lint over this package's own prose. All four
were lint bugs rather than prose bugs, and each fix is a deliberate trade worth stating:

- **A rule file quotes the form it bans.** `blank_mentions()` now blanks quoted and italicised
  spans before the phrase bans run, so a mention is not read as a use. The cost: a draft that
  italicises its own closing summary escapes that check.
- **Quotes wrap across lines.** The blanking works on the whole text with newlines preserved, and
  the span cap is 900 characters. Below that, long quotes mispair and the blanking lands in the
  wrong place.
- **A categorical in subject position is not a scope instruction.** "Every finding carries its
  failure scenario" states a property of a class; "review all the error states" asks for an
  enumeration. Only the second hard-fails, gated on a task verb appearing before it. **This buys
  precision with recall and therefore misses real cases**, which show up as warnings rather than
  silence. A hard check that cries wolf gets switched off, and a switched-off check catches
  nothing.
- **"overall" is an adverb as well as a summary opener.** "11.6% more expensive overall" is not a
  closing flourish; "Overall, the change is a net win" is. Now anchored to sentence start.

---

## What was NOT run

Stated plainly. The `create-skill` pipeline's Phase 3 specifies more than this, and the rest did
not happen.

- **No blind multi-family judge panel.** The pipeline calls for anonymised A/B pairs judged by
  heterogeneous families that never see the skill. Not run: this session operates under an
  instruction not to spawn subagents unless asked, and the user asked for a skill rather than a
  benchmark. The deterministic lint comparison above was chosen precisely because it needs no
  judge, but it also cannot see anything the lint does not encode.
- **No subagent-graded structural assertions with quoted evidence.** Same reason.
- **Three tasks, one generation each, one family, no repeats.** There is no variance estimate, no
  significance claim, and no per-register coverage: four of the seven registers
  (`commit`, `review`, `doc`, `brief`) were never generated in either arm. Their rules rest on
  cited guidance and worked examples, not on measurement.
- **No Claude-arm result.** The first attempt generated both arms with
  `claude --model claude-fable-5 --effort high`, and the baseline was contaminated: `claude -p`
  inherits the user's global `CLAUDE.md`, which already contains verbosity rules, and the run
  also read repo files it was not given (its output cites "the fixture in this directory" and
  facts from the operator's browser-tooling notes). That is not a no-skill baseline, so it was
  discarded rather than reported. One contaminated output is kept at
  `evals/runs/contaminated-claude-task1.md` as the evidence for this paragraph. The consequence:
  **the skill has never been measured on the family it is primarily written for.**
- **No corpus of approved output.** A human voice package accretes anchors from pieces its owner
  approved. The fourteen worked examples here are authored and lint-clean, not harvested. Until
  real approved output replaces them, they are synthetic exemplars.

### The three tasks that would settle the open questions

1. **The Claude arm, uncontaminated.** Same three tasks, generated in an isolated settings
   environment or through the API directly, to find out whether the skill adds anything on a
   model whose own guidance it quotes. Plausible outcome: much of the effect is already in
   Anthropic's defaults, and the skill's value concentrates in the agent-read registers.
2. **The four unmeasured registers**, particularly `brief`, where the claim is that an
   underspecified brief is the expensive failure and the register therefore has no brevity rule.
   That claim is untested.
3. **A blind judge on the shorter-and-worse question**, across more than one task. The fact-count
   check above is mechanical and narrow; it cannot see a piece that kept every fact and lost the
   reasoning that made them useful.

---

## Referrals: who decided what, when the user was not asked

Recorded because a skipped checkpoint that leaves no trace reads afterwards as a checkpoint that
passed.

| Fork | Lane | Outcome |
| --- | --- | --- |
| What `agent-voice` is for (three candidate readings, order swapped per lane) | `agy --model gemini-3.7-flash-high` | Answered: reading A, write-for-agents. |
| | `codex exec -m gpt-5.6-sol` at high | **Failed**: "Not inside a trusted directory and --skip-git-repo-check was not specified." No output file. Reported, not retried. |
| | `claude --model claude-fable-5 --effort high` | **Failed**: no output within a 10-minute deadline. |
| | `grok -m grok-4.6 --effort xhigh` | Returned a verdict, but its output narrated a panel it had not run and asserted results for lanes never launched. **Discarded as contaminated**, not counted. |
| | **Resolution** | The user's own mid-build clarification superseded the panel entirely. The panel's converged reading was *not* taken. |
| Register set, register boundaries, length targets, lint thresholds, the precision/recall trade on the categorical check | decided in-session | Craft calls on this author's axis; each traces to a citation in `references/evidence.md` or to a defect the gates found. |
| Whether to buy a Dossier research panel | decided in-session | **Not bought.** The `create-skill` pipeline's own rule is to check for an existing corpus first, and four existed: Google's 201KB verbatim consolidation, `geminify`'s distilled Gemini evidence, `create-voice-persona`'s replication-research layer, and `discipline`'s benchmark. Buying a panel on the same field would have returned the same field at a cost. |
| Icon concept | asked | Put to the user before any generation, per the pipeline's Phase 4 checkpoint. |

**Not decided by anyone but the author, and worth a second look:** the em-dash policy is
`advisory` rather than `forbid`, on the grounds that this voice has no owner's habit to encode
and sibling skills in this repository use em dashes freely (geminify 18, discipline 23, clarify
64). A project that bans them sets `"em_dash": "forbid"` in its config.

## Re-baselining

Calibrated on Claude Opus 5 (`claude-opus-5`) and Gemini 3.7 Flash, August 2026. Anthropic's own
guidance notes that prose style shifts between generations and says to re-evaluate style prompts
against the new baseline. On a model change: run `./scripts/check_package.sh`, then regenerate one
task from `evals/runs/` in both arms. If the gap has closed, the finding is that the model
absorbed the rule, and the rule can come out.
