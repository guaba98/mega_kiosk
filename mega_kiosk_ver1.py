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


main_page_ui = resource_path('mega_ui_ver3.ui')  # 메가 메인 UI 불러오기
main_page_class = uic.loadUiType(main_page_ui)[0]
choose_option_ui = resource_path('mega_choose_option_page.ui') # 메가 선택창 불러오기
choose_option_class = uic.loadUiType(choose_option_ui)[0]
msg_box_ui = resource_path('msg_box.ui') # 메세지박스 ui 불러오기
msg_box_class = uic.loadUiType(msg_box_ui)[0]

class MSG_Dialog(QDialog, msg_box_class):
    """메세지 박스 다이얼로그"""
    data_signal = pyqtSignal(str)
    def __init__(self, page_data):
        super().__init__()
        self.setupUi(self)
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # self.setStyleSheet('''
        # #QDialog{border-radius: 15px;}
        # ''')
        #버튼 페이지 설정
        if page_data == 1:
            self.info_label.setText("메뉴가 품절이라 선택하실 수 없습니다.")
            self.stackedWidget.setCurrentWidget(self.one_btn_page)
        else:
            self.stackedWidget.setCurrentWidget(self.two_btn_page)

        #버튼 누르면 정보 넘겨주기
        self.ok_btn.clicked.connect(self.close)


class Option_Class(QDialog, choose_option_class):
    """선택옵션 창"""
    data_signal = pyqtSignal(str)
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.move(30,40)

        # 데이터 불러오기
        self.order_num = 0
        con = sqlite3.connect('./DATA/data.db')
        price_df = pd.read_sql('select * from drinks_price', con)  # 가격 테이블


        # 가격 이름 메뉴정보 불러오기
        data = parent.send_info
        self.drink_name = data['menu_name_x'].to_string(index=False)
        self.drink_price = data['price'].to_string(index=False)
        self.drink_info = data['info'].to_string(index=False)

        # 정보 담기
        self.menu_photo_label.setPixmap(QPixmap(data['img_path'].to_string(index=False))) #메뉴 이미지
        self.menu_name_label.setText(str(self.drink_name)) #메뉴 이름
        self.menu_info_label.setText(str(self.drink_info)) #메뉴 정보
        self.menu_price_label.setText(str(self.drink_price)+'원') #메뉴 가격

        # 버튼 시그널 연결
        self.cancel_btn.clicked.connect(lambda x: self.close()) # 창 종료하기
        self.cancel_btn.clicked.connect(self.close) # 창 종료하기
        self.order_btn.clicked.connect(self.order_confirm)

        #옵션 위한 테이블 생성
        option_df = data.loc[:, 'cinnamon':'zero_cider_changed']
        option_df_dict = option_df.to_dict('list')


        option_df_dict_not_null = {key: [int(x) for x in value[0].split(',')] for key, value in option_df_dict.items() if
                     value != ['0']}  # '이 양쪽에 들어가지 않은 인수형의 숫자 반환
        if '디카페인' in self.drink_name:
            option_df_dict_not_null['decaffein'] = 1
        visible_dict = {'cinnamon':1, 'whip':2, 'strong_or_weak':3, 'syrup_add':4, 'light_vanilia_add':5,'stevia_changed':6,
                        'stevia_add':7, 'honey_add':8, 'choose_milk':9, 'choose_topping':10, 'decaffein':11, 'zero_cider_changed':12}
        option_frame_list = [getattr(self, f'option_frame_{frame}') for frame in range(1, 13)]
        print(list(option_df_dict_not_null.keys()))
        for idx, column in enumerate(list(visible_dict.keys())):
            if column in list(option_df_dict_not_null.keys()):
                option_frame_list[idx].setVisible(True)
            else:
                option_frame_list[idx].setVisible(False)



            # print('선택옵션:', i)
            # option_frame_list[visible_dict[i]].setVisible(True)
            # print(visible_dict[i])
            # print('=======================')



    def close(self):
        self.parent.remove_label()
        self.accept()

    def order_confirm(self):
        """선택옵션 확인 후 db에 저장"""
        self.order_num += 1

        # 고객 db 불러오기 및 order table 테이블에 에 값 append(추가해주기)
        conn = sqlite3.connect('./DATA/data.db')  # 데이터베이스 연결 정보 설정
        cur = conn.cursor()  # 커서 생성
        cur.execute("INSERT INTO order_table (id, order_drink, price) VALUES(?,?,?);", # SQL 쿼리 실행
                    (self.order_num, self.drink_name, self.drink_price))
        conn.commit() #변경사항 저장
        cur.close() #연결 종료
        conn.close()

        # 선택옵션 창 종료
        self.sample_label.close()
        self.close()


class WindowClass(QMainWindow, main_page_class):
    """오픈화면 & 메인화면 창"""
    clicked = pyqtSignal()

    def add_page_mouse_press(self, event):
        """오픈화면 누르면 발생하는 이벤트"""
        self.stackedWidget.setCurrentWidget(self.main_page)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 오픈화면
        self.stackedWidget.setCurrentIndex(0)  # 시작할때 화면은 오픈 페이지로 설정
        self.set_ad_image()  # 이미지 변경
        # self.setWindowFlags(Qt.FramelessWindowHint) # 프레임 지우기
        # self.move(10,30) #창이동

        # 페이지 이동 및 타이머 시작
        self.ad_label.mousePressEvent = lambda event: (self.stackedWidget.setCurrentWidget(self.main_page))  # 페이지 이동)

        # 메인화면
        # 0. DB 불러오기
        con = sqlite3.connect('./DATA/data.db')
        cur = con.cursor()
        self.price_df = pd.read_sql('select * from drinks_price', con)  # 가격 테이블
        self.menu_df = pd.read_sql('select * from drinks_menu', con)  # 음료상세정보 전체 테이블
        self.img_path_df = pd.read_sql('select * from drinks_img_path', con)  # 음료 이미지 경로 테이블
        self.order_table_df = pd.read_sql('select * from order_table', con)  #
        print(self.order_table_df)

        # 1. 타이머
        # 타이머 기본 설정값
        self.DURATION_INT = 120
        self.remaining_time = self.DURATION_INT

        # # 타이머와 관련된 변수들
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.setInterval(1000)

        # 2. 카테고리 버튼 이동
        self.category_btn_list = [getattr(self, f"category_btn_{i}") for i in range(1, 16)]  # 카테고리 버튼 리스트화
        for btn in self.category_btn_list:
            btn.clicked.connect(self.change_categroy_btn_color)  # 버튼 색 바꾸기
            btn.clicked.connect(self.set_categroy_num)  # 카테고리 하단 메뉴 크기 설정
            btn.clicked.connect(self.show_menu_arrow_btn)  # 카테고리 하단 메뉴 크기 설정
            btn.clicked.connect(lambda: self.menu_stackedWidget.setCurrentWidget(self.page_1)) # 음료 페이지 1페이지로 초기화
            btn.clicked.connect(
                lambda x, category=btn: self.start_timer(btn)) #카테고리 버튼 누를 때마다 타이머 초기화


        # 3. 카테고리 페이지 넘기기 (메인화면 페이지 넘기기)
        self.category_right_btn.clicked.connect(lambda: self.category_stackedWidget.setCurrentWidget(self.category_2))
        self.category_left_btn_2.clicked.connect(lambda: self.category_stackedWidget.setCurrentWidget(self.category_1))

        # 4. 커피 메뉴 좌/우 버튼
        self.category_btn_1.click()
        self.menu_arrow_btn_num = 2
        self.menu_left_btn.clicked.connect(lambda: self.menu_stackedWidget.setCurrentWidget(self.page_1))
        self.menu_right_btn.clicked.connect(lambda: self.menu_stackedWidget.setCurrentWidget(self.page_2))
        self.menu_right_btn.clicked.connect(self.show_menu_arrow_btn)
        self.menu_left_btn.clicked.connect(self.show_menu_arrow_btn)

        # 5. 프레임 버튼 클릭하기 및 가격 폰트 변경
        self.menu_frame_list = [getattr(self, f"menu_frame_{i}") for i in range(1, 25)]  # 메뉴 프레임 리스트화
        for frame in self.menu_frame_list:
            frame.mousePressEvent = lambda event, name=frame.objectName(): self.click_frame(event, name)

        self.menu_price_label_list = [getattr(self, f"menu_price_label_{i}") for i in range(1, 25)]  # 가격 폰트 리스트
        for label in self.menu_price_label_list:
            label.setStyleSheet('color: rgb(229, 79, 64);font: 63 12pt "Pretendard SemiBold";')

        # 6. 전체 삭제 버튼
        self.all_remove_label.clicked.connect(self.delete_order_table_values)


    def delete_order_table_values(self):
        """ 주문 값 삭제"""
        conn = sqlite3.connect('./DATA/data.db')  # 데이터베이스 연결 정보 설정
        cur = conn.cursor()  # 커서 생성
        cur.execute("DELETE FROM 'order_table'")  # SQL 쿼리 실행
        conn.commit() #변경사항 저장
        cur.close() # 연결 종료
        conn.close()

    def start_timer(self, category):
        """타이머 시작하는 함수"""
        self.timer.stop()
        self.remaining_time = self.DURATION_INT
        self.timer.start()

    def update_timer(self):
        """타이머 시간 업데이트"""
        self.remaining_time -= 1
        if self.remaining_time == 0:
            self.remaining_time = self.DURATION_INT
            self.stackedWidget.setCurrentWidget(self.main_page)
        self.timer_label.setText(f"{str(self.remaining_time)}초")

    def click_frame(self, event, name):
        """메뉴 선택하고 선택옵션 창 띄우기"""
        print(f'{name}프레임을 선택했습니다.')
        option_page_df = pd.merge(self.menu_df, self.img_path_df, on='id')
        print(option_page_df.columns)

        #조건설정
        condition1 = (option_page_df['category'] == self.user_clicked_category)
        condition2 = (option_page_df['category_num'] == int(name[11:]))
        # condition3 = (self.menu_df['sold_out'] == 0)

        #조건에 맞는 변수이름에 저장
        sold_out_state = option_page_df.loc[condition1 & condition2, 'sold_out']
        self.send_info = option_page_df.loc[condition1 & condition2]
        print(self.send_info['info'])
        if sold_out_state.sum() > 0:
            msg_box_page = MSG_Dialog(1)
            msg_box_page.show()
            msg_box_page.exec_()
        else:
            print('낫품절')
            self.show_sample_label()
            dialog_page = Option_Class(self)
            dialog_page.setWindowFlags(Qt.WindowStaysOnTopHint)  # Always on top
            dialog_page.setAttribute(Qt.WA_ShowWithoutActivating)  # Prevent dialog from stealing focus
            dialog_page.show()
            # dialog_page.exec_()

    def remove_label(self):
        """선택옵션창 뒤에 검은 화면 숨겨줌"""
        self.sample_label.hide()

    def show_sample_label(self):
        """임시 검은 라벨 띄우기"""
        print('라벨 띄움')
        self.sample_label = QLabel(self)
        self.sample_label.setGeometry(0, 0, 768, 1024)
        self.sample_label.setStyleSheet('background-color: rgba(45,45,45,200);')
        self.sample_label.show()

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

        # self.menu_arrow_btn_num = category_drinks_num % 12 > 0
        print('페이지번호',category_drinks_num // 12)
        print('나머지', category_drinks_num % 12)
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
