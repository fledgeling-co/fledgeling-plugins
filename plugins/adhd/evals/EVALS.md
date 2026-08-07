# adhd v2 — eval results

Run: 2026-08-07 · iteration 1 · grader: independent subagent, structural assertions only (no LLM 1-10 scores, consistent with the skill's own scoring philosophy).

**Headline:** new skill 15/15 assertions (100%) vs predecessor 8/15 (61.1%) on the same prompts. Mean wall clock 355s vs 198s — the boss gate, differentiation pass, and receipt cost real time; that trade is deliberate.

## Per-eval results

| Eval | What it targets | New skill | Old skill |
|---|---|---|---|
| 1 reliability-boss-gate | The predecessor's historic benchmark loss: a creative pick that doesn't solve the stated problem | 6/6 | 1/6 |
| 2 technical-frame-fit | Unfit personas rendered beside technical output (the 10-year-old-frame field report); mechanism-distinct shortlists | 6/6 | 4/6 |
| 5 closed-phrasing-aborts | Pre-flight router: closed phrasing gets a direct answer, no run | 3/3 | 3/3 |

## Notable observations

- On eval 1 the old skill reproduced its historic failure exactly: its ★ pick (a Ctrl-C save-state mechanic) treats the *wait*, not the *hang*. The new skill's boss gate produced verdict chips (two BEATS, one TIES) and a ★ pick that addresses the hang itself.
- Old-skill failures were the expected structural absences: no labeled baseline, no verdicts, no tier receipt, no apoptosis accounting.
- Eval 5 does not discriminate new-vs-old (both abort correctly); it guards the router against regression.
- Eval 2's "no child persona" assertion passed vacuously in both runs — neither run spawned an unfit frame on this prompt. A future adversarial prompt that tempts a whimsical frame onto a technical problem would make it discriminating.

## Eval set

`evals.json` holds 6 evals; 1, 2 and 5 are the core iteration set run above. 3 (shortlist mechanism diversity on the monolith-split problem), 4 (naming run), and 6 (any% tier receipt + upgrade path) widen coverage for full benchmark runs.

All assertions are structural properties of the rendered output — checkable by reading the response. This is intentional: the research this skill is built on (see `../skills/adhd/references/evidence.md` §5) shows LLM-judged quality scores collapse toward the middle and don't track expert judgment, so the evals assert *artifacts* (baseline present, verdicts present, one-per-cluster shortlists, receipts, apoptosis notes) rather than scores.

Full run outputs, grading, and benchmark.json for iteration 1 live in the session workspace (scratchpad, not committed); re-run via the skill-creator loop with `old_skill` pointed at a snapshot of github.com/uditakhourii/adhd.
