#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from skin import app_theme
from dtk.ui.draw import draw_vlinear
from dtk.ui.dialog import DialogBox, DIALOG_MASK_MULTIPLE_PAGE
from dtk.ui.entry import InputEntry
from file_choose_button import FileChooserButton
from dtk.ui.button import Button
from dtk.ui.label import Label
from dtk.ui.combo import ComboBox
from new_combobox import NewComboBox

import gtk

FORM_WIDTH = 465
FORM_HEIGHT = 280

supported_containers_imtes = [ # supported_containers
        ["Ogg", 0], 
        ["Matroska", 1], 
        ["AVI", 2], 	
        ["MPEG PS", 3],	
        ["MPEG TS", 4],	
        ["AVCHD/BD", 5], 	
        ["FLV", 6], 	
        ["Quicktime", 7], 
        ["MPEG4", 8], 
        ["3GPP", 9], 
        ["MXF", 10], 
        ["ASF", 11], 		
        ["WebM", 12], 
        ["No container (Audio-only)", 13]
        ]

class Form(DialogBox):
    def __init__(self):
        DialogBox.__init__(self, 
                           "格式转换器", 
                           FORM_WIDTH, FORM_HEIGHT- 80, 
                           mask_type=DIALOG_MASK_MULTIPLE_PAGE,
                           modal=False,
                           window_hint=gtk.gdk.WINDOW_TYPE_HINT_DIALOG,
                           window_pos=gtk.WIN_POS_CENTER,
                           resizable=False
                           )                        
        # Init value.
        self.init_value()
        # Init all widgets.
        self.InitializeComponent()
        self.draw_mask = self.draw_dialogbox_mask
        
    def draw_dialogbox_mask(self, cr, x, y, width, height):
        pass
                
    def init_value(self):
        # left.
        self.left_x = 20
        self.left_y = 20
        self.left_offset_x = 0
        self.left_offset_y = 0
        # right.
        self.right_x = 200
        self.right_y = 20
        self.right_offset_x = 0
        self.right_offset_y = 0
        # move.
        self.move_offset_x = 0
        self.move_offset_y = 0
        
    def InitializeComponent(self):
        # Init form event.
        self.connect("destroy", lambda w : self.destroy())
        # Init widgets.
        self.main_fixed = gtk.Fixed()
        self.brand_label = Label("品牌 : ")
        self.format_label = Label("格式 : ")        
        self.bit_rate_label = Label("码率 : ")
        self.frame_rate_label = Label("帧率 : ")
        self.path_label = Label("路径 : ")
        self.model_label = Label("    型号 : ")
        self.ratio_label = Label("分辨率 : ")        
        
        self.brand_combo = NewComboBox(110) #ComboBox(supported_containers_imtes, 100, max_width=110)
        self.format_combo = NewComboBox(110) #ComboBox(supported_containers_imtes, 100, max_width=110) # connect 
        self.bit_rate_combo = NewComboBox(110) #ComboBox(supported_containers_imtes, 100)
        self.frame_rate_combo = NewComboBox(110) #ComboBox(supported_containers_imtes, 100)
        self.path_entry = InputEntry()
        self.model_combo = NewComboBox(110) #ComboBox(supported_containers_imtes, 100)        
        self.ratio_combo = NewComboBox(110) #ComboBox(supported_containers_imtes, 100) # Resolution
        
        self.modify_chooser_btn = FileChooserButton("选择") # connect self.FileChooser
        self.start_btn = Button("开始")
        self.close_btn = Button("关闭")
        self.higt_set_bool = False
        self.higt_set_btn = Button("高级")
        self.align = gtk.Alignment()
        self.align.add(self.higt_set_btn)
        self.align.set(1, 0, 1, 0)
        self.align.set_padding(0, 0, 0, 200)
        self.right_button_box.set_buttons([self.align, self.start_btn, self.close_btn])
        
        # path_entry.
        PATH_ENTRY_WIDTH = 240
        PATH_ENTRY_HEIGHT = 25
        self.path_entry.set_sensitive(False)
        self.path_entry.set_size(PATH_ENTRY_WIDTH, PATH_ENTRY_HEIGHT)
        self.close_btn.connect("clicked", lambda w : self.destroy())
        # higt_set_btn.
        self.higt_set_btn.connect("clicked", self.higt_set_btn_clicked)
        
        ''' add all widgets. '''
        #
        self.left_widgets = [self.brand_label, self.brand_combo, self.format_label, self.format_combo,
                             self.bit_rate_label, self.bit_rate_combo, self.frame_rate_label, self.frame_rate_combo,
                             self.path_label, self.path_entry, self.modify_chooser_btn]
        # add left widgets.
        for widget in self.left_widgets:
            self.main_fixed.put(widget, 0, 0)
        #    
        self.right_widgets = [(self.model_label, self.model_combo),
                              (self.ratio_label, self.ratio_combo)]
        # add right widgets.
        for label, combo in self.right_widgets:
            padding_width, padding_height = label.get_size_request()
            padding_y = int(padding_height/3.5)
            self.main_fixed.put(label,
                                self.right_x,
                                self.right_y + self.right_offset_y - padding_y)
            self.main_fixed.put(combo, 
                                self.right_x + padding_width + 5, 
                                self.right_y + self.right_offset_y - padding_y) 
            self.right_offset_y += 40
            
        # form body box add main fixed.
        self.body_box.pack_start(self.main_fixed, True, True)            
        self.hide_setting()
                
    def higt_set_btn_clicked(self, widget):    
        if self.higt_set_bool:
            self.hide_setting()
            self.set_geometry_hints(None, FORM_WIDTH, FORM_HEIGHT-80, FORM_WIDTH, FORM_HEIGHT-80, -1, -1, -1, -1, -1, -1)
            self.set_size_request(FORM_WIDTH, FORM_HEIGHT-80)
            # self.set_geometry_hints(None, FORM_WIDTH, FORM_HEIGHT, -1, -1, -1, -1, -1, -1, -1, -1)
        else:    
            self.show_setting()
            self.set_geometry_hints(None, FORM_WIDTH, FORM_HEIGHT, FORM_WIDTH, FORM_HEIGHT, -1, -1, -1, -1, -1, -1)
            self.set_size_request(FORM_WIDTH, FORM_HEIGHT+80) 
        self.higt_set_bool = not self.higt_set_bool
        
    def move_left_widgets(self):        
        self.init_value()
        other_padding_x = 5
        button_padding_x = 10
        #
        for label, other, button in self.left_widgets:
            padding_width, padding_height = label.get_size_request()
            padding_y = int(padding_height/3.5)
            # main fixed add label widget.
            self.main_fixed.move(label, 
                                self.left_x, 
                                self.left_y + self.left_offset_y)
            # main fixed add other widget.            
            self.main_fixed.move(other, 
                                self.left_x + padding_width + other_padding_x, 
                                self.left_y + self.left_offset_y - padding_y)
            if button:
                # main fixed add button widget.                
                self.main_fixed.move(button, 
                                    self.left_x + padding_width + other.get_size_request()[0] + button_padding_x, 
                                    self.left_y + self.left_offset_y - padding_y) 
            # set left offset y -> left_offset_y + 40. 
            self.left_offset_y += 40                          
        self.main_fixed.show_all()
        
    def hide_setting(self):    
        # hide widget.
        #     
        self.left_widgets = [(self.brand_label, self.brand_combo, None),
                             (self.format_label, self.format_combo, None),
                             (self.path_label, self.path_entry, self.modify_chooser_btn),
                             ]
        
        self.move_left_widgets()        
        
        for hide_widget in [self.bit_rate_label, self.bit_rate_combo, self.frame_rate_label, self.frame_rate_combo]:
            hide_widget.hide_all()
        
    def show_setting(self):
        # show widget.
        #
        self.left_widgets = [(self.brand_label, self.brand_combo, None),
                             (self.format_label, self.format_combo, None),
                             (self.bit_rate_label, self.bit_rate_combo, None),
                             (self.frame_rate_label, self.frame_rate_combo, None),
                             (self.path_label, self.path_entry, self.modify_chooser_btn),
                             ]
        self.move_left_widgets()
        self.show_all()
        
if __name__ == "__main__":
    form = Form()
    form.show_all()
    form.hide_setting()
    # form.hide_setting()
    # form.show_setting()
    gtk.main()
    
    