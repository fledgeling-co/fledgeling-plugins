Case 1: WINNER=A · REASON=A catches the real blockers (missing provenance, unpaired non-IFRS measure under Reg G, generic filename) while B passes a regulated deck that has actual disclosure defects.

Case 2: WINNER=B · REASON=B flags all seventeen sub-floor text elements with the reason and the standard behind the 24px floor; A silently passes a deck that is unreadable from row four.

Case 3: WINNER=B · REASON=B catches both truncated baselines and states the denominator ("2 of 2 charts checked"), where A reports a clean pass on two misleading charts.

Case 4: WINNER=A · REASON=A refuses to call a zero denominator a pass and tells the operator how to fix the selector, whereas B prints "PASS · 0 blockers across 0 slides" for a run that examined nothing.

Case 5: WINNER=A · REASON=On a genuinely clean deck both correctly pass, but A discloses its chart coverage ("1 judged, 0 not zero-based, 0 groups unverified") and the gated geometry, which is what makes the pass trustworthy; the one extra non-gating warning is a small price.

Case 6: WINNER=A · REASON=Both correctly deny a pass, but A includes the underlying navigation error, so the operator knows it was a connection failure rather than a tool bug.

Case 7: WINNER=B · REASON=B surfaces the thrown check as its own NOT RUN section and gates on it; A reports a pass while one check never ran, which is the exact null-reads-as-zero failure the gate exists to prevent.

OVERALL: A · The winning output in every case is the same variant — it appears as A in cases 1, 4, 5 and 6 and as B in cases 2, 3 and 7 — so the letter tally (4–3) understates how one-sided this is. What separated them was refusal to launder absence as absence-of-defect: the winner distinguishes "examined and clean" from "never examined" and "threw mid-run", carries denominators on the checks it can count, and attaches a consequence and a cited standard to each finding instead of a bare counter. The loser's leanness came entirely from omitting things a reader needs, not from ranking better; its only defensible moment is Case 5, where its brevity is merely less informative rather than wrong.

WORST FAILURE: Case 4, Option B — printing "[DECK-PREFLIGHT PASS] 0 blockers across 0 slides examined" on a regulated deck where the selector matched nothing, so a gate that never ran is indistinguishable from a clean result and the deck ships unchecked. Case 7's Option A is the same class of failure one step further in (a pass concealing a check that threw), and Case 1's Option B passes a live Reg G prominence breach.
