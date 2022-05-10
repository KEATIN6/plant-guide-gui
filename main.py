# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 19:55:16 2022

@author: KEATIN6
"""

# %%

import wx
from ObjectListView import ObjectListView, ColumnDefn
import controller
import dialogs

# %%

class AppPanelMain(wx.Panel):
    def __init__(self, parent):
        #INITATE FRAME-----------------------------------01
        super().__init__(parent)
        self.parent = parent
        
        #FONTS-------------------------------------------02
        font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        
        #------------------------------------------------00
        self.plant_results = []
        
        #SIZERS------------------------------------------03
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        #ADD TITLE---------------------------------------04
        title = wx.StaticText(self, label="Plant Varieties")
        title.SetFont(font)
        main_sizer.Add(title, 0, wx.ALL, 5)
        
        #ADD ObjectListView------------------------------05
        self.plants_olv = ObjectListView(
            self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.plants_olv.SetEmptyListMsg("No records found")
        main_sizer.Add(self.plants_olv, 1, wx.EXPAND|wx.ALL, 5)
        
        #------------------------------------------------00
        button = wx.Button(self, label="Add Record")
        button.Bind(wx.EVT_BUTTON, self.on_add)
        main_sizer.Add(button,0, wx.CENTER)
        
        #SET SIZER---------------------------------------06
        self.SetSizer(main_sizer)
        self.show_all_results()
        
        #------------------------------------------------07
        
    def on_add(self, event):
        self.add_record(event)
        self.show_all_results()
        
    def add_record(self, event):
        with dialogs.PlantDialog(self.parent.session) as dlg:
            dlg.ShowModal()
        
    def show_all_results(self):
        self.plant_results = controller.get_plant_results(self.parent.session)
        self.update_results()
        
    def update_results(self):
        #------------------------------------------------08
        self.plants_olv.SetColumns([
            ColumnDefn("Category", "left", 100, "category"),
            ColumnDefn("Subcategory", "left", 100, "subcategory"),
            ColumnDefn("PlantType", "left", 160, "plant_type"),
            ColumnDefn("Plant", "left", 160, "plant"),
            ColumnDefn("Botanic", "left", 160, "scientific")])
        self.plants_olv.SetObjects(self.plant_results)

# %%
        
class AppFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Ultimate Plant Guide", size=(1000,600))
        self.session = controller.connect_to_database()
        
        panel = AppPanelMain(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(panel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)

# %%

if __name__ == "__main__":
    app = wx.App(False)
    frame = AppFrame()
    frame.Show()
    app.MainLoop()
    del app

# %%