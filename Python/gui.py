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

from globals import sensor_data, console_command

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

        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.ReadCSVButton = wx.Button(self, enum['UseCSV'], "Import CSV")
        self.Bind(wx.EVT_BUTTON, self.on_import_csv, self.ReadCSVButton)

        self.CSVPathBox = wx.TextCtrl(self, enum['CSVPathBoxE'], "Type Path to CSV File Here")

        #self.ReadCSVButton.Move((675, 540))
        #self.ReadCSVButton.SetBackgroundColour(wx.Colour(0x886421))
        #self.ReadCSVButton.SetForegroundColour(wx.Colour(0xFFFFFF))
        #self.CSVPathBox.Move(790, 536, wx.EXPAND | wx.ALL | wx.HORIZONTAL | wx.TE_CHARWRAP | wx.GROW)
        #self.CSVPathBox.SetSize(790, 536, 250, 40, wx.HORIZONTAL | wx.GROW)
        #self.DebugBox.SetSize(0, 500, 450, 200, wx.VERTICAL | wx.GROW)


        self.SetMode0 = wx.Button(self, enum['SimMode_0'], "Set Mode 0")
        self.Bind(wx.EVT_BUTTON, self.on_mode_0, self.SetMode0)
        self.SetMode0.Move((25, 0))
        self.SetMode0.SetBackgroundColour(wx.Colour(0x886421))
        self.SetMode0.SetForegroundColour(wx.Colour(0xFFFFFF))

        self.SetMode1 = wx.Button(self, enum['SimMode_1'], "Set Mode 1")
        self.Bind(wx.EVT_BUTTON, self.on_mode_1, self.SetMode1)
        self.SetMode1.Move((50, 0))
        self.SetMode1.SetBackgroundColour(wx.Colour(0x886421))
        self.SetMode1.SetForegroundColour(wx.Colour(0xFFFFFF))

        self.SetMode2 = wx.Button(self, enum['SimMode_2'], "Set Mode 2")
        self.Bind(wx.EVT_BUTTON, self.on_mode_2, self.SetMode2)
        self.SetMode2.Move((0, 75))
        self.SetMode2.SetBackgroundColour(wx.Colour(0x886421))
        self.SetMode2.SetForegroundColour(wx.Colour(0xFFFFFF))

        csv_box = wx.BoxSizer(wx.HORIZONTAL)
        csv_box.Add(self.ReadCSVButton, flag=wx.ALIGN_CENTER_VERTICAL)
        csv_box.Add(self.CSVPathBox, flag=wx.ALIGN_CENTER_VERTICAL)

        mode_box = wx.BoxSizer(wx.VERTICAL)
        mode_box.Add(self.SetMode0, flag=wx.ALIGN_CENTER_HORIZONTAL)
        mode_box.Add(self.SetMode1, flag=wx.ALIGN_CENTER_HORIZONTAL)
        mode_box.Add(self.SetMode2, flag=wx.ALIGN_CENTER_HORIZONTAL)

        sizer.Add(csv_box, 0, wx.ALL, 0)
        sizer.Add(mode_box, 0, wx.ALL, 10)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def on_mode_0(self):
       pass

    def on_mode_1(self):
       # return self.value
       pass

    def on_mode_2(self):
       # return self.value
       pass

    def on_import_csv(self):
       # return self.value
       pass

class InputControlBox(wx.Panel):
    def __init__(self,parent, ID, label, initval):
        wx.Panel.__init__(self, parent, ID)

        self.value = initval

        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.XVal_SetButton = wx.Button(self, enum['ID_SetMagX'], "Set Mag X")
        self.Bind(wx.EVT_BUTTON, self.on_set_value_buttonX, self.XVal_SetButton)
        self.XVal_SetButton.Move((80, 160))
        self.XVal_SetButton.SetBackgroundColour(wx.Colour(0x886421))
        self.XVal_SetButton.SetForegroundColour(wx.Colour(0xFFFFFF))
        #self.SetX = wx.TextCtrl(self, enum['ID_ValX'], "", wx.Point(105, 180), wx.DefaultSize)
        self.SetX = wx.TextCtrl(self, enum['ID_ValX']) 

        self.YVal_SetButton = wx.Button(self, enum['ID_SetMagY'], "Set Mag Y")
        self.Bind(wx.EVT_BUTTON, self.on_set_value_buttonY, self.YVal_SetButton)
        self.YVal_SetButton.Move((80, 160))
        self.YVal_SetButton.SetBackgroundColour(wx.Colour(0x886421))
        self.YVal_SetButton.SetForegroundColour(wx.Colour(0xFFFFFF))
        #self.SetX = wx.TextCtrl(self, enum['ID_ValX'], "", wx.Point(105, 180), wx.DefaultSize)
        self.SetY = wx.TextCtrl(self, enum['ID_ValY']) 

        self.ZVal_SetButton = wx.Button(self, enum['ID_SetMagZ'], "Set Mag Z")
        self.Bind(wx.EVT_BUTTON, self.on_set_value_buttonZ, self.ZVal_SetButton)
        self.ZVal_SetButton.Move((80, 160))
        self.ZVal_SetButton.SetBackgroundColour(wx.Colour(0x886421))
        self.ZVal_SetButton.SetForegroundColour(wx.Colour(0xFFFFFF))
        #self.SetX = wx.TextCtrl(self, enum['ID_ValX'], "", wx.Point(105, 180), wx.DefaultSize)
        self.SetZ = wx.TextCtrl(self, enum['ID_ValZ']) 

        set_value_boxX = wx.BoxSizer(wx.HORIZONTAL)
        set_value_boxX.Add(self.XVal_SetButton, flag=wx.ALIGN_CENTER_VERTICAL)
        set_value_boxX.Add(self.SetX, flag=wx.ALIGN_CENTER_VERTICAL)

        set_value_boxY = wx.BoxSizer(wx.HORIZONTAL)
        set_value_boxY.Add(self.YVal_SetButton, flag=wx.ALIGN_CENTER_VERTICAL)
        set_value_boxY.Add(self.SetY, flag=wx.ALIGN_CENTER_VERTICAL)

        set_value_boxZ = wx.BoxSizer(wx.HORIZONTAL)
        set_value_boxZ.Add(self.ZVal_SetButton, flag=wx.ALIGN_CENTER_VERTICAL)
        set_value_boxZ.Add(self.SetZ, flag=wx.ALIGN_CENTER_VERTICAL)

        sizer.Add(set_value_boxX, 0, wx.ALL, 10)
        sizer.Add(set_value_boxY, 0, wx.ALL, 10)
        sizer.Add(set_value_boxZ, 0, wx.ALL, 10)

        self.SetSizer(sizer)
        sizer.Fit(self)


    def on_set_value_buttonX(self, event):
        inputX_mag = self.SetX.GetValue()
        print("X Mag Input = " + inputX_mag) # for debugging purposes

        if not (float(inputX_mag) <= 1.0 and float(inputX_mag) >= -1.0):
            print("Error, invalid input range")
        else:
            print("Setting pwm to: " + str(int(255*float(inputX_mag))))
            #arduino.set_coil_current(int(255*float(inputX_mag)))
    
    def on_set_value_buttonY(self, event):
        inputY_mag = self.SetY.GetValue()
        print("Y Mag Input = " + inputY_mag) # for debugging purposes

        if not (float(inputY_mag) <= 1.0 and float(inputY_mag) >= -1.0):
            print("Error, invalid input range")
        else:
            print("Setting pwm to: " + str(int(255*float(inputY_mag))))
            #arduino.set_coil_current(int(255*float(inputY_mag)))
    
    def on_set_value_buttonZ(self, event):
        inputZ_mag = self.SetZ.GetValue()
        print("Z Mag Input = " + inputZ_mag) # for debugging purposes

        if not (float(inputZ_mag) <= 1.0 and float(inputZ_mag) >= -1.0):
            print("Error, invalid input range")
        else:
            print("Setting pwm to: " + str(int(255*float(inputZ_mag))))
            #arduino.set_coil_current(int(255*float(inputZ_mag)))

class DebugConsoleBox(wx.Panel):
    """ A static box with a debug console.
    """
    def __init__(self, parent, ID, label, initval):
        wx.Panel.__init__(self, parent, ID)

        self.value = initval

        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)


        self.DebugOutput = wx.TextCtrl(self, enum['DebugOutputID'], size=wx.Size(400,72), style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.DebugBox = wx.TextCtrl(self, enum['DebugBoxID'], size=wx.Size(400,24), style= wx.TE_PROCESS_ENTER) #probably want to change this to 'CommandBox'

        self.Bind(wx.EVT_TEXT_ENTER, self.on_command_enter, self.DebugBox)        

        sizer.Add(self.DebugOutput, 0, wx.ALL, 10)
        sizer.Add(self.DebugBox, 0, wx.ALL, 10)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def on_command_enter(self,event):
        input_str = self.DebugBox.GetValue()
        self.DebugBox.SetValue("")
        self.DebugOutput.write("Command: " + input_str + "\n")
        global console_command #this is dumb why is python like this
        console_command = input_str
        print(input_str)

class AxisControlBox(wx.Panel):
    """ A static box with a box for reading magnetometer and current sensor values, and setting a current
    """
    def __init__(self, parent, ID, label, initval, axis):
        wx.Panel.__init__(self, parent, ID)

        self.value = initval
        self.axis = axis
        self.mag_field = 0

        if (axis == 1):
            #something
            self.mag_field = sensor_data["mag_field_x"]
        elif (axis == 2):
            #something
             self.mag_field = sensor_data["mag_field_y"]
        else:
             self.mag_field = sensor_data["mag_field_z"]

        #Writing the values to a csv
        with open("mag_field_values.csv", "w", newline="") as f:
            writer = csv.writer(f)
            start_values = [["X", "Y", "Z"],
            [sensor_data["mag_field_x"], sensor_data["mag_field_y"], sensor_data["mag_field_z"]],
            ]
            writer.writerows(start_values)

        self.mag_field_str = str(self.mag_field)

        box = wx.StaticBox(self, -1, label)
        sizer = wx.StaticBoxSizer(box, wx.VERTICAL)

        self.ReadMagX = wx.StaticText(self, enum['ID_MagXRead'], "M. Field Strength: ")

        self.MagXInput = wx.TextCtrl(self, enum['ID_MagXInput'], "", wx.Point(200, 43), wx.DefaultSize, wx.TE_READONLY)
        self.MagXInput.SetValue(self.mag_field_str)

        self.ReadCurrentX = wx.StaticText(self, enum['ID_CurrentRead'], "Current: ")
        self.ReadCurrentX.Move(105, 90, wx.SIZE_USE_EXISTING)
        self.CurrentInputX = wx.TextCtrl(self, enum['ID_MagXInput'], "", wx.Point(200, 83), wx.DefaultSize, wx.TE_READONLY)

        # self.XVal_SetButton = wx.Button(self, enum['ID_SetMagX'], "Set Value")
        # self.Bind(wx.EVT_BUTTON, self.on_set_value_button, self.XVal_SetButton)
        # self.XVal_SetButton.Move((80, 160))
        # self.XVal_SetButton.SetBackgroundColour(wx.Colour(0x886421))
        # self.XVal_SetButton.SetForegroundColour(wx.Colour(0xFFFFFF))
        # self.SetX = wx.TextCtrl(self, enum['ID_ValX'], "", wx.Point(105, 180), wx.DefaultSize)

        read_mag_box = wx.BoxSizer(wx.HORIZONTAL)
        read_current_box = wx.BoxSizer(wx.HORIZONTAL)
        # set_value_box = wx.BoxSizer(wx.HORIZONTAL)

        read_mag_box.Add(self.ReadMagX, flag=wx.ALIGN_LEFT)
        read_mag_box.Add(self.MagXInput, flag=wx.ALIGN_LEFT)

        read_current_box.Add(self.ReadCurrentX, flag=wx.ALIGN_LEFT)
        read_current_box.Add(self.CurrentInputX, flag=wx.ALIGN_LEFT)

        # set_value_box.Add(self.XVal_SetButton, flag=wx.ALIGN_LEFT)
        # set_value_box.Add(self.SetX, flag=wx.ALIGN_LEFT)

        sizer.Add(read_mag_box, 0, wx.ALL, 10)
        sizer.Add(read_current_box, 0, wx.ALL, 10)
        # sizer.Add(set_value_box, 0, wx.ALL, 10)

        self.SetSizer(sizer)
        sizer.Fit(self)

    #Update the value of the "magnetic field" variable, which gets used for plotting,
    #based on which axis is selected for plotting
    def update_value(self, axis):
        self.axis = axis
        self.mag_field = 0

        if (axis == 1):
            #something
            self.mag_field = sensor_data["mag_field_x"]
        elif (axis == 2):
            #something
             self.mag_field = sensor_data["mag_field_y"]
        else:
             self.mag_field = sensor_data["mag_field_z"]

        #Writing the values to a csv
        with open("mag_field_values.csv", "a", newline="") as f:
            writer = csv.writer(f)
            values = [
            [sensor_data["mag_field_x"], sensor_data["mag_field_y"], sensor_data["mag_field_z"]],
            ]
            writer.writerows(values)

        self.mag_field_str = str(self.mag_field)
        self.MagXInput.SetValue(self.mag_field_str)

    def update_current(self, axis):
        self.axis = axis
        self.current = 0

        if (axis == 1):
            #something
            self.current = sensor_data["current"]
        elif (axis == 2):
            #something
             self.current = sensor_data["current"]
        else:
             self.current = sensor_data["current"]

        self.current_str = str(self.current)
        self.CurrentInputX.SetValue(self.current_str)

    def on_set_value_button(self, axis):
        #called when button pressed
        #-----------------------------------------------
        #1. get magnetic field value from text box
        desired_mag_field = self.SetX.GetValue()
        
        #for testing:
        #self.CurrentInputX.SetValue(desired_mag_field)
        #-----------------------------------------------
        #2. calculate required current (theoretical)
        #turns: 2*5 
        #size: 0.6m -> a = 0.3m
        a = 0.3 #constant, TODO add somehwere else
        miu_0 = 4*pi*pow(10, -7) #also a constant

        #check equation
        # b = (sqrt(2)*miu_0*I)/(pi*a)
        # I = b*(pi*a)/(sqrt(2)*miu_0)
        I = float(desired_mag_field)*(pi*a)/(sqrt(2)*miu_0)

        #3. call control system loop
       #pass



class GraphFrame(wx.Frame):
    """ The main frame of the application
    """
    title = 'Helmholtz Cage'

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
        
        #this is basically polling, should look into getting it to be 'interrupt style'
        self.command_timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.process_command, self.command_timer)
        self.command_timer.Start(100)


    def create_menu(self):
        self.menubar = wx.MenuBar()

        menu_file = wx.Menu()
        m_expt = menu_file.Append(-1, "&Save plot\tCtrl-S", "Save plot to file")
        m_import = menu_file.Append(enum['ID_IMPORT'], "&Import CSV File\tCtrl-M", "Help string shown in status bar for this menu item")
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
        self.Bind(wx.EVT_MENU, self.on_save_plot, m_import)
        menu_file.AppendSeparator()
        m_exit = menu_file.Append(-1, "E&xit\tCtrl-X", "Exit")
        self.Bind(wx.EVT_MENU, self.on_exit, m_exit)

        menuHelp = wx.Menu()
        menuHelp.Append(wx.ID_ABOUT)
        menuHelp.Append(enum['ID_Documentation'], "&How to Use\tCtrl-D", "Help string shown in status bar for this menu item")

        self.menubar.Append(menu_file, "&File")
        self.menubar.Append(menuHelp, "&Help")
        self.SetMenuBar(self.menubar)

    def create_main_panel(self):
        self.panel = wx.Panel(self)

        self.init_plot()
        #self.canvas = FigCanvas(self.panel, -1, self.fig)
        self.canvas1 = FigCanvas(self.panel, -1, self.fig)
        self.canvas2 = FigCanvas(self.panel, -1, self.fig2)
        self.canvas3 = FigCanvas(self.panel, -1, self.fig3)

        self.mode_control = ModeControlBox(self.panel, -1, "DYNAMIC CONTROL", 0)
        self.x_axis_control = AxisControlBox(self.panel, -1, "X AXIS", 50, 1)
        self.y_axis_control = AxisControlBox(self.panel, -1, "Y AXIS", 75, 2)
        self.z_axis_control = AxisControlBox(self.panel, -1, "Z AXIS", 100, 3)
        self.static_control = InputControlBox(self.panel, -1, "STATIC CONTROL", 125)
        self.debug_console = DebugConsoleBox(self.panel, -1, "CONSOLE", 150)

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
            "Show X axis field",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_BUTTON, self.show_x_plot, self.cb_xline)
        self.cb_xline.SetValue(True)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_line_value, self.cb_xline)

        self.cb_yline = wx.RadioButton(self.panel, -1,
            "Show Y axis field",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_BUTTON, self.show_y_plot, self.cb_yline)
        self.cb_yline.SetValue(False)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_line_value, self.cb_yline)

        self.cb_zline = wx.RadioButton(self.panel, -1,
            "Show Z axis field",
            style=wx.ALIGN_RIGHT)
        self.Bind(wx.EVT_UPDATE_UI, self.show_z_plot, self.cb_zline)
        self.cb_yline.SetValue(False)
        self.Bind(wx.EVT_UPDATE_UI, self.on_update_line_value, self.cb_zline)

        self.update_button = wx.Button(self.panel, -1, "Update")
        #self.Bind(wx.EVT_BUTTON, self.on_update_button, self.update_button)
        #self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.update_button)

       # self.DebugBox = wx.TextCtrl(self.panel, enum['DebugBoxID'])

        self.hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox1.Add(self.pause_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(20)
        self.hbox1.Add(self.cb_xline, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.cb_yline, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.cb_zline, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
        self.hbox1.AddSpacer(10)
        self.hbox1.Add(self.update_button, border=5, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

        self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.hbox2.Add(self.mode_control, border=5, flag=wx.ALL)
        #self.hbox2.Add(self.debug_console, border=5, flag=wx.ALL | wx.GROW)
        self.hbox2.Add(self.static_control, border=5,flag=wx.ALL | wx.GROW)
        self.hbox2.AddSpacer(24)
        #self.hbox2.Add(self.debug_console, border=5, flag=wx.ALL | wx.GROW)

        self.axis_control_vbox = wx.BoxSizer(wx.VERTICAL)
        self.axis_control_vbox.Add(self.x_axis_control, border=5, flag=wx.ALL)
        self.axis_control_vbox.Add(self.y_axis_control, border=5, flag=wx.ALL)
        self.axis_control_vbox.Add(self.z_axis_control, border=5, flag=wx.ALL)
       

        #self.axis_control_vbox.AddSpacer(24)

        self.graph_control_vbox =  wx.BoxSizer(wx.VERTICAL)

        self.graph_test_vbox =  wx.BoxSizer(wx.HORIZONTAL)
        self.graph_test_vbox.Add(self.canvas1, 1, flag=wx.TOP | wx.RIGHT)
        self.graph_test_vbox.Add(self.canvas2, 1, flag=wx.RIGHT)
        self.graph_test_vbox.Add(self.canvas3, 1, flag=wx.RIGHT)
        #self.vbox.Add(self.graph_test_vbox, 0, flag=wx.TOP | wx.RIGHT | wx.GROW)
        #self.graph_control_vbox.Add(self.canvas, 1, flag=wx.TOP | wx.TOP | wx.GROW)
        self.graph_control_vbox.Add(self.graph_test_vbox, 1, flag=wx.TOP | wx.TOP | wx.GROW)

        self.graph_control_vbox.Add(self.hbox1, border=5, flag=wx.ALL)
        self.graph_control_vbox.Add(self.hbox2, border=5, flag=wx.ALL)

        self.console_vbox = wx.BoxSizer(wx.HORIZONTAL)
        self.console_vbox.Add(self.debug_console, border=10, flag=wx.ALL | wx.GROW)
        self.graph_control_vbox.Add(self.console_vbox, border=5, flag=wx.ALL)

        self.vbox = wx.BoxSizer(wx.HORIZONTAL)

        # self.graph_test_vbox =  wx.BoxSizer(wx.HORIZONTAL)
        # self.graph_test_vbox.Add(self.canvas1, 1, flag=wx.TOP | wx.RIGHT)
        # self.graph_test_vbox.Add(self.canvas2, 1, flag=wx.RIGHT)
        # self.graph_test_vbox.Add(self.canvas3, 1, flag=wx.RIGHT)
        # self.vbox.Add(self.graph_test_vbox, 0, flag=wx.TOP | wx.RIGHT | wx.GROW)

        
       
        self.vbox.Add(self.axis_control_vbox, 0, flag=wx.ALIGN_TOP | wx.TOP)
        self.vbox.Add(self.graph_control_vbox, 0, flag=wx.ALIGN_TOP | wx.TOP)


        #testing obj methods from outside
        #self.debug_console.DebugOutput.SetValue("test from outside")




        self.vbox2 =  wx.BoxSizer(wx.VERTICAL)

        


        self.panel.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def create_status_bar(self):
        self.statusbar = self.CreateStatusBar()
        self.SetStatusText("Designed for UTAT")

    def init_plot(self):
        """ Sets up the initial plot and data objects
        """
        self.dpi = 100
        self.fig = Figure((3.0, 3.0), dpi=self.dpi)
        self.fig2 = Figure((3.0, 3.0), dpi=self.dpi)
        self.fig3 = Figure((3.0, 3.0), dpi=self.dpi)

        self.axes = self.fig.add_subplot(111)
        self.axes.set_facecolor(COLOR_NAME)
        self.axes.set_title('Magnetometer: X', size=12)

        self.axes2 = self.fig2.add_subplot(111)
        self.axes2.set_facecolor(COLOR_NAME)
        self.axes2.set_title('Magnetometer: Y', size=12)

        self.axes3 = self.fig3.add_subplot(111)
        self.axes3.set_facecolor(COLOR_NAME)
        self.axes3.set_title('Magnetometer: Z', size=12)

        pylab.setp(self.axes.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes.get_yticklabels(), fontsize=8)

        pylab.setp(self.axes2.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes2.get_yticklabels(), fontsize=8)

        pylab.setp(self.axes3.get_xticklabels(), fontsize=8)
        pylab.setp(self.axes3.get_yticklabels(), fontsize=8)
        # plot the data as a line series, and save the reference
        # to the plotted line series
        #

        self.plot_data_x = self.axes.plot(
        self.dataX,
        linewidth=2,
        color=(1, 0, 1),
        )[0]

        self.plot_data_y = self.axes2.plot(
        self.dataY,
        linewidth=1,
        color=(0, 1, 1),
        )[0]

        self.plot_data_z = self.axes3.plot(
        self.dataZ,
        linewidth=1,
        color=(1, 1, 0),
        )[0]
        #x-axis
        # if (axis_int == 0):
        #     self.plot_data = self.axes.plot(
        #     self.dataX,
        #     linewidth=2,
        #     color=(1, 0, 1),
        #     )[0]
        #     self.plot_data = self.axes2.plot(
        #     self.dataX,
        #     linewidth=2,
        #     color=(1, 0, 1),
        #     )[0]
        # #y-axis
        # elif (axis_int == 1):
        #     self.plot_data = self.axes.plot(
        #     self.dataY,
        #     linewidth=1,
        #     color=(0, 1, 1),
        #     )[0]
        #     self.plot_data = self.axes2.plot(
        #     self.dataY,
        #     linewidth=1,
        #     color=(0, 1, 1),
        #     )[0] 
        # #z-axis
        # else:
        #     self.plot_data = self.axes.plot(
        #     self.dataZ,
        #     linewidth=1,
        #     color=(1, 0, 1),
        #     )[0]
        #     self.plot_data = self.axes2.plot(
        #     self.dataZ,
        #     linewidth=1,
        #     color=(1, 0, 1),
        #     )[0]
        
    def draw_plot(self):
        """ Redraws the plot
        """
        #print("test")
        #global axis_int
        #doesnt work right now
        self.x_axis_control.update_value(1)
        self.y_axis_control.update_value(2)
        self.z_axis_control.update_value(3)

        self.x_axis_control.update_current(1)
        self.y_axis_control.update_current(2)
        self.z_axis_control.update_current(3)

        # if (self.cb_xline.GetValue()):
        #     self.data = self.dataX
        #     axis_int = 0

        # elif (self.cb_yline.GetValue()):
        #     self.data = self.dataY
        #     axis_int = 1
        # else:
        #     self.data = self.dataZ
        #     axis_int = 2

        # when xmin is set as the lower bound in set_xbound,
        # it "follows" xmax to produce a sliding window effect. 
        # therefore, xmin is assigned after xmax.
        

        xmax_x = len(self.dataX) if len(self.dataX) > 50 else 50
        xmin_x = xmax_x - 50

        xmax_y = len(self.dataY) if len(self.dataY) > 50 else 50
        xmin_y = xmax_y - 50

        xmax_z = len(self.dataZ) if len(self.dataZ) > 50 else 50
        xmin_z = xmax_z - 50

        # for ymin and ymax, find the minimal and maximal values
        # in the data set and add a mininal margin.
        #
        # note that it's easy to change this scheme to the
        # minimal/maximal value in the current display, and not
        # the whole data set.
    
        ymin_x = round(min(self.dataX), 0) - 1
        ymax_x = round(max(self.dataX), 0) + 1

        ymin_y = round(min(self.dataY), 0) - 1
        ymax_y = round(max(self.dataY), 0) + 1

        ymin_z = round(min(self.dataZ), 0) - 1
        ymax_z = round(max(self.dataZ), 0) + 1

        #set the bounds of the x axis (sliding window or not)
        self.axes.set_xbound(lower=xmin_x, upper=xmax_x)
        self.axes.set_ybound(lower=-10000, upper=10000)

        self.axes.grid(True, color='gray')

        self.axes2.set_xbound(lower=xmin_y, upper=xmax_y)
        self.axes2.set_ybound(lower=-10000, upper=10000)

        self.axes2.grid(True, color='gray')

        self.axes3.set_xbound(lower=xmin_z, upper=xmax_z)
        self.axes3.set_ybound(lower=-10000, upper=10000)

        self.axes3.grid(True, color='gray')

        # Using setp here is convenient, because get_xticklabels
        # returns a list over which one needs to explicitly
        # iterate, and setp already handles this.
        #
        pylab.setp(self.axes.get_xticklabels(),
            visible=True)

        pylab.setp(self.axes2.get_xticklabels(),
            visible=True)

        pylab.setp(self.axes3.get_xticklabels(),
            visible=True)

        self.plot_data_x.set_xdata(np.arange(len(self.dataX)))
        self.plot_data_x.set_ydata(np.array(self.dataX))

        self.plot_data_y.set_xdata(np.arange(len(self.dataY)))
        self.plot_data_y.set_ydata(np.array(self.dataY))

        self.plot_data_z.set_xdata(np.arange(len(self.dataZ)))
        self.plot_data_z.set_ydata(np.array(self.dataZ))

        #self.canvas.draw()
        self.canvas1.draw()
        self.canvas2.draw()
        self.canvas3.draw()

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
        # if (self.cb_xline.GetValue()):
        #     label = "x axis"

        # elif (self.cb_yline.GetValue()):
        #     label = "y axis"
        # else:
        #     label = "z axis"
        # self.update_button.SetLabel(label)
        self.draw_plot()

    def show_x_plot(self, event):
       # self.draw_plot()
       label = "test"

    def show_y_plot(self, event):
       # self.draw_plot()
       label = "test"

    def show_z_plot(self, event):
       # self.draw_plot()
       label = "test"

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
            #self.canvas.print_figure(path, dpi=self.dpi)
            self.canvas1.print_figure(path, dpi=self.dpi)
            self.canvas2.print_figure(path, dpi=self.dpi)
            self.canvas3.print_figure(path, dpi=self.dpi)
            #self.flash_status_message("Saved to %s" % path)

    def on_redraw_timer(self, event):
        # if paused do not add data, but still redraw the plot
        # (to respond to scale modifications, grid change, etc.)
        #
        if not self.paused:
            self.update_sensor_data(event)

            self.testingX = sensor_data["mag_field_x"]
            self.dataX.append(self.datagenX.next(self.testingX))

            self.testingY = sensor_data["mag_field_y"]
            self.dataY.append(self.datagenY.next(self.testingY))

            self.testingZ = sensor_data["mag_field_z"]
            self.dataZ.append(self.datagenZ.next(self.testingZ))
            
            # if (self.cb_xline.GetValue()):
            #     #self.testing = -0.1
            #     self.testingX = sensor_data["mag_field_x"]
            #     self.dataX.append(self.datagenX.next(self.testingX))

            # elif (self.cb_yline.GetValue()):
            #     #self.testing = 2.2
            #     self.testingY = sensor_data["mag_field_y"]
            #     self.dataY.append(self.datagenY.next(self.testingY))
        
            # else:
            #     #self.testing = 3.5
            #     self.testingZ = sensor_data["mag_field_z"]
            #     self.dataZ.append(self.datagenZ.next(self.testingZ))
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

        #all of these commands will need to reset the global 'console_command' global var 
    def process_command(self, event):
        global console_command
        command_terms = console_command.split(" ")

        if command_terms[0] == "":
            pass
        elif command_terms[0] == "set0": #turn all coils 'off' by setting current to 0, will need to call set_coil_current
            pass
            #arduino.set_coil_current(0)
        elif command_terms[0] == "clear": # clear debug output box
            pass
        elif command_terms[0] == "tune_pid": # set kd,kp,ki vals
            pass
        elif command_terms[0] == "set_pwm": # also calls set coil current, will only check 
            pass
        else:
            self.debug_console.DebugOutput.write("Invalid Command\n") #maybe something like this should be a try_catch instead?
        
        console_command = "" #it's one line but I could make this its own function?

    def on_exit(self, event):
        self.Destroy()


#if __name__ == '__main__':

    # sensor_data["magnetic_field"] = 1

    # app = wx.App()
    # app.frame = GraphFrame()
    # app.frame.Show()
    # app.MainLoop()
