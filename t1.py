import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtMultimedia import *
from PyQt5.QtCore import *
from UI import Ui_MainWindow
import requests


class MyApplication(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.scale = 0.3
        self.x_coords = 37.622504
        self.y_coords = 55.753215
        self.point_x = 37.622504
        self.point_y = 55.753215
        self.map_type = 'map'
        self.maps_api_server = "https://static-maps.yandex.ru/1.x/"
        self.coder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        self.ispoint = False
        self.painter = QPainter()

        self.pushButton_Back.clicked.connect(self.back)
        self.pushButton_Minus.clicked.connect(self.minus)
        self.pushButton_Plus.clicked.connect(self.plus)
        self.pushButton_Search.clicked.connect(self.search)
        self.pushButton_Change.clicked.connect(self.change)
        self.update()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_PageUp:
            self.plus()
        elif e.key() == Qt.Key_PageDown:
            self.minus()
        elif e.key() == Qt.Key_Up or e.key() == Qt.Key_W:
            self.up()
        elif e.key() == Qt.Key_Down or e.key() == Qt.Key_S:
            self.down()
        elif e.key() == Qt.Key_Right or e.key() == Qt.Key_D:
            self.right()
        elif e.key() == Qt.Key_Left or e.key() == Qt.Key_A:
            self.left()
        elif e.key() == Qt.Key_Enter:
            self.search()
        elif e.key() == Qt.Key_Backspace:
            self.back()

    def update(self):
        if self.ispoint:
            maps_params = {
                "ll": ','.join([str(self.x_coords), str(self.y_coords)]),
                "l": self.map_type,
                "spn": ','.join([str(self.scale), str(self.scale)]),
                "size": '650,450',
                "pt": '{},{},pm2dgm'.format(str(self.point_x), str(self.point_y))
            }
        else:
            maps_params = {
                "ll": ','.join([str(self.x_coords), str(self.y_coords)]),
                "l": self.map_type,
                "spn": ','.join([str(self.scale), str(self.scale)]),
                "size": '650,450'
            }
        maps_response = requests.get(self.maps_api_server, params=maps_params)
        if self.map_type != 'map':
            map_file = "map.jpg"
        else:
            map_file = 'map.png'
        try:
            with open(map_file, "wb") as file:
                file.write(maps_response.content)
        except IOError as ex:
            print("Ошибка записи временного файла:", ex)
            sys.exit(2)
        self.pixmap = QPixmap(map_file)
        self.label.setPixmap(self.pixmap)
        print('update', self.pixmap.isNull())

    def minus(self):
        max_scale = 50
        new_scale = self.scale * 1.2
        if new_scale >= max_scale:
            self.scale = max_scale
        else:
            self.scale = new_scale
        self.update()

    def plus(self):
        min_scale = 0.005
        new_scale = self.scale * 0.8
        if new_scale <= min_scale:
            self.scale = min_scale
        else:
            self.scale = new_scale
        self.update()

    def right(self):
        self.x_coords = float(self.x_coords) + self.scale * 0.3
        self.update()

    def left(self):
        self.x_coords = float(self.x_coords) - self.scale * 0.3
        self.update()

    def up(self):
        self.y_coords = float(self.y_coords) + self.scale * 0.3
        self.update()

    def down(self):
        self.y_coords = float(self.y_coords) - self.scale*0.3
        self.update()

    def change(self):
        map_types = ['map', 'sat', 'sat,skl']
        try:
            self.map_type = map_types[map_types.index(self.map_type) + 1]
        except IndexError:
            self.map_type = 'map'
        self.update()

    def search(self):
        self.ispoint = True
        text = self.lineEditSearch.text()
        coder_params = {
            "geocode": text,
            "format": 'json'
        }
        coder_response = requests.get(self.coder_api_server, params=coder_params)
        json_response = coder_response.json()
        coords = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]['Point']['pos'].split()
        print(coords)
        x, y = coords[0], coords[1]
        self.point_x = x
        self.point_y = y
        self.x_coords = x
        self.y_coords = y
        self.update()

        print(x)

    def back(self):
        self.ispoint = False
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = MyApplication()
    application.show()
    sys.exit(app.exec_())
