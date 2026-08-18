# Email UX — Marketing & Transactional

Email is a hostile rendering environment read in a two-second triage pass. Everything web UX says about scanning, hierarchy, and one-primary-action applies *harder* here — plus constraints no web page has. This file owns email structure, copy, rendering constraints, and compliance. (Figma campaign graphics → `email-mockups`; the sending infrastructure → engineering.)

## The two-second contract

An email gets a triage glance in a crowded inbox, usually on a phone. Design for that order of perception:

1. **Sender name** — the #1 open factor. Consistent, recognizable, human where appropriate ("Amy from Diolog" for relationship emails; "Diolog" for system notifications). Never "noreply" as a display name for anything you want read.
2. **Subject line** — ~30–40 characters survive mobile truncation; front-load the meaning ("Your March investor update is live", not "We're excited to share that…"). Say what's inside, not how you feel about it. For transactional email the subject *is* the notification: "Payment received — invoice #4821", "Your password was changed."
3. **Preheader** — the ~40–90 characters after the subject. Continue the subject, don't repeat it; never let "View this email in your browser" be your preheader. Hidden-preview-text technique: a visually hidden div at the very top of the body.
4. **First viewport** — identity (logo), the message's thesis, and the primary CTA visible without scrolling on mobile.

## Structure

- **Inverted pyramid**: conclusion → supporting detail → action. One email, one job. If it has three jobs, it's three emails (or a digest, which is its own pattern).
- **One primary CTA**, styled as a button, appearing early and (in longer emails) repeated at the end. Secondary links are text links. CTA copy = specific outcome verb: "View the update", "Confirm your email", "Download the report" — never "Click here" (also an accessibility failure: link text must make sense out of context).
- **Scannable body**: short paragraphs (1–3 sentences), meaningful subheads, generous spacing. People scan email even more ruthlessly than web pages.
- **Footer**: physical address (legal), unsubscribe (marketing), the sensible extras (preferences, contact, why-you're-receiving-this). Don't hide the unsubscribe in 9px gray — a findable unsubscribe beats a spam complaint every time, and spam complaints hurt every future email's deliverability.
- **Plain-text alternative** always (multipart/alternative): some readers, some clients, some spam filters require it; write it properly (real line breaks, full URLs), don't autogenerate garbage.

## The rendering reality (why email HTML is different)

Email clients — Outlook desktop (Word rendering engine), Gmail (strips `<style>` in some contexts, clips messages >102KB), Apple Mail, and dozens of others — support wildly different HTML. Rules that follow from this:

- **600–640px max width**, single column, designed mobile-first. Multi-column only if it stacks cleanly.
- **Tables for layout** (with `role="presentation"` so screen readers don't announce grid semantics), **inline CSS** for anything that must survive. No JavaScript (stripped everywhere), no forms (unreliable), no background images as load-bearing content (Outlook).
- **Bulletproof buttons**: the whole button is a padded `<a>` (padding + background-color on the anchor itself), min ~44px tall — an image-as-button fails when images are off.
- **Design for images-off** (still a default in some clients, and Outlook blocks by default): the email must make sense with every image replaced by its alt text. Meaningful alt on every informative image; `alt=""` on decorative ones. Never put the headline or CTA *inside* an image.
- **Dark mode**: clients invert or partially adjust colors unpredictably. Include `<meta name="color-scheme" content="light dark">`, test dark rendering explicitly, avoid pure black/white (they invert worst), and give logos a safe treatment (padding + transparent-safe version).
- **System font stacks or web fonts with solid fallbacks** — Outlook shows Times New Roman when a web font fails and no fallback is declared.
- **Text ≥ 14px (body 16px preferred), line-height ~1.5, contrast ≥ 4.5:1**, `lang` attribute set, single `<h1>`-led heading order — email accessibility is real accessibility.
- Total weight small: heavy emails clip (Gmail 102KB HTML) and clipped emails hide your footer — including the unsubscribe link, which is a compliance problem, not just a design one.

## Marketing email

The register is persuasion, so the ethics gate applies at full strength: real deadlines only, real scarcity only, social proof that's true and verifiable. For a regulated audience (Diolog: listed companies, investors), sincerity isn't just ethics — misleading urgency in investor-facing comms is a compliance exposure.

- **Value before ask.** The reader's question is "what's in this for me, in 5 seconds?" Lead with the reader's outcome, not company news phrasing ("See which investors read your update" beats "We've launched analytics").
- **Claims pass the falsifiability test**: honest urgency/scarcity/social-proof claims are falsifiable (the reader could catch a lie), specific (a verifiable referent — a date, a named cohort, a real count), and checkable. "Registration closes Friday 6 June" qualifies; "Spots filling fast!" doesn't.
- **The email is one artifact in a field.** B2B recipients experience your email + the deck it links to + the proposal + the portal as a single composite impression — one unstyled or off-brand artifact undercuts the rest. And the recipient is often a *relay* (an IR officer forwarding to a board, a champion pitching a committee): give them quotable, forwardable lines and an asset they can paste into their own internal case, not just a personal conversion push.
- **Segmented tone via the tone matrix** (ux-writing.md): a product-update to customers ≠ a nurture email to prospects ≠ an investor communication. Same voice, calibrated tone.
- **Lifecycle fit (the honest Hook)**: emails are external triggers; each should connect to genuine value the recipient signed up for, at a moment tied to *their* behavior (kairos — the right moment beats better copy). Re-engagement emails get one honest attempt, then respect the silence — emailing disengaged users trains spam-flagging.
- **Compliance floor**: working unsubscribe honored promptly (one-click — RFC 8058 List-Unsubscribe is now a bulk-sender requirement at Gmail/Yahoo), physical address, truthful subject (CAN-SPAM), and consent-based lists (GDPR/Australian Spam Act: opt-in, not opt-out; no pre-checked consent).
- **Measure behavior, not vanity**: clicks and downstream action over opens (opens are inflated by privacy proxies). One email = one primary metric, decided before sending.

## Transactional email

Receipts, password resets, notifications, invites, digests, alerts. These get the highest open rates a product will ever see and carry the trust burden: they're what users check when something feels wrong.

**Universal rules**
- **The subject carries the entire message** for triage: state the event and the object ("Invite: Sarah Chen added you to Acme's board room"). The body confirms, details, and offers the next action.
- **Answer the anxiety**: what happened, to what, when, was it me, what do I do if it wasn't. Security-relevant emails (password changed, new device) must include the "this wasn't me" path prominently.
- **Deep-link to the exact object**, not the homepage — an email about an annotation lands on the annotation (mobile: into the app if installed).
- **Don't smuggle marketing into transactional email.** A small contextual pointer is acceptable; a promo banner in a receipt breaches the register and (legally) can reclassify the email. Transactional emails are exempt from unsubscribe requirements *only while they stay transactional*.
- Timing is part of the UX: resets arrive in seconds (and say how long the link lives); receipts immediately; digests at a chosen, consistent time with user control over frequency.

**Pattern notes**
- *Password reset*: single CTA, expiry stated, ignore-if-not-you line, never the password itself.
- *Receipt/confirmation*: scannable summary table (what, when, how much, where), reference number, what happens next.
- *Notification*: enough context to decide without clicking (recognition over recall — quote the comment, name the document), then the deep link. Batch high-frequency events into digests before users batch them with the mute button.
- *Digest*: serial-position effect — most important item first, one glanceable section per category, per-category frequency controls in preferences, not just "unsubscribe from everything".
- *Invite*: who invited, to what, what happens on accept; works for recipients without accounts.

## Pre-send checklist

- [ ] Sender name recognizable; reply-to monitored (or expectations set)
- [ ] Subject front-loaded, survives 35-char truncation; preheader written, not defaulted
- [ ] One primary CTA, bulletproof button, outcome-verb copy, ≥44px tall
- [ ] Renders single-column at 320–375px; readable with images off; dark mode checked
- [ ] Alt text on informative images; `role="presentation"` on layout tables; `lang` set; body ≥14px; contrast ≥4.5:1
- [ ] Plain-text part present and human-written
- [ ] Footer: physical address; unsubscribe present, findable, one-click (marketing); preferences link for multi-stream senders
- [ ] Links tested; deep links land on the object; no "click here"
- [ ] Under ~100KB HTML (Gmail clipping); real content tested (longest company name, 0-item digest suppressed rather than sent empty)
- [ ] Register check: transactional emails contain no marketing payload; marketing claims pass the sincerity test
