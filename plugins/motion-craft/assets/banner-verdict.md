# motion-craft banner: verdict

**Ships.** Same family grammar as the ux-craft and design-craft banners: porcelain ground on the icon's 118° light axis, Instrument Sans 600 wordmark, one vermilion accent used twice (the landed capsule and "directed").

The strip on the right lays the icon's idea flat: one capsule sampled every 0.2 s through a quadratic ease-out, so the gaps shrink as it lands and the ticks on the run show the deceleration.

Known liabilities:

- The 0.0s / 0.8s stamps are unreadable below the 900 px display row. They carry nothing the strip doesn't already show.
- The 0.6 s ghost sits mostly under the landed capsule. That is what the easing does, but at 200 px the strip reads as three ghosts, not four.
- The essence line is 26 px at layout size, so it gets small at 400 px. It stays legible there; at 200 px only the wordmark and icon read, which matches the sibling banners.
- The tile shadow is a CSS box-shadow behind the icon. `filter: drop-shadow` would follow the squircle exactly, but the render engine accepts it and never paints it.
