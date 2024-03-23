"""
Helmholtz Cage
ECE496 Team 2023808
Carmen Lamprecht
Rudaina Khalil
Vimal Raj
Date: 2023-11-13

"""
import os
import pprint
import random
import sys
import wx
import csv
import math
from math import pi
import time
import threading

from globals import sensor_data, graph_y_max, graph_y_min, avg_data
from arduino import arduino
from control import pid
from logger import logger, log_stream
from dynamic_sim import dyna_sim

import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
from numpy import sqrt
import pylab

# Define the enum dictionary
enum = {
    'ID_IMPORT': 1,
    'BUTTON1_Hello': 2,
    'UseCSV': 3,
    'BUTTON3_Hello': 4,
    'CSVPathBoxE': 5,
    'ID_Documentation': 6,
    'DebugBoxID': 7,
    'ID_MagXRead': 8,
    'ID_MagYRead': 9,
    'ID_MagZRead': 10,
    'ID_MagXInput': 11,
    'ID_MagYInput': 12,
    'ID_MagZInput': 13,
    'ID_CurrentRead': 14,
    'ID_CurrentInput': 15,
    'ID_Graph_ToggleX': 16,
    'ID_Graph_ToggleY': 17,
    'ID_Graph_ToggleZ': 18,
    'Axis_LabelX': 19,
    'Axis_LabelY': 20,
    'Axis_LabelZ': 21,
    'ID_SetMagX': 22,
    'ID_SetMagY': 23,
    'ID_SetMagZ': 24,
    'ID_ValX': 25,
    'ID_ValY': 26,
    'ID_ValZ': 27,
    'SimMode_0': 28,
    'SimMode_1': 29,
    'SimMode_2': 30,
    'DebugOutputID' : 31
}

COLOR_NAME = 'black'
axis_int = 0


"""""
(used for sliding window part of graph display)
Sample graph code:
Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
"""""

"""""
Class for data from sensor for plotting  X axis of cage
"""""
class DataGenXAxis(object):
    def __init__(self, init=50):
        self.dataX = self.init = init

    def next(self, testing_xaxis):
        self._recalc_data(testing_xaxis)
        return self.dataX

    def _recalc_data(self, testing_xaxis):

        self.dataX = sensor_data["mag_field_x"]
        self.dataX = testing_xaxis

"""""
Class for data from sensor for plotting  Y axis of cage
"""""
class DataGenYAxis(object):
    def __init__(self, init=50):
        self.dataY = self.init = init

    def next(self, testing_yaxis):
        self._recalc_data(testing_yaxis)
        return self.dataY

    def _recalc_data(self, testing_yaxis):
        self.dataY = sensor_data["mag_field_y"]
        self.dataY = testing_yaxis

"""""
Class for data from sensor for plotting  Z axis of cage
"""""
class DataGenZAxis(object):
    def __init__(self, init=50):
        self.dataZ = self.init = init

    def next(self, testing_zaxis):
        self._recalc_data(testing_zaxis)
        return self.dataZ

    def _recalc_data(self, testing_zaxis):
        self.dataZ = sensor_data["mag_field_z"]
        self.dataZ = testing_zaxis

class ModeControlBox(wx.Panel):
    """ A static box with csv upload and 3 preset mode buttons (preset csv files).
    """
    def __init__(self, parent, ID, label, initval):
        wx.Panel.__init__(self, parent, ID)

        self.value = initval

        box = wx.StaticBox(self, -1, "Dynamic Control")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.ReadCSVButton = wx.Button(self, enum['UseCSV'], "Load Sim")
        self.Bind(wx.EVT_BUTTON, self.on_import_csv, self.ReadCSVButton)

        self.CSVPathBox = wx.TextCtrl(self, enum['CSVPathBoxE'], size=(250, -1))
        self.CSVPathBox.SetHint("Enter path/to/csv_file")

        #self.ReadCSVButton.Move((675, 540))
        #self.ReadCSVButton.SetBackgroundColour(wx.Colour(0x886421))
        #self.ReadCSVButton.SetForegroundColour(wx.Colour(0xFFFFFF))
        #self.CSVPathBox.Move(790, 536, wx.EXPAND | wx.ALL | wx.HORIZONTAL | wx.TE_CHARWRAP | wx.GROW)
        #self.CSVPathBox.SetSize(790, 536, 250, 40, wx.HORIZONTAL | wx.GROW)
        #self.DebugBox.SetSize(0, 500, 450, 200, wx.VERTICAL | wx.GROW)


        self.SetMode0 = wx.Button(self, wx.ID_ANY, "Start Sim")
        self.Bind(wx.EVT_BUTTON, self.on_mode_0, self.SetMode0)
        self.SetMode0.Move((25, 0))


        self.SetMode1 = wx.Button(self, wx.ID_ANY, "Stop Sim")
        self.Bind(wx.EVT_BUTTON, self.on_mode_1, self.SetMode1)
        self.SetMode1.Move((50, 0))

        self.SetMode2 = wx.Button(self, wx.ID_ANY, "Reset")
        self.Bind(wx.EVT_BUTTON, self.on_mode_2, self.SetMode2)
        self.SetMode2.Move((0, 75))

        csv_box = wx.BoxSizer(wx.HORIZONTAL)
        csv_box.Add(self.CSVPathBox, flag=wx.ALIGN_CENTER)
        csv_box.AddSpacer(2)
        csv_box.Add(self.ReadCSVButton, flag=wx.ALIGN_CENTER)

        mode_box = wx.BoxSizer(wx.HORIZONTAL)
        mode_box.Add(self.SetMode0, flag=wx.ALIGN_CENTER)
        mode_box.AddSpacer(10)
        mode_box.Add(self.SetMode1, flag=wx.ALIGN_CENTER)
        mode_box.AddSpacer(10)
        mode_box.Add(self.SetMode2, flag=wx.ALIGN_CENTER)

        sizer.Add(csv_box, 0, wx.ALL | wx.ALIGN_CENTRE_HORIZONTAL, 5)
        sizer.Add(mode_box, 0, wx.ALL  | wx.ALIGN_CENTRE_HORIZONTAL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def on_mode_0(self):
        #check if sim is actually loaded
        if dyna_sim.sim_data == []:
            pass #error msg
        else:
            dyna_sim.turn_on_sim()

    def on_mode_1(self):
       #effectively pause sim
       # return self.value
       pass

    def on_mode_2(self):
       #does reset mean restart? or clear everything
       # return self.value
       pass

    def on_import_csv(self):
        input_path = self.CSVPathBox.GetValue()
        fileStatus = dyna_sim.get_sim(input_path)
        if fileStatus == None:
            pass #error stuff, I think I need logging to print to debug console?
        else:
            pass #added some kind of status message like "sim loaded or something"



class InputControlBox(wx.Panel):
    def __init__(self, parent, ID, label, initval):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        self.value = initval

        box = wx.StaticBox(self, wx.ID_ANY, "Static Control")
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.SetX = wx.TextCtrl(self, wx.ID_ANY, size=(80, -1))
        self.SetY = wx.TextCtrl(self, wx.ID_ANY, size=(80, -1))
        self.SetZ = wx.TextCtrl(self, wx.ID_ANY, size=(80, -1))


        self.SetPointButton = wx.Button(self, wx.ID_ANY, "Set Setpoint")
        self.ToggleControllerButton = wx.Button(self, wx.ID_ANY, "Toggle Controller")

        self.Bind(wx.EVT_BUTTON, self.on_set_setpoint, self.SetPointButton)
        self.Bind(wx.EVT_BUTTON, self.on_toggle_controller, self.ToggleControllerButton)

        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(self.SetPointButton, flag=wx.ALIGN_CENTER)
        button_sizer.AddSpacer(10)
        button_sizer.Add(self.ToggleControllerButton, flag=wx.ALIGN_CENTER)

        set_value_box = wx.BoxSizer(wx.HORIZONTAL)
        set_value_box.Add(wx.StaticText(self, wx.ID_ANY, "X: "), flag=wx.ALIGN_CENTER_VERTICAL)
        set_value_box.Add(self.SetX, flag=wx.ALIGN_CENTER_VERTICAL)
        set_value_box.AddSpacer(12)
        set_value_box.Add(wx.StaticText(self, wx.ID_ANY, "Y: "), flag=wx.ALIGN_CENTER_VERTICAL)
        set_value_box.Add(self.SetY, flag=wx.ALIGN_CENTER_VERTICAL)
        set_value_box.AddSpacer(12)
        set_value_box.Add(wx.StaticText(self, wx.ID_ANY, "Z: "), flag=wx.ALIGN_CENTER_VERTICAL)
        set_value_box.Add(self.SetZ, flag=wx.ALIGN_CENTER_VERTICAL)
        set_value_box.AddSpacer(12)

        sizer.Add(set_value_box, 0, wx.ALIGN_CENTER, 5)
        sizer.AddSpacer(10)
        sizer.Add(button_sizer, 0, wx.ALIGN_CENTER)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def on_toggle_controller(self, event):
        pid.toggle_PID()

    def on_set_setpoint(self, event):
        inputX_mag = self.SetX.GetValue()
        inputY_mag = self.SetY.GetValue()
        inputZ_mag = self.SetZ.GetValue()

        if not (float(inputX_mag) <= 1.0 and float(inputX_mag) >= -1.0):
            logger.error("Invalid input range for X-axis setpoint")
        else:
            pid.set_setpoint(float(inputX_mag))

        # TODO: add for Y and Z axis

class DebugConsoleBox(wx.Panel):
    """ A static box with a debug console.
    """
    def __init__(self, parent, ID, label, initval):
        wx.Panel.__init__(self, parent, ID)

        self.value = initval

        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)


        self.DebugOutput = wx.TextCtrl(self, enum['DebugOutputID'], size=wx.Size(800,200), style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.DebugBox = wx.TextCtrl(self, enum['DebugBoxID'], size=wx.Size(800,24), style= wx.TE_PROCESS_ENTER) #probably want to change this to 'CommandBox'

        self.Bind(wx.EVT_TEXT_ENTER, self.on_command_enter, self.DebugBox)

        sizer.Add(self.DebugOutput, 0, wx.ALL, 5)
        sizer.Add(self.DebugBox, 0, wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

        # Create a timer to periodically update the GUI
        self.update_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_debug_output, self.update_timer)

        # Start the timer to update every second (1000 milliseconds)
        self.update_timer.Start(100)

    def on_command_enter(self,event):
        input_str = self.DebugBox.GetValue()
        self.DebugBox.SetValue("")
        logger.info("Received CMD: " + input_str)
        self.process_command(input_str)

    def process_command(self, command):
        command_terms = command.split(" ")
        if command_terms[0] == "":
            pass
        elif command_terms[0] == "set0": #turn all coils 'off' by setting current to 0, will need to call set_coil_current
            arduino.set_coil_current(0)
        elif command_terms[0] == "clear": # clear debug output box
            self.DebugOutput.Clear()
        elif command_terms[0] == "tune_pid": # set kp,ki,kd vals, atm only does single coil pair
            pid.tune_constants(float(command_terms[1]), float(command_terms[2]), float(command_terms[3]))
        elif command_terms[0] == "set_pwm": # also calls set coil current, will only check
            # TODO: add axis argument
            pwm_val = int(command_terms[1])
            if pwm_val > 255 or pwm_val < -255:
                logger.error("Invalid PWM value")
            else:
                sensor_data["pwm_x"] = pwm_val
                arduino.set_coil_current(pwm_val)
                logger.info(f"Setting PWM to {pwm_val}")
        elif command_terms[0] == "reset_avg":
            avg_data["avg_mag_x"] = 0
            avg_data["avg_mag_y"] = 0
            avg_data["avg_mag_z"] = 0
            avg_data["reading_cnt"] = 0
        else:
            logger.error(f"Invalid command - {command}")


    def update_debug_output(self, event):
        # Get the latest logs from the StringIO stream
        new_logs = log_stream.getvalue()

        # Update the DebugOutput text control
        self.DebugOutput.SetValue(new_logs)

        # Scroll to the end of the text
        self.DebugOutput.ShowPosition(self.DebugOutput.GetLastPosition())

class AxisControlBox(wx.Panel):
    """ A static box with a box for reading magnetometer and current sensor values, and setting a current
    """
    def __init__(self, parent, ID, initval, axis):
        wx.Panel.__init__(self, parent, ID)

        self.value = initval
        self.axis = axis

        self.mag_label = wx.StaticText(self, enum['ID_MagXRead'], "M. Field Strength: ")
        self.mag_val = wx.TextCtrl(self, enum['ID_MagXInput'], "          ", style=wx.TE_READONLY)

        self.curr_label = wx.StaticText(self, enum['ID_CurrentRead'], "Current: ")
        self.curr_val = wx.TextCtrl(self, enum['ID_MagXInput'], "          ", style=wx.TE_READONLY)

        self.avg_mag_label = wx.StaticText(self, enum['ID_MagXRead'], "Avg M. Field Strength: ")
        self.avg_mag_val = wx.TextCtrl(self, enum['ID_MagXInput'], "          ", style=wx.TE_READONLY)

        self.mag_setpoint_label = wx.StaticText(self, wx.ID_ANY, "M. Field Strengh Setpoint: ")
        self.mag_setpoint_val = wx.TextCtrl(self, wx.ID_ANY, "          ", style=wx.TE_READONLY)

        self.pwm_label = wx.StaticText(self, wx.ID_ANY, "PWM Value: ")
        self.pwm_val = wx.TextCtrl(self, wx.ID_ANY, "          ", style=wx.TE_READONLY)

        sizer = wx.FlexGridSizer(5, 2, 2, 2)
        sizer.AddMany([(self.mag_label, 1, wx.ALIGN_RIGHT), (self.mag_val),
                       (self.curr_label, 1, wx.ALIGN_RIGHT), (self.curr_val),
                       (self.mag_setpoint_label, 1, wx.ALIGN_RIGHT), (self.mag_setpoint_val),
                       (self.pwm_label, 1, wx.ALIGN_RIGHT), (self.pwm_val),
                       (self.avg_mag_label, 1, wx.ALIGN_RIGHT), (self.avg_mag_val)])

        box = wx.StaticBox(self, wx.ID_ANY, f"{axis.upper()}-Axis")
        box_sizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        box_sizer.Add(sizer, 1, wx.EXPAND | wx.ALL, 5)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(box_sizer, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)

    #Update the value of the "magnetic field" variable, which gets used for plotting,
    #based on which axis is selected for plotting
    def update_values(self):
        self.mag_field = round(sensor_data["mag_field_" + self.axis], 3)
        self.mag_field_str = str(self.mag_field)
        self.mag_val.SetValue(self.mag_field_str)

        self.current = round(sensor_data["current_" + self.axis], 3)
        self.current_str = str(self.current)
        self.curr_val.SetValue(self.current_str)

        self.avg_mag_field = round(avg_data["avg_mag_" + self.axis], 3)
        self.avg_mag_field_str = str(self.avg_mag_field)
        self.avg_mag_val.SetValue(self.avg_mag_field_str)

        self.mag_setpoint_label = round(pid.setpoint, 3)
        self.mag_setpoint_str = str(self.mag_setpoint_label)
        self.mag_setpoint_val.SetValue(self.mag_setpoint_str)

        self.pwm = round(sensor_data["pwm_" + self.axis], 3)
        self.pwm_str = str(self.pwm)
        self.pwm_val.SetValue(self.pwm_str)

class GraphFrame(wx.Frame):
    """ The main frame of the application
    """
    title = 'Helmholtz Cage Control Panel'

    def __init__(self):
        wx.Frame.__init__(self, None, -1, self.title)

        #Initializing the objects for X, Y, and Z axis data:
        self.datagenX = DataGenXAxis()
        self.dataX = [self.datagenX.next(3.3)]

        self.datagenY = DataGenYAxis()
        self.dataY = [self.datagenY.next(3.3)]

        self.datagenZ = DataGenZAxis()
        self.dataZ = [self.datagenZ.next(3.3)]

        self.paused = False

        self.create_menu()
        self.create_status_bar()
        self.create_main_panel()

        self.redraw_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)
        self.redraw_timer.Start(100)


    def create_menu(self):
        self.menubar = wx.MenuBar()

        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        m_import = menu_file.Append(enum['ID_IMPORT'], "&Import CSV File\tCtrl-M", "Help string shown in status bar for this menu item")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_import)
        menu_file.AppendSeparator()

        # Bind on_exit to both the exit menu item and the frame close event
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
        self.Bind(wx.EVT_CLOSE, self.on_exit)

        menuHelp = wx.Menu()
        menuHelp.Append(wx.ID_ABOUT)
        menuHelp.Append(enum['ID_Documentation'], "&How to Use\tCtrl-D", "Help string shown in status bar for this menu item")

        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menuHelp, "&Help")
        self.SetMenuBar(self.menubar)

    def create_main_panel(self):
        self.panel = wx.Panel(self)


        self.init_plot()
        self.canvas = FigCanvas(self.panel, -1, self.fig)

        self.mode_control = ModeControlBox(self.panel, -1, "Dynamic Control", 0)
        self.x_axis_control = AxisControlBox(self.panel, -1, 50, "x")
        self.y_axis_control = AxisControlBox(self.panel, -1, 75, "y")
        self.z_axis_control = AxisControlBox(self.panel, -1, 100, "z")
        self.static_control = InputControlBox(self.panel, -1, "Static Control", 125)
        self.debug_console = DebugConsoleBox(self.panel, -1, "Console", 150)

        self.pause_button = wx.Button(self.panel, -1, "Pause")
        self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)

        # self.cb_grid = wx.CheckBox(self.panel, -1,
        #     "Show Grid",
        #     style=wx.ALIGN_RIGHT)
        # self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)
        # self.cb_grid.SetValue(True)

        # self.cb_xlab = wx.CheckBox(self.panel, -1,
        #     "Show X labels",
        #     style=wx.ALIGN_RIGHT)
        # self.Bind(wx.EVT_CHECKBOX, self.on_cb_xlab, self.cb_xlab)
        # self.cb_xlab.SetValue(True)

        self.cb_xline = wx.RadioButton(self.panel, -1,
            "Show X-axis",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_BUTTON, self.show_x_plot, self.cb_xline)
        self.cb_xline.SetValue(True)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_line_value, self.cb_xline)

        self.cb_yline = wx.RadioButton(self.panel, -1,
            "Show Y-axis",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_BUTTON, self.show_y_plot, self.cb_yline)
        self.cb_yline.SetValue(False)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_line_value, self.cb_yline)

        self.cb_zline = wx.RadioButton(self.panel, -1,
            "Show Z-axis",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_UPDATE_UI, self.show_z_plot, self.cb_zline)
        self.cb_yline.SetValue(False)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_line_value, self.cb_zline)

        # self.update_button = wx.Button(self.panel, -1, "Update")
        #self.Bind(wx.EVT_BUTTON, self.on_update_button, self.update_button)
        #self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.update_button)

       # self.DebugBox = wx.TextCtrl(self.panel, enum['DebugBoxID'])

        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1.Add(self.pause_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER)
        self.hbox1.AddSpacer(20)
        self.hbox1.Add(self.cb_xline, border=5, flag=wx.ALL | wx.ALIGN_CENTER)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.cb_yline, border=5, flag=wx.ALL | wx.ALIGN_CENTER)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.cb_zline, border=5, flag=wx.ALL | wx.ALIGN_CENTER)
        # self.hbox1.AddSpacer(10)
        # self.hbox1.Add(self.update_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2.AddSpacer(40)

        self.hbox2.Add(self.mode_control, proportion=1, border=5, flag=wx.ALL | wx.EXPAND)
        #self.hbox2.Add(self.debug_console, border=5, flag=wx.ALL | wx.GROW)
        self.hbox2.Add(self.static_control, proportion=1, border=5,flag=wx.ALL | wx.EXPAND)
        self.hbox2.AddSpacer(40)
        #self.hbox2.Add(self.debug_console, border=5, flag=wx.ALL | wx.GROW)

        self.axis_control_vbox = wx.BoxSizer(wx.VERTICAL)
        self.axis_control_vbox.Add(self.x_axis_control, border=5, flag=wx.ALL | wx.EXPAND)
        self.axis_control_vbox.Add(self.y_axis_control, border=5, flag=wx.ALL | wx.EXPAND)
        self.axis_control_vbox.Add(self.z_axis_control, border=5, flag=wx.ALL | wx.EXPAND)


        #self.axis_control_vbox.AddSpacer(24)

        self.graph_control_vbox =  wx.BoxSizer(wx.VERTICAL)
        self.graph_control_vbox.Add(self.canvas, 1, flag=wx.TOP | wx.EXPAND)
        self.graph_control_vbox.Add(self.hbox1, border=1, flag=wx.EXPAND)
        self.graph_control_vbox.Add(self.hbox2, border=1, flag=wx.EXPAND)

        self.console_vbox = wx.BoxSizer(wx.HORIZONTAL)
        self.console_vbox.Add(self.debug_console, border=5, flag=wx.ALL | wx.EXPAND)
        self.graph_control_vbox.Add(self.console_vbox, border=5, flag=wx.ALL | wx.EXPAND)

        self.vbox = wx.BoxSizer(wx.HORIZONTAL)


        self.vbox.Add(self.axis_control_vbox, 0, flag=wx.ALIGN_TOP | wx.TOP | wx.EXPAND)
        self.vbox.Add(self.graph_control_vbox, 0, flag=wx.ALIGN_TOP | wx.TOP | wx.EXPAND)


        #testing obj methods from outside
        #self.debug_console.DebugOutput.SetValue("test from outside")



        #self.vbox.Add(self.hbox2, 0, flag=wx.ALIGN_TOP | wx.TOP)
        #self.vbox.Add(self.canvas, 1, flag=wx.TOP | wx.TOP | wx.GROW)

        self.vbox2 =  wx.BoxSizer(wx.VERTICAL)




        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)
        self.vbox.SetSizeHints(self)

    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()
        self.SetStatusText("Designed for UTAT")

    def init_plot(self):
        """ Sets up the initial plot and data objects
        """
        self.dpi = 100
        self.fig = Figure((3.0, 3.0), dpi=self.dpi) #note this needs to be adjusted on windows, plot doesnt completely show up

        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor(COLOR_NAME)
        self.axes.set_title('Magnetic Field', size=12)
        self.axes.set_xlabel('Time (s)', size=8)
        self.axes.set_ylabel('Magnetic Field Strength (Gauss)', size=8)

        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        # plot the data as a line series, and save the reference
        # to the plotted line series
        #

        #x-axis
        if (axis_int == 0):
            self.plot_data = self.axes.plot(
            self.dataX,
            linewidth=2,
            color=(1, 0, 1),
            )[0]
        #y-axis
        elif (axis_int == 1):
            self.plot_data = self.axes.plot(
            self.dataY,
            linewidth=1,
            color=(0, 1, 1),
            )[0]
        #z-axis
        else:
            self.plot_data = self.axes.plot(
            self.dataZ,
            linewidth=1,
            color=(1, 0, 1),
            )[0]

    def draw_plot(self):
        """ Redraws the plot
        """
        self.x_axis_control.update_values()
        self.y_axis_control.update_values()
        self.z_axis_control.update_values()

        if (self.cb_xline.GetValue()):
            self.data = self.dataX
            axis_int = 0

        elif (self.cb_yline.GetValue()):
            self.data = self.dataY
            axis_int = 1
        else:
            self.data = self.dataZ
            axis_int = 2

        # when xmin is set as the lower bound in set_xbound,
        # it "follows" xmax to produce a sliding window effect.
        # therefore, xmin is assigned after xmax.


        xmax = len(self.data) if len(self.data) > 50 else 50
        xmin = xmax - 50

        # for ymin and ymax, find the minimal and maximal values
        # in the data set and add a mininal margin.
        #
        # note that it's easy to change this scheme to the
        # minimal/maximal value in the current display, and not
        # the whole data set.

        ymin = round(min(self.data), 0) - 1
        ymax = round(max(self.data), 0) + 1

        self.axes.set_xbound(lower=xmin, upper=xmax)
        self.axes.set_ybound(lower=graph_y_min, upper=graph_y_max)

        self.axes.grid(True, color='gray')

        # Using setp here is convenient, because get_xticklabels
        # returns a list over which one needs to explicitly
        # iterate, and setp already handles this.
        #
        pylab.setp(self.axes.get_xticklabels(),
            visible=True)

        self.plot_data.set_xdata(np.arange(len(self.data)))
        self.plot_data.set_ydata(np.array(self.data))

        self.canvas.draw()

    def on_pause_button(self, event):
        """ Pauses the graphing
        (used for debug/demo purposes only)
        """
        self.paused = not self.paused

    def on_update_pause_button(self, event):
        """ Changes pause button label
        """
        label = "Resume" if self.paused else "Pause"
        self.pause_button.SetLabel(label)

    def on_update_line_value(self, event):
        #COLOR_NAME = 'green'
        label =  "test"
        if (self.cb_xline.GetValue()):
            label = "x axis"

        elif (self.cb_yline.GetValue()):
            label = "y axis"
        else:
            label = "z axis"
        #self.update_button.SetLabel(label)
        self.draw_plot()

    def show_x_plot(self, event):
        self.draw_plot()

    def show_y_plot(self, event):
        self.draw_plot()

    def show_z_plot(self, event):
        self.draw_plot()

    def on_save_plot(self, event):
        """ Should save the plot as a png
        TODO: get this working? decide if it's needed?
        """
        file_choices = "PNG (*.png)|*.png"

        dlg = wx.FileDialog(
            self,
            message="Save plot as...",
            defaultDir=os.getcwd(),
            defaultFile="plot.png",
            wildcard=file_choices,
            style=wx.SAVE)

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.canvas.print_figure(path, dpi=self.dpi)
            #self.flash_status_message("Saved to %s" % path)

    def on_redraw_timer(self, event):
        # if paused do not add data, but still redraw the plot
        # (to respond to scale modifications, grid change, etc.)
        #
        if not self.paused:
            self.update_sensor_data(event)

            if (self.cb_xline.GetValue()):
                #self.testing = -0.1
                self.testingX = sensor_data["mag_field_x"]
                self.dataX.append(self.datagenX.next(self.testingX))

            elif (self.cb_yline.GetValue()):
                #self.testing = 2.2
                self.testingY = sensor_data["mag_field_y"]
                self.dataY.append(self.datagenY.next(self.testingY))

            else:
                #self.testing = 3.5
                self.testingZ = sensor_data["mag_field_z"]
                self.dataZ.append(self.datagenZ.next(self.testingZ))
            #self.data.append(self.datagen.next(self.testing))

        self.draw_plot()

    def update_sensor_data(self, event):
        """ Testing data, for when GUI isn't connected to sensor
        """
        self.testing = 0

        if (self.cb_xline.GetValue()):
           self.testing = -0.1
           #self.testing = sensor_data["mag_field_x"]

        elif (self.cb_yline.GetValue()):
            self.testing = 2.2
            #self.testing = sensor_data["mag_field_y"]
        else:
            self.testing = 3.5
            #self.testing = sensor_data["mag_field_z"]

    def on_exit(self, event):
        # Exit Sequence
        logger.info("Exiting GUI")
        arduino.set_coil_current(0)
        logger.info("Turned off all coils")
        # TODO: add logic to stop threads before closing serial connection23
        #arduino.ser.close()
        logger.info("Closed Arduino connection")

        event.Skip() # Allow the window to close

        #self.Destroy() # on winows this male it close on the second click
