# Redesign: Modernise an Existing Surface Without Breaking It

Redesign an existing site, screen, or artifact — a surface with users, traffic, brand equity, and history — rather than designing from a blank file. Use this whenever the brief starts from something that already exists: "redesign this", "modernise our site", "make this look current", "upgrade the UI without losing the brand".

**Misclassifying the mode is the single biggest source of bad redesign output.** A preserve-brief treated as greenfield destroys equity the user never asked you to spend; an overhaul-brief treated as preserve delivers timid polish when they wanted a new visual language. Detect the mode first, audit second, touch pixels last.

## Phase 1: Detect the mode

Classify the request before any design work:

- **Preserve** — modernise without breaking the brand. The identity, IA, and voice stay; execution improves. This is the default reading of "refresh", "clean up", "modernise". Scope is sovereign here (SKILL.md ch. 19): touch the named target, and introduce no colour, font, radius, shadow, or other system primitive the surface doesn't already own — if the existing system genuinely can't express the direction, stop and ask, naming the exact addition and the job it would do.
- **Overhaul** — new visual language on existing content. Treat the *visuals* as greenfield (route through `frontend-aesthetic-direction.md`), but preserve content, IA, and the Phase 3 never-change list. The old look is **evidence of what the subject is, not authority over what it becomes** — mine it for the subject's own materials and vocabulary, then replace it.
- **Actually greenfield** — the brand itself is changing, or the old surface is being abandoned. Leave this file; run the normal greenfield chain.

**Never split the difference.** Once the mode is Overhaul, polish stops being applied to the discarded look — spend on both sides of a decision nobody made is the most expensive way to redesign. Once the mode is Preserve, the replacement world stays out of the diff entirely.

If the mode is ambiguous, ask once — "Should this preserve the existing brand, or start visually from scratch?" — and nothing else; the audit answers the rest. And before modernising at all, apply the trust-signal test from SKILL.md ch. 4: on long-lived, high-trust surfaces (documentation, reference tools, institutional pages), "looks dated" may be doing credibility work — prefer changing behavior (affordances, IA, states) over appearance unless the brief explicitly asks for a new look.

## Phase 2: Audit before touching

Document the current state first — the audit is what separates a redesign from a drive-by rewrite. Read the actual source (per SKILL.md ch. 4: code over screenshots, token files first) and record:

1. **Brand tokens** — primary/accent colors, type stack, logo treatment, radii, shadow language. Extract these *before* applying any palette or type rules from the craft references: a brand that is already purple stays purple; existing brand values are the override, not the violation.
2. **Information architecture** — page tree, primary nav labels, key conversion paths, URL slugs and anchor IDs.
3. **Content inventory** — which blocks are doing work, which are filler. Filler gets cut under the ch. 5 content principles; working content is preserved verbatim unless a rewrite was requested.
4. **Patterns to preserve** — signature interactions, a recognisable hero, established copy voice, anything users have muscle memory for.
5. **Patterns to retire** — run the review references as the diagnosis: `ai-slop-check.md` for template tropes, `hierarchy-rhythm-review.md` for flat hierarchy and random spacing, `interaction-states-pass.md` for missing states, `accessibility-audit.md` for violations. Their findings become this redesign's work list — don't re-derive a separate audit catalogue.
6. **Invisible dependencies** — analytics events bound to button labels, form field names, and element IDs; SEO surface (meta titles, structured data, OG cards, ranking pages). SEO migration is the #1 redesign risk precisely because it's invisible in the mockup.

## Phase 3: What never changes silently

These carry user muscle memory, tracking, or legal weight — change them only with explicit user approval, never as a side effect of visual work:

- URL structure, route slugs, anchor IDs
- Primary navigation labels
- Form field names and field order (breaks analytics and browser autofill)
- The logo/wordmark
- Legal, consent, and cookie copy
- Existing accessibility wins (focus states, alt text, keyboard paths, contrast) — a redesign that regresses accessibility failed regardless of how it looks

## Phase 4: Modernisation levers, in priority order

Apply in order and **stop when the brief is satisfied** — each lever costs more risk than the last, and the early levers carry most of the value (levers 1–4 typically deliver ~70% of the perceived modernisation at a fraction of the risk of restructuring):

1. **Typography refresh** — the biggest visual lift per unit of risk. Font swap, scale discipline, tracking per `hierarchy-rhythm-review.md`.
2. **Spacing and rhythm** — snap to a scale, fix vertical rhythm, let sections breathe.
3. **Color recalibration** — unify the neutral scale, desaturate accents, keep the brand accent recognisable. Tone pure whites/blacks.
4. **Interaction states** — hover/active/focus/disabled/loading per `interaction-states-pass.md`; makes the surface feel alive at near-zero layout risk.
5. **Motion layer** — micro-interactions and entrances per `motion-design.md`, scaled to the surface's register.
6. **Hero and key-section recomposition** — restructure top-of-funnel sections; layout changes begin here, so does real risk.
7. **Full block replacement** — only when a block is unsalvageable, and preserving its content and any bound events.

Escalate past lever 4 only when the visual debt is structural (broken IA, no coherent system, broken mobile) — then run a full redesign with strict content preservation, not a quiet rewrite.

## Phase 5: Execute and verify

- **Work with the existing stack.** Match the file's conventions and framework; don't migrate styling systems or restructure markup that works. The surgical-iteration rules from SKILL.md ch. 19 govern every edit.
- **Small reviewable steps, verified as you go** — after each lever, check the rendering yourself per `visual-verification.md`, with before/after pairs at the same viewports and the same states (capture the *before* before editing). If the surface has both themes, check both. Delegation belongs to the ship-time panel, not to confirming a change you just made.
- **Finish with `polish-pass.md`** on the changed surface.

Summarize for the user: the detected mode, what was preserved and why, which levers were applied, what was retired (with the finding that justified it), and anything from the Phase 3 list you recommend changing but didn't touch.
