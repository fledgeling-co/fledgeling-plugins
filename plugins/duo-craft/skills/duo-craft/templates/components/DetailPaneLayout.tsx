import React, { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react';

import { PlatformColor, StyleSheet, View, useWindowDimensions } from 'react-native';

import { SafeAreaInsetsContext, useSafeAreaInsets } from 'react-native-safe-area-context';

import { useRouter } from 'expo-router';

import { useTwoPane, type TwoPane } from '~/lib/fold';
import { PaneWidthContext } from '~/lib/layout';

/**
 * List and detail split at the fold, for the open inner display of a folding iPhone.
 *
 * Opening the device reveals one more level of the same hierarchy rather than a
 * different app: the tab's own screen stays in the left pane, and what it would
 * otherwise push (a company, a conversation) fills the right one. With one pane —
 * every other device and pose — `open` pushes exactly as before.
 */

type DetailPaneValue = {
  /** True while the screen is split into two panes. */
  split: boolean;
  /** The id shown in the right pane, or null. */
  selectedId: string | null;
  /** Show `id` in the right pane when split; push its screen otherwise. */
  open: (id: string) => void;
};

const DetailPaneContext = createContext<DetailPaneValue | null>(null);

/** The enclosing pane, or null outside a `DetailPaneLayout`. */
export function useDetailPane(): DetailPaneValue | null {
  return useContext(DetailPaneContext);
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
  const pane = useTwoPane();
  const [chosenId, setChosenId] = useState<string | null>(null);
  const selectedId = chosenId ?? defaultId;

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

  const value = useMemo(() => ({ split: pane != null, selectedId, open }), [open, pane, selectedId]);

  return (
    <DetailPaneContext.Provider value={value}>
      {pane ? <Split pane={pane} left={children} right={renderDetail(selectedId)} /> : children}
    </DetailPaneContext.Provider>
  );
}

function Split({ pane, left, right }: { pane: TwoPane; left: React.ReactNode; right: React.ReactNode }) {
  const { width } = useWindowDimensions();
  const insets = useSafeAreaInsets();
  const trailing = insets.right;
  // Each pane owns only its outer edges: the right pane stops at the side bar rather than
  // padding for it, and neither pads for the fold, which the gap between them clears.
  const leftInsets = useMemo(() => ({ ...insets, right: 0 }), [insets]);
  const rightInsets = useMemo(() => ({ ...insets, left: 0, right: 0 }), [insets]);
  return (
    <View style={styles.row}>
      <PaneWidthContext.Provider value={pane.leftWidth}>
        <SafeAreaInsetsContext.Provider value={leftInsets}>
          <View style={{ width: pane.leftWidth }}>{left}</View>
        </SafeAreaInsetsContext.Provider>
      </PaneWidthContext.Provider>
      {/* The gap at the fold: nothing tappable sits in it, flat or folded. */}
      <View style={{ width: pane.rightX - pane.leftWidth }} />
      <PaneWidthContext.Provider value={Math.max(0, width - trailing - pane.rightX)}>
        <SafeAreaInsetsContext.Provider value={rightInsets}>
          <View
            style={[
              styles.right,
              { marginRight: trailing },
            ]}
          >
            {right}
          </View>
        </SafeAreaInsetsContext.Provider>
      </PaneWidthContext.Provider>
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flex: 1, flexDirection: 'row' },
  // System colours, so the detail pane follows light and dark mode without app tokens.
  right: {
    flex: 1,
    minWidth: 0,
    borderLeftWidth: StyleSheet.hairlineWidth,
    backgroundColor: PlatformColor('systemBackground'),
    borderLeftColor: PlatformColor('separator'),
  },
});
