import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QAction
import matplotlib.pyplot as plt
import time

# 自定义的类
from plot_canvas import PlotCanvas, ViewOption
from input_wid import InputWid
import CustomStyle

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = '星巴克门店分布'
        self.left = 100
        self.top = 100
        self.width = 1000
        self.height = 625

        # 记录当前的视图
        self.view_option = ViewOption.DESTINY

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # 创建菜单栏
        self.menubar = self.menuBar()
        self.menubar.setStyleSheet(CustomStyle.menubar_style)  # 自定义样式
        # 添加菜单
        self.view_menu = self.menubar.addMenu('&视图')
        self.view_menu.setStyleSheet(CustomStyle.menu_style)  # 自定义样式

        # 子菜单
        destiny_view = QAction('&密度视图', self)
        destiny_view.triggered.connect(self.destiny_view_selected)  # 子菜单绑定的事件

        timezone_view = QAction('&时区视图', self)
        timezone_view.triggered.connect(self.timezone_view_selected)

        query_view = QAction("&查询视图", self)
        query_view.triggered.connect(self.query_view_selected)

        self.view_menu.addAction(destiny_view)
        self.view_menu.addAction(timezone_view)
        self.view_menu.addAction(query_view)

        # 以下是查询界面的控件，InpudWid为自定义的控件，包含了一个标题label，一个文本框，一个警告label
        self.input_lon = InputWid(self, 'Lon:', '输入区间为[-180,180]')
        self.input_lon.set_location(0, 50)
        self.input_lon.connect(self.text_changed)  # 绑定了文本改变的事件

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

        # top-k查询按钮
        self.button_check = QPushButton('top-k', self)
        self.button_check.move(20, 420)
        self.button_check.setFixedWidth(70)
        self.button_check.clicked.connect(self.top_k_query)

        # range查询按钮
        self.button_radius = QPushButton('Range', self)
        self.button_radius.move(110, 420)
        self.button_radius.setFixedWidth(70)
        self.button_radius.clicked.connect(self.radius_query)

        self.lbl_delay = QLabel('此次查询时延为', self)
        self.lbl_delay.setFixedWidth(140)
        self.lbl_delay.move(20, 460)
        self.lbl_delay.hide()
        # 以上是查询界面的控件

        # 地图列表，保存三种不同的视图，减少切换视图所需的时间
        self.map_list = []

        self.map_query = PlotCanvas(self, width=8, height=6, view_option=ViewOption.QUERY)
        self.map_query.move(200, 25)
        self.map_list.append(self.map_query)

        self.map_destiny = PlotCanvas(self, width=8, height=6, view_option=ViewOption.DESTINY)
        self.map_destiny.move(200, 25)
        self.map_list.append(self.map_destiny)

        self.map_timezone = PlotCanvas(self, width=8, height=6, view_option=ViewOption.TIMEZONE)
        self.map_timezone.move(200, 25)
        self.map_list.append(self.map_timezone)

        self.show_view()
        self.show()

    # 选中密度视图
    @pyqtSlot()
    def destiny_view_selected(self):
        if self.view_option == ViewOption.DESTINY:
            return
        self.view_option = ViewOption.DESTINY
        self.show_view()
        self.show()

    # 选中时区视图
    @pyqtSlot()
    def timezone_view_selected(self):
        if self.view_option == ViewOption.TIMEZONE:
            return
        self.view_option = ViewOption.TIMEZONE
        self.show_view()
        self.show()

    # 选中查询视图
    @pyqtSlot()
    def query_view_selected(self):
        if self.view_option == ViewOption.QUERY:
            return
        self.view_option = ViewOption.QUERY
        self.show_view()
        self.show()

    # 显示视图
    @pyqtSlot()
    def show_view(self):
        if self.view_option == ViewOption.QUERY:
            self.input_lon.show()
            self.input_lat.show()
            self.input_k.show()
            self.input_word.show()
            self.input_radius.show()
            self.button_check.show()
            self.button_radius.show()
        else:
            self.input_lon.hide()
            self.input_lat.hide()
            self.input_k.hide()
            self.input_word.hide()
            self.input_radius.hide()
            self.button_check.hide()
            self.button_radius.hide()
            self.lbl_delay.hide()

        # 判断当前的视图，显示相应的map，否则隐藏
        for item in self.map_list:
            if item.get_view_option() == self.view_option:
                item.show()
            else:
                item.hide()

    # 输入文字时隐藏警告
    @pyqtSlot()
    def text_changed(self):
        self.input_lon.hide_warning()
        self.input_lat.hide_warning()
        self.input_k.hide_warning()
        self.lbl_delay.hide()

    # top-k查询
    @pyqtSlot()
    def top_k_query(self):
        lon = float(self.input_lon.text())
        lat = float(self.input_lat.text())
        k = int(self.input_k.text())
        word = self.input_word.text()
        if lon >= -180 and lon <= 180 and lat >= -90 and lat <= 90 and k >= 1 and k <= 25600:
            start = time.clock()
            if self.map_query.get_point() is not None:
                self.map_query.get_point().set_visible(False)
            self.map_query.show_top_k(lon, lat, k, word)
            self.map_query.get_point().set_visible(True)
            self.map_query.refresh()
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

    # 按距离查询
    @pyqtSlot()
    def radius_query(self):
        lon = float(self.input_lon.text())
        lat = float(self.input_lat.text())
        radius = int(self.input_radius.text())
        if lon >= -180 and lon <= 180 and lat >= -90 and lat <= 90:
            start = time.clock()
            if self.map_query.get_point() is not None:
                self.map_query.get_point().set_visible(False)
            self.map_query.show_radius(lon, lat, radius)
            self.map_query.get_point().set_visible(True)
            self.map_query.refresh()
            end = time.clock()
            delay = round(end - start, 3)
            self.lbl_delay.setText('此次查询时延为' + str(delay) + '秒')
            self.lbl_delay.show()

    # 生成range-时延变化图
    @pyqtSlot()
    def radius_delay_graph(self):
        x = []
        y = []

        lon = float(self.input_lon.text())
        lat = float(self.input_lat.text())

        radius = 1000
        while radius <= 20000:
            if lon >= -180 and lon <= 180 and lat >= -90 and lat <= 90:
                start = time.clock()
                if self.map_query.get_point() is not None:
                    self.map_query.get_point().set_visible(False)
                self.map_query.show_radius(lon, lat, radius)
                # self.map_query.refresh()
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

    # 生成k-时延变化图
    @pyqtSlot()
    def k_delay_graph(self):
        x = []
        y = []

        lon = float(self.input_lon.text())
        lat = float(self.input_lat.text())

        i = 1250
        while i <= 25600:
            k = i
            if lon >= -180 and lon <= 180 and lat >= -90 and lat <= 90 and k >= 1 and k <= 25600:
                start = time.clock()
                if self.map_query.get_point() is not None:
                    self.map_query.get_point().set_visible(False)
                self.map_query.show_top_k(lon, lat, k, '')
                # self.map_query.refresh()
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



