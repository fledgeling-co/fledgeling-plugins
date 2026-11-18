import SwiftUI
import WidgetKit
struct StatusWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "Status", provider: Provider()) { entry in
            Text(entry.title).background(Color.blue)
        }
        .supportedFamilies([.systemSmall])
    }
}
