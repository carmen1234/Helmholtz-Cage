import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

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
    'SimMode_2': 30
}

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, wx.ID_ANY, "HCageGui", wx.DefaultPosition, wx.Size(720, 1280))

        menuFile = wx.Menu()
        menuFile.Append(enum['ID_IMPORT'], "&Import CSV File\tCtrl-M", "Help string shown in status bar for this menu item")
        menuFile.AppendSeparator()
        menuFile.Append(wx.ID_EXIT)

        menuHelp = wx.Menu()
        menuHelp.Append(wx.ID_ABOUT)
        menuHelp.Append(enum['ID_Documentation'], "&How to Use\tCtrl-D", "Help string shown in status bar for this menu item")

        menuBar = wx.MenuBar()
        menuBar.Append(menuFile, "&File")
        menuBar.Append(menuHelp, "&Help")
        self.SetMenuBar(menuBar)

        self.CreateStatusBar()
        self.SetStatusText("Designed for UTAT")

        self.XAxisLabel = wx.TextCtrl(self, enum['Axis_LabelX'], "", wx.DefaultPosition, wx.Size(450, 35), wx.TE_READONLY | wx.ALIGN_CENTER_HORIZONTAL | wx.TE_CENTER)
        self.XAxisLabel.WriteText("X-Axis")
        self.XAxisLabel.SetBackgroundColour(wx.Colour(0xF7E9DC))


        self.YAxisLabel = wx.TextCtrl(self, enum['Axis_LabelY'], "", wx.Point(0, 160), wx.Size(450, 35), wx.TE_READONLY | wx.ALIGN_CENTER_HORIZONTAL | wx.TE_CENTER)
        self.YAxisLabel.WriteText("Y-Axis")
        self.YAxisLabel.SetBackgroundColour(wx.Colour(0xF7E9DC))


        self.ZAxisLabel = wx.TextCtrl(self, enum['Axis_LabelZ'], "", wx.Point(0, 320), wx.Size(450, 35), wx.TE_READONLY | wx.ALIGN_CENTER_HORIZONTAL | wx.TE_CENTER)
        self.ZAxisLabel.WriteText("Z-Axis")
        self.ZAxisLabel.SetBackgroundColour(wx.Colour(0xF7E9DC))

        self.CSVFilePicker= wx.FilePickerCtrl(self, enum['UseCSV'],"Open CSV", wildcard="CSV files (*.csv)|*.csv", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        self.CSVFilePicker.Move((675, 540))
        
   

        #self.CSVPathBox = wx.TextCtrl(self, enum['CSVPathBoxE'], "Type Path to CSV File Here")
        self.DebugBox = wx.TextCtrl(self, enum['DebugBoxID'])

        self.Bind(wx.EVT_MENU, self.OnImport, id=enum['ID_IMPORT'])
        self.Bind(wx.EVT_MENU, self.OnHowTo, id=enum['ID_Documentation'])
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)

        self.XVal_SetButton = wx.Button(self, enum['ID_SetMagX'], "Set Value")
        self.XVal_SetButton.Move((80, 120))
        self.XVal_SetButton.SetBackgroundColour(wx.Colour(0x886421))
        self.XVal_SetButton.SetForegroundColour(wx.Colour(0xFFFFFF))

        self.YVal_SetButton = wx.Button(self, enum['ID_SetMagY'], "Set Value")
        self.YVal_SetButton.Move((80, 280))
        self.YVal_SetButton.SetBackgroundColour(wx.Colour(0x886421))
        self.YVal_SetButton.SetForegroundColour(wx.Colour(0xFFFFFF))

        self.ZVal_SetButton = wx.Button(self, enum['ID_SetMagZ'], "Set Value")
        self.ZVal_SetButton.Move((80, 440))
        self.ZVal_SetButton.SetBackgroundColour(wx.Colour(0x886421))
        self.ZVal_SetButton.SetForegroundColour(wx.Colour(0xFFFFFF))

        self.SetX = wx.TextCtrl(self, enum['ID_ValX'], "", wx.Point(200, 120), wx.DefaultSize)
        self.SetY = wx.TextCtrl(self, enum['ID_ValY'], "", wx.Point(200, 280), wx.DefaultSize)
        self.SetZ = wx.TextCtrl(self, enum['ID_ValZ'], "", wx.Point(200, 440), wx.DefaultSize)

        # self.ReadCSVButton = wx.Button(self, enum['UseCSV'], "Import CSV")
        # self.ReadCSVButton.Move((675, 540))
        # self.ReadCSVButton.SetBackgroundColour(wx.Colour(0x886421))
        # self.ReadCSVButton.SetForegroundColour(wx.Colour(0xFFFFFF))
        # self.CSVPathBox.Move(790, 536, wx.EXPAND | wx.ALL | wx.HORIZONTAL | wx.TE_CHARWRAP | wx.GROW)
        # self.CSVPathBox.SetSize(790, 536, 250, 40, wx.HORIZONTAL | wx.GROW)
        self.DebugBox.SetSize(0, 500, 450, 200, wx.VERTICAL | wx.GROW)

        self.ReadMagX = wx.StaticText(self, enum['ID_MagXRead'], "M. Field Strength")
        self.ReadMagY = wx.StaticText(self, enum['ID_MagYRead'], "M. Field Strength")
        self.ReadMagZ = wx.StaticText(self, enum['ID_MagZRead'], "M. Field Strength")

        self.ReadMagX.Move((80, 50))
        self.ReadMagY.Move((80, 210))
        self.ReadMagZ.Move((80, 370))

        self.MagXInput = wx.TextCtrl(self, enum['ID_MagXInput'], "", wx.Point(200, 43), wx.DefaultSize, wx.TE_READONLY)
        self.MagYInput = wx.TextCtrl(self, enum['ID_MagYInput'], "", wx.Point(200, 203), wx.DefaultSize, wx.TE_READONLY)
        self.MagZInput = wx.TextCtrl(self, enum['ID_MagZInput'], "", wx.Point(200, 363), wx.DefaultSize, wx.TE_READONLY)

        self.ReadCurrentX = wx.StaticText(self, enum['ID_CurrentRead'], "Current")
        self.ReadCurrentX.Move(105, 90, wx.SIZE_USE_EXISTING)
        self.CurrentInputX = wx.TextCtrl(self, enum['ID_MagXInput'], "", wx.Point(200, 83), wx.DefaultSize, wx.TE_READONLY)
        self.ReadCurrentY = wx.StaticText(self, enum['ID_MagZRead'], "Current")
        self.ReadCurrentY.Move(105, 250, wx.SIZE_USE_EXISTING)
        self.CurrentInputY = wx.TextCtrl(self, enum['ID_MagXInput'], "", wx.Point(200, 243), wx.DefaultSize, wx.TE_READONLY)
        self.ReadCurrentZ = wx.StaticText(self, enum['ID_MagZRead'], "Current")
        self.ReadCurrentZ.Move(105, 410, wx.SIZE_USE_EXISTING)
        self.CurrentInputZ = wx.TextCtrl(self, enum['ID_MagXInput'], "", wx.Point(200, 403), wx.DefaultSize, wx.TE_READONLY)

        self.SetMode0 = wx.Button(self, enum['SimMode_0'], "Set Mode 0")
        self.SetMode0.Move((750, 580))
        self.SetMode0.SetBackgroundColour(wx.Colour(0x886421))
        self.SetMode0.SetForegroundColour(wx.Colour(0xFFFFFF))

        self.SetMode1 = wx.Button(self, enum['SimMode_1'], "Set Mode 1")
        self.SetMode1.Move((750, 620))
        self.SetMode1.SetBackgroundColour(wx.Colour(0x886421))
        self.SetMode1.SetForegroundColour(wx.Colour(0xFFFFFF))

        self.SetMode2 = wx.Button(self, enum['SimMode_2'], "Set Mode 2")
        self.SetMode2.Move((750, 660))
        self.SetMode2.SetBackgroundColour(wx.Colour(0x886421))
        self.SetMode2.SetForegroundColour(wx.Colour(0xFFFFFF))

        self.Graph_ToggleX = wx.Button(self, enum['ID_Graph_ToggleX'], "Toggle X")
        self.Graph_ToggleX.Move((600, 470))
        self.Graph_ToggleX.SetBackgroundColour(wx.Colour(0x886421))
        self.Graph_ToggleX.SetForegroundColour(wx.Colour(0xFFFFFF))

        self.Graph_ToggleY = wx.Button(self, enum['ID_Graph_ToggleY'], "Toggle Y")
        self.Graph_ToggleY.Move((750, 470))
        self.Graph_ToggleY.SetBackgroundColour(wx.Colour(0x886421))
        self.Graph_ToggleY.SetForegroundColour(wx.Colour(0xFFFFFF))

        self.Graph_ToggleZ = wx.Button(self, enum['ID_Graph_ToggleZ'], "Toggle Z")
        self.Graph_ToggleZ.Move((900, 470))
        self.Graph_ToggleZ.SetBackgroundColour(wx.Colour(0x886421))
        self.Graph_ToggleZ.SetForegroundColour(wx.Colour(0xFFFFFF))

        self.figure = Figure()
        self.m_plot = FigureCanvas(self, -1, self.figure)
        self.m_plot.SetSize((460, 40, 735, 400))
        self.figure.subplots_adjust(left=0.08, bottom=0.08, right=0.95, top=0.9)
        ax = self.figure.add_subplot(111)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        self.m_plot.draw()

        self.Bind(wx.EVT_BUTTON, self.OnSetMagX, id=enum['ID_SetMagX'])
        self.Bind(wx.EVT_BUTTON, self.OnCSVButton, id=enum['UseCSV'])
        self.Bind(wx.EVT_BUTTON, self.OnSetMagY, id=enum['ID_SetMagY'])

        self.SetSize(1200, 800)

    def OnImport(self, event):
        # Handle import event
        pass

    def OnSetMagX(self, event):
        # Handle SetMagX event
        pass

    def OnSetMagY(self, event):
        # Handle SetMagX event
        pass

    def OnCSVButton(self, event):
        #when clicked, read from CSV Path box
        csv_path = self.CSVFilePicker.GetPath()
       

    def OnHowTo(self, event):
        # Handle HowTo event
        pass

    def OnAbout(self, event):
        # Handle About event
        pass

    def OnExit(self, event):
        self.Close()

app = wx.App()
frame = MyFrame()
frame.Show()
app.MainLoop()