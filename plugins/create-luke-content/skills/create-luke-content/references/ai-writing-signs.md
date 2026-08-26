# Signs of AI Writing — Field Guide for Voice Personas

Distilled from Wikipedia's "Signs of AI writing" field guide (WikiProject AI Cleanup, as of mid-2026), adapted from its Wikipedia-specific framing into guidance for ghostwriting personal content (LinkedIn posts, articles, marketing, messages), and augmented (July 2026) with an empirical layer distilled from 2023–2026 corpus studies, human-perception experiments, and editorial style authorities (§6). Every generated voice persona must be built so its output exhibits **none** of these tells, and its lint config should ban the mechanical ones.

**How to use this file:** read it fully when building a persona package; encode the relevant bans into the generated base-voice file and `voice-lint.json`; re-read the checklist at the end when self-checking any sample content you draft.

## Why AI text is detectable at all (the root mechanism)

LLMs regress to the statistical mean. Specific, unusual, nuanced facts are statistically rare, so models replace them with generic, positive descriptions that could apply to almost anything. The subject becomes simultaneously **less specific and more exaggerated** — like shouting louder that a portrait shows a uniquely important person while the portrait fades into a blurry sketch.

This is the master key. Nearly every tell below is a surface symptom of it. The antidote is always the same: **concrete beats generic**. A named tool, an exact number, a lived moment, a real trade-off. If a sentence could be pasted into a post about a different topic without edits, it is the mean, not the person.

Two caveats the source guide is careful about, and so should you be:

- These signs are **descriptive, not prescriptive** — observations, not laws. Humans use some of them too (and human speech is measurably drifting toward LLM patterns since 2024). One tell in isolation proves nothing; density of tells is the signal.
- **Do not treat the signs as the problem itself.** Stripping the surface tells from mean-regressed writing just makes hollow content harder to detect. The goal is writing that is genuinely specific, grounded, and in the person's voice — at which point the tells disappear as a side effect.

## 1. Content-level tells

### 1.1 Inflated significance and legacy

The single most recognisable AI habit: puffing up the subject by asserting its contribution to a broader theme.

Words/patterns to ban: *stands as / serves as a testament*, *a pivotal moment/role*, *underscores its importance*, *highlights its significance*, *reflects broader trends*, *symbolising its enduring/ongoing legacy*, *setting the stage for*, *marking a shift*, *key turning point*, *evolving landscape*, *focal point*, *indelible mark*, *deeply rooted*, *rich tapestry*.

The tell survives topic changes: an LLM will claim a routine product update "marks a pivotal moment in the evolution of investor communications". A person would say what changed and why they care.

### 1.2 Superficial analysis via participle tails

Sentences that end with an "-ing" clause asserting unearned meaning: "…, highlighting the importance of transparency", "…, ensuring alignment with stakeholders", "…, fostering a sense of community", "…, contributing to the broader conversation". The clause is synthesis the facts don't support — analysis-shaped filler. Also watch *reflecting*, *emphasising*, *showcasing*, *demonstrating the ongoing relevance of*, *cementing*.

If the analysis is real, give it its own sentence with its own evidence. If it isn't, cut it.

### 1.3 Promotional puffery

LLMs struggle to stay neutral; output drifts toward travel-brochure or press-release tone even when asked not to (sometimes *while claiming to remove promotional tone*). Ban: *boasts*, *vibrant*, *nestled*, *in the heart of*, *rich (cultural) heritage*, *breathtaking*, *stunning natural beauty*, *renowned*, *groundbreaking*, *cutting-edge*, *seamless*, *world-class*, *commitment to excellence/innovation*, *diverse array*. Newer models are subtler — the puffery hides in adjectives and "communicates a powerful emotional presence"-style analysis rather than "the best" claims. Marketing personas especially need this ban: the register sells by concrete demonstration, never adjectives.

### 1.4 Vague attribution and overgeneralised opinion

Weasel constructions that launder the model's own claims: *experts argue*, *observers have cited*, *industry reports suggest*, *some critics argue*, *is widely regarded as*, *described in scholarship as*. Also: presenting one source as many ("several publications" when one exists), and implying lists are non-exhaustive ("such as…" before an exhaustive list). A voice persona states opinions as the person's own ("I reckon…", "my read is…") or attributes them to a named, real source.

### 1.5 The challenges-and-future-prospects formula

A rigid closing arc: "Despite its [positives], X faces several challenges… Despite these challenges, X continues to [vaguely positive assessment / speculative future]." Also "Future Outlook" sections and endings that speculate about how "ongoing initiatives could" improve things. Humans end on the actual point; personas should end the way the person ends (often a genuine question or a plain landing).

### 1.6 Canned notability / coverage emphasis

Hitting the reader over the head with claims of coverage and credibility: "featured in *Vogue*, *Wired*, and other prominent outlets", "maintains an active social media presence", "profiled in multiple high-quality, independent outlets". In personal-brand writing this surfaces as credential-stacking bios and posts that cite their own press instead of saying something. If coverage matters, one specific fact from it beats a list of mastheads.

### 1.7 Compressed abstraction where information was needed

A tell the source guide doesn't name but voice owners reliably flag: the **epigram used in place of a plain statement**. Gnomic headings that need the body to decode them (a two-noun riddle, a bare count like "Why these thirty" where the point belonged), aphoristic paragraph closers that neatly resolve a messy topic, and slogan-shaped lines that don't survive a literal reading. Each is fine once; a document where every unit lands one is exhausting and distinctly machine-like — LLM reward models favour "quotable" resolutions, humans mostly just end. Two rules:

- **Names and headings carry the message, not the wit.** A heading's job is to let a reader skim; a riddle-heading fails at its actual job. Every name for an artifact or section must survive a literal reading (a guide of questions is a question bank, not an "answer bank").
- **Epigram budget:** roughly one landing line per page or major section, and any given epigram appears **once per document** — captions, panel text, pull quotes and image copy count as part of the document, so a line in the body may not recur as the caption on the same spread. The same contrast construction ("an X, not a Y") also may not become a document's verbal tic across units. Most paragraphs end on information, plainly. [Source: owner review of a shipped 20-page guide, 2026-07, and its follow-up validation; corroborated by §6's "forced aphorisms / quotable closers" research marker.]

## 2. Language-level tells

### 2.1 AI vocabulary

Empirically overused words (multiple corpus studies, 2023–2026). Density is the signal: one may be coincidence; several co-occurring is one of the strongest tells. Core list to ban or heavily restrict:

> *delve*, *tapestry* (abstract), *testament*, *underscore(s)* (verb), *pivotal*, *crucial*, *intricate/intricacies*, *meticulous(ly)*, *boasts* (meaning "has"), *showcase/showcasing*, *garner*, *foster(ing)*, *bolster(ed)*, *enhance/enhancing*, *emphasising*, *highlighting* (as analysis filler), *interplay*, *landscape* (abstract), *vibrant*, *enduring*, *key* (adjective, reflexive use), *valuable insights*, *align with*, *robust*, *Additionally,* (sentence-initial), *concrete* (as in "concrete evidence/examples" in argumentative replies).

The overused set drifts by model era (*delve* peaked 2023–24 and fell off; *emphasising/highlighting/showcasing* persist in 2025+ models), so treat the list as maintained, not fixed. Note the guide's precision: a word being overused does **not** taint its synonyms; ban the actual words, not the concept.

### 2.2 Copula avoidance

LLMs dodge plain *is/are/has*: "serves as the company's flagship", "functions as", "represents a shift", "features four spaces", "offers a range of", "began his career as" (for "was"). Corpus studies show a >10% drop in *is/are* in post-2023 LLM-touched text. Plain copulas are a positive human sign — the generated base-voice file should explicitly prefer "X is Y" and "X has Y".

### 2.3 Negative parallelisms

The most stereotyped AI sentence shapes:

- **Not just X, but Y**: "It's not just a tool — it's a philosophy", "not only dismissive but also harsh".
- **Not X, but Y**: "This isn't dilution. It's evolution." / "no fluff, no hype, just results".
- **X rather than Y** used reflexively to manufacture contrast.
- **Hook transitions** manufacturing momentum between paragraphs: "But here's the kicker:", "That's only half the story.", "And that's where it gets interesting." — bridge paragraphs with the actual conceptual link instead.

Humans use these occasionally; LLMs reach for them constantly to fake profundity. Lint should flag them; drafts should earn any contrast with actual content on both sides.

### 2.4 Rule of three

Triads everywhere: "adjective, adjective, adjective", "short phrase, short phrase, and short phrase", three-bullet lists by default, "ownership, consent, and dignity". Mechanically symmetrical triples make superficial analysis look comprehensive. Vary list lengths; let rhythm follow the content.

### 2.5 Elegant variation (synonym cycling)

Repetition penalties make models cycle synonyms instead of repeating a term: "non-conformist artists… like-minded artists… Russian avant-garde artists… these artists". Humans (native English writers, at least) repeat the natural term. Personas should name the thing the same way each time unless the person demonstrably varies.

### 2.6 Nominalization density and uniform rhythm

Two structural tells with hard empirical backing (PNAS corpus studies): instruction-tuned models use **participial clauses at 2–5× human rates and nominalizations at 1.5–2×** ("the implementation of the solution provided an improvement" for "implementing it improved things"), and they emit **uniform mid-length sentences** where humans are spiky — a two-word fragment here, a 40-word run-on there. LLM text mimicking an author measures at roughly *half* the author's perplexity even when the surface style matches: the blueprint is copied, the unpredictability isn't. Prefer plain verbs over "-tion/-ment/-ness/-ity" abstractions, and vary sentence length deliberately — rhythm variance is a fidelity lever, not decoration.

The overcorrection is equally detectable: a **metronomic short-then-long alternation** (punchy fragment, longer explaining sentence, punchy fragment, longer explaining sentence…) is uniform rhythm at one remove, and readers — especially the person being imitated — flag it as AI. Human spikiness is a distribution: short beats cluster where the writer got emphatic, and whole paragraphs pass without one.

### 2.7 Em dash overuse

LLM text uses em dashes more than non-professional human writing of the same genre, in a formulaic "punched-up" way — often spaced, often in pairs, often powering a negative parallelism — like this. Because the tell became notorious, newer models suppress it; absence proves nothing. The generated persona should encode the **person's actual dash habit** from their corpus (many people never use them; if so, ban outright and let the lint enforce it).

### 2.8 Missing epistemic stance

Corpus work on lexical bundles (Jiang & Hyland 2024/25) finds AI prose leans on noun- and preposition-based bundles for transitions and abstraction, while human writers use clause bundles that carry authorial presence: "I believe that", "my read is", "some argue that", "what I'd watch is". The absence of a visible author weighing things is itself a tell — AI text reads expository even when prompted to persuade. Capture the person's actual stance markers and hedges during extraction and encode them as a positive habit (where their corpus shows them; never invent a stance the task didn't supply).

## 3. Style and formatting tells

- **Title Case Headings** on every section. Most people write sentence case; use whatever the corpus shows.
- **Bold overuse**: mechanically bolding key phrases in a "key takeaways" fashion, or bolding every instance of a term.
- **Inline-header bullet lists**: `**Durability:** description…` — bullet + bold label + colon + explanation, repeated. The signature AI list shape. Also emoji-decorated headings/bullets (🚀 ✅ 💡) and numbered lists where numbers add nothing.
- **Unnecessary tables** for three facts that belong in a sentence.
- **Curly quotes** mixed inconsistently with straight quotes (model/platform-dependent; Claude and Gemini mostly emit straight quotes, so this is weak evidence either way).
- **Section summaries**: paragraphs opening *In summary*, *In conclusion*, *Overall*; a closing section that restates the piece.
- **Self-narrating meta-labels**: the writer announcing their own register or structure instead of just writing in it — *Short version:*, *The honest one:*, *Long story short:*, *Thanks for reading* as an opener. A person being brief is simply brief; a label promising brevity or honesty is the tell.
- **Didactic disclaimers**: *it's important to note/remember*, *worth noting*, *it should be mentioned*. Older-model tell but still common in prompted "professional" tone.
- **Thematic breaks** (`---`) before every section; heading levels that skip.
- **Chat leakage** (fatal in ghostwritten content): *I hope this helps*, *Certainly!*, *Would you like me to…*, *Here's a…*, *Let me know if…* — assistant correspondence pasted as content. Also placeholder text left unfilled: `[Your Name]`, `[insert example]`, `2025-XX-XX`.
- **Knowledge-cutoff/speculation disclaimers**: *as of my last update*, *specific details are not widely documented*, *based on available information* — plus speculative filler about what the missing information "likely" is.
- **Markdown artifacts in the wrong medium**: `**bold**` asterisks or `##` headings surviving into a LinkedIn post (which renders neither), ````` fences, `citeturn0search0` / `oaicite` / `utm_source=chatgpt.com` residue in links. Lint for these; they are near-certain proof of unreviewed paste.

## 4. Signs of human writing (preserve and emulate these)

The guide's inverse list — patterns *more* common in human prose that models avoid because they don't sound "formal, neutral, encyclopedic":

- **Simple is/has phrases**: "there is a", "it has a".
- **Plain verbs** over stiff synonyms: *wrote* not *authored*, *used* not *utilised*, *moved* not *relocated*, *tried* not *attempted*, *died* not *passed away*.
- **Superlative or definitive commitments**: "the best decision we made", "the only reason", "we were first". LLMs hedge toward the mean; people commit.
- **Honest hedges and intensifiers**: *very*, *perhaps*, *tends to*, *I think* — a person weighing something, not weasel attribution.
- **Wordy human constructions**: *as a result of*, *in order to*, *the fact that* — mild inefficiency reads human.
- **Specific, unusual, low-frequency facts** — the sharp detail regression-to-the-mean erases. This is where a real corpus is gold: the person's actual anecdotes, numbers, and phrasing quirks cannot be statistically inferred.
- **Uneven rhythm**: fragments, asides, a sentence that runs long because the thought did, inconsistent list punctuation. Perfect uniformity is the machine tell.

When mining a writing corpus, these are as important to capture as the bans: they are what the persona must actively *do*, not merely avoid.

One dating fact worth using during corpus intake: ChatGPT launched publicly on 30 November 2022, and earlier LLMs were niche paid services. Writing that verifiably predates that launch can be treated as guaranteed human — the most trustworthy extraction material a corpus can contain.

## 5. Ineffective indicators (don't overcorrect)

Things that look like tells but aren't, per the guide — a persona must not sand these off when the corpus shows them:

- **Perfect grammar** — many humans write cleanly.
- **Formal or "fancy" prose** — only the specific overused words correlate with AI, not formality itself.
- **Transition words in isolation** — *however*, *consequently* are ordinary; only formulaic sentence-initial *Additionally,* patterns matter.
- **Mixed casual/formal register** — often just a technical person, a young person, or neurodivergence.
- **Em dashes per se** — professional human writers use them; the tell is density + the spaced punchy pattern + co-occurrence with other signs.
- **Repeated functional structure** — a document that gives every entry the same labelled sub-sections ("Why they ask / A good answer / The trap") is scaffolding, not a tell; readers and owners *like* it because it aids scanning. See §6 on structure versus texture before "fixing" consistency.

## 6. The empirical layer (2023–2026 research)

Distilled from a July 2026 deep-research pass over corpus studies, perception experiments, and editorial style authorities (where a package bundles the full report, it lives at `references/research/ai-writing-markers-research.md`). The field guide above is observational; this layer is quantified, and it changes how seriously to take the whole file.

### 6.1 Expert readers catch AI text almost perfectly

In controlled trials (Russell et al., ACL 2025; 300 articles, active evasion including paraphrasing and "humanise" prompts), annotators who rarely use LLMs detected AI poorly and overestimated themselves — but a majority vote of five **frequent LLM users misclassified 1 article in 300** (99.6%), beating automated detectors. Their reported cues were structural and tonal — formulaic document shapes, "optimistically vague introductions and conclusions", over-polished cadence — with vocabulary only the first-pass heuristic. Kill the working assumption "if it reads fluently, nobody can tell": the professional audiences these personas write for are heavy LLM users, i.e. exactly the readers who can tell.

### 6.2 Being read as AI costs real trust

Pre-registered experiments (Sahebi et al. 2026, N=547; Nakano et al. 2025, N=261) find an **AI Penalty**: text attributed to AI is rated less trustworthy, less authentic, less competent, less caring, and less worth acting on — because readers price the author's effort and relational intent. There is also a **Disclosure Paradox**: audiences say disclosure is ethically required, then penalise disclosed content anyway. For high-involvement B2B audiences, assume the penalty applies in full. The only durable posture: writing so grounded and specific it reads as the named human's judgment, with that human genuinely reviewing and owning it.

### 6.3 The structural tells, quantified

- **Nominalisations at 1.5–2× and present-participial clauses at 2–5×** human baselines (Reinhart et al., PNAS 2025) — the "informationally dense, noun-heavy" register instruction tuning rewards.
- **76% of syntactic templates** in AI text mirror high-frequency pre-training patterns, versus 35% in human text (Shaib et al. 2024).
- **Templated discourse sequences**: 83–90% of AI responses to a given task follow one identical macro-structure where humans scatter widely (Gueorguieva et al. 2026). The tell is document-shaped, not sentence-shaped.
- **Low burstiness**: AI sentence lengths cluster tightly around the mean; human variance is far wider. This is what the lint's fingerprint block measures.
- **AI-vocabulary frequency spikes of 9.8–34.7×** pre-2023 baselines for words like *meticulous*, *intricate*, *commendable*.
- **Missing stance bundles** (see §2.8) — the measurable absence of an author.

### 6.4 Structure and texture are different things

Reconcile two findings that look opposed: predictable structure *helps* readers (repeated scaffolding lowers effort; owners ask for labels to be clearer, not removed), yet "templatedness" is the strongest document-level tell. The resolution: **repeat the scaffold, vary the texture.** What marks AI is every unit landing the same aphoristic closer, the same contrast construction, the same entry length — uniform *rhetorical texture*. What helps humans is consistent *functional structure* whose entries vary in length by how much there genuinely is to say, and whose flourishes are rationed (§1.7's epigram budget). When editing "AI-sounding" repetition, sand the texture, never the scaffold.

Two corollaries, both confirmed by blind-testing a rules-compliant persona on fresh content (2026-07): **texture rules must be countable** — "vary the rhythm" as an intention regresses under generation (§6.5), so state budgets a draft can be checked against (at most half of repeated units opening on a fragment; at least one unit with no landing line; no two units ending on the same rhetorical move). And **scaffold slots are fabrication traps** — a repeated slot that demands a motive, pain, or psychology the source doesn't supply gets filled with plausible invention ("wants comfort", "is listening for a firm no"); the fix is to state observable behaviour or leave the slot leaner, never to manufacture the internal state.

### 6.5 What removes the tells, and what backfires

- **Zero-shot style instructions fail.** "Write like a human", "vary your sentence length", "be engaging" trigger regression to the default register or overcorrect into the short/long metronome (§2.6). Vague "be conversational" prompts also hallucinate chatty transitions the Economist-style guides ban ("Surprise, surprise…").
- **What works:** (1) **flatten then reconstruct** — extract the substance from source material as a deliberately style-less draft, then rewrite it under few-shot voice anchors and hard constraints, rather than asking the model to draft stylishly from zero; (2) **deterministic checks over self-assessment** — the voice lint exists because "I checked" is not checking; (3) **explicit negative constraints in context** — this file plus the lint config, present while drafting, measurably bounds both surface and structural tells.
- **Editorial authorities converge on restraint.** The Economist: let the analysis show it, never hector, cut pre-packaged metaphor. McKinsey: every claim quantified, active verbs, no puffery. BCG: short action titles that lead with the number. The shared rule beneath all three: the facts persuade; the prose stays out of the way. A persona whose corpus shows restraint should treat that restraint as its strongest anti-AI asset.

## 7. Drafting checklist (run on every piece a persona produces)

1. Could any sentence move to a different topic unchanged? Rewrite it with a specific.
2. Any banned-vocabulary word or phrase from §1–§2? (The lint catches the listed ones; you catch the spirit.)
3. Any participle-tail analysis, negative parallelism, hook transition, or manufactured triad? Earn it or cut it.
4. Copulas: is anything "serving as" what it simply *is*?
5. Formatting: does the shape (bullets, bold, headings, emoji, dashes) match the person's corpus, not chatbot defaults?
6. Ending: does it land the way this person lands, or does it summarise/moralise/speculate about the future?
7. Chat leakage, placeholders, markdown artifacts: zero tolerance.
8. Epigram budget: does more than one unit per page or section end on a quotable line, or does any landing line or contrast construction recur anywhere in the document (captions and panel text included)? Keep the best instance; end the rest on information. Do headings and names survive a literal reading and a skim?
9. Texture check: across repeated units, does the length vary with the content, or does every entry land the same rhetorical move? Sand the texture, keep the scaffold (§6.4).
10. Positive check: does it contain at least one thing only this person could have written — a lived specific, an owned opinion, their actual phrasing? If not, it isn't done, even if it's clean.
