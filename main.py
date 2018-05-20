import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QGridLayout
import matplotlib.pyplot as plt
import time

from plot_canvas import PlotCanvas
from input_wid import InputWid

topk_canvas = True


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = '星巴克门店分布'
        self.left = 100
        self.top = 100
        self.width = 1000
        self.height = 600

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.m = PlotCanvas(self, width=8, height=6)
        self.m.move(200, 0)

        if topk_canvas:
            self.input_lon = InputWid(self, 'Lon:', '输入区间为[-180,180]')
            self.input_lon.set_location(0, 50)
            self.input_lon.connect(self.text_changed)

            self.input_lat = InputWid(self, 'Lat', '输入区间为[-90,90]')
            self.input_lat.set_location(0, 120)
            self.input_lat.connect(self.text_changed)

            self.input_k = InputWid(self, 'K:', '输入区间为[1,25600]')
            self.input_k.set_location(0, 190)
            self.input_k.connect(self.text_changed)

            self.input_word = InputWid(self, '关键字:')
            self.input_word.set_location(0, 260)
            self.input_word.connect(self.text_changed)

            self.input_radius = InputWid(self, 'Range:')
            self.input_radius.set_location(0, 330)
            self.input_radius.connect(self.text_changed)

            self.button_check = QPushButton('top-k', self)
            self.button_check.move(20, 420)
            self.button_check.setFixedWidth(70)
            self.button_check.clicked.connect(self.button_check_on_click)

            # self.button_k = QPushButton('展示', self)
            # self.button_k.move(110, 420)
            # self.button_k.setFixedWidth(70)
            # self.button_k.clicked.connect(self.button_k_on_click)

            self.button_radius = QPushButton('Range', self)
            self.button_radius.move(110, 420)
            self.button_radius.setFixedWidth(70)
            self.button_radius.clicked.connect(self.button_radius_on_click)

            self.lbl_delay = QLabel('此次查询时延为', self)
            self.lbl_delay.setFixedWidth(140)
            self.lbl_delay.move(20, 460)
            self.lbl_delay.hide()

        self.show()

    @pyqtSlot()
    def text_changed(self):
        self.input_lon.hide_warning()
        self.input_lat.hide_warning()
        self.input_k.hide_warning()
        self.lbl_delay.hide()

    @pyqtSlot()
    def button_check_on_click(self):
        lon = float(self.input_lon.text())
        lat = float(self.input_lat.text())
        k = int(self.input_k.text())
        word = self.input_word.text()
        if lon >= -180 and lon <= 180 and lat >= -90 and lat <= 90 and k >= 1 and k <= 25600:
            start = time.clock()
            if self.m.get_point() is not None:
                self.m.get_point().set_visible(False)
            self.m.show_top_k(lon, lat, k, word)
            self.m.get_point().set_visible(True)
            self.m.refresh()
            end = time.clock()
            delay = round(end - start, 3)
            self.lbl_delay.setText('此次查询时延为' + str(delay) + '秒')
            self.lbl_delay.show()
        else:
            if lon < -180 or lon > 180:
                self.input_lon.show_warning()
            if lat < -90 or lat > 90:
                self.input_lat.show_warning()
            if k < 1 or k > 25600:
                self.input_k.show_warning()

    @pyqtSlot()
    def button_radius_on_click(self):
        lon = float(self.input_lon.text())
        lat = float(self.input_lat.text())
        radius = int(self.input_radius.text())
        if lon >= -180 and lon <= 180 and lat >= -90 and lat <= 90:
            start = time.clock()
            if self.m.get_point() is not None:
                self.m.get_point().set_visible(False)
            self.m.show_radius(lon, lat, radius)
            self.m.get_point().set_visible(True)
            self.m.refresh()
            end = time.clock()
            delay = round(end - start, 3)
            self.lbl_delay.setText('此次查询时延为' + str(delay) + '秒')
            self.lbl_delay.show()

    @pyqtSlot()
    def button_radius_delay_on_click(self):
        x = []
        y = []

        lon = float(self.input_lon.text())
        lat = float(self.input_lat.text())

        radius = 1000
        while radius <= 20000:
            if lon >= -180 and lon <= 180 and lat >= -90 and lat <= 90:
                start = time.clock()
                if self.m.get_point() is not None:
                    self.m.get_point().set_visible(False)
                self.m.show_radius(lon, lat, radius)
                # self.m.refresh()
                end = time.clock()
                delay = round(end - start, 3)
                x.append(radius)
                y.append(delay)
                radius += 1000

        plt.figure('range-时延变化图')
        plt.scatter(x, y, color='k', s=25, marker="o")

        plt.xlabel('range/千米')
        plt.ylabel('时延/秒')
        plt.title('Lon: ' + self.input_lon.text() + '    Lat: ' + self.input_lat.text())
        plt.legend()
        plt.show()

    @pyqtSlot()
    def button_k_on_click(self):
        x = []
        y = []

        lon = float(self.input_lon.text())
        lat = float(self.input_lat.text())

        i = 1250
        while i <= 25600:
            k = i
            if lon >= -180 and lon <= 180 and lat >= -90 and lat <= 90 and k >= 1 and k <= 25600:
                start = time.clock()
                if self.m.get_point() is not None:
                    self.m.get_point().set_visible(False)
                self.m.show_top_k(lon, lat, k, '')
                # self.m.refresh()
                end = time.clock()
                delay = round(end - start, 3)
                x.append(k)
                y.append(delay)
            else:
                if lon < -180 or lon > 180:
                    self.input_lon.show_warning()
                if lat < -90 or lat > 90:
                    self.input_lat.show_warning()
                if k < 1 or k > 25600:
                    self.input_k.show_warning()

            i += 1250

        plt.scatter(x, y, color='k', s=25, marker="o")

        plt.xlabel('k/数量')
        plt.ylabel('时延/秒')
        plt.title('k-时延变化图')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())



