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

    dynamic_sim_thread = threading.Thread(target=main_controller.run_sim, daemon=True)
    dynamic_sim_thread.start()

    app = wx.App()
    app.frame = GraphFrame()
    app.frame.Show()
    app.MainLoop()

