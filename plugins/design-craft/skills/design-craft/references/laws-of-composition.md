# Laws of Composition: Cognitive Laws as Code Directives

Named, research-backed laws of perception, decision-making, memory, and motor action — each translated into a directive with concrete numbers you can apply while emitting HTML/CSS/JS. Use this two ways:

- **Design-time reference** — consult while composing a surface: how many options to show, where the primary action anchors, how a settings page groups.
- **Review lens** — audit an existing design, phrasing each finding as *law → violation → fix* (format at the bottom).

These laws decide *composition* — what goes on the screen and in what arrangement. Aesthetic direction decides the visual language; this file decides the structure underneath it.

## Perception and grouping

- **Proximity** (Wertheimer, 1923). Nearness is the cheapest grouping signal — cheaper than borders or shared color.
  - Variable vertical rhythm: **8–12px within a group, 32–48px between groups.**
  - The portable ratio: **between-group spacing ≥2× within-group spacing** — it scales with density where the absolute ranges don't.
  - Uniform spacing everywhere reads as *nothing* being grouped.
- **Similarity** (Wertheimer, 1923). Equivalent affordances must share treatment.
  - Every list row, every secondary button, every destructive action: identical class set.
  - Visible deviation is reserved for the one item meant to draw the eye.
- **Common Region** (Palmer, 1992). A shared bounded area binds its contents — but only when scarce.
  - Use enclosure **only when proximity isn't enough**; it's the more expensive signal.
  - ≥16px padding inside the region; hairline (≥1px) border or tinted surface.
  - A page where every section is bordered destroys the signal — enclosure means something only when most things aren't enclosed.
- **Uniform Connectedness** (Palmer & Rock, 1994). Connected lines and bracketing containers group more strongly than proximity or similarity. Use for wizard steps, comparison sets, explicit flows.
- **Von Restorff** (1933). The one item that differs from a uniform field is the one remembered.
  - **Exactly one** distinct item per field: the recommended tier, the active nav item.
  - Pair the contrast with a **non-color signal** (icon, label, position) — color-alone fails colorblind users and grayscale prints.
- **Selective Attention** (Broadbent, 1958). Users filter aggressively; repeated attention-grabbers train banner blindness.
  - Reserve the strongest visual contrast on a surface for **the single goal-relevant action**.
  - Supporting content recedes in weight; badges and dots are not a substitute for hierarchy.

## Decision-making

- **Hick's Law** (Hick, 1952; Hyman, 1953). Decision time grows ~log(n) with equivalent options.
  - Cap a decision screen at **3–5 visible primary options**; collapse the rest behind progressive disclosure ("More…").
  - Visually mark the recommended choice.
  - The opposite failure — hiding the path forward entirely — is just as bad: keep the full set reachable, just not all at equal weight.
- **Choice Overload** (Iyengar & Lepper, 2000). Too many near-equivalents stall or abandon the decision.
  - Pricing: **3–4 tiers, exactly one marked recommended.**
  - Product grids: **6–9 hero cards** above the fold.
  - Settings: **≤5 named groups.** Never emit a flat wall of equivalents.
- **Anchoring** (Tversky & Kahneman, 1974). The first number seen re-weights all that follow.
  - Place the recommended tier where it anchors the comparison (typically center or first).
  - Render yearly-billing savings as **concrete dollar deltas**, not just percentage badges.
  - **Pre-select the safer default** in radio groups — visual weight should match intended decision weight.
- **Tesler's Law** (Tesler, Apple, 1980s). Complexity is conserved — it moves between engineering, interface, and user; it is never removed.
  - When complexity must reach the user, surface guidance (smart defaults, tooltips, progressive disclosure) at the exact step where it lands.
  - A "simplified" screen that pushes the hard part downstream didn't remove the cost — it relocated it onto the user.

## Memory

- **Miller / Cowan chunking** (Miller, 1956; Cowan, 2001). Working memory holds **~4 chunks** reliably. (Miller's 7±2 is short-term recall, and his paper is about chunks — it was never a menu-length rule.)
  - Group related controls into named sections; each section is one chunk.
  - A settings page with "Account / Notifications / Privacy / Billing / Danger zone" beats one flat list of 30 toggles.
- **Serial Position** (Ebbinghaus, 1885). Recall favors the extremes; middles fade.
  - Anchor the most important nav items at the **leftmost and rightmost** positions of a horizontal menu.
  - Cluster utilities in the middle.
- **Peak-End Rule** (Kahneman et al., 1993). Memory of an experience is its emotional peak and its ending, not its average.
  - Stage the celebratory high-effort moment **at the end of the flow** — success screen after checkout, completion after onboarding.
  - Keep intermediate steps calm. Mid-flow confetti is a misplaced peak; motion should confirm state changes, not perform.
- **Zeigarnik Effect** (1927). Uncompleted tasks pull users back — visible progress converts tension into completion.
  - "3 of 5 steps", greyed-out next sections, checked-off prerequisites.
  - **Honest progress only:** show completed steps when they truly exist; otherwise render "1 of N" with the current step plainly marked.
  - Fabricated progress bars, streak pressure, and quest counters are the same lever used as a **dark pattern** — don't.

## Motor action

- **Fitts's Law + platform floors** (Fitts, 1954). Bigger and closer targets are faster to hit; spacing between adjacent hit zones matters as much as size.
  - Fitts alone doesn't set the minimum — apply the platform floor: **24×24 CSS px (WCAG 2.2 AA), 44×44pt (iOS HIG), 48×48dp (Material 3).**
  - On mobile, put high-frequency controls in the natural thumb arc — concretely, primary actions in the **bottom third** of the screen; top corners are the hardest reach (see `mobile-design.md`).
- **Postel's Law** (RFC 760, 1980). Be liberal in what you accept, conservative in what you emit.
  - Accept input in whatever shape users give it: phone numbers with or without dashes, dates in mixed formats, percentages with or without `%`.
  - Normalize internally to a canonical form; emit **one consistent format** on output.
  - Rejecting a parseable input to enforce a display format transfers your work to the user.

## Expectation

- **Jakob's Law** (Nielsen, 2000). Users spend most of their time on *other* products and expect yours to work the same.
  - Reuse category conventions — nav placement, cart icon, settings gear, primary CTA position — so zero cycles go to relearning grammar.
  - Per-vertical conventions (finance = blue-family trust, sleep = low-contrast dark, e-commerce = photography-led) are tabulated in `mobile-design.md` Phase 6 — they apply beyond mobile.
  - When the brief names a reference product, **anchor on it explicitly** and inherit its interaction grammar.
  - Novelty must earn its keep against the convention's ROI; "innovate everywhere" is the opposite failure mode.
- **Paradox of the Active User** (Carroll & Rosson, 1987). Users skip the manual and start doing, even when reading would be faster.
  - Never design guidance as a separate manual, tour, or help page.
  - Bake it into the surface **at the action point**: empty-state coaching, inline hints, contextual tooltips on the control the user is about to use.

## Using this file as a review lens

Walk the surface and test each law against what's actually rendered. Phrase every finding as **law → violation → fix**, with the numbers:

- *Proximity → uniform 24px spacing everywhere, no visible grouping → 8–12px within field groups, 40px between sections.*
- *Von Restorff → three buttons all high-contrast → keep one filled primary; demote the rest to ghost.*
- *Hick's → 11 equally-weighted menu items → 4 primaries visible, rest under "More".*
- *Zeigarnik → progress bar starts at 30% with nothing done → start at "1 of 4", show real state.*

Findings that cite a named law with a concrete number are actionable and arguable; "this feels cluttered" is neither.
