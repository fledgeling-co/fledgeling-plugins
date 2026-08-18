# Discovery Questions: Kickoff Question Protocol

Run a structured question round at the start of new or ambiguous design work. Use this whenever the user asks for something new and you don't already have what you need to start. **Asking good questions is the single biggest lever for design quality.** Bad designs come from missing context, not missing skill.

## Phase 1: Read what's already attached

Before asking anything, **read every attached resource** the user has provided:

- Codebases or files
- Screenshots
- Brand guides or PDFs
- Linked design system or UI kit projects
- The user's stated brief

Your questions should be informed by what's already there. Asking "do you have a brand guide?" when they just attached one is the fastest way to lose the user's confidence.

## Phase 2: Decide whether to ask

**Ask when:**

- The work is new or ambiguous
- The output, audience, or fidelity are unclear
- You don't know which design system, UI kit, or brand is in play
- The user hasn't specified how many variations they want
- The task spans multiple non-trivial dimensions (audience + format + tone + content all unspecified)

**Skip asking when:**

- The user gave you everything you need
- It's a small tweak or follow-up to existing work
- The user is explicit about scope, audience, and constraints
- The task is "recreate this exact thing" (a clear reference)

If the open question changes the design's direction (audience, format, brand, scope), ask. If it's a minor choice you can defensibly make yourself (a label, a default value, two equivalent approaches), decide, build, and note the decision in your summary instead of asking.

**Ask everything in one round.** You do your best work handed a complete brief and left to run, so the goal of this phase is to make the brief complete *before* you start — not to drip-feed questions across the build. Front-load every direction-changing question into the single kickoff round, then execute. Coming back mid-build for something you could have asked at the start costs the user a context switch and costs you the units already drafted against the wrong assumption (Phase 7 covers the exception: a signal that genuinely changes during the work).

## Phase 3: Build the question set

**One question is always asked. Everything else is asked only when the brief leaves it open.** A fixed list of six categories is a quota, and a quota contradicts the rule this file's own anti-patterns end with — a question is justified by the design impact of its answer, not by your uncertainty.

### The one always-ask: the starting point

- **"Is there a UI kit, design system, codebase, brand guide, or screenshots I should match? If not, I'll commit to an aesthetic from scratch — confirm that's OK."**
- Non-negotiable, because starting hi-fi work without context produces bad design and because the answer changes every later decision. Confirm it with a question rather than with an assumption.

### Ask these when they are genuinely open

- **Where will you open this?** A file you open yourself, a page I publish for you, or something you'll pin to a phone. Ask when the brief hasn't said and the answer would change what you build — a scroll-driven GSAP page and a CSP-bound Artifact are two different commissions (`delivery-surfaces.md`), and discovering that at handover costs the whole build.
- **Variations.** How many, and on what axes? Skip when the user already said, or when the deliverable is one settled surface.
- **By-the-book or novel?** Ask when the brief's register is genuinely ambiguous, not as a warm-up.
- **Focus axis** — flows, copy, or visuals? Ask when you can't tell where the exploration budget should go.

### Assert these rather than asking them

- **Visitor mode.** Persuade / Operate / Read / Experience. State your reading and invite correction — "reading this as an Operate surface: the user is here to reconcile transactions, not to be sold to." It is usually obvious from the brief, and it governs everything downstream (`visitor-modes.md`), so a wrong reading is expensive and a menu is slow.
- **Tweak controls.** SKILL.md §18 already adds 1–2 by default, so asking which knobs the user wants is asking them to do the job you were given. Choose the axes, expose them, and name them in the summary.

### Problem-specific (4+)

These vary by the task. Examples:

**For a landing page:** what action should users take? primary persona? competitors/references that inspire (positively or negatively)? mobile-first or desktop-first?

**For an interactive prototype:** what flow / what screens? hi-fi or mid-fi? device frame? goal state of the flow? sample data to fill the screens?

**For a brand or aesthetic:** mood/tone in 3 adjectives? existing brands you admire (and what specifically)? anything explicitly off-limits? industry/context (B2B SaaS, consumer, editorial, government)? how should it make the user *feel* (trust, delight, confidence, calm)?

**For a mobile app screen:** which platform grammar (iOS / Material / both)? which user stage is this screen for (new / returning / power)? installable on a real phone or presentation-framed?

Size the round to the ambiguity: a genuinely open brief may warrant ~10 questions; a half-specified one only 3–4. Never pad the round to hit a number — a question whose answer wouldn't change what you build is noise.

### Special case: "surprise me / show me something cool"

When the user explicitly opens the door to anything (never as a default), do NOT start building. Ask ONE single-select question offering 4–5 enticing, concrete directions — e.g. "A generative art piece / A playable mini-game / A slick product concept / An interactive data visualization" — plus a **"Decide for me"** option (then pick the direction *you* can execute most impressively) and a freeform "anything you're into — a theme, a hobby, a vibe?". Then build the most polished, visually striking version you can: **favor motion, interactivity, and craft over breadth** (`motion-design.md` and `depth-and-3d.md` are your ammunition).

## Phase 4: Format the question round (AskUserQuestion)

In Claude Code, use the **`AskUserQuestion`** tool to render the round as structured choices instead of a wall of free text. It accepts 1–4 questions per call (2–4 options each, with "Other" added automatically), so a larger round becomes one or two `AskUserQuestion` calls grouped by theme (e.g. one call for context + variations, one for audience + tone).

For each question:

- **Prefer concrete options** over open-ended text — easier for the user to answer. Put your recommended option first and mark it `(Recommended)`.
- **Offer escape hatches.** Where it fits, include an "Explore a few options" and/or a "Decide for me" option — users often want them. ("Other" is always available for freeform.)
- **Use `multiSelect: true`** when choices aren't mutually exclusive (e.g. "which axes should I vary on?").
- **Use the `preview` field** for visual/structural choices — drop in a small ASCII mockup or code/token snippet so the user can compare layouts, palettes, or component styles side by side.
- Keep `header` labels short (≤12 chars) and questions specific.

If a question is genuinely open-ended (a freeform description, a pasted reference), ask it in plain text instead of forcing it into options.

## Phase 5: End the turn

`AskUserQuestion` blocks until the user answers — after calling it, **end your turn.** Do not anticipate answers and proceed before they respond. When the answers come back, read every one before starting to design.

## Phase 6: Confirm and proceed

Once the user has answered:

- Declare a one-line **Design Read** so your interpretation is on the table: "Reading this as: ⟨page kind⟩ for ⟨audience⟩, with a ⟨vibe⟩ visual language, leaning toward ⟨system/aesthetic family⟩."
- Briefly recap the choices that will most affect the design ("OK — landing page, B2B audience, formal tone, three variations on different visual treatments, single CTA, no novel ideas")
- Note any answers that surprised you or that you'd push back on (gently — the user is the manager)
- Then proceed to the appropriate building procedure (`make-a-prototype`, `wireframe`, `make-a-doc`, etc. — slides go to `deck-craft`) and execute autonomously. This round was your chance to ask — don't come back with follow-up questions for minor decisions; make them and list them in your summary.

## Phase 7: Re-question on signal change

If during the work you discover an early answer was wrong (e.g. the user said "no novel ideas" but their feedback shows they want bolder choices), re-question. Don't carry on with the wrong assumption — surface the contradiction and confirm.

## Anti-patterns

- **Don't skip asking.** "I'll just start building" produces designs that miss the brief.
- **Don't ask everything.** A 30-question form is hostile. Cap around 10–15 for most work.
- **Don't ask one at a time across multiple turns.** Bundle into one or two `AskUserQuestion` calls.
- **Don't ask about details you can derive.** If the user attached a brand guide with their primary color, don't ask what their primary color is.
- **Don't ask to be safe.** A question is justified by the design impact of its answer, not by your uncertainty.
- **Don't ask for CSS values or canned aesthetic lanes.** "What border radius do you want?" and "pick a vibe: minimal / bold / playful" both hand the design decision back to the user in the one form they can't evaluate. Ask about the job, the audience, the proof, and the constraints; commit to the aesthetic yourself and present it (`frontend-aesthetic-direction.md`).
