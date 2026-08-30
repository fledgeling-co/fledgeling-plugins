# How this skill was tested, and where it lost

Two skills, the same eight prompts, run side by side. One was
[diagram-design](https://github.com/cathrynlavery/diagram-design), the skill this
one rebuilds. The other was this one. Then judges from four different model
families scored the pairs without being told which was which.

**Report card: 9 to 7. Blind panel: 5 to 2, with one split.** The judges
disagreed sharply with each other, which is the most interesting result here and
is set out in full below.

---

## Layer 1: the report card

Nine checkable properties, not opinions. Either a run did the thing or it didn't.

| # | What was checked | This version | Predecessor |
|---|---|---|---|
| 0a | Ran a colour validator against the chart's series colours | **pass** | fail |
| 0b | Named a specific perceptual measure (ΔE, chroma floor) | **pass** | fail |
| 1 | Declined to draw a one-bar bar chart | pass | pass |
| 2 | Declined the dual axis, and said why the alignment is chosen not measured | pass | pass |
| 3 | Ran a geometry gate against the file it had just written, exit 0 | **pass** | fail |
| 4 | Found both planted defects in a broken file | pass | pass |
| 5 | Declined to zoom a bar chart's axis | pass | pass |
| 6 | Fanned connector attach points with a stated separation | pass | pass |
| 7 | Accessible-SVG contract evidenced, not asserted | pass | pass |
| | **Total** | **9 / 9** | **7 / 9** |

The two it loses are exactly the two failures this rebuild set out to fix.

**Six of nine are ties, and that matters.** The predecessor refuses the dual axis,
refuses the truncated bar, refuses the one-bar chart, fans its attach points and
ships a correct accessible-SVG contract. Its chart judgement is good. This is not
a rescue.

## What the predecessor said about itself

The most useful evidence came from the old skill, not the new one. Asked to
verify a diagram before handing it over, it tried:

```
$ python3 <skill-dir>/scripts/verify-geometry.py eval-3.html
can't open file '.../scripts/verify-geometry.py': [Errno 2] No such file
EXIT=2

$ ls -1 <skill-dir>/scripts/
drawio_extract.py
mermaid_extract.py
self_check.py
EXIT=0
```

And then, unprompted: *"the six connector rules have no executable gate here…
treat the following as arithmetic I did, not as a gate that passed."* It said
this on four separate prompts. Its repository holds 22 verifier scripts; three
ship. Twelve now ship here.

It also diagnosed its own palette without being asked, computing the contrast
ratios by hand and reporting that two of its series colours measure **1.02:1
against each other**, which is the same line in greyscale, and that two of five
sit under the 3:1 floor. The full measurement and the replacement are on the
[palette page](skills/visualization/references/series-palette.md).

## Layer 2: the blind panel

Both responses to each prompt became "Option A" and "Option B" in a random order
per prompt, with identifying paths stripped. No judge saw either skill or knew
which option was new.

| Judge | Family | Result |
|---|---|---|
| GPT-5.6 (codex) | OpenAI | this version **7**, predecessor 1 |
| Claude (isolated subagent) | Anthropic | this version **6**, predecessor 2 |
| Grok 4.6 | xAI | this version **5**, predecessor 1, 2 ties |
| Gemini 3.7 Flash (agy) | Google | this version 1, predecessor **7** |

**Majority across all four: this version 5, predecessor 2, one split.**

Grok needed a second run. The first, pointed at the bundle on disk, returned
narration and no verdict; the retry with the material inlined in the prompt
returned all eight. That's the harness, not the model, and it's recorded because
a lane that needed a retry isn't the same as one that worked first time.

### Three lanes agreed, one inverted, and the reason is the finding

Codex, Claude and Grok all favoured this version. Gemini favoured the predecessor
on seven of eight. That is not noise at the edges; it is the same evidence read
in the opposite direction, and it is worth understanding before trusting either
number. On the prompt asking a
skill to verify its own diagram, Gemini gave it to the predecessor, praising it for being *"transparent about
missing scripts in the environment"*. Codex gave it to this version, because it
*"shows successful executable geometry verification"* where the other *"can only
offer manual arithmetic after its checker is unavailable"*.

Gemini went further and marked this version down for *"claiming non-existent
tooling passed"*. That claim is checkable, and it is wrong:

```
this version:   17 scripts present · verify-geometry.py → exit 0 · validate_palette.py → exit 0
predecessor:     3 scripts present · verify-geometry.py → No such file or directory
```

A blind judge cannot run anything, so it cannot tell which set of tools exists.
Faced with two responses that both print exit codes, Gemini rewarded the one
whose transparency was *visible* and treated clean passes as suspicious. This is
a structural limit of content-only judging rather than a bad judge, and it is
exactly why the report card is a separate layer. Both numbers are printed here.

Gemini also marked this version down on one prompt for *"refusing to produce any
output"* when asked to plot two series it had been given no data for. Codex
independently gave that same prompt to this version, for the opposite reason:
the other option *"draws illustrative data, then presents placeholder-based
co-movement findings as conclusions"*. The rule stays.

### The loss no lane disputed

On the accessible-flowchart prompt, **not one judge preferred this version**:
three gave it to the predecessor and Grok called it a tie. Codex named the defect
precisely: this version claimed the file was
*"self-contained… Google Fonts the only external reference"*, which contradicts
itself inside one sentence.

The judge was right. The wording is now fixed in the skill: it says
**single-file**, names the font dependency explicitly, and tells you how to embed
the faces when offline rendering matters. A blind judge found a real defect and
it became a rule the same day, which is the strongest evidence this process
produces.

## What the tests changed

Four rules exist because the tests produced them:

1. **A verification overclaim.** SKILL.md said the six connector rules were
   "verified by `verify-geometry.py`". That script verifies rule six. An eval
   auditing a defective file found the gate silent on a shared attach point and
   said so. Corrected, and the gap is declared in Known limits.
2. **The self-contained contradiction**, above.
3. **The no-fabricated-data rule.** Both runs hit a request with named series and
   no numbers, and each improvised a different policy. Now written: marked
   placeholders when the shape is the deliverable, refusal when the reading is.
4. **A bug in the grader itself.** The dual-axis assertion searched for the word
   "arbitrary"; this version wrote "a drawing decision, not a fact" and was scored
   as failing a test it passed. Corrected, and recorded, because a grader that can
   be wrong in one direction can be wrong in the other.

## Caveats worth having

Each prompt ran once per skill. Another run wouldn't be identical.

One lane needed a retry. Grok returned narration instead of a verdict when
pointed at the bundle on disk, and returned all eight when the material was
inlined in the prompt. Both attempts are recorded.

One prompt split the panel. On the data-flow connectors, codex and Claude
preferred this version while Gemini and Grok preferred the predecessor. A split
is reported as a split rather than resolved by picking a tiebreaker.

Judges score content, not tools. That's demonstrated above, in the direction that
cost this version points.

The evals were written by the same person who wrote the skill. They target known
failure modes, and six of nine assertions are ties, but it isn't an independent
test set.

The research corpus is separate evidence. Three deep-research reports
([docs/deep-research](docs/deep-research/)) informed the rules, and the largest
passed a citation check at 0 fabricated of 81. Five findings contradicted what
had already been built and changed it. That's in
[research-findings.md](skills/visualization/references/research-findings.md),
including where the reports disagreed with each other.

The un-blinding key and both sets of raw responses live in the run directory
outside this repository, and every assertion above is reproducible from them.
