# Plain words

The pages are read by someone who does not know this codebase. They can follow a real
mechanism happily; they do not know the vocabulary and will not look anything up.

The hardest jargon here is not the technical-looking kind. It is ordinary English words
carrying a private meaning — *gate*, *armed*, *coverage*, *finding*, *wave*, *verdict*.
Nothing about them looks technical, which is why they survive a proofread and why the first
version of these pages shipped with `armed` thirty times and `verdict` thirty-one.

## Use the right-hand column

| Instead of | Write |
|---|---|
| gate | check |
| gate passed, exit 0 | passed |
| verdict | how it went |
| armed | the check was tested — we broke the code on purpose and it noticed |
| armed: false | untested check — nobody has proved this one can fail |
| mutation | the fault we introduced on purpose |
| case reddened | which test caught it |
| red / green counts | tests that failed when broken / tests that pass normally |
| sha, head sha, commit sha | version (seven characters) |
| worktree | workspace |
| worktree clean | no unsaved changes |
| commits ahead | changes not yet shared |
| pushed | shared with the team |
| denominator | out of how many |
| coverage | how much of the work is watched by tests |
| unmeasured | nobody checked this |
| finding, defect | problem found |
| severity high / medium / low | serious / worth fixing / minor |
| deliberately not done, waived | left undone on purpose |
| what would unblock it | what it is waiting for |
| remaining | still to do |
| in-flight | being worked on now |
| needs-work | tried, did not pass |
| blocked | stuck, waiting on something |
| item, work item | task |
| run label, wave | round |
| correction, retraction | what we got wrong |
| earlier claim | what we said |
| true state | what was actually true |
| mechanism | why we got it wrong |
| caught by | how we found out |
| artifacts | files to open |
| roadmap / upcoming waves | what is coming next |
| estimate / duration | estimated time (always a range, never a single point) |
| task size tier (S/M/L/XL) | size: small (3–25m), medium (7–56m), large (14–68m), very large (25–155m) |
| basis | how we sized it (measured past runs) |

Keep an id such as `WEB-5089` as it is — it is a name, and the reader can carry it to a
tracker. Label its column *task*.

Three terms have no plain equivalent and stay, defined once on the page where they first
appear: **round**, **version** and **branch**. The templates carry those definitions; you do
not need to write them.

## How much to write per field

Every string below is prose a stranger reads. One clause each. The layout clips anything
longer without saying so, which is worse than cutting it deliberately.

| field | budget | holds |
|---|---|---|
| `verdict.headline` | ~90 chars | the one thing that matters about this round |
| `tasks[].title` | ~50 chars | what the task was |
| `gates[].name` | ~30 chars | what the check looks at, in plain words |
| `armed[].mutation` | ~60 chars | what we broke, so a reader can picture it |
| `findings[].claim` | ~70 chars | what is wrong, stated as a fact |
| `corrections[].*` | ~80 chars each | the four atoms, one clause each |
| `not_done[].reason` | ~50 chars | why it was left |
| `needs_you[].one_line` | ~70 chars | what it blocks |

Meet the budget by making fewer claims, never by compressing until the sentence turns into a
slogan. "Verified is a different axis" is what compression produces, and it explains nothing
to the person this page is for. Plain language costs more words than a slogan and is worth
them.

## One idea worth stating plainly

The alarms zone is the most valuable thing on the project page and the least
self-explanatory. Its framing, which the template carries, is worth knowing so your data
matches it:

> A check that has never failed might be watching carefully, or might be broken and
> silently passing everything. The only way to tell them apart is to break the code on
> purpose and see whether the check notices.

So `armed[].mutation` should describe the break in terms a reader can picture — *"lowered
the contrast limit to 1 to 1"*, not *"inverted the WCAG threshold assertion"*. And a check
where breaking the code produced zero failures renders as the loudest state on the page
after an outright failure, because an alarm with a flat battery is worse than no alarm: it
is a reassurance nobody has earned.
