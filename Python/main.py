import threading
import wx

from arduino import arduino
from control import main_controller
from logger import logger

from gui import GraphFrame

if __name__ == "__main__":

    sensor_thread = threading.Thread(target=arduino.update_arduino_data, daemon=True)
    sensor_thread.start()

    controller_thread = threading.Thread(target=main_controller.run_pid_xyz, daemon=True)
    controller_thread.start()

    # dynamic_sim_thread = threading.Thread(target=main_controller.run_sim, daemon=True)
    # dynamic_sim_thread.start()


    # while True:
    #     # Read and print current/field values
    #     current, mag_field_x, mag_field_y = sensor_data["current"], sensor_data["mag_field_x"], sensor_data['mag_field_y']
    #     if current is not None and mag_field_x is not None and mag_field_y is not None:
    #         print(f"Current: {current}, Magnetic Field - X: {mag_field_x}, Magnetic Field - Y: {mag_field_y}")

        # Example of how to set coil_current (must be between -255 and 255) (PWM freq)
        #coil_current = 150
        #arduino.set_coil_current(coil_current)

        #For testing without actual sensor readings
        #sensor_data["current"] = 1

    app = wx.App()
    app.frame = GraphFrame()
    app.frame.Show()
    app.MainLoop()

