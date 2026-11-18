import UIKit
@preconcurrency import CarPlay
import MediaPlayer
final class CarScene: UIResponder, CPTemplateApplicationSceneDelegate {
    func templateApplicationScene(_ scene: CPTemplateApplicationScene, didConnect controller: CPInterfaceController) {
        MPNowPlayingInfoCenter.default().nowPlayingInfo = [:]
        let pois = CPPointOfInterestTemplate(title: "Stations", pointsOfInterest: [], selectedIndex: 0)
        let tabs = CPTabBarTemplate(templates: [pois])
        controller.setRootTemplate(tabs, animated: false)
    }
}
let role = UISceneSession.Role.carTemplateApplication
