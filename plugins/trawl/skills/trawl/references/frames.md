# Frames — portfolio seats, synthesis template, fit floor, apoptosis

The predecessor skill picked 5 frames from a static 15-row table by tag.
Two failure modes followed: unfit frames on technical problems (a child
persona critiquing a memory allocator), and the same 15 lenses regardless
of domain. This file replaces the table with a portfolio: five *seats*
with selection rules, a synthesis template for composing bespoke frames,
a fit floor that vetoes catastrophic mismatches, and apoptosis rules for
frames that produce nothing usable.

## The five seats

Every standard run fills all five. any% fills seat 5 plus the one other
seat with the most leverage on the problem. 100% fills all five plus two
extra synthesized frames targeting whichever seats showed the most
traction.

### Seat 1 — Ordinary stakeholder

A concrete occupational persona who lives with the consequences of the
decision. Research: one-sentence *ordinary* personas partition knowledge
better than celebrity or "creative genius" personas; breadth beats depth.

Catalog (pick or compose; one sentence is enough):
night-shift support lead · legacy-system maintainer · accessibility
tester · municipal procurement officer · bootstrapped solo founder ·
data-protection officer · junior dev in their first on-call week ·
customer-success rep who demos this weekly · SRE who inherits it ·
technical writer who must document it · finance controller who pays for
it · QA engineer who regression-tests it.

Pick the stakeholder whose daily pain intersects the problem most
directly — not the most senior or most obvious role.

### Seat 2 — Operational constraint

An extreme that breaks anchoring on the reasonable middle:
$0 budget / 1 hour · infinite budget / 10 years · no network · no
database · provable-correct-only · single file · must survive a 3am page
untouched · must run on a 10-year-old phone · the load-bearing
dependency is deleted tomorrow.

### Seat 3 — Adversary / inversion

Attacker, hostile competitor, or the inverted question ("how do we
guarantee NOT-goal?", then negate each answer back). Adversarial frames
double as trap detectors: their ideas often name the failure modes
Phase 2 needs.

### Seat 4 — Cross-domain mechanism

Biology (immune memory, apoptosis, quorum sensing, evolution) ·
logistics (queues, batching, hub-and-spoke, last-mile) · markets
(auctions, futures, clearing houses) · game design (loops, save-states,
difficulty curves) · speedrunning (skips, abusive-but-legal paths) ·
urban planning · epidemiology · aviation safety.

The transplant contract, verbatim in the branch prompt: *"Extract one
transferable mechanism, state its source-domain constraint, map it onto
the target problem, then state where the analogy breaks."* An analogy
that can't name its mechanism is decoration and will be merged away in
Phase 2 anyway — demand the mechanism up front.

### Seat 5 — Wild seat (fit-exempt)

One deliberately unfit-looking frame: the 10-year-old, the medieval
guild master, the ant colony, a poet, the maximalist. Exempt from the
fit floor *by design* — the gate is scored by the same model whose
priors make obvious answers obvious, so it will systematically rate
alien frames as unfit, and alien frames are occasionally where the
reframe comes from. The wild seat's quality control is apoptosis
(output-judged, after the fact), never fit (persona-judged, before).

## Synthesizing bespoke frames

Frames need not come from any list. Compose one per run when the problem
suggests it, from three slots:

**domain-adjacent expert × temperament × constraint style**

- *Domain-adjacent expert:* an expert from a field structurally adjacent
  to the problem — not the problem's own field (whose defaults are the
  baseline already). Cache invalidation → postal logistics dispatcher.
  Feature flags → theater lighting operator.
- *Temperament:* paranoid · minimalist · maximalist · contrarian ·
  frugal · archivist.
- *Constraint style:* cannot trust any clock · sees only aggregates ·
  must justify every moving part · allergic to state.

Worked examples:
- "A paranoid postal-logistics dispatcher who cannot trust any clock"
  (cache invalidation).
- "A minimalist theater lighting operator who must justify every moving
  part" (feature-flag service design).
- "A frugal aviation-safety investigator who sees only aggregates"
  (intermittent 0.1% timeout debugging).

## The fit floor (seats 1–4 only)

Before spawning, each candidate frame answers two questions:

1. **Leverage** — name the specific mechanism in this frame's vantage
   that bites on this problem's core tension. Naming it is the test; a
   frame whose advocate cannot name a mechanism fails. Steelman in the
   frame's own voice ("why does this vantage bite *here*?") — a neutral
   judge under-rates alien frames.
2. **Translatability** — could an idea phrased in this frame's
   vocabulary plausibly translate back into an action on this problem?
   Name one plausible back-translation.

A frame failing either question is swapped for another candidate for the
same seat. The floor is a veto on catastrophic mismatches, **not a
ranking** — do not pick the "best-fitting" five, or the run converges
before it diverges. A frame the **user explicitly requested** always
runs, whatever the floor says — the floor governs the skill's own picks,
never an instruction; apoptosis still applies to what the frame
produces. Two properties keep the floor safe: the wild seat is
exempt, and the floor judges the *frame–problem pairing*, not the frame
("10-year-old" fails on a memory allocator, passes on onboarding UX).

Record the frame ledger for the receipt: chosen seats, any rejected
candidates and the failed question.

## Apoptosis (after Phase 2 scoring)

A frame whose *entire* yield failed the quality floors is apoptosed:

- Its ideas are dropped from the Wide set, Converge, and Focus sections.
- The receipt gets one line: `frame X apoptosed: <best idea's failed
  floor>`. Nothing silently vanishes — the user can ask to see the dead
  branch.
- Judge output, never persona. A wild frame with one floor-passing idea
  survives in full, silly name and all.
- Apoptosis is per-run. It says this frame found no traction on this
  problem, not that the frame is bad. If the same frame apoptoses
  repeatedly on a problem class, stop selecting it for that class —
  that's the fit floor learning from evidence.

Why both mechanisms: the fit floor prevents spending an Agent call on a
predictable mismatch; apoptosis catches the mismatch the floor couldn't
predict, and keeps a silly-persona-next-to-serious-problem pairing out of
the rendered output — which is a credibility requirement, not cosmetics.

## Picking guidance by problem shape

- **Code/systems problems:** seats 1–4 grounded in operations (support
  lead, on-call constraint, attacker, logistics/biology mechanism) +
  wild.
- **Product/strategy problems:** stakeholder from the buying side,
  market-shaped constraint, hostile competitor, game-design mechanism +
  wild.
- **Naming problems:** the stakeholder is whoever says the name aloud in
  a sales call; cross-domain seats do the heavy lifting; wild seat runs
  loose.
- **Fuzzy debugging:** adversary seat becomes "the bug is adversarial";
  cross-domain from epidemiology/aviation-safety; constraint seat is
  "you may only observe, not patch".

Vary picks across sessions so a re-run of the same problem explores a
different candidate set.
