from PyQt6.QtWidgets import QMainWindow

from ui.native_app.media_player import MediaPlayer
from ui.native_app.tool_tab import UIToolTab
from ui.native_app.end_window import UIEndWindow
from ui.native_app.head_window import UIWindow
from domain.processor import Processor
from domain.model import ProcessData


class MainWindow(QMainWindow):
    processor: Processor
    data: ProcessData

    def __init__(self, processor: Processor, parent=None):
        super(MainWindow, self).__init__(parent)
        self.processor = processor

        self.setGeometry(50, 50, 400, 450)
        self.x, self.y = 700, 500
        self.setFixedSize(self.x, self.y)
        self.setWindowTitle("Говорящая голова")
        self.startUIToolTab()

    def startUIToolTab(self):
        self.data = self.processor.make_data()

        self.ToolTab = UIToolTab(self.processor, self.data, self)
        self.setWindowTitle("Говорящая голова звук")
        self.setCentralWidget(self.ToolTab)
        self.ToolTab.btn1.clicked.connect(self.startUIWindow)
        self.show()

    def startUIWindow(self):
        self.Window = UIWindow(self.processor, self.data, self)
        self.setWindowTitle("Говорящая голова картинка")
        self.setCentralWidget(self.Window)
        self.Window.ToolsBTN.clicked.connect(self.startVideo)
        self.show()

    def startVideo(self):
        self.Player = MediaPlayer(self.processor, self.data, self)
        self.setWindowTitle("Говорящая голова видео")
        self.setCentralWidget(self.Player)
        self.Player.nextbutton.clicked.connect(self.endUIWindow)
        self.show()

    def endUIWindow(self):
        self.EndWindow = UIEndWindow(self.processor, self.data, self)
        self.setWindowTitle("Сохранение файла")
        self.setCentralWidget(self.EndWindow)
        self.EndWindow.button.clicked.connect(self.startUIToolTab)
        self.EndWindow.button2.clicked.connect(self.startUIToolTab)
        self.show()
