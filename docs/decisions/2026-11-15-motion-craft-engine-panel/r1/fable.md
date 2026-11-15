🫥 All seven files read. Verdict below.

VERDICT: C
CONFIDENCE: medium

### Ranking
- **C. HyperFrames** — Apache-2.0, nothing third-party bundled in the plugin, and it already ships the seek-by-frame render, Studio, check, snapshot and motion assertions the skill would otherwise have to build; the marketplace's own rule says route rather than reimplement.
- **B. Own MIT runtime** — licence-clean, but it duplicates design-craft's existing t-engine and requires a from-scratch preview studio, which the owner ruled out.
- **D. Remotion** — clear but restrictive licence (company licence at 4+ employees) for a public marketplace, React-only, and claude-motion itself routes sims away from it.
- **A. GSAP runtime** — the only option that bundles a file whose licence is silent on redistribution and restricts visual animation builders, which a shipped tweaks panel resembles.

### Why
The constraint that bites is redistribution: GSAP's licence does not address redistribution inside another package and prohibits "tools that allow users to build visual animations without code" with "a visual interface or builder" (evidence.md:12), and Option A ships exactly such a preview page with a tweaks panel, so A fails the licence gate the panel was given (evidence.md: "Engines and licences"). HyperFrames is Apache-2.0 and is invoked via `npx`, so the plugin bundles no third-party code; it already provides deterministic seek-by-frame rendering where "every render is identical" and editing in Studio (hyperframes SKILL.md:12), a 12-rule determinism contract (SKILL.md:18-33), a `check` gate, `snapshot` review and `.motion.json` assertions (motion.md:69-84), which is the Claude Motion behaviour the owner wants (evidence.md:8) delivered by an existing library. Option B would reimplement what design-craft's make-an-animation.md already ships (t-engine, scrubber, `__animStage.setTime()` bridge, make-an-animation.md:29-75) and would add a self-built studio, colliding with both the owner's "existing libraries" constraint (evidence.md:4) and create-skill's route-don't-reimplement rule. Remotion's licence requires a company licence at four or more employees (evidence.md:14; claude-motion README.md:171), a friction every marketplace installer inherits, and even claude-motion moves 3D and simulation work out of Remotion to plain HTML because it is "easier to write as a web page than as React" (README.md:25; web-sims SKILL.md:10-16). From my own knowledge, medium confidence: HyperFrames renders locally with its own Puppeteer and FFmpeg engine (hyperframes CLAUDE.md "engine/" entry), so Obscura's inability to execute GSAP timelines (make-an-animation.md:87) does not block Option C.

Two costs of C that the files record and the owner should weigh: the skill opens with an account-linked usage beacon (SKILL.md:8), it steers media to HeyGen and reports "remaining plan usage" (SKILL.md:12, 16), and two of its skills are Pro-gated (hyperframes CLAUDE.md skill list). The files are silent on whether a local `hyperframes render` is itself metered.

### What would change my mind
Evidence that local rendering through `npx hyperframes render` is plan-metered or paywalled, or that the telemetry beacon cannot be omitted by motion-craft's own instructions, would flip me to B built as a thin extraction of design-craft's existing engine rather than new code.

### Risk if this is wrong
If HeyGen relicenses, meters local renders, or changes the composition contract, motion-craft's output and review loop break for every installer at once and the owner owns none of the fix. The cost is a rewrite of the engine layer onto B, which the director layer (story, rhythm, review, sound) should be written to survive.

### Better option
A sharpened C rather than a new letter: motion-craft defaults to HyperFrames but skips its usage beacon and HeyGen media routing, and names design-craft's make-an-animation.md engine as the routed fallback when a user declines the vendor CLI. That keeps the licence gate clean, respects the route-don't-reimplement rule, and leaves the director layer engine-independent.
