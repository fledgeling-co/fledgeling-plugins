import { requireOptionalNativeModule } from 'expo';
import type { EventSubscription } from 'expo-modules-core';

export type FoldRegion = { x: number; y: number; width: number; height: number; active: boolean };

export type HingeStatus = 'none' | 'unknown' | 'closed' | 'partiallyOpen' | 'fullyOpen';

export type FoldState = {
  /** The device has a fold, whether or not it is folded right now. */
  hasFold: boolean;
  /** Division regions in window points, inactive ones included (zero width while flat). */
  divisions: FoldRegion[];
  hinge: HingeStatus;
  /** Radians, or null without a hinge. */
  hingeAngle: number | null;
};

type NativeFold = {
  getState(): FoldState;
  addListener(event: 'onChange', listener: (state: FoldState) => void): EventSubscription;
};

export const NO_FOLD: FoldState = { hasFold: false, divisions: [], hinge: 'none', hingeAngle: null };

/** Null on Android, web, Expo Go and in tests: every caller treats that as "no fold". */
export const DuoFold = requireOptionalNativeModule<NativeFold>('DuoFold');
