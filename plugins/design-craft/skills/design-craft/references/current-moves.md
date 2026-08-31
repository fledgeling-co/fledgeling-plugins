# Current Moves — dated axes, not a costume checklist

Read this when choosing a direction in 2026 and you need axes that are not the 2023–24 AI defaults (cream editorial, dark mesh, three-card bento). It is a candidate list for `frontend-aesthetic-direction.md` and `aesthetic-worlds.md`, not a look to apply wholesale.

**As-at 2026-08-31.** Last reviewed 2026-08-31. A page that wears every row is a trend collage, which is the other way sites look the same. Treat each row as a permission the current year has granted, then still subject-mine.

## How to read a row

| Field | Meaning |
|---|---|
| **Strength** | `measured` a documented standard or API; `repeated-shipped` a named public pattern; `practitioner` a skill or studio observation |
| **Source** | The URL or repo snapshot that supports the row |
| **Accessed** | The date that source was read for this file |
| **Status** | `emerging` still distinctive; `mainstream` available and useful; `ai-default` now a reflex, do not spend a free axis on it |

## Moves that still earn a place

| Move | What it actually changes | When it earns a place | Lazy version | Strength | Status | Source | Accessed |
|---|---|---|---|---|---|---|---|
| **Off-centre thesis** | First viewport starts top-left or object-led, not centred hero plus two CTAs | Persuade and Experience when the variance dial is above the quiet band | A centred hero with `text-align: left` on the headline | practitioner | emerging | [taste-skill v2](https://github.com/Leonxlnx/taste-skill/blob/ccbc15639c97057cbfcf32ecebc38ef716e4bb37/skills/taste-skill/SKILL.md) (`ccbc1563`, anti-centre bias) | 2026-08-31 |
| **Type as the image** | One word or short line at display scale does the illustration's job | When photography is an honest placeholder or the product is language | Gradient-clipped text, italic word-accent, or a serif injected into a sans headline | repeated-shipped | emerging | [Pentagram](https://www.pentagram.com/) public identity work; [garden-skills pentagram recipe](https://github.com/ConardLi/garden-skills/blob/aaf9a82f5efd73e87cc0998edc398e75bfc35901/skills/web-design-engineer/references/style-recipes/pentagram.md) (snapshot `aaf9a82f`) | 2026-08-31 |
| **Variable type with a job** | Weight, width, or position change that tracks scroll or state | One moment, with a still composition under `prefers-reduced-motion` | Letters that jitter on every headline | repeated-shipped | emerging | [Field.io](https://www.field.io/); [garden-skills field-io recipe](https://github.com/ConardLi/garden-skills/blob/aaf9a82f5efd73e87cc0998edc398e75bfc35901/skills/web-design-engineer/references/style-recipes/field-io.md) (snapshot `aaf9a82f`) | 2026-08-31 |
| **One spatial moment** | CSS 3D or a WebGL island, budgeted (`depth-and-3d.md`) | Experience, or a Persuade hero that is the product | A mesh blob behind a normal layout | practitioner | emerging | [garden-skills active-theory recipe](https://github.com/ConardLi/garden-skills/blob/aaf9a82f5efd73e87cc0998edc398e75bfc35901/skills/web-design-engineer/references/style-recipes/active-theory.md) (snapshot `aaf9a82f`); [Active Theory](https://activetheory.net/) | 2026-08-31 |
| **Magazine structure on a product site** | Multi-deck hierarchy, column rhythm, pull quotes, an index | Read surfaces; Persuade when the argument is long | Broadsheet costume: hairline rules, zero radius, oversized serif, no argument | repeated-shipped | mainstream | [Monocle](https://monocle.com/); [garden-skills monocle-magazine recipe](https://github.com/ConardLi/garden-skills/blob/aaf9a82f5efd73e87cc0998edc398e75bfc35901/skills/web-design-engineer/references/style-recipes/monocle-magazine.md) (snapshot `aaf9a82f`) | 2026-08-31 |
| **Visible accessibility as craft** | Large body, real focus, 4.5:1 designed contrast, a skip-link that looks owned | Public-sector, trust-first, any Operate surface | A high-contrast theme that is just inverted colours | measured | mainstream | [WCAG 2.2 Understanding 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum); [GOV.UK Design System](https://design-system.service.gov.uk/styles/colour/) | 2026-08-31 |
| **Photographed material, not CSS material** | Real paper, metal, cloth, or object shots | Premium-consumer, editorial, hardware | Bevel, grain filter, or letterpress faked in CSS (`ai-slop-check.md` §4) | practitioner | mainstream | garden-skills `aesop.md` and `stripe-press.md` snapshot `aaf9a82f`; [Stripe Press](https://press.stripe.com/) | 2026-08-31 |
| **Bento as one family** | Mixed cell sizes used once; cell count equals content count | Feature clusters with genuinely different cell jobs | The whole page is a bento, including empty cells | practitioner | ai-default when overused | [taste-skill v2](https://github.com/Leonxlnx/taste-skill/blob/ccbc15639c97057cbfcf32ecebc38ef716e4bb37/skills/taste-skill/SKILL.md) bento cell-count rule | 2026-08-31 |
| **Maximalism as a register** | One committed loud world (Y2K, typographic violence, toy) | When the brief asked for it and half-measures would look broken | Stickers and marquees on a Linear-style tool page | practitioner | emerging | [garden-skills y2k-retrofuturism recipe](https://github.com/ConardLi/garden-skills/blob/aaf9a82f5efd73e87cc0998edc398e75bfc35901/skills/web-design-engineer/references/style-recipes/y2k-retrofuturism.md) (snapshot `aaf9a82f`) | 2026-08-31 |
| **Dark as a designed theme** | Separate tonal steps, not inverted light | When the scene (ambient light, duty, mood) forces dark | `#0a0a0a` plus one acid accent | practitioner | ai-default when unexamined | [garden-skills linear recipe](https://github.com/ConardLi/garden-skills/blob/aaf9a82f5efd73e87cc0998edc398e75bfc35901/skills/web-design-engineer/references/style-recipes/linear.md) (snapshot `aaf9a82f`); [Linear](https://linear.app/) | 2026-08-31 |
| **Native CSS scroll-driven motion** | Scroll timeline instead of a JavaScript scroll listener | One storytelling beat on a served page that supports the API | `window.addEventListener('scroll')` driving React state | measured | emerging | [MDN CSS scroll-driven animations](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_scroll-driven_animations) (updated 2026-05-28); [Scroll-driven Animations spec](https://drafts.csswg.org/scroll-animations-1/) | 2026-08-31 |
| **Pinned scroll at the viewport top** | `start: "top top"` and `pin: true` so a stack or pan begins after it is held | Sticky-stack and horizontal-pan sequences | `"top 80%"` transforms that start before the section is pinned | measured | mainstream | [GSAP ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) pin default is `"top top"` | 2026-08-31 |
| **Viewport-stable full-height sections** | `min-height: 100dvh` rather than `h-screen` / `100vh` | Heroes and pinned scenes on mobile | Layout jump as browser chrome appears and disappears | practitioner | mainstream | [taste-skill v2](https://github.com/Leonxlnx/taste-skill/blob/ccbc15639c97057cbfcf32ecebc38ef716e4bb37/skills/taste-skill/SKILL.md) viewport stability; `polish-pass.md` already gates `100vh` | 2026-08-31 |
| **Motion isolated from render** | Motion values or GSAP context update without re-rendering the tree | Any interactive motion above a hover | `useState` tracking mouse or scroll on every frame | measured | mainstream | [Motion for React](https://motion.dev/docs/react-motion-component) (`motion/react`); GSAP `kill()` / React cleanup in [ScrollTrigger](https://gsap.com/docs/v3/Plugins/ScrollTrigger/) | 2026-08-31 |

## What not to treat as current

- **Inter / Geist / Space Grotesk as the distinctive choice.** They are the 2024–26 default stack. Distinctive is a pairing or a display face with a subject reason. Practitioner: taste-skill v2 and this skill's `ai-slop-check.md` §5.
- **Liquid Glass on the web.** Apple documents it for Apple platforms. A `backdrop-filter` approximation is honest only when labelled, and it is not a 2026 identity. Measured: [Apple HIG Materials](https://developer.apple.com/design/human-interface-guidelines/materials).
- **"AI purple" and indigo Tailwind accents.** Still a tell. A brief that asks for violet is an override, not a trend. Practitioner: taste-skill v2 Lila rule.
- **Infinite micro-loops.** Pulse, float, shimmer on every card. Motion still has to say something (`motion-design.md` Phase 1).
- **`window` scroll listeners.** Use ScrollTrigger, CSS `animation-timeline`, IntersectionObserver, or Motion `useScroll`. Practitioner: taste-skill v2 §5.D; measured: MDN scroll-driven animations as the CSS alternative.

## How this file goes stale

A move that has become the new default belongs on the AI-default list in `ai-slop-check.md` §9, not here. When updating:

1. Change **As-at** and **Last reviewed**.
2. Add or replace the source URL and accessed date on the changed row.
3. Set **Status** honestly. If a row is now `ai-default`, move it to "What not to treat as current" rather than leaving it as a permission.
4. Do not add a row whose only support is "it feels current".
