# Flow Shape Variety: Do Not Sequence Every Journey the Same Way

Use this in Build mode after the goal sentence and before the state grid. The standing complaint that sites look the same is not only visual. Generated flows converge on the same skeleton: a 3-step "how it works", a centred hero call-to-action, a 3-column feature row, then a frequently-asked-questions block. That skeleton can be usable and still be the last product you designed.

Mobbin's `search_flows` already supplies shipped sequences (`plugins/design-craft/skills/design-craft/references/mobbin-trawl.md`). This file is the check that the sequence you adopted is not the sequence you always adopt.

## Name the category default sequence first

Write one line: the steps this category always ships. Example for a SaaS trial: `hero CTA → social proof → 3 features → 3-step how-it-works → pricing → FAQ → final CTA`.

That line is now banned as the unexamined first answer. You may still ship it if the user took the category-standard exit, or if analytics show that sequence converts. Both need a stated reason.

## Axes that actually change a flow

Pick **one** primary axis to vary. Five rearrangements of the same 3-step wizard are not a choice (`SKILL.md` Build step 3).

| Axis | Default generated shape | Alternate that is still usable |
|---|---|---|
| **Commitment** | Long form, then submit | Progressive disclosure; one decision per step; save-and-resume |
| **Proof placement** | Logo wall under the hero | Proof beside the claim it supports; a case study before the ask |
| **Orientation** | Feature list, then how-it-works | Object or job first: show the artifact, then the steps that produce it |
| **Recovery** | Happy path only | Empty, partial, and resume designed as first-class steps, not afterthoughts |
| **Device** | Desktop wizard shrunk | Thumb-zone primary action; fewer fields; camera / wallet / passkeys where the platform has them |

The alternate must still pass the trunk test (where am I, what can I do, what happens next) and non-negotiable 1 (one primary action). Variety that hides the next step is a defect, not a direction.

## Session and project ledger

Before locking the step list, name the flow shapes already used this session **and** read the project ledger at `<project>/.design-craft/diversity-ledger.json` (`plugins/design-craft/skills/design-craft/references/diversity-ledger.md`). A second onboarding does not get another 3-step personalisation wizard unless the product has only that journey.

```bash
python3 plugins/design-craft/skills/design-craft/scripts/diversity_ledger.py check   <project>/.design-craft/diversity-ledger.json --kind flow --flow-shape "3-step-personalisation-wizard"
```

Record in the handoff, then `record --kind flow` after the step list is settled:

```
FLOW SHAPE
  default banned: hero → 3 features → 3-step how-it-works → FAQ
  axis: proof placement
  took: one worked example before the ask (Mobbin q2, Linear-class onboarding)
  left: 6-step preference quiz — this audience is at-work and impatient
  ledger: recorded | skipped-absent | override: <reason>
```

## When not to vary

- An incumbent product flow the user asked to match.
- Checkout, auth, and payment sequences where platform convention is the prediction the user already made (non-negotiable 8). Deviate only when the deviation carries information worth its cost.
- A one-screen form whose job is "submit this". Inventing a wizard for flavour inverts non-negotiable 6: friction without blast radius.

## Repair

If a review finds the step list is the brief's own headings in the brief's own order, that is the same structural tell `ai-slop-check.md` §17 names for pages. Rewrite the sequence from the user's job, then rename the steps as verbs ("Pick a workspace", "Invite two people") rather than noun-phrase filing labels.
