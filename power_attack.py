#!/usr/bin/python
# -*- coding: UTF-8 -*-

# Python built-in modules
import time, threading, sys, os, math, re
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
TITLE = "Pathfinder Power Attack Calculator v"+VERSION
AC_COLUMNS = 11

class MyFrame(wx.Frame):
    
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
#        self.SetMinSize((340, 228))
        self.SetSize(wx.Size(550, 575))

        p = wx.Panel(self)
        
        self.BABDropdown = wx.ComboBox(p, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.BABDropdown.AppendItems(["{0:+}".format(i) for i in xrange(1,21)])
        self.BABDropdown.SetSelection(0)
        self.BABDropdown.Bind(wx.EVT_COMBOBOX, self.BuildTable)
        self.BABDropdown.Bind(wx.EVT_COMBOBOX, self.SetActionUsable)
        
#        self.AddModDropdown = wx.ComboBox(p, style=wx.CB_DROPDOWN | wx.CB_READONLY)
#        self.AddModDropdown.AppendItems(["{0:+}".format(i) for i in xrange(-20,41)])
#        self.AddModDropdown.SetSelection(20)
#        self.AddModDropdown.Bind(wx.EVT_COMBOBOX, self.BuildTable)

        self.StrengthScoreCtrl = wx.TextCtrl(p, value="10", size=(80,-1))
        self.StrengthScoreCtrl.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.StrengthScoreCtrl.Bind(wx.EVT_TEXT, self.ParseStrMod)
        self.StrengthModCtrl = wx.TextCtrl(p, value="0", size=(40,-1), style=wx.TE_READONLY)
        self.StrengthModCtrl.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.StrengthModCtrl.Bind(wx.EVT_TEXT, self.BuildTable)

        self.AddModCtrl = wx.TextCtrl(p, value="0", size=(80,-1))
        self.AddModCtrl.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.AddModCtrl.Bind(wx.EVT_TEXT, self.ParseAvgHitMod)
        self.AvgAddModCtrl = wx.TextCtrl(p, value="0", size=(40,-1), style=wx.TE_READONLY)
        self.AvgAddModCtrl.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.AvgAddModCtrl.Bind(wx.EVT_TEXT, self.BuildTable)
        
        self.ActionDropdown = wx.ComboBox(p, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.ActionDropdown.AppendItems(["Single Attack","Full Attack"])
        self.ActionDropdown.SetSelection(1)
        self.ActionDropdown.Bind(wx.EVT_COMBOBOX, self.BuildTable)
        self.ActionDropdown.Disable()
        
        self.ExtraAttacksCtrl = wx.SpinCtrl(p, value="0", max=100, size=(50,-1))
        self.ExtraAttacksCtrl.Bind(wx.EVT_TEXT, self.BuildTable)
        
        self.WeaponDmgCtrl = wx.TextCtrl(p, value="1d6+1", size=(80,-1))
        self.WeaponDmgCtrl.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.WeaponDmgCtrl.Bind(wx.EVT_TEXT, self.ParseAvgWeaponDmg)
        self.AvgWeaponDmgCtrl = wx.TextCtrl(p, value="", size=(40,-1))
        self.AvgWeaponDmgCtrl.SetValue("0")
        self.AvgWeaponDmgCtrl.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.AvgWeaponDmgCtrl.Bind(wx.EVT_TEXT, self.BuildTable)
        
        self.AddDmgCtrl = wx.TextCtrl(p, value="", size=(80,-1))
        self.AddDmgCtrl.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.AddDmgCtrl.Bind(wx.EVT_TEXT, self.ParseAvgAddDmg)
        self.AvgAddDmgCtrl = wx.TextCtrl(p, value="", size=(40,-1))
        self.AvgAddDmgCtrl.SetValue("0")
        self.AvgAddDmgCtrl.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.AvgAddDmgCtrl.Bind(wx.EVT_TEXT, self.BuildTable)
        
        self.DmgMultDropdown = wx.ComboBox(p, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.DmgMultDropdown.AppendItems(["x{0}".format(i) for i in xrange(1,7)])
        self.DmgMultDropdown.SetSelection(0)
        self.DmgMultDropdown.Bind(wx.EVT_TEXT, self.BuildTable)
        
        self.CritRangeDropdown = wx.ComboBox(p, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        L = ["{0}-20".format(i) for i in range(11,20)]
        L.reverse()
        self.CritRangeDropdown.AppendItems(["20"]+L)
        self.CritRangeDropdown.SetSelection(0)
        self.CritRangeDropdown.Bind(wx.EVT_TEXT, self.BuildTable)
#        self.CritRangeDropdown.Disable()
        
        self.CritMultDropdown = wx.ComboBox(p, style=wx.CB_DROPDOWN | wx.CB_READONLY)
        self.CritMultDropdown.AppendItems(["x{0}".format(i) for i in xrange(2,5)])
        self.CritMultDropdown.SetSelection(0)
        self.CritMultDropdown.Bind(wx.EVT_TEXT, self.BuildTable)
#        self.CritMultDropdown.Disable()
        
        self.ExtraCritDmgCtrl = wx.TextCtrl(p, value="", size=(80,-1))
        self.ExtraCritDmgCtrl.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.ExtraCritDmgCtrl.Bind(wx.EVT_TEXT, self.ParseAvgCritDmg)
        self.AvgExtraCritDmgCtrl = wx.TextCtrl(p, value="", size=(40,-1))
        self.AvgExtraCritDmgCtrl.SetValue("0")
        self.AvgExtraCritDmgCtrl.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.AvgExtraCritDmgCtrl.Bind(wx.EVT_TEXT, self.BuildTable)
        
        self.CritConfBonusCtrl = wx.TextCtrl(p, value="", size=(80,-1))
        self.CritConfBonusCtrl.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.CritConfBonusCtrl.Bind(wx.EVT_TEXT, self.ParseAvgCritConfBonus)
        self.AvgCritConfBonusCtrl = wx.TextCtrl(p, value="", size=(40,-1))
        self.AvgCritConfBonusCtrl.SetValue("0")
        self.AvgCritConfBonusCtrl.Bind(wx.EVT_SET_FOCUS, self.OnGainFocusTB)
        self.AvgCritConfBonusCtrl.Bind(wx.EVT_TEXT, self.BuildTable)
        
        self.THWRadioButton = wx.RadioButton(p, label="Two-handed Weapon/Only natural attack", style=wx.RB_GROUP)
        self.OffHandRadioButton = wx.RadioButton(p, label="Off-hand weapon/Secondary natural attack")
        self.NormalWeapRadioButton = wx.RadioButton(p, label="Neither")
        self.THWRadioButton.Bind(wx.EVT_RADIOBUTTON, self.BuildTable)
        self.OffHandRadioButton.Bind(wx.EVT_RADIOBUTTON, self.BuildTable)
        self.NormalWeapRadioButton.Bind(wx.EVT_RADIOBUTTON, self.BuildTable)
        self.NormalWeapRadioButton.SetValue(True)
        
        self.FuriousFocusCheckbox = wx.CheckBox(p)
        self.FuriousFocusCheckbox.Bind(wx.EVT_CHECKBOX, self.BuildTable)
#        self.FuriousFocusCheckbox.Disable()
        
        self.TargetACCtrl = wx.SpinCtrl(p, value="10", min=-100, max=100, size=(50,-1))
        self.TargetACCtrl.Bind(wx.EVT_TEXT, self.BuildTable)
        
        self.TargetDRCtrl = wx.SpinCtrl(p, value="0", min=0, max=100, size=(50,-1))
        self.TargetDRCtrl.Bind(wx.EVT_TEXT, self.BuildTable)
        
        self.ImmuneCritsCheckbox = wx.CheckBox(p)
        self.ImmuneCritsCheckbox.Bind(wx.EVT_CHECKBOX, self.BuildTable)
#        self.ImmuneCritsCheckbox.Disable()
        
        normalFont = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.NORMAL)
        boldFont = wx.Font(10, wx.NORMAL, wx.NORMAL, wx.BOLD)
        self.TargetACList = [wx.StaticText(p, label="X", style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE, size=wx.Size(40,20)) for i in xrange(AC_COLUMNS)]
        for x in self.TargetACList:
            x.SetFont(boldFont)
        self.PANoList = [wx.StaticText(p, label="0", style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE, size=wx.Size(40,20)) for i in xrange(AC_COLUMNS)]
        for x in self.PANoList:
            x.SetBackgroundColour("White")
        self.PAYesList = [wx.StaticText(p, label="0", style=wx.ALIGN_CENTER | wx.ST_NO_AUTORESIZE, size=wx.Size(40,20)) for i in xrange(AC_COLUMNS)]
        for x in self.PAYesList:
            x.SetBackgroundColour("White")

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add Text Box 1 and Com Port Selector 1
        controlsSizer = wx.FlexGridSizer(cols=2)
        
        controlsSizer.Add(wx.StaticText(p, label="Base Attack Bonus:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        controlsSizer.Add(self.BABDropdown, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        controlsSizer.Add(wx.StaticText(p, label="Strength Score:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        hsizer_strmod = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_strmod.Add(self.StrengthScoreCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer_strmod.Add(wx.StaticText(p, label="Avg"), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 30)
        hsizer_strmod.Add(self.StrengthModCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 6)
        controlsSizer.Add(hsizer_strmod, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        controlsSizer.Add(wx.StaticText(p, label="Additional Modifiers:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        hsizer_addmod = wx.BoxSizer(wx.HORIZONTAL)
        hsizer_addmod.Add(self.AddModCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer_addmod.Add(wx.StaticText(p, label="Avg"), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 30)
        hsizer_addmod.Add(self.AvgAddModCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 6)
        controlsSizer.Add(hsizer_addmod, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
#        controlsSizer.Add(self.AddModDropdown, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        controlsSizer.Add(wx.StaticText(p, label="Action:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        controlsSizer.Add(self.ActionDropdown, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        controlsSizer.Add(wx.StaticText(p, label="Extra Attacks:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        hsizer0 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer0.Add(self.ExtraAttacksCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer0.Add(wx.StaticText(p, label="(at highest base attack bonus)"), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        controlsSizer.Add(hsizer0, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        controlsSizer.Add(wx.StaticText(p, label="Normal Weapon Dmg:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add(self.WeaponDmgCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer1.Add(wx.StaticText(p, label="Avg"), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 30)
        hsizer1.Add(self.AvgWeaponDmgCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 6)
        controlsSizer.Add(hsizer1, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        controlsSizer.Add(wx.StaticText(p, label="Additional Dmg:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add(self.AddDmgCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer2.Add(wx.StaticText(p, label="Avg"), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 30)
        hsizer2.Add(self.AvgAddDmgCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 6)
        controlsSizer.Add(hsizer2, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        controlsSizer.Add(wx.StaticText(p, label="Damage Multiplier:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        hsizer2_5 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2_5.Add(self.DmgMultDropdown, 0, wx.ALIGN_CENTER_VERTICAL)
        controlsSizer.Add(hsizer2_5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        controlsSizer.Add(wx.StaticText(p, label="Critical:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        hsizer3 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer3.Add(self.CritRangeDropdown, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer3.Add(wx.StaticText(p, label="/"), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT, 6)
        hsizer3.Add(self.CritMultDropdown, 0, wx.ALIGN_CENTER_VERTICAL)
        controlsSizer.Add(hsizer3, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        controlsSizer.Add(wx.StaticText(p, label="Extra Dmg on Crit:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        hsizer4 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer4.Add(self.ExtraCritDmgCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer4.Add(wx.StaticText(p, label="Avg"), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 30)
        hsizer4.Add(self.AvgExtraCritDmgCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 6)
        controlsSizer.Add(hsizer4, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        controlsSizer.Add(wx.StaticText(p, label="Crit Confirmation Bonus:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        hsizer5 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer5.Add(self.CritConfBonusCtrl, 0, wx.ALIGN_CENTER_VERTICAL)
        hsizer5.Add(wx.StaticText(p, label="Avg"), 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 30)
        hsizer5.Add(self.AvgCritConfBonusCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 6)
        controlsSizer.Add(hsizer5, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        controlsSizer.Add(wx.StaticText(p, label="Type of attack?"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        controlsSizer.Add(self.THWRadioButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        controlsSizer.Add(wx.StaticText(p, label=""), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        controlsSizer.Add(self.OffHandRadioButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        controlsSizer.Add(wx.StaticText(p, label=""), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        controlsSizer.Add(self.NormalWeapRadioButton, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        controlsSizer.Add(wx.StaticText(p, label="Furious Focus?"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        controlsSizer.Add(self.FuriousFocusCheckbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        controlsSizer.Add(wx.StaticText(p, label="Target AC:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        controlsSizer.Add(self.TargetACCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        controlsSizer.Add(wx.StaticText(p, label="Target DR:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        controlsSizer.Add(self.TargetDRCtrl, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        controlsSizer.Add(wx.StaticText(p, label="Immune to Crits?"), 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 3)
        controlsSizer.Add(self.ImmuneCritsCheckbox, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT | wx.ALL, 3)
        
        sizer.Add(controlsSizer, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        
        tableSizer = wx.GridBagSizer(0,0)
        tableSizer.Add(wx.StaticText(p, label="Power Attack"), (0,0), flag=wx.ALIGN_CENTER)
        tableSizer.Add(wx.StaticText(p, label="Target AC"), (0,1), (1,11), flag=wx.ALIGN_CENTER)
        for i,t in enumerate(self.TargetACList):
            tableSizer.Add(t, (1,i+1), flag=wx.ALIGN_CENTER)
        tableSizer.Add(wx.StaticText(p, label="No"), (2,0), flag=wx.ALIGN_CENTER)
        for i,t in enumerate(self.PANoList):
            tableSizer.Add(t, (2,i+1), flag=wx.ALIGN_CENTER)
        tableSizer.Add(wx.StaticText(p, label="Yes"), (3,0), flag=wx.ALIGN_CENTER)
        for i,t in enumerate(self.PAYesList):
            tableSizer.Add(t, (3,i+1), flag=wx.ALIGN_CENTER)
        
        sizer.Add(tableSizer, 0, wx.ALIGN_CENTER | wx.ALL, 3)
        
        p.SetSizerAndFit(sizer)
        p.SetAutoLayout(1)
        sizer.Fit(p)
        self.Center()
        
        self.InitControls()

    def InitControls(self):
        self.ParseAvgWeaponDmg(None)
        self.ParseAvgAddDmg(None)
        self.ParseAvgCritDmg(None)
        self.SetActionUsable(None)
    
    def ParseStrMod(self, event):
        try:
            str_mod = int((self.ParseAvgDmg(self.StrengthScoreCtrl.GetValue())-10)/2)
        except Exception:
            pass
        else:
            self.StrengthModCtrl.SetValue(str(str_mod))
    
    def ParseAvgHitMod(self, event):
        avg = self.ParseAvgDmg(self.AddModCtrl.GetValue())
        if not avg == None:
            self.AvgAddModCtrl.SetValue(str(avg))
    
    def ParseAvgWeaponDmg(self, event):
        avg = self.ParseAvgDmg(self.WeaponDmgCtrl.GetValue())
        if not avg == None:
            self.AvgWeaponDmgCtrl.SetValue(str(avg))
    
    def ParseAvgAddDmg(self, event):
        avg = self.ParseAvgDmg(self.AddDmgCtrl.GetValue())
        if not avg == None:
            self.AvgAddDmgCtrl.SetValue(str(avg))
    
    def ParseAvgCritDmg(self, event):
        avg = self.ParseAvgDmg(self.ExtraCritDmgCtrl.GetValue())
        if not avg == None:
            self.AvgExtraCritDmgCtrl.SetValue(str(avg))
            
    def ParseAvgCritConfBonus(self, event):
        avg = self.ParseAvgDmg(self.CritConfBonusCtrl.GetValue())
        if not avg == None:
            self.AvgCritConfBonusCtrl.SetValue(str(avg))
    
    def ParseAvgDmg(self, s):
        if s == "":
            return 0
        regex = r"(\d*d\d+)" # Matches "d8", "12d6", "1d20", etc
        m = re.findall(regex, s)
        for x in set(m):
            s = s.replace(x,str(self.CalcDiceAvg(x)))
        return self.safe_eval(s)
    
    def CalcDiceAvg(self, s):
        n,p,d = s.partition('d')
        try:
            if n == "": n = 1
            n = int(n)
            d = int(d)
        except ValueError:
            return 0
        return ((d+1)/2.0)*n 
    
    def safe_eval(self, func):
        try:
            return eval(func,{"__builtins__":None},{})
        except (SyntaxError, NameError):
            return None

    def SetActionUsable(self, event):
        if self.BABDropdown.GetSelection() < 5:  # +6
            self.ActionDropdown.SetSelection(0)  # Set action to Single Attack and disable
            self.ActionDropdown.Disable()
        elif not self.ActionDropdown.IsEnabled():
            self.ActionDropdown.Enable()         # Set action to Full Attack and enable
            self.ActionDropdown.SetSelection(1)
        self.BuildTable(event)

    def BuildTable(self,event):
        try:
            target_ac = int(self.TargetACCtrl.GetValue())
            str_mod = int(self.StrengthModCtrl.GetValue())
            str_dmg = str_mod
            hit_mod = int(self.AvgAddModCtrl.GetValue())
            extra_hits = int(self.ExtraAttacksCtrl.GetValue())
            weap = self.AvgWeaponDmgCtrl.GetValue()
            weap = float(weap) if weap else 0
            add_dmg = self.AvgAddDmgCtrl.GetValue()
            add_dmg = float(add_dmg) if add_dmg else 0
            extra_crit_dmg = self.AvgExtraCritDmgCtrl.GetValue()
            extra_crit_dmg = float(extra_crit_dmg) if extra_crit_dmg else 0
            crit_conf_bonus = int(self.AvgCritConfBonusCtrl.GetValue())
            target_dr = int(self.TargetDRCtrl.GetValue())
        except ValueError:  # If one of the fields isn't a number, don't parse and calc
            return
        else:
            if not self.THWRadioButton.GetValue():
                self.FuriousFocusCheckbox.SetValue(False)
                self.FuriousFocusCheckbox.Disable()
            else:
                self.FuriousFocusCheckbox.Enable()
                
            bab = self.BABDropdown.GetSelection()+1
            hit_penalty = int(bab/4)+1
            dmg_bonus = hit_penalty*2
            furious_focus_mod = hit_penalty if self.FuriousFocusCheckbox.GetValue() else 0
            full_attack = (self.ActionDropdown.GetSelection() == 1)
            dmg_mult = self.DmgMultDropdown.GetSelection()+1
            crit_range = (20-self.CritRangeDropdown.GetSelection())
            crit_mult = self.CritMultDropdown.GetSelection()+2
            if self.THWRadioButton.GetValue():
                dmg_bonus = int(dmg_bonus*1.5)
                str_dmg = int(str_dmg*1.5)
            elif self.OffHandRadioButton.GetValue():
                dmg_bonus = int(dmg_bonus*0.5)
                str_dmg = int(str_dmg*0.5)
            can_crit = not self.ImmuneCritsCheckbox.GetValue()
            
            # Perform a calculation of average damage for each visible AC value
            # Do two calculations, with Power Attack and without Power Attack
            for i,x in enumerate(self.TargetACList):
                ac = target_ac-int(len(self.TargetACList)/2)+i
                x.SetLabel(str(ac))
                
                # Create a list of average damage results without power attack
                no_dmg_list = self.CalcAvgDmg(bab, hit_mod+str_mod, ac, weap+str_dmg, add_dmg, dmg_mult, crit_range, crit_mult, 
                                              can_crit, extra_crit_dmg, crit_conf_bonus, target_dr, 0, extra_hits, full_attack)
                # Sum all the damage
                no_dmg = sum(no_dmg_list)
                # Set result for the given AC
                self.PANoList[i].SetLabel("{0:.2f}".format(no_dmg))
                
                # Create a list of average damage results with power attack
                yes_dmg_list = self.CalcAvgDmg(bab, hit_mod+str_mod-hit_penalty, ac, weap+str_dmg+dmg_bonus, add_dmg, dmg_mult, crit_range, crit_mult, 
                                               can_crit, extra_crit_dmg, crit_conf_bonus, target_dr, furious_focus_mod, extra_hits, full_attack)
                # Sum all the damage
                yes_dmg = sum(yes_dmg_list)
                # Set result for the given AC
                self.PAYesList[i].SetLabel("{0:.2f}".format(yes_dmg))
                
                # Highlight the greater result in light blue, and the lesser result in white
                if yes_dmg > no_dmg:
                    self.PANoList[i].SetBackgroundColour("White")
                    self.PAYesList[i].SetBackgroundColour("Light Blue")
                else:
                    self.PANoList[i].SetBackgroundColour("Light Blue")
                    self.PAYesList[i].SetBackgroundColour("White")
            
            if DEBUG:
                print ""
                print bab+hit_mod+str_mod
                print no_dmg_list
                print yes_dmg_list
            
            self.Refresh()
        
    def CalcHitProb(self, tohit, ac):
        temp = min(20,max(1,ac-tohit-1))
        return 1-(temp/20.0)

    def CalcAvgDmg(self, bab, hit_mod, ac, dmg, add_dmg=0, dmg_mult=1, crit_range=20, crit_mult=2, can_crit=True, extra_crit_dmg=0, 
                   crit_conf_bonus=0, dr=0, furious_focus_mod=0, extra_hits=0, full_attack=True):
        if DEBUG: print bab,hit_mod,dmg,add_dmg,dmg_mult
        # Calculate the probability of hitting, given the AC of the target, and the BAB and hit mod of the attacker
        hit_prob = self.CalcHitProb(bab+hit_mod+furious_focus_mod, ac)
        if DEBUG: print "Hit prob:",hit_prob
        # Total damage is the average weapon damage times damage mult, plus additional
        total_dmg = (dmg)*dmg_mult+add_dmg
        # Multiply total damage by the hit probability to get the average damage 
        avg_dmg = hit_prob*total_dmg
        if DEBUG: print "Avg dmg:",avg_dmg
        if can_crit:
            # Calculate the chance of a crit threat. If the hit probability is lower, use that instead
            # i.e. Rolling an 18 with a rapier when you need a 19 to normally hit is still a miss
            # Only a natural 20 is a guaranteed hit
            crit_chance = min(hit_prob,(21-crit_range)/20.0)
            # Calculate the crit confirmation chance. This is the same as the hit chance, except
            # with possibly crit confirmation bonuses 
            crit_hit_prob = self.CalcHitProb(bab+hit_mod+furious_focus_mod+crit_conf_bonus, ac)
            # Find the additional damage added by a crit (x2 crit means adding 1*average damage)
            # Add extra crit damage as well
            crit_dmg = (crit_mult-1)*avg_dmg+extra_crit_dmg
            # Find average crit damage by multiplying by crit chance and crit confirmation chance
            avg_crit_dmg = crit_hit_prob*crit_chance*crit_dmg
        else:
            # If the attack can't crit, just set average crit damage to 0
            avg_crit_dmg = 0
        if DEBUG: print "Crit dmg:",avg_crit_dmg
        # Start a new damage list for this attack
        avg_dmg_list = [max(avg_dmg+avg_crit_dmg-dr,0)]
        if DEBUG: print "Dmg:",avg_dmg_list 
        # Call this function again recursively, and add further results to the damage list
        if extra_hits > 0:
            # If the attacker gets extra hits (like from Haste) perform the calculations again without reducing BAB.
            # However, any bonus added by furious focus goes away for any further attacks.
            avg_dmg_list += self.CalcAvgDmg(bab, hit_mod, ac, dmg, add_dmg, dmg_mult, crit_range, crit_mult, can_crit, extra_crit_dmg, 
                                            crit_conf_bonus, dr, 0, extra_hits-1, full_attack)
        elif full_attack:
            # If full attacking and the BAB is still greater than 5, more attacks can be made.
            # Reduce BAB by 5 and perform the calculations again.
            if bab > 5:
                avg_dmg_list += self.CalcAvgDmg(bab-5, hit_mod, ac, dmg, add_dmg, dmg_mult, crit_range, crit_mult, can_crit, extra_crit_dmg,
                                                crit_conf_bonus, dr)
        # Return damage list, to either be appended to other lists or returned to the main function to be averaged
        return avg_dmg_list

    def ErrorDialog(self, e):
        dial = wx.MessageDialog(None, e, 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
    
    def OnGainFocusTB(self, event):
        wx.CallAfter(event.GetEventObject().SelectAll)
    
    def OnClose(self, event):
        self.Destroy()

if __name__ == "__main__":
    app = wx.App(redirect=False)
    MyFrame().Show()
    app.MainLoop()
