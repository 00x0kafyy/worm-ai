#!/bin/bash
# Quick launcher for streaming mode

cd "$(dirname "$0")"

# Check dependencies
if ! python3 -c "import obswebsocket" 2>/dev/null; then
    echo "Installing OBS WebSocket library..."
    pip3 install obswebsocket-py
fi

echo "🎮 StreamFusion BROADCASTER"
echo "=============================="
echo ""
echo "This app helps you stream TO Twitch"
echo ""
echo "Requirements:"
echo "  1. Install OBS Studio: https://obsproject.com/download"
echo "  2. Enable OBS WebSocket: Tools → WebSocket Server Settings"
echo "  3. Get Twitch Stream Key: https://dashboard.twitch.tv/settings/stream"
echo ""
echo "Starting..."
echo ""

python3 streamfusion_streamer.py
