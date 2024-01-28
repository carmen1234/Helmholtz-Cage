# Hold all global configuration and data variables here
# Can be imported into other files using `from globals import ...`

from enum import Enum

# Config
port = "/dev/cu.usbmodem21201"


# Data
sensor_data = {"current": 0.0, # float
               "mag_field_x": 0.0, # float
               "mag_field_y": 0.0,# float
               "mag_field_z": 0.0 # float
              }

# HW parameters
class HW_params(float, Enum):
    raw_mag_min = -32768.0
    raw_mag_max = 32767.0
    min_gauss = -8.0
    max_guass = 8.0
