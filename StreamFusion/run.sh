#!/bin/bash
# StreamFusion Launcher

cd "$(dirname "$0")"

# Check for PyQt6
if ! python3 -c "import PyQt6, PyQt6.QtWebEngineWidgets" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install PyQt6 PyQt6-WebEngine
fi

# Run StreamFusion
echo "🎮 Starting StreamFusion..."
python3 streamfusion.py
