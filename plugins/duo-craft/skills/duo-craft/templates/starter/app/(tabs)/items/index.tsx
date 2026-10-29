import React from 'react';

import { FlatList, Pressable, StyleSheet, Text, View } from 'react-native';

import { Stack } from 'expo-router';

import { DetailPaneLayout, useDetailPane } from '~/components/DetailPaneLayout';
import { ScreenTitle } from '~/components/ScreenTitle';
import { systemColor } from '~/lib/layout';
import { ITEMS } from '../../item/[id]';

const itemHref = (id: string) => `/item/${id}`;

/** The list. Inside a split it opens items in the pane beside it; with one pane it pushes them. */
function ItemList() {
  const pane = useDetailPane();
  return (
    <>
      {/* Split at the fold, the bar carries the detail's toolbar items, which iPhone Duo stands
          in its side column; transparent so it takes no space from the list. Hidden otherwise,
          because the list draws its own large title. */}
      <Stack.Screen
        options={pane?.split ? { headerShown: true, headerTransparent: true, title: '' } : { headerShown: false }}
      />
      <FlatList
        data={ITEMS}
        keyExtractor={item => item.id}
        ListHeaderComponent={<ScreenTitle>Items</ScreenTitle>}
        renderItem={({ item }) => (
          <Pressable
            accessibilityRole="button"
            onPress={() => pane?.open(item.id)}
            style={[styles.row, pane?.split && pane.selectedId === item.id ? styles.selected : null]}
          >
            <Text style={styles.rowText}>{item.title}</Text>
          </Pressable>
        )}
      />
    </>
  );
}

/**
 * Required on first use rather than imported: only a split loads the detail screen into this tab,
 * and a detail screen's native dependencies stay out of the tab's tests.
 */
function EmbeddedItem({ id }: { id: string }) {
  const { ItemDetail } = require('../../item/[id]') as typeof import('../../item/[id]');
  return <ItemDetail id={id} embedded />;
}

export default function ItemsScreen() {
  return (
    <DetailPaneLayout
      hrefFor={itemHref}
      defaultId={ITEMS[0]?.id ?? null}
      renderDetail={id => (id ? <EmbeddedItem key={id} id={id} /> : <View />)}
    >
      <ItemList />
    </DetailPaneLayout>
  );
}

const styles = StyleSheet.create({
  row: { minHeight: 52, justifyContent: 'center', paddingHorizontal: 20 },
  selected: { backgroundColor: systemColor('systemFill', 'rgba(120, 120, 128, 0.2)') },
  rowText: { fontSize: 17, color: systemColor('label', '#000000') },
});
