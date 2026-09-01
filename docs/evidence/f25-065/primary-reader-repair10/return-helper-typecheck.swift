func write() {}
func read() {}
private func seed() -> Int { write(); return 1 }
func measure() -> Int { return seed(); read(); return 2 }
