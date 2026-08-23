# gemini.md — `discipline`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the section it lands on.

`discipline` is a skill about how much a model writes, written against a model that writes too much. Here the resting
state is the opposite — **[docs]** *"By default, Gemini 3 models provide direct and efficient answers. If you need a
more conversational or detailed response, you must explicitly request it in your instructions."* — so the saving
clauses land near where the model already sits, and the two whose job is to *prevent* a saving carry the file.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[measured-here]`, `[derived]`. `[measured-here]` is this skill's own
  scan and gate run, not a Gemini run: **no Gemini run of `discipline` has been observed**, and the block has never
  been injected into a Gemini session.
- **`[measured-family]` sources:** two single sessions (n=1 each) and a 106-task benchmark corpus at two effort
  levels — `geminify/references/evidence.md` §1 and §2, which every §-reference below points into.
- **The target's own numbers are not evidence about this family.** Every `first-party+results-read` row in
  `references/provenance.md` was measured on `claude-opus-5` at `xhigh` — `−7.61 pp`, `−16.3%` output, `+32.6%` cost
  are not readings about Gemini and may not be restated as such.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash` (one session on
  `gemini-3.7-flash-high`) — flash-tier claims, **not** to be projected onto the Pro tier, where these overrides hold
  as documented discipline and every family-measured number is open. **[docs]** The defaults drift inside the family:
  *"If thinking_level is not specified, Gemini 3 will default to high."* against, from the 3.5 Flash release notes,
  *"The default thinking effort is now medium, changed from high in Gemini 3 Flash Preview."*
- **Unmeasured on this skill:** no Gemini run of `discipline` at any tier · no evidence a `gemini.md` fixes anything ·
  nothing measures whether this block changes a Gemini session's spend either way, the gap the target itself books as
  `assumed+none` · §2.2's bound rate was measured on UI assertions, so its transfer here is `[derived]`.
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns about: *"Avoid writing
  a prompt with non-linear logic or conditionals that require the model to piece together fragmented instructions
  from multiple different places in the prompt."* One pass, before the skill; do not come back mid-edit.

## Route out, or don't — and it splits by lane

**The editing lane** — changing the block literal, its pins, the registry — is code work in an existing multi-file
tree under compound acceptance, the bucket the bench is worst on. **[measured-family]** §2.1: brownfield scored 16.1
at `medium` and 19.6 at `high` against opus's 46.4 over 28 tasks, by **hard zero on 79% and 75% of decided rows**.

| shape | what it is here |
|---|---|
| `brownfield-integration` | a literal, its byte pin, its sha256 pin, the retained set, a registry row and a version, all in one commit |
| `regression-sensitive` | `block-check.py` and the per-conversation replay contract, both of which currently hold |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape brownfield-integration
```

Two measured shapes get no row: `static-page`, because `injected-block.md` is a literal and nothing here authors a
page, and `visual-design`, because nothing here is judged for looks. **The answering lane** — why a session cost what
it did, whether a compressed style is worth running — gets no routing: both sources watch a model *build* something,
so the corpus abstains and `lane_pick.py` returns the policy answer unchanged.

**[docs]** *"Avoid using prompts that ask the model to perform a task for which it has a known, fundamental
limitation."* Where no lane is available, the table names what to distrust first: an edit satisfying one acceptance
criterion and silently dropping another.

## What transfers intact

- **The block is already seven declarative statements with escape hatches**, and **[measured-here]** all 7 emphasis
  tokens the scan found are the skill *naming* the register it bans. **[docs]** *"Remove language outside of the core
  task from the prompt that attempts to influence performance using emotional appeals, flattery, or artificial
  pressure"*.
- **`provenance.md` is already the mechanical form:** figures are rows, marks are cells from two closed sets, and a
  mark outside them is refused. **[docs]** *"When model outputs must be machine-readable or follow a specific format,
  use a widely recognized standard like JSON, XML, Markdown or YAML that can be parsed by common libraries."*
- **`unlocated` is Google's grounding clause with a name** — the Giskard pairs are registered as searched-for-and-
  absent rather than restated. **[docs]** *"If the exact answer is not explicitly written in the context, you must
  state that the information is not available."*
- **Placement and sizing carry numbers, not qualifiers** — 881, 1,200, 600, 150–300, 319 bytes of headroom — and
  Google reaches rung 1 from adherence rather than cost. **[docs]** *"Prioritize critical instructions: Place
  essential behavioral constraints, role definitions (persona), and output format requirements in the System
  Instruction or at the very beginning of the user prompt."* Nothing needs converting from guidance into a phase
  either: the scan found zero qualitative skill references.

## The quota ledger — filled, not described

**[measured-here]** The scan returned 8 categorical rows and 7 bound rows over 5 files. I bound **4 distinct scopes**
and dropped **10**: three quota rows that are prose about metrics rather than deliverable scope (`every token metric
rewards it`, an `all tokens` quotation about effort, `every figure read in the article's own results` in a source
cell), and all seven bound rows, magnitudes and BPE prose rather than constraints. The real bounds sit in the
argument as prohibitions — 103 counted, not listed — so Override 2 moves them across by hand:

| Scope, and where the skill states it | Denominator | Filled | Delivery line |
|---|---|---|---|
| **every figure** in SKILL.md carries a composed pair — `SKILL.md:28`, `:339` | 24 registry rows against the figures in the prose | 23 covered, **1 uncovered** | `provenance/coverage: FAIL — 22.0 has no row` |
| **each row's** independence mark is pinned so a change cannot be silent — `SKILL.md:354` | 24 marks | 24 | `provenance/promotion: 24 independence marks match their pins` |
| **every row** naming a living document carries an `observed` date — `evidence.md:141` | every `independent` / `vendor-doc` / `self-report` / `anecdote` row | all dated | `provenance/observed: every living-source row carries a read date` |
| **every figure** in `evidence.md` is marked — `evidence.md:10` | ungated: coverage runs on SKILL.md only | **nothing checks this** | say so rather than implying the gate covers it |

**[measured-family]** Why a table and not the sentence: one run delivered 12 of 12 enumerated features and 1 of 6
categorically named states, while the skill it followed stated the six *and* a completeness condition in prose (§1.1.1).

## Override 1 — clause 6 is the load-bearing clause here (§ *What the block covers*)

Clauses 1, 2, 3 and 5 buy less here than on Opus 5, for the reason quoted at the top of this file. Clause 6 — `This
changes how much you write, never how much you do` — is the one aimed at the failure this family measurably has.
**[measured-family]** Twice over: §1.1.1, every categorically named requirement delivered once or not at all; §2.1,
the self-contained-page bucket at 22.2 against opus's 66.9, by hard zero on 71% of decided rows rather than by
scoring low. §2.4 is that as a number — 44 of 46 tests and 4 of 6 verifier groups passed, score zero.

**[derived]** So, reporting on the block from a Gemini session: shorter output is not evidence it worked, and the
skill names the correct measurement — total session tokens including cache misses, never this-turn output length. A
run reading its own shorter transcript as a saving is the confound the target books against v4.

**[docs]** One further reason not to spend the 319 bytes of headroom here: *"Be concise in your input prompts. Gemini
3 responds best to direct, clear instructions. It may over-analyze verbose or overly complex prompt engineering
techniques used for older models."*

## Override 2 — the bound ledger, read off the gate rather than off the prose

**[measured-family]** This is the shape the benchmark says gets exceeded rather than forgotten. By whether a failing
UI assertion states a bound or asks for a thing: 58% of Gemini's failures at `medium` and **86%** at `high` were
bound-shaped, against 8% for opus and 6% for the OpenAI lane, and one rule failed on every card and every toast in
its set on a run that passed 37 of its 39 others (§2.2). A bound is violated by what you did not write, so it
survives every check of what you did.

**[docs]** Google treats these as a component in their own right — *"Restrictions on what the model must adhere to
when generating a response, including what the model can and can't do."* — and asks for the same completeness in the
plan: *"Ensure that all requirements, constraints, options, and preferences are exhaustively incorporated into your
plan."*

**The rule:** every bound becomes a row whose observed value is read back off the artifact by `block-check.py`, never
restated from `SKILL.md`. Real output from `block-check.py --verbose`, run in `plugins/discipline`, 2026-08-23:

| bound, as the skill states it | readback | observed | within? |
|---|---|---|---|
| ceiling 1,200 bytes | `block/ceiling` | 881 of 1200, 319 headroom | yes |
| v4 is byte-stable | `block/v4` | 881 bytes, digest `a4f1ff0d16fdb4c7` | yes |
| v3 and v1 stay, nothing in the literal varies | `block/retention`, `block/literal` | 3 retained; no clock or id | yes |
| no `MUST` / `CRITICAL` in the register | `block/register` | declarative throughout | yes |
| all five survivors named, clause 6 present | `block/quality-floor`, `block/work-floor` | both | yes |
| no verification ban, no self-audit clause | `block/no-verification-ban`, `block/no-self-audit` | both clean | yes |
| every figure in SKILL.md tiered | `provenance/coverage` | `22.0` at SKILL.md:304 has no row | **no** |

`19 of 20 checks pass, 1 fails.` **[derived]** Run the gate **before** your first edit and keep that receipt: the last
row is already red on a clean tree, and without a baseline you will inherit someone else's failure as yours or read
your own as pre-existing. Not this run's to fix unless the user asks; report it as found.

## Override 3 — the receipt is the claim (§ *Editing the block*)

**[docs]** *"Include specific verification steps in either the system instructions or your prompts directly."* and
*"Verify your claims by quoting the exact applicable information (including policies) when referring to them."*

**[measured-family]** What fills the vacuum is well-formed and false: a run's own review asserted a browser engine as
verified when it had failed all four invocation attempts and never run, plus a 100% contrast pass rate from a probe
never executed — measured afterwards at 3.65:1 on every primary button, 1.00:1 on one glyph (§1.1.2, n=1). Not
dishonesty: a requested *shape* completed where the procedure was not specified.

So paste the exit code and the counts. `19 passed, 1 failed` is a result; *the gate is green* is not, `0 errors` with
no count beside it is a gate that may never have run, and piping the script through `grep` makes `$?` grep's status.

**Prerequisite receipts.** **[measured-family]** On one run a deterministic auditor checked final properties and had
no check that its upstream artifacts existed, so a skipped step passed with exit 0 (§1.2.2). `block-check.py` is
better placed — digest pins and `references/exist` catch a literal edited without its pin — but it cannot see whether
a `results-read` row's source was re-read. Name the URL and date in the edit.

## Override 4 — rung 4 of the placement ladder is a closed choice, written down

**[docs]** Google's remedy for a model that answered correctly but *"didn't stay within the bounds of the options"*
is to reframe as a closed choice. Resolve the rung in writing first: rung 1 proxy `system`-field injection · rung 2
an output style with `keep-coding-instructions: true` · rung 3 `CLAUDE.md` · rung 4 no cached-prefix injection point,
so report it and leave the block uninstalled.

**[derived]** This is the bound most worth converting, because breaking it produces a metric that looks fine. In the
skill's own words, `a block that costs more than it saves is worse than no block` — a placement after the last cache
breakpoint is full price every turn, forever. A rung you did not name is one you improvised.

## Override 5 — figures get read, not recalled (§ *Honesty about the numbers*)

**[docs]** *"Your knowledge cutoff date is January 2025."* For this model, *"users can expect updated information for
some domains while in others they may experience the model's knowledge is limited to January 2025"*. The remedy is
grounding: *"Grounding with Google Search connects the Gemini model to real-time web content, and should be enabled
whenever the model may need to know obscure or recent facts."* And for a pass writing a figure: *"Do not assume or
infer from the provided facts; simply report them exactly as they appear."*

**[measured-family]** The informative failure on the observed run was a previous-generation *published* value
returned confidently — Windows 10's accent colour on a Windows 11 surface (§1.1.4, n=1). That is what `observed`
exists to catch: caveman's README sat at the verified end for a week and one fetch moved it. A figure you cannot tag
is one you invented.

**And read what the prompt names, then answer.** **[measured-family]** Asked a question naming three skills, one run
answered from memory without loading any, then inverted the error when corrected by launching a skill instead of
answering (§1.2.4, n=1). Two ordered steps: if the request names a file or a URL, open it, then answer yourself.

## Override 6 — phases with a file between them, and the delegation cap

**[docs]** *"Chain prompts: For complex tasks that involve multiple sequential steps, make each step a prompt and
chain the prompts together in a sequence."* A block edit is that chain, each step's output the next step's input:

```
1. references/injected-block.md   new literal in the fence; the outgoing one retained BEFORE overwrite
2. scripts/block-check.py         BLOCK_PINS: bytes + sha256 of the new literal, old digest kept
3. references/provenance.md       a row for every figure the edit introduces
4. block-check.py --verbose       the receipt, pasted, with its exit code
5. the commit message             what behaviour you expect to change
```

**[derived]** Step 2 is not tidying: the pins are what make step 4 mean anything, and a literal edited without them
fails the gate rather than passing it. Those steps are also why the cap is **zero subagents for a block edit, at most
one for a sweep re-reading living sources**: six coupled files, and splitting them bumps a version in one place and
pins it in another. `do not delegate verification` is clause 4 of the block, and it binds the run editing it.
**[docs]** On low-risk reads, *"Prefer calling the tool with the available information over asking the user"* — open
`provenance.md` rather than asking which tier a figure carries.

## One worked example, before the set

**[docs]** *"We recommend to always include few-shot examples in your prompts."* and *"Avoid leaving the model to
guess the structure of the output; instead, use a clear, explicit instruction to specify the format and show the
output structure in your few-shot examples."* Filled from the v5 proposal that sits in the tree and emits nothing:

```
BLOCK EDIT — v4 -> v5 (proposal only; nothing emits this)
  rung          1, proxy system-field injection — confirmed present     bytes  1101 of 1200 (v4 881, +220)
  digest        7309fadd20eb969bf5a952d106b6f1554f88faf24fae3941b9c09bcaf282aeaf
  retained      v4, v3, v1        registry  no new figures introduced
  gate          block-check.py --verbose -> exit 1; 19 passed, 1 failed
                provenance/coverage: 22.0 — PRE-EXISTING, baseline captured before this edit
  not measured  v4 against v5 head to head; no version has been compared to another
```

Every later note carries the same keys in the same order, `not measured` included.

## `thinking_level`

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation, or advanced function
calling scenarios"* — which the editing lane is and the answering lane is not; 3.7 Flash defaults to `MEDIUM`.
**[measured-family]** Not a remedy for anything above: paired across 106 tasks, `high` beat `medium` on 24, lost on
24, tied on 58, mean −1.7 points (§2.3).

**[docs]** One caution in the same breath: *"Higher thinking levels encourage the model to use more tools to explore
and verify, so lowering the level can reduce tool calls."* Fewer tool calls is the wrong direction here: the failure
this file guards against is not running the gate at all.

## Modules deliberately not written

The scan fired four — `authorship` (6 hits), `bounded-constraint` (6), `gate` (4), `delegation` (4) — all above. Six
did not: **`visual`** and **`states`** (nothing is rendered, no state matrix), **`platform-values`** (the vendor
values here are prices and multipliers, covered by Override 5), **`injection`** (papers and a competitor's README are
cited sources `provenance.md` keeps as data with a mark and a date), **`count-contract`** (folded into the quota
ledger) and **`emphasis`** (7 tokens, all the skill naming the register it refuses).

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response format, at the
end of the prompt."*

1. Run `block-check.py --verbose` before your first edit and keep the baseline; `provenance/coverage` is already red.
2. Fill the bound ledger from that output, not from `SKILL.md`; report `N of N within`.
3. Paste exit codes and counts — no receipt, no claim — and name the placement rung as one of four before installing.
4. Read living sources and stamp the date; a figure with no registry row does not ship.
5. Clause 6 is the clause this family needs. Shorter output is not evidence the block worked.
