from ctypes import alignment
import tkinter as tk
from typing import List
import CustomEntry



import TopLevelWindow
import CustomCanvas
import CustomButton
import master_funcs





# class text_box:
#     list_of_boxes = []
#     regular_boxes = []
#     meta_boxes = []
#     error_box_already_exists = False
#     height = 20
#     def __init__(self, master, root, index, xpos, width, text, view_or_edit, disabled = False):
#         self.master = master
#         self.root = root
#         self.disabled = disabled
#         self.xpos = xpos
#         self.index = index
#         self.width = width 
#         self.text = text
#         self.view_or_edit = view_or_edit
#         #self.dataelement = self.master.dfs[self.master.MainView.currentim.get()][self.index]
#         self.element_str = tk.StringVar()
#         if len(str(self.text)) < 30:
#             self.element_str.set(str(self.text))
        
#         # self.view_or_edit = view_or_edit        
#         # if self.attrib == "tag":
#         #     self.element_str.set(str(self.dataelement.tag))
#         # elif self.attrib == "keyword":
#         #     self.element_str.set(str(self.dataelement.keyword))
#         # elif self.attrib == "VR":
#         #     self.element_str.set(str(self.dataelement.VR))

#         #fix me
#         # elif self.attrib == "value":
#         #     if (self.dataelement.keyword) != "PixelData":
#         #         self.element_str.set(str(self.dataelement.value))
#         #     else:
#         #         self.element_str.set("Array of {} elements".format(
#         #                                                                 len(self.dataelement.value),))
#         # else:
#         #     self.element_str.set(self.attrib)

#         # self.orig_string = self.element_str.get()
#         # text_box.list_of_boxes.append(self)
#         # if box_to_add_to == "regular":
#         #     text_box.regular_boxes.append(self)
#         # elif box_to_add_to == "meta":
#         #     text_box.meta_boxes.append(self)      
#         self.label = tk.Entry(
#                     self.root, 
#                     font = (self.master.fontstyle, 10),
#                     textvariable=self.element_str,
#                     justify = tk.CENTER,
#                     bg = 'black',
#                     bd = 2,
#                     fg = 'white',


#                     )
#         if self.view_or_edit == 'view':
#             self.element_str.trace_add("write", self.error_message)
#         elif self.view_or_edit == 'edit':
#             if disabled == False:
#                 self.element_str.trace_add("write", self.change_made)            
#             else:
#                 self.element_str.trace_add("write", self.cant_edit_element)
#     def change_made(self, one, two, three):
#         pass
#         # save_button.config(state = tk.NORMAL)
#         # revert_button.config(state = tk.NORMAL)
#     def show_self(self):
#         self.label.place(x = self.xpos, y = self.index * text_box.height, anchor='nw', width = self.width, height = text_box.height)

#     def error_message(self, one, two, three):
#         self.element_str.set(self.orig_string)
#         #global Error_Window
#         if  text_box.error_box_already_exists == False:
#             text_box.error_box_already_exists = True
#             # Error_Window = TopLevelWindow.top_window(root=rootcopy, width=400, height=200, title="ERROR", color = 'grey')
#             # error_message = tk.Label(Error_Window.toplevel, text = "Editing Data is only possible in 'Custom Edit' mode",
#             #                         bg = 'grey',
#             #                         fg = 'white')
#             # error_message.place(relx = 0.5, rely = 0.5, anchor  ='center')
#             global EW
#             EW = TopLevelWindow.show_error_window(root=Full_DF_Wind.toplevel, fontstyle=self.master.fontstyle, message="Editing Data is only possible in 'Custom Edit' mode", width = 400)
#             EW.toplevel.protocol("WM_DELETE_WINDOW", on_closing)
#     def cant_edit_element(self, one, two, three):
#         self.element_str.set(self.orig_string)
#         #global Error_Window
#         if  text_box.error_box_already_exists == False:
#             text_box.error_box_already_exists = True
#             # Error_Window = TopLevelWindow.top_window(root=rootcopy, width=400, height=200, title="ERROR", color = 'grey')
#             # error_message = tk.Label(Error_Window.toplevel, text = "Editing Data is only possible in 'Custom Edit' mode",
#             #                         bg = 'grey',
#             #                         fg = 'white')
#             # error_message.place(relx = 0.5, rely = 0.5, anchor  ='center')
#             global EW
#             EW = TopLevelWindow.show_error_window(root=Full_DF_Wind.toplevel, fontstyle=text_box.fontstyle, message="Unable to Edit Data Element", width = 400)
#             EW.toplevel.protocol("WM_DELETE_WINDOW", on_closing)
# def on_closing():
#     text_box.error_box_already_exists = False
#     EW.toplevel.destroy()

# def mouse_move(val):
#     scroll.set(scroll.get() - val.delta)
#     update_scroll(66)

# def update_scroll(yo):
#     val = scroll.get()
#     num_boxes = 200
#     canv.place_configure(
#         y = (-canv_length+Full_DF_Wind.height - buffer)/(scroll_bar_to_) * int(val)
#         )
#     if int(val) != 0:
#         if int(val) <= scroll_bar_to_ - num_boxes:
#             for box in text_box.list_of_boxes[int(val)-1:int(val)-1+num_boxes]:
#                 box.place_self() 
#         else:
#             for box in text_box.list_of_boxes[int(val)-1:-2]:
#                 box.place_self() 
#         if int(val) >= num_boxes:
#             for box in text_box.list_of_boxes[int(val)-num_boxes:int(val)]:
#                 box.place_self() 
#         else:
#             for box in text_box.list_of_boxes[0:int(val)]:
#                 box.place_self() 
#     else:
#         for box in text_box.list_of_boxes[0:num_boxes]:
#                 box.place_self() 

#     if int(val)> num_boxes:
#         for box in text_box.list_of_boxes[0:int(val)-num_boxes]:
#             box.label.place_forget() 
#     if int(val)< scroll_bar_to_ - num_boxes:
#         for box in text_box.list_of_boxes[int(val)+num_boxes: -1]:
#             box.label.place_forget() 

class full_df_cascade:
    def __init__(self):
        self.current_data_box = 0
    def create_full_df_toplevel(self, master, view_or_edit = 'edit'):
        global buffer
        if view_or_edit == "edit":
            buffer = 50
        else:
            buffer = 0


        #create window
        title = "Full Data Frame: " + master.image_names[master.MainView.currentim.get()]
        window_width = 1200
        window_height = 700
        global Full_DF_Wind
        Full_DF_Wind = TopLevelWindow.top_window(master = master, root = master.root, width = window_width, height=window_height + buffer, title = title, color =CustomEntry.CustomEntryClass.defaultidlecolor)
        self.scale_val = tk.IntVar()
        self.scale = tk.Scale(Full_DF_Wind.toplevel, bg = CustomEntry.CustomEntryClass.defaultidlecolor, borderwidth=0, command = self.move_canvas, from_= 0, to = 10,
                sliderlength=200, variable = self.scale_val)
        Full_DF_Wind.toplevel.bind('<MouseWheel>', self.set_scale_from_mouse_wheel)

        all_elements = list(master.dfs_metas[master.MainView.currentim.get()])
        all_elements.extend(list(master.dfs[master.MainView.currentim.get()])) 
        self.display_canvases = {}
        #create canvas
        total_length = Full_DF_Wind.width
        tag_length = total_length * 0.1
        key_word_length = total_length * 0.2
        value_length = total_length * 0.6
        vr_length = total_length * 0.1

        self.hex_5_digit_keys = list(master.display_strings[str(master.MainView.currentim.get())].keys())
        for index_of_catagory, key in enumerate(self.hex_5_digit_keys):
            self.display_canvases[key] = CustomCanvas.CustomCanv(master = master, root = Full_DF_Wind.toplevel, color = CustomEntry.CustomEntryClass.defaultidlecolor, relposx = 0, relposy = 0, relwidth = total_length/Full_DF_Wind.width * 1, relheight = 0.9)
            #self.display_canvases[key].show_self()
        for key, canvas in self.display_canvases.items():
            y_level = 1
            title = CustomEntry.CustomEntryClass(master = master, root = self.display_canvases[key].canvobject, index = 0, xpos = 0, width = total_length, 
                text = "Catagory: (" + (key) + ",____)", 
                view_or_edit = view_or_edit, state = "TITLE")
            title.show_self()
            for item in all_elements:
            
                if (str(item.tag)[1:5]) == key:
                    tag = CustomEntry.CustomEntryClass(master = master, root = self.display_canvases[key].canvobject, index = y_level, xpos = 0, width = tag_length, 
                    text = item.tag, 
                    state = view_or_edit)
                    tag.show_self()

                    keyword = CustomEntry.CustomEntryClass(master = master, root = self.display_canvases[key].canvobject, index = y_level, xpos = tag_length, width = key_word_length, 
                    text = item.keyword, 
                    state = view_or_edit)
                    keyword.show_self()

                    value = CustomEntry.CustomEntryClass(master = master, root = self.display_canvases[key].canvobject, index = y_level, xpos = tag_length + key_word_length, width = value_length, 
                    text = item.value, 
                    state = view_or_edit)
                    value.show_self()

                    VR = CustomEntry.CustomEntryClass(master = master, root = self.display_canvases[key].canvobject, index = y_level, xpos = tag_length + key_word_length + value_length, width = vr_length, 
                    text = item.VR, 
                    state = view_or_edit)
                    VR.show_self()


                    y_level += 1


            self.display_canvases[key].relheight = (CustomEntry.CustomEntryClass.height * y_level)/Full_DF_Wind.height

        button_canvas = CustomCanvas.CustomCanv(master = master, root = Full_DF_Wind.toplevel, color = '#%02x%02x%02x' % (20, 20, 20), relposx = 0.5, relposy = 0.95, relwidth = 1, relheight = .1, anchor = 'center')
        button_canvas.show_self()
        next_button = CustomButton.Button(master = master, root = button_canvas.canvobject, relxpos = 0.9, relypos = 0.5, width = 100, height = 50, text = "Next", size_reduce=3, command = self.show_next, anchor = 'center')
        back_button = CustomButton.Button(master = master, root = button_canvas.canvobject, relxpos = 0.1, relypos = 0.5, width = 100, height = 50, text = "Back", size_reduce=3, command = self.show_previous, anchor  = 'center')
        self.indicator = tk.Label(button_canvas.canvobject, bg = '#%02x%02x%02x' % (20, 20, 20), fg = '#%02x%02x%02x' % (240, 240, 240))
        self.indicator.place(relx = 0.5, rely = 0.5, anchor = 'center')
        self.indicator.config(text = str(self.current_data_box+1) + '/' + str(len(self.display_canvases)))
        next_button.show_self()
        back_button.show_self()
        self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].show_self()

    def show_next(self):
        if self.current_data_box  < len(self.hex_5_digit_keys)-1:
            self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].hide_self()  
            self.current_data_box += 1
            self.show_canvas()
    def show_previous(self):
        if self.current_data_box > 0:
            self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].hide_self() 
            self.current_data_box -= 1
            self.show_canvas()
    def show_canvas(self):
            self.scale.place_forget()
            self.indicator.config(text = str(self.current_data_box+1) + '/' + str(len(self.display_canvases)))
            if self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relheight > 0.9:
                self.scale_val.set(0)
                self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relwidth = 1 - 15/Full_DF_Wind.width
            
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
    #print(all_elements)
#     canv_width = Full_DF_Wind.width - 22
#     canv = tk.Canvas(Full_DF_Wind.toplevel, bg = 'white', width = Full_DF_Wind.width - 22, height = Full_DF_Wind.height)
#     canv.place(x = 0, y = 0, anchor = 'nw')

#     #clear text box list


   #populate df_meta entries
    # for index, dataelement in enumerate(master.dfs_metas[master.MainView.currentim.get()]):
    #     #tag
    #     newTB = text_box(toplevel = canv, fontstyle=fontstyle, index=index, dataelement=dataelement, xpos=0, width=canv_width/8, attrib = 'tag',
    #             box_to_add_to = 'meta', view_or_edit = view_or_edit)

    #     #keyword
    #     newTB2 = text_box(toplevel = canv, fontstyle=fontstyle, index=index, dataelement=dataelement, xpos=canv_width/8+1, width=canv_width/8, attrib = 'keyword',
    #             box_to_add_to = 'meta', view_or_edit = view_or_edit)

    #     #value
 
    #     newTB3 = text_box(toplevel = canv, fontstyle=fontstyle, index=index, dataelement=dataelement, xpos=2*canv_width/8+1, width=5*canv_width/8, attrib = 'value',
    #             box_to_add_to = 'meta', view_or_edit = view_or_edit)


    #     #VR
    #     newTB4 = text_box(toplevel = canv, fontstyle=fontstyle, index=index, dataelement=dataelement, xpos=7*canv_width/8+2, width=canv_width/8+2, attrib = 'VR',
    #             box_to_add_to = 'meta', view_or_edit = view_or_edit)

#     global current_length
#     current_length = len(df_meta)

#     #populate df entries
#     for index, dataelement in enumerate(df):

#         #tag
#         newTB = text_box(toplevel = canv, fontstyle=fontstyle, index=index+current_length, dataelement=dataelement, xpos=0, width=canv_width/8, attrib = 'tag',
#                 box_to_add_to = 'regular', view_or_edit = view_or_edit)


#         #keyword
#         newTB2 = text_box(toplevel = canv, fontstyle=fontstyle, index=index+current_length, dataelement=dataelement, xpos=canv_width/8+1, width=canv_width/8, attrib = 'keyword',
#                 box_to_add_to = 'regular', view_or_edit = view_or_edit)
        
#         #value
#         if dataelement.tag != "PixelData":
#             newTB3 = text_box(toplevel = canv, fontstyle=fontstyle, index=index+current_length, dataelement=dataelement, xpos=2*canv_width/8+1, width=5*canv_width/8, attrib = 'value',
#                 box_to_add_to = 'regular', view_or_edit = view_or_edit)
#         else:
#             newTB3 = text_box(toplevel = canv, fontstyle=fontstyle, index=index+current_length, dataelement=dataelement, xpos=2*canv_width/8+1, width=5*canv_width/8, attrib = 'value',
#                 box_to_add_to = 'regular', view_or_edit = view_or_edit, disabled = True)

#         #VR
#         newTB4 = text_box(toplevel = canv, fontstyle=fontstyle, index=index+current_length, dataelement=dataelement, xpos=7*canv_width/8+2, width=canv_width/8+2, attrib = 'VR',
#                 box_to_add_to = 'regular', view_or_edit = view_or_edit)

    

#     if view_or_edit == 'edit':
#         #Save or revert canvas  
#         save_or_revert_canv = tk.Canvas(Full_DF_Wind.toplevel, bg = 'grey', bd = 0, highlightthickness=0)
#         save_or_revert_canv.place(x = 0, y = Full_DF_Wind.height - buffer, width = Full_DF_Wind.width - 18, height = buffer, anchor = 'nw')
#         #save button
#         global save_button
#         save_button = tk.Button(save_or_revert_canv, text = "Save Changes", bg = 'black', fg = 'black', 
#                                 state = tk.DISABLED, command  = produce_just_one_or_all_files_window)
#         save_button.place(relx = 0.25, rely = 0.5, relwidth = 0.3, relheight = 0.5, anchor = 'center')
#         #revert button
#         global revert_button
#         revert_button = tk.Button(save_or_revert_canv, text = "Revert Back to Original", bg = 'black', fg = 'black', 
#                                 state = tk.DISABLED, command= revert)
#         revert_button.place(relx = 0.75, rely = 0.5, relwidth = 0.3, relheight = 0.5, anchor = 'center')

#         #create objects for final save changes window
#         global just_one_or_all_files
#         just_one_or_all_files = TopLevelWindow.top_window(rootcopy, width = 400, height=100, title = "Save Changes", color = 'grey')
#         just_one_or_all_files.toplevel.withdraw()

#         global option
#         option = tk.StringVar()

#         global just_one
#         just_one = tk.Radiobutton(just_one_or_all_files.toplevel, text = 'Just for ' + image_name, variable = option, value = "Just One",
#         bg = 'grey', fg = 'black', font = text_box.fontstyle)
#         just_one.select()

#         global all
#         all = tk.Radiobutton(just_one_or_all_files.toplevel, text = 'All Files', variable = option, value = "All", 
#         bg = 'grey', fg = 'black', font = text_box.fontstyle)
        
#         global final_save_changes
#         final_save_changes = tk.Button(just_one_or_all_files.toplevel, text = "Save Changes", bg = 'black', fg = 'black')

#     #configure scroll bar to and from
#     global scroll_bar_to_
#     scroll_bar_to_ = len(text_box.list_of_boxes)
#     scrollbar.config(to = scroll_bar_to_)
#     scrollbar.config(from_ = 0)

#     #configure canvas length
#     global canv_length
#     canv_length = text_box.height * (len(df) + len(df_meta))
#     canv.place_configure(height = canv_length)
#     update_scroll(1)



# def revert():
#     for box in text_box.list_of_boxes:
#         if box.disabled == False:
#             box.element_str.set(box.orig_string)
#     save_button.configure(state = tk.DISABLED)
# def produce_just_one_or_all_files_window():
#     just_one_or_all_files.toplevel.deiconify()
#     just_one.place(relx = 0.33, rely = 0.33, anchor = 'center')
#     all.place(relx = 0.75, rely = 0.33, anchor = 'center')
#     final_save_changes.place(relx = 0.5, rely = 0.66, relwidth = 0.4, relheight = 0.3, anchor = 'center')

# def save_changes_regular(input_df):
    
#     for index, box in enumerate(text_box.regular_boxes):
#         if str(box.orig_string) != str(box.element_str.get()):
#             print(hex_key)
#             hex_key = list(input_df.keys())[box.index - current_length]
#             # if box.attrib  =="tag":
#             #     input_df[hex_key].tag = box.element_str.get()
#             if box.attrib  =="keyword":
#                 input_df[hex_key].keyword = box.element_str.get()
#             elif box.attrib  =="value":
#                 input_df[hex_key].value = str(box.element_str.get())
#             elif box.attrib  =="VR":
#                 input_df[hex_key].VR = box.element_str.get()  
                
#     return input_df
# def save_changes_meta(input_df):
    
#     for index, box in enumerate(text_box.meta_boxes):
#         if box.orig_string != box.element_str.get():
#             hex_key = list(input_df.keys())[box.index]
#             # if box.attrib  =="tag":
#             #     input_df[hex_key].tag = box.element_str.get()
#             if box.attrib  =="keyword":
#                 input_df[hex_key].keyword = box.element_str.get()
#             elif box.attrib  =="value":
#                 input_df[hex_key].value = str(box.element_str.get())
#             elif box.attrib  =="VR":
#                 input_df[hex_key].VR = box.element_str.get()  
                
#     return input_df