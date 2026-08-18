# Component visual regression — story-per-composite, pixel-diffed to a reference crop

This is a **pattern, not a bundled tool.** No script ships for it; this doc is the harness sketch.

## The problem it solves

The slow part of alignment is the loop: **edit → recompile → render the whole page → log in →
navigate → populate data → measure**. Each iteration is tens of seconds to minutes, and you pay
it again every time you touch a shared composite — and the *other* pages reusing that composite
are never re-checked, so a fix for page A can silently regress page B.

## The pattern

Render each **composite** (the card, the stat panel, the list row, the page header — the unit
the mock repeats) in its own **Storybook story**, fed the **reference's** content as fixed
props, and pixel-diff that story against a **cropped image of the corresponding mock section**.
Each check is then sub-second, runs with no app/login/data, and — once it's green — becomes a
**golden-fixture regression harness**: every page reusing the composite is verified in seconds,
and a future change that drifts the composite fails the snapshot instead of shipping.

This complements measurement, it does not replace it. The first time you align a composite you
still do the full method (structure-diff → content-diff → style-diff → overlay) against the
rendered page. The story harness is what makes the *second through Nth* verification — and every
later regression check — cheap.

## Capture the reference crops once

The reference is immutable for the whole pass — crop each composite's region from it **once** and
commit the crops as fixtures:

```bash
# in the served reference, screenshot each composite's bounding box to a fixture file
# `obscura fetch --screenshot` has no element target, so measure the component's box first
# and clip the capture to it over CDP.
obscura --allow-private-network fetch "http://localhost:8770/<mock>.html" \
  --eval "(() => JSON.stringify(document.querySelector('#hero .module-cards').getBoundingClientRect()))()"
#   → pass that box to Page.captureScreenshot as `clip` (with captureBeyondViewport when the
#     component sits below the fold) to write fixtures/visual/module-cards.ref.png
# …one crop per composite, named after the story
```

Render the story at the **same viewport / DPR** as the crop, or the pixel diff is all noise.

## Harness sketch (framework-agnostic)

1. **A story per composite**, fed the reference content as fixed props:
   ```tsx
   // ModuleCards.stories.tsx
   export const AsReference = {
     args: { items: referenceFixture.moduleCards },   // the mock's exact copy/data
   };
   ```
2. **A snapshot test** (Storybook test-runner, or a `node:test` spec driving Obscura against the story iframe) that
   screenshots the rendered story and diffs it against the committed crop:
   ```ts
   // visual.spec.mjs — node:test / Storybook test-runner
   test('ModuleCards matches reference', async ({ page }) => {
     await page.goto(storyUrl('modulecards--as-reference'));
     await expect(page.locator('#storybook-root')).toHaveScreenshot('module-cards.ref.png', {
       maxDiffPixelRatio: 0.01,   // tight; this is design-conformance, not flake-tolerance
     });
   });
   ```
   (Reference-crop and rendered-story must share viewport + DPR; mask any intentionally-dynamic
   region — a live timestamp/avatar — so it doesn't churn the diff.)
3. **Run on every change.** The first green run promotes the crop to the golden baseline; later
   edits that drift the composite fail the diff. Because the story renders the composite in
   isolation, the failing pixels point straight at the composite, not at page chrome.

## Why this is the golden fixture, not just a faster check

- **Reuse verifies for free.** A composite used on six pages is proven once; the other five are
  covered by the same story snapshot — no per-page render/login/navigate.
- **Fixes can't silently regress.** The snapshot is the contract: a later refactor that nudges a
  radius/gap fails CI instead of shipping. This is the regression harness the one-shot alignment
  pass otherwise lacks.
- **No app needed.** Stories run on Storybook's static build — no dev session, no populated
  tenant, no flag.

## Honest boundary

A pixel snapshot is its **own** image baseline — it tells you the composite still matches *the
committed crop*, not that the crop was ever a faithful read of intent. So the measurement pass
(structure/content/style diff) is what establishes the crop is correct in the first place; the
snapshot harness only *holds* it there. Treat a failing snapshot as the trigger to re-measure,
the same way `overlay.mjs` is a trigger and never proof. Keep the crops in sync when the
reference itself changes — a stale fixture certifies drift.
