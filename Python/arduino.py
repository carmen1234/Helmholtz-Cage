import serial
import re
from logger import logger
import json

from globals import sensor_data, port

class Arduino:
    def __init__(self, port, baud_rate=9600):
        self.port = port
        self.connected = True
        try:
            self.ser = serial.Serial(port, baud_rate, timeout=1)
            logger.info(f"Connected to Arduino on port {port}")
        except serial.SerialException:
            logger.warn(f"Failed to open port {port}. Running without Arduino connection.")
            self.connected = False


    def update_data(self, current_x, current_y, current_z, mag_field_x, mag_field_y, mag_field_z):
        sensor_data["current_x"] = current_x
        sensor_data["current_y"] = current_y
        sensor_data["current_z"] = current_z
        sensor_data["mag_field_x"] = mag_field_x
        sensor_data["mag_field_y"] = mag_field_y
        sensor_data["mag_field_z"] = mag_field_z

    def parse_serial_data(self, serial_data):
        match = re.match(r'CX:(-?\d+),CY:(-?\d+),CZ:(-?\d+),X:(-?\d+),Y:(-?\d+),Z:(-?\d+)', serial_data)
        if match:
            return float(match.group(1)), float(match.group(2)), float(match.group(3)), float(match.group(4)), float(match.group(5)), float(match.group(6))
        else:
            return None, None, None, None, None, None

    def update_arduino_data(self):

        # Open file to log sensor data
        fp = open('sensor_data.csv', 'w')
        fp.write("Current X,Current Y,Current Z,Magnetic Field X,Magnetic Field Y,Magnetic Field Z\n")

        while True:
            # Read and parse serial data if Arduino is connected
            line = self.ser.readline().decode('utf-8').strip() if self.connected else "CX:0,CY:0,CZ:0,X:0,Y:0,Z:0"
            current_x, current_y, current_z, mag_field_x, mag_field_y, mag_field_z = self.parse_serial_data(line)

            if current_x is not None and current_y is not None and current_z is not None and mag_field_x is not None and mag_field_y is not None and mag_field_z is not None:
                # Convert to Gauss and Amp
                mag_field_x, mag_field_y, mag_field_z = mag_field_x / 3000, mag_field_y / 3000, mag_field_z / 3000
                current_x, current_y, current_z = current_x / 1000, current_y / 1000, current_z / 1000
                self.update_data(current_x, current_y, current_z, mag_field_x, mag_field_y, mag_field_z)

                # Log sensor data to file
                fp.write(f"{current_x},{current_y},{current_z},{mag_field_x},{mag_field_y},{mag_field_z}\n")

    def set_coil_current(self, speed):
        command = f"S:{-speed}\n"
        logger.debug(f"Sending command to Arduino: {command}")
        if self.connected:
            self.ser.write(command.encode('utf-8'))
        else:
            logger.debug(f"Arduino not connected. Command not sent: {command}")


arduino = Arduino(port)

