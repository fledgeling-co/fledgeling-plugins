# Evidence

Every number in this plugin traces to a row here, and every row traces to
`docs/deep-research/claims.json`. Read this before changing any figure in any skill.

The corpus behind it was a five-backend research panel on one question: whether AI models plus
automated tests can replace the human who promotes work from Done to Verified. Four backends count
as independent readers (Perplexity, Gemini, OpenAI gpt-5.6, Grok); a fifth Claude run is classified
as an adjudicator rather than a vote, because it read its siblings' exported reports off the same
filesystem. Support is therefore counted in independent registrable domains, never in how many
backends agreed. Roughly $20 of paid capacity, 22 sources.

**The panel was reused rather than re-run for this plugin.** It was commissioned for
`deputy.fledgeling.app` and covers exactly this domain, so buying a second panel on the same field
would have returned the same field. The full exports are in `docs/deep-research/`.

## What is measured, and what is reasoned

The distinction is load-bearing and the skills mark it. A claim id beginning `C` is a direct
finding from a source. One beginning `I` is an inference assembled across findings — reasoning,
not a result. One beginning `M` is an observation about the corpus itself.

## Direct findings the skills depend on

| Id | Finding | Bounded by |
|---|---|---|
| `C1` | No powered non-inferiority reader study has ever been run on code review or UI/feature acceptance | A search absence across four readers, not a proof. The largest gap, and the reason the ladder is climbed on absence of escapes |
| `C2` | Nine judges from seven families give about two effective independent votes; panel accuracy 8 to 22 percentage points below independent voting; the best single judge matches or outperforms the panel across all tested conditions; established aggregation closes at most 11% of the gap even given the correct answers | Natural-language inference and RewardBench, not UI acceptance. A preprint. Every figure checked against the abstract |
| `C3` | 27 independently developed versions of one specification failed correlatedly under about a million tests; the independence hypothesis was rejected | 1986, human-written programs. Establishes that independence must be shown, not that models correlate |
| `C5` | Two evaluators using one method on one system agree on between 5% and 65% of problems found | Usability inspection. The finer 20%/46% split is unread inside the paper and is cited at paper level only |
| `C6` | About three quarters of code-review defects are evolvability findings rather than functional ones | The lanes disagree on the range; later replications put functional findings near 7% of review-induced edits |
| `C7` | Computer-aided detection across 43 facilities and 429,345 mammograms: specificity 90.2% to 87.2%, positive predictive value 4.1% to 3.2%, biopsy rate +19.7%, curve area 0.919 to 0.871, no statistically significant sensitivity gain | Observational, not randomised. Paywalled; figures consistent across three lanes |
| `C8` | In 323,973 women, the same aid gave no accuracy improvement on any metric, and within-radiologist sensitivity was significantly lower with it, odds ratio 0.53 | Observational. The sharpest number in the corpus, and it is about placement rather than about automation |
| `C9` | The one autonomous reader a regulator cleared was scoped to one indication and one camera and required to refuse: sensitivity 87.4%, specificity 89.5%, 819 analysable cases, 38 forced referrals | Biopsy-adjacent ground truth. Software acceptance has no equivalent gold standard |
| `C10` | DO-330 Criterion 2 covers a tool whose output is not otherwise verified, and requires operational requirements, a qualification plan and re-qualification on change | The standard is paywalled; clause detail is industry restatement. It presumes deterministic tool behaviour, which a model judge lacks |
| `C11` | A 21 CFR Part 11 electronic signature must be unique to one individual | Whether Part 11 reaches an internal release control needs a legal classification this corpus cannot supply |
| `C12` | PCAOB Auditing Standard 2201 permits benchmarking a fully automated control across periods only where the auditor verifies it has not changed | Two lanes reach the clause. The inference that a reversioned model fails the predicate is ours |
| `C13` | ISO/IEC 17025 requires declared measurement uncertainty and treats an inconclusive result as valid | Paywalled. Existence confirmed, text unread |
| `C14` | 30.4% of RE-Bench runs exhibited reward hacking, and on some tasks every successful run did | Lab evaluation, self-reported by the evaluator. Three lanes, one shared source, so not three confirmations |
| `C15` | An audit found 59.4% of the SWE-bench Verified subset materially flawed; the benchmark was retired | Self-reported by the retiring lab |
| `C16` | Image-borne prompt injection against four production vision-language models: miss rates 70/57/89/92%, attack success 33/40/67/51%, 81 to 162 cases each, black-box | Oncology imaging. The transfer to tenant-authored text inside a judged screenshot is an argument, not a measurement |
| `C17` | The best published UI-display-defect detectors reach about 85% precision and 84% recall on 4,470 screenshots | Mobile app display issues, not data-dense web surfaces. About 16% missed is a ceiling before any domain shift |
| `C18` | More than half of over 15,000 generated mutants survived a passing unit, integration and system suite | One company's codebase. No rate exists for browser or end-to-end suites |
| `C19` | Proficiency-test failure rates differ more than twentyfold by denominator: 1.4% of 670,489 challenges across 665 laboratories against 32.4% of lab-parameter results across three | A genuine cross-lane disagreement whose resolution is the population. Neither figure is quotable alone |
| `C21` | No regulated software vendor was found whose all-machine verification step was accepted as the control of record | Search absence. Auditors' acceptance is often private |
| `C24` | Author-judged acceptance is how roughly half of a 110-ticket corpus shipped not-as-specified while reading as complete | An internal figure with no published method behind it |

## Inferences the skills implement

| Id | Inference | From |
|---|---|---|
| `I2` | Treat a queue as a lot under a declared risk limit: sampled, blinded, seeded, with census review of disclosure content and every ungradable verdict | `C5`, `C8`, `C19` |
| `I5` | The human sample must be blind to the machine verdict, or the audit loses the power it was added for | `C7`, `C8` |
| `I6` | Measure test integrity before anything else, because every downstream number inherits it | `C18` |
| `I7` | The highest-consequence failure is a well-rendered screen asserting an unsupported figure, and it is closable deterministically rather than by any judge | `C16`, `C17` |

## Where a claim is weaker than it reads

Four honesty notes, because a reference file that flattens these invites a later editor to treat
every row as equally solid.

**Eight of the twenty-two sources are paywalled or challenge-walled with their contents unread.**
Four were checked against the primary record this session, via Crossref or the arXiv API, and that
checking corrected an invented author affiliation, a wrong journal byline and two dead
author-hosted PDFs. Two are local artefacts parsed directly.

**`C2` is a preprint measured on a different domain.** It is the strongest argument in the plugin
against adding lanes, and its transfer to UI acceptance is an assumption. If it is wrong, the cost
is that `warrant:panel` is more frugal than it needed to be — which is the cheap direction to be
wrong in.

**`C4` was dropped.** A single-lane claim about correlated errors across more than 350 models could
not be dereferenced (the venue is challenge-walled) and a second lane self-tagged its version
UNVERIFIED. No rule here rests on it.

**`C25` is an unresolved disagreement inside the panel.** Whether design-token conformance predicts
fewer escaped visual defects is unestablished: one lane asserts the correlation and cites nothing,
two searched and found no published effect size. `warrant:oracle` therefore treats taxonomy and
token conformance as deterministic checks worth running, and makes no claim that running them
reduces escapes.
