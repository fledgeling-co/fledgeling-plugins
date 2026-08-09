import { useState } from "react";
import { useNotes, useCreateNote } from "../lib/api";

export function SiteNotes({ siteId }: { siteId: string }) {
  const { data: notes, isPending, error } = useNotes(siteId);
  const create = useCreateNote(siteId);
  const [draft, setDraft] = useState("");

  if (isPending) return <p>Loading notes…</p>;
  if (error) return <p role="alert">Could not load notes. Check your signal.</p>;

  return (
    <section>
      <ul>
        {notes.map((n) => (
          <li key={n.id}>{n.body}</li>
        ))}
      </ul>
      <textarea value={draft} onChange={(e) => setDraft(e.target.value)} />
      <button
        onClick={() => {
          create.mutate(draft);
          setDraft("");
        }}
        disabled={create.isPending}
      >
        Save note
      </button>
    </section>
  );
}
