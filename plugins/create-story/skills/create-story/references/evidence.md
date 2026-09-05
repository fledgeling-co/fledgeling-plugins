# Evidence

Every rule in this skill traces to one of the entries below. Each entry names the source, what it found, and the rule, script check, or discarded option it produced. A finding that changed nothing is not listed.

The corpus is the three Dossier panel reports exported into `docs/deep-research/` (Grok 4.3, Gemini Deep Research, Perplexity Sonar Deep Research; panel `dr_2295e3e855ba4ba6`, 5 September 2026, $6.44 settled) plus the 21-claim graph distilled from them in `docs/deep-research/claims.json`, and the four Anthropic prompting documents read in full on the day the skill was written. Claims from the panel are cited as `c1`..`c21`; report-specific findings cite the report.

## E1. Flat context loses local continuity

**Source.** c1, c2, c19; Gemini report, "The Pathology of Local Narrative Drift"; Perplexity report, "Transformer Attention Dynamics And The Illusion Of Continuous Thought". Storywriter.pro (29 Aug 2026) on 120k-word manuscripts as flat files; Gemini 3 Pro needle retrieval at 77% across 128k tokens cited as retrieval, not reasoning.

**Finding.** Loading the whole manuscript makes early plot and character detail exert pull on local sentence generation. The model satisfies the outline and drops the conditional link to the paragraph before. Retrieval accuracy is not working memory.

**Consequence.** The drafter never sees the manuscript. `scripts/context_pack.py` is the only way a drafting brief is assembled, and it includes the bible sections that apply, the entry state, the beat card, and the last two paragraphs of the previous scene. The drafter runs as a fresh subagent whose only input is that pack, because the orchestrating session's context already holds the whole story and would defeat the window.

## E2. The window is the last one or two paragraphs plus structured state

**Source.** c18 (inference), c7; Gemini report, "Recursive Sliding-Window Contexts and Chain of States", step 3: "prompted only with the immediate previous 500 words, the current extracted CoS, and the target CoS"; Perplexity report, "Recursive Sliding-Window Contexts Within Long-Context Models" (last 1,000 to 2,000 tokens plus a concise summary).

**Finding.** The reports disagree on width: two paragraphs, 500 words, or 1,000 to 2,000 tokens. They agree on shape: a short verbatim tail plus a structured state, not a summary of the whole.

**Consequence.** Default tail is two paragraphs (`--tail 2`), adjustable per run. The disagreement on width is held loosely and recorded here rather than resolved.

## E3. The paragraph-as-micro-idea prior

**Source.** Perplexity report, "Decoding Strategies, Sampling, And Micro-Level Non Sequiturs": "a model trained on internet and book data learns that paragraphs often encapsulate a self-contained micro-idea ... the model may treat each new paragraph as an opportunity to introduce a fresh micro-idea that is stylistically related but not tightly causally connected to the previous one". c3.

**Finding.** Each paragraph makes sense alone and fits the theme, and the seam between them is where the reader feels the thread go.

**Consequence.** The drafting task in the pack states the counter-rule in one sentence ("each paragraph after the first takes something from the paragraph before it"), and `scripts/transition_audit.py` checks it: a paragraph whose first sentence carries no personal pronoun, no leading connective, no cast name from the previous paragraph, no shared content word, and is not a spoken line, and which shares no content word with the previous paragraph anywhere, is an orphan and fails the gate unless a `* * *` break precedes it.

## E4. Structured state beats prose summaries

**Source.** c15, c7; Perplexity report, "Scene-Level State Tracking With Structured Representations" (schema: characters_present with emotional_state, goals, secrets; items with status and location; open_threads; time_location); Anthropic best practices, "State management best practices": "Use structured formats for state data ... use JSON or other structured formats to help Claude understand schema requirements"; SCORE (alphaxiv 2503.23512) key-item tracking.

**Finding.** Items disappear, motivations flip and minor characters get renamed when the only carrier of state is prose. A schema names what must survive.

**Consequence.** The Chain of States schema in `references/state-schema.md`: scene, time, location, characters (position, holding, wants, feels, knows), items (where, status), open_threads, promises, last_paragraph. `scripts/story_state.py validate` enforces the shape; `diff` reports what moved between two scenes.

## E5. The exit state is checked against the beat, not trusted

**Source.** Perplexity report, "Training Distribution, Story Priors, And Positivity Bias": signed-network analysis of 1,200 stories (arXiv 2510.18932) found a consistent bias toward tightly-knit positive relationships and premature reconciliation; c13.

**Finding.** Models resolve conflict early. A beat that asks for tension to stay high gets a paragraph in which everyone makes up.

**Consequence.** Every beat card carries `exit.unresolved` and `exit.tension`. `scripts/story_state.py check-exit` fails when a thread the beat kept open is missing from the exit state's `open_threads`, and when the last paragraph shares no word with the beat's `last_image`. The drafting task repeats the rule ("resolve nothing the beat keeps open").

## E6. One scene per pass, bounded in words

**Source.** c8; Grok report, "Prose beat-sheet chunking": one scene of 200 to 1,600 words per generation pass, beat sheet first (location, participants, single change, emotional function); claims.json narrows to 200 to 800.

**Finding.** Longer passes rush beats; the reports disagree on the ceiling (800 or 1,600).

**Consequence.** Beat cards carry a `words` band; `validate-beats` refuses a `max` above 1,600 and the example uses 400 to 1,000. The upper figure is the loose end of the two reports and is recorded as such.

## E7. Reasoning inside the draft stiffens the prose

**Source.** c6; Gemini report, "The 'Overthinking' Degradation Paradox" (AdapThink, HuggingFace, May 2025: extended reasoning makes agents "introverted", shorter, stilted); Perplexity report, "Chain-of-Thought Steering For Narrative Planning vs Prose Realization"; ICCC25 Morain et al.: complex prompting methods including CoT do not outperform basic prompts on creative artefacts.

**Finding.** The reasoning that holds the macro plot is the mechanism that flattens micro-prose when it runs inside the drafting call. The fix is structural: plan with reasoning, draft without it.

**Consequence.** The drafting task contains no instruction to reason, plan, or explain. Planning (bible, beat sheet) happens in the orchestrating session with thinking on. The drafter subagent gets the pack and a request for prose plus an exit state, nothing else.

## E8. Critique in a separate context

**Source.** c9, c17; Grok report, "Multi-pass editing pipelines": separate Promises Auditor, Voice Drift Detector, Continuity Deposition, Tension/Lull Mapper passes outperform joint generate-and-edit; Gemini report: "treating the model as both the raw creator and ruthless editor in one continuous generation pass leads to prompt-compliance collision" (arXiv 2604.01029); Anthropic best practices, "Chain complex prompts": self-correction as separate calls.

**Finding.** Ten to thirty structural issues per chapter are caught by separated passes that a single pass misses.

**Consequence.** One critic subagent per scene, fresh context, given the scene, the pack and the exit state. Its report format is fixed in `references/passes.md`. The drafter never critiques its own scene in the same context.

## E9. Goal and reason framing; no verification scaffolding; explicit length

**Source.** c11, c16; Anthropic, "Prompting Claude Opus 5": "Claude Opus 5 verifies its own work without being told to ... remove them"; "Written deliverable length ... add explicit length calibration"; "Add context to improve performance ... Claude is smart enough to generalize from the explanation"; Grok report, "Core prompt structures" (goal + audience + why over step lists).

**Consequence.** The drafting task and the critic brief state the goal and the reason for each rule, carry word bands, and contain no "double-check" or "verify" instruction. The SKILL.md caps subagents at two per scene and says which two.

## E10. Mannered prose and the stock tells

**Source.** Anthropic, "Prompting Claude Fable 5.1", "Writing density": the mannered-prose definition ("substitutes metaphor and flourish for direct statement"); Gemini report: kylehughes five rules (cut significance inflation, plain verbs, stop at the fact, vary cadence, earn every adjective) and the "delve / tapestry / testament" list (ACL INLG 2025); agent-voice's bundled AI-writing field guide.

**Consequence.** The drafting task carries the literal-phrase rule in one sentence. `transition_audit.py` fails on five hard tells and warns on a longer soft list, warns when sentence-length variation is low (coefficient of variation under 0.35 across eight or more sentences), and warns when three paragraphs in a row open with the same word.

## E11. Voice locking with rules plus a sample

**Source.** Grok report, "Voice locking: 2 to 5 explicit rules or 300-word samples pasted every session"; Fable 5.1 "holds codified voice with high fidelity".

**Consequence.** The bible's `## Voice` section is five checkable rules plus a sample under 300 words, and it goes into every pack. When the author is a named person, that person's voice skill supplies the rules instead (SKILL.md, "Whose voice").

## E12. The outline is approved before prose

**Source.** Perplexity report, "Human Oversight And Creative Judgment": models overestimate the creativity of their output (ICCC25); human checkpoints on beat sheets and arcs. The game project's own restart brief (5 Sep 2026) asked for an outline for review before any derivative output.

**Consequence.** The skill stops after writing the bible and beat sheet when neither existed, and drafts prose only once the user has said the beat sheet stands.

## E13. Influences are cards of observable habits, sourced, never remembered plots

**Source.** A free Dossier local research loop (handle `dr_7dcc00535d2c820e`, 5 September 2026, four workers and a fact-checker, 37 registered sources across 30 domains), which found author method statements (Howey on scenes as chapters; Stine on writing a chapter backwards from its fixed ending; Sawyer's one-viewpoint-per-scene rule; Gibson on condensing and the hook on every page; Scarrow on stripping profanity after the first draft; Applegate on pace and ghostwriting) and outlet reviews naming person, tense, paragraph and sentence habits (Publishers Weekly on Peace's one-sentence paragraphs and fragments; The Comics Journal on Kirkman's subtext-free dialogue; Language Log and Ben Blatt's counts on Rowling). The fact-check pass overturned one card: the Red Riding Quartet is not one first-person narrator per book (1977 alternates two, 1983 runs three strands with one in the second person, per the publisher's own page), so Peace's card carries person: any and says which book does what. It confirmed Winter World's first-person present from the book's quoted opening and Project Hail Mary's present-tense timeline with past-tense flashbacks. Gaps recorded per author in the run: no peer-reviewed stylometry for eleven of the twelve, and no established-outlet review at all for Scarrow or Riddle. E11 (voice locking with rules plus a sample) is the rule this extends.

**Finding.** What a review or an author can state about style is observable and countable: person, tense, chapter as scene, sentence fragments, dialogue share, the chapter-ending fake-out. What they do not state is a number for sentence length; the numeric bands on most cards are therefore absent, and the two that carry one (Peace, Luke) say where the number came from.

**Consequence.** `references/influences.md` holds one card per author with person, tense, optional bands, three to five moves, borrow and leave lists, and the sources. `scripts/voice_card.py compose` merges a base card and up to three influences into the bible's `## Voice` section deterministically, base rule first then round robin; `voice_card.py check` measures a scene against the merged bands and fails outside them. A card carries no theme, plot or setting, and its leave list names the borrowed subject as the pastiche trap. A recall layer from a model trained on the books, when one is used, is marked as recall on the card and never cited as a source.

## Discarded options, with the reason

- **An MCP lore server** (c5, Gemini report). The state files on disk read by a tool call are the same shape without a server process; the drafter reads one JSON file either way. Revisit if a story outgrows one directory.
- **Prompt-cache economics** (c10). Real for API pipelines; inside Claude Code the harness owns caching, so no rule follows.
- **Cross-family drafting** (c14, c21; Gemini report's Flash-as-writer). Claude Code subagents run one family. The critic can be routed out-of-family through `clarify:clarify`'s lanes when a scene keeps failing, and the SKILL.md says when.
- **A paragraph-level coherence metric.** All three reports record its absence (Grok, "Knowledge Gaps"; Gemini, "Empirical Measurement of Stylistic Degradation"). The transition audit is a tripwire with named heuristics, not a measurement, and the SKILL.md says so.

## Held loosely

- Window width: two paragraphs versus 500 words versus 1,000 to 2,000 tokens (E2).
- Scene ceiling: 800 versus 1,600 words (E6).
- Whether pure long-context with rich planning scaffolds can match chunking (arXiv 2605.17064 versus 2603.05890, Grok report "Contrasting viewpoints"). This skill takes the chunking side because the failure it targets is the one the long-context side does not claim to fix.
