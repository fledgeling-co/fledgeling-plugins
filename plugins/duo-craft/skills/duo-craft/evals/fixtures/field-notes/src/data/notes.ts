export type Note = { id: string; title: string; body: string; updated: string };

export const NOTES: Note[] = [
  { id: '1', title: 'Ridge walk', body: 'Wind from the west, cloud lifting by ten. Three wedge-tailed eagles over the saddle.', updated: '2026-10-09' },
  { id: '2', title: 'Creek crossing', body: 'Water knee-deep after the rain. Stepping stones on the downstream side are stable.', updated: '2026-10-07' },
  { id: '3', title: 'Campsite', body: 'Flat ground behind the boulders, sheltered from the south. Tank water available.', updated: '2026-10-05' },
];

export function noteById(id: string): Note | undefined {
  return NOTES.find(n => n.id === id);
}
