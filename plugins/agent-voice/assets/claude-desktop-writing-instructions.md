# Claude Desktop instructions: a fault line names its actor

Paste the block below into Claude Desktop under **Settings → Profile → personal preferences**
(the box headed "What personal preferences should Claude consider in responses?"). It is written
to be pasted whole, and it is about one thing: how Claude describes something that went wrong.

The style it displaces is worth naming so you recognise it when it comes back. Three shapes
compound into it, and together they read like a film trailer:

An event gets named by its absence, as in "A merge that had never happened". A passive or
abstract subject stands where an actor belongs, as in "The command meant to check the evidence
overwrote it". And an ironic reversal closes the clause, as in "A check that could never have
passed".

A verbless noun phrase does the same job in one line: "Markers with nothing holding them" states
a subject and withholds the consequence, so you supply it yourself. The register is compelling,
which is exactly the problem. It withholds the two things a fault line exists to carry: who did
it, and how much.

## The block to paste

```text
When you tell me something went wrong, name who or what did it, and give the number.
"I recorded a merge that had not happened" and "the verify command re-hashed 30 digests it
was checking" are the shape I want. Write each fault as a full sentence with a subject, a
verb, and its cost to me.

Three habits pull against this, so write around them:
- Name the event, not its absence: say what happened rather than what never did.
- Put the actor in the subject: you, a named command, a named file, a named person.
- Let the irony sit in the facts: state the outcome plainly and let me notice the reversal.

A finding gets a sentence rather than a caption. Instead of "Markers with nothing holding
them", write "47 rows carry a marker no manifest entry accounts for, so the check cannot
verify them".

This applies to your own mistakes most of all. When you got something wrong, say "I" and
say what it cost, in the same sentence.

Keep the same voice everywhere: reports, chat replies, commit messages and documents.
```

## Two shorter variants

If your instruction box is already full, this carries most of the effect in three sentences:

```text
When something went wrong, name who or what did it and give the number, in a full sentence
with its cost to me. Say "I" for your own mistakes. A finding is a sentence, not a caption.
```

And if you want it as a reminder near the end of a longer instruction set, where a tail
reminder holds better than a rule stated once at the top:

```text
<tone_preference>
Fault lines name their actor and their number.
</tone_preference>
```

## Why each line is there

**It is phrased as what to do.** Anthropic's current guidance is explicit: *"Tell Claude what to
do instead of what not to do"*, with the worked example of replacing "Do not use markdown in your
response" with "Your response should be composed of smoothly flowing prose paragraphs". A
prohibition tells the model which door is shut and nothing about the room. So the block leads
with the sentence shape wanted and gives the three habits as things to write around rather than
as bans.

**The examples are before-and-after pairs, and they are short.** The same guidance recommends
three to five relevant, diverse examples, and the Opus 5 page adds that *"positive examples of
the communication style you want tend to be more effective than instructions about what not to
do"*. Four pairs is enough to fix the shape; more starts to read as a style guide and gets
skimmed.

**It names the reason, once.** A rule with its reason attached generalises to the cases you did
not list, which is why the block says a fault line carries who and how much rather than only
listing the shapes to avoid.

**It asks for a countable thing.** "Name the actor" and "give the number" are checkable in a
glance. "Be direct" and "avoid dramatic phrasing" are not, and a model fills an unmeasurable
qualifier with its own priors.

**It says the register applies to Claude's own mistakes.** That is where withheld agency is most
tempting and most costly, because "a merge that had never happened" and "I recorded a merge that
had not happened" describe the same event and only one of them tells you who to ask about it.

**The block itself is written in the voice it asks for.** Anthropic notes that *"the formatting
style used in your prompt may influence Claude's response style"*, so an instruction asking for
plain sentences with named actors is written that way itself.
