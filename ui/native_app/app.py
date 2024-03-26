from PyQt6.QtWidgets import QApplication
from ui.native_app.main_window import MainWindow
from domain.processor import Processor


def run():
    app = QApplication([])
    window = MainWindow(Processor(), None)
    window.show()

    app.exec()
