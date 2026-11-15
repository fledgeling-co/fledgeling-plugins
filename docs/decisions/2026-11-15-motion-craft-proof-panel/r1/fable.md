🫥 All three files read. Answer follows.

VERDICT: B
CONFIDENCE: medium

### Ranking
- **B** — the only option that runs the comparison the pipeline calls "the honest one" with more than a single pair, so a win or loss cannot be dismissed as one brief's noise.
- **C** — same honesty, but one pair cannot distinguish "the skill helps" from "this brief suited it", and cannot expose an assertion the baseline also passes.
- **A** — the ship-without-evals clause exists for sessions that cannot run the evals, not for ones that would rather not; here the runners, the budget and the delegated mandate are all present.

### Why
Phase 3 names the no-skill comparison as the test of whether the skill "earns its place in the context window" (SKILL.md:111-115), and permits skipping it only when subagents are off, budget is absent, or the user asked for a skill and not a benchmark (SKILL.md:129-132); the evidence pack shows none of those, since the owner delegated the proof level rather than declining it, and the skill ships to other people through the marketplace (evidence.md "What the owner asked for"). The reference already asks for 6-8 prompts each run twice (evals-and-judging.md:19-24) and warns that single runs carry sampling noise (evals-and-judging.md:86), so B's two briefs is itself a cut and C's one brief is a cut below the point where "honest enough to lose" (SKILL.md:248-250) can be checked, because a 1-0 result reports nothing about variance and a tied brief is just a deadlock (evals-and-judging.md:56-57). The "assertion that cannot fail" check (evals-and-judging.md:32-36) needs the baseline to run on more than one prompt to tell a vacuous assertion from a lucky one. The panel is warranted because motion quality is a matter of judgment rather than an artifact check (evals-and-judging.md:40-43), and the contact-sheet limit (evidence.md "Proof requirements"; batch1.txt line 63) means judges score composition and scene variety but not timing or easing, which is exactly the caveat the reference tells EVALS.md to carry (evals-and-judging.md:86-87). From my own knowledge, medium confidence: the marginal hour between C and B is small against a pipeline whose research phase alone runs 5-60 minutes (SKILL.md:76), and the 10-30 minute render figure comes from Claude Motion's cloud and long local films (evidence.md "Engines" and "Proof requirements"), so briefs kept to 20-30 seconds should render well under that.

### What would change my mind
If a dry run showed a no-skill baseline cannot produce any MP4 at all, the structural layer alone would settle the question and the panel would be measuring nothing (evals-and-judging.md:40-43), which would move me to C with the panel dropped. If the four renders actually cost two hours each rather than two hours total, I would move to C.

### Risk if this is wrong
If B is more than the skill needed, the owner loses about an hour of machine time and judge spend, and the EVALS.md is longer than it had to be. If I am wrong the other way and A or C was right, nothing is lost, because B strictly contains both.

### Better option (only if one exists)
B's design with the two briefs deliberately short, about 20 seconds at 720p and 30 fps, so four renders fit nearer one hour, and each judge receives the contact sheet plus a three-frame strip per scene so motion direction is at least legible from stills. The files are silent on whether a short film still exercises what the skill owns, such as scene sequencing, so I rank this below plain B rather than choosing it.
