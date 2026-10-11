import { router, useLocalSearchParams } from 'expo-router';
import { Pressable, Share, StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import { noteById } from '@/data/notes';

export default function NoteScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const note = noteById(id);
  const insets = useSafeAreaInsets();
  if (!note) return <Text>Note not found</Text>;
  return (
    <View style={[styles.page, { paddingTop: insets.top }]}>
      <View style={styles.header}>
        <Pressable onPress={() => router.back()}><Text style={styles.link}>‹ Notes</Text></Pressable>
        <Pressable onPress={() => Share.share({ message: note.body })}><Text style={styles.link}>Share</Text></Pressable>
      </View>
      <Text style={styles.title}>{note.title}</Text>
      <Text style={styles.body}>{note.body}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: '#fff', paddingHorizontal: 16 },
  header: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 10 },
  link: { color: '#007aff', fontSize: 17 },
  title: { fontSize: 28, fontWeight: '700', marginTop: 8 },
  body: { fontSize: 17, lineHeight: 24, marginTop: 12 },
});
