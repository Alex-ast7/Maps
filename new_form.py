import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self, x, y):
        super().__init__()
        self.resize(400, 50)
        self.move(x - 200, y + 30)
        self.address_text = QtWidgets.QLabel(self)
        self.address_text.setText('Введите адресс или название объекта:')
        self.address_text.move(10, 10)
        self.address_text.resize(270, 20)
        self.address_edit = QtWidgets.QLineEdit(self)
        self.address_edit.move(285, 10)
        self.address_edit.resize(100, 20)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
