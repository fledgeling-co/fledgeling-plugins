# The oracle order

**Build the numbered requirement list from the ticket before opening anything the
worker wrote.** Description, then every comment oldest to newest, then every attached
image. Only then the completion record, the plan, the diff.

## Why the order is the rule

Read the diff first and it supplies the frame: you check the requirements the diff
happens to address, and the ones it silently dropped never enter the list. The
resulting review is a description of the change rather than a test of it.

This is the same positioning failure as concurrent-read computer-aided detection. When
the machine's marks are shown before the reader's own pass, the reader anchors on them.
Measured across 429,345 mammograms: specificity fell 90.2% → 87.2%, biopsy rate rose
19.7%, AUC fell 0.919 → 0.871, and **detection did not improve**. Second-read and
arbitration — an independent pass first, comparison afterwards — is the design that
worked. A completion record read before the requirement list is the same mistake with
the same shape.

## Comments are where the requirements live

A card's body is its first draft. What the work was actually judged against was
negotiated underneath it — a correction, a narrowed scope, an acceptance criterion
somebody added on the third pass. A triage that reads only the description is judging
against a specification nobody agreed to.

Read them oldest to newest so the negotiation reads forward. The last comment often
records a decision whose reasoning is three comments earlier.

**A comment can also invalidate the card.** Where a comment and the card body
disagree, the comment is later and usually wins — but say which you followed and why,
because sometimes the body is the contract and the comment is one person's opinion.

## Read the images

Attachments are requirements, not decoration. A bug report whose expected behaviour is
a screenshot cannot be triaged from its text, and a card that says "the spacing is
wrong" is unanswerable without the picture that shows which spacing.

Three things images carry that the text usually does not: the actual rendered state at
the moment of the report, the surrounding surface that locates the defect, and — in
screenshots of errors — the verbatim string, which is frequently the fastest route to
the producing line.

Where a tracker exposes attachments by URL, fetch and view them. Where an image cannot
be retrieved, say so in the ledger rather than triaging around it: a card whose only
statement of intent is an unreadable attachment is **inconclusive**, not "no
requirements found".

## What the list looks like

Numbered, each item independently checkable, each traceable to where it came from:

```
R1  Widget titles render as a heading element        [body]
R2  ...including the empty state                     [comment 3, 2026-08-17]
R3  Existing headings are not re-levelled            [comment 5 — explicit non-goal]
R4  Spacing matches the attached mock                [image: screenshot-2.png]
```

Non-goals earn a number too. A requirement list without them invites a reviewer to
"fix" something the card deliberately left alone, and that argument is expensive to
have after the fact.
