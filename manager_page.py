import os
import sys

from PyQt5.QtWidgets import *
from PyQt5 import uic

import sqlite3
import pandas as pd


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('./UI/manager_page.ui')
form_class = uic.loadUiType(form)[0]
form_2 = resource_path('./UI/menu_widget.ui')
form_class_2 = uic.loadUiType(form_2)[0]

class Manager_Page(QDialog, form_class):
    def __init__(self):
        super( ).__init__( )
        self.setupUi(self)



        btn_list = self.stackedWidget.findChildren(QPushButton)
        self.category_btn_list = [btn for btn in btn_list if 'left' not in btn.objectName() and 'right' not in btn.objectName()]
        arrow_list = [a for a in btn_list if a not in self.category_btn_list]

        # 버튼 시그널 연결
        for c_btn in self.category_btn_list:
            c_btn.clicked.connect(self.make_list_for_category)
        for arrow in arrow_list:
            arrow.clicked.connect(self.move_stacked_widget)
        self.cancel_btn.clicked.connect(self.close)

        # 기본 화면 구성
        self.pushButton_2.click()
        self.stackedWidget_2.setCurrentWidget(self.password_page)

        # 관리자 버튼 입력
        p_btn_list = self.point_buttons.findChildren(QPushButton)
        for p_btn in p_btn_list:
            p_btn.clicked.connect(self.write_point_num)
        self.manager_page_check.clicked.connect(self.check_manager_password)

    def check_manager_password(self):
        """관리자인지 확인하고 페이지 넘기기"""
        if self.manager_num_label.text() == '1234':
            self.stackedWidget_2.setCurrentWidget(self.menu_manage_page)
        else:
            self.manager_num_label.setText('관리자 비밀번호가 아닙니다.')

    def write_point_num(self):
        """번호를 누르면 번호창에 업데이트 된다"""
        num_list = [str(num) for num in range(0, 10)]  # 버튼은 0부터 010까지 존재함

        btn_name = self.sender().text()  # 누른 버튼 텍스트 가져옴
        now_label_text = self.manager_num_label.text()  # 라벨의 텍스트 가져옴

        if btn_name in num_list:
            now_label_text += str(btn_name)
            self.manager_num_label.setText(now_label_text)
        elif btn_name =='clear':
            self.manager_num_label.setText('')
        else:
            now_label_text = now_label_text[:-1]
            self.manager_num_label.setText(now_label_text)

    def move_stacked_widget(self):
        """버튼에 따라 카테고리 스택위젯 넘기기"""
        arrow_btn_obj = self.sender().objectName()
        current_index = self.stackedWidget.currentIndex()
        if 'right' in arrow_btn_obj:
            self.stackedWidget.setCurrentIndex(current_index + 1)
        else:
            self.stackedWidget.setCurrentIndex(current_index - 1)


    def make_list_for_category(self):
        """누른 카데고리에 따라 품절여부 보여주기"""

        # 위젯 모두 불러오고 숨겨주기
        widget_list = self.widget.findChildren(QWidget)
        for i in widget_list:
            i.setVisible(False)

        # 버튼 스타일시트 변경해줌(초기화)
        for btn in self.category_btn_list:
            btn.setStyleSheet('')

        # 누른 버튼만 스타일 바꿔주기
        btn_ = self.sender()
        btn_.setStyleSheet('''
        background-color: rgb(45,45,45);
        color:white;
        border-top-left-radius: 10px; 
        border-top-right-radius: 10px;
        ''')

        # db연결
        con = sqlite3.connect('./DATA/data.db')
        self.menu_df = pd.read_sql('select * from drinks_menu', con)  # 음료상세정보 전체 테이블
        condition = self.menu_df.loc[self.menu_df['category']== btn_.text()]
        menu_list = condition[['menu_name', 'sold_out']].values.tolist()

        for index, menu_name in enumerate(menu_list):
            self.initialize_widget(menu_name[0], menu_name[1], index)

    def initialize_widget(self, menu_name, sold_out, index):
        if self.widget.layout() is None:
            v_layout = QVBoxLayout(self)
            self.widget.setLayout(v_layout)
        v_layout = self.widget.layout()
        v_layout.addWidget(MenuWidget(self, menu_name, sold_out, index))

class MenuWidget(QWidget, form_class_2):
    def __init__(self, parent, menu_name, sold_out, row):
        super( ).__init__( )
        self.setupUi(self)
        self.parent = parent
        # self.setStyleSheet(self.styleSheet()+self.parent.styleSheet())
        self.label.setText(menu_name)
        self.label.setStyleSheet('background-color: #F3F3F3')
        self.pushButton.setText('판매')
        self.pushButton_2.setText('품절')


        ''' 스타일시트'''
        self.sold_out_y = '''
            color: rgb(229, 79, 64);
            border: 2px solid rgb(229, 79, 64);
            border-radius: 10px; 
            font: 63 12pt "Pretendard SemiBold";

            '''

        self.sold_out_n = '''
            border: 2px solid rgb(229, 79, 64);
            border: 2px solid  black;
            border-radius:10px;
            font: 63 12pt "Pretendard SemiBold";
        '''

        if sold_out == 1:
            self.set_stylesheet_btn(self.pushButton, self.sold_out_n)
            self.set_stylesheet_btn(self.pushButton_2, self.sold_out_y)
        if sold_out == 0:
            self.set_stylesheet_btn(self.pushButton, self.sold_out_y)
            self.set_stylesheet_btn(self.pushButton_2, self.sold_out_n)

        self.row_index = row

        self.pushButton.clicked.connect(self.check_btn_sell)
        self.pushButton_2.clicked.connect(self.check_btn_sold_out)


    def set_stylesheet_btn(self, btn, style):
        btn.setStyleSheet(style)

    def check_btn_sell(self):

        con = sqlite3.connect('./DATA/data.db')
        menu_df = pd.read_sql('select * from drinks_menu', con)  # 음료상세정보 전체 테이블

        condition = menu_df.loc[menu_df['menu_name'] == self.label.text()]
        menu_list = condition[['menu_name', 'sold_out']].values.tolist()
        print(menu_list[0][0], menu_list[0][1])
        if menu_list[0][1] == 0:
            self.show_msgbox('이미 판매중인 상품입니다.')
        else:
            self.show_msgbox('판매로 상품을 전환합니다.')
            update_query = f"UPDATE drinks_menu SET sold_out = 0 WHERE menu_name='{menu_list[0][0]}'"
            con.execute(update_query)
            con.commit()
            con.close()
            self.set_stylesheet_btn(self.pushButton, self.sold_out_y)
            self.set_stylesheet_btn(self.pushButton_2, self.sold_out_n)
            return self.label.text()

    def check_btn_sold_out(self):

        con = sqlite3.connect('./DATA/data.db')
        menu_df = pd.read_sql('select * from drinks_menu', con)  # 음료상세정보 전체 테이블

        condition = menu_df.loc[menu_df['menu_name'] == self.label.text()]
        menu_list = condition[['menu_name', 'sold_out']].values.tolist()
        print(menu_list[0][0], menu_list[0][1])
        if menu_list[0][1] == 1:
            self.show_msgbox('이미 품절중인 상품입니다.')
        else:
            self.show_msgbox('품절로 상품을 전환합니다.')
            update_query = f"UPDATE drinks_menu SET sold_out = 1 WHERE menu_name='{menu_list[0][0]}'"
            con.execute(update_query)
            con.commit()
            self.set_stylesheet_btn(self.pushButton, self.sold_out_n)
            self.set_stylesheet_btn(self.pushButton_2, self.sold_out_y)
            con.close()
        return self.label.text()

    def show_msgbox(self, text):
        msgbox = QMessageBox()
        msgbox.setText(text)
        msgbox.show()
        msgbox.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWindow = Manager_Page( )
    myWindow.show( )
    app.exec_( )