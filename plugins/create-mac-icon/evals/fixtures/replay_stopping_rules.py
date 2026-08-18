#!/usr/bin/env python3
"""Replay the improve-skill trace against the naive and promotion-armed patience rules.

The per-round verdicts are RECONSTRUCTED from the counts documented in
references/fidelity-loop.md — the raw panel logs are not in this plugin. The
reconstruction is pinned by assertions against every documented figure, and by
the two documented OUTCOMES, so it cannot drift into telling a nicer story:

  - 13 judged rounds; the panel preferred the PREVIOUS take in 7
  - it preferred the new take in 3: r07, r10, r11; r11 was the last
  - in the six judged rounds after r11: five baseline, one tie, zero candidate
  - the naive "two consecutive non-winning rounds" rule fires at r04
  - the same rule armed after the first promotion stops at r13, ships r11,
    and skips six rounds
"""
PATIENCE = 2        # the published rule under test
HARNESS_VETO = 3    # PANEL_VETO in loop_runner.py

TRACE = {r: None for r in range(20)}
TRACE.update({
    3: "baseline", 4: "baseline",                    # naive rule trips here
    5: "tie", 6: "tie",
    7: "candidate", 10: "candidate", 11: "candidate",  # the three genuine wins
    12: "baseline", 13: "baseline", 14: "tie",
    15: "baseline", 16: "baseline", 17: "baseline",     # six after r11
})

judged = {r: v for r, v in TRACE.items() if v}
assert len(judged) == 13, len(judged)
assert sum(1 for v in judged.values() if v == "baseline") == 7
assert sum(1 for v in judged.values() if v == "tie") == 3
assert [r for r, v in judged.items() if v == "candidate"] == [7, 10, 11]
after = {r: v for r, v in judged.items() if r > 11}
assert len(after) == 6
assert sum(1 for v in after.values() if v == "baseline") == 5
assert sum(1 for v in after.values() if v == "tie") == 1
assert not any(v == "candidate" for v in after.values())


def run(armed_after_promotion: bool, patience: int):
    """Return (stop_round, shipped_round, rounds_used, wins_seen_before_stop)."""
    nonwins, promoted, best, wins = 0, False, None, []
    for r in sorted(TRACE):
        v = TRACE[r]
        if v == "candidate":
            nonwins, promoted, best = 0, True, r
            wins.append(r)
        elif v in ("baseline", "tie") and (promoted or not armed_after_promotion):
            nonwins += 1
        if nonwins >= patience:
            return r, best, r + 1, wins
    return max(TRACE), best, len(TRACE), wins


rows = [
    ("naive: patience counts from round 1", run(False, PATIENCE)),
    ("promotion-armed patience", run(True, PATIENCE)),
    (f"promotion-armed, harness veto={HARNESS_VETO}", run(True, HARNESS_VETO)),
]
print(f"{'rule':<40} {'stops':<7} {'ships':<9} {'rounds':<7} wins seen")
print("-" * 78)
for label, (stop, ship, used, wins) in rows:
    print(f"{label:<40} r{stop:02d}{'':<4} "
          f"{('r%02d' % ship) if ship is not None else 'NOTHING':<9} {used:<7} "
          f"{', '.join('r%02d' % w for w in wins) or 'none'}")

n_stop, n_ship, _, n_wins = run(False, PATIENCE)
p_stop, p_ship, _, _ = run(True, PATIENCE)
assert (n_stop, n_ship, n_wins) == (4, None, []), (n_stop, n_ship, n_wins)
assert (p_stop, p_ship) == (13, 11), (p_stop, p_ship)
print(f"\nnaive stops at r{n_stop:02d} having seen no win at all, so it ships NOTHING the "
      f"panel ever preferred.")
print(f"promotion-armed stops at r{p_stop:02d}, ships r{p_ship:02d}, and skips "
      f"{19 - p_stop} of the 20 rounds.")
print("\nBoth documented outcomes reproduced exactly.")
