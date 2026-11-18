import NowPlaying
import MediaPlayer
@preconcurrency import CarPlay
@MainActor
final class CarScene: UIResponder, CPTemplateApplicationSceneDelegate {
    func templateApplicationScene(_ scene: CPTemplateApplicationScene, didConnect controller: CPInterfaceController) {
        MPRemoteCommandCenter.shared().playCommand.isEnabled = true
        Task { _ = try? await controller.setRootTemplate(CPNowPlayingTemplate.shared, animated: false) }
    }
}
let role = UISceneSession.Role.carTemplateApplication
