import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import *

# 더 추가할 필요가 있다면 추가하시면 됩니다. 예: (from PyQt5.QtGui import QIcon)

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('test.ui')
form_class = uic.loadUiType(form)[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)

        # 외부 프레임의 레이아웃 설정해줌 - vbox
        vbox = QVBoxLayout(self.frame)

        # 내부 프레임 생성, 외부 프레임 내에 생성해줌
        inner_frame = QFrame(self.frame)

        # 내부 프레임에 들어갈 레이아웃 넣어줌
        hbox = QHBoxLayout()

        # 내부 프레임에 들어갈 라벨, 버튼 생성해줌
        x_btn = QPushButton('x버튼')
        label = QLabel('번호')
        drink_name_lab = QLabel('음료이름')
        minus_btn = QPushButton('-')
        num_label = QLabel('수량')
        plus_btn = QPushButton('+')
        drink_price_lab = QLabel('가격')

        # 레이아웃에 생성한 객체 넣어줌
        hbox.addWidget(x_btn)
        hbox.addWidget(label)
        hbox.addWidget(drink_name_lab)
        hbox.addWidget(minus_btn)
        hbox.addWidget(num_label)
        hbox.addWidget(plus_btn)

        hbox.addWidget(drink_price_lab)

        # 레이아웃을 내부 프레임에 넣어주고 외부 프레임에 담아줌
        inner_frame.setLayout(hbox)
        vbox.addWidget(inner_frame)

        # 스페이서 생성
        vbox.addStretch()



        # hbox = QHBoxLayout(inner_frame)
        # 여기에 시그널, 설정
    #여기에 함수 설정

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )