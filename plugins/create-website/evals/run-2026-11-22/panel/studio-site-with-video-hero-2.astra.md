🫥 1. Dimension judgments

- **Fidelity — A.** Its footer identifies the stand-in film and flags the missing Instagram handle. B invents a handle, three studio wheels and a firing inclusion for the taster. A also adds unsupported details, including “on one wheel.”
- **Distinctive design — A.** The fixed depth ruler and hatched section breaks in `style.css` carry the Bindoon clay-pit idea from “Surface” to “The pit.” B’s dark palette echoes the iron glaze, but its pill buttons and rounded cards are less specific to this studio.
- **Phone-first booking — B.** The sticky header’s “Book” link goes straight to Bookwhen from the first screen. After the hero, the 54px `.dock` keeps booking within thumb reach. A offers direct links but reserves 64px of phone width for section navigation.
- **Video hero and fallback — A.** `main.js` defers video loading, selects the finished-bowl still for reduced motion, offers “Play the film” after autoplay refusal and supports pause and replay. B has a poster, a still and retry, but no pause control. Neither clip’s final frame can be verified from the file listing.
- **Page motion — A.** `style.css` ties ruler travel, class underlines and section reveals to scrolling under `prefers-reduced-motion: no-preference`. B’s main effect is a continuous ticker. Under reduced motion it stops, leaving its nonwrapping text clipped on phones.
- **Accessibility — A, narrowly.** Its 44px film control lets visitors pause playback. B supplies a descriptive video label and contextual class-link names, but its infinite ticker has no pause control and its offscreen booking dock remains keyboard-focusable.
- **Cross-browser robustness — B.** Its HTML supplies WebM and MP4 sources directly, and `assets/site.js` handles browsers without `IntersectionObserver`. A’s poster survives script failure, but the video sources remain in `data-src` and the visible film button then does nothing.

2. Most serious defect in each option

- **A —** “Three ways in, six people at a time” in `#classes` implies a six-person cap on every class. The notes specify that cap only for the wheel taster.
- **B —** The $95 taster promises “the best one gets glazed and fired.” That gives paying students a concrete expectation the owner never authorized.

VERDICT: A