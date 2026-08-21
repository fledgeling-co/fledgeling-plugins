# The payload

`render_digest.py` takes one JSON object. Run `--example` to print a working one.

## Top level

| Key | Required | Notes |
|---|---|---|
| `subject` | yes | Names a specific capability. A bare count fails the gate. Must vary per issue, because Gmail threads same-subject messages and clips on their combined size. |
| `preheader` | yes | A fallback rather than a controlled surface: Apple Intelligence generates the inbox preview from the HTML on the majority of opens. Make the opening body text carry the meaning. |
| `heading` | yes | The `h1`. One per email. |
| `lang` | no | Defaults to `en`. Emitted on `<html>`, without which a screen reader uses its own default language. |
| `brand` | yes | `wordmark`, `siteUrl`, `logoUrl` (PNG — Gmail strips SVG), optional `palette`, optional `fonts`. The wordmark splits on a middle dot: the part before it renders in the display face, the part after in mono caps, matching how a site header is usually built. `fonts` takes `sans` / `serif` / `mono` stacks and a `link` href; every stack must end web-safe, because Gmail ignores the link and Outlook falls back to Times New Roman rather than to the next name in the list. |
| `issue` | yes | `webUrl`, `preferencesUrl`, `unsubscribeUrl`. All absolute. |
| `summary` | no | `counts` string and up to three `highlights`. A highlight is either `{text, url}` or `{parts: [{text}, {text, url}, ...]}`, the second form so one line can name the work in plain text and link each destination separately. Links point outward, never at an anchor. |
| `items` | yes | See below. No cap. |
| `featured` | no | How many auto-assign to the featured tier. Default 2, gate allows 2-4. |
| `spotlight` | no | How many auto-assign to the spotlight row. Default 3, gate warns outside 2-5. Three is the count the row is built around; more than three columns at 600px leaves each one too narrow to carry a banner. |

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
| `headline` | featured, spotlight | The claim. In the featured tier this becomes the `h2`; in the spotlight row it is the one line under the title, clipped at 110 characters. |
| `body` | featured | 25-55 words. What changed, why it matters. |
| `install` | featured | Either a string, set as a monospace command block above the actions, or `{label, url}`, set as the subordinate action beside the primary button. Prefer the link where a route exists: a shell line asks the reader to copy it into the right window, and a phone cannot act on it at all. |
| `bannerUrl` | featured | Optional. Email-sized, not the source asset: about 1072px for a 536px column at 2x. Only the featured tier is wide enough for a banner to mean anything. |
| `iconUrl` | spotlight, one-line | Decorative, rendered with `alt=""`. About 224px for the spotlight row (shown at 112) and 48px for a tail row (shown at 24). Pointing a tail of eighteen rows at 256px card icons costs the recipient most of a megabyte. |
| `oneline` | one-line | A short tag after the title. |
| `group` | one-line | Category heading to group under. Defaults to "More". |
| `tier` | all | Explicit override: `featured`, `spotlight` or `oneline`. |

## On choosing the featured items

Auto-assignment falls to position, which is a weak proxy for relevance. The
causal evidence behind featuring is conditional on the featured item mattering
to that reader, so pass an explicit `tier` whenever the source knows something
position does not — engagement history, category subscription, an editor's pick.
When you do, say in the run report what the ranking was, because the next person
to read the issue will assume recency.
