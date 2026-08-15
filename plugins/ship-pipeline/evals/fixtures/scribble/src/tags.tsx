// Tag picker used on the note editor. Colors come from the theme tokens.
export function TagPicker({ tags, onPick }: TagPickerProps) {
  return (
    <div className="tag-picker">
      {tags.map((t) => (
        <button key={t.id} style={{ background: t.color }} onClick={() => onPick(t)}>
          {t.name}
        </button>
      ))}
    </div>
  );
}
