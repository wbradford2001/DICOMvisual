

import tkinter as tk
import numpy as np
import CustomEntry



import TopLevelWindow
import CustomCanvas
import CustomButton
import master_funcs
import SaveChanges
import CustomRadioButton
import DeletingElements
import AddingElements
import AnonymizeDataBase





class full_df_cascade:
    def __init__(self, master):
        self.current_data_box = 0
        self.master = master
    def create_full_df_toplevel(self,view_or_edit):
        self.delete_cascade = DeletingElements.delete_cascade()
        self.view_or_edit = view_or_edit
        if self.view_or_edit == "view" or self.view_or_edit == "anonymize":
            self.value_enabled_or_disabled = "view"
        elif self.view_or_edit == "edit":
            self.value_enabled_or_disabled = "ENABLED"

        self.current_data_box = 0
        self.checked_boxes = []

        
        #create window
        if self.view_or_edit != "anonymize":
            title = "Full Data Frame: " + self.master.image_names[self.master.MainView.currentim.get()]
        else:
            title = "Anonymize Data Set"
        window_width = 1000
        window_height = 500
        self.Full_DF_Wind = TopLevelWindow.top_window(master = self.master, root = self.master.root, width = window_width, height=window_height, title = title, color =CustomEntry.CustomEntryClass.defaultidlecolor)
        
        #create scale
        self.scale_val = tk.IntVar()
        self.scale = tk.Scale(self.Full_DF_Wind.toplevel, bg = CustomEntry.CustomEntryClass.defaultidlecolor, borderwidth=0, command = self.move_canvas, from_= 0, to = 10,
                sliderlength=200, variable = self.scale_val)
        self.Full_DF_Wind.toplevel.bind('<MouseWheel>', self.set_scale_from_mouse_wheel)

        #combine DFS and meta DFS
        self.all_elements = list(self.master.dfs_metas[self.master.MainView.currentim.get()])
        self.all_elements.extend(list(self.master.dfs[self.master.MainView.currentim.get()])) 
        if self.view_or_edit == "anonymize":
            self.new_elements = self.all_elements.copy()
            self.new_elements.clear()
            for element in self.all_elements:
                print(str(element.tag))
                print(str(element.tag) == '(0010, 0010)')
                if str(element.tag) in AnonymizeDataBase.anonymizable:
                    print("Hey")
                    self.new_elements.append(element)
                    
            print(len(self.new_elements))
            self.all_elements = self.new_elements.copy()
        #filter if anonymizing
        
        self.display_canvases = {}
        #create canvases


        CustomEntry.CustomEntryClass.boxes_so_far.clear()
        if view_or_edit != "anonymize":
            #create canvases
            self.hex_5_digit_keys = list(self.master.display_strings[str(self.master.MainView.currentim.get())].keys())
            for index_of_catagory, key in enumerate(self.hex_5_digit_keys):
                self.display_canvases[key] = CustomCanvas.CustomCanv(master = self.master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = CustomEntry.CustomEntryClass.defaultidlecolor, relposx = 0, relposy = 0, relwidth = 1, relheight = 0.9)
            


            #populate each canvas

            for key, canvas in self.display_canvases.items():
                self.populate_canvas(key, canvas)
            self.define_indicators_and_button()
        elif view_or_edit == "anonymize":
            self.maincanvas = CustomCanvas.CustomCanv(master = self.master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = CustomEntry.CustomEntryClass.defaultidlecolor, relposx = 0, relposy = 0, relwidth = 1, relheight = 0.9)
            self.populate_canvas('none', self.maincanvas)
            self.maincanvas.show_self()
            self.show_canvas()
            self.top_label = tk.Label(self.Full_DF_Wind.toplevel, bg = 'grey', fg = 'white', 
                text = 'The following data elements must be anonymized')
            self.top_label.place(x=0, y=0, relwidth = 1, height = CustomEntry.CustomEntryClass
            .height)
            

    def define_indicators_and_button(self):

        #indicator canvases
        self.indicator_canvas = CustomCanvas.CustomCanv(master = self.master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = '#%02x%02x%02x' % (130, 130, 130), relposx = 0.5, relposy = 0.975, relwidth = 1, relheight = .05, anchor = 'center')
        self.indicator_canvas.show_self()
            #next button
        self.next_button = CustomButton.Button(master = self.master, root = self.indicator_canvas.canvobject, relx = 0.95, rely = 0.5, width = 0.1*self.Full_DF_Wind.width, height = 50, text = "Next",  command = self.show_next,  idleback = 'grey')
        self.next_button.show_self()
            #back button
        self.back_button = CustomButton.Button(master = self.master, root = self.indicator_canvas.canvobject, relx = 0.05, rely = 0.5, width = 0.1*self.Full_DF_Wind.width, height = 50, text = "Back",  command = self.show_previous,  idleback = 'grey')
        self.back_button.show_self()  
        self.back_button.disable()        
            #indicator
        self.indicator = tk.Label(self.indicator_canvas.canvobject, bg = '#%02x%02x%02x' % (130, 130, 130), fg = '#%02x%02x%02x' % (240, 240, 240))
        self.indicator.place(relx = 0.5, rely = 0.5, relwidth = 0.06, height = 50, anchor = 'center')
        self.indicator.config(text = str(self.current_data_box+1) + '/' + str(len(self.display_canvases)))


        #show first canvas
        self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].show_self()

        #In edit mode
        if self.view_or_edit == 'edit':
            #button canvas
            self.button_canvas = CustomCanvas.CustomCanv(master = self.master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = '#%02x%02x%02x' % (20, 20, 20), relposx = 0.5, relposy = 0.925, relwidth = 1, relheight = .05, anchor = 'center')
            self.button_canvas.show_self()

            butt_idle = '#%02x%02x%02x' % (40, 35, 35)
            disabledb = '#%02x%02x%02x' % (100, 90, 90)
                #save changes
            self.save_changes = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 1/8, rely = 0.5, width = 0.25*self.Full_DF_Wind.width, height = 50, text = "Save Changes",  command = self.decide_save_changes, 
                     state = "DISABLED", idleback = butt_idle, disabledback = disabledb)
                #revert changes
            self.revert_changes = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 3/8, rely = 0.5, width = 0.25*self.Full_DF_Wind.width, height = 50, text = "Revert Changes",  command = self.revert_changes_func, 
                     state = "DISABLED", idleback = butt_idle, disabledback = disabledb)
                #add element
            self.add_el = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 5/8, rely = 0.5, width = 0.25*self.Full_DF_Wind.width, height = 50, text = "Add Element",  command = self.add_element, 
                    state = "ENABLED", idleback = butt_idle, disabledback = disabledb)
                #delete element
            self.delete_el = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 7/8, rely = 0.5, width = 0.25*self.Full_DF_Wind.width, height = 50, text = "Delete Element(s)",  command = self.delete_element, 
                    state = "ENABLED", idleback = butt_idle, disabledback = disabledb)
        #In edit mode
        if self.view_or_edit == 'delete':
            #button canvas
            self.button_canvas = CustomCanvas.CustomCanv(master = self.master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = '#%02x%02x%02x' % (20, 20, 20), relposx = 0.5, relposy = 0.925, relwidth = 1, relheight = .05, anchor = 'center')
            self.button_canvas.show_self()

            butt_idle = '#%02x%02x%02x' % (40, 35, 35)
            disabledb = '#%02x%02x%02x' % (100, 90, 90)
                #save changes
            self.save_changes = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 0.25, rely = 0.5, 
                width = self.Full_DF_Wind.width * 0.5, height = 50, text = "Delete Element(s)", 
                    command = lambda: self.delete_cascade.Delete_From_Button_List(self.master, self, self.checked_boxes), 
                    state = "DISABLED", idleback = butt_idle, disabledback = disabledb)
                #revert changes
            self.select_all = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 0.75, rely = 0.5, width = 0.5*self.Full_DF_Wind.width, height = 50, text = "Select All", command = self.select_all_boxes, 
                    state = "ENABLED", idleback = butt_idle, disabledback = disabledb)
                #add element
                  
    
        self.show_canvas()   
    def hide_indicators_and_button(self):
                #indicator canvases
        self.indicator_canvas.hide_self()



        #hide canvas
        for key, canvas in self.display_canvases.items():
            canvas.canvobject.place_forget()

        #In edit mode
        if self.view_or_edit == 'edit':
            #button canvas
            self.button_canvas.hide_self()


        #In edit mode 
    def populate_canvas(self, key, canvas):
            #get length of canvas ahead of time
            predicted_y_level = 1
            for item in self.all_elements:
                if (str(item.tag)[1:5]) == key:
                    predicted_y_level += 1

            #EDIT
            if self.view_or_edit == "edit" or self.view_or_edit == "delete":
                if (CustomEntry.CustomEntryClass.height * predicted_y_level)/self.Full_DF_Wind.height > 0.9:
                    total_length = self.Full_DF_Wind.width -15
                else:
                    total_length = self.Full_DF_Wind.width

            #VIEW
            elif self.view_or_edit == "view" or self.view_or_edit == "anonymize":
                if (CustomEntry.CustomEntryClass.height * predicted_y_level)/self.Full_DF_Wind.height > 0.95:
                    total_length = self.Full_DF_Wind.width -15
                else:
                    total_length = self.Full_DF_Wind.width


            if self.view_or_edit == "edit" or self.view_or_edit == "view":
                delete_box_width = 0
            elif self.view_or_edit == "delete":

                delete_box_width = total_length * 0.05
                self.delete_menu = CustomRadioButton.RadioMenu(master = self.master, root = canvas.canvobject, 
                    background_color=CustomEntry.CustomEntryClass.defaultidlecolor, height = CustomEntry.CustomEntryClass.height,
                        width = CustomEntry.CustomEntryClass.height, exclusive = False, idleback = CustomEntry.CustomEntryClass.defaultidlecolor,
                        pressed_object_size_reduce=19)
            elif self.view_or_edit == "anonymize":
                delete_box_width = total_length * 0.2
                

            tag_length = total_length * 0.15 - delete_box_width/4
            key_word_length = total_length * 0.25- delete_box_width/4
            vr_length = total_length * 0.09 - delete_box_width/4
            value_length = total_length * (1-0.15 - 0.25 - 0.09)- delete_box_width/4
            y_level = 1
            #title
            if self.view_or_edit != "anonymize":
                title = CustomEntry.CustomEntryClass(master = self.master, parent = self, root = self.display_canvases[key].canvobject, index = 0, xpos = 0, width = total_length, 
                    text = "Catagory: (" + (key) + ",____)", 
                    view_or_edit = self.view_or_edit, state = "TITLE")
                title.show_self()

            #elements
            for index, item in enumerate(self.all_elements):
            
                if (str(item.tag)[1:5]) == key or self.view_or_edit == "anonymize":
                    if self.view_or_edit == "view" or self.view_or_edit == "edit" or self.view_or_edit == "anonymize":
                        start_pos = 0
                    elif self.view_or_edit == "delete":
                        start_pos = self.Full_DF_Wind.width * 0.05
                        avoid_list = ['PixelData', 'SliceThickness', 'PixelSpacing', 'TransferSyntaxUID', 
                                'SamplesPerPixel', 'BitsAllocated', 'Rows', 'Columns', 'PixelRepresentation',
                                'PhotometricInterpretation', 'BitsStored']
                        if item.keyword not in avoid_list:
                            New_Button = self.delete_menu.add_button(value = item.tag, xpos = 0.025*self.Full_DF_Wind.width,
                                ypos = CustomEntry.CustomEntryClass.height * y_level + CustomEntry.CustomEntryClass.height/2,
                                text= "", command = self.enable_save_changes, deselect_command = self.disable_save_changes)
                        else:
                            New_Button = self.delete_menu.add_button(value = item.tag, xpos = 0.025*self.Full_DF_Wind.width,
                                ypos = CustomEntry.CustomEntryClass.height * y_level + CustomEntry.CustomEntryClass.height/2,
                                text= "", command = self.enable_save_changes, deselect_command = self.disable_save_changes, state = "DISABLED")
                        self.checked_boxes.append(New_Button)

                    #tag

                    tag = CustomEntry.CustomEntryClass(master = self.master, parent = self, root = canvas.canvobject, index = y_level, xpos = start_pos, width = tag_length, 
                    text = item.tag, 
                    state = "view", element = item, attrib = "tag")
                    tag.show_self()


                    #keyword
                    keyword = CustomEntry.CustomEntryClass(master = self.master, parent = self, root = canvas.canvobject, index = y_level, xpos = start_pos + tag_length, width = key_word_length, 
                    text = item.keyword, 
                    state = "view", element = item, attrib= "keyword")
                    keyword.show_self()


                    #value
                    value = CustomEntry.CustomEntryClass(master = self.master, parent = self, root = canvas.canvobject, index = y_level, xpos = start_pos + tag_length + key_word_length, width = value_length, 
                    text = item.value, 
                    state = self.value_enabled_or_disabled, element = item, attrib = 'value')
                    value.show_self()


                    #VR
                    VR = CustomEntry.CustomEntryClass(master = self.master, parent = self, root = canvas.canvobject, index = y_level, xpos = start_pos + tag_length + key_word_length + value_length, width = vr_length, 
                    text = item.VR, 
                    state = "view", element = item, attrib = 'VR')
                    VR.show_self()


                    y_level += 1

            #set appropriate canvas height
            canvas.relheight = (CustomEntry.CustomEntryClass.height * y_level)/self.Full_DF_Wind.height



    def show_next(self):
        self.back_button.enable()
        #check to be sure you're not at the end
        if self.current_data_box  < len(self.hex_5_digit_keys)-1:
            #hide current canvas
            self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].hide_self()  
            #increment current data box
            self.current_data_box += 1
            self.show_canvas()
            #check to see you're not at the end
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
            #get rid of scale
            self.scale.place_forget()

            #test to see if you need to set the scale
            if self.view_or_edit != "anonymize":
                            #configure indicator
                self.indicator.config(text = str(self.current_data_box+1) + '/' + str(len(self.display_canvases)))
                if self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relheight > 0.9:
                    #set scale to 0
                    self.scale_val.set(0)
                    #adjust width of display canvas
                    self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relwidth = 1 - 15/self.Full_DF_Wind.width
                    #place scale
                    if self.view_or_edit == "edit":
                        self.scale.place(relx = 1, rely = 0, relheight = 0.9, anchor = 'ne')
                    elif self.view_or_edit == "view":
                        self.scale.place(relx = 1, rely = 0, relheight = 0.95, anchor = 'ne')
                    elif self.view_or_edit == "delete":

                        self.scale.place(relx = 1, rely = 0, relheight = 0.90, anchor = 'ne')                    
                self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].show_self()      
            else:
                  if self.maincanvas.relheight > 0.95:
                    #set scale to 0
                    self.scale_val.set(0)
                    #adjust width of display canvas
                    self.maincanvas.relwidth = 1 - 15/self.Full_DF_Wind.width
                    #place scale

                    self.scale.place(relx = 1, rely = 0, relheight = 0.95, anchor = 'ne')                    
                    self.maincanvas.show_self()      

    def move_canvas(self, scroll_to):
        if self.view_or_edit == "view":
            new_func = master_funcs.map_ranges([0, 10], [0, -(self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relheight-0.95)])
        elif self.view_or_edit == "edit" or self.view_or_edit == "delete":
            new_func = master_funcs.map_ranges([0, 10], [0, -(self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relheight-0.90)])
        elif self.view_or_edit == "anonymize":
            new_func = master_funcs.map_ranges([0, 10], [0, -(self.maincanvas.relheight-0.95)])            
        
        if self.view_or_edit != "anonymize":
            self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relposy = new_func(int(self.scale_val.get()))
            self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].show_self() 
        else:
            self.maincanvas.relposy = new_func(int(self.scale_val.get()))            
            self.maincanvas.show_self()

    def set_scale_from_mouse_wheel(self, delta):
        if self.view_or_edit != "anonymize":
            if self.display_canvases[self.hex_5_digit_keys[self.current_data_box]].relheight > 0.9:
                self.scale_val.set(self.scale_val.get() - delta.delta)
                self.move_canvas(9)
        else:
            if self.maincanvas.relheight > 0.9:
                self.scale_val.set(self.scale_val.get() - delta.delta)
                self.move_canvas(9)  


    def decide_save_changes(self):       
        if self.master.multiple_images == True:
            self.just_one_or_many_wind = TopLevelWindow.just_one_or_many(master = self.master, root = self.Full_DF_Wind.toplevel
                        ,message = "Would you like to save changes for just " + str(self.master.image_names[self.master.MainView.currentim.get()]) 
                                    + " or for all files?", image_name = str(self.master.image_names[self.master.MainView.currentim.get()]) ,
                                    proceed_command = self.final_save_changes)

        elif self.master.multiple_images == False:
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

    def revert_changes_func(self):

        for index, box in enumerate(CustomEntry.CustomEntryClass.boxes_so_far):
            if box.orig_string != box.text.get():
                box.text.set(box.orig_string)
                box.show_self()
        self.save_changes.disable()
        self.revert_changes.disable()        


    def add_element(self):
        self.add_element_top_window = TopLevelWindow.top_window(master = self.master, root = self.Full_DF_Wind.toplevel,
                    width = 1000, height = 500, title = "Add Element", color = 'grey')
        enter_element_below = tk.Label(self.add_element_top_window.toplevel, bg = 'grey', fg= 'white', 
            text = "Enter Element Details Below", font =(self.master.fontstyle, 20))
        enter_element_below.place(relx = 0.5 ,rely = 0.2, anchor = 'center', relwidth = 0.8, relheight = 0.2)

        enter_element_below_tag = tk.Label(self.add_element_top_window.toplevel, bg = 'grey', fg= 'white', 
            text = "Please Enter Group Number and Element Number in hexidecimal", font =(self.master.fontstyle, 15))
        enter_element_below_tag.place(relx = 0.5 ,rely = 0.35, anchor = 'center', relwidth = 0.8, relheight = 0.2)        
        
        self.add_element_cascade = AddingElements.add_element_cascade(master = self.master, parent_cascade = self)



        example_tag = tk.Label(self.add_element_top_window.toplevel, bg = 'grey', fg = 'white', text = 'Example: 0010', font = (self.master.fontstyle, 10))
        example_tag.place(relx = 0.1, rely = 0.6, anchor = 'center')
        example_tag = tk.Label(self.add_element_top_window.toplevel, bg = 'grey', fg = 'white', text = 'Example: 0010', font = (self.master.fontstyle, 10))
        example_tag.place(relx = 0.2, rely = 0.6, anchor = 'center')        
        example_value = tk.Label(self.add_element_top_window.toplevel, bg = 'grey', fg = 'white', text = 'Example: John Smith', font = (self.master.fontstyle, 10))
        example_value.place(relx = 0.6, rely = 0.6, anchor = 'center')        



        self.add_entry = CustomButton.Button(master = self.master, root = self.add_element_top_window.toplevel,
                relx = 0.5, rely = 0.8, width = 200, height = 50, text = "Add Data Element",  command = self.add_element_cascade.add_decide, state = "DISABLED")
        self.add_entry.show_self()

        self.group_number_entry = AddingElements.add_element_entry(master = self.master, parent_cascade = self, root = self.add_element_top_window.toplevel,
                                startval = "Group Number", relx = 0.1, relwidth = 0.1)

        self.element_number_entry = AddingElements.add_element_entry(master = self.master, parent_cascade = self, root = self.add_element_top_window.toplevel,
                                startval = "Element Number", relx = 0.2, relwidth = 0.1)                                

        self.group_number_entry.partner = self.element_number_entry
        self.element_number_entry.partner = self.group_number_entry
        
        
        
        self.Value_Entry = AddingElements.add_element_entry(master = self.master, parent_cascade = self,root = self.add_element_top_window.toplevel,
                                startval = "Value", relx = 0.6, relwidth = 0.7, form = 'string')

    def delete_element(self):
        self.load_win, self.load_bar = TopLevelWindow.loading_win(master = self.master, root = self.Full_DF_Wind.toplevel, 
            number_of_loads = 2 + len(self.hex_5_digit_keys)+ len(self.display_canvases), message = "One Moment Please")
        self.load_win.toplevel.update()
        self.load_bar.increase_width()
        self.value_enabled_or_disabled = "view"
        self.view_or_edit = "delete"
        CustomEntry.CustomEntryClass.boxes_so_far.clear()
        self.hide_indicators_and_button()
        self.display_canvases = {}
        for index_of_catagory, key in enumerate(self.hex_5_digit_keys):
            self.load_bar.increase_width()
            self.display_canvases[key] = CustomCanvas.CustomCanv(master = self.master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = CustomEntry.CustomEntryClass.defaultidlecolor, relposx = 0, relposy = 0, relwidth = 1, relheight = 0.9)
        
        for key, canvas in self.display_canvases.items():
            self.load_bar.increase_width()
            self.populate_canvas(key, canvas)

        #FIX ME: unplace all current menu items
        self.define_indicators_and_button()
        self.load_bar.increase_width()
        self.load_win.toplevel.destroy()

    def enable_save_changes(self):
      
        self.save_changes.enable()
    def disable_save_changes(self):
        print(len(self.checked_boxes))
        box_pressed = False
        for box in self.checked_boxes:
            if box.pressed == True:
                box_pressed = True
                break
                
        if box_pressed == False:
            self.save_changes.disable()



    def select_all_boxes(self):
        for box in self.checked_boxes:
            if (str(box.value)[1:5]) == self.hex_5_digit_keys[self.current_data_box]:
                box.change_to_pressed(3)
