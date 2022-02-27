import os
import sys
import math
import requests
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, \
    QPushButton, QInputDialog
from PyQt5.QtCore import Qt
from new_form import MyWidget

SCREEN_SIZE = [600, 600]
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
        self.start_show.move(0, 510)
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
        self.address_text.setText('Введите адресс или название объекта:')
        self.address_text.move(250, 490)
        self.address_text.resize(200, 20)
        self.address_edit = QtWidgets.QLineEdit(self)
        self.address_edit.move(460, 490)
        self.address_edit.resize(100, 20)
        self.restart_btn = QtWidgets.QPushButton(self)
        self.restart_btn.move(130, 510)
        self.restart_btn.resize(160, 30)
        self.restart_btn.setText('Сброс поискового результата')
        self.restart_btn.clicked.connect(self.restart)
        self.label_adress = QtWidgets.QLabel(self)
        self.label_adress.move(300, 515)
        self.label_adress.resize(145, 20)
        self.label_adress.setText('Адрес найденного объекта:')
        self.label_adress_edit = QtWidgets.QLineEdit(self)
        self.label_adress_edit.move(445, 515)
        self.label_adress_edit.resize(130, 20)
        self.label_adress_edit.setEnabled(False)
        self.show_index = QtWidgets.QCheckBox(self)
        self.show_index.move(470, 540)
        self.show_index.resize(20, 20)
        self.show_index_label = QtWidgets.QLabel(self)
        self.show_index_label.move(300, 540)
        self.show_index_label.resize(160, 20)
        self.show_index_label.setText('Показывать почтовый индекс')
        self.show_index.stateChanged.connect(self.change_value)

    def getImage(self):
        if self.address_edit.text():
            map_request = f"http://static-maps.yandex.ru/1.x/?ll={self.lon}," \
                          f"{self.lat}8&spn={str(self.spn)},{str(self.spn)}&l=" \
                          f"{self.map_type}&pt={self.lon_point},{self.lat_point},pmwtm1"
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

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.object, ok_pressed = QInputDialog.getText(self, "Поиск объекта",
                                                    "Введите адресс или название объекта:")
            if ok_pressed:
                self.address = self.object
                x, y = self.get_coordinates()
                self.lonlat_distance((x, y), (self.lon, self.lat))
                distance = self.lonlat_distance((x, y), (self.lon, self.lat))
                if distance <= 50:
                    self.address_edit.setText(self.object)
                    self.start()
        if event.button() == Qt.LeftButton:
            self.object, ok_pressed = QInputDialog.getText(self, "Поиск объекта",
                                                              "Введите адресс или название объекта:")
            if ok_pressed:
                self.address_edit.setText(self.object)
                self.start()

        # сделали на кнопки WASD, потому что по нажатию на стрелочки функция
        # не срабатывает, а передвигается курсор в line_edit
    def start(self):
        try:
            if self.address_edit.text():
                self.spn = float(self.spn_edit.text())
                self.address = self.address_edit.text()
                self.lon, self.lat = self.get_coordinates()
                self.label_adress_edit.setText(self.toponym_address)
                self.lon_point = self.lon
                self.lat_point = self.lat
                self.map_type = self.map_edit.text()
                self.ll_edit.setText(f"{self.lon}, {self.lat}")


            else:
                self.lon, self.lat = map(float, self.ll_edit.text().split(', '
                                                                          ''))
                self.spn = float(self.spn_edit.text())
                self.map_type = self.map_edit.text()
            self.getImage()
            self.update_image()
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
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey={API_KEY}" \
                           f"&geocode={self.address}&format=json"

        # Выполняем запрос.
        response = requests.get(geocoder_request)

        if response:
            # Преобразуем ответ в json-объект
            json_response = response.json()
            toponym = \
                json_response["response"]["GeoObjectCollection"][
                    "featureMember"][0][
                    "GeoObject"]
            self.toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"][
                "text"]
            self.toponym_index = toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
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

    def restart(self):
        self.address_edit.clear()
        self.label_adress_edit.clear()
        self.getImage()
        self.update_image()

    def change_value(self):
        if self.show_index.isChecked():
            self.label_adress_edit.setText(f"{self.toponym_address}, {self.toponym_index}")
        else:
            self.label_adress_edit.setText(self.toponym_address)

    def lonlat_distance(self, a, b):
        degree_to_meters_factor = 111 * 1000
        a_lon, a_lat = a
        b_lon, b_lat = b
        radians_lattitude = math.radians((a_lat + b_lat) / 2.)
        lat_lon_factor = math.cos(radians_lattitude)
        dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
        dy = abs(a_lat - b_lat) * degree_to_meters_factor
        distance = math.sqrt(dx * dx + dy * dy)
        return distance

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = Example()
        ex.show()
        sys.exit(app.exec())
    except Exception as e:
        print(e)
