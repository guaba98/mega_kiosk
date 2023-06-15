from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtCore
import sys

DURATION_INT = 600

def secs_to_minsec(secs: int):
    mins = secs // 60
    secs = secs % 60
    minsec = f'{mins:02}:{secs:02}'
    return minsec

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.time_left_int = DURATION_INT
        self.myTimer = QtCore.QTimer(self)

        # App window
        self.app = QApplication(sys.argv)
        self.win = QMainWindow()
        self.win.setGeometry(200, 200, 200, 200)
        self.win.setWindowTitle("test")

        # Widgets
        self.titleLabel = QtWidgets.QLabel(self.win)
        self.titleLabel.setText("Welcome to my app")
        self.titleLabel.move(50,20)

        self.timerLabel = QtWidgets.QLabel(self.win)
        self.timerLabel.setText("01:00")
        self.timerLabel.move(50,50)
        self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerLabel.setStyleSheet("font: 10pt Helvetica")

        self.startButton = QtWidgets.QPushButton(self.win)
        self.startButton.setText("Start")
        self.startButton.move(50,100)
        self.startButton.clicked.connect(self.startTimer)

        self.stopButton = QtWidgets.QPushButton(self.win)
        self.stopButton.setText("Stop")
        self.stopButton.move(50,130)

        self.update_gui()

        # Show window
        self.win.show()
        sys.exit(app.exec_())

    def startTimer(self):
        self.time_left_int = DURATION_INT

        self.myTimer.timeout.connect(self.timerTimeout)
        self.myTimer.start(1000)

    def timerTimeout(self):
        self.time_left_int -= 1

        if self.time_left_int == 0:
            self.time_left_int = DURATION_INT

        self.update_gui()

    def update_gui(self):
        minsec = secs_to_minsec(self.time_left_int)
        self.timerLabel.setText(minsec)

app = QtWidgets.QApplication(sys.argv)
main_window = App()
main_window.show()
sys.exit(app.exec_())