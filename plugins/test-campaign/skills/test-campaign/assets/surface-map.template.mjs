/* ============================================================================
 * surface-map.template.mjs — where each surface lives in the real application.
 * ----------------------------------------------------------------------------
 * Copy this into the project, fill it in, and let the capture pass read it.
 *
 * Something has to say where a named surface actually lives, and it cannot be
 * derived from the test plan's prose. Guessing produces screenshots of the wrong
 * surface that score well against nothing — so this file is hand-authored, and
 * an unmapped surface is a status in its own right rather than a silent absence.
 *
 * Each entry carries:
 *   route     the path to visit
 *   region    a CSS selector for the element the surface depicts, or the main
 *             content area by default. Resolve it at capture time rather than
 *             assuming — when a visible [role="dialog"] is present, that IS the
 *             region, because a dialog must sit outside the main landmark to own
 *             its focus trap.
 *   wait      a selector to await before capturing
 *   act       ordered actuation steps (see the closed list below)
 *   status    'auto'    the capture pass drives this unattended
 *             'manual'  a human has to reach it (two people, a real email, a
 *                       device, an external site)
 *             'blocked' reachable in principle, not from a clean workspace
 *                       without seeding this pass does not do
 *   reason    REQUIRED for manual and blocked. Printed verbatim under the
 *             placeholder, so a reader never meets an unexplained gap.
 *   anon      true where the surface is reached without a session
 *
 * ── The actuation list is CLOSED, and the closure is the point ──────────────
 * Most real defects live behind a drawer, an expanded row or a confirmation
 * sheet, and none of those is a route. A pass that can only address routes
 * records them all as blocked — which is how one console came to have eleven
 * built screens and a single capture between them.
 *
 * So `act` accepts exactly these, one key per step, executed in order:
 *
 *     { click:    '<selector>' }
 *     { press:    '<key>' }              e.g. 'ControlOrMeta+k', 'Escape'
 *     { focus:    '<selector>' }
 *     { fill:     ['<selector>', '<text>'] }
 *     { viewport: [<width>, <height>] }
 *     { settle:   <ms> }
 *
 * An open field that could run arbitrary code would be a second test suite
 * living in a data file, and nobody would look for it there. A step that cannot
 * be performed fails THAT ONE SURFACE and is recorded with its reason, exactly
 * as a missing region is.
 *
 * ── Order matters ───────────────────────────────────────────────────────────
 * goto → press → wait → act → region. Running `act` before `wait` clicks a
 * selector that has not rendered yet.
 * ========================================================================== */

/** The main content region of the authenticated shell — the default capture. */
export const MAIN = '#main-content';

export const SURFACE_MAP = {
  /* ---- reached without a session ---------------------------------------- */
  signIn: { route: '/login', region: 'body', anon: true, status: 'auto' },

  /* ---- the shell -------------------------------------------------------- */
  nav: { route: '/dashboard', region: '#main-navigation', status: 'auto' },

  commandPalette: {
    route: '/dashboard',
    region: 'body',
    press: 'ControlOrMeta+k',
    status: 'auto',
    note: 'An overlay, so the capture is the whole viewport with it open.',
  },

  /* ---- behind an interaction, not a route ------------------------------- */
  rowControls: {
    route: '/records',
    wait: '[data-ui="row"]',
    act: [
      { click: '[data-ui="row"]:first-of-type button[aria-label^="Open the controls"]' },
      { settle: 200 },
    ],
    region: '[role="dialog"]',
    status: 'auto',
  },

  /* ---- a state, forced ---------------------------------------------------*/
  recordsEmpty: {
    route: '/records?fixture=empty',
    region: MAIN,
    status: 'auto',
    note: 'The empty state is served by a fixture; the live workspace is never empty.',
  },

  /* ---- honestly out of reach -------------------------------------------- */
  streamedAnswer: {
    status: 'blocked',
    reason: 'A streamed answer is not reproducible without spending a real model call, and this pass makes no paid calls.',
  },

  inviteAccepted: {
    status: 'manual',
    reason: 'Needs a second person opening a real invitation email on their own account.',
  },
};

/**
 * Anything absent from this map falls through to UNMAPPED — its own status,
 * with its own honest reason, counted in the denominator. That is deliberate:
 * a surface nobody mapped is a gap the ledger shows, not one it hides.
 */
