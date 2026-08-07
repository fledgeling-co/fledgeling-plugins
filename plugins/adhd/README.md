# adhd

Parallel divergent ideation for coding agents; an evidence-grounded successor to [uditakhourii/adhd](https://github.com/uditakhourii/adhd).

## At a glance vs the original

| | Original | This version |
|---|---|---|
| Core loop | Isolated parallel frames, then converge | Same; kept deliberately, the research backs it |
| Obvious answers | Banned by phrase | Written down, frozen, and used as the bar to beat |
| Recommendation | Highest weighted score | Must beat the baseline blind on your stated ask, or the baseline is recommended |
| Frames | 15-row static table, picked by tag | Five-seat portfolio with a fit floor and apoptosis; your explicit frame requests always run |
| Scoring | 1-10 novelty/viability/fit | Pass/fail floors + mechanism clustering; no numeric scores (they're measurably unreliable) |
| First steps | "First concrete step" | Same-week starter naming the problem's actual tools |
| Cost control | Run or abort | `--any` / standard / `--100` tiers, receipt line on every run |
| Structural evals | none shipped | 96.4% vs 49.0% for the original on identical prompts |
| Blind panel (4 model families, no skill access) | none shipped | v2 sweeps the evals its engineering targets (4-0 twice, 3-1 once); its one unanimous loss was fixed and re-judged, flipping unanimously to v2.1; two evals deadlocked 2-2 |
| Typical run time | ~198s | ~355s; the gate and differentiation passes are where it goes |

## Why this exists

Ask a model an open-ended design question and you get the answer a senior engineer gives in thirty seconds. Correct, forgettable, and the same every time. This isn't a vibe; it's measured. When researchers over-sampled 4,000 ideas from one aligned model, roughly 95% were semantic duplicates. Nine independent ChatGPT users once produced the identical product name. Raising temperature doesn't fix it, and neither does asking the model to "be creative"; the homogenisation comes from preference training itself, so the fix has to live in the harness.

The original adhd skill was, in my opinion, the right harness: isolated parallel branches under different cognitive frames, a strict generator/critic split, then converge with a real opinion. Full credit to Udit Akhouri and the contributors on the original project; the two-phase loop, the isolation invariant, and the habit of actually benchmarking the skill against baselines all come from them, and all three survive here because the 2024-2026 research backs them. If you want the original, it lives at the link above and installs in one line.

This version exists because using the original surfaced two failure modes worth engineering away, and because a five-backend deep-research pass over the ideation literature turned up mechanisms the original couldn't have known about. Every structural change below traces to a measured result or a documented failure; the citations live in `skills/adhd/references/evidence.md`, and the raw research reports ship in `docs/deep-research/`.

## What's different from the original, and why

- **A frozen textbook baseline, used twice.** The original banned "the first three obvious answers" as a phrase; a model evades a phrase-level ban by rewording the same mechanism. v2 writes the pragmatic answer down first, hands it to every branch as a concrete thing to differ from (in cause, intervention point, or assumption), then makes the final shortlist beat it head-to-head, blind and order-swapped, on your stated problem. If nothing beats it, the skill says so and recommends the baseline. The original lost exactly one benchmark problem, and it lost it by starring a creative pick that didn't solve the stated problem; this gate is the structural fix.
- **A frame portfolio instead of a static table.** The original picked 5 frames from 15 rows by tag, so a child persona could land on a memory-allocator problem (we watched it happen). v2 fills five seats: an ordinary occupational stakeholder (research finding: ordinary personas partition knowledge better than exotic ones), an operational constraint, an adversary, a cross-domain mechanism that must name its mechanism and where the analogy breaks, and one wild seat that is deliberately exempt from fit-checking. Frames pass a fit floor before spawning, and a frame whose whole yield fails the quality floors is dropped from the output with a note in the receipt. Judge the output, never the persona.
- **Convergence by mechanism, not by score.** The original scored ideas 1-10 on novelty/viability/fit and ranked by weighted average. The judge-bias literature is brutal about this: direct scores collapse toward the middle, LLM judges don't model the novelty-feasibility trade-off humans make, and judged novelty *anti-correlates* with ideas that survive execution. v2 gates instead (soundness, feasibility, fit as pass/fail with written justification), merges ideas that share a mechanism, takes at most one winner per cluster, and compares pairwise with order swapping when ranking matters.
- **Generate-then-differentiate inside every branch.** The best-measured prompt lever in the literature (pooled similarity dropped to near human-group levels in the study that tested 35 strategies) is a second pass: "make them bolder and more different; no two the same". Every branch runs it.
- **Tiers and a receipt.** `--any` (2 frames, 3-4 agent calls), standard (5 frames, 8-14), `--100` (7 frames plus a hybridisation pass). Every run stamps one line stating what ran, what got merged, floored, or dropped, and the baseline verdict, so a light run reads as a deliberate choice and a weird one is diagnosable.
- **What we kept, on purpose.** Strict isolation during divergence (sharing ideas mid-flight measurably homogenises the pool; the two intuitive versions of it made diversity *worse* in controlled tests), the two-phase generator/critic split, and the output shape that converges with a named recommendation.

Note: the new machinery costs real time. Standard runs averaged ~355s against ~198s for the original in our benchmark; the boss gate and differentiation passes are where it goes. That trade is deliberate.

## The evals, and how they were judged

Two layers, both in `evals/`, both designed so nobody has to eyeball transcripts.

**Structural assertions** (`evals.json`, 7 problems; results in `EVALS.md`). Each eval asserts artifacts a correct run must produce: a labelled baseline, verdict chips, one-idea-per-cluster shortlists, a receipt, apoptosis accounting, traps that cite the requirement they break. An independent grading agent reads each output and passes or fails each assertion with quoted evidence. We deliberately assert artifacts rather than quality scores, because the research says LLM quality scores are the unreliable part. Result: v2 passed 31/32 (96.4%) vs the original's 15/32 (49.0%) on identical prompts in the same harness. The one v2 failure (a trap flag citing a generic downside instead of the conflicted requirement) became a rule in `references/convergence.md` the same day.

**A blind quality panel** (`evals/blind-panel/`). Both versions' outputs for each problem were anonymised as Option A/B in seeded-random order, and judged by four model families with no access to the skill files, so no judge knew which output came from which version or what either was supposed to look like: a Claude-family judge in strict isolation, grok-4.5 at high effort, composer-2.5, and gpt-5.6-sol at max reasoning effort over the OpenAI API ($2.89 for all seven judgments, token receipts committed). Multi-family blind panels are themselves an evidence-backed choice; single LLM judges disagree with each other often, and ours disagreed outright on 4 of 7 problems. The panel's verdict is more honest than flattering: v2 swept the problems its engineering targets, the original won on toolchain-native first steps until that became a rule and the re-judge flipped unanimously, and one judge caught a winning idea overclaiming its crash-safety guarantees, which is now a soundness rule too. Per-eval verdicts, the un-blinding map, and the raw judge reasoning are all in the repo.

## Using it

Run `/adhd <your problem>` on architecture decisions, API surfaces, naming, positioning, or fuzzy bugs with no known root cause. Closed phrasing ("quick", "standard", "just") routes to a direct answer without the run; that's tested. `--any` for cheap, `--100` for exhaustive.

## Files

- `skills/adhd/SKILL.md`: the loop.
- `skills/adhd/references/evidence.md`: the research grounding, with citations.
- `skills/adhd/references/frames.md` and `convergence.md`: frame seats, fit floor, apoptosis; floors, judge-bias defences, the boss gate.
- `evals/`: assertions, results, blind-panel verdicts.
- `docs/deep-research/`: the five full research reports this was built from.

Found a run that misbehaved? The receipt line exists to make that diagnosable; open an issue with it included.
