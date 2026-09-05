# Influences

One card per author. `scripts/voice_card.py compose` turns a base card plus up to three influence cards into the bible's `## Voice` section, and `voice_card.py check` measures a drafted scene against the bands that section declares. A card carries what can be observed from the outside: point of view, tense, sentence-length band, dialogue share, paragraph ceiling, then the named moves a drafter can follow and a critic can quote a slip of, then what to borrow and what to leave. Themes, plots and characters are not on a card, because an influence is a way of writing, not a thing to write about, and a scene that borrows an author's subject reads as pastiche.

Card format, read by the script:

```
## <Author name>
works: <the books the card was drawn from>
person: first | third | any
tense: past | present | any
sentence_mean: <lo>-<hi>        words per sentence, narration only
dialogue_share: <lo>-<hi>       share of words inside quotation marks
paragraph_max: <words>
moves:
- <one checkable rule, sourced>
recall:
- <one checkable rule a model remembers of the books; used only with --use-recall>
borrow:
- <what to take>
leave:
- <what not to take>
sources:
- <where the observation came from>
```

A `recall:` line is a model's memory of how the prose reads (the brief for producing them is `docs/recall-brief.md`), kept apart from `moves:` because memory of a book is not a citation; `compose --use-recall` lets recall lines fill rule slots after the sourced moves, suffixed [recall]. Bands are drawn so that the author's own prose sits inside them with room; when two chosen cards' bands overlap, the composed band is the overlap, and when they do not, the base card's band stands. The rules are taken base first, then one from each influence in turn, capped at five, so no single influence crowds the others.

## Luke Rhodes

works: the create-luke-content voice reference and its book persona, read on 5 September 2026
person: any
tense: any
sentence_mean: 8-18
dialogue_share: 0.05-0.6
paragraph_max: 110
moves:
- No em dashes anywhere; a semicolon for a linked clause, a comma for a light pause, a full stop to split.
- Spiky sentence lengths that turn where the thought turns, never a metronomic short-then-long alternation.
- Plain verbs with a named actor, no -tion and -ment abstractions, contractions throughout, Australian spelling.
- Every sentence carries its referent; a fragment sits hard against the thing it refers to.
- One concrete thing within a sentence of any abstract one, and short paragraphs with air between them.
borrow:
- the dry, understated wit used sparingly, never explained
- the calm register where energy comes from the material rather than from exclamation
leave:
- the technical-writing furniture (bold key terms, "Note:" callouts) which belongs to product prose, not to a scene
sources:
- create-luke-content `references/luke-voice.md`, sections Mechanics, Syntactic fingerprint and The voice in one breath
- create-luke-content `references/personas/adhd-book.md`, section 2, the Luke half of the merged register
- bands: sentence_mean around the 14.5-word corpus average the create-luke-content lint measures against; dialogue_share and paragraph_max are this skill's judgement, unmeasured

## Andy Weir

works: The Martian, Project Hail Mary, Artemis
person: first
tense: any
moves:
- Narrate as a log or journal entry when the frame allows: dated, first person, the narrator talking to a reader who is not there.
- Humour is the narrator's default register, not a device laid on top; the joke arrives inside the technical sentence.
- Every technical detail is carried by a line of wit so a general reader stays with it.
- A flashback lands only when the reader is already asking the question it answers.
borrow:
- the competence-under-pressure narrator who explains by doing
- the flashback placed as an answer
leave:
- the specific problems (potatoes, astrophage, lunar welding); a borrowed problem is a borrowed plot
sources:
- Publishers Weekly review of The Martian, 25 Nov 2013: "Weir laces the technical details with enough keen wit to satisfy hard science fiction fan and general reader alike."
- Weir on Goodreads Q&A: "Originally I had it in mind for the whole book to be just his log entries."
- Writer's Digest interview, 22 Jan 2018: "The humor is just my narration style."
- Astronomy interview, 16 Mar 2026: "I tried to structure my flashbacks such that you are happy when they happen."

## Hugh Howey

works: Wool (the Silo trilogy)
person: third
tense: past
paragraph_max: 130
moves:
- One scene is one chapter; the chapter list is the scene list.
- Paragraphs run three to seven sentences of similar length, and a one-line paragraph is kept for the rare moment that earns it.
- Plain, functional prose that is strongest on machinery, physical movement and bodily danger.
- Each section escalates to its own climax; the book reads as a chain of self-contained rises.
borrow:
- the scene-as-chapter discipline
- the physical specificity of hands on machines
leave:
- the silo, the cleaning, the stairs; the setting is the book
sources:
- Howey, "Questions about my process", 16 Mar 2012: "Then I'll make a list of scenes, which become my chapters."
- Howey, "Writing insights part three", 24 Aug 2017: "Short paragraphs stand out – but only if used sparingly!"
- The Astromech review of Wool, 3 Dec 2025: "He writes machinery, movement and physical danger particularly well."
- bands: paragraph_max follows from Howey's three-to-seven-sentence paragraphs; the number is a judgement

## Alex Scarrow

works: Last Light, Afterlight, TimeRiders, Remade
person: third
tense: past
moves:
- Rotate between three or four close third-person viewpoints inside a compressed timeframe; the rotation is the pacing.
- Very short chapters that cut like a screenplay, large casts moving through set-pieces.
- Draft at adult register and take the profanity out afterwards, so the pressure stays in the sentences after the swearing has gone.
- Brief interludes from a non-human perspective (the virus in Remade) between the human chapters.
borrow:
- the viewpoint rotation as a pacing engine
- the short chapter as the unit of tension
leave:
- the oil-crash and time-travel apparatus; the mechanism is the franchise
sources:
- Judge Tutor Semple interview, 23 Jul 2013: "At the end of the first draft I nip back in and delete all of the profanity."
- Dead Book Darling review of TimeRiders, 10 Sep 2010: "This book felt like a blockbuster movie – but with a superior script."
- Reflexiones Finales review of Last Light, 27 Jul 2011: "With the four points of view to bounce around between, this tends to keep the pace moving."
- The Bookbag review of Remade, Jun 2016 (interludes from the virus's perspective; urgent pace)

## David Peace

works: the Red Riding Quartet (1974, 1977, 1980, 1983)
person: first
tense: past
sentence_mean: 3-10
paragraph_max: 60
moves:
- One-sentence paragraphs and sentence fragments; a paragraph can be two words.
- Repeated leitmotif phrases that come back changed, the repetition doing the work a summary would.
- Dialogue monosyllabic and abrupt, in the dialect of the place.
- Interior monologue as the narration, no reflective pauses; the plot churns.
borrow:
- the fragment as a unit of dread
- the returning phrase
leave:
- the profanity density and the period Yorkshire dialect, unless the story is set there
sources:
- Publishers Weekly review of 1974, 3 Jan 2000: "Peace's style is punchy and tough, replete with one-sentence paragraphs, partial sentences and a plenitude of f-words"; "The dialogue is monosyllabic, abrupt, and the plot churns with narrative adrenaline."
- Irish Times, 26 May 2018: "the use of leitmotif and repetition, the power of terse one- and two-word sentences, terrifying interior monologues"
- bands: sentence_mean and paragraph_max follow from the one-sentence paragraphs and one- and two-word sentences above; the ceiling is a judgement

## Robert J. Sawyer

works: Flashforward, Calculating God, Quantum Night, the WWW trilogy
person: third
tense: past
moves:
- One viewpoint character per scene, followed through that scene's eyes only; a switch happens at a chapter end or a scene break, never inside.
- Description density scales with the stakes: routine business in a plain line, a major moment slowed and expanded.
- Scientific explanation stated in the open, in blocks, rather than smuggled; the idea is the event.
borrow:
- the single-viewpoint scene rule
- the swelling-and-quiet description curve
leave:
- the inserted explanatory block, which reviewers called clumsy; explain through what a character does with the idea
sources:
- Sawyer, "On Writing" column 7, 1996: "The rule is simple: pick one character, and follow the entire scene through his or her eyes only."
- Sawyer, "On Writing" column 12, 1995: "when something major is happening, increase the amount of description; think of your words as swelling background music"
- Kirkus review of Flashforward, 1 Apr 2000: "explicative passages clumsily inserted into a scattershot narrative"

## William Gibson

works: Neuromancer
person: third
tense: past
moves:
- A hook on every page; the sentence is written against the fear of losing the reader.
- Revise by condensing until each sentence carries more weight than it did; the text gets shorter with each pass.
- Superspecific concrete detail (brand, material, surface) in place of explanation; the technology is never explained.
- Dated subcultural slang mixed with invented terms, none of it glossed.
borrow:
- the unglossed noun
- the condensing pass
leave:
- the cyberspace vocabulary and the noir furniture; the register is the book
sources:
- Gibson interviewed by Larry McCaffery, Aug 1986 (repost, 2 Jun 2012): "Neuromancer is fueled by my terrible fear of losing the reader's attention."; "condensing my prose so that individual parts carry more weight"; "Hammett may have been the guy who turned me on to the idea of superspecificity"
- Paul Brians, study guide to Neuromancer, WSU, 1994 rev. 2013: "Gibson has no hesitation about using rather dated slang in his narrative mixed with futuristic locutions."

## Richard Matheson

works: I Am Legend
person: third
tense: past
moves:
- Third person limited fixed on one character; the reader sees what he sees and shares his moods, nothing more.
- Flat, direct, almost journalistic sentences that report a survival chore and a horror in the same register.
- Description spare; backstory arrives as memory inside the present action, never as exposition.
borrow:
- the chore-and-horror flatness
- the memory as backstory
leave:
- the vampire apparatus and the last-man premise
sources:
- BookRags study guide, style section: "The story is told in the third person from the point of view of Robert Neville ... the reader sees what he sees and shares his thoughts and moods."
- Conquered Worlds essay, 2 Feb 2026: "The language he uses is sturdy, flat and direct; professional in an almost journalistic way."
- FictionFan review, 20 Jul 2015: "The descriptive writing is spare but very effective in building an atmosphere of fear and tension"

## A. G. Riddle

works: The Atlantis Gene, Winter World
person: any
tense: any
moves:
- Very short chapters, some only a snippet of dialogue or a news item, so that things are felt to happen at once in many places.
- Viewpoint changes at the chapter boundary, never inside a chapter.
- In a dual-narrator book, each chapter is headed with the narrator's name and both narrate in first person.
borrow:
- the snippet chapter as a pacing device
- the chapter heading as the viewpoint marker
leave:
- the conspiracy-thriller escalation; the reveal chain is the plot
sources:
- Riddle on Goodreads Q&A: "I used short chapters to add a sense that things were happening rapidly and concurrently in many places."
- BookRags study guide to The Atlantis Gene: "The viewpoint switches from chapter to chapter."
- NetMassimo review of Winter World, 29 Nov 2023: "The story is told in the first person by the two protagonists"
- Winter World's present tense rests on a single Goodreads reader status (20 Jun 2020) and is held loosely

## J. K. Rowling

works: the Harry Potter series
person: third
tense: past
moves:
- Close third limited to one character; the reader knows only what that character witnesses or overhears.
- Dialogue carries the scene, and the tag is "said" plus an adverb more often than in most adult prose (about 140 adverbs per 10,000 words, against Hemingway's 80).
- Word-pair habits are stable enough to identify the author across genres; the voice is in the collocations, not the vocabulary.
borrow:
- the strict single-witness point of view
- the dialogue-led scene
leave:
- the adverb rate, which is the most-cited weakness of the prose, and the school-story furniture
sources:
- Nathan Bransford, "Five writing tips from reading J.K. Rowling", 9 Nov 2010: "we only know what Harry knows and only see what Harry sees"
- Mint (via inkl), Apr 2017, on Ben Blatt's counts: Rowling "used them at the rate of 140 per 10,000" (adverbs); Stephen King's remark quoted there
- Language Log, 16 Jul 2013, on the Galbraith attribution: "The word pairs, on the other hand, were clearly Rowling-like"

## K. A. Applegate

works: the Animorphs series
person: first
tense: past
moves:
- Open in first person with a direct address that gives a first name and refuses the rest because it is too dangerous.
- The narrator rotates per book, and each keeps the same frame so the series voice holds across narrators.
- Written fast to an outline, about six pages a day for three weeks, which shows as momentum rather than polish.
borrow:
- the direct address that names the reader as a confidant
- the rotating narrator inside a fixed frame
leave:
- the morphing and the war; the premise is the series
sources:
- The Paris Review blog, 23 Jan 2019: "\"My name is Rachel,\" they began ... they couldn't tell you their last name, or their exact age, or their location; it was too dangerous." (quoted from the search excerpt; the page itself was blocked)
- Scholastic author page: "Generally, I write about 6 pages a day for 23 or 24 days."
- Applegate AMA, 28 Apr 2011: "books 25 through 52 were ghosted. We did all the outlines"

## R. L. Stine

works: the Goosebumps series
person: first
tense: past
moves:
- Every chapter ends on a shock or a cliffhanger, and the ending is fixed before the chapter is written; the chapter is written to reach it.
- The cliffhanger is usually a fake scare that the next chapter's first line undoes.
- Language kept simple; a twelve-year-old narrates; the book runs 100 to 130 pages from an outline that already holds every chapter ending.
borrow:
- the chapter written backwards from its last line
- the fake-out as a rhythm, used sparingly outside horror for children
leave:
- the fake-out on every chapter, which a reader older than twelve learns to discount
sources:
- Fatherly interview, 13 Oct 2023: "Every chapter ending in Goosebumps is some kind of shock or some kind of cliffhanger, and I know how the chapter's going to end, and then I just write the chapter to get to the ending."
- Sliding Magazine, 10 Oct 2025: "Almost every chapter ends with a cliffhanger, often a fake scare or prank."; "Goosebumps stories are almost always told in the first person by the child protagonist."
- Writer's Digest, 11 Jan 2012: "Keep the language simple."

## Robert Kirkman

works: The Walking Dead comics and the novels with Jay Bonansinga
person: third
tense: present
moves:
- Characters say exactly what they think and feel to whoever asks; there is no subtext, and a withheld feeling is a flat denial.
- The turn of a page or the end of an issue is a set-up and knock-down: the last beat telegraphs that a shock is coming, the reveal lands after the turn.
- The novels run in present tense, close third, at a breakneck pace with occasional slower character passages.
borrow:
- the subtext-free line as a way to make a scene move
- the set-up before the knock-down
leave:
- the walkers and the survival-camp politics
sources:
- The Comics Journal review of The Walking Dead 100, 13 Jul 2012: "The Walking Dead is a subtext-free comic. Writer Robert Kirkman's characters say exactly what they're thinking and feeling to anyone who asks at almost any time."
- Screen Rant, 5 May 2025, relaying Kirkman's notes in The Walking Dead Deluxe 110: "I do like a set-up and knock-down structure to my page turns."
- Shelf Awareness review of Rise of the Governor, 28 Oct 2011: "Told in the present tense, mainly from Brian and Phillip's perspective"
