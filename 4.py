import sys

from PIL import Image, ImageQt
from io import BytesIO
import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, \
    QPushButton
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 550]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("Отображение карты")
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.ll_text = QtWidgets.QLabel(self)
        self.ll_text.setText('Введите координаты:')
        self.ll_text.move(10, 460)
        self.ll_text.resize(110, 20)
        self.ll_text.setGeometry(QtCore.QRect(10, 460, 110, 20))
        self.ll_text = QtWidgets.QLabel(self)
        self.ll_text.setText('Введите координаты:')
        self.ll_text.setGeometry(QtCore.QRect(10, 460, 110, 20))
        self.ll_edit = QtWidgets.QLineEdit(self)
        self.ll_edit.move(130, 460)
        self.ll_edit.resize(100, 20)
        self.spn_text = QtWidgets.QLabel(self)
        self.spn_text.setText('Введите масштаб:')
        self.spn_text.move(10, 490)
        self.spn_text.resize(110, 20)
        self.spn_edit = QtWidgets.QLineEdit(self)
        self.spn_edit.move(130, 490)
        self.spn_edit.resize(100, 20)
        self.start_show = QtWidgets.QPushButton(self)
        self.start_show.setText('Показать карту')
        self.start_show.move(260, 510)
        self.start_show.resize(120, 30)
        self.start_show.clicked.connect(self.start)
        self.image = QtWidgets.QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.map_text = QtWidgets.QLabel(self)
        self.map_text.setText('Введите слой карты:')
        self.map_text.move(210, 460)
        self.map_text.resize(110, 20)
        self.map_text.setGeometry(QtCore.QRect(10, 460, 110, 20))
        self.map_text = QtWidgets.QLabel(self)
        self.map_text.setText('Введите координаты:')
        self.map_text.setGeometry(QtCore.QRect(210, 460, 110, 20))
        self.map_edit = QtWidgets.QLineEdit(self)
        self.map_edit.move(330, 460)
        self.map_edit.resize(100, 20)


    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.lon}," \
                      f"{self.lat}8&spn={str(self.spn)},{str(self.spn)}&l={self.map_type}"
        try:
            response = requests.get(map_request)
            self.img = Image.open(BytesIO(response.content))
            self.update_image()
        except Exception:
            print('недопустимое значение масштаба')


    def update_image(self):
        self.image.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.img)))


    def keyPressEvent(self, event):
        print('sddsdsdsa')
        if event.key() == Qt.Key_PageUp:
            self.spn += 0.001
            self.getImage()
        elif event.key() == Qt.Key_PageDown:
            self.spn -= 0.001
            self.getImage()
        elif event.key() == Qt.Key_W:
            self.lat += 0.001
            self.getImage()
        elif event.key() == Qt.Key_S:
            self.lat -= 0.001
            self.getImage()
        elif event.key() == Qt.Key_D:
            self.lon += 0.001
            self.getImage()
        elif event.key() == Qt.Key_A:
            self.lon -= 0.001
            self.getImage()
        # сделали на кнопки WASD, потому что по нажатию на стрелочки функция
        # не срабатывает, а передвигается курсор в line_edit


    def start(self):
        try:
            self.lon, self.lat = map(float, self.ll_edit.text().split(', '))
            self.spn = float(self.spn_edit.text())
            self.map_type = self.map_text.text()
            self.getImage()
            self.update_image()
        except Exception:
            print('Недопустимое значение параметров')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
