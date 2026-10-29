import React from 'react';

import { ScrollView, Share, StyleSheet, Text } from 'react-native';

import { Stack, useLocalSearchParams } from 'expo-router';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { FoldColumns } from '~/components/FoldColumns';
import { systemColor, titleTopPadding } from '~/lib/layout';

/** Replace with the app's own data source. */
export const ITEMS = [
  { id: '1', title: 'First item', body: 'Shown beside the list when iPhone Duo is open.' },
  { id: '2', title: 'Second item', body: 'Pushed full screen on a phone or the closed display.' },
];

export default function ItemScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  return <ItemDetail id={id} />;
}

/**
 * One item. As the pushed screen it owns the navigation bar and its actions; `embedded` draws it in
 * the detail pane of a split, where the tab owns the bar. Actions are native toolbar items with an
 * icon and a title, so iPhone Duo can stand them in the side bar.
 */
export function ItemDetail({ id, embedded = false }: { id: string; embedded?: boolean }) {
  const item = ITEMS.find(i => i.id === id);
  const insets = useSafeAreaInsets();
  return (
    // As the pushed screen the navigation bar sits above the content; in a pane there is no bar
    // above it, so its title clears the top the way a screen title does.
    <ScrollView contentContainerStyle={[styles.content, embedded ? { paddingTop: titleTopPadding(insets.top) } : null]}>
      {embedded ? null : <Stack.Screen options={{ title: item?.title ?? '' }} />}
      <Stack.Toolbar placement="right">
        <Stack.Toolbar.Button
          icon="square.and.arrow.up"
          accessibilityLabel="Share"
          disabled={!item}
          onPress={() => item && Share.share({ title: item.title, message: `${item.title}\n\n${item.body}` })}
        />
      </Stack.Toolbar>
      <Text style={styles.title}>{item?.title}</Text>
      <FoldColumns
        left={<Text style={styles.body}>{item?.body}</Text>}
        right={<Text style={styles.body}>Secondary detail</Text>}
        gap={16}
      />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  content: { padding: 20, gap: 12 },
  title: { fontSize: 28, fontWeight: '700', color: systemColor('label', '#000000') },
  body: { fontSize: 17, lineHeight: 24, color: systemColor('secondaryLabel', 'rgba(60, 60, 67, 0.6)') },
});
