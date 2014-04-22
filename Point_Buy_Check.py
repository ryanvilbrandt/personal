#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

# Process command line arguments
DEBUG = False
TITLE = "Point Buy calculator"

class MyFrame(wx.Frame):
    
    pathfinder_point_list = ["","","","","","","",-4,-2,-1,0,1,2,3,5,7,10,13,17,""]
    dandd_5e_point_list = ["","","","","","","","",0,1,2,3,4,5,7,9,12,"","",""]
    
    def __init__(self):
        wx.Frame.__init__(self, None, title=TITLE, style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | 
                          wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        
        self.InitGUI()

    def InitGUI(self):
        size = (435, 320)
        self.SetSize(size)
#        self.SetSize(wx.Size(1150, 700))
        
        p = wx.Panel(self)
        
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        
        attr_names = ['Str','Dex','Con','Int','Wis','Cha']
        self.AttrSpinList = [wx.SpinCtrl(p, value='10', min=7, max=18, size=(55,-1)) for n in xrange(6)]
        self.CurLabelList = [wx.TextCtrl(p, value="XXX", size=(35,-1), style=wx.TE_READONLY)
                             for n in enumerate(self.AttrSpinList)]
        self.DecLabelList = [wx.TextCtrl(p, value="XXX", size=(75,-1), style=wx.TE_READONLY)
                             for n in enumerate(self.AttrSpinList)]
        self.IncLabelList = [wx.TextCtrl(p, value="XXX", size=(75,-1), style=wx.TE_READONLY)
                             for n in enumerate(self.AttrSpinList)]
        self.TotalCtrl = wx.TextCtrl(p, size=(55,-1), style=wx.TE_READONLY)
        self.TotalCtrl.SetFont(font)

        sizer = wx.FlexGridSizer(cols=5)
        
        sizer.Add(wx.StaticText(p, label=""), 0, wx.ALL, 3)
        sizer.Add(wx.StaticText(p, label=""), 0, wx.ALL, 3)
        sizer.Add(wx.StaticText(p, label="Current cost"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)
        sizer.Add(wx.StaticText(p, label="Cost to decrement"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)
        sizer.Add(wx.StaticText(p, label="Cost to increment"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)
        
        for i,s in enumerate(self.AttrSpinList):
            text = wx.StaticText(p,label=attr_names[i])
            text.SetFont(font)
            sizer.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
            s.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusSpin)
            s.Bind(wx.EVT_TEXT, self.RecalcPoints)
            s.SetFont(font)
            sizer.Add(s, 0, wx.ALL, 3)
            self.CurLabelList[i].SetFont(font)
            self.CurLabelList[i].SetBackgroundColour("White")
            sizer.Add(self.CurLabelList[i], 0, wx.ALIGN_CENTER | wx.ALL, 3)
            self.DecLabelList[i].SetFont(font)
            self.DecLabelList[i].SetBackgroundColour("White")
            sizer.Add(self.DecLabelList[i], 0, wx.ALIGN_CENTER | wx.ALL, 3)
            self.IncLabelList[i].SetFont(font)
            self.IncLabelList[i].SetBackgroundColour("White")
            sizer.Add(self.IncLabelList[i], 0, wx.ALIGN_CENTER | wx.ALL, 3)
        
        sizer.Add(wx.StaticText(p, label=""), 0, wx.ALL, 5)
        sizer.Add(wx.StaticText(p, label=""), 0, wx.ALL, 5)
        sizer.Add(wx.StaticText(p, label=""), 0, wx.ALL, 5)
        sizer.Add(wx.StaticText(p, label=""), 0, wx.ALL, 5)
        sizer.Add(wx.StaticText(p, label=""), 0, wx.ALL, 5)
        
        text = wx.StaticText(p, label="Points")
        text.SetFont(font)
        sizer.Add(text, 0, wx.ALL, 3)
        sizer.Add(self.TotalCtrl, 0, wx.ALL, 3)
        
        point_buy_table1 = wx.StaticText(p, label="7\n8\n9\n10\n11\n12\n13\n14\n15\n16\n17\n18")
        point_buy_table2 = wx.StaticText(p, label="-4\n-2\n-1\n0\n1\n2\n3\n5\n7\n10\n13\n17")
        
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(sizer, 0, wx.ALL, 3)
        hsizer.Add(point_buy_table1, 0, wx.ALL, 5)
        hsizer.Add(point_buy_table2, 0, wx.ALL, 5)
        
        p.SetSizerAndFit(hsizer)
        p.SetAutoLayout(1)
        hsizer.Fit(p)
        self.Center()
        
        self.RecalcPoints(None)

    def OnGainFocusSpin(self, event):
        wx.CallAfter(event.GetEventObject().SetSelection,0,-1)
    
    def GetPointList(self):
        return self.pathfinder_point_list
    
    def RecalcPoints(self, event):
#        print self.GetSize()
        total = 0
        try:
            for i,tc in enumerate(self.AttrSpinList):
                val = int(tc.GetValue())
                point_list = self.GetPointList()
                cur_cost = point_list[val]
                dec_cost = point_list[val-1]
                inc_cost = point_list[val+1]
                total += cur_cost
                
                self.CurLabelList[i].SetValue("{0}".format(cur_cost))
                
                if dec_cost == "":
                    temp = '--'
                else:
                    temp = "{0:+} ({1})".format(dec_cost-cur_cost, dec_cost)
                self.DecLabelList[i].SetValue(temp)
                
                if inc_cost == "":
                    temp = '--'
                else:
                    temp = "{0:+} ({1})".format(inc_cost-cur_cost, inc_cost)
                self.IncLabelList[i].SetValue(temp)
                    
            self.TotalCtrl.SetValue(str(total))
        except TypeError:
            pass
        

if __name__ == "__main__":
    app = wx.App(redirect=False)
    MyFrame().Show()
    app.MainLoop()
