import AVFoundation
import MediaPlayer

// One app-lifetime owner for playback, shared by the phone UI, CarPlay and HomeView.
// It publishes Now Playing through MediaPlayer. If the app adopts the iOS 27 NowPlaying
// framework instead, replace this whole type: Apple documents mixing the two as undefined behavior.
@MainActor
final class PlaybackService {
    static let shared = PlaybackService()

    enum PlaybackError: LocalizedError {
        case sessionActivationFailed(Error)

        var errorDescription: String? {
            switch self {
            case .sessionActivationFailed(let underlying):
                return "The audio session could not be activated: \(underlying.localizedDescription)"
            }
        }
    }

    struct Item: Sendable {
        let id: String
        let title: String
        let url: URL
        let isVideo: Bool
    }

    /// The app fills this from its own store at launch; the car lists read it.
    var catalogue: [Item] = []

    private let player = AVPlayer()
    private var current: Item?
    private var isPrepared = false
    private var timeObserver: Any?

    private init() {}

    func prepare() {
        guard !isPrepared else { return }
        isPrepared = true
        // Video with an audio component plays on the car or HomeView display over AirPlay.
        player.allowsExternalPlayback = true
        registerRemoteCommands()
        timeObserver = player.addPeriodicTimeObserver(
            forInterval: CMTime(seconds: 1, preferredTimescale: 1),
            queue: .main
        ) { _ in
            MainActor.assumeIsolated { PlaybackService.shared.publishNowPlaying() }
        }
    }

    /// Activates the session only now, when there is something to play: activating it earlier
    /// silences the car's radio for nothing.
    func play(_ item: Item) throws {
        prepare()
        let session = AVAudioSession.sharedInstance()
        do {
            try session.setCategory(.playback, mode: item.isVideo ? .moviePlayback : .default, policy: .longFormAudio)
            try session.setActive(true)
        } catch {
            throw PlaybackError.sessionActivationFailed(error)
        }
        current = item
        player.replaceCurrentItem(with: AVPlayerItem(url: item.url))
        player.play()
        publishNowPlaying()
    }

    func resume() -> MPRemoteCommandHandlerStatus {
        guard player.currentItem != nil else { return .noSuchContent }
        player.play()
        publishNowPlaying()
        return .success
    }

    func pause() -> MPRemoteCommandHandlerStatus {
        player.pause()
        publishNowPlaying()
        return .success
    }

    private func registerRemoteCommands() {
        let commands = MPRemoteCommandCenter.shared()
        commands.playCommand.addTarget { _ in
            MainActor.assumeIsolated { PlaybackService.shared.resume() }
        }
        commands.pauseCommand.addTarget { _ in
            MainActor.assumeIsolated { PlaybackService.shared.pause() }
        }
    }

    /// Publishes what the player is actually doing, not what was requested.
    private func publishNowPlaying() {
        guard let current, let playerItem = player.currentItem else {
            MPNowPlayingInfoCenter.default().nowPlayingInfo = nil
            return
        }
        var info: [String: Any] = [
            MPMediaItemPropertyTitle: current.title,
            MPNowPlayingInfoPropertyElapsedPlaybackTime: player.currentTime().seconds,
            MPNowPlayingInfoPropertyPlaybackRate: Double(player.rate),
            MPNowPlayingInfoPropertyMediaType: current.isVideo
                ? MPNowPlayingInfoMediaType.video.rawValue
                : MPNowPlayingInfoMediaType.audio.rawValue
        ]
        let duration = playerItem.duration.seconds
        if duration.isFinite {
            info[MPMediaItemPropertyPlaybackDuration] = duration
        }
        MPNowPlayingInfoCenter.default().nowPlayingInfo = info
    }
}
