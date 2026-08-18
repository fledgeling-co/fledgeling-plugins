// Generation fixture: one line per mutation kind in real code, and the same
// tokens again inside a comment and a string literal, where nothing may be
// mutated. The comment below is the trap: true === false and await this.
export async function loadTotals(client: Client) {
  const label = "true === false, await this, 1 + 1";
  const rows = await client.query(label);
  const ready = true;
  const matched = rows.length === 3;
  const scaled = rows.length * 2;
  return matched && ready ? scaled : 0;
}
