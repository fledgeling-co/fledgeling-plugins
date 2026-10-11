import { Tabs } from 'expo-router';
import { Text } from 'react-native';

export default function TabsLayout() {
  return (
    <Tabs screenOptions={{ headerShown: false }}>
      <Tabs.Screen name="index" options={{ title: 'Notes', tabBarIcon: () => <Text>📝</Text> }} />
      <Tabs.Screen name="settings" options={{ title: 'Settings', tabBarIcon: () => <Text>⚙️</Text> }} />
    </Tabs>
  );
}
