import wx, re, serial, time, os
from CPS import ComPortSelector

DEBUG = True
TITLE = "Z-Con Pump Provisioning Tool"

class ProvisionTab(wx.Panel):

    LabelNames = [ "IP Address", "Datalog Server IP Address", "NexGen IP Address",
                   "Network Mask", "Default Gateway", "Listen Port", "Debug Server Port",
                   "NexGen Port", "Pump ID", "Firmware Update IP", "MAC Address", 
                   "Distance to Ground", "Current Transducer Value" ]
#    TargetTextCtrl = 0 # Initialize with IP Address TextCtrl having target
    NON_TARGET_COLOR = "White"
#    TARGET_COLOR = (255, 255, 175, 255) # Pale Yellow
    ERROR_COLOR = (255, 50, 50, 255) # Pale Red
#    ComList = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM10", "COM11",
#               "COM12", "COM13", "COM14", "COM15", "COM16", "COM17", "COM18", "COM19", "COM20"]
    filename = 'settings.prov'
    dirname = ''
    RecallSettings = ["0.0.0.0", "0.0.0.0", "0.0.0.0", "0.0.0.0", "0.0.0.0", "0", "0", "0", "0"]
    
    def __init__(self, parent, output, frame):
        wx.Panel.__init__(self, parent)

        self.output = output
        self.frame = frame

#        labelFont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        textBoxFont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
#        buttonFont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        # ID namespace
        # 100 = CheckBox
        # 200 = StaticText
        # 300 = TextCtrl
        # 400 = SpinButton
        # 500 = Button

        self.CheckAllBox = wx.CheckBox(self)
        self.CheckAllBox.SetValue(True)
        self.CheckAllBox.Bind(wx.EVT_CHECKBOX, self.onCheckAllBox)

        self.ComDropdown = ComPortSelector(self)
#        self.ComDropdown = wx.Choice(self)
#        self.ComDropdown.AppendItems(strings=self.ComList)
#        self.ComDropdown.SetFont(labelFont)
        #self.ComDropdown.SetSelection(0)
        
        self.CheckBoxList = []
        for i in range(100, 110):
            checkbox = wx.CheckBox(self, id=i)
            self.CheckBoxList.append(checkbox)
            checkbox.SetValue(True)
            wx.EVT_CHECKBOX(self, i, self.EnableEntry)
            
        self.LabelList = []

        for x in self.LabelNames:
            label = wx.StaticText(self, label=x)
#            label.SetFont(labelFont)
            self.LabelList.append(label)
            
        self.TextCtrlList = []
        for i in range(300, 310):
            textbox = wx.TextCtrl(self, id=i, size=wx.Size(140,-1))
            textbox.SetFont(textBoxFont)
            self.TextCtrlList.append(textbox)
            textbox.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        for i in range(310, 313):
            self.TextCtrlList.append(wx.TextCtrl(self, id=i, style=wx.TE_READONLY))
#        for x in self.TextCtrlList:
#            x.SetFont(textBoxFont)
        self.ResetTextCtrls()

        self.UpDownList = []
        for i in range(400, 405):
            self.UpDownList.append(wx.SpinButton(self, id=i, style=wx.SP_VERTICAL))
            wx.EVT_SPIN_UP(self, i, self.OnUpIP)
            wx.EVT_SPIN_DOWN(self, i, self.OnDownIP)
        for i in range(405, 409):
            self.UpDownList.append(wx.SpinButton(self, id=i, style=wx.SP_VERTICAL))
            wx.EVT_SPIN_UP(self, i, self.OnUpNum)
            wx.EVT_SPIN_DOWN(self, i, self.OnDownNum)
        self.UpDownList.append(wx.SpinButton(self, id=410, style=wx.SP_VERTICAL))
        wx.EVT_SPIN_UP(self, 410, self.OnUpIP)
        wx.EVT_SPIN_DOWN(self, 410, self.OnDownIP)
#        self.UpDownList.append(wx.SpinButton(self, id=408, style=wx.SP_VERTICAL))
#        wx.EVT_SPIN_UP(self, 408, self.OnUpMAC)
#        wx.EVT_SPIN_DOWN(self, 408, self.OnDownMAC)
#        self.UpDownList.append(wx.SpinButton(self, id=409, style=wx.SP_HORIZONTAL, size=wx.Size(70, 39)))
#        wx.EVT_SPIN_UP(self, 409, self.OnUpNum)
#        wx.EVT_SPIN_DOWN(self, 409, self.OnDownNum)

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
        for i in range(10, 13):
            grid1.Add(wx.StaticText(self, label=""), 1, wx.EXPAND)
            grid1.Add(self.LabelList[i], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
            grid1.Add(self.TextCtrlList[i], 1, wx.EXPAND | wx.ALL, 3)
            grid1.Add(wx.StaticText(self, label=""), 1, wx.EXPAND)

#        self.NumButtons = []
        # 0-9 = 0-9
        # 10-15 = a-f
        # 16 = ./-
        # 17 = Backspace
        # 18 = Clear
#        for i in range(500, 516):
#            button = wx.Button(self, id=i, label=hex(i - 500)[2:].upper(), size=wx.Size(60, 40))
#            self.NumButtons.append(button)
#        self.NumButtons.append(wx.Button(self, id=516, label='./-', size=wx.Size(60, 40)))
#        self.NumButtons.append(wx.Button(self, id=517, label='Backspace', size=wx.Size(60, 40)))
#        self.NumButtons.append(wx.Button(self, id=518, label='Clear', size=wx.Size(60, 40)))
#        for i in range(19):
#            self.NumButtons[i].SetFont(buttonFont)
#            self.NumButtons[i].Bind(wx.EVT_BUTTON, self.OnNumButtonPress)
        
        LoadButton = wx.Button(self, label="Load Provision file...")
        LoadButton.Bind(wx.EVT_BUTTON, self.OnLoadPress)
        SaveButton = wx.Button(self, label="Save Provision file...")
        SaveButton.Bind(wx.EVT_BUTTON, self.OnSavePress)
        
        ResetButton = wx.Button(self, label="Reset All Values")
#        ResetButton.SetFont(buttonFont)
        ResetButton.Bind(wx.EVT_BUTTON, self.OnResetPress)
        GetButton = wx.Button(self, label="Get Current Values")
#        GetButton.SetFont(buttonFont)
        GetButton.Bind(wx.EVT_BUTTON, self.OnGetPress)
        RecallButton = wx.Button(self, label="Recall Last Submitted Values")
        RecallButton.Bind(wx.EVT_BUTTON, self.OnRecallPress)
        CalibrateButton = wx.Button(self, label="Calibrate Distance To Ground")
#        CalibrateButton.SetFont(buttonFont)
        CalibrateButton.Bind(wx.EVT_BUTTON, self.OnCalibratePress)
        SubmitButton = wx.Button(self, label="Submit")
#        SubmitButton.SetFont(buttonFont)
        SubmitButton.Bind(wx.EVT_BUTTON, self.OnSubmitPress)
        IncrementButton = wx.Button(self, label="Increment IP and Pump ID")
        IncrementButton.Bind(wx.EVT_BUTTON, self.OnIncrementPress)

#        grid2 = wx.GridBagSizer(hgap=5, vgap=5)
#        grid2.Add(self.NumButtons[7], pos=(0, 0), flag=wx.EXPAND, border=5)
#        grid2.Add(self.NumButtons[8], pos=(0, 1), flag=wx.EXPAND, border=5)
#        grid2.Add(self.NumButtons[9], pos=(0, 2), flag=wx.EXPAND, border=5)
#        grid2.Add(self.NumButtons[4], pos=(1, 0), flag=wx.EXPAND, border=5)
#        grid2.Add(self.NumButtons[5], pos=(1, 1), flag=wx.EXPAND, border=5)
#        grid2.Add(self.NumButtons[6], pos=(1, 2), flag=wx.EXPAND, border=5)
#        grid2.Add(self.NumButtons[1], pos=(2, 0), flag=wx.EXPAND, border=5)
#        grid2.Add(self.NumButtons[2], pos=(2, 1), flag=wx.EXPAND, border=5)
#        grid2.Add(self.NumButtons[3], pos=(2, 2), flag=wx.EXPAND, border=5)
#        grid2.Add(self.NumButtons[0], pos=(3, 0), span=(1, 2), flag=wx.EXPAND, border=5)
#        grid2.Add(self.NumButtons[16], pos=(3, 2), flag=wx.EXPAND, border=5) # ./-
#        grid2.Add(self.NumButtons[17], pos=(4, 0), span=(1, 3), flag=wx.EXPAND, border=5) # Backspace
#        grid2.Add(self.NumButtons[18], pos=(5, 0), span=(1, 3), flag=wx.EXPAND, border=5) # Clear
#        grid2.Add(self.NumButtons[10], pos=(0, 3), flag=wx.EXPAND, border=5) # a
#        grid2.Add(self.NumButtons[11], pos=(1, 3), flag=wx.EXPAND, border=5) # b
#        grid2.Add(self.NumButtons[12], pos=(2, 3), flag=wx.EXPAND, border=5) # c
#        grid2.Add(self.NumButtons[13], pos=(3, 3), flag=wx.EXPAND, border=5) # d
#        grid2.Add(self.NumButtons[14], pos=(4, 3), flag=wx.EXPAND, border=5) # e
#        grid2.Add(self.NumButtons[15], pos=(5, 3), flag=wx.EXPAND, border=5) # f
#        grid2.Add(wx.StaticText(self, label=""), pos=(6, 0), flag=wx.ALL, border=10)
#        grid2.Add(ResetButton, pos=(7, 0), span=(1, 4), flag=wx.EXPAND, border=5)
#        grid2.Add(GetButton, pos=(8, 0), span=(1, 4), flag=wx.EXPAND, border=5)
#        grid2.Add(CalibrateButton, pos=(9, 0), span=(1, 4), flag=wx.EXPAND, border=5)
#        grid2.Add(wx.StaticText(self, label=""), pos=(10, 0), flag=wx.ALL, border=0)
#        grid2.Add(SubmitButton, pos=(11, 0), span=(1, 4), flag=wx.EXPAND, border=5)
        
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer.Add(LoadButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(SaveButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(wx.StaticText(self, label=""), 1, flag=wx.ALL, border=0)
        buttonSizer.Add(ResetButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(GetButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(RecallButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(CalibrateButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(wx.StaticText(self, label=""), 1, flag=wx.ALL, border=0)
        buttonSizer.Add(SubmitButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(IncrementButton, 1, flag=wx.EXPAND, border=5)
        # Comment out below four lines for non-Zonar use
        if (DEBUG):
            MACButton = wx.Button(self, label="Change MAC (Admin only)")
            MACButton.Bind(wx.EVT_BUTTON, self.OnMACPress)
            buttonSizer.Add(wx.StaticText(self, label=""), 1, flag=wx.ALL, border=0)
            buttonSizer.Add(MACButton, 1, flag=wx.EXPAND, border=5)
        
        # Use some sizers to see layout options
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.SetMinSize((-1, 200))
        sizer.Add(grid1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, border=5)
        sizer.Add(wx.StaticText(self, label=" "), 1, wx.EXPAND)
        sizer.Add(buttonSizer, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, border=10)
        
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)

        # GUI has been loaded. Set variables
        self.NON_TARGET_COLOR = self.TextCtrlList[1].GetBackgroundColour()  # Save current default color for text boxes
#        self.TextCtrlList[0].SetBackgroundColour(self.TARGET_COLOR)         # Set bg color on IP Address box
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
        all = True
        for x in self.CheckBoxList:
            if not x.GetValue():
                all = False # If any box is unchecked, uncheck the CheckAll box
        self.CheckAllBox.SetValue(all)

    def OnUpIP(self, event):
        textctrl = self.TextCtrlList[event.GetId() - 400]
        octets = textctrl.GetValue().split(".")
        try:
            octets[3] = str((int(octets[3]) + 1) % 256)
        except:
            self.output.AppendText("Invalid entry in field '" + self.LabelNames[event.GetId() - 400] + "'\n")
            return False
        else:
            textctrl.SetValue(octets[0] + '.' + octets[1] + '.' + octets[2] + '.' + octets[3])
            return True

    def OnDownIP(self, event):
        textctrl = self.TextCtrlList[event.GetId() - 400]
        octets = textctrl.GetValue().split(".")
        try:
            octets[3] = str((int(octets[3]) - 1) % 256)
        except:
            self.output.AppendText("Invalid entry in field '" + self.LabelNames[event.GetId() - 400] + "'\n")
            return False
        else:
            textctrl.SetValue(octets[0] + '.' + octets[1] + '.' + octets[2] + '.' + octets[3])
            return True

#    def OnUpMAC(self, event):
#        textctrl = self.TextCtrlList[event.GetId() - 400]
#        try:
#            address = long(''.join(re.split("\-", textctrl.GetValue())), 16)
#        except:
#            self.output.AppendText("Invalid entry in field '" + self.LabelNames[event.GetId() - 400] + "'\n")
#        else:
#            address = ('%012X' % ((address + 1) % 0x1000000000000)) # FF-FF-FF-FF-FF-FF modulos to 00-00-00-00-00-00
#            textctrl.SetValue(address[0] + address[1] + "-" + address[2] + address[3] + "-" + address[4] + address[5] + "-" + 
#                              address[6] + address[7] + "-" + address[8] + address[9] + "-" + address[10] + address[11])
#
#    def OnDownMAC(self, event):
#        textctrl = self.TextCtrlList[event.GetId() - 400]
#        try:
#            address = long(''.join(re.split("\-", textctrl.GetValue())), 16)
#        except:
#            self.output.AppendText("Invalid entry in field '" + self.LabelNames[event.GetId() - 400] + "'\n")
#        else:
#            address = ('%012X' % ((address - 1) % 0x1000000000000)) # FF-FF-FF-FF-FF-FF modulos to 00-00-00-00-00-00
#            textctrl.SetValue(address[0] + address[1] + "-" + address[2] + address[3] + "-" + address[4] + address[5] + "-" + 
#                              address[6] + address[7] + "-" + address[8] + address[9] + "-" + address[10] + address[11])

    def OnUpNum(self, event):
        textctrl = self.TextCtrlList[event.GetId() - 400]
        if not (textctrl.GetValue()):
            textctrl.SetValue(str(0))
            return False
        else:
            textctrl.SetValue(str(int(textctrl.GetValue()) + 1))
            return True

    def OnDownNum(self, event):
        textctrl = self.TextCtrlList[event.GetId() - 400]
        if not (textctrl.GetValue()):
            textctrl.SetValue(str(0))
            return False
        elif (int(textctrl.GetValue()) > 0):
            textctrl.SetValue(str(int(textctrl.GetValue()) - 1))
            return True

    def OnGainFocusTB(self, event):
        textnum = event.GetId() - 300
#        if not (self.TargetTextCtrl == textnum):
#            self.TextCtrlList[self.TargetTextCtrl].SetBackgroundColour(self.NON_TARGET_COLOR)
#            self.TextCtrlList[textnum].SetBackgroundColour(self.TARGET_COLOR)
#            self.Refresh()
#            self.TargetTextCtrl = textnum
        wx.CallAfter(self.TextCtrlList[textnum].SelectAll)
        
#    def OnLoseFocusMAC(self, event):
#        pass

#    def OnNumButtonPress(self, event):
#        textbox = self.TextCtrlList[self.TargetTextCtrl]
#        if (event.GetId() < 516):
#            textbox.WriteText(str(event.GetEventObject().GetLabel()))
#        elif (event.GetId() == 516): # ./-
#            if (self.TargetTextCtrl < 5):
#                textbox.WriteText(".")
#            elif (self.TargetTextCtrl == 8):
#                textbox.WriteText("-")
#        elif (event.GetId() == 517): # Backspace
#            to = textbox.GetInsertionPoint()
#            frm = to - 1
#            #self.output.AppendText("({0}, {1})\n".format(frm, to))
#            if (to > 0):
#                textbox.Remove(frm, to)
#        elif (event.GetId() == 518): # Clear
#            textbox.Clear()
#        else:
#            return
    
    def OnLoadPress(self, event):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, self.filename, "*.prov", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            
            # Open the file, read the contents and set them into
            # the text edit window
            filehandle=open(os.path.join(self.dirname, self.filename),'r')
            try:
                list = eval(filehandle.read())
            except:
                self.output.AppendText("Unable to load {0}".format(self.dirname+"\\"+self.filename))
            else:
                for i in range(len(list)):
                    if not (list[i] == "DNL"):
                        self.TextCtrlList[i].SetValue(list[i])
            filehandle.close()
            
            # Later - could be enhanced to include a "changed" flag whenever
            # the text is actually changed, could also be altered on "save" ...
        dlg.Destroy()
        self.frame.SetTitle("{} - {}".format(TITLE,self.filename))
    
    def OnSavePress(self, event):
        # Save away the edited text
        # Open the file, do an RU sure check for an overwrite!
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, self.filename, "*.prov", \
                            wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
        # Grab the content to be saved
            list = []
            for i in range(len(self.CheckBoxList)):
                if self.CheckBoxList[i].IsChecked():
                    list.append(self.TextCtrlList[i].GetValue())
                else:
                    list.append("DNL") # If entry is unchecked, don't save
            
            # Open the file for write, write, close
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            filehandle=open(os.path.join(self.dirname, self.filename),'w')
            filehandle.write(repr(list))
            filehandle.close()
        # Get rid of the dialog to keep things tidy
        dlg.Destroy()
        self.frame.SetTitle("{} - {}".format(TITLE,self.filename))
    
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
        self.TextCtrlList[8].SetValue("0")
        self.TextCtrlList[9].SetValue("0.0.0.0")
        self.TextCtrlList[10].SetValue("FF-FF-FF-FF-FF-FF")
        self.TextCtrlList[11].SetValue("0")
        self.TextCtrlList[12].SetValue("0")

    def OnGetPress(self, event):
        if self.ComDropdown.GetValue() == "":
            self.output.AppendText("\nPlease set a valid Com port number.\n")
            return
        self.PopulateFields(self.ReqSettings())
        
    def OnRecallPress(self, event):
        self.PopulateFields(self.RecallSettings)
        
    def PopulateFields(self, settings):
        if (settings):
            for i in range(len(settings)):
                if (DEBUG):
                    self.output.AppendText("Parsing {0}...\n".format(self.LabelNames[i]))
                if not (settings[i] == "DNL"):
                    try:
                        if (i == 9):
                            address = settings[i]
                            self.TextCtrlList[i].SetValue(address[0] + address[1] + "-" + address[2] + address[3] + "-" + address[4] + address[5] + "-" + 
                                                          address[6] + address[7] + "-" + address[8] + address[9] + "-" + address[10] + address[11])
                        else:
                            self.TextCtrlList[i].SetValue(settings[i])
                    except:
                        self.output.AppendText("{0} value couldn't be retrieved: Invalid data\n".format(self.LabelNames[i]))

    def OnCalibratePress(self, event):
        if self.ComDropdown.GetValue() == "":
            self.output.AppendText("\nPlease set a valid Com port number.\n")
            return
        if (self.Calibrate()):
            self.OnGetPress(None)
            self.output.AppendText("Pump board calibrated successfully!\n")
        else:
            self.output.AppendText("Calibration failed.\n")

    def OnSubmitPress(self, event):
        if self.ComDropdown.GetValue() == "":
            self.output.AppendText("\nPlease set a valid Com port number.\n")
            return
        if (self.CheckFields()):
            settings = []
            for i in range(9):
                if self.CheckBoxList[i].IsChecked():
                    settings.append(str(self.TextCtrlList[i].GetValue()))
                    self.RecallSettings[i] = str(self.TextCtrlList[i].GetValue())
                else:
                    settings.append("DNL")
#                self.output.AppendText("Provisioning device...\n")
#                for x in settings:
#                    self.output.AppendText(x + "\n")
            self.Submit(settings)
        else:
            self.output.AppendText("\nBoard not provisioned. Found some fields with invalid values.\n\n")
            
    def OnIncrementPress(self, event):
        event.SetId(400) # Spoof the IP Address SpinButton
        if (self.OnUpIP(event)):
            event.SetId(408) # Spoof the Pump ID SpinButton
            self.OnUpNum(event)
            
    def OnMACPress(self, event):
        try:
            address = ''.join(self.TextCtrlList[9].GetValue().split("-"))
            address_long = long(address, 16)
        except:
            self.output.AppendText("\nBad MAC Address\n")
        else:
            if (not (len(address) == 12) or (address_long < 0) or (address_long > int("FFFFFFFFFFFF", 16))):
                self.output.AppendText("\nBad MAC Address\n")
            else:
                MACAddressChanger(self).Show()

    def CheckFields(self):
        ERROR_MESSAGE = "Invalid value in {0} field.\n"
        NoErrors = True
        # Checking IP fields
        for i in [range(5), 10]:
            if self.CheckBoxList[i].IsChecked():
                try:
                    octets = self.TextCtrlList[i].GetValue().split('.')
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
                        a > 255 or b > 255 or c > 255 or d > 255) or (      # If invalid IP or 
                        a == 0 and b == 0 and c == 0 and d == 0) or (       # 0.0.0.0 or
                        a == 255 and b == 255 and c == 255 and d == 255):           # 255.255.255.255
                        self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[i]))
                        self.TextCtrlList[i].SetBackgroundColour(self.ERROR_COLOR)
                        NoErrors = False
                    else:
#                        if (i == self.TargetTextCtrl):
#                            self.TextCtrlList[i].SetBackgroundColour(self.TARGET_COLOR)
#                        else:
                        self.TextCtrlList[i].SetBackgroundColour(self.NON_TARGET_COLOR)
        # Checking port and lane number fields
        for i in range(5,9):
            if self.CheckBoxList[i].IsChecked():
                try:
                    a = int(self.TextCtrlList[i].GetValue())
                except:
                    self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[i]))
                    self.TextCtrlList[i].SetBackgroundColour(self.ERROR_COLOR)
                    NoErrors = False
                else:
                    if (a <= 0 or a >= 65535):
                        self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[i]))
                        self.TextCtrlList[i].SetBackgroundColour(self.ERROR_COLOR)
                        NoErrors = False
                    else:
#                        if (i == self.TargetTextCtrl):
#                            self.TextCtrlList[i].SetBackgroundColour(self.TARGET_COLOR)
#                        else:
                        self.TextCtrlList[i].SetBackgroundColour(self.NON_TARGET_COLOR)
        # Checking MAC address
#        if self.CheckBoxList[8].IsChecked():
#            try:
#                address = ''.join(re.split("\-", self.TextCtrlList[8].GetValue()))
#                address_long = long(address, 16)
#            except:
#                self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[8]))
#                self.TextCtrlList[8].SetBackgroundColour(self.ERROR_COLOR)
#                NoErrors = False
#            else:
#                if (not (len(address) == 12) or (address_long < 0) or (address_long > int("FFFFFFFFFFFF", 16))):
#                    self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[8]))
#                    self.TextCtrlList[8].SetBackgroundColour(self.ERROR_COLOR)
#                    NoErrors = False
#                else:
#                    if (8 == self.TargetTextCtrl):
#                        self.TextCtrlList[8].SetBackgroundColour(self.TARGET_COLOR)
#                    else:
#                        self.TextCtrlList[8].SetBackgroundColour(self.NON_TARGET_COLOR)

        self.Refresh()
        return NoErrors

    # self.ComList[self.ComDropdown.GetSelection()]

    def ReqSettings(self):
        self.output.AppendText("\nAttempting to open port to pump board...\n")
        try:
            settingsPort = serial.Serial(self.ComDropdown.GetValue(), 9600, timeout=0.5)
        except serial.SerialException as strerror:
            self.output.AppendText(("'{0}' could not be opened. Please double-check that you've chosen the right COM port.\n" + 
                                    "(SerialException: {1})\n").format(self.ComDropdown.GetValue(), strerror))
        else:
#            settingsPort.flushInput()
#            settingsPort.flushOutput()
#            settingsPort.write("1\r")
#            time.sleep(1)
            settingsPort.flushInput()
            settingsPort.flushOutput()
            settingsPort.write("1\r")
            dataList = []
            parsedList = []
            
            self.output.AppendText("Reading data...\n")
            for each in range(14):
                dataList.append(settingsPort.readline())
            settingsPort.close()
            
            if (DEBUG):
                self.output.AppendText(str(dataList)+"\n")
            
            if dataList[2] == "Current settings:\t\n":
                data = "".join(dataList[3:])
                parsedList = re.split("\\t\\r\\n(.*?)\: ", data[19:-1])
                newList = parsedList[:10] + parsedList[10].split(':') + parsedList[11:]
                
                self.output.AppendText("Done!\n")
                
                return [newList[0], newList[2], newList[4], newList[6], newList[8], newList[10], newList[11], 
                        newList[12], newList[16], newList[14], newList[18], newList[20], newList[22]]
                
            else:
                self.output.AppendText("Failed to retrieve settings.\n")
                return None

    def Calibrate(self):
        self.output.AppendText("\nAttempting to open port to pump board...\n")
        try:
            calibratePort = serial.Serial(self.ComDropdown.GetValue(), 9600, timeout=1)
        except serial.SerialException as strerror:
            self.output.AppendText(("'{0}' could not be opened. Please double-check that you've chosen the right COM port.\n" + 
                                    "(SerialException: {1})\n").format(self.ComDropdown.GetValue(), strerror))
        else:
            calibratePort.flushInput()
            calibratePort.flushOutput()
            calibratePort.write("14\r")
            calibratePort.close()
            return True

    def Submit(self, settings):
        self.output.AppendText("\nAttempting to open port to pump board...\n")
        try:
            submitPort = serial.Serial(self.ComDropdown.GetValue(), 9600, timeout=1)
        except serial.SerialException as strerror:
            self.output.AppendText(("'{0}' could not be opened. Please double-check that you've chosen the right COM port.\n" + 
                                    "(SerialException: {1})\n").format(self.ComDropdown.GetValue(), strerror))
        else:
            submitPort.flushInput()
            submitPort.flushOutput()
            for i in range(len(settings)):
                if not(settings[i] == "DNL"):
                    if (i == 8):
                        temp = "12:" + settings[i] + "\r" # Pump ID
                    elif (i == 8):
                        temp = "13:" + settings[i] + "\r" # Firmware Update IP
                    else:
                        temp = str(i + 2) + ":" + settings[i] + "\r"
                    self.output.AppendText("Setting {0} to {1}".format(self.LabelNames[i],temp.split(':')[1]))
#                    self.output.AppendText(temp)
                    submitPort.write(temp)
                    time.sleep(1)
            
            submitPort.close()
            self.output.AppendText("Done!\n")

class MACAddressChanger(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, None, title="Change MAC Address", style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | 
                          wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
#        self.SetMinSize(wx.Size(520, -1))
#        self.SetMaxSize(wx.Size(800, 800))
        self.SetSize(wx.Size(331, 141))
        
        self.output = parent.output
        self.parent = parent
        textBoxFont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        p = wx.Panel(self)

        self.Octet1Ctrl = wx.TextCtrl(p, size=wx.Size(35,-1))
        self.Octet1Ctrl.SetFont(textBoxFont)
        self.Octet2Ctrl = wx.TextCtrl(p, size=wx.Size(35,-1))
        self.Octet2Ctrl.SetFont(textBoxFont)
        self.Octet3Ctrl = wx.TextCtrl(p, size=wx.Size(35,-1))
        self.Octet3Ctrl.SetFont(textBoxFont)
        self.Octet4Ctrl = wx.TextCtrl(p, size=wx.Size(35,-1))
        self.Octet4Ctrl.SetFont(textBoxFont)
        self.Octet5Ctrl = wx.TextCtrl(p, size=wx.Size(35,-1))
        self.Octet5Ctrl.SetFont(textBoxFont)
        self.Octet6Ctrl = wx.TextCtrl(p, size=wx.Size(35,-1))
        self.Octet6Ctrl.SetFont(textBoxFont)
        self.ParseMAC("64-fc-8c" + (parent.TextCtrlList[9].GetValue())[8:])
        self.MACUpDown = wx.SpinButton(p, id=262, style=wx.VERTICAL)
        wx.EVT_SPIN_UP(self, 262, self.OnUpMAC)
        wx.EVT_SPIN_DOWN(self, 262, self.OnDownMAC)
        SubmitButton = wx.Button(p, label="Submit MAC")
        SubmitButton.Bind(wx.EVT_BUTTON, self.OnSubmitPress)
        
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add(self.Octet1Ctrl, 0, wx.CENTER | wx.ALL, border=3)
        hsizer1.Add(wx.StaticText(p, label="-"), 0, wx.CENTER | wx.ALL, border=3)
        hsizer1.Add(self.Octet2Ctrl, 0, wx.CENTER | wx.ALL, border=3)
        hsizer1.Add(wx.StaticText(p, label="-"), 0, wx.CENTER | wx.ALL, border=3)
        hsizer1.Add(self.Octet3Ctrl, 0, wx.CENTER | wx.ALL, border=3)
        hsizer1.Add(wx.StaticText(p, label="-"), 0, wx.CENTER | wx.ALL, border=3)
        hsizer1.Add(self.Octet4Ctrl, 0, wx.CENTER | wx.ALL, border=3)
        hsizer1.Add(wx.StaticText(p, label="-"), 0, wx.CENTER | wx.ALL, border=3)
        hsizer1.Add(self.Octet5Ctrl, 0, wx.CENTER | wx.ALL, border=3)
        hsizer1.Add(wx.StaticText(p, label="-"), 0, wx.CENTER | wx.ALL, border=3)
        hsizer1.Add(self.Octet6Ctrl, 0, wx.CENTER | wx.ALL, border=3)
        hsizer1.Add(self.MACUpDown, 0)
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add(SubmitButton, 0, wx.TOP, border=10)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer1, 0, wx.CENTER | wx.LEFT | wx.RIGHT | wx.TOP, border=20)
        vsizer.Add(hsizer2, 0, wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, border=20)
        
        p.SetSizer(vsizer)
        
#        wx.CallAfter(self.Octet4Ctrl.SelectAll)
    
    def OnUpMAC(self, event):
        try:
            address = long(self.Octet1Ctrl.GetValue()+self.Octet2Ctrl.GetValue()+self.Octet3Ctrl.GetValue()+
                           self.Octet4Ctrl.GetValue()+self.Octet5Ctrl.GetValue()+self.Octet6Ctrl.GetValue(), 16)
        except:
            self.output.AppendText("\nInvalid MAC Address\n")
        else:
            address = ('{:012X}'.format((address + 1) % 0x1000000000000)) # FF-FF-FF-FF-FF-FF modulos to 00-00-00-00-00-00
            self.ParseMAC(address[0] + address[1] + "-" + address[2] + address[3] + "-" + address[4] + address[5] + "-" + 
                          address[6] + address[7] + "-" + address[8] + address[9] + "-" + address[10] + address[11])

    def OnDownMAC(self, event):
        try:
            address = long(self.Octet1Ctrl.GetValue()+self.Octet2Ctrl.GetValue()+self.Octet3Ctrl.GetValue()+
                           self.Octet4Ctrl.GetValue()+self.Octet5Ctrl.GetValue()+self.Octet6Ctrl.GetValue(), 16)
        except:
            self.output.AppendText("\nInvalid MAC Address\n")
        else:
            address = ('{:012X}'.format((address - 1) % 0x1000000000000)) # FF-FF-FF-FF-FF-FF modulos to 00-00-00-00-00-00
            self.ParseMAC(address[0] + address[1] + "-" + address[2] + address[3] + "-" + address[4] + address[5] + "-" + 
                          address[6] + address[7] + "-" + address[8] + address[9] + "-" + address[10] + address[11])
    
    def OnSubmitPress(self, event):
        if self.parent.ComDropdown.GetValue() == "":
            self.output.AppendText("\nPlease set a valid Com port number.\n")
            return
        try:
            submitPort = serial.Serial(self.parent.ComDropdown.GetValue(), 9600, timeout=1)
        except:
            self.output.AppendText("\nCan't open submit port.\n")
        else:
            submitPort.write("10:" + self.Octet1Ctrl.GetValue()+self.Octet2Ctrl.GetValue()+self.Octet3Ctrl.GetValue() + "\r")
            time.sleep(1)
            submitPort.write("11:" + self.Octet4Ctrl.GetValue()+self.Octet5Ctrl.GetValue()+self.Octet6Ctrl.GetValue() + "\r")
            submitPort.close()
            self.output.AppendText("\nMAC Address updated.\n")
        return True
    
    def ParseMAC(self, mac):
        octets = mac.split("-")
        self.Octet1Ctrl.SetValue(octets[0])
        self.Octet2Ctrl.SetValue(octets[1])
        self.Octet3Ctrl.SetValue(octets[2])
        self.Octet4Ctrl.SetValue(octets[3])
        self.Octet5Ctrl.SetValue(octets[4])
        self.Octet6Ctrl.SetValue(octets[5])

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=TITLE, style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | 
                          wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.SetMinSize(wx.Size(590, 500))
#        self.SetMaxSize(wx.Size(800, 800))
        self.SetSize(wx.Size(590, 650))
        
        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)

        # create the page windows as children of the notebook
        self.tb = wx.TextCtrl(p, style=wx.TE_MULTILINE | wx.TE_READONLY)
        pt = ProvisionTab(p, self.tb, self)
        ClearButton = wx.Button(p, label="Clear Screen")
#        ClearButton.SetFont(wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
        self.Bind(wx.EVT_BUTTON, self.ClearScreen, ClearButton)
        
        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(pt, 0, wx.EXPAND)
        sizer.Add(self.tb, 1, wx.EXPAND)
        sizer.Add(ClearButton, 0, wx.ALIGN_RIGHT)
        p.SetSizer(sizer)
        self.Center()

    def ClearScreen(self, event):
        self.tb.Clear()
        self.tb.AppendText(str(self.GetSize()))

if __name__ == "__main__":
    app = wx.App(redirect=False)
    MainFrame().Show()
    app.MainLoop()
