import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

# 더 추가할 필요가 있다면 추가하시면 됩니다. 예: (from PyQt5.QtGui import QIcon)

def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('test_2.ui')
form_class = uic.loadUiType(form)[0]

class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)

        # 외부 프레임의 레이아웃 설정해줌 - vbox
        self.my_veticalLayout = QVBoxLayout(self.my_scrollAreaWidgetContents)
        self.my_veticalLayout.setSpacing(0)
        self.my_veticalLayout.setObjectName(u"my_veticalLayout")
        self.my_veticalLayout.setContentsMargins(0, 0, 0, 0)


        self.my_frame = QFrame(self.my_scrollAreaWidgetContents)
        self.my_frame.setObjectName(u"my_frame")
        self.my_frame.setMinimumSize(QSize(516, 40))
        self.my_frame.setMaximumSize(QSize(16777215, 40))
        self.my_frame.setFrameShape(QFrame.StyledPanel)
        self.my_frame.setFrameShadow(QFrame.Raised)

        self.horizontalLayout = QHBoxLayout(self.my_frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.my_remove_btn_1 = QPushButton(self.my_frame)
        self.my_remove_btn_1.setObjectName(u"my_remove_btn_1")
        self.my_remove_btn_1.setMaximumSize(QSize(40, 40))
        self.my_remove_btn_1.setStyleSheet(u"background-color: rgba(255, 255, 255, 0);")
        self.my_remove_btn_1.setIconSize(QSize(35, 35))
        self.horizontalLayout.addWidget(self.my_remove_btn_1)

        self.my_cart_num_1 = QLabel(self.my_frame)
        self.my_cart_num_1.setObjectName(u"my_cart_num_1")
        self.my_cart_num_1.setMaximumSize(QSize(30, 40))
        self.my_cart_num_1.setStyleSheet(u"background-color: rgb(170, 255, 255);\n"
                                      "color:rgb(229, 79, 64);")
        self.my_cart_num_1.setAlignment(Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.my_cart_num_1)

        self.my_drink_name_1 = QLabel(self.my_frame)
        self.my_drink_name_1.setObjectName(u"cart_drink_name_1")
        self.my_drink_name_1.setMinimumSize(QSize(180, 0))
        self.my_drink_name_1.setMaximumSize(QSize(180, 40))
        self.my_drink_name_1.setStyleSheet(u"background-color: rgb(255, 255, 0);")
        self.horizontalLayout.addWidget(self.my_drink_name_1)

        self.my_minus_btn_1 = QPushButton(self.my_frame)
        self.my_minus_btn_1.setObjectName(u"my_minus_btn_1")
        self.my_minus_btn_1.setMaximumSize(QSize(40, 40))
        self.my_minus_btn_1.setStyleSheet(u"background-color: rgb(229, 79, 64);")
        self.horizontalLayout.addWidget(self.my_minus_btn_1)

        self.my_drink_cnt_1 = QLabel(self.my_frame)
        self.my_drink_cnt_1.setObjectName(u"my_drink_cnt_1")
        self.my_drink_cnt_1.setMaximumSize(QSize(16777215, 40))
        self.my_drink_cnt_1.setStyleSheet(u"background-color: rgb(255, 170, 255);")
        self.my_drink_cnt_1.setAlignment(Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.my_drink_cnt_1)

        self.my_plus_btn_1 = QPushButton(self.my_frame)
        self.my_plus_btn_1.setObjectName(u"my_plus_btn_1")
        self.my_plus_btn_1.setMaximumSize(QSize(40, 40))
        self.my_plus_btn_1.setStyleSheet(u"background-color:rgb(229, 79, 64);")
        self.horizontalLayout.addWidget(self.my_plus_btn_1)

        self.my_price_1 = QLabel(self.my_frame)
        self.my_price_1.setObjectName(u"cart_price_1")
        self.my_price_1.setStyleSheet(u"background-color: rgb(170, 255, 255);")
        self.my_price_1.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.my_price_1)


        self.my_veticalLayout.addWidget(self.my_frame)
        self.my_verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.my_veticalLayout.addItem(self.my_verticalSpacer)


        self.my_scroll_area.setWidget(self.my_scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.my_scroll_area)

        # 스페이서 생성
        # vbox.addStretch()



        # hbox = QHBoxLayout(inner_frame)
        # 여기에 시그널, 설정
    #여기에 함수 설정

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass( )
    myWindow.show( )
    app.exec_( )