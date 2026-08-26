🫥
1. CONCEPTUAL CLARITY — **B**: its core claim that "a program's address does not name a location in memory. It names a row in a table" plus "the low 12 bits pass through the table untouched" lets you predict unseen cases like relocation and fork/copy-on-write, where A's "pretend house" story never gives you a rule to extrapolate from.

2. HONESTY ABOUT LIMITS — **B**: it has dedicated sections "Where this analogy stops being true" and "Still simplified here" ("A miss becomes a two-dimensional walk of up to 24 memory accesses"), while A's only hedge is calling the mechanism "a very useful lie" and it never flags its own simplifications (e.g. presenting a flat page table as the whole story).

3. ENGAGEMENT DEPTH — **B**: its predict-first quizzes ("Commit to an answer to unlock the run") force the reader to stake a guess before seeing the answer, and its wrong-answer debriefs teach ("that is exactly what a machine without a page table does"), whereas A is watch-only from start to recap — though B's engagement is undercut by the artifact ending with no `<script>`, leaving the unlock buttons permanently disabled.

4. VISUAL CRAFT — **A**: its SVGs are complete and information-bearing (the page-table diagram genuinely maps "page 0 → slot 3 … page 2 → on disk" with crossing arrows showing "Neat order in, jumbled order out"), while every one of B's diagrams is an empty `<svg>` element awaiting JavaScript that is absent from the artifact, so they render as blank space and Tiers 2–3 stay `hidden` and unreachable.

5. REGISTER — **B**: it addresses the reader as capable ("the scaffolding below is built for people who do not, and it slows down people who do") and does real arithmetic with them ("512 GiB of table, per process"), where A's "That's MY spot!", chocolate-bar emoji and "pretend street" framing talk noticeably down.

OVERALL: B
