// Bulk PDF text extraction via PDFKit.
// Compile once:  swiftc -O pdftext.swift -o /tmp/pdftext
// One file:      /tmp/pdftext a.pdf b.pdf         -> stdout, delimited
// Many files:    /tmp/pdftext --out /tmp/pdftext *.pdf   -> one .txt per input
//
// `swift -e '<code>'` under a subprocess returns EMPTY STDOUT with a clean exit.
// Always run from a file.
import Foundation
import PDFKit

var args = Array(CommandLine.arguments.dropFirst())
var outDir: String? = nil
if let i = args.firstIndex(of: "--out"), i + 1 < args.count {
    outDir = args[i + 1]
    args.removeSubrange(i...(i + 1))
}
if let d = outDir {
    try? FileManager.default.createDirectory(atPath: d, withIntermediateDirectories: true)
}

var extracted = 0, failed = 0
for p in args {
    guard let doc = PDFDocument(url: URL(fileURLWithPath: p)) else {
        FileHandle.standardError.write("!! cannot open \(p)\n".data(using: .utf8)!)
        failed += 1
        continue
    }
    // doc.string is whole-document; the per-page loop is safer on very large files.
    var text = ""
    for i in 0..<doc.pageCount { text += (doc.page(at: i)?.string ?? "") + "\n" }
    if let d = outDir {
        let safe = (p as NSString).lastPathComponent.replacingOccurrences(of: "/", with: "_") + ".txt"
        try? ("PATH:\(p)\n" + text).write(toFile: d + "/" + safe, atomically: true, encoding: .utf8)
    } else {
        print("=== \(p) ===")
        print(text)
    }
    extracted += 1
}
FileHandle.standardError.write("extracted \(extracted), failed \(failed)\n".data(using: .utf8)!)
