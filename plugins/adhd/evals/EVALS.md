# adhd v2 — eval results

Run: 2026-08-07 · iteration 1, full 7-eval set · grader: independent subagent, structural assertions only (no LLM 1-10 scores, consistent with the skill's own scoring philosophy).

**Headline:** new skill **31/32 assertions (96.4%)** vs predecessor **15/32 (49.0%)** on the same prompts, same subagent harness. Mean wall clock is higher for the new skill (roughly 355s vs 198s on the heavy evals); the boss gate, differentiation pass, and receipt cost real time, and that trade is deliberate.

## Per-eval results

| Eval | What it targets | New skill | Old skill |
|---|---|---|---|
| 1 reliability-boss-gate | The predecessor's historic benchmark loss: a creative pick that doesn't solve the stated problem | 6/6 | 1/6 |
| 2 technical-frame-fit | Unfit personas rendered beside technical output (the 10-year-old-frame field report); mechanism-distinct shortlists | 6/6 | 4/6 |
| 3 shortlist-mechanism-diversity | One-elite-per-cluster shortlists on a wide decomposition problem | 5/5 | 3/5 |
| 4 naming-run | Clustered naming, traps citing requirement conflicts, baseline comparison | 3/4 | 1/4 |
| 5 closed-phrasing-aborts | Pre-flight router: closed phrasing gets a direct answer, no run | 3/3 | 3/3 |
| 6 any-percent-tier | Light tier is visibly deliberate: 2 frames, receipt, upgrade path, still converges | 4/4 | 1/4 |
| 7 adversarial-frame-fit | "Be adventurous with your frames" on a hard technical problem must not degrade output | 4/4 | 2/4 |

## Notable observations

- On eval 1 the old skill reproduced its historic failure exactly: its ★ pick (a Ctrl-C save-state mechanic) treats the *wait*, not the *hang*. The new skill's boss gate produced verdict chips (two BEATS, one TIES) and a ★ pick that addresses the hang itself.
- On eval 3 the old skill's shortlist double-dipped one cluster (two variants of the same seam-census mechanism); the new skill's one-elite-per-cluster rule held.
- On eval 7 the new-skill run lost two branch agents mid-flight and recovered exactly as designed: converged on the surviving branches and recorded both dead branches in the receipt. Degraded-mode behaviour got exercised for real, unplanned.
- The single new-skill failure (eval 4): one of three trap flags cited a generic downside (procurement/security connotation) instead of naming which stated requirement the name conflicts with. `references/convergence.md` now requires trap mechanisms to connect to the stated requirements.
- Old-skill failures are dominated by absent v2 artifacts (no baseline label, no verdicts, no tier receipt, no apoptosis accounting) plus the two substantive misses above — which is the point of the comparison.
- Evals that pass for both variants (5, and eval 7's conditional apoptosis assertion when no frame floors out) are regression guards, not discriminators.

## Blind quality panel (no human review)

Separate from the structural assertions: each eval's two outputs were anonymised (seeded-random A/B per eval), and judged blind by two independent families — **Cursor composer-2.5** (non-Anthropic) and a **Fable subagent with no access to the skill files** — on breadth, novelty, trap detection, actionability, and builder usefulness. Neither judge knew which output came from which version. Raw un-blinded verdicts: `blind-panel/panel-results.json`. A third leg (Codex gpt-5.6-sol, xhigh) is deferred to its usage-limit reset.

| Eval | composer-2.5 | Fable (blind) |
|---|---|---|
| 1 reliability-boss-gate | OLD | NEW |
| 2 technical-frame-fit | NEW | NEW |
| 3 shortlist-mechanism-diversity | OLD | OLD |
| 4 naming-run | OLD | NEW |
| 5 closed-phrasing-aborts | OLD | TIE |
| 6 any-percent-tier | NEW | NEW |
| 7 adversarial-frame-fit | NEW | NEW |

Overall: composer 3 NEW / 4 OLD; Fable 5 NEW / 1 OLD / 1 TIE. Judges disagreed on 3 of 7 — consistent with the measured unreliability of single LLM judges that motivated the panel design.

Pooled per-dimension: NEW wins trap detection 8-4 and breadth 7-4; OLD wins actionability 6-3; novelty and builder usefulness split. The signal is coherent across both judges' prose: the new skill's exploration and trap analysis are stronger, but blind judges reward first steps phrased in the problem's *native toolchain* (eval 3's unanimous OLD verdict praised packwerk / ActiveSupport::Notifications-specific starts over generic instrumentation language). The FOCUS deepen instruction now requires toolchain-native first steps as a direct fix; re-run the panel after the next iteration to see whether the actionability gap closes.

Two honest caveats: single runs per variant per eval, so per-eval verdicts carry sampling noise (eval 5 compares two near-identical direct answers — composer's OLD pick there is noise, Fable's TIE is the sensible read); and blind judges score only content value, so v2's audit artifacts (receipts, verdicts) earn nothing here by design — the structural assertions cover those.

## Eval set

`evals.json` holds 7 evals, all run above. All assertions are structural properties of the rendered output — checkable by reading the response. This is intentional: the research this skill is built on (see `../skills/adhd/references/evidence.md` §5) shows LLM-judged quality scores collapse toward the middle and don't track expert judgment, so the evals assert *artifacts* (baseline present, verdicts present, one-per-cluster shortlists, receipts, apoptosis notes) rather than scores.

Full run outputs, grading, and benchmark.json for iteration 1 live in the session workspace (scratchpad, not committed); re-run via the skill-creator loop with `old_skill` pointed at a snapshot of github.com/uditakhourii/adhd.
