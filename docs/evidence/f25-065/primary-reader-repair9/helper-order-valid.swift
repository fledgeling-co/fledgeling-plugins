func read() {}
func store() {}
func seed(_ body: () -> Void) { body(); store() }
func measure() { seed { read() } }
