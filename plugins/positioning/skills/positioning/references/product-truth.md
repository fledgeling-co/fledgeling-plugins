# Product truth — the table every claim has to land on

Positioning fails in two directions. It can be unsupported by the market, which
is what research is for. It can also be unsupported by the product, which
research cannot catch at all, because a deep-research panel reads the web and
the web does not know what shipped last Tuesday.

The predecessor skill handled this in prose: *"never claim a capability the
product doesn't have; mark designed-but-unbuilt work as such."* Good rule,
unenforceable. A model writing a hero line four thousand tokens later has every
incentive to reach for the most compelling capability in scope, and nothing
downstream reads that instruction again.

So the rule becomes a table with ids, and a hero line that does not name a
`shipped` row does not pass `claim_ledger.py check`.

## Build it before the research lands

The panels run for the better part of an hour. This is what to do with that
time, and it is not filler: it is the half of the evidence that no amount of
research money can buy.

**Read the product, not the pitch.** In order of authority:

1. **The running code.** Routes, feature flags, migrations, the CLI's `--help`,
   the API's OpenAPI document, what the tests actually assert. A capability with
   a passing end-to-end test is `shipped`.
2. **The shipped surface.** The live site, the App Store listing, the changelog,
   the release notes. What a customer can buy today.
3. **The plans.** `docs/plans/`, `docs/specs/`, the PRD, the backlog, the design
   mocks. These are `designed` — real, decided, not yet true.
4. **The founder's ambition.** The deck, the vision doc, the conversation you
   are having. `aspirational`, and it is not a lesser category — it is where the
   expansion story lives. It just may not appear in a headline.

**Where the three statuses actually go:**

| Status | May appear in | May not appear in |
|---|---|---|
| `shipped` | anything, including the hero line and the proof point | — |
| `designed` | the roadmap section, the expansion story, "where this goes" | hero, headline, one-liners, unique attributes, value proof |
| `aspirational` | the vision paragraph, the internal ambition note | anything a prospect reads as a present-tense promise |

The gate enforces exactly that split, through the `PROMISSORY_MOVES` set in
`claim_ledger.py`.

## Record it

```bash
python3 scripts/claim_ledger.py init docs/positioning/work --product "Acme"
python3 scripts/claim_ledger.py add-truth docs/positioning/work \
  --id T-011 --status shipped \
  --capability "Per-tenant audit export, CSV and JSON, self-serve" \
  --evidence "apps/api/src/audit/export.controller.ts + e2e/audit-export.spec.ts"
```

`--evidence` is a path, a URL or a test name. It is the thing someone would open
to disagree with you. A truth row with no evidence is a claim about the product
wearing a ledger row's clothes.

## Two failure modes worth naming

**The demo-ware promotion.** A capability that works in a demo, behind a flag,
for one customer, becomes `shipped` in the writer's head because it has been
seen working. The test is not "does it work" but "can a customer buy it and use
it today without you in the room". If the honest answer is no, it is `designed`.

**The category error.** "We're an AI-native platform" is not a capability and
does not belong in this table. Truth rows are things the product does, stated so
that a specific artifact proves or disproves them. Frames, adjectives and
category claims are positioning moves, and they get bound to the rows that make
them true rather than being recorded as rows themselves.

## The line this table lets you draw

The most useful output of this exercise is usually not the hero line. It is the
sentence you can say to a founder: *"Territory B is the strongest on the
evidence, and eleven of its fourteen moves rest on shipped capability. The other
three rest on T-042, T-043 and T-051, which are designed and not built. Ship
those three and B is fully claimable; until then, B's hero line has to be the
one bound to T-011."*

That sentence is a roadmap derived from a positioning decision, and it falls out
of the ledger for free. The predecessor could not produce it, because it had no
table to count.
