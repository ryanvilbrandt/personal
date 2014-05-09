import wx

TITLE = "SlaveHack Progress bar proof of concept"

class SHFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title=TITLE, style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | 
                          wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        
        self.InitGUI()
        self.MasterCpuList = []
        self.MasterConnList = []
##        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def InitGUI(self):
##        self.SetMinSize(wx.Size(500, 600))
##        self.SetSize(wx.Size(500, 600))

        self.p = wx.Panel(self)

        # create splitters:
        split1 = ProportionalSplitter(self.p,-1, 0.60, style=wx.SP_3DSASH | wx.SP_NO_XP_THEME)
        # create controls to go in the splitter windows...
        main_panel = wx.Panel(split1)
        progress_window = wx.ScrolledWindow(split1)
        progress_window.SetScrollbars(20,20,-1,-1)
        self.ProgressPanel = wx.Panel(progress_window)
##        self.ProgressPanel.SetScrollbar(wx.VERTICAL, 0, 6, 50)
        # add your controls to the splitters:
        split1.SplitHorizontally(main_panel, progress_window)

        button1 = wx.Button(main_panel, label="Add CPU")
        button1.Bind(wx.EVT_BUTTON, self.AddToCpuTasks)
        button2 = wx.Button(main_panel, label="Add Conn")
        button2.Bind(wx.EVT_BUTTON, self.AddToConnectionTasks)
        button3 = wx.Button(main_panel, label="Del CPU")
        button3.Bind(wx.EVT_BUTTON, self.DelCpuTask)
        button4 = wx.Button(main_panel, label="Del CPU")
        button4.Bind(wx.EVT_BUTTON, self.DelConnectionTask)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        main_panel.SetSizerAndFit(mainSizer)

        mainSizer.Add(button1, 0)
        mainSizer.Add(button2, 0)
        mainSizer.Add(button3, 0)
        mainSizer.Add(button4, 0)
        
        # Build process window
        progressSizer = wx.BoxSizer(wx.VERTICAL)
        self.ProgressPanel.SetSizerAndFit(progressSizer)

        cpuBox = wx.StaticBox(self.ProgressPanel, label='CPU tasks')
        self.CpuSizer = wx.StaticBoxSizer(cpuBox, wx.VERTICAL)
        progressSizer.Add(self.CpuSizer, 0, wx.EXPAND | wx.ALL, 3)
        self.CpuGridSizer = wx.GridBagSizer(2,5)

        connBox = wx.StaticBox(self.ProgressPanel, label='Connection tasks')
        self.ConnSizer = wx.StaticBoxSizer(connBox, wx.VERTICAL)
        progressSizer.Add(self.ConnSizer, 0, wx.EXPAND | wx.ALL, 3)
        self.ConnGridSizer = wx.GridBagSizer(2,5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(split1, 1, wx.EXPAND)

        self.p.SetSizerAndFit(sizer)
        self.p.SetAutoLayout(1)
##        sizer.Fit(self.p)
##        self.Fit()
        self.Center()

    def AddToCpuTasks(self, event):
        self.AddToTasks("CPU Task {0}".format((len(self.MasterCpuList)+1)), "", 0, self.MasterCpuList, self.CpuSizer)

    def AddToConnectionTasks(self, event):
        self.AddToTasks("Conn Task {0}".format("TEST"*(len(self.MasterConnList)+1)), "", 0, self.MasterConnList, self.ConnSizer)

    def AddToTasks(self, name, task_type, total_size, proc_list, sizer):
        gauge = wx.Gauge(self.ProgressPanel, -1, 1000)

        proc_list.append({"name":name, "type":task_type, "gauge":gauge, "progress":0, "total":total_size})

        self.BuildProcessSizers(proc_list)

    def BuildProcessSizers(self, task_list=[]):
        if (not task_list or task_list == self.MasterCpuList) and self.MasterCpuList:
            del self.CpuGridSizer
            self.CpuGridSizer = wx.GridBagSizer(2,5)
            for i,n in enumerate(self.MasterCpuList):
                self.CpuGridSizer.Add(wx.StaticText(self.ProgressPanel, label=n["name"]), (i,0), wx.DefaultSpan, wx.ALIGN_CENTER)
                self.CpuGridSizer.Add(n["gauge"], (i,1), wx.DefaultSpan, wx.ALIGN_CENTER | wx.EXPAND)
                self.CpuGridSizer.Add(wx.StaticText(self.ProgressPanel, label="00h 00m"), (i,2), wx.DefaultSpan, wx.ALIGN_CENTER)
            self.CpuGridSizer.AddGrowableCol(1)
            self.CpuSizer.Clear()
            self.CpuSizer.Add(self.CpuGridSizer, 1, wx.EXPAND)
        if (not task_list or task_list == self.MasterConnList) and self.MasterConnList:
            del self.ConnGridSizer
            self.ConnGridSizer = wx.GridBagSizer(2,5)
            for i,n in enumerate(self.MasterConnList):
                self.ConnGridSizer.Add(wx.StaticText(self.ProgressPanel, label=n["name"]), (i,0), wx.DefaultSpan, wx.ALIGN_CENTER)
                self.ConnGridSizer.Add(n["gauge"], (i,1), wx.DefaultSpan, wx.ALIGN_CENTER | wx.EXPAND)
                self.ConnGridSizer.Add(wx.StaticText(self.ProgressPanel, label="00h 00m"), (i,2), wx.DefaultSpan, wx.ALIGN_CENTER)
            self.ConnGridSizer.AddGrowableCol(1)
            self.ConnSizer.Clear()
            self.ConnSizer.Add(self.ConnGridSizer, 1, wx.EXPAND)
            
        self.Redraw()

    def DelCpuTask(self, event):
        pass

    def DelConnectionTask(self, event):
        pass
        
    def Redraw(self):
        """Redraws the frame"""
##        self.ProgressPanel.Fit()
        self.ProgressPanel.Layout()
##        self.p.Fit()
        self.p.Layout()
##        self.Fit()
        self.Layout()
        self.Refresh()


# Taken wholesale from http://wiki.wxpython.org/ProportionalSplitterWindow
class ProportionalSplitter(wx.SplitterWindow):
    def __init__(self, parent, id= -1, proportion=0.66, size=wx.DefaultSize, **kwargs):
        wx.SplitterWindow.__init__(self, parent, id, wx.Point(0, 0), size, **kwargs)
        self.SetMinimumPaneSize(50) #the minimum size of a pane.
        self.proportion = proportion
        if not 0 < self.proportion < 1:
            raise ValueError, "proportion value for ProportionalSplitter must be between 0 and 1."
        self.ResetSash()
        self.Bind(wx.EVT_SIZE, self.OnReSize)
        self.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGED, self.OnSashChanged, id=id)
        ##hack to set sizes on first paint event
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.firstpaint = True

    def SplitHorizontally(self, win1, win2):
        if self.GetParent() is None: return False
        return wx.SplitterWindow.SplitHorizontally(self, win1, win2,
                int(round(self.GetParent().GetSize().GetHeight() * self.proportion)))

    def SplitVertically(self, win1, win2):
        if self.GetParent() is None: return False
        return wx.SplitterWindow.SplitVertically(self, win1, win2,
                int(round(self.GetParent().GetSize().GetWidth() * self.proportion)))

    def GetExpectedSashPosition(self):
        if self.GetSplitMode() == wx.SPLIT_HORIZONTAL:
            tot = max(self.GetMinimumPaneSize(), self.GetParent().GetClientSize().height)
        else:
            tot = max(self.GetMinimumPaneSize(), self.GetParent().GetClientSize().width)
        return int(round(tot * self.proportion))

    def ResetSash(self):
        self.SetSashPosition(self.GetExpectedSashPosition())

    def OnReSize(self, event):
        "Window has been resized, so we need to adjust the sash based on self.proportion."
        self.ResetSash()
        event.Skip()

    def OnSashChanged(self, event):
        "We'll change self.proportion now based on where user dragged the sash."
        pos = float(self.GetSashPosition())
        if self.GetSplitMode() == wx.SPLIT_HORIZONTAL:
            tot = max(self.GetMinimumPaneSize(), self.GetParent().GetClientSize().height)
        else:
            tot = max(self.GetMinimumPaneSize(), self.GetParent().GetClientSize().width)
        self.proportion = pos / tot
        event.Skip()

    def OnPaint(self, event):
        if self.firstpaint:
            if self.GetSashPosition() != self.GetExpectedSashPosition():
                self.ResetSash()
            self.firstpaint = False
        event.Skip()


if __name__ == "__main__":
    app = wx.App(redirect=False)
    SHFrame().Show()
    app.MainLoop()
