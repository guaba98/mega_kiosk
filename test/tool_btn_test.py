import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.resize(506, 312)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(220, 120, 100, 100))
        # self.toolButton.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.toolButton.setText('hi')


        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../img/qt자료/kb페이.png"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)


        # adding icon to the toolbutton
        self.toolButton.setIcon(icon)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # adding signal and slot
        self.toolButton.clicked.connect(self.exitapp)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

    # For closing the application
    def exitapp(self):
        sys.exit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

