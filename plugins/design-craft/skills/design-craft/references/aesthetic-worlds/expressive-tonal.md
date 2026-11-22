# Expressive tonal — shape and roundness that report state

- **Family:** hand, archive and play
- **Best for:** consumer and Android-first apps, productivity tools that need to feel warmer without losing density, onboarding, learning and wellbeing products
- **Touchstones:** Google Material 3 Expressive; roundness-axis type such as Allo and Google Sans Flex
- **Source:** [Compose Material 3 1.5.0 stable](https://m3.material.io/blog/compose-material-3-is-stable) (Expressive APIs stable, 18 Nov 2026); [Allo](https://github.com/joshpuckett/allo) (OFL, the SIL Open Font License; `ROND` axis 0–100, plus weight and optical size); [Google Sans Flex](https://github.com/googlefonts/googlesans-flex) (OFL; weight, width, slant, optical size, grade, roundness); all accessed 2026-11-22

On native Android, install the platform library (`MaterialExpressiveTheme` in Compose Material 3) rather than recreating it, per `frontend-aesthetic-direction.md`. This recipe carries the mechanism to the web or to a brand that is not Material.

## Tokens

- **Palette:** one seed colour generates the system: primary, secondary and tertiary containers as tonal steps at a fixed `oklch()` hue. Surfaces are near-neutral with at most 0.01 chroma toward the seed. Identity lives in saturated containers, not in coloured body text. Check 4.5:1 on every text-on-container pair.
- **Type:** one variable sans with a roundness or width axis. Display heavy and round (`"ROND" 70–100`), labels sharper and tighter (`"ROND" 0–40`), body at the face's default. Roundness has no CSS property, so set it with `font-variation-settings`; leave `font-optical-sizing: auto` for optical size.
- **Scale:** high contrast between tiers — display 48–96px, labels 12–14px, few sizes in between.
- **Spacing:** 4 / 8 / 12 / 16 / 24 / 32 / 48px.
- **Shape:** radii encode role. Full pill for the primary action and chips; 16–28px for containers; 4–8px for inputs and dense lists. Selected or pressed components change shape. `corner-shape: squircle` as a progressive enhancement over `border-radius`.
- **Motion:** interruptible springs with small overshoot that keep velocity when retargeted; a shape change on press within 150–250ms. Under `prefers-reduced-motion` the state changes instantly and the shape change stays, because it carries the information.

## Signature moves

1. Roundness as a friendliness dial: the same face sharper in dense interface, rounder in display text and empty states.
2. Shape morphing that reports state — selected, pressed, expanded — so the shape change is information rather than flourish.
3. A single seed colour behind the whole tonal system.
4. Mixed radii by role, never one radius everywhere.

## Avoid

One large radius on every element; a bounce on every control; coloured body text; glass layered over the tonal surfaces; and a hand-faked Material look on Android when the official library exists.

## Do not use when

The brand is austere or editorial; the work is Apple-platform native (use system components there, which carry Liquid Glass); or the surface is a dense expert tool where morphing shapes slow scanning.

## Subject-mining prompt

What in this subject changes shape when it changes state — a seed that sprouts, a ticket that gets punched, a dial that clicks into place? Let that object decide which components morph and how far.
