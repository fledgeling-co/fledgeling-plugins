import UIKit
@preconcurrency import CarPlay
import MediaPlayer
@MainActor
final class CarScene: UIResponder, CPTemplateApplicationSceneDelegate {
    func templateApplicationScene(_ scene: CPTemplateApplicationScene, didConnect controller: CPInterfaceController) {
        MPNowPlayingInfoCenter.default().nowPlayingInfo = [:]
        let list = CPListTemplate(title: "Listen", sections: [])
        _ = CPListTemplate.maximumItemCount
        Task { _ = try? await controller.setRootTemplate(list, animated: false) }
    }
}
// role routing
let role = UISceneSession.Role.carTemplateApplication
