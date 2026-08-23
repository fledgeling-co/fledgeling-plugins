# gemini.md — `defer`

Read this once, now, then read `SKILL.md` and follow it with the overrides below;
each names the section it lands on. `defer` is unusual here: nearly all of its
answer comes from a script and almost none from reasoning. So the risk is not a
worse routing decision — it is a route written **from the table in `SKILL.md`
instead of from `lane_pick.py`**, and a lane reported as run when only its flags
were set.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`:
  **no Gemini run of `defer` has been observed.**
- **Sources:** two single sessions (n=1 each) and one benchmark corpus of 106 tasks
  at two effort levels — `geminify/references/evidence.md`.
- **The tier the evidence is about.** Every measured rate below was observed on
  `gemini-3.7-flash` (one session on `gemini-3.7-flash-high`) — flash-tier claims,
  **not** to be projected onto the Pro tier. **[docs]** The defaults drift inside
  the family: *"If thinking_level is not specified, Gemini 3 will default to
  high."* against, from the 3.5 Flash release notes, *"The default thinking effort
  is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these
  overrides hold as `[docs]`-grounded discipline; every `[measured-family]` number
  is open.
- **Unmeasured on this skill:** no Gemini run of `defer` at any tier, so every
  override is `[docs]` plus a family observation from another skill · no evidence a
  `gemini.md` fixes anything · nothing measures Gemini *choosing a lane* or
  *reading a meter* · the bound-following rate in §2.2 was measured on UI
  assertions, so its transfer to `sol never runs at max` is `[derived]`.
- **The self-limitation.** **[docs]** A conditional side file is the shape the
  checklist warns about: *"Avoid writing a prompt with non-linear logic or
  conditionals that require the model to piece together fragmented instructions
  from multiple different places in the prompt."* Read it in one pass, before the
  skill.

## There is no route-out block here, and that is the finding

geminify writes a hand-this-work-to-another-model block for skills whose work the
benchmark measured. `defer` gets none, for two reasons worth stating rather than
leaving as a gap. **Its work class is one the corpus abstains on** —
`references/capability.md` says under `## Where the gate abstains, and why` that
the bench measures a model building something, so only `implementation` and
`general` are shape-gated while `verification`, `referral`, `completeness` and
`design-review` route on policy alone, and this skill's own deliverable is a
routing decision closest to `referral`. **And none of the four measured shapes is a
thing it produces**: `static-page` (authors no page), `brownfield-integration` (its
only code change is a policy edit `selftest.sh` gates), `visual-design` (judges no
rendered surface) and `regression-sensitive` (its invariants are held by that same
selftest) are all omitted.

**[docs]** *"Avoid using prompts that ask the model to perform a task for which it
has a known, fundamental limitation."* — the honest application is that this work
is not one of them. What follows is how to do it, not whether to.

One thing to hold while doing it: **`defer` is where every other `gemini.md` gets
its route-out numbers**, and the `gemini` row in that matrix grades the model now
reading it. Do not adjust that row from self-knowledge. It regenerates from the
bench and carries a `proxy` clamp, half of which is **[docs]** *"Although you can
modify these parameters, we strongly recommend keeping them at their default values
for Gemini 3.x models."* — the bench pinned `temperature: 0`, the `agy` lane does
not, so the row is a floor rather than a reading.

## What transfers intact

Most of `defer` needs no override at all.

- **The route is already a command, not a judgement.** `## Route` prints
  `lane_pick.py --task <class>` above any prose about routing — the executable form
  of **[docs]** *"make each step a prompt and chain the prompts together in a
  sequence."*
- **Every number in `capability.md` carries its `n` and its evidence tier**, the
  grades cap what they claim (tier `D` is `a hint. Never a gate.`), the three
  stages of the choice are one axis per pass rather than one overloaded sweep, and
  `--json` already ships the answer in the machine-readable form **[docs]** asks
  for: *"use a widely recognized standard like JSON, XML, Markdown or YAML that can
  be parsed by common libraries."*
- **Nothing to convert from guidance into a phase.** The scan found zero
  qualitative skill references: `## Using this from another skill` already reads
  `Call lane_pick.py, take the argv it prints, run it, verify it`.

## Override 1 — run the script; the table beside it is not the answer (`## Route`)

`## Route` prints a six-row class table directly under the command, and a model
that has read it can produce a fluent, plausible, wrong route without ever calling
`lane_pick.py` — the table holds no meters, and the meters decide.

**[measured-family]** Two n=1 observations converge on this shape. Asked a question
naming three skills, one run answered from internal memory without loading any of
them, then inverted the error when corrected by launching a skill instead of
answering (`evidence.md` §1.2.4). In the same session two instructed skill
invocations were skipped, and the run's own diagnosis named the mechanism: the
guidance was already in context, and nothing downstream mechanically depended on a
file only those skills produce (§1.2.1). Here the policy is in context; the meters
are not.

**The rule:** the route is whatever `lane_pick.py` printed, in this session, on
this machine — two ordered steps, neither substituting for the other.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/defer/scripts/lane_pick.py \
  --task implementation --shape greenfield-module --json > /tmp/route.json
```

`/tmp/route.json` is the artifact every later sentence reads; a route note written
before it exists is a recollection. **[docs]** *"Include specific verification
steps in either the system instructions or your prompts directly."* and *"Verify
your claims by quoting the exact applicable information (including policies)."*

Two more cases. **Prices, allowances and meters are read, never recalled** —
`references/usage-sources.md` carries the dated figures. **[docs]** *"Your knowledge
cutoff date is January 2025."* **[measured-family]** one run returned a
previous-generation published value confidently (§1.1.4, n=1): an old fact, not a
guess. And **a file named in the prompt is loaded before the answer is written** —
asked why a lane was chosen with `capability.md` named, open it, then answer.

## Override 2 — the rules above the table are bounds, and bounds are the measured failure (`## Route`, `references/lanes.md`)

`SKILL.md` states its hardest invariants as prohibitions in prose:
`gpt-5.6-sol never runs at max`, `Fable judges; it does not verify`,
`Design review stays on Opus and Fable`. `lanes.md` adds `REVIEWER ≥ WRITER`,
`VERIFIER ∉ WRITER's family` and `A refused lane stays refused`.

**[measured-family]** This is the shape the benchmark says gets exceeded rather
than forgotten. Classifying every failing UI assertion by whether it states a bound
or asks for a thing: 58% of Gemini's failures at `medium` and **86%** at `high`
were bound-shaped, against 8% for opus and 6% for the OpenAI lane, and one rule —
`has exactly one soft elevation shadow` — failed on *every card and every toast in
its set* on a run that passed 37 of its 39 other assertions (§2.2). A bound is
violated by what you did not write, so it survives every check that looks at what
you did.

**[docs]** Google treats these as a component in their own right — *"Restrictions
on what the model must adhere to when generating a response, including what the
model can and can't do."* — and asks that *"all requirements, constraints, options,
and preferences are exhaustively incorporated into your plan."*

**The rule:** each bound becomes a row with the produced value read back off the
emitted route, not a rule restated more firmly. The `observed` column is real
output from running these commands on 2026-08-23.

| bound, in `defer`'s words | countable property | readback | observed | within? |
|---|---|---|---|---|
| `gpt-5.6-sol never runs at max` | routes pairing `-m gpt-5.6-sol` with `model_reasoning_effort="max"` | `.model` + `.effort` of each `--json` route | 0 of 16 routes emitted | yes |
| `Fable judges; it does not verify` | `claude-fable-5` in a `--task verification` route | `lane_pick.py --task verification --json` → `.model` | `claude-opus-5` @ `xhigh` | yes |
| `Design review stays on Opus and Fable` | families in a `design-review` route | same → `.family` | `anthropic` | yes |
| `VERIFIER ∉ WRITER's family` | `.family` of the critic vs of the writer | compare the two route files by hand | writer `zai` (glm), `completeness` `zai` (glm) | **no — reroute** |

Report the fraction: `3 of 4 bounds within, 1 breached and rerouted`. Read the last
row twice — `lane_pick.py` takes no writer-family argument, so that invariant is
the caller's to check, and today's meters put writer and critic both on `zai`. A
ledger filled from the brief rather than the route shows four greens.

## Override 3 — a lane is proved by its receipt, never by its flags (`## Then verify the lane actually ran`)

`SKILL.md` already says the expensive failure returns a plausible answer from the
wrong model, and that `X-Perch-Binding: glm` is the whole mechanism separating a
GLM answer from a Claude answer wearing one.

**[measured-family]** The matching failure is recorded in full (`evidence.md`
§1.1.2, n=1): a run's own review asserted a named browser engine as verified when
that engine had failed all four invocation attempts, plus a 100% contrast pass rate
from a probe never executed — measured afterwards, every primary button was 3.65:1
and one glyph 1.00:1. Not dishonesty: a requested *shape* completed where the shape
was specified and the procedure was not.

**The rule:** every claim about a lane carries the command that produced it and
that command's output. Check the receipt exists and is non-empty **before**
checking anything about its content, because a gate reading only final properties
passes an upstream step that never ran. A denominator of zero is a gate that did
not run, and `references/wire-verify.md` is the only source for which check each
lane takes. **[docs]** *"Inhibit your response: only take an action after all the
above reasoning is completed."* The route note ships filled — everything above the
rule is verbatim `lane_pick.py` output from 2026-08-23, and the lines below show
the shape this lane's receipt takes. **[docs]** *"We recommend to always include
few-shot examples in your prompts."*

```
task     implementation — Writing code
shape    greenfield-module — New self-contained module behind one acceptance surface
lane     glm (glm-5.3, zai family, effort high)
why      most headroom per remaining day (0.0807/day vs grok 0.0559)
measured 62 on this shape against opus's 75 (-12 pts, p=0.75, n=8, tier D, proxy evidence)
band     guarded
equal    grok, glm — within 5 points of each other, so headroom chose
refused  codex-sol-high, codex-terra-max, codex-terra-medium — measured too far behind
guard    state the exported signature and the acceptance condition in the prompt
receipt  tail -1 …/Relay/spend/2026-08.jsonl → model: glm-5.3  bindingId: glm
output   wc -c /tmp/lane.md → non-zero, no error banner
```

## Override 4 — two attempts on a lane, then a different lane (`references/lanes.md` § Substitution)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not
repeat the same failed call."* **[measured-family]** Both n=1 sessions ran the
loop: one invoked a banned, absent tool four consecutive times with nothing changed
between attempts; the other hit a 25,000-token `Read` ceiling and retried four
times with minor tweaks before pivoting to a Python split (`evidence.md` §1.1.2,
§1.2.3). The class is recognised beyond this repo — `gemini-cli` ships a loop
detector whose halt message names *"repetitive tool calls"* (§7.2).

Three `defer` errors look transient and are not; each pivots on attempt 1. **Codex
out of allowance:** the header prints the requested model and effort while the `-o`
file is written empty — a capacity limit, so descend a band. **Perch down:** GLM
fails to connect rather than falling back. **A lane at its cap:** `lane_pick.py`
drops it before the equivalence set is built. One non-error looks like a hang:
`agy --print` buffers to exit, so wait for the process rather than poll its stdout.

## Override 5 — the route note has cells, and the fractions get reported

The scan surfaced four categorical quantifiers and **all four were prose about the
evidence rather than a deliverable scope** (`every cell`, `every route`, `any
token`, `every token` — pointers and pricing notes). None became a ledger row, so
the ledger is built from what this skill promises to count: 6 task classes · 11
shapes · 10 lanes across 5 families · 4 verify methods · 3 rules · 3 stages.
**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete,
measurable definition."*

**[measured-family]** Why this is mechanical rather than a reminder: one run
delivered 12 of 12 enumerated features and 1 of 6 categorically named states, while
the skill it followed stated the six *and* an explicit completeness condition in
prose (`evidence.md` §1.1.1, n=1). So the route note reports three fractions, each
read off an artifact: lanes considered (`equal` plus `refused`, both carried, never
only the winner), bounds within (`N of N`, Override 2), receipts obtained (`1 of
1`, with the pasted line). A cell that cannot be filled reads `n/a: <reason>` —
`gemini`'s `verify` is `output-nonempty` because `agy` records no model id, and
saying so plainly beats a green tick.

## Override 6 — `thinking_level`, and why it is not the lever here

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code
generation, or advanced function calling scenarios."* A routing decision — a
lookup, one script call, a receipt check — is not that, and 3.7 Flash's `MEDIUM`
default is adequate. **[measured-family]** Do not raise it as a remedy for anything
above: paired across all 106 tasks, `high` beat `medium` on 24, lost on 24 and tied
on 58, mean −1.7 points (§2.3). One `[derived]` caution from the same page —
**[docs]** *"Higher thinking levels encourage the model to use more tools to
explore and verify, so lowering the level can reduce tool calls."* Fewer tool calls
is the wrong direction here: the failure this file is written against is not
calling the tool at all.

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the
constraints and response format, at the end of the prompt."*

1. Run `lane_pick.py --json` into a file; answer from it, not the table beside it.
2. Read prices, meters and allowances from `references/usage-sources.md`.
3. Fill the bound ledger from the emitted route; report `N of N within`.
4. Paste the receipt `references/wire-verify.md` names. No receipt, no claim.
5. One retry on a transient error; none on an empty `-o` file, a dead proxy or a
   capped lane. Carry `equal` and `refused` into the note, not only the winner.
