// Swift operator tokens are not valid argument labels, even when escaped.
func read(`+` value: Int) -> Int { value }
let reference = read(`+`:)
