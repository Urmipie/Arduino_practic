import serial
import serial.tools.list_ports as list_ports


class SerialPort(serial.Serial):
    def __init__(self, port =None, speed=9600):
        if port is None:
            for port in list_ports.comports():
                if "Arduino" in port.name:
                    port_name = port.device
                    break
            raise ConnectionError("Arduino did not found")
        super().__init__(port, speed)

    def readline(self, size: any) -> str:
        return super().readline(size).decode("utf-8")

    def write(self, text: str):
        super().write(text.encode('utf-8'))
