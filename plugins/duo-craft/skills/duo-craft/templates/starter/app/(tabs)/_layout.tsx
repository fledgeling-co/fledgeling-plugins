import React from 'react';

import { NativeTabs } from 'expo-router/unstable-native-tabs';

import { useFold } from '~/lib/fold';

/**
 * System tabs, so iPhone Duo can stand them down the side bar. Native tab items carry an icon and a
 * label: the icon is what goes vertical, the label is what the overflow menu shows. A device with a
 * fold keeps the tabs in the side bar rather than turning them into an iPad sidebar, because open, a
 * sidebar would take most of the left half that belongs to the list.
 */
export default function TabsLayout() {
  const { hasFold } = useFold();
  return (
    <NativeTabs sidebarAdaptable={!hasFold}>
      <NativeTabs.Trigger name="items">
        <NativeTabs.Trigger.Icon sf="list.bullet" />
        <NativeTabs.Trigger.Label>Items</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}
