import sys
from os import path
import sqlite3
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class ListWidget(QDialog):
    def __init__(self, table=None, name='', db=None, header_labels=None):
        self.data = None
        super().__init__()
        uic.loadUi(path.dirname(__file__) + '\\ListWidget.ui', self)

        self.deleteButton.clicked.connect(self.delete)
        if table:
            self.load_table(table)
        if header_labels is not None:
            self.tableWidget.setHorizontalHeaderLabels(header_labels)
        self.db = db
        if db is None:
            self.deleteButton.setVisible(False)

    def delete(self):
        if self.db is not None:
            delete_id = list(item.text() for item in self.tableWidget.selectedItems())[0]
            self.db.delete_mode(delete_id)
            self.close()

    def load_table(self, table):
        rows = len(table)
        columns = len(table[0])
        self.tableWidget.setColumnCount(columns)
        self.tableWidget.setRowCount(rows)
        for row, items in enumerate(table):
            for column, item in enumerate(items):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))

    def save_selected(self, data):
        self.data = data


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ListWidget(table=[[1,2,3], [3,4,5]])
    ex.show()
    app.exec()
    sys.exit()