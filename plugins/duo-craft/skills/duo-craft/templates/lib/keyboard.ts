import type React from 'react';
import { useEffect, useRef, useState } from 'react';

import { Keyboard, LayoutAnimation, Platform, type KeyboardEvent, type View } from 'react-native';

type ViewInstance = React.ComponentRef<typeof View>;

/**
 * The bottom padding a composer's container needs so its content clears the keyboard: the part of
 * the container the keyboard covers, measured against the keyboard's top edge in the window on every
 * keyboard event.
 *
 * `KeyboardAvoidingView`'s automatic offset is measured from the view's layout, which goes stale
 * whenever the view moves without re-laying out: in a pane on the open iPhone Duo, inside a sheet,
 * after the device folds. There the composer stayed under the split keyboard, which covers up to 42%
 * of the open display, and only sometimes lifted. Measuring the container in the window when the
 * keyboard appears does not depend on when the view last laid out.
 *
 * Put the lift on the container (`paddingBottom: lift`) and the gap above the keys (16pt) on the
 * composer inside it. While the keyboard is up, drop the composer's home-indicator inset: the lift
 * already clears it, and keeping both leaves the composer floating too high.
 */
export function useKeyboardLift(): { ref: React.RefObject<ViewInstance | null>; lift: number } {
  const ref = useRef<ViewInstance>(null);
  const [lift, setLift] = useState(0);

  useEffect(() => {
    const showEvent = Platform.OS === 'ios' ? 'keyboardWillChangeFrame' : 'keyboardDidShow';
    const hideEvent = Platform.OS === 'ios' ? 'keyboardWillHide' : 'keyboardDidHide';

    const animate = (event: KeyboardEvent) => {
      if (Platform.OS === 'ios' && event.duration > 0) {
        LayoutAnimation.configureNext({
          duration: event.duration,
          update: { type: LayoutAnimation.Types.keyboard },
        });
      }
    };

    const onShow = (event: KeyboardEvent) => {
      const keyboardTop = event.endCoordinates.screenY;
      ref.current?.measureInWindow((_x: number, y: number, _w: number, height: number) => {
        // The lift is bottom padding inside the container, so its frame, and its bottom edge, do not move.
        setLift(current => {
          const next = Math.max(0, Math.round(y + height - keyboardTop));
          if (next !== current) animate(event);
          return next;
        });
      });
    };
    const onHide = (event: KeyboardEvent) => {
      animate(event);
      setLift(0);
    };

    const show = Keyboard.addListener(showEvent, onShow);
    const hide = Keyboard.addListener(hideEvent, onHide);
    return () => {
      show.remove();
      hide.remove();
    };
  }, []);

  return { ref, lift };
}
