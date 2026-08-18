# Flows, Forms, States & Navigation

The working patterns for structuring web/desktop experiences. Mobile-specific grammar lives in `mobile-ux.md`; the words live in `ux-writing.md`.

## Flow architecture

A flow is a promise: "do these steps and you'll get X." Design the promise first.

1. **Name the goal and the completion signal.** What does the user have when they're done, and how do they *know*? Flows that end with a silent redirect fail the peak–end rule at the moment that matters most — the end is what users remember.
2. **One decision per step** (GDS "one thing per page", validated across millions of government transactions). A "thing" is a conceptual unit, not a field — first+last name is one thing; shipping address is one thing. Bend it for expert tools and editing contexts (speed beats guidance there); never bend it for checkout, registration, or anything on mobile where drop-off costs money.
3. **Show position and size**: step indicator for 3+ steps ("Step 2 of 4 — Payment"), with meaningful step names. Progress accelerates completion near the goal (goal-gradient) — but only earned progress; fake head starts fail the ethics gate.
4. **Map every exit before building the happy path**: Back (preserves entered data — losing form data on Back is a High finding), Cancel (with a named consequence if data is lost), Abandon (auto-save drafts on anything long), and Resume (return the user to where they left off, with context re-displayed — recognition over recall).
5. **Eliminate excise** (Cooper): every step that serves the system rather than the user's goal — forced account creation before value, re-entering known data, confirmation of non-destructive actions — is excise. Cut it or absorb it (Tesler: complexity someone must pay; make the system pay).
6. **Guest paths and progressive commitment**: ask for information at the moment it's needed and justified ("we need your email to send the receipt"), not upfront. Each early field costs conversions and must earn its place.

### Flow-level review questions
- Could any step be removed, merged, defaulted, or deferred?
- Is anything asked twice? (WCAG 2.2 redundant-entry is now a formal criterion.)
- What happens on failure at each step — is the user's prior work preserved?
- Does the final screen say what happened *and what happens next*?

### Interrupted journeys (save, resume, re-enter)

Users don't finish flows in one sitting — they get interrupted, switch devices, come back tomorrow. Design the interruption as a first-class path: auto-save progress (not "did you remember to save?"); define and state the expiration policy for drafts and abandoned carts; and design **re-entry** deliberately — a returning user needs recognition of prior progress, a summary of previous choices re-displayed (never quizzed from memory), one tap to resume, and the option to start over. Cross-device: deep links and magic links restore the exact state, and re-engagement messages go to the device the user is likely on *now*, not the one they abandoned.

### First-run and onboarding

The first encounter has the least context, the least investment, and the lowest friction tolerance. Value first: show what the product does (populated sample data, a preview of the outcome) before demanding setup — sample data doubles as a mental model of what "full" looks like. Teach by doing with just-in-time guidance at the moment a feature becomes relevant — never a 5-slide tour (universally skipped) or mandatory profile completion before any value. The first task should deliver a real win, and reveal complexity only as the user demonstrates readiness.

## Forms

Forms are where users exchange value with the product; every needless field is friction taxed against the goal.

**Fields**
- The best field is no field: infer (country from locale), default (date = today, quantity = 1), or compute (totals, comparisons) instead of asking.
- Visible label above every field — never placeholder-as-label (disappears on focus, low contrast, breaks autofill and screen readers). Placeholders are for format examples only ("DD/MM/YYYY").
- Single column by default. The eye-tracking work usually cited for this (Penzo 2006) and Baymard's checkout research point the same way, but **no controlled experiment establishes an effect size** for single- versus multi-column, so argue it as a clearer scan path and a shorter label-to-field distance, never as a conversion percentage. The same caution applies to one-page-versus-wizard and guest-versus-account checkout: all three are practitioner consensus with vendor case studies behind them and no peer-reviewed effect size. Group related fields with fieldset/legend; the gap inside a group must be smaller than the gap between groups or grouping collapses.
- Mark required fields; better, cut optional ones. If a form has 20 fields but 6 matter for this user, conditionally show 6.
- Right input type per field (`email`, `tel`, `number`, `date`) — drives mobile keyboards and autofill. `autocomplete` attributes are an accessibility criterion in WCAG 2.2 (3.3.7 Redundant Entry, and 3.3.8 by way of not blocking password managers), and they carry a measured completion benefit: on one large observational form-analytics dataset, sessions where browser autofill was used completed at 71% against 59% for manual entry — a 12-point absolute gap — with keystroke effort down by as much as 80%. It is a vendor dataset rather than a controlled trial, so take the direction and not the decimal.

    **Autofill also has a failure mode, and it is yours to prevent.** In roughly 10% of forms in that same dataset, autofill *reduced* completion: the browser filled a value its cache held, the field's own validation rejected the shape of it, and the user landed in an error they could not resolve without deleting what looked correct. So the rule is not "add `autocomplete` and stop" — it is that the `autocomplete` token, the input type, and the server-side validation must agree on one shape. Test every form by autofilling it from a populated browser profile, not by typing into it; typing is the path that never trips this.

**Validation timing** — get this wrong and validation becomes harassment:
- Validate **on blur**, not on keystroke. The usual citation for this (Wroblewski/Etre 2009) is a single small practitioner study and **no replication of it could be found**, so treat the completion claim as practitioner consensus. What survives independently is the failure it identified: validating mid-word tells the user they are wrong while they are still typing the right answer, which is harassment rather than help.
- After a field first errors, re-validate **on change** so the error clears the moment it's fixed.
- Real-time only when the user is building toward a visible goal: password strength, character count, username availability.
- Cross-field rules ("end date after start date") on submit; on a failed submit, focus the first invalid field and, for multiple errors, show a summary at top with anchor links (WCAG).

**Error messages**: what went wrong + how to fix it, adjacent to the field, `aria-describedby`-linked, never color-only, never blaming. See ux-writing.md for tone.

**`novalidate` removes a state machine; it does not remove the need for one.** Turning off native validation to control the styling is routine. Shipping nothing in its place is the defect, and its signature is that the *only reachable state is the terminal one*. Measured on a real contact form: submit three empty fields and you land on "Not sent — your text is still in the field above" when there is no text in any field. No field-level error, no required marker, no distinction at all between empty, invalid and submitted. Drive **empty submit** on every form as a matter of course; a form whose empty submit and valid submit produce the same screen has one state, and it is the wrong one.

**A live region created at the moment of the announcement usually does not announce.** Assistive technology watches an *existing* `aria-live` / `role="status"` container for mutations. A node created carrying `role="status"` with its text already inside it commonly arrives as one atomic insertion with nothing to observe, and the message is dropped silently. Render the region empty and permanently in the DOM, then write text into it. Both versions look identical in a screenshot and identical in the final DOM — the difference is only visible if you compare the DOM before and after the submit. `role="status"` (implicitly polite) is for routine updates and waits for a pause in speech; `role="alert"` (implicitly assertive) interrupts and is for blocking, destructive or time-critical states only.

**And `hidden` on a live region silences it completely — the trap that survives knowing the trap.** A region rendered empty and permanently in the DOM is the rule everyone learns, and the obvious way to keep it out of the layout is `hidden` or `display: none`. Both remove the element from the accessibility tree, so every message written into it afterwards is announced to nobody, and the visual result is exactly what you wanted because you never wanted it seen. Hide it visually instead and leave it in the tree: `position: absolute; width: 1px; height: 1px; overflow: hidden; clip-path: inset(50%)`. Never `hidden`, `display: none` or `visibility: hidden` on anything carrying `aria-live`, `role="status"`, `role="alert"` or `role="log"`. This was found in this skill's own clean control fixture — the file whose whole job was to have nothing wrong with it, which had passed every other check — so treat it as the default mistake rather than an exotic one. A state placeholder in a mock is the separate case: if a hidden `<div>` exists only to show what the error state looks like, drop the live role from it, because a placeholder that claims to announce and cannot is worse than one that claims nothing.

**A live region flattens any interactive element inside it — which breaks the undo toast this skill recommends.** A screen reader reading a live region strips the roles and states of what it finds there: `<button>Undo</button>` announced inside an `aria-live` container arrives as the word "Undo" and nothing operable. So the toast pattern below — "Archived — Undo", a 5–10 second window — silently degrades to an announcement of a control that cannot be reached, and every visual check passes. Two fixes, and pick by stakes: announce the *outcome* in the live region and put the undo affordance outside it as a real focusable control that survives the toast's lifetime, or move undo to a permanent place (a trash view, a history panel, `Ctrl/Cmd+Z`) and let the live region carry only text. A time-limited undo that is only reachable by sighted mouse users is not an undo; it is a countdown.

**An honest "not wired yet" is still a full component.** A form that is deliberately not connected is a legitimate state to ship; it is not a licence to ship one state. It still owes required-field marking, an empty-submit path that says which fields are empty, and a completion message that describes what actually happened.

**A contact answer with no contact mechanism is not an answer.** "Who can I talk to?" answered with a department name — no email, no phone, no link, no form — is the comprehension failure wearing the shape of a completed section. Whatever the question promises, the answer has to carry the thing the reader came for.

**Smart defaults ethics**: a default is good if ~80% of users would pick it anyway; it's manipulation if it primarily benefits the business (pre-checked marketing consent, pre-selected premium tier). GDPR makes prechecked consent illegal, not just rude.

## The state machine

Every component and screen exists in more states than the ideal one. Enumerating them before building prevents the most common class of UX bug: the state nobody designed.

**Component states**: default → hover (never load-bearing — no touch equivalent) → focus-visible (distinct from hover; keyboard users live here) → active/pressed (feedback within ~100ms) → disabled (with a reason available — unexplained disabled buttons are a top frustration) → loading (button disables + spinner; the double-submit bug is a state-machine failure).

**Screen states — six required, three conditional.** This is the same grid SKILL.md Build step 4 asks you to write into the deliverable and count, described here in full. The six that every surface owes: **first-run/empty**, **loading**, **ideal** (with *normal* data — decide what normal means), **partial** (some loaded, some pending, one widget failed — the most overlooked state and one of the most common in real use; design the messy middle), **error**, **done**. The three that apply conditionally, each either filled or written `n/a: <reason>`: **offline** (any surface that can lose the network — what's cached, what degrades, how the user knows, and what happens to actions attempted offline: queued or lost?), **disabled** (any surface with a control that can be unavailable, with its reason reachable — unexplained disabled buttons are a top frustration), **overflow** (any surface holding content the user can grow: 10,000 items in a list designed for 50, a 200-character name, 999+ badges). For each state answer three questions: what does the user see, what can they do, how do they recover or progress.

Earlier versions of this file said nine while SKILL.md said six, and the lists were not nested — so a build following the six shipped six, and a review using the nine flagged three absences nobody had asked for. Six mandatory, three conditional, one grid, one count.

**Stress-test prompts** — run these against every screen before calling it done:
- *Content*: 3-character title? 300? Emoji-only? A name that's "O" or 40 characters? RTL text? A URL pasted into a text field? Completely empty?
- *Volume*: 0, 1, 3, 50, 10,000 items? Every badge at 999+? All sections expanded at once?
- *Time*: API answers in 200ms? 5s? 30s? Never? User leaves mid-flow and returns next month? Session expires mid-step?
- *Network*: drop mid-upload? mid-payment? 2G? Intermittent (10s up, 5s down)?
- *Behavior*: double-click? Browser Back mid-flow? Same flow open in two tabs? Paste instead of type? Shared link to an auth-required state?

**Graduated waiting**: under ~500ms, nothing — it reads as instant; 0.5–3s, spinner or skeleton; 3–10s, determinate progress where possible; 10–30s, add context ("taking longer than usual…"); 30s+, offer alternatives ("we'll email you when it's ready"). Never an indefinite spinner with no information — and **never fake progress**: an honest spinner beats a progress bar that lies, and a fabricated percentage is a sincerity violation users eventually catch.

**Spatial consistency**: no layout shift after load, no auto-rearranging content "for" the user, muscle memory respected (controls stay where they were), meaningful states have URLs (bookmarkable, shareable), and state survives refresh. Undo lives at the *data* layer — soft-delete by default — not just as a UI toast; "Are you sure?" is not a substitute for undo.

- **Empty states are the product's first impression** and most products waste them. Formula: what this area is for (education) + how to create the first item (action) + why it's worth it (motivation). "No data" is a defect. Distinguish first-use empty, cleared-by-user empty, and no-search-results (offer recovery: check spelling, broaden, popular items).
- **Loading**: skeleton screens that match the real layout for content surfaces (>300ms); spinners with context ("Uploading your file…") only for short indeterminate waits; determinate progress + time estimate for long operations. Reserve layout space — content jumping (CLS) is a UX defect, not just a metric.
- **Error**: what happened, is my data safe, what do I do now. Retry buttons for transient failures; never a dead end.
- **Optimistic UI** for low-stakes high-success actions (favorite, reorder, send message) — update immediately, reconcile with the server, and design the rollback ("Couldn't send — tap to retry"), never silently revert. Never optimistic for money, destructive actions, or anything affecting other users.
- **Perceived speed is a design material** (web implementation patterns): stream the page shell fast and let expensive widgets load inside their own boundaries — perceived latency drops without changing a single query; during heavy filtering, keep the input responsive and dim stale results (~0.7 opacity) instead of blocking; preload the next screen on hover/focus intent; never lazy-load above-the-fold or accessibility-critical content; set image dimensions and self-host fonts so nothing jumps after first paint (layout shift *is* a UX defect); load the saved theme synchronously before first paint — a flash of the wrong theme is a polish defect users notice.
- **Symptom catalog for reviews**: an input that loses focus on every keystroke, an animation that restarts, or scroll position that resets mid-interaction usually means a component is being re-created on each render — file it as the user-facing defect it is and route the code fix to code-review. A stray literal "0" rendered in the UI is the `count && …` falsy-render bug.

## Undo & destructive actions

Undo is a safety net that makes every other interaction feel lighter (forgiveness, Lidwell).

- **Don't confirm reversible actions.** Routine "Are you sure?" trains click-through blindness and devalues the confirmations that matter. Provide undo instead: toast with a 5–10s window ("Archived — Undo") for quick actions — **built so the undo control is reachable by keyboard and not buried inside the live region that announces it**, per the flattening rule above; history/versions for documents; trash-with-schedule ("empties after 30 days") for deletion.
- **Friction proportional to blast radius** for the genuinely destructive:
  1. Visual distinction (danger styling, spatially separated from safe actions)
  2. Confirmation naming the consequence ("Delete this project and all 47 files in it?") — generic "Are you sure?" carries no information
  3. Type-to-confirm for severe, rare actions (GitHub repo deletion)
  4. Cooling period for the gravest ("Account deletes in 14 days; cancel anytime before")

  The ladder is **practitioner consensus, and it is worth knowing that no published study measures the error rates of type-to-confirm against a plain dialog or against undo.** Every major design system uses it and none has published the comparison. So argue it as a deliberate shift from an automatic click to a conscious act of typing, which is a mechanism, and not as a measured reduction in accidents. Where the two disagree, prefer undo: a recoverable mistake beats a well-gated irrecoverable one.
- Always name what will be lost, show it when possible, and offer the lighter alternative ("Archive instead?").

## Navigation & IA essentials

(Deep IA work — taxonomy design, card sorts, tree tests — belongs to `intent-layer`; this is what you need while building/reviewing.)

- **Wayfinding trio** at every moment: orientation (where am I — highlighted nav item, page title, breadcrumbs at 3+ levels), route decision (labels informative enough to choose without clicking — information scent), closure (the landing page's title matches the link that promised it; a "Privacy Settings" link landing on "Account Management" is a closure failure).
- **Pattern fit**: hierarchical trees for clearly categorical content (≤3–4 levels; a growing "Other" category means the taxonomy failed); hub-and-spoke for independent task areas; flat+search/filter for homogeneous sets; faceted for multi-attribute browsing (design the zero-results combinations); dashboards that link to action, not widget dumps.
- Navigation reflects **user mental models, not the org chart**. Labels use the user's words (card-sort evidence beats stakeholder preference).
- **State preservation**: Back restores scroll position, filters, and input. Breaking Back is breaking the user's most-trusted button.
- Current location always visibly marked; primary nav placement identical on every page.
- **Test labels cheaply**: 5-second test (show the nav; can users predict what's under each label?) and cloze test (show the contents; can they guess the label?). Format labels ("Resources", "Hub", "Library") describe containers, not contents — they force click-and-check. And mine the search logs: high-volume searches for things that should be browsable mean the IA failed; zero-result searches mean the labels don't speak the user's language.
- **Zero results is a design problem, not an edge case**: spelling suggestions, broaden-filter offers, popular items, and a path to browse. New users browse (they lack the vocabulary to search); experts search — support both and their combinations.
- **Chrome rendered unconditionally on a surface that has nothing for it is worse than absent chrome.** Three shapes of the same defect, all from one build: an empty `<nav aria-label="Investor portal">` that announces itself to a screen reader and holds nothing; a mobile drawer that opens onto an empty list; and a header link to a route that returns 404 on this tier, shipped across 7,404 generated pages. Each element renders only when it has content, and any link whose target is conditional must read that condition **per request**, not from a stored prop that can go stale against the page it points at.
- **A navigation panel sized by its own content will be clipped by the viewport it opens in.** Measured at 375px on a live site: an open drawer laid out 327px wide starting at `left: -8`, so the first glyph of every label — *"nnouncements"*, *"eports and financial statements"* — was cut off, and the document gained 32px of horizontal scroll. It fired on one tenant out of six, and only because that tenant's longest label set the panel's intrinsic width; the same latent bug sits under every other one. Anchor an overlay panel to the **viewport** (`inset: … 0 auto 0`, `max-width: 100vw`, `box-sizing: border-box`) and let the labels wrap. A drawer whose width is a function of its content is a drawer whose correctness is a function of the data.
- **A list with no pagination, no filter and no search is not a list, it is an archive dumped on a page.** Measured on a live disclosure portal: 387 items in one section, **83,703px** of document (93 viewport-heights), 6,429 DOM nodes, zero controls. The primary task on that surface is "find the release about X"; the only route to it was the browser's own find-in-page. The threshold is not a number of items, it is whether the user's task is *browse* or *find* — the moment it is *find*, the page owes at least one of: a search box, the facets the data already carries (year, category, type), or progressive disclosure that keeps the first paint bounded. Look for the pattern already in the product: the same build collapsed 836 documents into ten closed `<details>` shelves on another page and never applied it here.

## Hierarchy tactics while implementing (Refactoring UI, UX-relevant core)

- Hierarchy via **weight and color before size**: dark ink for primary, medium gray for secondary, light gray for tertiary — three levels, not a font-size zoo. (But keep body ≥4.5:1 — "de-emphasized" never means "fails contrast".)
- **De-emphasize the neighbors instead of emphasizing the star** — often the cleaner fix for a competing element.
- **Labels are a last resort**: format data so it self-describes ("12 left in stock" beats "Quantity: 12"); when labels are needed, they're the de-emphasized part.
- **Actions carry hierarchy**: one solid high-contrast primary; secondary as outline/ghost; destructive as text-level unless it's the page's purpose. Three buttons of equal weight = no decision made.
- **Design for the real content distribution**: 1 item, 40 items, a 60-character name, a missing avatar. If the layout only works with the demo data, it doesn't work.
