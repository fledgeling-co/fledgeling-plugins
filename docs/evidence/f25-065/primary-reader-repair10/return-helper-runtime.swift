var reads = 0
func read() { reads += 1 }
func seed() -> Int { 1 }
func measure() -> Int { return seed(); read() }
print("value=\(measure()) reads=\(reads)")
