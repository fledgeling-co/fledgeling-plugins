import { useMemo, useSyncExternalStore } from 'react';

import { useWindowDimensions } from 'react-native';

import { DuoFold, NO_FOLD, type FoldRegion, type FoldState } from '../modules/duo-fold';

/**
 * The fold on a folding iPhone (iPhone Duo), read from the native `DuoFold` module.
 *
 * Layout branches on space and on whether the device HAS a fold, never on its model: a
 * fold is reported even while the device lies flat (an inactive division region with no
 * width), so the choice of one pane or two is made once and does not change as the hinge
 * moves. Only the divider moves: a fixed list column while flat, the fold once folded.
 * Everything here is "no fold" on Android, web, in tests and on devices without one.
 */

/** Space kept clear on either side of the fold line, in points: nothing tappable sits in it. */
export const FOLD_GAP = 27;
/** The narrowest window that splits into list and detail on a device with a fold. */
export const TWO_PANE_MIN_WIDTH = 800;
/**
 * List width on the open inner display lying flat. Apps on iPhone Duo keep a fixed list
 * column there (320pt in Settings, Files, Shortcuts, Claude and ChatGPT; 292-403pt across
 * 21 apps) and let the fold fall inside the detail; only a folded device divides at the fold.
 */
export const FLAT_LIST_WIDTH = 320;

export type Posture =
  /** No fold on this device. */
  | 'none'
  /** Has a fold, lying flat or closed. */
  | 'flat'
  /** Folded with the hinge running top to bottom: two pages side by side. */
  | 'book'
  /** Folded with the hinge running across: a raised half and a flat half, as on a table. */
  | 'tabletop';

export type FoldGeometry = {
  hasFold: boolean;
  posture: Posture;
  /** Window x of a fold running top to bottom (active or not), or null. */
  verticalFoldX: number | null;
  /** Window y of a fold running across (active only — it only exists folded), or null. */
  horizontalFoldY: number | null;
  /** Width kept clear at the fold: the active region, or `FOLD_GAP` while flat. */
  gap: number;
};

const NONE: FoldGeometry = { hasFold: false, posture: 'none', verticalFoldX: null, horizontalFoldY: null, gap: 0 };

const runsTopToBottom = (r: FoldRegion) => r.height >= r.width;

export function foldGeometry(state: FoldState): FoldGeometry {
  if (!state.hasFold) return NONE;
  const active = state.divisions.find(r => r.active) ?? null;
  const vertical = state.divisions.find(r => runsTopToBottom(r) && r.height > 0) ?? null;
  let posture: Posture = 'flat';
  if (active) posture = runsTopToBottom(active) ? 'book' : 'tabletop';
  return {
    hasFold: true,
    posture,
    verticalFoldX: vertical ? vertical.x + vertical.width / 2 : null,
    horizontalFoldY: active && posture === 'tabletop' ? active.y + active.height / 2 : null,
    gap: Math.max(FOLD_GAP, active ? (runsTopToBottom(active) ? active.width : active.height) : 0),
  };
}

/**
 * The narrowest pane, on a device without a fold, that splits into list and detail: iPad in
 * landscape (1180pt, less its sidebar) and a wide Mac window qualify; iPad in portrait (820pt)
 * and a Split View half keep one pane, as Mail and Settings do.
 */
export const SPLIT_MIN_WIDTH = 900;
/** List column bounds without a fold: about 35% of the pane, as Apple's split views size it. */
export const LIST_MIN_WIDTH = 320;
export const LIST_MAX_WIDTH = 420;

export type TwoPane = {
  /** Width of the left (list) pane, from the window's left edge to the gap. */
  leftWidth: number;
  /** Left edge of the right (detail) pane, in window points. */
  rightX: number;
};

/**
 * List and detail on a device with a fold, or null for one pane. Needs a fold running top
 * to bottom inside a landscape window at least `TWO_PANE_MIN_WIDTH` wide: the open inner
 * display. Lying flat, the list is a fixed `FLAT_LIST_WIDTH` column meeting the detail at a
 * hairline; folded like a book, the panes divide at the fold with its gap between them.
 * Split View (half the display) and the closed outer display stay single-pane.
 */
export function twoPaneFor(fold: FoldGeometry, windowWidth: number, windowHeight: number): TwoPane | null {
  if (fold.verticalFoldX == null) return null;
  if (windowWidth < TWO_PANE_MIN_WIDTH || windowWidth <= windowHeight) return null;
  if (fold.posture === 'flat') return { leftWidth: FLAT_LIST_WIDTH, rightX: FLAT_LIST_WIDTH };
  const half = fold.gap / 2;
  return { leftWidth: Math.max(0, fold.verticalFoldX - half), rightX: fold.verticalFoldX + half };
}

/**
 * List and detail without a fold, from the width of the pane being split (not the window,
 * which on iPad includes the sidebar). No gap: the panes meet at a hairline.
 */
export function twoPaneForWidth(paneWidth: number): TwoPane | null {
  if (paneWidth < SPLIT_MIN_WIDTH) return null;
  const leftWidth = Math.round(Math.min(LIST_MAX_WIDTH, Math.max(LIST_MIN_WIDTH, paneWidth * 0.36)));
  return { leftWidth, rightX: leftWidth };
}

/** The least a column may keep on its side of the fold before a row will meet at it. */
export const FOLD_COLUMN_MIN = 120;
/** ...and the least share of the row it may keep, so a row never splits into a sliver. */
export const FOLD_COLUMN_MIN_SHARE = 0.35;

/**
 * Where a row of two columns should end its left column so the columns meet at the fold, or
 * null to share the row by flex. The fold has to run top to bottom through the row with at least
 * `FOLD_COLUMN_MIN` points and `FOLD_COLUMN_MIN_SHARE` of the row on each side. A row across the
 * open display qualifies; a row inside the detail pane beside a 320pt list does not, because the
 * fold sits about 155pt into it, and apps let such content cross the fold instead.
 */
export function foldColumnLeftWidth(fold: FoldGeometry, rowX: number, rowWidth: number): number | null {
  if (fold.verticalFoldX == null || rowWidth <= 0) return null;
  const leftWidth = fold.verticalFoldX - fold.gap / 2 - rowX;
  const rightWidth = rowX + rowWidth - (fold.verticalFoldX + fold.gap / 2);
  const least = Math.max(FOLD_COLUMN_MIN, rowWidth * FOLD_COLUMN_MIN_SHARE);
  return leftWidth >= least && rightWidth >= least ? leftWidth : null;
}

// One subscription to the native module, shared by every hook.
let current: FoldState = DuoFold?.getState() ?? NO_FOLD;
const listeners = new Set<() => void>();
let subscribed = false;

function subscribe(listener: () => void) {
  listeners.add(listener);
  if (!subscribed && DuoFold) {
    subscribed = true;
    DuoFold.addListener('onChange', next => {
      current = next;
      listeners.forEach(l => l());
    });
    // The module may have read the window between the first read and this subscription.
    const latest = DuoFold.getState();
    if (latest !== current) {
      current = latest;
      queueMicrotask(() => listeners.forEach(l => l()));
    }
  }
  return () => {
    listeners.delete(listener);
  };
}

const snapshot = () => current;

/** The raw fold state; re-renders as the device opens, closes and folds. */
export function useFoldState(): FoldState {
  return useSyncExternalStore(subscribe, snapshot, snapshot);
}

export function useFold(): FoldGeometry {
  const state = useFoldState();
  // Keyed on a state object that only changes when the native side reports one.
  return useMemo(() => foldGeometry(state), [state]);
}

/** The two-pane split for the current window, or null. */
export function useTwoPane(): TwoPane | null {
  const fold = useFold();
  const { width, height } = useWindowDimensions();
  return twoPaneFor(fold, width, height);
}
