# Getting started with Claude Code Projects (omihvjf0A2k)

A 273 s tutorial from Claude. An on-camera presenter alternates with real product screen recordings, plus a few redrawn diagrams and text cards.

## Hook and structure

Frame 0 is the presenter, not the product. An ffmpeg luma check reads 47 at t=0 and 249 at t=0.7, and `strips/window-01-0s.jpg` shows her still for 0.25 s. The sampled `f0001.jpg` and sheet-01 show the empty prompt box at 0.0, which disagrees with the video itself. The cut at 0.62 s lands on the prompt box, where the goal types out (`f0006.jpg`: "Our Core Web Vitals for the marketing site have been dropping for a month: p75 LCP is 4.1s on mobile and CLS is 0.28, and users keep telling us navigation is slow. Investigate and fix."). By 13 s eight named threads sit under it (`f0011.jpg`). The voice opens with "Watch this. I'm going to brain dump a large goal for Claude", so the product is doing the job inside 3 s.

The shape is: demo hook (0.6-20 s), presenter definition (20-25 s), a You, Coordinator, threads diagram (25-45 s), a "When to reach for a project" card (47.6-53.5 s), then chapters with lower-third titles: Setting up a new project, Working with threads, Reviewing pull requests, Connecting to external services, Routines, Managing cost, Tell Claude how you want to work, Use project memory. The recap card "Start a project" runs 258.5-264.75 s and a 7.8 s presenter sign-off ends the film. The hero is the thread fan-out at about 18 s (share 0.066), where the "Projects Beta" lockup appears over it (`strips/window-14-18.084s.jpg`).

## Rhythm

`metrics.json` gives 42 hard cuts, 9.24 per minute, median shot 3.83 s and mean 6.34 s. Eight shots run past 10 s; the longest is 24.75 s (83.21-107.96 s, the New project dialog through to the first prompt). There are no bursts (`bursts: []`). Two cut clusters exist, 177-188 s (six cuts) and 246.5-258.5 s (six cuts), but each spans 10-12 s, not 5. Cuts follow sentences: `cuts_on_strong_onset_share` is 0.048 against a `chance_share` of 0.053, so they are not locked to the sound. Screen stretches can go static for long; `longest_static_run_s` is 18, ending at 234 s, on the Settings dialog (sheet-06).

## Look and type

The ground is warm off-white for UI and cards and a dark wood room for the presenter (dark share 0.287, light share 0.691). The palette is near-black, one terracotta coral for the Coordinator box (`f0013.jpg`), muted green for success states and the After bars, and grey for Before. Type is a serif for titles and lower thirds, a clean sans for card bullets, and monospace for the URL pill (`crops/w-urlpill.png`).

`measure ink` gives title heights against the 720 px frame: "Delba de Oliveira" 41 px (5.7 %, t=7 s), "When to reach for a project" 38 px (5.3 %, t=48.5 s), "Connecting to" 53 px (7.4 %) and "external services" 42 px (5.8 %) at t=178.5 s, and "Start a project" 37 px (5.1 %, t=258.5 s). The range is 5.1-7.4 %, inside the 4-9 % band, and the longest title line is 5 words. Titles are lower-left in white over a dark gradient (`crops/w-lowerthird.png`, `crops/w-connecting.png`). Density is sparse; the cards leave most of the frame empty (`f0025.jpg`).

## Product interface

About 59 % of runtime is screen content or diagram (light share 0.691 minus roughly 26 s of cards and diagrams). The UI is a real capture with a real cursor, whose pointer shows a halo under it (`f0034.jpg`). The windowed app sits on a beige ground (`f0036.jpg`); the film then punches into the working area (`f0049.jpg`, `f0073.jpg`). At full-window framing the UI text is about 12 px of 720 (`crops/w-threadspanel.png` is readable only at 2x), so phone-width legibility is partial. The punched-in frames are legible: `f0073.jpg` shows "Optimize images", "Approved · Checks passed" and a black "Merge it" button. The redrawn diagram (`f0021.jpg`) simplifies the app to You, Coordinator and eight rows with branch names such as "claude/optimize-images".

The payoff is a post-mortem artifact with three bar charts (`f0088.jpg`): LCP mobile 4.1 s to 2.2 s, LCP desktop 2.9 s to 1.4 s, CLS 0.28 to 0.06.

## Motion and transitions

Between presenter and screen the film uses a one-frame cross-dissolve, seen at 5.46, 9.375, 25.167, 34.458 and 69.917 s (`strips/window-06-5.375s.jpg`, `window-09-9.292s.jpg`, `window-19-25.084s.jpg`, `window-23-34.375s.jpg`, `window-46-69.834s.jpg`). That is a mixed frame of roughly 0.04 s, so it reads as a soft cut, but it is a dissolve between worlds. Other seams are hard cuts on the voice. Lower thirds fade up over about 0.4 s (`strips/window-36-58.5s.jpg`), with "Setting up a new project" reaching full opacity at about 59 s. Typed prompts type out live (`f0049.jpg`, `f0094.jpg`, `f0109.jpg`). The thread list zooms out into the windowed app with the Projects Beta lockup entering (`strips/window-14-18.084s.jpg`), and the dialog closes into the project window after the Create click (`strips/window-56-82.875s.jpg`).

## Copy on screen

Cards use short fragments: "When to reach for a project" with "A goal bigger than one session", "Work that spans several repos" and "Many tasks that can run in parallel" arriving one line every 2 s (sheet-02, 48-52 s). The recap card shows "Give Claude the goal", "Let it split the work into threads" and "Check in when it needs you" (sheet-09, 258-262 s). A "Research preview" tag sits next to "Routines" (`f0092.jpg`). The CTA is a monospace pill, "code.claude.com/docs/en/claude-projects" (`crops/w-urlpill.png`, `f0136.jpg` at t=270 s). The "Projects" and "Beta" lockup appears twice, at 18 s and 264 s. The spoken script carries the detail, including usage tips; the screen carries only titles and cards. Hold times for cards could not be resolved at 2 s sampling.

## Sound

The film is voice only. `audio.json` tags: speech 0.908, writing 0.163, music 0.101, click 0.076, all but speech below 0.2, so there is no evidence of music or effects. `beats.count` is 0 with confidence 0.003. The master is -23.7 LUFS integrated, short-term max -21.3, true peak -3.7 dBTP and LRA 3.0 LU, which is about 9.7 LU under the -14 LUFS target. Silence spans are 0.3-1.3 s between sentences. The cuts are not locked to the sound (0.048 against 0.053). The transcript came from local whisper and gives 863 words, about 190 words per minute.

## What to steal

1. Open on the product doing the task: the goal types out at 0.62 s and eight threads are on screen by 13 s.
2. Use one redrawn diagram with three node types and one accent to explain the system (25-45 s).
3. Carry one worked example through every chapter, ending on a before/after chart with numbers (`f0088.jpg`).
4. Titles at 5-7 % of frame height, lower-left, 3-6 words, fade up in about 0.4 s.
5. Reveal bullet lines one every 2 s and hold the last one for more than 0.5 s plus 0.3 s a word.
6. Cut any screen shot that holds with no change for longer than about 8 s; this film has an 18 s run.
7. Master the voice at -14 LUFS for social; this one sits 9.7 LU under.
