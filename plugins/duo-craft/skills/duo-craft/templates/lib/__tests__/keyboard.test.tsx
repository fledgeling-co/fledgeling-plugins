import React from 'react';

import { Keyboard, View } from 'react-native';

import { act, render } from '@testing-library/react-native';

import { useKeyboardLift } from '../keyboard';

type Handler = (event: unknown) => void;
const handlers: Record<string, Handler> = {};

beforeEach(() => {
  jest.spyOn(Keyboard, 'addListener').mockImplementation(((event: string, handler: Handler) => {
    handlers[event] = handler;
    return { remove: jest.fn() };
  }) as never);
});
afterEach(() => jest.restoreAllMocks());

let frame = { y: 0, height: 0 };
let lift = 0;
function Probe() {
  const keyboard = useKeyboardLift();
  lift = keyboard.lift;
  return (
    <View
      ref={node => {
        if (node) {
          (node as unknown as { measureInWindow: (cb: (x: number, y: number, w: number, h: number) => void) => void }).measureInWindow =
            cb => cb(0, frame.y, 400, frame.height);
        }
        (keyboard.ref as React.MutableRefObject<unknown>).current = node;
      }}
    />
  );
}

const keyboardAt = (screenY: number) => ({ endCoordinates: { screenY, height: 0, screenX: 0, width: 0 }, duration: 0 });

describe('useKeyboardLift', () => {
  it('lifts by the part of the view the keyboard covers, measured where the view is now', () => {
    render(<Probe />);
    // A pane on the open Duo: the view runs from 60 to 669; the split keyboard's top is at 391.
    frame = { y: 60, height: 609 };
    act(() => handlers.keyboardWillChangeFrame(keyboardAt(391)));
    expect(lift).toBe(278);
    // The same view, moved since it last laid out (folded closed): measured again, not reused.
    frame = { y: 0, height: 678 };
    act(() => handlers.keyboardWillChangeFrame(keyboardAt(374)));
    expect(lift).toBe(304);
  });

  it('does not lift a view the keyboard does not reach, and drops the lift when it hides', () => {
    render(<Probe />);
    frame = { y: 0, height: 300 };
    act(() => handlers.keyboardWillChangeFrame(keyboardAt(391)));
    expect(lift).toBe(0);
    frame = { y: 0, height: 669 };
    act(() => handlers.keyboardWillChangeFrame(keyboardAt(391)));
    expect(lift).toBe(278);
    act(() => handlers.keyboardWillHide(keyboardAt(669)));
    expect(lift).toBe(0);
  });
});
