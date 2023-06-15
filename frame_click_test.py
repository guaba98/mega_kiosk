from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5 import QtWidgets


class ClickableFrame(QtWidgets.QFrame):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.frame = ClickableFrame(self)
        self.frame.clicked.connect(self.click_frame)
        self.setCentralWidget(self.frame)

    def click_frame(self):
        print('Frame clicked')

app = QtWidgets.QApplication([])
window = MyWindow()
window.show()
app.exec_()
