import serial
import serial.tools.list_ports as list_ports
from serial.serialutil import SerialException


class SerialPort(serial.Serial):
    def __init__(self, port=None, speed=9600, auto_select=True):
        if port is None:
            com_ports = list_ports.comports()
            if len(com_ports) == 0:
                raise ConnectionError("Arduino did not found")
            elif len(com_ports) == 1 or auto_select:
                port = com_ports[0].device
            else:
                print("Choose port:")
                for n, port in enumerate(com_ports):
                    print(f'{n}: {port.device}')
                port = com_ports[int(input().strip())].device
        print(f"Connecting to: {port}")
        super().__init__(port, speed)

    def readline(self) -> str:
        if self.in_waiting > 0:
            line = super().readline().decode().strip()
            if 'sensorState' not in line:
                print(f'{self.name}>>', line)
            return line
        else:
            return ''

    def _write(self, text: str):
        super().write(text.encode('utf-8'))

    def _send_command(self, command, value=0):
        # print(f'{self.name}<< {command}:{value};')
        try:
            self._write(f'{command}:{value};')
        except SerialException:
            pass

    def sensor_state(self):
        self._send_command('sensorState')

    def set_sensor_threshold(self, threshold):
        self._send_command('setSensorThreshold', threshold)

    def set_relay(self, relay):
        self._send_command('setRelay', 1 if relay else 0)

    def set_mode_on(self, value):
        self._send_command('setModeOn', 1 if value else 0)

    def set_mode_off(self, value):
        self._send_command('setModeOff', 1 if value else 0)


if __name__ == '__main__':

    port = SerialPort()
    while True:
        #port._write('sensorState:;')
        #port._write(f'setSensorThreshold:100;')
        #port._write(f'setModeOn:1;')
        try:
            print(port.readline())
        except SerialException:
            print('err')