# EVALS   email-digest

## No benchmark run, and why

**The A/B panel described in `create-skill`'s pipeline was not run for this
skill.** No no-skill baseline was generated, no blind judges were spawned, and
no comparative numbers exist. This section exists so that absence is a recorded
fact rather than something a later reader infers from a missing heading.

The reason is scope: this skill was commissioned as one half of a session that
also ran a five-backend research panel and published a report, and a benchmark
would have been a third project. It is a real gap, not a considered exclusion,
and the tasks that would close it are named at the bottom.

What *was* verified is mechanical, and it is listed below with the evidence,
because a gate demonstrated failing on a bad fixture is worth more than a score
nobody can reproduce.

## What was verified

### The gate fires on a bad email

A deliberately bad fixture (flat list, prose intro, anchor links, inline SVG,
unmarked layout tables, `display:flex`, pure `#FFFFFF`/`#000000`, missing alt,
generic link text, no unsubscribe, a count-only subject) was run through
`lint_email.py`.

**Result: 13 errors, 3 warnings, exit 1.** Every rule class fired.

### The gate passes a good email

A 24-item payload built from real marketplace skills was rendered by
`render_digest.py` and gated.

**Result: 0 errors, 0 warnings, exit 0, 24.7KB of HTML** against a 90KB budget
and Gmail's ~102KB clip.

### The gate caught four real defects during development

This is the part worth reading, because each one is a defect that would have
shipped and each was found by the tooling rather than by inspection:

| Defect | How it presented | Caught by |
|---|---|---|
| The renderer emitted no tier markers | Every tier rule and the prose-intro rule silently measured nothing while still printing a verdict | `tiers` gate reporting zero items on a 24-item email |
| The whole email was centre-aligned | Nobody wrote `text-align:center` once. The outer `align="center"` that centres the card cascaded into every descendant | Opening the render and looking at it. The gate did **not** catch this, and `a11y:alignment` was added afterwards so it would |
| Featured banners were links with no accessible name | Their only content was an `alt=""` image, so a screen reader announced a link with nothing in it | `a11y:link-empty` |
| Two linter rules over-matched | `text-transform` matched the `transform:` rule, and the font-family capture stopped at the first quote, so every system stack read as ending non-web-safe | 59 false failures on a clean template |

The third and fourth rows are the honest ones. A gate that has never produced a
false positive has probably never been run on anything real, and the alignment
row is a case where the deterministic check was added because looking caught
what it missed.

### The asset pipeline works on real inputs

`email_assets.py` was run against a real 3200x1040 banner (663KB), a real 256px
icon, and the Fledgeling SVG mark:

```
banner-1072.png     1072x348   121.9 KB
code-review-56.png  56x56        4.5 KB
fledgeling-icon-56.png 56x56     3.1 KB
```

The SVG path matters because Gmail strips `<svg>` from the DOM entirely, so a
vector mark has to be rasterised before it can appear in mail at all.

## What would settle the open question

Three tasks, in order of what they would tell you:

1. **Tiered against flat, in a real programme.** Same items, same subject, same
   send time, split by subscriber. Measure bot-filtered unique clicks per
   delivered email and per-tier click penetration. This is the load-bearing
   unmeasured claim in the whole skill, no published study answers it, and one
   issue would resolve it for a given audience. Do not measure opens: Apple's
   Mail Privacy Protection broke them in 2021 and took click-to-open with them.

2. **The summary block, instrumented as its own link set.** Distinct tracking
   parameters on the three highlights. If index links take meaningful share
   while the items below retain theirs, the block amplifies; if index clicks
   cannibalise, it satisfies. Nobody has published an answer either way.

3. **The no-skill baseline.** Give an agent the same payload and the same
   instruction without this skill loaded, and judge both outputs blind against
   the gate's own sixteen checks. That is the comparison that says whether the
   skill earns its context window, and it is the one this file cannot currently
   answer.

## A gap that should not have needed asking about

**Version 1.0.0 shipped without routing to `ux-craft` or `design-craft`, and it
should have.** The user asked whether it did, which is how it was found.

Three things made it a miss rather than a judgement call. `ux-craft`'s own
description names emails among the surfaces it covers. `create-skill`'s
operating rules say plainly: route, do not reimplement. And the same pairing was
applied correctly to the research page published in the same session, so the
rule was in front of the author and went unapplied here.

The concrete cost was measurable rather than theoretical. Run against this
skill's own 24-item fixture, `ux-lint.py` reported:

```
2 failures, 1 warnings
  focus-suppressed     d24.html:43
  no-focus-visible     d24.html:39
  state-coverage       (warn)
```

The first was **a real defect this skill's own gate missed**: an `outline:none`
left on the featured banner after that element stopped being a link. Dead CSS,
found by the skill that should have been in the loop from the start. Fixed in
1.1.0.

The other two do not transfer to email, and 1.1.0 records why rather than
suppressing them: Gmail's published CSS allowlist has no pseudo-class support,
so a `:focus-visible` treatment cannot render in the medium at all, and an email
has no states to cover.

1.1.0 also removes contrast and touch-target checks from this skill's remit
entirely. Both have primary sources in `evidence.md` and both are already gated
properly by `ux-lint.py`; implementing them twice would only produce two gates
disagreeing about one standard.

## Decisions taken without the user

Two forks were put to the user directly and answered: the skill is a general
digest builder rather than a fledgeling-specific one, and the icon is the
three-unequal-bars direction.

Two further forks were decided without asking, and are recorded here because
they turn on judgement rather than evidence:

- **Featured items auto-assign by position** when the caller gives no explicit
  tier. Position is a weak proxy for relevance, and the causal evidence behind
  featuring is conditional on relevance, so this is the weakest link between the
  research and the implementation. The payload accepts an explicit `tier` for
  exactly this reason.
- **Subject length warns rather than fails.** Three large datasets give three
  different optima and an academic study across 455 million users found no
  relation at all. Making it a hard gate would encode a disagreement as a fact.
