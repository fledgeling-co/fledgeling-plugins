# Portals

Where the invoice is not in the mail and not on disk, it is behind a login. This is the stage that most often
stalls, and the two ways it stalls are different problems.

## Route to `proctor`, not to a headless browser

`proctor` drives the operator's **own running, signed-in browser** through the macOS accessibility tree. Every
other option drives a separate browser with its own cookie jar, which means its own signed-out session.

Measured on a real run: `agent-browser` with `--profile "Profile 1"` — the operator's actual Chrome profile — still
presented a signed-out page, because it runs its own Chrome from a profile copy. And Obscura has its own cookie jar
by design.

More decisive: **Cloudflare blocks the automation outright** on several supplier portals, and the operator's real
browser is the only thing that gets through. Two measured on one run:

```
claude.ai/settings/billing  →  "Performing security verification"  (persists after 15s and a profile restart)
console.x.ai                →  "Attention Required! | Cloudflare — Sorry, you have been blocked"
```

This is a **hard boundary**, not an automation failure to retry. When a portal blocks, stop and hand off.

## Driving the real browser

Navigate by URL, never by clicking. A click reports success unconditionally; a URL navigation can be verified by
re-reading the URL.

```bash
osascript -e 'tell application "Google Chrome" to set URL of active tab of window 1 to "<url>"'
osascript -e 'tell application "Google Chrome" to return URL of active tab of window 1'
```

Locate a tab by URL substring rather than by index; indices drift as tabs open, and Chrome's AppleScript window
ordering does not correspond to proctor's window handles.

Known proctor behaviours worth carrying:

- **`proctor_capture` normalises the image** (`maxLongEdge 1024`) and invoice text is unreadable at that size. Use
  `proctor_zoom` with a region, which emits at `scale: 2` — reading pixel coordinates off a zoom and clicking them
  directly is a 2× error.
- **Synthetic events can be blocked entirely.** `proctor_doctor` reports `Secure Event Input is active`, and when
  it does, clicks and keystrokes cannot be delivered. Check `proctor_doctor.blockers` rather than probing the
  IORegistry.
- **A returned node is not necessarily pressable** — `AXPress is not offered by this element` is common on web
  content.
- Window handles die on agent restart and renumber; re-attach and re-read them.

## The download is proven by the filesystem, never by the click

```bash
cd "$VOUCH_DOWNLOADS" && ls -1t *.pdf | head -5 | while read f; do
  printf '%s  %s\n' "$(stat -f '%Sm' -t '%H:%M' "$f")" "$f"
done
```

A click that "succeeded" and produced no file is the single most common portal failure.

## Emailed invoice links expire

Hosted-invoice links in a receipt email are not a durable source. Measured:

- `curl -sL '<stripe>/pdf?s=em'` exits **0** and writes 745 bytes of HTML. A `.pdf` extension and a zero exit code
  prove nothing; check the size and the magic bytes.
- Following the link in a real browser resolves to a page reading **"This link expired. To get sent a fresh link,
  enter the email address that the invoice was originally sent to."**

So: fetch from the portal's billing history, not from the email's link, whenever the charge is more than a few
weeks old.

## When it will not work: the wanted-invoices hand-off

`scripts/wanted_invoices.py` writes a single HTML page the operator can work through in one sitting. Per
outstanding charge:

| Column | Why it is there |
|---|---|
| **Charge date** | What to search the portal's billing history for |
| **Supplier** | — |
| **Amount as charged** | The local-currency figure from the feed or statement |
| **Estimated original amount** | Back-derived from the implied FX band, marked as an estimate |
| **Account address** | The address the invoice is expected to name, so the operator knows which login |
| **Portal link** | Deep link to the billing-history page, not the vendor's home page |
| **What is needed** | "Download the invoice PDF", or "open the email so Mail fetches the attachment" |

Two hand-off kinds, and they read differently:

- **Portal blocked** → the operator signs in and downloads. Give the deep link.
- **Mail attachment never downloaded** → the operator opens the message in Mail and the bytes arrive. Give the
  subject line and date, not a link.

Sort by amount descending so the operator's first five minutes recover the most value.

## Verified portal URL shapes

Deep links to billing history, which is what you want rather than a dashboard root:

```
github.com/organizations/<org>/settings/billing
admin.google.com/ac/billing/history
linear.app/<workspace>/settings/billing
app.axiom.co/<slug>/settings/billing
console.supermemory.ai/settings/billing
elevenlabs.io/app/settings/billing
cloud.redis.io/#/billing-history
sentry.io/settings/billing/receipts/
login.tailscale.com/admin/settings/billing
slack.com/admin/billing/invoices
portal.azure.com/#view/Microsoft_Azure_GTM/ModernBillingMenuBlade/~/Invoices
fly.io/dashboard/personal/billing/invoices/<id>.pdf
```

Measured broken even when signed in: `github.com/…/settings/billing/history` (404),
`pay.google.com/gp/w/home/transactions` (404), `claude.ai/settings/billing` (redirects into a fragment route).

Keep this list in the operator's own config rather than here once it drifts; a portal URL is a fact with a short
half-life.
