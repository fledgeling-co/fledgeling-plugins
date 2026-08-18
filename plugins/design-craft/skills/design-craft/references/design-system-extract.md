# Design System Extract: Pull Tokens from Sources

Extract design tokens (color, typography, spacing, radii, shadow) from a brand reference, codebase, or screenshots, and emit a structured tokens file. Use this when starting design work that should match an existing visual language.

A tokens file is the foundation of system thinking. Once tokens exist, future designs reference them — keeping the system consistent without re-asking the user for values every time.

## Phase 1: Identify sources

Determine what to extract from. The user may provide:

- **A codebase** — read theme files (`theme.ts`, `tokens.css`, `_variables.scss`, `tailwind.config.js`, design system source).
- **A live site or screenshots** — extract values from CSS via DevTools-style inspection or by reading screenshots carefully.
- **A brand guide** — PDF, Figma file, or document that lists colors, fonts, spacing.
- **An existing design system project** — a UI kit you can list and read.

If the user hasn't specified, ask. Don't extract from your own assumptions — invented tokens defeat the point.

## Phase 2: Extract by category

Walk through each category. For each, capture concrete values from the source — never guess.

### Colors

Pull: **brand primary** (and dark/light variants if defined), **brand accent** (and variants), **semantic colors** (success, warning, error, info, and their light backgrounds where defined), **neutral scale** (typically 9–11 steps from near-white to near-black, with a consistent tone — warm / cool / neutral), **surface colors** (background, foreground, card, overlay, border).

For each color, record: the hex (or oklch) value, its name in the source, and its intended usage (where the source documents it). Flag inconsistencies — multiple slightly-different blues, neutrals on different tones — as a finding, and rank **near-misses highest**: a value within ~5% of another candidate token is almost certainly drift from it (and perceptually reads as "almost right, therefore wrong" — color perception is non-linear), where a clearly distinct value may be a real second color. Don't silently merge either kind; the inconsistency itself is information — but recommend snapping near-misses in the report.

**Contrast is part of the token contract, not a later audit.** For every text-role token, compute its ratio against the backgrounds it's declared for and record it — a token ladder should pass WCAG AA *by construction*. The systemic traps to flag: "subtle"/"tertiary" mid-gray text tokens in the `#6b7380` neighborhood (fail 4.5:1 on light backgrounds most of the time), font-size tokens below 12px, and opacity-based muting (compute the *effective* color). When a brand color fails on its declared background, emit an AA-compliant variant in the same color family as the working token and keep the original as a `-display` token reserved for text-free surfaces.

### Typography

Pull: **font families** (sans, serif, mono — include the full stack with fallbacks), **font sizes** (the actual scale used — `12 / 14 / 16 / 18 / 20 / 24 / 30 / 36 / 48 / 60` is common but not universal), **font weights** (only those actually loaded), **line heights** (at minimum: tight ~1.1 for headlines, normal ~1.5 for body, loose ~1.7 for long-form), **letter spacing** (usually only matters for all-caps labels), **text styles** (named combinations like "Heading 1", "Body Large", "Caption" if the source defines them).

### Spacing

Pull the spacing scale used. Common bases: 4px or 8px. The scale typically runs 0 to 64–128px. Document the actual scale in use, not a generic one. If the source has separate scales for inset / inline / block / between-components, capture all of them.

### Radii

Pull the corner-radius values used. Typically 3–5 distinct radii (`0`, `4`, `8`, `12`, `9999` for pills).

### Shadows

Pull the shadow system. Typically 3–5 elevations (`shadow-sm` through `shadow-2xl`). Capture the full CSS value (offset, blur, spread, color, opacity).

### Other tokens (if present)

Z-index scale (modals, dropdowns, toasts, tooltips); animation tokens (duration `fast`/`normal`/`slow` and easing curves); breakpoints (if responsive); container widths (max-width values for content).

### Signature moves (prose, not tokens)

Tokens alone don't reproduce a brand — capture the 4–8 observations that actually distinguish it, each concrete enough to act on. The kind of thing to hunt for: a signature headline weight ("display runs at weight 300 — anti-convention, whispered authority"), tinted rather than gray shadows ("multi-layer `rgba(50,50,93,.25)` — elevation stays on-brand"), OpenType features (`"ss01"` stylistic sets, `"tnum"` for financial data), a deliberately conservative radius, a color that is never used for a role ("the yellow is jewelry, never a CTA"). These observations are what let a future agent produce on-brand work the tokens can't specify.

## Phase 3: Emit the tokens file

Write a `tokens.css` (or matching format if the source uses a different language: `tokens.ts`, `tokens.json`, etc.). Structure:

```css
:root {
  /* ---------- Colors ---------- */
  --color-primary: #...; --color-primary-dark: #...; --color-primary-light: #...; --color-accent: #...;
  --color-success: #...; --color-warning: #...; --color-error: #...; --color-info: #...;
  --color-gray-50: #...; --color-gray-100: #...; /* … */ --color-gray-900: #...;
  --color-bg: #...; --color-surface: #...; --color-border: #...;

  /* ---------- Typography ---------- */
  --font-sans: "...", -apple-system, sans-serif; --font-serif: "...", serif; --font-mono: "...", monospace;
  --text-xs: 12px; --text-sm: 14px; --text-base: 16px; --text-lg: 18px; --text-xl: 20px;
  --text-2xl: 24px; --text-3xl: 30px; --text-4xl: 36px; --text-5xl: 48px;
  --weight-regular: 400; --weight-medium: 500; --weight-semibold: 600; --weight-bold: 700;
  --leading-tight: 1.1; --leading-normal: 1.5; --leading-loose: 1.7;

  /* ---------- Spacing ---------- */
  --space-0: 0; --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px;
  --space-5: 24px; --space-6: 32px; --space-7: 40px; --space-8: 48px; --space-10: 64px;

  /* ---------- Radii ---------- */
  --radius-sm: 4px; --radius-md: 8px; --radius-lg: 12px; --radius-full: 9999px;

  /* ---------- Shadow ---------- */
  --shadow-sm: 0 1px 2px rgba(0,0,0,.05); --shadow-md: 0 4px 6px rgba(0,0,0,.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,.1); --shadow-xl: 0 20px 25px rgba(0,0,0,.15);
}
```

Adapt to the source language and naming convention. If the source uses Tailwind, emit a `tailwind.config.js` extension. If TypeScript, emit a `tokens.ts` with typed exports. Match the project's style.

**Optional companion: a portable `DESIGN.md`.** When the user wants the system usable by other agents/tools (or a local design-system library exists to slot it into), also emit a prose `DESIGN.md` in the 9-section shape used by portable design-system libraries: **1 Visual Theme & Atmosphere** (including the signature moves from Phase 2) · **2 Color** (values + usage rules) · **3 Typography** · **4 Spacing & Grid** · **5 Layout & Composition** · **6 Components** · **7 Motion & Interaction** · **8 Voice & Brand** · **9 Anti-patterns**. Open with an H1 title and a `> Category: <group>` line. The tokens file is for CSS; the DESIGN.md is for the next agent's system prompt.

## Phase 4: Document findings

After emitting the tokens, summarize:

- **Source(s) used** — codebase paths, screenshots, brand guide
- **Categories extracted** — which token sets were found
- **Gaps** — categories the source didn't define (e.g. no shadow scale). These are the user's decisions to make; don't fill them silently.
- **Inconsistencies** — near-duplicate values or off-scale outliers. These often represent ad-hoc decisions worth consolidating.
- **Recommended next steps** — typically: review the token file with the user, then use it in subsequent designs.

The output is a tokens file the user can drop in, plus a clear-eyed report of where the source design system has gaps or inconsistencies.
