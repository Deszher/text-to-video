"""Audio Player Class"""
import glob
import os
import sys

import vlc
from PIL import Image
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QLabel, QStyle
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSlider, QPushButton, QHBoxLayout


class MediaPlayer(QWidget):
    def __init__(self, parent=None):
        super(MediaPlayer, self).__init__(parent)
        self.setWindowTitle("Media Player")
        self.setWindowIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
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
        file = glob.glob("1.*")

        for f in file:
            if not f.endswith('.png'):
                im = Image.open(f)
                im = im.resize((500, 400))
                new_file = "1.png"
                im.save(new_file, 'PNG')
        if file:
            pixmap = QPixmap("1.png")
        else:
            pixmap = QPixmap("img/1.png")

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
        # Получаем список всех файлов в текущей директории
        files = os.listdir()

        # Удаляем файлы с расширениями .png, .jpg и .jpeg
        for file in files:
            if file.endswith(('.png', '.jpg', '.jpeg')):
                os.remove(file)

    def play_pause(self):
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.is_paused = True
            self.timer.stop()
        else:
            if self.mediaplayer.play() == -1:
                self.open_file("test.wav")
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
