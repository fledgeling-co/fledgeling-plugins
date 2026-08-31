# Lookalike Gate: Prove This Page Is Not the Last One

A direction can be committed, lint-clean, and still be the same site as the previous commission. This file is the check that catches that. Run it after the first viewport is on disk and before `polish-pass`.

The complaint this exists for is not "it looks AI-generated". It is "the websites frequently look very similar to one another". That is a session-level failure, and no per-file slop scan can see it.

## What to compare against

Write the comparison set before judging. Three sources, in this order:

1. **This session.** Aesthetic families, display faces, signatures, and first-viewport topologies already shipped. Read them from the artifacts' direction-contract comments (`<!-- session-used: … -->`) and from the previous replies. If this is the first commission of the session, say so and skip this source.
2. **The category default named in the direction contract.** The actual arrangement, not the word "generic".
3. **The nearest named neighbour.** One real product in the same category, from the Mobbin ledger or a URL the user supplied. If neither exists, skip this source and say so.

A gate with an empty comparison set has not run. Record `lookalike: n/a — no prior commission, no named neighbour` rather than a pass.

## The four questions

Each is MET or UNMET (the criterion holds, or it does not). UNMET is a finding with a pasteable fix, not a vibe.

1. **Topology.** Could you describe the first viewport in one sentence that also describes the comparison page? "Left headline, right product shot, two CTAs under the dek" is a topology. If the sentence transfers unchanged, UNMET: change at least one of position of the primary action, image role, or reading start. Three equal feature cards in a row is a topology, not a feature section — it fails this question against the category default even when the copy is unique.
2. **Type system.** Same display family, same pairing logic, or the same "one distinctive face used as a costume on Inter-class body"? UNMET unless the incumbent brand named that face. A new commission in the same session does not get the previous display face.
3. **Signature move.** Is the memorable element the same class of trick (italic word-accent, acid underline, three-card bento, kinetic marquee, mesh gradient hero)? UNMET: pick a different class, not a recolour of the same trick.
4. **Swap test against the neighbour.** Change the nouns and the accent hex. Does the page still read as this product? If yes, UNMET: the world was never subject-mined.

Score `n/4 MET`. A commission that is supposed to be distinct ships at 4/4. 3/4 is a documented deviation with a reason. 2/4 or below is a rebuild of the first viewport, not a polish.

## Counts that decide it

Judgement is where two reviewers disagree. These four counts are not:

| Count | How | Fail |
|---|---|---|
| Distinct layout families on the page | Name each section's family (split-hero, editorial-manifesto, bento, quote, table, full-bleed figure, stepper, marquee, stacked-prose, comparison). | 8 sections with fewer than 4 families; any family used twice |
| First-viewport element count | Count discrete elements a cold visitor can point at | Generated UI is reliably sparser than shipped UI; if the neighbour's first viewport has ≥8 and ours has 4, density is the finding |
| Accent moments in the first 100vh | Filled buttons, filled chips, coloured rules, glowing marks | More than 2 under Restrained; more than 4 under Committed |
| Display faces used this session | Family name, not weight | The same display family on two consecutive greenfield commissions |

Record the four numbers in the delivery next to the lint counters. A lookalike pass with no numbers is a claim.

## What this gate does not do

- It does not fail a page for matching its own design system. Operate and Read surfaces that inherit an incumbent identity are supposed to look like the last screen. Mark `lookalike: n/a — incumbent system` and stop.
- It does not fail a page for looking like its category when the user took the standing exit (the category standard, played straight). That choice is the direction.
- It does not clone the neighbour as the fix. UNMET means change our topology, type, signature or subject-mining, not paste theirs.

## Repair order

When the score is 2/4 or below, repair in this order because later steps are cheaper and hide an earlier miss:

1. Change the first-viewport topology (split, stacked, manifesto, object-led, index-led).
2. Change the display face or the pairing axis (serif+sans, geometric+humanist, display+text). Do not swap Inter for Space Grotesk.
3. Change the signature class (type-as-image, object photography, data-ink annotation, command-surface, generative field, raw content).
4. Recolour last, and only inside the committed world.

Then re-run the four questions on the new first viewport. Do not re-run the whole polish panel for a topology change.
