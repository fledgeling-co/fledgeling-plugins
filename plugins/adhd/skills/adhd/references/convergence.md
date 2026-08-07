# Convergence — floors, clustering, judge-bias defenses, boss gate

Phase 2/3 mechanics in full. The design premise, from the judge-bias
literature: an LLM's direct 1–10 scores cluster toward the middle, don't
model the novelty–feasibility trade-off, and are near-noise for novelty
specifically. So this skill never ranks by absolute numbers. It gates
with pass/fail floors, clusters by mechanism, selects for coverage, and
compares pairwise when order matters.

## Quality floors (pass/fail, applied per idea)

An idea must pass all three to survive. Floors are judged with a short
written justification each — the justification is what makes a floor
falsifiable rather than a vibe.

1. **Soundness.** Does the stated mechanism plausibly produce the claimed
   effect? Trace the causal chain in one sentence; if the chain needs a
   miracle step, fail. Stated guarantees are part of the claim: a
   crash-safety promise, a complexity bound, or a loss-window number
   must follow from the mechanism, and an overclaim is a soundness fail
   even when the underlying idea is good — downgrade the claim to what
   the mechanism actually delivers rather than shipping the overclaim.
   (A blind gpt-5.6 judge rejected an otherwise-winning run precisely
   for "overclaims mmap crash safety and O(1) recovery".)
2. **Feasibility.** Could a small team validate or build a first version
   under the stated constraints? Name the first test and the scarcest
   resource. "Weeks of R&D before we know if it's real" is a fail at
   standard tier and a flag (not a fail) at 100%.
3. **Fit.** Does it address the *stated* ask, not a generic neighbor?
   Trace to the user's actual words. An idea solving "make retries
   pleasant" when the ask was "stop the hangs" fails fit — this exact
   substitution caused the predecessor's benchmark loss.

Novelty is deliberately absent: it is never a floor, and it never
rescues a floor failure. Reaching Phase 2 already required differing
from the baseline in mechanism; that is the novelty bar.

## Mechanism-level dedup and clustering

- Two ideas are duplicates when they share cause + intervention point,
  regardless of wording. Merge, keep the strongest phrasing, note the
  merge count for the receipt.
- Cluster the survivors by underlying angle (3–6 clusters), labeled by
  the play ("remove-the-server plays", "pre-warm plays"). If everything
  lands in one cluster, that is a divergence failure worth naming in the
  receipt — the frames all walked into the same room.
- Each idea carries its `mechanism` field from Phase 1; cluster on that
  field, not on surface keywords.

## Trap flags

A trap is attractive-but-broken. Every flag must cite a concrete failure
mechanism: hidden cost, false economy, scaling cliff, premature
abstraction, incentive misalignment, untestability. Two symmetric
requirements keep the trap detector honest:

- A flag without a mechanism is deleted (a tone classifier that
  penalizes exciting writing is not trap detection).
- The mechanism must connect to the user's stated requirements: name
  which stated requirement or constraint the idea breaks, not just a
  generic downside. In a naming run, "conflicts with the reversibility
  the ask demands" is a trap reason; "sounds enterprise-unfriendly" on
  its own is not.
- Each non-flagged shortlist idea survives one hostile-reviewer line:
  "how would a skeptic kill this?" If the kill lands, it was a trap.

## Shortlist selection (quality-diversity, not top-N)

1. Take the best surviving idea per cluster (pairwise within cluster if
   unclear — see below).
2. From those elites, pick 3 (2 at any%) maximizing mutual mechanism
   distance. Hard rule: no two shortlist slots from one cluster.
3. The global "highest average" idea has no special claim to a slot —
   selecting three near-duplicate safe ideas is the documented failure
   of global weighted ranking.

## Pairwise comparison protocol (when ranking is needed)

Used within clusters and in the boss gate:

- Present the two ideas as **Option A / Option B with frame names,
  agent labels, and any "wildcard" styling stripped** — judges anchor on
  provenance and verbosity, not just content.
- Run both orders (A/B, then B/A). Stable verdict → accept. Flipped
  verdict → tie; prefer the idea with the cheaper first test.
- Verdict must cite which floor-relevant property decided it, in one
  sentence.
- In the companion CLI (where a second model family is available), route
  pairwise judging to a different family than the generator —
  self-enhancement bias is measured and material. Inside the markdown
  skill, order-swap + blinding is the practical subset.

## The boss gate

Runs after shortlist selection, once per shortlist idea, against the
Phase 0 frozen baseline.

Prompt shape:

> Problem, exactly as stated: [user's words]
> Option A: [one of baseline/finalist, randomized]
> Option B: [the other]
> Judge ONLY on solving the stated problem: correctness on the core ask,
> effort-to-ship, risk. Novelty and interestingness are excluded — do
> not reward or punish either option for being unusual.
> Verdict: A/B/TIE, one sentence citing the stated ask.

Calibration rules, both directions:

- **Against novelty theater:** the ★ pick needs BEATS at high stakes.
  If nothing beats the baseline, recommend the baseline openly and file
  the shortlist under "worth exploring later" — that honest outcome is
  the point of the gate.
- **Against the boring machine:** the gate asks "solves the stated ask
  at least as well, with an articulable edge", never "which would a
  cautious senior ship today" — a concrete incumbent is legible and
  low-risk, and a naive comparison always crowns it. TIE keeps the
  creative pick at exploratory stakes. If several consecutive runs all
  end in baseline wins, the gate is miscalibrated toward incumbency;
  loosen to the TIE bar or check whether the baseline is absorbing
  finalist mechanisms (it must stay frozen from Phase 0 — a drifting
  baseline is an unbeatable one).
- **Hybrid ladder:** on a LOSS, one optional Agent call grafts the
  finalist's single most interesting mechanism onto the baseline
  ("baseline + the one novel bit") and re-gates the hybrid once. No
  ladder past one rung.

## Adversarial repair (bounded, post-gate)

For each deepened winner, one critique from a *distinct* failure-mode
lens (security/on-call, economics, adoption, implementation) — either
inline or as part of the deepen call. The critic must produce a concrete
repair or a demotion, not commentary. This is where debate-shaped work
belongs; during divergence it homogenizes (evidence.md §3, §7).

## Receipt fields

Emit as output section 0, one line:

`ADHD <tier> — <frames spawned>/<returned> frames, <ideas generated> →
<after merge> after merge, <floored> floored, <apoptosed frames + reason
if any>. ★ <BEATS|TIES|LOSES> baseline. [Upgrade: /adhd --<next tier>]`

The receipt is the observability surface: it makes a light run read as
deliberate, a degraded run (dead branch, apoptosed frame) read as
handled, and the spend auditable after the fact. It also records the
gate verdict so a "baseline wins" run is visibly an honest result, not
a malfunction.
