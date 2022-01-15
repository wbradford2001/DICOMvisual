from ctypes import alignment
from distutils import command
import tkinter as tk
import numpy as np
import CustomEntry



import TopLevelWindow
import CustomCanvas
import CustomButton
import master_funcs
import SaveChanges
import CustomRadioButton





class full_df_cascade:
    def __init__(self):
        self.current_data_box = 0
    def create_full_df_toplevel(self, master, view_or_edit = 'edit'):
        self.current_data_box = 0
        self.master = master
        
        #create window
        title = "Full Data Frame: " + master.image_names[master.MainView.currentim.get()]
        window_width = 1000
        window_height = 500
        self.Full_DF_Wind = TopLevelWindow.top_window(master = master, root = master.root, width = window_width, height=window_height, title = title, color =CustomEntry.CustomEntryClass.defaultidlecolor)
        self.scale_val = tk.IntVar()
        self.scale = tk.Scale(self.Full_DF_Wind.toplevel, bg = CustomEntry.CustomEntryClass.defaultidlecolor, borderwidth=0, command = self.move_canvas, from_= 0, to = 10,
                sliderlength=200, variable = self.scale_val)
        self.Full_DF_Wind.toplevel.bind('<MouseWheel>', self.set_scale_from_mouse_wheel)

        self.all_elements = list(master.dfs_metas[master.MainView.currentim.get()])
        self.all_elements.extend(list(master.dfs[master.MainView.currentim.get()])) 
        self.display_canvases = {}
        #create canvas
        total_length = self.Full_DF_Wind.width
        tag_length = total_length * 0.1
        key_word_length = total_length * 0.2
        value_length = total_length * 0.6
        vr_length = total_length * 0.1

        self.hex_5_digit_keys = list(master.display_strings[str(master.MainView.currentim.get())].keys())
        for index_of_catagory, key in enumerate(self.hex_5_digit_keys):
            self.display_canvases[key] = CustomCanvas.CustomCanv(master = master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = CustomEntry.CustomEntryClass.defaultidlecolor, relposx = 0, relposy = 0, relwidth = total_length/self.Full_DF_Wind.width * 1, relheight = 0.9)
            #self.display_canvases[key].show_self()
        CustomEntry.CustomEntryClass.boxes_so_far.clear()
        for key, canvas in self.display_canvases.items():
            y_level = 1
            title = CustomEntry.CustomEntryClass(master = master, parent = self, root = self.display_canvases[key].canvobject, index = 0, xpos = 0, width = total_length, 
                text = "Catagory: (" + (key) + ",____)", 
                view_or_edit = view_or_edit, state = "TITLE")
            title.show_self()
            for item in self.all_elements:
            
                if (str(item.tag)[1:5]) == key:
                    tag = CustomEntry.CustomEntryClass(master = master, parent = self, root = self.display_canvases[key].canvobject, index = y_level, xpos = 0, width = tag_length, 
                    text = item.tag, 
                    state = "view", element = item, attrib = "tag")
                    tag.show_self()

                    keyword = CustomEntry.CustomEntryClass(master = master, parent = self, root = self.display_canvases[key].canvobject, index = y_level, xpos = tag_length, width = key_word_length, 
                    text = item.keyword, 
                    state = "view", element = item, attrib= "keyword")
                    keyword.show_self()

                    value = CustomEntry.CustomEntryClass(master = master, parent = self, root = self.display_canvases[key].canvobject, index = y_level, xpos = tag_length + key_word_length, width = value_length, 
                    text = item.value, 
                    state = view_or_edit, element = item, attrib = 'value')
                    value.show_self()

                    VR = CustomEntry.CustomEntryClass(master = master, parent = self, root = self.display_canvases[key].canvobject, index = y_level, xpos = tag_length + key_word_length + value_length, width = vr_length, 
                    text = item.VR, 
                    state = "view", element = item, attrib = 'VR')
                    VR.show_self()


                    y_level += 1


            self.display_canvases[key].relheight = (CustomEntry.CustomEntryClass.height * y_level)/self.Full_DF_Wind.height

        button_canvas = CustomCanvas.CustomCanv(master = master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = '#%02x%02x%02x' % (20, 20, 20), relposx = 0.5, relposy = 0.95, relwidth = 1, relheight = .1, anchor = 'center')
        button_canvas.show_self()
        self.next_button = CustomButton.Button(master = master, root = button_canvas.canvobject, relxpos = 0.95, relypos = 0.5, width = 0.1*self.Full_DF_Wind.width, height = 50, text = "Next", size_reduce=3, command = self.show_next, anchor = 'center')
        self.back_button = CustomButton.Button(master = master, root = button_canvas.canvobject, relxpos = 0.05, relypos = 0.5, width = 0.1*self.Full_DF_Wind.width, height = 50, text = "Back", size_reduce=3, command = self.show_previous, anchor  = 'center')
   

        self.save_changes = CustomButton.Button(master = master, root = button_canvas.canvobject, relxpos = 0.275 + 0.01, relypos = 0.5, width = 0.35*self.Full_DF_Wind.width, height = 50, text = "Save Changes", size_reduce=3, command = self.decide_save_changes, 
                anchor = 'center', state = "DISABLED")
        self.revert_changes = CustomButton.Button(master = master, root = button_canvas.canvobject, relxpos = 0.725 - 0.01, relypos = 0.5, width = 0.35*self.Full_DF_Wind.width, height = 50, text = "Revert Changes", size_reduce=3, command = self.revert_changes_func, 
                anchor  = 'center', state = "DISABLED")
  
        self.indicator = tk.Label(button_canvas.canvobject, bg = '#%02x%02x%02x' % (130, 130, 130), fg = '#%02x%02x%02x' % (240, 240, 240))
        self.indicator.place(relx = 0.5, rely = 0.5, relwidth = 0.06, height = 50, anchor = 'center')
        self.indicator.config(text = str(self.current_data_box+1) + '/' + str(len(self.display_canvases)))
        self.next_button.show_self()
        self.back_button.show_self()
        self.back_button.disable()
        self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].show_self()

    def show_next(self):
        self.back_button.enable()
        if self.current_data_box  < len(self.hex_5_digit_keys)-1:
            self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].hide_self()  
            self.current_data_box += 1
            self.show_canvas()
            if self.current_data_box == len(self.hex_5_digit_keys)-1:
                self.next_button.disable()

    def show_previous(self):
        self.next_button.enable()
        if self.current_data_box > 0:
            self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].hide_self() 
            self.current_data_box -= 1
            self.show_canvas()
            if self.current_data_box == 0:
                self.back_button.disable()
    def show_canvas(self):
            self.scale.place_forget()
            self.indicator.config(text = str(self.current_data_box+1) + '/' + str(len(self.display_canvases)))
            if self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relheight > 0.9:
                self.scale_val.set(0)
                self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relwidth = 1 - 15/self.Full_DF_Wind.width
            
                self.scale.place(relx = 1, rely = 0, relheight = 0.9, anchor = 'ne')
            self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].show_self()         
    def move_canvas(self, scroll_to):
        new_func = master_funcs.map_ranges([0, 10], [0, -(self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relheight-0.9)])
        self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relposy = new_func(int(self.scale_val.get()))
        self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].show_self() 

    def set_scale_from_mouse_wheel(self, delta):
        if self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relheight > 0.9:
            self.scale_val.set(self.scale_val.get() - delta.delta)
            self.move_canvas(9)


    def decide_save_changes(self):       
        if len(self.master.dfs) > 1:
            self.just_one_or_many_wind = TopLevelWindow.just_one_or_many(master = self.master, root = self.Full_DF_Wind.toplevel
                        ,message = "Would you like to save changes for just " + str(self.master.image_names[self.master.MainView.currentim.get()]) 
                                    + " or for all files?", image_name = str(self.master.image_names[self.master.MainView.currentim.get()]) ,
                                    proceed_command = self.final_save_changes)

        elif len(self.master.dfs) == 1:
            self.final_save_changes("Just One")
            
    def final_save_changes(self,one_or_all):
        image_indeces = [] 
        if one_or_all == "Just One":
            image_indeces.append(self.master.MainView.currentim.get())
        elif one_or_all == "All":
            for index in range(0, len(self.master.MainView.arr)):
                image_indeces.append(index)
        self.savechangecascade = SaveChanges.save_cascade()
        self.savechangecascade.save_from_boxes(master = self.master, input_full_df_cascade = self, image_indexes = image_indeces)
        # types = []
        # for index, box in enumerate(CustomEntry.CustomEntryClass.boxes_so_far):
        #     if box.orig_string != box.text.get():
        #         if box.attrib == "tag":
        #             pass
        #         elif box.attrib == "keyword":
        #             pass
        #         elif box.attrib == "value":
        #             if box.element.tag in self.master.dfs[self.master.MainView.currentim.get()]:
        #                 self.master.dfs[self.master.MainView.currentim.get()][box.element.tag].value = (box.text.get())
        #             elif box.element.tag in self.master.dfs_metas[self.master.MainView.currentim.get()]:
        #                 self.master.dfs_metas[self.master.MainView.currentim.get()][box.element.tag].value = (box.text.get())                        
                
        #         elif box.attrib == "VR":
        #             pass                                 

        # types = set()
        # for index, element in enumerate(list(self.master.dfs[self.master.MainView.currentim.get()])):
        #     if isinstance(element.value, bytes):
        #         print(element)
        #print(types)
    def revert_changes_func(self):
        for index, box in enumerate(CustomEntry.CustomEntryClass.boxes_so_far):
            if box.orig_string != box.text.get():
                box.text.set(box.orig_string)
                box.show_self()
        self.save_changes.disable()
        self.revert_changes.disable()        

