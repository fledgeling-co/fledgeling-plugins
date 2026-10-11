import React from 'react';

import { PlatformColor, StyleSheet, Text, View } from 'react-native';

import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { titleTopPadding } from '~/lib/layout';

/**
 * A screen's own large title, for screens that hide the navigation bar. Under a status bar it sits
 * 8pt below it; on iPhone Duo, where the status bar stands down the side and the top inset is 0, it
 * clears where a status bar would be instead of touching the edge.
 */
export function ScreenTitle({ children, trailing }: { children: string; trailing?: React.ReactNode }) {
  const insets = useSafeAreaInsets();
  return (
    <View style={[styles.row, { paddingTop: titleTopPadding(insets.top) }]}>
      <Text accessibilityRole="header" style={styles.title}>
        {children}
      </Text>
      {trailing}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 20, paddingBottom: 8 },
  title: { flex: 1, fontSize: 34, fontWeight: '700', color: PlatformColor('label') },
});
