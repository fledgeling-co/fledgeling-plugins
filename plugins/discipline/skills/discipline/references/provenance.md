# Provenance registry

Every credibility-bearing figure in this skill, with what it rests on. **The gate reads this file** —
`scripts/block-check.py` parses the table below, so a figure that appears in the prose without a row
here fails the build, and a row whose figure has drifted out of the prose fails it too.

## Two families, composed — not one list

A mark is a **pair**, written `independence+verification`. The two axes are orthogonal, and flattening
them into one list is a defect: it makes a promotion along one axis look like a promotion along the
other. Both sets are **closed**. A mark outside them is refused rather than ignored, a single mark is
incomplete rather than valid, and two marks from the same family are malformed.

**Family A — independence.** A property of *the source*. **Not improvable by reading harder.**

| Mark | Meaning |
| --- | --- |
| `first-party` | Measured by this operator, from a store that can be re-queried |
| `independent` | A third party with no stake in the result |
| `vendor-doc` | Primary vendor documentation of its own product's *behaviour* — pricing, mechanics; checkable by using the thing |
| `self-report` | A party with a stake reporting a *performance claim* about itself, unaudited |
| `anecdote` | No methodology, nothing reproducible |
| `assumed` | No source at all. Reasoning only. |

**Family B — verification.** A property of *our diligence here*. **Improvable by doing the work.**

| Mark | Meaning |
| --- | --- |
| `results-read` | Read in the source's own results section or equivalent primary text |
| `summarised` | Dereferenced, but through a summary rather than the primary text |
| `second-hand` | Taken from someone else's citation of the source, not the source |
| `unlocated` | Looked for in the source and **not found there** |
| `none` | Nothing to verify; pairs only with `assumed` |

### Promotion runs along Family B only

Reading a paper's results section moves `second-hand` → `results-read`. It **never** moves
`self-report` → `independent`. A competitor's README read with total care is still a self-report, and a
vendor's benchmark of its own feature does not become independent by being read twice. Independence is
fixed at the source; only our verification of it improves.

`caveman-readme` is why this file is shaped this way. Under the previous single flat axis it sat at
"reported-not-verified", which conflated two unrelated things — that we had not checked it, and that its
author has a stake in the number. It is now `self-report+results-read`: **fully read, permanently a
self-report.** The old scheme could not express that, and a reader fixing the "not verified" half would
have appeared licensed to promote it.

That flattening had already forced a visible workaround: the PRISM persona study was split across *two
rows*, one for its figures and one for its narrow scope, because one axis could not carry both. Scope is
now its own column and those rows are merged.

`observed` is the date the source was read, required whenever Family A is `independent`, `vendor-doc`,
`self-report` or `anecdote`. A claim about what a living document "currently says", undated, is
unfalsifiable and will become false without anyone noticing. Not hypothetical: see `caveman-readme`.

## The registry

| id | figures | provenance | scope | appears_in | observed | source |
| --- | --- | --- | --- | --- | --- | --- |
| swe-bench-caveman | 63.3; 55.7; 7.61; 7.6; 229.02; 152.34; 33.5; 126.1; 73.4; 41.8; 24.5; 16.5; 32.7; 48.6; 42.0; 13.6; 78 | first-party+results-read | Opus 5 at xhigh only. Machine-graded; two samples per (model, task). | SKILL.md; evidence.md; README.md; EVALS.md | 2026-08-10 | Benchwarmer SQLite store, `~/Dev/diolog-swe-bench`, graded by that repo's `docs/SCORING.md`. 106 paired tasks, `claude-opus-5` vs `claude-opus-5-caveman`. `7.6` is the rounded form of `7.61`, registered so the rounding cannot read as a separate finding. |
| swe-bench-tasklength | 0.68 | first-party+results-read | Split by pure-arm step count. | SKILL.md; evidence.md; README.md; EVALS.md | 2026-08-10 | Same store. 10-19 steps: 13 worse / 10 better. 20+ steps: 34 worse / 4 better. |
| register-compliance | 97.5; 98.9; 2,690; 1,979; 26; 1.19 | first-party+results-read | Transcript-scraped, not judged. | SKILL.md; evidence.md; EVALS.md | 2026-08-10 | 683 caveman and 370 pure run transcripts from the same store. |
| swe-bench-v4 | 61.6; 303.77; 32.6; 21.6; 16.3; 1.73; 4.09; 2.41; 3.43; 41.0; 12 | first-party+results-read | **One sample per task against the baseline's two — the cost figure is not on equal footing.** | SKILL.md; evidence.md; README.md; EVALS.md | 2026-08-14 | Same store, v4 block appended via `--append-system-prompt`. |
| blind-panel | 0.0115 | first-party+results-read | Three model families judging models; no human grader. | README.md; EVALS.md | 2026-08-14 | `docs/blind-panel/`, 14 pairs, withheld key. 29 baseline / 12 compressed / 1 tie. |
| effort-sweep | 4.93; 6.6; 0.0135 | first-party+results-read | Opus 5 xhigh vs medium. | SKILL.md | 2026-08-10 | Same store. 40 tasks worse, 20 better. |
| block-size | 881; 736; 1,029; 220; 150; 300; 1,200 | first-party+results-read | Byte counts; the ~220 tokens is an estimate at ~4 bytes/token. | SKILL.md; injected-block.md; EVALS.md | 2026-08-18 | Counted from the committed literals by `scripts/block-check.py`. All three verify exactly on stripped bytes. |
| jetbrains | 8.5; 65; 592; 542; 11.6; 40.60; 36.39; 8.29; 0.33; 0.82; 106; 29.5 | independent+results-read | `claude-sonnet-5` at `--effort low`, short tasks. k=1, which its authors flag. | SKILL.md; evidence.md; README.md; EVALS.md | 2026-08-18 | [JetBrains AI blog, July 2026](https://blog.jetbrains.com/ai/2026/07/speak-to-ai-agents-like-cavemen-tosave-tokens/). Re-dereferenced 18 Aug 2026; every figure read in the article's own results. SkillsBench, 86 of 87 tasks, 82 clean pairs, Claude Code 2.1.200. |
| cost-anatomy | 44.3; 35.4; 10.4; 1.3; 2,848; 38.4; 6.8; 0.154; 8.7; 6.0; 5.0; 3.3; 715; 24.7 | independent+summarised | **Haiku 4.5, Sonnet 5, Opus 4.8 — not Opus 5 at xhigh,** which is the only workload this block runs against. | SKILL.md; evidence.md; README.md | 2026-08-18 | Weinberger & Hozez, *Token Reduction Is Not Cost Reduction*, [arXiv:2607.12161](https://arxiv.org/abs/2607.12161) (v5, 12 Aug 2026). 2,848 analysed Claude Code runs, 103 tasks, 7 repos. Billed shares with 95% CIs; generated output 10.4% [10.0, 10.9]. `summarised` because it was read via fetch-and-summarise rather than the PDF — re-read the PDF before quoting a CI in anything load-bearing. |
| caveman-readme | 1.5 | self-report+results-read | Its own product, its own numbers. | SKILL.md; evidence.md | 2026-08-18 | [caveman README](https://github.com/JuliusBrussee/caveman) and `docs/HONEST-NUMBERS.md`, both read in full 18 Aug 2026. **The headline is still 65%, it does not report 8.5%, and it does not link JetBrains** — an earlier version of this skill claimed all three. `HONEST-NUMBERS.md` lists the aggregate output reduction as "Not published". The "Honest number warning" and net-negative caveat are verbatim present. Fully read; permanently a self-report. |
| prism-persona | 71.6; 68.0; 66.3; 0.65; 7; 8; 70 | independent+results-read | **Every model tested is 7-8B; the authors flag 70B+ as untested.** A sizing prior, not a law about Opus 5. | SKILL.md; evidence.md | 2026-08-10 | Hu, Rostami & Thomason (USC), [arXiv:2603.18507](https://arxiv.org/html/2603.18507v1). MMLU baseline to persona to long persona; MT-Bench Coding the largest single loss at -0.65. Read first-hand. Merged from the two rows the old flat scheme forced apart. |
| giskard-aggregate | 20 | independent+results-read | Aggregate across "most models tested". **Which models were in the brevity condition is not stated,** so Claude's inclusion is unknown and must not be asserted either way. | SKILL.md; evidence.md; injected-block.md | 2026-08-18 | [Giskard Phare](https://www.giskard.ai/knowledge/good-answers-are-not-necessarily-factual-answers-an-analysis-of-hallucination-in-leading-llms), published 30 Apr 2025, read 18 Aug 2026. Conciseness instructions "degraded factual reliability across most models tested", up to a 20-point drop in extreme cases. |
| giskard-permodel | 84; 64; 74; 63 | independent+unlocated | Registered as unlocated, not as findings. | SKILL.md; evidence.md | 2026-08-18 | The widely-repeated pairs 84→64 (Gemini 1.5 Pro) and 74→63 (GPT-4o). **Searched for in Giskard's article on 18 Aug 2026 and not found there;** two independent research passes also failed to locate them. Registered because the prose names them *as missing*. Do not restate them as Giskard's figures. |
| renze-guven | 48.70; 27.69 | independent+second-hand | GPT-3.5 / GPT-4, **not Claude**. The 27.69% is from the paper's body, not its results section. | SKILL.md; evidence.md | 2026-08-10 | Renze & Guven, [arXiv:2401.05618](https://arxiv.org/abs/2401.05618), FLLM 2024. Direction high confidence, exact magnitude unverified. |
| nayab-budgets | 2407.19825 | independent+second-hand | GPT-series. Tables not retrieved. | evidence.md | 2026-08-10 | Nayab et al., [arXiv:2407.19825](https://arxiv.org/abs/2407.19825), *Information Sciences* 2026. |
| brevity-counterevidence | 2604.00025 | independent+second-hand | **Single-author, non-peer-reviewed**, and cited by caveman in its own defence. | evidence.md | 2026-08-10 | [arXiv:2604.00025](https://arxiv.org/abs/2604.00025) claims brevity constraints *raise* accuracy on over-elaboration-prone items. Recorded because it argues against this skill. |
| tool-definitions-anthropic | 134 | vendor-doc+second-hand | A high-complexity multi-server setup **before optimisation** — not a typical one. | SKILL.md; evidence.md | 2026-08-18 | [Anthropic Engineering, advanced tool use](https://www.anthropic.com/engineering/advanced-tool-use). A primary observation of its own product's overhead. No published methodology. |
| tool-definitions-practitioner | 55 | independent+second-hand | **The GitHub MCP server alone, not "a typical multi-server setup."** The "typical" framing accreted in retelling. | SKILL.md; evidence.md | 2026-08-18 | Traced by two independent research passes on 18 Aug 2026 to a practitioner measurement of GitHub MCP's tool definitions. **Not Anthropic telemetry**, which this skill implied until that date. Split from the 134k row because they measure different things. |
| lever-hierarchy | 85; 77; 8.7; 79.5; 88.1; 37; 43,588; 27,297; 46.5; 51.2 | self-report+second-hand | Vendor-internal benchmarks of the vendor's own features, unaudited. | evidence.md | 2026-08-18 | Same two Anthropic pages. Tool Search Tool and Programmatic Tool Calling effects. `self-report` rather than `vendor-doc` because these are favourable performance claims, not documented behaviour. |
| cache-economics | 0.1 | vendor-doc+results-read | — | SKILL.md; evidence.md | 2026-08-18 | Anthropic prompt-caching documentation: cache reads bill at 0.1x base input, and the cache matches an exact byte prefix. Documented behaviour, checkable by using the API. |
| tokenizer-change | 1.35 | vendor-doc+second-hand | Reported as a range, ~1x-1.35x. | evidence.md | 2026-08-10 | Anthropic's tokenizer changed at Opus 4.7+, producing more tokens for the same text. No primary methodology read here. |
| reused-input-anecdote | 3.77; 96; 2.6 | anecdote+unlocated | — | evidence.md | 2026-08-18 | **Removed from this skill; recorded so the deletion is auditable.** "3.77B tokens through a workspace in a day, 96% reused input" — traced by two independent research passes to a practitioner writeup (Nate B. Jones / The Learning Atlas, July 2026) with no methodology, no log export, nothing reproducible. Its derived `2.6%` compounded the error by treating a `100 - 96` residual as output alone when it is new input plus output. `cost-anatomy` is the auditable replacement. |
| output-share | 14; 9 | assumed+none | Superseded by `cost-anatomy`'s measured 10.4%. | evidence.md | — | **Retained because the argument's history matters.** This skill assumed output was ~14% of a cache-warm session with nothing behind it, giving a notional ~9% ceiling. The measured figure is 10.4%, so the assumption was close and slightly generous. May appear only inside an honesty or limits section; the gate enforces it. |
| perch-enrollment | 0 | first-party+results-read | A configuration fact, not a result. | SKILL.md | 2026-08-14 | PERCH-0333 ships a three-arm experiment enrolled at 0% by default. |

## What this registry cannot do

It checks that a figure is marked, that both marks are real and drawn from different families, that an
`assumed` figure stays inside an honesty section, that a living source carries a read date, and that the
registry has not drifted out of the prose. Coverage is enforced on `SKILL.md`; figures appearing only in
`README.md` or `EVALS.md` are registered by convention rather than by gate.

It cannot check that a mark is *correct* — that a row claiming `results-read` was genuinely read.
`caveman-readme` is the worked example: it sat at the verified end across four files for about a week,
and one fetch moved it. So the operation that keeps this honest is re-reading the living sources on a
cadence and moving the `observed` date. The gate's job is narrower and worth having anyway: it makes an
undated claim, an unmarked figure, and a silent promotion across families impossible to ship.
