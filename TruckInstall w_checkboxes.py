import wx, re, serial, time, os
from CPS import ComPortSelector

DEBUG = True
TITLE = "Z-Con Pump Provisioning Tool"

class ProvisionTab(wx.Panel):

    LabelNames = [ "ZID", "Odometer", "VIN", "Engine Hours", "Fuel Used", "Faults" ]
#    TargetTextCtrl = 0 # Initialize with IP Address TextCtrl having target
    NON_TARGET_COLOR = "White"
#    TARGET_COLOR = (255, 255, 175, 255) # Pale Yellow
    ERROR_COLOR = (255, 50, 50, 255) # Pale Red
#    ComList = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9", "COM10", "COM11",
#               "COM12", "COM13", "COM14", "COM15", "COM16", "COM17", "COM18", "COM19", "COM20"]
    filename = 'settings.truck'
    dirname = ''
    ResetSettings = ["0123456789ABCDEFG", "0", "ZYXWVUTSRQPONMLKJ", "0", "0", "0"]
    
    def __init__(self, parent, output, frame):
        wx.Panel.__init__(self, parent)

        self.output = output
        self.frame = frame

        textBoxFont = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        
        self.RecallSettings = self.ResetSettings 
        
        # ID namespace
        # 100 = CheckBox
        # 200 = StaticText
        # 300 = TextCtrl
        # 500 = Button

        self.CheckAllBox = wx.CheckBox(self)
        self.CheckAllBox.SetValue(True)
        self.CheckAllBox.Bind(wx.EVT_CHECKBOX, self.onCheckAllBox)

        self.ComDropdown = ComPortSelector(self)
        
        self.CheckBoxList = []
        for i in range(100, 106):
            checkbox = wx.CheckBox(self, id=i)
            self.CheckBoxList.append(checkbox)
            checkbox.SetValue(True)
            wx.EVT_CHECKBOX(self, i, self.EnableEntry)
            
        self.LabelList = []

        for x in self.LabelNames:
            label = wx.StaticText(self, label=x)
            self.LabelList.append(label)
            
        self.TextCtrlList = []
        for i in range(300, 306):
            textbox = wx.TextCtrl(self, id=i, size=wx.Size(260,-1))
            textbox.SetFont(textBoxFont)
            self.TextCtrlList.append(textbox)
            textbox.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.ResetTextCtrls()

        grid1 = wx.FlexGridSizer(rows=7, cols=3)
        grid1.Add(self.CheckAllBox, 1, wx.EXPAND)
        grid1.Add(wx.StaticText(self, label=""), 1, wx.EXPAND)
        grid1.Add(self.ComDropdown, 0, wx.ALL, 3)
        # Add edittable fields to grid
        for i in range(len(self.CheckBoxList)):
            grid1.Add(self.CheckBoxList[i], 1, wx.EXPAND)
            grid1.Add(self.LabelList[i], 1, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
            grid1.Add(self.TextCtrlList[i], 1, wx.EXPAND | wx.ALL, 3)
        
        LoadButton = wx.Button(self, label="Load Settings file...")
        LoadButton.Bind(wx.EVT_BUTTON, self.OnLoadPress)
        SaveButton = wx.Button(self, label="Save Settings file...")
        SaveButton.Bind(wx.EVT_BUTTON, self.OnSavePress)
        
        ResetButton = wx.Button(self, label="Reset All Values")
        ResetButton.Bind(wx.EVT_BUTTON, self.OnResetPress)
        RequestZIDButton = wx.Button(self, label="Request ZID")
        RequestZIDButton.Bind(wx.EVT_BUTTON, self.OnRequestZIDPress)
        GetButton = wx.Button(self, label="Get Current Values")
        GetButton.Bind(wx.EVT_BUTTON, self.OnGetPress)
        RecallButton = wx.Button(self, label="Recall Last Submitted Values")
        RecallButton.Bind(wx.EVT_BUTTON, self.OnRecallPress)
        SubmitButton = wx.Button(self, label="Submit")
        SubmitButton.Bind(wx.EVT_BUTTON, self.OnSubmitPress)
        
        buttonSizer = wx.BoxSizer(wx.VERTICAL)
        buttonSizer.Add(LoadButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(SaveButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(wx.StaticText(self, label=""), 1, flag=wx.ALL, border=0)
        buttonSizer.Add(ResetButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(RequestZIDButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(GetButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(wx.StaticText(self, label=""), 1, flag=wx.ALL, border=0)
        buttonSizer.Add(RecallButton, 1, flag=wx.EXPAND, border=5)
        buttonSizer.Add(SubmitButton, 1, flag=wx.EXPAND, border=5)
        
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
        
        self.output.AppendText("Connect the Provisioning Board to your PC and click \"Request ZID\".")

    def onCheckAllBox(self, event):
        for i in range(len(self.CheckBoxList)):
            self.CheckBoxList[i].SetValue(event.Checked())
            if (event.Checked()):
                self.TextCtrlList[i].Enable()
            else:
                self.TextCtrlList[i].Disable()
    
    def EnableEntry(self, event):
        if (event.Checked()):
            self.TextCtrlList[event.GetId() - 100].Enable()
        else:
            self.TextCtrlList[event.GetId() - 100].Disable()
        all = True
        for x in self.CheckBoxList:
            if not x.GetValue():
                all = False # If any box is unchecked, uncheck the CheckAll box
        self.CheckAllBox.SetValue(all)

    def OnGainFocusTB(self, event):
        textnum = event.GetId() - 300
        wx.CallAfter(self.TextCtrlList[textnum].SelectAll)
        
    def OnLoadPress(self, event):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, self.filename, "*.truck", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            
            # Open the file, read the contents and set them into
            # the text edit window
            filehandle=open(os.path.join(self.dirname, self.filename),'r')
            try:
                list = eval(filehandle.read())
            except:
                self.output.AppendText("\nUnable to load {0}".format(self.dirname+"\\"+self.filename))
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
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, self.filename, "*.truck", \
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
            filehandle.write(str(list))
            filehandle.close()
        # Get rid of the dialog to keep things tidy
        dlg.Destroy()
        self.frame.SetTitle("{} - {}".format(TITLE,self.filename))
    
    def OnResetPress(self, event):
        self.ResetTextCtrls()
    
    def ResetTextCtrls(self):
        for i in range(len(self.ResetSettings)):
            self.TextCtrlList[i].SetValue(self.ResetSettings[i])

    def OnGetPress(self, event):
        if self.ComDropdown.GetValue() == "":
            self.output.AppendText("\n\nPlease set a valid Com port number.")
            return
        settings = self.ReqSettings()
        if (settings):
            self.PopulateFields(settings)
            self.output.AppendText("\nValues retrieved. Make any changes you want to the settings then hit \"Submit\".")
        
    def OnRecallPress(self, event):
        self.PopulateFields(self.RecallSettings)
        
    def PopulateFields(self, settings):
        for i in range(len(settings)):
            if (DEBUG):
                self.output.AppendText("\nParsing {0}...".format(self.LabelNames[i]))
            if not (settings[i] == "DNL"):
                if (i == 0) or (i == 2):
                    try:
                        self.TextCtrlList[i].SetValue(settings[i])
                    except:
                        self.output.AppendText("\n{0} value couldn't be retrieved: Invalid data".format(self.LabelNames[i]))
                else:
                    try:
                        self.TextCtrlList[i].SetValue(str(int(settings[i])))
                    except:
                        self.output.AppendText("\n{0} value couldn't be retrieved: Not an integer".format(self.LabelNames[i]))

    def OnRequestZIDPress(self, event):
        if self.ComDropdown.GetValue() == "":
            self.output.AppendText("\n\nPlease set a valid Com port number.")
            return
        if (self.RequestZID()):
            self.output.AppendText("\nZID requested. Wait for the LED on the Truck Provisioning Tool to illuminate, then press \"Get Current Values\".")
        else:
            self.output.AppendText("\nRequest failed.")

    def OnSubmitPress(self, event):
        if self.ComDropdown.GetValue() == "":
            self.output.AppendText("\n\nPlease set a valid Com port number.")
            return
        if (self.CheckFields()):
            settings = []
            for i in range(len(self.CheckBoxList)):
                if self.CheckBoxList[i].IsChecked():
                    settings.append(str(self.TextCtrlList[i].GetValue()))
                    self.RecallSettings[i] = str(self.TextCtrlList[i].GetValue())
                else:
                    settings.append("DNL")
            self.Submit(settings)
        else:
            self.output.AppendText("\nSettings not submitted. Found some fields with invalid values.\n")

    def CheckFields(self):
        ERROR_MESSAGE = "\nInvalid value in {} field."
        NoErrors = True
        for i in range(len(self.CheckBoxList)):
            if self.CheckBoxList[i].IsChecked():
                if (i == 0) or (i == 2):
                    temp = self.TextCtrlList[i].GetValue()
                    if not temp.isalnum():
                        self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[i]) + 
                                               " Non alphanumeric characters in string.")
                        self.TextCtrlList[i].SetBackgroundColour(self.ERROR_COLOR)
                        NoErrors = False
                    elif not (len(temp) == 17):
                        self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[i]) + 
                                               " String needs to be exactly 17 characters" + 
                                               " It's currently {} characters long.".format(len(temp)))
                        self.TextCtrlList[i].SetBackgroundColour(self.ERROR_COLOR)
                        NoErrors = False
                    else:
                            self.TextCtrlList[i].SetBackgroundColour(self.NON_TARGET_COLOR)
                else:
                    try:
                        n = int(self.TextCtrlList[i].GetValue())
                    except:
                        self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[i]))
                        self.TextCtrlList[i].SetBackgroundColour(self.ERROR_COLOR)
                        NoErrors = False
                    else:
                        if (n < 0 or 
                            (n > 9999999 and i == 1) or     # Odometer
                            (n > 999999 and i == 3) or      # Engine Hours
                            (n > 9999999 and i == 4) or     # Fuel Used
                            (n > 9999 and i == 5)):         # Faults
                            self.output.AppendText(ERROR_MESSAGE.format(self.LabelNames[i]) + 
                                                   " Value out of range.")
                            self.TextCtrlList[i].SetBackgroundColour(self.ERROR_COLOR)
                            NoErrors = False
                        else:
                            self.TextCtrlList[i].SetBackgroundColour(self.NON_TARGET_COLOR)
        self.Refresh()
        return NoErrors

    # self.ComList[self.ComDropdown.GetSelection()]
    
    def Submit(self, settings):
        self.output.AppendText("\n\nAttempting to open port to provisioning board...")
        try:
            submitPort = serial.Serial(self.ComDropdown.GetValue(), 9600, timeout=1)
        except serial.SerialException as strerror:
            self.output.AppendText(("\n'{0}' could not be opened. Please double-check that you've chosen the right COM port." + 
                                    "\n(SerialException: {1})").format(self.ComDropdown.GetValue(), strerror))
        else:
            submitPort.flushInput()
            submitPort.flushOutput()
            self.output.AppendText("Sending settings to the provisioning tool...")
            temp = "{}{:0>7}{}{:0>6}{:0>7}{:0>4}".format(*settings)
            submitPort.write('\xAA' + chr(len(temp)) + '\x01' + temp)
            submitPort.close()
            self.output.AppendText("\nDone! You may want to \"Get Current Values\" to verify that the settings were saved properly")
    
    def GetSettings(self):
        ZID_OFFSET = 0 
        ZID_LENGTH = 17
        ODOMETER_OFFSET = 17 
        ODOMETER_LENGTH = 7
        VIN_OFFSET = 24
        VIN_LENGTH = 17
        ENGINE_HOURS_OFFSET = 41 
        ENGINE_HOURS_LENGTH = 6
        FUEL_USED_OFFSET = 47
        FUEL_USED_LENGTH = 7
        FAULTS_OFFSET = 54
        FAULTS_LENGTH = 4
        
        self.output.AppendText("\n\nAttempting to open port to provisioning board...")
        try:
            settingsPort = serial.Serial(self.ComDropdown.GetValue(), 9600, timeout=0.5)
        except serial.SerialException as strerror:
            self.output.AppendText(("\n'{0}' could not be opened. Please double-check that you've chosen the right COM port." + 
                                    "\n(SerialException: {1})").format(self.ComDropdown.GetValue(), strerror))
        else:
#            settingsPort.flushInput()
#            settingsPort.flushOutput()
#            settingsPort.write("1\r")
#            time.sleep(1)
            settingsPort.flushInput()
            settingsPort.flushOutput()
            settingsPort.write('\xAA' + '\x01' + '\x03') # Request the settings
            
            self.output.AppendText("\nReading data...")
            settings = settingsPort.read(61)
            
            if (DEBUG):
                self.output.AppendText("\n"+settings)
            
            sync = settings.find('\xAA')
            
            if sync == -1:
                self.output.AppendText("\nNo sync byte encountered. Aborting.")
                settingsPort.close()
                return None
            
            if sync > 0:
                temp = settingsPort.read(sync)
                settings = settings[sync:] + temp
            
            settingsPort.close()
            
            if not ord(settings[1]) == 59: # If the length byte is not 59 
                self.output.AppendText("\nIncorrect length byte ({}). Aborting.".format(ord(settings[1])))
            elif not len(settings[2:]) == ord(settings[1]):  # If the length of the payload is not equal to the value of the length byte
                self.output.AppendText("\nIncorrect length of payload ({}). Aborting.".format(len(settings[2:])))  
            else:
                settings = settings[2:]
                return [settings[ZID_OFFSET:ZID_OFFSET + ZID_LENGTH], 
                        settings[ODOMETER_OFFSET:ODOMETER_OFFSET + ODOMETER_LENGTH], 
                        settings[VIN_OFFSET:VIN_OFFSET + VIN_LENGTH], 
                        settings[ENGINE_HOURS_OFFSET:ENGINE_HOURS_OFFSET + ENGINE_HOURS_LENGTH], 
                        settings[FUEL_USED_OFFSET:FUEL_USED_OFFSET + FUEL_USED_LENGTH], 
                        settings[FAULTS_OFFSET:FAULTS_OFFSET + FAULTS_LENGTH]]
            
            return None
                
            
    def RequestZID(self):
        self.output.AppendText("\n\nAttempting to open port to provisioning board...")
        try:
            requestPort = serial.Serial(self.ComDropdown.GetValue(), 9600, timeout=1)
        except serial.SerialException as strerror:
            self.output.AppendText(("\n'{0}' could not be opened. Please double-check that you've chosen the right COM port." + 
                                    "\n(SerialException: {1})").format(self.ComDropdown.GetValue(), strerror))
        else:
            requestPort.flushInput()
            requestPort.flushOutput()
            requestPort.write('\xAA' + '\x01' + '\x03')
            requestPort.close()
            return True
        
class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title=TITLE, style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | 
                          wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.SetMinSize(wx.Size(550, 331))
#        self.SetMaxSize(wx.Size(800, 800))
        self.SetSize(wx.Size(550, 500))
        
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

if __name__ == "__main__":
    app = wx.App(redirect=False)
    MainFrame().Show()
    app.MainLoop()