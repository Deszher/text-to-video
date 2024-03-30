from PyQt6.QtWidgets import (
    QPlainTextEdit,
    QWidget,
    QPushButton,
    QComboBox,
    QLabel,
)

from domain.model import ProcessData
from domain.processor import Processor


class UIToolTab(QWidget):
    processor: Processor
    data: ProcessData

    def __init__(self, processor: Processor, data: ProcessData, parent=None):
        super(UIToolTab, self).__init__(parent)
        self.processor = processor
        self.data = data

        x = self.window().width()
        y = self.window().height()
        self.label_1 = QLabel(self)
        self.label_1.move(int(x - x / 1.175), 10)
        self.label_1.setText("Подготовим речь для головы")
        self.label_1.setStyleSheet(
            # Границы, цвет
            "font-size: 20px;"
            # 'font-weight: bold;'
        )
        self.textbox = QPlainTextEdit(self)

        self.combo = QComboBox(self)
        self.label_2 = QLabel(self)
        self.label_2.move(325, 220)
        self.label_2.setText("Выберите голос говорящего:")
        for i in range(101):
            self.combo.addItem(f"en_{i}")

        self.combo.move(490, 220)
        self.textbox.setGeometry(
            int(x - x / 1.175), int(y - y / 1.1), int(x - x / 3.5), int(y - y / 1.45)
        )
        self.textbox.setPlaceholderText(
            "Введите текст, который хотите добавить к говорящей голове..."
        )

        self.btn1 = QPushButton("Готово", self)
        self.btn1.setGeometry(
            int(x - x / 1.175), int(y - y / 2.5), int(x - x / 3.5), int(y - y / 1.1)
        )
        self.btn1.setStyleSheet(
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
        text = self.textbox.toPlainText()
        if text.strip():  # Проверка на наличие символов
            print("Текст введен:", text)
        else:
            print("Пожалуйста, введите текст.")
        self.btn1.setCheckable(True)
        self.btn1.clicked.connect(self.get)

    def get(self):
        selected_speaker = self.combo.currentText()
        text = self.textbox.toPlainText()

        self.processor.set_text_and_speaker(self.data, text, selected_speaker)
        self.processor.make_speech(self.data)
