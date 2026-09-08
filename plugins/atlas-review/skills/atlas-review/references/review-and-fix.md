# Stages 1 and 2: review, then fix

## The split, and why it exists

`code-review:code-review` is read-only. It finds and verifies; it applies nothing. That is
deliberate, and it means the fixing is yours. A review whose findings nobody acts on is a
document, not a gate.

Run it per PR rather than over the whole stack. A stack is usually ordered, and a finding
on PR 3 often disappears when PR 7 rewrites the file.

## Verify before you act

Raw LLM review runs at **40 to 70% false positives**, and **cross-model verification cuts
errors by up to half** (`docs/deep-research/`). So a finding that would change production
code earns a second reading from a different model family first.

This is not theoretical here. In one session an out-of-family lane refuted a finding its
author was confident in, and was right; in another the author was right and the lane was
wrong, and the deciding evidence was a measurement neither had taken. Treat disagreement as
the interesting result and go and measure.

The cheapest lane is a gateway call rather than a paid CLI. `clarify:clarify` carries the
commands and the rule that a lane which returns an answer about a different subject is a
lane failure, not a verdict. That has happened on two different lanes.

## What to fix, and what to leave

Fix what is wrong. Leave what is a preference, and say so in the comment.

Three shapes recur and all three are worth fixing:

- **A check that cannot fail.** See `void-checks.md`. This is the highest-value class.
- **A control with no test anchor**, or an anchor that matches the wrong element. A selector
  matching nothing fails loudly; one matching the wrong thing does not.
- **A record that disagrees with its twin.** Two files describing the same fact drift, and
  only a merged tree shows it.

Leave the product owner's copy alone unless it is wrong. Renaming a tab is not licence to
rename the thing the tab contains.

## Commenting

Write the comment through `create-luke-content:create-luke-content`, `review` format, and
run its `voice_lint.py` before posting. The reader may be the non-technical product owner,
so lead with what it means rather than the mechanism.

State what you changed, what you left and why, and anything you found that is worth a
decision rather than a fix. A comment that only lists what was wrong is worth less than one
that says which of it mattered.
