# UX Writing & Interface Typography

Words are the interface's densest material — a one-word button change moves conversion more than most redesigns. Write the real words as part of the design, never as a fill-in-later.

## Ground rules (Krug + plain language)

- **Omit needless words**: cut half, then cut half of what's left. Every word competes for the scan.
- **The user's language, never the org's**: no internal jargon, feature codenames, or acronyms the user didn't choose to learn. Unavoidable technical terms get defined in context on first use ("Download as CSV (a spreadsheet format)").
- **Banned-word discipline**: marketing-inflation words are noise in an interface — *seamless(ly), effortless(ly), powerful, robust, leverage, unleash, blazing/lightning-fast, turnkey, holistic, best-in-class, next-generation, cutting-edge, world-class, streamline, elevate, harness, empower, revolutionary, synergy, utilize (→ use), myriad, plethora*. Also cut the invisible fillers (*just, simply, actually* — "simply click" insults anyone who found it hard) and the hedges (*Consider…, You may want to…, It is important to note…*) — say the thing.
- **AI-tell patterns to lint out of product copy**: significance inflation ("crucial", "critical" on routine things), sycophancy ("Great question!"), filler openers ("It's important to note that…"), template closings ("The future of X is bright"), vague authority ("experts say"), "not only X but also Y" parallelism, artificial "from X to Y" scale claims, and rule-of-three synonym churn — repeating the *same* word is natural; rotating synonyms to avoid repetition reads as machine. Bold only what genuinely needs attention; a dry statement lands harder than an exclamation mark.
- **Front-load meaning**: action or benefit first, conditions second. First two words of every heading, link, and list item carry the scan.
- **Active voice, present tense, direct address** ("We'll review your application", "This deletes your account"). Passive is acceptable only for system states ("Your file was saved").
- Sentences ~15–20 words; one idea each. Target reading grade 6–8 for consumer surfaces, 8–10 for professional tools (Diolog's IR audience: professional, not academic).
- Don't pad with "please" everywhere — it inflates and goes invisible; save politeness for genuinely inconvenient asks.
- **A masthead may not restate the thing directly under it.** The eyebrow/kicker exists to say what the H1 cannot: status, date, section, scope. Measured on five live sites from one generator, the hero eyebrow and the H1 were the **same string** — the company's legal name, stacked in two sizes — so the largest type on the page carried nothing, and a screen-reader user heard the name three times before reaching content. If the kicker would repeat the heading, delete the kicker or give it a different job.
- **Copy that only varies by a substituted proper noun has not varied.** *"Facts %s publishes, with their sources"* / *"Documents in the order %s published them"* / *"What %s does"* rendered on five sites, character-identical after the name; two of the five headings did not even change that much. Structure, layout and colour can all differ and the pages will still read as the same document, because a reader compares **sentences**. When copy is generated per instance, diff the emitted strings against the previous instance before shipping, and treat a high overlap as the defect it is — not as consistency.
- **A surface's copy is about the subject, never about the system that renders it.** *"245 dated documents held, each linking its published PDF"* shipped as the lead evidence line on an investor portal's hero: it counts what the CMS holds, not what the company does. The tell is the verb — *held*, *found*, *indexed*, *crawled*, *mirrored* are things the product does. Also here: provenance leaking into a label (*"Head office as stated on the FAQ page"* — the source belongs in a source field, not in the name of the thing).
- **On a content surface, headings are claims — not labels.** *Process topology*, *Deployment model*, *Security posture* are filing labels: they tell a scanner what a section is about and never what it says, so the reader has to enter every section to find out whether it holds anything they need. A heading a reader could disagree with (*The reach of the two calls is not the same*) carries the finding into the scan, which is where most readers stop — median scroll depth is around half the page. The test is reordering: if the sections could be shuffled and no reader would notice, the headings are an index and the page has no spine. This does not apply to product UI, where a section label naming a settings group is exactly right.
- **Uncertainty is content, and its absence is a finding.** On any surface making evidence-backed claims — a report, a research page, an analysis, a status write-up — the honest limits belong in the interface, not filed in a methods note at the foot. Where sources disagreed, say so in the body copy; where a number is single-sourced, say that beside the number; where something could not be established, give it a heading of its own. Measured on two pages built from one corpus: the weaker carried **one** hedge-free statement of a limit in 3,700 words, the stronger twenty-six, and blind judges in both orderings preferred the second largely on this. A page that resolves everything reads as generated, because a human author with real sources almost always has something they are unsure about. Note the difference from the banned hedges above: *"You may want to consider…"* is filler, *"the two reports that looked hardest each went to find this figure and reported it does not exist"* is information.

## The patterns

**Buttons** say the outcome: "Save changes", "Send invitation", "Start free trial" — never "Submit", "OK", "Yes". The label should let a user predict exactly what happens (information scent at its smallest scale). Paired buttons: the safe action is never styled to be mistaken for the destructive one, and neither is labeled so vaguely ("Cancel" the subscription vs "Cancel" the dialog) that the pair is a riddle.

**Labels** are nouns the user would say; status labels are states ("Sent", "Draft", "Archived"), action labels are verbs ("Send", "Archive"). Pick one term per concept and enforce it everywhere — "workspace" in one screen and "project space" in another reads as two features. Keep a terminology list for the product; "log in" vs "sign in" inconsistency across surfaces is a real finding.

**Error messages** = what happened + how to fix it, always both:
- ✗ "Invalid input" · "Error 422" · "Something went wrong"
- ✓ "That email is missing an @ — like name@company.com"
- ✓ "Your payment was declined by your bank. Try another card or contact your bank."
Never blame ("you entered an invalid…"); focus on the fix. Place adjacent to the problem; clear the error the moment it's resolved. For system-level failures, add: is my data safe, and what do I do now.

**Confirmations** = what happened + what to expect next: "Payment processed — receipt on its way to amy@…". "Success!" alone answers neither question. Pending states name the wait: "Verifying your identity — usually 1–2 business days."

**Empty states** = education + action + motivation: what this area is for, how to create the first thing, why it's worth doing — plus the prominent button. Search/filter empty results offer recovery (spelling, broaden, popular items), never a bare "No results found."

**Tooltips & helper text**: tooltips explain unfamiliar concepts, never carry essential information (invisible until triggered, hostile on touch); persistent helper text below the field for anything needed *while* typing. Placeholders are format examples only.

**Destructive dialogs** name the object and the consequence: "Delete 'Q3 board pack' and its 12 files? This can't be undone." — with the loss quantified, an alternative offered where one exists ("Archive instead?"), and buttons that repeat the verb ("Delete pack" / "Keep pack"), not Yes/No.

## Tone matrix

Voice is constant (Diolog's voice: direct, expert, calm — see `diolog-brand-voice` for prose work); tone flexes by context. Calibrate on four dials: formality, emotion, authority, complexity.

| Context | Tone | Example register |
|---|---|---|
| Onboarding | Casual, warm, peer, simple | "Let's set up your first update — about 2 minutes." |
| Success | Brief celebration | "Done! Your update is live." |
| Errors | Calm, empathetic, expert, simple | "We couldn't save — your connection dropped. Try again when you're back online." |
| Empty states | Encouraging, pointed | "No questions yet. Investors' questions will land here." |
| Settings | Neutral, precise | "Two-factor adds a second check at sign-in. Recommended." |
| Destructive | Serious, concrete | "This removes all member access. It can't be undone." |
| Legal/compliance | Formal + plain-language summary | Technical text with a one-line human summary above it |
| Marketing email | Enthusiastic but honest, peer | Benefit-led, no hype inflation |
| Transactional email | Matter-of-fact, complete | Event + object + next step; zero cleverness in security emails |

The tell of a broken tone: celebration in an error, cleverness in a security notice, legalese in onboarding. Humor is highest-risk in the states where users are already frustrated — never joke in an error message.

## Interface typography (Butterick essentials)

These are correctness rules, not styling taste — apply silently whenever producing UI or email text:

- **Curly quotes and apostrophes** (" " ' '), never straight — except foot/inch marks (6′ 2″), which stay straight. In JSX, `’` in *text content* renders literally; paste the actual character or use `{'’'}`.
- **Three dashes**: hyphen for compounds (cost-effective), en dash for ranges (1–10), em dash for breaks — like this. Never `--`.
- **One space after punctuation.** Real ellipsis (…) not three periods. Real ©/™/® not (c)/(TM).
- **Accents are mandatory in proper names** (Plácido Domingo).
- **Bold OR italic, never both; never underline** (underline means "link" and nothing else on screens).
- **ALL-CAPS only for short labels, always letterspaced** (+5–12%, `letter-spacing: 0.06em`); never for body text.
- **Line length 45–90ch** (`max-width: 65ch` is a safe default); **line-height 1.2–1.45** for body (tighter as size grows); body ≥16px web, ≥14px email.
- **Tabular figures** (`font-variant-numeric: tabular-nums`) for any column of numbers, prices, or timers.
- Headings: max 3 levels, bold not italic, space-above > space-below, sentence case unless the brand says otherwise, `text-wrap: balance` where supported.
- Numbers users compare get the math done for them ("Save $40/yr" next to the annual toggle) — formatting is cognition offloaded.

## Localization hygiene (write once, translate safely)

Never concatenate strings ("You have " + n + " messages" breaks in most languages — use ICU plural formats); never bake text into images; assume +30% length for German and design the button/label to survive it; dates/numbers/currency formatted per locale, stored in ISO. Give translators context in string keys (`button.save_changes`, not `string_47`).
