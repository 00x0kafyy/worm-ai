#!/bin/bash
# StreamFusion v2.0 Launcher

cd "$(dirname "$0")"

echo "🔥 StreamFusion v2.0 - ULTIMATE STREAMING PLATFORM"
echo "═══════════════════════════════════════════════════"
echo ""

# Check dependencies
if ! python3 -c "import PyQt6" 2>/dev/null; then
    echo "Installing PyQt6..."
    pip3 install PyQt6 PyQt6-WebEngine
fi

if ! python3 -c "import psutil" 2>/dev/null; then
    echo "Installing psutil..."
    pip3 install psutil
fi

if ! python3 -c "import obswebsocket" 2>/dev/null; then
    echo "Installing OBS WebSocket..."
    pip3 install obswebsocket-py
fi

echo ""
echo "🎮 Features Included:"
echo "   📡 Streaming & Output: Multi-platform, Vertical streams, Recording, Replay buffer"
echo "   🎬 Scenes & Production: Auto-switching, BRB timers, Overlay editor"
echo "   🎮 Game Integration: Auto-detection, Game profiles, Speedrun timer"
echo "   💬 Chat & Engagement: Bot, Loyalty points, TTS, Polls"
echo "   🔊 Audio & Music: Visualizer, Filters, Voice changer"
echo "   🤖 AI & Automation: Highlight detection, Sentiment analysis"
echo "   📈 Metrics: Real-time graphs, Stream health"
echo ""
echo "Starting StreamFusion v2.0..."
echo ""

python3 streamfusion_v2.py
