import tkinter as tk
import EditWindows.EditWindow as EditWindow
import CustomThings.CustomCanvas as CustomCanvas
import CustomThings.CustomButton as CustomButton
import CustomThings.TopLevelWindow as TopLevelWindow
import CustomThings.CustomEntry as CustomEntry
import master_funcs
import DataBaseStuff.AnonymizeDataBase as AnonymizeDataBase
import DataBaseStuff.knownelements as knownelements


class AnonymizeDF(EditWindow.EditWindow):
    def __init__(self, master, title):
        super().__init__(master, title)

        #populate anonymizable elements
        self.appendixEelements = []
        for element in self.all_elements:
            if str(element.tag).upper() in AnonymizeDataBase.anonymizable or str(element.tag)[1:3] == "50":
            
                
                self.appendixEelements.append(element) 

        #populate private elements
        self.private_elements = []
        for element in self.all_elements:
            if (((str(element.tag).upper() not in knownelements.elements))):
               
                self.private_elements.append(element)

        



        

        # if ((len(self.anonymizable_elements) + 1) * CustomEntry.CustomEntryClass.height)/self.Full_DF_Wind.height > 0.9:
        #     total_length = (1-15/self.Full_DF_Wind.width)*self.Full_DF_Wind.width

            
        # else:
        total_length = self.Full_DF_Wind.width
          
        self.relative_ceh = (CustomEntry.CustomEntryClass.height)/total_length           
        self.delete_column_width = 0.4
        self.delete_column_bounds = [1-self.delete_column_width, 1-self.delete_column_width + 2 * self.relative_ceh]

        self.avoid_list = ['PixelData', 'SliceThickness', 'PixelSpacing', 'TransferSyntaxUID', 
                                'SamplesPerPixel', 'BitsAllocated', 'Rows', 'Columns', 'PixelRepresentation',
                                'PhotometricInterpretation', 'BitsStored']

        self.delete_buttons_pos = ((self.delete_column_bounds[0]  + self.delete_column_bounds[1] )/(2) ) 


        self.define_canvases_and_elements(elements_width = 1-self.delete_column_width , radio_buttons = [{'relx': self.delete_buttons_pos, 'text': None}, {'relx': self.delete_column_bounds[1] + self.relative_ceh, 'text': 'Entry'}])
        for button in self.all_delete_buttons:
            button.change_to_pressed(5)

        self.show_canvas()
  

    def define_canvases_and_elements(self, elements_width = 1,  radio_buttons = None, mode = 'regular'):

        #decide whether or not to split up canvases
        threshold = 40
        self.anonymizable_elements ={}

        self.hex_5_digit_keys = []
        self.titles = []
        for element in self.appendixEelements:
            print(element.tag)

        print('\n\n\n')
        for element in self.private_elements:
            print(element.tag)

        if len(self.appendixEelements) < threshold:        

            self.hex_5_digit_keys.append('Main')
            self.titles.append('Elements Identified in Appendix E of the DICOM standard')

            self.anonymizable_elements['Main'] = self.appendixEelements.copy()
        else:
            self.appendixEdict = (master_funcs.convert_elements_to_dict(self.appendixEelements))
            self.anonymizable_elements.update(self.appendixEdict)
            self.hex_5_digit_keys.extend(self.appendixEdict.keys())
            self.titles.extend("Elements Identified in Appendix E of the DICOM standard: Group Number " + key for key in self.appendixEdict.keys())

        if len(self.private_elements) < threshold:
            self.anonymizable_elements['private elements'] = self.private_elements

            self.hex_5_digit_keys.append('private elements')
                #create titles
            self.titles.append("Private Elements")            

        else:
            self.private_elements_dict = (master_funcs.convert_elements_to_dict(self.private_elements))

            self.anonymizable_elements.update(self.private_elements_dict)

            self.hex_5_digit_keys.extend(self.private_elements_dict.keys())
                #create titles
            self.titles.extend("Private Elements: Group Number " + key for key in self.private_elements_dict.keys())

        self.display_canvases = {}        
        for index_of_catagory, key in enumerate(self.hex_5_digit_keys):
            #create canvas
            self.display_canvases[key] = CustomCanvas.CustomCanv(master = self.master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = CustomEntry.CustomEntryClass.defaultidlecolor, relposx = 0, relposy = 0, relwidth = 1, relheight = 0.9)       
            self.populate_canvas(key = key, canvas = self.display_canvases[key], elements = self.anonymizable_elements[key], elements_width=elements_width, value_enable = "view",  radio_buttons = radio_buttons, start_y_level=2)
        

#===============to prevent errors ===============================
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


        #     #select all
        # self.select_all = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 0.25, rely = 0.5, relwidth = 0.5, relheight = 1.1, text = "Select All",  command = self.select_all_func, 
        #         state = "ENABLED", idleback = butt_idle, disabledback = disabledb)
            #delete element
        self.delete_all = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 0.75, rely = 0.5, relwidth = 0.5, relheight = 1.1, text = "Delete Element(s)",  command = None, 
                state = "DISABLED", idleback = butt_idle, disabledback = disabledb)

#=================================================================


        butt_idle = '#%02x%02x%02x' % (40, 35, 35)
        disabledb = '#%02x%02x%02x' % (100, 90, 90)


                #save changes
        self.save_changes = CustomButton.Button(master = self.master, root = self.button_canvas.canvobject, relx = 0.5, rely = 0.5, relwidth = 1, relheight = 1, text = "Save Changes",  command = self.decide_save_changes, 
                        state = "ENABLED", idleback = butt_idle, disabledback = disabledb)

 

        # self.title = tk.Label(self.Full_DF_Wind.toplevel, bg = 'grey', text = 'The Following Elements need to be anonymized')
        # self.title.place(x = 0, relwidth = 1, y = 0, height = CustomEntry.CustomEntryClass.height)

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
        errorflag = self.savechangescascade.save_from_boxes(input_full_df_cascade = self, image_indexes = image_indeces, box_list=self.all_edit_buttons)
        self.delete_cascade.set_delete_elements(self.all_delete_buttons)
        self.delete_cascade.final_delete(one_or_all)
        if errorflag == False:
            self.show_new_df()
            
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

        #labels
        self.dataelementlabel = tk.Label(self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].canvobject, bg = '#%02x%02x%02x' % (100, 100, 100), fg = 'white', text = 'Data Element')
        self.dataelementlabel.place(x = 0, y = CustomEntry.CustomEntryClass.height, anchor = 'nw', relwidth = (self.delete_column_bounds[0]), height = CustomEntry.CustomEntryClass.height)


        self.delete_label = tk.Label(self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].canvobject, bg = '#%02x%02x%02x' % (100, 100, 100), fg = 'white', text = 'Delete')
        self.delete_label.place(relx = self.delete_column_bounds[0], y = CustomEntry.CustomEntryClass.height, anchor = 'nw', relwidth = (self.delete_column_bounds[1] - self.delete_column_bounds[0]), height = CustomEntry.CustomEntryClass.height)

        self.edit_label = tk.Label(self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].canvobject, bg = '#%02x%02x%02x' % (100, 100, 100), fg = 'white', text = 'Custom Edit')
        self.edit_label.place(relx = self.delete_column_bounds[1], y = CustomEntry.CustomEntryClass.height, anchor = 'nw', relwidth = (1-self.delete_column_bounds[1]), height = CustomEntry.CustomEntryClass.height)


        #lines
        self.delete_left_bound = tk.Label(self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].canvobject, bg = 'white')
        self.delete_left_bound.place(relx= self.delete_column_bounds[0], y = CustomEntry.CustomEntryClass.height, width = 2, relheight = 1, anchor = 'n')

        self.delete_right_bound = tk.Label(self.display_canvases[self.hex_5_digit_keys[self.current_canvas]].canvobject, bg = 'white')
        self.delete_right_bound.place(relx=self.delete_column_bounds[1], y = CustomEntry.CustomEntryClass.height, width = 2, relheight = 1, anchor = 'n')
