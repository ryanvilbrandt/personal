#!/usr/bin/python
# -*- coding: UTF-8 -*-
#import pychecker.checker

# Display items to add:
# Gbat always on?
# Only respond to/report ZIDs from MAC address? 
# Load up a collection of Gbat readings
# Datalog server doesn't disconnect until pump board ends connection

import wx, serial, time, os, sys, threading, re, subprocess, socket, select, ConfigParser, struct, mmap
import wx.grid as gridlib
import winsound as ws

# Process command line arguments
DEBUG = False
#print sys.argv
if "-debug" in sys.argv:
    DEBUG = True

VERSION = "1.0.3"
TITLE = "PyGrep v"+VERSION+"RC1"
NORMAL, ERROR, SUCCESS = 0, 1, 2
LOGFILENAME = "zfunction test log {0}.txt"
NEXGENLOGFILENAME = "zfunction nexgen log {0}.txt"
DATALOGLOGFILENAME = "zfunction datalog log {0}.txt"
SOUNDS = {"start sound": "C:\windows\Media\chord.wav", "error sound": "C:\windows\Media\Windows XP Error.wav",
          "success sound": "C:\windows\Media\tada.wav"}
if not os.path.isfile(SOUNDS["error sound"]):
    SOUNDS["error sound"] = "C:\windows\Media\Windows Error.wav"
MAXPORTS = 48
CONFIG_FILENAME = "settings.cfg"

class FunctionTestFrame(wx.Frame):
    
    RunThreads = True
    NexGenThreadRunning = False
    DatalogThreadRunning = False
    ThreadList = []
    IgnoreMAC = ""
    LastMessage = None
    SubmitNames = [ 'pump ip', 'datalog ip', 'NexGen ip', 'tftp ip', 'network mask', 'default gateway',
                    'listen port', 'datalog port', 'NexGen port', 'mac oui', 'pump id', 'distance to ground' ]
    DEFAULT_COLOR = "White"
    NORMAL_TEXT_COLOR = "Black"
#    NON_DEFAULT_COLOR = (255, 255, 175, 255) # Pale Yellow
#    ERROR_COLOR = (255, 50, 50, 255) # Pale Red
    ERROR_TEXT_COLOR = "White"
    ERROR_BG_COLOR = (150, 0, 0, 255) # Red
    SUCCESS_TEXT_COLOR = "White"
    SUCCESS_BG_COLOR = (0, 150, 0, 255) # Green
    
    DirList = []
    
    def __init__(self):
        wx.Frame.__init__(self, None, title=TITLE, style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | 
                          wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        
        self.Config = self.InitConfig()
        self.InitGUI(self.Config)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def InitGUI(self, config):
        self.SetMinSize(wx.Size(480, 500))
#        self.SetSize(wx.Size(1150, 700))

        p = wx.Panel(self)

        self.DirectoryListBox = wx.ListBox(p, style=wx.LB_RIGHT)
        addDirectoryButton = wx.Button(p, label="Add Directory...")
        addDirectoryButton.Bind(wx.EVT_BUTTON, self.AddToDirList)
        removeDirectoryButton = wx.Button(p, label="Remove Selected")
        removeDirectoryButton.Bind(wx.EVT_BUTTON, self.RemoveFromDirList)
        self.SubfoldersCheckbox = wx.CheckBox(p, label="incl. subfolders")


        self.BooleanTypeDropdown = wx.ComboBox(p, style=wx.CB_READONLY|wx.CB_DROPDOWN, choices=["AND","OR"])
        self.BooleanTypeDropdown.SetSelection(0)
        self.NormalRadioButton = wx.RadioButton(p, label='Normal', style=wx.RB_GROUP)
        self.RegexRadioButton = wx.RadioButton(p, label='Regex')

        self.KeywordTBList = [wx.TextCtrl(p) for i in xrange(5)]
        for tb in self.KeywordTBList:
            tb.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)

        self.SearchAllRB = wx.RadioButton(p, label='Search all file types', style=wx.RB_GROUP)
        self.SearchOnlyRB = wx.RadioButton(p, label='Search only:')
        self.SearchNotRB = wx.RadioButton(p, label='Search all EXCEPT:')
        self.SearchOnlyTB = wx.TextCtrl(p)
        self.SearchOnlyTB.SetValue("TXT CSV")
        self.SearchNotTB = wx.TextCtrl(p)
        self.SearchNotTB.SetValue("EXE DLL")


        self.ResultsGrid = gridlib.Grid(p)
        self.ResultsGrid.CreateGrid(5, 2)
        self.ResultsGrid.SetRowLabelSize(0)
        self.ResultsGrid.SetColLabelSize(20)
        self.ResultsGrid.Bind(wx.EVT_SIZE, self.AutoGridSize)
#        print self.ResultsGrid.GetSize()
#        print self.GetSize()

        searchButton = wx.Button(p, label="Search")
        searchButton.Bind(wx.EVT_BUTTON, self.SearchPress)

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        hsizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add Directory box/sizer
        directoryBox = wx.StaticBox(p, label='Directories to search')
        directorySizer = wx.StaticBoxSizer(directoryBox, wx.VERTICAL)
        directorySizer.Add(self.DirectoryListBox, 1, wx.EXPAND)
        dirButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
        dirButtonSizer.Add(addDirectoryButton, 0, wx.ALL, border=2)
        dirButtonSizer.Add(removeDirectoryButton, 0, wx.ALL, border=2)
        directorySizer.Add(dirButtonSizer, 0, wx.EXPAND)
        directorySizer.Add(self.SubfoldersCheckbox, 0, wx.ALL, border=2)
        hsizer.Add(directorySizer, 1, wx.EXPAND | wx.ALL, border=2)
        
        # Add Keywords box/sizer
        keywordsBox = wx.StaticBox(p, label='Keyphrases to search for')
        keywordsSizer = wx.StaticBoxSizer(keywordsBox, wx.VERTICAL)
        hsizer_keywords = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_keywords.Add(self.BooleanTypeDropdown, 0, wx.ALL, border=2)
        hsizer_keywords.Add(self.NormalRadioButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        hsizer_keywords.Add(self.RegexRadioButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        keywordsSizer.Add(hsizer_keywords, 1, wx.EXPAND)
        for tb in self.KeywordTBList:
            keywordsSizer.Add(tb, 0, wx.EXPAND | wx.ALL, border=2)
        keywordsSizer.Add(self.SearchAllRB, 0, wx.ALL, border=2)
        hsizer_search_only = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_search_only.Add(self.SearchOnlyRB, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        hsizer_search_only.Add(self.SearchOnlyTB, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        keywordsSizer.Add(hsizer_search_only, 1, wx.EXPAND)
        hsizer_search_not = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_search_not.Add(self.SearchNotRB, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        hsizer_search_not.Add(self.SearchNotTB, 1, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        keywordsSizer.Add(hsizer_search_not, 1, wx.EXPAND)
        hsizer.Add(keywordsSizer, 1, wx.EXPAND | wx.ALL, border=2)
        sizer.Add(hsizer, 0, wx.EXPAND)
        
        
        # Add Results grid box/sizer
        resultsBox = wx.StaticBox(p, label='Keyphrases to search for')
        resultsSizer = wx.StaticBoxSizer(resultsBox, wx.VERTICAL)
        resultsSizer.Add(self.ResultsGrid, 1, wx.EXPAND | wx.ALL, border=2)
        resultsSizer.Add(searchButton, 0, wx.ALL, border=2)
#        hsizer_results = wx.BoxSizer(wx.HORIZONTAL)
#        hsizer_results.Add(self.BooleanTypeDropdown, 0)
#        hsizer_results.Add(self.NormalRadioButton, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        hsizer_results.Add(self.RegexRadioButton, 0)
#        resultsSizer.Add(hsizer_results, 1, wx.EXPAND)
        
        sizer.Add(resultsSizer, 1, wx.EXPAND | wx.ALL, border=2)

#        self.HistoryTB = wx.TextCtrl(p, style=wx.TE_READONLY | wx.TE_MULTILINE)
#        self.NexGenTB = wx.TextCtrl(p, style=wx.TE_READONLY | wx.TE_MULTILINE)

        # COM port selectors and scan checkbox
#        self.UltraPortSelector = wx.ComboBox(p, style=wx.CB_DROPDOWN | wx.CB_READONLY)
#        self.InfraPortSelector = wx.ComboBox(p, style=wx.CB_DROPDOWN | wx.CB_READONLY)
#        self.TruckPortSelector = wx.ComboBox(p, style=wx.CB_DROPDOWN | wx.CB_READONLY)
#        
#        self.ScanCheckBox = wx.CheckBox(p, label="Showing active ports")
#        self.ScanCheckBox.SetValue(eval(self.ConfigGet('Scan Check Box', 'True')))
#        self.ScanCheckBox.Bind(wx.EVT_CHECKBOX, self.CheckAutoPorts)
#        
#        if self.ScanCheckBox.GetValue():
#            port_items = self.scan()
#            if not port_items:
#                port_items = ["          "]
#        else:
#            port_items = ["COM" + str(i) for i in xrange(1, MAXPORTS + 1)]
#        self.UltraPortSelector.AppendItems(port_items)
#        self.InfraPortSelector.AppendItems(port_items)
#        self.TruckPortSelector.AppendItems(port_items)
#        ultra = self.ConfigGet('Ultra COM Port')
#        infra = self.ConfigGet('Infra COM Port')
#        truck = self.ConfigGet('Truck COM Port')
#        # If the COM port defined in the config file is available, use that
#        # Otherwise, use the next available COM port in the list
#        # Otherwise, leave blank
#        if ultra in port_items:
#            self.UltraPortSelector.SetValue(ultra)
#            port_items.remove(ultra)
#        elif port_items:
#            self.UltraPortSelector.SetValue(port_items[0])
#            del port_items[0]
#        if infra in port_items:
#            self.InfraPortSelector.SetValue(infra)
#            port_items.remove(infra)
#        elif port_items:
#            self.InfraPortSelector.SetValue(port_items[0])
#            del port_items[0]
#        if truck in port_items:
#            self.TruckPortSelector.SetValue(truck)
#            port_items.remove(truck)
#        elif port_items:
#            self.TruckPortSelector.SetValue(port_items[0])
#            del port_items[0]
#        
#        self.TruckRadioList = [wx.RadioButton(p, label='Validation Tool', style=wx.RB_GROUP),
#                               wx.RadioButton(p, label='Truck Board')]
#        self.TruckRadioList[eval(str(self.ConfigGet('Truck Board', 0)))].SetValue(True)
#        
#        self.NetworkTBList = [wx.TextCtrl(p, size=wx.Size(95, -1)) for i in xrange(9)]
#        for tb in self.NetworkTBList:
#            tb.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
#        self.NetworkTBList[0].SetValue(self.ConfigGet('Pump IP', "10.0.2.220"))
#        self.NetworkTBList[1].SetValue(self.ConfigGet('Datalog IP', "10.0.2.64"))
#        self.NetworkTBList[2].SetValue(self.ConfigGet('Datalog Port', "9829"))
#        self.NetworkTBList[3].SetValue(self.ConfigGet('NexGen IP', "10.0.2.64"))
#        self.NetworkTBList[4].SetValue(self.ConfigGet('NexGen Port', "6627"))
#        self.NetworkTBList[5].SetValue(self.ConfigGet('TFTP IP', "10.0.2.64"))
#        self.NetworkTBList[6].SetValue(self.ConfigGet('Default Gateway', "10.0.0.1"))
#        self.NetworkTBList[7].SetValue(self.ConfigGet('Network Mask', "255.255.0.0"))
#        self.NetworkTBList[8].SetValue(self.ConfigGet('MAC Address', "64FC8C10001D"))
#        self.NetworkGetButton = wx.Button(p, label="Get")
#        self.NetworkGetButton.Bind(wx.EVT_BUTTON, self.NetworkGetPress)
#        self.NetworkSubmitButton = wx.Button(p, label="Submit")
#        self.NetworkSubmitButton.Bind(wx.EVT_BUTTON, self.NetworkSubmitPress)
#        
#        # Test start options
#        self.TestStartPingCheckbox = wx.CheckBox(p, label="Ping board")
#        self.TestStartPingCheckbox.SetValue(eval(self.ConfigGet('Test Start Ping Checkbox', 'True')))
#        self.TestStartZIDCheckbox = wx.CheckBox(p, label="Check ZID")
#        self.TestStartZIDCheckbox.SetValue(eval(self.ConfigGet('Test Start ZID Checkbox', 'True')))
#        self.LoadUltraCheckbox = wx.CheckBox(p, label="Load Ultra COM")
#        self.LoadUltraCheckbox.SetValue(eval(self.ConfigGet('Load Ultra Checkbox', 'True')))
#        self.LoadInfraCheckbox = wx.CheckBox(p, label="Load Infra COM")
#        self.LoadInfraCheckbox.SetValue(eval(self.ConfigGet('Load Infra Checkbox', 'True')))
#        self.LoadTruckCheckbox = wx.CheckBox(p, label="Load Truck COM")
#        self.LoadTruckCheckbox.SetValue(eval(self.ConfigGet('Load Truck Checkbox', 'True')))
#        
#        # Display options
#        self.RadioMessagesCheckbox = wx.CheckBox(p, label="Radio messages")
#        self.RadioMessagesCheckbox.SetValue(eval(self.ConfigGet('Radio Messages Checkbox', 'False')))
#        self.RadioResponsesCheckbox = wx.CheckBox(p, label="Radio responses")
#        self.RadioResponsesCheckbox.SetValue(eval(self.ConfigGet('Radio Responses Checkbox', 'True')))
#        self.NexGenMessagesCheckbox = wx.CheckBox(p, label="NexGen messages (full)")
#        self.NexGenMessagesCheckbox.SetValue(eval(self.ConfigGet('NexGen Messages Checkbox', 'False')))
#        self.NexGenEventsCheckbox = wx.CheckBox(p, label="NexGen events only")
#        self.NexGenEventsCheckbox.SetValue(eval(self.ConfigGet('NexGen Events Checkbox', 'False')))
#        self.DatalogMessagesCheckbox = wx.CheckBox(p, label="Datalog messages (full)")
#        self.DatalogMessagesCheckbox.SetValue(eval(self.ConfigGet('Datalog Messages Checkbox', 'False')))
#        self.DatalogEventsCheckbox = wx.CheckBox(p, label="Datalog events only")
#        self.DatalogEventsCheckbox.SetValue(eval(self.ConfigGet('Datalog Events Checkbox', 'False')))
#        self.PlaySoundsCheckbox = wx.CheckBox(p, label="Play sounds")
#        self.PlaySoundsCheckbox.SetValue(eval(self.ConfigGet('Play Sounds Checkbox', 'True')))
#        
#        self.LogHistoryCheckbox = wx.CheckBox(p, label="Log History")
#        self.LogHistoryCheckbox.SetValue(eval(self.ConfigGet('Log History Checkbox', 'True')))
#        self.NexGenLogHistoryCheckbox = wx.CheckBox(p, label="Log NexGen History")
#        self.NexGenLogHistoryCheckbox.SetValue(eval(self.ConfigGet('Log NexGen History Checkbox', 'False')))
#        self.DatalogLogHistoryCheckbox = wx.CheckBox(p, label="Log Datalog History")
#        self.DatalogLogHistoryCheckbox.SetValue(eval(self.ConfigGet('Log Datalog History Checkbox', 'False')))
#        
#        self.EchoesSpin = wx.SpinCtrl(p, value=self.ConfigGet('Num echoes', '20'), min=1, max=999, size=(49, -1))
#        self.EchoesSpin.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusSpin)
#        self.FailTimeSpin = wx.SpinCtrl(p, value=self.ConfigGet('Time til fail', '20'), min=1, max=999, size=(49, -1))
#        self.FailTimeSpin.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusSpin)
#        self.WaitSpin = wx.SpinCtrl(p, value=self.ConfigGet('Wait time', '10'), min=0, max=999, size=(49, -1))
#        self.WaitSpin.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusSpin)
#        self.RepeatTestCheckBox = wx.CheckBox(p, label="Repeat Test?")
#        self.RepeatTestCheckBox.SetValue(eval(self.ConfigGet('Repeat Test Checkbox', 'True')))
#        self.GbatIdleSpin = wx.SpinCtrl(p, value=self.ConfigGet('Not Present distance', '200'), min=0, max=999, size=(49, -1))
#        self.GbatIdleSpin.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusSpin)
#        self.GbatRunSpin = wx.SpinCtrl(p, value=self.ConfigGet('Present distance', '100'), min=0, max=999, size=(49, -1))
#        self.GbatRunSpin.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusSpin)
#        
#        self.ZIDTB = wx.TextCtrl(p, size=wx.Size(185, -1))
#        self.ZIDTB.SetValue(self.ConfigGet('ZID', "ZONARTESTSTATION1"))
#        self.ZIDTB.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
#        
##        self.GbatMessageTB = wx.TextCtrl(p, size=wx.Size(300, -1))
##        self.GbatMessageTB.SetValue('R506*10 + R100*10 + R506*5 + R100*5')
##        self.GbatMessageTB.Disable()
#        
#        self.StartButton = wx.Button(p, label="Start")
#        self.StartButton.Bind(wx.EVT_BUTTON, self.OnStartStopPress)
#        
#        self.SaveSettingsButton = wx.Button(p, label="Save Settings...")
#        self.SaveSettingsButton.Bind(wx.EVT_BUTTON, self.OnSaveSettingsPress)
#
#        #Add Controls box/sizer
#        controlsSizer = wx.BoxSizer(wx.HORIZONTAL)
#        portsSizer = wx.GridBagSizer(2,5)
#        portsSizer.Add(wx.StaticText(p, label="Ultra:"), (0,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        portsSizer.Add(self.UltraPortSelector, (0,1))
#        portsSizer.Add(wx.StaticText(p, label="Infra:"), (1,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        portsSizer.Add(self.InfraPortSelector, (1,1))
#        portsSizer.Add(wx.StaticText(p, label="Truck:"), (2,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        portsSizer.Add(self.TruckPortSelector, (2,1))
#        portsSizer.Add(self.ScanCheckBox, (3,0), (1,2))
#        portsBox = wx.StaticBox(p, label='COM Ports')
#        portsBoxSizer = wx.StaticBoxSizer(portsBox, wx.VERTICAL)
#        portsBoxSizer.Add(portsSizer, 0)
#        
#        truckBox = wx.StaticBox(p, label='For truck, use:')
#        truckSizer = wx.StaticBoxSizer(truckBox, wx.VERTICAL)
#        truckSizer.Add(self.TruckRadioList[0], 0, wx.EXPAND | wx.BOTTOM, border=2)
#        truckSizer.Add(self.TruckRadioList[1], 0, wx.EXPAND)
#        
#        networkSizer = wx.GridBagSizer(2,5)
#        networkSizer.Add(wx.StaticText(p, label="Pump:"), (0,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        networkSizer.Add(wx.StaticText(p, label="Datalog:"), (1,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        networkSizer.Add(wx.StaticText(p, label="DL Port:"), (2,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        networkSizer.Add(wx.StaticText(p, label="NexGen:"), (3,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        networkSizer.Add(wx.StaticText(p, label="NG Port:"), (4,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        networkSizer.Add(wx.StaticText(p, label="TFTP:"), (5,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        networkSizer.Add(wx.StaticText(p, label="Gateway:"), (6,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        networkSizer.Add(wx.StaticText(p, label="Mask:"), (7,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        networkSizer.Add(wx.StaticText(p, label="MAC:"), (8,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        for i in xrange(len(self.NetworkTBList)):
#            networkSizer.Add(self.NetworkTBList[i], (i,1))
#        networkBox = wx.StaticBox(p, label='Network')
#        networkBoxSizer = wx.StaticBoxSizer(networkBox, wx.VERTICAL)
#        networkBoxSizer.Add(networkSizer, 0, wx.BOTTOM, border=5)
#        networkButtonSizer = wx.BoxSizer(wx.HORIZONTAL)
#        networkButtonSizer.Add(self.NetworkGetButton, 0, wx.EXPAND)
#        networkButtonSizer.Add(self.NetworkSubmitButton, 0, wx.EXPAND)
#        networkBoxSizer.Add(networkButtonSizer, 0)
#        
#        testStartBox = wx.StaticBox(p, label='Test check')
#        testStartSizer = wx.StaticBoxSizer(testStartBox, wx.VERTICAL)
#        testStartSizer.Add(self.TestStartPingCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        testStartSizer.Add(self.TestStartZIDCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        testStartSizer.Add(self.LoadUltraCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        testStartSizer.Add(self.LoadInfraCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        testStartSizer.Add(self.LoadTruckCheckbox, 0, wx.EXPAND)
#        
#        displayBox = wx.StaticBox(p, label='Display options')
#        displaySizer = wx.StaticBoxSizer(displayBox, wx.VERTICAL)
#        displaySizer.Add(self.RadioMessagesCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        displaySizer.Add(self.RadioResponsesCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        displaySizer.Add(self.NexGenMessagesCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        displaySizer.Add(self.NexGenEventsCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        displaySizer.Add(self.DatalogMessagesCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        displaySizer.Add(self.DatalogEventsCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        displaySizer.Add(self.PlaySoundsCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        
#        testConfigSizer = wx.GridBagSizer(2,5)
#        testConfigSizer.Add(wx.StaticText(p, label="# echoes:"), (0,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        testConfigSizer.Add(self.EchoesSpin, (0,1))
#        testConfigSizer.Add(wx.StaticText(p, label="Time til fail (s):"), (1,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        testConfigSizer.Add(self.FailTimeSpin, (1,1))
#        testConfigSizer.Add(wx.StaticText(p, label="Wait time (s):"), (2,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        testConfigSizer.Add(self.WaitSpin, (2,1))
#        testConfigSizer.Add(self.RepeatTestCheckBox, (3,0), (1,2))
#        testConfigBox = wx.StaticBox(p, label='Test config')
#        testConfigBoxSizer = wx.StaticBoxSizer(testConfigBox, wx.VERTICAL)
#        testConfigBoxSizer.Add(testConfigSizer, 0)
#        
#        logBox = wx.StaticBox(p, label='Logging options')
#        logSizer = wx.StaticBoxSizer(logBox, wx.VERTICAL)
#        logSizer.Add(self.LogHistoryCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        logSizer.Add(self.NexGenLogHistoryCheckbox, 0, wx.EXPAND | wx.BOTTOM, border=2)
#        logSizer.Add(self.DatalogLogHistoryCheckbox, 0, wx.EXPAND)
#        
#        gbatConfigSizer = wx.GridBagSizer(2,5)
#        gbatConfigSizer.Add(wx.StaticText(p, label="Not Present distance (cm):"), (0,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        gbatConfigSizer.Add(self.GbatIdleSpin, (0,1))
#        gbatConfigSizer.Add(wx.StaticText(p, label="Present distance (cm):"), (1,0), wx.DefaultSpan, wx.ALIGN_CENTER_VERTICAL)
#        gbatConfigSizer.Add(self.GbatRunSpin, (1,1))
#        gbatConfigBox = wx.StaticBox(p, label='Gbat config')
#        gbatConfigBoxSizer = wx.StaticBoxSizer(gbatConfigBox, wx.VERTICAL)
#        gbatConfigBoxSizer.Add(gbatConfigSizer, 0)
#        
#        zidBox = wx.StaticBox(p, label='ZID')
#        zidBoxSizer = wx.StaticBoxSizer(zidBox, wx.VERTICAL)
#        zidBoxSizer.Add(self.ZIDTB, 0, wx.EXPAND)
#        
#        buttonSizer = wx.BoxSizer(wx.VERTICAL)
#        buttonSizer.Add(self.StartButton, 0, wx.BOTTOM, border=5)
#        buttonSizer.Add(self.SaveSettingsButton, 0)
#        
#        vSizer1 = wx.BoxSizer(wx.VERTICAL)
#        vSizer1.Add(portsBoxSizer, 0, wx.EXPAND)
#        vSizer1.Add(truckSizer, 0, wx.EXPAND)
#        controlsSizer.Add(vSizer1, 0)
#        controlsSizer.Add(networkBoxSizer, 0)
#        vSizer3 = wx.BoxSizer(wx.VERTICAL)
#        vSizer3.Add(testStartSizer, 0, wx.EXPAND)
#        vSizer3.Add(displaySizer, 0)
#        controlsSizer.Add(vSizer3, 0)
#        vSizer4 = wx.BoxSizer(wx.VERTICAL)
#        vSizer4.Add(testConfigBoxSizer, 0, wx.EXPAND)
#        vSizer4.Add(logSizer, 0, wx.EXPAND)
#        controlsSizer.Add(vSizer4, 0)
#        vSizer5 = wx.BoxSizer(wx.VERTICAL)
#        vSizer5.Add(gbatConfigBoxSizer, 0)
#        vSizer5.Add(zidBoxSizer, 0, wx.EXPAND)
#        controlsSizer.Add(vSizer5, 0)
#        controlsSizer.Add(buttonSizer, 0)
#        sizer.Add(controlsSizer, 0, wx.EXPAND | wx.ALL, border=5)
        
        p.SetSizerAndFit(sizer)
        p.SetAutoLayout(1)
        sizer.Fit(p)
        self.Center()
    
    def ConfigGet(self, option, default='', section='Settings'):
        if self.Config and self.Config.has_section(section) and self.Config.has_option(section, option):
            return self.Config.get(section, option)
        else:
            return default
    
#    def str2bool(self, s):
#        b = ['false', 'f', 'no', '0', '']
#        return not s in b
    
    # Bound to Checkbox
    # If unchecked, replaces 
    
    def OnSaveSettingsPress(self, event):
        section = None
        if not self.Config.has_section(section):
            self.Config.add_section(section)
        self.Config.set(section, 'Ultra COM Port', self.UltraPortSelector.GetValue())
        self.Config.set(section, 'Infra COM Port', self.InfraPortSelector.GetValue())
        self.Config.set(section, 'Truck COM Port', self.TruckPortSelector.GetValue())
        self.Config.set(section, 'Scan Check Box', self.ScanCheckBox.GetValue())
        self.Config.set(section, 'Pump IP', self.NetworkTBList[0].GetValue())
        self.Config.set(section, 'Datalog IP', self.NetworkTBList[1].GetValue())
        self.Config.set(section, 'Datalog Port', self.NetworkTBList[2].GetValue())
        self.Config.set(section, 'NexGen IP', self.NetworkTBList[3].GetValue())
        self.Config.set(section, 'NexGen Port', self.NetworkTBList[4].GetValue())
        self.Config.set(section, 'TFTP IP', self.NetworkTBList[5].GetValue())
        self.Config.set(section, 'Default Gateway', self.NetworkTBList[6].GetValue())
        self.Config.set(section, 'Network Mask', self.NetworkTBList[7].GetValue())
        self.Config.set(section, 'MAC Address', self.NetworkTBList[8].GetValue())
        self.Config.set(section, 'ZID', self.ZIDTB.GetValue())
        self.Config.set(section, 'Test Start Ping Checkbox', self.TestStartPingCheckbox.GetValue())
        self.Config.set(section, 'Test Start ZID Checkbox', self.TestStartZIDCheckbox.GetValue())
        self.Config.set(section, 'Load Ultra Checkbox', self.LoadUltraCheckbox.GetValue())
        self.Config.set(section, 'Load Infra Checkbox', self.LoadInfraCheckbox.GetValue())
        self.Config.set(section, 'Load Truck Checkbox', self.LoadTruckCheckbox.GetValue())
        self.Config.set(section, 'Radio Messages Checkbox', self.RadioMessagesCheckbox.GetValue())
        self.Config.set(section, 'Radio Responses Checkbox', self.RadioResponsesCheckbox.GetValue())
        self.Config.set(section, 'NexGen Messages Checkbox', self.NexGenMessagesCheckbox.GetValue())
        self.Config.set(section, 'Datalog Messages Checkbox', self.DatalogMessagesCheckbox.GetValue())
        self.Config.set(section, 'Datalog Events Checkbox', self.DatalogEventsCheckbox.GetValue())
        self.Config.set(section, 'Play Sounds Checkbox', self.PlaySoundsCheckbox.GetValue())
        self.Config.set(section, 'Log History Checkbox', self.PlaySoundsCheckbox.GetValue())
        self.Config.set(section, 'Log NexGen History Checkbox', self.PlaySoundsCheckbox.GetValue())
        self.Config.set(section, 'Log Datalog History Checkbox', self.PlaySoundsCheckbox.GetValue())
        self.Config.set(section, 'Num echoes', self.EchoesSpin.GetValue())
        self.Config.set(section, 'Time til fail', self.FailTimeSpin.GetValue())
        self.Config.set(section, 'Wait time', self.WaitSpin.GetValue())
        self.Config.set(section, 'Repeat Test Checkbox', self.RepeatTestCheckBox.GetValue())
        self.Config.set(section, 'Not Present distance', self.GbatIdleSpin.GetValue())
        self.Config.set(section, 'Present distance', self.GbatRunSpin.GetValue())
        self.Config.set(section, 'Truck board', [b.GetValue() for b in self.TruckRadioList].index(True))
        
        with open(CONFIG_FILENAME, 'wb') as configfile:
            self.Config.write(configfile)
    
    def InitConfig(self):
        config = ConfigParser.ConfigParser()
        if os.path.isfile(CONFIG_FILENAME):
            config.read(CONFIG_FILENAME)
        return config
    
    def ErrorDialog(self, e):
        dial = wx.MessageDialog(None, e, 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
    
    def TestGetSize(self, event):
        print self.GetSize()
    
    def OnGainFocusTB(self, event):
        wx.CallAfter(event.GetEventObject().SelectAll) 
    
    def OnGainFocusSpin(self, event):
        wx.CallAfter(event.GetEventObject().SetSelection,0,-1)
    
    def AutoGridSize(self, event):
        event.Skip()
    
    def AddToDirList(self, event):
        """
        Calls up a new Character Sheet window, and adds the character to the Master list, if it has a valid name.
        Updates the character's perm status for the current date. For this reason, only add new characters at the 
        beginning of a season, or expect their perm status to be slightly out of wack, if the date has changed since
        the start of the season.
        """
        bad_name = False 
        dlg = wx.DirDialog(self, "Choose a directory:",
                          style=wx.DD_DEFAULT_STYLE
                           #| wx.DD_DIR_MUST_EXIST
                           #| wx.DD_CHANGE_DIR
                           )
        if dlg.ShowModal() == wx.ID_OK:
            new_path = dlg.GetPath()
        else:
            new_path = ""
        dlg.Destroy()
        
        if new_path:
            self.DirList.append(new_path)
            self.DirectoryListBox.Set(self.DirList)
            self.DirectoryListBox.SetSelection(len(self.DirList)-1)
        
        
    def RemoveFromDirList(self, event):
        """Removes all selected items from the Directory list."""
        sel = self.DirectoryListBox.GetSelections()
        self.DirList = [x for i,x in enumerate(self.DirList)
                                if i not in sel]
        self.DirectoryListBox.Set(self.DirList)
        
    def SearchPress(self, event):
        pass
    
    def SearchFile(self, file_name, pattern):
        try:
            f = open(file_name)
        except Exception:
            return False
        s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        if pattern in s:
            print 'true'
        f.close()


#    def CheckAutoPorts(self, event):
#        if self.ScanCheckBox.GetValue():
#            self.ScanCheckBox.SetLabel("Scanning...")
#            list = self.scan()
#            self.ScanCheckBox.SetLabel("Showing active ports")
#            if self.UltraPort and self.UltraPort.isOpen(): list.append(self.UltraPortSelector.GetValue())
#            if self.InfraPort and self.InfraPort.isOpen(): list.append(self.InfraPortSelector.GetValue())
#            if self.TruckPort and self.TruckPort.isOpen(): list.append(self.TruckPortSelector.GetValue())
#            list.sort(key=self.COMsort)
#        else:
#            list = ["COM" + str(i) for i in xrange(1, MAXPORTS + 1)]
#            self.ScanCheckBox.SetLabel("Showing all ports")
#        self.FillDropdown(self.UltraPortSelector, list)
#        self.FillDropdown(self.InfraPortSelector, list)
#        self.FillDropdown(self.TruckPortSelector, list)
#        
#    # Fills dropdown with provided list 
#    def FillDropdown(self, dropdown, ports):
#        sel = dropdown.GetValue()
#        dropdown.Clear()
#        dropdown.AppendItems(ports)
#        dropdown.SetStringSelection(sel)
#        
#    def COMsort(self, s):
#        return int(s[3:])
#    
#    def scan(self):
#        """scan for available ports. return a list of the names"""
#        available = []
#        for i in xrange(MAXPORTS):
#            try:
#                s = serial.Serial(i)
#                available.append(s.portstr)
#                s.close()   # explicit close 'cause of delayed GC in java
#            except serial.SerialException:
#                pass
#        return available
#    
#    def NetworkGetPress(self, event):
#        try:
#            settingsPort = serial.Serial(self.InfraPortSelector.GetValue(), 9600, timeout=0.5)
#        except serial.SerialException as strerror:
#            self.ProcessOutput(("'{0}' could not be opened. Please double-check that you've chosen the right COM port.\n" + 
#                                "(SerialException: {1})").format(self.InfraPortSelector.GetValue(), strerror), 
#                                "Couldn't open serial conn to pump board", ERROR)
#            return
#        
#        settingsPort.flushInput()
#        settingsPort.flushOutput()
#        settingsPort.write("16\r")
#        self.ProcessOutput(settingsPort.readline())
#        
#        settingsPort.flushInput()
#        settingsPort.flushOutput()
#        settingsPort.write("1\r")
#        
#        dataList = settingsPort.readlines()
#        settingsPort.close()
#        if not dataList:
#            self.ProcessOutput("Unable to talk to pump board. Make sure the cable is " +
#                               "plugged in and the board is in provisioning mode.",
#                               "No response from pump board", ERROR)
#            return
#        
#        self.ProcessOutput(str(dataList))
#
#        for i in xrange(len(dataList)):
#            if dataList[i] == "Current settings:\t\n":
#                break
#        try:
#            n = dataList.index("Current settings:\t\n")
#        except Exception:
#            self.ProcessOutput("Network settings retrieved were invalid.", 
#                               "Invalid network settings retrieved", ERROR)
#            return None
#        else:
#            dataList = dataList[n+1:]
#            for i in xrange(len(dataList)):
#                temp = dataList[i]
#                dataList[i] = temp[temp.find(": ")+2:temp.rfind("\t")]
##                parsedList = re.split("\\t\\r\\n(.*?)\: ", data[19:-1])
#            newList = dataList[:6] + dataList[6].split(':') + dataList[7:]
#            
#            self.ProcessOutput(newList,"Network settings retrieved")
#            
#            s_list = [0,1,7,2,8,3,5,4,9]
#            for i in xrange(len(s_list)):
#                self.NetworkTBList[i].SetValue(newList[s_list[i]])
#    
#    def NetworkSubmitPress(self, event):
#        success = False
#        settings = [self.NetworkTBList[0].GetValue(),
#                    self.NetworkTBList[1].GetValue(),
#                    self.NetworkTBList[3].GetValue(),
#                    self.NetworkTBList[5].GetValue(),
#                    self.NetworkTBList[7].GetValue(),
#                    self.NetworkTBList[6].GetValue(),
#                    "7879",
#                    self.NetworkTBList[2].GetValue(),
#                    self.NetworkTBList[4].GetValue(),
#                    self.NetworkTBList[8].GetValue()[:6],
#                    self.NetworkTBList[8].GetValue()[6:],
#                    "200",
#                    "183"
#                    ]
#        try:
#            submitPort = serial.Serial(self.InfraPortSelector.GetValue(), 9600, timeout=0.5)
#        except serial.SerialException as strerror:
#            self.ProcessOutput(("'{0}' could not be opened. Please double-check that you've chosen the right COM port.\n" + 
#                                "(SerialException: {1})").format(self.InfraPortSelector.GetValue(), strerror), 
#                                "Couldn't open serial conn to pump board", ERROR)
#            return
#        
#        submitPort.flushInput()
#        submitPort.flushOutput()
#        submitSettings = "15:"+":".join(settings)+"\r"
#        submitPort.write(submitSettings)
#        
#        ack = submitPort.read(2)
#        if (ack == '\x01\x01'):
#            success = True
#            self.ProcessOutput("Done!","Network settings submitted")
#        elif (ack == '\x01\x00'):
#            self.ProcessOutput("Board not provisioned due to error. Please try again.", "Error when submitting", ERROR)
#        else:
#            self.ProcessOutput("No response from the pump board when attempting to save settings "+
#                               "to EEPROM. Make sure the cable is plugged in and the board is in provisioning mode.\n",
#                               "No response from pump board", ERROR)
#            
#        submitPort.flushInput()
#        submitPort.flushOutput()
#        submitPort.write("17\r")
#        
#        submitPort.close()
#    
#    def OpenCOMPort(self, portname, baud=9600, bytes=8, par='N', stop=1, time=0.5):
#        try:
#            port = serial.Serial(port=portname, baudrate=baud, bytesize=bytes, parity=par,
#                              stopbits=stop, timeout=time)
#        except serial.SerialException as e:
#            self.ProcessOutput("Can't open {0}. Check your config settings.\n".format(portname) + str(e),
#                               "Can't open COM port", ERROR)
#            port = None
#        except ValueError as e:
#            self.ProcessOutput("Invalid parameter when attempting to open {0}. ".format(portname) + 
#                               "Check your config settings.\n" + str(e),
#                               "Can't open COM port", ERROR)
#            port = None    
#        return port
#    
#    def CloseCOMPort(self, port):
#        if port and port.isOpen(): port.close()
#    
#    def InitLogFiles(self):
#        ready = self.OpenLogConnection()
#        if not ready:
#            self.ErrorDialog("Unable to open log files. See History for details.")
#        self.CloseLogConnection()
#    
#    def InitGbat(self):
#        if self.UltraPort:
#            self.RunGbatThread = True
#            g = threading.Thread(name="Gbat", target=self.RunGbat)
#            self.ThreadList.append(g)
#            g.start()
#    
#    def OnStartStopPress(self, event):
##        print self.GetSize()
#        if self.StartButton.GetLabel() == "Start":
##            if self.ThreadList[-1].getName == "StartTest":
##                t = self.ThreadList[-1]
##                print "You shouldn't be here."
##            else:
#            self.ResetPressed = False
#            t = threading.Thread(name="StartTest", target=self.StartTest)
#            self.ThreadList.append(t)
#            t.start()
#        elif self.StartButton.GetLabel() == "Reset":
#            self.ResetPressed = True
#            
#    def StartTest(self):
#        self.ClearStoppedThreads(self.ThreadList)
#        print self.GetSize()
#        self.OpenLogConnection()
#        self.StartButton.SetLabel("Reset")
#        self.UltraPortSelector.Disable()
#        self.InfraPortSelector.Disable()
#        self.TruckPortSelector.Disable()
#        for tb in self.NetworkTBList:
#            tb.Disable()
#        self.ZIDTB.Disable()
#        self.NetworkGetButton.Disable()
#        self.NetworkSubmitButton.Disable()
#        self.RunTestThreads = True
#        if self.CheckSettings():
#            self.SetGbat('RUN')
#            self.InitGbat()
#            threadlist = [t.name for t in self.ThreadList]
##            if not self.NexGenThreadRunning:
##                nt = threading.Thread(name="NexGenListen", target=self.NexGenListen)
##                self.ThreadList.append(nt)
##                nt.start()
#            if not self.DatalogThreadRunning:
#                dt = threading.Thread(name="DatalogListen", target=self.DatalogListen)
#                self.ThreadList.append(dt)
#                dt.start()
#            if self.TruckRadioList[0].GetValue():
#                runTest = not self.ResetPressed
#                while runTest:
#                    self.RunTest(self.InfraPort, self.TruckPort)    # Main test
#                    runTest = self.RepeatTestCheckBox.GetValue() and not self.ResetPressed
#                    if runTest:
#                        self.SetGbat('IDLE')
#                        self.TestWait(self.WaitSpin.GetValue())
#                        self.SetGbat('RUN')
#                        runTest = self.RepeatTestCheckBox.GetValue() and not self.ResetPressed
#            elif self.TruckRadioList[1].GetValue():
#                self.ProcessOutput("Beginning Pump Board test procedure", "Test Started...", NORMAL, "start sound")
#                while not self.ResetPressed:
#                    time.sleep(1)
#            else:
#                self.ProcessOutput("Invalid selection in the Truck radio button area", "Bad Truck selection", ERROR, "error sound")
#        self.RunTestThreads = False
#        self.UltraPortSelector.Enable()
#        self.InfraPortSelector.Enable()
#        self.TruckPortSelector.Enable()
#        for tb in self.NetworkTBList:
#            tb.Enable()
#        self.ZIDTB.Enable()
#        self.NetworkGetButton.Enable()
#        self.NetworkSubmitButton.Enable()
#        self.CloseCOMPort(self.InfraPort)
#        self.CloseCOMPort(self.TruckPort)
#        self.StartButton.SetLabel("Start")
#        if self.ResetPressed:
#            self.ProcessOutput("Test aborted by user", "Test aborted by user")
#        self.CloseLogConnection()
##        else:
##            self.ProcessOutput("Settings are bad :-(", "", ERROR)
#    
#    def CheckSettings(self):
#        if self.TestStartPingCheckbox.GetValue() and not (self.PingBoard(self.NetworkTBList[0].GetValue())):
#            self.ProcessOutput("No network response from pump board. Please check the network settings of your computer " + 
#                               "and the Pump IP text box.", "Bad network conn to pump board", ERROR)
#            return False
#        if self.TestStartZIDCheckbox.GetValue() and not self.CheckZID(self.ZIDTB.GetValue()):
#            self.ProcessOutput("Bad ZID defined. Correct ZID must be 17 alphanumeric characters.",
#                               "Bad ZID", ERROR, "error sound")
#            self.ZIDTB.SelectAll()
#            return False
#        if self.LoadInfraCheckbox.GetValue():
#            self.InfraPort = self.OpenCOMPort(self.InfraPortSelector.GetValue(), baud=2400)
#            if not self.InfraPort:
#                return False
#        else:
#            self.InfraPort = None
#        if self.LoadTruckCheckbox.GetValue():
#            self.TruckPort = self.OpenCOMPort(self.TruckPortSelector.GetValue())
#            if not self.TruckPort:
#                return False
#        else:
#            self.TruckPort = None
#        if self.LoadUltraCheckbox.GetValue():
#            self.UltraPort = self.OpenCOMPort(self.UltraPortSelector.GetValue())
#            if not self.UltraPort:
#                return False
#        else:
#            self.UltraPort = None
#        return True
#    
#    def TestWait(self, t):
#        for i in xrange(t):
#            if self.ResetPressed:
#                return
#            time.sleep(1)
#    
#    def RunTest(self, infraPort, truckPort):
#        endTime = time.clock() + self.FailTimeSpin.GetValue()
#        START, ZID, DATA, ECHO = 0, 1, 2, 3
#        num_echoes = self.EchoesSpin.GetValue()
#        stage = START
##        list_mac = [chr(int(mac[i:i+2],16)) for i in xrange(0,len(mac),2)]
#        zid_request = "\xaa\x07\x03" #{0}{1}{2}{3}{4}{5}".format(*list_mac)
#        ir_zid = str(self.ZIDTB.GetValue())
##        ir_zid = "1\x11%M\x13E$D\x13\x14T\x14\x132w\x19z"
#        data_request = "\xaa\x12\x08" + ir_zid
#        data_response = "\xaaB\x07" + ir_zid + "   12341M2B209C11M028024    -1     -1   0\xf6\x85\x03\x00\x00\x00\x00"
#        echo_request = "\xaa\x12\x01" + ir_zid
#        echo_response = "\xaa\x12\x02" + ir_zid
#        
#        self.ProcessOutput("Beginning Pump Board test procedure", "Test Started...", NORMAL, "start sound")
#        if truckPort:
#            truckPort.flushInput()
#            truckPort.flushOutput()
#        while (time.clock() < endTime):
#            if self.ResetPressed: return NORMAL
#            if truckPort:
#                msg = self.ReadRadio(truckPort, 9)
#            else:
#                msg = ""
#            if self.RadioMessagesCheckbox.GetValue():
#                self.ProcessOutput(repr(msg))
#                
#            if msg.startswith(zid_request):
#                if infraPort:
#                    infraPort.write("\xaa"+ir_zid)
#                    if self.RadioResponsesCheckbox.GetValue():
#                        self.ProcessOutput("Received ZID request. Sent ZID over IR")
#                elif self.RadioResponsesCheckbox.GetValue():
#                    self.ProcessOutput("Received ZID request, but didn't send a ZID because the Infra COM port is disabled.")
#                stage = max(stage, ZID)
#            elif msg == data_request:
#                if self.RadioResponsesCheckbox.GetValue():
#                    self.ProcessOutput("Received data request. Sent data response")
#                truckPort.write(data_response)
#                stage = max(stage, DATA)
#            elif msg == echo_request:
#                if self.RadioResponsesCheckbox.GetValue():
#                    self.ProcessOutput("Received echo request. Sent echo response")
#                truckPort.write(echo_response)
#                stage = max(stage, ECHO)
#                num_echoes -= 1
#                if num_echoes <= 0:
##                    self.IgnoreMAC = mac
#                    self.ProcessOutput("Pump Board Test finished successfully!", "Test Passed!", SUCCESS, "success sound")
#                    truckPort.flushInput()
#                    truckPort.flushOutput()
#                    return "Test SUCCESS"
#            else:
#                pass
##            self.ProcessOutput(repr(msg))
#        
#        if stage == START:    
#            self.ProcessOutput("No radio response from pump board after detecting a 'truck' in its 'lane'. There may be an issue with the ULTRA port.",
#                               "Test Failed", ERROR, "error sound")
#            return "Test Fail - No radio response from pump board after detecting a 'truck' in its 'lane'."
#        elif stage == ZID:
#            self.ProcessOutput("No response from pump board after sending ZID over IR. Check if the INFRA LED is flashing.",
#                               "Test Failed", ERROR, "error sound")
#            return "Test Fail - No response from pump board after sending ZID over IR."
#        elif stage == DATA:
#            self.ProcessOutput("No response from pump board after sending vehicle data. Check radio connection.",
#                               "Test Failed", ERROR, "error sound")
#            return "Test Fail - No response from pump board after sending vehicle data."
#        elif stage == ECHO:
#            self.ProcessOutput("Timed out waiting for an echo response from the pump board. Check radio connection.",
#                               "Test Failed", ERROR, "error sound")
#            return "Test Fail - Timed out waiting for an echo response from the pump board."
#        else:
#            self.ProcessOutput("Unknown failure.",
#                               "Test Failed", ERROR, "error sound")
#            return "Test Fail - Unknown error"
#    
#    def PingBoard(self, host):
#        startupinfo = subprocess.STARTUPINFO()
#        startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
#        ping = subprocess.Popen(
#            ["ping", "-n", "1", "-w", "100", host],
#            stdout=subprocess.PIPE,
#            stderr=subprocess.PIPE,
#            startupinfo=startupinfo
#        )
#        
#        out, error = ping.communicate()
#        g = re.search(r"Received = (\d+)\,", out)
#        if g:
#            return (g.group(1) == "1")
#        else:
#            return False
#
#    def socketListen(self, port, timeout=10):
#        try:
#            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#            s.settimeout(timeout)
#            s.bind(('', port)) #bound to localhost
#            s.listen(6) #Listen for 6 connections
#            c, a = s.accept()
#            return c, a, None
#        except Exception, e:
#            return None, None, str(e)
#
##    def NexGenListen(self):
##        s = None
##        while not s:
##            if not self.RunTestThreads:
##                return
##            s = self.socketBind(port=6627,timeout=5)
##        self.NexGenTB.AppendText("[{0}] Listening to NexGen messages on port 6627...\n".format(self.ftime()))
##        clientConn = None
##        MSG = ""
##        while self.RunTestThreads:
##            if not clientConn:
##                self.NexGenTB.AppendText("[{0}] Attempting connection... ".format(self.ftime()))
##                s.listen(1) #Listen for 1 connection
##                try:
##                    clientConn, a = s.accept()
##                    self.NexGenTB.AppendText("Connection made!\n")
##                except Exception, e:
##                    self.NexGenTB.AppendText(repr(e)+"\n")
##            if clientConn:
##                try:
##                    ready = select.select([clientConn], [], [], 0)
##                    if ready[0]:
##                        MSG = clientConn.recv(1024)
##                except Exception, e:
##                    self.NexGenTB.AppendText(repr(e)+"\n")
##                    self.NexGenTB.AppendText("[{0}] Closing connection...\n".format(self.ftime()))
##                    if clientConn: clientConn.close()
##                    clientConn = None
##                else:
##                    if MSG:
##                        self.NexGenTB.AppendText("RECV: {0}\n".format(repr(MSG)))
##                        if MSG.startswith('\x00\x10SSC20 ') or MSG.startswith('\x00XDPT20 '):
##                            reply = MSG[:7] + 'A' + MSG[8:]
##                            clientConn.send(reply)
##                            self.NexGenTB.AppendText("SEND: {0}\n\n".format(repr(reply)))
##                            if MSG.startswith('\x00\x10SSC20 B'):
##                                self.NexGenTB.AppendText("Closing NexGen connection...\n\n".format(self.ftime()))
##                                clientConn.close()
##                                clientConn = None
##                    else:
##                        time.sleep(0.5)
##                MSG = ""
##        try:
##            clientConn.close()
##            s.close()
##        except Exception:
##            pass
##        self.NexGenTB.AppendText("[{0}] Not listening to Datalog messages anymore...\n".format(self.ftime()))
#        
#    def NexGenListen(self):
#        self.NexGenThreadRunning = True
#        port = int(self.NetworkTBList[4].GetValue())
#        self.TBAppend(self.NexGenTB,
#                      "Listening to NexGen messages on port {0}...\n".format(port),
#                      self.nexgenlogfile)
#        clientConn = None
#        while self.RunTestThreads:
#            MSG = ""
#            if not clientConn:
#                bad_msg_count = 0
##                self.NexGenTB.AppendText("[{0}] Attempting connection... ".format(self.ftime()))
#                clientConn, addrinfo, error = self.socketListen(port=port)
#                if clientConn:
#                    self.TBAppend(self.NexGenTB,
#                                  "Connection made!\n",
#                                  self.nexgenlogfile)
##                else:
##                    self.NexGenTB.AppendText(repr(error).strip("'")+"\n")
#            if clientConn:
#                try:
#                    MSG = clientConn.recv(1024)
#                    if self.NexGenMessagesCheckbox.GetValue():
#                        self.HistoryTB.AppendText(repr(MSG)+"\n")
#                except Exception, e:
#                    self.TBAppend(self.NexGenTB,
#                                  repr(e)+"\n",
#                                  self.nexgenlogfile)
#                    bad_msg_count += 1
#                    if bad_msg_count > 3:
#                        self.TBAppend(self.NexGenTB,
#                                      "Closing connection...\n",
#                                      self.nexgenlogfile)
#                        if clientConn: clientConn.close()
#                        clientConn = None
#                else:
#                    bad_msg_count = 0
#                    if MSG:
#                        self.TBAppend(self.NexGenTB,
#                                      "RECV: {0}\n".format(repr(MSG)),
#                                      self.nexgenlogfile)
#                        if MSG.startswith('\x00\x10SSC20 ') or MSG.startswith('\x00XDPT20 '):
#                            reply = MSG[:7] + 'A' + MSG[8:]
#                            if self.NexGenEventsCheckbox.GetValue():
#                                if MSG.endswith('P'):
#                                    self.ProcessOutput("NexGen: Truck Present (P)")
#                                elif MSG.endswith('N'):
#                                    self.ProcessOutput("NexGen: Truck Not Present (N)")
#                            clientConn.send(reply)
#                            self.TBAppend(self.NexGenTB,
#                                          "SEND: {0}\n\n".format(repr(reply)),
#                                          self.nexgenlogfile)
#                            if MSG.startswith('\x00\x10SSC20 B'):
#                                self.TBAppend(self.NexGenTB,
#                                              "Closing NexGen connection...\n\n",
#                                              self.nexgenlogfile)
#                                clientConn.close()
#                                clientConn = None
#                    else:
#                        time.sleep(0.5)
#        try:
#            clientConn.close()
#        except Exception:
#            pass
#        self.NexGenTB.AppendText("[{0}] Not listening to NexGen messages anymore...\n".format(self.ftime()))
#        self.NexGenThreadRunning = False
#    
#    def socketBind(self, port, timeout=None):
#        try:
#            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#            if timeout:
#                s.settimeout(timeout)
#            s.bind(('', port)) #bound to localhost
#            return s
#        except Exception, e:
#            print e
#            return None
#    
#    def DatalogListen(self):
#        self.DatalogThreadRunning = True
#        port = int(self.NetworkTBList[2].GetValue())
#        s = None
#        while not s:
#            if not self.RunTestThreads:
#                self.DatalogThreadRunning = False
#                return
#            s = self.socketBind(port=port)
#        self.TBAppend(self.DatalogTB,
#                      "Listening to Datalog messages on port {0}...\n".format(port),
#                      self.dataloglogfile)
#        clientConn = None
#        while self.RunTestThreads:
#            MSG = ""
#            if not (self.PingBoard(self.NetworkTBList[0].GetValue())):
#                if clientConn:
#                    self.TBAppend(self.DatalogTB,
#                                  "Lost connection to board.\n",
#                                  self.dataloglogfile)
#                    clientConn.close()
#                clientConn = None
#            if not clientConn:
#                self.TBAppend(self.DatalogTB,
#                              "Attempting connection... ",
#                              self.dataloglogfile)
#                s.listen(1) #Listen for 1 connection
#                try:
#                    clientConn, a = s.accept()
#                    self.TBAppend(self.DatalogTB,
#                                  "Connection made!\n",
#                                  self.dataloglogfile)
#                except Exception, e:
#                    self.TBAppend(self.DatalogTB,
#                                  "{0!r}\n".format(e),
#                                  self.dataloglogfile)
#                    self.DatalogTB.AppendText()
#            if clientConn:
#                try:
#                    ready = select.select([clientConn], [], [], 0)
#                    if ready[0]:
#                        MSG = clientConn.recv(1024)
#                except Exception, e:
#                    self.TBAppend(self.DatalogTB,
#                                  "{0!r}\n".format(e),
#                                  self.dataloglogfile)
#                    self.TBAppend(self.DatalogTB,
#                                  "Closing Datalog connection...\n\n",
#                                  self.dataloglogfile)
#                    if clientConn: clientConn.close()
#                    clientConn = None
#                else:
#                    if MSG:
#                        if self.ascii2int(MSG[0:1])+2 == len(MSG):
#                            if DEBUG: print repr(MSG)
#                            log = self.DatalogParse(MSG)
#                            if self.DatalogMessagesCheckbox.GetValue():
#                                self.ProcessOutput(str(log))
#                            elif self.DatalogEventsCheckbox.GetValue():
#                                self.ProcessOutput("Datalog Event: "+self.DatalogEventPrint(log[0]))
#                            self.DatalogPrint(self.DatalogTB,log)
#                    else:
#                        time.sleep(0.5)
#        try:
#            clientConn.close()
#            s.close()
#        except Exception:
#            pass
#        self.TBAppend(self.DatalogTB,
#                      "Not listening to Datalog messages anymore...\n",
#                      self.dataloglogfile)
#        self.DatalogThreadRunning = False
#
##    def DatalogListen(self):
##        s = None
##        self.DatalogTB.AppendText("[{0}] Listening to Datalog messages on port 9829...\n".format(self.ftime()))
##        clientConn = None
##        MSG = ""
##        while self.RunTestThreads:
##            if not s:
##                s = self.socketBind(port=9829, timeout=0) # Open blocking socket
##            if s:
##                if not MSG:
##                    self.DatalogTB.AppendText("[{0}] Attempting connection... ".format(self.ftime()))
##                    s.listen(1) #Listen for 1 connection
##                    try:
##                        clientConn, a = s.accept()
##                    except Exception, e:
##                        self.DatalogTB.AppendText(repr(e)+"\n")
##                        clienConn = None
##                    if clientConn:
##                        self.DatalogTB.AppendText("Connection made!\n")
##                if clientConn:
##                    try:
##                        MSG = clientConn.recv(1024)
##                        self.DatalogTB.AppendText(repr(MSG)+"\n")
##                    except Exception, e:
##                        self.DatalogTB.AppendText(repr(e)+"\n")
##                        self.NexGenTB.AppendText("[{0}] Closing connection...\n".format(self.ftime()))
##                        if clientConn: clientConn.close()
##                        clientConn = None
##                        MSG = ""
##                    else:
##                        if MSG:
##                            if self.ascii2int(MSG[0:1],True)+2 == len(MSG):
##                                log = self.DatalogParse(MSG)
##                                self.HistoryTB.AppendText(str(log))
##                                self.DatalogPrint(self.DatalogTB,log)
##                        else:
##                            time.sleep(0.5)
##            else:
##                time.sleep(5) # If failed to open a socket, wait 5 seconds
##        try:
##            clientConn.close()
##            s.close()
##        except Exception:
##            pass
##        self.DatalogTB.AppendText("[{0}] Not listening to Datalog messages anymore...\n".format(self.ftime()))
#        
#    def DatalogParse(self, log):
#        L = [ord(log[2]),                                   # event
#        self.myunpack(log[4:8]),                            # Pump ID
#        self.IPParse(log[9:13]),                            # Pump IP
#        self.IPParse(log[14:18]),                           # Datalog IP
#        self.IPParse(log[19:23]),                           # NexGen IP
#        self.IPParse(log[24:28]),                           # TFTP IP
#        self.IPParse(log[29:33]),                           # Network Mask
#        self.IPParse(log[34:38]),                           # Default Gateway
#        self.myunpack(log[39:41]),                          # Datalog Port
#        self.myunpack(log[42:44]),                          # NexGen Port
#        self.myunpack(log[45:47]),                          # TFTP Port
#        "{0:02X}:{1:02X}:{2:02X}:{3:02X}:{4:02X}:{5:02X}".format(*[ord(c) for c in log[48:54]]), # MAC address
#        self.myunpack(log[55:59]),                          # Datalog Interval
#        self.myunpack(log[60:64]),                          # Transducer Read Interval
#        self.myunpack(log[65:69]),                          # Vehicle Poll Interval
#        self.myunpack(log[70:71]),                          # Configuration Mode Active
#        repr(log[72:89]).strip("'"),                        # Current ZID
#        repr(log[90:107]).strip("'"),                       # Current VIN
#        self.myunpack(log[108:112],signed=True),            # Transducer Value
#        self.myunpack(log[113:114],signed=True),            # Vehicle Present
#        self.myunpack(log[115:116],signed=True),            # Vehicle Verified
#        self.myunpack(log[117:118]),                        # Vehicle Departed Cause
#        self.myunpack(log[119:123],signed=True),            # Distance To Ground
#        self.myunpack(log[124:128],signed=True),            # Transducer Trigger Height
#        self.myunpack(log[129:133],signed=True),            # Vehicle Present Timeout
#        self.myunpack(log[134:138],signed=True),            # Vehicle Present Timer
#        self.myunpack(log[139:141],signed=True),            # RSSI Bel
#        self.myunpack(log[142:146]),                        # Reset Cause
#        ".".join([str(self.myunpack(log[i:i+2])) for i in xrange(147,155,2)]), # System Revision
#        self.myunpack(log[156:157]),                        # NexGen Status
#        self.myunpack(log[158:159])]                        # Power Status
#        if len(log) > 159:
#            L += [".".join([str(self.myunpack(log[i])) for i in xrange(160,163)]),  # Radio FW version
#                  self.myunpack(log[164:166]),                                      # Radio Bootloader version
#                  self.myunpack(log[167:171]),                                      # Radio App Size
#                  self.myunpack(log[172:176]),                                      # Radio App XOR Checksum
#                  self.myunpack(log[177:181])]                                      # Radio App ADD Checksum
#        if len(log) > 181:
#            L += [self.myunpack(log[182:186]),                                      # Odometer
#                  self.myunpack(log[187:191]),                                      # Engine Hours
#                  self.myunpack(log[192:196]),                                      # Total Fuel Used
#                  self.myunpack(log[197:199]),                                      # Fuel Needed
#                  self.myunpack(log[200:202]),                                      # DEF Needed
#                  self.myunpack(log[203:204])]                                      # Active Fault Count
#        return L
#    
#    # Takes in ASCII values for IP
#    def IPParse(self, ip):
#        return ".".join([str(ord(c)) for c in ip])
#
#    def ascii2int(self, data, signed=False, LSB=True):
#        if LSB: data = data[::-1]
#        b = 0
#        for c in data:
#            b = (b<<8) + ord(c)
#        if signed and (b & (1<<(8*len(data)-1))): # If MSB is a 1
#            b -= (1<<(8*len(data)))
##        print b, self.myunpack(data, LSB, signed)
#        return b
#    
#    def myunpack(self, data, signed=False, LSB=True, fmt=""):
#        if not fmt:
#            # Get the required format of the data, based on the data length
#            d = {1:'B', 2:'H', 4:'I', 8:'Q'}
#            fmt = d.get(len(data),'B')
#            # If signed, convert fmt string to lowercase
#            if signed: fmt = fmt.lower()
#            # Determine endianness. If the LSB comes first, it's big-endian
#            if LSB: fmt="<"+fmt
#            else: fmt=">"+fmt
#        return struct.unpack(fmt, data)[0]
#    
#    # If len(a) < length, will pad with leading nulls
#    def int2ascii(self, data, length, LSB=True):
#        if data < 0:
#            data += (1<<(8*length))
#        a = ""
#        while not data<=0:
#            a = chr(data & 0xFF) + a
#            data = data >> 8
#        while len(a)<length: a = "\x00"+a
#        if LSB: a = a[::-1]
#        return a
#    
#    def DatalogPrint(self, tb, log):
#        s = ("Datalog server message received\n"+
#             "Event: {0}\n".format(self.DatalogEventPrint(log[0]))+
#             "Pump ID: {0}\n".format(log[1])+
#             "Pump IP: {0}\n".format(log[2])+
#             "Datalog IP: {0}\n".format(log[3])+
#             "NexGen IP: {0}\n".format(log[4])+
#             "TFTP IP: {0}\n".format(log[5])+
#             "Network Mask: {0}\n".format(log[6])+
#             "Default Gateway: {0}\n".format(log[7])+
#             "Datalog Port: {0}\n".format(log[8])+
#             "NexGen Port: {0}\n".format(log[9])+
#             "TFTP Port: {0}\n".format(log[10])+
#             "MAC address: {0}\n".format(log[11])+
#             "Datalog Interval: {0} ms\n".format(log[12])+
#             "Transducer Read Interval: {0} ms\n".format(log[13])+
#             "Vehicle Poll Interval: {0} ms\n".format(log[14]))
#        if log[15]:
#            configuration_mode = "Y ({0})".format(log[15])
#        else:
#            configuration_mode = "N ({0})".format(log[15])
#        s += "Configuration Mode Active: {0}\n".format(configuration_mode)
#        if log[16] == "A"*17:  
#            ZID_state = " (IR sync byte received)"
#        elif log[16] == "Z"*17:
#            ZID_state = " (System initialized, and no ZID operations have yet been performed)"
#        else:
#            ZID_state = ""
#        s += "Current ZID: {0}{1}\n".format(log[16], ZID_state)
#        if 'Q' in log[17]:
#            error = " (Nonalphanumeric characters received for VIN and replaced with Q)"
#        else:
#            error = ""
#        s += "Current VIN: {0}{1}\n".format(log[17], error)
#        s += "Transducer Value: {0} cm\n".format(log[18])
#        if log[19]:
#            present = "Y ({0})".format(log[19])
#        else:
#            present = "N ({0})".format(log[19])
#        s += "Vehicle Present: {0}\n".format(present)
#        if log[20]:
#            verified = "Y ({0})".format(log[20])
#        else:
#            verified = "N ({0})".format(log[20])
#        s += "Vehicle Verified: {0}\n".format(verified)
#        if log[21] == 0:
#            depart = "No departed (0)"
#        elif log[21] == 1:
#            depart = "Transducer (1)"
#        elif log[21] == 2:
#            depart = "Radio disconnect (2)"
#        else:
#            depart = log[21]
#        s += ("Vehicle Departed Cause: {0}\n".format(depart)+
#              "Distance To Ground: {0} cm\n".format(log[22])+
#              "Transducer Trigger Height: {0} cm\n".format(log[23])+
#              "Vehicle Present Timeout: {0} ms\n".format(log[24])+
#              "Vehicle Present Timer: {0} ms\n".format(log[25])+
#              "RSSI Bel: {0} dBm\n".format(log[26])+
#              "Reset Cause: {0}\n".format(log[27])+
#              "System Revision: {0}\n".format(log[28]))
#        nexgen = {0:"No operation has been attempted since system initialization (0)",
#                  1:"A TCP connection to the NexGen is being attempted (1)",
#                  2:"The NexGen connection was successful, and a sign on attempt is being made (2)",
#                  3:"The NexGen sign on was successful, and a vehicle departed or vehicle arrived command is being sent to the NexGen (3)",
#                  4:"The message was received by the NexGen, and a sign off attempt is being made (4)",
#                  0xAA:"The vehicle arrived or vehicle departed command was cleared prematurely. The NexGen connection will be closed. (0xAA)",
#                  0xBB:"Three attempts to send any message to the NexGen were attempted and all of them failed. (0xBB)",
#                  0xCC:"The NexGen is connected, but the pump board was unable to determine the current status of the message cycle. The NexGen connection will be closed. (0xCC)",
#                  0xDD:"A response was received from the NexGen, but three attempts to send a message have already failed, so the response is being ignored. (0xDD)"
#                  }.get(log[29],log[29])
##        if log[29] == 0:
##            nexgen = "No operation has been attempted since system initialization (0)"
##        elif log[29] == 1:
##            nexgen = "A TCP connection to the NexGen is being attempted (1)"
##        elif log[29] == 2:
##            nexgen = "The NexGen connection was successful, and a sign on attempt is being made (2)"
##        elif log[29] == 3:
##            nexgen = "The NexGen sign on was successful, and a vehicle departed or vehicle arrived command is being sent to the NexGen (3)"
##        elif log[29] == 4:
##            nexgen = "The message was received by the NexGen, and a sign off attempt is being made (4)"
##        elif log[29] == 0xAA:
##            nexgen = "The vehicle arrived or vehicle departed command was cleared prematurely. The NexGen connection will be closed. (0xAA)"
##        elif log[29] == 0xBB:
##            nexgen = "Three attempts to send any message to the NexGen were attempted and all of them failed. (0xBB)"
##        elif log[29] == 0xCC:
##            nexgen = "The NexGen is connected, but the pump board was unable to determine the current status of the message cycle. The NexGen connection will be closed. (0xCC)"
##        elif log[29] == 0xDD:
##            nexgen = "A response was received from the NexGen, but three attempts to send a message have already failed, so the response is being ignored. (0xDD)"
##        else:
##            nexgen = log[29]
#        s += "NexGen Status: {0}\n".format(nexgen)
#        power = {0:"No faults (0)",
#                 1:"Transducer power fault (1)",
#                 2:"IR power fault (2)"
#                 }.get(log[30],log[30])
#        s += "Power Status: {0}\n".format(power)
##        if log[30] == 0:
##            power = "No faults (0)"
##        elif log[30] == 1:
##            power = "Transducer power fault (1)"
##        elif log[30] == 2:
##            power = "IR power fault (2)"
##        else:
##            power = log[30]
#        if len(log) > 31:
#            s += ("Radio FW version: {0}\n".format(log[31])+
#                  "Radio bootloader version: {0}\n".format(log[32])+
#                  "Radio app size: {0}\n".format(log[33])+
#                  "Radio app XOR checksum: {0}\n".format(log[34])+
#                  "Radio app ADD checksum: {0}\n".format(log[35]))
#        if len(log) > 36:
#            s += ("Odometer: {0}\n".format(log[36])+
#                  "Engine Hours: {0}\n".format(log[37])+
#                  "Total Fuel Used: {0}\n".format(log[38])+
#                  "Fuel Needed: {0}\n".format(log[39])+
#                  "DEF Needed: {0}\n".format(log[40])+
#                  "Active Faults: {0}\n".format(log[41]))
#        s += "\n"
#        self.TBAppend(tb, s, self.dataloglogfile)
#    
#    def DatalogEventPrint(self, event):
#        return {1:"Datalog Timeout (1)",
#                2:"ZCon Online (2)",
#                3:"Vehicle Arrive (3)",
#                4:"ZID Received (4)",
#                5:"Vehicle Verified (5)",
#                6:"Vehicle Departed (6)",
#                7:"System Reset (7)",
#                8:"NexGen Event (8)",
#                9:"Transducer Error (9)",
#                10:"Radio Error (10)",
#                11:"Power Error (11)"
#                }.get(event, str(event))
#    
#    def OpenLogConnection(self):
#        try:
#            if self.LogHistoryCheckbox.GetValue():
#                self.logfile = open(LOGFILENAME.format(self.ZIDTB.GetValue()), 'a')
#        except IOError as e:
#            self.logfile = None
#            self.ProcessOutput('IOError encountered when trying to write to ' + LOGFILENAME + 
#                               '\n' + str(e), "Can't write to log file", ERROR, sound="error sound")
#            return False
#        try:
#            if self.NexGenLogHistoryCheckbox.GetValue():
#                self.nexgenlogfile = open(NEXGENLOGFILENAME.format(self.ZIDTB.GetValue()), 'a')
#        except IOError as e:
#            self.logfile = None
#            self.ProcessOutput('IOError encountered when trying to write to ' + NEXGENLOGFILENAME + 
#                               '\n' + str(e), "Can't write to log file", ERROR, sound="error sound")
#            return False
#        try:
#            if self.DatalogLogHistoryCheckbox.GetValue():
#                self.dataloglogfile = open(DATALOGLOGFILENAME.format(self.ZIDTB.GetValue()), 'a')
#        except IOError as e:
#            self.logfile = None
#            self.ProcessOutput('IOError encountered when trying to write to ' + DATALOGLOGFILENAME + 
#                               '\n' + str(e), "Can't write to log file", ERROR, sound="error sound")
#            return False
#        return True
#    
#    def CloseLogConnection(self):
#        if self.logfile:
#            self.logfile.flush()
#            os.fsync(self.logfile)
#            self.logfile.close()
#            self.logfile = None
#        
#        if self.nexgenlogfile:
#            self.nexgenlogfile.flush()
#            os.fsync(self.nexgenlogfile)
#            self.nexgenlogfile.close()
#            self.nexgenlogfile = None
#            
#        if self.dataloglogfile:
#            self.dataloglogfile.flush()
#            os.fsync(self.dataloglogfile)
#            self.dataloglogfile.close()
#            self.dataloglogfile = None
#    
#    def SetGbat(self, set="IDLE"):
#        if set == "IDLE":
#            g = self.GbatIdleSpin.GetValue()
#        elif set == "RUN":
#            g = self.GbatRunSpin.GetValue()
#        else:
#            g = set
#        try:
#            g = int(g)
#        except ValueError:
#            self.ProcessOutput("Gbat distance setting not a number. Please check the config file.",
#                               "Bad Gbat Config Value", ERROR, sound="error sound")
#        else:
#            self.GbatReading = "{0:03}".format(g)
#        if self.UltraPort and self.UltraPort.isOpen():
#            self.UltraPort.flushOutput()
#    
#    def RunGbat(self):
#        while(self.RunTestThreads):
#            if self.UltraPort:
#                g = self.GbatReading
##                print repr(g)
#                for i in xrange(10):
#                    if self.UltraPort and not (g == '000'): # If g is not 0
#                        self.UltraPort.write("R{0}\r".format(g))
#                    time.sleep(0.1) # 10 readings/sec
#            else:
#                time.sleep(0.5) # Anti-CPU waster
#        self.CloseCOMPort(self.UltraPort)
#        
#    def CheckZID(self, zid):
#        return zid.isalnum() and len(zid) == 17   
#    
#    # Reads the next message from the radio
#    # defined as starting with a sync byte, and length+2 of the byte after the sync byte
#    # Returns: '' or '\xAA\x<length of payload><payload>'
#    def ReadRadio(self, radio, length=8):
#        msg = radio.read(length)
##        self.ProcessOutput(repr(msg))
#        sync = msg.rfind('\xAA')
#        if sync < 0:
#            return ''
#        msg = msg[sync:]
#        if len(msg) == 1:
#            msg += radio.read(1)
##            print repr(msg)
#        more = (ord(msg[1]) + 2) - len(msg) 
#        if more == 0:
##            print repr(msg), "[1]"
#            return msg
#        if more > 0:
#            m = msg + radio.read(more)
##            print repr(m), "[2]"
#            return m
#        else:
##            print repr(msg[:more]), "[3]"
#            return msg[:more]
#    
#    def ProcessOutput(self, history=None, status=None, messagetype=NORMAL, sound=None):
#        if history:
#            self.HistoryAppend(history)
#        if status:
#            if messagetype == ERROR:
#                self.StatusLabel.SetForegroundColour("White")
#                self.StatusLabel.SetBackgroundColour(self.ERROR_BG_COLOR)
#            elif messagetype == SUCCESS:
#                self.StatusLabel.SetForegroundColour("White")
#                self.StatusLabel.SetBackgroundColour(self.SUCCESS_BG_COLOR)
#            else:
#                self.StatusLabel.SetForegroundColour(self.NORMAL_TEXT_COLOR)
#                self.StatusLabel.SetBackgroundColour(self.NORMAL_BG_COLOR)
#            self.StatusLabel.SetLabel(status)
#        if sound and self.PlaySoundsCheckbox.GetValue():
#            ws.PlaySound(SOUNDS[sound], ws.SND_FILENAME)
#    
#    def HistoryAppend(self, i):
#        temp = "[{0}] {1}\n".format(self.ftime(), str(i))
#        self.HistoryTB.AppendText(temp)
#        if self.logfile and self.LogHistoryCheckbox.GetValue():
#            self.WriteToFile(self.logfile, temp)
#    
#    def TBAppend(self, tb, i, log=None):
#        temp = "[{0}] {1}".format(self.ftime(), str(i))
#        tb.AppendText(temp)
#        if log:
#            self.WriteToFile(log, temp)
#    
#    def ftime(self):
#        # Truncate to third decimal place, and remove leading zero
#        s = "{0:.03}".format(time.time() % 1)[1:]
#        # Add trailing zeroes to fractional seconds
#        return time.strftime("%m-%d-%y %H:%M:%S")+"{0:0<4}".format(s)
    
    def WriteToFile(self, file, output):
        file.write(output)
        # Force write done on file close
#        file.flush()
#        os.fsync(file)
    
    def ClearStoppedThreads(self, L):
        for t in L[:]:
            if not t.isAlive(): L.remove(t)
    
    def OnClose(self, event):
        t = threading.Thread(name="Close", target=self.CloseThreads)
        t.start()
        
    def CloseThreads(self):
        self.RunThreads = False
        self.ResetPressed = True
#        print self.ThreadList
        t = time.clock()
        while ((True in [th.isAlive() for th in self.ThreadList]) and time.clock() < t + 5):
            pass
#        print self.ThreadList
#        self.CloseLogConnection()
        self.Destroy()

# Taken wholesale from http://wiki.wxpython.org/ProportionalSplitterWindow
#class ProportionalSplitter(wx.SplitterWindow):
#    def __init__(self, parent, id= -1, proportion=0.66, size=wx.DefaultSize, **kwargs):
#        wx.SplitterWindow.__init__(self, parent, id, wx.Point(0, 0), size, **kwargs)
#        self.SetMinimumPaneSize(50) #the minimum size of a pane.
#        self.proportion = proportion
#        if not 0 < self.proportion < 1:
#            raise ValueError, "proportion value for ProportionalSplitter must be between 0 and 1."
#        self.ResetSash()
#        self.Bind(wx.EVT_SIZE, self.OnReSize)
#        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSashChanged, id=id)
#        ##hack to set sizes on first paint event
#        self.Bind(wx.EVT_PAINT, self.OnPaint)
#        self.firstpaint = True
#
#    def SplitHorizontally(self, win1, win2):
#        if self.GetParent() is None: return False
#        return wx.SplitterWindow.SplitHorizontally(self, win1, win2,
#                int(round(self.GetParent().GetSize().GetHeight() * self.proportion)))
#
#    def SplitVertically(self, win1, win2):
#        if self.GetParent() is None: return False
#        return wx.SplitterWindow.SplitVertically(self, win1, win2,
#                int(round(self.GetParent().GetSize().GetWidth() * self.proportion)))
#
#    def GetExpectedSashPosition(self):
#        if self.GetSplitMode() == wx.SPLIT_HORIZONTAL:
#            tot = max(self.GetMinimumPaneSize(), self.GetParent().GetClientSize().height)
#        else:
#            tot = max(self.GetMinimumPaneSize(), self.GetParent().GetClientSize().width)
#        return int(round(tot * self.proportion))
#
#    def ResetSash(self):
#        self.SetSashPosition(self.GetExpectedSashPosition())
#
#    def OnReSize(self, event):
#        "Window has been resized, so we need to adjust the sash based on self.proportion."
#        self.ResetSash()
#        event.Skip()
#
#    def OnSashChanged(self, event):
#        "We'll change self.proportion now based on where user dragged the sash."
#        pos = float(self.GetSashPosition())
#        if self.GetSplitMode() == wx.SPLIT_HORIZONTAL:
#            tot = max(self.GetMinimumPaneSize(), self.GetParent().GetClientSize().height)
#        else:
#            tot = max(self.GetMinimumPaneSize(), self.GetParent().GetClientSize().width)
#        self.proportion = pos / tot
#        event.Skip()
#
#    def OnPaint(self, event):
#        if self.firstpaint:
#            if self.GetSashPosition() != self.GetExpectedSashPosition():
#                self.ResetSash()
#            self.firstpaint = False
#        event.Skip()


if __name__ == "__main__":
    app = wx.App(redirect=False)
    FunctionTestFrame().Show()
    app.MainLoop()
