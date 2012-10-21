#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Hai longqiu.
# 
# Author:     Hai longqiu <qiuhailong@linuxdeepin.com>
# Maintainer: Hai longqiu <qiuhailong@linuxdeepin.com>
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
from dtk.ui.dialog import DialogBox, DIALOG_MASK_MULTIPLE_PAGE
from dtk.ui.listview import ListView, get_content_size
from dtk.ui.progressbar import ProgressBuffer
from dtk.ui.scrolled_window import ScrolledWindow
from dtk.ui.constant import DEFAULT_FONT_SIZE,ALIGN_END, ALIGN_START
from dtk.ui.draw import draw_text, draw_pixbuf
from dtk.ui.button import Button

from new_progressbar import NewProgressBar as ProgressBar

import gtk
import gobject

FORM_WIDTH  = 300
FORM_HEIGHT = 400

class ConvTAskGui(DialogBox):
    def __init__(self):
        DialogBox.__init__(self, 
                           "格式转化任务管理器", 
                           FORM_WIDTH, FORM_HEIGHT, 
                           mask_type=DIALOG_MASK_MULTIPLE_PAGE,
                           close_callback=self.hide_all,
                           modal=False,
                           window_hint=gtk.gdk.WINDOW_TYPE_HINT_DIALOG,
                           window_pos=gtk.WIN_POS_CENTER,
                           resizable=False
                           )
        self.init_widgets()
        # add widgets.
        self.body_box.pack_start(self.scrolled_window, False, False)
        
    def init_widgets(self):
        
        self.scrolled_window = ScrolledWindow()
        self.list_view = ListView()                
        self.scrolled_window.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        self.scrolled_window.add_child(self.list_view)
        
        self.start_btn = Button("开始")
        self.pause_btn = Button("暂停")
        self.right_button_box.set_buttons([self.start_btn, self.pause_btn])
        
class MediaItem(gobject.GObject):
    '''List item.'''    
    __gsignals__ = {
        "redraw-request" : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
    }    
    def __init__(self):
        '''Init list item.'''
        gobject.GObject.__init__(self)
        self.update()
        self.index = None
        
    def set_text(self, text):
        if text == "Done Transcoding":
            self.set_status_icon("success")
        elif text == "show_error":    
            self.set_status_icon("error")
        elif text == "":    
            pass
        
    def set_fraction(self, value):
        if 0.0 <= value <= 1.0:
            self.progress_ratio = value
            self.emit_redraw_request()
        
    def set_status_icon(self, name):
        if name == "wait":
            self.status_icon = self.wait_icon
            self.status_icon_press = self.wait_icon_press
        elif name == "stop":
            self.status_icon =  self.stop_icon
            self.status_icon_press = self.stop_icon_press
        elif name == "success":
            self.status_icon =  self.success_icon
            self.status_icon_press = self.success_icon_press
        elif name == "working":
            self.status_icon = self.working_icon
            self.status_icon_press = self. working_icon_press
        elif name == "error":
            self.status_icon = self.error_icon
            self.status_icon_press = self. error_icon_press
        
        self.emit_redraw_request()
        
    def set_index(self, index):
        '''Update index.'''
        self.index = index
        
    def get_index(self):
        '''Get index.'''
        return self.index
        
    def emit_redraw_request(self):
        '''Emit redraw-request signal.'''
        self.emit("redraw-request")
        
    def update(self, title="icon_pixbuf", length="progress_buffer"):
        '''Update.'''
        # Update.
        self.title = title
        self.length = length
        
        # Calculate item size.
        self.title_padding_x = 10
        self.title_padding_y = 5
        (self.title_width, self.title_height) = get_content_size(self.title, DEFAULT_FONT_SIZE) #DEFAULT_FONT_SIZE
        self.title_width = 20
        
        self.length_padding_x = 20
        self.length_padding_y = 5
        (self.length_width, self.length_height) = get_content_size(self.length, DEFAULT_FONT_SIZE) #DEFAULT_FONT_SIZE
        self.length_width = 150
        
        # ProgressBar buffer.
        self.progress_ratio = 0.0
        self.progress_padding_x = 10
        self.progress_padding_y = 5
        self.progress_w, self.progress_h = 200, 10                
        self.progress_buffer = ProgressBuffer()
        
        self.status_icon = None
        self.status_icon_press = None
        self.wait_icon = app_theme.get_pixbuf("transcoder/wait.png").get_pixbuf()
        self.wait_icon_press = app_theme.get_pixbuf("transcoder/wait_press.png").get_pixbuf()
        # stop conv.
        self.stop_icon = app_theme.get_pixbuf("transcoder/stop.png").get_pixbuf()        
        self.stop_icon_press = app_theme.get_pixbuf("transcoder/stop_press.png").get_pixbuf()
        # conv success.
        self.success_icon = app_theme.get_pixbuf("transcoder/success.png").get_pixbuf()
        self.success_icon_press = app_theme.get_pixbuf("transcoder/success_press.png").get_pixbuf()
        # staring conv.
        self.working_icon = app_theme.get_pixbuf("transcoder/working.png").get_pixbuf()
        self.working_icon_press = app_theme.get_pixbuf("transcoder/working_press.png").get_pixbuf()
        # error .
        self.error_icon = app_theme.get_pixbuf("transcoder/error.png").get_pixbuf()
        self.error_icon_press = app_theme.get_pixbuf("transcoder/error_press.png").get_pixbuf()
        # Init icon state.        
        self.set_status_icon("wait")        
        # set icon[position]->> x and y.
        self.status_icon_padding_x = 10
        self.status_icon_padding_y = 5        
        # get icon width and height .
        self.status_icon_w, self.status_icon_h = (self.status_icon.get_width(), self.status_icon.get_height())
        
    def render_title(self, cr, rect, in_selection, in_highlight):
        '''Render title.'''
        rect.x += self.title_padding_x
        icon_x = rect.x + self.status_icon_padding_x
        icon_y = rect.y + (rect.height - self.status_icon_h) / 2
        if in_selection:
            draw_pixbuf(cr, self.status_icon_press, icon_x, icon_y)
        else:    
            draw_pixbuf(cr, self.status_icon, icon_x, icon_y)

        
    def render_length(self, cr, rect, in_selection, in_highlight):
        '''Render length.'''
        rect.width -= self.length_padding_x
        self.progress_buffer.progress = self.progress_ratio * 100
        progress_x = rect.x + self.progress_padding_x
        progress_y = rect.y + (rect.height - self.progress_h) / 2
        progress_rect = gtk.gdk.Rectangle(progress_x, progress_y, self.progress_w, self.progress_h)
        self.progress_buffer.render(cr, progress_rect)        
                
    def get_column_sizes(self):
        '''Get sizes.'''
        return [(self.title_width + self.title_padding_x * 2, 
                 self.title_height + self.title_padding_y * 2),
                (self.length_width + self.length_padding_x * 2,                 
                 self.length_height + self.length_padding_y * 2),
                ]    
    
    def get_renders(self):
        '''Get render callbacks.'''
        return [self.render_title,
                self.render_length]
        
if __name__ == "__main__":
    value = 0.01
    def start_btn_clicked(widget):
            conv_task_gui.list_view.items[1].set_status_icon("success")
            conv_task_gui.list_view.items[1].set_fraction(1.0)

    def update_progressbar():        
        global value 
        value += 0.01
        conv_task_gui.list_view.items[1].set_status_icon("working")
        conv_task_gui.list_view.items[1].set_fraction(value)
        return True
    
    conv_task_gui = ConvTAskGui()
    conv_task_gui.list_view.add_items([
            MediaItem(), 
            MediaItem(),
            MediaItem(),
            MediaItem(),
            MediaItem(),
            ])
    conv_task_gui.start_btn.connect("clicked", start_btn_clicked)
    conv_task_gui.list_view.items[0].set_status_icon("error")
    conv_task_gui.list_view.items[1].set_status_icon("success")
    conv_task_gui.list_view.items[1].set_fraction(1.0)
    gtk.timeout_add(500, update_progressbar)
    conv_task_gui.show_all()
    gtk.main()    
    

    
    
    