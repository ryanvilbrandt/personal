# draw lines, a rounded-rectangle and a circle on a wx.PaintDC() surface
# tested with Python24 and wxPython26     vegaseat      06mar2007
# Works with Python2.5 on OSX bcl 28Nov2008

import wx 

class MyFrame(wx.Frame): 
    """a frame with a panel"""
    def __init__(self, parent=None, id=-1, title=None): 
        wx.Frame.__init__(self, parent, id, title)
        self.InitGui()

    def InitGui(self):
        p = wx.Panel(self)

        self.DrawPanel1 = wx.Panel(p, size=(350, 200))
        self.DrawPanel1.Bind(wx.EVT_PAINT, self.on_paint)
        self.DrawPanel2 = wx.Panel(p, size=(350, 200))
        self.DrawPanel2.Bind(wx.EVT_PAINT, self.on_paint)
##        self.GraphPanel = wx.Panel(self), size=(350, 200)) 
##        self.GraphPanel.Bind(wx.EVT_PAINT, self.on_paint)
        
        self.WInitPosCtrl = wx.TextCtrl(p, value="100")
        self.XInitPosCtrl = wx.TextCtrl(p, value="0")
        self.YInitPosCtrl = wx.TextCtrl(p, value="100")
        self.ZInitPosCtrl = wx.TextCtrl(p, value="0")
        
        self.WInitVelCtrl = wx.TextCtrl(p, value="0")
        self.XInitVelCtrl = wx.TextCtrl(p, value="0.5")
        self.YInitVelCtrl = wx.TextCtrl(p, value="0")
        self.ZInitVelCtrl = wx.TextCtrl(p, value="0.5")

        self.MassCtrl = wx.TextCtrl(p, value="200")

        orbit_button = wx.Button(p, label="Orbit!")
        orbit_button.Bind(wx.EVT_BUTTON, self.OnOrbitPress)
        stop_button = wx.Button(p, label="Stop!")
        stop_button.Bind(wx.EVT_BUTTON, self.OnStopPress)

        draw_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        draw_sizer1.Add(self.DrawPanel1, 1, wx.EXPAND)
        draw_sizer1.Add(self.DrawPanel2, 1, wx.EXPAND)
        draw_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        draw_sizer2.Add(wx.StaticText(p, label="X - Y"))
        draw_sizer2.Add(wx.StaticText(p, label="Z - W"))
        draw_sizer3 = wx.BoxSizer(wx.VERTICAL)
        draw_sizer3.Add(draw_sizer1, 1, wx.EXPAND)
        draw_sizer3.Add(draw_sizer2)
        textbox_sizer = wx.BoxSizer(wx.VERTICAL)
        textbox_sizer.Add(wx.StaticText(p, label="Initial Position:"))
        textbox_sizer.Add(self.WInitPosCtrl)
        textbox_sizer.Add(self.XInitPosCtrl)
        textbox_sizer.Add(self.YInitPosCtrl)
        textbox_sizer.Add(self.ZInitPosCtrl)
        textbox_sizer.Add(wx.StaticText(p, label="Initial Velocity:"))
        textbox_sizer.Add(self.WInitVelCtrl)
        textbox_sizer.Add(self.XInitVelCtrl)
        textbox_sizer.Add(self.YInitVelCtrl)
        textbox_sizer.Add(self.ZInitVelCtrl)
        textbox_sizer.Add(wx.StaticText(p, label="Mass:"))
        textbox_sizer.Add(self.MassCtrl)
        textbox_sizer.Add(orbit_button)
        textbox_sizer.Add(stop_button)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(draw_sizer3)
        top_sizer.Add(textbox_sizer)
        
        p.SetSizer(top_sizer)
        p.SetAutoLayout(1)
        top_sizer.Fit(p)

    def OnOrbitPress(self, event):
        pass
    
    def OnStopPress(self, event):
        pass

    def on_paint(self, event):
        # establish the painting surface
        dc = wx.PaintDC(self.DrawPanel1)
        dc.SetPen(wx.Pen('blue', 4))
        # draw a blue line (thickness = 4)
        dc.DrawLine(50, 20, 300, 20)
        dc.SetPen(wx.Pen('red', 1))
        # draw a red rounded-rectangle
        rect = wx.Rect(50, 50, 100, 100) 
        dc.DrawRoundedRectangleRect(rect, 8)
        # draw a red circle with yellow fill
        dc.SetBrush(wx.Brush('yellow'))
        x = 250
        y = 100
        r = 50
        dc.DrawCircle(x, y, r)


# test it ...
app = wx.PySimpleApp() 
frame1 = MyFrame(title='rounded-rectangle & circle') 
frame1.Center() 
frame1.Show() 
app.MainLoop()
