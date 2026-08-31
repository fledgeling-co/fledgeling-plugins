# Data ink - Tufte / analytical publishing

- **Family:** grids and data
- **Best for:** analytical reports, scientific publishing, data-led storytelling, static evidence
- **Touchstones:** *The Visual Display of Quantitative Information*, *Beautiful Evidence*, Edward Tufte's work
- **Source:** [garden-skills recipe](https://github.com/ConardLi/garden-skills/blob/aaf9a82f5efd73e87cc0998edc398e75bfc35901/skills/web-design-engineer/references/style-recipes/tufte-dataink.md) (snapshot `aaf9a82f`)

## Tokens

- **Palette:** warm neutral ground, ink, two data colours. Add a third only for a real third dimension.
- **Type:** old-style or transitional serif for prose; humanist sans for axis labels and utility text.
- **Scale:** body 12 to 14px for a print-like analytical surface; 10 to 11px axis labels.
- **Spacing:** tight 4 / 8 / 12 / 16 / 24 / 48px. Margins carry notes, not emptiness.
- **Shape:** zero radius, no shadow, faint reference rules.
- **Motion:** none. A chart that needs motion is a different deliverable.

## Signature moves

1. Inline sparklines sit beside the sentence they support.
2. Side notes hold annotation instead of hiding it in a tooltip.
3. Small multiples repeat one chart grammar across distinct data slices.
4. Series labels sit at their endpoints when direct labelling is possible.

## Avoid

Do not use chart junk, 3D charts, dark gridlines, decorative colour, or a legend when direct labels work. Do not make a data page resemble a dashboard by turning every figure into a rounded tile.

## Do not use when

The chart is decorative, the reader needs rich filtering, or the primary audience is on a small phone. Use a product-data pattern instead.

## Subject-mining prompt

What is the smallest visual distinction that lets this audience compare the thing that matters? Make that distinction visible and remove the rest.
