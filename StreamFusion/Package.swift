// swift-tools-version:5.5
import PackageDescription

let package = Package(
    name: "StreamFusion",
    platforms: [.macOS(.v11)],
    targets: [
        .executableTarget(
            name: "StreamFusion",
            path: "Sources"
        )
    ]
)
