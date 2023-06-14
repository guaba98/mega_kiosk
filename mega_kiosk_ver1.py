import os
import sys
import sqlite3
import pandas as pd

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *


def resource_path(relative_path):
    """UI 받아오는 함수"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form = resource_path('mega_ui_ver3.ui')  # 메가 메인 UI 불러오기
form_class = uic.loadUiType(form)[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 오픈화면
        self.stackedWidget.setCurrentIndex(0)  # 시작할때 화면은 오픈 페이지로 설정
        self.set_ad_image()  # 이미지 변경
        # 오픈 화면에서 아무 곳이나 클릭하면 메인 페이지 1번으로 이동한다.
        self.ad_label.mousePressEvent = lambda event: self.stackedWidget.setCurrentWidget(self.main_page)   #


        # 메인화면

        # 0. DB 불러오기
        con = sqlite3.connect('./DATA/data.db')
        cur = con.cursor()
        price_df = pd.read_sql('select * from drinks_price', con)  # 가격 테이블
        self.menu_df = pd.read_sql('select * from drinks_menu', con)  # 음료상세정보 전체 테이블
        self.img_path_df = pd.read_sql('select * from drinks_img_path', con)  # 음료 이미지 경로 테이블

        # 1. 카테고리 버튼 이동
        self.category_btn_list = [getattr(self, f"category_btn_{i}") for i in range(1, 16)]  # 카테고리 버튼 리스트화
        # print(self.category_btn_list)  # 확인용
        for btn in self.category_btn_list:
            btn.clicked.connect(self.change_categroy_btn_color)  # 버튼 색 바꾸기
            btn.clicked.connect(self.set_categroy_num)  # 카테고리 하단 메뉴 크기 설정
            btn.clicked.connect(self.show_menu_arrow_btn)  # 카테고리 하단 메뉴 크기 설정

        # 2. 카테고리 페이지 넘기기 (메인화면 페이지 넘기기)
        self.category_right_btn.clicked.connect(lambda: self.category_stackedWidget.setCurrentWidget(self.category_2))
        self.category_left_btn_2.clicked.connect(lambda: self.category_stackedWidget.setCurrentWidget(self.category_1))

        # 3. 커피 메뉴 좌/우 버튼
        self.category_btn_1.click()
        self.menu_arrow_btn_num = 2
        self.menu_right_btn.clicked.connect(lambda: self.menu_stackedWidget.setCurrentWidget(self.page_2))
        self.menu_right_btn.clicked.connect(self.show_menu_arrow_btn)
        self.menu_left_btn.clicked.connect(lambda: self.menu_stackedWidget.setCurrentWidget(self.page_1))
        self.menu_left_btn.clicked.connect(self.show_menu_arrow_btn)



    def show_menu_arrow_btn(self):
        """카테고리 개수에 따라 메뉴 화살표상태를 변경합니다."""

        current_page = self.menu_stackedWidget.currentWidget().objectName()
        # print(current_page)
        if self.menu_arrow_btn_num == 2:
            # print('번호는 2페이지')
            if current_page == 'page_1':
                # print('페이지1번입니다.')
                self.menu_right_btn.show()
                self.menu_left_btn.hide()
            else:
                self.menu_right_btn.hide()
                self.menu_left_btn.show()
        elif self.menu_arrow_btn_num == 1:
            self.menu_right_btn.hide()
            self.menu_left_btn.hide()

    def set_categroy_num(self):
        """카테고리 숫자에 따라 음료 라벨 보여주기"""

        # [1] 카테고리 수 만큼 프레임 보여주기
        menu_frame_list = [getattr(self, f"menu_frame_{i}") for i in range(1, 25)]  # 담길 라벨 리스트화
        btn_name = self.sender().text()  # 버튼 이름 가져오기
        category_drinks_num = len(self.menu_df[self.menu_df['category'] == btn_name])  # 카테고리 메뉴 갯수 세기

        # 카테고리 번호만큼 프레임 보여주기
        for index, frame in enumerate(menu_frame_list):
            getattr(self, f'menu_img_{index + 1}').clear() # 라벨 클리어 시켜주기
            getattr(self, f'menu_name_label_{index + 1}').clear()
            getattr(self, f'menu_price_label_{index + 1}').clear()
            if index+1 <= category_drinks_num: # 해당하는 카테고리 번호까지 프레임의 background-color 바꿔준다.
                frame.setStyleSheet('background-color: white;')
            else:
                frame.setStyleSheet('background-color: rgb(255, 204, 0);')

        # [2] 이미지 삽입
        # 1) menu table과 img_path 테이블을 join (key = id)
        menu_and_price_join_df = pd.merge(self.menu_df, self.img_path_df, how='left', on='id') #조인
        menu_and_price_join_df_2 = menu_and_price_join_df.loc[:, ['id','category', 'category_num', 'menu_name_x', 'img_path', 'price']] #테이블 2차 가공 원하는 열만
        # print(menu_and_price_join_df_2) #확인용

        # 2)이미지 열을 라벨에 입힌다. 카테고리 번호에 맞게
        con1 = (menu_and_price_join_df_2['category']==btn_name) #버튼 번호에 맞는 조건 설정
        menu_df = menu_and_price_join_df_2.loc[con1, ['category_num','img_path', 'menu_name_x', 'price']] #카테고리 번호와 이미지 경로만 출력
        print(menu_df)

        for i in range(1, category_drinks_num+1):
            print(i)
            con2 = menu_df['category_num']==i
            # print(menu_df.loc[con2, ['img_path']])
            # print(menu_df.loc[con2, 'menu_name_x'].values)
            # print(menu_df.loc[con2, 'price'].values)
            drink_img = menu_df.loc[con2, 'img_path'].values
            drink_name =menu_df.loc[con2, 'menu_name_x'].values
            drink_price = menu_df.loc[con2, 'price'].values
            getattr(self, f'menu_img_{i}').setPixmap(QPixmap(drink_img[0]).scaled(QSize(120, 116), aspectRatioMode=Qt.IgnoreAspectRatio))
            getattr(self, f'menu_name_label_{i}').setText(str(drink_name[0]))
            getattr(self, f'menu_price_label_{i}').setText(str(drink_price[0]))


        # for num, path in img_dict.items():
        #     getattr(self, f'menu_img_{num}').setPixmap(
        #                         QPixmap(path).scaled(QSize(155, 84), aspectRatioMode=Qt.IgnoreAspectRatio))


        # new_dict = img_df.set_index('category_num').to_dict(orient='index')
        # print(new_dict)

        # for key in new_dict.keys():
        #     new_dict[key] = {'img_path': new_dict[key]['img_path'], 'menu_name_x': new_dict[key]['menu_name_x'],
        #                      'price': new_dict[key]['price']}
        # print(new_dict)
        # new_dict = img_df.loc[:, ['category_num', 'img_path']].set_index('category_num').to_dict()['img_path']
        #
        # for num, path in img_dict.items():
        #     getattr(self, f'menu_img_{num}').setPixmap(
        #                         QPixmap(path).scaled(QSize(155, 84), aspectRatioMode=Qt.IgnoreAspectRatio))

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
