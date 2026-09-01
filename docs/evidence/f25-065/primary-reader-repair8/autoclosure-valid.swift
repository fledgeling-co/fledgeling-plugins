func read() -> Int { 1 }
func store() {}
func seed(_ observation: @autoclosure () -> Int) { store() }
func measure() {
    seed(read())
}
