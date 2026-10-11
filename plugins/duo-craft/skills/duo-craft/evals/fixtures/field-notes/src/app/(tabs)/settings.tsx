import { StyleSheet, Text, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

export default function Settings() {
  const insets = useSafeAreaInsets();
  return (
    <View style={[styles.page, { paddingTop: insets.top + 8, paddingHorizontal: 16 }]}>
      <Text style={styles.title}>Settings</Text>
      <Text>Units: metric</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  page: { flex: 1, backgroundColor: '#fff' },
  title: { fontSize: 34, fontWeight: '700', marginBottom: 12 },
});
