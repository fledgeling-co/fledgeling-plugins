# Site craft and interactive behavior

Load `design-craft:design-craft` and `ux-craft:ux-craft`, then implement the selected direction in the existing project stack. The approved product and audience determine the palette, typography, section structure and demonstrations.

## Choose interactions by purpose

List each requested interaction, its inputs, output and accessible alternative before coding. A pricing toggle must update approved terms; a feature demonstration must show the claimed behavior. Simulated values are labeled as a demonstration. Do not add telemetry, platform tabs or a calculator merely because a reference page contains them.

## GSAP and scroll motion

Use the project's installed GSAP version or verify the supported package version before adding it. If loading from a CDN, pin the selected version and respect the project's content-security policy. Content is visible with JavaScript disabled and after dependency failure.

A reduced-motion CSS media query alone does not disable JavaScript animation. Use GSAP's supported media-query lifecycle or an explicit `matchMedia` branch to skip nonessential tweens, restore readable static states and clean up when the preference changes. Test that branch in a browser that supports media emulation, or record it as unverified.

## Three.js or WebGL

Include 3D when requested or when spatial change communicates the product. Handle resize, cap device pixel ratio to a deliberate budget, dispose resources on unmount and pause the render loop when hidden or offscreen. Provide a static fallback for unavailable WebGL and reduced motion. Do not promise zero CPU use or a frame rate without a relevant measurement on a named device.

## Rendered acceptance

For the page's actual target viewports and supported themes:

- Open the rendered page and inspect text, imagery, hierarchy, overflow and overlap.
- Exercise the named controls with pointer and keyboard, including focus and error/empty states where relevant.
- Check text contrast against the rendered background using the applicable WCAG criterion: ordinarily 4.5:1 for normal text and 3:1 for large text, with control boundaries assessed separately.
- Confirm dependency loading, the no-script or failure fallback, reduced motion and any offscreen pause behavior.
- Confirm every platform badge and price matches the approved claims ledger.

Source substring checks do not establish any of these rendered results. Use one evidence set for overlapping design gates and recheck affected behavior after a repair. If a browser capability is unavailable, state exactly which criterion remains unverified.
