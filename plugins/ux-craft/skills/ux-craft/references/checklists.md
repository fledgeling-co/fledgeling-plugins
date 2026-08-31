# Pre-Ship Checklists

Condensed verification passes. Run the matching list before calling any build/mock done, and as the closing sweep of any review. These are floors, not reviews — a pass here doesn't replace the lens pass in review-playbook.md.

**Report the fraction, not the fact.** A list of 43 boxes that gets "checked" as a block is a list that was read, not run. Report `<n> of <n> checked, <n> n/a with reasons` for the list you ran, the same way the state grid reports its cells — an unticked box is visible, "ran the checklist" is not. `scripts/ux-lint.py` mechanises the subset of these that a machine can decide; the rest are yours.

## Any screen (web or mobile)

- [ ] Trunk test: a cold visitor can tell what this is, where they are, and what to do next
- [ ] Exactly one primary action; secondaries visually subordinate
- [ ] The six required state cells exist — first-run/empty, loading, ideal, partial, error, done — and the three conditional ones are each filled or marked `n/a: <reason>`: offline (if the surface can lose the network), disabled (if a control can be unavailable), overflow (if the user can grow the content)
- [ ] All interactive states designed: hover (web), focus-visible, active, disabled (with reason), loading
- [ ] Errors: what + how-to-fix, adjacent, not color-only
- [ ] Nothing requires remembering an earlier step (recognition over recall)
- [ ] Real content tested: longest name, 0 items, 100 items, missing image
- [ ] Fixed-width columns sized from the longest real string in the face that column uses — monospace and tabular figures are wider than they look, and an overlong cell overlaps its neighbour silently, with no scrollbar and no warning
- [ ] Every value sits with the mark it describes — a bar's number beside or inside its own fill, never pinned to the far end of a track where a short bar strands it
- [ ] Reversible actions have undo, not confirmation; destructive actions have proportional friction with named consequences
- [ ] Copy passes ux-writing rules: outcome-verb buttons, no jargon, front-loaded meaning, correct typography
- [ ] No dead ends anywhere the user can land: not-found/error routes are designed (a 404 that names the problem and offers search/home/key paths — the raw system page is a wayfinding failure), and every page offers a way onward
- [ ] Legally required links present and findable (privacy, terms; cookie consent where the jurisdiction demands it) — routinely forgotten in mocks, and a compliance issue, not a preference, in regulated contexts

## Flow

- [ ] Category-default sequence named and either varied on one axis or kept with a stated reason (`flow-shape-variety.md`); session and project ledger recorded if this is not the first flow of the session
- [ ] Entry, steps, completion, and every exit (back/cancel/abandon/resume) mapped
- [ ] One decision per step; ≤4–7 fields visible per step; progress shown for 3+ steps
- [ ] Back preserves entered data; long flows auto-save
- [ ] Nothing asked twice; nothing asked before it's needed and justified
- [ ] Failure at each step preserves prior work and offers recovery
- [ ] Completion screen: what happened + what happens next (peak–end)


## Persuade (landing, campaign, pricing, waitlist only)

- [ ] One-sentence offer, audience, and primary action written before the section list (`persuade-conversion.md`)
- [ ] Primary call to action visible without scrolling at 1280px and 375px
- [ ] Proof beside the claim it supports, or an honest placeholder; no invented logos or metrics
- [ ] Final call to action uses the same label as the first viewport
- [ ] This list was not applied to Operate, Read, Experience, checkout, auth, or payment

## Form

- [ ] Every removable field removed, defaulted, or inferred
- [ ] Visible labels (not placeholders); single column; related fields grouped tighter than groups
- [ ] Semantic input types + autocomplete/textContentType (right keyboard, autofill, WCAG 3.3.7/3.3.8) — and **autofill the form from a populated browser profile rather than typing into it**, because a token whose shape the validation rejects only fails on that path
- [ ] Validation on blur; clears on change after first error; submit failure focuses first invalid field; multi-error summary with anchors; errors wired with `aria-invalid` and `aria-describedby`, not colour alone
- [ ] Defaults pass the 80% test; zero pre-checked consent
- [ ] Submit button disables + shows progress during async (no double-submit)
- [ ] Any undo offered in a toast is reachable by keyboard and is **not** the only copy of the affordance — an interactive element inside a live region is announced as flat text with its role stripped

## Responsive / mobile quick pass

- [ ] No horizontal scroll at 360px; longest heading survives; body ≥16px (mobile web)
- [ ] Targets: ≥24×24 CSS px (WCAG 2.2 SC 2.5.8, **AA** — the only one you may call a WCAG failure) or a qualifying exception; craft target 44 (44×44 CSS px web = SC 2.5.5 **AAA**, 44pt iOS, 48dp Android); hit areas extended on small glyphs; primaries in thumb reach
- [ ] Safe areas respected; scroll content not hidden under fixed bars; `min-h-dvh` not `100vh`
- [ ] No hover-only functionality; gestures have visible alternatives; press feedback <100ms
- [ ] Back preserves scroll/filter/input state; key screens deep-linkable
- [ ] Dynamic Type / 200% font scale without truncation or overlap; dark mode contrast checked separately

## WCAG 2.2 quick pass (A/AA essentials)

Perceivable: text contrast ≥4.5:1 (large ≥3:1); UI components/focus indicators ≥3:1 non-text contrast; color never the only signal; informative images have alt (decorative `alt=""`); visual structure matches semantic structure (real headings, lists, tables); reflow to 320px without 2-D scrolling; text resizes 200%.
Operable: everything keyboard-operable, no traps; visible focus, not fully obscured by sticky UI (2.4.11); logical focus order matching visual order; skip link; descriptive titles/headings/links (no bare "learn more"); **targets ≥24×24 CSS px (2.5.8, AA)** unless one of its exceptions applies — Spacing (a 24px-diameter circle centred on the target overlaps no other target's circle; this, not a flat 8px gap, is the normative form), Equivalent, Inline, User Agent Control, Essential — with **44×44 CSS px being 2.5.5 at AAA**, so a 32px button is not an AA failure; dragging has a non-drag alternative (2.5.7); nothing flashes >3×/s; auto-moving content pausable; `prefers-reduced-motion` respected.
Understandable: `lang` set; no context change on focus/input; consistent nav and component identity across pages; errors identified in text with suggestions; labels/instructions present; no re-asking known info (3.3.7 — a billing address with no "same as shipping" bypass is the canonical failure); **authentication without a cognitive function test (3.3.8, AA) — blocking paste into a password field, or blocking a password manager, is the canonical violation, and a transcription CAPTCHA is another**; high-stakes submissions reversible/confirmable.
Robust: custom controls have name/role/value; status messages announced via live regions without stealing focus; modals trap focus, restore it on close, background inert.

State honestly what a static/screenshot review cannot verify (screen reader output, keyboard flow, real AT behavior) — list those under "Needs verification", **never claim conformance**. Mechanical supplements, both of which narrow the unverified set without emptying it: `scripts/ux-lint.py --static <paths>` and `--probe <url>`, then `npx @accesslint/cli` on a live page. Note what the render engine could not see at all (native form controls, motion, reduced-motion, web fonts) as not-checked rather than as passing — see the engine table in `review-playbook.md`.

## Severity ladder (shared by all reviews)

- **Blocker** — a user group cannot complete the task
- **High** — likely task failure/drop-off, AA violation, dark pattern, trust breach
- **Medium** — real friction; completable but costly
- **Low** — polish

Calibration: use the full range; severity = user impact, not fix effort; multiple-lens agreement raises confidence, not severity; a report where everything is Medium hasn't decided anything.

## AI feature

- [ ] Scope of what the AI acts on is visible before it runs; autonomy level (suggest/ask/act) is explicit
- [ ] Preview-before-commit on anything that modifies user content; AI output marked until accepted; bulk runs sampled first (2–3 records verified before the rest)
- [ ] Friction matches blast radius: verification only for real loss (money/work/reputation/security); undo for the rest; "don't ask again" after first confirmed run
- [ ] Stop always available and in the same place; long tasks pause/resume, never force restart
- [ ] Empty state scaffolds the first prompt (3–6 contextual suggestions/templates; never a bare box on an empty state)
- [ ] AI involvement disclosed with verbs ("Summarized with AI"); AI content visually distinct; a human is reachable where it matters
- [ ] Claims cite sources with working references; missing sources declared, never filled
- [ ] Retrieved/connected content treated as untrusted: sources-in-play visible, tool actions gated on previews, per-source kill switch
- [ ] Memory visible, editable, deletable; save events announced; training/retention consents separate and opt-in
- [ ] Cost shown before long/bulk/chained runs
- [ ] Narration cadence specified, not inherited: one line before the first action, updates only on findings or direction changes, outcome first at the end; self-corrections surfaced only when they change the user's decision or data
- [ ] Cancel/downgrade/opt-out paths no harder than their opposites (click-symmetry ≤ ~1×; >2× is a hard fail)

## Email

Use the pre-send checklist in `email-ux.md` — it's the complete list (subject/preheader, one CTA, images-off, dark mode, plain-text part, compliance footer, <100KB, register check).
