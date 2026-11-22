---
name: create-website
description: >-
  Build a complete multi-section website from a brief: a personal or portfolio site, a studio,
  small business, event or product marketing site, with a generated hero image, an optional
  generated video hero or real-time 3D scene, and motion through every section that still works
  under reduced motion, without WebGL and on touch. Runs one trawl:trawl pass to pick the site's
  world, takes a shipped Mobbin reference for each section, builds through
  design-craft:design-craft and ux-craft:ux-craft, checks the plan, the files and a scrolled
  browser capture with bundled scripts, and deploys only when the person says so, checking every
  path and the custom domain's states. Use whenever someone asks to "build me a website", "make a
  site for my studio", "a portfolio site with a video hero", "a landing page with scroll
  animation and a 3D hero", or "redo my personal site", even when they never say "website". Not
  for a launch site generated from a repo's product docs (launch-craft:launch-craft), a single
  app screen or dashboard (design-craft:design-craft), a standalone video
  (motion-craft:motion-craft), or reviewing a site that already exists
  (design-review:design-review).
---

# Create website

Build one served site from one direction, section by section, with the motion and media the
brief asks for and a working plain path under each of them. The deliverable is the site
directory, `.create-website/site-plan.json`, the media with its prompts and costs, the scrolled
captures, and a short report. Publishing is a separate act that waits for the person.

This skill orchestrates. The design judgement lives in `design-craft:design-craft` and
`ux-craft:ux-craft`, the idea-widening in `trawl:trawl`, the rendered review in
`design-review:design-review`. What this skill adds is the whole-site plan that ties them
together, the per-section reference and motion ledgers, the generated-video procedure, the
decision about where 3D comes from, and the checks that a scroll-driven, media-heavy site needs
and a static review cannot see. Every rule below traces to `references/evidence.md`.

**Running as a Gemini model?** Read `gemini.md` in this directory first.

## Route first

| The request is | Use instead |
|---|---|
| A launch or marketing site built from a repository's briefs, code and mocks | `launch-craft:launch-craft` |
| One app screen, dashboard, prototype or design system | `design-craft:design-craft` |
| A video or animation as the deliverable, made from code | `motion-craft:motion-craft` |
| A review or audit of a site that already exists | `design-review:design-review` |
| A résumé site, where the copy is the résumé's facts | `career-kit:career-kit` (it carries the copy rules this skill does not) |

Everything else that is a multi-section site comes here.

## What the person decides, and what you decide

Theirs: the facts on the page, the choice between two concepts that are both good, whether a
generated image carries a credit, the spend cap for billed generation, anything that deploys,
buys a domain or publishes, and whether a stylised likeness of a real person appears. Yours:
structure, references, motion, encoding, fallbacks and every check. Ask through
`clarify:clarify` when a fork reaches the person; batch the opening questions into one round.

In autonomous mode (a harness invoked you, or the brief says proceed without questions), write
each open choice into the plan as a stated assumption, generate no billed media past a quote,
and deploy nothing.

## Procedure

Work in the project's site directory, or `site/` when there is none. Keep run state in
`.create-website/` beside it: the plan, the trawl packet, the spend ledger, captures.

### 1. Brief and plan

Write `.create-website/site-plan.json` before any layout. `python3 scripts/plan_check.py
--example` prints a complete plan to start from. Fill in the subject, the audience and the device
they arrive on, the visitor mode (Persuade, Operate, Read or Experience, as design-craft defines
them), and every section with a one-sentence job. Take facts only from the person and their
material; a site about a person or business carries no invented figures, clients or quotes.

Ask the opening round now: facts you lack, the hero kind they want (image, video, 3D or plain),
the spend cap, and where it will live. `references/plan-and-references.md` has the plan's fields.

### 2. Widen the world with one trawl run

Invoke `trawl:trawl` once for the commission, through design-craft's aesthetic-ideation packet
(`design-craft:design-craft` → `references/aesthetic-ideation.md`), with three website additions:
the motion grammar the world implies, at most two signature moments, and what the hero is made
of. Use `--any` by default and `--standard` for a lasting brand identity or after a "too
generic" verdict. Record tier, pick, TOOK and LEFT in `plan.trawl`. If trawl is not installed,
record `"skipped": "trawl not installed"` and use design-craft's substitute; the plan check
warns on it so the report cannot imply a pass that did not happen.

### 3. One shipped reference per section

Search Mobbin yourself, following design-craft's checkpoints M1 (taste board, 3 to 5 searches
including one outside the category) and M2 (one gold per section type, `limit` 4 to 6). Open
the images; a result you did not open was not used. Write each section's `mobbin` block: the
query, how many results you opened, the gold, what you took in measurable terms (first-viewport
element count, frame, type sizes, where the focal object sits) and what you left. Adjacent
sections take different golds. Without the Mobbin server, write `"none": "<reason>"` per section
and say so in the report.

### 4. Build the plain site first

Build through `design-craft:design-craft` and `ux-craft:ux-craft` together, one section at a
time against its gold (design-craft's M5 side-by-side). Ship the content, navigation and calls
to action as semantic HTML with still imagery before any motion is added, so every enhancement
that later fails leaves a usable page. The hero's still (the poster, or the 3D fallback render)
exists from this step on.

### 5. Motion through every section

Give every section a `motion` block: entrance, scroll, hover, signature (two per site at most),
and the reduced-motion behaviour. Default to CSS transitions and CSS scroll-driven animation on
`transform` and `opacity`; reach for GSAP ScrollTrigger only to pin, to scrub a canvas or WebGL
scene, or to coordinate a timeline (`design-craft:design-craft` → `references/gsap-motion.md`).
Keep native scrolling. Under reduced motion, remove the effect and its dependencies so every
element ends visible and nothing stays pinned. `references/motion-map.md` has the rules and the
pitfalls each one came from.

### 6. Hero media

Record each billed call: quote it with `scripts/spend.py quote` and say the price before the
first one, then `spend.py add` and say the running total after each. `spend.py total --cap`
exits 1 when the person's cap is reached, and the next call waits for them.

- **Image.** Route through design-craft's `references/generate-images.md` with the
  `media-gen-pro` server's `generate_image`. Where the choice between concepts is real, generate
  several, tile them on one contact sheet, put it to `decision-panel:decision-panel` when the
  call is technical, and let the person pick when it is taste. Export display-sized AVIF or WebP
  variants with `srcset` and a phone crop when the subject would be cut; write alt text from the
  approved image, never from its prompt.
- **Video.** Follow `references/video-hero.md` in order: settle four things with the person,
  approve stills, generate image-to-video with first and last frames, then measure joins, the loop
  seam and flashes with `scripts/clip_tools.py` and encode with `clip_tools.py variants`.
- **3D.** Decide where it comes from before building, using `references/hero-media.md`:
  a still render, CSS or scroll depth, a three.js scene, or a mesh generator if the run finds one
  connected. A real-time scene has to show something a still cannot, and carries a still fallback,
  a capped pixel ratio, off-screen pausing and context-loss handling.

### 7. Iterate on an effect cheaply

Show an effect as a still, a short recording or a local page before building it in. Keep the
plain version working throughout, so reverting is one edit. After two iterations on one effect,
offer the plain version beside the next attempt and record it in `plan.effects`. A chooser
between options is a review tool: keep it in one block marked `data-review-tool`, serve it
locally, and remove it before any deploy (`site_audit.py --deploy` fails while it remains).

### 8. Verify

Run these, read each exit code, and fix what fails before showing the site:

```bash
python3 scripts/plan_check.py .create-website/site-plan.json
python3 scripts/site_audit.py site/ [--private .create-website/private.txt]
python3 -m http.server 8960 --bind 127.0.0.1 --directory site &
node scripts/scroll_capture.mjs http://127.0.0.1:8960/ .create-website/captures --widths 1440,390
```

`scroll_capture.mjs` runs four passes (default, reduced motion, no WebGL, touch) on agent-browser,
or Playwright when asked, and fails on horizontal overflow, uncaught exceptions, reveals that
never fired and video playing under reduced motion. Then open the captures and ask of each one
"what is wrong with this?"; writing a PNG proves nothing until it is read. Run
`design-review:design-review` on the served page for the contrast, target-size and semantics
gates. For a video hero, play it at speed on the local page, since a contact sheet shows poses
and the person sees motion.

### 9. Ship, on the person's say-so

Deploy, attach a domain or buy one only when the person says so. An unlisted address with
`noindex` is public. Before an address goes anywhere, run `scripts/deploy_check.py paths` over
the origin, `media` over every video URL, `access` when the site is meant to be private, and
`domain` for the custom domain's states. `references/ship.md` has the host specifics, the domain
purchase checklist and the five domain states.

## The report

Lead with what was built and where it is served. Then, in this order: the trawl pick, the
section count with one gold each, the hero media and its total spend, the four capture passes'
result line, the design-review result, and a "not checked" line naming what no tool here can
see: Safari, a real phone, touch drag against page scroll, and video pace if nobody watched it.
Put anything waiting on the person last: a choice, a credential, a verification email.

## Operating rules

- **One trawl run, Mobbin yourself.** `trawl:trawl` launches its own agents; spawn none on top of
  it. The Mobbin searches, the build and the checks are this session's work. Delegate a section
  build to a subagent only on a site of eight or more sections, and give it the section's plan
  entry, its gold and the direction contract.
- **The plain path is the product.** A video that is refused autoplay, a scene without WebGL and a
  page under reduced motion each show the still and the full content.
- **Measure, then claim.** Report the scripts' result lines and the captures you opened by name.
  "The audit passed" and "I looked at captures X and Y" are two claims; keep them apart.
- **Never route around a refusal.** When a model refuses a prompt or an image, report it and the
  choices; trying another model is the person's call.
- **Credentials come from the secrets broker** or the owner's explicit say-so, and never enter the
  page, the plan or a brief.
