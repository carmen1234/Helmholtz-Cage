import serial
import re
import threading
import time

sensor_data = {"current": None, "magnetic_field": None}

class Arduino:
    def __init__(self, port):
        self.port = port
        self.ser = serial.Serial(port, 9600, timeout=1)

    def update_data(self, current, magnetometer):
        sensor_data["current"] = current
        sensor_data["magnetic_field"] = magnetometer

    def parse_serial_data(self, serial_data):
        match = re.match(r'C:(-?\d+\.\d+),M:(-?\d+\.\d+)', serial_data)
        if match:
            return float(match.group(1)), float(match.group(2))
        else:
            return None, None

    def update_sensor_data(self):
        while True:
            line = self.ser.readline().decode('utf-8').strip()
            current, magnetometer = self.parse_serial_data(line)
            if current is not None and magnetometer is not None:
                self.update_data(current, magnetometer)

    def set_coil_current(self, speed):
        command = f"S:{speed}\n"
        self.ser.write(command.encode('utf-8'))

if __name__ == "__main__":
    arduino = Arduino("/dev/cu.usbmodem21201")
    sensor_thread = threading.Thread(target=arduino.update_sensor_data, daemon=True)
    sensor_thread.start()

    while True:
        current, magnetometer = sensor_data["current"], sensor_data["magnetic_field"]
        if current is not None and magnetometer is not None:
            print(f"Current: {current}, Magnetometer: {magnetometer}")

        coil_current = 150
        arduino.set_coil_current(coil_current)

        time.sleep(3)
