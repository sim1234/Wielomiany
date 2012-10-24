#!/usr/bin/python
# coding: utf-8

#       This file is part of X-enon.

#        X-enon is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.

#       X-enon is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.

#       You should have received a copy of the GNU General Public License
#       along with X-enon; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import re, wx
from fp import nm, mnoz, wielomian
from math import *


class GetWDialog(wx.Dialog):
    
    def __init__(self, parent, name="W", wielomiann="0", title=u'Podaj wielomian'):
        super(GetWDialog, self).__init__(parent=parent, title=title, size=(250, 200))
        self.Name = ""
        self.Wielomian = ""
        self.panel = wx.Panel(self, wx.ID_ANY)
        inputTxtZero = wx.TextCtrl(self.panel, wx.ID_ANY, name, size=(18,18))
        self.In0 = inputTxtZero
        labelOne = wx.StaticText(self.panel, wx.ID_ANY, '(x) =')
        inputTxtOne = wx.TextCtrl(self.panel, wx.ID_ANY, wielomiann)
        self.In1 = inputTxtOne
        #inputTxtOne.SetFocus()

        okBtn = wx.Button(self.panel, wx.ID_ANY, u'OK')
        helpmeBtn = wx.Button(self.panel, wx.ID_ANY, u'Pomóż mi wpisać wielomian')
        cancelBtn = wx.Button(self.panel, wx.ID_ANY, u'Anuluj')
        self.Bind(wx.EVT_BUTTON, self.onOK, okBtn)
        self.Bind(wx.EVT_BUTTON, self.onHelpMe, helpmeBtn)
        self.Bind(wx.EVT_BUTTON, self.onCancel, cancelBtn)

        topSizer        = wx.BoxSizer(wx.VERTICAL)
        inputOneSizer   = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer        = wx.BoxSizer(wx.HORIZONTAL)

        inputOneSizer.Add(inputTxtZero, 0, wx.ALL|wx.EXPAND, 0)
        inputOneSizer.Add(labelOne, 0, wx.ALL, 2)
        inputOneSizer.Add(inputTxtOne, 1, wx.ALL|wx.EXPAND, 0)

        btnSizer.Add(okBtn, 0, wx.ALL, 5)
        btnSizer.Add(helpmeBtn, 0, wx.ALL, 5)
        btnSizer.Add(cancelBtn, 0, wx.ALL, 5)
        
        topSizer.Add(inputOneSizer, 0, wx.ALL|wx.EXPAND, 10)
        #topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(btnSizer, 0, wx.ALL|wx.CENTER, 0)

        self.panel.SetSizer(topSizer)
        topSizer.Fit(self)

    def onOK(self, event):
        try:
            mnoz(self.In1.GetValue())
            self.Name = self.In0.GetValue()
            self.Wielomian = self.In1.GetValue()
            self.Close()
        except (ValueError, SyntaxError, NameError):
            m = wx.MessageDialog(self, u"To nie jest poprawny wielomian!", u"Błąd")
            m.ShowModal()
            m.Destroy()
        
    def onCancel(self, event):
        self.Name = ""
        self.Wielomian = ""
        self.Close()
        
    def onHelpMe(self, event):
        s=-1
        while s<0:
            t = wx.TextEntryDialog(self, u"Stopień wielomianu " + self.GetName() + " = ", u"Stopień wielomianu", "0")
            t.ShowModal()
            s = t.GetValue()
            t.Destroy()
            s = s.replace(",", ".")
            try:
                s = float(eval(s))
            except (ValueError, SyntaxError, NameError):
                m = wx.MessageDialog(self, u"To nie jest liczba!", u"Błąd")
                m.ShowModal()
                m.Destroy()
                s = -1
                continue
            if s<0:
                m = wx.MessageDialog(self, u"Stopień wielomianu nie może być ujemny!", u"Błąd")
                m.ShowModal()
                m.Destroy()
            if int(s)!=s:
                m = wx.MessageDialog(self, u"Stopień wielomianu musi być całkowity!", u"Błąd")
                m.ShowModal()
                m.Destroy()
                s = -1
        w = wielomian()
        while s>=0:
            r = ""
            while r == "":
                t = wx.TextEntryDialog(self, u"Współczynnik " + self.GetName() + " przy x^" + str(int(s)) + " = ", u"Współczynnik wielomianu", "0")
                t.ShowModal()
                r = t.GetValue()
                t.Destroy()
                r = r.replace(",", ".")
                try:
                    r = float(eval(r))
                except (ValueError, SyntaxError, NameError):
                    m = wx.MessageDialog(self, u"To nie jest liczba!", u"Błąd")
                    m.ShowModal()
                    m.Destroy()
                    r = ""
            w.wsp.append(r)
            s -= 1
        w.wsp.reverse()
        w.nm()
        self.In1.SetValue(str(w))
        
    def GetName(self):
        return self.Name
    
    def GetWielomian(self):
        return self.Wielomian

class MyNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)#wx.BK_TOP#wx.BK_BOTTOM#wx.BK_LEFT#wx.BK_RIGHT)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
        #self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.OnPageChanging)
 
    def OnPageChanged(self, event):
        old = event.GetOldSelection()
        new = event.GetSelection()
        sel = self.GetSelection()
        #print 'OnPageChanged,  old:%d, new:%d, sel:%d\n' % (old, new, sel)
        event.Skip()

    def Add(self, name, panel=None):
        if panel == None:
            panel = wx.Panel(self, wx.ID_ANY)
        self.AddPage(panel, name)

def sete(s, fn):
    s.Bind(wx.EVT_LEFT_UP, fn)
    c = s.GetChildren()
    for k in c:
        sete(k, fn)

class LWielomian(wx.Panel):
    def __init__(self, parent, name, string):#, fn):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.SetBackgroundColour((230,255,230))
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.c = wx.StaticText(self, -1, name + "(x) = " + string, (0, 0))
        sizer.Add(self.c, 1, wx.ALL, 2)
        self.SetFocusIgnoringChildren()
        self.Bind(wx.EVT_LEFT_DOWN, self.wruchu)
        self.c.Bind(wx.EVT_LEFT_DOWN, self.wruchu)
        bmp = wx.ArtProvider.GetBitmap(wx.ART_FIND, wx.ART_BUTTON, (16, 16))
        self.e = wx.StaticBitmap(self, wx.ID_ANY, bmp, pos=(54,0))
        bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_BUTTON, (16, 16))
        self.x = wx.StaticBitmap(self, wx.ID_ANY, bmp, pos=(54,0))
        self.e.Bind(wx.EVT_LEFT_UP, self.OnEdit)
        #self.x.Bind(wx.EVT_LEFT_UP, self.OnDelete)
        sizer.Add(self.e, 0, wx.ALIGN_RIGHT, 0)
        sizer.Add(self.x, 0, wx.ALIGN_RIGHT, 0)
        self.SetSizer(sizer)
        self.n = name
        self.w = string

    def wruchu(self, e):
        tdo = wx.PyTextDataObject(str(self.n)+";"+str(self.w))
        tds = wx.DropSource(self)
        tds.SetData(tdo)
        tds.DoDragDrop(True)
        #self.fn(self.w)
        e.Skip()

    def OnEdit(self, e):
        g = GetWDialog(self, self.n, self.w, "Edycja wielomianu")
        g.ShowModal()
        if g.GetName() != "" and str(g.GetWielomian()) != "":
            self.n = g.GetName()
            self.w = str(g.GetWielomian())
            self.c.SetLabel(self.n + "(x) = " + self.w)
        g.Destroy()
        self.GetParent().Layout()

class DropTarget(wx.TextDropTarget):
    def __init__(self, fn):
        wx.TextDropTarget.__init__(self)
        #self.obj = obj
        self.fn = fn

    def OnDropText(self, x, y, data):
        d = data.split(";")  
        self.fn(d[0], d[1])

class DropWTarget(wx.Panel):
    def __init__(self, parent, pos, color, fn, dropa = 1,size=(100,32)):
        wx.Panel.__init__(self, parent, wx.ID_ANY, pos=pos, size=size)
        self.fn = fn
        self.SetBackgroundColour(color)
        self.n = wx.StaticText(self, wx.ID_ANY, "", (0,0))
        self.w = wx.StaticText(self, wx.ID_ANY, "", (0,16))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.n, 0, wx.EXPAND, 2)
        sizer.Add(self.w, 0, wx.EXPAND, 2)
        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.Add(sizer, 1, wx.ALIGN_LEFT, 0)
        if dropa:
            bmp = wx.ArtProvider.GetBitmap(wx.ART_DELETE, wx.ART_BUTTON, (16, 16))
            self.x = wx.StaticBitmap(self, wx.ID_ANY, bmp, pos=(84,0))
            self.x.Bind(wx.EVT_LEFT_UP, self.OnClear)
            sizer2.Add(self.x, 0, wx.ALIGN_RIGHT, 0)
            self.dt = DropTarget(self.OnDrop)
            self.SetDropTarget(self.dt)
        #self.x = wx.Button(self,wx.ID_ANY,"X",pos=(82,0), size=(18,20))
        #self.x.Bind(wx.EVT_BUTTON, self.OnClear)
        self.SetSizer(sizer2)
        self.SetFocusIgnoringChildren()
        self.Bind(wx.EVT_LEFT_DOWN, self.wruchu)
        self.n.Bind(wx.EVT_LEFT_DOWN, self.wruchu)
        self.w.Bind(wx.EVT_LEFT_DOWN, self.wruchu)
        
    def OnDrop(self, n, w, force=1):
        self.n.SetLabel(n + "(x)")
        self.w.SetLabel(w)
        if force:
            self.fn()

    def OnClear(self, e, force=1):
        self.n.SetLabel("")
        self.w.SetLabel("")
        if force:
            self.fn()
            e.Skip()

    def wruchu(self, e):
        tdo = wx.PyTextDataObject(self.GetName()[0:-3]+";"+self.GetWielomian())
        tds = wx.DropSource(self)
        tds.SetData(tdo)
        tds.DoDragDrop(True)
        self.n.SetLabel("")
        self.w.SetLabel("")
        self.fn()
        e.Skip()

    def GetName(self):
        return self.n.GetLabel()
    
    def GetWielomian(self):
        return self.w.GetLabel()

    def GetColor(self):
        return self.GetBackgroundColour()
        
class MyWykres(wx.Panel):
    def __init__(self, parent, pos, size):
        wx.Panel.__init__(self, parent, wx.ID_ANY, pos=pos, size=size)
        self.dc = None
        self.bl1 = {}
        self.bl2 = {}
        self.lista = {}
        self.ssx = 0
        self.ssy = 0
        self.sx = 10
        self.sy = 10
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        #self.SetWykresy({})
        
    def OnPaint(self, event):
        self.dc = wx.PaintDC(self)
        self.dc.SetBackground(wx.Brush((255,255,255))) 
        self.Update()
        event.Skip()
        
    def Update(self, force=0):
        if self.dc:
            sizex = self.GetSize()[0]
            sizey = self.GetSize()[1]
            if self.bl1 != self.bl2 or self.ssx != self.GetSize()[0] or self.ssy != self.GetSize()[1] or force:
                self.ssx = sizex
                self.ssy = sizey
                self.SetWykresy(self.bl1)
            self.Rysuj()
            
    def Rysuj(self):
            sizex = self.GetSize()[0]
            sizey = self.GetSize()[1]
            self.dc.Clear()
            self.dc.SetPen(wx.Pen((0,0,0), 1))
            #self.dc.DrawLine(0, 0, 300, 200)
            self.dc.DrawLine(0, sizey/2, sizex, sizey/2) #x
            self.dc.DrawLine(sizex-10, sizey/2-10, sizex, sizey/2)
            self.dc.DrawLine(sizex, sizey/2, sizex-10, sizey/2+10)
            for y in range(0, sizey/20+1):
                if y%5==0:
                    self.dc.DrawLine(sizex/2-5, sizey/2-y*10, sizex/2+5, sizey/2-y*10)
                    self.dc.DrawLine(sizex/2-5, sizey/2+y*10, sizex/2+5, sizey/2+y*10)
                else:
                    self.dc.DrawLine(sizex/2-2, sizey/2-y*10, sizex/2+2, sizey/2-y*10)
                    self.dc.DrawLine(sizex/2-2, y*10+sizey/2, sizex/2+2, y*10+sizey/2)
            for x in range(0, sizex/20+1):
                if x%5==0:
                    self.dc.DrawLine(sizex/2-x*10, sizey/2-5, sizex/2-x*10, sizey/2+5)
                    self.dc.DrawLine(sizex/2+x*10, sizey/2-5, sizex/2+x*10, sizey/2+5)
                else:
                    self.dc.DrawLine(sizex/2-x*10, sizey/2-2, sizex/2-x*10, sizey/2+2)
                    self.dc.DrawLine(sizex/2+x*10, sizey/2-2, sizex/2+x*10, sizey/2+2)
            self.dc.DrawLine(sizex/2, 0, sizex/2, sizey) #y
            self.dc.DrawLine(sizex/2-10, 10, sizex/2, 0)
            self.dc.DrawLine(sizex/2, 0, sizex/2+10,10)
            self.dc.DrawLabel("X", (sizex-20,sizey/2-12,8,8))
            self.dc.DrawLabel("Y", (sizex/2+1,10,8,8))
            self.dc.DrawLabel("0", (sizex/2+6,sizey/2-16,8,8))
            self.dc.DrawLabel(str(nm(self.sx/2.0)), (sizex/2+46,sizey/2-19,8,8))
            self.dc.DrawLabel(str(nm(self.sy/2.0)), (sizex/2+6,sizey/2-56,8,8))
        
            for k in self.lista:
                self.dc.SetPen(wx.Pen(k[0], 2))
                self.dc.DrawLines(k[1])
        
    def SetWykresy(self, lista):
            self.lista = []
            self.bl2 = self.bl1
            self.bl1 = lista.copy()
            sizex = self.GetSize()[0]
            sizey = self.GetSize()[1]
            for k in lista:
                l = (k, [])
            
                for x in range(0,sizex+1):
                    try:
                        r = int(lista[k]((x-sizex/2)/float(100.0/self.sx))*-1*(100.0/self.sy))+sizey/2
                        if r >= 0:
                            l[1].append((x, min(r, 100000)))
                        else:
                            l[1].append((x, max(r, -100000)))
                    except (ZeroDivisionError, ValueError):
                        if l[1]!=[]:
                            self.lista.append(l)
                        l = (k, [])
                        
                if l[1]!=[]:
                            self.lista.append(l)
            self.Update()
    

class WykresPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.d1 = DropWTarget(self, (5,5), (255,200,200), self.OnChange)
        self.d2 = DropWTarget(self, (110,5), (200,255,200), self.OnChange)
        self.d3 = DropWTarget(self, (215,5), (200,200,255), self.OnChange)
        self.d4 = DropWTarget(self, (5,40), (255,255,200), self.OnChange)
        self.d5 = wx.TextCtrl(self, wx.ID_ANY, "")# DropWTarget(self, (110,40), (200,255,255), self.OnChange)
        self.d5.SetBackgroundColour((200,255,255))
        self.Bind(wx.EVT_TEXT, self.OnChange, self.d5)
        self.d6 = wx.TextCtrl(self, wx.ID_ANY, "")# DropWTarget(self, (215,40), (255,200,255), self.OnChange)
        self.d6.SetBackgroundColour((255,200,255))
        self.Bind(wx.EVT_TEXT, self.OnChange, self.d6)
        self.sx = wx.SpinCtrl(self, wx.ID_ANY, "10", min=1, max = 1000, initial = 10, size=(50,-1))
        self.tsx =  wx.StaticText(self, wx.ID_ANY, "Skala OX", (0,0))
        self.sy = wx.SpinCtrl(self, wx.ID_ANY, "10", min=1, max = 1000, initial = 10, size=(50,-1))
        self.tsy =  wx.StaticText(self, wx.ID_ANY, "Skala OY", (0,0))
        self.Bind(wx.EVT_TEXT, self.OnChange, self.sx)
        self.Bind(wx.EVT_TEXT, self.OnChange, self.sy)
        self.wykres = MyWykres(self, (20,75), (300,300))
        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(self.d1, 1, wx.EXPAND|wx.ALL, 2)
        s1.Add(self.d2, 1, wx.EXPAND|wx.ALL, 2)
        s1.Add(self.d3, 1, wx.EXPAND|wx.ALL, 2)
        s1.Add(self.tsx, 0, wx.EXPAND|wx.ALL, 2)
        s1.Add(self.sx, 0, wx.EXPAND|wx.ALL, 2)
        s2 = wx.BoxSizer(wx.HORIZONTAL)
        s2.Add(self.d4, 1, wx.EXPAND|wx.ALL, 2)
        s2.Add(self.d5, 1, wx.EXPAND|wx.ALL, 2)
        s2.Add(self.d6, 1, wx.EXPAND|wx.ALL, 2)
        s2.Add(self.tsy, 0, wx.EXPAND|wx.ALL, 2)
        s2.Add(self.sy, 0, wx.EXPAND|wx.ALL, 2)
        sa = wx.BoxSizer(wx.VERTICAL)
        sa.Add(s1, 0, wx.EXPAND|wx.ALL, 0)
        sa.Add(s2, 0, wx.EXPAND|wx.ALL, 0)
        sa.Add(self.wykres, 1, wx.EXPAND|wx.ALL, 2)
        self.SetSizer(sa)
        self.OnChange()
        
    def OnChange(self, e=""):
        self.wykres.sx = self.sx.GetValue()
        self.wykres.sy = self.sy.GetValue()
        w={}
        if self.d1.GetWielomian() != "":
            w[(255,0,0)] = mnoz(self.d1.GetWielomian())
        if self.d2.GetWielomian() != "":
            w[(0,255,0)] = mnoz(self.d2.GetWielomian())
        if self.d3.GetWielomian() != "":
            w[(0,0,255)] = mnoz(self.d3.GetWielomian())
        if self.d4.GetWielomian() != "":
            w[(255,255,0)] = mnoz(self.d4.GetWielomian())
        if self.d5.GetValue() != "":
            try:
                x = 1
                eval(mnoz(self.d5.GetValue(), 0))
                w[(0,255,255)] = lambda x: eval(mnoz(self.d5.GetValue(), 0))
            except (ValueError, SyntaxError, NameError, ZeroDivisionError, TypeError):
                pass
            try:
                x = 1
                eval(self.d5.GetValue())
                #w[(0,255,255)] = lambda x: eval(self.d5.GetValue())
            except (ValueError, SyntaxError, NameError, ZeroDivisionError, TypeError):
                pass
            
        if self.d6.GetValue() != "":
            try:
                x = 1
                print mnoz(self.d6.GetValue(), 0)
                eval(mnoz(self.d6.GetValue(), 0))
                w[(255,0,255)] = lambda x: eval(mnoz(self.d6.GetValue(), 0))
            except (ValueError, SyntaxError, NameError, ZeroDivisionError, TypeError):
                pass
            try:
                x = 1
                eval(self.d6.GetValue())
                w[(255,0,255)] = lambda x: eval(self.d6.GetValue())
            except (ValueError, SyntaxError, NameError, ZeroDivisionError, TypeError):
                pass
            
        self.wykres.SetWykresy(w)

class WielomianyPanel(wx.Panel):
    def __init__(self, parent, pos=(400,0), size=(200,600), style=wx.SUNKEN_BORDER):
        wx.Panel.__init__(self, parent, wx.ID_ANY, pos=pos, size=size, style=style)
        self.SetBackgroundColour((255,255,255))
        addwBtn = wx.Button(self, wx.ID_ANY, u"Dodaj wielomian")
        self.Bind(wx.EVT_BUTTON, self.onAddW, addwBtn)
        #self.Bind(wx.EVT_MOTION, self.OnUsun2, self.wielony)
        self.dt = DropTarget(self.OnDrop)
        self.SetDropTarget(self.dt)
        Sizer = wx.BoxSizer(wx.VERTICAL)
        Sizer.Add(addwBtn, 0, wx.EXPAND,3)
        self.SetSizer(Sizer)

    def onAddW(self, e):
        g = GetWDialog(self)
        g.ShowModal()
        if g.GetName() != "" and str(g.GetWielomian()) != "":
            self.dodaj(g.GetName(),str(g.GetWielomian()))
        g.Destroy()
        e.Skip()

    def OnDrop(self, n, w):
        c = self.GetChildren()
        r = 1
        for x in c:
            if type(x) == LWielomian:
                if x.n == n and x.w == w:
                    r = 0
        if r:
            self.dodaj(n, w)
        
    def OnDelete(self, e):
        b = e.GetEventObject().GetParent()
        b.Destroy()
        self.Layout()
    
    def dodaj(self, n, w):
        Btn = LWielomian(self, n, w)
        #sb = wx.BoxSizer(wx.HORIZONTAL)
        #sb.Add(Btn, 1, wx.ALL, 0)
        s = self.GetSizer()
        s.Add(Btn, 0, wx.ALL, 3)
        Btn.x.Bind(wx.EVT_LEFT_UP, self.OnDelete)
        self.Layout()

class DzialaniaPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.d1 = DropWTarget(self, (5,5), (200,255,200), self.OnChange)
        self.d2 = DropWTarget(self, (110,5), (200,255,200), self.OnChange)
        self.d3 = DropWTarget(self, (215,5), (200,255,200), self.OnChange, 0)
        self.d4 = DropWTarget(self, (5,40), (255,200,200), self.OnChange)
        self.d5 = DropWTarget(self, (110,40), (255,200,200), self.OnChange)
        self.d6 = DropWTarget(self, (215,40), (255,200,200), self.OnChange, 0)
        self.d7 = DropWTarget(self, (5,80), (200,200,255), self.OnChange)
        self.d8 = DropWTarget(self, (110,80), (200,200,255), self.OnChange)
        self.d9 = DropWTarget(self, (215,80), (200,200,255), self.OnChange, 0)
        self.t1a = wx.StaticText(self, wx.ID_ANY, " + ", (0,0))
        self.t1b = wx.StaticText(self, wx.ID_ANY, " = ", (0,0))
        self.t2a = wx.StaticText(self, wx.ID_ANY, " - ", (0,0))
        self.t2b = wx.StaticText(self, wx.ID_ANY, " = ", (0,0))
        self.t3a = wx.StaticText(self, wx.ID_ANY, " x ", (0,0))
        self.t3b = wx.StaticText(self, wx.ID_ANY, " = ", (0,0))
        s1 = wx.BoxSizer(wx.HORIZONTAL)
        s1.Add(self.d1, 1, wx.EXPAND|wx.ALL, 2)
        s1.Add(self.t1a, 0, wx.EXPAND|wx.ALL, 2)
        s1.Add(self.d2, 1, wx.EXPAND|wx.ALL, 2)
        s1.Add(self.t1b, 0, wx.EXPAND|wx.ALL, 2)
        s1.Add(self.d3, 1, wx.EXPAND|wx.ALL, 2)
        s2 = wx.BoxSizer(wx.HORIZONTAL)
        s2.Add(self.d4, 1, wx.EXPAND|wx.ALL, 2)
        s2.Add(self.t2a, 0, wx.EXPAND|wx.ALL, 2)
        s2.Add(self.d5, 1, wx.EXPAND|wx.ALL, 2)
        s2.Add(self.t2b, 0, wx.EXPAND|wx.ALL, 2)
        s2.Add(self.d6, 1, wx.EXPAND|wx.ALL, 2)
        s3 = wx.BoxSizer(wx.HORIZONTAL)
        s3.Add(self.d7, 1, wx.EXPAND|wx.ALL, 2)
        s3.Add(self.t3a, 0, wx.EXPAND|wx.ALL, 2)
        s3.Add(self.d8, 1, wx.EXPAND|wx.ALL, 2)
        s3.Add(self.t3b, 0, wx.EXPAND|wx.ALL, 2)
        s3.Add(self.d9, 1, wx.EXPAND|wx.ALL, 2)
        sa = wx.BoxSizer(wx.VERTICAL)
        sa.Add(s1, 0, wx.EXPAND|wx.ALL, 0)
        sa.Add(s2, 0, wx.EXPAND|wx.ALL, 0)
        sa.Add(s3, 0, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(sa)
        
    def OnChange(self):
        if self.d1.GetWielomian() == "" or self.d2.GetWielomian() == "":
            self.d3.OnClear(0,0)
        else:
            w = str(mnoz(self.d1.GetWielomian())+mnoz(self.d2.GetWielomian()))
            self.d3.OnDrop(self.d1.GetName()[0:-3] + self.d2.GetName()[0:-3], w ,0)
            
        if self.d4.GetWielomian() == "" or self.d5.GetWielomian() == "":
            self.d6.OnClear(0,0)
        else:
            w = str(mnoz(self.d4.GetWielomian())-mnoz(self.d5.GetValue()))
            self.d6.OnDrop(self.d4.GetName()[0:-3] + self.d5.GetName()[0:-3], w ,0)
            
        if self.d7.GetWielomian() == "" or self.d8.GetWielomian() == "":
            self.d9.OnClear(0,0)
        else:
            w = str(mnoz(self.d7.GetWielomian())*mnoz(self.d8.GetWielomian()))
            self.d9.OnDrop(self.d7.GetName()[0:-3] + self.d8.GetName()[0:-3], w ,0)
           
       



