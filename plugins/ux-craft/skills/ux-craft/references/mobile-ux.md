# Mobile UX

For native apps (iOS/Android/React Native) and mobile web. Wroblewski's core insight drives everything here: mobile constraints force clarity — if it works on a 360px screen for one thumb and partial attention, the design's priorities are actually right.

## The physical layer (non-negotiable)

- **Target size, with each number attributed** — they are not interchangeable and the difference decides a finding's severity. **≥24×24 CSS px** is WCAG 2.2 SC 2.5.8 Target Size (Minimum), Level **AA**: the only one you may call a WCAG failure, and it has real exceptions (Spacing — a 24px-diameter circle centred on the target overlapping no other target's circle, which is the normative form of the "gaps" rule — plus Equivalent, Inline, User Agent Control, Essential). **≥44×44 CSS px** is SC 2.5.5 Target Size (Enhanced), Level **AAA**. The platform craft targets are Apple's **44×44 pt** and Android's **48×48 dp** — both density-independent units, neither a WCAG number, and 44pt equals 44px only at 1× density. When the visual glyph is smaller, extend the hit area (`hitSlop` in RN, padding on the touchable): the visual and interactive sizes are separate decisions, and the spacing exception is what makes a small glyph conformant.
- **Thumb zone**: on phones, the bottom half-screen is comfortable, the top corners are not. Primary actions and navigation live in reach; destructive actions live *out* of casual reach. On large phones one-handed, the top third is effectively two-handed territory.
- **Safe areas**: keep fixed headers, tab bars, CTA bars, and any tappable content clear of the notch/Dynamic Island, status bar, and home-gesture bar (`contentInsetAdjustmentBehavior` / safe-area insets). Scroll content needs bottom inset so the last item isn't buried under a fixed bar.
- **No hover.** Anything load-bearing on hover (tooltips, reveals, dropdown triggers) needs a tap-visible equivalent. `cursor: pointer` conventions don't exist here; affordances must be visual.
- **Feedback within ~100ms of touch** (press state: ripple/opacity/scale 0.95–1.05) or the tap feels dropped and users tap again — the double-action bug. On mobile web, `touch-action: manipulation` removes the legacy 300ms tap delay.
- **No precision requirements**: no pixel-perfect taps on thin edges, no tiny dismiss ×'s. Swipe actions need a visible affordance (chevron, partial reveal, first-run hint) — invisible gestures are invisible features.
- **Gestures always have visible alternatives** for critical actions, and never fight system gestures (edge swipe-back on iOS, predictive back on Android, Control/Notification Center pulls).

## Content & layout

- **Content priority is the design** (Mobile First): the single most important thing on this screen shows first; secondary content folds, defers, or moves. If everything fits by shrinking, nothing was prioritized.
- **Body text ≥ 16px** on mobile web (below that, iOS Safari auto-zooms form inputs); line length 35–60 characters; `min-h-dvh` not `100vh` (browser chrome).
- **No horizontal scroll**, ever, at 360px. Test the longest real heading and the German translation (+30% length).
- **Single column by default**; the ambiguous reading order of multi-column collapses on small screens.
- **Landscape must remain operable** — not optimized, but not broken.
- **Performance is design** (Wroblewski): on mobile networks, weight is UX. Skeletons over blank screens for >300ms loads, compressed images, virtualized lists (any list that can exceed ~50 items), offline/slow-network states designed, not discovered.

## Platform grammar

Respect the platform the user's muscle memory was trained on (Jakob's law at the OS level). React Native ships one codebase but should still feel native per platform where the grammar diverges.

| Concern | iOS (HIG) | Android (Material) |
|---|---|---|
| Top-level nav | Bottom tab bar, 2–5 items, icons + labels | Bottom nav (3–5) or nav drawer for many sections |
| Back | Edge swipe + top-left back; back is *spatial* | System back button/gesture; back is *historical* — must behave predictably |
| Primary action | Prominent button in content or nav bar | FAB or prominent button |
| Menus/pickers | Native action sheets, context menus | Native menus, bottom sheets |
| Type system | SF/Dynamic Type text styles | Roboto/Material type roles |
| Press feedback | Highlight/opacity | Ripple (state layers) |

Cross-platform rules regardless of OS:
- Bottom nav is for **top-level destinations only** — never nest sub-navigation there; max 5 items, always labeled (icon-only nav kills discoverability).
- **Back must preserve state**: scroll position, filters, half-entered input. Navigation resets are trust resets.
- **Deep-link every key screen** — notifications, shares, and emails land people mid-app.
- Current tab/location visibly marked; don't mix tab + drawer + bottom-nav at the same hierarchy level.
- Prefer **native controls and modals** over reimplementations (they get accessibility, dynamic type, and platform behavior for free); customize only where brand genuinely requires it.

## Mobile forms & input

Typing on glass is 3–5× more costly than desktop typing; design like every keystroke is a favor.

- Right keyboard per field (`email`, `tel`, `number`, URL types; `textContentType`/`autocomplete` for autofill and password managers).
- Prefer selection over typing: pickers, chips, steppers, recents, geolocation — but free text beats a 200-item picker.
- Input height ≥ 44pt; labels above (not beside) fields; one column.
- Support paste everywhere (verification codes especially — and use SMS one-time-code autofill).
- Long forms: auto-save, chunk into steps, show progress; sheet/modal with unsaved input confirms before dismissing (swipe-down data loss is a High finding).

## Mobile accessibility specifics

- Dynamic Type / font scaling up to at least 200% without truncation or overlapping layout — test at the largest setting, not the default.
- VoiceOver/TalkBack: every control has a meaningful `accessibilityLabel` (visible label text must be *in* the accessible name — voice-control users say what they see); reading order matches visual order; grouped elements announce as one.
- Reduced motion honored for transitions and parallax; motion-triggered features (shake to undo) have alternatives.
- Contrast rules don't relax outdoors — mobile is used in sunlight; treat 4.5:1 as the floor it is, and test dark mode separately (desaturated tonal variants, not inverted colors).
- Situational impairment is the mobile default: one-handed (holding a child, a rail), interrupted attention, gloves, motion. The most-constrained user is the design target (Levey's principle) — it makes the product better for everyone else too.

## React Native implementation notes

The organizing principle: **prefer native primitives over JS reimplementations** — they carry the accessibility, gestures, and platform behavior you can't cheaply rebuild.

- **Navigation**: native stack + native tabs (react-navigation native-stack / expo-router native tabs), and use native *header options* (large titles, in-header search bar) rather than custom header components. Native tabs give scroll-to-top-on-tab-tap and correct behavior behind translucent bars for free.
- **Sheets & menus**: native `Modal` `formSheet` presentation (swipe-to-dismiss, keyboard avoidance, detents) over JS bottom-sheet libraries when you don't need custom snap behavior; native menus (e.g. zeego) for dropdown/context menus — built-in a11y, destructive styling, long-press. Native shared-element lightbox (e.g. Galeria) for image viewing.
- **Images**: expo-image with a blurhash `placeholder` + short `transition` fade — the standard perceived-speed pattern; in lists, request thumbnails at ~2× display size, never full-res.
- **Touch**: `Pressable` over legacy Touchables; for animated press states, run the animation on the UI thread (gesture handler + Reanimated) so presses stay responsive under load.
- **Lists**: virtualize every list (LegendList/FlashList — never `map` in a ScrollView); heterogeneous lists use item types so cells don't recycle into the wrong shape (visible layout thrash); never track scroll position in React state (dropped frames).
- **Safe areas**: `contentInsetAdjustmentBehavior="automatic"` on root ScrollViews handles insets natively (note: this is newer guidance that supersedes wrap-everything-in-SafeAreaView for scrolling screens; non-scroll screens still need insets).
- **Fonts at build time** (config plugin) so there's no async font flash at launch.
- Wrap all strings in `<Text>`; never `&&` with a possibly-falsy left operand in JSX (renders a literal `0` on web, crashes RN).

Deeper performance rules belong to the `code-review:code-review` skill — flag, don't duplicate.
