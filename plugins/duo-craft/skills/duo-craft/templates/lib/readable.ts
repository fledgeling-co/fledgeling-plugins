/** Side inset that centres a column of at most `maxWidth` in `width`. Zero when the column fills it. */
export function readableInset(width: number, maxWidth: number): number {
  return Math.max(0, Math.floor((width - maxWidth) / 2));
}
