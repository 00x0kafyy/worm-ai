#!/usr/bin/env python3
"""
StreamFusion - Twitch + YouTube Music Fusion
Native macOS app using Python + PyQt6 + WebEngine
For gaming streams
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QPushButton, QSlider, QLabel, QLineEdit, QToolBar
)
from PyQt6.QtCore import Qt, QUrl, QSize
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWebEngineWidgets import QWebEngineView


class StreamPlayer(QWidget):
    """Web-based stream player"""
    
    def __init__(self, platform="twitch"):
        super().__init__()
        self.platform = platform
        self.web_view = QWebEngineView()
        self.volume = 1.0
        
        self.setup_ui()
        self.load_default()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.web_view)
    
    def load_default(self):
        if self.platform == "twitch":
            self.load_url("https://www.twitch.tv/directory/game/Just%20Chatting")
        else:
            self.load_url("https://music.youtube.com")
    
    def load_url(self, url):
        self.web_view.setUrl(QUrl(url))
    
    def load_channel(self, channel):
        if self.platform == "twitch":
            self.load_url(f"https://www.twitch.tv/{channel}")
    
    def set_volume(self, volume):
        """Set volume via JavaScript"""
        self.volume = volume
        js = f"document.querySelector('video').volume = {volume};"
        self.web_view.page().runJavaScript(js)
    
    def get_title(self):
        return self.web_view.title()


class StreamFusion(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StreamFusion - Twitch + YouTube Music")
        self.setMinimumSize(1200, 800)
        
        self.setup_ui()
        self.setup_toolbar()
        self.setup_hotkeys()
    
    def setup_ui(self):
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Splitter for side-by-side view
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Twitch player
        self.twitch_player = StreamPlayer("twitch")
        self.twitch_player.setMinimumWidth(400)
        
        # YouTube Music player
        self.yt_player = StreamPlayer("youtube")
        self.yt_player.setMinimumWidth(400)
        
        # Add to splitter
        self.splitter.addWidget(self.twitch_player)
        self.splitter.addWidget(self.yt_player)
        
        # Set equal sizes
        self.splitter.setSizes([600, 600])
        
        layout.addWidget(self.splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready - StreamFusion v1.0")
    
    def setup_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Twitch section
        toolbar.addWidget(QLabel("Twitch: "))
        self.twitch_input = QLineEdit()
        self.twitch_input.setPlaceholderText("Channel name")
        self.twitch_input.setMaximumWidth(150)
        self.twitch_input.returnPressed.connect(self.load_twitch_channel)
        toolbar.addWidget(self.twitch_input)
        
        twitch_btn = QPushButton("Load")
        twitch_btn.clicked.connect(self.load_twitch_channel)
        toolbar.addWidget(twitch_btn)
        
        toolbar.addSeparator()
        
        # View mode buttons
        self.btn_both = QPushButton("Both")
        self.btn_both.setCheckable(True)
        self.btn_both.setChecked(True)
        self.btn_both.clicked.connect(self.show_both)
        toolbar.addWidget(self.btn_both)
        
        self.btn_twitch = QPushButton("Twitch Only")
        self.btn_twitch.setCheckable(True)
        self.btn_twitch.clicked.connect(self.show_twitch_only)
        toolbar.addWidget(self.btn_twitch)
        
        self.btn_yt = QPushButton("YT Music Only")
        self.btn_yt.setCheckable(True)
        self.btn_yt.clicked.connect(self.show_yt_only)
        toolbar.addWidget(self.btn_yt)
        
        toolbar.addSeparator()
        
        # Volume control
        toolbar.addWidget(QLabel("Volume: "))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setMaximumWidth(150)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.valueChanged.connect(self.set_volume)
        toolbar.addWidget(self.volume_slider)
        
        toolbar.addSeparator()
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_players)
        toolbar.addWidget(refresh_btn)
    
    def setup_hotkeys(self):
        # Cmd+1 for Twitch only
        shortcut1 = QAction(self)
        shortcut1.setShortcut(QKeySequence("Ctrl+1"))
        shortcut1.triggered.connect(self.show_twitch_only)
        self.addAction(shortcut1)
        
        # Cmd+2 for YT Music only
        shortcut2 = QAction(self)
        shortcut2.setShortcut(QKeySequence("Ctrl+2"))
        shortcut2.triggered.connect(self.show_yt_only)
        self.addAction(shortcut2)
        
        # Cmd+3 for both
        shortcut3 = QAction(self)
        shortcut3.setShortcut(QKeySequence("Ctrl+3"))
        shortcut3.triggered.connect(self.show_both)
        self.addAction(shortcut3)
    
    def load_twitch_channel(self):
        channel = self.twitch_input.text().strip()
        if channel:
            self.twitch_player.load_channel(channel)
            self.statusBar().showMessage(f"Loading Twitch channel: {channel}")
    
    def show_twitch_only(self):
        self.splitter.setSizes([self.width(), 0])
        self.btn_twitch.setChecked(True)
        self.btn_yt.setChecked(False)
        self.btn_both.setChecked(False)
        self.statusBar().showMessage("Twitch mode")
    
    def show_yt_only(self):
        self.splitter.setSizes([0, self.width()])
        self.btn_twitch.setChecked(False)
        self.btn_yt.setChecked(True)
        self.btn_both.setChecked(False)
        self.statusBar().showMessage("YouTube Music mode")
    
    def show_both(self):
        self.splitter.setSizes([self.width() // 2, self.width() // 2])
        self.btn_twitch.setChecked(False)
        self.btn_yt.setChecked(False)
        self.btn_both.setChecked(True)
        self.statusBar().showMessage("Side-by-side mode")
    
    def set_volume(self, value):
        volume = value / 100.0
        self.twitch_player.set_volume(volume)
        self.yt_player.set_volume(volume)
    
    def refresh_players(self):
        self.twitch_player.web_view.reload()
        self.yt_player.web_view.reload()
        self.statusBar().showMessage("Players refreshed")


def main():
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("StreamFusion")
    app.setApplicationDisplayName("StreamFusion")
    
    # Set style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = StreamFusion()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
