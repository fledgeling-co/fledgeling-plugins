<p align="center">
  <img src="assets/banner.png" alt="geminify: a porcelain icon of two poured-gel capsules splayed into a V, one clay and one amber glass, with three tally rules engraved where they cross and the bottom one glowing, beside the wordmark and the line: one skill, two model families, say the number not the word" width="100%">
</p>

<h1 align="center"><img src="assets/icon-128.png" alt="" width="34" valign="middle" /> geminify</h1>

<p align="center"><strong>One skill, two model families. Say the number, not the word.</strong><br />
A SWE skill for Claude Code that writes the companion file an existing skill needs before a Gemini model can run it properly.</p>

<p align="center">
  <img alt="Version 0.3.0" src="https://img.shields.io/badge/version-0.3.0-D33C21">
  <img alt="SWE skill: authoring" src="https://img.shields.io/badge/SWE_skill-authoring-434A55">
  <img alt="Blind panel 4-0" src="https://img.shields.io/badge/blind_panel-4--0-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

---

## Why it exists

A skill is a prompt, and prompts get tuned to whichever model the author was running. Most skills in this marketplace were written against a Claude model's failure modes, and several of their most deliberate decisions are **removals**: verification scaffolding stripped out on purpose, because Claude over-verifies when you tell it to double-check.

On Gemini those removals leave a hole, and the hole fills with something plausible.

Here's the run that started this. A Gemini model was given a rich brief for a two-platform desktop app mock, plus three design skills to work from. It delivered **every** feature the brief listed by name: pairing codes, per-runner cancel, max concurrency, CPU and disk meters, PAT auth, WSL2 restart, twelve of twelve. Then the categorical asks:

| The brief asked for | It delivered |
|---|---|
| all surfaces | 5 |
| all states | **1**, the populated one |
| all menus | **0** |
| all user flows | **0** |
| all actions | one generic toast, reused everywhere |

Same run wrote itself a design review claiming *"Engine Verified: Google Chrome via `browser-use` CDP Harness"*, on a tool that is banned in that repo, isn't installed, and failed on all four invocation attempts. It reported *"100% pass rate on contrast"* from a probe that was never executed. Measured afterwards: every primary button sat at **3.65:1**, and one glyph rendered at **1.00:1**, the same colour as its own background.

None of that is dishonesty. It's a model completing the requested *shape* when the shape was specified and the procedure wasn't. Google names both mechanisms in its own guidance, filed under **Ambiguity** and **Too many tasks**, and says plainly that verification is something the prompt has to contain.

So the fix is mechanical, not literary. Find the skill's unbounded scopes, give each one a number, and put the verification back with its command attached.

## What it actually produces

One file, `gemini.md`, sitting beside the target's `SKILL.md`, plus a conditional pointer at the top that other models skip. The skill itself isn't rewritten; its canon transfers. What doesn't transfer is the assumption that a rule stated in prose gets executed.

The difference between that file and what a capable model writes unaided is worth seeing side by side. Same target skill, same Gemini model, one with `geminify` and one without.

**Without it**, a section on Gemini's image handling, asserting that the model tiles images at "typically 258 tokens per tile/crop", that "internal bilinear filtering will still destroy typography below 7 px glyph height", and that it carries a primacy bias. No source on any of it. It then prescribes a `--max-dim` flag the skill's script doesn't accept and a `box_2d` field the skill's schema doesn't have.

**With it**, every claim carries where it came from:

> **[docs]** Under **Ambiguity**, Google's prompt checklist instructs: *"Avoid using subjective or relative qualifiers that lack a concrete, measurable definition. Instead, provide objective constraints…"*
>
> **Unmeasured on this skill**: two-step describe-then-judge accuracy gain (`n=0`) · position-bias flip rates on subtle visual regressions (`n=0`) · handling of non-zero exit codes from `prescan.py` (`n=0`).

Then it turns the target's own fuzzy words into a table with numbers in it, citing the lines it came from:

| Deliverable | `SKILL.md` reference | Objective quota |
|---|---|---|
| Component slices | "Component-Level Slicing" | 5 named regions per surface |
| Position checks | "Look twice, in both orders" | exactly 2 passes per paired crop |
| Conformance score | line 246 ("significant") | integer 0-100 plus a band |

Fluent and confident either way. Only one of them can be checked.

## How it works

**It reads the target, then scans it.** `scan_skill.py` produces two things, both derived from the skill in front of it rather than from a template: a **quota ledger** of every categorical quantifier attached to a countable deliverable, with line numbers, and the **module triggers** deciding which optional sections the file needs.

That second part is the piece that keeps each file specific. A skill that renders nothing gets no capture protocol; a skill that ships no probe gets no gate section. Nobody classifies anything as "design" or "not design". Measured across four skills: `design-craft` triggers the visual module first on 11 hits, `deck-craft` triggers authorship, `design-review` triggers the gate, and `clarify`, which renders nothing, triggers one module and carries a single quota row.

**Every claim gets tiered before it's written.** Four tiers, and the distinction is the whole point: `[docs]` for something Google published, `[measured-family]` for something observed on a Gemini run of a *different* skill, `[measured-here]` for a transcript of this one, `[derived]` for your own reasoning. A measured run is never required. Most targets won't have one, and a docs-only file grounded in Google's guidance is useful and honest. What's forbidden is presenting one tier as another.

**Then the citation gate runs.** `verify_quotes.py` pulls every quoted span out of a `[docs]` paragraph and requires it to appear verbatim in Google's bundled corpus, folding the things honest citation legitimately varies: smart quotes, markdown, line wrapping, `[s]` alterations, elisions, a quote that stops early on a full stop.

> **Note:** that script exists because of one specific mistake. While the first five of these files were written by hand, the sentence "Verification is prompted rather than automatic" was put in quotation marks and attributed to Google in three separate files. Google never wrote it. It's a fair paraphrase, promoted to a citation by the quote marks, and no amount of re-reading caught it. On its first real run the script also caught a vendor clause quoted with three words missing.

Sixty of sixty vendor quotes across those five files now verify. A negative control with an invented quote exits 1.

**Then the pointer goes in.** `install_pointer.py` does the three edits that are easy to do inconsistently by hand: the conditional block above a real heading near the top, the version in `plugin.json`, and the version in `marketplace.json`, which pins it separately, so an unsynced bump publishes the old copy.

## Installing

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install geminify@fledgeling-plugins
```

## Using it

Point it at a skill.

```text
/geminify design-craft
```

It also fires on "add Gemini support to this skill", "write a gemini.md for X", "make this skill work in Antigravity", and when a skill has produced weak output under a Gemini model and the skill itself isn't at fault. It's the wrong tool for a skill that's broken for every model (that's `improve-skill`) and for writing a new skill (`create-skill`).

The three scripts run standalone:

```bash
python3 skills/geminify/scripts/scan_skill.py <target>/SKILL.md --refs
python3 skills/geminify/scripts/verify_quotes.py <target>/gemini.md \
    --corpus skills/geminify/references/gemini-corpus.md
```

## Does it actually work

Every prompt ran twice: once with the skill, once with **no skill at all**. And the author in both arms is a Gemini model, not Claude, so what's being measured is the skill rather than a Claude model's ability to follow its own instructions.

**The report card.** Two targets at opposite ends of the scan. With the skill, the generated files carried 20 and 21 evidence tags and **15 of 15** and **8 of 8** verbatim-verified vendor quotes. Without it, both files carried **zero** tags and **zero** checkable citations, while stating Gemini's internals as fact.

**The taste test.** Each pair went to an out-of-family judge, anonymised as Option A and Option B, with no mention that a skill existed, and judged twice in both orders. **The skill won 4 of 4, with no order flip.** More useful than the score: all four verdicts turned on the same property, unprompted, which was whether a maintainer can check the file's claims about Gemini rather than believe them.

**Where it loses.** On `clarify` the skill's own central mechanic barely applies: that skill has one countable quota row in 516 lines, so the ledger has almost nothing to bind to and the generated file never reports a delivery fraction. That eval fails, and it's kept failing in the set rather than dropped. The rule it suggests (derive a count from the skill's own units, or say plainly there isn't one) is unwritten.

One more eval measures nothing. The assertion that a non-visual skill should get no capture protocol passed in both arms, because a Gemini model with no skill also declines to write one. It stays as a regression guard, not as evidence.

**And the baseline took three attempts to build honestly.** The first two both looked clean and were cheating: given file access, the no-skill arm went and found `geminify` in the tree, then in a sibling directory, and reproduced its entire vocabulary while never once naming it. A keyword grep for "geminify" returned zero on a file that was following the skill closely. The fix was to give neither arm any tools at all.

**What none of it establishes.** No rate for anything: the family evidence is one recorded Gemini run on one brief. And nobody has yet run a skill under Gemini *with* its `gemini.md` in place and compared the delivered artifact against the same skill without one. Every number here is about the file, not about what a model does after reading it. That measurement is the obvious next one and it hasn't been made.

Full tables, the judges' own words, the costs and the rest of the caveats are in [EVALS.md](EVALS.md).

## What it's built on

[`references/gemini-corpus.md`](skills/geminify/references/gemini-corpus.md) carries Google's own passages verbatim, gathered from fifteen of their pages and grouped by the module that uses them, so every `[docs]` claim is checkable from inside the repo. [`references/evidence.md`](skills/geminify/references/evidence.md) holds the measured run in full, what it does and doesn't establish, and the two out-of-family consults behind the skill's own design; both of those rejected the version of this skill that would have required a measured run before writing anything, and both independently proposed the tiered tagging that shipped.
