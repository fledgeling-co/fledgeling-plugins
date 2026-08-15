// Renders the notes list. Heading uses the app's standard title style.
export function NotesList({ notes }: { notes: Note[] }) {
  return (
    <section>
      <h2 className="font-serif text-xl">Your notes</h2>
      <ul>
        {notes.map((n) => (
          <li key={n.id} className="note-row">
            <span>{n.title}</span>
            <button onClick={() => archive(n.id)}>Archive</button>
          </li>
        ))}
      </ul>
    </section>
  );
}
