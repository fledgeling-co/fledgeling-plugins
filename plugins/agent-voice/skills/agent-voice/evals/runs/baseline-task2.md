## Interactive Control State Audit & Reporting

Audit every interactive element across all discrete visual states to ensure state parity, focus visibility, token consistency, and accessible feedback before marking a surface complete.

---

### 1. Control Inventory & Target Matrix

Identify and test all interactive targets on the rendered surface:
- **Triggers**: Buttons (`<button>`, `[role="button"]`), links (`<a>`), segmented controls, icon triggers.
- **Inputs**: Text fields, textareas, search bars, number steppers.
- **Selection**: Checkboxes, radio buttons, toggles/switches, dropdown selects, comboboxes.
- **Complex**: Accordion headers, tab triggers, modal dismissals, context menu triggers.

For each identified control, systematically evaluate the full **7-State Matrix**:

| State | Trigger / Emulation | Required Visual Indicators & Invariants |
| :--- | :--- | :--- |
| **Idle (Default)** | Default viewport state | Base token styling, legible label, correct `cursor: pointer` or `cursor: text`. |
| **Hover** | Pointer hover / `:hover` | Subtle background tint, elevation shift, or border highlight. **Never** shift layout/dimensions on hover. |
| **Focus-Visible** | Keyboard Tab navigation / `:focus-visible` | Unclipped focus ring (min 2px with offset), min 3:1 contrast against adjacent background. Never rely solely on color change. |
| **Active / Pressed** | Pointer down / Spacebar hold / `:active` | Depth reduction, inset shadow, or slight opacity drop (e.g., `scale(0.98)` or darker background token). |
| **Disabled** | `disabled` attribute / `aria-disabled="true"` | Muted contrast (min accessible text opacity), `cursor: not-allowed` or `default`, pointer events suppressed, zero hover/focus states. |
| **Loading / Busy** | `aria-busy="true"` / async pending | Inline spinner or shimmer; control width preserved to prevent layout shift; label either hidden or accompanied by progress indicator. |
| **Invalid / Error** | `aria-invalid="true"` / form error | Error token border/ring (semantic red/danger), error message association (`aria-describedby`), focus state retains error hue. |

---

### 2. Inspection & Verification Rules

Execute the following checks on each control state:

1. **Focus Ring Integrity**:
   - Verify that ancestor containers with `overflow: hidden` or `overflow: auto` do not clip focus rings or outlines.
   - Confirm outlines utilize `outline-offset` to avoid overlapping inner text or border radiuses.
2. **Layout Stability (Cumulative Layout Shift)**:
   - Ensure state changes (such as activating an active/selected border) use `box-shadow` or `border-color` transitions rather than changing `border-width`, which causes geometric reflow.
3. **Contrast Compliance**:
   - Measure text and icon contrast against the element background across all active states (Hover, Active, Focus) to ensure minimum 4.5:1 (standard text) and 3:1 (large text / UI icons).
4. **Transition Continuity**:
   - Ensure transitions on color, background, and transform are smooth (100ms–200ms `ease-out`) and non-jarring. Ensure `transition: all` is avoided in favor of explicit properties.

---

### 3. Reporting Findings

Output findings in the following standardized format. Group entries by severity (`[CRITICAL]`, `[HIGH]`, `[MEDIUM]`, `[LOW]`).

#### Finding Schema

```markdown
### [<SEVERITY>] <Control Name> - <State>: <Brief Issue Summary>
- **Target**: `<CSS selector or component path>` (e.g., `button#submit-form` or `src/components/Button.tsx`)
- **State Audited**: `[Idle | Hover | Focus-Visible | Active | Disabled | Loading | Invalid]`
- **Expected**: <Explicit design token, CSS rule, or HIG/WCAG guideline expected>
- **Observed**: <Exact observed visual failure, computed style, or clipping behavior>
- **Evidence**: <Screenshot reference, computed style dump, or bounding box measurement>
- **Remediation**: <Concrete CSS/JSX patch to resolve the defect>
```

#### State Audit Summary Table

Conclude the audit with a synthesis table:

```markdown
| Element Selector | Idle | Hover | Focus | Active | Disabled | Loading | Error | Overall Verdict |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `button.btn-primary` | PASS | PASS | FAIL | PASS | PASS | N/A | N/A | ❌ FAIL (Focus clipped) |
| `input#user-email` | PASS | PASS | PASS | PASS | PASS | PASS | FAIL | ❌ FAIL (Missing error border) |
```
