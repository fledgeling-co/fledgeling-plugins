import UIKit
@preconcurrency import CarPlay

/// CarPlay scene for an app holding `com.apple.developer.carplay-audio` (or `-video`).
/// The same scene is what HomeView shows when the paired iPhone is nearby: Apple runs eligible
/// audio and video apps there without any change to the app.
@MainActor
final class CarPlayMediaSceneDelegate: UIResponder, CPTemplateApplicationSceneDelegate {
    private var interfaceController: CPInterfaceController?
    private var sessionConfiguration: CPSessionConfiguration?

    func templateApplicationScene(
        _ templateApplicationScene: CPTemplateApplicationScene,
        didConnect interfaceController: CPInterfaceController
    ) {
        self.interfaceController = interfaceController
        sessionConfiguration = CPSessionConfiguration(delegate: self)
        PlaybackService.shared.prepare()

        // Configure Now Playing before the root is up: the car's own Now Playing button can open it first.
        if #available(iOS 27.0, *) {
            CPNowPlayingTemplate.shared.allowsMiniPlayer = true
        }

        Task {
            do {
                _ = try await interfaceController.setRootTemplate(makeRootTemplate(), animated: false)
            } catch {
                // A root that fails to install leaves a blank car screen; surface it, never swallow it.
                NSLog("CarPlay root template failed: %@", String(describing: error))
            }
        }
    }

    func templateApplicationScene(
        _ templateApplicationScene: CPTemplateApplicationScene,
        didDisconnectInterfaceController interfaceController: CPInterfaceController
    ) {
        // Playback is the phone's to keep; disconnecting the car does not stop it.
        self.interfaceController = nil
        sessionConfiguration = nil
    }

    private func makeRootTemplate() -> CPTemplate {
        var tabs: [CPTemplate] = [makeList(title: "Listen", symbol: "headphones", items: audioItems())]
        if #available(iOS 26.4, *), sessionConfiguration?.supportsVideoPlayback == true {
            tabs.append(makeList(title: "Watch", symbol: "play.tv", items: videoItems()))
        }
        // The tab limit depends on the entitlement (4 for audio today); read it, never hard-code it.
        return CPTabBarTemplate(templates: Array(tabs.prefix(CPTabBarTemplate.maximumTabCount)))
    }

    private func makeList(title: String, symbol: String, items: [PlaybackService.Item]) -> CPListTemplate {
        // Some cars show only 12 rows; the template reports what this car allows.
        let limit = CPListTemplate.maximumItemCount
        let rows = items.prefix(limit).map(makeRow)
        let list = CPListTemplate(title: title, sections: [CPListSection(items: Array(rows))])
        list.tabTitle = title
        list.tabImage = UIImage(systemName: symbol)
        return list
    }

    private func makeRow(_ item: PlaybackService.Item) -> CPListItem {
        let row = CPListItem(text: item.title, detailText: nil)
        if #available(iOS 26.4, *) {
            row.playbackConfiguration = CPPlaybackConfiguration(
                preferredPresentation: item.isVideo ? .video : .audio,
                playbackAction: .play,
                elapsedTime: .zero,
                duration: .indefinite
            )
        }
        row.handler = { [weak self] _, completion in
            MainActor.assumeIsolated {
                self?.start(item, from: row)
            }
            completion()
        }
        return row
    }

    private func start(_ item: PlaybackService.Item, from row: CPListItem) {
        do {
            try PlaybackService.shared.play(item)
        } catch {
            row.setDetailText("Can't play right now")
            return
        }
        guard let interfaceController else { return }
        Task {
            do {
                _ = try await interfaceController.pushTemplate(CPNowPlayingTemplate.shared, animated: true)
            } catch {
                NSLog("Now Playing push failed: %@", String(describing: error))
            }
        }
    }

    private func audioItems() -> [PlaybackService.Item] { PlaybackService.shared.catalogue.filter { !$0.isVideo } }
    private func videoItems() -> [PlaybackService.Item] { PlaybackService.shared.catalogue.filter(\.isVideo) }
}

extension CarPlayMediaSceneDelegate: CPSessionConfigurationDelegate {
    nonisolated func sessionConfiguration(
        _ sessionConfiguration: CPSessionConfiguration,
        contentStyleChanged contentStyle: CPContentStyle
    ) {
        // Templates restyle themselves; only custom imagery needs to react to day and night here.
    }
}
