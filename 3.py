import sys

from PIL import Image, ImageQt
from io import BytesIO
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.lon, self.lat = map(float, input().split(', '))
        self.spn = float(input())

        self.initUI()
        self.getImage()

    def getImage(self):
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={str(self.lon)}," \
                      f"{str(self.lat)}8&spn={str(self.spn)},{str(self.spn)}&l=map"
        try:
            response = requests.get(map_request)
            self.img = Image.open(BytesIO(response.content))
            self.update_image()
        except Exception:
            print('недопустимое значение параметров')

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.image = QLabel(self)

    def update_image(self):
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(QPixmap.fromImage(ImageQt.ImageQt(self.img)))

    def keyPressEvent(self, event):
        try:
            if event.key() == Qt.Key_PageUp:
                self.spn += 0.001
            elif event.key() == Qt.Key_PageDown:
                self.spn -= 0.001
            elif event.key() == Qt.Key_Up:
                self.lat += 0.001
            elif event.key() == Qt.Key_Down:
                self.lat -= 0.001
            elif event.key() == Qt.Key_Right:
                self.lon += 0.001
            elif event.key() == Qt.Key_Left:
                self.lon -= 0.001
        except Exception as e:
            print(e)
        self.getImage()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
