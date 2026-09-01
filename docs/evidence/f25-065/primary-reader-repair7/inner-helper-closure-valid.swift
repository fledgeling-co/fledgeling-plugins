func read() {}
func seed(_ body: () -> Void) { }
func measure() {
    seed { read() }
}
