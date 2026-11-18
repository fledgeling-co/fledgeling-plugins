import Security
@preconcurrency import CarPlay
@MainActor
final class AssistantScene: UIResponder, CPTemplateApplicationSceneDelegate {
    func templateApplicationScene(_ scene: CPTemplateApplicationScene, didConnect controller: CPInterfaceController) {
        let alert = CPAlertTemplate(titleVariants: ["Unlock your iPhone to sign in"], actions: [])
        let query: [String: Any] = [kSecAttrAccessible as String: kSecAttrAccessibleWhenUnlocked]
        _ = query
        Task { _ = try? await controller.presentTemplate(alert, animated: true) }
    }
}
