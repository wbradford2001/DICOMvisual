import tkinter as tk
class RadioMenu:
    def __init__(self,  master, root, variable, background_color, size_reduce, height, width):
        self.variable = variable
        self.background_color = background_color
        self.size_reduce = size_reduce
        self.height = height
        self.width = width
        self.master = master
        self.root = root
        self.buttons_so_far = []
    def add_button(self, value, xpos, relypos, text, selected = False):
        New_Button = RadioButton(master = self.master, parent_menu = self, root = self.root, value = value, xpos = xpos, relypos = relypos, width = self.width, height = self.height, text = text, size_reduce = self.size_reduce, background_color=self.background_color)
        if selected == True:
            New_Button.change_to_pressed(6)
        New_Button.show_self()     
        self.buttons_so_far.append(New_Button)               
   
class RadioButton:
    defaultdisabedcolor ='#%02x%02x%02x' % (40, 40, 40)
    defaultidlecolor = '#%02x%02x%02x' % (200, 200, 200)
    defaultactivecolor = '#%02x%02x%02x' % (100, 100, 100)
    defaultpressedcolor = 'green'
    def __init__(self, master, parent_menu, root, value, xpos, relypos, width, height,text, size_reduce, background_color, command = None,  
            disabledback = defaultdisabedcolor, idleback=defaultidlecolor, activeback=defaultactivecolor, pressedback=defaultpressedcolor, state = 'ENABLED', show = True,
            anchor = 'center'):
        self.master = master
        self.parent_menu = parent_menu
        self.value = value
        self.root = root
        self.xpos = xpos
        self.relypos = relypos
        self.width = width
        self.height = height
        self.background_color= background_color
        self.disabledback = disabledback
        self.idleback = idleback
        self.activeback = activeback
        self.text = text
        self.pressedback = pressedback
        self.size_reduce = size_reduce
        self.anchor = anchor
        self.radio_obj  = tk.Label(self.root, borderwidth=4, relief = 'solid', highlightcolor='black', highlightthickness=4)
        self.text_obj = tk.Label(self.root, text = self.text, bg = self.background_color, wraplength=self.width*4)
        self.state = state
        self.pressed_object = tk.Label(self.root, bg = 'red')
        if self.state == "ENABLED":
            self.radio_obj.config(bg = self.idleback)
            self.radio_obj.config(fg = 'white')
            self.text_obj.config(fg = 'white')
        elif self.state == "DISABLED":
            self.radio_obj.config(bg = self.disabledback)
            self.radio_obj.config(fg = 'grey')
        self.radio_obj.bind('<Enter>', self.change_to_active)
        self.radio_obj.bind('<Leave>', self.change_to_idle) 
        self.radio_obj.bind('<Button>', self.change_to_pressed)
        self.radio_obj.bind('<ButtonRelease>', self.change_to_active) 
        if show == True:
            self.show_self()
        self.command = command

       
    def change_to_active(self, yo):
        if self.state == "ENABLED":
            if self.anchor == 'center':
                self.radio_obj.config(bg = self.activeback)
                self.radio_obj.place_configure(width = self.width - self.size_reduce, height = self.height - self.size_reduce)
        elif self.state == "DISABLED":
            self.radio_obj.config(bg = self.disabledback)
            self.show_self()
    def  change_to_pressed(self, yo):
        if self.state == "ENABLED":
            for button in self.parent_menu.buttons_so_far:
                if button != self:
                    button.state = "ENABLED"
                    button.change_to_idle(4)
                    button.pressed_object.place_forget()
                    

                    button.show_self()

            self.pressed_object.place(x = self.xpos, rely= self.relypos, width = self.width - 20, height = self.height - 20, anchor = 'center')      
            self.state = "PRESSED"
            self.parent_menu.variable = self.value



    def  change_to_idle(self, yo):
        if self.state == "ENABLED" or self.state == "PRESSED":
            self.radio_obj.config(bg = self.idleback)
            self.radio_obj.place_configure(width = self.width , height = self.height )
            self.state = "ENABLED"
    def show_self(self):
            self.radio_obj.place(x= self.xpos, rely = self.relypos, width = self.width, height = self.height, anchor = self.anchor)
            self.text_obj.place(x= self.xpos+(self.width/2), rely = self.relypos, width = self.width * 4, height = self.height, anchor = 'w')
    def hide_self(self):
        self.radio_obj.place_forget()
        self.text_obj.place_forget()        
    def enable(self):
        self.state = "ENABLED"        
        self.radio_obj.config(bg = self.idleback)
        self.radio_obj.config(fg = 'white')

        self.show_self()

    def disable(self):
        self.state = "DIABLED"
        self.radio_obj.config(bg = self.disabledback)
        self.radio_obj.config(fg = 'grey')
        self.show_self()

