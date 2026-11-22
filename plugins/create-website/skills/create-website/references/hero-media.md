# Hero media: the image, and where 3D comes from

## A generated hero image

Route through `design-craft:design-craft` → `references/generate-images.md`: offer imagery as a
choice, decide the medium by what the region shows, write the prompt file first, generate, then
open and check every image. The `media-gen-pro` server's `generate_image` takes `prompt`,
`context`, `aspectRatio` or `size`, `n` (each billed, capped at 4), `referenceImages`, `seed`,
`outputDir`, `basename`, and `style` (the model; leave it out unless the person named one). It
reports which model served the request; record that beside the prompt.

- **Concepts on a contact sheet.** Where the choice is real, generate three or four, tile them on
  one sheet, and put the sheet to `decision-panel:decision-panel` when the call is technical
  (legibility under the headline, crop survival on a phone). The pick between two good ones is
  taste, and the person makes it.
- **Keep the master, ship display sizes.** Export AVIF or WebP at the sizes the layout uses, with
  `<picture>`, `srcset` and `sizes`, and make a separate phone crop when automatic cropping would
  cut the subject. Reserve the box with width and height or `aspect-ratio`.
- **Alt text from the approved image**, never from the prompt that made it. A caption that says
  what an image stands for is copy about the subject: ground it in the person's material and
  check it against the picture. The first caption drafted in the source session described its
  image wrongly.
- **Credit is the person's choice.** Ask whether a generated image says so on the page.
- **Generate during authoring, never per visit.** Approved assets ship with the site, and no
  provider credential reaches the browser.

## Where the 3D comes from

Decide this before building, and record it in `plan.hero.threeD`. Climb design-craft's depth
ladder (`references/depth-and-3d.md`) only as far as the brief needs; each rung costs more
performance and accessibility risk than the last.

| Source | Use it when | What ships |
|---|---|---|
| `generated-image` | The 3D look is the point and nothing needs to move or respond: a rendered object, a diorama, an isometric scene | A still from `generate_image`, art-directed as a render, with optional CSS tilt or scroll depth |
| `css-depth` | One object or a layered scene should feel touchable, or sections should part in depth as the page scrolls | CSS 3D transforms and scroll-driven translate and scale, no WebGL |
| `three-scene` | The object is the content and the visitor gains by turning or exploring it, or the scroll drives a camera through a scene | A three.js scene with a still fallback |
| `mesh-generator` | A mesh generator turns out to be connected in this run (none was when this skill was written) | Its glTF, through the asset pipeline below, inside a `three-scene` |

`hero.threeD.why` says what a real-time scene shows that a still, CSS depth or scroll depth
cannot. If the answer is "it looks impressive", take `generated-image` or `css-depth`.

## A three.js scene

Sources for each rule are in `evidence.md` under "WebGL".

- **Check before you build the renderer.** Current `WebGLRenderer` needs WebGL 2 (WebGL 1 support
  ended in r163). Test with `WebGL.isWebGL2Available()` from `three/addons/capabilities/WebGL.js`;
  when it is false, show the still and skip downloading the model and its decoders. `site_audit.py`
  fails a page that creates a context with no check or fallback.
- **Cap the drawing buffer.** `renderer.setPixelRatio(Math.min(devicePixelRatio, 2))`; a pixel
  ratio of 3 draws nine times the pixels of 1 at the same CSS size. Start constrained devices
  lower (1 to 1.5) and measure.
- **Render on demand, and stop when nobody is looking.** A scene that is not changing does not
  need a frame. Pause the loop when the canvas leaves the viewport (IntersectionObserver) and when
  the tab is hidden (`visibilitychange`), and resume without a jump from accumulated time.
- **Context loss is an expected failure.** Listen for `webglcontextlost` on
  `renderer.domElement`, call `preventDefault()`, stop the loop and show the still; rebuild on
  `webglcontextrestored` or stay on the still. Dispose geometries, materials, textures and the
  renderer when the scene unmounts; garbage collection does not free GPU memory.
- **Reduced motion stops decorative camera travel, rotation and parallax.** Show the still, or a
  static frame of the scene.
- **Make the canvas accessible through HTML.** A decorative canvas gets `aria-hidden="true"`. A
  meaningful one gets a name (`role="img"` and `aria-label`, or a labelled region) and its
  controls and information as real HTML beside it; an `aria-label` does not expose controls drawn
  inside a canvas. Keep headings, links and calls to action out of the canvas. A drag-to-rotate
  needs buttons that do the same.
- **Headless engines are not the scene's judge.** A headless browser without 3D reports a WebGL
  error that is the engine's, not the page's; the no-WebGL capture pass checks the fallback, and a
  real browser checks the scene.

## glTF delivery

Run the asset through `gltf-transform` before it reaches the page: prune, dedup, resize textures
(1024 px for secondary models, 2048 px at most for the hero), compress geometry, and convert
textures to KTX2.

- **Geometry: compare Meshopt and Draco on the actual asset.** Meshopt compresses animation and
  morph targets as well as geometry and has a much smaller decoder; Draco can be smaller on a
  dense static mesh. Count the decoder's download and decode time, since a smaller file is not a
  faster first frame. Wire the matching `GLTFLoader` decoder (`setMeshoptDecoder` or
  `DRACOLoader`).
- **Textures: KTX2 with Basis Universal.** ETC1S for colour maps, UASTC for normal maps and other
  non-colour data. A PNG or JPEG texture is decoded to raw RGBA in GPU memory: 2048 × 2048 × 4
  bytes is about 16.8 MB before mipmaps, which is how a phone runs out of memory long before the
  network is the problem. Wire `KTX2Loader` with its transcoder.
- **Count everything.** The model, its textures, environment maps, decoders and transcoders all
  load. One research member proposed a 1.5 to 2.5 MB above-the-fold budget and mobile ceilings of
  about 50 draw calls and 100,000 to 150,000 triangles; another found no source that establishes
  any universal ceiling. Treat those numbers as a starting policy, read `renderer.info` for the
  real counts, and measure on a phone.
