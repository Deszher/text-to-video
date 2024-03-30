from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QFileDialog,
    QLabel,
    QHBoxLayout,
)

from domain.model import ProcessData
from domain.processor import Processor


class UIEndWindow(QWidget):
    processor: Processor
    data: ProcessData

    def __init__(self, processor: Processor, data: ProcessData, parent=None):
        super(UIEndWindow, self).__init__(parent)
        self.processor = processor
        self.data = data
        x = self.window().width()

        self.lbl = QLabel("", self)
        self.lbl.move(325, 220)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.button = QPushButton("Сохранить видео", self)
        # self.button.setFixedHeight(int(x - x / 0.2))
        self.button.setFixedWidth(int(x - x / 1.5))
        self.button.clicked.connect(self.save_file_dialog)

        self.button.clicked.connect(self.print_end)
        self.layout.addWidget(self.button)

        self.button2 = QPushButton("Создать новое видео", self)
        # self.button2.setFixedHeight(int(x - x / 0.5))
        self.button2.setFixedWidth(int(x - x / 1.5))

        self.button2.clicked.connect(self.print_end)
        self.layout.addWidget(self.button2)

    def print_end(self):
        print("end")

    def save_file_dialog(self):
        # Запросить директорию для сохранения файла
        save_dir = QFileDialog.getExistingDirectory(
            None, "Выберите директорию для сохранения"
        )

        # Проверяем, что пользователь выбрал директорию
        if save_dir:
            # Путь и название сохраняемого файла
            save_path = self.processor.save_to(self.data, save_dir)

            self.lbl = QLabel(f"Файл успешно сохранен по пути: {save_path}", self)

        else:
            print("Отменено пользователем")
