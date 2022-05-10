# -*- coding: utf-8 -*-
"""
Created on Sat Mar 19 10:18:58 2022

@author: keatin6
"""

# %%

import wx
import controller

# %%

class PlantDialog(wx.Dialog):
    def __init__(self, session, row=None, title="Add", addRecord=True):
        #----------------------------------------------------------------------
        super().__init__(None, title=f"{title} Plant Record")
        #----------------------------------------------------------------------
        
        #----------------------------------------------------------------------
        self.addRecord = addRecord
        self.selected_row = row
        self.session = session
        
        #sizers----------------------------------------------------------------
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        #----------------------------------------------------------------------
        
        #----------------------------------------------------------------------
        category = subategory = plant_type = ""
        size = (130, -1)
        size_input = (200, -1)
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        #----------------------------------------------------------------------
        
        #Category label set up-------------------------------------------------
        category_label = wx.StaticText(self, label="Category", size=size)
        category_label.SetFont(font)
        #----------------------------------------------------------------------
        
         #Category comb box set up---------------------------------------------
        self.category_combo = wx.ComboBox(
            self, value=category,
            choices=controller.get_combo_choices(self.session, "cat"),
            size=size_input)
        #----------------------------------------------------------------------
        
        #Bind a function to the category combo box-----------------------------
        self.category_combo.Bind(
            wx.EVT_COMBOBOX, self.filter_for_category_selection)
        #----------------------------------------------------------------------
        
        #----------------------------------------------------------------------
        category_row = self.row_builder([category_label, self.category_combo])
        main_sizer.Add(category_row, 0, wx.ALL)
        #----------------------------------------------------------------------
        
        #----------------------------------------------------------------------
        plant_type_label = wx.StaticText(self, label="Plant Type", size=size)
        plant_type_label.SetFont(font)
        
         #Plant type combo box-------------------------------------------------
        self.plant_type_combo = wx.ComboBox(
            self, value=plant_type,
            choices=controller.get_combo_choices(self.session, "plt"),
            size=size_input)
        #----------------------------------------------------------------------
        
        #----------------------------------------------------------------------
        self.plant_type_combo.Bind(
            wx.EVT_COMBOBOX, self.filter_for_plant_type_selection)
        #----------------------------------------------------------------------
        
        #Plant type row set up-------------------------------------------------
        plant_type_row = self.row_builder(
            [plant_type_label, self.plant_type_combo])
        main_sizer.Add(plant_type_row, 0, wx.ALL)
        #----------------------------------------------------------------------
        
         #Category label set up------------------------------------------------
        subategory_label = wx.StaticText(self, label="Subategory", size=size)
        subategory_label.SetFont(font)
        #----------------------------------------------------------------------
        
        #Category comb box set up----------------------------------------------
        self.subcategory_combo = wx.ComboBox(
            self, value=subategory,
            choices=[],
            size=size_input)
        #----------------------------------------------------------------------
        
        #----------------------------------------------------------------------
        subcategory_row = self.row_builder(
            [subategory_label, self.subcategory_combo])
        main_sizer.Add(subcategory_row, 0, wx.ALL)
        #----------------------------------------------------------------------

        #Plant Label Set Up----------------------------------------------------
        plant_label = wx.StaticText(self, label="Plant", size=size)
        plant_label.SetFont(font)
        self.plant_textctrl = wx.TextCtrl(self, size=size_input, value="")
        plant_row = self.row_builder([plant_label, self.plant_textctrl])
        main_sizer.Add(plant_row, 0, wx.ALL)
        #----------------------------------------------------------------------
        
        dtg_label = wx.StaticText(self, label="Days to Germination", size=size)
        dtg_label.SetFont(font)
        self.dtg_textctrl = wx.TextCtrl(self, size=size_input, value="")
        dtg_row = self.row_builder([dtg_label, self.dtg_textctrl])
        main_sizer.Add(dtg_row, 0, wx.ALL)
        
        #----------------------------------------------------------------------
                
        dtm_label = wx.StaticText(self, label="Days to Maturity", size=size)
        dtm_label.SetFont(font)
        self.dtm_textctrl = wx.TextCtrl(self, size=size_input, value="")
        dtm_row = self.row_builder([dtm_label, self.dtm_textctrl])
        main_sizer.Add(dtm_row, 0, wx.ALL)
        
        #----------------------------------------------------------------------
        self.button = wx.Button(self, label=f"{title} Record")
        self.button.Bind(wx.EVT_BUTTON, self.on_add)
        button_sizer.Add(self.button, 0, wx.ALL, 5)
        main_sizer.Add(button_sizer, 0, wx.CENTER)
        #----------------------------------------------------------------------

        #Set the sizer and fit it----------------------------------------------
        self.SetSizerAndFit(main_sizer)
        #----------------------------------------------------------------------
        
    def filter_for_category_selection(self, event):
        category = self.category_combo.GetValue()
        table = controller.table_routing("cat")
        category_id = controller.find_id_from_value(
            self.session, table, category)
        choices = controller.get_combo_choices(
            self.session, "plt", category_filter=category_id)
        self.plant_type_combo.SetValue("")
        self.subcategory_combo.SetValue("")
        self.subcategory_combo.Clear()
        self.plant_type_combo.Clear()
        self.plant_type_combo.Append(choices)
        
    def filter_for_plant_type_selection(self, event):
        plant_type = self.plant_type_combo.GetValue()
        table = controller.table_routing("plt")
        plant_type_id = controller.find_id_from_value(
            self.session, table, plant_type)
        choices = controller.get_combo_choices(
            self.session, "sub", plant_type_filter=plant_type_id)
        self.subcategory_combo.SetValue("")
        self.subcategory_combo.Clear()
        self.subcategory_combo.Append(choices)

    def on_add(self, event):
        self.add_record()

    def add_record(self):

        #----------------------------------------------------------------------
        subcategory = self.subcategory_combo.GetValue()
        sub_table = controller.table_routing("sub")
        subcategory_id = controller.find_id_from_value(
            self.session, sub_table, subcategory)
        
        #----------------------------------------------------------------------
        #Get plant type value and find corresponding id
        
        plant_type = self.plant_type_combo.GetValue()
        plt_table = controller.table_routing("plt")
        plant_type_id = controller.find_id_from_value(
            self.session, plt_table, plant_type)

        #----------------------------------------------------------------------
        #
        
        plant = self.plant_textctrl.GetValue()
        dtm_range = self.dtm_textctrl.GetValue()
        dtg_range = self.dtg_textctrl.GetValue()
        
        #----------------------------------------------------------------------
        controller.insert_plant_record(
            self.session, plant, subcategory_id, plant_type_id, 
            dtg_range, dtm_range)
        #----------------------------------------------------------------------
        #Clear widget values
    
        self.category_combo.SetValue("")
        self.subcategory_combo.SetValue("")
        self.plant_type_combo.SetValue("")
        self.plant_textctrl.SetValue("")
        self.dtg_textctrl.SetValue("")
        self.dtm_textctrl.SetValue("")
        
        #----------------------------------------------------------------------
        
        
    def row_builder(self, widgets):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label, text = widgets
        sizer.Add(label, 0, wx.ALL, 5)
        sizer.Add(text, 0, wx.ALL, 5)
        return sizer
    
# %%

def show_message(message, caption, flag=wx.ICON_ERROR):
    msg = wx.MessageDialog(None, message=message, caption=caption, style=flag)
    msg.ShowModal()
    msg.Destroy()
    
# %%