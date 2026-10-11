import { createContext, useContext, useMemo } from 'react';

import { useWindowDimensions } from 'react-native';

import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { useFold } from './fold';

/**
 * Width tiers read from the space the screen actually has, never from the device model.
 *
 * - `compact`: phones, iPhone Duo's outer display (382pt after its side bar), either half of
 *   iPhone Duo Split View (~475pt), narrow iPad windows.
 * - `regular`: iPad portrait, iPhone Duo's inner display in portrait (669pt) and landscape
 *   (867pt after its side bar).
 * - `expanded`: iPad landscape and large windows.
 *
 * On a device with a fold, `regular` starts at 640pt instead of 700pt so the inner display in
 * portrait is regular, as iOS's own size class treats it. No phone (440pt at most) or iPad
 * (744pt at least) changes tier.
 */
export type SizeClass = 'compact' | 'regular' | 'expanded';

export const REGULAR_MIN_WIDTH = 700;
export const FOLD_REGULAR_MIN_WIDTH = 640;
export const EXPANDED_MIN_WIDTH = 1100;

export function sizeClassFor(width: number, hasFold = false): SizeClass {
  if (width >= EXPANDED_MIN_WIDTH) return 'expanded';
  if (width >= (hasFold ? FOLD_REGULAR_MIN_WIDTH : REGULAR_MIN_WIDTH)) return 'regular';
  return 'compact';
}

/**
 * The status bar height on a Dynamic Island iPhone. Where no status bar crosses the top (iPhone
 * Duo, whose status bar and controls stand down the side) the top safe-area inset is 0, and a
 * title placed at `insets.top + 8` touches the edge. Settings starts its content about 83pt down
 * on the same display; clearing where a status bar would be puts the title where it sits on
 * every other iPhone.
 */
export const TOP_CLEARANCE_WITHOUT_STATUS_BAR = 59;

/** Space above a screen's own large title: 8pt under the status bar, or under where it would be. */
export function titleTopPadding(safeTop: number): number {
  return (safeTop > 0 ? safeTop : TOP_CLEARANCE_WITHOUT_STATUS_BAR) + 8;
}

/**
 * The width of the pane a screen is drawn in when it is one of two panes split at a fold. Inside
 * it `useLayout` reads the pane rather than the window, so the list in the left half lays out as
 * the phone-sized screen it is.
 */
export const PaneWidthContext = createContext<number | null>(null);

export type Layout = { sizeClass: SizeClass; width: number; isWide: boolean };

export function layoutFor(width: number, hasFold = false): Layout {
  const sizeClass = sizeClassFor(width, hasFold);
  return { sizeClass, width, isWide: sizeClass !== 'compact' };
}

/**
 * The current tier; re-renders when the window resizes (open, close, rotate, Split View, PiP).
 * Subtracts each side's inset on its own: on iPhone Duo they are unequal, and which side carries
 * the 84pt bar flips with the Split View half.
 */
export function useLayout(): Layout {
  const pane = useContext(PaneWidthContext);
  const { width } = useWindowDimensions();
  const { left, right } = useSafeAreaInsets();
  const { hasFold } = useFold();
  const contentWidth = pane ?? Math.max(0, width - left - right);
  return useMemo(() => layoutFor(contentWidth, hasFold), [contentWidth, hasFold]);
}
