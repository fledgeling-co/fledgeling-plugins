import ActivityKit
import AppIntents
import SwiftUI
import WidgetKit

// The surface every iOS app gets on HomeView, entitlement or not: a system-small widget from the
// paired iPhone, on HomeView's Home Screen and on its shared Modular face. CarPlay shows the same
// widget in its widget stack.
//
// The Modular face is shared by the household, so this widget shows only what anyone at home may see.

struct StatusEntry: TimelineEntry {
    let date: Date
    let headline: String
    let detail: String
}

struct StatusProvider: TimelineProvider {
    func placeholder(in context: Context) -> StatusEntry {
        StatusEntry(date: .now, headline: "Next up", detail: "Morning briefing")
    }

    func getSnapshot(in context: Context, completion: @escaping @Sendable (StatusEntry) -> Void) {
        completion(placeholder(in: context))
    }

    func getTimeline(in context: Context, completion: @escaping @Sendable (Timeline<StatusEntry>) -> Void) {
        // Read the app group's shared store here. The entry must not need the phone unlocked,
        // because the car and HomeView show it while the phone is locked.
        let entry = StatusEntry(date: .now, headline: "Next up", detail: "Morning briefing")
        completion(Timeline(entries: [entry], policy: .after(.now.addingTimeInterval(30 * 60))))
    }
}

struct StatusWidgetView: View {
    let entry: StatusEntry

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(entry.headline)
                .font(.headline)
            Text(entry.detail)
                .font(.title3.weight(.semibold))
                .minimumScaleFactor(0.8)
        }
        // CarPlay, StandBy and the Modular face remove this background; the content must read without it.
        .containerBackground(.fill.tertiary, for: .widget)
    }
}

struct StatusWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "Status", provider: StatusProvider()) { entry in
            StatusWidgetView(entry: entry)
        }
        .configurationDisplayName("Status")
        .supportedFamilies([.systemSmall])
        // Add this only if the widget needs an unlocked phone or repeated tapping. It demotes the
        // widget in the CarPlay gallery and greys its interaction; it does not remove it, and Apple
        // documents no effect on HomeView either way.
        // .disfavoredLocations([.carPlay], for: [.systemSmall])
    }
}

// Live Activities reach CarPlay from iOS 26 through the small family, non-interactive. Apple does
// not document third-party Live Activities on HomeView, so do not promise them there.
struct DeliveryAttributes: ActivityAttributes {
    struct ContentState: Codable, Hashable {
        let minutesAway: Int
    }
    let orderName: String
}

struct DeliveryActivity: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: DeliveryAttributes.self) { context in
            Text("\(context.attributes.orderName): \(context.state.minutesAway) min")
        } dynamicIsland: { context in
            DynamicIsland {
                DynamicIslandExpandedRegion(.center) {
                    Text("\(context.state.minutesAway) min")
                }
            } compactLeading: {
                Image(systemName: "bag")
            } compactTrailing: {
                Text("\(context.state.minutesAway)m")
            } minimal: {
                Image(systemName: "bag")
            }
        }
        .supplementalActivityFamilies([.small])
    }
}

@main
struct HomeCraftWidgets: WidgetBundle {
    var body: some Widget {
        StatusWidget()
        DeliveryActivity()
    }
}
