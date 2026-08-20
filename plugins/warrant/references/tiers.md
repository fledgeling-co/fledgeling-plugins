# Tiers — the authority ladder

Read this before proposing a tier change. It carries the entry and exit criteria, why entry is worded
as absence of escapes rather than as a measured rate, and why tier 4 is in the table at all.

## The ladder

Authority is held per defect class, never globally.

| Tier | The machine may close | Entry | Automatic exit |
|---|---|---|---|
| 0 | nothing; it advises and records | a valid signed warrant, and a ledger that is writing | — |
| 1 | classes where the oracle plane is green and no perceptual judgement is required | oracle coverage at or above the warrant's `[oracle] coverage_min` for the surface | any lineage gap |
| 2 | tier 1 plus perceptual classes carrying a declared miss ceiling | assay green, and the grader re-catches every historical escape in this class | a pinned model version change, or any new escape in the class |
| 3 | tier 2 across all non-disclosure surfaces | `tiers.tier3_items_closed_min` closed in the class with zero escapes over `tiers.tier3_window_days` (the older spelling `tier3_items` is still read) | one escape in a tier-3 class |
| 4 | tier 3 plus disclosure content | unreachable on current evidence | — |

`warrant:ratchet` computes the tier each class has earned and applies exits immediately.
Promotions are written as proposals for a person to sign in `warrant:charter`.

## The default that carries the safety property

**A class the warrant does not name sits at tier 0.** `_state.tier_of()` returns 0 for an unknown
class rather than inheriting the warrant's highest tier, which means a defect class nobody wrote down
is a class no machine may close.

That is the single most important line of code in the plugin, and it is one line. The opposite default
— unknown classes inherit the surface's tier — would mean every novel defect type arrives
pre-authorised.

## Why entry is absence of escapes, not a measured rate

This is the plugin's weakest link, stated plainly so nobody mistakes a clean run for a measurement.

The defensible entry condition would be a measured sensitivity per defect class, from a powered
non-inferiority reader study. No such study has ever been run on code review or UI acceptance (`C1`),
and building one requires a labelled case set and human reader time — which inverts the plugin's whole
purpose, spending human review to remove human review. It was designed and cut.

What replaces it is the regression corpus: every escape anyone reports becomes a permanent case, and a
class may hold tier 2 only while the machine still catches all of its historical escapes. That is
genuinely better than a study in one respect — it never goes stale, because it re-measures every model
version against every escape ever found — and worse in three:

- **It is a numerator with no denominator.** You learn about escapes that got noticed.
- **It cannot bound what is still hidden.** Without seeded items there is no estimate of the misses
  nobody found. The corpus proves the pipeline catches known failure modes and says nothing about
  novel ones.
- **It says nothing about false rejections.** An item wrongly failed and never reviewed is invisible;
  `falsealarm_proxy.py` infers candidates from churn and is a proxy.

So absence of escapes gains weight from volume and time, and never becomes a rate. A class at tier 3
with 400 items and no escapes is better evidence than one with 40, and neither is a sensitivity.

## Why tier 4 is in the table

Because its absence would otherwise read as an oversight rather than a decision, and because the next
person to look at this will want to add it.

Disclosure content is the class where the consequence of an escape is highest and the evidence channel
is least trustworthy. Tenant-authored text renders into the very screenshot a vision judge reads, and
image-borne prompt injection defeated four production vision-language models with miss rates of 70%,
57%, 89% and 92% (`C16`). That was oncology imaging; the transfer to a disclosure surface is an
argument rather than a measurement, and nobody has measured this specific channel.

An argument is enough to withhold authority and not enough to grant it. Tier 4 becomes reachable when
someone measures the channel — an injection corpus against the actual lanes on the actual surfaces —
and not before.

## What a tier change needs

**A promotion** needs the evidence that earned it, read by the owner, and a commit authored by the
owner. `ratchet.py` writes the proposal; it does not apply it. Signing a promotion without reading the
evidence leaves the ladder in place and removes the only thing it was measuring.

**A revocation** needs nothing. It has already applied by the time anyone sees it, and re-signing a
revoked class back up without new evidence is the one edit that turns the warrant into a fiction.

**A new tier**, or a change to an entry condition, is a change to this file and to `charter_validate.py`
in the same commit. A tier whose entry condition lives only in prose is a tier the validator cannot
enforce.
