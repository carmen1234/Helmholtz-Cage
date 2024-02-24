# Hold all global configuration and data variables here
# Can be imported into other files using `from globals import ...`

from enum import Enum

# Config
port = "/dev/cu.usbmodem101"
debug = 0


# Data
sensor_data = {"current_x": 0.0,
               "current_y": 0.0,
               "current_z": 0.0,
               "mag_field_x": 0.0,
               "mag_field_y": 0.0,
               "mag_field_z": 0.0,
               "pwm_x": 1,
               "pwm_y": 1,
               "pwm_z": 1,
               "time_interval": 0.1
              }

# HW parameters
class HW_params(float, Enum):
    raw_mag_min = -32768.0
    raw_mag_max = 32767.0
    min_gauss = -8.0
    max_guass = 8.0

# Command Processing
console_command = ""
