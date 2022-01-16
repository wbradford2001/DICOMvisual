import tkinter as tk
from unittest.mock import NonCallableMagicMock

class RadioMenu:
    defaultdisabedcolor ='#%02x%02x%02x' % (40, 40, 40)
    defaultidlecolor = '#%02x%02x%02x' % (200, 200, 200)
    defaultactivecolor = '#%02x%02x%02x' % (100, 100, 100)
    defaultpressedcolor = 'green'
    default_pressed_object_size_reduce = 20
    def __init__(self,  master, root, background_color, height, width, 
        exclusive = True, size_reduce=3, 
        disabled_back = defaultdisabedcolor, idleback = defaultidlecolor, activeback = defaultactivecolor, pressedback = defaultpressedcolor,
        pressed_object_size_reduce = default_pressed_object_size_reduce, variable = None):

        #input variabled
        self.master = master
        self.root = root
        self.background_color = background_color
        self.height = height
        self.width = width     

        #autofilled
        self.exclusive = exclusive           
        self.size_reduce = size_reduce
        self.disabled_back = disabled_back
        self.idleback = idleback
        self.activeback = activeback
        self.pressedback = pressedback
        self.pressed_object_size_reduce = pressed_object_size_reduce

        self.variable = variable

        self.buttons_so_far = []
    
    def add_button(self, value, xpos, ypos, text, command = None, deselect_command = None, state = "ENABLED", selected = False):
        New_Button = RadioButton(master = self.master, parent_menu = self, root = self.root, value = value, 
            xpos = xpos, ypos = ypos, text = text, command = command, deselect_command = deselect_command, state = state)
        if selected == True:
            New_Button.change_to_pressed(6)
        New_Button.show_self()     
        self.buttons_so_far.append(New_Button) 
        return New_Button
    def append_to_variable_list(self, value):
        self.variable.append(value)   
  
    def remove_from_variable_list(self, value):
        self.variable.remove(value)           
   
class RadioButton:

    def __init__(self, master, parent_menu, root, value, xpos, ypos,text, command, deselect_command, state):
        #input variables
        self.master = master
        self.parent_menu = parent_menu
        self.root = root        
        self.value = value
        self.xpos = xpos
        self.ypos = ypos
        self.text = text

        #autofill variables
        self.command = command
        self.deselect_command = deselect_command
        self.state = state

        #variables from parent
        self.background_color = self.parent_menu.background_color
        self.height = self.parent_menu.height
        self.width = self.parent_menu.width 
        self.size_reduce = self.parent_menu.size_reduce
        self.disabledback = self.parent_menu.disabled_back
        self.idleback = self.parent_menu.idleback
        self.activeback = self.parent_menu.activeback
        self.pressedback = self.parent_menu.pressedback  
        self.pressed_object_size_reduce = self.parent_menu.pressed_object_size_reduce                

        #define objects
        self.radio_obj  = tk.Label(self.root, borderwidth=4, relief = 'solid', highlightcolor='black', highlightthickness=4)
        self.text_obj = tk.Label(self.root, text = self.text, bg = self.background_color, wraplength=self.width*3)
        self.pressed_object = tk.Label(self.root, bg = 'red')


        #configure background and text color
        if self.state == "ENABLED":
            self.radio_obj.config(bg = self.idleback)
            #self.radio_obj.config(fg = 'white')
            self.text_obj.config(fg = 'white')
        elif self.state == "DISABLED":
            self.radio_obj.config(bg = self.disabledback)
            #self.radio_obj.config(fg = 'grey')
            self.text_obj.config(fg = 'grey')            

        #bind radio object
        self.radio_obj.bind('<Enter>', self.change_to_active)
        self.radio_obj.bind('<Leave>', self.change_to_idle) 
        self.radio_obj.bind('<Button>', self.change_to_pressed)
        #self.radio_obj.bind('<ButtonRelease>', self.change_to_active) 

        self.pressed_object.bind('<Enter>', self.change_to_active)
        self.pressed_object.bind('<Leave>', self.change_to_idle)         
        self.pressed_object.bind('<Button>', self.depress)         

        self.pressed = False

    #Mouse enters
    def change_to_active(self, yo):
        if self.state == "ENABLED":
            self.radio_obj.config(bg = self.activeback)
            self.radio_obj.place_configure(width = self.width - self.size_reduce, height = self.height - self.size_reduce)

    #Mouse press
    def  change_to_pressed(self, yo):
        if self.state == "ENABLED":
            #if its not pressed already
            if self.pressed == False:
                self.pressed_object.place(x = self.xpos, y= self.ypos, width = self.width-self.parent_menu.pressed_object_size_reduce, height = self.height-self.parent_menu.pressed_object_size_reduce, anchor = 'center')      
                self.pressed = True
                if self.command != None:
                    
                    self.command()

                #if not exclusive
                if self.parent_menu.exclusive == False:
                    pass
                    #self.parent_menu.append_to_variable_list(self.value)

                else:
                #if exclusive
                    self.parent_menu.variable = self.value
                    for button in self.parent_menu.buttons_so_far:
                        if button != self:
                            button.pressed = False
                            button.change_to_idle(4)
                            button.pressed_object.place_forget()
                            button.show_self()
                    self.parent_menu.variable = self.value
    def depress(self, yo):                    
            #if its pressed already
            if self.pressed == True and self.parent_menu.exclusive == False:
                self.pressed_object.place_forget()     
                self.pressed_object.place_forget()                 
                self.pressed = False



                #self.parent_menu.remove_from_variable_list(self.value)

                if self.deselect_command != None:
                    self.deselect_command()
                 


    def  change_to_idle(self, yo):
        if self.state == "ENABLED":
            self.radio_obj.config(bg = self.idleback)
            self.radio_obj.place_configure(width = self.width , height = self.height)
         
    def show_self(self):
            self.radio_obj.place(x= self.xpos, y = self.ypos, width = self.width, height = self.height, anchor = 'center')
            self.text_obj.place(x= self.xpos+(self.width/2), y = self.ypos, width = self.width * 4, height = self.height, anchor = 'w')
    def hide_self(self):
        self.radio_obj.place_forget()
        self.text_obj.place_forget() 
        self.pressed_object.place_forget()       
    def enable(self):
        self.state = "ENABLED"        
        self.radio_obj.config(bg = self.idleback)
        self.radio_obj.config(fg = 'white')

        self.show_self()

    def disable(self):
        self.state = "DISABLED"
        self.radio_obj.config(bg = self.disabledback)
        self.radio_obj.config(fg = 'grey')
        self.pressed_object.place_forget()
        self.show_self()

