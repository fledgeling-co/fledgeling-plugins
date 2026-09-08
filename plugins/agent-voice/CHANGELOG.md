# Changelog

## 0.3.3 - 2026-09-08

The rule widens from a fault line to any line about something that happened, matching the Desktop block at 0.3.2. The 0.3.0 wording said "a line about a fault", which left the register free everywhere else: the page it was measured on carried the same shapes on timings and capacities, where "the reading lane is the slow part, and it times out" names no actor and no figure and "the judge reads 1,460 pairs in eight minutes and times out above 240 seconds a row" names both. Both the lintable rule and the skill constraint now read "a finding, a change you made, a measurement, a mistake or the state of a thing", and `advisory_phrases` gains the two timing fragments. Self-test 18 of 18, 14 worked examples clean, SKILL.md clean at format `skill`.

## 0.3.2 - 2026-09-08

The Claude Desktop block widens from faults to anything that happened, and loses half its words. The 0.3.1 wording opened "when you tell me something went wrong", which left the register free everywhere else — the measured page carried it on timings and capacities too ("the reading lane is the slow part, and it times out"). It now reads "anything that happened: a finding, a change you made, a measurement, a mistake, the state of something", and one of the four before-and-after pairs is a timing rather than a fault. 809 words to 434, with the paste block itself cut to eleven lines.

## 0.3.1 - 2026-09-08

`assets/claude-desktop-writing-instructions.md`: the same rule as a block a person can paste into Claude Desktop's personal-preferences box, with two shorter variants and a note on why each line is phrased the way it is. Written against the current Anthropic guidance rather than from memory: the block says what to do rather than what to avoid (the docs' own worked example replaces "Do not use markdown" with "Your response should be composed of smoothly flowing prose paragraphs"), carries four before-and-after pairs because positive examples of a communication style beat instructions about what not to do, asks for two checkable things (the actor and the number), and is written in the voice it asks for, since the formatting style of a prompt influences the response's.

## 0.3.0 - 2026-09-08

Two shapes join the lintable layer, both about a line describing a fault. A fault line names who or what did it and, where the reader needs it, the number: "I recorded a merge that had not happened" rather than "a merge that had never happened", and "the verify command re-hashed 30 digests it was checking" rather than "the command meant to check the evidence overwrote it".

- **No withheld agency in a line about a fault.** Three shapes drift into a case-file register that reads as a film trailer and they compound: an event named by its absence, a passive or abstract subject where an actor belongs, and an ironic reversal closing the clause. Measured 2026-09-08: fifteen consecutive fault lines in one status page carried no actor and no figure between them, and the reader described the page as a noir case file rather than a status page. The register is compelling and it withholds the two things a fault line exists to carry.
- **No verbless noun phrase where a finding belongs.** "Markers with nothing holding them" states a subject and withholds the consequence, so the reader supplies it. The finding goes in a sentence with what happened and what it cost.
- **Five literal fragments added to `advisory_phrases`** in `scripts/agent-voice-lint.json`, warning rather than failing: the shape needs a reader's judgement, so the config catches its commonest phrasings and leaves the call to the writer. Self-test 18 of 18; the skill file lints clean at format `skill`.
