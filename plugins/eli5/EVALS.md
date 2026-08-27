# EVALS

The full scorecard behind the claims in [README.md](README.md), including the eval this
version lost, why it lost, and what happened when the fault was fixed.

**These numbers are from the 0.1.0 comparison and are left as recorded.** The gate they were
graded by had 20 checks in four families; 0.2.0's has 29 in five, and it fails all six
artifacts in this document on the composition rules it did not then have. Re-running the
current linter against these files will not reproduce the table below, which is the point of
dating it rather than editing it.

## The setup

Six topics, chosen because each has a mechanism people reliably get wrong: Raft consensus,
what happens when you type a URL, Diffie-Hellman key exchange, virtual memory and page
tables, transformer self-attention, quantum superposition.

Both skills ran all six, as background agents on Claude Opus 5 at high effort, in separate
directories with no git access. Same prompts, same model, same machine.

Two layers of scoring, deliberately different in kind. Neither substitutes for the other,
and the first one has a bias the second one exists to correct.

---

## Layer 1: the deterministic gate

Twenty checks across containment, geometry, interaction and pedagogy. Both arms were graded
by the same script.

**Read this bias before the numbers.** The gate encodes the rebuilt skill's own
specification, so it measures conformance to that spec, not quality in the abstract. The
original was never trying to pass most of these. Layer 2 is the neutral half.

| Check | original | eli5 |
|---|---|---|
| No external assets | 6/6 | 6/6 |
| No runtime network calls | 6/6 | 6/6 |
| Images inline only | 6/6 | 6/6 |
| SVG present | 6/6 | 6/6 |
| SVG carries a viewBox | 5/6 | 6/6 |
| No hardcoded pixel dimensions | 5/6 | 6/6 |
| Interactive controls, wired | 0/6 | 5/6 |
| Pointer capture on drags | 0/6 | 5/6 |
| touch-action set | 0/6 | 5/6 |
| Animation frames cancelled | 0/6 | 2/6 |
| Motion is steppable | 3/6 | 5/6 |
| Theme aware | 0/6 | 6/6 |
| **Analogy boundary stated** | **0/6** | **6/6** |
| **Boundary reachable by tier 2** | **0/6** | **6/6** |
| **Prediction beat present** | **0/6** | **6/6** |
| Register (no talking down) | 3/6 | 6/6 |
| Disclosure tiers | 1/6 | 6/6 |
| Skip-ahead for experts | 0/6 | 6/6 |
| Emoji within budget | 4/6 | 6/6 |
| **Total failures** | **29** | **1** |

### The gate found a defect in itself first

The register check originally passed all six baseline artifacts. Reading them rather than
the score turned up `"Grown-up word: DNS"`, `"grown-ups call the boss the leader"`,
`"the magic rule"`, `"it gets the crown"`, `"a little timer goes ding"`, in four of six.

The rule could fail; a fixture proved it. It simply never fired on the failure actually
present. That is a finding about the evals, not a pass, so the lexicon was rebuilt from
those measured markers and now fires on 3 of 6.

**Provenance caveat that matters:** the lexicon was strengthened *after* seeing baseline
output, which means it is fitted to observed data. Two things keep it honest. The candidate
arm was already running against the weaker version, so no candidate pass on register is the
linter's doing. And the blind panel never sees the linter at all.

The gate's `--self-test` proves all 19 rules can fail against broken fixtures before any
pass is credited. It earned that on its first run by catching a trailing `\b` in the
network-call regex which made `fetch(` unmatchable: a rule that could never have fired,
reporting green.

---

## Layer 2: the blind panel

For each eval, both pages became Option A and Option B in **seeded-random order**
(seed 20260826, map in `evals/unblinding-map.json`, written before any judging). Judges saw
only the two artifacts and the original request. They never saw either skill, the linter,
or any indication that a comparison between versions was happening. Bundle contents were
fenced as data with an explicit injection guard.

Three judge families, none of them the builder's:

| Judge | Family | Harness | Returned |
|---|---|---|---|
| gpt-5.6-sol | OpenAI | `codex exec`, reasoning high | 6/6 |
| gemini-3.7-flash-high | Google | `agy --new-project` from a neutral cwd | 6/6 |
| grok-4.6 | xAI | `cursor-agent -p --force` | 6/6 |
| fable-5 | **Anthropic, same family as the builder** | `claude -p` | 6/6 |

### Result: 17 of 18

| eval | codex | agy | grok | fable † |
|---|---|---|---|---|
| Raft consensus | eli5 | eli5 | eli5 | eli5 |
| URL to rendered page | eli5 | eli5 | eli5 | eli5 |
| Diffie-Hellman | eli5 | eli5 | eli5 | eli5 |
| Virtual memory | **original** | eli5 | eli5 | eli5 |
| Transformer attention | eli5 | eli5 | eli5 | eli5 |
| Quantum superposition | eli5 | eli5 | eli5 | eli5 |

† fable-5 is the same model family as the builder. It is reported for completeness and
**excluded from every count**, because a family grading its own output is not an
independent check. It was added only because the xAI lane was flaky mid-run and a
two-judge panel has no majority. It agreed with the out-of-family lanes on all six.

Per dimension, across the three out-of-family lanes:

| Dimension | eli5 | original | tie |
|---|---|---|---|
| Honesty about limits | **14** | 0 | 0 |
| Register | **14** | 0 | 0 |
| Conceptual clarity | 13 | 1 | 0 |
| Visual craft | 13 | 1 | 0 |
| Engagement depth | 13 | 0 | 1 |

The two clean sweeps are the two rules with the strongest research convergence behind them:
the analogy boundary, which all four research backends agreed on, and the register.

---

## The eval it lost, which is the most useful result here

`codex` gave **virtual memory to the original**, and its reasoning was better than the
gate's:

It scored **engagement depth a tie** and **visual craft to the original**, on this evidence:

> B says "Predict first, then run it" but its missing JavaScript leaves "Run it"
> permanently disabled and the answer hidden.

> B's corresponding `<svg ...></svg>` elements contain no rendered marks.

(Both clauses verbatim from `evals/verdicts/eval-4-virtual-memory.codex.md`. The judge's own
dimension labels used em dashes as separators; the clauses above are its words, unedited.)

That artifact shipped **25 controls and zero JavaScript**: no listeners, no inline
handlers, no `:checked` CSS. Tabs that did not switch. A prediction button permanently
inert. Empty SVG elements. It looks finished at 38KB and does nothing.

Two instruments reached the same conclusion independently. The gate failed it on
`interactive-controls`; a blind judge from another company, which never saw the gate,
diagnosed the same fault and found more of it. The judge still gave the rebuild **honesty
about limits** and **register** on that page, and it still lost, because a page that
invites an action and does nothing is worse than an honestly static one. The reader blames
themselves.

The failure was the runner shipping without reaching exit 0, not the gate missing it. It
became a rule in the skill the same day: *never ship a dead control; if the gate fails on
`interactive-controls`, wire them or delete them.*

### Fixed, then re-judged blind: unanimous flip

The topic was re-run through the skill with the gate enforced and the new dead-control rule
in place. The artifact now passes at exit 0: **16 event listeners** against zero, one script
tag against none, and three SVGs carrying drawn marks against three empty ones.

Re-judged blind on a fresh seed (20260827), same three out-of-family judges, no judge told
that anything had changed or that a previous round existed:

| Judge | first round | re-judge |
|---|---|---|
| gpt-5.6-sol (OpenAI) | original | **eli5** |
| gemini-3.7-flash-high (Google) | eli5 | eli5 |
| grok-4.6 (xAI) | eli5 | eli5 |

**3 of 3.** The out-of-family tally across both rounds becomes **18 of 18**.

codex flipped on precisely the two dimensions it had faulted. Engagement depth had been a
tie because "Run it" was inert; it now reads *"asks readers to 'Predict first' and 'Commit a
guess,' then lets them manipulate addresses, mappings, and page sizes."* Visual craft had
gone to the original over empty SVG elements; it now reads *"diagrams connect virtual pages,
per-process page tables, physical frames, swap, and address offsets into coherent
interactive models."*

**One control did not exercise.** The fresh seed happened to land on the same A/B
orientation as the first round, so position bias was not re-tested. That makes this a
cleaner single-variable test, since only the artifact changed, but it is not the
order-swapped check it was meant to be. Raw verdicts are in `evals/verdicts-reflip/`.

---

## Where the original is better

Stated plainly, because a scorecard that only shows wins convinces nobody.

| | original | eli5 |
|---|---|---|
| Visible words, median | **352** | 2,667 |
| SVG shapes drawn, median | **96** | 78 |
| Prose block size, median | 6 words | 8 words |
| Longest unbroken paragraph | **16 words** | 108 words |

The rebuild is **7.6× longer**. The original's entire thesis was "few words", and on that
measure it wins outright. It also draws more shapes per page.

The mitigation is partial and worth stating as such: prose *chunking* is comparable, so it
is not a wall of text, it is three tiers where there was one. But three tiers only pay for
themselves if a reader can stop after the first one. That became the second rule from this
run: **tier 1 now carries a 150-word budget**, and a `length-budget` check warns above
2,600 words. Progressive disclosure that front-loads nothing is a long document with
headings.

---

## Caveats

- **Six evals, one run each.** Single runs carry sampling noise. Nothing here is a
  significance claim.
- **Both arms ran on Claude Opus 5.** These results say what the *instructions* change on
  one model, not how the skills behave elsewhere.
- **Blind judges score content only.** The audit sheet, the icon, the research corpus and
  the gate itself earn nothing in Layer 2, by design.
- **Layer 1 is conformance, not quality.** See the bias note above.
- **The register lexicon is fitted to observed baseline output.** Disclosed above.
- **No trial anywhere measures learning gains from AI-generated explainers.** All four
  research backends flagged that gap. Every effect size in the skill comes from
  human-authored instructional material; it justifies a design choice and predicts nothing
  about a particular page.

## Reproducing

```bash
python3 skills/eli5/scripts/lint_explainer.py --self-test   # 19 rules proven fallible
python3 skills/eli5/scripts/lint_explainer.py <artifact>    # exit 0 required
python3 evals/tally.py                                      # un-blind and tally
```

`evals/` holds the prompts, the grading, the un-blinding map and all 24 raw judge verdicts.
