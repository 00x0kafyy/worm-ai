#!/bin/bash
# StreamFusion Build Script
# Native macOS Swift app builder

set -e

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "StreamFusion Native macOS App Builder"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Configuration
APP_NAME="StreamFusion"
BUNDLE_ID="com.nullframe.streamfusion"
BUILD_DIR="build"
SRC_DIR="StreamFusion"

echo "[1] Creating build directory..."
mkdir -p "$BUILD_DIR"

echo ""
echo "[2] Checking Swift toolchain..."
if ! command -v swift &> /dev/null; then
    echo "❌ Swift not found. Install Xcode Command Line Tools:"
    echo "   xcode-select --install"
    exit 1
fi

echo "✓ Swift version: $(swift --version | head -1)"

echo ""
echo "[3] Building StreamFusion..."

# Create app bundle structure
APP_BUNDLE="$BUILD_DIR/$APP_NAME.app"
mkdir -p "$APP_BUNDLE/Contents/MacOS"
mkdir -p "$APP_BUNDLE/Contents/Resources"

# Compile Swift code
cd "$SRC_DIR"

# Check if we can use swiftc directly
if swiftc -help &>/dev/null; then
    echo "Building with swiftc..."
    swiftc \
        -o "../$APP_BUNDLE/Contents/MacOS/$APP_NAME" \
        -framework Cocoa \
        -framework WebKit \
        -framework AVFoundation \
        -framework Combine \
        -target x86_64-apple-macos11 \
        main.swift 2>&1 || {
        echo "⚠️  Build failed. Creating Xcode project instead..."
        cd ..
        ./create_xcode_project.sh
        exit 0
    }
else
    echo "⚠️  swiftc not available. Creating Xcode project..."
    cd ..
    ./create_xcode_project.sh
    exit 0
fi

cd ..

echo ""
echo "[4] Copying resources..."
cp "$SRC_DIR/Info.plist" "$APP_BUNDLE/Contents/Info.plist"

echo ""
echo "[5] Creating icon..."
# Create a simple app icon using sips if available
if command -v sips &> /dev/null; then
    echo "Creating app icon..."
    # Create a simple colored square as icon
    mkdir -p "$BUILD_DIR/icon.iconset"
    
    # Generate icons at different sizes
    for size in 16 32 128 256 512; do
        sips -z $size $size \
            /System/Library/CoreServices/CoreTypes.bundle/Contents/Resources/GenericApplicationIcon.icns \
            --out "$BUILD_DIR/icon.iconset/icon_${size}x${size}.png" 2>/dev/null || true
    done
    
    # Convert to icns
    if command -v iconutil &> /dev/null; then
        iconutil -c icns "$BUILD_DIR/icon.iconset" -o "$APP_BUNDLE/Contents/Resources/AppIcon.icns" 2>/dev/null || true
    fi
fi

echo ""
echo "[6] Setting permissions..."
chmod +x "$APP_BUNDLE/Contents/MacOS/$APP_NAME"

echo ""
echo "[7] Signing..."
codesign --force --deep --sign - "$APP_BUNDLE" 2>/dev/null || echo "⚠️  Self-signed (expected for local builds)"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "Build Complete!"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "App Location: $PWD/$APP_BUNDLE"
echo ""
echo "To run:"
echo "  open '$APP_BUNDLE'"
echo ""
echo "Or copy to Applications:"
echo "  cp -r '$APP_BUNDLE' /Applications/"
echo ""
echo "Features:"
echo "  ✓ Side-by-side Twitch + YouTube Music"
echo "  ✓ Global hotkey (Cmd+Tab to switch)"
echo "  ✓ Unified volume control"
echo "  ✓ Native macOS performance"
echo ""
