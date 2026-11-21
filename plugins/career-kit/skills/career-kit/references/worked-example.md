# Worked example — the run this skill came from

One real run, with the person's name changed to L. and every contact detail removed. The full
record of the session, under her own name, lives in `SESSION-RECORD.md` in that project; this
file carries only what is useful as a pattern.

**The person.** A product owner at a large Australian bank, twenty years at the same employer
across six roles, applying for five internal roles at once. A family member ran the sessions
and relayed her answers.

**The shape of the work.** Four research lanes on Australian bank hiring in 2026, reconciled
into one digest. A 20-finding review of her existing résumé and LinkedIn. Five role-targeted
résumés from one source file. A personal website. LinkedIn copy. An interview guide with about
thirty questions. Two question forms, a day apart.

## The variant spec

Five roles, one facts file. What actually differed per variant was three fields:

```json
{"variants": {
  "Product-Owner": {
    "summary": "<intro> Own the roles and entitlements backlog and its outcomes within a
      12-person squad ... within the Chief Product Owner's direction. <background>",
    "skills":  ["product", "risk", "leadership", "tools"],
    "bullets": ["prio", "discovery", "sod", "model", "releases", "dependencies", "identity", "ai"],
    "max_pages": 2},
  "Delivery-Lead": {
    "summary": "<a different opening, mirroring the delivery ad's phrases> ...",
    "skills":  ["delivery", "leadership", "risk", "tools"],
    "bullets": ["releases", "plan", "dependencies", "identity", "sod", "prio", "ai"],
    "max_pages": 2}}}
```

Nothing else changed. The bullets are keys into one shared map, so a corrected bullet corrected
five documents.

## Three corrections, and what they changed

**Scope.** Her first draft said she owned the squad's backlog. She owns one of about three
backlogs inside a twelve-person squad, and said overstating it "could raise eyebrows" with
internal readers who know the real structure. The wording became "one of the backlogs in a
12-person agile squad" everywhere. She also declined "one of about three backlogs" as too
specific, which is the useful half of the lesson: the correct scope statement is hers to choose,
not the most precise one available.

**Targeting.** The first résumé was a good generic product owner résumé. The instruction was
that it had to target the five named roles, using the research. That is where the one-file,
many-variants build came from.

**Weighting.** Asked for example answers about her workforce planning and IVR work, the relay
said not to dwell on it, because that work ended seven years ago. Recent roles carry the
document; earlier ones get a line or two.

## Two things that went wrong quietly

A fixed-height page container cut bullets off page one of all five résumés. The page count was
still two. Nothing errored. It was found by looking at the rendered pages.

A private interview-practice page was deployed unlisted, with a `noindex` header and a footer
mentioning a password that was never set. It returned 200 to anyone with the URL and carried
three figures she had asked to keep off public pages.

## What the panels decided, and what they did not

A five-model panel settled the photo question 5-0 and chose between three phrasings of a
coaching sentence 4-1. A five-model panel on four hero-image concepts split 3-2, and the person
chose a different combination that none of the five had proposed. Panels are good at a bounded
choice between written options and are not the person's taste.
