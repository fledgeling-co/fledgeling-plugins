# Typesetting: Micro-Typography That Separates Typeset from Typed

Apply professional typesetting to every deliverable with visible text. These are permanent rules from centuries of typographic practice (distilled largely from Butterick's *Practical Typography*), not trends — and they are the rules LLM-generated markup most reliably gets wrong. **Enforcement mode (default):** apply every rule silently while writing HTML/JSX/CSS — don't ask, don't explain. **Audit mode:** when reviewing existing text, flag violations with before/after fixes.

## Phase 1: Characters — the substitution pass

Substitute these automatically in every visible string:

| Typed | Typeset | HTML entity | Rule |
|---|---|---|---|
| "straight" 'quotes' | “curly” ‘quotes’ | `&ldquo;` `&rdquo;` `&lsquo;` `&rsquo;` | Always curly; apostrophe = closing single quote (’) |
| `--` / `---` | – / — | `&ndash;` / `&mdash;` | En dash for ranges (1–10) and connections (Sarbanes–Oxley); em dash for sentence breaks |
| `...` | … | `&hellip;` | One character, never three periods |
| `12 x 34` | 12 × 34 | `&times;` | Real multiplication sign; `&minus;` (−) for math minus |
| `(c)` `(TM)` `(R)` | © ™ ® | `&copy;` `&trade;` `&reg;` | "Copyright ©" is redundant — word *or* symbol |

**The one straight-quote exception:** foot and inch (minute/second) marks stay straight — `6&#39;&nbsp;10&quot;`, never curly.

**Decade abbreviations and word-initial contractions** get a *closing* quote: ’70s, rock ’n’ roll — smart-quote engines wrongly insert an opening quote; fix explicitly with `&rsquo;`.

**Accents are mandatory in proper names** (François, Plácido); loanwords per dictionary.

### The JSX escape gotcha (React prototypes)

Unicode escapes (`’`, `“`) do **not** work in JSX *text content* — they render literally, so the user sees `’` on screen. Either paste the real UTF-8 character into the source (preferred) or wrap in an expression: `Don{'’'}t`. HTML entities (`&rsquo;`) work in plain HTML but not reliably in JSX. Escapes *do* work inside JS string literals and data arrays — the bug is only JSX text between tags. For bulk CLI fixes, `sed` with raw UTF-8 bytes (`CURLY=$(printf '\xe2\x80\x99')`), not escape sequences.

## Phase 2: Spacing

- **Exactly one space after punctuation.** Never two. Not debatable.
- **`&nbsp;` prevents orphaned fragments:** before numeric references (`Fig.&nbsp;3`, `§&nbsp;42`), after `©`, inside measurements and shortcuts (`10&nbsp;MB`, `⌘&nbsp;K`), after honorifics (`Dr.&nbsp;Smith`).
- Never stack spaces, `<br>`s, or empty paragraphs for layout — that's what margin is for.

## Phase 3: Emphasis and caps

- **Bold OR italic — mutually exclusive, and rationed.** If everything is emphasized, nothing is. Serif body: italic for gentle, bold for strong. Sans body: bold only (italic sans barely registers). Never quotation marks or underline for emphasis — underline means "link" on the web and nothing else.
- **ALL CAPS: under one line of text, always letterspaced.** `0.06–0.1em` is the house range — `hierarchy-rhythm-review.md` Lens 2 item 3 owns the full tracking table and the lint gates the same numbers; treat `0.05` and `0.12` as the outer bounds of what a specific face can justify rather than as the default. Kerning on (`font-feature-settings: "kern" 1; text-rendering: optimizeLegibility`). Never caps for whole paragraphs.
- **Small caps only if real** (`font-variant-caps: small-caps` with a font that has the `smcp` feature) — scaled-down capitals are fake and look thin. System fonts don't have them; skip rather than fake.
- **Exclamation points: budget one per document.**

## Phase 4: Headings and paragraphs

- **Headings:** space **above > below** (a heading belongs to what follows); bold, not italic; the *smallest* size increment that establishes hierarchy (body 16px → heading 20px, not 32px); `hyphens: none`; max 3 levels; keep with next paragraph in print (`break-after: avoid`).
- **Paragraphs: first-line indent OR space-between — never both.** Space-between is the web default (`margin-bottom: 0.5–1em`); if indenting instead, `p + p { text-indent: 1.5em }` with zero margin.
- **Body text first:** font, size (web 15–25px), line-height (1.2–1.45 body; the browser's default single-spacing is too tight), and measure (45–90 characters; `max-width: 65ch`) are the four decisions everything else calibrates against.
- **Never justify web text** without `hyphens: auto` — and even then prefer `text-align: start` with a ragged edge. Centered text: short titles only, never blocks.

## Phase 5: Tables, lists, rules

- **Tables: remove borders, add padding.** Data creates an implied grid; cell borders are clutter. Keep one thin rule under the header row (`border-bottom: 1.5px solid currentColor` at reduced opacity), generous cell padding (`0.5em 1em`), **numbers right-aligned with `font-variant-numeric: tabular-nums lining-nums`**, text left-aligned.
- **Lists:** semantic `<ul>/<ol>`, never typed bullets; modest indentation.
- **Horizontal rules:** try space alone first; if a rule earns its place, hairline (0.5–1pt, low opacity), never patterned or thick.

## Phase 6: Numbers and OpenType

- `tabular-nums` on any column of comparable figures (tables, dashboards, timers, prices) so digits align and don't shift as they tick.
- Kerning and ligatures on by default: `font-feature-settings: "kern" 1, "liga" 1`.
- Oldstyle figures (`"onum"`) suit long-form prose; lining figures suit UI and data.

## Phase 7: Screen-specific notes

- **Dark mode makes text look heavier** — drop body weight slightly (e.g. 400 → 350 on a variable font, or let `-webkit-font-smoothing` revert to `auto`), and re-check contrast separately from light mode.
- `text-wrap: balance` on headings (kills widows); `text-wrap: pretty` on prose.
- Web links: subtle underline, not heavy — `text-decoration-thickness: 1px; text-underline-offset: 2px`.
- Fluid sizing via `clamp()` (`font-size: clamp(16px, 2.5vw, 20px)`), scaling measure and size together — the common responsive failure is scaling everything *except* the body text.

## Review checklist (run in audit mode)

Straight quotes in visible text · `...` instead of … · hyphens where en/em dashes belong · double spaces · unletterspaced caps · fake small caps · bold+italic combined · underlined non-links · headings with more space below than above · indent *and* space between paragraphs · bordered spreadsheet-style tables · proportional figures in data columns · justified body text · JSX rendering literal `’`. Report violations with the exact replacement, then fix.
