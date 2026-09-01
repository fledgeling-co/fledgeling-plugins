# eli5 on a Gemini runner

Read this once, before `SKILL.md`, then work from `SKILL.md` with the overrides below. Each names the
section it lands on, because a side-file is the shape Google's own checklist warns about — **[docs]**
*"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece together
fragmented instructions from multiple different places in the prompt."*

The canon transfers: `eli5`'s pedagogy — invariant, misconception, structure-mapping table, boundary,
prediction beat — is model-independent and none of it changes here. What does not transfer is the
assumption that a rule stated in prose gets executed, and `eli5` states several of its floors and caps in
prose that no part of the gate reads back.

## Epistemic status

`[docs]` is quoted verbatim from `geminify/references/gemini-corpus.md`. `[measured-family]` is one recorded Gemini
run of a *different* skill (n=1) plus a 106-task benchmark running `gemini-3.7-flash` at `medium` and `high` against
`claude-opus-5`. `[derived]` is reasoning from those onto `eli5`'s rules, and says so. There is no
`[measured-here]`: no transcript of a Gemini run of `eli5` has been read. Every rate below is **flash-tier**; on Pro
the overrides hold as `[docs]`-grounded discipline and every `[measured-family]` number is an open question.

**Unmeasured on this skill** — the distinctive predictions this file makes, all on family or docs backing:

1. that `defines-its-terms` gets satisfied at its warn floor of three `<dfn>` while fifteen terms stay undefined
2. that `visual-scenes` (≥3), `interactive-controls` (≥3) and `interaction-variety` (≥2) land at exactly the floor
3. that the prose budgets get met by compressing claims into aphorisms rather than by cutting them
4. that `surface-reach` gets discharged with a `<!-- surface: … -->` comment instead of a library
5. that the geometry contract gets written into a comment and then not honoured
6. whether supplying a reference image lifts the page — the documented strong path, never measured
7. whether the benchmark's `static-page` numbers hold for an explainer; that bucket's briefs were not `eli5` briefs

The `emphasis` module is absent: the scan found zero shouted passages. `delegation` fired at its minimum and is
folded into override 4, because `SKILL.md` already closes the half that matters: `Build it in this session rather
than delegating`. `authorship` fired mostly on `evidence.md`'s account of its own research panel, so its one clause
that lands is folded into override 7.

## Before you start: route out, or know what to distrust

**[docs]** The health checklist says it outright, under **Task outside of model capabilities**: *"Avoid
using prompts that ask the model to perform a task for which it has a known, fundamental limitation."* Two
of `eli5`'s deliverable shapes sit in buckets the corpus measured well behind, and both are the same file:

| shape | what it is here | `[measured-family]` |
|---|---|---|
| `static-page` | the single self-contained HTML file, authored from a prose topic | 22 against opus's 67, hard zero on 71% of decided rows |
| `visual-design` | the Phase 3 identity pass — palette, type, ground, a look somebody chose | 35 against 63 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

`brownfield-integration` and `regression-sensitive` get no row: `eli5` writes one new file, breaks no existing
contract, and Phases 1 and 2 reason rather than author a page. Where the run builds it anyway, distrust the rendered
artifact, not the pedagogy behind it.

## What transferred intact — most of `eli5` needs nothing from this file

- **Every threshold in the gate** — `prose-budget` 350, `prose-block` 50, `prose-run` 120, `opening-budget` 90,
  `no-template-boilerplate` at 3, `plain-statements` at 4, `names-things` at 4, `visual-scenes` at 3. **[docs]**
  *"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition."* These are objective
  constraints with a script that reads them back, which is why they survive on this family when prose around them
  does not.
- **`python3 scripts/lint_explainer.py <file.html>` with `must exit 0`** — a command with an exit status rather than
  a standard to agree with. **`--self-test`** reports `36 of 36 rules proved able to fail`, the negative control the
  `gate` module otherwise has to ask for, already built.
- **Checksummed vendoring as a build step rather than a claim.** `new_explainer.py --with gsap,scrolltrigger` calls
  `vendor_lib.py`, which fetches each library once from a pinned URL, refuses on `checksum mismatch`, and inlines
  it; the linter's containment family then reads the result off the file. A prohibition the run has to keep
  remembering becomes a script that fails — the shape every override below is reaching for.
- **The four `data-*` markers**, so staging, the boundary and the prediction beat are countable rather than
  asserted; and **the eight forms with their worked assignments**, a closed set with an example per row — **[docs]**
  *"you can rephrase the instructions as a multiple choice question and ask the model to choose an option."*
- **The before-and-after tables under `Who is reading`.** **[docs]** *"We recommend to always include few-shot
  examples in your prompts."* They are the strongest single lever in the file and work as written.

## 1. Give every categorical scope a number before you build

`[measured-family]` One run delivered all twelve enumerated features of its brief and satisfied every categorical
requirement with one instance: `all surfaces` → 5, `all states` → 1, `all menus` → 0, `all flows` → 0. **[docs]**
the checklist's **Too many tasks** entry explains why one pass cannot hold five categorical nouns at once, and its
remedy is *"Break the requests into separate prompts."* The rule most at risk here is `every word specific to this
topic is defined where it first appears, or replaced with a plain one`: `defines-its-terms` fails on zero `<dfn>`
and warns below three, so three definitions and fifteen undefined terms passes.

Write this into `notes.md` before markup, one row per unit, then report the fraction:

| unit | `SKILL.md` says | number for this artifact | read back by |
|---|---|---|---|
| topic-specific terms | `every word … is defined where it first appears` | 14, listed in `notes.md` | count `<dfn>` = 14; `defines-its-terms` only floors at 3 |
| visual scenes | `at least three visual scenes` | 5, one per form beat | `visual-scenes` counts svg + canvas + data-img + video |
| interaction kinds | `at least two distinct kinds` | 3: drag, step, pick | `interaction-variety` |
| depth passes | three, no nesting | 3 `[data-pass]` containers | `disclosure-tiers` |
| wired controls | `Never ship a dead control.` | 9 controls, 9 handlers | `interactive-controls` floors at 3 |
| SVG elements | `place every element against a named line` | 22 rows in the geometry comment | arithmetic in code, override 3 |
| reduced-motion end states | `lands each state statically` | 3, one per pass | no rule — check by hand |
| generated images | `Caption every generated image` | 2 of 2 captioned | no rule — check by hand |

`22 of 22 elements placed, 14 of 14 terms defined, 3 of 3 reduced-motion states landed` is the delivery line. A floor in the gate is not the number; it is the point below which the file is indefensible.

## 2. The bound ledger — and the four bounds nothing reads back

`[measured-family]` Across 106 benchmark tasks, classifying every failing UI assertion by whether it states a bound
(`exactly N`, `no`, `not`, `only`) or asks for a thing: Gemini's failures were 58% bound-shaped at `medium` and 86%
at `high`, against 8% for opus. One rule — `has exactly one soft elevation shadow` — failed on every card and every
toast in its set on a run that passed 37 of its 39 other assertions.

**[docs]** Google treats these as a component in their own right — *"Restrictions on what the model must adhere to
when generating a response, including what the model can and can't do."* — and the **Recap** is where they go: a
*"Concise repeat of the key points of the prompt, especially the constraints and response format, at the end of the
prompt."* This ledger is that recap. `eli5` is unusually well defended, because `lint_explainer.py` reads most of
its caps back off the produced file. Four it does not — fill these from the artifact, never from the brief:

| bound | stated at | limit | readback | observed | within? |
|---|---|---|---|---|---|
| prose on the page | budget table | ≤ 350 | `lint_explainer.py` → `prose-budget` | paste the line | |
| single text block | budget table | ≤ 50 | → `prose-block` | paste the line | |
| generated images | `Three images per artifact at most` | ≤ 3 | `grep -co 'src="data:image' out.html` | **2** | yes |
| live variables in pass 1 | `One live variable in the first pass.` | exactly 1 | count `<input>`/`<button>` inside `[data-pass="1"]` | **1** | yes |
| text contrast | accessibility floor | ≥ 4.5:1 | compute from the `:root` tokens in code | **4.9:1** | yes |
| stroke contrast | accessibility floor | ≥ 3:1 | same, per accent token | **3.4:1** | yes |

**Two prohibitions that read as taste and are counted properties.** The scan found 130 prohibitions in prose across
the skill and its references; these two are countable. `Keep it off anything the reader did not cause` → count
tweens and `requestAnimationFrame` loops with no user event in their call path, target zero, since `raf-lifecycle`
checks cancellation rather than causation. `What stays out is decoration` → per mark, name the variable it encodes.

**[derived]** Watch the compression trap on a terse default — **[docs]** *"By default, Gemini 3 models provide
direct and efficient answers."* `evidence.md` §4.7 records a page that met every budget at 200 words and was
unreadable. `SKILL.md` answers it — `Meet the budget by cutting claims and moving explanation onto the diagram,
never by shortening sentences until they turn into slogans` — and text inside `<dfn>` and `<svg>` is exempt from the
count.

## 3. Verification is asked for here, not assumed

`[measured-family]` The run that satisfied `all states` with one instance also wrote itself a review claiming a
browser engine that failed on all four invocation attempts and never ran, and a `100% pass rate on contrast` from a
probe never executed; measured after, every primary button was 3.65:1 and one glyph 1.00:1, invisible. **[docs]**
*"Include specific verification steps in either the system instructions or your prompts directly."* And *"Verify
your claims by quoting the exact applicable information (including policies) when referring to them."*

`SKILL.md`'s `Reporting back` asks for `the lint result`. Give it the output rather than the verdict:

```
$ python3 scripts/lint_explainer.py out.html; echo "rc=$?"
36 checked · 34 passed · 2 warned · 0 failed
rc=0
```

A denominator of zero is a gate that never ran, never a pass — which is why `SKILL.md` asks for
`--self-test` once on a new machine.

**The step a headless runner cannot perform.** Phase 6 closes with `Then open the file and look at it. The linter
cannot see a warped diagram`, and `evidence.md` §4.6 is the case: two axis labels drew on top of each other while
all 29 checks passed. Replace it: run the four self-checks in `artifact-engineering.md` as arithmetic in code
over the emitted markup — `x + width` inside the viewBox, no two boxes overlapping in a band, `len
× 0.55 × font-size` of clearance either side of a centred anchor, arrows computed edge to edge. **[docs]**
*"Gemini's code execution tool enables the model to generate and run Python code, and should be enabled whenever the
model needs to perform any kind of arithmetic, counting, or calculation."* Then capture it (override 5). With no
capture, say so: `evidence.md` §1.9 — `eli5`'s *open-loop visual blindness* — is unmitigated for this file.

## 4. Phases become files, not notes

**[docs]** *"make each step a prompt and chain the prompts together in a sequence"*. `[measured-family]` On the one
recorded run whose skill composition was phrased as a lens rather than a gate, both invocations were skipped, and
the run's own diagnosis named the mechanism: nothing downstream depended on a file only those skills produce.

Phase 1 asks you to `Name three things in your working notes`. Working notes are not a file, so nothing reads them
back. Write `notes.md` — filled like this, from `eli5`'s own Phase 1 and 2 vocabulary — and read it before markup:

```
topic         virtual memory — what one address does on the way to a byte
invariant     every address a program names is translated on use; the page table, not the program,
              decides which frame it lands in                             (a constraint relation)
misconception that addresses are places
entry point   a cloakroom ticket — a number you hold that is not the shelf it names
mapping       ticket number | virtual address  | a label its holder cannot resolve alone
              the desk      | page table + MMU | sole authority mapping label → location
              shelf slot    | physical frame   | reassignable without reissuing the label
boundary      carries   the indirection, and that the desk may move the coat while the ticket stays valid
              does not  paging to disk has no cloakroom row; and two tickets never name one shelf, where
                        two processes can share one frame
              wrong     believing addresses are places predicts two processes at the same address collide,
                        and that a page fault has lost the bytes
form          Machine, because the invariant is a discrete process with state run step by step — the reason
              `forms.md` assigns Raft to Machine; stepper both directions
surface       SVG + GSAP, because one reader-caused access moves the TLB row, the table row and the frame
              highlight in order (`forms.md`: Machine → plain SVG, GSAP once a state change moves several)
terms         14: virtual address, physical address, page, frame, page table, TLB, MMU, page fault, offset,
              resident, swap, dirty bit, working set, translation
```

The artifact-side receipts already exist: the `<!-- FORM: … -->` comment from Phase 3 and the `<!-- surface: … -->`
comment `surface-reach` reads. Fill both from `notes.md` rather than composing them at the end.

**Skill composition, converted.** `Load dataviz before the first line of chart code` is a `Skill` tool call,
discharged by the call and the palette validator's output; chart code that conforms to `dataviz`'s rules is not a
receipt for having loaded it. Same for `/remotion-best-practices` when a clip is in scope. The one skill `eli5`
deliberately does *not* invoke is `agent-voice`: `evidence.md` §4.8 — its gate passed the unreadable artifact — so
read that skill's `ai-writing-signs.md` §1.7 and §2.3 and report no check from it.

## 5. Describe the capture before you judge it

**[docs]** *"Ask the model to describe the images before performing the task in the prompt."* And *"To
improve the response, point out which parts of the image are most relevant to the prompt."* And on reading
a failure: *"A prompt can fail because the model did not understand the image at all, or because it did not
perform the correct reasoning steps afterward."* `[measured-family]` The comparison run opened 4 images for
a 10-cell artifact and reported on all ten.

The denominator for an `eli5` page is one capture per depth pass × theme, plus one at a narrow width and one under
reduced motion — for a three-pass page in two themes, **8 captures**. Open all of them and report the fraction. Crop
to the diagram, name what is in the crop, then judge it. When a label looks wrong, say what is in the image before
changing CSS, and capture in Chromium: Obscura drops whitespace at inline-element boundaries.

**Second lever, unmeasured here.** **[docs]** *"For UI generation, the model shows high design adherence
and parity based on a reference input, whether it's a screenshot, an image, or a full design system."*
Every static-page task in the benchmark was a prose brief with no reference, and that is the bucket that
collapsed. Where the requester has a mock, a screenshot or a palette, supply it before Phase 3.

## 6. Two attempts, then change approach

**[docs]** *"you must change your strategy or arguments, not repeat the same failed call."*
`[measured-family]` Four consecutive invocations of one absent tool with nothing changed between them.
Three of `eli5`'s build steps fail permanently rather than transiently, and each pivots on attempt 1:
`vendor_lib.py` refusing a checksum mismatch or a split Three.js build (pass a local path, or take the
single-file r169 route); a `media-gen-pro` call, which bills per image, so a retry costs money against a
cap of three; and a `Read` that hits a token ceiling on `evidence.md`, which takes a line range instead.

## 7. `thinking_level`, sourcing, and the examples in this file

**`thinking_level`.** **[docs]** `HIGH` is described as suitable for *"such as multi-step planning,
verified code generation, or advanced function calling scenarios"*, which is what Phases 1–6 are.
**[docs]** 3.7 Flash defaults to `MEDIUM` — *"The default thinking effort is now medium, changed from high
in Gemini 3 Flash Preview."* `[measured-family]` Paired across 106 tasks, `high` beat `medium` on 24, lost
on 24 and tied on 58. Set it for what Google says it is for; nothing in overrides 1, 2 or 3 gets better by
raising it. **[docs]** *"Higher thinking levels encourage the model to use more tools to explore and
verify, so lowering the level can reduce tool calls"* — which bites, since overrides 3 and 5 add tool calls.

**Recall is not a source.** **[docs]** *"Your knowledge cutoff date is January 2025."* The mechanism you are
explaining may have moved, and so may the API you are drawing it with. Read `references/forms.md` and
`references/pedagogy.md` rather than recalling them; read the vendored GSAP or Three.js file rather than
recalling its API; and **[docs]** *"Grounding with Google Search connects the Gemini model to real-time web
content, and should be enabled whenever the model may need to know obscure or recent facts."* A mechanism
detail you cannot source is stated as omitted in the third pass, not filled in — **[docs]** *"If the exact
answer is not explicitly written in the context, you must state that the information is not available."*

**One tension worth naming.** **[docs]** *"Prompts without few-shot examples are likely to be less effective."* But
`eli5`'s measured failure is a model copying its worked examples verbatim — three artifacts reused nine or ten of
them, which is why `no-template-boilerplate` exists. Both hold: copy the *structure* of the filled ledgers above,
take no string from `eli5`'s illustrations into the page, and name the headings from the topic's own vocabulary.
