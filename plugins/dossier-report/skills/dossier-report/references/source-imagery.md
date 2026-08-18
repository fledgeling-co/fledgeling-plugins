# Imagery — from the sources, and generated

A page whose argument is its evidence has an obvious use for pictures and
a specific way of getting them wrong. This file covers where an image may
come from, what it has to carry to be publishable, and when a generated
still or clip earns its place.

Two standing requirements sit behind everything here:

> **Every page uses imagery from the research sources where the subject
> has a visible form.** A page about products, hardware, interfaces,
> places or documents that renders as pure typography has thrown away
> evidence the corpus already contains.

> **An image is a claim, so it carries provenance.** Caption, source row,
> and the same registry the prose cites. An uncaptioned picture on an
> evidence page is the one element that asserts something with no
> attribution at all.

## Where an image may come from

In priority order. Take the highest one available and record which.

1. **The vendor's or publisher's own press asset.** A media kit, a
   newsroom, a product page's own hero, an official spec drawing. This is
   the best option on every axis: it depicts the thing accurately, it is
   published to be used, and the licence terms are usually stated on the
   page you took it from.
2. **A figure the source itself published for reuse** — an
   openly-licensed diagram, a government or standards-body illustration, a
   paper's figure under a licence that permits it. Record the licence.
3. **A generated illustration or diagram** via `media-gen-pro`, where the
   picture is *depicting a concept* rather than showing a real object.
4. **An honest placeholder** naming what is missing, when the asset does
   not exist and cannot be generated truthfully.

**Not on the list, and not admissible:** an image found by search with no
traceable origin, a photograph lifted from a review site, a competitor's
marketing composite, a still cropped out of a video, and anything whose
licence you cannot state in a clause. On a page published under a real
name to a real subdomain, "it was on the internet" is not a basis.

## The four things every image carries

```html
<figure class="fig fig--photo">
  <img src="assets/miele-c3-body.jpg" width="960" height="640"
       alt="The C3's canister with the dust bag compartment open, showing
            the sealed collar the filtration claim depends on."
       loading="lazy" decoding="async">
  <figcaption>
    The sealed bag collar — the mechanism behind the filtration result.
    <span class="prov">Miele press kit, retrieved 18 Aug 2026<a class="cite"
      href="#r14" data-cite="r14" data-n="14" aria-describedby="r14">14</a></span>
  </figcaption>
</figure>
```

1. **A caption that says what it is** — the thing shown and why it is
   here, not a repetition of the heading above it.
2. **Provenance in the caption**, with a citation marker into the shared
   registry. The registry row records the origin and the retrieval date
   like any other source.
3. **Alt text describing what matters about it**, not what it is of. "The
   canister with the bag compartment open, showing the sealed collar"
   carries the evidence; "a vacuum cleaner" carries nothing.
4. **Explicit `width` and `height`** matching the file, so the box is
   reserved before the image lands.

**Generated assets say so in the caption**, in words a skimming reader
cannot miss: *"Illustration, generated"*. An illustration a reader could
mistake for a photograph of the thing under discussion is a provenance
failure, not a decoration choice — the same standard the claim graph
applies to numbers.

## Licensing, plainly

Record the basis for every image in its registry row: `press kit`,
`CC BY 4.0`, `public domain`, `generated`, `vendor spec drawing`. Where the
basis is unclear, **do not ship the image** — describe the thing in prose
and say a picture was not available on terms the page could use. That
sentence costs nothing and an unlicensed asset on a published page costs a
takedown at best.

This is a production rule, not legal advice. Where a case is genuinely
borderline — a product photo you believe is fair to use in a review
context, an editorial image with unclear terms — put it to the user rather
than deciding for them, and say what you would use it for.

**Never reproduce a paywalled publisher's own figures.** A Which? or
RTINGS chart is the paid product; screenshotting it, and redrawing it as
your own graphic, are the same act. Cite the verdict, describe the method,
and let `product-verdicts.md`'s rule govern the rest.

## Downloaded, resized, and local

Self-containment already forbids hotlinking, and two measurements make the
handling specific:

- **Download into `assets/` and reference relatively.** A remote `<img>`
  is a live dependency on someone else's CDN, on a page meant to outlast
  it, and it leaks the reader's request to a third party.
- **Resize to the width it displays at** before wiring it in. A 1408px
  hero delivered for a 720px slot is bytes nobody sees, and a page with
  three of them is several megabytes.
- **Nothing generated goes in the hero.** A full-width image at the top
  pushes the finding below the fold, which costs more than the picture is
  worth. Imagery sits after the finding, or beside it.

One CSS trap, measured elsewhere and cheap to hit here: an `<img>` with
**both** a `height` attribute and a CSS `aspect-ratio` has two definite
dimensions, so `aspect-ratio` is ignored and the picture renders
distorted. Set `height: auto` in the style and let the attribute seed the
intrinsic ratio.

## Generated stills — where they earn it

`media-gen-pro`'s `generate_image` is for the picture prose cannot carry:
a mechanism drawn as a diagram, a comparison of two physical
arrangements, a scene establishing a subject with no photographable form.

- **Never for charts, numbers, labelled diagrams, tables, or anything with
  exact text.** Image models garble those, and re-prompting garbles them
  differently. A number in a generated image is a fabricated number.
- **Diagrams and vector artwork use `svg: true`**, which routes to a
  vector model and returns editable source that scales without resampling
  and keeps its text as text. The raster models can only imitate one.
- **Hold one visual language across the set.** Pass the page's first
  accepted illustration back as `referenceImages` on every subsequent
  call, and put the page's palette and register in `context`. A page whose
  four illustrations were each prompted from scratch has four styles, and
  it reads as four sources rather than one author.
- **Say what a run will spend before spending it.** Each image is a billed
  call.

## Generated video — the narrow case

`generate_video` exists and is the most expensive thing in this pipeline,
so the bar is the motion bar, not the imagery bar: a clip earns its place
only when **the change over time is the evidence** — a mechanism that only
reads while moving, an assembly, a physical process. Anything a still with
an annotation can carry gets the still.

When one is genuinely right:

- **Image-to-video.** Generate the still first, accept it, then pass it as
  `sourceImage` so it becomes the first frame. This is the only reliable
  way to keep a subject consistent, and it means the poster frame and the
  clip agree by construction.
- **Short.** Five seconds, one subject, one simple motion, one camera
  move. Several short clips beat one long one, and every model handles
  complex multi-action animation badly.
- **The poster frame is the static fallback**, and it is the frame that
  prints and that a reduced-motion reader gets. Author it as a real
  figure with its own caption.
- **Never autoplaying with sound; never autoplaying under reduced
  motion.** `muted`, `playsinline`, visible `controls`, `preload="none"`,
  and a `poster`. Under `prefers-reduced-motion: reduce` it does not
  start on its own.
- **No claim lives only in the clip.** Whatever it shows is also stated in
  the prose and available in the poster's caption, because a reader with
  the video blocked, printing the page, or on a metered connection is
  reading the same argument.
- **Weight it honestly.** A clip is hundreds of kilobytes to megabytes
  against a page budget aiming at zero network requests. It goes in
  `assets/`, lazily, below the finding, and its cost goes in the methods
  note beside its provenance.

Say the spend before the call, and report the actual after.

## The review, before it ships

Imagery fails if:

- an image on the page has no caption, no provenance, or no registry row
- a generated asset is not labelled as generated
- alt text names the object rather than the evidence
- a figure was taken from a paywalled publisher
- the licence basis for any asset cannot be stated in a clause
- a raster is served wider than it displays
- the subject has a visible form and the page shows none of it
- a video autoplays, carries sound, or holds a claim the prose does not
