# Evidence pack for the motion-craft decisions (compiled 2026-11-15)

## What the owner asked for (conversation, verbatim)
"I'd like a new motion skill ... Many talk about claude motion, I'm interested in achieving what claude motion does but with existing libraries as I don't have access to claude motion."
The skill joins the fledgeling-plugins marketplace (/Volumes/LLMs/Dev/fledgeling-plugins), whose plugins are installed by other people via a marketplace.

## What Claude Motion is (from 18 YouTube transcripts, /private/tmp/claude-501/-Users-lukerhodes-Dev-dAIolog/71aa0a44-4a67-4066-96bc-90723a122818/scratchpad/transcripts/batch1.txt and batch2.txt)
- Writes the animation as code (HTML), no video model; edit by comments on the frame, a "tweaks" panel listing every word/scene length/speed, chat for larger changes; exports MP4/GIF at chosen resolution/fps. Team/Enterprise only; renders in Anthropic's cloud.
- Alternatives the videos name: HyperFrames (HeyGen, has a browser studio), Remotion (React; "free until your company hits four people" — transcript mJ6ZvGiwZEc in batch2.txt), or "plain HTML and FFmpeg" skills (transcript rscb1DgJtNg: "every frame is a function of time; a headless browser jumps to each moment and screenshots; FFmpeg stitches").

## Engines and licences (checked 2026-11-15 with npm view / vendor pages)
- gsap 3.15.1 — "Standard 'no charge' license". Free for commercial use including formerly paid plugins. Prohibited: "any implementation and/or use of GSAP Products in tools that allow users to build visual animations without code" that compete with Webflow's visual animation building; Competitive Products "enable users to create, edit, or manage animations through a visual interface or builder similar to Webflow". Redistribution inside another open-source package is not addressed (gsap.com/standard-license).
- hyperframes 0.9.52 — Apache-2.0. Its skill starts with a usage beacon: "run `npx hyperframes events --skill=hyperframes` once as this skill starts. It sends the skill's name with the CLI's usual telemetry (account-linked when signed in) and honours the opt-out." (/private/tmp/claude-501/-Users-lukerhodes-Dev-dAIolog/71aa0a44-4a67-4066-96bc-90723a122818/scratchpad/motion-repos/hyperframes/skills/hyperframes/SKILL.md:8). Provides check/snapshot/keyframes CLI, Studio preview, registry blocks, and steers media to HeyGen ("/media-use, which says when HeyGen is needed").
- remotion 4.0.543 — custom licence (company licence required at 4+ employees per its LICENSE.md and the transcript above). React-based.
- claude-motion (MIT, /private/tmp/claude-501/-Users-lukerhodes-Dev-dAIolog/71aa0a44-4a67-4066-96bc-90723a122818/scratchpad/motion-repos/claude-motion) uses Remotion for motion graphics and a separate plain-HTML "sims" pipeline: one HTML page with render(t) pure in t, Playwright steps frame-by-frame into ffmpeg at 60 fps.
- huashu-motion (MIT, /private/tmp/claude-501/-Users-lukerhodes-Dev-dAIolog/71aa0a44-4a67-4066-96bc-90723a122818/scratchpad/motion-repos/huashu-motion) uses one HTML + GSAP composition per film rendered frame by frame in the user's Chrome, with its own studio for comments and edits.

## What this marketplace already has
- design-craft's make-an-animation.md already ships a hand-rolled timeline engine whose every visual is a pure function of t, a scrubber, and a `window.__animStage.setTime()` export bridge; it names a paused GSAP master timeline as an alternative (/Volumes/LLMs/Dev/fledgeling-plugins/plugins/design-craft/skills/design-craft/references/make-an-animation.md:27-79).
- The owner's machine policy: Playwright is a sanctioned browser fallback (~/.claude/CLAUDE.md "Browsers" section); ffmpeg is installed.

## Proof requirements (decision 2)
- create-skill Phase 3 (/Volumes/LLMs/Dev/fledgeling-plugins/plugins/create-skill/skills/create-skill/SKILL.md:111-140): baseline = same prompts with no skill; structural assertions graded independently; blind panel of heterogeneous judges; "If the evals cannot be run, the skill ships saying so" with EVALS.md stating no run happened and naming the tasks that would settle it.
- A rendered motion film takes roughly 10-30 minutes per render per the transcripts (Claude Motion 10-30 min; local rigs ~4-30 min). Two briefs x with/without = 4 renders plus judging, about 2 hours.
