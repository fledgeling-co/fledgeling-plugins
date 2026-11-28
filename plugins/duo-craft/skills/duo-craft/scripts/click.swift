import CoreGraphics
import Foundation

// Clicks at a global screen point, for setting iPhone Duo poses in Xcode 27.1's Device Hub, which
// refuses Accessibility scripting and which proctor cannot attach to.
//
//     swiftc -O click.swift -o click
//     ./click <x> <y>          # global screen points; see references/simulator.md for the pose bar
//
// The process posting the events needs Accessibility permission. When the agent's own process does
// not have it, launch the click through Terminal, which usually does: write the command into a
// `.command` file and `open -a Terminal` it.
let args = CommandLine.arguments
guard args.count == 3, let x = Double(args[1]), let y = Double(args[2]) else {
    print("usage: click <x> <y>")
    exit(2)
}
let point = CGPoint(x: x, y: y)
let source = CGEventSource(stateID: .hidSystemState)
for type in [CGEventType.mouseMoved, .leftMouseDown, .leftMouseUp] {
    CGEvent(mouseEventSource: source, mouseType: type, mouseCursorPosition: point, mouseButton: .left)?
        .post(tap: .cghidEventTap)
    usleep(60_000)
}
print("clicked \(x),\(y)")
