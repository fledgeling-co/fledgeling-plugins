"use client";

import { gsap } from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useGSAP } from "@gsap/react";

gsap.registerPlugin(ScrollTrigger, useGSAP);

/**
 * The site's motion, in one place.
 *
 * The budget is spent on two moments rather than scattered across twenty hover
 * effects: the hero arriving, and the cards arriving as you scroll into a
 * group. Hover stays in CSS, where a 150ms transition belongs — it happens tens
 * of times a session and a timeline would be the wrong instrument for it.
 *
 * Two rules keep this from costing what it is meant to buy:
 *
 * - Entrances are `gsap.from`, so the authored markup is the END state. If the
 *   script fails to parse, or a reader lands before the tween resolves, the
 *   page is simply the page. Nothing here can leave content in a void.
 * - Nothing already on screen is hidden. A card below the fold gets a reveal; a
 *   card the reader is looking at is already readable and animating it in would
 *   be a defect rather than a flourish.
 *
 * `gsap.matchMedia` owns the reduced-motion branch, because the global CSS
 * block in globals.css cannot reach GSAP: it writes inline styles from JS and a
 * `transition-duration` override never sees them.
 */
export function SiteMotion() {
  // No scope: the elements this animates live in sibling trees (the hero in the
  // page, the cards in the roster), so a scoped selector would match nothing.
  useGSAP(() => {
      const mm = gsap.matchMedia();

      mm.add(
        {
          motion: "(prefers-reduced-motion: no-preference)",
          reduce: "(prefers-reduced-motion: reduce)",
        },
        (context) => {
          // Reduced motion is the authored page, untouched. Not a faster
          // version of the animation: no set, no tween, nothing to revert.
          if (context.conditions?.reduce) return;

          gsap.defaults({ duration: 0.55, ease: "power3.out" });

          // The one orchestrated moment. Overlapping starts read composed;
          // strictly sequential ones read like a slideshow.
          const hero = gsap.utils.toArray<HTMLElement>("[data-motion='hero'] > *");
          const [lead, ...rest] = hero;
          if (lead) {
            const tl = gsap.timeline().from(lead, { autoAlpha: 0, y: 10, duration: 0.45 });
            if (rest.length) {
              tl.from(rest, { autoAlpha: 0, y: 16, stagger: 0.07 }, "-=0.28");
            }
          }

          // Cards arriving. Only ones the reader has not reached yet: hiding
          // what is already visible trades readability for a flourish nobody
          // asked for, and strands the content if a trigger never fires.
          const below = gsap.utils
            .toArray<HTMLElement>("[data-motion='card']")
            .filter((el) => el.getBoundingClientRect().top > window.innerHeight * 0.9);

          if (below.length) {
            gsap.set(below, { autoAlpha: 0, y: 18 });
            ScrollTrigger.batch(below, {
              start: "top 92%",
              once: true,
              onEnter: (batch) =>
                gsap.to(batch, {
                  autoAlpha: 1,
                  y: 0,
                  duration: 0.5,
                  stagger: 0.055,
                  overwrite: true,
                }),
            });
          }

          // A group heading is the label for the set under it, so it leads.
          gsap.utils.toArray<HTMLElement>("[data-motion='group-head']").forEach((head) => {
            if (head.getBoundingClientRect().top <= window.innerHeight * 0.9) return;
            gsap.from(head, {
              autoAlpha: 0,
              y: 12,
              duration: 0.45,
              scrollTrigger: { trigger: head, start: "top 92%", once: true },
            });
          });
        },
      );

    return () => mm.revert();
  });

  return null;
}
