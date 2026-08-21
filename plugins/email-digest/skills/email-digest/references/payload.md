# The payload

`render_digest.py` takes one JSON object. Run `--example` to print a working one.

## Top level

| Key | Required | Notes |
|---|---|---|
| `subject` | yes | Names a specific capability. A bare count fails the gate. Must vary per issue, because Gmail threads same-subject messages and clips on their combined size. |
| `preheader` | yes | A fallback rather than a controlled surface: Apple Intelligence generates the inbox preview from the HTML on the majority of opens. Make the opening body text carry the meaning. |
| `heading` | yes | The `h1`. One per email. |
| `lang` | no | Defaults to `en`. Emitted on `<html>`, without which a screen reader uses its own default language. |
| `brand` | yes | `wordmark`, `siteUrl`, `logoUrl` (PNG — Gmail strips SVG), optional `palette`. |
| `issue` | yes | `webUrl`, `preferencesUrl`, `unsubscribeUrl`. All absolute. |
| `summary` | no | `counts` string and up to three `highlights`, each `{text, url}`. Links point outward, never at an anchor. |
| `items` | yes | See below. No cap. |
| `featured` | no | How many auto-assign to the featured tier. Default 3, gate allows 2-4. |
| `compact` | no | How many auto-assign to compact. Default 8, gate warns outside 5-9. |

## Palette

Overrides `DEFAULT_PALETTE`: `paper`, `surface`, `ink`, `muted`, `hairline`,
`accent`, `codebg`. Flatten design tokens to literals — Gmail supports `var()`
but not the custom-property declaration, so every `var()` resolves to its
fallback.

Two colour constraints worth checking before you pass a palette in. Avoid pure
`#FFFFFF` and `#000000`, which Outlook.com's inversion targets specifically. And
verify the accent against its background at 4.5:1 rather than assuming: a brand
accent tuned for large display type routinely fails as button text.

## Per item

| Key | Tier | Notes |
|---|---|---|
| `title` | all | The name. Also the link text in the one-line tier. |
| `url` | all | Absolute. |
| `headline` | featured, compact | The claim. In the featured tier this becomes the `h2`. |
| `body` | featured | 25-55 words. What changed, why it matters. |
| `install` | featured | Optional command line, set in monospace. |
| `bannerUrl` | featured | Optional. Email-sized (about 1072px wide for a 536px column at 2x), not the source asset. |
| `iconUrl` | compact | Decorative, rendered with `alt=""`. |
| `oneline` | one-line | A short tag after the title. |
| `group` | one-line | Category heading to group under. Defaults to "More". |
| `tier` | all | Explicit override: `featured`, `compact` or `oneline`. |

## On choosing the featured items

Auto-assignment falls to position, which is a weak proxy for relevance. The
causal evidence behind featuring is conditional on the featured item mattering
to that reader, so pass an explicit `tier` whenever the source knows something
position does not — engagement history, category subscription, an editor's pick.
When you do, say in the run report what the ranking was, because the next person
to read the issue will assume recency.
