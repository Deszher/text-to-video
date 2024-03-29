import os

from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QSpinBox,
    QFileDialog,
    QLabel,
)

from domain.model import ProcessData
from domain.processor import Processor


class UIWindow(QWidget):
    processor: Processor
    data: ProcessData

    def __init__(self, processor: Processor, data: ProcessData, parent=None):
        super(UIWindow, self).__init__(parent)
        self.processor = processor
        self.data = data
        x = self.window().width()
        y = self.window().height()
        self.label = QLabel(self)
        self.label.move(int(x - x / 1.175), 30)
        self.label.setText(
            "Введите размер стороны исходной картинки в виде целого числа,"
            " картинка будет квадратной формы\n по умолчанию = 450 px"
        )
        self.numtbox = QSpinBox(self)
        self.numtbox.setGeometry(
            int(x - x / 1.175), int(y - y / 1.2), int(x - x / 1.5), int(y - y / 1.1)
        )

        self.numtbox.setRange(100, 700)
        self.numtbox.setValue(450)
        self.numtbox.setSuffix(" px")

        self.ToolsBTN = QPushButton("Загрузить изображение", self)

        # self.ToolsBTN.move(50, 350)
        self.ToolsBTN.setGeometry(
            int(x - x / 1.175), int(y - y / 2.5), int(x - x / 3.5), int(y - y / 1.1)
        )
        self.ToolsBTN.setStyleSheet(
            # Границы, цвет
            "margin: 0;"
            "padding: 0;"
            "width: 100 %;"
            "height: 100 vh;"
            "display: flex;"
            "flex - direction: row;"
            "justify - content: center;"
            "align - items: center;"
            "background:  # 000;"
            "border-color: blue;"
            "border-width: 5px;"
            "border-style: ridge;"
            "border-radius: 5;"
            "font-size: 60px;"
            "font-weight: bold;"
        )
        self.ToolsBTN.setCheckable(True)
        self.ToolsBTN.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        desktop = os.path.join(os.path.join(os.path.expanduser("~")), "Desktop")
        filename, ok = QFileDialog.getOpenFileName(
            self, "Select a File", f"{desktop}", "Images (*.png *.jpg *.jpeg)"
        )
        if filename:
            self.processor.add_image(self.data, filename)
