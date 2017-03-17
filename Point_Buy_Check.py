#!/usr/bin/python
# -*- coding: UTF-8 -*-

import wx

# Process command line arguments
DEBUG = False
TITLE = "Point Buy calculator"
# SYSTEM = "Pathfinder"
SYSTEM = "5e"

attr_names = ['Str', 'Dex', 'Con', 'Int', 'Wis', 'Cha']
point_list = {
    "Pathfinder": ["", "", "", "", "", "", "", -4, -2, -1, 0, 1, 2, 3, 5, 7, 10, 13, 17, ""],
    "5e": ["", "", "", "", "", "", "", "", 0, 1, 2, 3, 4, 5, 7, 9, "", "", "", ""]
}
min_attr = {"Pathfinder": 7, "5e": 8}
max_attr = {"Pathfinder": 18, "5e": 15}
start_attr = {"Pathfinder": 10, "5e": 8}

class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title=TITLE, style=wx.MINIMIZE_BOX | wx.MAXIMIZE_BOX | wx.RESIZE_BORDER | 
                          wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX | wx.CLIP_CHILDREN)
        
        self.init_gui()

    def init_gui(self):
        size = (540, 340)
        self.SetSize(size)
        
        p = wx.Panel(self)
        
        font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        table_font = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, faceName="Courier New")

        # Create list of GUI objects to be added to window later
        self.AttrSpinList = [wx.SpinCtrl(p, value=str(start_attr[SYSTEM]),
                                         min=min_attr[SYSTEM], max=max_attr[SYSTEM], size=(55, -1))
                             for _ in attr_names]
        self.BonusSpinList = [wx.TextCtrl(p, value="XXX", size=(35, -1), style=wx.TE_READONLY)
                              for _ in attr_names]
        self.CurSpinList = [wx.TextCtrl(p, value="XXX", size=(35, -1), style=wx.TE_READONLY)
                            for _ in attr_names]
        self.DecSpinList = [wx.TextCtrl(p, value="XXX", size=(75, -1), style=wx.TE_READONLY)
                            for _ in attr_names]
        self.IncSpinList = [wx.TextCtrl(p, value="XXX", size=(75, -1), style=wx.TE_READONLY)
                            for _ in attr_names]
        self.TotalCtrl = wx.TextCtrl(p, size=(55, -1), style=wx.TE_READONLY)
        self.TotalCtrl.SetFont(font)

        grid_sizer = wx.FlexGridSizer(cols=6)
        
        grid_sizer.Add(wx.StaticText(p, label=""), 0, wx.ALL, 3)
        grid_sizer.Add(wx.StaticText(p, label=""), 0, wx.ALL, 3)
        grid_sizer.Add(wx.StaticText(p, label="With bonus"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)
        grid_sizer.Add(wx.StaticText(p, label="Current cost"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)
        grid_sizer.Add(wx.StaticText(p, label="Cost to decrement"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)
        grid_sizer.Add(wx.StaticText(p, label="Cost to increment"), 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 3)

        # Loop through lists, making a row of GUI items for each ability scores
        for i, s in enumerate(self.AttrSpinList):
            text = wx.StaticText(p, label=attr_names[i])
            text.SetFont(font)
            grid_sizer.Add(text, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
            s.Bind(wx.EVT_SET_FOCUS, self.on_gain_focus_spin)
            s.Bind(wx.EVT_TEXT, self.recalc_points)
            s.SetFont(font)
            grid_sizer.Add(s, 0, wx.ALL, 3)
            self.BonusSpinList[i].SetFont(font)
            self.BonusSpinList[i].SetBackgroundColour("White")
            grid_sizer.Add(self.BonusSpinList[i], 0, wx.ALIGN_CENTER | wx.ALL, 3)
            self.CurSpinList[i].SetFont(font)
            self.CurSpinList[i].SetBackgroundColour("White")
            grid_sizer.Add(self.CurSpinList[i], 0, wx.ALIGN_CENTER | wx.ALL, 3)
            self.DecSpinList[i].SetFont(font)
            self.DecSpinList[i].SetBackgroundColour("White")
            grid_sizer.Add(self.DecSpinList[i], 0, wx.ALIGN_CENTER | wx.ALL, 3)
            self.IncSpinList[i].SetFont(font)
            self.IncSpinList[i].SetBackgroundColour("White")
            grid_sizer.Add(self.IncSpinList[i], 0, wx.ALIGN_CENTER | wx.ALL, 3)

        # Show current points spents
        text = wx.StaticText(p, label="Points Spent")
        text.SetFont(font)
        points_spent_sizer = wx.BoxSizer(wx.HORIZONTAL)
        points_spent_sizer.Add(text, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        points_spent_sizer.Add(self.TotalCtrl, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 3)
        points_spent_sizer.AddSpacer(20)

        bonus_sizer = wx.BoxSizer(wx.VERTICAL)
        bonus_sizer.Add(wx.StaticText(p, label="Pick your racial stat bonuses:"))
        if SYSTEM == "Pathfinder":
            bonus_sizer.Add(wx.StaticText(p, label="Under construction"))
        elif SYSTEM == "5e":
            # Allow the user to select the bonus type (+1 to all, or +2 to one stat and +1 to another)
            self.BonusButton1 = wx.RadioButton(p, label="+2 to ", style=wx.RB_GROUP)
            self.BonusButton1.Bind(wx.EVT_RADIOBUTTON, self.on_bonus_select)
            self.Plus2Ctrl = wx.Choice(p, choices=attr_names)
            self.Plus2Ctrl.Bind(wx.EVT_CHOICE, self.on_bonus_select)
            self.Plus2Ctrl.SetSelection(0)
            self.Plus1Ctrl = wx.Choice(p, choices=attr_names)
            self.Plus1Ctrl.Bind(wx.EVT_CHOICE, self.on_bonus_select)
            self.Plus1Ctrl.SetSelection(1)

            button1_hsizer = wx.BoxSizer(wx.HORIZONTAL)
            button1_hsizer.Add(self.BonusButton1, 0, wx.ALIGN_CENTER_VERTICAL)
            button1_hsizer.Add(self.Plus2Ctrl)
            button1_hsizer.Add(wx.StaticText(p, label="   +1 to "), 0, wx.ALIGN_CENTER_VERTICAL)
            button1_hsizer.Add(self.Plus1Ctrl)
            bonus_sizer.AddSpacer(3)
            bonus_sizer.Add(button1_hsizer, 0, wx.LEFT, border=10)

            self.BonusButton2 = wx.RadioButton(p, label="+1 to all stats")
            self.BonusButton2.Bind(wx.EVT_RADIOBUTTON, self.on_bonus_select)
            bonus_sizer.AddSpacer(3)
            bonus_sizer.Add(self.BonusButton2, 0, wx.LEFT, border=10)
        else:
            bonus_sizer.Add(wx.StaticText(p, label="Invalid system"))

        points_spent_sizer.Add(bonus_sizer)

        # Get list of indices and list of points, to print out as table
        current_point_list = self.get_point_list()
        point_list_list = ["{:< 4} {}".format(i, current_point_list[i])
                           for i in xrange(len(current_point_list))
                           if not current_point_list[i] == ""]
        point_buy_table = wx.StaticText(p, label="\n".join(point_list_list))
        point_buy_table.SetFont(table_font)
        
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(grid_sizer, 0, wx.ALL, 3)
        hsizer.Add(point_buy_table, 0, wx.ALL, 5)

        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(hsizer)
        vsizer.Add(points_spent_sizer, 0, wx.ALL, border=5)
        
        p.SetSizerAndFit(vsizer)
        p.SetAutoLayout(1)
        vsizer.Fit(p)
        self.Center()
        
        self.on_bonus_select(None)

    def on_gain_focus_spin(self, event):
        wx.CallAfter(event.GetEventObject().SetSelection, 0, -1)

    def get_point_list(self):
        return point_list[SYSTEM]
    
    def recalc_points(self, event):
        # print self.GetSize()
        # print self.BonusButton1.GetValue()
        # print self.BonusButton2.GetValue()
        total = 0
        try:
            for i, tc in enumerate(self.AttrSpinList):
                val = int(tc.GetValue())

                if SYSTEM == "5e":
                    with_bonus = val
                    if self.BonusButton2.GetValue():
                        # If +1 to all stats
                        with_bonus += 1
                    elif self.BonusButton1.GetValue():
                        if self.Plus2Ctrl.GetString(self.Plus2Ctrl.GetSelection()) == attr_names[i]:
                            # If +2 control matches current ability score
                            with_bonus += 2
                        if self.Plus1Ctrl.GetString(self.Plus1Ctrl.GetSelection()) == attr_names[i]:
                            # If +1 control matches current ability score
                            with_bonus += 1
                    self.BonusSpinList[i].SetValue(str(with_bonus))
                else:
                    self.BonusSpinList[i].SetValue("")

                current_point_list = self.get_point_list()
                cur_cost = current_point_list[val]
                dec_cost = current_point_list[val - 1]
                inc_cost = current_point_list[val + 1]
                total += cur_cost
                
                self.CurSpinList[i].SetValue("{}".format(cur_cost))
                
                if dec_cost == "":
                    temp = '--'
                else:
                    temp = "{:+} ({})".format(dec_cost - cur_cost, dec_cost)
                self.DecSpinList[i].SetValue(temp)
                
                if inc_cost == "":
                    temp = '--'
                else:
                    temp = "{:+} ({})".format(inc_cost - cur_cost, inc_cost)
                self.IncSpinList[i].SetValue(temp)
                    
            self.TotalCtrl.SetValue(str(total))
        except TypeError:
            pass

    def on_bonus_select(self, event):
        if event and event.GetEventObject() in [self.Plus2Ctrl, self.Plus1Ctrl]:
            self.BonusButton1.SetValue(True)
        # Save the +1 bonus choice for later.
        plus2_string = self.Plus2Ctrl.GetString(self.Plus2Ctrl.GetSelection())
        plus1_string = self.Plus1Ctrl.GetString(self.Plus1Ctrl.GetSelection())
        plus1_items = attr_names[:]
        plus1_items.remove(plus2_string)
        self.Plus1Ctrl.SetItems(plus1_items)
        # If +2 hasn't already chosen that option, reselect the choice for +1
        if plus1_string and not plus2_string == plus1_string:
            self.Plus1Ctrl.SetSelection(plus1_items.index(plus1_string))
        self.recalc_points(None)

if __name__ == "__main__":
    app = wx.App(redirect=False)
    MyFrame().Show()
    app.MainLoop()
