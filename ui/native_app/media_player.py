"""Audio Player Class"""
import sys

import vlc
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QStyle
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QPushButton, QHBoxLayout

from domain.model import ProcessData
from domain.processor import Processor


class MediaPlayer(QWidget):
    processor: Processor
    data: ProcessData

    def __init__(self, processor: Processor, data: ProcessData, parent=None):
        super(MediaPlayer, self).__init__(parent)
        self.processor = processor
        self.data = data

        self.setWindowTitle("Media Player")
        self.setWindowIcon(
            self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        )
        self.resize(800, 600)
        self.instance = vlc.Instance()
        self.media = None
        self.mediaplayer = self.instance.media_player_new()
        self.create_ui()
        self.is_paused = False

    def create_ui(self):
        self.vboxlayout = QVBoxLayout()
        self.setLayout(self.vboxlayout)

        self.videoframe = QLabel()
        self.videoframe.resize(600, 500)

        pixmap = QPixmap(self.processor.get_image_preview(self.data))

        scaled_pixmap = pixmap.scaled(self.videoframe.size())
        self.videoframe.setPixmap(scaled_pixmap)

        self.positionslider = QSlider(self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.positionslider.sliderMoved.connect(self.set_position)
        self.positionslider.sliderPressed.connect(self.set_position)

        self.hbuttonbox = QHBoxLayout()
        self.playbutton = QPushButton("Play")
        self.hbuttonbox.addWidget(self.playbutton)
        self.playbutton.clicked.connect(self.play_pause)
        self.hbuttonbox.addSpacing(10)

        self.nextbutton = QPushButton("Next")
        self.hbuttonbox.addWidget(self.nextbutton)
        self.hbuttonbox.addSpacing(10)

        self.hbuttonbox.addStretch(1)

        self.volumeslider = QSlider(self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("Volume")
        self.hbuttonbox.addWidget(self.volumeslider)
        self.volumeslider.valueChanged.connect(self.set_volume)

        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addWidget(self.positionslider)
        self.vboxlayout.addLayout(self.hbuttonbox)

        open_action = QAction("Load Video", self)
        close_action = QAction("Close App", self)
        open_action.triggered.connect(self.open_file)
        close_action.triggered.connect(sys.exit)

        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)

    def play_pause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.is_paused = True
            self.timer.stop()
        else:
            if self.mediaplayer.play() == -1:
                self.open_file(self.data.audio_file_path)
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.timer.start()
            self.is_paused = False

    def stop(self):
        self.mediaplayer.stop()
        self.playbutton.setText("Play")

    def open_file(self, filename=None):
        if not filename:
            return
        self.media = self.instance.media_new(filename)
        self.mediaplayer.set_media(self.media)
        self.media.parse()
        self.setWindowTitle(self.media.get_meta(0))
        self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
        self.play_pause()

    def set_volume(self, volume):
        self.mediaplayer.audio_set_volume(volume)

    def set_position(self):
        self.timer.stop()
        pos = self.positionslider.value()
        self.mediaplayer.set_position(pos / 100.0)
        self.timer.start()

    def update_ui(self):
        media_pos = int(self.mediaplayer.get_position() * 1000)
        self.positionslider.setValue(media_pos)

        if not self.mediaplayer.is_playing():
            self.timer.stop()
            if not self.is_paused:
                self.stop()
