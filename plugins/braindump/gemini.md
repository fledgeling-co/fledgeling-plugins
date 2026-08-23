# `braindump` on Gemini

`SKILL.md` is the canon and it stands. This is the layer a Gemini runner reads first; every
override names the `SKILL.md` section it lands on, so nothing has to be reassembled from two
places — **[docs]** the health checklist warns against that shape under **Conflicting internal
references**: *"Avoid writing a prompt with non-linear logic or conditionals that require the
model to piece together fragmented instructions from multiple different places in the prompt."*

`braindump` exists because a compaction summary loses things; the measured Gemini failure is
losing whatever a requirement named categorically. This skill's four sweeps are categorical.

## Epistemic status

**Tiers:** `[docs]` (Google, verbatim) · `[measured-family]` (Gemini runs of *other* skills, plus
a benchmark corpus) · `[derived]`. **`[measured-here]`: none** — no Gemini run of `braindump` has
been observed; every rate is n=1 per session (`Egress Gemini`, `COD Dossier`) or n=106 tasks
(`diolog-swe-bench`, bench `diolog-2.0`).

**The tier the evidence is about:** all of it is **flash-tier** — `gemini-3.7-flash` at `medium`
and `high`, plus one `gemini-3.7-flash-high` session. None is measured on Pro and none should be
projected there; on Pro these overrides hold as `[docs]`-grounded discipline while every
`[measured-family]` number is an open question.

**Unmeasured on this skill:** no Gemini run has produced a compaction summary under `braindump`,
so there is no before/after and no evidence these overrides move `scripts/score_retention.py`. The
benchmark corpus measures a model **building** code artifacts — compressing a transcript is
neither building nor judging code, so everything below transfers **by analogy**. And `SKILL.md`'s
own numbers (0.3% retention, 121 events, the paired case, the ~168k residue) came from **Claude**
summaries and the built-in `/compact`; they are not Gemini rates.

## What transfers intact

- **The two-tier split, the nine-section shape, the escape hatch and the REREAD list** — all four
  are decisions about structure and file references rather than prose exhortations, and that is
  what survives. **[docs]** **Missing output format specification**: *"Avoid leaving the model to
  guess the structure of the output; instead, use a clear, explicit instruction to specify the
  format and show the output structure in your few-shot examples."*
- **The keep/drop question** — `does the next session do something wrong, or merely something
  slower?` A binary test with a stated criterion is the form **Ambiguity** asks for.
- **Verbatim reproduction inside Tier 1.** **[measured-family]** the `Egress Gemini` run's
  content was specific — real CIDRs, real port numbers, a licence cap cited by clause — and
  quoting a span you have already located is what this family does well.

## What the scan found

`scan_skill.py --refs` over `SKILL.md` and its three references (960 lines): **6 quota rows, 8
bound rows, 12 relative qualifiers, 0 qualitative skill references, 0 emphasis tokens**, plus 66
distributive and 51 prohibition phrases counted as loose prose. Modules earned at three
triggers: `authorship` (5), `delegation` (3), `bounded-constraint` (3). **Three quota rows were
dropped as prose:** `SKILL.md:385` *any claim* (a sentence in **The honest limits**),
`compact-addendum.md:125` *every item* (the superseded v2 literal, duplicating the live v3 row),
`evidence.md:183` *all errors* (a quotation of Claude Code's built-in prompt, not this skill's
scope).

The rows that matter most were **not** in the scan's list: `every standing constraint`, `every
correction`, `every method dead end`, `every product dead end` sit among the 66 counted
distributives and are moved into the ledger by hand below. For two of the 12 relative qualifiers
`SKILL.md` supplies its own number (`~20 pinned items`, `20,585 chars`) — use those.

## Override 1 — the four sweeps become a counted ledger

**Lands on:** `§ The two tiers` (items 1–4), `§ Sweep the whole window`. `SKILL.md` already says
`Sweep once per category, not once overall` and names the four. **[measured-family]** that is the
phrasing that collapsed elsewhere: a run delivered 12 of 12 enumerated features and **1 of 6**
named states, `all menus` → 0, `all user flows` → 0, on a brief whose skill named six states *and*
stated a completeness condition. **[docs]** **Ambiguity**: *"Avoid using subjective or relative
qualifiers that lack a concrete, measurable definition."* And on why one pass cannot carry four
categories: *"Break the requests into separate prompts."*

Write the ledger to a file **before** the summary, one row per sweep, each sweep its own pass
oldest-turn-forward, and report the fraction at delivery. Filled from arm B of
`references/case-study-paired.md` — the run this skill produced:

| # | sweep (`SKILL.md` line) | items found | destination | note |
|---|---|---|---|---|
| 1 | standing constraints (40) | `n/a: recorded as quoted, never counted` | — | live runs need an integer |
| 2 | user corrections (42) | 1 | pin | a peer-runner correction; both arms pinned it |
| 3 | method dead ends (48) | `n/a: pointed at a named section, not counted` | point | pointer re-read, section confirmed |
| 4 | product dead ends (50) | 8 | pin | no durable home existed |
| 5 | exact identifiers (53) | `n/a: not separately counted in the case` | — | live runs need an integer |
| 6 | REREAD paths (227) | `n/a: the case predates the v3 REREAD list` | — | — |
| 7 | items carried from a prior pinned block (196) | 0 | — | none existed; B was first |
| 8 | pin-or-point decisions (202) | 9 recorded | 8 pin · 1 point | one tag per item, none implicit |

Delivery line: `4 of 8 ledger rows carry a count, 4 n/a with reasons (rows 1, 3, 5, 6).`
**[derived]** Four `n/a` cells is a poor score and showing it is the point: on a live run rows 1,
3 and 5 must carry integers, because the transcript is in front of you and `not counted` is a
sweep that did not happen. **[docs]** hand the counting to code — *"Gemini's code execution tool
enables the model to generate and run Python code, and should be enabled whenever the model needs
to perform any kind of arithmetic, counting, or calculation."* The pinned tier is the stated
exemption from **[docs]** *"By default, Gemini 3 models provide direct and efficient answers."*,
carried as a count: ceiling ~20, every ledger row placed.

## Override 2 — every bound is read back off the written summary

**Lands on:** `§ Preserve exactly, never paraphrase`, `§ Length`. **Module:** `bounded-constraint`.
The highest-value section, because `braindump` has measured this failure on itself: `SKILL.md`
line 145 records an eval where both arms pasted a nine-line header comment and a schema fragment,
both blew the length cap, and the skill arm put the comment **inside its pinned block** — against
a rule stated three lines earlier. **[measured-family]** that shape dominates Gemini's benchmark
failures: 58% of failing UI assertions are bound-shaped at `medium` and **86%** at `high`, against
8% for `claude-opus-5`, and one rule — a stated maximum of one shadow — failed on *every* instance
in its set on a run that passed 37 of its 39 others. A bound is violated by what you did not
write, so it survives every check that looks at what you did.

**[docs]** Google names where constraints go: the **Recap** component is a *"Concise repeat of
the key points of the prompt, especially the constraints and response format, at the end of the
prompt."* The bound ledger is that recap, carrying values rather than restating the rule. Fill it
from the **produced** summary, not from `SKILL.md`, on every instance:

| instance | property | stated bound (line) | readback | observed | within? |
|---|---|---|---|---|---|
| pinned block | Tier-1 items | `~20 pinned items as the ceiling` (38) | count ledger rows placed | 13 | yes |
| pinned block | fenced content | `The pinned tier never contains file contents` (142) | count fences between the block markers | 1 (nine-line header comment) | **no** |
| pinned block | categories | `Four categories, and only these four` (34) | count distinct category headings | 4 | yes |
| REREAD list | one item per line | `one path per line` (227) | `awk 'NF>1' reread.txt \| wc -l` | 0 | yes |
| each Tier-1 item | destinations | `exactly two safe destinations` (202) | every item tagged `PIN` or `POINT` | 13 of 13 | yes |
| whole summary | length | `20.6k characters … a ceiling, not a target` (281) | `wc -c summary.md` | 9,388 | yes |
| Tier 1 | trimming | `Never cut Tier 1 to fit` (284) | ledger rows before and after the trim | 13 → 13 | yes |

Report `7 bound rows, 6 within bound, 1 violation — fenced content inside the pinned block` on
every run, not only a clean one. The violated row stays rather than being tidied away: a ledger
that has never printed **no** is a ledger nothing reads.

**The prohibition trap, in this skill's own words.** `The pinned tier never contains file
contents` and `Preserve exactly, never paraphrase` are both binding, they collide, and `SKILL.md`
says which wins. As prohibitions they read as style advice; as a counted property with a readback
— *fenced blocks inside the pinned block: 0* — one becomes checkable. Convert `never paraphrase`
the same way (every Tier-1 span is substring-present in the transcript), and `It's somewhere in
the repo is not a destination` (every `POINT` names a file **and** a section, opened).

## Override 3 — verification is a command with its output, and a zero denominator is not a pass

**Lands on:** `§ Order of work` step 3, `§ Scoring`, `§ The honest limits`. **[docs]** *"Include
specific verification steps in either the system instructions or your prompts directly."* And from
the agentic template: *"Verify your claims by quoting the exact applicable information (including
policies) when referring to them."* **[measured-family]** the vacuum is not hypothetical: one run
wrote itself a review asserting a browser engine that failed on all four invocation attempts and
never ran, and a 100% contrast pass rate from a probe never executed — measured afterwards, every
primary button 3.65:1 and one glyph at 1.00:1, invisible. So every number in the delivery note
carries the command that produced it and its pasted output:

```
python3 scripts/score_retention.py --transcript <session.jsonl> --summary <summary.md>
```

**The zero-denominator rule, which this skill needs more than most.** `SKILL.md`'s limits section
reports that over 30 random events the correction detector yields zero spans in **93%** and
rejected approaches zero in **70%**. `n/a (0 of 0)` is therefore the expected output and it means
the instrument found nothing — never that the summary passed. Write it as `detector found 0 spans
in this class; unverified`, and name which Override 1 rows then rest on the hand sweep alone. Same
for `--against`: `SKILL.md` says the disjoint sets settle a comparison and the percentages do not,
so paste the disjoint sets. And never let the summary assert its own verification: `tree clean` in
`Current Work` is a claim about a command's output, and the paired case holds the arm that got
this wrong — accurate about the tree, wrong about the obligation.

## Override 4 — the transcript will not fit in one read, and retrying will not help

**Lands on:** `§ Order of work` step 1, `§ Sweep the whole window`. A window worth compacting is
large — the paired case works a 4,563-row transcript — and the read will hit a ceiling.
**[measured-family]** on a 28.6k-token file against a 25,000 token ceiling, one run retried the
same `Read` **four consecutive times** with minor parameter tweaks before pivoting to a Python
split; a separate session invoked one absent tool four times unchanged. **[docs]** *"On *other*
errors, you must change your strategy or arguments, not repeat the same failed call."*

Two attempts per tool, then change approach — and **one** when the error is a capacity ceiling or
a permanent failure (`command not found`, a `--help` that errors). Pivot on attempt 1 to
line-ranged reads, `jq` over the `.jsonl`, or a Python helper that slices the window into ordered
chunks. Write that chunk list to a file and walk it oldest-first, so `start at the oldest turn and
walk forward` is a file rather than a memory of how far you got.

## Override 5 — pin-or-point is a closed two-option choice, and the sweep is not delegated

**Lands on:** `§ Pin it, or point at it`, last paragraph of `§ Order of work`. **Module:**
`delegation`. **Subagent cap: zero** — `SKILL.md`: `Do the sweep yourself. A subagent returns what
it judged salient, and salience is the judgment being replaced here.` That holds unchanged;
Override 4's chunking is the answer to a large window, not a fan-out, and verification of your own
summary is not delegated either. **[docs]** Google's remedy for a model that answers correctly but
outside the offered options is to close the set: *"you can rephrase the instructions as a multiple
choice question and ask the model to choose an option."* So every Tier-1 item carries a literal
`PIN` or `POINT` tag and row 8 of the ledger counts them; an untagged item is one dropped on
assumption.

## Override 6 — quote it, or record it as unavailable; read what the prompt names

**Lands on:** `§ Preserve exactly, never paraphrase`, `§ The re-read list`, and `treat it as a
checklist, not a source` in `§ Sweep the whole window`. **Module:** `authorship`. The output is a
document a stranger acts on without the transcript. **[docs]** Google's strictly-grounded system
instruction ends on the clause that matters here: *"If the exact answer is not explicitly written
in the context, you must state that the information is not available."* So an item that cannot be
quoted from the window is written as `not located in window` with the sweep that looked for it,
never reconstructed from a memory of the session — the same rule **Underspecified task** states
for missing data: *"provide instructions for handling missing data rather than assuming inserted
data will always be present and well-formed."*

The reciprocal is reading. **[measured-family]** asked a question naming three skills, one run
answered from memory without loading any; asked to fix it, it inverted the error and launched a
skill instead. The rule is two ordered steps — read what the prompt names, **then** answer — so a
prior summary, plan, spec or rules file named in the request is opened before the sweep starts and
its Tier-1 items become row 7. **[docs]** *"Your knowledge cutoff date is January 2025."* — March
2026 for 3.7 Flash, though in some domains *"they may experience the model's knowledge is limited
to January 2025 (in line with the Gemini 3 Model Family)"*.

## `thinking_level`

**[docs]** `HIGH` is *"suitable for complex prompts requiring deep reasoning, such as multi-step
planning, verified code generation, or advanced function calling scenarios."* Four ordered sweeps
over a long window, each feeding a ledger, is that shape. 3.7 Flash defaults to `MEDIUM` and the
default has drifted inside the family — *"The default thinking effort is now medium, changed from
high in Gemini 3 Flash Preview."* — so name the level rather than inheriting it. And **[docs]**
*"Higher thinking levels encourage the model to use more tools to explore and verify, so lowering
the level can reduce tool calls."* — fewer tool calls is the wrong direction for a method whose
content is re-reading the transcript.

**Not a remedy.** **[measured-family]** paired across 106 tasks, `high` beat `medium` on 24, lost
on 24, tied on 58, mean −1.7 points — and the bound-shaped share of failures rose from 58% to 86%
at `high`. Nothing in Overrides 1–3 improves by raising it.

## The worked example — one Tier-1 item at full fidelity

**[docs]** *"We recommend to always include few-shot examples in your prompts."* Author one item
completely before the set and measure the rest against it. Item text from
`references/case-study-paired.md`; the row index is illustrative. Where the default produces one
clause — `Rejected several approaches, including a Boolean coercion` — the exemplar is:

```
PINNED · rejected approaches — product (4 of 8)

R3  `Boolean(...)` for a default that must be `??`
    rejected because: it coerces a stored `0` and `""` to the default, corrupting
    the row on write-back.
    do not retry unless: the column is documented non-nullable and never zero-valued.
    source: window row 3841 · destination: PIN (no durable home)
```

Four countable fields — a reason, a retry condition, a locatable source, a destination tag — none
of which survives the collapsed form.

## Modules not written, and why

`visual` (1 trigger), `states` (1), `platform-values` (1), `count-contract` (1) and `injection` (0)
fell below the three-trigger threshold: the skill renders nothing, cites no vendor design values
and enumerates no interface states. `gate` also scored 1 — the bare `scripts/` path — despite the
skill shipping two deterministic scorers; its denominator and prove-it-can-fail rules are folded
into Override 3, because a module whose content is the core applied to the target is not a module.

**No route-out block.** The corpus measures a model *building* code artifacts and its four named
shapes are `static-page`, `brownfield-integration`, `visual-design` and `regression-sensitive`.
`braindump` produces none of them: it compresses a conversation into markdown and scores it with
Python. **[docs]** the entry a route-out block applies — *"Avoid using prompts that ask the model
to perform a task for which it has a known, fundamental limitation."* — needs a known limitation,
and nothing in the corpus measures Gemini summarising a transcript.
