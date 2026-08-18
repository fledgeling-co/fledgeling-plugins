# Wireframe: Explore Many Ideas Quickly

Produce low-fidelity wireframes or storyboards to explore a flow, layout, or idea before committing to hi-fi design. Use this when the user wants to "explore options," "sketch something out," "see a few directions," or when the problem is open enough that hi-fi work would be wasted now.

**Wireframes are disposable.** They exist to test ideas, not to be polished. Their value is in the breadth of options, not the fidelity of any one.

**The failure this procedure prevents is committing hi-fi work to a structure nobody chose.** A hi-fi round buys one bet at full cost; the same budget at this fidelity buys three or four structures the user can reject in seconds. The other failure it prevents is the opposite one — a wireframe polished until it is a slow hi-fi mock, which is spend on a fidelity the decision does not need. Both are avoided by the same rule: greyscale, disposable, and only as detailed as the axis being tested.

## Phase 1: Understand the goal

Confirm:

- **What's being explored.** A single screen, a multi-screen flow, a navigation pattern, an information hierarchy, an interaction model?
- **The user goal.** What is the imagined user trying to accomplish on this screen / flow?
- **Constraints.** Mobile or desktop? Existing context or greenfield? Any non-negotiable elements (logo position, mandatory legal copy, fixed brand color)?
- **Number of variations.** 3 minimum. 5–6 is a healthy ceiling for one round.
- **Axis of variation.** What dimension should the variations differ on? (Layout? Information density? Step count? Where the primary CTA lives? Single-page vs multi-page?)

If the user just says "wireframe a sign-up flow" without specifying, propose 2–3 axes (e.g. "single-page form vs multi-step wizard vs progressive disclosure") and ask which they want explored.

## Phase 2: Establish wireframe conventions

Wireframes have a visual language. Stick to it so the user reads them as wireframes — not as broken hi-fi:

- **Greyscale only.** No brand color. Black, white, and 2–3 grays.
- **System sans-serif.** No type personality. The user shouldn't form opinions about the font yet.
- **Boxes for content areas.** A rectangle labeled "headline" or "image" or "feature card."
- **Striped placeholders for imagery.** Diagonal-stripe pattern with a monospace label (`product shot 1200×800`) — the honest placeholder recipe from SKILL.md §6. Never an actual image; it pulls focus.
- **Label-style placeholder copy, never lorem ipsum.** Write "Headline goes here / one short sentence about the value prop", or the real string when you have it. Greeked copy hides the length the layout has to hold, and it is the one content defect this skill's gate refuses at critical — a wireframe full of ipsum cannot pass its own review round, which is a contradiction rather than a standard.
- **Annotations welcome.** Numbered callouts pointing to key decisions are fine — the wireframe is a thinking artifact.

This is the one context where hand-drawn-feeling SVG (rectangles, lines, simple icons) is acceptable — because everything is at the same low fidelity.

## Phase 3: Sketch variations

Produce **at least 3** variations, each differing on the axis established in Phase 1. Lay them out side-by-side on a single self-contained **canvas page** — the CSS-grid snippet in SKILL.md §18. For a multi-screen flow, build each variation as a small storyboard (3–5 screens stacked or arranged horizontally) inside its cell.

Vary across: **layout** (centered single-column / left-aligned / split-screen / grid), **information density** (minimal hero / feature-rich / feed-style), **flow structure** (single page / multi-step / progressive disclosure), **primary CTA placement** (top / bottom / sticky / inline), **navigation pattern** (top nav / side nav / bottom tab / hamburger).

Start with the most by-the-book variation and end with the most novel. **Write down each variation's distinguishing structure before sketching it** — left unspecified, variations converge on near-identical layouts. Make at least one genuinely off-distribution. The axis discipline, the squint test, and the rules for keeping three variations genuinely three are owned by `generate-variations.md` Phases 3 and 5; read them rather than re-deriving them here, and note that its option-name stability rule applies at this fidelity too.

## Phase 4: Annotate the variations

For each variation, add 2–4 annotation points so the user can see what's interesting about it:

```
- Variation 1 (single-column wizard): → simple, focused, but slow
- Variation 2 (single-page form):      → fastest path, but heavy first impression
- Variation 3 (progressive disclosure):→ balances both, but more JS state
```

Place annotations next to each variation, not in a separate doc. The user should read the variation and the rationale together.

## Phase 5: Capture decisions

After the user picks a direction, capture: the chosen variation (or hybrid); what attracted them to it; what they explicitly rejected from the other options; any new constraints surfaced during the review. This becomes the brief for the hi-fi follow-up — and the variation keeps its number and name into that round.

## Phase 6: Hand off

Wireframes are a stepping stone. When the user picks a direction, suggest one of:

- **`make-a-prototype`** to take the chosen wireframe to hi-fi interactive
- **`frontend-aesthetic-direction`** first, when the structure is settled and no brand exists yet
- A new round of wireframes if the user wants to iterate further at low fidelity

Do not invest hi-fi polish in the wireframes themselves. They've served their purpose; let them go.

## Phase 7: Summarize

Report: number of variations produced; axis of variation; recommended next step; any open questions the wireframe round surfaced.
