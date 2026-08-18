# Evals

**No two-arm eval has been run, so nothing here is a measured result about the skill.** The eval suite exists now, in [`skills/mockup-fidelity/evals/evals.json`](skills/mockup-fidelity/evals/evals.json), beside the fixtures and the answer key that were already there. Not one of its eight prompts has been executed with the skill loaded, none without it, no judge has looked at anything, and there is no pass rate. That is a legitimate state to ship in, and it is written here plainly so a defined suite is not mistaken for an evaluated one.

The harness itself is a different matter. It was run, against the fixtures on disk, and what it measured is below.

## What was checked, and what it found

Everything in this section was produced on 18 Aug 2026 on this machine, with Obscura 0.2.0 and Node 22.23.1.

**The SKILL.md parses, and everything it points at exists.** Frontmatter reads as strict YAML with exactly `name` and `description`, and the name matches the plugin directory. Sixteen internal paths are cited across the file, spanning `references/` and `assets/diff/`, and all sixteen resolve. The grader compiles.

**The fixtures are a real answer key.** `evals/fixtures/target-control-identical.html` is **byte-identical** to `reference.html`, confirmed with `cmp`. `target-10-defects.html` differs by exactly the ten planted defects `grade.py` keys on, each verifiable by reading the diff: the whole watchlist card removed, a heading changed from "Editor's picks" to "Movers today", the muted colour token moved from `#9ca0ac` to `#5e6a82`, the card's `box-shadow` deleted, `padding-top` moved 16 to 24, the row's `flex-direction` moved row to column, `text-transform: uppercase` removed while the source text stayed the same, the trailing arrow `<svg>` removed from the CTA, `border-radius` moved 12 to 4, and a `linear-gradient` flattened to a solid colour.

**The harness runs, and it discriminates.**

| run | findings | high | score | exit |
|---|---|---|---|---|
| the ten-defect fixture | **49** | 26 | 83 | **3** |
| the byte-identical control | **0** | 0 | 100 | **3** |

Zero findings on a target that is byte-identical to its reference, and 49 on one that is not, is the discrimination evidence a fixture pair exists to produce.

**Eight of the ten planted defects were caught, with no false passes.** Scored by the repository's own `grade.py` against the defect run's `target.findings.json`:

| | caught | declared inconclusive | false pass |
|---|---|---|---|
| the ten planted defects | **8** | 2 | **0** |

The two it could not measure are the `box-shadow` deletion and the `text-transform` removal, and both were **declared** rather than silently graded clean, which is the whole distinction this skill is built around. The missing trailing arrow was caught, but labelled presence-only: `hasSvgChild` sees the absent child, while a wrong-size or swapped glyph would not be seen at all.

**Nine of nine probed detector classes are silenced on this engine, and that is the headline.** `summary.scoreCovers` reported `{ detectorClassesProbed: 9, ran: 0, silenced: 9, fraction: 0 }` on both runs. Each silenced class carried its own `reason` string naming the declaration set and the value that came back. Four of them, quoted from the run:

> `background-image` was set to `linear-gradient(rgb(1,2,3), rgb(4,5,6))` and getComputedStyle returned ""

> `transition` was set to `color 1s` and getComputedStyle().transitionDuration returned ""

> ::placeholder colour was set to `rgb(1,2,3)` on an input whose own colour is `rgb(8,8,8)`; getComputedStyle(input, "::placeholder").color returned "rgb(8, 8, 8)"

> A probe declared `border-top: 9px` on the element and `content:"X"; border-top: 3px` on its ::after. getComputedStyle(el, "::after") returned content "" and borderTopWidth "9px"

The consequence is worth stating in plain words. **On this engine, `capture.mjs --assert` cannot return 0.** Every probed class fails its round-trip, so every run exits 3, including the run against a target that is byte-for-byte the reference. The skill's Done criteria already anticipate this: they accept a 3 when every capability in `inconclusive[]` has a ledger row saying where it was confirmed instead. What the measurement shows is that this is not the rare path here, it is the only path, and a reader of a `mockup-fidelity` report on this setup should expect the score to arrive with `scoreCaveat` attached every single time.

That also means the score is the most dangerous number in the output. The defect fixture scored **83** while nine classes were shut. Eighty-three beside nine closed shutters reads as 83 percent right, and the run's own caveat says so in as many words.

### One thing failed

**`grade.py` could not be run as shipped, and now can.** It read `out-old/target.findings.json` and `out-new/target.findings.json` from the working directory with no argument interface and no check, so running it raised a bare `FileNotFoundError` from `json.load` several frames deep. Neither directory existed in the repository and neither ever can: a run directory is output. To get the table above, both paths were created as symlinks to the one capture available, and only the current-harness column was read. Fixed on 2026-08-19: it takes two run directories as arguments, defaulting to the old paths so any existing invocation still works, and refuses with a sentence naming the `capture.mjs --out` command that produces its inputs. The grading logic is untouched and was re-verified against synthetic runs exercising a catch, a false pass and a declared inconclusive.

**No prior run exists.** No `grading.json`, no `results/` directory, no `benchmark.json`, no committed judge log, no blind-panel key anywhere under `plugins/mockup-fidelity/`. Checked, not assumed. `grade.py` and the three fixtures are the only eval scaffolding that was here, and the file that says what to run them on is the one this commit adds.

## What the eval set would settle

Eight prompts. Each runs twice, once with the skill and once with no skill at all, because there is no predecessor and the honest question is whether the skill earns the context window it costs. What the harness measurements above cannot tell you is the interesting part: whether a model handed all of this *behaves* differently, which is where every one of this skill's rules actually lives.

Three prompts are where the answer would come from:

1. **`an-authored-justification-is-not-a-citation`.** The user offers a plausible reason why two real differences are fine, and asks for the rows closed. This is the failure the whole gate was written for, and it has already happened once: a run let "zero unexplained" stand as done while the app had dropped the mock's labelled buttons to bare icons and omitted a card, both sitting in the unpaired list, rationalised away. Grade two properties: are both rows recorded as defects, and does the phrase "app-ahead" or its cousins appear as a resolution. A baseline handed the same friendly reasoning is very likely to accept it.

2. **`inconclusive-is-read-before-findings`.** Hand both arms the real capture output measured above, score 83 with nine silenced classes, and ask for the verdict. Grade whether the verdict is inconclusive, whether the nine reason strings come back verbatim, and whether the score is quoted with its caveat. This is the cheapest eval in the set to run, because the input already exists on disk in `/tmp` and can be committed as a fixture.

3. **`a-source-read-is-not-a-measurement`.** The user offers a shared component import, a shared token file and a commit message as certification. Every input is inadmissible. Grade whether anything was certified without a render.

Grade with a subagent that never sees the skill, marking each assertion passed or failed with quoted evidence, and no 1-to-10 scores. Every assertion in the set is a property of an artifact on disk, an exit code, or a row in the ledger.

## Caveats, stated rather than buried

- **Nothing above measures the skill.** The 49 findings, the 8 of 10 and the nine silenced classes are facts about `capture.mjs`, `analyze.js` and Obscura. None of them says anything about what a model does after reading the SKILL.md, which is what the eval set is for.
- **Two fixtures, one screen, one viewport, one engine.** Both fixtures are small static HTML files rendered by Obscura 0.2.0 at the harness default. No React app, no React Native target, no Metro connection, no simulator, no real browser, and no second run to measure variance.
- **The nine silenced classes are a property of this engine, not of the skill.** In packaged Chrome the numbers above would be different, and probably better. Nobody has measured them there, so the comparison is unavailable rather than favourable.
- **The defect this file used to name is now fixed.** `grade.py` has an argument interface, a documented invocation and a refusal that says how to produce its inputs. What remains open is that no comparative run has been performed with it: the table above reads one column, because there is only one capture.
- **The eight prompts are unrun, so the set's own quality is unknown.** One assertion is labelled a control on the expectation that a capable model passes it without the skill. Which of the others discriminate is unknown, and any a baseline also passes measure the model rather than the skill and should be relabelled or dropped.
