from PyQt5.QtWidgets import QApplication, QVBoxLayout, QListWidgetItem, QListWidget, QLabel, QPushButton, QHBoxLayout, QWidget


class ShoppingItemWidget(QWidget):
    def __init__(self, name, price, list_widget):
        super().__init__()

        self.name_label = QLabel(name)
        self.quantity_label = QLabel("1")
        self.price_label = QLabel(price)

        self.decrease_button = QPushButton("-")
        self.decrease_button.clicked.connect(self.decrease_quantity)
        self.increase_button = QPushButton("+")
        self.increase_button.clicked.connect(self.increase_quantity)
        self.delete_button = QPushButton("삭제")
        self.delete_button.clicked.connect(self.delete_item)

        layout = QHBoxLayout()
        layout.addWidget(self.delete_button)
        layout.addWidget(self.name_label)
        layout.addWidget(self.decrease_button)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.increase_button)
        layout.addWidget(self.price_label)

        self.list_widget = list_widget
        self.price = int(price)

        self.setLayout(layout)

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
        self.price_label.setText(str(new_price))

    def delete_item(self):
        item = self.list_widget.itemAt(self.pos())
        row = self.list_widget.row(item)
        self.list_widget.takeItem(row)


def add_shopping_item_to_listwidget(list_widget, name, price):
    item_widget = ShoppingItemWidget(name, price, list_widget)

    item = QListWidgetItem()
    item.setSizeHint(item_widget.sizeHint())

    list_widget.addItem(item)
    list_widget.setItemWidget(item, item_widget)
