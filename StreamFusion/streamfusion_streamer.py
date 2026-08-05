#!/usr/bin/env python3
"""
StreamFusion BROADCASTER - Stream to Twitch + YouTube Music
Native streaming integration for gaming
"""

import sys
import os
import json
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QPushButton, QSlider, QLabel, QLineEdit, QToolBar,
    QComboBox, QMessageBox, QDialog, QFormLayout, QGroupBox, QCheckBox,
    QTextEdit, QProgressBar, QTabWidget
)
from PyQt6.QtCore import Qt, QUrl, QTimer, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QAction, QKeySequence, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
import obswebsocket
from obswebsocket import obsws, requests as obs_requests


class OBSController:
    """OBS WebSocket controller for streaming"""
    
    def __init__(self, host="localhost", port=4455, password=None):
        self.host = host
        self.port = port
        self.password = password
        self.ws = None
        self.connected = False
    
    def connect(self):
        try:
            self.ws = obsws(self.host, self.port, self.password)
            self.ws.connect()
            self.connected = True
            return True
        except Exception as e:
            print(f"OBS connection failed: {e}")
            return False
    
    def disconnect(self):
        if self.ws:
            self.ws.disconnect()
            self.connected = False
    
    def start_stream(self):
        if self.connected:
            try:
                self.ws.call(obs_requests.StartStream())
                return True
            except Exception as e:
                print(f"Failed to start stream: {e}")
        return False
    
    def stop_stream(self):
        if self.connected:
            try:
                self.ws.call(obs_requests.StopStream())
                return True
            except Exception as e:
                print(f"Failed to stop stream: {e}")
        return False
    
    def get_stream_status(self):
        if self.connected:
            try:
                response = self.ws.call(obs_requests.GetStreamStatus())
                return {
                    'active': response.getOutputActive(),
                    'reconnecting': response.getReconnecting(),
                    'timecode': response.getOutputTimecode(),
                    'duration': response.getOutputDuration(),
                    'congestion': response.getOutputCongestion(),
                    'bytes': response.getOutputBytes(),
                    'skipped_frames': response.getOutputSkippedFrames(),
                    'total_frames': response.getOutputTotalFrames()
                }
            except:
                pass
        return None


class StreamOutputThread(QThread):
    """Background thread for stream monitoring"""
    status_update = pyqtSignal(dict)
    
    def __init__(self, obs_controller):
        super().__init__()
        self.obs = obs_controller
        self.running = True
    
    def run(self):
        while self.running:
            if self.obs.connected:
                status = self.obs.get_stream_status()
                if status:
                    self.status_update.emit(status)
            self.msleep(1000)  # Update every second
    
    def stop(self):
        self.running = False


class StreamFusionStreamer(QMainWindow):
    """Main streaming application"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StreamFusion BROADCASTER - Stream to Twitch")
        self.setMinimumSize(1400, 900)
        
        self.obs = OBSController()
        self.stream_thread = None
        self.is_streaming = False
        
        self.setup_ui()
        self.setup_streaming_ui()
        self.setup_hotkeys()
        
        # Check OBS connection
        self.check_obs_connection()
    
    def setup_ui(self):
        """Setup main UI"""
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Tab widget for different views
        self.tabs = QTabWidget()
        
        # Tab 1: Dashboard
        self.dashboard = self.create_dashboard()
        self.tabs.addTab(self.dashboard, "📊 Dashboard")
        
        # Tab 2: YouTube Music
        self.music_tab = self.create_music_tab()
        self.tabs.addTab(self.music_tab, "🎵 YouTube Music")
        
        # Tab 3: OBS Preview
        self.obs_tab = self.create_obs_tab()
        self.tabs.addTab(self.obs_tab, "🎥 OBS Preview")
        
        layout.addWidget(self.tabs)
        
        # Status bar
        self.statusBar().showMessage("Ready - Connect OBS to start streaming")
    
    def create_dashboard(self) -> QWidget:
        """Create streaming dashboard"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Left panel - Stream Controls
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Connection group
        conn_group = QGroupBox("OBS Connection")
        conn_layout = QFormLayout()
        
        self.obs_host = QLineEdit("localhost")
        self.obs_port = QLineEdit("4455")
        self.obs_password = QLineEdit()
        self.obs_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.obs_password.setPlaceholderText("OBS WebSocket Password")
        
        conn_layout.addRow("Host:", self.obs_host)
        conn_layout.addRow("Port:", self.obs_port)
        conn_layout.addRow("Password:", self.obs_password)
        
        self.connect_btn = QPushButton("🔗 Connect to OBS")
        self.connect_btn.clicked.connect(self.connect_obs)
        conn_layout.addRow(self.connect_btn)
        
        self.obs_status = QLabel("❌ Not Connected")
        self.obs_status.setStyleSheet("color: red;")
        conn_layout.addRow("Status:", self.obs_status)
        
        conn_group.setLayout(conn_layout)
        left_layout.addWidget(conn_group)
        
        # Stream controls group
        stream_group = QGroupBox("Stream Controls")
        stream_layout = QVBoxLayout()
        
        # Twitch stream key
        twitch_layout = QFormLayout()
        self.stream_key = QLineEdit()
        self.stream_key.setEchoMode(QLineEdit.EchoMode.Password)
        self.stream_key.setPlaceholderText("Twitch Stream Key (from OBS)")
        twitch_layout.addRow("Stream Key:", self.stream_key)
        
        # Stream title
        self.stream_title = QLineEdit("Gaming Stream - StreamFusion")
        twitch_layout.addRow("Stream Title:", self.stream_title)
        
        stream_layout.addLayout(twitch_layout)
        
        # Control buttons
        btn_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("🔴 Start Stream")
        self.start_btn.setStyleSheet("background-color: #ff4444; color: white; font-weight: bold;")
        self.start_btn.clicked.connect(self.start_stream)
        self.start_btn.setEnabled(False)
        
        self.stop_btn = QPushButton("⏹ Stop Stream")
        self.stop_btn.setStyleSheet("background-color: #4444ff; color: white;")
        self.stop_btn.clicked.connect(self.stop_stream)
        self.stop_btn.setEnabled(False)
        
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        
        stream_layout.addLayout(btn_layout)
        
        # Stream stats
        self.stats_label = QLabel("Stream Stats: Not streaming")
        stream_layout.addWidget(self.stats_label)
        
        self.stream_time = QLabel("Duration: 00:00:00")
        stream_layout.addWidget(self.stream_time)
        
        stream_group.setLayout(stream_layout)
        left_layout.addWidget(stream_group)
        
        # Scene controls
        scene_group = QGroupBox("Quick Scene Switch")
        scene_layout = QVBoxLayout()
        
        self.scene_combo = QComboBox()
        self.scene_combo.addItems(["Gaming", "Just Chatting", "BRB", "Starting Soon"])
        scene_layout.addWidget(self.scene_combo)
        
        switch_btn = QPushButton("🎬 Switch Scene")
        switch_btn.clicked.connect(self.switch_scene)
        scene_layout.addWidget(switch_btn)
        
        # Quick toggles
        self.mic_checkbox = QCheckBox("🎤 Microphone")
        self.mic_checkbox.setChecked(True)
        self.mic_checkbox.stateChanged.connect(self.toggle_mic)
        scene_layout.addWidget(self.mic_checkbox)
        
        self.desktop_checkbox = QCheckBox("🔊 Desktop Audio")
        self.desktop_checkbox.setChecked(True)
        scene_layout.addWidget(self.desktop_checkbox)
        
        scene_group.setLayout(scene_layout)
        left_layout.addWidget(scene_group)
        
        left_layout.addStretch()
        layout.addWidget(left_panel, 1)
        
        # Right panel - Chat + Preview
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Chat view
        chat_label = QLabel("Twitch Chat")
        right_layout.addWidget(chat_label)
        
        self.chat_view = QWebEngineView()
        self.chat_view.setMinimumHeight(400)
        right_layout.addWidget(self.chat_view, 2)
        
        # Chat input
        chat_input_layout = QHBoxLayout()
        self.chat_input = QLineEdit()
        self.chat_input.setPlaceholderText("Send message to chat...")
        self.chat_input.returnPressed.connect(self.send_chat)
        chat_input_layout.addWidget(self.chat_input)
        
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_chat)
        chat_input_layout.addWidget(send_btn)
        
        right_layout.addLayout(chat_input_layout)
        
        layout.addWidget(right_panel, 2)
        
        return widget
    
    def create_music_tab(self) -> QWidget:
        """Create YouTube Music tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Controls
        controls = QHBoxLayout()
        
        load_playlist_btn = QPushButton("📋 Load Playlist")
        load_playlist_btn.clicked.connect(self.load_playlist)
        controls.addWidget(load_playlist_btn)
        
        self.music_volume = QSlider(Qt.Orientation.Horizontal)
        self.music_volume.setMaximum(100)
        self.music_volume.setValue(50)
        self.music_volume.valueChanged.connect(self.set_music_volume)
        controls.addWidget(QLabel("Volume:"))
        controls.addWidget(self.music_volume)
        
        layout.addLayout(controls)
        
        # Web view
        self.music_view = QWebEngineView()
        self.music_view.load(QUrl("https://music.youtube.com"))
        layout.addWidget(self.music_view)
        
        return widget
    
    def create_obs_tab(self) -> QWidget:
        """Create OBS preview tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info = QLabel("OBS Preview - Install OBS and enable WebSocket to see preview")
        info.setStyleSheet("color: gray; padding: 20px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        # OBS download link
        self.obs_preview = QTextEdit()
        self.obs_preview.setReadOnly(True)
        self.obs_preview.setHtml("""
        <h2>OBS Studio Setup</h2>
        <ol>
            <li><a href='https://obsproject.com/download'>Download OBS Studio</a></li>
            <li>Install and run OBS</li>
            <li>Go to Tools → WebSocket Server Settings</li>
            <li>Enable WebSocket server</li>
            <li>Set password (optional but recommended)</li>
            <li>Click 'Connect to OBS' in StreamFusion</li>
        </ol>
        <h3>Twitch Stream Setup</h3>
        <ol>
            <li>Go to <a href='https://dashboard.twitch.tv/settings/stream'>Twitch Stream Settings</a></li>
            <li>Copy your Stream Key</li>
            <li>In OBS: Settings → Stream → Service: Twitch</li>
            <li>Paste your Stream Key</li>
        </ol>
        """)
        layout.addWidget(self.obs_preview)
        
        return widget
    
    def setup_streaming_ui(self):
        """Setup streaming-specific UI elements"""
        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Stream status
        self.stream_indicator = QLabel("🔴 OFFLINE")
        self.stream_indicator.setStyleSheet("color: red; font-weight: bold; padding: 5px;")
        toolbar.addWidget(self.stream_indicator)
        
        toolbar.addSeparator()
        
        # Quick actions
        start_action = QAction("▶️ Start Stream", self)
        start_action.triggered.connect(self.start_stream)
        toolbar.addAction(start_action)
        
        stop_action = QAction("⏹ Stop Stream", self)
        stop_action.triggered.connect(self.stop_stream)
        toolbar.addAction(stop_action)
        
        toolbar.addSeparator()
        
        # Viewer count (placeholder)
        self.viewer_label = QLabel("👥 Viewers: 0")
        toolbar.addWidget(self.viewer_label)
    
    def setup_hotkeys(self):
        """Setup keyboard shortcuts"""
        # F9 - Start/Stop Stream
        stream_shortcut = QAction(self)
        stream_shortcut.setShortcut(QKeySequence("F9"))
        stream_shortcut.triggered.connect(self.toggle_stream)
        self.addAction(stream_shortcut)
        
        # F10 - Toggle Mic
        mic_shortcut = QAction(self)
        mic_shortcut.setShortcut(QKeySequence("F10"))
        mic_shortcut.triggered.connect(self.toggle_mic_shortcut)
        self.addAction(mic_shortcut)
    
    def check_obs_connection(self):
        """Try to connect to OBS automatically"""
        QTimer.singleShot(1000, self.auto_connect_obs)
    
    def auto_connect_obs(self):
        """Auto-connect to OBS"""
        if self.obs.connect():
            self.obs_connected()
        else:
            self.statusBar().showMessage("OBS not running - Start OBS and click 'Connect to OBS'")
    
    def connect_obs(self):
        """Manual OBS connection"""
        self.obs.host = self.obs_host.text()
        self.obs.port = int(self.obs_port.text())
        self.obs.password = self.obs_password.text() or None
        
        if self.obs.connect():
            self.obs_connected()
            QMessageBox.information(self, "Connected", "Successfully connected to OBS!")
        else:
            QMessageBox.warning(self, "Connection Failed", 
                "Could not connect to OBS.\n\nMake sure OBS is running and WebSocket is enabled.\n"
                "Go to: Tools → WebSocket Server Settings → Enable")
    
    def obs_connected(self):
        """Update UI when OBS connects"""
        self.obs_status.setText("✅ Connected")
        self.obs_status.setStyleSheet("color: green;")
        self.connect_btn.setText("🔄 Reconnect")
        self.start_btn.setEnabled(True)
        
        # Start monitoring thread
        self.stream_thread = StreamOutputThread(self.obs)
        self.stream_thread.status_update.connect(self.update_stream_stats)
        self.stream_thread.start()
        
        self.statusBar().showMessage("Connected to OBS - Ready to stream")
    
    def start_stream(self):
        """Start streaming"""
        if self.obs.start_stream():
            self.is_streaming = True
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.stream_indicator.setText("🟢 LIVE")
            self.stream_indicator.setStyleSheet("color: green; font-weight: bold; padding: 5px;")
            self.statusBar().showMessage("🔴 STREAMING LIVE")
            
            # Load chat
            self.load_chat()
        else:
            QMessageBox.warning(self, "Stream Error", 
                "Failed to start stream. Check OBS settings.")
    
    def stop_stream(self):
        """Stop streaming"""
        if self.obs.stop_stream():
            self.is_streaming = False
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.stream_indicator.setText("🔴 OFFLINE")
            self.stream_indicator.setStyleSheet("color: red; font-weight: bold; padding: 5px;")
            self.statusBar().showMessage("Stream stopped")
            self.stats_label.setText("Stream Stats: Not streaming")
    
    def toggle_stream(self):
        """Toggle stream on/off"""
        if self.is_streaming:
            self.stop_stream()
        else:
            self.start_stream()
    
    def update_stream_stats(self, stats):
        """Update stream statistics"""
        if stats['active']:
            duration = stats['duration'] // 1000  # Convert to seconds
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            
            self.stream_time.setText(f"Duration: {hours:02d}:{minutes:02d}:{seconds:02d}")
            
            stats_text = f"FPS: {stats['total_frames'] // max(duration, 1)} | "
            stats_text += f"Dropped: {stats['skipped_frames']} | "
            stats_text += f"Network: {self.format_bytes(stats['bytes'])}"
            
            self.stats_label.setText(stats_text)
    
    def format_bytes(self, bytes_val):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024
        return f"{bytes_val:.1f} TB"
    
    def switch_scene(self):
        """Switch OBS scene"""
        scene = self.scene_combo.currentText()
        if self.obs.connected:
            try:
                self.obs.ws.call(obs_requests.SetCurrentProgramScene(sceneName=scene))
                self.statusBar().showMessage(f"Switched to scene: {scene}")
            except Exception as e:
                print(f"Scene switch failed: {e}")
    
    def toggle_mic(self, state):
        """Toggle microphone"""
        # Would use obs-websocket to mute/unmute mic source
        pass
    
    def toggle_mic_shortcut(self):
        """Toggle mic via shortcut"""
        self.mic_checkbox.setChecked(not self.mic_checkbox.isChecked())
    
    def load_chat(self):
        """Load Twitch chat"""
        # Extract channel from stream key or settings
        # For now, show generic Twitch chat
        self.chat_view.load(QUrl("https://www.twitch.tv/popout/chat"))
    
    def send_chat(self):
        """Send chat message"""
        msg = self.chat_input.text()
        if msg:
            # Would integrate with Twitch IRC
            self.chat_input.clear()
            self.statusBar().showMessage(f"Chat: {msg}")
    
    def load_playlist(self):
        """Load YouTube Music playlist"""
        # Show dialog for playlist URL
        pass
    
    def set_music_volume(self, value):
        """Set YouTube Music volume"""
        volume = value / 100.0
        js = f"document.querySelector('video').volume = {volume};"
        self.music_view.page().runJavaScript(js)
    
    def closeEvent(self, event):
        """Clean up on close"""
        if self.stream_thread:
            self.stream_thread.stop()
            self.stream_thread.wait()
        if self.obs.connected:
            self.obs.disconnect()
        event.accept()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("StreamFusion Broadcaster")
    
    window = StreamFusionStreamer()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
