import os
import shutil
from pathlib import Path

from PyQt6.QtWidgets import QMainWindow, QPlainTextEdit, QWidget, QPushButton, \
    QComboBox, QSpinBox, QApplication, QFileDialog, QLabel, QHBoxLayout

from audio_player import MediaPlayer
from speech_synt import get_speech


class UIWindow(QWidget):
    def __init__(self, parent=None):
        super(UIWindow, self).__init__(parent)
        x = self.window().width()
        y = self.window().height()
        self.label = QLabel(self)
        self.label.move(int(x - x / 1.175), 30)
        self.label.setText("Введите размер стороны исходной картинки в виде целого числа,"
                           " картинка будет квадратной формы\n по умолчанию = 450 px")
        self.numtbox = QSpinBox(self)
        self.numtbox.setGeometry(int(x - x / 1.175), int(y - y / 1.2),
                                 int(x - x / 1.5), int(y - y / 1.1))

        self.numtbox.setRange(100, 700)
        self.numtbox.setValue(450)
        self.numtbox.setSuffix(" px")

        self.ToolsBTN = QPushButton('Загрузить изображение', self)

        # self.ToolsBTN.move(50, 350)
        self.ToolsBTN.setGeometry(int(x - x / 1.175), int(y - y / 2.5), int(x - x / 3.5), int(y - y / 1.1))
        self.ToolsBTN.setStyleSheet(
            # Границы, цвет
            'margin: 0;'
            'padding: 0;'
            'width: 100 %;'
            'height: 100 vh;'
            'display: flex;'
            'flex - direction: row;'
            'justify - content: center;'
            'align - items: center;'
            'background:  # 000;'
            'border-color: blue;'
            'border-width: 5px;'
            'border-style: ridge;'
            'border-radius: 5;'
            'font-size: 60px;'
            'font-weight: bold;'
        )
        self.ToolsBTN.setCheckable(True)
        self.ToolsBTN.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
        filename, ok = QFileDialog.getOpenFileName(
            self,
            "Select a File",
            f"{desktop}",
            "Images (*.png *.jpg *.jpeg)"
        )
        if filename:
            path = Path(filename)
            current_dir = os.getcwd()
            new_filename = "1"
            target_dir = os.path.join(current_dir, new_filename + path.suffix)

            shutil.copyfile(path, target_dir)
            print("Картинка успешно сохранена как", new_filename)


class UIToolTab(QWidget):
    def __init__(self, parent=None):
        super(UIToolTab, self).__init__(parent)
        x = self.window().width()
        y = self.window().height()
        self.label_1 = QLabel(self)
        self.label_1.move(int(x - x / 1.175), 10)
        self.label_1.setText("Подготовим речь для головы")
        self.label_1.setStyleSheet(
            # Границы, цвет
            'font-size: 20px;'
            # 'font-weight: bold;'
        )
        self.textbox = QPlainTextEdit(self)

        self.combo = QComboBox(self)
        self.label_2 = QLabel(self)
        self.label_2.move(325, 220)
        self.label_2.setText("Выберите голос говорящего:")
        for i in range(101):
            self.combo.addItem(f'en_{i}')

        self.combo.move(490, 220)
        self.textbox.setGeometry(int(x - x / 1.175), int(y - y / 1.1),
                                 int(x - x / 3.5), int(y - y / 1.45))
        self.textbox.setPlaceholderText("Введите текст, который хотите добавить к говорящей голове...")

        self.btn1 = QPushButton("Готово", self)
        self.btn1.setGeometry(int(x - x / 1.175), int(y - y / 2.5), int(x - x / 3.5), int(y - y / 1.1))
        self.btn1.setStyleSheet(
            # Границы, цвет
            'margin: 0;'
            'padding: 0;'
            'width: 100 %;'
            'height: 100 vh;'
            'display: flex;'
            'flex - direction: row;'
            'justify - content: center;'
            'align - items: center;'
            'background:  # 000;'
            'border-color: blue;'
            'border-width: 5px;'
            'border-style: ridge;'
            'border-radius: 5;'

            'font-size: 60px;'
            'font-weight: bold;'
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
        print(text, selected_speaker)
        if text == "":
            text = "can't say anything, you forgot to write down the text"
        get_speech(text, selected_speaker)


class UIEndWindow(QWidget):
    def __init__(self, parent=None):
        super(UIEndWindow, self).__init__(parent)
        x = self.window().width()
        y = self.window().height()

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
        save_dir = QFileDialog.getExistingDirectory(None, "Выберите директорию для сохранения")

        # Проверяем, что пользователь выбрал директорию
        if save_dir:
            # Путь к файлу и его название
            source_file_path = r"test.wav"

            # Путь и название сохраняемого файла
            save_path = os.path.join(save_dir, "test.wav")

            # Код для сохранения файла
            shutil.copyfile(source_file_path, save_path)
            self.lbl = QLabel(f"Файл успешно сохранен по пути: {save_path}", self)

            print(f"Файл успешно сохранен по пути: {save_path}")

        else:
            print("Отменено пользователем")


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setGeometry(50, 50, 400, 450)
        self.x, self.y = 700, 500
        self.setFixedSize(self.x, self.y)
        self.setWindowTitle("Говорящая голова")
        self.startUIToolTab()

    def startUIToolTab(self):
        self.ToolTab = UIToolTab(self)
        self.setWindowTitle("Говорящая голова звук")
        self.setCentralWidget(self.ToolTab)
        self.ToolTab.btn1.clicked.connect(self.startUIWindow)
        self.show()

    def startUIWindow(self):
        self.Window = UIWindow(self)
        self.setWindowTitle("Говорящая голова картинка")
        self.setCentralWidget(self.Window)
        self.Window.ToolsBTN.clicked.connect(self.startVideo)
        self.show()

    def startVideo(self):
        self.Player = MediaPlayer(self)
        self.setWindowTitle("Говорящая голова видео")
        self.setCentralWidget(self.Player)
        self.Player.nextbutton.clicked.connect(self.endUIWindow)
        self.show()

    def endUIWindow(self):
        self.EndWindow = UIEndWindow(self)
        self.setWindowTitle("Сохранение файла")
        self.setCentralWidget(self.EndWindow)
        self.EndWindow.button.clicked.connect(self.startUIToolTab)
        self.EndWindow.button2.clicked.connect(self.startUIToolTab)
        self.show()


app = QApplication([])
window = MainWindow()
window.show()

app.exec()
