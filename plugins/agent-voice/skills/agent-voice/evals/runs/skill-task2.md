## Interactive Control State Inspection

Inspect each interactive control across six distinct states: `default`, `hover`, `focus-visible`, `active`, `disabled`, and `error` (for form fields). Target five control types: buttons, text inputs, selects, checkboxes/radios, and inline links.

### Inspection Procedure

1. **Trigger and observe each state**: Use the browser automation tool to cycle through each state sequentially. For `hover`, hover the pointer over the bounding box center. For `focus-visible`, send a Tab key event. For `active`, trigger a mouse-down event without mouse-up. For `disabled` and `error`, inspect the element with the `disabled` attribute or `aria-invalid="true"` applied.
2. **Read computed properties**: For each state, execute a DOM script to query `window.getComputedStyle(element)` and record:
   - `color`
   - `background-color`
   - `border-color`
   - `outline-color`, `outline-style`, and `outline-width`
   - `box-shadow`
3. **Evaluate against contrast criteria**:
   - **Text readability**: Text-to-background contrast ratio must measure 4.5:1 or higher for normal text (under 18pt / 24px) and 3.0:1 or higher for large text (18pt / 24px and above).
   - **Interface components and boundaries**: Button borders, input outlines, and state indicators must measure at least 3.0:1 against adjacent background colors.
   - **Focus indicator presence**: The `focus-visible` state must show an outline or box-shadow with a thickness of at least 2px and a minimum 3.0:1 contrast against the surrounding background.

### Reporting Format

Emit findings in a Markdown table containing every examined control and state. Do not omit rows for states that could not be reached; report them with a status of `unreachable` and record the blocking reason in the notes column.

| Control Identifier | State | Computed Colors (Text / BG / Border) | Contrast Ratio | Focus Ring Width | Status | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `button#submit` | default | `#ffffff` / `#1d4ed8` / `transparent` | 4.62:1 | 0px | pass | — |
| `button#submit` | hover | `#ffffff` / `#1e40af` / `transparent` | 5.89:1 | 0px | pass | — |
| `button#submit` | focus-visible | `#ffffff` / `#1d4ed8` / `#93c5fd` | 4.62:1 | 2px | pass | 3.2:1 ring contrast against page |
| `input#email` | error | `#0f172a` / `#fef2f2` / `#ef4444` | 13.4:1 | 0px | pass | Border contrast 3.4:1 against page |

The expected number of rows in the report equals the total count of identified controls multiplied by the number of applicable states for each control type (5 for standard controls, 6 for form inputs).
