import sys
from os import path
import sqlite3
from PyQt5.QtCore import Qt, QTime
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTableWidgetItem, QMainWindow
from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

import Widgets
from db import db


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(path.dirname(__file__) + '\\Widgets\\MainWindow2.ui', self)
        self.db = db.DataBase()
        # self.tableWidget.setColumnCount(3)
        # self.tableWidget.setRowCount(25)

        # item = QTableWidgetItem("aaaa")

        #   self.tableWidget.setItem(1, 1, item)
        self.button_load_mode.clicked.connect(self.load_mode_clicked)

    def load_mode_clicked(self):
        dialog = Widgets.ListWidget(self.db.get_modes())
        if dialog.exec():
            data = list(item.text() for item in dialog.tableWidget.selectedItems())
            if data[1] != '-':
                h, m = map(int, data[1].split(':'))
                self.timeEdit_on.setTime(QTime(h, m, 0))
                self.radiobutton_turning_on_time.setChecked(True)
            else:
                self.radiobutton_turning_on_sensor.setChecked(True)
            if data[2] != '-':
                h, m = map(int, data[2].split(':'))
                self.timeEdit_off.setTime(QTime(h, m, 0))
                self.radiobutton_turning_off_time.setChecked(True)
            else:
                self.radiobutton_turning_off_sensor.setChecked(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec()
    sys.exit()
