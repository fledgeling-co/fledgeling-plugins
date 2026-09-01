# gemini.md — `defer`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the
section it lands on. `defer` is unusual: nearly all of its answer comes from a script, so the
risk is not a worse routing decision. It is a route written from the tables in `SKILL.md` instead
of from `lane_pick.py`, a lane reported as run when only its flags were set, and a lane call
killed at two minutes and read as an answer of nothing.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`: no Gemini run
  of `defer` has been observed. Sources: two n=1 sessions and a 106-task benchmark corpus at two
  effort levels (`geminify/references/evidence.md`), plus one dispatch-set observation recorded
  in `defer`'s own `references/lanes.md` and named at its use.
- **The tier the evidence is about.** Every measured rate below was observed on
  `gemini-3.7-flash` (one session on `-high`) — flash-tier claims, not to be projected onto Pro,
  where they hold as `[docs]`-grounded discipline and every number is open. **[docs]** Defaults
  drift inside the family: *"If thinking_level is not specified, Gemini 3 will default to high."*
  against, from the 3.5 Flash release notes, *"The default thinking effort is now medium, changed
  from high in Gemini 3 Flash Preview."*
- **Unmeasured on this skill:** no Gemini run of `defer` at any tier · nothing measures Gemini
  choosing a lane, reading a meter, picking an opus effort row, or honouring the 900-second bound
  · §2.2's rate was measured on UI assertions, so its transfer to `sol never runs at max` is
  `[derived]` · the delivery penalty below is dispatch-level, not routing.
- **The self-limitation.** Read this in one pass, before the skill: **[docs]** a conditional side
  file is the shape the checklist warns about, *"Avoid writing a prompt with non-linear logic or
  conditionals that require the model to piece together fragmented instructions from multiple
  different places in the prompt."*

## There is no route-out block here, and that is the finding

geminify writes a hand-this-work-to-another-model block only for skills whose work the
benchmark measured. `defer` gets none: `capability.md` § *Where the gate abstains, and why*
says the bench measures a model building something, so its own deliverable — a routing
decision closest to `referral` — sits outside it, and it produces none of the four named shapes
either. **[docs]** *"Avoid using prompts that ask the model to perform a task for which it has
a known, fundamental limitation."* The honest application: this work is not one of them.

Two self-referential things to hold. `defer` is where every other `gemini.md` gets its route-out
numbers, and the `gemini` row in that matrix grades the model now reading it — do not adjust it
from self-knowledge. Half its `proxy` clamp is **[docs]** *"Although you can modify these
parameters, we strongly recommend keeping them at their default values for Gemini 3.x models."*:
the bench pinned `temperature: 0`, `agy` does not, so the row is a floor, not a reading.

The second is new since this file was written, and sharper. `SKILL.md` now says gemini `carries
a 12-point delivery penalty on top of its bench score`; `lanes.md` measures it: as an autonomous
builder it `failed 8 of 12 dispatches` and one completion report was fabricated — `4,406 bytes
claiming four schedulers created, against a ground truth of nothing created`.
**[measured-family]** Same shape as `evidence.md` §1.1.2, where a run's own review asserted a
browser engine that failed all four invocation attempts and a contrast rate from a probe never
executed. The penalty is not a verdict on the reader — `lanes.md` gives the lifting condition,
`a dispatch set of 12 or more` completing `with no fabricated report and a failure rate under
20%`, and Override 4 is how a run earns it.

## What transfers intact

- **The route is already a command, not a judgement**, with nothing to convert from guidance
  into a phase — the scan found zero qualitative skill references, and both new sections arrive
  already bounded (a number and a median; a closed set of four rows). `## Route` prints
  `lane_pick.py --task <class>` above any prose, and `## Using this from another skill` reads
  `Call lane_pick.py, take the argv it prints, run it, verify it`: the executable form of
  **[docs]** *"make each step a prompt and chain the prompts together in a sequence."*
- **Every number in `capability.md` carries its `n` and its tier**, the grades cap what they
  claim (tier `D` is `a hint. Never a gate.`), the three stages of the choice are one axis per
  pass, and `--json` ships the answer in the form **[docs]** asks for: *"use a widely recognized
  standard like JSON, XML, Markdown or YAML that can be parsed by common libraries."*

## Override 1 — run the script; the tables beside it are not the answer (`## Route`)

`## Route` prints a six-row class table under the command, and the section below it a four-row
effort table. A model that has read both can produce a fluent, plausible, wrong route without
calling `lane_pick.py` — the tables hold no meters, and meters decide.

**[measured-family]** Two n=1 observations converge. Asked a question naming three skills, one
run answered from memory without loading any (`evidence.md` §1.2.4); in the same session two
instructed skill invocations were skipped, and its own diagnosis named the mechanism — the
guidance was in context, and nothing downstream depended on a file only those skills produce
(§1.2.1). Here the policy is in context; the meters are not.

**The rule:** the route is whatever `lane_pick.py` printed, in this session, on this machine —
two ordered steps, neither substituting for the other.

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/defer/scripts/lane_pick.py \
  --task implementation --shape greenfield-module --json > /tmp/route.json
```

`/tmp/route.json` is the artifact every later sentence reads; a note written before it exists is
a recollection. **[docs]** *"Include specific verification steps in either the system
instructions or your prompts directly."* and *"Verify your claims by quoting the exact applicable
information (including policies) when referring to them."*

Three more cases, one new. Prices, allowances and meters are read, never recalled;
`usage-sources.md` carries the dated figures. **[docs]** *"Your knowledge cutoff date is January
2025."* **[measured-family]** one run returned a previous-generation published value confidently
(§1.1.4, n=1): an old fact, not a guess. A file named in the prompt is loaded before answering.
And an opus effort is one of the four rows in `## Opus does not need xhigh for everything` —
`xhigh` only for grading and rendered-UI review, `medium` for `extraction, arithmetic, JSON
assembly, file streaming, censusing` — checked by its tell: `the agent's answer would not change
if it thought less`.

## Override 2 — the rules above the table are bounds, and bounds are the measured failure (`## Route`, `references/lanes.md`)

`SKILL.md` states its hardest invariants as prohibitions in prose: `gpt-5.6-sol never runs at
max`, `Fable judges; it does not verify`, `Design review stays on Opus and Fable`, and now
`gemini is now ranked behind glm, grok and sol on every class it appears in`. `lanes.md` adds
`REVIEWER ≥ WRITER`, `VERIFIER ∉ WRITER's family` and `A refused lane stays refused`.

**[measured-family]** This is the shape the benchmark says gets exceeded rather than forgotten.
Classifying every failing UI assertion by whether it states a bound or asks for a thing: 58% of
Gemini's failures at `medium` and 86% at `high` were bound-shaped, against 8% for opus and 6%
for the OpenAI lane, and `has exactly one soft elevation shadow` failed on every card and toast
in its set on a run that passed 37 of its 39 other assertions (§2.2). A bound is violated by
what you did not write, so it survives every check that looks at what you did.

**[docs]** Google treats these as a component in their own right — *"Restrictions on what the
model must adhere to when generating a response, including what the model can and can't do."* —
and asks that *"all requirements, constraints, options, and preferences are exhaustively
incorporated into your plan."*

**The rule:** each bound becomes a row with the produced value read back off the emitted route,
not a rule restated more firmly. The `observed` column is real output from running these
commands on 2026-09-01.

| bound, in `defer`'s words | countable property | readback | observed | within? |
|---|---|---|---|---|
| `gpt-5.6-sol never runs at max` | routes pairing `gpt-5.6-sol` with effort `max` | `.model` + `.effort` of every `--json` route | 0 of 17 routes emitted | yes |
| `Fable judges; it does not verify` | `claude-fable-5` in a `--task verification` route | `--task verification --json` → `.model` | `claude-opus-5` @ `xhigh` | yes |
| `Design review stays on Opus and Fable` | families in a `design-review` route | same → `.family` | `anthropic` | yes |
| `gemini … ranked behind glm, grok and sol on every class` | routes whose `.lane` is `gemini` | `.lane` over the same 17 | 0 of 17 | yes |
| `VERIFIER ∉ WRITER's family` | `.family` of the critic vs of the writer | compare the two route files by hand | writer `xai` (grok), `completeness` `xai` (grok) | no — reroute |
| `Every command in this file needs a bound of 900 seconds` | the launching Bash call's `timeout`, or `run_in_background` | the tool call's own parameters | n/a: route emitted, no lane launched | n/a |

Report the fraction: `4 of 5 decidable bounds within, 1 breached and rerouted, 1 n/a`. Read the
fifth row twice — `lane_pick.py` takes no writer-family argument, so that invariant is the
caller's to check, and today's meters put writer and critic both on `xai`. A ledger filled from
the brief rather than the route shows six greens. Two of the skill's own counts also fail to
read back: `Three rules hold above the table` introduces five bullets, and `ten lanes` meters
eleven. Take a count from the artifact, never from the sentence introducing it.

## Override 3 — 900 seconds is part of the invocation, and a killed call is not a refusal (`## Give the lane 900 seconds, or background it`)

This section is new, and the one place `defer` asks the reader to bound its own tool call rather
than read a bound off a script. `SKILL.md`: the harness default is `120 000 ms`, the median lane
call is `150 seconds`, and `23 of grok's 24 failures` were that default firing on calls that
were going to succeed.

**The rule:** every lane launch carries `timeout: 900000` or `run_in_background: true`, and the
note records which. Then read the output file rather than the exit status — `Codex prints a
correct-looking header on a run that produced nothing at all`.

The retry ceiling lands here too, because the two are easy to confuse. **[docs]** *"On *other*
errors, you must change your strategy or arguments, not repeat the same failed call."*
**[measured-family]** Both n=1 sessions ran the loop: one invoked a banned, absent tool four times
unchanged; the other hit a 25,000-token `Read` ceiling and retried four times before pivoting to
a Python split (§1.1.2, §1.2.3), and `gemini-cli` ships a loop detector whose halt message names
*"repetitive tool calls"* (§7.2). So an empty output file has two causes taking opposite actions,
and only the second earns a second attempt:

| what you see | which it is | do |
|---|---|---|
| empty `-o`, log tail carries a usage-limit line | capacity, permanent for now | pivot on attempt 1, descend a band |
| empty output, the call ended at ≈120s | the harness bound fired | re-run once with `timeout: 900000` — the lane never answered |

Neither is `agy` appearing to hang: `--print` buffers to exit, so wait for the process.

## Override 4 — a lane is proved by its receipt, and reported only from it (`## Then verify the lane actually ran`, `lanes.md` § DELIVERY_PENALTY)

`SKILL.md` already says the expensive failure returns a plausible answer from the wrong model,
and that `X-Perch-Binding: glm` separates a GLM answer from a Claude answer wearing one. The
fabricated completion report above is the other half of the same rule.

**The rule, first half:** every claim about a lane carries the command that produced it and that
command's output, and the receipt is checked for existence and non-emptiness *before* anything
about its content — a gate reading only final properties passes an upstream step that never ran,
and a denominator of zero is a gate that did not run. `wire-verify.md` is the only source for
each lane's check. **[docs]** *"Inhibit your response: only take an action after all the above
reasoning is completed."*

**Second half:** adopt Google's grounding discipline for anything written *about* the run.
**[docs]** *"In your answers, rely only on the facts that are directly mentioned in that
context."* and its operative last clause: *"If the exact answer is not explicitly written in the
context, you must state that the information is not available."* A figure the lane's output does
not contain is `n/a: <reason>`, never a plausible number — a byte count is not a result, and four
schedulers claimed is not four schedulers created. Let `--report` compute the headroom, and treat
no cross-bench figure as transferable: `only the relative ordering crosses between them`.

The route note ships filled: above the dividing comment is verbatim `lane_pick.py` output from
2026-09-01; the two lines below it stay empty until the lane has run. **[docs]** *"We recommend
to always include few-shot examples in your prompts."*

```
task     implementation — Writing code
shape    greenfield-module — New self-contained module behind one acceptance surface
lane     grok (grok-4.6, xai family, effort xhigh)
why      within 20% on headroom (glm/grok), so the cheapest wins at $0.63 a task — 0.1264/day vs glm 0.1429
measured 62 on this shape against opus's 75 (-12 pts, p=0.74, n=8, tier D, proxy evidence)
band     guarded
equal    glm, grok — within 5 points of each other, so headroom chose
outrank  codex-luna-max, gemini — eligible but measured further behind, so not considered on headroom
refused  codex-sol, codex-sol-high, codex-terra-max, codex-terra-medium — measured too far behind on this shape
guard    state the exported signature and the acceptance condition in the prompt
run      grok -m grok-4.6 --effort xhigh -p {PROMPT}
verify   grok-store (see references/wire-verify.md)
# --- filled only after the lane has run; never pre-filled ---
launch   Bash(timeout: 900000) | run_in_background: true      <- which one
receipt  ~/.grok/sessions/<cwd>/<uuid>/summary.json -> current_model_id; output file non-empty
```

Note the `outrank` line: `gemini` is set aside on the one shape `capability.md` grades level with
opus (75 against 75) — delivery penalty and preference order run after the score, per `lanes.md`
§ *Two facts a bench cannot see*.

## Override 5 — the route note has cells, and the fractions get reported

All four categorical quantifiers the scan surfaced were prose about the evidence rather than a
deliverable scope (`every cell`, `every route`, `any token`, `every token`), so none became a
row. The ledger comes instead from what this skill promises to count: 6 task classes · 11 shapes
· 11 metered lanes across 5 families · 4 verify methods · 5 rules above the class table · 3 stages
of the choice. **[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete,
measurable definition."* **[measured-family]** Why a cell rather than a reminder: one run
delivered 12 of 12 enumerated features and 1 of 6 categorically named states, while the skill it
followed stated the six *and* a completeness condition in prose (§1.1.1, n=1). So the note reports
three fractions off artifacts — lanes considered (`equal` plus `outrank` plus `refused`), bounds
within (Override 2), receipts obtained (`1 of 1`, pasted). A cell that cannot be filled reads
`n/a: <reason>`: `gemini`'s `verify` is `output-nonempty` because `agy` records no model id.

## Override 6 — `thinking_level`, and why it is not the lever here

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation,
or advanced function calling scenarios."* A routing decision — a lookup, one script call, a
receipt check — is not that, and 3.7 Flash's `MEDIUM` default is adequate. **[measured-family]**
Do not raise it as a remedy for anything above: paired across all 106 tasks, `high` beat `medium`
on 24, lost on 24 and tied on 58, mean −1.7 points (§2.3). One `[derived]` caution — **[docs]**
*"Higher thinking levels encourage the model to use more tools to explore and verify, so lowering
the level can reduce tool calls."* Fewer tool calls is the wrong direction: the failure this file
is written against is not calling the tool at all.

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and
response format, at the end of the prompt."*

1. Run `lane_pick.py --json` into a file; answer from it, not the tables beside it, and name the
   opus effort row rather than defaulting to `xhigh`. Read meters from `usage-sources.md`.
2. Fill the bound ledger from the emitted route; report `N of N within`.
3. Launch with `timeout: 900000` or in the background, then read the output file, not the exit
   status. A call that died at 120s is a re-run, not a refusal.
4. Paste the receipt `wire-verify.md` names. No receipt, no claim, no figure the lane's own
   output does not carry. Carry `equal`, `outrank` and `refused`, not only the winner.
