# Persuade Conversion: One Offer, One Audience, One Action

Load this only when the surface's visitor mode is **Persuade**: a landing page, campaign, pricing page, or waitlist whose job is a decision. Do not load it for Operate, Read, Experience, native Mac chrome, dashboards, settings, docs, checkout, auth, or payment.

The standing UX canon still binds: one primary action, trunk test, real states, honest errors, recognition over recall, proportional friction, accessibility as a floor, and the ethics gate. This file adds conversion architecture, not a visual system and not a second house style.

**Source.** Structure and conversion rules from [ai-design-skills landing-page-design](https://github.com/elayadesign/ai-design-skills/blob/1c1e97cb9878e236552c772092dda7adcdddbcb2/skills/landing-page-design/SKILL.md) (snapshot `1c1e97cb`, accessed 2026-08-31). Font whitelist, hyphen ban, forced heading gradients, and a universal landing-page costume were not imported: those would replace one house look with another.

## The contract

Write one sentence before any section list:

> One offer is <offer> for <audience>. The primary action is <verb + what they get>. Conversion is <click / signup / purchase>.

If that sentence cannot be written, the page is not a Persuade surface, or the brief is incomplete. In autonomous mode, infer the sentence and record the inference.

## First viewport

Required, in this order, unless a named exception applies:

1. Headline: outcome plus audience.
2. Subheadline: what it is and how, in one or two sentences.
3. Primary call to action: a verb plus what they get. Never "Learn more" or "Submit".
4. One proof signal: a real logo, a sourced number, or a short testimonial. Invented proof is a High ethics finding, not a placeholder to style.
5. A hero visual that demonstrates the offer, or an honest placeholder naming the missing asset.

The primary action must be visible without scrolling at 1280px and at 375px. A first viewport whose call to action sits below the fold is a High finding.

## The argument, then the objections

Mid-page does one job: make the offer believable. Use the sections the argument needs, not a fixed twelve-block template.

Typical useful blocks, used only when they carry new information:

- Problem to solution, one section
- Three to five outcome-led benefits
- How it works, as a real sequence with recovery, not a decorative 3-step strip
- Proof beside the claim it supports

Bottom of page handles remaining objections:

- Frequently asked questions as plain questions and answers
- Risk reversal that is true: trial, cancel, guarantee, or "no card needed"
- Final call to action using the **same label** as the first viewport

Do not invent a logo wall, fake metrics, or a guarantee the product does not offer. An honest gap beats decorative trust.

## Layout families, not a costume

Pick one and say why:

| Type | Use when |
|---|---|
| Classic hero plus sections | The product is understandable from one screenshot or object |
| Long-form story | The visitor needs education before they can act |
| Minimal conversion page | High-intent traffic, a download, or a waitlist |
| Comparison page | Search intent includes alternatives |

Then run `references/flow-shape-variety.md` so the chosen family is not the same 3-feature, 3-step, FAQ skeleton as the last Persuade page. Proof placement, orientation, and commitment are the useful axes here. Device still matters: the mobile primary action stays in the thumb zone (`references/mobile-ux.md`).

## Copy

Write benefit first, then the proof or mechanism. Specific beats category language.

- "Cut weekly reporting from 4 hours to 15 minutes" rather than "streamline reporting".
- One primary action label reused in nav, hero, and footer.
- Headlines name an outcome a visitor could disagree with.

`references/ux-writing.md` still owns the words. This file does not add a second copy register.

## What never changes here

- **Non-negotiable 1:** one primary action. A second equally weighted button in the first viewport is a defect.
- **Ethics gate:** scarcity, social proof, and deadlines must be true. An invented claim in a high-contrast, well-set first viewport is worse than an honest gap on an unfinished page.
- **Non-negotiable 12:** do not print verification output on the page.
- **Visual craft** stays in `design-craft:design-craft`. Do not use this file to pick fonts, radii, or palettes.

## Delivery line

```
PERSUADE
  offer: <one sentence>
  action: <label>
  first-viewport CTA visible: 1280 yes/no · 375 yes/no
  proof: real | honest placeholder | missing
  flow-shape: <axis taken or category-standard with reason>
```
