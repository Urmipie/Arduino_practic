import sys
import sqlite3
from PyQt5.QtWidgets import QApplication
import Widgets

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Widgets.MainWindow()
    ex.show()
    app.exec()
    sys.exit()
