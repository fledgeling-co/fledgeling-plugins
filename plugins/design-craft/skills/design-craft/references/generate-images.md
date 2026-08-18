# Generate Images: Raster Art via an Image Backend

Generate original raster images — conceptual scenes, characters and mascots, hero/section art, textures, app icons, and genuine infographics — when a design lands better with a real picture than a placeholder. Use this whenever a flow (deck, prototype, hi-fi mockup, doc) has decided it wants imagery; this procedure resolves *how* to generate, not *whether*.

**Imagery is opt-in, not reflexive.** A clean placeholder beats a bad generated attempt. Generate only when the content earns a picture.

## Phase 1: Offer the choice up front

Fold one imagery question into the flow's opening clarifying round:

- Whether to add imagery at all, and in what style — recommend a direction from the source material and the chosen aesthetic.
- **Always include a "none / minimal" option.** Asking late means regenerating everything late.
- If the content clearly won't benefit (dense data UI, terse internal review, an explicit "keep it minimal"), skip the question and proceed without imagery.

## Phase 2: Divide the labor — the medium gate

Route each visual to the right medium by **editability and exactness**, not by whether it contains text:

- **HTML/CSS owns** anything that must stay live-editable, selectable, pixel-exact, or data-bound: tables the user will edit, exact financial figures, charts bound to real numbers, dense small print. These change after generation; a bitmap can't.
- **Generation owns** what raster is good at: conceptual metaphors, characters/mascots, hero and section art, textures, and genuine infographics whose narrative labels don't need data-exactness.
- **Don't avoid text out of fear.** Modern backends render text reliably — including CJK. Text-rich infographics with headings, labels, and callouts are a good use of generation; don't shrink labels or strip copy to dodge rendering errors that no longer happen.

**The medium is decided by what the region *shows*, never by what feels buildable in the current stack.** This is where an approved design most often dies quietly, so it's a gate rather than a preference:

- **A human figure, a product object, machinery, or any material with lighting and depth is raster, whatever the stack.** So is any texture named as one — woven cloth, paper grain, fabric, leather, brushed metal — and it needs no depth argument to qualify. A CSS gradient is not a texture medium, and "layered CSS textures" is not a medium at all.
- Writing "silhouette" for a photographic figure, or "CSS" for a sculpted panel's finish, isn't a medium choice — it's the quiet deletion of the design, and it's how a page full of physical material becomes a flat page with the same section order.
- **Style doesn't move the boundary.** A region with perspective, shading, figure drawing, or dense mechanical detail is *illustration* however line-drawn it looks, and no build session authors illustration as vectors. An instruction-manual world doesn't convert its illustrations into diagrams; it makes them line-art illustrations, generated.
- **Authored SVG covers what a session can specify exactly** — diagrams with countable elements, controls, flat shape systems, crisp vector geometry, animated linework — and it ends where drawing skill begins.
- **The gate runs both ways.** Precise geometry, hard-edged shape systems, diagrams, expressive motion, shaders, and anything interactive are vector and GPU territory (SVG, canvas, WebGL), where a raster flattens what should move, scale, and respond. Choosing code there is ambition, not economy.
- **Dropping an image-native region is a scope decision the user makes, never a silent flattening after the fact.**

**Fields and textures carry a quantity commitment.** When a region is built from many small elements, write down its approximate density and coverage before building — "thousands of glyphs over two-thirds of the fold, dense at the top, fading into the path". A field rebuilt at a tenth of its density passes every checklist and still isn't the design.

Keep **one shared style/identity block** — medium, palette, lighting, character description, mood — reused verbatim across every generated image in a project. Per-image prompts written independently produce a set that looks like it came from five different artists.

## Phase 3: Resolve the backend — once, in this order

1. **User-named backend.** If the user names a backend in this request, use it.
2. **Session tool inventory.** Search the available tools and skills for an image-generation capability — an MCP tool or an installed skill (names vary: `generate_image`, `imagegen`, `image_generate`, a `*-image-gen` skill). If deferred tools are in play, query them (e.g. `ToolSearch` with "image generation") before concluding nothing exists. If a match is found, use it — and note its quirks:
   - Some take an aspect-ratio parameter; others need dimensions stated in the prompt text.
   - Some write to a managed location you must move the file out of afterward.
3. **None available → ask.** Tell the user no image backend is available and ask how to proceed: install one, point at one, or switch to the none/minimal path. **Never silently fall back.**

Resolve once per project, not per image — re-detecting mid-flow risks a style break from a backend switch.

## Phase 4: Write the prompt file first

Before invoking any backend, write each image's full, final prompt to `prompts/NN-{type}-{slug}.md` (e.g. `prompts/01-hero-launch-scene.md`). The prompt file is the reproducibility record: it lets you regenerate after a bad roll, swap backends without rewriting anything, and lets the user read exactly what produced each image.

Each prompt file contains:

```md
# 01 — hero — launch-scene    (aspect 16:9, → imgs/01-hero-launch-scene.png)

## Style (shared across project)
Flat editorial illustration, warm cream ground, terracotta + deep-blue
accents, soft grain, no outlines. Characters: round-faced, simple limbs.

## Scene
A small rocket lifting off a desk between coffee cup and keyboard,
papers swirling. Camera slightly low. Empty upper-left third for headline.

## Text to render (verbatim)
"Launch day" — hand-set caps, bottom-right.
```

- The **style block** is identical in every file — copy it, don't rephrase it.
- **Every string that must appear in the image goes in verbatim** — exact characters, exact casing. The backend renders what it's given; paraphrased labels come out paraphrased.

## Phase 5: Generate and place

- Invoke the resolved backend with the prompt-file content. Save (or move) the output to `imgs/NN-{type}-{slug}.png`, alongside `prompts/`, inside the project directory — deliverables stay self-contained, and the matching NN makes prompt→image traceable.
- Place images on white or contrasting areas so they don't melt into the background.
- Full-bleed art aspect-**fills** its container (`object-fit: cover`); screenshots and diagram-like images aspect-**fit** (`object-fit: contain`) so nothing informative is cropped.

## Phase 6: Verify every image

- **View each generated file** with the Read tool — actually look at it. Check: the subject is right, the style matches the shared block, every required string rendered correctly.
- **Uncanny-valley check on anything depicting people or creatures.** Viewers reject almost-right humans pre-verbally, before they can say why. Look specifically at: faces (asymmetry, dead eyes, misplaced features), hands (finger count, joint angles), teeth, and skin texture that's too smooth or too waxy. A stylized illustration that's clearly not aiming at realism is safe; a photorealistic face that's 95% right is worse than either — regenerate with a more stylized prompt or crop the problem out of frame.
- **Confirm it loads in the artifact** — open the embedding HTML and verify no broken-image icon. A wrong relative path fails silently until someone looks.
- **Wrong text → regenerate, never paint over.** If a label came out wrong, tighten the prompt file (quote the exact string more explicitly, reduce competing text) and regenerate. Don't patch the bitmap with overlaid HTML text or image edits — the seam always shows, and the prompt file stops being the record of the image.
- **Edit the prompt file, then regenerate from it** — never invoke with an ad-hoc tweaked prompt that the file doesn't contain, or the record and the image diverge.
- **The produced material has to survive to the screen.** Check the composite, not the asset: a texture buried under a near-opaque colour wash ships the wash, and an asset applied at near-zero opacity or hidden behind other paint is a compliance token, not a shipped material. Judge every asset in the rendered screenshot beside what it was supposed to be.

## Generation context travels with the asset

A build composed by a session that never saw the prompts places assets it doesn't understand. Keep `prompts/NN-*.md` next to `imgs/NN-*.png` with matching numbers, and read the prompt before composing with the image — especially when the image was produced in a different pass or by a delegate. The prompt file is what makes the asset legible to whoever places it.

## Hard rules

- **Never substitute SVG, HTML, or canvas for a raster you decided to generate.** If no backend resolves, fall through to asking the user — do not emit `<svg>` or CSS art as a stand-in. This holds even for "diagram-like" content; the calling flow already decided it wants a raster, and a hand-drawn SVG imitation is exactly the AI-slop look this skill exists to avoid.
- **Prompt file before invocation, every time.** An image with no prompt file is unreproducible and unswappable.
- **One style block per project.** New images join the existing block; they don't get a fresh one.

## Summarize

Report: which backend was resolved and how (named / found in inventory / asked); the list of `prompts/` ↔ `imgs/` pairs; any image that needed regeneration and why; anything you could not verify visually.
