# Interaction States Pass

Verify every interactive element has a complete set of states (default, hover, active, disabled, focus) plus appropriate transitions and feedback. Add what's missing.

**Interactive elements without state feedback feel broken.** A button without a hover state looks like a label. A disabled button that looks enabled feels broken when nothing happens on click. A removed focus ring locks out keyboard users.

This skill is the safety net before a design is shown to users.

## Phase 1: Identify interactive elements

Walk the design and inventory every interactive element:

- **Buttons** — `<button>`, anything `role="button"`, anything that calls a click handler
- **Links** — `<a>`, anything that navigates or opens external content
- **Form inputs** — `<input>`, `<textarea>`, `<select>`, file pickers, range sliders, color pickers
- **Toggles** — checkboxes, radios, custom switches
- **Cards or rows that act as links** — clickable rows in a table, clickable cards in a grid
- **Navigation items** — tabs, sidebar links, breadcrumbs
- **Custom widgets** — dropdowns, accordions, modals, popovers

Two structural checks while inventorying overlays: a dropdown/menu rendered with `position: absolute` inside an `overflow: hidden`/`auto` container **will be clipped** — use the popover API, `position: fixed`, or a portal to escape the container. And a modal scrim needs to actually isolate the foreground: typically 40–60% black — a weak scrim leaves the background visually competing with the dialog.

For each element, verify the full state set in Phase 2.

## Phase 2: Per-element state verification

For each interactive element, check all six aspects below. Flag everything you find, including borderline cases — note a confidence level rather than silently dropping a finding you're unsure about.

### 1. Default (resting) state

The element looks clearly interactive at rest: buttons have background fill, border, or both — distinct from body text; links are obviously links (color + underline, or a clear visual treatment); form inputs have visible borders or fills. **Every clickable element gets `cursor: pointer`** (web) — clickable cards, rows, and custom widgets are the usual omissions; `<div onclick>` with a default cursor reads as static content. Flag elements that look like static text and only reveal interactivity on hover — some users will never hover (touch devices, keyboard users).

### 2. Hover state

Visual change on cursor over. At minimum a color shift. Better: color + shadow + slight transform (`translateY(-2px)`). Flag missing hover states. Don't use opacity reduction as the hover state for buttons — it makes them look disabled.

### 3. Active / pressed state

Visual change while clicking — typically a darker color, a slight scale-down (`transform: scale(0.98)`), or a return-to-baseline if hover lifted the element. The active state confirms the click registered before the action completes.

### 4. Disabled state

Clearly disabled: lower opacity (~0.6), no hover effect, `cursor: not-allowed`, neutral or muted color. The disabled state must look different from both default and hover. If a button is disabled because the user hasn't met some condition (e.g. "fill all required fields"), provide an indicator of *why* — a tooltip, an inline message, or a `title` attribute. A silently disabled button is a frustration trap.

### 5. Focus state

Visible focus ring for keyboard users. Use `:focus-visible` over `:focus` so the ring shows for keyboard navigation but not on every mouse click. Required: the ring is visible against the adjacent background (3:1 contrast minimum); the ring is at least 2px thick, with 2px offset; `outline: none` is **never** used without a replacement.

### 6. Loading state (for elements that trigger async work)

For buttons that submit forms, save data, or wait on a network call: disable the button immediately on click (prevent double-submission); replace the label with a spinner or "Loading…" text; re-enable and restore the label on completion. For elements that fetch data on render: a skeleton, spinner, or progress indicator while waiting.

#### Skeleton discipline

A skeleton is a design of the content it stands in for, and this is the state most often shipped as a grey box. Seven checks, each one a defect that has been caught by a reviewer rather than by this pass:

1. **It matches the real content's size.** Load the surface twice and compare: the skeleton card and the resolved card have the same height and width. A mismatch guarantees a layout jump, and it is the same defect whether the skeleton is too small or the mock is too big.
2. **It matches the real content's shape.** Card skeletons have the card's radius and internal block structure; a text skeleton has the line count and last-line raggedness of real copy. A single flat rectangle where three stacked elements will appear is a placeholder for the *slot*, not for the content.
3. **It sits on the surface the content will sit on.** Grey blocks dropped on a coloured or dark ground read as breakage. Derive the skeleton fill from the surface token it covers, not from a global grey.
4. **It moves.** A static block is indistinguishable from a broken image or a failed fetch. A shimmer or pulse on a 1.2–2s loop says "still working"; it also needs `prefers-reduced-motion` handling, where the honest fallback is a static block plus visible text, not silence.
5. **It clears per section, as that section resolves.** A skeleton still visible under content that has already painted is worse than no skeleton — the surface reads as stuck. Section headers in particular usually resolve first and should stop being skeletons first.
6. **Skeletons in a stack are separated.** A run of blocks with no gap reads as one large block; 1–2px minimum between them, and shrink the blocks to make room rather than growing the stack.
7. **Static things get no skeleton at all.** A button, a nav item, or a section heading whose content does not depend on data should simply be there from the first paint. Wrapping the whole page in skeletons because part of it is async invents a loading state for elements that were never loading.

**Every async action gets one, not just page load.** Recording, saving, uploading, generating, submitting, deleting, refreshing — each needs its own in-flight, success and failure treatment. A surface where every state is either the ideal one or an empty one is not finished, however good the ideal one looks.

## Phase 3: Verify transitions

Every state change should be smoothly transitioned, not snapped:

```css
button { transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease; }
```

Check durations: **0.15–0.3s** for state changes (hover, focus, active) — feels responsive; **0.3–0.5s** for entry/exit (modals, drawers, toasts) — feels composed; **avoid** transitions slower than 0.5s for micro-interactions (laggy); **avoid** transitions of 0s or no transition (state changes feel broken). Wrap motion-heavy transitions in `@media (prefers-reduced-motion: reduce)` to shorten or remove for users who prefer reduced motion.

## Phase 4: Verify feedback for actions

For every action, the result should be visible: **form submission success** (toast, inline message, or redirect with confirmation); **form submission failure** (clear error, tied to the field if field-specific); **validation errors** (appear when the field loses focus or on submit; cleared when the user fixes the issue); **state changes** (toggle on/off, item added to a list → immediate visual change, optionally with a brief animation).

Flag silent successes ("user submitted, page does nothing visible") and silent failures ("user submitted, nothing happened, no error shown") — both feel broken. For state visibility: the current page or tab in navigation is visually distinct; selected items in a list are visually distinct; active filters or sorts are visually distinct.

### Form validation discipline

- **Timing: first blur after edit, then per-keystroke.** Run the field's constraint when the user blurs after editing — never on focus or first keystroke ("why are you telling me my email is wrong, I haven't finished typing it"). Once a field is invalid, switch to re-validating on every `input` event so the error clears the instant the value becomes valid — don't make the user blur again to dismiss it.
- **Style via `:user-invalid`, never `:invalid`.** `:invalid` matches required-but-empty fields on page load — red borders before the user touched anything is the loudest "validation added without testing" tell. `:user-invalid` matches only after the user has blurred with bad input or submitted.
- **On submit, an error summary at the top.** A heading-led container ("2 problems") with anchor links to each invalid field and `tabindex="-1"`; render it into the DOM, then move focus to it with `.focus()`. **No `role="alert"` on the summary** — a moved-focus target plus an alert role double-announces. Reserve `role="alert"` for inline per-field errors that appear without focus moving.
- **Specific, adaptive error messages.** "Phone number is too short" beats "Provide a valid phone number" — the validator already knows which subrule fired; surfacing it cuts re-submit attempts. Ship 4–7 distinct messages for each complex high-traffic field (email, phone, card, postal code). And **preserve user input across the failure** — wiping fields on an unrelated error is a direct abandonment cause.
- **Numeric fields:** `type="text" inputmode="numeric" pattern="[0-9]*"` for ZIPs, OTPs, and card numbers — never `type="number"`, which adds spinners, strips leading zeros, and applies locale-decimal handling.
- **Respect the user's tools.** No email-confirm fields (validate the one field; retype-to-catch-typos fails WCAG redundant-entry); never block paste, especially on password and verification-code fields; support password managers.
- **API correctness:** clear a custom error with `setCustomValidity('')` — `null` does not clear it. Submit programmatically with `form.requestSubmit()`, which honors validation; `form.submit()` silently skips it.

## Phase 5: Apply fixes

For each missing state or feedback element, add it. Use the design system's tokens for colors and timings. If the design system doesn't define something, use sensible defaults:

- Hover: 10–15% darker than the default (or `color-mix` if the design uses modern CSS)
- Active: another 10% darker, or `transform: scale(0.98)`
- Disabled: opacity 0.6 + `cursor: not-allowed`
- Focus: `outline: 2px solid var(--color-primary); outline-offset: 2px`
- Transition: `0.2s ease`
- Clickable anything: `cursor: pointer` + `touch-action: manipulation`

For elements where the right state isn't obvious (e.g. a toggle button — what's the active vs inactive vs hover-on-active state?), make a judgment call and note it in the summary.

## Phase 6: Summarize

Report: interactive elements inventoried; missing states added (counts by category — hover / active / disabled / focus / loading); transitions added or normalized; feedback added (toasts, error messages, loading indicators); any judgment calls the user should review.
