//
//  main.swift
//  StreamFusion
//
//  Native macOS app combining Twitch and YouTube Music
//  For gaming streams - lightweight, overlay-friendly
//

import Cocoa
import WebKit
import AVFoundation
import Combine

// MARK: - App Entry
@main
struct StreamFusionApp {
    static func main() {
        let app = NSApplication.shared
        let delegate = AppDelegate()
        app.delegate = delegate
        app.run()
    }
}

// MARK: - App Delegate
class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow?
    var mainViewController: MainViewController?
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Create main window
        let window = NSWindow(
            contentRect: NSRect(x: 100, y: 100, width: 1200, height: 800),
            styleMask: [.titled, .closable, .miniaturizable, .resizable, .fullSizeContentView],
            backing: .buffered,
            defer: false
        )
        window.title = "StreamFusion - Twitch + YouTube Music"
        window.minSize = NSSize(width: 900, height: 600)
        
        // Create main view controller
        let mainVC = MainViewController()
        window.contentViewController = mainVC
        self.mainViewController = mainVC
        
        window.makeKeyAndOrderFront(nil)
        self.window = window
        
        // Setup global hotkeys
        setupGlobalHotkeys()
    }
    
    func setupGlobalHotkeys() {
        // Global hotkey for quick source switching
        // Uses Carbon API for global hotkeys
        NSEvent.addGlobalMonitorForEvents(matching: .keyDown) { event in
            if event.modifierFlags.contains(.command) && event.keyCode == 48 {
                // Cmd+Tab to switch sources
                self.mainViewController?.toggleSource()
            }
        }
    }
}

// MARK: - Main View Controller
class MainViewController: NSViewController {
    
    // MARK: Properties
    var twitchPlayer: TwitchPlayerView?
    var youtubeMusicPlayer: YouTubeMusicPlayerView?
    var currentSource: StreamSource = .twitch
    
    var splitView: NSSplitView?
    var toolbarView: NSView?
    var volumeSlider: NSSlider?
    
    var cancellables = Set<AnyCancellable>()
    
    // MARK: Enums
    enum StreamSource {
        case twitch
        case youtubeMusic
        case both
    }
    
    // MARK: Lifecycle
    override func loadView() {
        self.view = NSView(frame: NSRect(x: 0, y: 0, width: 1200, height: 800))
        self.view.wantsLayer = true
        self.view.layer?.backgroundColor = NSColor.black.cgColor
    }
    
    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupConstraints()
    }
    
    // MARK: UI Setup
    func setupUI() {
        // Toolbar
        let toolbar = createToolbar()
        self.toolbarView = toolbar
        view.addSubview(toolbar)
        
        // Split view for side-by-side or tabbed interface
        let split = NSSplitView()
        split.translatesAutoresizingMaskIntoConstraints = false
        split.isVertical = true
        split.dividerStyle = .thin
        split.delegate = self
        self.splitView = split
        
        // Twitch Player
        let twitchView = TwitchPlayerView()
        twitchView.translatesAutoresizingMaskIntoConstraints = false
        self.twitchPlayer = twitchView
        
        // YouTube Music Player
        let ytView = YouTubeMusicPlayerView()
        ytView.translatesAutoresizingMaskIntoConstraints = false
        self.youtubeMusicPlayer = ytView
        
        // Add to split view
        split.addArrangedSubview(twitchView)
        split.addArrangedSubview(ytView)
        
        // Set initial sizes
        split.setPosition(600, ofDividerAt: 0)
        
        view.addSubview(split)
        
        // Set initial state - show both
        currentSource = .both
    }
    
    func createToolbar() -> NSView {
        let toolbar = NSView()
        toolbar.translatesAutoresizingMaskIntoConstraints = false
        toolbar.wantsLayer = true
        toolbar.layer?.backgroundColor = NSColor.darkGray.cgColor
        
        // Title
        let titleLabel = NSTextField(labelWithString: "StreamFusion")
        titleLabel.font = NSFont.boldSystemFont(ofSize: 16)
        titleLabel.textColor = .white
        titleLabel.translatesAutoresizingMaskIntoConstraints = false
        toolbar.addSubview(titleLabel)
        
        // Twitch Button
        let twitchBtn = createToolbarButton(title: "Twitch", color: .systemPurple)
        twitchBtn.target = self
        twitchBtn.action = #selector(showTwitch)
        toolbar.addSubview(twitchBtn)
        
        // YouTube Music Button
        let ytBtn = createToolbarButton(title: "YouTube Music", color: .systemRed)
        ytBtn.target = self
        ytBtn.action = #selector(showYouTubeMusic)
        toolbar.addSubview(ytBtn)
        
        // Both Button
        let bothBtn = createToolbarButton(title: "Both", color: .systemBlue)
        bothBtn.target = self
        bothBtn.action = #selector(showBoth)
        toolbar.addSubview(bothBtn)
        
        // Volume Slider
        let volumeLabel = NSTextField(labelWithString: "Volume:")
        volumeLabel.textColor = .white
        volumeLabel.translatesAutoresizingMaskIntoConstraints = false
        toolbar.addSubview(volumeLabel)
        
        let slider = NSSlider(value: 1.0, minValue: 0.0, maxValue: 1.0, target: self, action: #selector(volumeChanged))
        slider.translatesAutoresizingMaskIntoConstraints = false
        self.volumeSlider = slider
        toolbar.addSubview(slider)
        
        // Layout constraints for toolbar
        NSLayoutConstraint.activate([
            toolbar.heightAnchor.constraint(equalToConstant: 50),
            
            titleLabel.leadingAnchor.constraint(equalTo: toolbar.leadingAnchor, constant: 20),
            titleLabel.centerYAnchor.constraint(equalTo: toolbar.centerYAnchor),
            
            twitchBtn.leadingAnchor.constraint(equalTo: titleLabel.trailingAnchor, constant: 30),
            twitchBtn.centerYAnchor.constraint(equalTo: toolbar.centerYAnchor),
            twitchBtn.widthAnchor.constraint(equalToConstant: 80),
            
            ytBtn.leadingAnchor.constraint(equalTo: twitchBtn.trailingAnchor, constant: 10),
            ytBtn.centerYAnchor.constraint(equalTo: toolbar.centerYAnchor),
            ytBtn.widthAnchor.constraint(equalToConstant: 120),
            
            bothBtn.leadingAnchor.constraint(equalTo: ytBtn.trailingAnchor, constant: 10),
            bothBtn.centerYAnchor.constraint(equalTo: toolbar.centerYAnchor),
            bothBtn.widthAnchor.constraint(equalToConstant: 80),
            
            volumeLabel.leadingAnchor.constraint(equalTo: bothBtn.trailingAnchor, constant: 30),
            volumeLabel.centerYAnchor.constraint(equalTo: toolbar.centerYAnchor),
            
            slider.leadingAnchor.constraint(equalTo: volumeLabel.trailingAnchor, constant: 10),
            slider.centerYAnchor.constraint(equalTo: toolbar.centerYAnchor),
            slider.widthAnchor.constraint(equalToConstant: 150),
            
            slider.trailingAnchor.constraint(lessThanOrEqualTo: toolbar.trailingAnchor, constant: -20)
        ])
        
        return toolbar
    }
    
    func createToolbarButton(title: String, color: NSColor) -> NSButton {
        let btn = NSButton(title: title, target: nil, action: nil)
        btn.bezelStyle = .rounded
        btn.translatesAutoresizingMaskIntoConstraints = false
        btn.contentTintColor = color
        return btn
    }
    
    func setupConstraints() {
        guard let toolbar = toolbarView, let split = splitView else { return }
        
        NSLayoutConstraint.activate([
            toolbar.topAnchor.constraint(equalTo: view.topAnchor),
            toolbar.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            toolbar.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            
            split.topAnchor.constraint(equalTo: toolbar.bottomAnchor),
            split.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            split.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            split.bottomAnchor.constraint(equalTo: view.bottomAnchor)
        ])
    }
    
    // MARK: Actions
    @objc func showTwitch() {
        currentSource = .twitch
        splitView?.setPosition(view.bounds.width, ofDividerAt: 0)
        twitchPlayer?.isHidden = false
        youtubeMusicPlayer?.isHidden = true
    }
    
    @objc func showYouTubeMusic() {
        currentSource = .youtubeMusic
        splitView?.setPosition(0, ofDividerAt: 0)
        twitchPlayer?.isHidden = true
        youtubeMusicPlayer?.isHidden = false
    }
    
    @objc func showBoth() {
        currentSource = .both
        splitView?.setPosition(view.bounds.width / 2, ofDividerAt: 0)
        twitchPlayer?.isHidden = false
        youtubeMusicPlayer?.isHidden = false
    }
    
    @objc func volumeChanged(_ sender: NSSlider) {
        let volume = sender.doubleValue
        twitchPlayer?.setVolume(volume)
        youtubeMusicPlayer?.setVolume(volume)
    }
    
    func toggleSource() {
        switch currentSource {
        case .twitch:
            showYouTubeMusic()
        case .youtubeMusic:
            showBoth()
        case .both:
            showTwitch()
        }
    }
}

// MARK: - Split View Delegate
extension MainViewController: NSSplitViewDelegate {
    func splitView(_ splitView: NSSplitView, constrainSplitPosition proposedPosition: CGFloat, ofSubviewAt dividerIndex: Int) -> CGFloat {
        // Minimum width for each pane
        let minWidth: CGFloat = 300
        let maxPosition = view.bounds.width - minWidth
        return min(max(proposedPosition, minWidth), maxPosition)
    }
}

// MARK: - Twitch Player View
class TwitchPlayerView: NSView {
    var webView: WKWebView?
    var streamUrl: String = "https://www.twitch.tv/directory/game/Just%20Chatting"
    
    override init(frame frameRect: NSRect) {
        super.init(frame: frameRect)
        setupWebView()
        loadStream()
    }
    
    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupWebView()
        loadStream()
    }
    
    func setupWebView() {
        let config = WKWebViewConfiguration()
        config.preferences.javaScriptEnabled = true
        config.allowsAirPlayForMediaPlayback = true
        
        // Enable media playback
        config.mediaTypesRequiringUserActionForPlayback = []
        
        // Allow autoplay
        if #available(macOS 10.12, *) {
            config.mediaTypesRequiringUserActionForPlayback = []
        }
        
        let webView = WKWebView(frame: bounds, configuration: config)
        webView.translatesAutoresizingMaskIntoConstraints = false
        webView.navigationDelegate = self
        
        addSubview(webView)
        NSLayoutConstraint.activate([
            webView.topAnchor.constraint(equalTo: topAnchor),
            webView.leadingAnchor.constraint(equalTo: leadingAnchor),
            webView.trailingAnchor.constraint(equalTo: trailingAnchor),
            webView.bottomAnchor.constraint(equalTo: bottomAnchor)
        ])
        
        self.webView = webView
    }
    
    func loadStream() {
        // Load Twitch with audio-only optimization
        let url = URL(string: streamUrl)!
        let request = URLRequest(url: url)
        webView?.load(request)
    }
    
    func setVolume(_ volume: Double) {
        // Execute JavaScript to control volume
        let script = "document.querySelector('video').volume = \(volume);"
        webView?.evaluateJavaScript(script, completionHandler: nil)
    }
    
    func loadChannel(_ channel: String) {
        streamUrl = "https://www.twitch.tv/\(channel)"
        loadStream()
    }
}

extension TwitchPlayerView: WKNavigationDelegate {
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        // Inject JavaScript to optimize for audio/gaming
        let optimizationScript = """
            // Hide UI elements, keep only essential controls
            document.querySelectorAll('[data-a-target="stream-chat"]').forEach(el => el.style.display = 'none');
            document.querySelectorAll('[data-a-target="right-column-chat-bar"]').forEach(el => el.style.display = 'none');
            
            // Auto-play
            const video = document.querySelector('video');
            if (video) {
                video.play();
                video.muted = false;
            }
        """
        webView.evaluateJavaScript(optimizationScript, completionHandler: nil)
    }
}

// MARK: - YouTube Music Player View
class YouTubeMusicPlayerView: NSView {
    var webView: WKWebView?
    
    override init(frame frameRect: NSRect) {
        super.init(frame: frameRect)
        setupWebView()
        loadYouTubeMusic()
    }
    
    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setupWebView()
        loadYouTubeMusic()
    }
    
    func setupWebView() {
        let config = WKWebViewConfiguration()
        config.preferences.javaScriptEnabled = true
        config.allowsAirPlayForMediaPlayback = true
        config.mediaTypesRequiringUserActionForPlayback = []
        
        // Enable media in background
        config.preferences.setValue(true, forKey: "allowsPictureInPictureMediaPlayback")
        
        let webView = WKWebView(frame: bounds, configuration: config)
        webView.translatesAutoresizingMaskIntoConstraints = false
        webView.navigationDelegate = self
        
        addSubview(webView)
        NSLayoutConstraint.activate([
            webView.topAnchor.constraint(equalTo: topAnchor),
            webView.leadingAnchor.constraint(equalTo: leadingAnchor),
            webView.trailingAnchor.constraint(equalTo: trailingAnchor),
            webView.bottomAnchor.constraint(equalTo: bottomAnchor)
        ])
        
        self.webView = webView
    }
    
    func loadYouTubeMusic() {
        let url = URL(string: "https://music.youtube.com")!
        let request = URLRequest(url: url)
        webView?.load(request)
    }
    
    func setVolume(_ volume: Double) {
        let script = "document.querySelector('video, audio').volume = \(volume);"
        webView?.evaluateJavaScript(script, completionHandler: nil)
    }
    
    func playPlaylist(_ playlistId: String) {
        let url = URL(string: "https://music.youtube.com/playlist?list=\(playlistId)")!
        let request = URLRequest(url: url)
        webView?.load(request)
    }
}

extension YouTubeMusicPlayerView: WKNavigationDelegate {
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        // Optimize YouTube Music for background audio
        let optimizationScript = """
            // Keep playing in background
            const video = document.querySelector('video');
            if (video) {
                video.addEventListener('pause', function() {
                    video.play();
                });
            }
        """
        webView.evaluateJavaScript(optimizationScript, completionHandler: nil)
    }
}

// MARK: - Extensions
extension NSView {
    var isHidden: Bool {
        get { return self.isHidden }
        set { self.isHidden = newValue }
    }
}
