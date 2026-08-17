---
name: geminify
description: >-
  Add a Gemini-calibrated `gemini.md` to an existing skill, so the same skill works on Google's models as well as Claude's. Reads the target skill, scans it for the unbounded scopes and assumed verification that Gemini handles differently, assembles the file from a shared core plus only the modules the skill's own subject matter earns, tags every claim by how strong its evidence actually is, gates the result by checking each quoted vendor sentence appears verbatim in Google's published guidance, then installs the conditional pointer and bumps the version. Use whenever someone wants a skill to work on Gemini — "geminify design-craft", "add Gemini support to this skill", "make this skill work in Antigravity", "write a gemini.md for X", "/geminify" — and whenever a skill produced weak output under a Gemini model and the skill itself is not at fault. NOT for fixing a skill that is broken for every model (use improve-skill), and NOT for authoring a new skill (use create-skill).
---

# geminify

A skill is a prompt. Prompts are tuned — usually silently, usually to whichever
model the author was running. Most of the skills in this ecosystem were written
against Claude's failure modes, and several of their most deliberate decisions are
*removals*: guidance stripped out because Claude over-does that thing when told to.

On Gemini those removals leave a vacuum, and the vacuum fills with something
plausible. This skill writes the layer that fills it deliberately instead.

The output is one file, `gemini.md`, beside the target's `SKILL.md`, plus a
conditional pointer at the top of the SKILL.md that other models skip. Not a
rewrite of the skill: the canon transfers. What does not transfer is the
assumption that a rule stated in prose gets executed.

## The finding everything here rests on

**[measured]** One recorded Gemini run on a rich brief delivered **every**
requirement the brief enumerated — twelve named features, all present — and
satisfied every requirement it named *categorically* with exactly one instance:
"all surfaces" → 5, "all states" → **1**, "all menus" → **0**, "all flows" → **0**,
"all actions" → one generic toast reused across the product. Same run wrote itself
a review claiming a browser engine that failed on all four invocation attempts and
never ran, and "100% pass rate on contrast" from a probe never executed. Measured
after: every primary button 3.65:1, one glyph at 1.00:1, invisible.

**[docs]** Google names both mechanisms. Under **Ambiguity**: *"Avoid using
subjective or relative qualifiers that lack a concrete, measurable definition.
Instead, provide objective constraints (for example, 'write a summary of 3
sentences or less' instead of 'write a brief summary')."* And verification is
something the prompt has to contain — *"Include specific verification steps in
either the system instructions or your prompts directly."*

So the work is mechanical, not literary: find the skill's unbounded scopes, give
each one a number, and put the verification back with its command attached.

Full evidence, including what is n=1 and what is not: `references/evidence.md`.

## Procedure

### 1. Read the target in full

The whole `SKILL.md`, and any reference it treats as binding. A `gemini.md`
written from a skill's description is a template with a filename, and it reads
like one. If the skill is large, read it anyway — this is the cheap part.

### 2. Scan it

```bash
python3 scripts/scan_skill.py <target>/SKILL.md --refs
```

Two outputs, both derived from the target rather than from a template:

- **The quota ledger** — every categorical quantifier attached to a countable
  deliverable, with its line number. These are what collapse to one instance.
- **The module triggers** — which optional sections this file needs, decided by
  what the skill demonstrably contains. A skill that renders nothing gets no
  capture guidance. Measured across four skills: `design-craft` triggers `visual`
  first (11 hits), `deck-craft` triggers `authorship` (11), `design-review`
  triggers `gate` (10), and `clarify` — which renders nothing — triggers one
  module and carries a single quota row.

Read the scan; do not just run it. It reports candidates, and a phrase like
"every element" may be prose rather than a deliverable scope. Drop the ones that
are, and say how many you dropped.

### 3. Fix the evidence tier of every claim before writing it

Four tiers, and the distinction is the point. Getting this wrong is the one
failure that makes the whole file untrustworthy.

| Tag | Means | Where it comes from |
|---|---|---|
| `[docs]` | Google published this | `references/gemini-corpus.md`, quoted verbatim |
| `[measured-family]` | observed on a Gemini run of *another* skill | `references/evidence.md` |
| `[measured-here]` | observed on a Gemini run of *this* skill | a transcript you have read |
| `[derived]` | your reasoning from the two above | you, and say so |

**A measured run is never required to write this file.** Most targets will have
none, and a `[docs]`-only `gemini.md` grounded in Google's own guidance is
useful and honest. What is forbidden is presenting one tier as another.

Every file carries an epistemic-status block near the top: which tiers it
actually uses, `n=` for anything measured, and an **unmeasured on this skill**
list naming the distinctive rules that have only family or docs backing. That
list is never empty on a first pass.

### 4. Write the file: core, then only the triggered modules

The core goes in every `gemini.md`; the modules are chosen by step 2. Both
catalogues, with the content and the citation for each:
`references/modules.md`.

**Core** — the quota ledger as an artifact · verification asked for, with claims
carrying their command · the retry ceiling (two attempts; a permanent error gets
one) · passes rather than one overloaded sweep · one worked example before the
set · `thinking_level` · recall is not a source · the epistemic-status block.

**Modules** — `visual` · `gate` · `states` · `platform-values` · `authorship` ·
`delegation` · `injection` · `count-contract` · `emphasis`.

Three rules that keep the file specific rather than generic:

- **Quote the target skill's own sentences back to it.** The strongest override
  names the line it lands on: *"Build mode step 4 already says it — six states,
  named, with an explicit completeness condition. The run delivered one."* A file
  that never cites its target could have been written about any skill.
- **Say what transferred intact.** Every skill has rules that work fine on
  Gemini, and naming them is what stops the file reading as a list of
  complaints — and stops a reader spending effort where there is no gap.
- **Hand over a filled block, not a description of one.** **[docs]** *"We
  recommend to always include few-shot examples in your prompts … you can remove
  instructions from your prompt if your examples are clear enough in showing the
  task at hand."* Every override that asks for a table, ledger or note ships one
  filled in.

Length: 150–250 lines. Long enough to be specific, short enough to be read in one
pass before the skill.

### 5. Gate it

```bash
python3 scripts/verify_quotes.py <target>/gemini.md \
    --corpus references/gemini-corpus.md --corpus <target>/SKILL.md
```

Exit 0 required. It pulls every quoted span out of `[docs]` paragraphs and
requires each to appear verbatim in a corpus, folding the things honest citation
legitimately varies — smart quotes, markdown, line wrapping, nested quote style,
`[s]` alterations, elisions, and a quote that ends early on a full stop.

It exists because of a specific mistake. While hand-authoring the first five of
these files, the sentence *"Verification is prompted rather than automatic"* was
put in quotation marks and attributed to Google in three separate files. Google
never wrote it. It is a fair paraphrase, promoted to a citation by the quote
marks, and no amount of re-reading caught it. On its first real run the same
script also caught a vendor clause quoted with three words missing.

**The quoting convention that makes this checkable:** inside a `[docs]`
paragraph, double quotes mean vendor text and nothing else. Your own prescribed
wording, the target skill's words, and anything the measured run produced go in
backticks, or in a paragraph tagged with their own tier.

Then read the report rather than the exit code alone. `0 presented as [docs]
claims` is not a pass — it means the file cites nothing.

### 6. Install the pointer and bump

```bash
python3 scripts/install_pointer.py <target>/SKILL.md \
    --before "## <first substantive heading>" \
    --summary "<one sentence naming what this file changes>"
```

Idempotent, and it does the three edits that are easy to do inconsistently by
hand: the pointer above a real heading near the top, `plugin.json`, and the
`marketplace.json` entry that pins the version separately — an unsynced bump
publishes the old copy.

The summary is the whole reason anyone reads the file, so make it specific to
this skill. A generic pointer gets skipped.

**One target, one file.** When a plugin is mirrored across marketplaces, write
the canonical copy and say which mirror you left alone; duplicating creates drift
that nothing checks.

## What not to do

- **Never fabricate a `[measured]` claim,** and never quote a paraphrase. Both
  are the failure this skill exists to prevent, and both read exactly like the
  real thing.
- **Never write the file without reading the target.** The scan is an instrument,
  not a substitute.
- **Do not rewrite the skill.** If the skill is wrong for every model, that is
  `improve-skill`'s job, and mixing the two produces a change nobody can review.
  Mention it in a sentence and stay in scope.
- **Do not add emphasis.** **[docs]** *"Remove language outside of the core task
  from the prompt that attempts to influence performance using emotional appeals,
  flattery, or artificial pressure … foundation model performance will no longer
  improve and in many cases will get worse."* If the target skill shouts, say so
  in the `emphasis` module and read it as a plain rule; do not shout back.
- **Do not claim a module you skipped was inapplicable** without saying which and
  why. The scan's output is the record of what you chose not to write.

## References

- `references/gemini-corpus.md` — Google's own words, verbatim, grouped by the
  module that uses them. Quote from here; `verify_quotes.py` checks against it.
  The full fifteen-source material lives in the `gemini-prompt-engineering` skill.
- `references/modules.md` — the core sections and the module catalogue: what each
  one says, its trigger, and the citation behind it.
- `references/evidence.md` — the measured run in full, what it does and does not
  establish, and the two out-of-family consults behind this skill's own design.
