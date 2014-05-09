#!/usr/bin/env python
# -*- coding: cp1252 -*-

"""
PolyEditor: a simple app for editing polygons

Used as a demo for FloatCanvas
"""
import numpy as N
import random
from math import pi, cos, sin
import numpy.random as RandomArray

## from wx.lib.floatcanvas import NavCanvas, FloatCanvas

# import a local copy:
import sys
sys.path.append("..")
from wx.lib.floatcanvas import NavCanvas, FloatCanvas

import wx

ID_ABOUT_MENU = wx.ID_ABOUT
ID_ZOOM_TO_FIT_MENU = wx.NewId()

class DrawFrame(wx.Frame):

    """
    A frame used for the FloatCanvas Demo

    """

    def __init__(self,parent, id,title,position,size):
        wx.Frame.__init__(self,parent, id,title,position, size)

        ## Set up the MenuBar
        MenuBar = wx.MenuBar()

        FileMenu = wx.Menu()
        FileMenu.Append(wx.NewId(), "&Close","Close Application")
        wx.EVT_MENU(self, FileMenu.FindItem("Close"), self.OnQuit)

        MenuBar.Append(FileMenu, "&File")

        view_menu = wx.Menu()
        view_menu.Append(wx.NewId(), "Zoom to &Fit","Zoom to fit the window")
        wx.EVT_MENU(self, view_menu.FindItem("Zoom to &Fit"), self.ZoomToFit)
        MenuBar.Append(view_menu, "&View")

        help_menu = wx.Menu()
        help_menu.Append(ID_ABOUT_MENU, "&About",
                                "More information About this program")
        wx.EVT_MENU(self, ID_ABOUT_MENU,      self.OnAbout)
        MenuBar.Append(help_menu, "&Help")

        self.SetMenuBar(MenuBar)

        self.CreateStatusBar()            
        # Add the Canvas
        self.Canvas = NavCanvas.NavCanvas(self,-1,(500,500),
                                          Debug = 0,
                                          BackgroundColor = "DARK SLATE BLUE"
                                          ).Canvas

        wx.EVT_CLOSE(self, self.OnCloseWindow)

        FloatCanvas.EVT_MOTION(self.Canvas, self.OnMove ) 
        FloatCanvas.EVT_LEFT_UP(self.Canvas, self.OnLeftUp ) 
        FloatCanvas.EVT_LEFT_DOWN(self.Canvas, self.OnLeftClick ) 

        self.ResetSelections()

        return None

    def ResetSelections(self):
        self.SelectedPoly = None
        self.SelectedPolyOrig = None
        self.SelectedPoints = None
        self.PointSelected = False
        self.SelectedPointNeighbors = None

    def OnAbout(self, event):
        dlg = wx.MessageDialog(self, "This is a small program to demonstrate\n"
                                                  "the use of the FloatCanvas\n",
                                                  "About Me", wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def ZoomToFit(self,event):
        self.Canvas.ZoomToBB()

    def Clear(self,event = None):
        self.Canvas.ClearAll()
        self.Canvas.SetProjectionFun(None)
        self.Canvas.Draw()

    def OnQuit(self,event):
        self.Close(True)

    def OnCloseWindow(self, event):
        self.Destroy()

    def OnMove(self, event):
        """
        Updates the status bar with the world coordinates

        And moves a point if there is one selected

        """
        self.SetStatusText("%.2f, %.2f"%tuple(event.Coords))

        if self.PointSelected:
            PolyPoints = self.SelectedPoly.Points
            Index = self.SelectedPoints.Index
            dc = wx.ClientDC(self.Canvas)
            PixelCoords = event.GetPosition()
            dc.SetPen(wx.Pen('WHITE', 2, wx.SHORT_DASH))
            dc.SetLogicalFunction(wx.XOR)
            if self.SelectedPointNeighbors is None:
                self.SelectedPointNeighbors = N.zeros((3,2), N.float_)
                #fixme: This feels very inelegant!
                if Index == 0:
                    self.SelectedPointNeighbors[0] = self.SelectedPoly.Points[-1]
                    self.SelectedPointNeighbors[1:3] = self.SelectedPoly.Points[:2]
                elif Index == len(self.SelectedPoly.Points)-1:
                    self.SelectedPointNeighbors[0:2] = self.SelectedPoly.Points[-2:]
                    self.SelectedPointNeighbors[2] = self.SelectedPoly.Points[0]
                else:
                    self.SelectedPointNeighbors = self.SelectedPoly.Points[Index-1:Index+2]
                self.SelectedPointNeighbors = self.Canvas.WorldToPixel(self.SelectedPointNeighbors)
            else:
                    dc.DrawLines(self.SelectedPointNeighbors)
            self.SelectedPointNeighbors[1] = PixelCoords
            dc.DrawLines(self.SelectedPointNeighbors)


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

    def Setup(self, event = None):
        "Seting up with some random polygons"
        wx.GetApp().Yield()
        self.ResetSelections()
        self.Canvas.ClearAll()

        Range = (-10,10)

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
        self.ArrangeCircle(self.Canvas, 5)
        p1 = (-2,-2)
        p2 = (-10,-2)
        self.Canvas.AddLine((p1,p2),LineWidth = 3)
        offset = self.GetOffsetLines(p1,p2)
        self.Canvas.AddLine(offset[0])
        self.Canvas.AddLine(offset[1])
        self.Canvas.ZoomToBB()


    def ArrangeCircle(self, canvas, n, d=10):
        if n < 1: return
        
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
           thepos = [startpos[0]*cosPhi - startpos[1]*sinPhi,
                     startpos[0]*sinPhi + startpos[1]*cosPhi]
           
           canvas.AddPoint(thepos,
                           Diameter=20)

    def GetOffsetLines(self, p1, p2, offset=2):
        hyp = ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5
        if not hyp: return (p1,p2),(p1,p2)
        x,y = (p2[1]-p1[1])*(offset/hyp), (p2[0]-p1[0])*(offset/hyp)
        return (([sum(a) for a in zip(p1, (-x,y))], [sum(a) for a in zip(p2, (-x,y))]),
                ([sum(a) for a in zip(p1, (x,-y))], [sum(a) for a in zip(p2, (x,-y))]))
        
    
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
        print "point #%i hit"%PointSet.Index
        #Index = PointSet.Index
        self.PointSelected = True

class PolyEditor(wx.App):
    """

    A simple example of making editable shapes with FloatCanvas

    """

    def OnInit(self):
        wx.InitAllImageHandlers()
        frame = DrawFrame(None,
                          -1,
                          "FloatCanvas Demo App",
                          wx.DefaultPosition,
                          (700,700),
                          )

        self.SetTopWindow(frame)
        frame.Show()

        frame.Setup()
        return True

PolyEditor(0).MainLoop()# put in True if you want output to go to it's own window.

   
    
     
    
    
    


















