import sys
import json
from datetime import datetime
from os import path
import sqlite3
from PyQt5.QtCore import Qt, QTime, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTableWidgetItem, QMainWindow, QTimeEdit
from PyQt5 import uic
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

import Widgets
from db import db
from port import SerialPort
from serial.serialutil import SerialException


def get_time(timeEdit: QTimeEdit) -> tuple:
    time = timeEdit.time()
    return time.hour(), time.minute()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(path.dirname(__file__) + '\\Widgets\\MainWindow2.ui', self)

        try:
            with open("settings.json", mode='r') as file:
                settings = json.loads(file.read())
                self.spinBox_threshold.setValue(settings['sensor_setting'])
                if (time_on := settings['turn_on']) is not None:
                    self.radiobutton_turning_on_time.setChecked(True)
                    self.timeEdit_on.setTime(QTime(*map(int, time_on.split(':')), 0))
                if (time_off := settings['turn_off']) is not None:
                    self.radiobutton_turning_off_time.setChecked(True)
                    self.timeEdit_off.setTime(QTime(*map(int, time_off.split(':')), 0))
        except Exception:
            pass

        self.button_load_mode.clicked.connect(self.load_mode_clicked)
        self.setup_sensor_now.clicked.connect(self.setup_sensor)
        self.button_save_mode.clicked.connect(self.save_mode_clicked)
        self.spinBox_threshold.valueChanged.connect(self.port_setup)

        self.db = db.DataBase()
        self.port = self.serial_port_init()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_cycle)

        self.radiobutton_turning_on_sensor.toggled.connect(self.port_setup)
        self.radiobutton_turning_off_sensor.toggled.connect(self.port_setup)
        self.timeEdit_on.timeChanged.connect(self.port_setup)
        self.timeEdit_off.timeChanged.connect(self.port_setup)
        self.timer.start(1000)

    def load_mode_clicked(self):
        dialog = Widgets.ListWidget(self.db.get_modes(), db=self.db, header_labels=['id', 'Включение', 'Выключение'])
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

    def save_mode_clicked(self):
        on = None
        off = None

        if self.radiobutton_turning_on_time.isChecked():
            on = int(''.join(map(lambda x: str(x).zfill(2), get_time(self.timeEdit_on))))
        if self.radiobutton_turning_off_time.isChecked():
            off = int(''.join(map(lambda x: str(x).zfill(2), get_time(self.timeEdit_off))))
        self.db.add_mode((on, off))

    @staticmethod
    def serial_port_init() -> SerialPort:
        port = None
        print('Try to connect...')
        try:
            port = SerialPort()
        except ConnectionError:
            print('Connection Failed')
        return port

    def update_cycle(self):
        if self.port is None:
            self.port = self.serial_port_init()
            return

        self.clock_check()

        try:
            while answer := self.port.readline():
                self.process_com_answers(answer)
            self.port.sensor_state()
        except SerialException:
            print("Connection Lost")
            self.port_disconnection()
            self.port = None
        # print('---END OF UPDATE CYCLE ---')

    def clock_check(self):
        on_timer = self.radiobutton_turning_on_time.isChecked()
        off_timer = self.radiobutton_turning_off_time.isChecked()
        setup_timer = self.checkBox_setup_by_time.isChecked()
        if not (on_timer or off_timer or setup_timer):
            return
        dt = datetime.now()
        hour, minute = dt.hour, dt.minute
        if on_timer:
            set_hour, set_minute = get_time(self.timeEdit_on)
            if hour == set_hour and set_minute <= minute <= set_minute + 1:
                self.port.set_relay(True)

        if off_timer:
            set_hour, set_minute = get_time(self.timeEdit_off)
            if hour == set_hour and set_minute <= minute <= set_minute + 1:
                self.port.set_relay(False)

        if setup_timer:
            set_hour, set_minute = get_time(self.timeEdit_setup)
            if hour == set_hour and set_minute == minute:
                self.setup_sensor()
                self.checkBox_setup_by_time.setCheckState(False)

    def process_com_answers(self, answer):
        if ':' not in answer:
            return
        command, value = answer.split(':')
        if command == "connected":
            self.port_setup()
        if command == 'sensorState':
            self.label_sensor_state.setText(str(value))

    def port_setup(self):
        if self.port is not None:
            self.port.set_sensor_threshold(self.spinBox_threshold.value())
            self.port.set_mode_on(self.radiobutton_turning_on_sensor.isChecked())
            self.port.set_mode_off(self.radiobutton_turning_off_sensor.isChecked())

    def port_disconnection(self):
        self.label_sensor_state.setText("ПОДКЛЮЧЕНИЕ ПОТЕРЯНО")

    def setup_sensor(self):
        threshold = self.label_sensor_state.text()
        if threshold.isnumeric():
            self.spinBox_threshold.setValue(int(threshold))

    def closeEvent(self, event):
        save = {"turn_on": None,
                "turn_off": None,
                "sensor_setting": self.spinBox_threshold.value()}
        if self.radiobutton_turning_on_time.isChecked():
            save['turn_on'] = ':'.join(map(lambda x: str(x).zfill(2), get_time(self.timeEdit_on)))
        if self.radiobutton_turning_off_time.isChecked():
            save['turn_off'] = ':'.join(map(lambda x: str(x).zfill(2), get_time(self.timeEdit_off)))
        save = json.dumps(save)
        with open("settings.json", mode='w') as file:
            file.write(save)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    app.exec()
    sys.exit()
