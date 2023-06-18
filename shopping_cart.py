from PyQt5.QtWidgets import * #QApplication, QVBoxLayout, QListWidgetItem, QListWidget, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt5.QtCore import *
import pandas as pd
import sqlite3

class ShoppingItemWidget(QWidget):
    def __init__(self, idx, name, price, list_widget):
        super().__init__()

        self.name_label = QLabel(name)
        self.name_label.setFixedSize(220,40)

        self.quantity_label = QLabel('1')
        self.quantity_label.setFixedSize(30,40)
        self.quantity_label.setAlignment(Qt.AlignCenter)

        self.index_label = QLabel(idx)
        self.index_label.setFixedSize(30,40)

        self.price_label = QLabel(price +'원')
        self.price_label.setStyleSheet('color:rgb(229, 79, 65)')

        self.decrease_button = QPushButton("-")
        self.decrease_button.setFixedSize(40,40)
        self.decrease_button.clicked.connect(self.decrease_quantity)
        self.increase_button = QPushButton("+")
        self.increase_button.setFixedSize(40,40)
        self.increase_button.clicked.connect(self.increase_quantity)
        self.delete_button = QPushButton("삭제")
        self.delete_button.setFixedSize(40,40)
        self.delete_button.clicked.connect(self.delete_item)

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.delete_button)
        layout.addWidget(self.index_label)
        layout.addWidget(self.name_label)
        layout.addWidget(self.decrease_button)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.increase_button)
        layout.addWidget(self.price_label)

        self.list_widget = list_widget
        self.price = int(price)

        self.setLayout(layout)

        self.con = sqlite3.connect('./DATA/data.db')
        self.order_df = pd.read_sql('select * from order_table', self.con)



    def decrease_quantity(self):
        quantity = int(self.quantity_label.text())
        if quantity > 1:
            quantity -= 1
            self.quantity_label.setText(str(quantity))

            self.update_price()

    def increase_quantity(self):
        quantity = int(self.quantity_label.text())
        quantity += 1
        self.quantity_label.setText(str(quantity))
        self.update_price()

    def update_price(self):
        quantity = int(self.quantity_label.text())
        new_price = self.price * quantity
        self.price_label.setText(str(new_price)+'원')

    def delete_item(self):
        item = self.list_widget.itemAt(self.pos())
        row = self.list_widget.row(item)
        self.list_widget.takeItem(row)
        idx_text = self.index_label.text()
        print(idx_text)
        # print(self.order_df[self.order_df['id'] == idx_text].index)
        self.order_df = self.order_df.drop(self.order_df[self.order_df['id'] == idx_text].index)
        print(self.order_df)
        # self.order_df = self.order_df[self.order_df['id'] != idx_text]
        self.con.commit()
        self.close()


def add_shopping_item_to_listwidget(list_widget, idx, name, price):
    item_widget = ShoppingItemWidget(idx, name, price, list_widget)

    item = QListWidgetItem()
    item.setSizeHint(item_widget.sizeHint())

    list_widget.addItem(item)
    list_widget.setItemWidget(item, item_widget)

