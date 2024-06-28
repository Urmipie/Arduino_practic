import serial
import serial.tools.list_ports as list_ports


class SerialPort(serial.Serial):
    def __init__(self, port=None, speed=9600):
        if port is None:
            com_ports = list_ports.comports()
            if len(com_ports) == 0:
                raise ConnectionError("Arduino did not found")
            elif len(com_ports) == 1:
                port = com_ports[0].device
            else:
                print("Choose port:")
                for n, port in enumerate(com_ports):
                    print(f'{n}: {port.device}')
                port = com_ports[int(input().strip())].device
        print(f"Connecting to: {port}")
        super().__init__(port, speed)

    def readline(self) -> str:
        data = super().readline()
        if data:
            return data.decode().strip()
        else:
            return ""

    def write(self, text: str):
        super().write(text.encode('utf-8'))
