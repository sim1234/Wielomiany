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

from fp import nm, wielomian, miejscabf, pierwiastkir, mnoz
from fpg import GetWDialog, MyNotebook, sete, LWielomian, DropWTarget, MyWykres, WielomianyPanel, WykresPanel, DzialaniaPanel
import code, wx


##        g = GetWDialog(self)
##        g.ShowModal()
##        if g.GetName() != "" and str(g.GetWielomian()) != "":
##            print g.GetName() + "(x) = " + str(g.GetWielomian())
##        g.Destroy()

class TabPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        txtOne = wx.TextCtrl(self, wx.ID_ANY, "a")
        txtTwo = wx.TextCtrl(self, wx.ID_ANY, "b")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(txtOne, 0, wx.ALL, 5)
        sizer.Add(txtTwo, 0, wx.ALL, 5)
        self.SetSizer(sizer)
        
fun = mnoz("(x-5)(x+5)")



class myframe(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY, title=u'X-enon', size = (600,600))
        self.CreateStatusBar()
        filemenu = wx.Menu()
        menuAbout = filemenu.Append(wx.ID_ABOUT, u"O programie",u" Informacje o tym programie")
        menuExit = filemenu.Append(wx.ID_EXIT,u"Wyjście",u" Wychondzi z programu")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,u"&Plik") 
        self.SetMenuBar(menuBar)
        self.Bind(wx.EVT_MENU, self.onAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.onExit, menuExit)

        self.panel = wx.Panel(self, wx.ID_ANY)
        self.wielony = WielomianyPanel(self, pos=(400,0), size=(200,600), style=wx.SUNKEN_BORDER)
        funkcje = wx.Panel(self, wx.ID_ANY,size=(100,100))
            
        notebook = MyNotebook(funkcje)
        #panel1 = wx.Panel(notebook, wx.ID_ANY)
        #dzialania = DzialaniaPanel
        #tstBtn = wx.Button(panel1, wx.ID_ANY, u"Import", pos=(10,10))
        #self.Bind(wx.EVT_BUTTON, self.ontest, tstBtn)
        
        #f = wx.Panel(panel1, wx.ID_ANY,size=(20,20), pos=(5,20))
        #f.SetBackgroundColour((230,255,230))
        #DropWTarget(panel1, (5,25), (230,255,230), fun)
        #wykres = MyWykres(panel1, (50,50), (300,300))
        #wykres.SetWykresy({(0,0,255):fun})
        notebook.Add(u"Wykres",WykresPanel(notebook))
        #notebook.Add(u"Import",panel1)
        notebook.Add(u"Działania",DzialaniaPanel(notebook))
        nsizer = wx.BoxSizer(wx.VERTICAL)
        nsizer.Add(notebook, 1, wx.ALL|wx.EXPAND, 3)
        funkcje.SetSizer(nsizer)
        
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        topSizer.Add(funkcje, 3, wx.EXPAND,0)
        topSizer.Add(self.wielony, 1, wx.EXPAND,0)
        self.SetSizer(topSizer)
        self.SetAutoLayout(True)
        
    def onAbout(self,e):
        d = wx.MessageDialog(self, u"Program X-enon został stworzony w celach edukacyjnych przez Sim & Ares", u"O programie", wx.OK)
        d.ShowModal()
        d.Destroy()
        e.Skip()

    def onExit(self,e):
        self.Close(True)
        e.Skip()

    def ontest(self, e):
        self.wielony.dodaj("a", "-(x+3)(x-1)(x+3)")
        self.wielony.dodaj("b", "-(x^2)((x-sqrt(2))^2)(x+2)")
        self.wielony.dodaj("c", "((x+2)^2)(x-4)^2")
        self.wielony.dodaj("d", "0.5*(x^3)(x-2)^3")
        self.wielony.dodaj("e", "-0.25*((x-1)^2)(x+3)^4")
        self.wielony.dodaj("f", "(x+4)(x^2-5)")
        self.wielony.dodaj("g", "0.5*(x^3)(x-2)(3-x)^2")
        e.Skip()

 
        

if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = myframe()
    frame.Show()
    app.MainLoop()
