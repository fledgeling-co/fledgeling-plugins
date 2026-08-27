<p align="center">
  <img src="assets/banner.png" alt="generate-investor-portal: a porcelain app icon of an open strongroom door with a warm lit room behind it and one pale record standing inside, beside the wordmark and the line: one generated record per company, and a gate reads it back before anything publishes, a figure with no provenance is refused, not flagged. To the right, the same room at scale, cropped by the frame." width="100%">
</p>

<h1 align="center"><img src="assets/icon.svg" alt="" width="34" valign="middle" /> generate-investor-portal</h1>
<p align="center">
  <img alt="Version 1.0.0" src="https://img.shields.io/badge/version-1.0.0-D33C21">
  <img alt="SWE skill: generation" src="https://img.shields.io/badge/SWE_skill-generation-434A55">
  <img alt="Blind panel: 6 of 7 tasks" src="https://img.shields.io/badge/blind_panel-6_of_7_tasks-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

Turns a company's design tokens and a crawl of its own website into one validated database record, then refuses to write it until a gate has read it back.

An investor portal built this way is not a website. The website already exists: one generic renderer serves every company from a record, resolved by hostname, so onboarding a new company is a generated record rather than new code. What this skill produces is that record, and what makes it worth using is what it will not let into one.

## Install

```
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install generate-investor-portal@fledgeling-plugins
```

Then ask for what you want in plain language. "Make ACME a paid portal", "regenerate the portal for BHP after the rebrand", or hand over a DESIGN.md plus a company overview and ask for a portal from them.

## The problem it exists for

A document written for external investors has one worst failure available to it, and it is not an ugly layout. It is a number nobody supplied.

The research behind this skill is blunt about how likely that is. A study of 197,000 questions about company revenue found that language models hallucinate *more* for larger, better-known companies in recent periods, which is exactly where a reader is least likely to check. A separate study masked numbers inside real annual-report tables, gave the model the table, and found it still returned figures that disagreed with the source on plain lookups. Fluency is not a signal. A citation is not a signal either: a peer-reviewed benchmark found the best systems tested lacked complete citation support half the time.

So the interesting question is not "how do we ask the model nicely". It is what a machine can refuse.

## What it refuses

Every rule below is a check in `assets/record-gate.mjs`, which runs against the record file with no server, no database, no deployment and no network. There are over 600 of them on a real record. The gate refuses the *write*, never the *read*, so adding a rule can never take a live portal off the air.

**A figure is not allowed to live in prose.** This is the honest version of "do not fabricate". A fabricated number does not arrive as a marked value with a bad source. It arrives as a sentence: "$412 million in contracted revenue" in a hero paragraph, rendered in the same type as a disclosed figure, carrying no date, no source and no marker. Nothing that inspects the provenance fields can see it. So a currency amount, a percentage, a thousands-separated number or a date in any prose slot is refused unless it sits inside a provenance-marked value.

**A missing figure becomes a visible, readable placeholder.** Not a blank, not a zero, not a plausible estimate. The record carries one of three states with no default, because the default used to be "this figure is real". And the placeholder has to be readable text rather than a pale dash or a lone superscript marker, which is an accessibility requirement rather than a matter of taste.

**A republish is refused before anything is crawled or generated.** The old version discovered a published record at the moment it tried to write, by which point the run had crawled a stranger's website twice and paid for image generation. That check now runs first.

**The crawl is treated as untrusted input.** The main input is a few thousand lines written by people outside the trust boundary, read by an agent with database write access and a paid image budget, and then fed verbatim into an image model as context. A fence sentence travels into every subagent brief and every image prompt, because a subagent cannot see the parent instructions and an image model certainly cannot.

**Two companies cannot ship the same portal.** The defect that survived every check on the live platform was between tenants, not inside one: a junior mining explorer and a national telco published the same eight pages, with the same section kinds in the same order, under the same layout. Every per-tenant check was green, and had to be. Sameness is a property of a pair.

**A mandated disclosure surface cannot simply be absent.** "Does the company do this" and "is the company obliged to publish this" are different questions, and an evidence threshold is the right answer to the first and the wrong answer to the second. A governance surface with nothing behind it says so, in words, rather than vanishing.

**Colour is checked arithmetically, by role.** A brand accent that is correct as a button fill can be unreadable as thirteen-pixel text, and a blanket floor over the accent rejects the brand colour everywhere it belongs. So the floors follow the role: 4.5:1 for body-size text, 3:1 for large text and fills. The arithmetic runs on hex values, never on a browser's computed styles, which is deliberate and worth keeping.

## What it will not do

It will not publish. Records are written as drafts, and publishing an investor surface is a human decision.

It will not edit one section. There is no targeted mode, and pretending otherwise would be worse than the gap: a one-token fix is a full regeneration from a fresh crawl, and the whole record changes.

It will not invent a figure to fill a section, generate a likeness of a real person, or present a generated photograph as depicting a real site or employee.

It will not touch the renderer. If a section cannot be expressed, the vocabulary gets extended in the contract on purpose, rather than worked around in the record.

## How to check it still works

```bash
node assets/record-gate.mjs record.json --peers ./published   # exit 0 required to write
node assets/record-gate.mjs --self-test                       # proves the gate still bites
```

The self-test runs four fixtures in `assets/fixtures/`, three of which are supposed to fail, and reports it as a failure if they pass. A gate that has quietly stopped catching things looks identical to a clean run, which is the whole reason the self-test exists.

Those fixtures are also the dry-run path. The record layer can be exercised end to end against a fictional company with no crawl, no database and no spend.

## Does it actually work

Eight tasks, run once under the original version of this skill and once under this one, then paired up and handed to three judges from three different model families with neither version shown to them. Over the six tasks both versions completed the report card was 28 of 30 for the original and 30 of 30 for this one, and the panel picked this version on six of the seven tasks it could judge, including two it first gave to the original and reversed after the losses were fixed.

The two losses, the task that never completed, the four assertions that could not fail, and the judge lane that hit a usage limit are all in [`evals/EVALS.md`](evals/EVALS.md), which also says plainly what the numbers cannot tell you.

## Honesty about the gate

The gate reads the record, so it proves things about the record. Anything the renderer decides for itself is outside its reach, and that is not hypothetical: on the live platform a single inline style reached past a compliant token and put a company's own name at 1.97:1 on five of six portals while the record-level check stayed green. That needs a second gate at the source layer, not a bigger claim from this one.

It also cannot decide materiality, cannot tell you which disclosures are legally mandatory for a particular entity, and cannot tell you that a technically accurate page is contextually misleading. Those are human judgements and the skill says so rather than implying coverage it does not have.

Nothing here is legal advice.

## Where it came from

The skill's substance, including every production incident it cites, comes from a working investor-portal pipeline in the Diolog codebase, where the original `generate-investor-portal` lives. That version is the source of the gate ladder, the collision keys, the provenance contract and the measured failures. This one adds the gate as shipped code, the injection fence, the pre-spend refusal, and a research corpus behind the rules.

That corpus is in `docs/deep-research/`: four independent deep-research reports read in full and citation-verified, with the citations that failed named rather than dropped, and the disagreements between them left in `references/evidence.md` rather than tidied away.

## Files

| Path | What it is |
|---|---|
| `skills/generate-investor-portal/SKILL.md` | the procedure |
| `assets/record-gate.mjs` | the publish-tier gate, dependency-free, node or bun |
| `assets/fixtures/` | one passing record, three deliberately failing, one published peer |
| `references/record-shape.md` | what a record carries, field by field |
| `references/tokens-and-motion.md` | lifting a theme, and the tokens brands forget |
| `references/imagery.md` | find before you generate, and what is never generated |
| `references/validate-and-prove.md` | the four-tier gate ladder and what each tier costs |
| `references/binding-decisions.md` | content decisions that bind |
| `references/refused-ideas.md` | six ideas that look good and are not |
| `references/what-shipped-wrong.md` | the production incidents, dated and measured |
| `references/evidence.md` | the external citations, with the thin spots named |
| `docs/deep-research/` | the full research corpus |
