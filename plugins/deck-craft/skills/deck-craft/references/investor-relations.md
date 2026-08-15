# Investor Relations & Retail Investor Decks — Design, Comprehension, and Engineering

A presentation deck for Investor Relations (IR) operates under constraints that do not exist for product pitches or internal company updates. It is read by **two distinct audiences** with conflicting cognitive strategies: **institutional analysts** (who model the raw numbers, test footnote consistency, and scrutinize GAAP reconciliations) and **retail investors** (who consume visual heuristics, top-line metrics, and strategic narrative). 

In regulated investor communications, **visual polish is a compliance responsibility**. Empirical accounting research (*Rennekamp, JAR 2012*) demonstrates that higher visual fluency produces more extreme valuation reactions in the direction of the news without increasing actual comprehension unless accompanied by strict structural clarity. Fluency without truth is a compliance exposure; truth without clarity leaves retail shareholders uninformed.

Read this reference whenever authoring, reviewing, or generating decks for:
* Quarterly and Annual Financial Results (e.g. ASX 4C/4D/4E, SEC 10-Q/10-K presentations)
* Strategic and Operational Updates
* Capital Allocation Frameworks & Dividend Reinstatement Pathways
* Debt Refinancing, Maturity Profiles, and Balance Sheet Reviews
* Investor Days, Roadshows, AGM Presentations, and Retail Investor SaaS Software

---

## 1. Mathematical Derivation of Typography & Visual Ergonomics

Slide typography is not a matter of subjective taste — it is governed by **human visual acuity and viewing geometry**.

### 1.1 The Closed-Form Legibility Formula (ISO 9241-303 & AVIXA DISCAS)
Under **ISO 9241-303 §5.5**, character legibility is specified as a subtended **visual angle** ($\text{arc-minutes}$):
* **Absolute Minimum**: $16'$ (arc-minutes)
* **Recommended Range**: $20' - 22'$

Combining ISO 9241-303 with **AVIXA DISCAS (Display Image Size for 2D Content)** standards across **Viewing Ratios** ($\text{VR} = \frac{\text{farthest viewer distance}}{\text{image height}}$), with a standard cap-height-to-point-size ratio of $\approx 0.70$ and $3437.75'$ per radian, yields the exact font size in pixels on a $1920 \times 1080$ canvas:

$$\text{font\_px} = \frac{\text{arcmin} \times \text{VR}}{2.228}$$

| Viewing Ratio ($\text{VR}$) | Typical Presentation Context | ISO Minimum ($16'$) | ISO Recommended ($20'$) | ISO Upper ($22'$) |
| :--- | :--- | :--- | :--- | :--- |
| **$\text{VR} = 3$** | **Desktop / Laptop reader @ 600mm** (Retail investor viewing web portal / PDF) | **$22\text{px}$** | **$27\text{px}$** | **$30\text{px}$** |
| **$\text{VR} = 4$** | **Analytical Decision Making** (Dense financial tables, balance sheets) | **$29\text{px}$** | **$36\text{px}$** | **$40\text{px}$** |
| **$\text{VR} = 6$** | **Basic Decision Making** (Standard boardroom table / projected back row) | **$43\text{px}$** | **$54\text{px}$** | **$59\text{px}$** |
| **$\text{VR} = 8 - 10$** | **Auditorium / AGM Hall** (Large investor roadshow / hybrid webcast) | **$57\text{px}$** | **$72\text{px}$** | **$79\text{px} - 96\text{px}$** |

### 1.2 Quantitative Rules for the Type Scale
1. **The $24\text{px}$ Floor is a *Reading Deck* Floor**: For retail investors reading on screens ($\text{VR} \approx 3$), $24\text{px}$ subtends $17.8'$ (clearing the ISO $16'$ minimum). For a boardroom projection ($\text{VR} = 6$), $24\text{px}$ drops to $8.9'$ ($44\%$ below the minimum). A projected deck requires $\ge 44\text{px}$ for core body copy.
2. **The Scientific Defense of the $96\text{px}$ Hero Metric**: At $\text{VR} = 10$ (row 10 in an AGM auditorium), a $96\text{px}$ numeral subtends $21.4'$—clearing the ISO recommended $20' - 22'$ band. The $96\text{px}$ hero stat is the smallest round number that survives the farthest seat in any room.
3. **The Two-Tier Typography Floor**:
   * **Tier 1 — Primary Content Floor ($\ge 24\text{px}$, recommended $28\text{px} - 34\text{px}$)**: Slide titles ($68\text{px} - 104\text{px}$), lead paragraphs ($32\text{px} - 40\text{px}$), body prose ($28\text{px} - 34\text{px}$), hero metrics ($56\text{px} - 96\text{px}$), chart data labels ($28\text{px} - 38\text{px}$).
   * **Tier 2 — Auxiliary / Metadata Floor ($18\text{px} - 20\text{px}$)**: Category eyebrows ($18\text{px}$ uppercase tracking $0.12 - 0.14\text{em}$), tabular data cells ($20\text{px}$), chart axis sub-labels ($20\text{px} - 24\text{px}$), stat descriptive notes ($20\text{px}$), statutory footnotes and timestamps ($20\text{px}$). Do not artificially inflate $18\text{px}$ eyebrows or legal footnotes to $24\text{px}$; doing so flattens visual hierarchy and causes metadata to compete with primary copy.

---

## 2. Narrative Pacing & Cognitive Science

### 2.1 The Coherence Principle vs. The "Minimal Text" Myth
* **Mayer’s Coherence Principle (Empirically verified in 23 of 23 trials, median effect size $d = 0.86$)**: Cutting extraneous decorative graphics, floating icons, and decorative background patterns dramatically improves comprehension and retention.
* **The Standalone IR Inversion**: The classic advice to *"put minimal text on slides"* applies only when a speaker is speaking live. Standalone or emailed IR decks (which retail investors review asynchronously on portals) fail when stripped of narrative context. Standalone IR slides must carry complete declarative headlines and contextual bullet takeaways.

### 2.2 Uncompressed 1-Topic Pacing
Never compress 12 quarterly themes into 8 composite slides. Each key milestone demands its own canvas:
* **Slide 01**: Executive Cover with verified ASX/SEC release date and statutory disclaimer.
* **Slide 02**: Quarterly Highlights ($96\text{px}$ hero metrics: FCF, Net Debt, Revenue, Safety).
* **Slide 03**: Strategic Delivery (Commitments + CEO/CFO quotes with top accent rules).
* **Slide 04**: Primary Revenue Division (Asymmetric split: zero-based chart + full-height photography).
* **Slide 05**: Asset Build / Operational Matrix (Inline progress tracks + commercial allocation chips).
* **Slide 06**: Secondary Division / Softer Market (Honest zero-based decline chart + project landmark).
* **Slide 07**: Restructuring / Cash Improvement (Shared-scale horizontal ROI bar chart).
* **Slide 08**: Net Debt & Balance Sheet Trajectory (3-period debt column chart + chevron seam).
* **Slide 09**: Capital Allocation & Dividend Pathway (Milestone scorecard).
* **Slide 10**: Board & Governance (Director credential cards).
* **Slide 11**: Forward Outlook & Guidance (2-column macro/micro operational narrative).
* **Slide 12**: Corporate Directory, Registry & Disclosures.

---

## 3. Financial Data Visualization Standards (IBCS)

International Business Communication Standards (IBCS) provide the gold standard for financial reporting notation.

### 3.1 Zero-Baseline Mandate (Empirical Invariant)
Research (*Long & Kay, ACM CHI 2024*) proved that **truncating a bar chart's baseline distorts perception by $\frac{100}{100 - t}$ and cannot be corrected by footnote disclosures or broken-axis marks**:
* If net debt decreases by $5.9\%$, truncating the axis exaggerates that decline to $24.6\%$ ($4.2\times$ distortion).
* **Rule**: Bar and column charts must begin at zero. If high-frequency variance must be highlighted, use an SVG line/area plot with explicit scale min/max tick labels.

### 3.2 Shared-Scale Horizontal Comparison Bars (Pattern C)
When presenting asymmetric one-off restructuring costs against ongoing annual benefits, plot both bars on a **shared zero-to-max axis**:
```html
<div class="hbars" role="img" aria-label="Restructuring cost $0.4m vs annual benefit ~$8.0m on a shared scale from zero">
  <div class="hbar">
    <p class="lab"><span>Restructuring cost incurred</span></p>
    <div class="track"><span class="fill" style="width: 5%"></span><span class="v">$0.4m</span></div>
  </div>
  <div class="hbar key">
    <p class="lab"><span>Targeted annualised pre-tax cash benefit</span></p>
    <div class="track"><span class="fill" style="width: 100%"></span><span class="v">~$8.0m</span></div>
  </div>
</div>
```

### 3.3 Financial & Cash Flow Waterfalls
* Cap waterfall bridge steps at **20–25 bars maximum** (IBCS guideline).
* Use distinct dark charcoal for opening and closing totals, muted neutral grey for operating deductions, and primary red/green for strategic additions.

### 3.4 Tabular Completion Tracks (Pattern D)
Inside asset build matrices or milestone tables, pair percentage text with visual progress tracks:
```html
<div class="barcell" style="display: flex; align-items: center; gap: 16px;">
  <div class="bar" style="width: 200px; height: 10px; background: var(--surface-sunken); border-radius: 9999px; overflow: hidden; position: relative;">
    <span style="position: absolute; inset: 0 auto 0 0; width: 75%; background: var(--ink); border-radius: 9999px;"></span>
  </div>
  <span class="d" style="font-family: var(--font-mono); font-weight: 500;">~75%</span>
</div>
```

---

## 4. Brand Geometry & Editorial Aesthetics

Avoid generic SaaS card grids. Translate the issuer's physical domain into authored CSS geometry:
1. **The 8px Solid Grounding Rule (`.rule`)**: A $96\text{px} \times 8\text{px}$ primary accent bar anchored above slide headers, evoking structural beams.
2. **Custom CSS Polygon Chevron Bullets (`.chevlist`)**:
   ```css
   .chevlist li::before {
     content: "";
     position: absolute;
     left: 0; top: .42em;
     width: 26px; height: 16px;
     background: var(--primary);
     clip-path: polygon(50% 0, 100% 100%, 76% 100%, 50% 46%, 24% 100%, 0 100%);
   }
   ```
3. **Asymmetric Editorial Splits (`1.06fr : 0.94fr`)**: Pair full-height vertical photography with soft gradient scrims on one side, and typographic narrative plus zero-based plots on the other.
4. **Top Accent Rules on Quote Cards (`border-top: 6px solid var(--primary)`)**: Forbid `border-left: 4px solid` on generic cards (which belongs exclusively to system warnings); use top accent beams on executive quotes.

---

## 5. Regulatory Compliance & Jurisdictional Invariants

| Jurisdiction | Governing Rules | Required Presentation Invariants |
| :--- | :--- | :--- |
| **Australia (ASX / ASIC)** | **ASX Listing Rule 3.1 & GN14**<br>**ASIC RG 230** (Non-IFRS information) | • Decks must be lodged on the Market Announcements Platform **separately and after** the formal Appendix 4D/4E financial release.<br>• Non-IFRS metrics (EBITDA, Underlying NPAT, Free Cash Flow) must be clearly labelled and reconciled to statutory NPAT.<br>• Oral remarks made during live slide delivery can constitute binding continuous disclosure (ASX GN8). |
| **United States (SEC)** | **Regulation FD**<br>**Regulation G & Item 10(e)** | • Decks must be furnished on Form 8-K or posted simultaneously with any intentional disclosure.<br>• Every non-GAAP measure requires **equal-or-greater prominence** to the most comparable GAAP measure, plus a quantitative reconciliation schedule. |
| **United Kingdom / EU** | **FRC Strategic Report Guidance**<br>**ESMA APM Guidelines** | • Alternative Performance Measures (APMs) must not overshadow IFRS metrics and must maintain consistent multi-year definitions. |

---

## 6. HTML/CSS Technical Presentation Engineering

### 6.1 The Scaling Shell (Never Fluid Reflow)
Decks must letterbox via `transform: translate(-50%, -50%) scale(s)` inside a fixed $1920 \times 1080$ stage. Content that reflows into a single fluid column breaks visual hierarchy and makes layout overflow uncomputable.

### 6.2 The `transform: scale()` Accessibility Gotcha
Automated contrast checkers evaluate `getComputedStyle(el).fontSize` before CSS transforms. When a $24\text{px}$ font is rendered inside `scale(0.6667)` (actual height $16\text{px}$), tools mistakenly apply WCAG's relaxed 3:1 large-text threshold. **Always maintain $\ge 4.5:1$ contrast on all body copy regardless of nominal font size.**

### 6.3 Floating Minimalist Chrome (Never Sticky Web Headers)
A fixed website navbar destroys the 16:9 aspect ratio and makes presentations look like web portals. Implement the floating trinity:
1. **Top 4px Scroll Progress Line (`#progress-bar`)**
2. **Right-Hand Glassmorphic Dot Rail (`#side-nav`)** with hover title tooltips
3. **Bottom Floating Pill Controller (`#controls`)** with slide counter and native PDF print action (`window.print()`).

### 6.4 Single-File Portability (Base64 Inlining)
Downsample high-resolution photography to $1600\text{px}$ WebP/JPEG ($80 - 85\%$ quality) and embed as Base64 Data URIs (`data:image/jpeg;base64,...`) to guarantee that standalone HTML decks open flawlessly offline and in sandboxed investor portal environments.
