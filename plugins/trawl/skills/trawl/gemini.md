# gemini.md — running `trawl` on Gemini

`trawl` is unusually well-numbered for a skill written against Claude: the scan
found 2 loose quota rows against 43 distributives that are ordinary prose. Where
a requirement is already a number this family holds up — **[measured-family]**
`geminify/references/evidence.md` §2.1, on tasks stating a complexity bound
`gemini-3.7-flash` scored 74.7 against `claude-opus-5`'s 75.0. So the overrides
are not about the counts: they are about the three places `trawl` keeps state in
conversation rather than a file, the bounds it states as prohibitions, and the
receipt — a line of arithmetic nothing recomputes.

Read this once, then follow `SKILL.md`; each override names the section it lands
on. **[docs]** That single pass is deliberate — **Conflicting internal
references** says to "Avoid writing a prompt with non-linear logic or conditionals
that require the model to piece together fragmented instructions from multiple
different places in the prompt", and a conditional side-file is that shape.

## Epistemic status

`[docs]` is Google's published guidance, quoted verbatim from
`geminify/references/gemini-corpus.md`; `[measured-family]` is Gemini runs of
*other* skills (two sessions, n=1 each, plus a 106-task benchmark); `[derived]`
is reasoning from those. `[measured-here]` appears nowhere — **no Gemini run of
`trawl` exists**, so every rate below was measured on something else.

**The tier these numbers are about.** Every measured claim here is flash-tier:
`gemini-3.7-flash` at both effort levels, plus one `gemini-3.7-flash-high`
session. Nothing measures Pro, whose defaults differ — **[docs]** the Gemini 3
developer guide says "If thinking_level is not specified, Gemini 3 will default
to high", while the 3.5 Flash release notes record that "The default thinking
effort is now medium, changed from high in Gemini 3 Flash Preview." On Pro the
overrides hold as `[docs]`-grounded discipline and every `[measured-family]` rate
is open.

**Unmeasured on this skill:**

- Whether any of this helps. No run has been measured with a `gemini.md` in place
  against the same work without one, on any skill.
- **Gemini judging rather than generating.** Both measured sources watch a model
  *build* an artifact. `trawl`'s Phases 2 and 3 are almost entirely judging —
  floors, clustering, pairwise comparison, the boss gate — and neither speaks to
  that, so those overrides are `[docs]`-grounded, not backed by a rate.
- Override 1's file conversion rests on one session's diagnosed mechanism plus
  Google's chaining guidance (§7.2 names the isolating A/B as still missing), and
  override 7's self-grading concern is `[derived]` from a relayed third-party
  figure in §7.1, measured nowhere in this corpus.

## No route-out block

The benchmark measures a model **building** something, and `trawl` builds nothing
— it reasons, judges and recommends. All four measured shapes are omitted for
that reason: `static-page` and `brownfield-integration` because the skill authors
no page and edits no repo, `visual-design` because it renders no surface,
`regression-sensitive` because it ships no contract that could regress. What
survives is the honest half: the boss gate and the Phase 2 floors are what this
corpus cannot vouch for, so their verdicts are the output most worth re-reading.

## What transfers intact

Most of the skill does, and effort spent re-hardening it is effort not spent
below.

- **Every count already written as a numeral** — 5 seats · 3–8 ideas per branch ·
  3–6 clusters · 3 shortlist slots (2 at any%) · 4–8 sentences per sketch · 3–5
  children · a 2–4 sentence baseline · the per-tier Agent-call table. This is
  §2.1's optimality bucket.
- **The JSON contract in the branch prompt.** **[docs]** the checklist asks for
  exactly this — "use a widely recognized standard like JSON, XML, Markdown or
  YAML that can be parsed by common libraries" — and to "show the output
  structure in your few-shot examples", which it already does.
- **The isolation invariant**: nothing about parallel non-communicating branches
  is model-specific.
- **The receipt exemplar** (`Trawl standard — 5 frames, 27 ideas → 19 after
  merge …`) is a filled example, not a schema. **[docs]** "We recommend to always
  include few-shot examples in your prompts." Same for the pairwise order-swap
  protocol in `references/convergence.md`: position bias is not Gemini-specific.
- **The register.** The scan found 0 emphasis markers, so nothing needs
  de-escalating. **[docs]** "Avoid unnecessary or overly persuasive language."

## The overrides

### 1. Freeze the baseline into a file, not into context

Lands on **Phase 0**, whose own line is `Freeze both verbatim. No Agent call;
you'd produce this anyway.` Add the file: write the baseline and named native
stack to `trawl/baseline.md` before spawning, embed its contents in every branch
prompt, and have the Phase 3 boss gate read it back off disk. Same for the other
state passed conversationally:

| state | file | written by | read by |
|---|---|---|---|
| baseline + native stack | `trawl/baseline.md` | Phase 0 | every branch, boss gate |
| frame ledger (seats, rejects, failed question) | `trawl/frames.json` | Phase 1 pre-spawn | receipt, apoptosis note |
| each branch's ideas | `trawl/branch-<n>.json` | that branch | dedup, clustering, receipt |

`references/convergence.md` already names the failure this prevents: `it must
stay frozen from Phase 0 — a drifting baseline is an unbeatable one`. That is the
target diagnosing the exact risk, and prose freezing is what fails to hold it.
**[measured-family]** §1.2.1 — on a run where a composition step had no concrete
artifact downstream of it, the step was skipped, and the model's own diagnosis
named the missing file dependency as the reason. **[docs]** the chaining remedy
is file-shaped: "make each step a prompt and chain the prompts together in a
sequence", where "the output of one prompt in the sequence becomes the input of
the next prompt." The branch files also make override 4 possible at all.

### 2. The output shape is six cells to fill, not six headings to read

**[docs]** "By default, Gemini 3 models provide direct and efficient answers. If
you need a more conversational or detailed response, you must explicitly request
it in your instructions." That agrees with `trawl`'s anti-ceremony rule — `Chips
and receipts are one line each; everything else earns its length or gets cut`
needs no defending here. The risk runs the other way: a terse default drops the
tail sections, and **[measured-family]** §1.1.1 is that failure in general form,
categorical scopes delivered once or not at all. *Focus* and *Provocation* sit
last, so they are most exposed.

```
sections: 0 receipt ✓ · 1 brief ✓ · 2 wide set ✓ · 3 converge ✓
          4 focus ✓ (3 of 3 shortlist clusters deepened) · 5 provocation ✓
          6 of 6 rendered
```

A section deliberately skipped is `n/a: <reason>`, never absent.

### 3. Every bound gets read back off the produced set

Lands on the **branch prompt** (`at least 3, at most 8`, `no two ideas may share
a mechanism`), **Phase 2 step 5** (`Never let two shortlist slots share a
cluster`), and the hybrid ladder in `references/convergence.md` (`No ladder past
one rung`). **[measured-family]** §2.2 is why this is separate from the counts.
Of Gemini's failing UI assertions, 58% at `medium` and **86%** at `high` were
*bound*-shaped — `exactly N`, `no`, `not`, `only` — against 8% for opus and 6%
for the OpenAI lane. The model delivers what was asked and exceeds what was
capped: a bound is violated by what you did not write, so it survives every check
that looks at what you did.

**[docs]** Google treats these as a component in their own right —
"Restrictions on what the model must adhere to when generating a response,
including what the model can and can't do." — and the **Recap** component is
where they go: a "Concise repeat of the key points of the prompt, especially the
constraints and response format, at the end of the prompt." The ledger is that
recap carrying values, and because Phase 1 now writes JSON the readbacks are real
commands:

| bound | stated | readback | observed | within? |
|---|---|---|---|---|
| ideas per branch | 3–8 | `jq length trawl/branch-2.json` | `9` | **no** — drop the weakest |
| mechanisms unique in branch | no repeats | `jq -r '.[].mechanism' b-2.json \| sort \| uniq -d` | `(empty)` | yes |
| clusters | 3–6 | `jq -r '.[].cluster' trawl/*.json \| sort -u \| wc -l` | `4` | yes |
| one shortlist slot per cluster | no repeats | `sort -u` over the shortlist's cluster labels | `3 of 3` | yes |
| hybrid attempts | ≤ 1 | count of hybrid Agent calls | `1` | yes |

**The prohibition trap, in this skill's own words.** `A frame returning filler to
look productive dilutes scoring attention downstream` is a bound wearing a style
note, and so is `Novelty is never a floor and never rescues a floor failure.`
Convert each into a counted property before Phase 2: filler is `ideas whose
differs_from_baseline restates the mechanism field`; novelty is `floor failures
overturned = 0`.

### 4. The receipt carries its arithmetic, or it carries nothing

The receipt claims six numbers — frames spawned, frames returned, ideas
generated, ideas after merge, ideas floored, frames apoptosed — and nothing in
`trawl` recomputes any of them. **[measured-family]** §1.1.2 — a run of a
different skill wrote itself a five-row review, all `PASS`, asserting a browser
engine that failed on all four invocation attempts and never ran, plus a contrast
pass rate that inverted the measured truth. Not dishonesty: a model completing a
requested *shape* where the shape was specified and the procedure was not.

**[docs]** "Include specific verification steps in either the system instructions
or your prompts directly", and "Verify your claims by quoting the exact
applicable information (including policies) when referring to them." Google names
the tool for the counting too: code execution "should be enabled whenever the
model needs to perform any kind of arithmetic, counting, or calculation."

```bash
ls trawl/branch-*.json | wc -l                   # frames returned → 5
jq -s 'map(length) | add' trawl/branch-*.json    # ideas generated → 27
jq -s 'length' trawl/merged.json                 # after merge     → 19
```

A number with no command behind it is reported as `not counted`, never estimated.
A frame that returned nothing is `spawned 5 / returned 4` with the dead branch
named — `references/convergence.md` already reserves that receipt slot. **This
reverses the house style deliberately:** removing verification scaffolding is
correct for a model that over-verifies; inheriting it here is the defect.

### 5. Load `frames.md` and `convergence.md` before the phase that uses them

Read the file, then run the phase — two ordered steps, neither substituting for
the other. `references/frames.md` before seat selection, because the fit floor is
two named questions with a steelman requirement and a recalled version is a vibe
check. `references/convergence.md` before Phase 2, because each floor needs a
short written justification — what makes it falsifiable, and the first thing lost
to recall. `references/evidence.md` stays optional. **[measured-family]** §1.2.4
— asked a question naming three skills, a run answered from memory without
loading any; asked to fix that, it launched a skill instead. **[docs]** "Your
knowledge cutoff date is January 2025."

### 6. Two attempts per branch, then apoptose the seat

**Phase 1** says nothing about failure. A branch that errors gets one retry; one
returning malformed JSON gets one retry with the schema restated. After that,
record it as a dead branch in the receipt and continue with the survivors — no
third spawn, and no fresh frame substituted mid-run, which would break the
isolation invariant's timing. A permanent error (an absent tool, a capacity
ceiling on a `Read`) pivots on attempt 1. **[docs]** "On *other* errors, you must
change your strategy or arguments, not repeat the same failed call."
**[measured-family]** §1.2.3 — four consecutive `Read` calls against a 25k-token
ceiling with only minor tweaks before the strategy changed.

### 7. Cap the spawn, and never let the generator grade itself

The scan did not fire `delegation` — its triggers are `subagent`, `fan-out`,
`orchestrate`, and `trawl` says `Agent` and `branch`. The skill spawns 8–14
Agents at standard tier, so the module is earned by subject matter and written
here deliberately. **The cap already exists**: the tier table gives frames and
Agent calls per tier, and `100% is reachable only by explicit ask`. Phase 3's
optional hybrid is the run's only discretionary spawn — cap it at one.

**The self-grading exposure has no fix inside a markdown skill, and `trawl` says
so.** `references/convergence.md`: `route pairwise judging to a different family
than the generator — self-enhancement bias is measured and material. Inside the
markdown skill, order-swap + blinding is the practical subset.` Under Gemini that
subset is the whole defence, and its limit is worth stating: the boss gate is one
model judging its own branches, blinded but not independent. Where an
out-of-family lane exists, route the gate to it and say so in the receipt.

**[docs]** the closed-set remedy covers the verdict format, and `trawl` already
uses it — BEATS / TIES / LOSES is the multiple-choice reframing Google prescribes
for a model that answered correctly but "didn't stay within the bounds of the
options", so a verdict never arrives as a sentence. On ordering: "Inhibit your
response: only take an action after all the above reasoning is completed." The
gate runs *after* shortlist selection, never merged into it.

### 8. `thinking_level`

`trawl` is multi-step planning with a judged output, which is what **[docs]**
Google describes `HIGH` as being for: it "Allows the model to use more tokens for
thinking and is suitable for complex prompts requiring deep reasoning, such as
multi-step planning, verified code generation, or advanced function calling
scenarios." `gemini-3.7-flash` defaults to `MEDIUM`.

Two reasons not to read that as a recommendation. **[measured-family]** paired
across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58 — mean
−1.7 points; and the bound-shaped failure rate in override 3 got *worse* at
`high` (86% against 58%). **[docs]** the level also couples to this skill's cost
model: "Higher thinking levels encourage the model to use more tools to explore
and verify, so lowering the level can reduce tool calls." `trawl`'s spend is
Agent calls, so a raised level is a cost decision for the receipt, not a remedy.
