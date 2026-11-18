import SwiftUI
import UIKit
@preconcurrency import CarPlay

// The phone UI and the car UI are two scenes of one process. CarPlay and HomeView can launch
// the app with only the car scene connected, so nothing the car needs may live in a SwiftUI view.
@main
struct HomeCraftApp: App {
    @UIApplicationDelegateAdaptor(AppDelegate.self) private var appDelegate

    var body: some Scene {
        WindowGroup {
            PhoneRootView()
        }
    }
}

struct PhoneRootView: View {
    var body: some View {
        Text("Library")
    }
}

@MainActor
final class AppDelegate: NSObject, UIApplicationDelegate {
    func application(
        _ application: UIApplication,
        didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]? = nil
    ) -> Bool {
        // Runs for a car-only cold launch too. Start shared services here, not in a view.
        PlaybackService.shared.prepare()
        return true
    }

    func application(
        _ application: UIApplication,
        configurationForConnecting connectingSceneSession: UISceneSession,
        options: UIScene.ConnectionOptions
    ) -> UISceneConfiguration {
        guard connectingSceneSession.role == .carTemplateApplication else {
            return UISceneConfiguration(name: "Phone", sessionRole: connectingSceneSession.role)
        }
        let configuration = UISceneConfiguration(name: "CarPlay", sessionRole: connectingSceneSession.role)
        configuration.sceneClass = CPTemplateApplicationScene.self
        // Swap in CarPlayConversationSceneDelegate for a voice-based conversational app.
        configuration.delegateClass = CarPlayMediaSceneDelegate.self
        return configuration
    }
}
