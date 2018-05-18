import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel
from plot_canvas import PlotCanvas
import matplotlib.pyplot as plt
import time

topk_canvas = True
if 1:
    class App(QMainWindow):

        def __init__(self):
            super().__init__()
            self.title = '星巴克门店分布'
            self.left = 100
            self.top = 100
            self.width = 1500
            self.height = 900

            self.initUI()

        def initUI(self):
            self.setWindowTitle(self.title)
            self.setGeometry(self.left, self.top, self.width, self.height)

            #self.m = PlotCanvas(self, width=8, height=6)
            self.m = PlotCanvas(self, width=12, height=9)
            self.m.move(300, 0)

            if topk_canvas:
                self.lbl_lon = QLabel('Lon:', self)
                self.lbl_lon.move(50, 150)

                self.line_lon = QLineEdit(self)
                self.line_lon.setFixedWidth(160)
                self.line_lon.move(100, 150)
                self.line_lon.textChanged.connect(self.text_changed)

                self.warn_lon = QLabel('输入区间为[-180,180]', self)
                self.warn_lon.setFixedWidth(200)
                self.warn_lon.move(100, 180)
                self.warn_lon.hide()

                self.lbl_lat = QLabel('Lat:', self)
                self.lbl_lat.move(50, 250)

                self.line_lat = QLineEdit(self)
                self.line_lat.setFixedWidth(160)
                self.line_lat.move(100, 250)
                self.line_lat.textChanged.connect(self.text_changed)

                self.warn_lat = QLabel('输入区间为[-90,90]', self)
                self.warn_lat.setFixedWidth(200)
                self.warn_lat.move(100, 280)
                self.warn_lat.hide()

                self.lbl_k = QLabel('  K:', self)
                self.lbl_k.move(50, 350)

                self.line_k = QLineEdit(self)
                self.line_k.setFixedWidth(160)
                self.line_k.move(100, 350)
                self.line_k.textChanged.connect(self.text_changed)

                self.warn_k = QLabel('输入区间为[1,25600]', self)
                self.warn_k.setFixedWidth(200)
                self.warn_k.move(100, 380)
                self.warn_k.hide()

                self.button_check = QPushButton('查询', self)
                self.button_check.move(40, 450)
                self.button_check.clicked.connect(self.button_check_on_click)

                self.button_k = QPushButton('展示', self)
                self.button_k.move(160, 450)
                self.button_k.clicked.connect(self.button_k_on_click)

                self.lbl_delay = QLabel('此次查询时延为',self)
                self.lbl_delay.setFixedWidth(220)
                self.lbl_delay.move(40, 500)
                self.lbl_delay.hide()
            self.show()

        @pyqtSlot()
        def text_changed(self):
            self.warn_lon.hide()
            self.warn_lat.hide()
            self.warn_k.hide()
            self.lbl_delay.hide()

        @pyqtSlot()
        def button_check_on_click(self):
            lon = float(self.line_lon.text())
            lat = float(self.line_lat.text())
            k = int(self.line_k.text())
            if lon >= -180 and lon <= 180 and lat >= -90 and lat <= 90 and k >= 1 and k <= 25600:
                start = time.clock()
                if not self.m.get_point() == None:
                    self.m.get_point().set_visible(False)
                self.m.show_top_k(lon, lat, k)
                self.m.get_point().set_visible(True)
                self.m.refresh()
                end = time.clock()
                delay = round(end - start, 3)
                self.lbl_delay.setText('此次查询时延为' + str(delay) + '秒')
                self.lbl_delay.show()
            else:
                if lon < -180 or lon > 180:
                    self.warn_lon.show()
                if lat < -90 or lat > 90:
                    self.warn_lat.show()
                if k < 1 or k > 25600:
                    self.warn_k.show()



        @pyqtSlot()
        def button_k_on_click(self):

            x = []
            y = []

            lon = float(self.line_lon.text())
            lat = float(self.line_lat.text())

            i = 1250
            while i <= 25600:
                k = i
                if lon >= -180 and lon <= 180 and lat >= -90 and lat <= 90 and k >= 1 and k <= 25600:
                    start = time.clock()
                    if not self.m.get_point() == None:
                        self.m.get_point().set_visible(False)
                    self.m.show_top_k(lon, lat, k)
                    # self.m.refresh()
                    end = time.clock()
                    delay = round(end - start, 3)
                    x.append(k)
                    y.append(delay)
                else:
                    if lon < -180 or lon > 180:
                        self.warn_lon.show()
                    if lat < -90 or lat > 90:
                        self.warn_lat.show()
                    if k < 1 or k > 25600:
                        self.warn_k.show()
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


