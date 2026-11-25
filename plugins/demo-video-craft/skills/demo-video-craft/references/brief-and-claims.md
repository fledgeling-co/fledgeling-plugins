# Brief and claims

Step 1 of every series, and the file to reopen whenever a note touches what the videos say. Everything here is
written before any scene is built, because a claim found false after the render costs a re-render of every film
it appears in.

## 1. Read in this order

1. **The product's own record**: the requirements or PRD, the specs, and whatever records what is built. A
   requirement-status file, a changelog or the live product all work; a roadmap does not. Check every branch for
   the newest version of the record before writing a line of narration. In the source run the narration was
   generated against version 0.17 and then rewritten when 0.19 turned up on another branch.
2. **The product's interface**: its design system, UI kit or live screens. The films rebuild these screens as live
   HTML, so read the code where it exists rather than screenshots.
3. **The audience notes**: meeting notes, a prospect's stated problems, the questions their team will ask. These
   shape what the series shows and must never be quoted, named or alluded to in anything published.
4. **The brand's site**: the header lockup, the fonts, the colours. Measure the lockup from the site's pixels
   (`picture.md` §7), not from its CSS alone.

## 2. BRIEF.md

Write these sections, each short:

- **Audience**: who watches, what they already use, what they are trying to get done, and the one objection they
  will raise. A technical buyer at a firm that already pays for an AI assistant will ask why the firm cannot build
  this itself, and the series should answer that question on screen, without naming it.
- **Where the videos play**: the video site, YouTube, LinkedIn, a link in a deck. This fixes the canvas: 16:9 for
  a site and YouTube, 9:16 for Shorts and Reels.
- **Series shape**: one overview, then N shorts, each named by its outcome ("Your post-earnings brief, ready").
- **Must-carry facts**: three to seven, numbered, each traced to a requirement id or a source line. Every one must
  reach the screen, not only the narration.
- **English variant and terms**: US or UK spelling and dates, and the words the audience uses. A US audience calls
  them "videos", not "films".
- **The ask**: the one action the series ends on, as text the end slide can show.

## 3. CLAIMS.md

One row per capability the series shows or says:

| Claim | Source | Status | How it appears |
|---|---|---|---|
| Checks a draft against the published record | REQ-12 | built | short 3, the draft and the record side by side |

- **Built** may appear. **Partial** may appear for the built part only. **Unbuilt** does not appear at all, in
  picture or words. One short in the source run was re-scripted because the feature it depended on was only
  partly built.
- **No timing or percentage claims** without a measurement behind them. Show time saved as pictures instead: work
  done before anyone asks, no copying between tools. A phrase the owner supplies, such as "in minutes", gets a
  row marked "owner's phrase, unmeasured" so the claims review can find it.
- **Product truth goes into the build as an assertion.** When the product does something one specific way (a
  second factor is an authenticator code, never a passkey; a requester never approves their own item), make the
  screen builder fail if any screen says otherwise. The source run did this for the second factor and for an old
  product name.
- **Owner overrides are recorded.** The owner may decide to show something the record holds back. Record the date
  and their words in the row, and show it as asked.

## 4. The fictional company

Use one invented customer across every screen, so the series reads as one business rather than a set of mockups.
Put it in `scenario.json`: the company, its ticker and exchange, five or six named people with roles, two or three
named counterparties, and one set of figures for the period shown.

- Check the name and ticker are free against the exchange's own register: SEC's `company_tickers.json` for US
  listings, the ASX company list for Australian ones. No real listed company may share the name.
- Reuse the same names and figures on at least four surfaces. The corpus films that did this read as real work.
- Make the scenario match the audience's market: a US audience gets a US-listed company, earnings, SEC filings and
  analyst calls, in US English.

## 5. Names and pronunciation

Write a names table before any narration exists:

| Thing | Written | Spoken (`respell.json`) |
|---|---|---|
| The host assistant | Claude | Clawd |
| The product, possessive in speech | Acme Guardian | Acme's Guardian |

- One public name per thing, used identically in the picture, the captions and the pages. When the product has a
  name for its connector and another for its agent, write down which surface uses which.
- `respell.json` changes only what the voice is sent. Captions, pages and screens keep the real spelling.
- Order the rules specific first: the rule for the two-word name has to run before the rule for the brand alone,
  or the possessive never fires. `gateway_audio.py --self-test` proves the order matters.
- Pronunciation cannot be checked by transcription: Scribe writes back what it expects to hear. Ask the owner to
  listen to one line per respelling, or listen yourself where audio playback is possible, and record who did.

## 6. Labels and disclosures

- Identity tags ("Dana Ruiz · advisor, in Claude") help the viewer follow who acts, and they stay.
- Disclaimer labels ("Illustrative workflow", "Replay") are the owner's call. In the source run the owner removed
  them all. When a caveat leaves the picture, move it into the page copy beside the video, because a workflow that
  needs approved access still needs saying somewhere.
- Put one label switch in `SERIES.md`, so turning every label off is one edit.

## 7. Questions

Run `clarify:clarify` before every question. What usually reaches the user, as one batched question:

- the overview storyline, from motion-craft's three;
- 16:9 or 9:16 for the shorts;
- the voice, after an audition of three or four on the lead line in the audience's accent;
- paid music, with its cost.

Read the note attached to every answer as well as the option chosen. In the source run, one note ("create all 3")
turned a pick of one storyline into three finished films.
