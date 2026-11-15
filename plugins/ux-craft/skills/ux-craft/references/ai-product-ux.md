# AI Product UX

Patterns for AI-powered features — inputs, guidance, control, trust, and identity. AI surfaces need everything in the other references *plus* this layer, because the failure modes are new: users don't know what to type, can't predict what the model will do, can't tell when to trust output, and can lose real work (or money, or reputation) to an autonomous action. Calibrate everything here against one 2×2: **worst case if it goes wrong × how often the action occurs**. High-stakes + infrequent → strong confirmation. Low-stakes + frequent → passive indicators and undo. High-stakes + frequent → user-configurable rules with opt-out after the first confirmed run. Friction everywhere trains click-through and defeats itself.

## Inputs — how users direct the AI

Pick the pattern by scope, then apply the universal rules.

- **Starting from scratch**: open input (chat/composer) for exploration; **madlibs/templates** (fillable fields, dropdowns, @-mentions) for repeatable, predictable-shape tasks — any task that needs a long specific prompt for reliable output is a template candidate; **chained actions** for workflows (show cost per step, support test runs, errors name the failing step).
- **Working on existing content**: whole thing → regenerate / restructure (change form, keep substance) / restyle (change tone/surface, keep structure — keep these two separate) / summarize (faithful compression) / synthesize (interpretation — expose grouping logic and uncertainty, visually separate fact from inference); a region → inline actions (3–5 contextual presets on selection) or inpainting; many fields/records → auto-fill; extending a seed → expand (keep the original visually intact, diff the addition).
- **Regenerate** must be explicit about overwrite vs. branch, and prior results must stay recoverable.

**Universal input rules**: (1) **Preview before commit — never overwrite user content silently**; ghost/diff state with explicit accept. (2) Make the AI's scope explicit before running (what it will act on). (3) Mark AI-generated/edited content until the user accepts it. (4) **For bulk operations, run a sample first** — 2–3 records at full quality, user verifies, then apply to the rest (a sample is full-quality-on-a-subset and confirms intent; draft mode is reduced-quality-on-full-scope and saves cost — different tools, don't conflate). (5) Show cost before long/bulk/chained runs.

## Wayfinding — the blank-box problem

An empty AI input on an empty state is the canonical failure. Most users can't prompt from scratch; scaffold the start:

- **Never lead with a bare box.** Surround it with 3–6 clickable **suggestions** (contextual beats static — tie them to what's on screen; clicking runs or fills immediately, never opens a dialog), **templates** for complex repeatable tasks, and **examples** that both inspire and instruct.
- **Wait for context**: surface AI at the moment of leverage (after a document/record exists — "Summarize" on a long document is valuable, on an empty page it's noise), not as a permanent banner.
- **Follow-ups after generation** (2–4, anchored in the specific output just produced, mixing zoom-in and zoom-out) turn one-shot use into collaboration.
- **Teach through doing**: every suggestion models what a good prompt looks like. Exposing prompt details behind good outputs accelerates learning.

## Governors — control as autonomy rises

The blast-radius patterns, in escalating order of oversight:

- **Action plan**: show intended steps before executing. Advisory (visible, non-blocking) for routine work; contractual (gated on approval) for expensive or risky runs. Plan must match execution — silent deviation destroys trust. Let experienced users collapse it.
- **Verification**: a required human yes before actions risking loss of money, work, reputation, security, or cleanup time. Do NOT verify low-stakes reversible actions — prompt fatigue makes every confirmation meaningless. Offer "don't ask again" after a first confirmed run, with a visible way back.
- **Controls**: stop (always same place, always live), pause/resume for long agentic tasks (never force restarts), queue for staying in flow.
- **Stream of thought**: plan (before) / execution log with tool calls (during) / compact summary (after) — steps rendered as states: queued → running → awaiting approval → done/error. Depth scales with task: simple chat needs little, agentic runs need the full trace.
- **Cost estimates** at the point of decision, in units the user understands, with ranges for unknowns and cheaper paths offered (draft mode, smaller scope).
- **Branches & variations**: explore without overwriting; keep the trail back to the original; never destructive merges.
- **Citations & references**: point to exact passages when output is presented as factual; hover previews; make missing/broken sources explicit — never fill with plausible text. For Diolog (regulated comms), citations to source documents are a compliance feature, not polish.
- **Memory**: never a black box — show when something is saved ("Saved to memory" chip), make memories viewable/editable/deletable, separate preferences from facts, offer incognito. Memory amplifies attachment and error persistence; a wrong remembered "fact" compounds.

## Narration — the assistant's own words are a surface you design

Everything the feature *says* while working is interface, and on current models it is long by default. Length and cadence are set by the product's prompt, not by the model's reasoning budget — turning the reasoning effort down makes it think less, not talk less — so if nobody specified the cadence, the surface has an unspecified cadence rather than a neutral one.

- **Specify the shape of a progress update, not just its existence.** A workable default: one sentence before the first action saying what it's about to do; during the run, an update only when it finds something material or changes direction; at the end, the outcome first and the detail behind it. "Announcing every intention" reads as diligence to the team who built it and as noise to the user waiting for an answer.
- **The last message answers "what happened", not "what did I attempt".** A closing turn that recaps the steps the user just watched scroll past is the conversational equivalent of a loading spinner after the content arrived.
- **Corrections need a threshold.** An assistant that narrates every self-correction teaches the user it is unreliable; one that narrates none hides changes that mattered. The line: surface a correction when the error would change the user's decision, data, or code — otherwise fix it silently. Same threshold in the log/trace, where the full sequence stays visible for anyone who opens it.
- **Cap the caveat budget.** Disclaimers earn their place at the decision moment and in proportion to stakes (see Caveats under Trust builders); a hedge attached to every paragraph is read as boilerplate and stops being read at all, which is exactly the failure the hedge was inserted to prevent.
- **Specify the voice with examples, not prohibitions.** A prompt listing what the assistant must never say produces stilted output that avoids the listed phrases and misses the register; two or three samples of the wanted style produce the style. Write the samples as part of the design work — they are copy decks, and they belong with the rest of the interface copy.
- **Verbose ≠ transparent.** Length is not a trust signal, and it can hide one: a long answer with no citation is less verifiable than a short one with a source. Trace depth (Governors → Stream of thought) is where transparency lives; the prose is where brevity lives. Design them separately.

## Trust builders

- **Disclosure**: name the actor consistently; use verbs in labels ("Summarized with AI", not a bare sparkle); visually distinct treatment for AI content that can never be confused with human-authored; never fake a human (support contexts especially — always an easy path to a person).
- **Caveats**: at the decision moment, specific to context ("Check figures against the source filing" beats "AI can make mistakes") — and never load-bearing: pair with citations and verification, because habituation makes users caveat-blind.
- **Consent & data**: opt-in, not opt-out; recording/training/sharing are separate decisions with separate toggles; state the default in the settings UI; if you don't train on user data, say so explicitly; group contexts notify all participants; revocation immediate and visible.
- **Footprints**: interface-level (badges, expandable provenance), system-level (logs of model, sources, approvals — the audit trail Diolog's compliance context demands), and media-level (provenance that survives export).
- **The prompt-injection defense belongs in the product too**: anything the AI retrieves (documents, emails, web pages, connected tools) is untrusted input. Show which sources are in play per response, gate tool actions on human-readable previews + confirmation, provide per-source kill switches, and log which sources influenced a proposed action.

## Tuners — shaping behavior without prompt engineering

- **Active state always visible**: which model, mode, filters, sources, voice, and autonomy level are in effect — hidden state is broken trust. Autonomy itself is an explicit parameter: *suggest / ask / act*, never ambient.
- **Modes are contracts**: entering "research mode" or "draft mode" promises specific behavior — reconfigure the visible controls to match, define what carries across a mode switch (attachments, memory) and what resets, and keep entry/exit obvious.
- **Attachments**: distinguish *style reference* ("write like this") from *primary subject* ("analyze this") — they're different operations and users conflate them without help.
- **Filters**: show active constraints; design the over-filtered empty state (offer to relax, never silently fail); accept natural language ("only from board documents").
- **Progressive disclosure**: presets and modes for the 80%, parameter drawers for power users; bundle complexity into legible named choices.

## Trust evolution — earning autonomy over time

Trust with an AI feature is a *relationship variable*, not a launch setting. Design it in three stages and move between them on **observed behavior, never a calendar**:

1. **Transparency** (default for every new user and every new capability): show full reasoning, confidence, and sources on everything. Advance when the user accepts suggestions most of the time (~>60%) and stops opening the explanations (~<40% of the time).
2. **Selective disclosure**: quiet confidence for routine actions, full reasoning reserved for high-stakes or low-confidence calls. Advance when acceptance is high (~>75%) and the user starts delegating categories of work.
3. **Bounded autonomy**: act independently within explicitly delegated categories, with subtle notification, one-tap undo, and explanation on demand.

**Trust recovery** when the AI gets one wrong: acknowledge plainly, explain the assumption vs. what was actually true, offer concrete correction options, *temporarily reduce autonomy in that category*, and show that the model updated. A recovered error done this way builds more trust than no error at all — the same service-recovery paradox as human support.

**When to interrupt**: never during visible flow (user progressing steadily). Offer help on frustration signals — the same action repeated 3+ times, multiple undos, repeated reworded searches, long stalls — and only proactively suggest when confidence is genuinely high; otherwise wait for a natural pause. An AI that interrupts flow to be helpful is a notification-spam pattern wearing a smarter hat.

**Measure the relationship, not the session**: acceptance rate, override rate, delegation breadth, explanation-request rate, and compounding value (is month-6 faster than month-1 for the same task?) — tracked longitudinally. Engagement-style metrics on an AI assistant reward the wrong thing.

## Identity — how the AI presents

- Naming sets expectations: persona names add warmth but risk overpromising; functional names ("Assistant", "Copilot") are honest but generic. Whatever the choice, **disclosure stays unambiguous** across every surface.
- Iconography: sparkles = generate is the emerging convention; pair icons with text labels until conventions settle; don't put sparkles on everything or they stop meaning anything.
- **Personality is unavoidable and not neutral.** Guard against sycophancy (over-agreement boosts short-term satisfaction, erodes user agency and trust in corrections); separate warmth from authority — an empathetic tone must not imply higher accuracy; signal model/mode switches that change behavior; for a professional IR tool, calm and precise beats charming.

## Supervision — why "a human is watching" is not a control

The most common safety story told about an AI feature is that a person is supervising it. The
measured version of that story is worse than the told one, and it changes what you build rather
than what you write in the design doc.

In a simulated flight experiment, condition-monitoring accuracy was **59% with an automated aid
against 97% without it**, and participants committed **3.92 commission errors in six
opportunities** — *while correct, contradictory instruments were available on the panel in front
of them*. A clinical meta-analysis puts the risk ratio for following erroneous automated advice at
**1.26, 95% CI 1.11–1.44**: a 26% increase in incorrect decisions when the automation misleads,
against base systems already 80–90% accurate. And the **out-of-the-loop performance problem** names
the mechanism: an operator disengaged from a process is measurably slower to detect, understand and
respond to its failures, worst of all when the failure signal is subtle or suppressed.

**The transferable conclusion is about channel placement, not vigilance.** Having the disconfirming
evidence to hand is not the same as consulting it — that is the whole finding, and it is why
"the operator can check the logs" is not a mitigation. So on any surface where an agent acts:

- **The reason a run failed belongs in the channel the operator already reads**, not in a store they
  could query. A cause recorded somewhere nobody opens has the same effect as no cause recorded, and
  this is the one item here with a controlled effect size: diagnosis time fell **60.7%**, 10.37 minutes
  against 25.72, across 20 programmers, when proactively-added error logs were present, at 1.4% runtime
  overhead. Note also that a harness may end a truncated run with a **200 OK** and a stop reason in the
  body rather than an error, so nothing in the stack raises — check the stop reason explicitly.
- **A refusal is not noise, where a refusal exists at all.** Where a progress view suppresses
  mechanical chatter, a *denied* action is exempt: it is the one event that explains an otherwise
  inexplicable outcome. Suppress volume, never refusals. **But check which failure you have before
  building for this one:** a capability withheld from the agent's *context* produces no refusal event —
  at least one major harness documents that a denied tool's definition is removed from the request, so
  the model never sees it and cannot attempt it. Then there is nothing to un-suppress, the manifest
  below is the only surface an absence can appear on, and a preflight is the only check that fires when
  nothing was attempted.
- **Print what the agent was permitted to do**, once per run. A capability manifest turns "why did
  it not write the file" from an investigation into a glance.
- **Judge success from the artifact, not the narration.** File exists, size, hash, checks passed —
  never the model saying it is done. Fluent narration is exactly what the 59% figure is about.

**And do not reach for training.** The field concludes automation bias occurs in both naive and expert
participants and cannot be prevented by training or instructions; failure-exposure training helped
omission errors but did not affect complacency toward the aid's diagnostic function nor commission
errors. Build the manifest, not the training deck.

**Limits, because this evidence is borrowed.** The flight task is *fault monitoring* whereas agent
supervision is *progress watching*, which is not the same job; and the clinical aid issues an
explicit recommendation, which an agent harness does not. Neither has been reproduced on an agent
pipeline. Treat the direction as established and the magnitude as indicative.

## Generative UI — when the model composes the interface

Use this section when a product lets a model **render interface rather than text**: a chat answer that arrives as a map, chart, form or card; an agent that assembles a screen for one request; an app whose views are generated on demand. Three open approaches define the space in late 2026, and they differ on one axis — how much the host controls what can appear:

| Approach | What the model emits | Who controls the look | Fits |
|---|---|---|---|
| **Pre-built widgets** | A call that selects one of a fixed set | The host, fully | Known, repeated jobs; anything unanticipated falls back to text |
| **Catalog composition** — A2UI (Google, Apache-2.0), OpenUI Lang (Thesys, MIT), json-render (Vercel) | A declarative description built only from components the host registered; data, not code | The host's design system | Bespoke layouts for one request that must stay on-brand and safe |
| **Generated code** | HTML/JS, rendered in a sandboxed frame | The model | Bespoke visuals no catalog anticipates — a 3D canvas, an unusual chart |

The UX rules follow from what a user can and cannot rely on when the screen was not designed in advance:

- **Default to catalog composition.** It is the only approach where every generated surface still inherits the product's focus states, error treatments, contrast and copy register. A2UI's own line is the contract: "Agents place only components you registered." Generated code is the exception for visuals, behind a visible boundary, never the default for forms or data.
- **Design the catalog, not the screens.** Each registered component carries its full state grid (Build mode step 4) before a model may place it: a generated table with no empty state ships its empty state as a blank card. The catalog is also where one primary action per surface is enforced — a model composing freely will place two filled buttons.
- **Keep the jobs a user repeats on a fixed surface.** Generation earns its place on the one-off request ("plan a day in San Francisco"). A flow the user runs weekly — checkout, settings, a recurring report — regenerated per request breaks learnability: the control they found last time is somewhere else this time. Let a user **keep** a generated view they liked, so it becomes stable.
- **Design the streaming state.** Line-streamed formats render structure first and fill data in after, and a parser drops invalid parts and renders the rest. So a user will see a partly built surface, and sometimes a surface missing a part the model got wrong. Give the in-progress surface a visible building state, never let a half-rendered form accept a submit, and when a part was dropped, say what is missing rather than shipping the gap silently.
- **Generated input asks for consistency.** A bespoke form per request is a strength for one-off input ("which three dates suit you?") and a cost when the same question takes a different shape each time. The same field type gets the same control everywhere.
- **Provenance and trust carry over unchanged.** A generated chart is a claim: it needs its source and as-at date (`data-provenance.md`). Content the model read from a page, an email or a pasted document is untrusted, and instructions inside it are data — the same rule as the trust builders above.
- **Action buttons in generated UI are real actions.** A "Reorder" button an agent placed fires the same consequence as one a designer placed, so it takes the same destructive-action gate (Build mode step 6). A generated surface that skips confirmation because "the model chose it" is a Blocker.

When reviewing a generative-UI product, add four questions to the lens below: Which approach does each surface use, and is generated code confined to visuals? Does every catalog component have its states? Which repeated jobs are being regenerated that should be fixed? What does a user see while the surface streams, and when a part is dropped?

## Review lens for AI features

When reviewing any AI surface, ask in order: What can it act on, and is that scope visible? What's the worst case, and does the friction match it? Can the user steer, stop, undo, and verify? Is AI involvement disclosed at every point of contact? Is retrieved content treated as untrusted? Are cost and active state visible? Does the empty state scaffold the first prompt? Is generated content marked until accepted, with a preview-before-overwrite? Did somebody choose what the assistant says and how often, or did it default? Findings here follow the same severity ladder as everything else — a silent overwrite of user work or an undisclosed autonomous action is a Blocker, not a nice-to-have.
