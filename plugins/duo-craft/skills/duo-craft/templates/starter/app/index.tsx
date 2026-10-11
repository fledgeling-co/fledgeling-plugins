import { Redirect } from 'expo-router';

/** The app opens on the first tab. Without this, `/` matches nothing and Expo Router shows its 404. */
export default function Index() {
  return <Redirect href="/items" />;
}
