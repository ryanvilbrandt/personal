#!/usr/bin/python
# -*- coding: UTF-8 -*-
import wx, re, time, os, sys, threading, datetime, random
from wx.lib.floatcanvas import FloatCanvas 
import wx.lib.sheet as sheet
from math import pi, cos, sin
# Third party libs
from dateutil import parser # http://labix.org/python-dateutil

# To do list
# Add recent files listing
# Check to save file on close
# Add button to view bonds/boons in Character Edit
# Build bond/boon viewer
# Build bond/boon canvas

# Process command line arguments
DEBUG = False
#print sys.argv
if "-debug" in sys.argv:
    DEBUG = True
    sys.argv.remove("-debug")

VERSION = "0.9.2" 
TITLE = "VampHelper v"+VERSION
DEFAULT_SEASON_TITLE = "SEASON TITLE HERE"
DEFAULT_EVENT_TITLE = "EVENT TITLE HERE"

class MainFrame(wx.Frame):
    """
    This is the root class for VampHelper, an application designed to handle social events,
    as well as display an easy-to-understand graph of blood bonds and boons.
    It can be run as a wx.App()
    
    if __name__ == "__main__":
        app = wx.App(redirect=False)
        MainFrame().Show()
        app.MainLoop()
    """
#    toolTipDict = {
#        'CheckAllBox': 'Enables or disables all checkboxes below.',
#        }
    filename = ''
    dirname = '.'
    suspendUpdates = False
    boonsDict = {}
#    boonsDict = {"Alex":{"Betty":[3,"Sexual favors"], 
#                         "!color":None, "!pos":None},
#                 "Betty":{"Alex":[4,"Use of his sister"],
#                          "Charles":[2,"BJ behind the 7-11"], 
#                          "!color":None, "!pos":None},
#                 "Charles":{"Alex":[5,"1 kilo of Heroin"], 
#                            "!color":None, "!pos":None}}
    
    def __init__(self):
        wx.Frame.__init__(self, None, title=TITLE, style=wx.MINIMIZE_BOX | #wx.RESIZE_BORDER | 
                          wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        
        self.InitGUI()
        
        self.DataPath = os.path.join(self.GetAppDataPath(),"VampHelper")
        self.InitPaths()
        
        self.InitLastOpened()
        
        self.AutoCheckForUpdates()
    
#    def GetAppDataPath(self):
#        """
#        Retrieves the path where it's safe to save the app's data.
#        On Windows 7/Vista, this is C:\User\Public\AppData (?) 
#        On Windows 2000/XP, this is C:\Documents and Settings\All Users\Application Data\ 
#        Currently, this app doesn't support Linux or Mac.
#        """
#        return os.environ['COMMONAPPDATA']
    
    def GetAppDataPath(self):
        """
        Retrieves the path where it's safe to save the app's data.
        On Windows 7/Vista, this is C:\ProgramData\ 
        On Windows 2000/XP, this is C:\Documents and Settings\All Users\Application Data\ 
        Currently, this app doesn't support Linux or Mac.
        """
        import ctypes
        from ctypes import wintypes, windll
        
        CSIDL_COMMON_APPDATA = 35
        
        _SHGetFolderPath = windll.shell32.SHGetFolderPathW
        _SHGetFolderPath.argtypes = [wintypes.HWND,
                                    ctypes.c_int,
                                    wintypes.HANDLE,
                                    wintypes.DWORD, wintypes.LPCWSTR]
        
        
        path_buf = wintypes.create_unicode_buffer(wintypes.MAX_PATH)
        result = _SHGetFolderPath(0, CSIDL_COMMON_APPDATA, 0, 0, path_buf)
        return path_buf.value

    def ErrorDialog(self, e):
        """
        Convenience method that creates an error dialog with the title "Error".
        Handles showing, and destroying after it's finished.
        """
        dial = wx.MessageDialog(None, e, 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
        dial.Destroy()
    
    def InitGUI(self):
        """
        Builds and organizes all visual elements in the GUI for this Frame
        """
#        self.SetMinSize(wx.Size(600, 492))
#        self.SetSize(wx.Size(600, 625))

        # ID namespace
        # 100 = Menu items
        
        self.CreateStatusBar()

        fileMenu = wx.Menu()
        fileMenu.Append(100, "&New season",
                        "Clear all controls and start a new season")
        fileMenu.Append(101, "&Load...",
                        "Load season")
        fileMenu.Append(102, "&Save...",
                        "Save season")
        fileMenu.AppendSeparator()
        fileMenu.Append(103, "&Show logs",
                        "Opens the logs folder in an explorer window")
        widgetMenu = wx.Menu()
        widgetMenu.Append(110, "&Master List",
                         "Shows a widget of a modifiable list of PCs and NPCs")
        widgetMenu.AppendSeparator()
        widgetMenu.Append(111, "B&lood Bonds",
                         "Shows a graph of blood bonds")
        widgetMenu.Append(112, "B&oons",
                        "Shows a graph of boons")
        updateMenu = wx.Menu()
        updateMenu.Append(120, "Check for &updates",
                        "Checks the web server for an update to the application")
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(widgetMenu, "&Widgets")
        menuBar.Append(updateMenu, "&Update")
        self.SetMenuBar(menuBar)
        wx.EVT_MENU(self, 100, self.OnNewMenu)
        wx.EVT_MENU(self, 101, self.OnLoadMenu)
        wx.EVT_MENU(self, 102, self.OnSaveMenu)
        wx.EVT_MENU(self, 103, self.OnShowLogsMenu)
        wx.EVT_MENU(self, 112, self.OnBoons)
        wx.EVT_MENU(self, 120, self.OnCheckForUpdates)
        
        self.p = wx.Panel(self)
        
        boldFont = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        
        self.SeasonTitleTB = wx.TextCtrl(self.p, size=(200,-1))
        self.SeasonTitleTB.SetValue(DEFAULT_SEASON_TITLE)
        self.SeasonTitleTB.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.EventTitleTB = wx.TextCtrl(self.p, size=(200,-1), style=wx.TB_RIGHT)
        self.EventTitleTB.SetValue(DEFAULT_EVENT_TITLE)
        self.EventTitleTB.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.EventDateCtrl = wx.TextCtrl(self.p, size=(100,-1))
        self.EventDateCtrl.SetValue(str(datetime.date.today()))
        self.EventDateCtrl.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocusDateCtrl)
        newSeasonButton = wx.Button(self.p, label="End Season")
        newSeasonButton.Bind(wx.EVT_BUTTON, self.OnNewMenu)
        
#        self.MasterListNames = ["Alex (20/20)", "Betty (10/10)", "Charles (30/30)"]
        self.MasterListNames = []
        self.MasterListFull = []
#        self.MasterListFull.append(self.BuildCharDict("Alex", 8, "Malkavian", 20, 20))
#        self.MasterListFull.append(self.BuildCharDict("Betty", 7, "Nosferatu", 10, 10))
#        self.MasterListFull.append(self.BuildCharDict("Charles", 6, "Ventrue", 30, 30))
        self.MasterListBox = wx.ListBox(self.p, size=(150,300), choices=self.MasterListNames, style=wx.LB_RIGHT)
        self.MasterListBox.Bind(wx.EVT_LISTBOX_DCLICK, self.EditCharInMasterList)
        addMLButton = wx.Button(self.p, label="+", size=(30,-1))
        addMLButton.Bind(wx.EVT_BUTTON, self.AddToMasterList)
        remMLButton = wx.Button(self.p, label="-", size=(30,-1))
        remMLButton.Bind(wx.EVT_BUTTON, self.RemoveFromMasterList)
        editMLButton = wx.Button(self.p, label="Edit", size=(40,-1))
        editMLButton.Bind(wx.EVT_BUTTON, self.EditCharInMasterList)
        addToAttackersButton = wx.Button(self.p, label="Attackers", size=(60,-1))
        addToAttackersButton.Bind(wx.EVT_BUTTON, self.AddToAttackers)
        addToDefendersButton = wx.Button(self.p, label="Defenders", size=(60,-1))
        addToDefendersButton.Bind(wx.EVT_BUTTON, self.AddToDefenders)
        
        self.AttackersTBList = []
#        for each in xrange(6):
#            self.AttackersTBList.append([wx.TextCtrl(self.p, size=(100,-1), style=wx.TE_READONLY),
#                                         wx.TextCtrl(self.p, size=(40,-1), style=wx.TE_READONLY),
#                                         wx.SpinCtrl(self.p, size=(40,-1)),
#                                         wx.SpinCtrl(self.p, size=(40,-1)),
#                                         wx.TextCtrl(self.p, size=(200,-1))])
#        for row in self.AttackersTBList:
#            row[4].Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.DefendersTBList = []
        
        self.AttackerTotalTB = wx.TextCtrl(self.p, size=(40,-1), style=wx.TE_READONLY)
        self.AttackerTotalTB.SetFont(boldFont)
        self.AttackerTotalTB.SetValue('0')
        self.DefenderTotalTB = wx.TextCtrl(self.p, size=(40,-1), style=wx.TE_READONLY)
        self.DefenderTotalTB.SetFont(boldFont)
        self.DefenderTotalTB.SetValue('0')
        self.AttackerMainPenaltyTB = wx.TextCtrl(self.p, size=(40,-1), style=wx.TE_READONLY)
        self.DefenderMainPenaltyTB = wx.TextCtrl(self.p, size=(40,-1), style=wx.TE_READONLY)
        self.AttackerHelpPenaltyTB = wx.TextCtrl(self.p, size=(40,-1), style=wx.TE_READONLY)
        self.DefenderHelpPenaltyTB = wx.TextCtrl(self.p, size=(40,-1), style=wx.TE_READONLY)
        commitButton = wx.Button(self.p, label="Commit!")
        commitButton.Bind(wx.EVT_BUTTON, self.OnCommit)
        
        headersizer = wx.BoxSizer(wx.HORIZONTAL)
        headersizer.Add(self.SeasonTitleTB, 0, wx.ALIGN_CENTER)
        headersizer.Add(wx.StaticText(self.p, label="  --  "), 0, wx.ALIGN_CENTER)
        headersizer.Add(self.EventTitleTB, 0, wx.ALIGN_CENTER)
        headersizer.Add(wx.StaticText(self.p, label="  --  "), 0, wx.ALIGN_CENTER)
        headersizer.Add(self.EventDateCtrl, 0, wx.ALIGN_CENTER)
        headersizer.Add(newSeasonButton, 0, wx.ALIGN_CENTER | wx.LEFT, 10)
        
        masterListBox = wx.StaticBox(self.p, label='Master List')
        masterListSizer = wx.StaticBoxSizer(masterListBox, wx.VERTICAL)
        masterListSizer.Add(self.MasterListBox, 1, wx.EXPAND)
        addRemButtons = wx.BoxSizer(wx.HORIZONTAL)
        addRemButtons.Add(addMLButton, 0, wx.ALL, 2)
        addRemButtons.Add(remMLButton, 0, wx.ALL, 2)
        addRemButtons.Add(editMLButton, 0, wx.ALL, 2)
        masterListSizer.Add(addRemButtons, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        attDefButtons = wx.BoxSizer(wx.HORIZONTAL)
        attDefButtons.Add(addToAttackersButton, 0, wx.ALL, 2)
        attDefButtons.Add(addToDefendersButton, 0, wx.ALL, 2)
        masterListSizer.Add(attDefButtons, 0, wx.ALIGN_CENTER | wx.ALL, 2)
        
        attackerSizer = wx.GridBagSizer(2,5)
        attackerSizer.Add(wx.StaticText(self.p, label=" Name:", size=(100,-1)), (0,0), wx.DefaultSpan, wx.ALIGN_CENTER)
        attackerSizer.Add(wx.StaticText(self.p, label=" Perm", size=(30,-1)), (0,1), wx.DefaultSpan, wx.ALIGN_CENTER)
        attackerSizer.Add(wx.StaticText(self.p, label=" temp", size=(30,-1)), (0,2), wx.DefaultSpan, wx.ALIGN_CENTER)
        attackerSizer.Add(wx.StaticText(self.p, label=" spent", size=(42,-1)), (0,3), wx.DefaultSpan, wx.ALIGN_CENTER)
        attackerSizer.Add(wx.StaticText(self.p, label=" misc", size=(50,-1)), (0,4), wx.DefaultSpan, wx.ALIGN_CENTER)
#        for i in xrange(len(self.AttackersTBList)):
#            self.AttackerSizer.Add(self.AttackersTBList[i][0], (i*2+1,0), wx.DefaultSpan, wx.ALIGN_CENTER)
#            self.AttackerSizer.Add(self.AttackersTBList[i][1], (i*2+1,1), wx.DefaultSpan, wx.ALIGN_CENTER)
#            self.AttackerSizer.Add(self.AttackersTBList[i][2], (i*2+1,2), wx.DefaultSpan, wx.ALIGN_CENTER)
#            self.AttackerSizer.Add(self.AttackersTBList[i][3], (i*2+1,3), wx.DefaultSpan, wx.ALIGN_CENTER)
#            self.AttackerSizer.Add(self.AttackersTBList[i][4], (i*2+2,0), (1,4), wx.ALIGN_CENTER | wx.EXPAND | wx.BOTTOM, 5)
        attackerBox = wx.StaticBox(self.p, label='Attackers')
        self.AttackerBoxSizer = wx.StaticBoxSizer(attackerBox, wx.VERTICAL)
        self.AttackerBoxSizer.Add(attackerSizer, 0)
#        self.AddCharacterToSocialEvent(self.AttackersTBList, self.AttackerBoxSizer)
        
        defenderSizer = wx.GridBagSizer(2,5)
        defenderSizer.Add(wx.StaticText(self.p, label=" Name:", size=(100,-1)), (0,0), wx.DefaultSpan, wx.ALIGN_CENTER)
        defenderSizer.Add(wx.StaticText(self.p, label=" Perm", size=(30,-1)), (0,1), wx.DefaultSpan, wx.ALIGN_CENTER)
        defenderSizer.Add(wx.StaticText(self.p, label=" temp", size=(30,-1)), (0,2), wx.DefaultSpan, wx.ALIGN_CENTER)
        defenderSizer.Add(wx.StaticText(self.p, label=" spent", size=(42,-1)), (0,3), wx.DefaultSpan, wx.ALIGN_CENTER)
        defenderSizer.Add(wx.StaticText(self.p, label=" misc", size=(51,-1)), (0,4), wx.DefaultSpan, wx.ALIGN_CENTER)
        defenderBox = wx.StaticBox(self.p, label='Defenders')
        self.DefenderBoxSizer = wx.StaticBoxSizer(defenderBox, wx.VERTICAL)
        self.DefenderBoxSizer.Add(defenderSizer, 0)
#        self.AddCharacterToSocialEvent(self.DefendersTBList, self.DefenderBoxSizer)
        
        outputsizer = wx.FlexGridSizer(3, 5)
        outputsizer.Add(wx.StaticText(self.p, label="Attacking total"),0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL,border=2)
        outputsizer.Add(self.AttackerTotalTB, 0, wx.ALL | wx.ALIGN_CENTER, border=2)
        outputsizer.Add(commitButton, 0, wx.ALL | wx.ALIGN_CENTER, border=2)
        outputsizer.Add(self.DefenderTotalTB, 0, wx.ALL | wx.ALIGN_CENTER, border=2)
        outputsizer.Add(wx.StaticText(self.p, label="Defending total"),0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL,border=2)
        outputsizer.Add(wx.StaticText(self.p, label="Main attacker penalty"),0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL,border=2)
        outputsizer.Add(self.AttackerMainPenaltyTB, 0, wx.ALL | wx.ALIGN_CENTER, border=2)
        outputsizer.Add(wx.StaticText(self.p, label=""),0)
        outputsizer.Add(self.DefenderMainPenaltyTB, 0, wx.ALL | wx.ALIGN_CENTER, border=2)
        outputsizer.Add(wx.StaticText(self.p, label="Main defender penalty"),0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL,border=2)
        outputsizer.Add(wx.StaticText(self.p, label="Assisting attackers penalty"),0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT|wx.ALL,border=2)
        outputsizer.Add(self.AttackerHelpPenaltyTB, 0, wx.ALL | wx.ALIGN_CENTER, border=2)
        outputsizer.Add(wx.StaticText(self.p, label=""),0)
        outputsizer.Add(self.DefenderHelpPenaltyTB, 0, wx.ALL | wx.ALIGN_CENTER, border=2)
        outputsizer.Add(wx.StaticText(self.p, label="Assisting defenders penalty"),0,wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT|wx.ALL,border=2)
        
        gridsizer = wx.GridBagSizer(2,5)
        gridsizer.Add(masterListSizer, (0,0), (2,1), wx.ALIGN_TOP)
        gridsizer.Add(self.AttackerBoxSizer, (0,1), wx.DefaultSpan, wx.ALIGN_TOP)
        gridsizer.Add(self.DefenderBoxSizer, (0,2), wx.DefaultSpan, wx.ALIGN_TOP)
        gridsizer.Add(outputsizer, (1,1), (1,2), wx.ALIGN_TOP | wx.ALIGN_CENTER_HORIZONTAL)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(headersizer, 0, wx.ALIGN_CENTER | wx.TOP, 5)
        sizer.Add(gridsizer, 0, wx.ALL, 5)
        
        self.p.SetSizerAndFit(sizer)
        self.p.SetAutoLayout(1)
        sizer.Fit(self.p)
        self.Fit()
        self.Center()

        # GUI has been loaded. Print instructions and set variables

        wx.ToolTip("").SetDelay(2000)                                       # Sets the delay before the tool tips pop up to 2 seconds
    
    def InitPaths(self):
        """
        Creates the necessary directories in the AppData folder, if they've not already been created.
        Creates the "VampHelper" directory, and the "logs" directory within that.
        """
        if not os.path.isdir(self.DataPath):
            os.mkdir(self.DataPath)
        if not os.path.isdir(os.path.join(self.DataPath,'logs')):
            os.mkdir(os.path.join(self.DataPath,'logs'))
        self.dirname = self.DataPath
    
    def InitLastOpened(self):
        """
        On app start, if last_opened.ini contains the name of a valid file, it will load that file
        """
        if os.path.isfile(os.path.join(self.DataPath,'last_opened.ini')):
            with open(os.path.join(self.DataPath,'last_opened.ini'), 'r') as f:
                path = f.read()
            if path:
                self.OnLoadMenu(None, dir=os.path.dirname(path), file=os.path.basename(path))
    
    def OnNewMenu(self, event):
        """
        Clears all lists and values, preparing the user to start a new season
        Attacker and Defender lists are cleared
        Perm statuses are recalculated based on the current date
        Temp statuses in the Master list are recalculated 
        """
        self.filename = ""
        self.ClearAttDefLists()
        current = DateFromString(self.EventDateCtrl.GetValue())
        # Correct the format for the date box
        self.EventDateCtrl.SetValue(str(current))
        for i,n in enumerate(self.MasterListNames):
            char = self.MasterListFull[i]
            status = self.GetUpdatedPermStatus(char)
            # Reset the Listbox values
            self.MasterListNames[i] = "{0} ({1}/{1})".format(char.get('name',''),int(status))
            # Give everyone their max for their temp status to spend
            char['temp status'] = status
        self.MasterListBox.Set(self.MasterListNames)
        self.boonsDict.clear()
        self.Redraw()
        self.SeasonTitleTB.SetValue(DEFAULT_SEASON_TITLE)
        self.EventTitleTB.SetValue(DEFAULT_EVENT_TITLE)
#        self.EventDateCtrl.SetValue(str(datetime.date.today()))
        self.SetTitle(TITLE)
        self.Redraw()
        
        self.SetLastSeason("", "")
        self.UpdateTotals(None)
    
    def OnLoadMenu(self, event, dir=None, file=None):
        if dir:
            self.dirname = dir
            self.filename = file
        else:
            dirname = self.dirname
            if not self.filename:
                t = self.EventDateCtrl.GetValue()
                savename = self.SeasonTitleTB.GetValue()+" -- "+self.EventTitleTB.GetValue()+" -- "+str(t).split(' ')[0]
                savename = savename.replace('/','-')
            else:
                savename = self.filename
            dlg = wx.FileDialog(self, "Choose a file", dirname, savename,
                                "Saved Seasons (*.ssf)|*.ssf|All files (*.*)|*.*", wx.OPEN)
            if dlg.ShowModal() == wx.ID_OK:
                self.filename=dlg.GetFilename()
                self.dirname=dlg.GetDirectory()
                dlg.Destroy()
            else:
                dlg.Destroy()
                return
            
        # Open the file, read the contents and set them into
        # the text edit window
        path = os.path.join(self.dirname, self.filename)
        if not os.path.isfile(path): return
        with open(path,'r') as f:
            i = f.read()
            
        lines = i.split('\n')
        if DEBUG: print lines
        title = lines[0].split(' -- ')
        self.SeasonTitleTB.SetValue(eval(title[0]))
        self.EventTitleTB.SetValue(eval(title[1]))
        self.EventDateCtrl.SetValue(eval(title[2]))
        self.MasterListFull = eval(lines[1])
        today = DateFromString(eval(title[2]))
        self.MasterListNames = ["{0} ({1}/{2})".format(c.get('name',''),
                                                       int(c.get('temp status',0)),
                                                       int(c.get('perm status',0)) + ((today - c.get('birthday',today)).days // 3650))
                                for c in self.MasterListFull]
        self.MasterListBox.Set(self.MasterListNames)
        
        self.suspendUpdates = True
        self.ClearAttDefLists()
        for c in eval(lines[2]):
            self.AddCharacterToSocialEvent(self.AttackersTBList, self.AttackerBoxSizer, c)
        for c in eval(lines[3]):
            self.AddCharacterToSocialEvent(self.DefendersTBList, self.DefenderBoxSizer, c)
        if len(lines) > 4:
            self.boonsDict = eval(lines[4])
        self.Redraw()
        self.suspendUpdates = False
        self.UpdateTotals(None)
        
        # Later - could be enhanced to include a "changed" flag whenever
        # the text is actually changed, could also be altered on "save" ...
        self.SetTitle("{0} - {1}".format(TITLE,self.filename))
        self.SetLastSeason(self.dirname, self.filename)
    
    def OnSaveMenu(self, event):
        # Save away the edited text
        # Open the file, do an RU sure check for an overwrite!
        if not self.filename:
            savename = self.SeasonTitleTB.GetValue()+" -- "+self.EventTitleTB.GetValue()+" -- "+self.EventDateCtrl.GetValue()
        else:
            savename = self.filename
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, savename, "Saved Seasons (*.ssf)|*.ssf",
                            wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            # Grab content to be saved. Create dicts for all the entries in
            # the AttackersTBList and DefendersTBList first
            att_list = []
            for row in self.AttackersTBList:
                att_list.append({'name':row[0].GetValue(),
                                 'perm status':row[1].GetValue(),
                                 'temp status':row[2].GetValue(),
                                 'spent':row[3].GetValue(),
                                 'misc':row[4].GetValue(),
                                 'blurb':row[5].GetValue()})
            def_list = []
            for row in self.DefendersTBList:
                def_list.append({'name':row[0].GetValue(),
                                 'perm status':row[1].GetValue(),
                                 'temp status':row[2].GetValue(),
                                 'spent':row[3].GetValue(),
                                 'misc':row[4].GetValue(),
                                 'blurb':row[5].GetValue()})
            # Build string to be written to file
            out = (repr(self.SeasonTitleTB.GetValue())+"  --  "+
                   repr(self.EventTitleTB.GetValue())+"  --  "+
                   repr(self.EventDateCtrl.GetValue())+"\n"+
                   repr(self.MasterListFull)+"\n"+
                   repr(att_list)+"\n"+
                   repr(def_list)+"\n"+
                   repr(self.boonsDict))
            
            # Open the file for write, write, close
            self.filename=dlg.GetFilename()
            self.dirname=dlg.GetDirectory()
            with open(os.path.join(self.dirname, self.filename),'w') as f:
                f.write(out)
                f.flush()
                os.fsync(f)
            self.SetTitle("{0} - {1}".format(TITLE,self.filename))
        # Get rid of the dialog to keep things tidy
        dlg.Destroy()
        self.SetLastSeason(self.dirname, self.filename)
        
    def SetLastSeason(self, dir, file):
        """
        Saves current season file to last_opened.ini
        Called on Save, Load, and New
        """
        with open(os.path.join(self.DataPath,'last_opened.ini'), 'w') as f:
            f.write(os.path.join(dir,file))
            f.flush()
            os.fsync(f)
    
    def OnShowLogsMenu(self, event):
        """Opens an explorer window to the logs directory. Currently only supports Windows"""
        import subprocess
        subprocess.Popen('explorer '+os.path.join(self.DataPath,'logs'))
    
    def OnBoons(self, event):
        """Under Construction"""
#        print self.GetSize()
        wx.InitAllImageHandlers()
        frame = DrawFrame(None,
                          -1,
                          "Boons",
                          wx.DefaultPosition,
                          (700,700),
                          )

        frame.Show()
        
        if DEBUG: print self.boonsDict
        frame.Setup(boons=self.boonsDict)
        return True
        
    def AutoCheckForUpdates(self):
        """Called on startup. Quietly checks for updates. See CheckForUpdates."""
        t = threading.Thread(name="UpdateAppThread", target=self.CheckForUpdates, args=[True])
        t.start()
    
    def OnCheckForUpdates(self, event):
        """Manual check for updates. See CheckForUpdates."""
        self.CheckForUpdates(False)
    
    def CheckForUpdates(self, autocheck):
        """
        Checks for updates to the VampHelper application.
        Downloads the VampHelper.update file via HTML. Checks the current version against the version in the first line
        of the .update file. If there's no update available and this function was called via the menu, it notifies the user
        that they are using the most recent version of VampHelper.
        If there is an update, it asks the user if they want to download it. If yes, it asks the user for the save location,
        then downloads the VampHelper.zip file to that location via HTML.
        """
        import urllib2
        url = "http://sites.google.com/site/marco262/stuff/VampHelper.update"
        u = None
        try:
            u = urllib2.urlopen(url)
            line1 = u.readline().strip()
            line2 = u.readline().strip()
        except Exception as e:
            if not autocheck:
                self.ErrorDialog("Error trying to contact update server:\n"+str(e))
        finally:
            if u: u.close()
        if not u: return
        try:
            v_web = [int(c) for c in line1.split('.')]
            v_local = [int(c) for c in VERSION.split('.')] 
        except Exception as e:
            self.ErrorDialog("Invalid update information on server:\n"+str(e))
            return
        if v_web > v_local:                        # If this version is not highest numbered version, update
            dial = wx.MessageDialog(None, "A new version ({0}) of VampHelper is available!\n".format(line1)+
                                    "Would you like to download it now?", "New version", wx.YES|wx.NO)
            if dial.ShowModal() == wx.ID_YES:
                webfilename = os.path.basename(line2)
                # Select location to save to
                dlg = wx.FileDialog(self, "Save the file", self.dirname, webfilename, "Application|*.exe",
                                    wx.SAVE | wx.OVERWRITE_PROMPT)
                if dlg.ShowModal() == wx.ID_OK:
                    # Open the file for write, write, close
                    filename=dlg.GetFilename()
                    dirname=dlg.GetDirectory()
                    # download filename from HTTP server
                    try:
                        with open(os.path.join(dirname,filename), 'wb') as f:
                            u = urllib2.urlopen(line2)
                            f.write(u.read())
                            f.flush()
                            os.fsync(f)
                    except Exception as e:
                        self.ErrorDialog("Failed to save {0} to local disk.\n{1}".format(webfilename, str(e)))
                    else:
                        dlg2 = wx.MessageDialog(None, webfilename+" downloaded successfully!\n", 
                                                "Download finished", wx.OK)
                        dlg2.ShowModal()
                        dlg2.Destroy()
                    finally:
                        if u: u.close()
                dlg.Destroy()
            dial.Destroy()
        elif not autocheck:                         # Prompt to revert, only if it was a manual check
            dial = wx.MessageDialog(None, "Your version of VampHelper ({0}) is up-to-date.".format(VERSION), 
                                    "Check for updates", wx.OK)
            dial.ShowModal()
            dial.Destroy()
        try:
            f.close()
        except:
            pass
    
    def OnGainFocusTB(self, event):
        """Highlights all text in a TextCtrl"""
        wx.CallAfter(event.GetEventObject().SelectAll)
    
    def OnLoseFocusDateCtrl(self, event):
        """When the date changes, the Attacker and Defender lists are cleared."""
        self.ClearAttDefLists()
    
    def GetUpdatedPermStatus(self, char, date=None):
        """
        Returns a character's status, including the increase they gain for their age.
        If no date is provided, it gets the date that's in the Event Date control.
        """
        if not date:
            date = DateFromString(self.EventDateCtrl.GetValue())
        # Calculate the number of status points to add for age
        delta = (date - char.get('birthday', date)).days
        return float(char.get('perm status',0)) + (delta // 3650)
    
    def AddToAttackers(self, event):
        """Wrapper to add a character to the Attacker List. See AddToSide."""
        self.AddToSide(self.AttackersTBList, self.AttackerBoxSizer)
    
    def AddToDefenders(self, event):
        """Wrapper to add a character to the Defender List. See AddToSide."""
        self.AddToSide(self.DefendersTBList, self.DefenderBoxSizer)
    
    def AddToSide(self, list, sizer):
        """
        Gets the currently selected character and adds it to the given list and sizer.
        See AddCharacterToSocialEvent.
        """
        chars = self.MasterListBox.GetSelections()
        for i in chars:
            if not self.MasterListFull[i]['active']:
                self.AddCharacterToSocialEvent(list, 
                                               sizer,
                                               self.MasterListFull[i])
#                self.MasterListFull[i]['active'] = True
        self.Redraw()
    
    def AddCharacterToSocialEvent(self, list, sizer, char={}):
        """
        Adds another character entry to the given list and sizer.
        If char is not a valid character dictionary, it adds an empty entry.
        """
        length = len(list)
        pan = wx.Panel(self.p)
        l = [wx.TextCtrl(pan, size=(100,-1), style=wx.TE_READONLY),
             wx.TextCtrl(pan, size=(30,-1), style=wx.TE_READONLY),
             wx.TextCtrl(pan, size=(30,-1), style=wx.TE_READONLY),
             wx.SpinCtrl(pan, size=(42,-1)),
             wx.SpinCtrl(pan, size=(46,-1)),
             wx.TextCtrl(pan, size=(240,-1)),
             wx.CheckBox(pan),
             pan]
        list.append(l)
        l[0].SetValue(str(char.get('name', '')))
        l[1].SetValue(str(int(self.GetUpdatedPermStatus(char))))
        l[2].SetValue(str(int(char.get('temp status', '0'))))
        l[3].SetRange(0,int(l[2].GetValue()))
        l[3].SetValue(char.get('spent', 0))
        l[3].Bind(wx.EVT_SPINCTRL, self.UpdateTotals)
        l[4].SetRange(-99,100)
        l[4].SetValue(char.get('misc', 0))
        l[4].Bind(wx.EVT_SPINCTRL, self.UpdateTotals)
        l[5].SetValue(char.get('blurb', ''))
        l[5].Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        l[6].Bind(wx.EVT_CHECKBOX, self.DeleteLine)
        l[6].SetValue(True)
        gridsizer = wx.GridBagSizer(2,5)
        gridsizer.Add(list[-1][0], (0,0), wx.DefaultSpan, wx.ALIGN_CENTER)
        gridsizer.Add(list[-1][1], (0,1), wx.DefaultSpan, wx.ALIGN_CENTER)
        gridsizer.Add(list[-1][2], (0,2), wx.DefaultSpan, wx.ALIGN_CENTER)
        gridsizer.Add(list[-1][3], (0,3), wx.DefaultSpan, wx.ALIGN_CENTER)
        gridsizer.Add(list[-1][4], (0,4), (1,2), wx.ALIGN_CENTER)
        gridsizer.Add(list[-1][5], (1,0), (1,5), wx.ALIGN_CENTER | wx.EXPAND | wx.BOTTOM, 5)
        gridsizer.Add(list[-1][6], (1,5), wx.DefaultSpan, wx.ALIGN_CENTER)
        pan.SetSizerAndFit(gridsizer)
        sizer.Add(pan, 0)
        
    def UpdateTotals(self, event):
        """Updates the attacker/defender totals and penalties based on temp status given and misc bonuses."""
        if self.suspendUpdates:
            return
        att_total = 0
        if DEBUG: print self.AttackersTBList
        for row in self.AttackersTBList:
            if DEBUG: print "FOO"
            att_total += int(row[3].GetValue()) + int(row[4].GetValue())
        self.AttackerTotalTB.SetValue(str(att_total))
        def_total = 0
        for row in self.DefendersTBList:
            def_total += int(row[3].GetValue()) + int(row[4].GetValue())
        self.DefenderTotalTB.SetValue(str(def_total))
        delta = att_total - def_total
        if delta < 0:
            self.AttackerMainPenaltyTB.SetValue(str(delta / 10.0))
            self.AttackerHelpPenaltyTB.SetValue(str(delta / 100.0))
        else:
            self.AttackerMainPenaltyTB.SetValue('0')
            self.AttackerHelpPenaltyTB.SetValue('0')
        if delta > 0:
            self.DefenderMainPenaltyTB.SetValue(str(delta / -10.0))
            self.DefenderHelpPenaltyTB.SetValue(str(delta / -100.0))
        else:
            self.DefenderMainPenaltyTB.SetValue('0')
            self.DefenderHelpPenaltyTB.SetValue('0')
    
    def ClearAttDefLists(self):
        """Removes all entries from the attacker and defender lists."""
        for list in [self.AttackersTBList, self.DefendersTBList]:
            for row in list:
                for c in row:
                    c.Destroy()
        self.AttackersTBList = []
        self.DefendersTBList = []
    
    def DeleteLine(self, event):
        """Removes a single entry from the attacker or defender list."""
        checkbox = event.GetEventObject()
        for list in [self.AttackersTBList, self.DefendersTBList]:
            for i,x in enumerate(list):
                row = x
                if checkbox == row[6]:
                    for c in row:
                        c.Destroy()
                    list.pop(i)
#                    if list == self.AttackersTBList: sizer = self.AttackerBoxSizer
#                    if list == self.DefendersTBList: sizer = self.DefenderBoxSizer
#                    sizer.Remove(i)
                    self.Redraw()
                    self.UpdateTotals(event)
                    return
    
    def Redraw(self):
        """Redraws the frame, usually after the attacker and/or defender entry lists have been changed."""
        self.p.Fit()
        self.p.Layout()
        self.Fit()
        self.Layout()
        self.Refresh()
    
    def OnCommit(self, event):
        """
        Marks the end of a social event.
        Applies penalties to the perm statuses of the losing side.
        Reduces all available temp status by the amount spent in the last event.
        Resets all Spent and Misc values to 0.
        Writes all details of the event to the season log.
        """
        main_att = float(self.AttackerMainPenaltyTB.GetValue())
        help_att = float(self.AttackerHelpPenaltyTB.GetValue())
        main_def = float(self.DefenderMainPenaltyTB.GetValue())
        help_def = float(self.DefenderHelpPenaltyTB.GetValue())
        
        out = "{0} -- {1}\n".format(self.EventTitleTB.GetValue(), self.EventDateCtrl.GetValue())
        out += "{0} attacks {1}: ".format(self.AttackersTBList[0][0].GetValue(), self.DefendersTBList[0][0].GetValue())
        if main_def:
            out += "Success!"
#            winner = 1
        elif main_att:
            out += "Fail!"
#            winner = -1
        else:
            out += "Stalemate!"
#            winner = 0
        out += "   ({0} vs. {1})\n".format(self.AttackerTotalTB.GetValue(), self.DefenderTotalTB.GetValue())
        
        # Go through Attackers list first, then Defenders 
        for list in [self.AttackersTBList, self.DefendersTBList]:
            if list == self.AttackersTBList:
                out += "\nAttackers:\n"
            elif list == self.DefendersTBList:
                out += "\nDefenders:\n"
            for row in list:
                # Log current stats before commit
                out += "{0}  ({1} perm, {2} temp, {3} spent, {4} misc)\n    {5}\n".format(row[0].GetValue(),
                                                                                          row[1].GetValue(),
                                                                                          row[2].GetValue(),
                                                                                          row[3].GetValue(),
                                                                                          row[4].GetValue(),
                                                                                          row[5].GetValue())
                # Decide which penalty to use
                # Based on which list and if it's the main attacker
                if list == self.AttackersTBList:
                    if row == list[0]:
                        penalty = main_att
                    else:
                        penalty = help_att
                elif list == self.DefendersTBList:
                    if row == list[0]:
                        penalty = main_def
                    else:
                        penalty = help_def
                # Set values in main status list first
                perm_status = 0
                temp_status = 0
                name = row[0].GetValue()
                for i,x in enumerate(self.MasterListFull):
                    c = x
                    if c.get('name','') == name:
                        perm_status = c['perm status'] + penalty
                        c['perm status'] = perm_status
                        updated_perm_status = int(self.GetUpdatedPermStatus(c))
                        temp_status = c['temp status'] - float(row[3].GetValue())
                        c['temp status'] = temp_status
                        if DEBUG: print perm_status, temp_status
                        # Set Listbox text for this character
                        self.MasterListNames[i] = "{0} ({1}/{2})".format(name,
                                                                         int(temp_status),
                                                                         updated_perm_status)
                        break
                if DEBUG: print row[0].GetValue(), row[1].GetValue()
                # Set values in the main area
                row[1].SetValue(str(updated_perm_status))
                row[2].SetValue(str(int(temp_status)))
                row[3].SetValue(0)
                row[4].SetValue(0)
        if main_att or main_def:
            if main_att:
                list = self.AttackersTBList
                main = main_att
                help = help_att
            elif main_def:
                list = self.DefendersTBList
                main = main_def
                help = help_def
            helpers = ", ".join([row[0].GetValue() for row in list[1:]])
            out += "\n{0} lost {1} status\n".format(list[0][0].GetValue(), -1*main)
            if helpers:
                out += "{0} lost {1} status\n".format(helpers, -1*help)
        out += "-"*80+"\n"
        self.MasterListBox.Set(self.MasterListNames)
        self.UpdateTotals(event)
        
        with open(os.path.join(self.DataPath,'logs',self.SeasonTitleTB.GetValue()+".log"), 'a') as f:
            f.write(out)
                
    def BuildCharDict(self, *args):
        """Creates a new character dictionary"""
        key_list = ['name', 'generation', 'clan', 'perm status', 'temp status', 'birthday', 
                    'blood bonds', 'boons', 'active', 'rewards']
        default_list = ['None',12,'None',0,0,datetime.date.today(),{},{},False,
                        [False]*10]
        char = {}
        for i,a in enumerate(args):
            char[key_list[i]] = a
        for j,k in enumerate(key_list, i+1):
            char[key_list[j]] = default_list[j]
        return char
    
#    def NewCharacter(self, name, generation, clan, perm, temp):
#        return {'name':name,
#                'generation':generation,
#                'clan':clan,
#                'perm status':perm,
#                'temp status':temp,
#                'birthday':'',
#                'blood bonds':{},
#                'boons':{},
#                'active':False}
        
    def AddToMasterList(self, event):
        """
        Calls up a new Character Sheet window, and adds the character to the Master list, if it has a valid name.
        Updates the character's perm status for the current date. For this reason, only add new characters at the 
        beginning of a season, or expect their perm status to be slightly out of wack, if the date has changed since
        the start of the season.
        """
        bad_name = False
        sheet = CharacterEdit(self, boons_dict = self.boonsDict)
        sheet.ShowModal()
        stats = sheet.stats
        sheet.Destroy()
        if not stats:
            return
        if not sheet.stats.get('name',''):
            dlg = wx.MessageDialog(None, "Please choose a valid name for the character.", 
                                   "No name given", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return
        for c in self.MasterListFull:
            if c.get('name', '') == stats.get('name',''):
                dlg = wx.MessageDialog(None, "That name is already in use. Please choose another.", 
                                   "Duplicate name", wx.OK)
                dlg.ShowModal()
                dlg.Destroy()
                return
        status = self.GetUpdatedPermStatus(stats)
        if status < 0:
            dlg = wx.MessageDialog(None, "The embrace date cannot be after the current event date.", 
                                   "Time traveler!", wx.OK)
            dlg.ShowModal()
            dlg.Destroy()
            return
        # If temp status was not defined, set equal to updated perm status
        if stats['temp status'] == '':
            stats['temp status'] = status
        self.MasterListFull.append(stats)
        self.MasterListNames.append("{0} ({1}/{2})".format(stats['name'],
                                                           int(stats['temp status']),
                                                           int(status)))
        self.MasterListBox.Set(self.MasterListNames)
        self.MasterListBox.SetSelection(len(self.MasterListNames)-1)
    
    def RemoveFromMasterList(self, event):
        """Removes all selected items from the Master list."""
        sel = self.MasterListBox.GetSelections()
        self.MasterListFull = [x for i,x in enumerate(self.MasterListFull)
                               if i not in sel]
        self.MasterListNames = [x for i,x in enumerate(self.MasterListNames)
                                if i not in sel]
#        for i in self.MasterListBox.GetSelections():
#            del self.MasterListFull[i]
#            del self.MasterListNames[i]
        self.MasterListBox.Set(self.MasterListNames)
    
    def EditCharInMasterList(self, event):
        """Edits the top selected character in the MasterListBox"""
        # If doubleclicked, use the item that was doubleclicked
        if event.IsSelection():
            i = event.GetSelection()
        # If button press, get top item of selections
        else:
            i = self.MasterListBox.GetSelections()
            if not i: return
            i = i[0]
        self.MasterListBox.DeselectAll(i)
        name = self.MasterListFull[i]['name']
        sheet = CharacterEdit(self, "Editting "+name, self.MasterListFull[i], boons_dict = self.boonsDict)
        sheet.ShowModal()
        if sheet.stats:
            status = self.GetUpdatedPermStatus(sheet.stats)
            self.MasterListFull[i] = sheet.stats
            self.MasterListNames[i] = ("{0} ({1}/{2})".format(sheet.stats['name'],
                                                              int(sheet.stats['temp status']),
                                                              int(status)))
            self.MasterListBox.Set(self.MasterListNames)
        sheet.Destroy()

class CharacterEdit(wx.Dialog):
    
    stats = {}
    
    def __init__(self, parent, title="New character", char={}, boons_dict={}):
        """
        A character sheet designed to easily display and edit everything about a character.
        Includes basic info: Name, Generation, Clan, Status, etc.
        Includes a list of all possible status "rewards".
        Will eventually have a way to easily edit blood bonds and boons per character.
        """
        wx.Dialog.__init__(self, parent, title=title)
        self.SetSize((380, 370))
        
        self.RewardsCheckBoxList = []
        
        p = wx.Panel(self)
        
        self.NameTB = wx.TextCtrl(p)
        self.NameTB.SetValue(char.get('name',''))
        self.GenSpin = wx.SpinCtrl(p, value=str(char.get('generation', 12)), size=(42,-1))
        self.GenSpin.SetRange(1,100)
        self.GenSpin.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusSpin)
        clan_names = ['Brujah', 'Malkavian', 'Nosferatu', 'Toreador', 'Tremere', 'Ventrue', '',
                      'Lasombra', 'Tzimisce', '',
                      'Assamite', 'Follower of Set', 'Gangrel', 'Giovanni', 'Ravnos',
                      'Daughter of Cacophony']
        self.ClanTB = PromptingComboBox(p, char.get('clan',''), clan_names, size=(100,-1))
        self.BirthdayTB = wx.TextCtrl(p, size=(100,-1))#, style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self.BirthdayTB.SetValue(str(char.get('birthday',datetime.date.today())))
        self.PermStatusSpin = wx.TextCtrl(p, value=str(char.get('perm status', 0)), size=(40,-1))
        self.TempStatusSpin = wx.TextCtrl(p, value=str(char.get('temp status', '')), size=(40,-1))
        
        rewardsNames = ["Welcomed by the authority (1)", "Recognized Neonite (3)", "Recognized Ancilla (6)", 
                        "Recognized Elder (9)", "Primogenture (2)", "Lesser Office (3)", "Greater Office (4)", 
                        "Prince (10)", "Baron (8)", "Harpy (10)"]
        
        r = char.get('rewards',[False]*10)
        for i in xrange(10):
            cb = wx.CheckBox(p, id=100+i, label=rewardsNames[i])
            self.RewardsCheckBoxList.append(cb)
            cb.Bind(wx.EVT_CHECKBOX, self.UpdateStatus)
            cb.SetValue(r[i])
        
        okButton = wx.Button(p, wx.ID_OK, label="OK")
        okButton.Bind(wx.EVT_BUTTON, self.OnOKPress)
        cancelButton = wx.Button(p, wx.ID_CANCEL, label="Cancel")
        cancelButton.Bind(wx.EVT_BUTTON, self.OnCancelPress)
        self.Bind(wx.EVT_CLOSE, self.OnCancelPress)
        
        gridsizer = wx.FlexGridSizer(5,2)
        gridsizer.Add(wx.StaticText(p, label="Name:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        gridsizer.Add(self.NameTB, 0, wx.ALL, 3)
        gridsizer.Add(wx.StaticText(p, label="Generation:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        gridsizer.Add(self.GenSpin, 0, wx.ALL, 3)
        gridsizer.Add(wx.StaticText(p, label="Clan:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        gridsizer.Add(self.ClanTB, 0, wx.ALL, 3)
        gridsizer.Add(wx.StaticText(p, label="Embraced:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        gridsizer.Add(self.BirthdayTB, 0, wx.ALL, 3)
        gridsizer.Add(wx.StaticText(p, label="Perm Status:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        gridsizer.Add(self.PermStatusSpin, 0, wx.ALL, 3)
        gridsizer.Add(wx.StaticText(p, label="Temp Status:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 3)
        gridsizer.Add(self.TempStatusSpin, 0, wx.ALL, 3)
        statsBox = wx.StaticBox(p, label='Stats')
        statsSizer = wx.StaticBoxSizer(statsBox, wx.VERTICAL)
        statsSizer.Add(gridsizer, 1, wx.EXPAND)
        
        rewardsBox = wx.StaticBox(p, label='Status Updates')
        rewardsSizer = wx.StaticBoxSizer(rewardsBox, wx.VERTICAL)
        for cb in self.RewardsCheckBoxList:
            rewardsSizer.Add(cb, 0, wx.ALL, 2)
        
        self.BoonsList = wx.ComboBox(p, style=wx.CB_READONLY | wx.CB_SORT)
        self.BoonsList.Bind(wx.EVT_COMBOBOX, self.GetBoonsOwed)
        items = [k for k in boons_dict
                 if not k == char.get('name','')]
        self.BoonsList.AppendItems(items)
        if len(items) > 0:
            self.BoonsList.SetSelection(0)
        self.BoonValueSpin = wx.SpinCtrl(p, size=(42,-1))
        self.BoonValueSpin.SetRange(0,100)
        self.BoonDescText = ""
        
        hSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hSizer1.Add(statsSizer, 0, wx.ALL | wx.EXPAND, 2)
        hSizer1.Add(rewardsSizer, 0, wx.ALL | wx.EXPAND, 2)
        
        boonsSizer = wx.BoxSizer(wx.VERTICAL)
        boonsSizer.Add(self.BoonsList, 0)
        
        buttonsizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsizer.Add(okButton, 0, wx.ALL, 3)
        buttonsizer.Add(cancelButton, 0, wx.ALL, 3)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(hSizer1, 0)
        sizer.Add(boonsSizer, 0, wx.ALIGN_CENTER)
        sizer.Add(buttonsizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        
        p.SetSizerAndFit(sizer)
        p.SetAutoLayout(1)
        sizer.Fit(p)
        self.Fit()
    
    def OnGainFocusSpin(self, event):
        event.GetEventObject().SetSelection(0,-1)
    
    def OnOKPress(self, event):
        temp_status = self.TempStatusSpin.GetValue()
        # If temp status is blank, leave blank
        if temp_status:
            temp_status = max(float(self.TempStatusSpin.GetValue()),0)
        self.stats = {'name':self.NameTB.GetValue(),
                      'generation':self.GenSpin.GetValue(),
                      'clan':self.ClanTB.GetValue(),
                      'birthday':DateFromString(self.BirthdayTB.GetValue()),
                      'perm status':max(float(self.PermStatusSpin.GetValue()),0),
                      'temp status':temp_status,
                      'blood bonds':{},
                      'boons':{},
                      'active':False,
                      'rewards':[cb.GetValue() for cb in self.RewardsCheckBoxList]
                      }
        self.Destroy()
    
    def OnCancelPress(self, event):
        if DEBUG: print self.GetSize()
        self.Destroy()

    def UpdateStatus(self, event):
        # Status amounts that are gained/lost
        nums = [1,3,6,9,2,3,4,10,8,10]
        i = event.GetId() % 100
        if self.RewardsCheckBoxList[i].GetValue():
            delta = nums[i]
        else:
            delta = -1*nums[i]
        self.PermStatusSpin.SetValue(str(float(self.PermStatusSpin.GetValue()) + delta))
#        if self.TempStatusSpin.GetValue():
#            self.TempStatusSpin.SetValue(str(float(self.TempStatusSpin.GetValue()) + nums[i]))
    
    def GetBoonsOwed(self, event):
        pass

# From http://wiki.wxpython.org/Combo%20Box%20that%20Suggests%20Options
# with a few minor changes
class PromptingComboBox(wx.ComboBox):
    def __init__(self, parent, value, choices=[], style=0, **par):
        wx.ComboBox.__init__(self, parent, wx.ID_ANY, value, style=style|wx.CB_DROPDOWN, choices=choices, **par)
        self.choices = choices
        self.Bind(wx.EVT_TEXT, self.EvtText)
        self.Bind(wx.EVT_CHAR, self.EvtChar)
        self.Bind(wx.EVT_COMBOBOX, self.EvtCombobox)
        self.ignoreEvtText = False

    def EvtCombobox(self, event):
        self.ignoreEvtText = True
        event.Skip()

    def EvtChar(self, event):
        if event.GetKeyCode() == 8:
            self.ignoreEvtText = True
        event.Skip()

    def EvtText(self, event):
        if self.ignoreEvtText:
            self.ignoreEvtText = False
            return
        currentText = event.GetString()
        for choice in self.choices:
            if choice.startswith(currentText):
                self.SetValue(choice)
                self.SetInsertionPoint(len(currentText))
                self.SetMark(len(currentText), len(choice))
                return

class DrawFrame(wx.Frame):

    boonsDict = {}
    BoonsKeys = []
    CIRCLE_RADIUS = 20
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self,*args,**kwargs)
        
        self.Canvas = FloatCanvas.FloatCanvas(self,-1,(500,500),
#                                              BackgroundColor = "DARK SLATE BLUE",
                                              Debug = 0)

        wx.EVT_CLOSE(self, self.OnCloseWindow)

        FloatCanvas.EVT_LEFT_UP(self.Canvas, self.OnLeftUp ) 
        FloatCanvas.EVT_LEFT_DOWN(self.Canvas, self.OnLeftClick ) 

        self.ResetSelections()
    
    def ResetSelections(self):
        self.SelectedPoly = None
        self.SelectedPolyOrig = None
        self.SelectedPoints = None
        self.PointSelected = False
        self.SelectedPointNeighbors = None
    
    def OnCloseWindow(self, event):
        self.Destroy()
        
    def OnLeftUp(self, event):
        ## if a point was selected, it's not anymore
        if self.PointSelected:
            self.SelectedPoly.Points[self.SelectedPoints.Index] = event.GetCoords()
            self.SelectedPoly.SetPoints(self.SelectedPoly.Points, copy = False)
            self.SelectedPoints.SetPoints(self.SelectedPoly.Points, copy = False)
            self.PointSelected = False
            self.SelectedPointNeighbors = None
            self.Canvas.Draw()

    def OnLeftClick(self,event):
        ## If a click happens outside the polygon, it's no longer selected
        self.DeSelectPoly()
        self.Canvas.Draw()
    
    def Setup(self, event=None, boons={}):
        wx.GetApp().Yield()
        self.ResetSelections()
        self.Canvas.ClearAll()

        Range = (-10,10)

        self.boonsDict = boons
        self.BoonsKeys = boons.keys()
##        # Create a couple of random Polygons
##        for i, color in enumerate(("LightBlue", "Green", "Purple","Yellow")):
##            points = RandomArray.uniform(Range[0],Range[1],(6,2))
##            Poly = self.Canvas.AddPolygon(points,
##                                     LineWidth = 2,
##                                     LineColor = "Black",
##                                     FillColor = color,
##                                     FillStyle = 'Solid')
##
##            Poly.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.SelectPoly)
        self.DrawIcons()
        self.DrawRelationships()
#        p1 = (-2,-2)
#        p2 = (-10,-2)
#        self.Canvas.AddLine((p1,p2),LineWidth = 3)
#        offset = self.GetOffsetLines(p1,p2)
#        self.Canvas.AddLine(offset[0])
#        self.Canvas.AddLine(offset[1])
        self.Canvas.ZoomToBB()

    def DrawIcons(self):
        positions = self.GenerateIconPositions(len(self.BoonsKeys))
        if DEBUG: print self.BoonsKeys
        for i,p in enumerate(positions):
            d = self.boonsDict[self.BoonsKeys[i]]
            d['!pos'] = p
            if not d['!color']:
                d['!color'] = self.RandomColor()
            c = self.Canvas.AddCircle(p, self.CIRCLE_RADIUS*2, FillColor=d['!color'])
            c.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.SelectPoly)
            self.Canvas.AddText("{0} ({1})".format(self.BoonsKeys[i],self.TotalBoonPoints(d)), 
                                p, Size=self.CIRCLE_RADIUS/1.5, Position = "cc", Weight=wx.BOLD)
            
    def DrawRelationships(self):
#        print help(self.Canvas.AddArrowLine)
        for k in self.BoonsKeys:
            master = self.boonsDict[k]
            for i,b in enumerate(master):
                if b in self.BoonsKeys:
                    slave = self.boonsDict[b]
                    boon = master[b]
                    arrow = self.GenerateArrow(master['!pos'], slave['!pos'], offset=self.CIRCLE_RADIUS)
                    self.Canvas.AddArrowLine(arrow, LineWidth=5, LineColor=master['!color'], ArrowHeadSize=16)
                    self.Canvas.AddText(str(boon[0]), arrow[0], Weight=wx.BOLD)

    def GenerateIconPositions(self, n, d=200):
        if n < 1: return []
        
        phi = 2*pi / n
        # radius depends on the icons spacing
        r = (n * d / (2.0 * pi))

        startpos = [0, r]
        thepos = [0, 0]

        l = []
        for i in xrange(n):
           
           cosPhi = cos(i * phi)
           sinPhi = sin(i * phi)
           
           # Rotate:            
           # x := x * cos(phi) - y * sin(phi)
           # y := x * sin(phi) + y * cos(phi)
           l.append([int(startpos[0]*cosPhi - startpos[1]*sinPhi),
                     int(startpos[0]*sinPhi + startpos[1]*cosPhi)])
           
        return l
        
    def RandomColor(self):
        a = random.randint(1,255)
        b = random.randint(1,255)
        c = max(255-(a+b),random.randint(1,255))    # Guarantees the color won't be too dark
        return (a, b, c, 255)

    def TotalBoonPoints(self, d):
        return sum([d[b][0] for b in d
                    if not b.startswith('!')])

    def GenerateArrow(self, p1, p2, offset=2):
        hyp = ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5
        if not hyp: return (p1,p2),(p1,p2)
        x,y = (p2[1]-p1[1])*(offset/hyp), (p2[0]-p1[0])*(offset/hyp)
        return ([sum(a) for a in zip(p1, (-x,y))], [sum(a) for a in zip(p2, (-x,y))])

    def SelectPoly(self, Object):
        Canvas = self.Canvas
        if Object is self.SelectedPolyOrig:
            pass
        else:
            if self.SelectedPoly:
                self.DeSelectPoly()
            self.SelectedPolyOrig = Object
            self.SelectedPoly = Canvas.AddPolygon(Object.Points,
                                                  LineWidth = 2,
                                                  LineColor = "Red",
                                                  FillColor = "Red",
                                                  FillStyle = "CrossHatch",
                                                  InForeground = True)
            # Draw points on the Vertices of the Selected Poly:
            self.SelectedPoints = Canvas.AddPointSet(Object.Points,
                                                     Diameter = 6,
                                                     Color = "Red",
                                                     InForeground = True)
            self.SelectedPoints.Bind(FloatCanvas.EVT_FC_LEFT_DOWN, self.SelectPointHit)
            Canvas.Draw()

    def DeSelectPoly(self):
        Canvas = self.Canvas
        if self.SelectedPolyOrig is not None:
            self.SelectedPolyOrig.SetPoints(self.SelectedPoly.Points, copy = False)
            self.Canvas.Draw(Force = True)
            Canvas.RemoveObject(self.SelectedPoly)
            Canvas.RemoveObject(self.SelectedPoints)
        self.ResetSelections()

    def SelectPointHit(self, PointSet):
        PointSet.Index = PointSet.FindClosestPoint(PointSet.HitCoords)
        if DEBUG: print "point #%i hit"%PointSet.Index
        #Index = PointSet.Index
        self.PointSelected = True

def DateFromString(t):
    if type(t) is datetime.datetime:
        return t.date()
    return parser.parse(t).date()        


if __name__ == "__main__":
    app = wx.App(redirect=False)
    MainFrame().Show()
    app.MainLoop()

"""
Changelog:

0.9.0 (07-25-11)
* First alpha release of the app
* Handles seasons
* Handles event calculations and stores the stats changes
* Saves/loads/autoloads files
* Auto-updates over the web

0.9.1 (07-26-11)
* Fixed crash when trying to update with no net connection
* Updating status in character sheet screen now only updates perm status
* Added event logging

0.9.2 (08-09-2011)
* First attempts at integrating a FloatCanvas to show boons and blood bonds
* Fixed a bug where sometimes penalties weren't committed properly.

0.9.3 (??)
* Embrace dates after the current event date are no longer allowed when adding new characters
* Fixed bug where trying to remove multiple entries from the master list sometimes caused a crash
"""