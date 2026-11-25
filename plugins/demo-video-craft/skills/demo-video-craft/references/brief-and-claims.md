# Brief and claims

Step 1 of every series, and the file to reopen whenever a note touches what the videos say. Everything here is
written before any scene is built, because a claim found false after the render costs a re-render of every film
it appears in.

## 1. Read in this order

0. **The series that came before.** Earlier films, kits and decisions may sit on another branch or in another
   worktree. Look before starting a new folder, and build on the branch that holds the kit:

   ```bash
   git worktree list
   for r in $(git for-each-ref --format='%(refname)' refs/heads refs/remotes); do
     git ls-tree -r "$r" --name-only | grep -qE 'hyperframes.json|_kit/' && echo "$r"; done
   ```
1. **The product's own record**: the requirements or PRD, the specs, and whatever records what is built. A
   requirement-status file, a changelog or the live product all work; a roadmap does not. Find the newest version
   across every branch and worktree (`git for-each-ref --sort=-committerdate refs/heads refs/remotes`, then
   `git -C <worktree> status --untracked-files=all <record dir>` in each, because the newest addenda were untracked
   files in another worktree), and write its version and line count into `BRIEF.md`. Read it by its section offsets
   (`grep -n '^## '`) so "read in full" can be checked. In the source run the narration was generated against
   version 0.17 and then rewritten when 0.19 turned up.
2. **The product's interface**: its design system, UI kit or live screens. The films rebuild these screens as live
   HTML, so read the code where it exists rather than screenshots.
3. **The audience notes**: meeting notes, a prospect's stated problems, the questions their team will ask. These
   shape what the series shows and must never be quoted, named or alluded to in anything published.
4. **The brand's site**: the header lockup, the fonts, the colours. Measure the lockup from the site's pixels
   (`picture.md` §7), not from its CSS alone. Probe every brand URL the owner names and its near siblings (`curl -s
   -o /dev/null -w '%{http_code}'`): the owner wrote one host while the kit and memory used another, and only one was
   the design of record.

When the owner retargets the series at a named prospect, read the prospect-facing pages and the record's gap notes as
the claims source, and answer the prospect's stated problems on screen (context kept by hand, checks done from memory,
an empty chat box, an approval tool they already have) without quoting, naming or alluding to the meeting.

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
  them "videos", not "films". Fix the variant once here, and name it in every brief to the voice skill: a brand voice
  skill may default to another variant, and a page-wide UK/US switch built in one round was removed in the next ("just
  stick to us english").
- **Lengths and counts asked for**: they are ceilings. When the series departs from them (asked: one 2-minute video
  and ten 30 s clips; shipped: 1:41 and nine 21-25 s shorts), record the change and its reason here and name it in
  the first report.
- **The ask**: the one action the series ends on, as text the end slide can show.

## 3. CLAIMS.md

One row per capability the series shows or says:

| Claim | Source | Status | How it appears |
|---|---|---|---|
| Checks a draft against the published record | REQ-12 | built | short 3, the draft and the record side by side |

- **Built** may appear. **Partial** may appear for the built part only. **Unbuilt** does not appear at all, in
  picture or words. One short in the source run was re-scripted because the feature it depended on was only
  partly built, and a seven-year retention claim reached three files before anyone checked its status. Before any
  voice is paid for, grep the brief, the narration and the storylines for every requirement id they cite and confirm
  each is built in the product's status file.
- **Each narration line names the card that proves it** (`voice-and-music.md` §1), and on-screen tool names come from
  the product's own tool registry.
- **No timing or percentage claims** without a measurement behind them. Show time saved as pictures instead: work
  done before anyone asks, no copying between tools. A phrase the owner supplies, such as "in minutes", gets a
  row marked "owner's phrase, unmeasured", listing every line that uses it, so the claims review can find them.
- **Product truth goes into the build as an assertion.** When the product does something one specific way (a
  second factor is an authenticator code, never a passkey; a requester never approves their own item), make the
  screen builder fail if any screen says otherwise. The source run did this for the second factor and for an old
  product name.
- **Owner overrides are recorded.** The owner may decide to show something the record holds back. Record the date
  and their words in the row, and show it as asked.

## 4. The fictional company

Use one invented customer across every screen, so the series reads as one business rather than a set of mockups.
Put it in `states.py`, its one source, as the names and figures every screen draws from: the company, its ticker and exchange, five or six named people with roles, two or three
named counterparties, and one set of figures for the period shown.

- Check the name and ticker are free against the exchange's own register: SEC's `company_tickers.json` for US
  listings, the ASX company list for Australian ones. No real listed company may share the name.
- Reuse the same names and figures in the overview and at least three shorts. The corpus films that did this read as
  real work.
- Make the scenario match the audience's market: a US audience gets a US-listed company, earnings, SEC filings and
  analyst calls, in US English.

## 4b. A real company instead

An owner may ask for a real listed company, usually the prospect's own client, because nothing lands like the
viewer's own figures. The source run switched to one in its fifth round. The rules change, because every invented
detail is now an invented fact about a company whose shareholders can read it.

- **Ask the owner first whether a public page may show the company.** It is their call, and the source run's owner
  kept the page public against a recommendation to gate it.
- **Every figure, date and holder comes from the filings, and `SOURCES.md` comes first.** For a US listing,
  `scripts/edgar.py` lists the filings (`filings <ticker> --forms 8-K,10-Q`; earnings are 8-Ks with items 2.02 and
  9.01), extracts the release from its Exhibit 99.1 (`release <ticker> <accession> -o q2.txt`; the financial tables
  are in thousands, so $1,204.5M reads as `1,204,532`) and reads every Schedule 13G cover page (`holders <ticker>`;
  XML pages since 2024 parse, older HTML and text pages print the URL to read). Set `SEC_USER_AGENT` to a name and a
  generic contact. Write `SOURCES.md` with each figure, its document, page and accession number before any screen
  changes: the source run wrote it last, after screens, renders and posters had been made from a scratch file.
- **Follow the real story.** The source run's fictional quarter had been a beat and a raised outlook; the real one
  was a fall in comparable sales and a lowered outlook. The demos then showed a revised outlook, a margin helped
  by a one-off item and a figure caught in a draft. Use the latest reported quarter as "this quarter" and the one
  before it as "last quarter", so the deck roll-forward and "what changed since" are both real.
- **Never invent an event, statement, plan, deal, date, approval, meeting or trade** for the company or for any named
  real person or institution. An invented acquisition or "said privately" line under a real name is fabricated
  non-public information. Rebuild such a demo around a public fact: a draft that states the new outlook before the
  release is filed (unreleased until then); a draft still quoting last quarter's range (a conflict with what was said
  since); two published statements on one metric (what was said before).
- **What is not public stays illustrative and anonymous.** The firm's drafts, inbox questions and a holder call can
  appear, with roles instead of people ("the CFO", "a shareholder", "a top-20 holder", "answered by management") and
  figures from the filings. A real executive never appears saying something they did not say.
- **The demo patterns that worked.** An ownership write-up still quoting a holder's old 13G percent, against its newest
  13G/A: one holder's 9.8% (2024) had become no shares (2026), its holding now reported by an affiliated adviser at
  6.9%. A draft with two digits of one figure swapped against the filed release (318.4 against 381.4). A draft stating the new outlook before the release is filed. A draft still quoting last quarter's
  range after it was revised.
- **A checked figure is not a good one.** Ink a real company's adverse figure neutral (`lead()` class `chk`); green
  is for "matches its source". Check every green figure's sign before rendering.
- **Switching scenario**: put every retired name, ticker, person, counterparty and period label in `states.py`'s
  `BANNED` (the build fails on any that survives on a screen), then `series_lint.py retired --term …` over the films,
  pages, page demos and poster sources. The source run's switch left 68 mentions of the fictional company in the
  features page's script after the videos were done.
- **Leave sensitive filings alone**: a proxy contest, litigation, an executive departure. They are real, and they are
  not what a product demo is for.
- **Narration and page copy say "your client"**, so the series reads as the viewer's own client without the voice
  naming it; the screens show the company. One disclosure line on the page names the company, says every figure
  comes from its filings and the drafts are illustrative, and credits the trademarks.
- **Take the brand from the company's own logo file**, usually linked from its corporate or investor site, and theme
  the deck and documents from it (`picture.md` §3b).

## 5. Names and pronunciation

Write a names table before any narration exists:

| Thing | Written | Spoken (`respell.json`) |
|---|---|---|
| The host assistant | Claude | Clawd (the owner's "clord" is non-rhotic; a US voice says every r it is given) |
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
