# Running with no campaign

The skill works against a brief queue alone. `--campaign` is optional and
`reckon.py` records `campaign_present: false` in the ledger when it is absent.

What changes is not the mechanics but what the output is entitled to claim,
and the difference is large enough that a report which looks the same either
way is misleading.

## What survives

- Every brief still gets a row and a class.
- The partition is still total, and the conservation gate still holds.
- Waivers declared in brief frontmatter still resolve to `waived` with their
  reasons.
- Duplicate and malformed briefs are still caught.

## What collapses

Almost everything that made the reckoning worth running:

- **Every brief lands in `unbuilt` or `waived`.** There is no evidence to
  disagree with the documents, so nothing can be `broken`, `retirable` or
  `undecided`.
- **`unnamed` is empty by construction.** Finding a surface nobody specified
  requires something that went and looked.
- **`unmeasured` is empty, and that is the dangerous one.** With no campaign,
  nothing has been measured *at all* — so the class that should hold
  everything holds nothing, purely because there is no registry to read it
  from. An empty `unmeasured` column here means the opposite of what it means
  in a full run.
- **The denominators are undefined,** not 100%. There is no case population
  and no requirement grading.

So the honest summary of a campaign-less run is: *this is a list of what the
project said it would do, sorted and de-duplicated. It contains no information
about what works.*

## What the report must say

Lead with the absence, in the first line, before any count:

> No verification evidence was available for this reckoning. What follows is
> the stated intent only — 47 briefs, none of which has been checked against
> the built product. Nothing here should be read as a claim about what works.

Then omit the denominator table entirely rather than printing empty or 100%
figures. A blank table invites a reader to fill it in with an assumption; an
absent one with a sentence saying why does not.

The `unmeasured` class is worth calling out by name, because a reader who
knows this skill will look for it: say that it is empty because there was no
campaign to read, not because everything has been measured.

## What to do instead

A campaign-less reckoning is a signal, not a deliverable. Two useful moves:

**Run a campaign first.** `test-campaign` produces exactly the registry this
skill reads, and the pair is the intended workflow: campaign establishes what
is true, reckon works out what that leaves. Say so in the report and offer it.

**Or scope down to what documents can answer.** Without evidence, a brief
queue can still be de-duplicated, sorted by declared status, checked for
briefs that contradict each other, and read for waivers whose stated reason
has expired. That is real work and it is honest, as long as it is not
presented as a completeness assessment.

Where somebody wants a genuine standing survey and has no campaign,
`product-gap-analysis` is the right skill — it goes and reads the code and the
git history rather than reconciling two documents, which is the only way to
say anything about done-ness without a verification run.
