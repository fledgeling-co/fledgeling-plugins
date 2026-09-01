func read() -> Int { 1 }
func seed() {}
func measure() {
    seed()
    func local(value: Int =
        read()) {}
    _ = local
}
