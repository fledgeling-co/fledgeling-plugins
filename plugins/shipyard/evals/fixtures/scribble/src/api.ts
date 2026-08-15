// Notes API client. share() posts to /api/notes/:id/share.
export async function share(id: string, email: string) {
  return fetch(`/api/notes/${id}/share`, {
    method: "POST",
    body: JSON.stringify({ email }),
  });
}
export async function archive(id: string) {
  return fetch(`/api/notes/${id}/archive`, { method: "POST" });
}
