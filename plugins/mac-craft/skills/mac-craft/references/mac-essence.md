# The Essence — what actually makes a great mac app great

The synthesis the whole corpus was built to answer. 135 curated apps, the UX canon (Krug, Norman, Yablonski, Wathan & Schoger via ux-craft), design-craft's philosophy, and Apple's eight principles converge on a small number of convictions. Read this before designing; use its vocabulary when critiquing. Everything here is evidenced — corpus statistics cited where they exist.

## The one-sentence answer

A great mac app **borrows the platform's trust and spends it on exactly one idea of its own** — native grammar everywhere, one committed signature, and obsessive completeness in the places users only notice when they're missing (states, keyboard, copy, dark mode).

## The eight convictions

**1. Familiarity is the canvas; the signature is the painting.**
The corpus's psychology profile is unambiguous: the two most-exploited laws across 134 apps are Von Restorff (one salient thing — 132 apps) and Jakob's law (look like what users already know — 111 apps). They only work *together*: isolation needs a calm field to stand against, and that field is native grammar. Apps that deviate everywhere have no way to emphasise anything. Design-craft's "spend your boldness in one place" is the same law from the craft side. *Practice: native floor first, then exactly one committed departure — the declared signature.*

**2. Restraint reads as confidence; density reads as respect.**
The best-scoring corpus apps de-emphasise instead of amplify (85/50/25 ink tiers — canon rule #1) and hold a single-accent budget (canon #2). Desktop density (13pt body, 24pt controls) tells a pro user "we know your time is precious"; inflated iOS density on the Mac tells them the app was ported, not made. Aesthetic-usability (108 apps) is earned through *coherence*, not decoration — users read consistency as quality before they can articulate why. *Practice: when in doubt, quieter and denser; emphasis by removing weight from everything else.*

**3. The app should answer its question before it's asked.**
The corpus is glanceability-obsessed — the strongest cluster identities (Menu-bar Instrument, Notch Native) are apps whose entire body answers one question in under a second (a 36pt tabular figure, a coloured status). That's Krug's law at mac scale: every moment spent parsing the interface is a cost. Hick's law showed up in 60 apps as ruthless choice-reduction. *Practice: name the surface's single question; promote its answer to the visual hero; cut or demote everything that competes (design-craft's five-question test per element).*

**4. States are where quality actually lives.**
The canon's single highest-leverage habit (ux-craft): design the **states**, not the screen — empty, loading, ideal, partial, error, done for every async surface; hover, focus, active, disabled for every control. The corpus's empty-state pattern evidence shows the great apps treat first-run as a designed moment (illustration + one sentence + one action), not an absence. A beautiful ideal-state mock is a third of a design. *Practice: every hi-fi mock ships its state matrix — ideal + empty rendered, the rest specified; unhappy paths get real copy.*

**5. Words are load-bearing.**
macOS has a copy grammar as strict as its spatial one: **verb-first buttons that name the action** ("Save changes", never "Submit"/"OK" on consequential actions); **"…" means opens-a-further-view**, absent means commits now; one name per action kept through the flow; errors say what happened + how to fix, adjacent, never blaming (never emoting); helper text is one quiet secondary sentence under its control. *Practice: write the real words as part of the design (ux-craft ux-writing); placeholder copy hides both layout and comprehension failures.*

> **Casing — this conviction previously overclaimed, and the correction is sourced.** It
> asserted sentence case *everywhere*. Apple's HIG specifies **title-style capitalization,
> articles removed, for menu-bar items** (two independent first-party sources, August 2026),
> and sentence case for body copy, field labels, placeholders and helper text. **Buttons are
> genuinely contested**: the corpus ships both, and the third-party claim for title case
> everywhere rests on citations that do not resolve. So the rule that survives is
> **consistency within an element type** — pick one for buttons and hold it across the
> surface — plus the part no source disputes: **tracked ALL-CAPS at heading size is the #1
> web tell.** Full register in `evidence.md`.

**6. Forgiveness over interrogation.**
The mac's cultural contract is ⌘Z. Don't confirm reversible actions — make them reversible and say what happened; scale friction to blast radius only for genuinely destructive ones (named-consequence dialog, never a default). Recognition over recall: if the user must remember something from another surface, display it. Disabled controls dim with a discoverable reason — never disappear (layout stability is a platform value). *Practice: for every action ask "undo or confirm?" — undo wins unless data leaves the machine.*

**7. The keyboard is half the app.**
Invisible in a static mock, decisive in the product: every command reachable from the menu bar with standard shortcuts (⌘N/F/W/S/Z/,), Esc dismisses, Return commits the one default action, focus ring visible and accent-bound, logical tab order. The corpus's native-audit failures cluster in apps that treat the pointer as the only citizen. *Practice: specs name the default button, the Esc behaviour, and the 3–5 signature shortcuts; mocks show the focused state somewhere.*

**8. Completeness is invisible until it's absent.**
Dark mode authored independently (graphite, never inverted); focus/active window states; Reduce Motion/Transparency honoured; contrast floors held even on vibrancy. No single one of these is ever *the reason* an app feels great — their joint presence is why nothing feels wrong, which users experience as "it just feels right". Peak-end applies: the app is remembered by its best moment (the signature) and its worst (usually a missing state). *Practice: the audits exist to protect the floor so the signature gets the attention.*

## Where general web/UX rules yield to mac grammar

design-craft and ux-craft are standing dependencies — but they were written web-first. When their general rules collide with platform grammar, **native wins inside app chrome**. The known collisions:

| General (design-craft / ux-craft) rule | macOS override |
|---|---|
| `cursor: pointer` on every clickable element | **Arrow cursor everywhere in app chrome** — the pointer hand is a web-content signal (links); a hand cursor on buttons/rows/toolbar items is a non-native tell. Keep `pointer` only for true hyperlinks and marketing-page surfaces. |
| Touch targets ≥44×44px everywhere | Desktop pointer precision: visible controls 20–28pt on the kit ladder, padded hit areas where sensible; 24px WCAG floor. 44pt binds only touch-adjacent/dual-platform work. |
| ALL-CAPS labels with tracking `0.06–0.1em` | Sentence case, system font, secondary colour. Tracked uppercase is the corpus's loudest defect tell — don't "fix" its tracking, replace it. |
| Hover as a primary affordance concern | Hover states still required (macOS is pointer-first), but resting affordance comes from bezels/placement per the kit — a borderless toolbar symbol *is* natively resting, don't give it a web button treatment. |
| One bold CTA + `border-radius` card grammar | One *prominent* (accent-filled) button per view via the kit's Bordered Default style; cards per cluster radius tokens, never the `12px + border-left` SaaS default. |
| Toasts for success feedback | Prefer in-place state change + subtle confirmation; macOS uses notifications sparingly and never for in-app acknowledgement of a click. |
| Validation styling patterns (red borders etc.) | Keep the timing discipline (validate on blur-after-edit, re-validate per keystroke) but render errors natively: field-adjacent secondary-red text + focus ring, not web alert boxes. |
| Custom scrollbars / persistent format bars / kebab menus | System scrollbars, Format menu + transient popover, system overflow (») — the web-Electron tells table in the native grammar. |

Everything else in those skills binds unchanged — the five-question content test, the states machine, spacing scales, contrast floors, the ethics gate, real-content discipline, per-unit critique on multi-surface commissions.

## Using this file

- **Design mode:** read after choosing a direction, before building — convictions 3–7 generate the mock's requirements (question, states, copy, keyboard, forgiveness) the way the direction generates its look.
- **Critique:** the convictions are the review vocabulary above the rubrics — a mock can pass all 24 audit points and still fail conviction 3 (no clear question) or 1 (no signature). Say which conviction a weakness violates.
- **The essence test, before delivery:** *Would a macapp.supply curator accept it (native at a glance, distinct at a second look)? Can you name its question, its signature, and its worst state's behaviour in one sentence each?* If any answer is missing, the design isn't done.
