#
# 自定义的输入控件，包含了一个标题label，一个文本框，一个警告label
#

from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QLabel
from PyQt5.QtCore import Qt


class InputWid:

    def __init__(self, parent=None, header='', warning=''):
        self._x = 0
        self._y = 0

        # 标题
        self.header = QLabel(header, parent)
        self.header.move(self._x, self._y)
        self.header.setFixedWidth(45)
        self.header.setAlignment(Qt.AlignRight | Qt.AlignCenter)

        # 文本内容
        self.content = QLineEdit(parent)
        self.content.move(self._x + 50, self._y)
        self.content.setFixedWidth(130)

        # 警告信息
        self.warning = QLabel(warning, parent)
        self.warning.move(self._x + 50, self._y + 30)
        self.warning.setFixedWidth(140)
        self.warning.hide()


    def set_header(self, header):
        self.header.setText(header)

    def set_text(self, text):
        self.content.setText(text)

    def text(self):
        return self.content.text()

    def set_warning(self, warning):
        self.warning.setText(warning)

    def reset(self):
        self.content.setText('')

    # 显示整个控件时，不需要显示警告信息
    def show(self):
        self.header.show()
        self.content.show()

    def hide(self):
        self.header.hide()
        self.content.hide()
        self.warning.hide()

    def show_warning(self):
        self.warning.show()

    def hide_warning(self):
        self.warning.hide()

    # 文本改变事件绑定到文本框上
    def connect(self, func):
        self.content.textChanged.connect(func)

    def set_location(self, x, y):
        self._x = x
        self._y = y

        self.header.move(self._x, self._y)
        self.content.move(self._x + 50, self._y)
        self.warning.move(self._x + 50, self._y + 30)