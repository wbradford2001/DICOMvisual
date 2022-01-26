import tkinter as tk
import EditWindows.EditWindow as EditWindow
import CustomThings.CustomCanvas as CustomCanvas
import CustomThings.CustomButton as CustomButton
import CustomThings.CustomEntry as CustomEntry
import DataBaseStuff.knownelements as knownelements
import master_funcs



class ViewPrivateElements(EditWindow.EditWindow):
    def __init__(self, master, title):
        super().__init__(master, title)
        #populate private elements
        self.private_elements = []
        for element in self.all_elements:
            if (((str(element.tag).upper() not in knownelements.elements))):
               
                self.private_elements.append(element)  
        self.display_elements = master_funcs.convert_elements_to_dict(self.private_elements)  
         
        self.define_canvases_and_elements()
        print(self.hex_5_digit_keys)
        self.show_canvas()



    def define_canvases_and_elements(self):
        self.display_canvases = {}


        #create hex keys
        self.hex_5_digit_keys = list(self.display_elements.keys())

        #create titles
        self.titles = []
        for hex_key in self.hex_5_digit_keys:
            self.titles.append("Group Number: " + hex_key)        
        
        for index_of_catagory, key in enumerate(self.hex_5_digit_keys):
            #create canvas
            self.display_canvases[key] = CustomCanvas.CustomCanv(master = self.master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = CustomEntry.CustomEntryClass.defaultidlecolor, relposx = 0, relposy = 0, relwidth = 1, relheight = 0.9)
            


            self.populate_canvas(key = key, canvas = self.display_canvases[key], elements = self.display_elements[key], elements_width=1, value_enable = "view", radio_buttons=None)


        #indicator and next button canvas
                #indicator canvases
        self.indicator_canvas = CustomCanvas.CustomCanv(master = self.master, parent = self.Full_DF_Wind, root = self.Full_DF_Wind.toplevel, color = '#%02x%02x%02x' % (130, 130, 130), relposx = 0.5, relposy = 1-(self.lower_canvas_width)/2, relwidth = 1, relheight = self.lower_canvas_width, anchor = 'center')
        self.indicator_canvas.show_self()
            #next button
        self.next_button = CustomButton.Button(master = self.master, root = self.indicator_canvas.canvobject, relx = 0.95, rely = 0.5, relwidth = 0.1, relheight = 1, text = "Next",  command = self.show_next,  idleback = 'grey')
        self.next_button.show_self()
            #back button
        self.back_button = CustomButton.Button(master = self.master, root = self.indicator_canvas.canvobject, relx = 0.05, rely = 0.5, relwidth = 0.1, relheight = 1, text = "Back",  command = self.show_previous,  idleback = 'grey')
        self.back_button.show_self()  
        self.back_button.disable()        
            #indicator
        self.indicator = tk.Label(self.indicator_canvas.canvobject, bg = '#%02x%02x%02x' % (130, 130, 130), fg = '#%02x%02x%02x' % (240, 240, 240))
        self.indicator.place(relx = 0.5, rely = 0.5, relwidth = 0.06, relheight = 1, anchor = 'center')
        self.indicator.config(text = str(self.current_canvas+1) + '/' + str(len(self.display_canvases)))




        
            

        