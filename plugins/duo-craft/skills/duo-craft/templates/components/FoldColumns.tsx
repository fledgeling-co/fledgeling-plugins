import React, { useCallback, useRef, useState } from 'react';

import { StyleSheet, View, type ViewStyle } from 'react-native';

import { foldColumnLeftWidth, useFold } from '~/lib/fold';

/**
 * Two columns side by side. On a folding iPhone, open with the fold running top to
 * bottom through the middle of this row, the columns meet at the fold — the gap between
 * them is the band nothing tappable should sit in. Where the fold falls near one edge of
 * the row (a detail pane beside a 320pt list), and everywhere else, they share the row by
 * `leftFlex : rightFlex`.
 */
export function FoldColumns({
  left,
  right,
  leftFlex = 1,
  rightFlex = 1,
  gap = 16,
  style,
}: {
  left: React.ReactNode;
  right: React.ReactNode;
  leftFlex?: number;
  rightFlex?: number;
  gap?: number;
  style?: ViewStyle;
}) {
  const fold = useFold();
  const ref = useRef<React.ComponentRef<typeof View>>(null);
  const [frame, setFrame] = useState<{ x: number; width: number } | null>(null);

  const measure = useCallback(() => {
    ref.current?.measureInWindow((x: number, _y: number, width: number) => setFrame({ x, width }));
  }, []);

  // The columns meet at the fold only if the row spans it with a fair share on each side.
  const leftWidth = frame ? foldColumnLeftWidth(fold, frame.x, frame.width) : null;

  return (
    <View ref={ref} onLayout={measure} style={[styles.row, style]}>
      <View style={leftWidth != null ? { width: leftWidth } : { flex: leftFlex, minWidth: 0 }}>{left}</View>
      <View style={{ width: leftWidth != null ? fold.gap : gap }} />
      <View style={{ flex: rightFlex, minWidth: 0 }}>{right}</View>
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'flex-start' },
  column: { flex: 1 },
});

/**
 * A raised half and a flat half, for a folding iPhone stood on a table with the fold
 * running across. `top` fills the raised half down to the fold; `bottom` starts below
 * the gap, on the half resting on the table, where controls are steady to tap. Without
 * an active fold across this view, the two stack with `top` at its natural height.
 */
export function FoldRows({ top, bottom }: { top: React.ReactNode; bottom: React.ReactNode }) {
  const fold = useFold();
  const ref = useRef<React.ComponentRef<typeof View>>(null);
  const [y, setY] = useState<number | null>(null);
  const measure = useCallback(() => {
    ref.current?.measureInWindow((_x: number, top: number) => setY(top));
  }, []);
  const foldY = fold.horizontalFoldY;
  const topHeight = foldY != null && y != null && foldY - fold.gap / 2 - y > 120 ? foldY - fold.gap / 2 - y : null;
  return (
    <View ref={ref} onLayout={measure} style={styles.column}>
      <View style={topHeight != null ? { height: topHeight } : null}>{top}</View>
      {topHeight != null ? <View style={{ height: fold.gap }} /> : null}
      <View style={styles.column}>{bottom}</View>
    </View>
  );
}
