# visualization on Gemini

Read this before `SKILL.md`, once, then follow `SKILL.md` with the overrides below. Each override names the section it lands on, so nothing here has to be held in mind while you draw.

The canon transfers. Fifty-three forms, six connector rules, the honesty rules and twelve runnable checkers are all correct for this family. What does not transfer is the assumption that a number stated in prose gets read back off the file that was drawn — and this skill is unusually dense in stated numbers: `9 nodes, 12 arrows, 2 accents`, `≤24px` bars, `Max radius 6–10px`, `5 chart series`, `Exactly one per view` for the hero figure, `At most two` items entering per motion step.

## Epistemic status

- `[docs]` — Google's published guidance, quoted verbatim. Most of this file.
- `[measured-family]` — Gemini runs of *other* skills, plus a 106-task benchmark (`gemini-3.7-flash` at `medium` and `high` against `claude-opus-5`, read 22 Aug 2026). Flash-tier throughout; on the Pro tier every rate here is an open question and only the `[docs]` half holds.
- `[derived]` — reasoning from those, labelled where used.
- No Gemini run of **this** skill has been read. There is no `[measured-here]` claim below.

**Unmeasured on this skill:** the bound ledger against §7's budget and §5's radius and shadow rows · the twelve-checker receipt · the reference-input path through `assets/` · the three-variant and reduced-motion state matrix · token provenance against `style-guide.md` · the taste gate as 60 cells rather than one line.

## Route out before you start (§9's deliverable)

**[docs]** The prompt health checklist, under **Task outside of model capabilities**: "Avoid using prompts that ask the model to perform a task for which it has a known, fundamental limitation."

§9's deliverable is `Always one .html file: embedded CSS, inline SVG, no external images` — a self-contained page authored from a prose brief, which is the bucket that collapsed hardest in the benchmark. The taste gate in §8 judges it aesthetically, which is the second.

| this skill's work | shape | `[measured-family]` |
|---|---|---|
| the single-file HTML in §9, drawn from a prose request | `static-page` | 22 against opus's 67; hard zero on 71% of decided rows |
| the editorial register the taste gate judges (§1, `taste-gate.md`) | `visual-design` | 35 against 63 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape static-page
```

`brownfield-integration` and `regression-sensitive` are not listed: this skill authors a new file every time and edits no existing multi-file code, so neither row lands. Where the work stays here — no lane, or this model was asked for — the block still says which part of the output to distrust first: the drawn page, before the routing and honesty rules that got it there.

## What transferred intact

Do not spend effort re-hardening these; they already have the shape this family needs.

- **§3's routing tables.** A lookup keyed on `what must the reader do?`, each row naming one form and one reference file. Objective, non-categorical, no judgement in the middle.
- **`Always load the chosen type reference before drawing.`** Already a read-then-act ordering rather than a standard to hold in mind.
- **§8's command table**, and **`Read the exit code, not the output`** stated twice (§4, §8) with the failure named. Twelve commands with exit codes is what C2 asks every other skill to build. Keep both as written.
- **§10, Known limits.** Declared gaps, including `Five of the six connector rules have no checker`. A file that says what it does not check is doing C2's work already.
- **The complexity budgets as numbers.** `9 nodes, 12 arrows, 2 accents` is the objective constraint **[docs]** asks for. What is missing is only the readback.

## Core overrides

### C1 — the quota ledger (§7, §9, `taste-gate.md`)

**[docs]** Under **Ambiguity**: "Avoid using subjective or relative qualifiers that lack a concrete, measurable definition." Under **Too many tasks**: "Break the requests into separate prompts."

**[measured-family]** A categorical noun is satisfiable with one instance, and on one recorded run it was: `all surfaces` → 5, `all states` → 1, `all menus` → 0, `all flows` → 0. This skill's categorical scopes sit in the references rather than in `SKILL.md`: `Every flow gets its own offset range` (Sankey), `All axes must be measurable on the same normalized scale` (radar), `every cell` within a few percent of its true share (treemap), `Every state` and `All stages` visible in the static frame (`animation.md`).

Write the ledger into the deliverable's notes before drawing, one row per unit, each filled or marked `n/a: <reason>`, and report the fraction.

| unit | scope, in the skill's words | n | built | evidence |
|---|---|---|---|---|
| variants | `Three variants ship for every type` (§9) | 3 | 3 | `ls flows-{light,dark,full}.html` |
| `<title>`/`<desc>` | the accessible-SVG contract (§9) | 6 | 6 | `grep -c '<desc>'` → 1,1,1 |
| Sankey ribbons | `Every flow gets its own offset range` | 11 | 11 | `verify-sankey.py` exit 0 |
| taste-gate boxes | `taste-gate.md` | 60 | 54 | 6 `n/a`: no motion, no CJK, not an import |

Report as `74 of 74 cells resolved, 6 n/a with reasons` — never as `taste gate run`.

### C2 — verification is asked for, not assumed (§8)

**[docs]** "Include specific verification steps in either the system instructions or your prompts directly." And "Verify your claims by quoting the exact applicable information (including policies) when referring to them."

Every number in the handover carries the command that produced it and that command's output. A denominator of zero is a gate that never ran, never a pass. §8 already warns about the pipe; the addition is that the *set* of gates that applied is itself a number to report. **[derived]** This reverses the usual house style — an instruction to verify gets removed for models that over-verify, and inheriting that removal here is the defect.

```
self_check.py flows-light.html                            exit 0
verify-geometry.py flows-light.html                       exit 0
verify-sankey.py flows-light.html                         exit 0
validate_palette.py "…" --mode light                      exit 0
validate_palette.py "…" --mode dark --surface "#2d3142"   exit 0
verify-motion.py     not run — mode none, no motion markup
verify-treemap.py    n/a — not a treemap
gates applicable 5 · run 5 · exit 0: 5 · type reference read: references/type-sankey.md
```

### C3 — the retry ceiling

**[docs]** "you must change your strategy or arguments, not repeat the same failed call." **[measured-family]** Four consecutive invocations of one absent tool with nothing changed between them. Two attempts per command, then change approach. A missing `python3`, an absent Playwright in `export.md`'s PNG path, or a checker that errors on its own `--help` gets one attempt, then the honest line: the artifact is ungated and the delivery says so. **[docs]** "You have a limited action budget of <n> tool calls. Use them efficiently."

### C4 — passes, and file dependencies rather than lenses (§0, §3, §4)

**[docs]** "Chain prompts: For complex tasks that involve multiple sequential steps, make each step a prompt and chain the prompts together in a sequence."

**[measured-family]** Where one phase can be completed without the literal output of the previous one, both collapse into one pass. §0's style-guide gate, §3's route and §4's palette gate are that shape — each is satisfiable by having read the rule. Make each depend on a file or a command output:

1. §0 → resolve `.visualization`, or read `references/style-guide.md`. Name the resolved profile in the notes; `profile: default` is a written answer, not a skip.
2. §3 → read the chosen `type-*.md` and quote its budget line into the notes.
3. §4 → run `validate_palette.py` and paste both exit codes before any hex reaches the file.
4. Draw. 5. Run §8's checkers. 6. Walk `taste-gate.md` as cells (C1).

Do not merge 2 into 4. **[docs]** "Avoid writing a prompt with non-linear logic or conditionals that require the model to piece together fragmented instructions from multiple different places in the prompt" — this file is read once, in order, and then set aside.

### C5 — one worked example first

**[docs]** "We recommend to always include few-shot examples in your prompts." Author one node, one bar, or one Sankey ribbon at full fidelity — mask, gap, attach point, `<desc>` line — before the other eight. Every table this file asks for ships filled in above rather than described.

### C6 — `thinking_level`

**[docs]** `HIGH` is "suitable for complex prompts requiring deep reasoning, such as multi-step planning, verified code generation, or advanced function calling scenarios", and the 3.5 Flash release notes record that "The default thinking effort is now medium, changed from high in Gemini 3 Flash Preview." Hand-authoring SVG coordinates against six connector rules is that description.

**[measured-family]** Do not read it as a remedy. Paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58 — and the bound-shaped share of failing assertions went *up*, 58% at `medium` to 86% at `high`. Nothing in C1 or `bounded-constraint` improves by raising it.

### C7 — recall is not a source (§4, `style-guide.md`)

**[docs]** "Your knowledge cutoff date is January 2025", and "Grounding with Google Search connects the Gemini model to real-time web content, and should be enabled whenever the model may need to know obscure or recent facts." Every hex, viewBox, type-ramp size and ΔE floor is read out of this skill's own files, never recalled. §4 states the rule — `specs refer to roles, never to literals` — and the failure it prevents is specific here; see `platform-values`.

## Modules

### `bounded-constraint` — the strongest override in this file

**[docs]** Google names constraints a component in their own right: "Restrictions on what the model must adhere to when generating a response, including what the model can and can't do." And names where they go — the **Recap** component is a "Concise repeat of the key points of the prompt, especially the constraints and response format, at the end of the prompt." The agentic template asks for the same: "Ensure that all requirements, constraints, options, and preferences are exhaustively incorporated into your plan."

**[measured-family]** This is the measured failure direction for this family, and it points opposite to C1. Of failing UI assertions, 58% at `medium` and 86% at `high` stated a bound (`exactly N`, `no`, `not`, `only`), against 8% for opus. One rule — `has exactly one soft elevation shadow` — failed on *every* card and *every* toast in its set on a run that passed 37 of its 39 other assertions. §5 of this skill bans `Shadow on any element` and `rounded-2xl on boxes`: the same two properties.

**[derived]** The mechanism is not a forgotten rule but a default idiom supplying the value under a rule that was read and agreed with. So the ledger is filled from the **produced file**, on **every** instance, by a command — not from the brief.

| instance | property | stated bound | readback | observed | within? |
|---|---|---|---|---|---|
| figure | accent elements | `1–2` (§1, §4) | count `accent`/`accent-tint` fills + strokes | 4 | **no** |
| figure | nodes | 9 (§7) | `grep -o 'data-node' f.html \| wc -l` | 9 | yes |
| figure | arrows | 12 (§7) | count `marker-end=` | 11 | yes |
| node boxes | corner radius | `6–10px, or none` (§5) | read every `rx=` | 6,6,6,16,6,6,16 | **no** |
| all elements | shadows | `Shadow on any element` is a fail (§5) | `grep -cE 'filter=\|drop-shadow\|box-shadow'` | 0 | yes |
| bars | thickness | `≤24px` (`marks-and-anatomy.md`) | read every bar `height=` | 24,24,24,28 | **no** |
| chart | series | 5 (§7, `series-palette.md`) | count legend keys | 5 | yes |
| motion steps | items entering | `At most two` (`animation.md`) | group by `data-step` | 2,2,1,3 | **no** |

Report `4 of 8 bounds within limit` and fix, rather than restating the rule. Two of this skill's bounds are stated as prohibitions and read as taste unless converted: `Shadow on any element` becomes a shadow count of 0, and `rounded-2xl on boxes` becomes every `rx` in `[0,6,8,10]`.

### `gate` — twelve checkers that exit non-zero (§8)

**[docs]** "When model outputs must be machine-readable or follow a specific format, use a widely recognized standard like JSON, XML, Markdown or YAML that can be parsed by common libraries", and "Gemini's code execution tool enables the model to generate and run Python code, and should be enabled whenever the model needs to perform any kind of arithmetic, counting, or calculation" — which covers every count in C1 and in the bound ledger. Count with a command; do not tally by eye.

Beyond C2's receipt: prove a gate can fail before trusting it passing. `validate_palette.py` exiting 0 on a palette you have not changed proves the script ran, not that your palette passed — pass the predecessor's set once (`"#7c8f6f,#5e7a9b,#b8915a,#9c6b50,#6e6479"`, documented as failing in `series-palette.md`) and confirm exit 1. **[measured-family]** On another skill's audit script, a check that matched nothing turned every file green, and only a negative control caught it.

`verify-geometry.py` covers connector rule 6 alone. Rules 1–5 are ungated and §10 says so; the handover names them as held by construction, never as passed.

### `visual` — a reference input exists, and it ships with the skill

**[docs]** Google's launch material for this model: "For UI generation, the model shows high design adherence and parity based on a reference input, whether it's a screenshot, an image, or a full design system." **[measured-family]** Every static-page task in the collapsed bucket was a prose brief with **no** reference. Untested together, but this is the documented strong path.

This skill ships 148 `assets/example-*.html` files — three variants for most of its types, plus `template-motion.html`. Read `assets/example-<type>.html` and its `-dark` twin before drawing, and name in the notes what you took from each: the ramp, the legend strip position, the eyebrow treatment. **[derived]** Two reads turn the collapsed shape into the documented one.

**[docs]** When judging a rendered capture: "Ask the model to describe the images before performing the task in the prompt", and "To improve the response, point out which parts of the image are most relevant to the prompt." Describe the crop — name what is in it — before judging it, and point at the region rather than the frame. Capture denominator: one per variant shipped, all opened, the fraction reported.

### `states` — the axes with no checker (§9, §10, `chart-honesty.md`)

**[docs]** Under **Underspecified task**: "provide instructions for handling missing data rather than assuming inserted data will always be present and well-formed."

§10 says it outright: `Interaction, print and reduced-motion are unverified by script.` Those are the states that get built once or zero times. A cell, not a line:

| state | rule | built | evidence |
|---|---|---|---|
| light / dark / full editorial | §9, three variants | y | three files; `verify-skin-polarity.py` exit 0 |
| no JavaScript | `complete meaning must render without JavaScript` | y | 0 `<script>`; `self_check.py` exit 0 |
| `prefers-reduced-motion` | complete static frame, controls hidden | n/a | mode `none` |
| print | §10 — unverified by script | n/a | no print destination requested |
| missing values | `chart-honesty.md` — disclosed, never imputed | y | 2 gaps drawn as gaps, named in `<desc>` |
| no data supplied | placeholders in four places, or don't draw | n/a | data supplied |

### `authorship` — the numbers a reader will act on (`chart-honesty.md`, §9)

**[docs]** Google's strictly-grounded system instruction, adopted verbatim for the data: "Treat the provided context as the absolute limit of truth", and its last clause — "If the exact answer is not explicitly written in the context, you must state that the information is not available."

That is `chart-honesty.md`'s traceability rule in Google's own words. Stated values appear in the table view as given; derived values are shown as derived with their base; a number that cannot be pointed at in the source does not go in the chart. The skill records why: an execution rate of 78.2% against a visual-accuracy score of 44.7% on the same set. A chart that renders perfectly from mis-extracted numbers is the failure nothing about the file looks wrong for.

The `<desc>` rule pulls the other way and matters as much: it states what is shown and does not editorialise or draw the conclusion. **[derived]** A model optimising for "useful" alt text adds exactly the interpretation 63% of blind readers were emphatic it must not have.

### `platform-values` — token provenance, and one specific trap

**[docs]** The knowledge cutoff plus the grounding clause; **[measured-family]** an old vendor value returned confidently rather than guessed. Here the values are this skill's own, and the trap is sharper than staleness: **the failed palette is printed verbatim in two reference files as a negative example.** Reaching for "the series palette" from memory can lift the set the gate rejects.

| value written into the file | role | source | tier |
|---|---|---|---|
| `#eb6c36` / `#2d3142` | `accent` light / `paper` dark | `style-guide.md` → Semantic roles | read |
| `#3f7a33 #5b4a8f #b07d18 #2a6ea8 #a4552c` | series 1–5, light | `series-palette.md` → The palette | read |
| `#7c8f6f #5e7a9b #b8915a #9c6b50 #6e6479` | — | **the predecessor's failing set** | never ship |
| `0 0 960 600` | `doc-inline` viewBox | `output-spec.md` §2 | read |
| 12 / 9 / 8 px | node name / sublabel / arrow label, standard ramp | `output-spec.md` type ramp | read |
| ΔE floor 15, CVD target 8 | palette gate thresholds | `series-palette.md` | read |

A cell you cannot tag with a file is a value you invented.

### `count-contract` — the skill already promises counts

**[docs]** Under **Ambiguity**, a named count is already an objective constraint, which is why these survive on this family when the surrounding prose does not. Extend them to the cells: `taste-gate.md` is 60 boxes and `output-spec.md` §6 is 11 more, so `taste gate: pass` is one claim standing for 71. Where the brief omits a count, derive it — an import's fidelity ledger reports `18 source nodes → 9 drawn` with the merged, collapsed and dropped rows named, and `9` comes from §7's budget rather than from the request.

## What is not here, and why

- **`delegation` fired on five triggers and is dropped.** All five are subject matter, not behaviour: `workflow` as a swimlane use-case, `orchestration` as an icon and a chevron name, `runner` as Airflow, `fan-out` as a connector routing rule. This skill spawns no agents.
- **`emphasis` did not fire** — three tokens, two of them domain rules inside type references (`connectors are MANDATORY`, `Markers MUST touch`). Read those as plain rules and add no capitals anywhere.
- **18 of the 44 quota rows the scan printed are dropped as prose**, not deliverable scope: a prohibition (`Shadow on any element`), a capture extent (`the whole page`), an XML-parsing note (`the whole file`), conditionals (`any check`, `any path`, `any cell carrying an info mark`), and a geometry phrase (`the full width`).
