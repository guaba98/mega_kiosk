# -*- coding: utf-8 -*-
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PIL import ImageQt


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(800, 600)
        self.setWindowTitle('Painter Board')

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 800, 600)
        self.label.setStyleSheet('background-colr:yellow')
        # self.label.setPixmap(QPixmap("../../Pictures/Saved Pictures/dog.jpg"))
        self.label.setScaledContents(True)

        self.add = QShortcut(QKeySequence("Ctrl+S"), self)
        self.add.activated.connect(self.compositeEvent)

    def compositeEvent(self):
        image = ImageQt.fromqpixmap(self.label.pixmap())
        image.save('test.png')


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())