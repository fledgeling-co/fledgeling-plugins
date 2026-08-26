# The four books, and the four ways a model misapplies them

Load this before generating candidates or writing a territory. Each book gives
specific *moves* and specific *failure modes*. Use all four; they constrain each
other, and the constraint is the point — Blue Ocean rewards bold breadth while
Ries/Trout and Baker demand narrow focus, so a territory that satisfies all four
has been through a real argument.

Each section closes with **the model failure**: how an LLM applying this
framework goes wrong in a way that reads as competent. These are the ones worth
watching, because the human failure modes are already in the books.

---

## 1 · Ries & Trout — *Positioning: The Battle for Your Mind*

**Core idea.** Positioning is not what you do to the product; it is what you do
to the mind of the prospect. The mind is small, hates complexity, and holds
roughly one idea per brand. You win by occupying an open slot and owning it.

**The moves:**
- **Own one word.** A brand that means many things means nothing.
- **Be first, or create a category you can be first in.** If you cannot lead an
  existing category, reframe to one you can lead.
- **Position against the leader.** Name an enemy. "The X for people who hate Y."
  An enemy gives the prospect an instant mental slot.
- **Beware the line-extension trap.** Every additional thing the brand stands
  for subtracts from the original idea. Breadth, *led with*, destroys the slot.

**Failure mode:** the "everything" pitch. All-in-one occupies no slot and reads
as bloatware.

**The model failure: the word that is not a word.** Asked for one word to own, a
model returns an abstraction — "clarity", "velocity", "trust", "intelligence" —
which is not a slot in anyone's mind, cannot be contested, and cannot be lost.
A real owned word is one a competitor would have to fight you for. Test it: name
the company that owns it today. If the answer is "nobody, it's a nice word",
it is not a position, and the territory needs a different word or a different
axis.

**In the synthesis:** each territory gets exactly one word and one named enemy,
and the enemy is a *specific* thing — a named competitor, a named practice, a
named status quo — never "complexity" or "the old way".

---

## 2 · April Dunford — *Obviously Awesome*

**Core idea.** Customers understand a new thing only through the context you
give them. The category sets expectations about competitors, price, and which
features matter. If you do not choose the frame, the prospect picks one badly
and your best features go invisible.

**The six components** — assemble all six for every territory:

1. **Competitive alternatives** — what would they do if you did not exist?
   Rarely "nothing".
2. **Unique attributes** — what you have that the alternatives do not.
3. **Value (+ proof)** — the benefit those attributes enable, that customers
   care about.
4. **Target-market characteristics** — who cares a lot and buys quickly.
5. **Market category** — the frame that makes your value obvious.
6. **(+) Relevant trend** — ride a wave, but only one that reinforces a durable
   attribute.

**The category choice, decisive:** (a) win the head of an existing category,
(b) win a subsegment of one, or (c) create a new category. Category creation is
expensive; the pragmatic play is usually (b) — anchor in an understood category,
then re-segment so your strengths become obvious.

**Dunford's preference for (b) has numbers under it now, and a live dispute.**
Historical analysis of ~500 brands across 50 categories found 47% of pioneers
failed, surviving pioneers averaged ~10% share, and early leaders entering
roughly 13 years later failed ~8% of the time and averaged ~28%. The
counter-claim that category kings capture 76% of category value defines a
category king *by* dominance and then measures the dominant, so it describes
winners rather than estimating a success rate. A 2026 meta-analysis of 90
category-spanning studies found the overall effect on audience appeal
statistically indistinguishable from zero with extreme heterogeneity — no
universal penalty, no universal premium, everything in the moderators. Take (b)
as the default, treat (c) as a separately funded hypothesis, and put both
positions in the evidence register. `references/evidence.md` §2.

**Test:** a cold prospect gets it in about ten seconds. If the category label
needs explaining, it is wrong.

**The model failure: alternatives that are all competitors.** Asked for
competitive alternatives, a model lists the category's vendors. The alternative
that actually loses most deals is a spreadsheet, an intern, a Slack channel, or
nothing at all — and a positioning built against the vendor set never addresses
the buyer who was never going to buy from that set. Require at least one
non-software alternative in every territory, or an explicit note on why there
genuinely is not one.

---

## 3 · Kim & Mauborgne — *Blue Ocean Strategy*

**Core idea.** Stop competing on the same factors. Create uncontested space via
value innovation — differentiate *and* lower cost — by changing which factors
you compete on.

**The Four Actions (ERRC), one per territory:**
- **Eliminate** — which factors the industry takes for granted should go?
- **Reduce** — which should be cut well below the standard?
- **Raise** — which should be raised well above it?
- **Create** — which factors the industry never offered should exist?

**Strategy canvas:** a winning value curve has **Focus** (all-in on a few
factors), **Divergence** (it looks unlike the field), and a **compelling
tagline**. A curve present on everything has none of these.

**The model failure: an ERRC with an empty Eliminate.** Eliminate and Reduce are
where the strategy is, and they are the two a model leaves thin, because they
require giving something up and the training data rewards addition. An ERRC
whose Eliminate row says "unnecessary complexity" has eliminated nothing. Name a
factor the industry *actually competes on* and actually drop it — and then check
the truth ledger, because dropping a factor you never had is not a choice.

---

## 4 · David C. Baker — *The Business of Expertise*

**Core idea.** Authority, pricing power and inbound demand flow to the
specialist. Expertise is pattern-matching inside a narrow domain. "Everything
for everyone" forfeits the premium.

**The moves:**
- **Specialise — horizontal (a discipline) or vertical (an audience)** — until
  it is almost uncomfortable.
- A broad *product* can still have a narrow *positioning*: specialise on the
  who/job even when the product does many things.
- Narrowing is not giving up the bigger market; it is the credible path to it.

**The model failure: the comfortable beachhead.** Asked to narrow, a model
narrows to a segment that is large, well-documented and adjacent to everything —
"mid-market B2B SaaS teams" — which is a description of the market, not a
beachhead. A real beachhead is uncomfortably small, nameable, reachable through
a specific channel, and feels the pain acutely enough to buy this quarter.
Require the territory to name where that beachhead congregates and what it
currently spends money on instead.

---

## How the four resolve: position narrow, deliver broad

Lead with one wedge — one word, one enemy, one beachhead, one category — that
gets you into the mind and the door. Let breadth be the expansion story told
*after* adoption, never the opening line. Amazon was books; Notion was docs;
Linear was issue tracking; Superhuman was fastest email; Figma was
design-in-the-browser.

**The repeated failure across all four is the feature-list pitch.** It destroys
the mind-slot (Ries/Trout), invites a red-ocean frame (Dunford), produces a
no-focus value curve (Blue Ocean), and forfeits the specialist premium (Baker).
Catch it every time.

It also has a measurement. A study of over a hundred firms' B2B value
propositions separated three approaches — **All Benefits** (list everything),
**Favourable Points of Difference** (every difference from the next-best
alternative), and **Resonating Focus** (the one or two differences that deliver
quantifiable value at the customer's actual bottleneck, with proof). **All
Benefits was observed in 85% of failed pitches.** So every territory here carries
one or two points of difference stated in the customer's units, not a list —
which is the same rule the four books arrive at separately, with a number
attached.

## Where the frameworks stop

All four are practitioner frameworks built from case evidence, not from
controlled study, and they were selected by their authors from the winners.
Nothing in them predicts which position will work; they are instruments for
making a position *coherent and defensible*, which is a different and smaller
claim. A territory that scores well on all four is well-constructed. Whether it
is *right* is what the pre-commitment tests in `decision-aid.md` are for.

The research panel put it more sharply than the books do: **no named positioning
framework has independently demonstrated a repeatable, causal ability to choose
successful market positions.** Blue Ocean specifically has been criticised in
peer-reviewed work for lacking a clear implementation protocol and for limited
scientific validation — which is why ERRC is used here as a *construction*
instrument (it forces the Eliminate question, which is the one a model otherwise
skips) rather than as evidence.

What does have empirical support is not a framework but a set of customer-perceived
properties: **favourability, uniqueness or dissimilarity, credibility, and
category comprehension**, validated across seven studies as predicting purchase
intention better than attribute-only measures, with benefit-based and user-based
positions generally outperforming feature-based ones. Check a territory against
those four directly, in addition to the books.
