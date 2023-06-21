import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget
from PyQt5.QtGui import QColor
from PyQt5 import QtGui

from PyQt5.QtCore import Qt

class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.btn = QPushButton('클릭!', self)
        self.btn.setGeometry(10, 10, 100, 30)
        self.btn.setStyleSheet('background-color: white;')
        self.btn.clicked.connect(self.change_color)

        self.show()

    def change_color(self):
        if self.btn.palette().color(QtGui.QPalette.Button) == QColor(Qt.white):
            self.btn.setStyleSheet('background-color: red')
        else:
            self.btn.setStyleSheet('background-color: white')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

