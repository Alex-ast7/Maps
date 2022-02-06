import os
import sys

import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, \
    QPushButton
from PyQt5.QtCore import Qt

SCREEN_SIZE = [600, 550]
API_KEY = '40d1649f-0493-4b70-98ba-98533de7710b'


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
        self.map_text.move(310, 460)
        self.map_text.resize(110, 20)
        self.map_text.setGeometry(QtCore.QRect(310, 460, 110, 20))
        self.map_edit = QtWidgets.QLineEdit(self)
        self.map_edit.move(430, 460)
        self.map_edit.resize(100, 20)
        self.address_text = QtWidgets.QLabel(self)
        self.address_text.setText('Введите адресс:')
        self.address_text.move(310, 490)
        self.address_text.resize(110, 20)
        self.address_edit = QtWidgets.QLineEdit(self)
        self.address_edit.move(430, 490)
        self.address_edit.resize(100, 20)

    def getImage(self):
        if self.address_edit.text():
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.lon}," \
                          f"{self.lat}8&spn={str(self.spn)},{str(self.spn)}&l=" \
                          f"{self.map_type}&pt={self.lon},{self.lat},pmwtm1"
        else:
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.lon}," \
                          f"{self.lat}8&spn={str(self.spn)},{str(self.spn)}&l=" \
                          f"{self.map_type}"
        print(map_request)
        try:
            response = requests.get(map_request)
            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)
            self.update_image()
        except Exception:
            print('недопустимое значение масштаба')

    def update_image(self):
        try:
            self.pixmap = QPixmap(self.map_file)
            self.image.setPixmap(self.pixmap)
        except Exception as e:
            print(e)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn += 0.001
            self.spn_edit.setText(str(self.spn))
            self.getImage()
        elif event.key() == Qt.Key_PageDown:
            self.spn -= 0.001
            self.spn_edit.setText(str(self.spn))
            self.getImage()
        elif event.key() == Qt.Key_W:
            self.lat += 0.001
            self.ll_edit.setText(f"{self.lon}, {self.lat}")
            self.getImage()
        elif event.key() == Qt.Key_S:
            self.lat -= 0.001
            self.ll_edit.setText(f"{self.lon}, {self.lat}")
            self.getImage()
        elif event.key() == Qt.Key_D:
            self.lon += 0.001
            self.ll_edit.setText(f"{self.lon}, {self.lat}")
            self.getImage()
        elif event.key() == Qt.Key_A:
            self.lon -= 0.001
            self.ll_edit.setText(f"{self.lon}, {self.lat}")
            self.getImage()
        # сделали на кнопки WASD, потому что по нажатию на стрелочки функция
        # не срабатывает, а передвигается курсор в line_edit

    def start(self):
        try:
            if self.address_edit.text():
                self.spn = float(self.spn_edit.text())
                self.address = self.address_edit.text()
                self.lon, self.lat = self.get_coordinates()
                self.map_type = self.map_edit.text()
            else:
                self.lon, self.lat = map(float, self.ll_edit.text().split(', '
                                                                          ''))
                self.spn = float(self.spn_edit.text())
                self.map_type = self.map_edit.text()
            self.getImage()
            self.update_image()
            self.ll_edit.setEnabled(False)
            self.spn_edit.setEnabled(False)
        except Exception as e:
            print(e)

    def closeEvent(self, event):
        os.remove(self.map_file)

    def get_coordinates(self):
        toponym = self.geocode()
        if not toponym:
            return None, None

        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]
        # Широта, преобразованная в плавающее число:
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        return float(toponym_longitude), float(toponym_lattitude)

    def geocode(self):
        # Собираем запрос для геокодера.
        print(self.address)
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}" \
                           f"&geocode={self.address}&format=json"

        # Выполняем запрос.
        response = requests.get(geocoder_request)

        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()
        else:
            raise RuntimeError(
                """Ошибка выполнения запроса:
                {request}
                Http статус: {status} ({reason})""".format(
                    request=geocoder_request, status=response.status_code,
                    reason=response.reason))

        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа он находится по следующему пути:
        features = json_response["response"]["GeoObjectCollection"][
            "featureMember"]
        return features[0]["GeoObject"] if features else None


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = Example()
        ex.show()
        sys.exit(app.exec())
    except Exception as e:
        print(e)
