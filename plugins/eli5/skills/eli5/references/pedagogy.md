# Pedagogy — the frameworks in operational form

`evidence.md` says what the research found and how strongly. This file says what to
type. Read it when the analogy will not come, when the interaction feels decorative, or
when the draft reads like a summary rather than an explanation.

## Finding the causal invariant

The invariant is the relationship that, once seen, makes the rest follow. It is not the
topic's definition and it is not a list of its parts.

A working test: write the candidate as a sentence with a verb of *causation, constraint
or conservation*. If the verb is "is" or "has", you have a definition, not an invariant.

| Topic | Definition (not this) | Causal invariant (this) |
|---|---|---|
| Raft | A consensus algorithm with leaders and followers | A term backed by a majority is authoritative; a term without one is only a proposal |
| Virtual memory | A layer mapping virtual to physical addresses | Every address is a *question* the hardware answers, so the answer can change without the asker knowing |
| Self-attention | A mechanism computing weighted sums over tokens | Each token writes a query about what it needs; every other token advertises what it has; the match decides the mix |
| Diffie-Hellman | A key exchange protocol | Two people can each do a private operation whose *order does not matter*, so both reach the same place without either revealing their step |
| TCP handshake | A three-way connection setup | Neither side may assume it can be heard until it has heard itself echoed back |

Notice the last one. That framing makes the *third* packet obvious — which is the part
every flat explanation of the handshake leaves mysterious.

## Naming the misconception

An explainer with no target changes nothing. Ask what a competent person believes here
that is wrong, then build to break it.

| Topic | The misconception worth defeating |
|---|---|
| Raft | That the leader is special. It is not; it holds a lease that a majority may decline to renew. |
| Virtual memory | That addresses name places. They name entries in a table that the OS may rewrite under you. |
| Self-attention | That the model looks things up. Nothing is retrieved; everything is blended, weighted continuously. |
| Diffie-Hellman | That something secret crosses the wire encrypted. Nothing secret crosses at all. |
| Garbage collection | That objects are freed when unreachable. They are freed when the collector next looks. |
| HTTPS | That the padlock means the site is trustworthy. It means the pipe is private. |

Write the misconception into the artifact explicitly — as *"the thing most people get
wrong"* — rather than only correcting it silently. Naming the error is what makes the
correction stick.

## Structure-mapping in practice

Gentner's constraint: analogy transfers **relations**, not attributes. Build the table
before the prose, and check each row is a *relation* with two or more arguments.

- Attribute (worthless): "both are big", "both are fast", "both are blue"
- Relation (the whole explanation): "x drives y", "x resists y", "x is conserved across y",
  "more x means less y"

Then the **systematicity check**: prefer the mapping where the relations *interlock*. One
matched relation is a simile; a system of relations that constrain each other is an
explanation that generates correct predictions the reader was never told.

### Choosing the source domain

- **Near enough to be owned.** Plumbing, post, queues at a counter, keys and locks, maps
  and territory, recipes, traffic. Things the reader has bodily experience of.
- **Far enough to force thought.** Sources with fewer surface similarities but real
  structural correspondence reduce overinterpretation (`evidence.md` §1.1). "A CPU cache is
  like the pile of papers on your desk versus the filing cabinet" beats "a cache is like a
  smaller, faster memory", which explains nothing by restating.
- **Never anthropomorphic without flagging it.** "The router *decides*" installs
  intentionality. If you use it, mark it as shorthand.

### The boundary is the deliverable

Every analogy gets a stated stopping point. Format that works:

> **Where this stops being true.** Water in a cut pipe sprays out. Current in a cut wire
> stops entirely — there is no charge spilling onto the floor. The analogy carries pressure,
> flow and resistance. It does not carry what happens at a break.

Three parts: what carries, what does not, and the concrete case where believing the
analogy would give the wrong answer. That last part is what makes it memorable.

## Predict-Observe-Explain — phrasing that works

The beat is worth roughly double the effect of an unprompted slider (`evidence.md` §1.3),
and it fails when it is vague. Make the prediction **discrete, committed and cheap**.

Good:
> Five nodes. Three can reach each other; two are cut off on their own.
> **Which side elects a leader?**  ( ) the three  ( ) the two  ( ) both  ( ) neither
> → *Run it*

Bad: "Try dragging the slider and see what happens." Nothing is committed, so nothing is
at stake, so nothing is learned.

The **Explain** half matters as much as the prediction. After the reveal, name the one
assumption that made the wrong pick a sound inference, and where that assumption stops
holding:

> Most people pick "both" — and in a system without quorum, both *would*. That is exactly
> the split-brain failure Raft's majority rule exists to prevent.

A reader who was wrong and now understands why their model was coherent has learned more
than a reader who was right.

## Staging the three passes

The **form** decides how depth is presented — scroll position, a depth control, what the
reader unlocks, tabs where tabs genuinely fit (`forms.md`). What each pass owns does not
change with the form. Mark each one `data-pass="1|2|3"` on its container, which is how the
gate checks staging without requiring any particular chrome.

| Pass | Owns | Live variables | Register |
|---|---|---|---|
| 1 | The causal invariant, the analogy, the boundary | Exactly one | Plain, concrete, zero jargon |
| 2 | The steps, in order, reader-paced | Two or three | Jargon introduced *and defined at first use* |
| 3 | Production behaviour, edge cases, what is still omitted | Open | Technical; the reader has earned it |

**Name the sections from the topic, not from this table.** Three consecutive artifacts built
by the first version of this skill carried the same stage names verbatim, and the gate's
`no-template-boilerplate` rule exists because of it. A Raft explainer's sections are about
terms, quorums and logs.

The third pass closes with what it leaves out. Without that line the reader finishes
believing they have the whole thing, which is worse than knowing they do not
(`evidence.md` §1.12):

> **Still simplified here.** Real Raft also handles log compaction, snapshot transfer and
> membership changes mid-term. Each of those is a mechanism this page never showed you.

## Coherence — what to cut

Mayer's coherence principle costs d = 0.65–0.86 when violated (`evidence.md` §1.7). Cut:

- Background particles, gradients that encode nothing, ambient drifting motion
- Emoji standing in for a diagram
- Icons chosen for personality rather than meaning
- Any animation that plays whether or not the reader is looking at it
- Historical asides and vendor trivia that do not bear on the mechanism

Keep every mark that encodes a real variable. The test is: *if I deleted this, would the
reader be able to answer one fewer question?* If not, delete it.

## The register, held under pressure

The failure is subtle in the middle of a page. Symptoms:

- Exclamation marks doing the work that clarity should do
- "Simply", "just", "easy" — all of which tell a stuck reader they are stupid
- Rhetorical questions the page immediately answers ("So what's going on here? Well…")
- Diminutives: "a little bit of data", "our tiny message"

The replacement is not formality. It is **concrete physical verbs**: holds, passes, locks,
routes, blocks, spills, waits, echoes. They carry mechanism, and they are shorter.
