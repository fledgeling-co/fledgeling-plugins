🫥 Judged from source only; nothing was rendered and the media files were not viewed.

**1. Dimensions**

- **Fidelity to the notes: B.** A states as fact things the notes never say: "the same three wheels", "the best one gets glazed and fired", "blended in the studio", "Fremantle WA 6160", and a guessed link to `https://instagram.com/saltbushceramics`. B's slips are smaller: "on one wheel", "matte, and heavier in the hand", and "six people at a time" in the classes `h2`, where the notes cap only the taster. B shows the gap honestly with `[Email, phone and Instagram handle — waiting on you]`, labels the film a stand-in, and sets `noindex` for "don't publish anything yet".
- **Distinctive design: B.** Its fixed `.ruler` depth gauge and hatched `.horizon` strata ("The wheel" down to "The pit") build the page around the Bindoon clay pit. A's dark palette, pill buttons, numbered sections and marquee are polished but familiar, though A does have glaze images where B has CSS swatches.
- **Phone-first booking path: A.** It keeps a "Book" button in the sticky `.bar`, adds a thumb-reach `.dock` that slides in past the hero, and gives each class its own link. B has the hero and per-class links but nothing persistent, and its 64px ruler plus 28px padding leaves about 255px of content on a 375px phone.
- **Video hero and degradation: B.** `main.js` keeps sources in `data-src` so reduced-motion visitors never download the clip, swaps the poster to `hero-rest.jpg`, and always offers Pause/Play/Replay. A's autoplay still works without JS and recovers from refusal ("Play the hero"), but under reduced motion it hides the video with no way to play it, still fetches it (`preload="auto"`), and has no pause control.
- **Motion through the page: B.** Scroll-driven reveals, the travelling `.ruler-mark` and the drawn underline on `.class` sit inside `prefers-reduced-motion: no-preference` and `@supports (animation-timeline: view())`. A's only page motion is the `.ticker`, which loops with no pause and under reduced motion becomes a clipped static row.
- **Accessibility: B, narrowly.** B has a labelled pause button, 44–48px targets and `aria-labelledby` sections; its faults are 10–11px ruler text and a green focus ring at roughly 2.3:1 on the `.iron` section. A has better link context (`sr-only` price and day on each CTA) and real alt text, but the unpausable ticker reads its duplicated spans twice and every link opens a new tab unannounced.
- **Robustness across browsers: A, narrowly.** It uses plain autoplay attributes, WebM and MP4 sources, an `IntersectionObserver` fallback and prefixed `backdrop-filter`. B degrades safely, but the video needs JS, `<source media>` falls back to the phone clip on older desktop browsers, and the scroll motion is absent in Firefox.

**2. Most serious defect**

- **A:** invented facts published as the owner's own, worst of all a live footer link to an Instagram handle she never supplied and a customer promise ("the best one gets glazed and fired") she never made.
- **B:** the always-on 64px ruler takes about 17% of a phone screen on a site whose bookings come from Instagram, and there is no persistent booking button to compensate.

VERDICT: B
