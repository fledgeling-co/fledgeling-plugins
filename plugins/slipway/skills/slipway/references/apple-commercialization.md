# Apple commercialization — region-aware decision tree

How to price and sell a Mac/iOS product without shipping copy that a storefront rule or a court ruling invalidates. Walk this before Phase O½ writes pricing cards for any native surface, and re-verify the legal state at launch time — this domain moves.

## The tree

1. **Which platform is the paid surface?**
   - **Web/SaaS only** → none of this applies; price on the marketing site, checkout via Stripe. Done.
   - **Mac app** → 2. **iOS/iPadOS app** → 3.

2. **Mac: how is it distributed?** (the `--macos-dist` interview answer)
   - **Direct (Developer ID)** → sell direct: Stripe/Paddle-style merchant-of-record checkout on the marketing site. The proven indie pattern is **one-time price + 1 year of updates + optional renewal** (CleanShot X $29; Sketch's $120 perpetual "yours to keep"). ~5% MoR fees vs 15-30% App Store. A 30-day refund can replace a trial. No Apple rules apply to the sale at all.
   - **Mac App Store** → Apple's IAP rules apply as per iOS below; App Sandbox is a review requirement (the scaffold's `mas` entitlements). Dual-channel (MAS + direct) is legitimate — Sketch sells both side by side — but the marketing site must not show a price the MAS build can't honour.

3. **iOS: what's being sold?**
   - **Digital features/content unlocked in-app** → **IAP is the default rule.** Presentation pattern with the strongest benchmark evidence: trial paywall + annual "most popular" + lifetime anchor (Flighty: $4.99/wk anchor, $59.99/yr, $299 lifetime). Hard paywalls convert ~5x freemium but refund higher — the trade is expectation management, so the marketing site must show the product honestly before the paywall does.
   - **Physical goods/services** → external payment is fine and normal.

4. **External purchase links (the flux zone).** The US position (post-Epic contempt ruling, affirmed Dec 2025): external purchase links can't be prohibited and the fee is 0% *pending rate-setting and a SCOTUS petition*. The EU, South Korea, Japan, Brazil each have their own entitlement-specific regimes, and Apple's external-purchase entitlements are storefront-specific. **Rules for the pipeline:**
   - Never bake a channel-fee claim ("save 30% buying on our site") into generated copy — it can invert within months.
   - Treat external-purchase implementation as counsel-reviewed, per-storefront configuration, not a growth default.
   - The marketing site may present real channel choices (Download for Mac / App Store badges), but only once each channel actually exists, and Apple badges are used as supplied, never animated.

5. **Fees worth knowing when modelling revenue:** Apple Small Business Program 15% (under $1M/yr); standard 30%/15% year-two subscriptions; MoR direct ~5%. The pricing recommendation in `docs/MARKETING-FEATURES.md` should state which channel model it assumed.

## What the pipeline does vs the owner

The pipeline: picks the pattern from this tree, writes the pricing section, drafts the App Store kit (docs/LAUNCH.md). The owner: opens the accounts, sets live prices in App Store Connect / the payment processor, and approves any external-purchase configuration after checking the current legal state.
