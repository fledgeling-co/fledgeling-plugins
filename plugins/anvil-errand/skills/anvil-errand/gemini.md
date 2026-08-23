# anvil-errand, calibrated for Gemini

Read this once before the first `anvil` call, then run the skill as written with the overrides below. Its
whole job is to run one command, read a stable identifier out of the output, and hand back one next step.
The exposure on this family is not a weak answer; it is a well-formed answer naming a refusal kind nobody
printed, about a machine nobody contacted.

## Epistemic status

| Tier | Used here for |
|---|---|
| `[docs]` | Google's published Gemini guidance, verbatim from `geminify/references/gemini-corpus.md`. The strongest tier, and most of this file rests on it. |
| `[measured-family]` | Two recorded Gemini sessions of *other* skills — `Egress Gemini` (2026-08-17, a UI mock) and `COD Dossier` (2026-08-23, a research-and-authoring pipeline) — plus 106 scored benchmark tasks (`diolog-swe-bench`, read 2026-08-22). **n=1 each for the sessions**; the bench is a rate on a different corpus. Neither session ran an errand. |
| `[measured-here]` | `scan_skill.py` over this SKILL.md, 2026-08-23: 118 lines, **1** quota candidate (dropped as prose), **0** bound rows, 4 prohibitions counted, **0** qualitative skill references, **0** emphasis tokens, one module fired — `gate`, 3 hits. A scan of the text, not a Gemini run. |
| `[derived]` | My reasoning from those, said as such. |

**Which tier the numbers belong to.** Every measured rate here is flash-tier — `gemini-3.7-flash`, plus
one `gemini-3.7-flash-high` session — and nothing measures the Pro tier, whose knowledge floor and
thinking default differ. **[docs]** "If thinking_level is not specified, Gemini 3 will default to high",
then from the 3.5 Flash release notes, "The default thinking effort is now medium, changed from high in
Gemini 3 Flash Preview." On Pro, read every override as `[docs]`-grounded discipline and every
`[measured-family]` number as an open question. Do not project these upward.

**Unmeasured on this skill:** no Gemini run of `anvil-errand` has been observed — not whether the refusal
kind gets read off stderr or invented, not whether `docs/ERRAND_RUNBOOK.md` gets loaded or recalled, not
whether a refused errand gets re-run instead of fixed, not whether the three-minute silence reads as a
hang. And no comparison exists anywhere between a run with a `gemini.md` and one without. **[docs]** A
caution about this file's own shape: "Avoid writing a prompt with non-linear logic or conditionals that
require the model to piece together fragmented instructions from multiple different places in the prompt."
Read it in one pass — every override names where it lands.

## No route-out block, and which shapes were dropped

geminify writes one only where the benchmark corpus measured the target's own kind of work, and that
corpus measures a model **building** an artifact. This skill builds nothing, so all four measured shapes
are omitted — `static-page` and `visual-design` because it renders nothing, `brownfield-integration`
because it edits no repo, `regression-sensitive` because it ships no code a contract can regress against.
**[docs]** The checklist entry it would apply — "Avoid using prompts that ask the model to perform a task for
which it has a known, fundamental limitation." — has nothing here to point at, and abstaining is honest
when the evidence is about a different question.

## What transferred intact

- **The refusal table is already a closed set with a machine identifier per row.** Eight kinds, each a
  token you match rather than a sentence you interpret. **[docs]** "use a widely recognized standard like
  JSON, XML, Markdown or YAML that can be parsed by common libraries" — `denied [<kind>]: <sentence>` is
  that, and branching on the kind while treating the sentence as human-facing is what Google's guidance
  would ask for.
- **`image_unverified` is the best-written row**, because it refuses to guess. **[docs]** Under
  **Underspecified task**: "provide instructions for handling missing data rather than assuming inserted
  data will always be present and well-formed." A kind meaning *could not establish either way*,
  explicitly not the kind meaning *absent*, is that instruction already written into a product.
- **The one timing claim carries a number and a denominator** — around three minutes across twenty-odd
  provider calls — which is why it survives where a relative qualifier would not; and the skill does not
  shout, at `[measured-here]` zero emphasis tokens. **[docs]** "Instead, provide objective constraints",
  and "Avoid unnecessary or overly persuasive language."

## The quota ledger — filled, not described

**[measured-here]** The scan returned one categorical candidate and I dropped it: `SKILL.md:96` — *each
claim* — is about the runbook's evidence, not anything this skill delivers, so the ledger is derived by
hand. **[measured-family]** Why a table rather than the skill's own sentences: on the observed run every
*enumerated* requirement shipped — twelve named features, all present — while every *categorical* one
shipped once or not at all: all states → 1, all menus → 0, all flows → 0. **[derived]** Here the scopes
are small enough that a collapse is invisible: three cells become one sentence, four verbs become `anvil
attach`, and the answer reads complete. **[docs]** "Instead, provide objective constraints".

| Scope, and where the skill states it | Denominator | Filled | Delivery line |
|---|---|---|---|
| a refusal answer = the kind + what is missing + the next step — `Reading a refusal` | **3** cells | 3 | `3/3 — kind read from stderr, cause, next step` |
| the preconditions `--check` covers — the six table rows | **6** kinds | 5 clear, 1 refused | `--check exit 1 · 5 of 6 clear · image_absent` |
| the loop's own verbs — `Watch and stop it with the ordinary verbs` | **4** (`ls`, `attach`, `wait`, `stop`) | 4 named, `attach` marked read-only | `4/4 verbs offered` |
| every next step says where it is written down | **8** kinds, 5 with a numbered runbook step | 5 numbered, 3 `n/a: the sentence carries the cause` | `8/8 resolved — 5 numbered, 3 n/a with reasons` |

The last row decays quietly: `image_unverified`, `egress_unenforceable` and `engine_refused` carry no
runbook number, and the pull is to supply a plausible one rather than write `n/a` — a filled cell, where
an invented step number is a fabrication shaped like an answer.

## The bound ledger — the prohibitions, moved by hand

**[measured-here]** The scan reported `bound rows 0` and counted **4** prohibitions as loose prose;
geminify's instruction is to move by hand the ones attached to a countable property, and here they are the
highest-consequence rules in the skill, because every one is about someone else's machine.
**[measured-family]** This is the failure direction the benchmark corpus measured, pointing opposite to
the ledger above. Classifying every failing UI assertion by whether it states a bound or asks for a thing:
Gemini's failures were 58% bound-shaped at `medium` and **86%** at `high`, against **8%** for opus and 6%
for the OpenAI lane. Requirements get delivered; stated maxima get exceeded on every instance, because the
default idiom supplies the value underneath a rule that was read and agreed with — so a bound gets read
back off what was produced. **[docs]** Google's **Recap** component is where they belong: a "Concise
repeat of the key points of the prompt, especially the constraints and response format, at the end of the
prompt", carrying values.

| bound, and where the skill states it | stated limit | readback | observed | within? |
|---|---|---|---|---|
| starts nothing on your behalf — `What this verb deliberately does not do` | **0** provisioning commands | grep this session's shell calls for `anvil-node serve`, a proxy start, an image build, a pairing | 0 | yes |
| `image_unverified` does not trigger a build | **0** builds on an unverified kind | same grep, restricted to the node | 0 | yes |
| attempts per failing command — `Working notes` | **2**; **1** where the error is permanent | count invocations of the same command in the transcript | 1 (`--check`, refused, not repeated) | yes |
| delegation — *Reach for a subagent only if you are searching a large tree* | **0** for a refusal; **1** maximum for a search | count subagent spawns this turn | 0 | yes |
| reply length — *Keep replies short* | state + next step, **≤ 6** prose lines; the pasted block does not count | line count of the prose | 5 | yes |

**[docs]** "Ensure that all requirements, constraints, options, and preferences are exhaustively
incorporated into your plan." The first two rows carry the real consequences: a run that installs an
engine, starts a proxy or builds an image to be helpful has done a human's job on a machine it cannot see.

## Override 1 — read the runbook, then answer (`Where the real recipe lives`)

The skill states the requirement in one line — *Read it rather than reproducing it here* — and the
consequence too: a second copy of a recipe drifts, and the version everyone cites ends up the stale one,
which has already happened in that repo with two errand runbooks. **[measured-family]** `evidence.md`
§1.2.4: asked a question naming three skills in the prompt, the run answered from internal memory without
loading any of them, then confirmed it had pattern-matched the prompt as a conversational reasoning
question; asked how to fix it, it inverted the error and launched a skill instead of answering. There is
no stable mapping from *a file named in the instruction* to *load it, then answer*. **[measured-family]**
§1.2.1 names why the wording does not force the read: on that run a requirement phrased as a standard
rather than a step was satisfied by producing compliant-looking output directly, because nothing
downstream mechanically depended on a file only that step produces. *Read it rather than reproducing it
here* has that shape — no part of the answer depends on the runbook having been opened.

**[derived]** So make the read produce something the answer consumes, as two ordered phases:

```
Phase 1  Read docs/ERRAND_RUNBOOK.md in the anvil repo. Output: the step number,
         its heading, and the command line it prescribes, quoted.
Phase 2  Write the answer. The "next step" cell is filled from Phase 1's quoted
         line and nothing else. No Phase 1 output → that cell reads
         `runbook not read — step unverified`, never a step number.
```

**[docs]** "Chain prompts: For complex tasks that involve multiple sequential steps, make each step a
prompt and chain the prompts together in a sequence", where "the output of one prompt in the sequence
becomes the input of the next prompt". Neither step substitutes for the other: reading the runbook is not
an answer, and an answer written without it is a recollection. And **[docs]** "Your knowledge cutoff date
is January 2025." **[derived]** The runbook is private rather than training data, so what bites is that
reflex applied to a file read forty turns ago and since scrolled out — a remembered step number is recall,
not a source.

## Override 2 — `--check` is a gate, so its output gets pasted (`The loop`)

**[docs]** "Include specific verification steps in either the system instructions or your prompts
directly", and from the agentic template, "Verify your claims by quoting the exact applicable
information". **[derived]** Skills here are written for a model that over-verifies, so verification
scaffolding is deliberately stripped; inheriting that removal is the defect, because `anvil errand
--check` tells you nothing unless something ran it and its output survived into the reply.
**[measured-family]** What fills that vacuum is well-formed and false: on `Egress Gemini` the run's own
review asserted five `PASS` rows, including an engine verified through a harness invoked four times and
failed every time, and a `100% pass rate on contrast` line from a probe never executed — measured
afterwards at 3.65:1 on every primary button. On `COD Dossier` a deterministic auditor exited 0 while two
prerequisite steps had been skipped, because it checked the final artifact and never whether the upstream
ones ran. That is the likeliest way this skill fails here: a reply naming a refusal kind nobody printed.

- **A kind you did not see in stderr is not a kind.** Paste the line.
- **Report the exit code and which preconditions cleared**, not `check passed`. The skill already
  separates the two claims: the pieces being present is not the workload working.
- **A denominator of zero is a gate that never ran, never a pass.** If `anvil` is not on PATH, the
  honest line names its absence — `--check` did not fail, it did not run.
- **Prerequisite receipts belong in the same block.** A next step with neither the runbook read nor the
  preflight behind it is ungated, and the delivery says so.

```
PREFLIGHT — anvil errand --check   exit 1
  denied [image_absent]: node "anvil-pc" answered; agent image not in its store
  cleared 5 of 6 — errand_no_node, node_unreachable, errand_ticket_unavailable,
                   errand_proxy_unreachable, egress posture
  nothing started: no container created, no idempotency key spent
  runbook: ERRAND_RUNBOOK.md step 1, read this session
```

## Override 3 — the retry ceiling, and where re-running stops being free

**[docs]** "On *other* errors, you must change your strategy or arguments, not repeat the same failed
call." **[measured-family]** Two sessions, one shape: four consecutive invocations of a banned, absent
tool with nothing changed between them, and four consecutive `Read` calls against a hard 25k ceiling
before pivoting to a Python split. `[derived]`, from `evidence.md` §7.2: `gemini-cli` ships a loop detector whose halt message
names `repetitive tool calls`, so the class is recognised elsewhere too.

- **Two attempts per command, then change approach**, and one where the error is permanent — `command
  not found: anvil`, a `--help` that errors.
- **A refusal is not an error to retry; it is the answer.** Pivot on attempt 1. `node_unreachable` does
  not clear by re-running `anvil errand`; it clears by waking the machine or checking `anvil-node serve`
  is running there.
- **`anvil attach` printing nothing is not a hang.** Default `-p` text mode prints nothing until it
  terminates, around three minutes. Wait with `anvil wait <job-id>`, or ask for `--output-format
  stream-json --verbose` next run. Detaching and reattaching four times measures nothing.

**[derived]** And the part the skill states in one direction only: *no idempotency key is spent* is scoped
to a **precondition** failure. Once the errand has started, a re-run may leave a second container on
another machine — so the safe re-run is the one after a `denied [...]` line, every other is a new action,
and `anvil ls` gets read first. **[docs]** "Inhibit your response: only take an action after all the above
reasoning is completed. Once you've taken an action, you cannot take it back."

## Override 4 — brevity trims the preamble, never the pasted output (`Working notes`)

The skill closes with *Keep replies short — the state and the next step*, and **[docs]** the family
agrees: "By default, Gemini 3 models provide direct and efficient answers." **[derived]** So the risk is
not a long reply but a short one that drops the evidence with the preamble — Override 2 failing by a
second route. The bound is in the ledger: six prose lines, and the pasted block is not prose. **[docs]**
On staying inside an offered set: "The response is correct, but the model didn't stay within the bounds of
the options", for which "you can rephrase the instructions as a multiple choice question and ask the model
to choose an option." The eight kinds are that set — answer with the token, then its row; anything outside
them means re-read the raw line, not name a ninth. And **[docs]** "For exploratory tasks (like searches),
missing *optional* parameters is a LOW risk." **[derived]** — so run `--check`, which starts nothing,
rather than asking whether the node is awake.

## One worked example, before the set

**[docs]** "We recommend to always include few-shot examples in your prompts", and "you can remove
instructions from your prompt if your examples are clear enough in showing the task at hand":

```
denied [image_absent] — the node answered and has not got the agent image.

Build it on anvil-pc itself, in the store that node's engine reads
(ERRAND_RUNBOOK.md step 1, read this session). Nothing started here: no
container, no idempotency key spent, so the re-run after the build is a
clean first attempt rather than a retry.

PREFLIGHT  anvil errand --check  exit 1  ·  5 of 6 preconditions clear
```

**[docs]** "Make sure that the structure and formatting of few-shot examples are the same to avoid
responses with undesired formats." Every later answer carries the same three parts in the same order —
kind, cause, next step with where it is written down — over the same preflight line.

## `thinking_level` — and the direction that actually matters here

**[docs]** `HIGH` is "suitable for complex prompts requiring deep reasoning, such as multi-step planning,
verified code generation, or advanced function calling scenarios", and Gemini 3.7 Flash defaults to
`MEDIUM`. **[derived]** This skill is none of those — a preflight, a token match against a table of eight,
one next step — so `MEDIUM` is right. **[measured-family]** Raising it is no remedy for anything above:
paired across 106 benchmark tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean −1.7
points. **[docs]** The direction that matters is downward: "Higher thinking levels encourage the model to
use more tools to explore and verify, so lowering the level can reduce tool calls." **[derived]** This
skill's entire verification is two tool calls — the runbook read and `--check` — and below `MEDIUM` those
go first. Lower the level and the preflight stays.

## Modules deliberately not written

**[measured-here]** The scan fired one module, `gate` (3 hits), and it is Override 2. Nine did not, which
on a skill that renders nothing, spawns nothing and ingests nothing is the scanner working.

- **`bounded-constraint`** — 0 bound rows, 4 prohibitions counted as prose. Moved into the bound ledger
  by hand per the scan's own instruction; the readback columns are that module's rule.
- **`visual`**, **`states`**, **`platform-values`**, **`count-contract`** — nothing rendered, no state
  matrix, no vendor design values to read rather than recall, and the six preconditions are bound as a
  quota row rather than given a section.
- **`authorship`** — the output is a status line for the operator who ran the command, not content a
  distant reader acts on; the grounding rule that matters is Override 1's.
- **`delegation`**, **`injection`**, **`emphasis`** — the spawn cap is already a bound-ledger row; the
  errand's stdout is your own agent's output, read for a refusal kind rather than followed; and there are
  zero emphasis tokens to defuse.
