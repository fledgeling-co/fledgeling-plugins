## 1.2.1 - 2026-08-30

Every skill name written in a prompt or a cross-reference now carries its full
`plugin:skill` form. A bare name is not resolvable by the Skill tool, so a runner told to
invoke one gets `Unknown skill` and carries on without it.

Measured across 51,763 session transcripts over 21 days: 53 of 77 Skill invocations failed,
a 68% failure rate. Bare names were 27 of those. Four more came from agents that knew a
prefix was needed and invented one (`plugin:`, or the marketplace name).

# design-craft changelog

## 1.1.0 - 2026-08-21

- A seventh CSS mechanic: an unterminated block swallows every rule after it while `matchMedia` still reports the query matching and the rule stays greppable.
- Two engine limits measured on a real build: `ch` units inside `minmax()` do not resolve, and `clip-path` is not applied, which disarms the 100vmax spread-shadow full-bleed idiom.
- `gsap-motion.md` gains the entrance rule: use `gsap.from` so the authored markup is the end state, and never animate the block carrying the conclusion.
- `evidence.md` section 8 records all four with their tier, n and which are engine-specific.

