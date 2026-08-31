# Diversity Ledger: Keep Variety Across Sessions

The session ledger catches repetition only until the terminal closes. This project-local ledger carries the last five decisions across sessions without creating user-level state or sending design history anywhere.

Use the ledger for three kinds of work:

- `visual` — greenfield Persuade or Experience commissions in `design-craft:design-craft`.
- `mac-content` — content-area directions in `mac-craft:mac-craft`; native chrome is never rotated.
- `flow` — open journey shapes in `ux-craft:ux-craft`.

Operate and Read surfaces that match an incumbent system are recorded as `n/a` rather than forced into rotation. An explicit user request, a brand system, and a platform convention override the ledger. Rotation is a guard against model gravity, not a reason to violate product truth.

## Location and schema

Default path:

```text
<project>/.design-craft/diversity-ledger.json
```

The file is JSON so a later run can read it without parsing prose. It retains five entries. Each entry has:

```json
{
  "date": "2026-08-31",
  "kind": "visual",
  "artifact": "harbour-map-landing.html",
  "family": "industrial-utilitarian",
  "display_face": "DIN Condensed",
  "pairing": "condensed grotesk + humanist sans",
  "topology": "index-led split with a live map",
  "signature": "route diagram as the hero",
  "palette_family": "cobalt-neutral",
  "motion": "one pinned route reveal",
  "note": "user asked for a maritime reference"
}
```

`family`, `display_face`, `pairing`, `topology`, `signature`, `palette_family`, and `motion` are rotation axes. `flow_shape` is used by `kind: flow`; the other axes are optional. Record the actual decision, not the candidate you declined.

## Commands

Run from the `design-craft` skill directory, or use the absolute script path:

```bash
python3 scripts/diversity_ledger.py init <project>/.design-craft/diversity-ledger.json
python3 scripts/diversity_ledger.py show <project>/.design-craft/diversity-ledger.json
python3 scripts/diversity_ledger.py check <project>/.design-craft/diversity-ledger.json \
  --kind visual --family editorial-literary --topology centred-hero
python3 scripts/diversity_ledger.py record <project>/.design-craft/diversity-ledger.json \
  --kind visual --artifact harbour-map-landing.html \
  --family industrial-utilitarian --display-face "DIN Condensed" \
  --topology "index-led split with a live map" \
  --signature "route diagram as the hero" \
  --palette-family cobalt-neutral --motion "one pinned route reveal"
```

`check` exits 0 when the history is absent or the proposed values are available, and exits 1 when a proposed axis repeats a retained entry. An absent history is not a failure: initialise it, make the decision, and record the result after the first viewport is settled. The script creates parent directories and never deletes an existing ledger.

## Procedure

1. Read the ledger before choosing a family. If it is absent, initialise it.
2. Run `check` with the family, topology, signature, display face, palette family, and motion candidates you are considering.
3. Prefer a candidate with no conflicts. If product truth forces a conflict, keep the truthful choice and put the reason in `note`.
4. After the direction contract is settled, record the chosen values. Do not record a rejected candidate.
5. In the delivery, report the retained history count and any deliberate override. A missing ledger, a skipped check, and a deliberate conflict are three different states.

The ledger does not decide taste. It makes repetition visible early enough to change it.
