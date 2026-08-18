# States and resilience

Shipping only the populated state is the most reliable failure in AI-generated UI. This is the highest-leverage pass in the review.

## The nine screen states

Per data surface. For each: what does the user see, what can they do, how do they recover or progress.

| State | What to check |
|---|---|
| **default** | With *normal* data. Decide what normal means for this surface |
| **empty** | Distinguish first-use, cleared-by-user, and no-results. See below |
| **loading** | Matched to expected duration. See thresholds below |
| **partial** | Some loaded, some pending, one widget failed. The most overlooked state and one of the most common in real use. Design the messy middle |
| **error** | What happened, is my data safe, what do I do now |
| **success** | What happened *and* what happens next |
| **offline** | What's cached, what degrades, how the user knows, what happens to actions attempted offline — queued or lost |
| **disabled** | With a discoverable reason. Unexplained disabled controls are a top frustration |
| **overflow** | 10,000 items in a list designed for 50; a 200-character name; 999+ badges |

Two other counts circulate (five states, six states). Nine is the superset; use it and mark any that genuinely do not apply.

## Component states

default → hover → focus-visible → active/pressed → disabled → loading.

- **hover** is never load-bearing. No touch equivalent. Anything essential behind hover is invisible on half of devices
- **focus-visible** is distinct from hover. Keyboard users live here
- **active/pressed** wants feedback within ~100ms, or the tap feels dropped and the user taps again — the double-action bug
- **disabled** must look different from both default and hover, and carry a reason (tooltip, inline message, `title`). Dim in place; never disappear — layout stability matters more than tidiness
- **loading** disables the control immediately on click (the double-submit bug is a state-machine failure), replaces the label with a spinner or "Loading…", and restores on completion

Every clickable element gets `cursor: pointer` on the web. Clickable cards and rows are the usual omissions; a `<div onclick>` with a default cursor reads as static content.

Don't use opacity reduction as a button's hover state — it makes the button look disabled.

## Loading, matched to duration

| Wait | Treatment |
|---|---|
| < 300ms | Nothing. Enforce a debounce or delayed render, or the indicator flickers |
| 300ms – 2s | Spinner, placed inline with the action that triggered it |
| 300ms – 10s | Skeleton for content surfaces. The skeleton's DOM must mimic the final render's shape, or it causes the layout shift it was meant to prevent |
| 2 – 10s | Skeleton matched to layout, or a labelled spinner ("Loading payments…") |
| 10 – 30s | Determinate progress with cancel |
| 30s+ | Offer an alternative ("we'll email you when it's ready") |
| 60s | Stop animating; show an error with retry |

Never an indefinite spinner with no information. Start a timeout on every request.

**Never fake progress.** An honest spinner beats a progress bar that lies; a fabricated percentage is a sincerity violation users eventually catch.

**Retry timing:** first retry fires immediately on click, then exponential backoff (2s, 4s, 8s). After three failures, swap "Retry" for "Contact support" plus a copyable error ID — the user has done their job and the system now needs a human.

**Skeleton vs spinner vs optimistic:**

- Skeleton previews structure — use for feeds, dashboards, initial page loads
- Spinner indicates activity without previewing — use for short blocking actions
- Optimistic UI updates instantly, assuming success — only for binary, low-risk, high-success actions (like, favourite, reorder). It must include a rollback path and a visible error, never a silent revert. Never optimistic for money, destructive actions, or anything affecting other users

**Auditing a skeleton is a two-capture measurement, not a look.** Capture the surface loading and resolved, then diff them. Seven findings live here, and each has reached a real user through a review that only looked at the loading state on its own:

| Check | How to measure | Finding when it fails |
|---|---|---|
| Size parity | `getBoundingClientRect()` on the skeleton node and on the element that replaces it | Layout shift on resolve; report with both heights and the CLS it causes |
| Shape parity | Child count and internal structure of the skeleton subtree vs the resolved subtree | One flat block standing in for three stacked elements is a slot placeholder, not a content placeholder |
| Ground match | Skeleton fill against the `background-color` of the surface it sits on | Grey blocks on a coloured or dark ground read as breakage, not as loading |
| Animation present | `getAnimations()` on the skeleton node | A static block is indistinguishable from a broken image or a failed fetch. **Unavailable on Obscura: `getAnimations()` returns 0 whatever the page declares, and `prefers-reduced-motion` cannot be emulated, so both halves of this row are `cantTell` rather than failures.** Record them as skipped; a static skeleton here is the engine, not the page |
| Clears per section | Capture mid-resolve, not only at the two endpoints | A skeleton still painted under resolved content reads as stuck; section headers usually resolve first and should stop being skeletons first |
| Stack separation | Vertical gap between sibling skeleton blocks | Below ~1–2px a run of blocks reads as one large block |
| Not over-applied | Which skeleton nodes correspond to elements whose content is static | A skeleton on a button, nav item or fixed heading invents a loading state for something that was never loading |

**Coverage, not just quality.** Enumerate the surface's async actions — record, save, upload, generate, submit, delete, refresh — and check each has its own in-flight, success and failure treatment. A surface offering only the ideal state and an empty state is incomplete however good the ideal state looks; *"nothing shows when I record an asset … the states are all static or empty states"* is the shape of that report when the user writes it instead of the review.

## Empty states

The product's first impression, and most products waste them. `data.length === 0` rendering a bare `<div>` is a defect, not a state.

Anatomy: a non-interactive contextual image or icon, a concise positively-framed title, and body text naming the next action. Plus the primary button.

Formula: **what this area is for** (education) + **how to create the first item** (action) + **why it's worth it** (motivation).

Four distinct empties, and they are not interchangeable:

1. **First-use** — the onboarding moment. Headline, value sentence, primary CTA
2. **Cleared-by-user** — celebratory phrasing, next action
3. **No search results** — echo the query, suggest alternatives, offer to clear filters or broaden. Never a bare "No results found"
4. **Pre-query search** — never blank. Recent searches, trending items, or suggestions

Never collapse error into empty. An error carries recovery information an empty does not.

The term for what a bad empty state produces: **void anxiety** — the user cannot tell whether the absence means a system error, a lack of permission, or their own success.

## Errors

Inline, below the field, appearing on blur-after-edit or on submit. Adjacent to the problem, linked with `aria-describedby`, never colour-only, never blaming.

Answer three questions in order: what happened ("Your card was declined", not "Something went wrong"), why if knowable, what the user can do now.

**Preserve user input across the failure.** A form that clears on submit error forces re-entry and is a direct abandonment cause.

Snackbars and toasts for transient, peripheral errors only — never for critical or persistent faults.

**Partial failure degrades locally.** When one microservice fails while the main UI loads, show a localised error or fallback component rather than breaking the whole page render.

**Permission-denied** gets neutral messaging plus a passive link to settings ("To use the camera, enable access in your device settings"). Persuasive or emotional re-prompting after a denial gets applications rejected under Apple guideline 5.1.1 — and it is hostile regardless of platform.

**`novalidate` removes a state machine; it does not remove the need for one.** Turning off native validation to control the styling is normal. Shipping nothing in its place is the defect, and its signature is that the *only* reachable state is the terminal one. Measured on a real form: three empty fields, submit, and the user lands on "Not sent — your text is still in the field above" when there is no text in any field. No field-level error, no required-field signal, no distinction at all between empty, invalid and submitted. Drive every form with an empty submit as a matter of course; a form whose empty submit and valid submit produce the same screen has one state.

**A live region inserted at the moment of the announcement usually does not announce.** Assistive technology observes an existing `aria-live` / `role="status"` container for mutations. A node that is *created* carrying `role="status"` and inserted with its text already in it frequently arrives as one atomic change with nothing to observe, and the message is silently dropped. Render the region empty and permanently, then write text into it. In a render this looks identical to a working one, so check the DOM before and after the submit rather than the after alone.

## Stress prompts

Run against every screen. These are where the real defects are.

**Content** — 3-character title? 300? Emoji-only? A name that's "O", or 40 characters, or 200? RTL text? A URL pasted into a text field? Completely empty?

**Volume** — 0, 1, 3, 50, 10,000 items? Every badge at 999+? All sections expanded at once?

**Time** — API answers in 200ms? 5s? 30s? Never? User leaves mid-flow and returns next month? Session expires mid-step?

**Network** — drop mid-upload? Mid-payment? 2G? Intermittent, 10s up and 5s down?

**Behaviour** — double-click? Browser Back mid-flow? Same flow open in two tabs? Paste instead of type? A shared link to an auth-required state?

## i18n and text expansion

Translated text is almost always longer. German and Finnish routinely expand 35–50%.

| Component | Typical English | Buffer needed | Check |
|---|---|---|---|
| Buttons and CTAs | 15–25 chars | +50% | Flag `width` / `max-width` on buttons; require padding-based intrinsic sizing |
| Headings | 30–60 chars | +35% | Flag `white-space: nowrap` without an ellipsis safeguard |
| Error messages | 50–70 chars | +30% | Ensure multi-line wrapping; flag fixed heights on error containers |
| User-generated names | up to 200 chars | n/a | Require `word-break: break-word` or truncation with a tooltip fallback |

Designing to strict character limits is an anti-pattern — it harms both accessibility and localisation, and produces truncation that obscures meaning.

Never concatenate strings for display ("You have " + n + " messages" breaks in most languages — use ICU plural formats). Never bake text into images. Dates, numbers and currency formatted per locale, stored in ISO. Give translators context in string keys (`button.save_changes`, not `string_47`).

## Viewport and zoom resilience

- Adapt without loss of function down to **320×256** minimum
- Browser zoom to **400% at a 1280px-wide screen** without breaking
- Relative units (`rem`, `em`) in media queries and font sizing rather than fixed `px`, so OS font-size preferences are respected
- Dynamic Type / font scaling to at least 200% without truncation or overlap — test at the largest setting, not the default
- `min-h-dvh`, never `100vh` — `100vh` overflows under mobile browser chrome
- Body text ≥16px on mobile web, below which iOS Safari auto-zooms form inputs
- No horizontal scroll at 360px, with the longest real heading and its German translation

## Spatial consistency

- No layout shift after load
- No auto-rearranging content "for" the user
- Muscle memory respected — controls stay where they were
- Meaningful states have URLs: filters, tabs, pagination in query params, so refresh and share work
- State survives refresh
- Back preserves scroll position, filters and half-entered input. Breaking Back is breaking the user's most-trusted button

## Undo and destructive actions

**Don't confirm reversible actions.** Routine "Are you sure?" trains click-through blindness and devalues the confirmations that matter. Provide undo instead — a toast with a 5–10s window, version history for documents, trash-with-schedule for deletion.

Undo lives at the **data layer** — soft-delete by default — not only as a UI toast.

Friction proportional to blast radius, for the genuinely destructive:

1. Visual distinction — danger styling, spatially separated from safe actions
2. Confirmation naming the consequence ("Delete this project and all 47 files in it?"). Generic "Are you sure?" carries no information
3. Type-to-confirm for severe, rare actions
4. Cooling period for the gravest ("Account deletes in 14 days; cancel anytime before")

Always name what will be lost, show it where possible, and offer the lighter alternative ("Archive instead?").

## Symptom catalogue

Some UI defects have a known code cause. Report them as the user-facing defect and route the code fix separately.

- An input that loses focus on every keystroke, an animation that restarts, or scroll position resetting mid-interaction — usually a component being re-created on each render
- A stray literal `0` rendered in the UI — the `count && …` falsy-render bug
- Dropdowns clipped by an ancestor — `position: absolute` inside `overflow: hidden`/`auto`. Fix with the popover API, `position: fixed`, or a portal
- Background scrolling behind a modal — missing `overscroll-behavior: contain`
- A weak modal scrim — 40–60% black is the range where the dialog actually separates from the page
- Double-tap zoom delay on tappables — missing `touch-action: manipulation`
