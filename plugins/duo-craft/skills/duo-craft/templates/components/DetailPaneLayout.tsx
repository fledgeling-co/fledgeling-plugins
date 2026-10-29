import React, { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';

import { StyleSheet, View, useWindowDimensions, type LayoutChangeEvent } from 'react-native';

import { SafeAreaInsetsContext, useSafeAreaInsets } from 'react-native-safe-area-context';

import { useRouter } from 'expo-router';

import { twoPaneForWidth, useFold, useTwoPane, type TwoPane } from '~/lib/fold';
import { PaneWidthContext, systemColor } from '~/lib/layout';

/**
 * List and detail side by side wherever there is room for both: on the open inner display of
 * a folding iPhone (a fixed 320pt list lying flat, divided at the fold once folded like a
 * book), and at about 35/65 on a wide pane without a fold (iPad in landscape, a wide Mac
 * window).
 *
 * Opening the device or widening the window reveals one more level of the same hierarchy
 * rather than a different app: the screen's own list stays in the left pane, and what it
 * would otherwise push (a company, a conversation, a setting) fills the right one. With one
 * pane, `open` pushes exactly as before.
 */

type DetailPaneValue = {
  /** True while the screen is split into two panes. */
  split: boolean;
  /** The id shown in the right pane, or null. */
  selectedId: string | null;
  /** Show `id` in the right pane when split; push its screen otherwise. */
  open: (id: string) => void;
  /** Offer the id to show before anything is chosen (the list's first item). */
  offerDefault: (id: string | null) => void;
};

const DetailPaneContext = createContext<DetailPaneValue | null>(null);

/** The enclosing pane, or null outside a `DetailPaneLayout`. */
export function useDetailPane(): DetailPaneValue | null {
  return useContext(DetailPaneContext);
}

/**
 * Opens `id` beside the list when the enclosing screen is split, and pushes `href` when it is
 * not (or when the list is used outside a `DetailPaneLayout`). `firstId` fills the detail pane
 * until something is chosen, so the second pane is never blank.
 */
export function useOpenDetail(push: (id: string) => void, firstId?: string | null) {
  const pane = useDetailPane();
  // Only a split needs a default, so a single pane never re-renders to record one.
  const offer = pane?.split ? pane.offerDefault : undefined;
  useEffect(() => {
    if (offer && firstId !== undefined) offer(firstId);
  }, [offer, firstId]);
  return useCallback((id: string) => (pane ? pane.open(id) : push(id)), [pane, push]);
}

type Props = {
  /** The route pushed for an id when there is one pane. */
  hrefFor: (id: string) => string;
  /** Shown in the right pane before anything is chosen; null leaves it to `renderDetail(null)`. */
  defaultId?: string | null;
  /** The left pane: the tab's own screen. */
  children: React.ReactNode;
  /** The right pane for the selected id. */
  renderDetail: (id: string | null) => React.ReactNode;
};

export function DetailPaneLayout({ hrefFor, defaultId = null, children, renderDetail }: Props) {
  const router = useRouter();
  const fold = useFold();
  const foldPane = useTwoPane();
  // Without a fold the split is decided by this pane's own width, which on iPad excludes the
  // sidebar. Null until the first layout: one pane renders first, then splits if it fits.
  const [paneWidth, setPaneWidth] = useState<number | null>(null);
  const { width: windowWidth } = useWindowDimensions();
  const pane = fold.hasFold ? foldPane : paneWidth == null ? null : twoPaneForWidth(paneWidth);
  // On a folding iPhone the screen fills the window, so the window stands in until the first layout.
  const splitWidth = paneWidth ?? windowWidth;
  const [chosenId, setChosenId] = useState<string | null>(null);
  const [offeredId, setOfferedId] = useState<string | null>(null);
  const selectedId = chosenId ?? defaultId ?? offeredId;
  const offerDefault = useCallback((id: string | null) => setOfferedId(id), []);
  const onLayout = useCallback((e: LayoutChangeEvent) => {
    const w = Math.round(e.nativeEvent.layout.width);
    setPaneWidth(prev => (prev === w ? prev : w));
  }, []);

  const open = useCallback(
    (id: string) => {
      if (pane) setChosenId(id);
      else router.push(hrefFor(id) as never);
    },
    [hrefFor, pane, router],
  );

  // State survives the fold: closing the device on a company someone chose keeps it
  // open, now as a full screen, instead of dropping them back to the list.
  const wasSplit = useRef(pane != null);
  useEffect(() => {
    if (wasSplit.current && !pane && chosenId) router.push(hrefFor(chosenId) as never);
    wasSplit.current = pane != null;
  }, [chosenId, hrefFor, pane, router]);

  const value = useMemo(
    () => ({ split: pane != null, selectedId, open, offerDefault }),
    [offerDefault, open, pane, selectedId],
  );

  return (
    <DetailPaneContext.Provider value={value}>
      <View style={styles.fill} onLayout={onLayout}>
        {pane ? (
          <Split pane={pane} width={splitWidth} left={children} right={renderDetail(selectedId)} />
        ) : (
          children
        )}
      </View>
    </DetailPaneContext.Provider>
  );
}

function Split({
  pane,
  width,
  left,
  right,
}: {
  pane: TwoPane;
  width: number;
  left: React.ReactNode;
  right: React.ReactNode;
}) {
  const insets = useSafeAreaInsets();
  const trailing = insets.right;
  // Each pane owns only its outer edges: the right pane stops at the side bar rather than
  // padding for it, and neither pads for the fold. Folded, the gap between them clears it;
  // lying flat, the fold falls inside the detail, as it does in the system's own apps.
  const leftInsets = useMemo(() => ({ ...insets, right: 0 }), [insets]);
  const rightInsets = useMemo(() => ({ ...insets, left: 0, right: 0 }), [insets]);
  return (
    <View style={styles.row}>
      <PaneWidthContext.Provider value={pane.leftWidth}>
        <SafeAreaInsetsContext.Provider value={leftInsets}>
          <View style={{ width: pane.leftWidth }}>{left}</View>
        </SafeAreaInsetsContext.Provider>
      </PaneWidthContext.Provider>
      {/* The gap at the fold when folded; zero while flat, where the panes meet at a hairline. */}
      <View style={{ width: pane.rightX - pane.leftWidth }} />
      <PaneWidthContext.Provider value={Math.max(0, width - trailing - pane.rightX)}>
        <SafeAreaInsetsContext.Provider value={rightInsets}>
          <View
            style={[styles.right, { marginRight: trailing }]}
          >
            {right}
          </View>
        </SafeAreaInsetsContext.Provider>
      </PaneWidthContext.Provider>
    </View>
  );
}

const styles = StyleSheet.create({
  fill: { flex: 1 },
  row: { flex: 1, flexDirection: 'row' },
  // System colours, so the detail pane follows light and dark mode without app tokens on iOS.
  right: {
    flex: 1,
    minWidth: 0,
    borderLeftWidth: StyleSheet.hairlineWidth,
    backgroundColor: systemColor('systemBackground', '#ffffff'),
    borderLeftColor: systemColor('separator', 'rgba(60, 60, 67, 0.29)'),
  },
});
