import tkinter as tk
import EditWindows.EditWindow as EditWindow
import CustomThings.CustomCanvas as CustomCanvas
import CustomThings.CustomButton as CustomButton
import CustomThings.TopLevelWindow as TopLevelWindow
import CustomThings.CustomEntry as CustomEntry
import Cascades.AddingElements as AddingElements


class EditAddDelete(EditWindow.EditWindow):
    def __init__(self, master, title):
        super().__init__(master, title)
        self.delete_column_width = 0.05   

        self.avoid_list = ['PixelData', 'SliceThickness', 'PixelSpacing', 'TransferSyntaxUID', 
                                'SamplesPerPixel', 'BitsAllocated', 'Rows', 'Columns', 'PixelRepresentation',
                                'PhotometricInterpretation', 'BitsStored']
                               
   
        self.define_canvases_and_elements()

        self.show_canvas()


    def define_canvases_and_elements(self, elements_width = 1, radio_buttons = None, mode = 'regular'):
        self.display_canvases = {}
        self.display_elements = {}


        #create hex keys
        self.hex_5_digit_keys = list(self.master.display_strings[str(self.master.MainView.currentim.get())].keys())
        
        #create titles
        self.titles = []
        for hex_key in self.hex_5_digit_keys:
            self.titles.append("Group Number: " + hex_key)
        for index_of_catagory, key in enumerate(self.hex_5_digit_keys):
            #create canvas
            self.display_canvases[key] = CustomCanvas.CustomCanv(master = self.master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = CustomEntry.CustomEntryClass.defaultidlecolor, relposx = 0, relposy = 0, relwidth = 1, relheight = 0.9)
            
            #create elements
            self.display_elements[key] = []
            for element in self.all_elements:
                if str(element.tag)[1:5] == key:
                    self.display_elements[key].append(element)

            self.populate_canvas(key = key, canvas = self.display_canvases[key], elements = self.display_elements[key], elements_width=elements_width, value_enable = "ENABLED", radio_buttons = radio_buttons)


        #indicator and next button canvas
                #indicator canvases
        self.indicator_canvas = CustomCanvas.CustomCanv(master = self.master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = '#%02x%02x%02x' % (130, 130, 130), relposx = 0.5, relposy = 1-(self.lower_canvas_width)/2, relwidth = 1, relheight = self.lower_canvas_width, anchor = 'center')
        self.indicator_canvas.show_self()
            #next button
        self.next_button = CustomButton.Button(master = self.master, root = self.indicator_canvas.canvobject, relx = 0.95, rely = 0.75, relwidth = 0.1, relheight = 0.51, text = "Next",  command = self.show_next,  idleback = 'grey')
        self.next_button.show_self()
            #back button
        self.back_button = CustomButton.Button(master = self.master, root = self.indicator_canvas.canvobject, relx = 0.05, rely = 0.75, relwidth = 0.1, relheight = 0.51, text = "Back",  command = self.show_previous,  idleback = 'grey')
        self.back_button.show_self()  
        self.back_button.disable()        
            #indicator
        self.indicator = tk.Label(self.indicator_canvas.canvobject, bg = '#%02x%02x%02x' % (130, 130, 130), fg = '#%02x%02x%02x' % (240, 240, 240))
        self.indicator.place(relx = 0.5, rely = 0.75, relwidth = 0.06, relheight = 0.5, anchor = 'center')
        self.indicator.config(text = str(self.current_canvas+1) + '/' + str(len(self.display_canvases)))


        #button canvas
        self.button_canvas = CustomCanvas.CustomCanv(master = self.master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = '#%02x%02x%02x' % (20, 20, 20), relposx = 0.5, relposy = 0.925, relwidth = 1, relheight = self.lower_canvas_width/2 + 0.003, anchor = 'center')
        self.button_canvas.show_self()

        butt_idle = '#%02x%02x%02x' % (40, 35, 35)
        disabledb = '#%02x%02x%02x' % (100, 90, 90)

        if mode == 'regular':
                #save changes
            self.save_changes = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 1/8, rely = 0.5, relwidth = 0.25, relheight = 1.1, text = "Save Changes",  command = self.decide_save_changes, 
                        state = "DISABLED", idleback = butt_idle, disabledback = disabledb)
                #revert changes
            self.revert_changes = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 3/8, rely = 0.5, relwidth = 0.25, relheight = 1.1,text = "Revert Changes",  command = self.revert_changes_func, 
                        state = "DISABLED", idleback = butt_idle, disabledback = disabledb)
                #add element
            self.add_el = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 5/8, rely = 0.5, relwidth = 0.25, relheight = 1.1, text = "Add Element",  command = self.load_add_element, 
                    state = "ENABLED", idleback = butt_idle, disabledback = disabledb)
                #delete element
            self.delete_el = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 7/8, rely = 0.5, relwidth = 0.25, relheight = 1.1, text = "Delete Element(s)",  command = self.load_delete_elements, 
                    state = "ENABLED", idleback = butt_idle, disabledback = disabledb)
        elif mode == "delete":
                #select all
            self.select_all = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 0.25, rely = 0.5, relwidth = 0.5, relheight = 1.1, text = "Select All",  command = self.select_all_func, 
                    state = "ENABLED", idleback = butt_idle, disabledback = disabledb)
                #delete element
            self.delete_all = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 0.75, rely = 0.5, relwidth = 0.5, relheight = 1.1, text = "Delete Element(s)",  command = self.decide_delete, 
                    state = "DISABLED", idleback = butt_idle, disabledback = disabledb)

            self.title = tk.Label(self.Full_DF_Wind.toplevel, bg = 'grey', text = 'Select Elements to be deleted')
            self.title.place(x = 0, relwidth = 1, y = 0, height = CustomEntry.CustomEntryClass.height)                    
    def hide_canvases_and_elements(self):
        self.button_canvas.canvobject.place_forget()
        self.indicator_canvas.canvobject.place_forget()
        #hide canvas
        for key, canvas in self.display_canvases.items():
            canvas.canvobject.place_forget()
    
    def decide_save_changes(self):    
        TopLevelWindow.just_one_or_many(master = self.master, root = self.Full_DF_Wind.toplevel, message = "Save Changes For ",
                proceed_command = self.final_save_changes)
            
    def final_save_changes(self,one_or_all):
        image_indeces = [] 
        if one_or_all == "Just One":
            image_indeces.append(self.master.MainView.currentim.get())
        elif one_or_all == "All":
            for index in range(0, len(self.master.MainView.arr)):
                image_indeces.append(index)
        errorflag = self.savechangescascade.save_from_boxes(input_full_df_cascade = self, image_indexes = image_indeces, box_list=self.entries)
        if errorflag == False:
            self.show_new_df()
            
    def load_delete_elements(self):
        self.loading_window, self.loading_bar = TopLevelWindow.loading_win(master = self.master, root = self.Full_DF_Wind.toplevel,
                    number_of_loads = 4, message = "One Moment Please")
        self.loading_bar.increase_width()


        self.hide_canvases_and_elements()
        self.loading_bar.increase_width()        


        self.define_canvases_and_elements(elements_width=1-self.delete_column_width, radio_buttons=[{'relx':(1-self.delete_column_width/2), 'text': None}], mode = 'delete')
        self.loading_bar.increase_width()

        self.show_canvas()
        self.loading_bar.increase_width()        
        self.loading_window.toplevel.destroy()

    def revert_changes_func(self):
        for index, box in enumerate(self.entries):
            if box.orig_string != box.text.get():
                box.text.set(box.orig_string)
                box.show_self()
        self.save_changes.disable()
        self.revert_changes.disable()    

    def select_all_func(self):
        for radiobutton in self.delete_radio_buttons[self.hex_5_digit_keys[self.current_canvas]]:
            radiobutton.change_to_pressed(6)
    def decide_delete(self):
        TopLevelWindow.just_one_or_many(master = self.master, root = self.Full_DF_Wind.toplevel, message = "Save Changes for ", proceed_command=self.final_delete)

    def final_delete(self, o_a):
        self.delete_cascade.set_delete_elements(self.all_delete_buttons)
        self.delete_cascade.final_delete(o_a)
    def load_add_element(self):

        self.add_element_top_window = TopLevelWindow.top_window(master = self.master, root = self.Full_DF_Wind.toplevel,
                    width = 1000, height = 500, title = "Add Element", color = 'grey')
        enter_element_below = tk.Label(self.add_element_top_window.toplevel, bg = 'grey', fg= 'white', 
            text = "Enter Element Details Below", font =(self.master.fontstyle, 20))
        enter_element_below.place(relx = 0.5 ,rely = 0.2, anchor = 'center', relwidth = 0.8, relheight = 0.2)

        enter_element_below_tag = tk.Label(self.add_element_top_window.toplevel, bg = 'grey', fg= 'white', 
            text = "Please Enter Group Number and Element Number in hexidecimal", font =(self.master.fontstyle, 15))
        enter_element_below_tag.place(relx = 0.5 ,rely = 0.35, anchor = 'center', relwidth = 0.8, relheight = 0.2)        
        



        example_tag = tk.Label(self.add_element_top_window.toplevel, bg = 'grey', fg = 'white', text = 'Example: 0010', font = (self.master.fontstyle, 10))
        example_tag.place(relx = 0.1, rely = 0.6, anchor = 'center')
        example_tag = tk.Label(self.add_element_top_window.toplevel, bg = 'grey', fg = 'white', text = 'Example: 0010', font = (self.master.fontstyle, 10))
        example_tag.place(relx = 0.2, rely = 0.6, anchor = 'center')        
        example_value = tk.Label(self.add_element_top_window.toplevel, bg = 'grey', fg = 'white', text = 'Example: John Smith', font = (self.master.fontstyle, 10))
        example_value.place(relx = 0.6, rely = 0.6, anchor = 'center')        



        self.add_entry = CustomButton.Button(master = self.master, root = self.add_element_top_window.toplevel,
                relx = 0.5, rely = 0.8, width = 200, height = 50, text = "Add Data Element",  command = self.add_decide, state = "DISABLED")
        self.add_entry.show_self()

        self.group_number_entry = AddingElements.add_element_entry(master = self.master, parent_cascade = self, root = self.add_element_top_window.toplevel,
                                startval = "Group Number", relx = 0.1, relwidth = 0.1)

        self.element_number_entry = AddingElements.add_element_entry(master = self.master, parent_cascade = self, root = self.add_element_top_window.toplevel,
                                startval = "Element Number", relx = 0.2, relwidth = 0.1)                                

        self.group_number_entry.partner = self.element_number_entry
        self.element_number_entry.partner = self.group_number_entry
        
        
        
        self.Value_Entry = AddingElements.add_element_entry(master = self.master, parent_cascade = self,root = self.add_element_top_window.toplevel,
                                startval = "Value", relx = 0.6, relwidth = 0.7, form = 'string')

    def add_decide(self):
        TopLevelWindow.just_one_or_many(master=self.master, root =self.Full_DF_Wind.toplevel
            , message = "Add Element for Just " + str(self.master.image_names[self.master.MainView.currentim.get()]) + " or for all files?", 
            proceed_command = self.add_element_cascade.add)
