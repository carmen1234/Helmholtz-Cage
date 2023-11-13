import serial
import re

from globals import sensor_data

class Arduino:
    def __init__(self, port, baud_rate=9600):
        self.port = port
        self.ser = serial.Serial(port, baud_rate, timeout=1)

    def update_data(self, current, magnetic_field):
        sensor_data["current"] = current
        sensor_data["magnetic_field"] = magnetic_field

    def parse_serial_data(self, serial_data):
        match = re.match(r'C:(-?\d+\.\d+),M:(-?\d+\.\d+)', serial_data)
        if match:
            return float(match.group(1)), float(match.group(2))
        else:
            return None, None

    def update_sensor_data(self):
        while True:
            line = self.ser.readline().decode('utf-8').strip()
            current, magnetic_field = self.parse_serial_data(line)
            if current is not None and magnetic_field is not None:
                self.update_data(current, magnetic_field)

    def set_coil_current(self, speed):
        command = f"S:{speed}\n"
        self.ser.write(command.encode('utf-8'))

