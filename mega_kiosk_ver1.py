import os
import sys
import ast
import sqlite3
import datetime
import pandas as pd
from random import randint

from PyQt5 import uic
from PyQt5.QtGui import *

import shopping_cart
from shopping_cart import *
from manager_page import *

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


def resource_path(relative_path):
    """UI 받아오는 함수"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


# UI 불러오기
main_page_class = uic.loadUiType(resource_path('./UI/mega_ui_ver3.ui'))[0] # 메가 메인 UI 불러오기
choose_option_class = uic.loadUiType(resource_path('./UI/mega_choose_option_page.ui'))[0] # 메가 음료옵션창 불러오기
msg_box_class = uic.loadUiType(resource_path('./UI/msg_box.ui'))[0]  # 메세지박스 ui 불러오기
point_page_class = uic.loadUiType(resource_path('./UI/point_page.ui'))[0] # 포인트페이지 창 띄우기
manager_page_class = uic.loadUiType(resource_path('./UI/manager_page.ui'))[0] # 관리자페이지
receipt_page = uic.loadUiType(resource_path('./UI/receipt_page_2.ui'))[0] # 영수증 창
# main_page_ui = resource_path('./UI/mega_ui_ver3.ui')
# choose_option_ui = resource_path('./UI/mega_choose_option_page.ui')
# msg_box_ui = resource_path('./UI/msg_box.ui')
# point_page_ui = resource_path('./UI/point_page.ui')
# manager_page_ui = resource_path('./UI/manager_page.ui')

class Rept(QDialog, receipt_page):
    """영수증"""
    def __init__(self, parent, order_num, t_price):
        super().__init__()
        self.setupUi(self)
        self.parent = parent

        self.order_number_label.setText(str(order_num))
        self.total_price_label.setText(str(t_price))
        self.set_datetime()

        self.parent.fill_the_table_widget(self.tableWidget)


    def set_datetime(self):
        now = datetime.datetime.now()
        formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
        self.date_label.setText(str(formatted_now))


class Point_Page(QDialog, point_page_class):
    """포인트 적립 창"""
    data_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 화면 설정
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)  # 프레임 지우기 / 윈도우가 다른 창 위에 항상 최상위로 유지되도록 함
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 배경 투명하게 함

        # 버튼 모으기
        buttons = self.point_buttons.findChildren(QPushButton)
        for button in buttons:
            button.clicked.connect(self.write_point_num)

        # 버튼 시그널 설정
        self.point_confirm_btn.clicked.connect(self.point_check)  # 확인 버튼
        self.cancel_btn.clicked.connect(self.close)  # x 버튼

    def write_point_num(self):
        """번호를 누르면 번호창에 업데이트 된다"""
        num_list = [str(num) for num in range(0, 10)]  # 버튼은 0부터 010까지 존재함
        num_list.append('010')

        self.user_num = []
        btn_name = self.sender().text()  # 누른 버튼 텍스트 가져옴
        now_label_text = self.user_number_label.text()  # 라벨의 텍스트 가져옴


        if btn_name in num_list:
            now_label_text += str(btn_name)
            self.only_num = now_label_text.replace('-', '')
            self.user_num.append(self.user_num.append(btn_name))
            print('누를때', self.user_num)
            if len(self.only_num) <= 11:
                self.user_number_label.setText(self.mask_numbers(now_label_text))
        else:
            self.user_num = self.user_num[:-1]
            print('지울때', self.user_num)
            now_label_text = now_label_text[:-1]
            self.user_number_label.setText(self.mask_numbers(now_label_text))

    def mask_numbers(self, i):
        i = i.replace('-', '')
        if len(i) <= 3:
            return i
        elif 3 < len(i) < 8:
            return f'{i[:3]}-{(len(i) - 3) * "*"}'
        else:
            return i[:3] + '-****-' + i[7:]

    def point_check(self):
        now_label_text = self.user_number_label.text()  # 라벨의 텍스트 가져옴
        if len(now_label_text) == 11:
            self.data_signal.emit(now_label_text)
            self.close()
        else:
            self.close()
            con = sqlite3.connect('./DATA/data.db')
            df = pd.read_sql('select * from order_table', con)
            df.loc[:, 'customer_id'] = self.user_num
            df.to_sql('order_table', con, if_exists='replace', index=False)
            con.commit()
            con.close()
            print('포인트 적립 확인')


class MSG_Dialog(QDialog, msg_box_class):
    """메세지 박스 다이얼로그"""
    data_signal = pyqtSignal(str)

    def __init__(self, parent, page_data):
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)

        # 화면 설정
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)  # 프레임 지우기 / 윈도우가 다른 창 위에 항상 최상위로 유지되도록 함
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 배경 투명하게 함
        self.sign = page_data
        self.stackedWidget.setCurrentWidget(self.one_btn_page)

        # 버튼 페이지 설정
        if page_data == 1:
            self.info_label.setText("메뉴가 품절이라 선택하실 수 없습니다.")
        elif page_data == 2:
            self.info_label.setText("메뉴를 1개 이상 선택하셔야 합니다.")
        elif page_data == 3:
            self.info_label.setText(f"결제중입니다.. 5초 후에 창이 닫힙니다.")
            self.remain_time = 5
            self.p_timer = QTimer()
            self.p_timer.timeout.connect(self.update_p_timer)
            self.p_timer.setInterval(1000)
            self.p_timer.start()
        elif page_data == 4:
            self.info_label.setText("포인트 적립을 하시겠습니까?")
            self.stackedWidget.setCurrentWidget(self.two_btn_page)
        elif page_data == 5:
            self.info_label.setText("회원정보가 사라집니다. 계속하시겠습니까?")
            self.stackedWidget.setCurrentWidget(self.two_btn_page)
        elif page_data == 6:
            self.info_label.setText("유효한 카드번호가 아닙니다. 다시 입력하세요.")
        elif page_data == 7:
            self.info_label.setText("이미 KT할인이 적용되었습니다.")
        elif page_data == 8:
            self.info_label.setText("영수증 출력을 하시겠습니까?")
            self.stackedWidget.setCurrentWidget(self.two_btn_page)
        else:
            pass

        # 버튼 누르면 정보 넘겨주기
        self.ok_btn.clicked.connect(self.check_and_close)  # 확인 누르면 확인하고 창 닫힘

        self.no_btn.clicked.connect(self.check_no_btn_and_close)  # 취소 누르면 창 닫힘
        self.yes_btn.clicked.connect(self.show_num_keypad)

    def check_and_close(self):
        print('닫기를 탐')
        if self.sign == 8:
            print('영수증 드릴게')

        else:
            self.close()

    def check_no_btn_and_close(self):
        if self.sign == 4:
            print('여기서 오픈 페이지로 바뀝니다. 그리고 데이터 삭제해야 함')
            self.close()
            msg_box_page = MSG_Dialog(self.parent, 8)  # 포인트 창이 뜨고
            msg_box_page.exec_()
        if self.sign == 8:
            self.close()
            self.parent.stackedWidget.setCurrentWidget(self.parent.opening_page)
            self.parent.timer.start()
            self.parent.delete_order_table_values()  # 테이블 내용 삭제
        else:
            self.close()

    def update_p_timer(self):
        self.remain_time -= 1
        if self.remain_time == 0:  # 시간이 종료되면
            self.p_timer.stop()  # 타이머가 멈추고
            self.close()
            self.show_point_msg_box()
        self.info_label.setText(f"결제중입니다.. {self.remain_time}초 후에 창이 닫힙니다.")

    def show_point_msg_box(self):
        msg_box_page = MSG_Dialog(self.parent, 4)  # 포인트 창이 뜨고
        msg_box_page.exec_()

    def show_num_keypad(self):
        """숫자패드 창 띄우기"""
        if not self.sign == 8:
            self.close()
            key_page = Point_Page()
            key_page.data_signal.connect(self.get_label_text)
            key_page.show()
            key_page.exec_()
        else:
            self.parent.order_num += 1 # 주문번호 늘리기
            rept = Rept(self.parent, self.parent.order_num, self.parent.get_total_price() )
            rept.show()
            rept.exec_()
            self.close()
            self.parent.stackedWidget.setCurrentWidget(self.parent.opening_page)
            self.parent.timer.start()
            self.parent.delete_order_table_values()  # 테이블 내용 삭제


    def get_label_text(self, text):
        print('테스트 텍스트 출력=============')
        print(text)


class Option_Class(QDialog, choose_option_class):
    """선택옵션 창"""
    data_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)

        # 화면 설정
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)  # 프레임 지우기 / 윈도우가 다른 창 위에 항상 최상위로 유지되도록 함
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 배경 투명하게 함
        self.move(30, 40)  # 창 이동

        # 가격 이름 메뉴정보 불러오기
        data = parent.send_info
        self.drink_name = data['menu_name_x'].to_string(index=False)
        self.drink_price = data['price'].to_string(index=False)
        self.drink_info = data['info'].to_string(index=False)

        # 정보 담기
        self.menu_photo_label.setPixmap(QPixmap(data['img_path'].to_string(index=False)))  # 메뉴 이미지
        self.menu_name_label.setText(str(self.drink_name))  # 메뉴 이름
        self.menu_info_label.setText(str(self.drink_info))  # 메뉴 정보
        self.menu_price_label.setText(str(self.drink_price) + '원')  # 메뉴 가격

        # 옵션 위한 테이블 생성
        option_df = data.loc[:, 'cinnamon':'zero_cider_changed']
        option_df_dict = option_df.to_dict('list')
        option_df_keys = list(option_df_dict.keys())
        option_df_keys.append('decaffein')
        print(option_df_keys)
        option_df_dict_not_null = {key: [int(x) for x in value[0].split(',')] for key, value in option_df_dict.items()
                                   if value != ['0']}  # 0이 들어가지 않은 인수형의 숫자 반환

        if '디카페인' in self.drink_name:  # 디카페인은 db에서 분리를안해서 후작업
            option_df_dict_not_null['decaffein'] = 1
            del option_df_dict_not_null['strong_or_weak']

        # 음료에 따라 옵션창 띄워주는 부분
        self.option_frame_list = [getattr(self, f'option_frame_{frame}') for frame in range(1, 13)]  # 프레임들을 리스트에 담음

        for idx, key in enumerate(option_df_keys):  # 음료에 맞게 옵션창 띄워줌
            if key in list(option_df_dict_not_null.keys()):
                self.option_frame_list[idx].setVisible(True)  # 음료에 있는 카테고리만 보여주고
            else:
                self.option_frame_list[idx].setVisible(False)  # 나머지는 안보여줌

        # 버튼 한번만 눌리게 체크
        self.btn_duplicates_check()

        # 버튼 누를 때마다 옵션 가격 추가해주는 시그널 연결
        self.option_buttons = self.option_bottom_frame.findChildren(QPushButton)
        for option_btn in self.option_buttons:
            option_btn.clicked.connect(self.set_extra_charge)
            if option_btn.isChecked():
                self.set_extra_charge()

        # 버튼 시그널 연결
        self.cancel_btn.clicked.connect(lambda x: self.close())  # 창 종료하기
        self.cancel_btn.clicked.connect(self.close)  # 창 종료하기
        self.order_btn.clicked.connect(self.order_confirm)
        self.reset_btn.clicked.connect(self.btn_duplicates_check)  # 옵션 초기화 버튼

        # db불러오기
        self.con = sqlite3.connect('./DATA/data.db')  # 데이터베이스 연결 정보 설정

    def set_extra_charge(self):
        """버튼 누를 때마다 옵션 가격 추가해주는 부분"""

        # 옵션 가격 데이터 불러오기
        option_price = pd.read_csv('./DATA/drinks_price.csv')
        option_price_eng_name = option_price['eng_name'].to_list()

        # 눌린 버튼들 확인하기 및 라벨에 업데이트
        add_price = 0
        self.customer_order_option_list = []
        self.customer_order_option_list_kor = []
        self.option_buttons = self.option_bottom_frame.findChildren(QPushButton)

        for btn in self.option_buttons:
            if btn.isChecked() and btn.isVisible():  # 체크된 버튼만 확인
                btn_object_name = btn.objectName()  # 버튼 객체 이름
                idx = option_price_eng_name.index(btn_object_name)  # 버튼의 index확인
                drinks_price = option_price.loc[idx, 'noraml_drink']  # 체크된 옵션 가격 가져오기
                drinks_option_name = option_price.loc[idx, 'eng_name']  # 체크된 옵션 영어 이름 가져오기
                drinks_option_kor_name = option_price.loc[idx, 'kor_name']
                add_price += drinks_price  # 가격 더해주기
                if '안함' not in drinks_option_kor_name:
                    self.customer_order_option_list_kor.append(drinks_option_kor_name)
                self.customer_order_option_list.append(drinks_option_name)

        # 상단에 값 추가
        self.update_drink_price = str(int(self.drink_price) + int(add_price))
        self.menu_price_label.setText(self.update_drink_price + '원')
        if len(self.customer_order_option_list_kor) != 0:
            self.choose_option_label.setText(str(', '.join(self.customer_order_option_list_kor)))
        else:
            self.choose_option_label.setText('없음')

    def btn_duplicates_check(self):
        """각 옵션창 프레임 내에 있는 버튼들 한번만 눌리게"""

        # 버튼 그룹 담아주기
        self.option_button_groups = []

        # 프레임들 안에 있는 버튼들을 각각 버튼 그룹으로 담아줌
        for i in range(1, 13):
            option_frame = self.option_frame_list[i - 1]
            buttons = option_frame.findChildren(QPushButton)
            button_group = QButtonGroup()
            button_group.setExclusive(True)

            for btn in buttons:
                button_group.addButton(btn)
            button_group.buttonClicked.connect(self.btn_check)  # 중복버튼 누르기 방지
            button_group.buttonClicked.connect(self.btn_clicked_style)  # 버튼 색 바뀌게 하기
            self.option_button_groups.append(button_group)

        # 각 옵션 선택창 안에 들어있는 1번 버튼 눌리게 하기
        for btn_group in self.option_button_groups:
            btn_group.buttons()[0].click()  # 첫번째 버튼 무조건 눌리게

    def btn_clicked_style(self, btn):
        """선택한 옵션버튼 색 바꿔줌"""
        for btn_group in self.option_button_groups:
            if btn in btn_group.buttons():
                for button in btn_group.buttons():
                    button.setStyleSheet('')
        btn.setStyleSheet('border: 3px solid rgb(229, 79, 65);')

    def btn_check(self):
        """버튼 그룹 가져와서 체크하는 부분"""
        sender = self.sender()  # 버튼 모두를 가져옴
        for button_group in self.option_button_groups:
            if sender not in button_group.buttons():
                button_group.setExclusive(True)

    def close(self):
        self.parent.remove_label()
        self.accept()

    def order_confirm(self):
        """선택옵션 확인 후 db에 저장"""

        self.parent.drink_num += 1  # 주문 수량 늘려줌
        option_str = str(self.customer_order_option_list)  # 리스트 str형태로 바꿔주기
        cur = self.con.cursor()  # 커서 생성
        cur.execute("INSERT INTO order_table (id, drink_cnt, order_drink, price, custom_option)"
                    "VALUES(?,?,?,?,?);",  # SQL 쿼리 실행
                    (self.parent.drink_num, 1, self.drink_name, self.update_drink_price, option_str))
        self.con.commit()  # 변경사항 저장

        # 장바구니 리스트위젯에 값 넣어주기
        add_shopping_item_to_listwidget(
            self.parent.drinks_cart_list_widget, str(self.parent.drink_num),
            self.drink_name, self.update_drink_price, self.parent.menu_cnt_label, self.parent.payment_admit_btn)

        # 메뉴 갯수 라벨에 넣어주기(담은 메뉴 수 라벨)
        cur.execute('SELECT SUM(drink_cnt) FROM order_table')  # 테이블에 있는 메뉴 수 세서
        result = cur.fetchone()[0]  # 이를 튜플 형태로 가져오고 첫번째 값만 가져옴
        self.parent.menu_cnt_label.setText(str(result) + '개')

        order_df = pd.read_sql('select * from order_table', self.con)
        order_df['drink_cnt'] = order_df['drink_cnt'].astype(int)
        order_df['price'] = order_df['price'].astype(int)
        total_price = (order_df['drink_cnt'] * order_df['price']).sum()
        self.parent.payment_admit_btn.setText(f'  {str(total_price)}원\n  결제하기')

        cur.close()  # 연결 종료
        self.con.close()
        # 선택옵션 창 종료
        self.parent.remove_label()
        self.accept()
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

        # 오픈화면 #######################################################################################################
        self.stackedWidget.setCurrentIndex(0)  # 시작할때 화면은 오픈 페이지로 설정
        self.set_ad_image()  # 이미지 변경
        self.setWindowFlags(Qt.FramelessWindowHint) # 프레임 지우기
        self.move(10,30) #창이동

        # 페이지 이동 및 타이머 시작
        self.ad_label.mousePressEvent = lambda event: (self.stackedWidget.setCurrentWidget(self.main_page))  # 페이지 이동)

        # 메인화면 시작 ##################################################################################################

        # 0. DB 불러오기
        con = sqlite3.connect('./DATA/data.db')
        self.price_df = pd.read_sql('select * from drinks_price', con)  # 가격 테이블
        self.menu_df = pd.read_sql('select * from drinks_menu', con)  # 음료상세정보 전체 테이블
        self.img_path_df = pd.read_sql('select * from drinks_img_path', con)  # 음료 이미지 경로 테이블
        self.order_table_df = pd.read_sql('select * from order_table', con)  #
        self.drink_num = 0  # 음료 주문번호
        self.order_num = 100 # 고객 주문번호 100부터 시작

        # 1. 타이머
        # 타이머 기본 설정값
        self.DURATION_INT = 120
        self.remaining_time = self.DURATION_INT

        # # 타이머와 관련된 변수들
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.setInterval(1000)

        # 2. 카테고리 버튼 이동
        self.category_stackedWidget.setCurrentWidget(self.category_1)  # 기본값
        self.category_btn_list = [getattr(self, f"category_btn_{i}") for i in range(1, 16)]  # 카테고리 버튼 리스트화
        for btn in self.category_btn_list:
            btn.clicked.connect(self.set_categroy_num)  # 카테고리 하단 메뉴 크기 설정
            btn.clicked.connect(self.change_categroy_btn_color)  # 버튼 색 바꾸기
            btn.clicked.connect(self.show_menu_arrow_btn)  # 카테고리 하단 메뉴 크기 설정
            btn.clicked.connect(lambda: self.menu_stackedWidget.setCurrentWidget(self.page_1))  # 음료 페이지 1페이지로 초기화
            btn.clicked.connect(
                lambda x, category=btn: self.start_timer(btn))  # 카테고리 버튼 누를 때마다 타이머 초기화

        # 3. 카테고리 페이지 넘기기 (메인화면 페이지 넘기기)
        self.category_right_btn.clicked.connect(lambda: self.check_current_page(1))
        self.category_right_btn_2.clicked.connect(lambda: self.check_current_page(2))
        self.category_left_btn.clicked.connect(lambda: self.check_current_page(1))
        self.category_left_btn_2.clicked.connect(lambda: self.check_current_page(2))

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

        # 6. 버튼 시그널 연결
        self.all_remove_label.clicked.connect(self.delete_order_table_values)  # 전체 삭제 버튼
        self.home_button.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.opening_page))  # 홈 버튼 누르면 오픈화면으로 이동

        # 7. 관리자페이지
        self.logo_label.mousePressEvent = lambda event: self.open_manager_page()
        self.manager_page_num = 0

        # 99. 스타일시트 관련된 부분
        # 가격 폰트 변경
        self.menu_price_label_list = [getattr(self, f"menu_price_label_{i}") for i in range(1, 25)]  # 가격 폰트 리스트
        for label in self.menu_price_label_list:
            label.setStyleSheet('color: rgb(229, 79, 64);font: 63 12pt "Pretendard SemiBold";')

        # 주문확인화면 시작 ############################################################################################

        # 1. 주문확인창 시작 및 테이블위젯 채우기
        self.payment_admit_btn.clicked.connect(self.move_to_order_check_page)

        # 2. 버튼 시그널 연결 모음
        self.cancel_btn_2.clicked.connect(self.timer_restart_and_go_to_main_page)
        self.back_to_main_page_btn.clicked.connect(self.timer_restart_and_go_to_main_page)
        self.eat_here_btn.clicked.connect(lambda: self.move_to_payment_choose('for_here'))
        self.take_out_btn.clicked.connect(lambda: self.move_to_payment_choose('to_go'))


        # 결제수단선택창 ############################################################################################

        # 버튼 시그널 연결
        self.payment_choose_signal()
        self.cancel_btn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.order_check_page))  # x 버튼 누르면 주문확인창으로 이동
        self.kt_discount = False

        # 카드 / 큐알코드 결제창 ######################################################################################

        ### 1. 카드 결제창

        # 버튼 클릭 이벤트

        self.cancel_btn_3.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.payment_choose_page))  # x 버튼 누르면 결제선택수단창으로 이동
        self.cancel_btn_4.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.payment_choose_page))  # 취소  버튼 누르면 결제선택수단창으로 이동
        self.card_img_frame.mousePressEvent = lambda event: self.mobile_pay_msgbox()
        self.barcode_type = None
        ### 2. 큐알코드 결제창
        # self.qr_check_frame.mousePressEvent = lambda event: self.fill_the_table_widget()
        # self.check_coupon_num.clicked.connect(self.) # 쿠폰 조회버튼
        self.use_coupon.clicked.connect(self.askRcpt)  # 쿠폰사용버튼 -> 영수증 물어보는 함수로 이동 및 종료

        self.cancel_btn_5.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.payment_choose_page))  # x 버튼 누르면 결제선택수단창으로 이동
        self.order_btn_2.clicked.connect(self.check_discount_and_move)  # 할인 적용하고 이동

        # 숫자 키보드 버튼 누를때 이벤트 발생
        keyboard_buttons = self.keyboard_frame.findChildren(QPushButton)
        for btn in keyboard_buttons:
            btn.clicked.connect(self.change_card_num)

        # 기타 스타일시트 변경 부분 ###############################################################################
        # 큐알코드 커서 변경해주기
        self.qr_check_frame.setCursor(QCursor(QPixmap('./img/qt자료/bacord').scaled(80, 80)))
        self.card_label.setCursor(QCursor(QPixmap('./img/qt자료/payment_phone.png').scaled(120, 100)))
        self.horizontalSlider.setCursor(QCursor(QPixmap('./img/qt자료/matercard.png').scaled(80, 70)))

    ## 함수 시작 #######################################################################################################
    '''결제창 관련 함수'''

    def askRcpt(self):
        """영수증 물어보는 함수로 이동"""

        # 만약 결제 전이라면 이동하지 않음
        try:
            card_num = self.table_widget_qr_code.item(0, 0).text()
        except AttributeError:
            card_num = ''

        if len(card_num) > 0:
            msg_box_page = MSG_Dialog(self, 8)
            msg_box_page.exec_()

    def check_discount_and_move(self):
        d_price = self.get_discount_price()  # 할인금액
        t_price = self.get_total_price()  # 총 금액
        self.r_price = t_price - d_price  # 총금액 - 할인금액 = 사용자의결제금액
        self.total_payment_price.setText(f'  주문금액: {str(t_price)}원 - 할인금액:{str(d_price)}원')
        self.total_payment_price_2.setText(f'  결제금액: {str(self.r_price)}원')
        self.payment_choose_title_bar.setText(f'    결제수단 선택({str(self.r_price)})원')
        self.stackedWidget.setCurrentWidget(self.payment_choose_page)

    def mobile_pay_msgbox(self):
        """모바일 페이 메세지박스 띄우기"""
        msg_box_page = MSG_Dialog(self, 3)
        msg_box_page.exec_()

    def set_table_widget(self, tablewidget, row, column, labels):
        """큐알코드 테이블 위젯 값 설정하기"""
        self.table_widget_qr_code.setRowCount(row)  # 행 갯수 설정
        self.table_widget_qr_code.setColumnCount(column)  # 열 갯수 설정
        self.table_widget_qr_code.setVerticalHeaderLabels(labels)  # 행 제목 설정
        self.table_widget_qr_code.horizontalHeader().setVisible(False)  # 열 헤더 숨기기
        self.table_widget_qr_code.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if self.barcode_type == 'qr_payment':
            print(self.get_total_price())
            print(self.get_discount_price())
            self.table_widget_qr_code.setItem(4, 0, QtWidgets.QTableWidgetItem(
                f"{str(int(self.get_total_price()) -self.get_discount_price())}원"))

    def change_card_num(self):
        """큐알코드 선택창에서 키패드 번호 입력"""

        # 사용자가 누른 키패드 번호 받아옴
        sender_name = self.sender().text()
        print('사용자가 누른 번호', sender_name)
        if self.barcode_type == 'kt_discount':
            card_num_row = 3
        if self.barcode_type == 'qr_payment':
            card_num_row = 2
        else:
            card_num_row = 1

        self.insert_value_in_tablewidget(self.table_widget_qr_code, sender_name, card_num_row)

    def insert_value_in_tablewidget(self, tablewidget, sender_obj, card_row):

        # 키패드 번호 리스트에 저장
        keypad_numbers = [str(num) for num in range(10)]
        keypad_numbers.extend(['00', '000'])

        # 현재 테이블위젯에 있는 카드번호
        try:
            card_num = tablewidget.item(card_row, 0).text()
        except AttributeError:
            card_num = ''
        string = (card_num + sender_obj).replace('-', '')
        print('카드번호는', card_num)

        # 테이블 위젯에 조건에 따라 값 넣어줌
        if sender_obj in keypad_numbers and len(string) <= 16:  # 키패드 리스트에 값이 있다면(0~9, 00, 000)
            string = (card_num + sender_obj).replace('-', '')
            divided_4_letter = '-'.join([string[i:i + 4] for i in range(0, len(string), 4)])
            tablewidget.setItem(card_row, 0, QtWidgets.QTableWidgetItem(divided_4_letter))  # 카드 번호 위치에 값 넣어줌
            # tablewidget.item(card_row, 0).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 값 오른쪽 정렬
        elif sender_obj == 'clear':
            tablewidget.setItem(card_row, 0, QtWidgets.QTableWidgetItem(''))  # clear 되었을 때 값 넣어주기
        elif sender_obj == '승인':
            if card_num.replace('-', '') == '1111222233334444':
                if self.barcode_type == 'kt_discount':
                    kt_info = ['KT할인', '특정할인', '20230601 ~ 20230930', card_num, str(self.get_total_price()) + '원',
                               str(self.get_discount_price()) + '원']
                    self.set_number_in_qr_payment_table(6, kt_info)
                if self.barcode_type == 'qr_payment':
                    coupon_info = [str(self.get_total_price() - self.get_discount_price()) + '원', str(randint(1, 3)), card_num]
                    self.set_number_in_qr_payment_table(3, coupon_info)
            else:
                msg_box_page = MSG_Dialog(self, 6)  # 유효한 카드번호가 아닙니다. 다시 입력하세요.
                msg_box_page.exec_()
        elif sender_obj == '←':
            card_num = card_num[:-1]
            tablewidget.setItem(card_row, 0, QtWidgets.QTableWidgetItem(card_num))  # 하나 줄여서 값 넣어주기
            tablewidget.item(card_row, 0).setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)  # 값 오른쪽 정렬
        else:
            pass

    def set_number_in_qr_payment_table(self, num, value):
        """qr/바코드 창에 값 넣어줌"""
        print('바코드 창 탑니다..')
        nums = [n for n in range(num)]
        for i in nums:
            self.table_widget_qr_code.setItem(nums[i], 0, QtWidgets.QTableWidgetItem(value[i]))

    def get_discount_price(self):
        """할인된 금액 리턴"""
        con = sqlite3.connect('./DATA/data.db')
        order_df = pd.read_sql('select * from order_table', con)
        if self.barcode_type == 'kt_discount':
            order_df.loc[0, 'discount_price'] = 1900

        order_df.to_sql('order_table', con, if_exists='replace', index=False)
        con.commit()
        con.close()
        discount_p = order_df.loc[0, 'discount_price']
        if discount_p == None:
            discount_p = 0

        return discount_p

    '''결제수단 선택창 관련 함수'''


    def payment_choose_signal(self):
        """결제수단 버튼에 따라 다른 정보 전달"""
        payment_btn_df = pd.read_csv('./DATA/payment_choose.csv')  # csv 값 가져오기(결제버튼 정보)
        payment_choose_buttons = self.payment_choose_main_widget.findChildren(QPushButton)  # 결제창에 있는 모든 버튼 가져오기
        for btn in payment_choose_buttons:
            con1 = payment_btn_df['btn_name'] == btn.objectName()  # 버튼객체이름과 같은 버튼이라는 조건에 맞다면
            crs_btn = payment_btn_df.loc[con1, ['kor_name', 'type']].to_dict('list')  # 버튼 이름과 결제형태 딕셔너리 형식으로 가져오기
            btn.clicked.connect(
                lambda x, y=crs_btn['kor_name'][0], z=crs_btn['type'][0]: self.move_to_payment_page(y, z))

    def move_to_payment_page(self, name, type):
        """전달해준 정보에 따라 다른 결제창 불러오기"""
        print('타입', type)
        print('kt할인여부', self.kt_discount)

        # 카드 결제창 이동
        if type == 1:  # 카드
            self.payment_card_title_bar.setText("  " + name)
            self.stackedWidget.setCurrentWidget(self.charge_page)
            self.update_card_payment_table()

        elif type == 2 or (type == 3 and not self.kt_discount) or type == 4:  # qr/바코드 창으로 이동
            self.move_to_payment_page_for_qr(name, type)
        else:
            msg_box_page = MSG_Dialog(self, 7)
            msg_box_page.exec_()

    def move_to_payment_page_for_qr(self, name, type):
        """선택한 버튼에 따라 맞는 결제창으로 이동"""
        self.table_widget_qr_code.clearContents()  # 테이블 위젯 지우기
        self.table_widget_qr_code.setRowCount(0)

        if type == 2:  # 쿠폰 조회창
            self.qr_check_btns_stackwidget.setCurrentWidget(self.coupon_check_btn)
            lab = ['쿠폰번호', '쿠폰명칭', '잔여금액', '받을금액', '결제금액']
            self.barcode_type = 'coupon_payment'

        if type == 4:  # qr/바코드 결제창 이동
            self.qr_check_btns_stackwidget.setCurrentWidget(self.coupon_check_btn)
            lab = ['총 결제금액', '할부개월', '카드번호']
            self.barcode_type = 'qr_payment'

        else:  # kt 할인창 이동
            self.qr_check_btns_stackwidget.setCurrentWidget(self.kt_check_btn)
            lab = ['제휴사명', '할인종료', '유효기간', '카드번호', '대상금액', '할인금액']
            self.barcode_type = 'kt_discount'
            self.kt_discount = True

        self.set_table_widget(self.table_widget_qr_code, len(lab), 1, lab)  # 테이블에 값 넣어주기
        self.barcord_payment_title_bar.setText("  " + name)  # 창 상단의 이름 바꾸기
        self.stackedWidget.setCurrentWidget(self.barcod_payment_page)  # qr/바코드 페이지로 이동

    def get_total_price(self):
        """총 가격 계산 및 반환"""
        con = sqlite3.connect('./DATA/data.db')
        order_table_df = pd.read_sql('select * from order_table', con)

        # 총 가격 계산
        order_table_df['drink_cnt'] = order_table_df['drink_cnt'].astype(int)
        order_table_df['price'] = order_table_df['price'].astype(int)
        total_price = (order_table_df['drink_cnt'] * order_table_df['price']).sum()
        return total_price

    def get_total_cnt(self):
        """총 갯수 계산 및 반환"""
        con = sqlite3.connect('./DATA/data.db')
        order_table_df = pd.read_sql('select * from order_table', con)
        total_count = order_table_df['drink_cnt'].sum()
        return total_count

    def update_card_payment_table(self):
        """카드 결제창 테이블 위젯 값 업데이트"""
        total_price = self.get_total_price()  # 총 가격
        discount_price = self.get_discount_price()
        f_price = total_price - discount_price

        # 카드번호 랜덤으로 만들어줄것
        card_num = self.make_random_card_num()

        # 카드 테이블에 값 업데이트 해주기
        self.card_payment_table_widget.setRowCount(3)
        self.card_payment_table_widget.setColumnCount(1)
        self.card_payment_table_widget.horizontalHeader().setVisible(False)  # 열 헤더를 숨깁니다.
        self.card_payment_table_widget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(f_price) + '원'))
        self.card_payment_table_widget.setItem(1, 0, QtWidgets.QTableWidgetItem('0개월'))
        self.card_payment_table_widget.setItem(2, 0, QtWidgets.QTableWidgetItem(card_num))
        self.card_payment_table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 열 너비를 조정합니다.

    def make_random_card_num(self):
        """카드 번호 랜덤으로 만들어주기"""
        random_card_num = [str(randint(1000, 9999)) for _ in range(4)]
        random_card_num_for_print = ' '.join(random_card_num)
        mask_card_num = "*" * (len(random_card_num_for_print) - 4) + random_card_num_for_print[-4:]
        return mask_card_num

    '''주문 확인창 관련 함수'''
    def insert_img_for_recommend(self):
        """추천 디저트 메뉴 5개 넣음"""
        menu_and_price_join_df = pd.merge(self.menu_df, self.img_path_df, on='id')  # 조인
        con1 = (menu_and_price_join_df['category'] == '디저트')


    def move_to_payment_choose(self, state):
        """포장/매장 선택하는 것 db에 저장해주기"""
        con = sqlite3.connect('./DATA/data.db')
        order_table_df = pd.read_sql('select * from order_table', con)
        order_table_df.loc[:, 'for_here_or_to_go'] = state
        order_table_df.to_sql('order_table', con, if_exists='replace', index=False)
        con.commit()
        con.close()
        self.stackedWidget.setCurrentWidget(self.payment_choose_page)

    def timer_restart_and_go_to_main_page(self):
        """타이머 재시작 및 메인 페이지로 이동"""
        self.timer.start()
        self.stackedWidget.setCurrentWidget(self.main_page)

    def fill_the_table_widget(self, table):
        """테이블 위젯 채우기"""
        # 업데이트한 db불러오기
        con = sqlite3.connect('./DATA/data.db')
        order_table_df = pd.read_sql('select * from order_table', con)
        price_df = pd.read_csv('./DATA/drinks_price.csv')  # 가격 csv 도 불러오기(한글이름으로 비교)

        # 테이블위젯 행 값 계산
        row = order_table_df['id'].count()
        table.setRowCount(row)  # 행값 적용

        # 옵션 값 딕셔너리 화 하기
        order_table_dict = pd.DataFrame(order_table_df).to_dict()

        # 테이블위젯 값 생성하고 넣기
        for idx in range(row):
            # 테이블위젯 값 생성
            drink_option_df = order_table_df.loc[idx, 'custom_option']  # 각 행의 옵션을 가져와서
            drink_option_list = ast.literal_eval(drink_option_df)  # 문자열로 되어 있는 리스트들을 리스트처럼 만들어줌
            option_choices_no_choice = [price_df[price_df['eng_name'] == i]['kor_name'].to_string(index=False)
                                        # 그리고 not choice가 써져 있지 않은 값들을 리스트에 넣어줌
                                        for i in drink_option_list if 'no_choice' not in i]

            # 값 넣기
            items = [QTableWidgetItem(str(order_table_dict[col][idx])) for col in ['order_drink', 'drink_cnt', 'price']]
            items.append(QTableWidgetItem(','.join(option_choices_no_choice)))

            # 테이블 위젯 가운데로 정렬
            for item in items:
                item.setTextAlignment(Qt.AlignCenter)  # Qt.AlignHCenter 가운데로 정렬

            # 테이블위젯에 값 넣기
            for col, item in enumerate(items):
                table.setItem(idx, col, item)

        # 테이블위젯 열 길이 헤더 크기만큼 정렬해주기
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

    def move_to_order_check_page(self):
        """주문확인창"""
        # 타이머 중단
        self.timer.stop()

        # 현재 db 연결
        con = sqlite3.connect('./DATA/data.db')
        order_table_df = pd.read_sql('select * from order_table', con)

        total_price = self.get_total_price()  # 총 가격 계산
        total_count = order_table_df['drink_cnt'].sum()  # 총 갯수 계산
        discount_price = order_table_df['discount_price'].sum()  # 할인금 계산

        # 라벨 및 버튼에 넣어주기
        self.total_price_for_check_page.setText(str(total_price) + '원')
        self.payment_choose_title_bar.setText(f'  결제수단 선택({str(int(total_price) - int(discount_price))}원)')  # 이건 결제수단 선택창임
        self.total_payment_price.setText(f'  주문금액: {str(total_price)}원 - 할인금액:{str(discount_price)}원')  # 이건 결제수단 선택창임
        self.total_payment_price_2.setText(f'  결제금액: {str(total_price)}원')  # 이건 결제수단 선택창임
        self.total_cnt_for_check_page.setText(str(total_count) + '개')

        # 총 갯수가 0 초과하면 창 넘어가기
        if total_count > 0:
            self.stackedWidget.setCurrentWidget(self.order_check_page)  # 주문 확인 창으로 이동
            self.fill_the_table_widget(self.tableWidget_menu_check)  # 테이블위젯 값 채우기
            self.fill_the_table_widget(self.tableWidget_menu_2_for_qr)  # 일단 여기에 넣음 @@@@@@@@@@@@@@@@@@@ 수정필요
        else:
            msg_box_page = MSG_Dialog(self, 2)  # 1보다 작으면 메세지 창 띄우기
            msg_box_page.exec_()

    '''메인창 관련 함수'''

    def open_manager_page(self):
        """관리자 페이지 열기"""
        self.manager_page_num += 1
        if self.manager_page_num == 5:
            self.manager_page_num = 0
            manager_page = Manager_Page()
            manager_page.show()
            manager_page.exec_()
            # sell_c = manager_page.MenuWidget.check_btn_sell()
            # sold_c = manager_page.MenuWidget.check_btn_sold_out()
            # print('판매', sell_c, '판매된', sold_c)
            self.stackedWidget.setCurrentWidget(self.opening_page)

    def check_current_page(self, num):
        if num == 1:
            self.category_stackedWidget.setCurrentWidget(self.category_2)
            self.category_btn_11.click()
        elif num == 2:
            self.category_stackedWidget.setCurrentWidget(self.category_1)
            self.category_btn_1.click()
        self.menu_stackedWidget.setCurrentWidget(self.page_1)

    def delete_order_table_values(self):
        """ 주문 값 삭제"""

        # 리스트 위젯 값 삭제
        self.drinks_cart_list_widget.clear()

        conn = sqlite3.connect('./DATA/data.db')  # 데이터베이스 연결 정보 설정
        cur = conn.cursor()  # 커서 생성
        cur.execute("DELETE FROM 'order_table'")  # SQL 쿼리 실행

        cur.execute("SELECT SUM(drink_cnt) FROM 'order_table'")
        # cursor.execute('SELECT SUM(column_name) FROM table_name')
        result = cur.fetchone()[0]
        if result == None:
            result = 0
        self.menu_cnt_label.setText(str(result) + '개')

        order_df = pd.read_sql('select * from order_table', conn)
        order_df['drink_cnt'] = order_df['drink_cnt'].astype(int)
        order_df['price'] = order_df['price'].astype(int)
        total_price = (order_df['drink_cnt'] * order_df['price']).sum()
        self.payment_admit_btn.setText(f'  {str(total_price)}원\n  결제하기')

        conn.commit()  # 변경사항 저장
        cur.close()  # 연결 종료
        conn.close()

    def start_timer(self, category):
        """타이머 시작하는 함수"""
        self.timer.stop()
        self.remaining_time = self.DURATION_INT
        self.timer.start()

    def update_timer(self):
        """타이머 시간 업데이트"""
        if self.stackedWidget.currentWidget() == self.main_page:  # 메인페이지에서만 구동함
            self.remaining_time -= 1
            if self.remaining_time == 0:
                self.remaining_time = self.DURATION_INT
                self.stackedWidget.setCurrentWidget(self.main_page)
            self.timer_label.setText(f"{str(self.remaining_time)}초")
        else:
            pass

    def click_frame(self, event, name):
        """메뉴 선택하고 선택옵션 창 띄우기"""
        # print(f'{name}프레임을 선택했습니다.')
        option_page_df = pd.merge(self.menu_df, self.img_path_df, on='id')
        print(option_page_df.columns)

        # 조건설정
        condition1 = (option_page_df['category'] == self.user_clicked_category)
        condition2 = (option_page_df['category_num'] == int(name[11:]))

        # 조건에 맞는 변수이름에 저장
        sold_out_state = option_page_df.loc[condition1 & condition2, 'sold_out']
        self.send_info = option_page_df.loc[condition1 & condition2]
        print(self.send_info['info'])
        if sold_out_state.sum() > 0:
            msg_box_page = MSG_Dialog(self, 1)
            # msg_box_page.show()
            msg_box_page.exec_()
        else:
            # print('낫품절')
            self.show_sample_label()
            dialog_page = Option_Class(self)
            dialog_page.show()

    def remove_label(self):
        """선택옵션창 뒤에 검은 화면 숨겨줌"""
        self.sample_label.hide()

    def show_sample_label(self):
        """임시 검은 라벨 띄우기"""
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

        # 값 초기화
        self.connn = sqlite3.connect('./DATA/data.db')
        self.menu_df = pd.read_sql('select * from drinks_menu', self.connn)  # 음료상세정보 전체 테이블

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
        self.connn.close()
        # self.menu_arrow_btn_num = category_drinks_num % 12 > 0
        print('페이지번호', category_drinks_num // 12)
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

    '''오프닝 페이지 관련 함수'''

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
