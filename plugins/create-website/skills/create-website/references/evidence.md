# Evidence: where each rule in this skill comes from

Three kinds of source, marked in the tables:

- **[session]** One engagement on 20 and 21 November 2026 that built a personal website with a
  generated video hero, recorded in `career-kit:career-kit`'s `references/evidence.md`. These are
  failures that happened once to one run and were fixed. They are not general findings.
- **[craft]** A rule already established in a sibling skill, cited by file, which this skill
  routes to rather than restates.
- **[research]** The Dossier panel run on 22 November 2026 for this skill, exported in full to
  `docs/deep-research/`. Three members answered: Gemini through agy (`dr_5c660135af58838c`),
  Codex (`dr_11cbb4fbc786b429`) and Grok (`dr_15b7ef252125d0f3`). The paid seat the person approved
  could not run, because the secrets broker could not release its key to this session; the free
  members ran instead, at a cost of $0. Citations were checked with `research_verify_citations`:
  84 of 89, 64 of 65 and 62 of 63 resolved. Every claim below that leaned on a citation that did
  not resolve was re-sourced from one that did, or dropped.

## Plan and references

| Rule | Source |
|---|---|
| Write the plan before layout; record references per section | [session] The source session used three references and named them in its notes, and that record kept later sessions consistent. [craft] design-craft `mobbin-trawl.md`: instruction-only reference steps have a measured history of being skipped, and the user's "did you use mobbin?" arrives with "boring and uninspiring" |
| One trawl run per commission, with an explicit textbook baseline | [craft] design-craft `aesthetic-ideation.md`: consecutive sites converge on cream editorial or dark-plus-acid when subject-mining and Mobbin are the only inputs; diversity comes from isolated parallel frames, not from asking one model to be distinctive |
| One gold per section type; adjacent sections differ | [craft] design-craft `mobbin-trawl.md` M2, and `ai-slop-check.md` §11 (the same layout family twice) |
| Never invent a fact; a gap goes back as a marked placeholder | [session] career-kit evidence, rows 1 and "missing information is a red placeholder" |
| When a fact changes, read the page for every restatement | [session] A corrected fact was still wrong on the website days later, restated in a form a search did not find |

## Scroll motion

| Rule | Source |
|---|---|
| CSS scroll-driven animation on transform and opacity runs off the main thread | [research] Chrome, "New in web UI, I/O 2024" (developer.chrome.com/blog/new-in-web-ui-io-2024); Codex and Gemini members |
| Support: Chromium 115, Safari 26 (threaded in 26.4, fixes in 26.5), Firefox 159 on 27 October 2026 | [research] webkit.org/blog/17862 and /17938; MDN Firefox 159 release notes. Codex member |
| Feature detection does not replace behavioural checks | [research] Safari 26.5 fixed pause, progress-boundary and history-restoration bugs in shipped support. Codex member |
| Firefox needs an explicit animation-duration on a timeline animation | [research] Grok member. Held loosely: one member, and it may be fixed in later releases |
| GSAP only to pin, scrub a canvas or coordinate; inside gsap.matchMedia() | [craft] design-craft `gsap-motion.md`. [research] gsap.com matchMedia docs; Gemini member's split between DOM effects and canvas scrubbing |
| No normalizeScroll() as boilerplate | [research] gsap.com normalizeScroll docs: it moves scrolling onto the JavaScript thread. Codex member |
| No scroll-jacking | [research] Nielsen Norman Group, "Scrolljacking 101". Gemini and Grok members |
| Layout properties cause CLS; transforms do not | [research] web.dev/articles/optimize-cls |
| INP measures clicks, taps and keys, not scrolling | [research] web.dev/articles/inp. Codex member |
| Reduced motion removes the effect; never leave opacity 0 | [research] web.dev/articles/prefers-reduced-motion; W3C technique C39. [craft] design-craft `visual-verification.md` rule 9 (a scroll-reveal system leaves bands at opacity 0 until scrolled) |
| WCAG 2.3.3 is AAA; 2.2.2 (pause past five seconds) is A; 2.3.1 (three flashes) is A | [research] W3C WAI Understanding documents for each. All three members |
| Two signature moments at most | [craft] design-craft `motion-design.md` Phase 1 (decoration-first motion is a slop tell) |

## Video

| Rule | Source |
|---|---|
| Settle replace-or-build, placement and edges, the resting frame and the beats before generating | [session] A character hero took 11 billed clips for a cut that used three |
| Read the video tool's parameters first | [session] A prompt-and-first-frame tool gave four clips that restarted at every join and came back at 720p |
| Generate the end state and reverse | [session] A hero of beads settling into rows |
| Reverse only isotropic motion | [research] Grok and Gemini members. [research] FFmpeg `reverse` buffers the whole clip (ffmpeg.org/ffmpeg-filters.html) |
| Join on a held pose; measure skips | [session] A frame difference of 1.41 against 0.4 to 0.5 either side at a join |
| xfade needs matching frame rate, size, pixel format and timebase | [research] ffmpeg.org/ffmpeg-filters.html#xfade. Codex member |
| First equals last for discrete loops; crossfade for continuous textures | [research] Gemini member's synthesis rule. Held loosely: a reasoned position, not a measurement |
| One continuous clip beats two joined; the full model held the design | [session] Four actions in one eight-second clip; the lite model redrew the face |
| Model ids turn over | [research] Google recorded the shutdown of Veo 3.1 preview ids on 22 October 2026 (aistudio.google.com/docs/video). Codex member |
| A contact sheet is not a viewing | [session] The person found pace, skips and a missing pause by watching. [research] Google's video understanding samples at one frame a second by default (aistudio.google.com/docs/video-understanding); VBench (CVPR 2024) measures temporal flicker separately from per-frame quality |
| Muted, playsinline, poster; autoplay is an attempt | [research] developer.chrome.com/blog/autoplay; Apple, "Delivering video content for Safari"; Mozilla, "Block autoplay" (users can block muted video). All three members |
| The poster is the likely LCP; preload it, never lazy-load the hero | [research] web.dev/articles/lcp (a video counts at the earlier of poster or first frame); web.dev/articles/lazy-loading-video |
| Reserve the box; width and height only if they match | [session] Attributes that fought the CSS ratio cropped the phone view. [research] web.dev/articles/cls |
| Phone source first; H.264 last; this is not adaptive streaming | [research] MDN `<source>` reference (media inside video); Codex member |
| AV1 on Safari needs a hardware decoder | [research] webkit.org/blog/14445 (Safari 17); caniuse AV1. Gemini member |
| CRF 23 is x264's default and a quality setting, not a size | [research] x264 source (common/base.c, x264.c). Codex member |
| Range requests: expect 206 | [session] Safari refused video from `python3 -m http.server`. [research] Apple's archived Safari web content guide (historical); MDN range requests |
| Don't assign sources under reduced motion; preload is advisory | [research] web.dev/learn/performance/video-performance. Codex member |
| Grade the backdrop to the page colour | [session] 88% of pixels matched the page after grading |

## WebGL

| Rule | Source |
|---|---|
| Climb the depth ladder only as far as needed | [craft] design-craft `depth-and-3d.md` Phase 1 |
| WebGLRenderer needs WebGL 2 since r163; check availability first | [research] threejs.org WebGLRenderer docs; three.js WebGL compatibility check. Codex and Gemini members |
| Cap the pixel ratio at 2 | [session] career-kit website rule. [research] threejs.org responsive manual (DPR 3 draws 9× the pixels of DPR 1) |
| Render on demand; pause off-screen and hidden | [research] threejs.org rendering-on-demand manual |
| Context loss is expected; dispose on unmount | [research] MDN WebGL best practices; three.js "How to dispose of objects" |
| Canvas alternatives in HTML; aria-label does not expose drawn controls | [research] WHATWG HTML canvas section; WAI dragging movements (2.5.7). The Gemini member's MDN hit-regions citation did not resolve and is not relied on |
| Meshopt versus Draco: compare on the asset | [research] Khronos extension specifications. See conflict 3 |
| KTX2: ETC1S for colour, UASTC for normals | [research] Khronos KHR_texture_basisu specification. All three members |
| Texture memory: 2048² RGBA is about 16.8 MB before mipmaps | Arithmetic (2048 × 2048 × 4 bytes) |

## Deploy

| Rule | Source |
|---|---|
| Deploy only on say-so; unlisted is public | [session] A private practice page returned 200 with three restricted figures |
| noindex is not access control | [research] Google Search Central, block-indexing and control-what-you-share |
| Certificate Transparency exposes subdomains | [research] RFC 9162; Let's Encrypt CT documentation. Gemini member |
| Vercel Standard Protection leaves production domains open | [research] vercel.com/docs/deployment-protection. Codex member |
| Netlify's latest branch deploy is not marked noindex | [research] Netlify deploy overview. Gemini member. Held loosely: one member |
| Check every path before the address is shared | [session] An unlinked path on the same domain carried restricted figures |
| Domain purchase checklist | [session] Buying took four turns: short balance, no registrant, an unexpected contact email |
| Report domain states separately; live only at HTTPS 200 | [session] "Set" and "working" were minutes apart; the old parking record was served after the change. [research] Vercel and Netlify domain docs: ownership verification does not prove DNS, and certificate issuance follows DNS verification |
| Stale AAAA, CAA and proxy interception stall certificates | [research] Vercel domain troubleshooting; Let's Encrypt challenge types. Gemini member |
| Credentials only from the secrets broker | [session] career-kit rule; the user's standing instruction |

## Conflicts the research left open

1. **Retiming a clip.** Grok and Gemini called a retime within 10 to 15% safe. The source session
   measured the opposite on its own footage: a 1.35× speed-up showed as skips the person named.
   This skill keeps "fit the length in the script" until a run shows a small retime survives a
   viewing.
2. **Universal budgets.** Gemini gave hard numbers (desktop 1.5 to 2.5 MB at CRF 22 to 25, mobile
   0.8 to 1.2 MB; glTF 1.5 to 2.5 MB; 50 draw calls; 100,000 to 150,000 triangles; 64 to 96 MB of
   VRAM). Codex found no source establishing any universal ceiling and labelled its own 1 MB and
   3 MB as experimental. The scripts warn at those numbers and the skill says to measure.
3. **Draco or Meshopt.** Gemini defaults to Meshopt (smaller decoder, faster decode, compresses
   animation); Draco can be smaller on dense static meshes. Codex: compare on the actual asset.
   The skill says compare, counting decoder cost.
4. **Scroll-driven animation is Baseline, or still needs feature checks.** Gemini called it
   Baseline 2026; Codex pointed to the Safari 26.5 bug fixes in shipped support. The skill uses
   `@supports` and a visible-by-default fallback, which costs nothing either way.

## Not established

No member measured a real site on real phones. The per-feature cost to LCP, INP and CLS, dropped
frames, thermals and battery remain unmeasured, as do the latency of the video models. No paid
generation endpoint was exercised during the research.
