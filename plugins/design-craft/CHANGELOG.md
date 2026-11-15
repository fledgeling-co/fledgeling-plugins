## 1.5.0 - 2026-11-15

- **Taste, tools, direction, dial.** Greenfield work now runs in four named stages. You pick, the model builds; it no longer re-rolls "be creative" until something sticks.
- **Taste board.** Drop in two to five screenshots you like (Pinterest, Dribbble, a saved folder). The skill writes three measurable observations per reference and one line naming what they share, then holds the direction to that line.
- **Mobbin at five checkpoints, not one.** It searches before the direction commits, then pulls one real screen per section type and borrows its proportions. It looks up the hardest states (empty, error). It finds evidence when you ask for "bolder" or name a competitor. And in critique, your render sits beside its reference.
- **Product demos that look like your product.** A new procedure, adapted from Benji Taylor's Stageshow (MIT), for hero demos, feature animations and bento tiles: one action in 3-5 beats over 10-16 seconds, 3-7 real words on screen, the window running off an edge rather than boxed in a card. It films the loop as a contact sheet and checks for one-frame jumps, text overflow and the loop seam before handover. If Stageshow is installed, it uses that instead.
- **Dial mode.** Once you've picked a direction, you get a tuning panel rather than another round of prompts: palette presets named from your subject's world, type, composition, material and motion controls, plus shuffle (kept inside the chosen direction), reset and copy-values. It's stripped back to four knobs or fewer before handover.
- **Pick, then fork.** After you choose one of three takes, the skill says whether the next round is macro (three versions of that take) or micro (the dial).
- **A sharper slop check.** It detects the current default look by its five named parts: cream background, italic accent words, 01/02/03 labels, monospace labels, pill buttons. That list comes from Anthropic's Opus 5.5 prompting guide. After the first render it adds whatever the model substituted to the ban list.
- **Fix only what needs fixing.** Three scopes (heavy, polish, already solid) and a fixed redline order, from spacing through to motion, adapted from Damir Sokolovsky's unslop (CC BY 4.0). An already solid screen gets two or three suggested refinements, applied only if you say yes.

Note: the demo rehearsal needs a browser engine that can seek the animation timeline. If it can't, the handover says which checks didn't run. The checks catch mistakes, not dull ideas, so someone still has to watch the loop.

## 1.4.0 - 2026-08-31

Adds the persistent project diversity ledger (`.design-craft/diversity-ledger.json`), ten lazy-loaded aesthetic recipes behind the 24-world index, sourced current-moves rows with evidence strength and review dates, and four paired variety / scope evals. The direction procedure now reads and records the last five visual decisions across sessions. The first-wave `trawl:trawl` and lookalike work remains in 1.3.0.

## 1.3.0 - 2026-08-31

Variety is now a procedure, not a hope. Greenfield hi-fi runs `trawl:trawl` (via `references/aesthetic-ideation.md`) before the direction commits, then a lookalike gate scores the first viewport against this session, the category default, and a named neighbour. `aesthetic-worlds.md` is 24 anchored directions grouped so candidates span material families; `current-moves.md` is a dated 2026 permission list, not a costume checklist. Sources: garden-skills' school catalogue, taste-skill 2.0's premium-consumer rotations and motion-claimed rule, `trawl:trawl`'s frame architecture. ai-design-skills' font whitelist was not imported — that would have been a new house style.

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

