import { router } from 'expo-router';
import { Dimensions, FlatList, Pressable, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { NOTES } from '@/data/notes';

const SCREEN_WIDTH = Dimensions.get('window').width;
const IS_TABLET = SCREEN_WIDTH > 700;

export default function NotesList() {
  const insets = useSafeAreaInsets();
  return (
    <View style={[styles.page, { paddingTop: insets.top + 8, paddingHorizontal: insets.left + 16 }]}>
      <Text style={styles.title}>Notes</Text>
      <FlatList
        data={NOTES}
        keyExtractor={n => n.id}
        numColumns={IS_TABLET ? 2 : 1}
        renderItem={({ item }) => (
          <Pressable style={styles.row} onPress={() => router.push(`/note/${item.id}`)}>
            <Text style={styles.rowTitle}>{item.title}</Text>
            <Text style={styles.rowMeta}>{item.updated}</Text>
          </Pressable>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: '#fff' },
  title: { fontSize: 34, fontWeight: '700', marginBottom: 12 },
  row: { width: IS_TABLET ? SCREEN_WIDTH / 2 - 24 : SCREEN_WIDTH - 32, paddingVertical: 14, borderBottomWidth: StyleSheet.hairlineWidth, borderColor: '#ccc' },
  rowTitle: { fontSize: 17 },
  rowMeta: { fontSize: 13, color: '#888', marginTop: 2 },
});
