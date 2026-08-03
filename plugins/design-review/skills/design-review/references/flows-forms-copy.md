# Flows, forms, copy

Tier 2. Judged, evidence-required.

## Walkthrough discipline

Per key task, walk every step asking four questions. A "no" is a locatable failure.

1. **Motivation** — does the user realise they need to act here at all? A no here is most severe: they won't even try.
2. **Visibility** — is the control findable, or buried and styled like body text?
3. **Understanding** — does the label predict what happens?
4. **Feedback** — after acting, do they know it worked?

Rate each step: pass / hesitation (one no) / failure (two or more — expect abandonment).

## The lens pass

Run these yourself in one pass by default. A screen, form or single flow is one reading, and the lenses inform each other as you go. Fan out only when scope genuinely exceeds one pass.

A finding two lenses catch independently is almost always real and ranks higher.

| Lens | Ask | Typical catches |
|---|---|---|
| **Scanning** | Is every screen self-evident? Trunk test: dropped here with no context — what site, what page, what sections, what can I do, where am I? Can half the words go? | Unclear page identity, wall-of-text, clickability ambiguity, needless steps |
| **Interaction** | Can users perceive what's interactive (affordance + signifier)? Does every action produce immediate feedback? Does the layout build a correct conceptual model? Do constraints prevent errors? | Dead-looking buttons, silent actions, mystery icons, mode confusion |
| **Heuristics** | Status visibility, real-world language, control and freedom (undo, exits), consistency, error prevention, recognition over recall, expert shortcuts, minimalism, error recovery, contextual help | Missing loading states, jargon, no way back, inconsistent components |
| **Structure** | Does the IA make content findable, does layout serve the task hierarchy, does visual design reinforce rather than fight structure? Diagnose at the *lowest failing plane* | Navigation mirroring the org chart, polished screens for the wrong task |
| **Mobile** | Works at 360px without horizontal scroll? Content prioritised? Targets ≥44pt with ≥8px gaps? One-thumb reachable primaries? Performance on a slow connection? | Desktop-first cramming, tiny targets, hover-dependent features |
| **Accessibility** | The gate set. Separate "can assess visually" from "needs implementation verification" — never claim conformance from a screenshot | Grey-on-white text, placeholder-as-label, missing focus rings, red-only errors |
| **Cognitive load** | Intrinsic load (the task — leave it) vs extraneous (the design — cut it). Squint test, 3-second test, subtraction test, memory test. What could the product do *for* the user: compute, remember, default, infer? | Competing CTAs, decorative noise, re-entering known data, mental math |
| **Ethics** | Alignment, sincerity, golden rule. The fluency trap: polished surface plus unverifiable claims | Fake urgency, pre-checked consent, confirmshaming, asymmetric cancel flows |
| **States** | Every component's interaction states; every screen's nine states | The states nobody designed |
| **Words** | Labels in the user's language, errors say what plus how-to-fix, buttons say outcomes, empty states educate and point | "Submit", "Invalid input", blank empty states |

Per heuristic, require either positive evidence or a documented issue. Missing evidence is itself a review failure.

## Techniques that sharpen findings

**Count, don't characterize.** "The cancel flow takes 12 clicks against a 2-click signup." "The same 'Remind me later' button appears 4 times." "This card carries 5 different signal colours." Counts are reproducible, stakeholder-legible, and harder to argue with than "feels cluttered". Where a finding can be a number, make it one.

**Compensation artifacts as evidence.** Legacy-version URLs kept alive, "recently visited" widgets promoted to primary navigation, a leaner mobile skin quietly fixing what desktop won't, rolled-back redesigns. These are the team's own engineering acknowledging the diagnosis — they often answer the review's central question before the surface critique begins.

**Internal state leaking into the UI.** Pricing tiers with mixed units, composite labels exposing an internal matrix, role-permission grids used as navigation. The system needs its cartesian product; the user needs a flat, decidable surface. One such element often violates load, fluency, honesty and decision clarity simultaneously.

**Verify your own measurements.** Counts sitting at suspicious boundaries — exactly 10 of something, font-family counts inflated by fallback stacks, broken images that are file-path artifacts — are often tool noise. Reconcile before reporting.

**Polish does not compensate for structure.** A visually cohesive surface with a broken flow is beautiful-but-broken, and the visual score must not drag the verdict up. On a surface with manipulative mechanics, polish actively *raises* the trust the manipulation then spends — flag high-polish plus low-honesty as a priority finding, not partial credit.

## Flow architecture

A flow is a promise: do these steps and you'll get X. Check the promise first.

- **Named completion signal.** What does the user have when done, and how do they know? Flows ending in a silent redirect fail at the moment users remember most
- **One decision per step.** A "thing" is a conceptual unit, not a field — first+last name is one thing; a shipping address is one thing. Bend for expert tools; never bend for checkout, registration, or anything on mobile
- **Position and size shown** for 3+ steps, with meaningful step names. Only *earned* progress — a fabricated head start is a dark pattern
- **Every exit mapped before the happy path**: Back (preserves entered data — losing it is a High finding), Cancel (with a named consequence), Abandon (auto-save drafts), Resume (return with context re-displayed, never quizzed from memory)
- **Eliminate excise** — any step serving the system rather than the user's goal. Forced account creation before value, re-entering known data, confirmation of non-destructive actions
- **Progressive commitment** — ask for information at the moment it's needed and justified, not upfront. Each early field costs conversions

Flow-level questions: could any step be removed, merged, defaulted or deferred? Is anything asked twice (WCAG 3.3.7 makes this a formal criterion)? What happens on failure at each step — is prior work preserved? Does the final screen say what happened *and* what happens next?

**Interrupted journeys.** Users don't finish in one sitting. Auto-save without asking; state the expiry policy for drafts; design re-entry deliberately — recognition of prior progress, a summary of previous choices re-displayed, one tap to resume, and the option to start over.

**First-run.** Value first: show what the product does with populated sample data before demanding setup. Teach by doing with just-in-time guidance at the moment a feature becomes relevant — never a five-slide tour, never mandatory profile completion before any value.

## Forms

Only 48% of desktop sites and 38% of mobile sites reach "decent or good" product-page and form UX (Baymard 2026 benchmark). The failures are consistent enough to check directly.

**Fields**
- The best field is no field: infer (country from locale), default (date = today, quantity = 1), or compute (totals) instead of asking
- Visible label above every field. Never placeholder-as-label — it disappears on focus, has low contrast, and breaks autofill and screen readers. Placeholders are format examples only
- Single column. Group related fields; the gap inside a group must be smaller than the gap between groups or grouping collapses
- Mark required fields; better, cut optional ones. If a form has 20 fields but 6 matter for this user, conditionally show 6
- Right input type per field — drives mobile keyboards and autofill. `autocomplete` attributes are an accessibility criterion in 2.2
- More than 10 visible inputs is a chunking finding. 18% abandon carts due to length
- `<select>` for fewer than 6 variations is a failure — 57% of sites do this. Use exposed radio groups or button-like selectors
- Splitting one semantic value across fields (country code / area code / number) breaks browser autofill. Single `<input type="tel">`

**Validation timing**
- Validate on **blur after edit**, never on focus or first keystroke. "Why are you telling me my email is wrong, I haven't finished typing it"
- Once a field is invalid, re-validate on every `input` event so the error clears the instant the value becomes valid — don't make the user blur again to dismiss it
- Real-time only where the user is building toward a visible goal: password strength, character count, username availability
- Cross-field rules on submit

**Styling and API correctness**
- Style via `:user-invalid`, never `:invalid`. `:invalid` matches required-but-empty fields on page load — red borders before the user touched anything is the loudest "validation added without testing" tell
- On submit, an error summary at the top: heading-led container ("2 problems"), anchor links to each invalid field, `tabindex="-1"`, rendered then focused with `.focus()`. **No `role="alert"` on the summary** — a moved-focus target plus an alert role double-announces. Reserve `role="alert"` for inline per-field errors appearing without focus moving
- Specific, adaptive messages. "Phone number is too short" beats "Provide a valid phone number" — the validator already knows which subrule fired, and surfacing it cuts re-submit attempts. Ship 4–7 distinct messages for each complex high-traffic field (email, phone, card, postal code)
- Preserve user input across failure
- Numeric fields: `type="text" inputmode="numeric" pattern="[0-9]*"` for ZIPs, OTPs and card numbers — never `type="number"`, which adds spinners, strips leading zeros and applies locale-decimal handling
- No email-confirm fields — retype-to-catch-typos fails WCAG redundant entry. Never block paste, especially on password and verification-code fields. Support password managers
- `setCustomValidity('')` clears a custom error; `null` does not
- `form.requestSubmit()` honours validation; `form.submit()` silently skips it
- Submit disables and shows progress during async, preventing double-submit

**Smart defaults ethics.** A default is good if ~80% of users would pick it anyway; it's manipulation if it primarily benefits the business. Pre-checked marketing consent and pre-selected premium tiers are defects, and pre-checked consent is illegal under GDPR rather than merely rude.

## Navigation and IA

**Wayfinding trio** at every moment: orientation (where am I — highlighted nav item, page title, breadcrumbs at 3+ levels), route decision (labels informative enough to choose without clicking), closure (the landing page's title matches the link that promised it — a "Privacy Settings" link landing on "Account Management" is a closure failure).

- Navigation reflects user mental models, not the org chart. Labels use the user's words
- Back restores scroll position, filters and input
- Current location always visibly marked; primary nav placement identical on every page
- Format labels ("Resources", "Hub", "Library") describe containers, not contents — they force click-and-check
- Zero results is a design problem, not an edge case: spelling suggestions, broaden-filter offers, popular items, a path to browse
- Nav taller than 80px or wrapping to two lines at desktop is a finding; 64–72px is the healthy default

## Copy

Words are the interface's densest material. A one-word button change moves conversion more than most redesigns.

**Ground rules**
- Omit needless words. Cut half, then cut half of what's left
- The user's language, never the org's. Unavoidable technical terms defined in context on first use
- Front-load meaning. The first two words of every heading, link and list item carry the scan
- Active voice, present tense, direct address. Passive only for system states
- Sentences 15–20 words, one idea each

**Banned-word discipline** — marketing-inflation words are noise in an interface: *seamless(ly), effortless(ly), powerful, robust, leverage, unleash, blazing/lightning-fast, turnkey, holistic, best-in-class, next-generation, cutting-edge, world-class, streamline, elevate, harness, empower, revolutionary, synergy, utilize, myriad, plethora*. Also the invisible fillers (*just, simply, actually* — "simply click" insults anyone who found it hard) and the hedges (*Consider…, You may want to…, It is important to note…*).

**Generated-copy tells to lint out**: significance inflation ("crucial", "critical" on routine things); sycophancy ("Great question!"); filler openers; template closings ("The future of X is bright"); vague authority ("experts say"); "not only X but also Y" parallelism; artificial "from X to Y" scale claims; rule-of-three synonym churn — repeating the *same* word is natural, rotating synonyms to avoid repetition reads as machine.

**Patterns**
- **Buttons** say the outcome: "Save changes", "Send invitation", "Start free trial" — never "Submit", "OK", "Yes". Paired buttons: the safe action is never styled to be mistaken for the destructive one, and neither is labelled so vaguely that the pair is a riddle ("Cancel" the subscription vs "Cancel" the dialog)
- **Labels** are nouns the user would say. Status labels are states ("Sent", "Draft"); action labels are verbs ("Send", "Archive"). One term per concept, enforced everywhere — "workspace" on one screen and "project space" on another reads as two features
- **One name per action through the whole flow.** The button that says "Publish" produces a toast that says "Published"
- **Errors** = what happened + how to fix, both. "That email is missing an @ — like name@company.com" beats "Invalid input". Never blame
- **Confirmations** = what happened + what to expect next. "Success!" alone answers neither
- **Empty states** = education + action + motivation
- **Tooltips** explain unfamiliar concepts, never carry essential information — invisible until triggered, hostile on touch
- **Destructive dialogs** name the object and the consequence: "Delete 'Q3 board pack' and its 12 files? This can't be undone." Buttons repeat the verb ("Delete pack" / "Keep pack"), not Yes/No

**Tone check.** The tell of broken tone: celebration in an error, cleverness in a security notice, legalese in onboarding. Humour is highest-risk in the states where users are already frustrated — never joke in an error message.

## Mechanisms worth citing

Cite the mechanism, not the name. "Cutting visible options from 9 to 4 shortens the decision" persuades; "Hick's Law!" doesn't.

- Working memory holds ~3–5 chunks. Extraneous processing — visual noise, redundant choices, inconsistent styling — spends those slots even when unattended. Implication: ≤5 content blocks above the fold, ≤7 top-nav items, ≤4–7 visible form fields per step
- Visual-appeal judgments form in ~50ms and are stable on re-test. Attractive interfaces are *perceived* as more usable — a halo that buys forgiveness downstream, which is why polish is not cosmetic
- Easy-to-process content is judged more *true*. Users can't articulate fluency failures — they say "something feels off" and leave
- Losses weigh roughly 2× gains, but only when the loss is real
- Decision time grows roughly logarithmically with option count — simplify *decision points*, not entire workspaces
- Acquisition time grows with distance and shrinks with target size
- Users navigate by information scent: labels must predict what's behind them
- Experiences are remembered by their peak and their end. Invest in the success moment and the exit, not evenly
- Response under ~400ms keeps the loop tight; feedback within ~100ms feels instant

**Evidence calibrations** — where the headline overstates the finding, and worth knowing before citing:

- Nudge effects are much weaker than popular accounts suggest; meta-analytic corrections put the average near zero. The *structural* claims survive — defaults matter, framing matters, there is no neutral presentation — but don't promise conversion lifts from re-ordering options
- Choice overload is context-dependent, not universal. Reduce options at decision points; never thin out expert tool palettes, where density is a feature
- Aesthetic-usability has limits: severe usability failures override the halo, and it erodes with repeated use
- The research base is WEIRD. The architecture (working-memory limits, 50ms judgments, fluency) is expected to be universal; the *calibration* is cultural — what signals trust, how much density is comfortable, which conventions are predicted

## Connect three links

Every finding that cites a mechanism connects **observation → mechanism → consequence**:

> The form shows 11 fields at once *(observation)*; simultaneous options compete for 3–5 working-memory slots and choice latency grows with count *(mechanism)*; expect abandonment concentrated on this step — split into 3 grouped steps with a progress indicator *(consequence and fix)*.

A mechanism without an observation is a lecture. An observation without a mechanism is an opinion.

## AI-facing surfaces

When the surface under review is itself an AI feature, add these checks:

- Scope of what the AI acts on is visible before it runs; autonomy level (suggest / ask / act) is explicit
- Preview before commit on anything modifying user content; AI output marked until accepted
- Bulk runs sampled first — 2–3 records verified at full quality before applying to the rest
- Friction matches blast radius: verification only for real loss (money, work, reputation, security); undo for the rest
- Stop always available, always in the same place
- Empty state scaffolds the first prompt — 3–6 contextual suggestions, never a bare box
- AI involvement disclosed with verbs ("Summarized with AI"), not a bare sparkle
- Retrieved content treated as untrusted: sources visible, tool actions gated on previews, per-source kill switch
- Memory visible, editable, deletable
- Cost shown before long or bulk runs
- Cancel and opt-out paths no harder than their opposites

A silent overwrite of user work, or an undisclosed autonomous action, is a Blocker.
