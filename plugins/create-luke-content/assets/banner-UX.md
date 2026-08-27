# Banner UX & Readability Specification: create-luke-content

## 1. Cognitive Ergonomics & Scannability
- **3-Second Scan Value:** A developer or founder glancing at the banner card in marketplace listings or the GitHub README immediately grasps:
  1. *What it is:* The canonical Luke Rhodes ghostwriting skill.
  2. *What changed:* It now carries an empirical B2B copywriting research layer under the marketing route.
  3. *Why it matters:* Replaces adjectival fluff with concrete outcome-mechanism pairing, explicit limitation disclosures, and verified numbers.
- **Read-Mode Contrast & Visual Density:**
  - High figure-ground separation between the wordmark and the porcelain field (>14:1 contrast ratio).
  - Badges use pill containers with 1px border and soft background tint for distinct cognitive chunking.
  - Zero text overlap with icon artwork.

## 2. Accessibility & Retinal Precision
- **Render target:** Native CSS `@media (-webkit-min-device-pixel-ratio: 2)` / viewport 1600×520 @ 2x → 3200×1040 PNG.
- **Font rendering:** Sub-pixel antialiasing with explicit fallback stacks: `-apple-system, BlinkMacSystemFont, "SF Pro Display", "Inter", "Segoe UI", sans-serif`.
- **Zero layout distortion:** Flexbox layout with fixed gutters, no horizontal scroll, explicit container padding (64px).
