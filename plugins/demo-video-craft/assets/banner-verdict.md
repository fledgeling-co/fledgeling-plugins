# demo-video-craft banner: verdict

**Ships.** Same family grammar as the other "making" banners: porcelain ground from the icon's build constants, light from the upper left, the real icon at 240 px with a soft tile shadow, an Instrument Sans 600 wordmark at 80 px so the 16-character name fits one line, and one vermilion accent used twice (the overview's play triangle and "muted and voiced").

The bench on the right lays the icon's idea flat as the thing the skill makes: one overview screen pressed by the icon's own cursor with its two rings, and four shorts beneath it. Only the overview carries the accent.

Known liabilities:

- The mono stamp ("1 overview · 4 shorts · 2 cuts each") is unreadable below the 900 px display row. It carries nothing the bench does not already show.
- The essence line is two lines at layout size and small at 400 px. It stays legible there; at 200 px only the wordmark, icon and bench read, which matches the sibling banners.
- The shorts' play triangles have sharper corners than the icon's rounded triangle, because the bench draws them with a round-join stroke rather than the icon's quadratic corners. Visible only in the 1600 px crop.
- The tile shadow is a CSS box-shadow behind the icon rather than a drop-shadow that follows the squircle, as on motion-craft's banner, for the same reason: the render engine does not paint `filter: drop-shadow`.
