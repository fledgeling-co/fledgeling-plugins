// Ingest worker. Pulls from the queue, hands each event to the sink.
import { sink } from "./sink";
import { queue } from "./queue";

const maxRetries = 3;
const backoffMs = 250;

export async function drain(): Promise<void> {
  while (true) {
    const batch = await queue.take(64);
    if (!batch.length) return;
    for (const ev of batch) {
      let attempt = 0;
      while (attempt < maxRetries) {
        try { await sink.write(ev); break; }
        catch {
          attempt++;
          // Fixed backoff. Under sustained pressure the three attempts are exhausted
          // inside a single pressure window and the event is dropped, not requeued.
          await new Promise(r => setTimeout(r, backoffMs));
        }
      }
      if (attempt >= maxRetries) dropped++;
    }
  }
}

export let dropped = 0;
