import wx, re, threading, serial, time, os, Queue
import winsound as ws

VERSION = "Version 1.0"
CONTACT_INFO = """Zonar: 206.878.2459    Zonar Fax: 206.878.3082    Contacts: Kelly Niemi and Ryan Vilbrandt"""  
NORMAL, ERROR, SUCCESS = 0,1,2

class GbatTab(wx.Panel):

    NORMAL_TEXT_COLOR = "Black"
    NORMAL_BG_COLOR = "White"
    ERROR_TEXT_COLOR = "White"
    ERROR_BG_COLOR = (150, 0, 0, 255) # Dark Red
    SUCCESS_TEXT_COLOR = "White"
    SUCCESS_BG_COLOR = (0, 150, 0, 255) # Dark Green
    OFF_COLOR = "White"
    RunThreads = True
    ThreadList = []
    COMPortList = []
    
    def __init__(self, parent, config):
        wx.Panel.__init__(self, parent)
        self.Config = config
        
        self.InitGUI()
##        s = self.OpenCOMPort('Gbat COM Port')
##        if s: s.close()
        self.InitLogFile()
        
    def InitGUI(self):
        statusFont = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        self.StatusLabel = wx.StaticText(self, label="",
                                         style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE)
        self.StatusLabel.SetFont(statusFont)
        self.HistoryTB = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.ThreeFootLight = wx.Button(self, size=(30,-1))
        self.SixFootLight = wx.Button(self, size=(30,-1))
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add Status sizer and components
        statusBox = wx.StaticBox(self, label='Status')
        statusSizer = wx.StaticBoxSizer(statusBox, wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(wx.StaticText(self, label=""), 1, wx.EXPAND)
        hsizer.Add(wx.StaticText(self, label="3 foot distance"), 0, wx.ALIGN_CENTER | wx.ALL, border=3)
        hsizer.Add(self.ThreeFootLight, 0, wx.ALIGN_CENTER | wx.ALL, border=3)
        hsizer.Add(wx.StaticText(self, label="    "), 0, wx.ALIGN_CENTER | wx.ALL, border=3)
        hsizer.Add(wx.StaticText(self, label="6 foot distance"), 0, wx.ALIGN_CENTER | wx.ALL, border=3)
        hsizer.Add(self.SixFootLight, 0, wx.ALIGN_CENTER | wx.ALL, border=3)
        hsizer.Add(wx.StaticText(self, label=""), 1, wx.EXPAND)
        statusSizer.Add(hsizer, 1, wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL)
        statusSizer.Add(self.StatusLabel, 1, wx.EXPAND)
        lightSizer = wx.BoxSizer
        sizer.Add(statusSizer, 0, wx.EXPAND)
        
        # Add History box/sizer
        historyBox = wx.StaticBox(self, label='History')
        historySizer = wx.StaticBoxSizer(historyBox, wx.VERTICAL)
        historySizer.Add(self.HistoryTB, 1, wx.EXPAND)
        sizer.Add(historySizer, 1, wx.EXPAND)
        
        self.SetSizerAndFit(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)
        
        self.NORMAL_BG_COLOR = self.StatusLabel.GetBackgroundColour()
        self.OFF_COLOR = self.ThreeFootLight.GetBackgroundColour()

    def OpenCOMPort(self, portname):
        try:
            baud = int(self.Config.get('baud rate', 9600))
        except ValueError as e:
            self.ErrorDialog("Baud rate in test_config.ini is not an integer.\n"+str(e))
            return None
        try:
            bytesize = int(self.Config.get('data size', 8))
        except ValueError as e:
            self.ErrorDialog("Data size in test_config.ini is not an integer.\n"+str(e))
            return None
        try:
            parity = self.Config.get('parity', 'N')[0].upper()
        except ValueError as e:
            self.ErrorDialog("Parity in test_config.ini must be N, E, O, M or S.\n"+str(e))
            return None
        try:
            stopbits = int(self.Config.get('stop bits', 1))
        except ValueError as e:
            self.ErrorDialog("Stop bits in test_config.ini is not an integer.\n"+str(e))
            return None
        
        try:
            port = serial.Serial(port=self.Config[portname.lower()], baudrate=baud, bytesize=bytesize, parity=parity, 
                              stopbits=stopbits)
        except serial.SerialException as e:
            self.ErrorDialog("Can't open {}. Check your config settings.\n".format(portname)+str(e))
            port = None
        except ValueError as e:
            self.ErrorDialog("Invalid parameter when attempting to open {}. ".format(portname) +
                             "Check your config settings.\n"+str(e))
            port = None    
        return port
        
    def InitLogFile(self):
        ready = self.OpenLogConnection()
        if not ready:
            self.ErrorDialog("Unable to open log file. See History for details.")
        self.CloseLogConnection()
        
    def OpenLogConnection(self):
        # If logs directory does not exist, create it.
        if not os.path.isdir('logs'):
            os.mkdir('logs')
        # Parse file names
        t = time.localtime()
        logFileName = time.strftime(self.Config['gbat log file'],t)
        try:
            self.logfile = open(logFileName, 'a')
        except IOError as e:
            self.logfile = None
            self.ProcessOutput('IOError encountered when trying to write to ' + logFileName + 
                               '\n' + str(e), "Can't write to log file", ERROR)
            return False
        return True
    
    def CloseLogConnection(self):
        if self.logfile:
            self.logfile.close()
            self.logfile = None
    
    def ErrorDialog(self, e):
        dial = wx.MessageDialog(None, e, 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
    
    def StartPage(self):
        self.RunThreads = True
        self.ThreadList.append(threading.Thread(name="GbatTest", target=self.StartTest))
        for t in self.ThreadList:
            t.start()
    
    def StopPage(self):
        self.RunThreads = False
        self.ThreadList = []
        for s in self.COMPortList:
            try:
                s.close()
            except:
                pass
        self.COMPortList = []
    
    def StartTest(self):        
        try:
            tol = int(self.Config.get('gbat tolerance',5))
            d1_min = int(self.Config.get('gbat distance1',91)) - tol
            d1_max = int(self.Config.get('gbat distance1',91)) + tol
            d2_min = int(self.Config.get('gbat distance2',183)) - tol
            d2_max = int(self.Config.get('gbat distance2',183)) + tol
            confirm_readings = int(self.Config.get("gbat confirm readings", 20))
            reject_readings = int(self.Config.get("gbat reject readings", 3))
            total_readings = int(self.Config.get("gbat fail readings", 200))
        except ValueError as e:
            self.ProcessOutput("One of the gbat values in the config file is not a number. " + 
                               "Update your config file and restart the app. " + str(e),
                               "Bad Gbat Config Values", ERROR, sound=self.Config["error sound"])
            return
        s = self.OpenCOMPort('Gbat COM Port')
        if not s:
            return
        self.COMPortList.append(s)
        try:
            s.timeout = float(self.Config.get('gbat timeout', 1))
        except ValueError as e:
            self.ProcessOutput("Gbat Timeout is not a valid number. Please update your config settings." + str(e),
                               "Bad Config Value", ERROR, sound=self.Config["error sound"])
            return None

        while self.RunThreads:
            line = s.read(5)
            while (self.RunThreads and not re.search(r"R(\d\d\d)\r$", line[-5:])):
                line += s.read(1)
            if self.RunThreads:
                self.ProcessOutput("Data received from Gbat. Starting test...",
                                   "Test Started", NORMAL, sound=self.Config["start sound"])
            
                d1Count = 0
                d2Count = 0
                failCount = 0
                d1succ = False
                d2succ = False
                for i in range(total_readings):
                    s.flushInput()
                    s.flushOutput()
                    line = s.read(5)
                    r = re.match(r"^R(\d\d\d)\r$", line)
                    if not r:
                        self.ProcessOutput("FAIL - Bad data from Gbat: "+repr(line),
                                           "Test Failed", ERROR, sound=self.Config["error sound"])
                        break
                    else:
                        d = int(r.group(1))
                        self.ProcessOutput(status="Test Started -- {:.1f}ft".format(d*0.032808399))
                        if (d > d1_min and d < d1_max):
                            d1Count += 1
                            d2Count = 0
                            failCount = 0
                            if d1Count >= confirm_readings:
                                d1Count = confirm_readings
                                self.ThreeFootLight.SetBackgroundColour("Green")
                                self.SixFootLight.SetBackgroundColour(self.OFF_COLOR)
                                if not d1succ:
                                    self.ProcessOutput("Three foot distance verified.")
                                d1succ = True
                        elif (d > d2_min and d < d2_max):
                            d1Count = 0
                            d2Count += 1
                            failCount = 0
                            if d2Count >= confirm_readings:
                                d2Count = confirm_readings
                                self.ThreeFootLight.SetBackgroundColour(self.OFF_COLOR)
                                self.SixFootLight.SetBackgroundColour("Green")
                                if not d2succ:
                                    self.ProcessOutput("Six foot distance verified.")
                                d2succ = True
                        else:
                            d1Count = 0
                            d2Count = 0
                            failCount += 1
                            if failCount >= reject_readings:
                                failCount = reject_readings
                                self.ThreeFootLight.SetBackgroundColour(self.OFF_COLOR)
                                self.SixFootLight.SetBackgroundColour(self.OFF_COLOR)
                    if (d1succ and d2succ) or (not self.RunThreads):
                        break
                if not (d1succ and d2succ):
                    self.ProcessOutput("FAIL - Test did not pick up both distances.",
                                       "Test Failed", ERROR, sound=self.Config["error sound"])
                else:
                    self.ProcessOutput("SUCCESS", "Test Passed!", SUCCESS, sound=self.Config["success sound"])
                self.ThreeFootLight.SetBackgroundColour(self.OFF_COLOR)
                self.SixFootLight.SetBackgroundColour(self.OFF_COLOR)

                c = s.read(1)
                while (self.RunThreads and c):
                    c = s.read(1)
                self.ProcessOutput(status="")
        s.close()
    
    def ProcessOutput(self, history=None, status=None, messagetype=NORMAL, progress=-1, sound=None):
        if not history == None:
            self.HistoryAppend(history)
        if not status == None:
            if messagetype == NORMAL:
                self.StatusLabel.SetForegroundColour(self.NORMAL_TEXT_COLOR)
                self.StatusLabel.SetBackgroundColour(self.NORMAL_BG_COLOR)
            elif messagetype == ERROR:
                self.StatusLabel.SetForegroundColour(self.ERROR_TEXT_COLOR)
                self.StatusLabel.SetBackgroundColour(self.ERROR_BG_COLOR)
            elif messagetype == SUCCESS:
                self.StatusLabel.SetForegroundColour(self.SUCCESS_TEXT_COLOR)
                self.StatusLabel.SetBackgroundColour(self.SUCCESS_BG_COLOR)
            self.StatusLabel.SetLabel(status)
#        if progress >= 0:
#            self.ProgressGauge.SetValue(int(progress))
        if sound:
            ws.PlaySound(sound, ws.SND_FILENAME)
    
    def HistoryAppend(self, i):
        temp = "[{0}] {1}\n".format(time.ctime(), str(i))
        self.HistoryTB.AppendText(temp)
        if self.logfile:
            self.logfile.write(temp)
    
class IRTab(wx.Panel):

    NORMAL_TEXT_COLOR = "Black"
    NORMAL_BG_COLOR = "White"
    ERROR_TEXT_COLOR = "White"
    ERROR_BG_COLOR = (150, 0, 0, 255) # Dark Red
    SUCCESS_TEXT_COLOR = "White"
    SUCCESS_BG_COLOR = (0, 150, 0, 255) # Dark Green
    RunThread = True
    ThreadList = []
    COMPortList = []
    
    def __init__(self, parent, config):
        wx.Panel.__init__(self, parent)
        self.Config = config
        
        self.InitGUI()
        s = self.OpenCOMPort('IR Receiver COM Port')
        if s: s.close()
        s = self.OpenCOMPort('IR Transmitter COM Port')
        if s: s.close()
        self.InitLogFile()
        
    def InitGUI(self):
        statusFont = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        self.StatusLabel = wx.StaticText(self, label="",
                                         style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE)
        self.StatusLabel.SetFont(statusFont)
        self.HistoryTB = wx.TextCtrl(self, style=wx.TE_READONLY | wx.TE_MULTILINE)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add Status sizer and components
        statusBox = wx.StaticBox(self, label='Status')
        statusSizer = wx.StaticBoxSizer(statusBox, wx.VERTICAL)
        statusSizer.Add(self.StatusLabel, 1, wx.EXPAND)
        sizer.Add(statusSizer, 0, wx.EXPAND)
        
        # Add History box/sizer
        historyBox = wx.StaticBox(self, label='History')
        historySizer = wx.StaticBoxSizer(historyBox, wx.VERTICAL)
        historySizer.Add(self.HistoryTB, 1, wx.EXPAND)
        sizer.Add(historySizer, 1, wx.EXPAND)
        
        self.SetSizerAndFit(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)

        self.NORMAL_BG_COLOR = self.StatusLabel.GetBackgroundColour()
    
    def OpenCOMPort(self, portname, baudrate='baud rate'):
        try:
            baud = int(self.Config.get(baudrate.lower(), 9600))
        except ValueError as e:
            self.ErrorDialog("Baud rate in test_config.ini is not an integer.\n"+str(e))
            return None
        try:
            bytesize = int(self.Config.get('data size', 8))
        except ValueError as e:
            self.ErrorDialog("Data size in test_config.ini is not an integer.\n"+str(e))
            return None
        try:
            parity = self.Config.get('parity', 'N')[0].upper()
        except ValueError as e:
            self.ErrorDialog("Parity in test_config.ini must be N, E, O, M or S.\n"+str(e))
            return None
        try:
            stopbits = int(self.Config.get('stop bits', 1))
        except ValueError as e:
            self.ErrorDialog("Stop bits in test_config.ini is not an integer.\n"+str(e))
            return None
        
        try:
            port = serial.Serial(port=self.Config[portname.lower()], baudrate=baud, bytesize=bytesize, parity=parity, 
                              stopbits=stopbits)
        except serial.SerialException as e:
            self.ErrorDialog("Can't open {}. Check your config settings.\n".format(portname)+str(e))
            port = None
        except ValueError as e:
            self.ErrorDialog("Invalid parameter when attempting to open {}. ".format(portname) +
                             "Check your config settings.\n"+str(e))
            port = None    
        return port
        
    def InitLogFile(self):
        ready = self.OpenLogConnection()
        if not ready:
            self.ErrorDialog("Unable to open log file. See History for details.")
        self.CloseLogConnection()
        
    def OpenLogConnection(self):
        # If logs directory does not exist, create it.
        if not os.path.isdir('logs'):
            os.mkdir('logs')
        # Parse file names
        t = time.localtime()
        logFileName = time.strftime(self.Config['ir log file'],t)
        try:
            self.logfile = open(logFileName, 'a')
        except IOError as e:
            self.logfile = None
            self.ProcessOutput('IOError encountered when trying to write to ' + logFileName + 
                               '\n' + str(e), "Can't write to log file", ERROR)
            return False
        return True
    
    def CloseLogConnection(self):
        if self.logfile:
            self.logfile.close()
            self.logfile = None
    
    def ErrorDialog(self, e):
        dial = wx.MessageDialog(None, e, 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
    
    def StartPage(self):
        self.RunThreads = True
##        self.MessageList = self.Config.get('ir messages','ABCDEFGHIJKLMNOP').split(',')
        self.ThreadList.append(threading.Thread(name="IRTest", target=self.StartTest))
##        self.ThreadList.append(threading.Thread(name="IRTransmit", target=self.RunTransmitter))
        for t in self.ThreadList:
            t.start()
    
    def StopPage(self):
        self.RunThreads = False
        self.ThreadList = []
        for s in self.COMPortList:
            try:
                s.close()
            except:
                pass
        self.COMPortList = []

##    def RunTransmitter(self):
##        try:
##            delay = int(self.Config.get('ir delay',500))/1000.0
##        except ValueError as e:
##            self.ProcessOutput("IR Delay in the config file is not a number. " + 
##                               "Update your config file and restart the app. " + str(e),
##                               "Bad IR Config Values", ERROR, sound=self.Config["error sound"])
##            return
##        s = self.OpenCOMPort('IR Transmitter COM Port', 'IR baud rate')
##        if s:
##            self.COMPortList.append(s)
##            while self.RunThreads:
##                for x in self.MessageList:
##                    s.write('\xAA'+chr(len(x))+x+'\n')
##                    time.sleep(delay)
##                    if not self.RunThreads:
##                        break
##            s.close()
    
    def StartTest(self):
        message_list = self.Config.get('ir messages','ABCDEFGHIJKLMNOP').split(',')
        try:
            readings = int(self.Config.get('ir readings',20))
            delay = int(self.Config.get('ir delay',500))/1000.0
            confirm_readings = int(self.Config.get('ir confirm readings',18))
        except ValueError as e:
            self.ProcessOutput("One of the IR values in the config file is not a number. " + 
                               "Update your config file and restart the app. " + str(e),
                               "Bad IR Config Values", ERROR, sound=self.Config["error sound"])  
        t = self.OpenCOMPort('IR Transmitter COM Port', 'IR baud rate')
        if not t:
            return
        self.COMPortList.append(t)
        r = self.OpenCOMPort('IR Receiver COM Port', 'IR baud rate')
        if not r:
            return
        self.COMPortList.append(r)
        try:
            r.timeout = float(self.Config.get('ir timeout', 1))
        except ValueError as e:
            self.ProcessOutput("IR Timeout is not a valid number. Please update your config settings." + str(e),
                               "Bad Config Value", ERROR, sound=self.Config["error sound"])
            return None
        while self.RunThreads:
            r.flushInput()
            t.flushOutput()
            t.write('\xAA')
            time.sleep(delay)
            c = r.read(1)
            while (self.RunThreads and not c):
                t.write('\xAA')
                time.sleep(delay)
                c = r.read(1)
            if self.RunThreads:
                self.ProcessOutput("Data received from IR receiver. Starting test...",
                                   "Test Started", NORMAL, sound=self.Config["start sound"])
                count = 0
                r.flushInput()
                t.flushOutput()
                for i in range(readings):
                    temp = message_list[i % len(message_list)]
                    temp = '\xAA'+chr(len(temp))+temp
                    t.write(temp)
                    time.sleep(delay)
                    line = r.read(len(temp))
                    self.ProcessOutput("{} of {}: {}".format(i+1,readings,repr(line[2:])),
                                       "Test Started - Reading {} of {}".format(i+1,readings))
                    if (line == temp):
                        count += 1
                    if not self.RunThreads:
                        break
                    
                if count < confirm_readings:
                    self.ProcessOutput("FAIL - less than {} valid readings out of {}. Only {} valid readings counted.".format(confirm_readings, readings, count),
                                       "Test Failed", ERROR, sound=self.Config["error sound"])
                else:
                    self.ProcessOutput("SUCCESS", "Test Passed! {} out of {} valid readings.".format(count, readings), SUCCESS, sound=self.Config["success sound"])

                while (self.RunThreads and c):
                    t.write('\xAA')
                    time.sleep(delay)
                    c = r.read(1)
                self.ProcessOutput(status="")
##        while self.RunThreads:
##            s.flushInput()
##            s.flushOutput()
##            line = s.readline()
##            while (self.RunThreads and not line):
##                line = s.readline()
##            if self.RunThreads:
##                self.ProcessOutput("Data received from IR receiver. Starting test...",
##                                   "Test Started", NORMAL, sound=self.Config["start sound"])
##                count = 0
##                for i in range(readings):
##                    if line and len(line) < 3:
##                        line += s.readline()
##                    while (self.RunThreads and line and (ord(line[1]) > len(line)-3)):
##                        line += s.readline()
##                    self.ProcessOutput("{} of {}: {}".format(i+1,readings,repr(line[2:-1])),
##                                       "Test Started - Reading {} of {}".format(i+1,readings))
##                    if (line and (line[0] == '\xAA') and (ord(line[1]) == len(line[2:-1])) and
##                        (line[2:-1] in self.MessageList) and (line[-1] == '\n')):
##                        count += 1
##                    line = s.readline()
##                    if not self.RunThreads:
##                        break
##                    
##                if count < confirm_readings:
##                    self.ProcessOutput("FAIL - less than {} valid readings out of {}. Only {} valid readings counted.".format(confirm_readings, readings, count),
##                                       "Test Failed", ERROR, sound=self.Config["error sound"])
##                else:
##                    self.ProcessOutput("SUCCESS", "Test Passed! {} out of {} valid readings.".format(count, readings), SUCCESS, sound=self.Config["success sound"])
##
##                while (self.RunThreads and line):
##                    line = s.readline()
##                self.ProcessOutput(status="")
        r.close()
        t.close()
    
    def ProcessOutput(self, history=None, status=None, messagetype=NORMAL, progress=-1, sound=None):
        if not history == None:
            self.HistoryAppend(history)
        if not status == None:
            if messagetype == NORMAL:
                self.StatusLabel.SetForegroundColour(self.NORMAL_TEXT_COLOR)
                self.StatusLabel.SetBackgroundColour(self.NORMAL_BG_COLOR)
            elif messagetype == ERROR:
                self.StatusLabel.SetForegroundColour(self.ERROR_TEXT_COLOR)
                self.StatusLabel.SetBackgroundColour(self.ERROR_BG_COLOR)
            elif messagetype == SUCCESS:
                self.StatusLabel.SetForegroundColour(self.SUCCESS_TEXT_COLOR)
                self.StatusLabel.SetBackgroundColour(self.SUCCESS_BG_COLOR)
            self.StatusLabel.SetLabel(status)
#        if progress >= 0:
#            self.ProgressGauge.SetValue(int(progress))
        if sound:
            ws.PlaySound(sound, ws.SND_FILENAME)
    
    def HistoryAppend(self, i):
        temp = "[{0}] {1}\n".format(time.ctime(), str(i))
        self.HistoryTB.AppendText(temp)
        if self.logfile:
            self.logfile.write(temp)

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="zCon Tools", style=wx.MINIMIZE_BOX | wx.RESIZE_BORDER | 
                          wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        self.SetMinSize(wx.Size(485, 400))
#        self.SetMaxSize(wx.Size(800, 800))
        self.SetSize(wx.Size(485, 400))
        
        config = self.InitConfigFile()
        if config:
            self.InitSoundFiles(config)
            self.InitGui(config)

    def InitGui(self, config):
        # Here we create a panel and a notebook on the panel
        p = wx.Panel(self)
        nb = wx.Notebook(p)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.NotebookChanged)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.NotebookChanging)
        self.Bind(wx.EVT_CLOSE, self.OnClose, self)

        # create the page windows as children of the notebook
        page1 = GbatTab(nb, config)
        page2 = IRTab(nb, config)
        self.NotebookList = [page1, page2]
        
        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page1, "Gbat tester")
        nb.AddPage(page2, "IR tester")
        
        # Add Contact Info box/sizer
        contactBox = wx.StaticBox(p, label='Contact and Version Info')
        contactSizer = wx.StaticBoxSizer(contactBox, wx.VERTICAL)
        contactSizer.Add(wx.StaticText(p, label=VERSION), 0, wx.ALIGN_CENTER | wx.BOTTOM, border=3)
        contactSizer.Add(wx.StaticText(p, label=CONTACT_INFO), 0, wx.ALIGN_CENTER)
        
        # finally, put the notebook in a sizer for the panel to manage
        # the layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(nb, 1, wx.EXPAND)
        sizer.Add(contactSizer, 0, wx.EXPAND | wx.ALL, border=3)
        p.SetSizer(sizer)
        self.Center()
        
    def InitConfigFile(self):
        filename = "test_config.ini"
        required_params = ['station number', 'gbat com port', 'ir receiver com port', 'ir transmitter com port', 
                           'gbat log file', 'ir log file', 'start sound', 'error sound', 'success sound', 
                           'gbat distance1', 'gbat distance2', 'gbat tolerance', 'gbat confirm readings',
                           'gbat reject readings', 'gbat fail readings', 'ir messages', 'ir readings', 'ir delay',
                           'ir confirm readings']
        # If config.ini doesn't exist, create it with default values
        if not os.path.isfile(filename):
            self.ErrorDialog("{} does not exist.".format(filename))
            return None
##            try:
##                file = open(filename, 'w')
##            except IOError as e:
##                self.ErrorDialog('IOError when trying to create {}\n".format(filename) + str(e))
##                return None
##            else:
##                file.write(DEFAULT_CONFIG_FILE)
##                file.close()
                
        # Open config.ini and read out the parameters
        try:
            file = open(filename, 'r')
        except IOError as e:
            self.ErrorDialog("IOError encountered when trying to open {}\n".format(filename) + str(e))
            return None
        config = {}
        for line in file:
            # Discard any comments
            no_comment = line[:line.find(';')]
            # '=' is the delimiter between variable name and value
            # Lines without a '=' are ignored.
            delim = no_comment.find('=')
            if not delim == -1:
                config[no_comment[:delim].strip().lower()] = no_comment[delim+1:].strip(' "\n')
        file.close()
        # Check to make sure log file names, sound file names and all default provision parameters are defined
        diff_list = [item for item in required_params
                     if (not item in config.keys()) or (not config[item])]
        if diff_list:
            self.ErrorDialog("Missing required config parameter(s):\n"+" ,".join(diff_list))            
            return None
        return config

    def InitSoundFiles(self, config):
        for file in ['start sound', 'error sound', 'success sound']:
            if not os.path.isfile(config[file]):
                self.ErrorDialog("'" + config[file] + "' is not a valid file name.\n" + 
                                 "Please update the value for '" + file + "' in the config file.")

    def ErrorDialog(self, e):
        dial = wx.MessageDialog(None, e, 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
    
    def NotebookChanged(self, event):
        if event.GetEventObject().GetCurrentPage():
            event.GetEventObject().GetCurrentPage().StartPage()
#        print self.GetSize()
        
    def NotebookChanging(self, event):
        if event.GetEventObject().GetCurrentPage():
            event.GetEventObject().GetCurrentPage().StopPage()
    
    # Catches EVT_CLOSE for this frame, and tells all LED threads to close gracefully first
    def OnClose(self, event):
        # Gather threads from all pages 
#        MasterThreadList = [item for sublist in self.NotebookList for item in sublist.ThreadList]
        MasterThreadList = []
        for page in self.NotebookList:
            page.StopPage()
            MasterThreadList += page.ThreadList
            for s in page.COMPortList:
                try:
                    s.close()
                except:
                    pass
        t = time.time()
#        print self.pt.ThreadList
        # If all the threads don't end after 3 seconds, force a shutdown
        while ((True in [th.isAlive() for th in MasterThreadList]) and time.time() < t+3):
            pass
        self.Destroy()

if __name__ == "__main__":
    app = wx.App(redirect=False)
    MainFrame().Show()
    app.MainLoop()

