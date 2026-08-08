# Discovery — pinning down what the skill is actually for

The phase that decides whether the rest is worth running. An improved
skill has a predecessor to argue with; a new one has only the brief, so
an unstated intention becomes a wrong skill built well.

## Answer it yourself before you ask

Every question you ask costs the user attention and implies you have not
read what they already gave you. Before writing a single question, mine:

- **This conversation**, including anything they said in passing about
  how they work or what annoyed them last time.
- **The repo**: existing skills, their READMEs, CLAUDE.md, the portfolio
  manifest, recent commits touching the area.
- **Sibling skills** in this and the user's other marketplaces, which fix
  naming conventions, structure and house style.
- **Earlier work in the session** you may have lost track of: a subagent's
  findings, a failed workflow's partial output, a research report that
  already answered it, a plan file written an hour ago.

Ask only what survives that sweep. When you do ask, say what you already
worked out, so the question reads as narrowing rather than starting over.

## How to ask

Use **AskUserQuestion**. For each question:

- **Multi-choice wherever the options are genuinely discrete.** Free text
  for a genuinely open axis; never a menu of near-synonyms.
- **Each option states what it means and what it costs**, not just a
  label. "Deterministic scripts (slower to build, reproducible output)"
  beats "scripts".
- **Lead with a recommendation** and mark it, with the reason in the
  description. A recommendation the user rejects tells you more than an
  open question they answer briefly.
- **Notes are always welcome.** Say plainly that they can add detail to
  any answer; the notes field is where the real constraint usually
  arrives, and it is often the thing that changes the design.
- **Batch them.** One round of up to four questions beats four rounds of
  one; each round costs a context switch.

## The axes a skill actually turns on

Cover these, in as few questions as they genuinely need. Several will
already be answered by the sweep above; ask only about the rest.

1. **Trigger.** What does the user type or intend when this should fire?
   Under- and over-triggering are both real failures, and the answer
   becomes the description's phrasing.
2. **Output.** What lands on disk or in the reply, in what format, and is
   it a deliverable, a report, or a change to files?
3. **Audience.** Who reads the output: the user, a teammate, a future
   agent, a build system? An artifact written for an agent is shaped
   differently from one written for a person.
4. **Definition of done.** What has to be true for a run to be a success?
   This becomes the eval assertions, so vagueness here means untestable
   evals later.
5. **Hard constraints.** What must the skill never do — touch production,
   spend money, push, delete, contact an external service? These become
   rules, not preferences.
6. **Checkability.** Is the output objectively verifiable (files, exit
   codes, string matches) or a matter of judgment (writing, design)? This
   decides whether evals are structural assertions or a judge panel, and
   it is worth asking directly.
7. **Routing.** Which existing skills or tools should it call rather than
   reimplement? Duplicated capability is the most common waste in a
   marketplace of related skills.
8. **Scale and cost.** Does a run spend real money (APIs, image models,
   research panels)? If so, the skill needs a stated budget posture.

## When an answer is too vague to build on

Say so, and ask again with narrower options. "It should help with
testing" does not determine a trigger, an output or a success condition,
and building against it produces a skill that fires at the wrong time and
delivers the wrong artifact. Offer two or three concrete readings of the
vague answer and let the user pick; that converts an open question into a
discrete one and usually resolves in a single round.

## Recording the brief

Write the agreed brief down before research starts — the trigger, the
output, the done condition, the constraints, the routing, and every
assumption you are proceeding on. It becomes the spec the evals are
written against, and the thing to re-read when a later phase drifts.
Anything the user did not settle is recorded as a stated assumption, not
quietly resolved.
