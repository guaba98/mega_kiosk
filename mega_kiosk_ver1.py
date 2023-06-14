import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *


def resource_path(relative_path):
    """UI 받아오는 함수"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path('mega_ui_ver1.ui')  # 메가 메인 UI 불러오기
form_class = uic.loadUiType(form)[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 오픈화면
        self.stackedWidget.setCurrentIndex(0)  # 시작할때 화면은 오픈 페이지로 설정
        self.set_ad_image()  # 이미지 변경 시작
        self.ad_label.mousePressEvent = lambda event: self.stackedWidget.setCurrentIndex(
            2)  # 오픈 화면에서 아무 곳이나 클릭하면 메인 페이지로 이동한다.

        # 메인화면
        category_btn_list = [getattr(self, f"category_btn_{i}") for i in range(1, 11)]  # 카테고리 버튼 리스트화
        print(category_btn_list) #확인용
        for btn in category_btn_list:
            btn.clicked.connect(self.change_categroy_btn_color)


    def change_categroy_btn_color(self):
        """메인화면 상단 카테고리 버튼 색 바뀌게 함"""
        btn_name = self.sender().objectName()
        btn_object = self.sender()
        btn_object.setStyleSheet('background-color: rgb(45, 45, 45); border: 2px solid rgb(45, 45, 45); border-radius:15px; color:white;')


    def set_ad_image(self):
        """3초에 한번씩 오픈 페이지 이미지 변하게 함"""
        self.ad_img_num = 1  # 오픈 페이지 이미지 변수 설정
        self.ad_label.setPixmap(QPixmap(f'./img/ad/ad_img_{self.ad_img_num}').scaled(QSize(768, 1024)))  # 첫번째 이미지

        # 3초 타이머 설정.
        ad_timer = QTimer(self)
        ad_timer.timeout.connect(self.change_ad_image)  # 타임아웃되면 change_ad_image 함수로 이동
        ad_timer.start(3000)

    def change_ad_image(self):
        """3초에 1번씩 이미지 변경해 줌"""
        self.ad_img_num += 1  # 이미지 변수에 1씩 더해줌
        if self.ad_img_num == 5:  # 만약 5라면
            self.ad_img_num = 1  # 1로 만들어준다

        pixmap = QPixmap(f'./img/ad/ad_img_{self.ad_img_num}')  # 사진 경로 받아오기
        self.ad_label.setPixmap(QPixmap(pixmap).scaled(QSize(768, 1024)))  # 라벨 이미지에 설정함


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
