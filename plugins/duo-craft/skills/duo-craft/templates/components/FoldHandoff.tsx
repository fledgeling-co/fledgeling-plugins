import { useEffect, useRef } from 'react';

import { useWindowDimensions } from 'react-native';

import { useRootNavigationState, useRouter } from 'expo-router';

import { SPLIT_MIN_WIDTH, useFold, useTwoPane } from '~/lib/fold';
import { handOff, handoffFromState, type HandoffRoutes, type RootState } from '~/lib/foldHandoff';

type Props = {
  /** The pushed detail routes and the tab each belongs to, e.g. `{ 'item/[id]': { tab: 'items' } }`. */
  routes: HandoffRoutes;
  /** The tab shown before the tab navigator has state of its own: the first tab. */
  initialTab?: string;
  /** The route name of the tab navigator in the root stack. */
  tabsRoute?: string;
};

/**
 * When the display opens into list and detail, a detail pushed on the closed display goes back into
 * the right pane beside its list instead of staying full screen (`lib/foldHandoff.ts`). Render it
 * once, inside the root stack's navigator, and give each list's `DetailPaneLayout` its `handoffTab`.
 */
export function FoldHandoff({ routes, initialTab, tabsRoute }: Props) {
  const router = useRouter();
  const fold = useFold();
  const twoPane = useTwoPane();
  const { width } = useWindowDimensions();
  const state = useRootNavigationState() as unknown as RootState | undefined;
  const split = fold.hasFold ? twoPane != null : width >= SPLIT_MIN_WIDTH;
  const wasSplit = useRef(split);
  useEffect(() => {
    const opened = split && !wasSplit.current;
    wasSplit.current = split;
    if (!opened) return;
    const h = handoffFromState(routes, state, { initialTab, tabsRoute });
    if (!h) return;
    handOff(h);
    if (router.canGoBack()) router.back();
  }, [split, state, router, routes, initialTab, tabsRoute]);
  return null;
}
