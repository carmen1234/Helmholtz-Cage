import threading
import time
import wx

from arduino import Arduino
from globals import sensor_data, port

from gui import GraphFrame

if __name__ == "__main__":

    #Comment out to test GUI without arduino
    #arduino = Arduino(port)
    #sensor_thread = threading.Thread(target=arduino.update_sensor_data, daemon=True)
    #sensor_thread.start()

    while True:
        # Read and print current/field values
        current, magnetic_field = sensor_data["current"], sensor_data["magnetic_field"]
        if current is not None and magnetic_field is not None:
            print(f"Current: {current}, Magnetic Field: {magnetic_field}")

        # Example of how to set coil_current (must be between -255 and 255) (PWM freq)
        #coil_current = 150
        #arduino.set_coil_current(coil_current)

        #For testing without actual sensor readings
        sensor_data["current"] = 1

        app = wx.App()
        app.frame = GraphFrame()
        app.frame.Show()
        app.MainLoop()

        time.sleep(1)
