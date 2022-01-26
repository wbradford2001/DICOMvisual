import tkinter as tk
import CustomThings.TopLevelWindow as TopLevelWindow
import CustomThings.CustomEntry as CustomEntry
import master_funcs
import Cascades.SaveChanges as SaveChanges
import CustomThings.CustomRadioButton as CustomRadioButton
import Cascades.DeletingElements as DeletingElements
import Cascades.AddingElements as AddingElements


class EditWindow:
    window_width = 1000
    window_height = 500
    def __init__(self, master, title):
        



        self.master = master
        self.title = title
        self.Full_DF_Wind = TopLevelWindow.top_window(master = self.master, root = self.master.root, width = EditWindow.window_width, height=EditWindow.window_height, title = title, color =CustomEntry.CustomEntryClass.defaultidlecolor)
        self.Full_DF_Wind.toplevel.bind('<MouseWheel>', self.set_scale_from_mouse_wheel)
        
        self.all_elements = list(self.master.dfs_metas[self.master.MainView.currentim.get()])
        self.all_elements.extend(list(self.master.dfs[self.master.MainView.currentim.get()])) 
        self.current_canvas = 0
        self.lower_canvas_width = 0.1
        self.entries = []
        self.universal_size_reduce = 0.6
        self.delete_radio_buttons = {}
        self.edit_radio_buttons = {}
        self.all_delete_buttons = []
        self.all_edit_buttons = []    
        self.title = tk.Label(self.Full_DF_Wind.toplevel, bg = 'grey', fg = 'white')
    


        #create scale
        self.scale_val = tk.IntVar()
        self.scale = tk.Scale(self.Full_DF_Wind.toplevel, bg = CustomEntry.CustomEntryClass.defaultidlecolor, borderwidth=0, command = self.move_canvas, from_= 0, to = 10,
                sliderlength=200, variable = self.scale_val)


        self.savechangescascade = SaveChanges.save_cascade(master = self.master)
        self.delete_cascade = DeletingElements.delete_cascade(master = self.master, parent_cascade = self)
        self.add_element_cascade = AddingElements.add_element_cascade(master = self.master, parent_cascade = self)



    def populate_canvas(self, key, canvas, elements, elements_width, value_enable, radio_buttons,start_y_level = 1):
        
        self.delete_radio_buttons[key] = []
        self.edit_radio_buttons[key] = []        

        #predict height
        future_height = (len(elements) +start_y_level )* CustomEntry.CustomEntryClass.height
        canvas.relheight = future_height/self.Full_DF_Wind.height
        if canvas.relheight > 1-self.lower_canvas_width:
            canvas.relwidth = 1 - 15/self.Full_DF_Wind.width


        # if title == None:
        #     y_level = 0
        # else:
          
        #     title = CustomEntry.CustomEntryClass(master = self.master, parent = self, root = canvas.canvobject, text = title, state = "TITLE",
        #                 relx = 0, relwidth = 1, y = 0)
        #     title.show_self()            
        y_level = start_y_level
        tag_width = elements_width * 0.15
        keyword_width = elements_width * 0.25
        value_width = elements_width * (1-0.15-0.1-0.25)
        VR_width = elements_width * 0.1              
        for element in elements:

            #tag
            tag_entry = CustomEntry.CustomEntryClass(master = self.master, parent = self, root = canvas.canvobject, text = element.tag, state = "view", element = element, attrib = "tag",
                        relx = 0, relwidth = tag_width, y = y_level * CustomEntry.CustomEntryClass.height)
            tag_entry.show_self()

            #keyword
            keyword_entry = CustomEntry.CustomEntryClass(master = self.master, parent = self, root = canvas.canvobject, text = element.keyword, state = "view", element = element, attrib = "keyword",
                        relx = tag_width, relwidth = keyword_width, y = y_level * CustomEntry.CustomEntryClass.height)
            keyword_entry.show_self()

            #value
            value_entry = CustomEntry.CustomEntryClass(master = self.master, parent = self, root = canvas.canvobject, text = element.value, state = value_enable, element = element, attrib = "value",
                        relx = tag_width + keyword_width, relwidth = value_width, y = y_level * CustomEntry.CustomEntryClass.height)
            value_entry.show_self()
            self.entries.append(value_entry)

            #VR
            VR_entry = CustomEntry.CustomEntryClass(master = self.master, parent = self, root = canvas.canvobject, text = element.VR, state = "view", element = element, attrib = "VR",
                        relx = tag_width + keyword_width + value_width, relwidth = VR_width, y = y_level * CustomEntry.CustomEntryClass.height)
            VR_entry.show_self()

            if radio_buttons != None:
                Menu = CustomRadioButton.RadioMenu(master = self.master, root = canvas.canvobject, background_color='grey',
                        relheight = CustomEntry.CustomEntryClass.height/(canvas.relheight * self.Full_DF_Wind.height), relwidth = CustomEntry.CustomEntryClass.height/(canvas.relwidth * self.Full_DF_Wind.width), pressed_object_size_reduce=  self.universal_size_reduce, exclusive=True, size_reduce=0) 
                for index, radio_button in enumerate(radio_buttons):
                    if element.keyword not in self.avoid_list:
                        NewButton = Menu.add_button(value = element.tag, 
                            relx = radio_button['relx'], 
                            rely = ((y_level * CustomEntry.CustomEntryClass.height)+CustomEntry.CustomEntryClass.height/2)/(canvas.relheight * self.Full_DF_Wind.height),
                            text=radio_button['text'], command = self.check_if_boxes_checked, deselect_command = self.check_if_boxes_checked, state = "ENABLED", selected = False, anchor = 'center')
                    else:
                        NewButton = Menu.add_button(value = element.tag, 
                            relx = radio_button['relx'], 
                            rely = ((y_level * CustomEntry.CustomEntryClass.height)+CustomEntry.CustomEntryClass.height/2)/(canvas.relheight * self.Full_DF_Wind.height),
                            text=radio_button['text'], command = self.check_if_boxes_checked, deselect_command = self.check_if_boxes_checked, state = "DISABLED", selected = False, anchor = 'center')
                    if radio_button['text'] == None:
                        self.delete_radio_buttons[key].append(NewButton)
                        self.all_delete_buttons.append(NewButton) 
                    if radio_button['text'] == 'Entry':
                        self.edit_radio_buttons[key].append(NewButton)                          
                        self.all_edit_buttons.append(NewButton)   
                        NewButton.entry_text.set(str(element.value)) 
                        NewButton.orig_string = str(element.value)
                        NewButton.element = element    

            y_level += 1
        
    
    def show_canvas(self):
        self.scale.place_forget()
        self.title.destroy()

        self.indicator.config(text = str(self.current_canvas+1) + '/' + str(len(self.display_canvases)))
        self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].show_self() 


        self.title = tk.Label(self.Full_DF_Wind.toplevel, bg = 'grey', fg = 'white', text =self.titles[self.current_canvas])


        if self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].relheight > 1- self.lower_canvas_width:
            self.scale.set(0)
            self.scale.config(sliderlength=1/(self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].relheight)* 200)
            self.scale.place(relx = 1, rely = 0, relheight = 0.9, anchor = 'ne')
            self.title.place(x=0, y=0, relwidth = 1 - 15/self.Full_DF_Wind.width, height = CustomEntry.CustomEntryClass.height)
        else:
            self.title.place(x=0, y=0, relwidth = 1, height = CustomEntry.CustomEntryClass.height)


    
            

    def show_next(self):
        if self.current_canvas < len(self.hex_5_digit_keys)-1:
            self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].hide_self()        
            self.back_button.enable()
            self.current_canvas += 1
            self.show_canvas()
            if self.current_canvas == len(self.hex_5_digit_keys)-1:
                self.next_button.disable()            


    def show_previous(self):

        if self.current_canvas > 0: 
            self.next_button.enable()               
            self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].hide_self()        
            self.current_canvas -= 1      
            self.show_canvas()    
            if self.current_canvas == 0:
                self.back_button.disable()   

    def move_canvas(self, scroll_to):
        new_func = master_funcs.map_ranges([0, 10], [0, -(self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].relheight-(1-self.lower_canvas_width))])
        self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].relposy = new_func(int(self.scale_val.get()))
        self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].show_self() 

    def set_scale_from_mouse_wheel(self, delta):
        if self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].relheight > (1-self.lower_canvas_width):
            self.scale_val.set(self.scale_val.get() - delta.delta)
            self.move_canvas(9)


    def show_new_df(self):
        self.Full_DF_Wind.toplevel.destroy()
        self.master.hide_all()
        self.master.load(from_existing_df = True)


    def check_if_boxes_checked(self):
        somethingpressed = False
        for radiocatagory in self.delete_radio_buttons.values():
            if somethingpressed == False:
                for radiobutton in radiocatagory:
                    if radiobutton.pressed == True:
                        somethingpressed = True
                        break

        if somethingpressed == True:
            self.delete_all.enable()
        elif somethingpressed == False:
            self.delete_all.disable()