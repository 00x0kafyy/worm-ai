# StreamFusion

A native macOS Swift app that combines **Twitch streams** and **YouTube Music** for gaming.

## Features

- ✅ **Side-by-side view** - Twitch + YouTube Music simultaneously
- ✅ **Native macOS performance** - Swift, WebKit, minimal resource usage
- ✅ **Quick source switching** - Toolbar buttons or global hotkey
- ✅ **Unified volume control** - Single slider controls both sources
- ✅ **Gaming optimized** - Lightweight, overlay-friendly, background audio

## Architecture

```
StreamFusion/
├── Sources/
│   └── StreamFusion/
│       └── main.swift          # Native Swift app
├── Package.swift               # Swift Package Manager
└── build.sh                    # Build script
```

## Building

```bash
# Using Swift Package Manager
swift build

# Or use the build script
./build.sh
```

## Usage

1. **Twitch** - Enter channel name, watch streams
2. **YouTube Music** - Sign in, play your playlists
3. **Both** - Side-by-side for gaming + music

## Controls

| Action | Method |
|--------|--------|
| Switch source | Toolbar buttons or Cmd+Tab |
| Adjust volume | Unified volume slider |
| Resize panes | Drag split view divider |

## Requirements

- macOS 11.0+
- Xcode 13+ (for building)
- Swift 5.5+

## Gaming Setup

Perfect for:
- Watching Twitch while gaming
- Background music from YouTube Music
- Low-latency audio mixing
- Stream overlay integration

---

Built with ❤️ using native Swift + WebKit
