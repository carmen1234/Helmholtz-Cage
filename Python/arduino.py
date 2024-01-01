import serial
import re

from globals import sensor_data

class Arduino:
    def __init__(self, port, baud_rate=9600):
        self.port = port
        self.ser = serial.Serial(port, baud_rate, timeout=1)

    def update_data(self, current, mag_field_x, mag_field_y, mag_field_z):
        sensor_data["current"] = current
        sensor_data["mag_field_x"] = mag_field_x
        sensor_data["mag_field_y"] = mag_field_y
        sensor_data["mag_field_z"] = mag_field_z

        write_header = 1

        with open('magnetic_field.csv', 'a', newline='') as csvfile:
            fieldnames = ['x_axis', 'y_axis', 'z_axis']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if (write_header == 1):
                writer.writeheader()
                write_header = 0
            writer.writerow({'x_axis':  mag_field_x, 'y_axis':  mag_field_y,'z_axis':  mag_field_z})

    def parse_serial_data(self, serial_data):
        match = re.match(r'C:(-?\d+\.?\d+),X:(-?\d+\.?\d+),Y:(-?\d+\.?\d+),Z:(-?\d+\.?\d+)', serial_data)
        if match:
            return float(match.group(1)), float(match.group(2)), float(match.group(3)), float(match.group(4))
        else:
            return None, None, None, None

    def update_arduino_data(self):
        while True:
            line = self.ser.readline().decode('utf-8').strip()
            current, mag_field_x, mag_field_y, mag_field_z = self.parse_serial_data(line)
            if current is not None and mag_field_x is not None and mag_field_y is not None and mag_field_z is not None:
                self.update_data(current, mag_field_x, mag_field_y, mag_field_z)

    def set_coil_current(self, speed):
        command = f"S:{speed}\n"
        self.ser.write(command.encode('utf-8'))

