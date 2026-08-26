# Feature brief: Overnight Question Digest

**Product:** Diolog (investor-relations workspace for ASX-listed companies)
**Audience for the copy:** IR managers and company secretaries at ASX-listed companies. They run continuous disclosure day to day; they do not need it explained.
**Shipping:** 3 September 2026, all plans.

## What it does

Retail investors post questions to a company's Diolog feed at all hours. The
Overnight Question Digest collects everything asked since the previous send,
groups it by topic, and emails the IR contact a single summary each morning.

## Mechanics (exact, from the build)

- Sends at **07:00 in the company's listing timezone**, Monday to Friday. No weekend send.
- Includes only questions asked **since the previous digest**, so nothing repeats.
- Topic grouping uses the same taxonomy as the existing feed filters: 14 topics.
- The digest surfaces the **top 3 topics by question volume** at the top, then the rest in a plain list.
- Configurable at **Settings > Notifications > Digest**: send time, weekday selection, or off entirely.
- Questions flagged **price-sensitive** by the existing classifier are held out of the digest body and listed separately under a "Needs a human read" heading, with no AI summary attached.

## Measured in the beta

- 11 companies ran it for 6 weeks.
- Median time from question asked to first response fell from **31 hours to 9 hours**.
- 2 of the 11 turned the weekday selection down to three days a week.

## Known rough edges (do not hide these)

- Topic grouping misfiles roughly **1 in 12** questions in the beta sample. The
  digest shows the original question text, so a misfile is visible rather than silent.
- There is no per-user digest yet. One address per company.
- The price-sensitive classifier is tuned to over-flag. IR teams in the beta
  reported it holding back questions that were fine.

## What it is not

Not an answer generator. It never drafts a reply, and it never posts anything to
the feed. Every response is still written and published by a human.

## Quote available for use

Nothing on the record yet. No customer has agreed to be named.
