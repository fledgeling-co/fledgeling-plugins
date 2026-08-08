# Scroll-reactive three.js particle hero

Here's the hero, set up and ready to drop in. Vanilla-module version first (works in any HTML page), React/Next wrapper after it, then the things worth deciding before you ship it.

One flag up front, because it affects what you actually want to build: a generic particle field is decoration — it looks expensive but it says nothing about citation click-through. Since the whole subject of the page is *readers not following the link*, the same particle system can be made to carry that number at no extra cost. I've built the decorative version you asked for as the primary, and included the data-carrying variant at the end as a ~20-line diff. Your call which ships.

---

## 1. Install

```bash
npm install three
```

Modern three.js (r160+). If you're on a plain HTML page with no bundler, use an import map instead:

```html
<script type="importmap">
{ "imports": { "three": "https://unpkg.com/three@0.171.0/build/three.module.js" } }
</script>
```

## 2. Markup

The canvas sits behind the hero copy. The hero element is the scroll reference — progress is measured against *it*, not the whole document, so the effect still works if you later move the hero down the page.

```html
<section id="hero" class="hero">
  <canvas id="hero-canvas" aria-hidden="true"></canvas>
  <div class="hero__content">
    <h1>Nobody clicks the citation.</h1>
    <p>Click-through rates on inline sources, measured across 1.2M article reads.</p>
  </div>
</section>
```

```css
.hero {
  position: relative;
  min-height: 100svh;      /* svh, not vh — avoids the mobile URL-bar jump */
  display: grid;
  place-items: center;
  overflow: hidden;
  background: #07080c;
}

#hero-canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
}

.hero__content {
  position: relative;   /* above the canvas */
  z-index: 1;
  text-align: center;
  max-width: 44rem;
  padding: 0 1.5rem;
  color: #f4f6fb;
}
```

## 3. The hero module

Save as `hero-particles.js`.

```js
import * as THREE from 'three';

/**
 * Scroll-reactive particle field.
 * @param {HTMLCanvasElement} canvas
 * @param {HTMLElement} section  scroll reference (the hero element)
 * @returns {() => void} dispose
 */
export function createParticleHero(canvas, section, options = {}) {
  const {
    count       = window.innerWidth < 768 ? 2500 : 6000,
    colorNear   = '#8fa6c9',   // cool, receding
    colorFar    = '#e8b155',   // warm accent — swap for your brand
    pointSize   = 7.0,
    dispersion  = 1.0,         // how far particles fly apart at full scroll
  } = options;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- renderer -------------------------------------------------------
  const renderer = new THREE.WebGLRenderer({
    canvas,
    alpha: true,
    antialias: false,            // points are round-masked in the shader; MSAA buys nothing
    powerPreference: 'high-performance',
  });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  const scene  = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(55, 1, 0.1, 200);
  camera.position.z = 22;

  // ---- geometry -------------------------------------------------------
  const positions = new Float32Array(count * 3);
  const scatter   = new Float32Array(count * 3);
  const seeds     = new Float32Array(count);

  for (let i = 0; i < count; i++) {
    const i3 = i * 3;

    // Home position: a wide, shallow slab so it reads as a field, not a ball.
    positions[i3 + 0] = (Math.random() - 0.5) * 38;
    positions[i3 + 1] = (Math.random() - 0.5) * 22;
    positions[i3 + 2] = (Math.random() - 0.5) * 18 - 5;

    // Scatter vector: where this particle drifts to at scroll = 1.
    // Biased outward and slightly toward camera so the field opens up.
    const theta = Math.random() * Math.PI * 2;
    const mag   = (2 + Math.random() * 9) * dispersion;
    scatter[i3 + 0] = Math.cos(theta) * mag;
    scatter[i3 + 1] = Math.sin(theta) * mag * 0.55;
    scatter[i3 + 2] = (Math.random() * 0.8 + 0.2) * mag * 0.7;

    seeds[i] = Math.random();
  }

  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
  geometry.setAttribute('aScatter', new THREE.BufferAttribute(scatter, 3));
  geometry.setAttribute('aSeed',    new THREE.BufferAttribute(seeds, 1));

  // ---- material -------------------------------------------------------
  const uniforms = {
    uTime:       { value: 0 },
    uScroll:     { value: 0 },
    uSize:       { value: pointSize },
    uPixelRatio: { value: renderer.getPixelRatio() },
    uColorNear:  { value: new THREE.Color(colorNear) },
    uColorFar:   { value: new THREE.Color(colorFar) },
  };

  const material = new THREE.ShaderMaterial({
    uniforms,
    transparent: true,
    depthWrite: false,                 // additive points need no depth sort
    blending: THREE.AdditiveBlending,
    vertexShader: /* glsl */`
      uniform float uTime;
      uniform float uScroll;
      uniform float uSize;
      uniform float uPixelRatio;

      attribute vec3  aScatter;
      attribute float aSeed;

      varying float vAlpha;
      varying float vTint;

      void main() {
        // Scroll drives dispersion: clustered field -> open field.
        vec3 pos = position + aScatter * uScroll;

        // Idle drift so it never looks frozen when the user stops scrolling.
        float t = uTime * 0.15 + aSeed * 6.2831853;
        pos.x += sin(t) * 0.4;
        pos.y += cos(t * 0.8) * 0.4;

        vec4 mv = modelViewMatrix * vec4(pos, 1.0);
        gl_Position = projectionMatrix * mv;

        float dist = max(-mv.z, 0.001);
        gl_PointSize = clamp(uSize * uPixelRatio * (12.0 / dist), 1.0, 64.0);

        // Nearer particles are brighter and warmer; field thins as it disperses.
        vTint  = smoothstep(40.0, 6.0, dist);
        vAlpha = (0.25 + aSeed * 0.75) * vTint * (1.0 - uScroll * 0.55);
      }
    `,
    fragmentShader: /* glsl */`
      uniform vec3 uColorNear;
      uniform vec3 uColorFar;

      varying float vAlpha;
      varying float vTint;

      void main() {
        // Round, soft-edged point. Cheaper and sharper than a sprite texture.
        float d = length(gl_PointCoord - 0.5);
        if (d > 0.5) discard;
        float mask = smoothstep(0.5, 0.05, d);

        vec3 color = mix(uColorNear, uColorFar, vTint * vTint);
        gl_FragColor = vec4(color, mask * vAlpha);
      }
    `,
  });

  const points = new THREE.Points(geometry, material);
  scene.add(points);

  // ---- sizing ---------------------------------------------------------
  // Cached so the rAF loop never forces a layout read.
  let sectionTop = 0;
  let sectionHeight = 1;

  function measure() {
    const rect = section.getBoundingClientRect();
    sectionTop = rect.top + window.scrollY;
    sectionHeight = rect.height || 1;

    const w = section.clientWidth;
    const h = section.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.updateProjectionMatrix();
    uniforms.uPixelRatio.value = renderer.getPixelRatio();
  }

  const resizeObserver = new ResizeObserver(measure);
  resizeObserver.observe(section);
  measure();

  // ---- scroll ---------------------------------------------------------
  let targetScroll = 0;   // raw 0..1
  let easedScroll  = 0;   // lerped, what the shader sees

  function readScroll() {
    const raw = (window.scrollY - sectionTop) / sectionHeight;
    targetScroll = Math.min(Math.max(raw, 0), 1);
  }

  window.addEventListener('scroll', readScroll, { passive: true });
  readScroll();

  // ---- loop -----------------------------------------------------------
  const clock = new THREE.Clock();
  let rafId = null;
  let visible = true;

  function frame() {
    rafId = requestAnimationFrame(frame);

    // Critically-damped-ish easing. Frame-rate independent enough for this.
    easedScroll += (targetScroll - easedScroll) * 0.08;

    uniforms.uTime.value   = clock.getElapsedTime();
    uniforms.uScroll.value = easedScroll;

    camera.position.z = 22 - easedScroll * 9;
    points.rotation.y = easedScroll * 0.22;
    points.rotation.x = easedScroll * -0.08;

    renderer.render(scene, camera);
  }

  function start() { if (!rafId && !reduceMotion) frame(); }
  function stop()  { if (rafId) { cancelAnimationFrame(rafId); rafId = null; } }

  // Don't burn GPU on a hero that's scrolled off screen.
  const io = new IntersectionObserver(([entry]) => {
    visible = entry.isIntersecting;
    visible ? start() : stop();
  }, { threshold: 0 });
  io.observe(section);

  if (reduceMotion) {
    // One static frame, no loop, no scroll coupling.
    uniforms.uTime.value = 0;
    uniforms.uScroll.value = 0;
    renderer.render(scene, camera);
  } else {
    start();
  }

  // ---- teardown -------------------------------------------------------
  return function dispose() {
    stop();
    io.disconnect();
    resizeObserver.disconnect();
    window.removeEventListener('scroll', readScroll);
    geometry.dispose();
    material.dispose();
    renderer.dispose();
  };
}
```

## 4. Wire it up

Plain page:

```html
<script type="module">
  import { createParticleHero } from './hero-particles.js';
  createParticleHero(
    document.getElementById('hero-canvas'),
    document.getElementById('hero')
  );
</script>
```

React / Next.js (client component — three.js must not run during SSR):

```tsx
'use client';
import { useEffect, useRef } from 'react';

export function ParticleHero() {
  const canvasRef  = useRef<HTMLCanvasElement>(null);
  const sectionRef = useRef<HTMLElement>(null);

  useEffect(() => {
    let dispose: (() => void) | undefined;
    let cancelled = false;

    // Dynamic import keeps three.js out of the initial bundle.
    import('./hero-particles').then(({ createParticleHero }) => {
      if (cancelled || !canvasRef.current || !sectionRef.current) return;
      dispose = createParticleHero(canvasRef.current, sectionRef.current);
    });

    return () => { cancelled = true; dispose?.(); };
  }, []);

  return (
    <section ref={sectionRef} className="hero">
      <canvas ref={canvasRef} id="hero-canvas" aria-hidden="true" />
      <div className="hero__content">
        <h1>Nobody clicks the citation.</h1>
        <p>Click-through rates on inline sources, measured across 1.2M article reads.</p>
      </div>
    </section>
  );
}
```

## 5. Knobs worth turning

| Option | Effect |
|---|---|
| `count` | Particle density. 6000 is comfortable on a laptop GPU; above ~20000 you'll feel it on integrated graphics. |
| `dispersion` | How violently the field opens on scroll. `0.4` reads as a slow breath, `2.0` as an explosion. |
| `pointSize` | Base point size in CSS pixels at mid-depth. |
| `colorNear` / `colorFar` | The depth gradient. Keep these close in hue or the field reads as confetti. |
| `easedScroll` lerp `0.08` | Lower = heavier, more cinematic lag. Above `0.2` it starts to feel twitchy. |

## 6. What this already handles

- **`prefers-reduced-motion`** — renders one static frame and never starts the loop. This matters more than usual here: a full-viewport moving field is exactly the pattern that triggers vestibular symptoms.
- **Off-screen pause** — `IntersectionObserver` stops the rAF loop once the hero leaves the viewport, so the rest of the page scrolls at full frame rate.
- **No per-frame layout reads** — scroll position is cached from a passive listener and section geometry is re-measured only on resize. A `getBoundingClientRect()` inside the loop is the standard way these heroes end up janky.
- **DPR clamped to 2** — a 3x phone screen would otherwise render 2.25x the fragments for no visible gain.
- **Full teardown** — geometry, material and renderer all disposed; matters in a SPA where the hero unmounts.

## 7. Two things to decide before shipping

**Contrast over the canvas.** Your `h1` sits on top of a moving, additive-blended field, which means its effective background luminance changes as particles drift under it. Check the worst case (a bright cluster directly behind the text), not the average. If it's marginal, put a radial scrim behind `.hero__content`:

```css
.hero__content::before {
  content: '';
  position: absolute;
  inset: -3rem -4rem;
  z-index: -1;
  background: radial-gradient(ellipse at center, rgba(7,8,12,.85), transparent 70%);
}
```

**The WebGL fallback.** If the context fails to create (old device, GPU blocklist, hardware acceleration off), `WebGLRenderer` throws and you get a bare dark section. Wrap the call and set a CSS gradient background on `.hero` as the floor so it degrades to something intentional rather than something empty.

---

## 8. The variant that carries the number

The above is decoration — it reacts to scroll but it's indifferent to the subject. Since your page is about *how rarely readers verify sources*, the same system can encode the actual click-through rate for roughly twenty lines of change, and then the hero is an argument rather than a screensaver.

The idea: each particle is one reader. At scroll 0 they're a single undifferentiated field. As the reader scrolls, the field splits — the small fraction who clicked the citation ignite and converge toward a point of light; the overwhelming majority dim and drift away. The visual asymmetry *is* the statistic, and it's legible before anyone reads a number.

The changes:

```js
// 1. Add a per-particle flag at build time. Swap 0.03 for your real rate.
const CLICK_THROUGH_RATE = 0.03;
const clicked = new Float32Array(count);
for (let i = 0; i < count; i++) clicked[i] = Math.random() < CLICK_THROUGH_RATE ? 1.0 : 0.0;
geometry.setAttribute('aClicked', new THREE.BufferAttribute(clicked, 1));
```

```glsl
// 2. In the vertex shader — clickers converge, the rest disperse.
attribute float aClicked;
varying float vClicked;

vec3 target  = mix(position + aScatter, vec3(0.0, 0.0, 6.0), aClicked);
vec3 pos     = mix(position, target, uScroll);
vClicked     = aClicked;

// Clickers hold their brightness; everyone else fades out.
vAlpha = (0.25 + aSeed * 0.75) * vTint * mix(1.0 - uScroll * 0.85, 1.0, aClicked);
```

```glsl
// 3. In the fragment shader — ignite the ones who clicked.
varying float vClicked;
vec3 color = mix(mix(uColorNear, uColorFar, vTint * vTint), vec3(1.0, 0.94, 0.82), vClicked);
```

Two caveats if you take this route. First, `CLICK_THROUGH_RATE` has to be your real measured figure with the source named in the caption — a hero that visually asserts a number is making a claim, and on a page whose entire thesis is that readers don't check sources, an unsourced one would be self-defeating. Second, a particle field is a *rhetorical* device, not a readable chart: nobody can count 3% of 6000 points. Put the actual figure in the `h1` and let the field do the emotional work. Pair it with a real chart further down the page for anyone who wants the precision.

**Recommendation:** ship the data-carrying variant. It's the same build cost, it survives the "why is there a particle field on this page" question, and it makes the hero the first piece of evidence instead of an unrelated flourish.
