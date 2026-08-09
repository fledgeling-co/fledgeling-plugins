import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

const API = import.meta.env.VITE_API_URL;

export interface Note {
  id: string;
  siteId: string;
  body: string;
  photoIds: string[];
  updatedAt: string;
}

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${API}${path}`);
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  return res.json();
}

export function useNotes(siteId: string) {
  return useQuery({
    queryKey: ["notes", siteId],
    queryFn: () => get<Note[]>(`/sites/${siteId}/notes`),
  });
}

export function useCreateNote(siteId: string) {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (body: string) => {
      const res = await fetch(`${API}/sites/${siteId}/notes`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ body }),
      });
      if (!res.ok) throw new Error(`${res.status}`);
      return res.json() as Promise<Note>;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notes", siteId] }),
  });
}
