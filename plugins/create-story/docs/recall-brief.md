# Recall brief: author style from a model trained on the books

The influence cards in `skills/create-story/references/influences.md` are sourced from interviews, reviews and stylometry. A model trained on the books themselves can add a second layer: what it remembers of how the prose actually reads, sentence by sentence. That layer is recall, not evidence, so it goes on the card as `recall:` lines and is used only when `voice_card.py compose --use-recall` asks for it.

This brief is written to be run outside a Claude Code session, because a nested `claude -p` call hangs in one. From a plain terminal:

```
claude --model claude-opus-4-8 --effort high --strict-mcp-config --mcp-config '{"mcpServers":{}}' --allowedTools "" \
  -p "Read the brief at $(pwd)/docs/recall-brief.md and answer its task section." > /tmp/recall.json
```

Then paste each author's lines under `recall:` on that author's card, one line per item, and add a `sources:` line reading "recall: claude-opus-4-8, <date>".

## Task

For each of the twelve authors below, describe the OBSERVABLE habits of their prose as you remember it from the named books: sentence length and rhythm, point of view and tense, how much of a page is dialogue, paragraph length, how chapters open and close, diction register, and any move a reader would recognise the author by. State each habit as one checkable sentence a drafter could follow. Do not quote passages longer than six words. Do not describe plots, settings or characters. Where you are unsure, say so in the line rather than leaving it out.

Return only JSON in this shape:

```
{"authors": [{"name": "...", "recall": ["one checkable sentence", "..."], "confidence": "high|medium|low"}]}
```

At most six lines per author.

Authors and works:

1. Andy Weir: The Martian, Project Hail Mary, Artemis
2. Hugh Howey: Wool (the Silo trilogy)
3. Alex Scarrow: Last Light, Afterlight, TimeRiders, Remade
4. David Peace: the Red Riding Quartet (1974, 1977, 1980, 1983)
5. Robert J. Sawyer: Flashforward, Calculating God, Quantum Night, the WWW trilogy (Wake, Watch, Wonder)
6. William Gibson: Neuromancer
7. Richard Matheson: I Am Legend
8. A. G. Riddle: The Atlantis Gene, Winter World
9. J. K. Rowling: the Harry Potter series
10. K. A. Applegate: Animorphs
11. R. L. Stine: Goosebumps
12. Robert Kirkman: The Walking Dead comics and the novels with Jay Bonansinga
