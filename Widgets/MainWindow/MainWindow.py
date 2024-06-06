import sys
from os import path
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTableWidgetItem, QMainWindow
from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(path.dirname(__file__) + '\\MainWindow.ui', self)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(25)

        item = QTableWidgetItem("aaaa")

        self.tableWidget.setItem(1, 1, item)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec()
    sys.exit()