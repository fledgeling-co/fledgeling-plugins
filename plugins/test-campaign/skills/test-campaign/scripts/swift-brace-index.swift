import Foundation
import SwiftParser
import SwiftSyntax

private struct CallClosure: Encodable {
    let brace: Int
    let paren: Int?
    let end: Int
}

private struct BraceIndex: Encodable {
    let valid: Bool
    let calls: [CallClosure]
    let blocks: [Int]
}

private struct Response: Encodable {
    let schema = 1
    let files: [BraceIndex]
}

private final class BraceVisitor: SyntaxVisitor {
    var calls: [CallClosure] = []
    var blocks: [Int] = []

    override func visit(_ node: FunctionCallExprSyntax) -> SyntaxVisitorContinueKind {
        if let closure = node.trailingClosure {
            calls.append(CallClosure(
                brace: closure.leftBrace.positionAfterSkippingLeadingTrivia.utf8Offset,
                paren: node.leftParen?.positionAfterSkippingLeadingTrivia.utf8Offset,
                end: node.endPositionBeforeTrailingTrivia.utf8Offset
            ))
        }
        return .visitChildren
    }

    override func visit(_ node: CodeBlockSyntax) -> SyntaxVisitorContinueKind {
        blocks.append(node.leftBrace.positionAfterSkippingLeadingTrivia.utf8Offset)
        return .visitChildren
    }

    override func visit(_ node: SwitchExprSyntax) -> SyntaxVisitorContinueKind {
        blocks.append(node.leftBrace.positionAfterSkippingLeadingTrivia.utf8Offset)
        return .visitChildren
    }
}

do {
    let input = FileHandle.standardInput.readDataToEndOfFile()
    let sources = try JSONDecoder().decode([String].self, from: input)
    let files = sources.map { source in
        let parsed = Parser.parse(source: source)
        // A recovered tree can contain synthesized or displaced tokens.
        guard !parsed.hasError else { return BraceIndex(valid: false, calls: [], blocks: []) }
        let visitor = BraceVisitor(viewMode: .sourceAccurate)
        visitor.walk(parsed)
        return BraceIndex(valid: true, calls: visitor.calls, blocks: visitor.blocks)
    }
    FileHandle.standardOutput.write(try JSONEncoder().encode(Response(files: files)))
} catch {
    FileHandle.standardError.write(Data("Invalid Swift brace index request or response.\n".utf8))
    exit(1)
}
