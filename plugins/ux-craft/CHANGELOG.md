## 2.7.0 - 2026-11-22

- **Generative UI as it ships now.** A2UI reached 1.0 on 11 November, and MCP Apps puts third-party UI inside Claude, ChatGPT, VS Code and Microsoft 365 Copilot. The guidance covers what that changes: a generated picker that checks availability as you choose needs its live states like any form, the same agent can render in hosts that draw it differently (so the plain-text fallback has to carry the answer), and actions started from embedded UI go through the host's approval rather than a second one of your own. An intent bar speeds up a stable layout; it does not replace one.
- **Agents that spend money or get rubber-stamped.** A booking or purchase an agent makes takes a fresh yes each time, and a standing rule shows its cap, its spend and where to revoke it. An approval screen with a lone Approve button trains people to stop reading, so put the agent's evidence beside the decision and offer real alternatives.
- **Onboarding beyond the profile form.** Two credible alternatives: a short interview whose answers change a live preview, or a setup the product drafts from something you import and you edit. Flow variety gains a matching axis, and the AI-assistant shell (history sidebar, centred prompt box, suggestion chips, sparkle) is named as the default to vary from. A mascot is fine with a specific drawing and a job; the generic blob with a face is the tell.
- **Smaller updates.** Style the native select before rebuilding it (now in Chrome and Safari). Mobile platform grammar covers the iOS 27 Liquid Glass slider and Material 3 Expressive, now stable. The accessibility checklist carries the current legal dates (ADA Title II moved to April 2027 and 2028; WCAG 3 is still a draft). Persuade pages write their key facts as live text, because AI assistants read and cite them.

Note: the agentic and onboarding patterns come from shipped protocols and practitioner debate in late 2026, recorded in `references/evidence.md`. None of the sources measures their effect on completion or trust.

## 2.6.0 - 2026-11-15

- **Mobbin in every mode.** Real shipped flows before the step list is written; the two hardest states before the state grid is filled; one or two shipped examples cited beside each serious review finding (three searches at most per review); and a count behind any "users expect X" claim, e.g. "4 of the 5 checkouts I opened do this". It works without design-craft installed.
- **Generative UI.** New guidance for products where the model builds the interface, like a map or a form inside a chat answer. There are three approaches shipping now: fixed widgets, composing from registered components (OpenUI, A2UI, json-render), and sandboxed generated code. For forms and data it recommends registered components. Each one needs its full set of states. Repeated jobs stay on fixed screens. A half-built surface can't accept a submit, and a button the model placed gets the same confirmation as one a designer placed.
- **Two copy rules.** A changed number names its comparison ("+12% vs last month"), and a page title names the context rather than greeting the user.
- **Hero demos as proof.** A demo counts as proof on a landing page only when it shows one action a visitor can follow, and its still frame makes the claim on its own.

Note: a Mobbin count shows what users have learned, not what works. It skews towards well-funded consumer and SaaS products, so the skill says so on enterprise and regulated surfaces, and the ethics checks still apply whatever the count.

## 2.5.0 - 2026-08-31

Adds `persuade-conversion.md` for Persuade surfaces only: one offer, one audience, one action; first-viewport CTA visibility; proof beside claims; honest objection handling. Flow-shape variety now reads and records the project diversity ledger, and two evals cover both paths. Operate, Read, Experience, checkout, auth, and payment do not load the conversion layer.

## 2.5.2 - 2026-09-01

Closes the auditor findings on `gemini.md`: filled the exemplars the overrides only described, corrected counts and citations that disagreed with the target `SKILL.md`, and brought the file inside the 150-250 line bound. `verify_quotes.py` exits 0.

## 2.5.1 - 2026-09-01

Refreshes `gemini.md` against a `SKILL.md` that had changed since it was written. Written by the `geminify` Mode A procedure and gated by `verify_quotes.py`.

## 2.4.0 - 2026-08-31

Build mode names the category-default journey and varies it on one axis (`references/flow-shape-variety.md`) so two onboardings in a session are not the same 3-step wizard. Checkout, auth and payment still follow convention (NN8). The flow checklist reports the ledger.

## 2.3.1 - 2026-08-30

Every skill name written in a prompt or a cross-reference now carries its full
`plugin:skill` form. A bare name is not resolvable by the Skill tool, so a runner told to
invoke one gets `Unknown skill` and carries on without it.

Measured across 51,763 session transcripts over 21 days: 53 of 77 Skill invocations failed,
a 68% failure rate. Bare names were 27 of those. Four more came from agents that knew a
prefix was needed and invented one (`plugin:`, or the marketplace name).

# ux-craft changelog

## 2.2.1 - 2026-08-21

- Correction to the supervision section: a capability withheld from the agent's context produces no refusal to un-suppress, so the manifest and the preflight carry the weight and refusal surfacing is conditional on a refusal existing.
- The channel-placement recommendation now carries its controlled effect size, 60.7% reduction in diagnosis time at 1.4% runtime overhead, and the note that a truncated run can end with a 200 OK and a stop reason in the body rather than an error.
- Added the finding that automation bias cannot be prevented by training or instructions, with the failure-exposure result that helped omission but not commission errors. Build the manifest, not the training deck.
- evidence.md records all four with tiers and limits, and states that the mechanism was verified against the code rather than the documentation alone.

## 2.2.0 - 2026-08-21

- Non-negotiable 4 now carries the measured effect size for diagnostic quality: a pinpointing message is diagnosed 3-13x faster than an ambiguous one and 1.2-14.5x faster than none.
- `ai-product-ux.md` gains a supervision section. The skill governed AI surfaces and carried no automation-bias material at all; it now carries the 59%-against-97% monitoring collapse, the 1.26 risk ratio, and the out-of-the-loop mechanism, with the conclusion that matters for an agent surface: channel placement, not vigilance.
- `evidence.md` records all five citations with their tier and the limit on each, including that none has been reproduced on an agent pipeline.

