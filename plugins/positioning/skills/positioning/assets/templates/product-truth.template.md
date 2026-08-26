# {{PRODUCT}} — Product truth

Rendered from `ledger.json`. What the product does, and whether a customer can
buy it today.

**Shipped:** {{N_SHIPPED}} · **Designed:** {{N_DESIGNED}} · **Aspirational:** {{N_ASPIRATIONAL}}

| id | Capability | Status | Evidence |
|---|---|---|---|
| {{TRUTH_ROWS}} | | | |

`--evidence` is the artifact someone would open to disagree: a path, a URL, a
test name. A row with none is a claim about the product wearing a ledger row's
clothes.

## Claimability by territory

| Territory | Moves | On shipped | On designed | Fully claimable? |
|---|---|---|---|---|
| {{CLAIMABILITY_ROWS}} | | | | |

## The roadmap this implies

{{ROADMAP}}

Where a strong territory rests on designed-but-unbuilt rows, shipping those rows
is a positioning decision expressed as engineering work. Name them, in order,
with what each unlocks.

## Promissory-copy rule

Hero lines, headlines, one-liners, unique attributes and value proof may rest
only on `shipped` rows. `claim_ledger.py check` enforces it; this table is where
you look when it fails.
