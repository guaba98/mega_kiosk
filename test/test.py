import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton, QVBoxLayout, QHBoxLayout, QLabel

class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()

        # 프레임 생성
        frame = QFrame(self)
        frame.setFrameShape(QFrame.Box)

        # 프레임 안에 배치할 위젯 생성
        label = QLabel("Frame")
        button = QPushButton("Button")

        # 수평 레이아웃 생성
        hbox = QHBoxLayout(frame)
        hbox.addWidget(label)
        hbox.addWidget(button)

        # 내부 프레임 생성
        inner_frame = QFrame(frame)
        inner_frame.setFrameShape(QFrame.Box)

        # 내부 프레임의 레이아웃 생성
        vbox = QVBoxLayout(inner_frame)
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)

        # 내부 프레임에 추가할 위젯 생성
        label = QLabel("Inner Frame")
        button = QPushButton("Button")

        # 내부 프레임에 위젯 추가
        hbox.addWidget(label)
        vbox.addWidget(button)

        # 내부 프레임의 레이아웃 설정
        inner_frame.setLayout(vbox)

        # 프레임 안에 내부 프레임 추가
        hbox.addWidget(inner_frame)

        # 윈도우의 레이아웃 설정
        self.setCentralWidget(frame)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
