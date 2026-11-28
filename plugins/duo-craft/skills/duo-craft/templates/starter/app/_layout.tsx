import React from 'react';

import { Stack } from 'expo-router';
import { SafeAreaProvider, useSafeAreaInsets } from 'react-native-safe-area-context';

import { FoldHandoff } from '~/components/FoldHandoff';
import { readableInset } from '~/lib/readable';
import { useLayout } from '~/lib/layout';

/**
 * Pushed screens fill the window, so they pad for the side safe areas themselves: on iPhone Duo
 * the side bar takes 84pt on one edge and 0 on the other, and the edge flips with the Split View
 * half. Each side gets its own inset plus the reading-column inset.
 */
function RootStack() {
  const { width } = useLayout();
  const { left, right } = useSafeAreaInsets();
  const column = readableInset(width, 760);
  return (
    <Stack
      screenOptions={({ route }) => ({
        headerShown: route.name !== '(tabs)',
        title: '',
        contentStyle: route.name === '(tabs)' ? undefined : { paddingLeft: left + column, paddingRight: right + column },
      })}
    />
  );
}

/** Pushed details and the tab whose list they belong to, so opening the Duo brings one back into its pane. */
const HANDOFF_ROUTES = { 'item/[id]': { tab: 'items' } };

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <RootStack />
      <FoldHandoff routes={HANDOFF_ROUTES} initialTab="items" />
    </SafeAreaProvider>
  );
}
