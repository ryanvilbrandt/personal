#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Python built-in modules
import time, threading, sys, os, math
from struct import pack, unpack
# Third party modules
import wx                           # http://www.wxpython.org/
import serial                       # http://pyserial.sourceforge.net/

# Process command line arguments
DEBUG = True
#print sys.argv
if "-debug" in sys.argv:
    DEBUG = True

VERSION = "0.0.1"
TITLE = "Steve's App v"+VERSION
MAXPORTS = 48

class FunctionTestFrame(wx.Frame):
    
    RunThreads = True
    ThreadList = []
    filename = ""
    dirname = ""
    DEFAULT_COLOR = "White"
    NORMAL_TEXT_COLOR = "Black"
#    NON_DEFAULT_COLOR = (255, 255, 175, 255) # Pale Yellow
#    ERROR_COLOR = (255, 50, 50, 255) # Pale Red
    ERROR_TEXT_COLOR = "White"
    ERROR_BG_COLOR = (150, 0, 0, 255) # Red
    SUCCESS_TEXT_COLOR = "White"
    SUCCESS_BG_COLOR = (0, 150, 0, 255) # Green
    READ_ONLY_COLOR = "Light Gray"
    
    def __init__(self):
        wx.Frame.__init__(self, None, title=TITLE, style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | 
                          wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        
        self.InitGUI()
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def InitGUI(self):
        self.SetMinSize((340, 228))
        self.SetSize(wx.Size(500, 300))

        p = wx.Panel(self)
        
        self.TB1 = wx.TextCtrl(p, style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.TB2 = wx.TextCtrl(p, style=wx.TE_READONLY | wx.TE_MULTILINE)

        # COM port selectors and scan checkbox
        self.Port1Selector = wx.ComboBox(p, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.Port2Selector = wx.ComboBox(p, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        
        self.ScanCheckBox = wx.CheckBox(p, label="Showing active ports")
        self.ScanCheckBox.SetValue(True)
        self.ScanCheckBox.Bind(wx.EVT_CHECKBOX, self.CheckAutoPorts)
        
        if self.ScanCheckBox.GetValue():
            port_items = self.scan()
            if not port_items:
                port_items = ["          "]
        else:
            port_items = ["COM" + str(i) for i in xrange(1, MAXPORTS + 1)]
        self.Port1Selector.AppendItems(port_items)
        self.Port2Selector.AppendItems(port_items)
        if port_items:
            self.Port1Selector.SetValue(port_items.pop(0))
        if port_items:
            self.Port2Selector.SetValue(port_items.pop(0))
        
        self.EdittableTB = wx.TextCtrl(p, size=wx.Size(300, -1))
        self.EdittableTB.SetValue('<Type your text here>')
        
        self.ReadOnlyTB = wx.TextCtrl(p, size=wx.Size(300, -1))
        self.ReadOnlyTB.SetValue('Read-only text here')
        self.ReadOnlyTB.SetBackgroundColour(self.READ_ONLY_COLOR)
        
        self.SendToZConpButton = wx.Button(p, label="Send to zconp")
        self.SendToZConpButton.Bind(wx.EVT_BUTTON, self.OnSendToZConpPress)
        self.StopZConpButton = wx.Button(p, label="Stop")
        self.StopZConpButton.Bind(wx.EVT_BUTTON, self.OnStopZConpPress)
        
        self.OpenFileButton = wx.Button(p, label="Open File...")
        self.OpenFileButton.Bind(wx.EVT_BUTTON, self.OnOpenFilePress)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # Add Text Box 1 and Com Port Selector 1
        vsizer1Box = wx.StaticBox(p, label='COM Port Selector/Text Box 1')
        vsizer1 = wx.StaticBoxSizer(vsizer1Box, wx.VERTICAL)
        vsizer1.Add(self.TB1, 1, wx.EXPAND | wx.ALL, 5)
        vsizer1.Add(self.Port1Selector, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(vsizer1, 1, wx.EXPAND | wx.ALL, 5)

        # Build top middle sizer
        midSizer1 = wx.BoxSizer(wx.VERTICAL)
        midSizer1.Add(self.EdittableTB, 1, wx.EXPAND | wx.ALL, 5)
        midSizer1.Add(self.SendToZConpButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        midSizer1.Add(self.StopZConpButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        
        # Build bottom middle sizer
        midSizer2 = wx.BoxSizer(wx.VERTICAL)
        midSizer2.Add(self.OpenFileButton, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        midSizer2.Add(self.ReadOnlyTB, 1, wx.EXPAND | wx.ALL, 5)
        midSizer2.Add(self.ScanCheckBox, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        # Add middle row sizer
        vsizer_mid = wx.BoxSizer(wx.VERTICAL)
        vsizer_mid.Add(midSizer1, 0, wx.EXPAND)
        vsizer_mid.Add(wx.StaticText(p, label=""), 1, wx.EXPAND) # Placeholder
        vsizer_mid.Add(midSizer2, 0, wx.EXPAND | wx.ALIGN_BOTTOM)
        sizer.Add(vsizer_mid, 1, wx.EXPAND | wx.ALL, 5)

        # Add Text Box 2 and Com Port Selector 2
        vsizer2Box = wx.StaticBox(p, label='COM Port Selector/Text Box 2')
        vsizer2 = wx.StaticBoxSizer(vsizer2Box, wx.VERTICAL)
        vsizer2.Add(self.TB2, 1, wx.EXPAND | wx.ALL, 5)
        vsizer2.Add(self.Port2Selector, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(vsizer2, 1, wx.EXPAND | wx.ALL, 5)
        
        p.SetSizerAndFit(sizer)
        p.SetAutoLayout(1)
        sizer.Fit(p)
        self.Center()

    # Bound to Checkbox
    # If unchecked, replaces 
    def CheckAutoPorts(self, event):
        if self.ScanCheckBox.GetValue():
            self.ScanCheckBox.SetLabel("Scanning...")
            list = self.scan()
            self.ScanCheckBox.SetLabel("Showing active ports")
            list.append(self.Port1Selector.GetValue())
            list.append(self.Port2Selector.GetValue())
            list.sort(key=self.COMsort)
        else:
            list = ["COM" + str(i) for i in xrange(1, MAXPORTS + 1)]
            self.ScanCheckBox.SetLabel("Showing all ports")
        self.FillDropdown(self.Port1Selector, list)
        self.FillDropdown(self.Port2Selector, list)
        
    # Fills dropdown with provided list 
    def FillDropdown(self, dropdown, ports):
        sel = dropdown.GetValue()
        dropdown.Clear()
        dropdown.AppendItems(ports)
        dropdown.SetStringSelection(sel)
        
    def COMsort(self, s):
        return int(s[3:])
    
    def scan(self):
        """scan for available ports. return a list of the names"""
        available = []
        for i in xrange(MAXPORTS):
            try:
                s = serial.Serial(i)
                available.append(s.portstr)
                s.close()   # explicit close 'cause of delayed GC in java
            except serial.SerialException:
                pass
        return available
    
    def OnSendToZConpPress(self, event):
        self.RunThreads = True
        self.ClearStoppedThreads(self.ThreadList)
        t = threading.Thread(name="SendToZConpThread", target=self.SendToZConpThread)
        t.start()
        self.ThreadList.append(t)

    def OnStopZConpPress(self, event):
        if DEBUG: print self.GetSize()
        self.RunThreads = False
    
    ##################################################################    
    # Make changes to backend here
    def SendToZConpThread(self):
        # Setup
        self.TBAppend(self.TB1, "Starting ZConp thread...")
        port = self.OpenCOMPort(self.Port1Selector.GetValue())
        
        if port:
            # Main Loop
            while self.RunThreads:
                self.TB1.AppendText(str(port.read(1))) # Reads one character out of the serial port and writes it
        else:
            self.ErrorDialog("Not able to connect to "+self.Port1Selector.GetValue())
        
        # Cleanup
        self.TBAppend(self.TB1, "Stopping ZConp thread...")
        self.CloseCOMPort(port)

    
    def OnOpenFilePress(self, event):
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, self.filename,
                            "All files (*.*)|*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            
            # Open the file, read the contents
            with open(os.path.join(self.dirname, self.filename),'r') as f:  # Use 'rb' to read binary data
                file_data_string = f.read()
        
            # Do stuff with file_data_string here
        
        dlg.Destroy()
        
    ##################################################################
    
    def OpenCOMPort(self, portname, baud=9600, bytes=8, par='N', stop=1, time=0.5):
        try:
            port = serial.Serial(port=portname, baudrate=baud, bytesize=bytes, parity=par,
                              stopbits=stop, timeout=time)
        except serial.SerialException as e:
            self.ErrorDialog("Can't open {0}. Check your config settings.\n".format(portname) + str(e),
                               "Can't open COM port", ERROR)
            port = None
        except ValueError as e:
            self.ErrorDialog("Invalid parameter when attempting to open {0}. ".format(portname) + 
                               "Check your config settings.\n" + str(e),
                               "Can't open COM port", ERROR)
            port = None    
        return port
    
    def CloseCOMPort(self, port):
        if port and port.isOpen(): port.close()

    def ErrorDialog(self, e):
        dial = wx.MessageDialog(None, e, 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
    
    def OnGainFocusTB(self, event):
        wx.CallAfter(event.GetEventObject().SelectAll)    
    
    def TBAppend(self, tb, i):
        temp = "[{0}] {1}\n".format(self.ftime(), str(i))
        tb.AppendText(temp)
    
    def ftime(self):
        # Truncate to third decimal place, and remove leading zero
        s = "{0:.03}".format(time.time() % 1)[1:]
        # Add trailing zeroes to fractional seconds
        return time.strftime("%m-%d-%y %H:%M:%S")+"{0:0<4}".format(s)
    
    def ClearStoppedThreads(self, l):
        for t in l[:]:
            if not t.isAlive(): l.remove(t)
    
    def OnClose(self, event):
        t = threading.Thread(name="Close", target=self.CloseThreads)
        t.start()
        
    def CloseThreads(self):
        self.RunThreads = False
#        print self.ThreadList
        t = time.clock()
        while ((True in [th.isAlive() for th in self.ThreadList]) and time.clock() < t + 5):
            pass
#        print self.ThreadList
        self.Destroy()

if __name__ == "__main__":
    app = wx.App(redirect=False)
    FunctionTestFrame().Show()
    app.MainLoop()
