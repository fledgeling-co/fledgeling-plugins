import AVFoundation
import UIKit
@preconcurrency import CarPlay

/// The app's own speech pipeline: capture, recognition, the model call and spoken replies.
/// It reports its phase so the car can show it; it never shows the answer as text.
@MainActor
protocol ConversationEngine: AnyObject {
    var onPhaseChange: ((ConversationPhase) -> Void)? { get set }
    func start() throws
    func stop()
}

enum ConversationPhase: String {
    case listening, thinking, speaking
}

@MainActor
enum ConversationServices {
    /// Set in `application(_:didFinishLaunchingWithOptions:)`, which also runs on a car-only launch.
    static var engine: (any ConversationEngine)?
}

/// CarPlay scene for `com.apple.developer.carplay-voice-based-conversation` (iOS 26.4+).
/// Voice is the primary modality from launch, the voice template is on screen whenever the
/// microphone is open, and the audio session is held only while voice is in use.
@available(iOS 26.4, *)
@MainActor
final class CarPlayConversationSceneDelegate: UIResponder, CPTemplateApplicationSceneDelegate {
    private var interfaceController: CPInterfaceController?
    private var voiceTemplate: CPVoiceControlTemplate?

    func templateApplicationScene(
        _ templateApplicationScene: CPTemplateApplicationScene,
        didConnect interfaceController: CPInterfaceController
    ) {
        self.interfaceController = interfaceController
        let startItem = CPListItem(text: "Start a conversation", detailText: nil)
        startItem.handler = { [weak self] _, completion in
            MainActor.assumeIsolated { self?.beginVoice() }
            completion()
        }
        let root = CPListTemplate(title: "Assistant", sections: [CPListSection(items: [startItem])])

        Task {
            do {
                // A list root with the voice template presented over it is the documented path.
                _ = try await interfaceController.setRootTemplate(root, animated: false)
                beginVoice()
            } catch {
                NSLog("CarPlay root template failed: %@", String(describing: error))
            }
        }
    }

    func templateApplicationScene(
        _ templateApplicationScene: CPTemplateApplicationScene,
        didDisconnectInterfaceController interfaceController: CPInterfaceController
    ) {
        endVoice(dismissTemplate: false)
        self.interfaceController = nil
    }

    private func makeVoiceTemplate() -> CPVoiceControlTemplate {
        let end = CPButton(image: UIImage(systemName: "xmark") ?? UIImage()) { [weak self] _ in
            MainActor.assumeIsolated { self?.endVoice(dismissTemplate: true) }
        }
        let states = [ConversationPhase.listening, .thinking, .speaking].map { phase in
            let state = CPVoiceControlState(
                identifier: phase.rawValue,
                titleVariants: [phase.rawValue.capitalized],
                image: nil,
                repeats: true
            )
            state.actionButtons = [end]
            return state
        }
        return CPVoiceControlTemplate(voiceControlStates: states)
    }

    private func beginVoice() {
        guard let interfaceController, let engine = ConversationServices.engine else { return }
        let template = makeVoiceTemplate()
        voiceTemplate = template
        Task {
            do {
                if #available(iOS 27.0, *) {
                    _ = try await interfaceController.showOverlayTemplate(template, animated: true)
                } else {
                    _ = try await interfaceController.presentTemplate(template, animated: true)
                }
                // States can only be activated once the template is on screen.
                try startCapture(engine: engine, template: template)
            } catch {
                NSLog("Voice session failed to start: %@", String(describing: error))
                endVoice(dismissTemplate: true)
            }
        }
    }

    private func startCapture(engine: any ConversationEngine, template: CPVoiceControlTemplate) throws {
        let session = AVAudioSession.sharedInstance()
        // Voice chat audio for the car: record and play, no mixing with other audio.
        try session.setCategory(.playAndRecord, mode: .default, options: [.allowBluetoothHFP])
        try session.setActive(true)
        engine.onPhaseChange = { phase in
            template.activateVoiceControlState(withIdentifier: phase.rawValue)
        }
        template.activateVoiceControlState(withIdentifier: ConversationPhase.listening.rawValue)
        try engine.start()
    }

    private func endVoice(dismissTemplate: Bool) {
        ConversationServices.engine?.stop()
        ConversationServices.engine?.onPhaseChange = nil
        do {
            try AVAudioSession.sharedInstance().setActive(false, options: .notifyOthersOnDeactivation)
        } catch {
            NSLog("Audio session deactivation failed: %@", String(describing: error))
        }
        guard dismissTemplate, voiceTemplate != nil, let interfaceController else {
            voiceTemplate = nil
            return
        }
        voiceTemplate = nil
        Task {
            do {
                if #available(iOS 27.0, *) {
                    _ = try await interfaceController.hideOverlayTemplate(animated: true)
                } else {
                    _ = try await interfaceController.dismissTemplate(animated: true)
                }
            } catch {
                NSLog("Voice template dismissal failed: %@", String(describing: error))
            }
        }
    }
}
