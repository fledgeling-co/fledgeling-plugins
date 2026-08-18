# Imagery — from the sources, and generated

A document whose argument is its evidence has an obvious use for pictures
and a specific way of getting them wrong. This file covers where an image
may come from, what it has to carry to be publishable, and what the PDF
does to all of it.

Two standing requirements sit behind everything here:

> **Where the evidence trail contains images, the report uses them.** A
> report about a product, a device, an interface, a rendered page or a
> document that renders as pure typography has thrown away evidence the
> session already gathered.

> **An image is a claim, so it carries provenance.** Caption, source row,
> and the same registry the prose cites. An uncaptioned picture in an
> evidence document is the one element that asserts something with no
> attribution at all.

## Where an image may come from

In priority order. Take the highest one available and record which.

1. **A render or screenshot the session itself produced.** The strongest
   option in this skill, because it is the same class of evidence as a
   command's output: it was made here, it can be remade, and the ledger
   already has a row shape for it (`kind: "render"`).
2. **The vendor's or publisher's own press asset.** A media kit, a
   newsroom, a product page's own hero, an official spec drawing.
   Published to be used, and the licence terms are usually stated on the
   page you took it from.
3. **A figure the source published for reuse** — an openly-licensed
   diagram, a standards-body illustration, a paper's figure under a licence
   that permits it. Record the licence.
4. **A generated illustration or diagram** via `media-gen-pro`, where the
   picture depicts a *concept* rather than showing a real object.
5. **An honest placeholder** naming what is missing, when the asset does
   not exist and cannot be made truthfully.

**Not on the list, and not admissible:** an image found by search with no
traceable origin, a photograph lifted from a review site, a competitor's
marketing composite, a still cropped out of a video, and anything whose
licence you cannot state in a clause. A report leaves the terminal and
gets forwarded; "it was on the internet" is not a basis.

## The four things every image carries

```html
<figure class="fig">
  <img src="assets/queue-depth-panel.png" width="960" height="540"
       alt="The dashboard at 3,000 events/min, with the drop counter at
            6.88% and the retry gauge pinned at its ceiling."
       loading="lazy" decoding="async">
  <figcaption>
    The panel at the ceiling — the retry gauge is what pins first.
    <span class="prov">Captured from staging, 9 Aug 2026<a class="cite"
      href="#r7" data-cite="r7" data-n="7" aria-describedby="r7">7</a></span>
  </figcaption>
</figure>
```

1. **A caption that says what it is** — the thing shown and why it is
   here, not a repetition of the heading above it.
2. **Provenance in the caption**, with a citation marker into the shared
   registry. The registry row records the origin and the date like any
   other source.
3. **Alt text describing what matters about it**, not what it is of. "The
   dashboard at 3,000/min with the drop counter at 6.88%" carries the
   evidence; "a screenshot of a dashboard" carries nothing.
4. **Explicit `width` and `height`** matching the file, so the box is
   reserved before the image lands and the page does not reflow.

**Generated assets say so in the caption**, in words a skimming reader
cannot miss: *"Illustration, generated"*. An illustration a reader could
mistake for a photograph of the thing under discussion is a provenance
failure, not a decoration choice — the same rule the ledger applies to
numbers.

## Licensing, plainly

Record the basis for every image in its registry row: `captured here`,
`press kit`, `CC BY 4.0`, `public domain`, `generated`, `vendor drawing`.
Where the basis is unclear, **do not ship the image** — describe the thing
in prose and say a picture was not available on terms the report could use.
That sentence costs nothing.

This is a production rule, not legal advice. Where a case is genuinely
borderline, put it to the user rather than deciding for them, and say what
you would use it for.

**Never reproduce a paywalled publisher's own figures.** A Which? or
RTINGS chart is the paid product; screenshotting it and redrawing it as
your own graphic are the same act. Cite the verdict, describe the method,
and let `product-verdicts.md`'s rule govern the rest.

**Never let the working path into an image's provenance.** The same rule
that governs source labels governs captions: cite the path as the reader's
repo sees it, or cite nothing. A caption reading `./fixture/dashboard.png`
tells the reader you analysed a fixture.

## What the PDF does to imagery

Three measurements, each from putting a real generated image through the
whole path:

- **Resize to the width it displays at** before wiring it in. A 614KB hero
  arrived at 1408px for a slot half that wide and nearly doubled the PDF on
  its own; a report with three of them is several megabytes of attachment.
- **The finding still comes first.** A full-width image at the top pushes
  the conclusion below the fold on screen and onto page two in print, which
  costs more than the picture is worth. Imagery sits after the finding, or
  beside it.
- **The figure and its caption are one `<figure>` with
  `break-inside: avoid`**, or the printer separates them and the caption
  opens the next sheet describing something the reader can no longer see.

Two more that only show up in the exported file:

- **Assets live in `assets/` and are referenced relatively.** The HTML
  stays readable, and the exporter embeds them at PDF time. A remote
  `<img>` is a live dependency on someone else's CDN in a document meant to
  outlast it, and it leaks the reader's request to a third party.
- **An `<img>` with both a `height` attribute and a CSS `aspect-ratio` has
  two definite dimensions**, so `aspect-ratio` is ignored and the picture
  renders distorted. Set `height: auto` in the style and let the attribute
  seed the intrinsic ratio.

## Generated stills — where they earn it

`media-gen-pro`'s `generate_image` is for the picture prose cannot carry: a
mechanism drawn as a diagram, a comparison of two physical arrangements, a
scene establishing a subject with no photographable form.

- **Never for charts, numbers, labelled diagrams, tables, or anything with
  exact text.** Image models garble those, and re-prompting garbles them
  differently. A number in a generated image is a fabricated number.
- **Diagrams and vector artwork use `svg: true`**, which routes to a vector
  model and returns editable source. It scales without resampling, keeps
  its text as text, and survives print at any size — which the raster
  imitation of a diagram does not.
- **Hold one visual language across the set.** Pass the report's first
  accepted illustration back as `referenceImages` on every subsequent call,
  and put the design system's palette and register in `context`. Four
  illustrations each prompted from scratch have four styles, and the
  document reads as four sources rather than one author.
- **Say what a run will spend before spending it.** Each image is a billed
  call.

## Generated video — the narrow case, and it is screen-only

`generate_video` exists, it is the most expensive thing in this pipeline,
and a report's primary artifact is a document that prints. So the bar is
higher here than on a page: a clip earns its place only when **the change
over time is the evidence** — a mechanism that only reads while moving, a
failure reproducing, a process unfolding — and even then it is an
enhancement on the screen rendering of a document whose PDF must carry the
same argument without it.

When one is genuinely right:

- **Image-to-video.** Generate or capture the still first, accept it, then
  pass it as `sourceImage` so it becomes the first frame. The poster frame
  and the clip then agree by construction, and a subject stays consistent
  across clips.
- **Short.** Five seconds, one subject, one simple motion, one camera move.
  Several short clips beat one long one; every model handles complex
  multi-action animation badly.
- **The poster frame is the printed figure.** Author it as a real figure
  with its own caption, and let it double as the reduced-motion branch —
  the same static-frame contract every moving block already ships under.
- **Never autoplaying with sound; never autoplaying under reduced
  motion.** `muted`, `playsinline`, visible `controls`, `preload="none"`,
  and a `poster`.
- **No claim lives only in the clip.** Whatever it shows is stated in the
  prose and visible in the poster, because the reader printing this, or
  reading the PDF you emailed, is reading the same argument.
- **Weight it honestly.** A clip is hundreds of kilobytes to megabytes
  against a document aiming at zero network requests, and it does not go in
  the PDF at all. Its cost and its provenance go in the methods note.

Say the spend before the call, and report the actual after.

## The review, before it ships

Imagery fails if:

- an image has no caption, no provenance, or no registry row
- a generated asset is not labelled as generated
- alt text names the object rather than the evidence
- a figure was taken from a paywalled publisher
- the licence basis for any asset cannot be stated in a clause
- a raster is served wider than it displays, or the PDF gained megabytes
- a figure and its caption can separate across a page break
- the evidence trail holds a render the argument needs and the report shows
  none of it
- a video autoplays, carries sound, or holds a claim the poster and the
  prose do not
