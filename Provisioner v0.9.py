import wx, re, threading, serial, time

# Pump board provisioner
# v0.9
# by Ryan Vibrandt and Peter Ezetta
#
# Changelog:
# v0.9 --   First release. All GUI, no innards.
#           Test Tab complete
#           Provisioner GUI finished

class TestTab(wx.Panel):

    IDLE_BUTTON_COLOR = (236, 233, 216, 255)
    RUN_BUTTON_COLOR = "Red"
    RunThread = True
    ComList = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM10", "COM11", "COM12"]
    
    def __init__(self, parent, output):
        wx.Panel.__init__(self, parent)

        self.output = output
        font1 = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        testLabel = wx.StaticText(self, label="Test Selection")
        testLabel.SetFont(font1)
        xmitLabel = wx.StaticText(self, label="Transmit Com Port")
        xmitLabel.SetFont(font1)
        receiveLabel = wx.StaticText(self, label="Receive Com Port")
        receiveLabel.SetFont(font1)
        self.testDropdown = wx.Choice(self)
        self.testDropdown.AppendItems(strings=["Gbat", "IR"])
        self.testDropdown.SetFont(font1)
        self.transmitComDropdown = wx.Choice(self)
        self.transmitComDropdown.AppendItems(strings=self.ComList)
        self.transmitComDropdown.SetFont(font1)
        self.receiveComDropdown = wx.Choice(self)
        self.receiveComDropdown.AppendItems(strings=self.ComList)
        self.receiveComDropdown.SetFont(font1)
        self.StartButton = wx.Button(self, label="Start Test")
        self.StartButton.Bind(wx.EVT_BUTTON, self.OnStartPress)
        self.StartButton.SetFont(font1)

        self.ResultLabel = wx.StaticText(self, label="                                              ", # Establish footprint of StaticText
                                         style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE)
        self.ResultLabel.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL))

        grid = wx.FlexGridSizer(rows=3,cols=4)
        grid.AddMany([(testLabel, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
                      (self.testDropdown, 0, wx.EXPAND | wx.ALL, 3),
                      (wx.StaticText(self, label="")),
                      (wx.StaticText(self, label="")),
                      (xmitLabel, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
                      (self.transmitComDropdown, 0, wx.EXPAND | wx.ALL, 3),
                      (wx.StaticText(self, label="                   ")),
                      (self.StartButton, 0, wx.ALIGN_CENTER),
                      (receiveLabel, 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
                      (self.receiveComDropdown, 0, wx.EXPAND | wx.ALL, 3),
                      ])
        
        # Use some sizers to see layout options
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(grid, 0, wx.CENTER)
        label = wx.StaticText(self,label="")
        label.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        vsizer.Add(label)
        vsizer.Add(self.ResultLabel, 1, wx.ALIGN_CENTER)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        #sizer.SetMinSize((-1,200))
        sizer.Add(vsizer, 1, wx.CENTER)
        
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)
        
        
    def OnStartPress(self, event):
        if (self.StartButton.GetLabel() == "Start Test"):
            self.StartButton.SetLabel("Stop Test")
            self.StartButton.SetBackgroundColour(self.RUN_BUTTON_COLOR)
            self.t = threading.Thread(target=self.StartTest)
            self.t.start()
        else:
            if (self.t.isAlive()):
                self.RunThread = False
            else:
                self.StopThread()        # In case of thread failure
                
    def StopThread(self):
        self.RunThread = True
        self.StartButton.SetLabel("Start Test")
        self.StartButton.SetBackgroundColour(self.IDLE_BUTTON_COLOR)
    
    def StartTest(self):
        self.SetResultLabel("running")
        #Read the input from the test selection box, and run the appropriate test.
        if(self.testDropdown.GetSelection() == 0): # Gbat
            self.GbatTest()
        elif(self.testDropdown.GetSelection() == 1): # IR
            self.IrTest()
        else:
            self.output.AppendText("Please select a test from the dropdown menu.\n")
            self.SetResultLabel("halted")
        self.StopThread()

    def GbatTest(self):
        if(self.receiveComDropdown.GetSelection() == -1):
            self.output.AppendText("Please select a receive com port from the dropdown menu.\n")
            self.SetResultLabel("halted")
        else:
            try:
                receivePort = serial.Serial(self.ComList[self.receiveComDropdown.GetSelection()], 9600, timeout=1)
            except serial.SerialException as strerror:
                self.output.AppendText("'{0}' could not be opened. Please double-check that you've chosen the right COM port.\n"+
                                       "(SerialException: {1})\n\n".format(self.ComList[self.receiveComDropdown.GetSelection()],strerror))
                self.SetResultLabel("halted")
            else:
                status = "Fail"
                for i in range(60):
                    gbat = receivePort.read(4)
                    self.output.AppendText(gbat)
                    if(re.match("^R\d\d\d$", gbat)):
                        status = "Pass"
                        break
                    if not self.RunThread:
                        break
                
                if(status == "Pass"):
                    self.SetResultLabel("success")
                    # Enter infinite loop
                    while(self.RunThread):
                        self.output.AppendText(receivePort.read(5))
                elif(status == "Fail"):
                    self.SetResultLabel("fail")

                #Close the serial port.
                receivePort.close()
            
##        

    def IrTest(self):
        if(self.receiveComDropdown.GetSelection() == -1):
            appendtext("Please select a receive com port from the dropdown menu.\n")
        elif(self.transmitComDropdown.GetSelection() == -1):
            appendtext("Please select a transmit com port from the dropdown menu.\n")
        else:
            try:
                transmitPort = serial.Serial(self.ComList[self.transmitComDropdown.GetSelection()], 2400, timeout=1)
                receivePort = serial.Serial(self.ComList[self.receiveComDropdown.GetSelection()], 2400, timeout=1)
            except serial.SerialException as strerror:
                self.output.AppendText("One of the ports could not be opened. Please double-check that you've chosen" +
                                       "the right COM port.(SerialException: {0})\n\n".format(strerror))
            else:
                status = "Pass"
                for i in range(3):
                    receivePort.flushInput()
                    transmitPort.write("ABCDEFGHIJKLMNOPQ")
                    irdata = receivePort.read(17)
                    self.output.AppendText(irdata + "\n")
                    if not(irdata == "ABCDEFGHIJKLMNOPQ"):
                        status = "Fail"
                        break
                    time.sleep(5000)
                        
                if(status == "Pass"):
                    self.SetResultLabel("success")
                elif(status == "Fail"):
                    self.SetResultLabel("fail")
                        
                receivePort.close()
                transmitPort.close()

    def SetResultLabel(self, result):
        if (result == "success"):
            self.ResultLabel.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.BOLD))
            self.ResultLabel.SetForegroundColour("Green")
            self.ResultLabel.SetLabel("Test Passed!")
        elif (result == "fail"):
            self.ResultLabel.SetFont(wx.Font(20, wx.DEFAULT, wx.ITALIC, wx.BOLD))
            self.ResultLabel.SetForegroundColour("Red")
            self.ResultLabel.SetLabel("Test Failed! ")
        elif (result == "running"):
            self.ResultLabel.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
            self.ResultLabel.SetForegroundColour("Black")
            self.ResultLabel.SetLabel("Running test, please wait...")
        elif (result == "halted"):
            self.ResultLabel.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
            self.ResultLabel.SetForegroundColour("Black")
            self.ResultLabel.SetLabel("Test halted due to error")
        else:
            self.ResultLabel.SetFont(wx.Font(20, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
            self.ResultLabel.SetForegroundColour("Black")
            self.ResultLabel.SetLabel(result)

class ProvisionTab(wx.Panel):

    LabelNames = [ "IP Address", "Datalog Server IP Address", "Pump Controller IP Address",
                   "Network Mask", "Default Gateway", "Listen Port", "Debug Server Port",
                   "Pump Controller Port", "MAC Address", "Pump ID", "Distance to Ground",
                   "Current Transducer Value" ]
    TargetTextCtrl = 0 # Initialize with IP Address TextCtrl having target
    NON_TARGET_COLOR = "White"
    TARGET_COLOR = (255,255,175,255) # Pale Yellow
    ERROR_COLOR = (255,50,50,255) # Pale Red
    ComList = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM10", "COM11", "COM12",
               "COM13", "COM14", "COM15", "COM16", "COM17", "COM18", "COM19", "COM20"]
    
    def __init__(self, parent, output):
        wx.Panel.__init__(self, parent)

        self.output = output

        labelFont   = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        textBoxFont = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        buttonFont  = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        # ID namespace
        # 100 = CheckBox
        # 200 = StaticText
        # 300 = TextCtrl
        # 400 = SpinButton
        # 500 = Button
        
##        self.ipCheck = wx.CheckBox(self, id=100)
##        self.ipCheck.SetValue(True)
##        self.datalogIpCheck = wx.CheckBox(self, id=101)
##        self.datalogIpCheck.SetValue(True)
##        self.controllerIpCheck = wx.CheckBox(self, id=102)
##        self.controllerIpCheck.SetValue(True)
##        self.networkMaskCheck = wx.CheckBox(self, id=103)
##        self.networkMaskCheck.SetValue(True)
##        self.defaultGatewayCheck = wx.CheckBox(self, id=104)
##        self.defaultGatewayCheck.SetValue(True)
##        self.listenPortCheck = wx.CheckBox(self, id=105)
##        self.listenPortCheck.SetValue(True)
##        self.debugPortCheck = wx.CheckBox(self, id=106)
##        self.debugPortCheck.SetValue(True)
##        self.controllerPortCheck = wx.CheckBox(self, id=107)
##        self.controllerPortCheck.SetValue(True)
##        self.macAddrCheck = wx.CheckBox(self, id=108)
##        self.macAddrCheck.SetValue(True)
##        self.pumpIdCheck = wx.CheckBox(self, id=109)
##        self.pumpIdCheck.SetValue(True)

        self.CheckAllBox = wx.CheckBox(self)
        self.CheckAllBox.SetValue(True)
        self.CheckAllBox.Bind(wx.EVT_CHECKBOX, self.onCheckAllBox)

        self.ComDropdown = wx.Choice(self)
        self.ComDropdown.AppendItems(strings=self.ComList)
        self.ComDropdown.SetFont(labelFont)
        self.ComDropdown.SetSelection(0)
        
        self.CheckBoxList = []
        for i in range(100,110):
            checkbox = wx.CheckBox(self, id=i)
            self.CheckBoxList.append(checkbox)
            checkbox.SetValue(True)
            wx.EVT_CHECKBOX(self, i, self.EnableEntry)
            
        self.LabelList = []
##        self.LabelList.append(wx.StaticText(self, label="IP Address"))
##        self.LabelList.append(wx.StaticText(self, label="Datalog Server IP Address"))
##        self.LabelList.append(wx.StaticText(self, label="Pump Controller IP Address"))
##        self.LabelList.append(wx.StaticText(self, label="Network Mask"))
##        self.LabelList.append(wx.StaticText(self, label="Default Gateway"))
##        self.LabelList.append(wx.StaticText(self, label="Listen Port"))
##        self.LabelList.append(wx.StaticText(self, label="Debug Server Port"))
##        self.LabelList.append(wx.StaticText(self, label="Pump Controller Port"))
##        self.LabelList.append(wx.StaticText(self, label="MAC Address"))
##        self.LabelList.append(wx.StaticText(self, label="Pump ID"))
##        self.LabelList.append(wx.StaticText(self, label="Distance to Ground"))
##        self.LabelList.append(wx.StaticText(self, label="Current Transducer Value"))
        for x in self.LabelNames:
            label = wx.StaticText(self, label=x)
            label.SetFont(labelFont)
            self.LabelList.append(label)
            
##        self.ipTextCtrl = wx.TextCtrl(self, id=200)
##        self.datalogIpTextCtrl = wx.TextCtrl(self, id=201)
##        self.controllerIpTextCtrl = wx.TextCtrl(self, id=202)
##        self.networkMaskTextCtrl = wx.TextCtrl(self, id=203)
##        self.defaultGatewayTextCtrl = wx.TextCtrl(self, id=204)
##        self.listenPortTextCtrl = wx.TextCtrl(self, id=205)
##        self.debugPortTextCtrl = wx.TextCtrl(self, id=206)
##        self.controllerPortTextCtrl = wx.TextCtrl(self, id=207)
##        self.macAddrTextCtrl = wx.TextCtrl(self, id=208)
##        self.pumpIdTextCtrl = wx.TextCtrl(self, id=209)
##        self.distanceToGroundTextCtrl = wx.TextCtrl(self, id=210, style=wx.TE_READONLY)
##        self.currentTransducerTextCtrl = wx.TextCtrl(self, id=211, style=wx.TE_READONLY)

        self.TextCtrlList = []
        for i in range(300,310):
            textbox = wx.TextCtrl(self, id=i, size=wx.Size(200,-1))
            self.TextCtrlList.append(textbox)
            textbox.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.TextCtrlList.append(wx.TextCtrl(self, id=210, style=wx.TE_READONLY))
        self.TextCtrlList.append(wx.TextCtrl(self, id=211, style=wx.TE_READONLY))
        for x in self.TextCtrlList:
            x.SetFont(textBoxFont)
        self.ResetTextCtrls()

##        self.ipUD = wx.SpinButton(self, id=300, style=wx.SP_VERTICAL)
##        self.datalogIpUD = wx.SpinButton(self, id=301, style=wx.SP_VERTICAL)
##        self.controllerIpUD = wx.SpinButton(self, id=302, style=wx.SP_VERTICAL)
##        self.networkMaskUD = wx.SpinButton(self, id=303, style=wx.SP_VERTICAL)
##        self.defaultGatewayUD = wx.SpinButton(self, id=304, style=wx.SP_VERTICAL)
##        self.listenPortUD = wx.SpinButton(self, id=305, style=wx.SP_VERTICAL)
##        self.debugPortUD = wx.SpinButton(self, id=306, style=wx.SP_VERTICAL)
##        self.controllerPortUD = wx.SpinButton(self, id=307, style=wx.SP_VERTICAL)
##        self.macAddrUD = wx.SpinButton(self, id=308, style=wx.SP_VERTICAL)
##        self.pumpIdUD = wx.SpinButton(self, id=309, style=wx.SP_VERTICAL)

        self.UpDownList = []
        for i in range(400,405):
            self.UpDownList.append(wx.SpinButton(self, id=i, style=wx.SP_HORIZONTAL, size=wx.Size(70,39)))
            wx.EVT_SPIN_UP(self, i, self.OnUpIP)
            wx.EVT_SPIN_DOWN(self, i, self.OnDownIP)
        for i in range(405,408):
            self.UpDownList.append(wx.SpinButton(self, id=i, style=wx.SP_HORIZONTAL, size=wx.Size(70,39)))
            wx.EVT_SPIN_UP(self, i, self.OnUpNum)
            wx.EVT_SPIN_DOWN(self, i, self.OnDownNum)
        self.UpDownList.append(wx.SpinButton(self, id=408, style=wx.SP_HORIZONTAL, size=wx.Size(70,39)))
        wx.EVT_SPIN_UP(self, 408, self.OnUpMAC)
        wx.EVT_SPIN_DOWN(self, 408, self.OnDownMAC)
        self.UpDownList.append(wx.SpinButton(self, id=409, style=wx.SP_HORIZONTAL, size=wx.Size(70,39)))
        wx.EVT_SPIN_UP(self, 409, self.OnUpNum)
        wx.EVT_SPIN_DOWN(self, 409, self.OnDownNum)


##        grid = wx.GridBagSizer(hgap=5, vgap=5)
##        for i in range(len(self.CheckBoxList)):
##            grid.Add(self.CheckBoxList[i], pos=(i,0), flag=wx.EXPAND|wx.ALL)
##        grid.Add(wx.StaticText(self, label="IP Address"), pos=(0,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
##        grid.Add(wx.StaticText(self, label="Datalog Server\nIP Address"), pos=(1,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
##        grid.Add(wx.StaticText(self, label="Pump Controller\nIP Address"), pos=(2,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
##        grid.Add(wx.StaticText(self, label="Network Mask"), pos=(3,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
##        grid.Add(wx.StaticText(self, label="Default Gateway"), pos=(4,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
##        grid.Add(wx.StaticText(self, label="Listen Port"), pos=(5,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
##        grid.Add(wx.StaticText(self, label="Debug Server Port"), pos=(6,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
##        grid.Add(wx.StaticText(self, label="Pump Controller Port"), pos=(7,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
##        grid.Add(wx.StaticText(self, label="MAC Address"), pos=(8,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
##        grid.Add(wx.StaticText(self, label="Pump ID"), pos=(9,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
##        grid.Add(wx.StaticText(self, label="Distance to Ground"), pos=(10,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
##        grid.Add(wx.StaticText(self, label="Current Transducer\nValue"), pos=(11,1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL)
##        for i in range(len(self.TextCtrlList)):
##            grid.Add(self.TextCtrlList[i], pos=(i,2), flag=wx.EXPAND|wx.ALL)
##        for i in range(len(self.UpDownList)):
##            grid.Add(self.UpDownList[i], pos=(i,2), flag=wx.EXPAND|wx.ALL)

            
        grid1 = wx.FlexGridSizer(rows=12, cols=4)
        grid1.Add(self.CheckAllBox, 1, wx.EXPAND)
        grid1.Add(wx.StaticText(self, label=""), 1, wx.EXPAND)
        grid1.Add(self.ComDropdown, 0, wx.ALL, 3)
        grid1.Add(wx.StaticText(self, label=""), 1, wx.EXPAND)
        # Add edittable fields to grid
        for i in range(10):
            grid1.Add(self.CheckBoxList[i], 1, wx.EXPAND)
            grid1.Add(self.LabelList[i], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
            grid1.Add(self.TextCtrlList[i], 1, wx.EXPAND | wx.ALL, 3)
            grid1.Add(self.UpDownList[i], 1, wx.EXPAND)
        # Add read-only fields to grid
        for i in range(10,12):
            grid1.Add(wx.StaticText(self, label=""), 1, wx.EXPAND)
            grid1.Add(self.LabelList[i], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
            grid1.Add(self.TextCtrlList[i], 1, wx.EXPAND | wx.ALL, 3)
            grid1.Add(wx.StaticText(self, label=""), 1, wx.EXPAND)


            
##        grid.AddMany([(self.CheckBoxList[0], 1, wx.EXPAND),
##                      (self.LabelList[0], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
##                      (self.TextCtrlList[0], 1, wx.EXPAND | wx.ALL, 3),
##                      (self.UpDownList[0], 1, wx.EXPAND),
##                      (self.CheckBoxList[1], 1, wx.EXPAND),
##                      (self.LabelList[1], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
##                      (self.TextCtrlList[1], 1, wx.EXPAND | wx.ALL, 3),
##                      (self.UpDownList[1], 1, wx.EXPAND),
##                      (self.CheckBoxList[2], 1, wx.EXPAND),
##                      (self.LabelList[2], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
##                      (self.TextCtrlList[2], 1, wx.EXPAND | wx.ALL, 3),
##                      (self.UpDownList[2], 1, wx.EXPAND),
##                      (self.CheckBoxList[3], 1, wx.EXPAND),
##                      (self.LabelList[3], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
##                      (self.TextCtrlList[3], 1, wx.EXPAND | wx.ALL, 3),
##                      (self.UpDownList[3], 1, wx.EXPAND),
##                      (self.CheckBoxList[4], 1, wx.EXPAND),
##                      (self.LabelList[4], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
##                      (self.TextCtrlList[4], 1, wx.EXPAND | wx.ALL, 3),
##                      (self.UpDownList[4], 1, wx.EXPAND),
##                      (self.CheckBoxList[5], 1, wx.EXPAND),
##                      (self.LabelList[5], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
##                      (self.TextCtrlList[5], 1, wx.EXPAND | wx.ALL, 3),
##                      (self.UpDownList[5], 1, wx.EXPAND),
##                      (self.CheckBoxList[6], 1, wx.EXPAND),
##                      (self.LabelList[6], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
##                      (self.TextCtrlList[6], 1, wx.EXPAND | wx.ALL, 3),
##                      (self.UpDownList[6], 1, wx.EXPAND),
##                      (self.CheckBoxList[7], 1, wx.EXPAND),
##                      (self.LabelList[7], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
##                      (self.TextCtrlList[7], 1, wx.EXPAND | wx.ALL, 3),
##                      (self.UpDownList[7], 1, wx.EXPAND),
##                      (self.CheckBoxList[8], 1, wx.EXPAND | wx.ALL, 3),
##                      (self.LabelList[8], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
##                      (self.TextCtrlList[8], 1, wx.EXPAND | wx.ALL, 3),
##                      (self.UpDownList[8], 1, wx.EXPAND),
##                      (self.CheckBoxList[9], 1, wx.EXPAND),
##                      (self.LabelList[9], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
##                      (self.TextCtrlList[9], 1, wx.EXPAND | wx.ALL, 3),
##                      (self.UpDownList[9], 1, wx.EXPAND),
##                      (wx.StaticText(self, label=""), 1, wx.EXPAND),
##                      (self.LabelList[10], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
##                      (self.TextCtrlList[10], 1, wx.EXPAND),
##                      (wx.StaticText(self, label=""), 1, wx.EXPAND),
##                      (wx.StaticText(self, label=""), 1, wx.EXPAND),
##                      (self.LabelList[11], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3),
##                      (self.TextCtrlList[11], 1, wx.EXPAND) ])

        self.NumButtons = []
        # 0-9 = 0-9
        # 10-15 = a-f
        # 16 = ./-
        # 17 = Backspace
        # 18 = Clear
        for i in range(500,516):
            button = wx.Button(self, id=i, label=hex(i-500)[2:].upper(), size=wx.Size(60,40))
            self.NumButtons.append(button)
        self.NumButtons.append(wx.Button(self, id=516, label='./-', size=wx.Size(60,40)))
        self.NumButtons.append(wx.Button(self, id=517, label='Backspace', size=wx.Size(60,40)))
        self.NumButtons.append(wx.Button(self, id=518, label='Clear', size=wx.Size(60,40)))
        for i in range(19):
            self.NumButtons[i].SetFont(buttonFont)
            self.NumButtons[i].Bind(wx.EVT_BUTTON, self.OnNumButtonPress)

        ResetButton = wx.Button(self, label="Reset All Values", size=wx.Size(60,40))
        ResetButton.SetFont(buttonFont)
        ResetButton.Bind(wx.EVT_BUTTON, self.OnResetPress)
        GetButton = wx.Button(self, label="Get Current Values", size=wx.Size(60,40))
        GetButton.SetFont(buttonFont)
        GetButton.Bind(wx.EVT_BUTTON, self.OnGetPress)
        CalibrateButton = wx.Button(self, label="Calibrate Distance To Ground", size=wx.Size(60,40))
        CalibrateButton.SetFont(buttonFont)
        CalibrateButton.Bind(wx.EVT_BUTTON, self.OnCalibratePress)
        SubmitButton = wx.Button(self, label="Submit", size=wx.Size(60,40))
        SubmitButton.SetFont(buttonFont)
        SubmitButton.Bind(wx.EVT_BUTTON, self.OnSubmitPress)

        grid2 = wx.GridBagSizer(hgap=5, vgap=5)
        grid2.Add(self.NumButtons[7], pos=(0,0), flag=wx.EXPAND, border=5)
        grid2.Add(self.NumButtons[8], pos=(0,1), flag=wx.EXPAND, border=5)
        grid2.Add(self.NumButtons[9], pos=(0,2), flag=wx.EXPAND, border=5)
        grid2.Add(self.NumButtons[4], pos=(1,0), flag=wx.EXPAND, border=5)
        grid2.Add(self.NumButtons[5], pos=(1,1), flag=wx.EXPAND, border=5)
        grid2.Add(self.NumButtons[6], pos=(1,2), flag=wx.EXPAND, border=5)
        grid2.Add(self.NumButtons[1], pos=(2,0), flag=wx.EXPAND, border=5)
        grid2.Add(self.NumButtons[2], pos=(2,1), flag=wx.EXPAND, border=5)
        grid2.Add(self.NumButtons[3], pos=(2,2), flag=wx.EXPAND, border=5)
        grid2.Add(self.NumButtons[0], pos=(3,0), span=(1,2), flag=wx.EXPAND, border=5)
        grid2.Add(self.NumButtons[16], pos=(3,2), flag=wx.EXPAND, border=5) # ./-
        grid2.Add(self.NumButtons[17], pos=(4,0), span=(1,3), flag=wx.EXPAND, border=5) # Backspace
        grid2.Add(self.NumButtons[18], pos=(5,0), span=(1,3), flag=wx.EXPAND, border=5) # Clear
        grid2.Add(self.NumButtons[10], pos=(0,3), flag=wx.EXPAND, border=5) # a
        grid2.Add(self.NumButtons[11], pos=(1,3), flag=wx.EXPAND, border=5) # b
        grid2.Add(self.NumButtons[12], pos=(2,3), flag=wx.EXPAND, border=5) # c
        grid2.Add(self.NumButtons[13], pos=(3,3), flag=wx.EXPAND, border=5) # d
        grid2.Add(self.NumButtons[14], pos=(4,3), flag=wx.EXPAND, border=5) # e
        grid2.Add(self.NumButtons[15], pos=(5,3), flag=wx.EXPAND, border=5) # f
        grid2.Add(wx.StaticText(self, label=""), pos=(6,0), flag=wx.ALL, border=10)
        grid2.Add(ResetButton, pos=(7,0), span=(1,4), flag=wx.EXPAND, border=5)
        grid2.Add(GetButton, pos=(8,0), span=(1,4), flag=wx.EXPAND, border=5)
        grid2.Add(CalibrateButton, pos=(9,0), span=(1,4), flag=wx.EXPAND, border=5)
        grid2.Add(wx.StaticText(self, label=""), pos=(10,0), flag=wx.ALL, border=0)
        grid2.Add(SubmitButton, pos=(11,0), span=(1,4), flag=wx.EXPAND, border=5) # Clear
        
        # Use some sizers to see layout options
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.SetMinSize((-1,200))
        sizer.Add(grid1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, border=5)
        sizer.Add(wx.StaticText(self, label=" "), 1, wx.EXPAND)
        sizer.Add(grid2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, border=10)
        
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)

        self.NON_TARGET_COLOR = self.TextCtrlList[1].GetBackgroundColour()  # Save current default color for text boxes
        self.TextCtrlList[0].SetBackgroundColour(self.TARGET_COLOR)         # Set bg color on IP Address box
        self.TextCtrlList[0].SelectAll()                                    # Select All in IP Address box

    def onCheckAllBox(self, event):
        for i in range(len(self.CheckBoxList)):
            self.CheckBoxList[i].SetValue(event.Checked())
            if (event.Checked()):
                self.TextCtrlList[i].Enable()
                self.UpDownList[i].Enable()
            else:
                self.TextCtrlList[i].Disable()
                self.UpDownList[i].Disable()
    
    def EnableEntry(self, event):
        if (event.Checked()):
            self.TextCtrlList[event.GetId() - 100].Enable()
            self.UpDownList[event.GetId() - 100].Enable()
        else:
            self.TextCtrlList[event.GetId() - 100].Disable()
            self.UpDownList[event.GetId() - 100].Disable()

    def OnUpIP(self, event):
        textctrl = self.TextCtrlList[event.GetId() - 400]
        octets = re.split("\.", textctrl.GetValue())
        try:
            octets[3] = str((int(octets[3])+1)%256)
        except:
            self.output.AppendText("Invalid entry in field '"+self.LabelNames[event.GetId()-400]+"'\n")
        else:
            textctrl.SetValue(octets[0]+'.'+octets[1]+'.'+octets[2]+'.'+octets[3])

    def OnDownIP(self, event):
        textctrl = self.TextCtrlList[event.GetId() - 400]
        octets = re.split("\.", textctrl.GetValue())
        try:
            octets[3] = str((int(octets[3])-1)%256)
        except:
            self.output.AppendText("Invalid entry in field '"+self.LabelNames[event.GetId()-400]+"'\n")
        else:
            textctrl.SetValue(octets[0]+'.'+octets[1]+'.'+octets[2]+'.'+octets[3])

    def OnUpMAC(self, event):
        textctrl = self.TextCtrlList[event.GetId() - 400]
        try:
            address = long(''.join(re.split("\-", textctrl.GetValue())),16)
        except:
            self.output.AppendText("Invalid entry in field '"+self.LabelNames[event.GetId()-400]+"'\n")
        else:
            address = ('%012X' % ((address + 1) % 281474976710656)) # FF-FF-FF-FF-FF-FF modulos to 00-00-00-00-00-00
            textctrl.SetValue(address[0]+address[1]+"-"+address[2]+address[3]+"-"+address[4]+address[5]+"-"+
                              address[6]+address[7]+"-"+address[8]+address[9]+"-"+address[10]+address[11])

    def OnDownMAC(self, event):
        textctrl = self.TextCtrlList[event.GetId() - 400]
        try:
            address = long(''.join(re.split("\-", textctrl.GetValue())),16)
        except:
            self.output.AppendText("Invalid entry in field '"+self.LabelNames[event.GetId()-400]+"'\n")
        else:
            address = ('%012X' % ((address - 1) % 281474976710656)) # FF-FF-FF-FF-FF-FF modulos to 00-00-00-00-00-00
            textctrl.SetValue(address[0]+address[1]+"-"+address[2]+address[3]+"-"+address[4]+address[5]+"-"+
                              address[6]+address[7]+"-"+address[8]+address[9]+"-"+address[10]+address[11])

    def OnUpNum(self, event):
        textctrl = self.TextCtrlList[event.GetId() - 400]
        if not (textctrl.GetValue()):
            textctrl.SetValue(str(0))
        else:
            textctrl.SetValue(str(int(textctrl.GetValue()) + 1))

    def OnDownNum(self, event):
        textctrl = self.TextCtrlList[event.GetId() - 400]
        if not (textctrl.GetValue()):
            textctrl.SetValue(str(0))
        elif (int(textctrl.GetValue()) > 0):
            textctrl.SetValue(str(int(textctrl.GetValue()) - 1))

    def OnGainFocusTB(self, event):
        textnum = event.GetId() - 300
        if not (self.TargetTextCtrl == textnum):
            self.TextCtrlList[self.TargetTextCtrl].SetBackgroundColour(self.NON_TARGET_COLOR)
            self.TextCtrlList[textnum].SetBackgroundColour(self.TARGET_COLOR)
            self.Refresh()
            self.TargetTextCtrl = textnum
            wx.CallAfter(self.TextCtrlList[textnum].SelectAll)
        
##    def OnLoseFocusMAC(self, event):
##        pass

    def OnNumButtonPress(self, event):
        textbox = self.TextCtrlList[self.TargetTextCtrl]
        if (event.GetId() < 516):
            textbox.WriteText(str(event.GetEventObject().GetLabel()))
        elif (event.GetId() == 516):
            if (self.TargetTextCtrl < 5):
                textbox.WriteText(".")
            elif (self.TargetTextCtrl == 8):
                textbox.WriteText("-")
        elif (event.GetId() == 517):
            to = textbox.GetInsertionPoint()
            frm = to - 1
            #self.output.AppendText("({0}, {1})\n".format(frm, to))
            if (to > 0):
                textbox.Remove(frm, to) # Backspace ASCII character
        elif (event.GetId() == 518):
            textbox.Clear()
        else:
            return

    def OnResetPress(self, event):
        self.ResetTextCtrls()
    
    def ResetTextCtrls(self):
        self.TextCtrlList[0].SetValue("0.0.0.0")
        self.TextCtrlList[1].SetValue("0.0.0.0")
        self.TextCtrlList[2].SetValue("0.0.0.0")
        self.TextCtrlList[3].SetValue("0.0.0.0")
        self.TextCtrlList[4].SetValue("0.0.0.0")
        self.TextCtrlList[5].SetValue("0")
        self.TextCtrlList[6].SetValue("0")
        self.TextCtrlList[7].SetValue("0")
        self.TextCtrlList[8].SetValue("FF-FF-FF-FF-FF-FF")
        self.TextCtrlList[9].SetValue("0")
        self.TextCtrlList[10].SetValue("0")
        self.TextCtrlList[11].SetValue("0")

    def OnGetPress(self, event):
        settings = self.ReqSettings()
        if (settings):
            for i in range(len(settings)):
                try:
                    if (i == 8):
                        address = settings[i]
                        self.TextCtrlList[i].SetValue(address[0]+address[1]+"-"+address[2]+address[3]+"-"+address[4]+address[5]+"-"+
                                                      address[6]+address[7]+"-"+address[8]+address[9]+"-"+address[10]+address[11])
                    else:
                        self.TextCtrlList[i].SetValue(settings[i])
                except:
                    self.output.AppendText("{0} value couldn't be retrieved: Invalid data\n".format(self.LabelNames[i]))

    def OnCalibratePress(self, event):
        if (self.Calibrate()):
            self.output.AppendText("Pump board calibrated successfully!\n")
            self.OnGetPress(None)
        else:
            self.output.AppendText("Calibration failed.\n")

    def OnSubmitPress(self, event):
        if (self.CheckFields()):
            settings = []
            for i in range(10):
                if self.CheckBoxList[i].IsChecked():
                    if (i == 8):
                        mac = str(self.TextCtrlList[i].GetValue()).replace("-", "")
                        settings.append(mac[6:])
                        settings.append(mac[:6])
                    else:
                        settings.append(str(self.TextCtrlList[i].GetValue()))
                else:
                    settings.append("")
            self.output.AppendText("Provisioning device...\n")
            for x in settings:
                self.output.AppendText(x+"\n")
            if (self.Submit(settings)):
                self.output.AppendText("Done!\n\n")
            else:
                self.output.AppendText("Provisioning attempt failed.\n\n")
        else:
            self.output.AppendText("Board not provisioned. Found some fields with invalid values.\n\n")

    def CheckFields(self):
        ERROR_MESSAGE = "Invalid value in {0} field.\n"
        NoErrors = True
        # Checking IP fields
        for i in range(5):
            if self.CheckBoxList[i].IsChecked():
                try:
                    octets = re.split("\.", self.TextCtrlList[i].GetValue())
                    a = int(octets[0])
                    b = int(octets[1])
                    c = int(octets[2])
                    d = int(octets[3])
                except:
                    self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[i]))
                    self.TextCtrlList[i].SetBackgroundColour(self.ERROR_COLOR)
                    NoErrors = False
                else:
                    if (a < 0 or b < 0 or c < 0 or d < 0 or
                        a > 255 or b > 255 or c > 255 or d > 255):
                        self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[i]))
                        self.TextCtrlList[i].SetBackgroundColour(self.ERROR_COLOR)
                        NoErrors = False
                    else:
                        if (i == self.TargetTextCtrl):
                           self.TextCtrlList[i].SetBackgroundColour(self.TARGET_COLOR)
                        else:
                           self.TextCtrlList[i].SetBackgroundColour(self.NON_TARGET_COLOR)
        # Checking port and lane number fields
        for i in [5, 6, 7, 9]:
            if self.CheckBoxList[i].IsChecked():
                try:
                    a = int(self.TextCtrlList[i].GetValue())
                except:
                    self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[i]))
                    self.TextCtrlList[i].SetBackgroundColour(self.ERROR_COLOR)
                    NoErrors = False
                else:
                    if (a < 0 or a > 65535):
                        self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[i]))
                        self.TextCtrlList[i].SetBackgroundColour(self.ERROR_COLOR)
                        NoErrors = False
                    else:
                        if (i == self.TargetTextCtrl):
                           self.TextCtrlList[i].SetBackgroundColour(self.TARGET_COLOR)
                        else:
                           self.TextCtrlList[i].SetBackgroundColour(self.NON_TARGET_COLOR)
        # Checking MAC address
        if self.CheckBoxList[8].IsChecked():
            try:
                address = ''.join(re.split("\-", self.TextCtrlList[8].GetValue()))
                address_long = long(address,16)
            except:
                self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[8]))
                self.TextCtrlList[8].SetBackgroundColour(self.ERROR_COLOR)
                NoErrors = False
            else:
                if (not (len(address) == 12) or (address_long < 0) or (address_long > int("FFFFFFFFFFFF",16))):
                    self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[8]))
                    self.TextCtrlList[8].SetBackgroundColour(self.ERROR_COLOR)
                    NoErrors = False
                else:
                    if (8 == self.TargetTextCtrl):
                       self.TextCtrlList[8].SetBackgroundColour(self.TARGET_COLOR)
                    else:
                       self.TextCtrlList[8].SetBackgroundColour(self.NON_TARGET_COLOR)

        self.Refresh()
        return NoErrors

    # self.ComList[self.ComDropdown.GetSelection()]

    def ReqSettings(self):
        return ['10.0.2.5', '64.14.130.116', '10.0.2.61', '255.255.0.0', '10.0.0.1',
                '7879', '9829', '6627', '64FC8C100027', '262', '301', '191']

    def Calibrate(self):
        return True

    def Submit(self, settings):
        return True

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="ZCon Tools", style=wx.MINIMIZE_BOX|wx.RESIZE_BORDER|
                          wx.SYSTEM_MENU|wx.CAPTION|wx.CLOSE_BOX|wx.CLIP_CHILDREN)
        self.SetMinSize(wx.Size(800,800))
        self.SetMaxSize(wx.Size(800,-1))
        self.SetSize(wx.Size(-1,800))

        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        self.tb = wx.TextCtrl(p, style=wx.TE_MULTILINE | wx.TE_READONLY)
        page1 = ProvisionTab(nb, self.tb)
        page2 = TestTab(nb, self.tb)
        ClearButton = wx.Button(p, label="Clear Screen")
        ClearButton.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.Bind(wx.EVT_BUTTON, self.ClearScreen, ClearButton)

        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Provisioning Tool")
        nb.AddPage(page2, "Gbat/IR tester")

        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 0, wx.EXPAND)
        sizer.Add(self.tb, 1, wx.EXPAND)
        sizer.Add(ClearButton, 0, wx.ALIGN_RIGHT)
        p.SetSizer(sizer)
        self.Center()

    def ClearScreen(self, event):
        self.tb.Clear()

class MyTextCtrl(wx.TextCtrl):

    def addtext(self, text):
        self.AppendText(text)
        

if __name__ == "__main__":
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()
