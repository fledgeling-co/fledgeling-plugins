# Mobile Design: App Screens That Feel Native, Not Shrunk

Design phone-first surfaces — app screens, mobile flows, installable prototypes — that read as real iOS/Android apps rather than a desktop page squeezed into a device frame. Use this whenever the deliverable targets a phone: any device-framed mock, mobile app prototype, or "design the mobile app for…" brief. Build the artifact per `make-a-prototype.md` (frames, installables, safe areas); this file supplies the design knowledge that goes inside the frame.

**A mobile screen is not a small web page.** It has one hand on it, one job per screen, a platform grammar users already know, and physics users can feel. Web-page tells inside a phone frame — hover-dependent affordances, 12-column hero layouts, footer nav — are the mobile version of AI slop.

## Phase 1: Baseline geometry

- **Design at 375–390 logical px wide** (verify at both); content must survive 320px without breaking.
- **Safe areas top and bottom, always** — `padding: env(safe-area-inset-top) 0 env(safe-area-inset-bottom)`. The status-bar region is layout, not dead space; the home-indicator region is never tappable real estate.
- **Thumb zone.** Primary actions live in the bottom third of the screen — tab bars, FABs, sticky CTAs, sheet footers. The top corners are the hardest reach on the device; put destructive or rare actions there, never the primary CTA. (This is Fitts's Law with geometry — see `laws-of-composition.md`.)
- **Touch targets ≥44×44px** with ≥8px between adjacent targets. A tappable row is the whole row, not just its label.
- **One primary action per screen.** Mobile enforces the SKILL.md rule harder than desktop — there is no room for two heroes.
- **Collapse the header action cluster.** On mobile the top bar is logo + **at most one** compact action (an icon, never a labelled button) + the menu toggle — everything else (Subscribe, "Ask AI", a price badge) moves into the nav sheet. Hiding only the *nav links* while leaving desktop actions in the bar overflows it and pushes the menu toggle **off the right edge, out of reach** (a fixed header doesn't trip a page-overflow probe, so this hides in plain sight). Verify the toggle's right edge is ≤ the viewport width at 375px, and that the nav sheet it opens is a real element the toggle reveals (give it a role/hook, not a bare `<div>` a reviewer's automation can't detect).

## Phase 2: Platform grammar (make it feel iOS / Android, not "webby")

Pick the platform and follow its grammar. Mixed grammar (Material FAB + iOS large title) reads as template output.

### iOS

- **Type:** SF-style ramp — 34px large title, 17px body, 15px secondary, 13px caption/footnote, 11px tab labels. Weight does the hierarchy work; iOS uses semibold, not bold-everything.
- **Ink at stepped alphas, not five greys.** One label color at 100% (headings/body), ~60% (secondary), ~30% (tertiary/placeholder) — this is how `label`/`secondaryLabel`/`tertiaryLabel` actually work, and it holds across light/dark and tinted surfaces. Check 60%-alpha secondary text still clears 4.5:1.
- **Large-title header that collapses.** Screen opens with a 34px bold left-aligned title; on scroll it shrinks into a centered 17px bar title with a hairline separator (and often a blur material). This one pattern makes an HTML mock read "iOS" instantly. Never paint a custom title inside the content area when the header should own it.
- **Tab bar:** 2–5 tabs, SF-symbol-style icons (outline at rest, filled when selected), 11px labels, optional badge (number or dot). Search tab last. On modern iOS the bar sits on a material (blur) and can minimize on scroll-down.
- **Sheets with detents.** Actions and sub-flows present as bottom sheets stopping at ~25% / 50% / 100% heights, with a grabber pill at top. Sheet headers put **Cancel left, confirm right** (confirm bold). Sheets own their dismissal — always reachable close, since swipe-down isn't discoverable. A map-under-sheet layout keeps the content behind the low detents interactive.
- **Navigation physics:** push slides in from the right with the previous screen parallaxing back; back is both the chevron and an edge swipe. Thumbnail → detail uses a **zoom transition** (the tapped image scales up into the detail view) — great for gallery/card sources, unnatural for skinny full-width list rows.
- **Corners are continuous.** iOS radii are superellipses; plain `border-radius` reads subtly non-native. It's an acceptable approximation — just keep radii generous (10–16px cards, capsule buttons) and concentric (inner radius = outer radius − inset).
- **Materials:** chrome (bars, sheets, overlays) sits on blurred translucent material over content, not opaque grey. In CSS: `backdrop-filter: blur(20px) saturate(1.8)` + a light/dark tint — and apply the glass rules from `depth-and-3d.md` Phase 4.
- **Motion feel is springs.** iOS motion is interruptible spring physics (≈ response 0.3 / damping 0.7 — in CSS, `--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1)` from `motion-design.md` is the closest single curve). Linear reads robotic; long ease-in-out reads Android-2014.

### Android (Material 3)

- Bottom navigation bar (3–5 destinations, active pill indicator), FAB for the one creation action, top app bar that scrolls away, 12px+ radius cards, tonal color system (one seed hue generating surface tints), ripple feedback on touch. Roboto/Google Sans-style type, 16px body.

## Phase 3: Mobile typography and data

- **Max 4 font sizes and 2 weights per screen.** The whole-product scale (SKILL.md §8) still exists; a single phone screen uses a slice of it. More sizes = the screen is doing too many jobs.
- **Numbers are content on mobile** (prices, balances, reps, steps): give metrics `font-variant-numeric: tabular-nums`, size the **value larger than its label** ("591" big, "Sales" small — inverted label/value hierarchy is a top mobile-dashboard tell), and format large numbers humanely (`1.4M`, `38k`, never `1400000`).
- Body ≥16px (also prevents iOS input auto-zoom), line-height ~1.4 on mobile (tighter than desktop's 1.5–1.6), text truncates with ellipsis rather than wrapping chrome labels.

## Phase 4: Input — typing is expensive

Every keystroke on glass costs more than a tap. Choose input methods accordingly:

- **Selection beats typing.** Offer tappable chips/cards for common answers (roles, preferences, amounts) with an "Other" free-text fallback. Full keyboards are for genuinely free text.
- **Sliders and wheels for one-time setup** (age, budget range); **text fields for repeated or precise entry** (a slider for a dollar amount you enter daily is hostile).
- **Right keyboard per field:** `inputmode="numeric" pattern="[0-9]*"` for PINs/amounts, `inputmode="email"`, `inputmode="tel"` — and `autocomplete` so the OS can fill it. Never block paste.
- Forms present as **one question (or one tight group) per screen** in onboarding flows — a wall of fields is a desktop pattern.
- The keyboard covers the bottom ~45% of the screen: the active field and the submit action must stay visible above it (sticky footer above the keyboard, content scrolls).

## Phase 5: Named screen patterns

Reach for the established pattern before inventing (Jakob's Law):

- **Search screens are never blank pre-query.** Fill with recent searches, trending/popular items, or personalized suggestions — this is a distinct empty state beyond the first-use/no-results/cleared trio in `make-a-prototype.md`.
- **Status/order tracking:** open with a confident status headline ("Arriving today, 2:15pm"), humanize with photo/name/quick actions, and render progress as a **visual timeline**, not a text list of dated events.
- **Home screens adapt to user stage:** new users get a simple welcome + guided setup + few options; returning users get personalized, routine-focused content with progress; power users get density and shortcuts. State which stage a mock represents.
- **People:** photo avatar > initials > generic icon, in that order of preference. Never the SVG egg.
- **Stat tiles:** value dominant, label quiet, delta with direction + color + arrow (not color alone), sparkline optional.
- **Pull-to-refresh** on feeds, **swipe actions** on list rows (leading = positive, trailing = destructive, full-swipe commits), **skeletons matched to the real layout** while loading.

## Phase 6: Industry conventions (defaults to honour or deliberately break)

Category conventions are Jakob's Law per vertical — they buy instant familiarity. Deviating is legitimate only as a stated choice. These also **override the slop rules where named**: a crypto app's neon-on-dark is convention, not slop — but only in that vertical.

| Vertical | Convention | Note |
|---|---|---|
| AI / tech | Soft depth and glow, smooth "intelligent" motion, ethereal accents | Earned gradients — still no rainbows |
| Crypto / fintech-degen | Dark ground, neon accent, bold type, geometric | Polish = trust: motion and detail are product features here |
| Banking / finance | Blue-family trust palette, generous whitespace, conservative type | Tactile touches (draggable charts, card flips) read premium |
| Health / wellness | Bright approachable color, friendly illustration, warm micro-interactions | Reduce anxiety; onboarding must feel non-intimidating |
| Sleep / meditation | Deep blues/purples, minimal UI, soft slow transitions, low contrast | The one vertical where slow motion is right |
| Education | Playful saturated palettes, character/mascot personality, streaks | Emotional feedback loops drive retention |
| Fitness | Energetic color, bold condensed type, momentum/progress indicators | Numbers big, tabular, celebrated |
| Productivity | Clean, dense-but-organized, strong grids, quick actions | Speed is the aesthetic |
| E-commerce / food | Real product photography, prominent CTAs, trust signals (ratings, delivery ETA), frictionless checkout | Photography quality is the design |

## Phase 7: Emotional design (without becoming slop)

Mobile apps live or die on feel. Apply with the honesty guardrails from SKILL.md §5 and the Peak-End discipline in `laws-of-composition.md`:

- **One peak per flow, at the end.** Map the journey, find where effort/stress concentrates, and place a single designed high moment at completion — never mid-flow confetti.
- **Design the ending.** Flows never just stop: a checkmark/summary card, progress reaffirmed ("You showed up today"), and one gentle next action.
- **Reduce negative peaks.** Waits, errors, and long forms are where the memory of the app is made — give waits useful content (tips, progress), errors the three answers (what/why/what now), and forms mercy (see Phase 4).
- **Feedback proportional to achievement.** A completed task gets a subtle tick; a completed 30-day streak gets the celebration. Uniform confetti devalues everything.
- **Share moments celebrate who the user is, not what the app did.** "You're a night owl — 80% of your writing happens after 9pm" beats "You completed 25 tasks" (the Wrapped pattern). Insight cards are designed as portrait-ratio, brand-saturated, screenshot-worthy artifacts.
- Haptics exist on the real device — note in the mock where a haptic would fire (toggle, success, error) so the intent survives handoff.

## Phase 8: Review gate (run on any mobile deliverable)

Flag on sight: primary CTA outside the thumb zone · touch targets <44px or flush-adjacent · hover-dependent affordances · painted status bar/keyboard in an installable (per `make-a-prototype.md`) · label visually louder than its value · >4 font sizes on one screen · desktop line-length or 12-column grids · mixed iOS/Material grammar · blank pre-query search screen · date-list where a timeline belongs · uniform celebration · safe areas ignored · web-style footer nav · header action cluster overflowing (menu toggle pushed off-screen) · a nav toggle that opens nothing. Then run the standard reviews (`accessibility-audit.md`, `interaction-states-pass.md`) — everything there still applies.
