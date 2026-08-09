// In-memory ring. Capacity is fixed at construction; overflow overwrites the oldest slot.
const CAPACITY = 8192;
export const queue = {
  buf: new Array(CAPACITY),
  head: 0, tail: 0, overwrites: 0,
  push(ev: unknown) {
    if ((this.head + 1) % CAPACITY === this.tail) { this.overwrites++; this.tail = (this.tail + 1) % CAPACITY; }
    this.buf[this.head] = ev; this.head = (this.head + 1) % CAPACITY;
  },
  async take(n: number) { const out = []; while (out.length < n && this.tail !== this.head) { out.push(this.buf[this.tail]); this.tail = (this.tail + 1) % CAPACITY; } return out; }
};
