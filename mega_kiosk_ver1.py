import os
import sys
import sqlite3
import pandas as pd
import numpy as np

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets


def resource_path(relative_path):
    """UI 받아오는 함수"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path('mega_ui_ver3.ui')  # 메가 메인 UI 불러오기
form_class = uic.loadUiType(form)[0]


class WindowClass(QMainWindow, form_class):
    clicked = pyqtSignal()
    def add_page_mouse_press(self, event):
        self.stackedWidget.setCurrentWidget(self.main_page)
        # self.start_timer()
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.timer_list = []

        # 오픈화면
        self.stackedWidget.setCurrentIndex(0)  # 시작할때 화면은 오픈 페이지로 설정
        self.set_ad_image()  # 이미지 변경
        self.DURATION_INT = 120
        self.ad_label.mousePressEvent = self.add_page_mouse_press

        # 페이지 이동 및 타이머 시작
        # self.ad_label.mousePressEvent = lambda event: (
        #     self.stackedWidget.setCurrentWidget(self.main_page), #페이지 이동
        #     self.start_timer() #동시에 타이머 시작
        # )

        # 메인화면
        # 0. DB 불러오기
        con = sqlite3.connect('./DATA/data.db')
        cur = con.cursor()
        price_df = pd.read_sql('select * from drinks_price', con)  # 가격 테이블
        self.menu_df = pd.read_sql('select * from drinks_menu', con)  # 음료상세정보 전체 테이블
        self.img_path_df = pd.read_sql('select * from drinks_img_path', con)  # 음료 이미지 경로 테이블
        self.sold_out_df = pd.read_sql('select * from sold_out', con)
        # print(self.menu_df['category'])

        # 1. 카테고리 버튼 이동
        self.category_btn_list = [getattr(self, f"category_btn_{i}") for i in range(1, 16)]  # 카테고리 버튼 리스트화
        for btn in self.category_btn_list:

            btn.clicked.connect(self.change_categroy_btn_color)  # 버튼 색 바꾸기
            btn.clicked.connect(self.set_categroy_num)  # 카테고리 하단 메뉴 크기 설정
            btn.clicked.connect(self.show_menu_arrow_btn)  # 카테고리 하단 메뉴 크기 설정
            btn.clicked.connect(lambda: self.menu_stackedWidget.setCurrentWidget(self.page_1))

        # 2. 카테고리 페이지 넘기기 (메인화면 페이지 넘기기)
        self.category_right_btn.clicked.connect(lambda: self.category_stackedWidget.setCurrentWidget(self.category_2))
        self.category_left_btn_2.clicked.connect(lambda: self.category_stackedWidget.setCurrentWidget(self.category_1))

        # 3. 커피 메뉴 좌/우 버튼
        self.category_btn_1.click()
        self.menu_arrow_btn_num = 2
        self.menu_left_btn.clicked.connect(lambda: self.menu_stackedWidget.setCurrentWidget(self.page_1))
        self.menu_right_btn.clicked.connect(lambda: self.menu_stackedWidget.setCurrentWidget(self.page_2))
        self.menu_right_btn.clicked.connect(self.show_menu_arrow_btn)
        self.menu_left_btn.clicked.connect(self.show_menu_arrow_btn)

        # 4. 프레임 버튼 클릭하기 및 가격 폰트 변경
        self.menu_frame_list = [getattr(self, f"menu_frame_{i}") for i in range(1, 25)]  # 메뉴 프레임 리스트화
        for frame in self.menu_frame_list:
            frame.mousePressEvent = lambda event, name=frame.objectName(): self.click_frame(event, name)

        self.menu_price_label_list = [getattr(self, f"menu_price_label_{i}") for i in range(1, 25)]  # 가격 폰트 리스트
        for label in self.menu_price_label_list:
            label.setStyleSheet('color: rgb(229, 79, 64);font: 63 12pt "Pretendard SemiBold";')

        # 5. 타이머
        # self.DURATION_INT = 10
        # self.start_timer()

        #타이머 시작 함수

    def timer_clear(self):
        # self.timer.stop()
        self.time_left_int = self.DURATION_INT
        self.start_timer()

    def start_timer(self):
        # 여기서부터 다시 해야함 #######################################################
        """타이머 시작하는 함수"""
        print('유저가 선택한 카테고리',self.user_clicked_category)
        if self.timer_list[0] != self.user_clicked_category:
            self.timer.stop()
            print('타이머 멈춤')
            self.time_left_int = self.DURATION_INT
            self.timer = QTimer(self)
            self.timer.start(1000)
            self.timer.timeout.connect(self.timerTimeout)
            self.timer.start()

        else:
            self.time_left_int = self.DURATION_INT
            self.timer = QTimer(self)
            self.timer.start(1000)
            self.timer.timeout.connect(self.timerTimeout)
            self.timer.start()

    def timerTimeout(self):
        """1초가 지날때마다 시간을 초기화 시켜줌"""
        self.time_left_int -= 1
        if self.time_left_int == 0:
            self.time_left_int = self.DURATION_INT
            self.stackedWidget.setCurrentIndex(0)  # 120초가 지나면 시간 초기화하고 오픈화면으로 이동
        self.timer_label.setText(f'{str(self.time_left_int)}초')


    def click_frame(self, event, name):
        """프레임 선택 테스트"""
        # print(f'{name}프레임을 선택했습니다.')
        # print(name[11:])
        condition1 = (self.menu_df['category'] == self.user_clicked_category)
        condition2 = (self.menu_df['category_num'] == int(name[11:]))
        # condition3 = (self.menu_df['sold_out'] == 0)
        sold_out_state = self.menu_df.loc[condition1&condition2, 'sold_out']
        print(sold_out_state)
        if sold_out_state.sum() > 0:
            print('품절')
        else:
            print('낫품절')


    def show_menu_arrow_btn(self):
        """카테고리 개수에 따라 메뉴 화살표상태를 변경합니다."""

        current_page = self.menu_stackedWidget.currentWidget().objectName()
        self.menu_right_btn.setVisible(current_page == 'page_1' and self.menu_arrow_btn_num == 2)
        self.menu_left_btn.setVisible(current_page == 'page_2' and self.menu_arrow_btn_num == 2)

    def set_categroy_num(self):
        """카테고리 숫자에 따라 음료 라벨 보여주기"""

        # [1] 카테고리 수 만큼 프레임 보여주기
        menu_frame_list = [getattr(self, f"menu_frame_{i}") for i in range(1, 25)]  # 담길 라벨 리스트화
        btn_name = self.sender().text()  # 버튼 이름 가져오기
        self.user_clicked_category = btn_name
        self.timer_list.insert(0, btn_name)
        print('타이머리스트',self.timer_list)
        print('타이머리스트 1번',self.timer_list[0])

        self.start_timer()  # 일단 여기에 넣어놓음 타이머
        category_drinks_num = len(self.menu_df[self.menu_df['category'] == btn_name])  # 카테고리 메뉴 갯수 세기

        # 카테고리 번호만큼 프레임 보여주기
        for index, frame in enumerate(menu_frame_list):
            getattr(self, f'menu_img_{index + 1}').clear()  # 라벨 클리어 시켜주기
            getattr(self, f'menu_name_label_{index + 1}').clear()
            getattr(self, f'menu_price_label_{index + 1}').clear()
            if index + 1 <= category_drinks_num:  # 해당하는 카테고리 번호까지 프레임의 background-color 바꿔준다.
                frame.setStyleSheet('background-color: white;')
            else:
                frame.setStyleSheet('background-color: rgb(255, 204, 0);')

        self.insert_img(btn_name, category_drinks_num)

    def insert_img(self, btn_name, category_drinks_num):
        # [2] 이미지 삽입
        # 1) menu table과 img_path 테이블을 join (key = id)
        menu_and_price_join_df = pd.merge(self.menu_df, self.img_path_df, how='left', on='id')  # 조인
        con1 = (menu_and_price_join_df['category'] == btn_name)  # 버튼 번호에 맞는 조건 설정
        user_click_category_df = menu_and_price_join_df.loc[
            con1, ['id', 'category', 'category_num', 'sold_out', 'menu_name_x', 'img_path',
                   'price']]  # 테이블 2차 가공 원하는 열만
        print(user_click_category_df[['category', 'category_num', 'img_path']])

        # 2)이미지 열을 라벨에 입힌다. 카테고리 번호에 맞게
        con3 = user_click_category_df['sold_out'] == 1
        for i in range(1, category_drinks_num + 1):
            con2 = user_click_category_df['category_num'] == i  # 조건: 카테고리 번호가 일치해야 함

            drink_img = user_click_category_df.loc[con2, 'img_path'].values
            drink_name = user_click_category_df.loc[con2, 'menu_name_x'].values
            drink_price = user_click_category_df.loc[con2, 'price'].values
            sold_out_state = user_click_category_df.loc[con2 & con3, 'sold_out'].values

            if sold_out_state.size > 0:
                print(drink_name, '품절')
                getattr(self, f'menu_img_{i}').setPixmap(
                    QPixmap('./img/qt자료/sold_out_3.png').scaled(175, 180, Qt.IgnoreAspectRatio))
            elif drink_img.size > 0 and drink_name.size > 0 and drink_price.size > 0:
                getattr(self, f'menu_img_{i}').setPixmap(QPixmap(drink_img[0]))
            getattr(self, f'menu_name_label_{i}').setText(str(drink_name[0]))
            getattr(self, f'menu_price_label_{i}').setText(f'{str(drink_price[0])}원')

        if category_drinks_num > 12:
            self.menu_arrow_btn_num = 2
        else:
            self.menu_arrow_btn_num = 1

    def change_categroy_btn_color(self):
        """메인화면 상단 카테고리 버튼 색 바뀌게 함"""


        btn_object = self.sender()  # 버튼 객체 가져오기

        # 선택한 버튼 색 바꾸고 그 외의 색 바꾸기
        for btn in self.category_btn_list:
            if btn == btn_object:
                btn.setStyleSheet('''
                    background-color: rgb(45, 45, 45);
                    border: 2px solid rgb(45, 45, 45);
                    border-radius:15px; color:white; 
                    ''')
            else:
                btn.setStyleSheet('''
                    background-color: rgb(255, 204, 0);
                    border: 2px solid rgb(45, 45, 45);
                    border-radius:15px;
                    color:black;
                    ''')

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
