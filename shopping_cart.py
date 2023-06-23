from PyQt5.QtWidgets import *  # QApplication, QVBoxLayout, QListWidgetItem, QListWidget, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
import sqlite3


# from mega_kiosk_ver1 import WindowClass


class ShoppingItemWidget(QWidget):
    def __init__(self, idx, name, price, list_widget, label, btn):
        super().__init__()

        # 이미지 불러오기
        plus_btn_img = QPixmap('./img/qt자료/plus-icon.png')
        minus_btn_img = QPixmap('./img/qt자료/minus_icon.png')
        cancel_img = QPixmap('./img/qt자료/cancel_icon.png')

        self.cnt_label = label
        self.price_btn = btn
        self.name_label = QLabel(name)
        self.name_label.setFixedSize(220, 40)

        self.quantity_label = QLabel('1')
        self.quantity_label.setFixedSize(30, 40)
        self.quantity_label.setAlignment(Qt.AlignCenter)

        self.index_label = QLabel(idx)
        self.index_label.setFixedSize(30, 40)

        self.price_label = QLabel(price + '원')
        self.price_label.setStyleSheet('color:rgb(229, 79, 65)')

        # (-) 버튼 생성
        self.decrease_button = QPushButton()
        self.decrease_button.setFixedSize(40, 40)
        self.decrease_button.setStyleSheet('background-color: rgb(229, 79, 64);')
        self.decrease_button.setIcon(QIcon(minus_btn_img))
        self.decrease_button.clicked.connect(self.decrease_quantity)

        # (+) 버튼 생성
        self.increase_button = QPushButton()
        self.increase_button.setFixedSize(40, 40)
        self.increase_button.setStyleSheet('background-color: rgb(229, 79, 64);')
        self.increase_button.setIcon(QIcon(plus_btn_img))
        self.increase_button.clicked.connect(self.increase_quantity)

        # (삭제) 버튼 생성
        self.delete_button = QPushButton()
        self.delete_button.setFixedSize(40, 40)
        self.delete_button.setIcon(QIcon(cancel_img))
        self.delete_button.setIconSize(QSize(38,38))
        self.delete_button.setStyleSheet('background-color: transparent ;')
        self.delete_button.clicked.connect(self.delete_item)

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.delete_button)
        # layout.addWidget(self.index_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.decrease_button)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.increase_button)
        layout.addWidget(self.price_label)
        self.setLayout(layout)

        self.list_widget = list_widget
        self.price = int(price)
        self.idx_text = self.index_label.text()

    def decrease_quantity(self):
        """리스트위젯 수량 업데이트 해줌(-)"""
        quantity = int(self.quantity_label.text())
        if quantity > 1:
            quantity -= 1
            self.quantity_label.setText(str(quantity))


            # db에서 수량 줄임
            con = sqlite3.connect('./DATA/data.db')
            order_df = pd.read_sql('select * from order_table', con)
            drinks_count = int(order_df.loc[order_df['id'] == self.idx_text, 'drink_cnt'].iloc[0]) - 1
            order_df.loc[order_df['id'] == self.idx_text, 'drink_cnt'] = drinks_count
            order_df.to_sql('order_table', con, if_exists='replace', index=False)
            con.commit()
            con.close()
            # total_price = (order_df['drink_cnt'] * order_df['price']).sum()

            self.cnt_label.setText(str(drinks_count) + '개')
            # self.price_btn.setText(str(total_price)+'원')
            self.update_price(drinks_count)

    def increase_quantity(self):
        """리스트위젯 수량 업데이트 해줌(+)"""
        quantity = int(self.quantity_label.text())
        quantity += 1
        self.quantity_label.setText(str(quantity))


        # db에서 수량 추가
        con = sqlite3.connect('./DATA/data.db')
        order_df = pd.read_sql('select * from order_table', con)
        drinks_count = int(order_df.loc[order_df['id'] == self.idx_text, 'drink_cnt'].iloc[0]) + 1
        order_df.loc[order_df['id'] == self.idx_text, 'drink_cnt'] = drinks_count

        order_df.to_sql('order_table', con, if_exists='replace', index=False)
        con.commit()
        con.close()
        self.cnt_label.setText(str(drinks_count) + '개')
        self.update_price(drinks_count)

    def update_price(self, cnt):
        """리스트 위젯 가격 업데이트 해주는 함수"""
        quantity = int(self.quantity_label.text())
        new_price = self.price * quantity
        self.price_label.setText(str(new_price) + '원')

        # 합 구하기
        con = sqlite3.connect('./DATA/data.db')
        order_df = pd.read_sql('select * from order_table', con)
        order_df['drink_cnt'] = order_df['drink_cnt'].astype(int)
        order_df['price'] = order_df['price'].astype(int)
        total_price = (order_df['drink_cnt'] * order_df['price']).sum()

        self.cnt_label.setText(str(cnt) + '개')
        self.price_btn.setText(f'  {str(total_price)}원\n  결제하기')




    def delete_item(self):
        """리스트위젯에서 아이템 지우고 db에서 지우는 함수"""

        # 리스트위젯에서 아이템 지워주기
        item = self.list_widget.itemAt(self.pos())
        row = self.list_widget.row(item)
        self.list_widget.takeItem(row)

        # db에서 id에 맞는 행 지워주기
        con = sqlite3.connect('./DATA/data.db')
        order_df = pd.read_sql('select * from order_table', con)
        order_df = order_df[order_df['id'] != self.index_label.text()]
        order_df.to_sql('order_table', con, if_exists='replace', index=False)
        con.commit()
        con.close()

        order_df['drink_cnt'] = order_df['drink_cnt'].astype(int)
        order_df['price'] = order_df['price'].astype(int)
        total_price = (order_df['drink_cnt'] * order_df['price']).sum()
        drinks_count = (order_df['drink_cnt']).sum()

        self.cnt_label.setText(f'{str(drinks_count)} 개')
        self.price_btn.setText(f'  {str(total_price)}원\n  결제하기')

def add_shopping_item_to_listwidget(list_widget, idx, name, price, label, btn):
    item_widget = ShoppingItemWidget(idx, name, price, list_widget, label, btn)

    item = QListWidgetItem()
    item.setSizeHint(item_widget.sizeHint())

    list_widget.addItem(item)
    list_widget.setItemWidget(item, item_widget)

