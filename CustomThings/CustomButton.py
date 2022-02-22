from textwrap import wrap
import tkinter as tk


import placement

class Button:
    defaultdisabedcolor ='#%02x%02x%02x' % (40, 40, 40)
    defaultidlecolor = '#%02x%02x%02x' % (70, 70, 70)
    defaultactivecolor = '#%02x%02x%02x' % (100, 120, 100)
    defaultpressedcolor = 'blue'
    defaultxsize_reduce = 1
    defaultysize_reduce = 1  
    def __init__(self, master, root,text, command,  
            disabledback = defaultdisabedcolor, idleback=defaultidlecolor, activeback=defaultactivecolor, pressedback=defaultpressedcolor, 
            state = 'ENABLED', show = True, anchor = 'center', xsize_reduce = defaultxsize_reduce,ysize_reduce = defaultysize_reduce,
            **kwargs):
        
        #necessary
        self.master = master
        self.root = root
        self.text = text
        self.command = command

        #optional - back ground
        self.disabledback = disabledback
        self.idleback = idleback
        self.activeback = activeback
        self.pressedback = pressedback

        #optional - miscellaneous
        self.state = state
        self.anchor = anchor
        self.xsize_reduce = xsize_reduce
        self.ysize_reduce = ysize_reduce        

        #positional
        self.__dict__.update(kwargs)
        
       
       #object
        self.obj  = tk.Label(self.root, text = self.text, borderwidth=2, font = (self.master.fontstyle, 10))
        if self.state == "ENABLED":
            self.obj.config(bg = self.idleback)
            self.obj.config(fg = 'white')
        elif self.state == "DISABLED":
            self.obj.config(bg = self.disabledback)
            self.obj.config(fg = 'grey')
        self.obj.bind('<Enter>', self.change_to_active)
        self.obj.bind('<Leave>', self.change_to_idle) 
        self.obj.bind('<Button>', self.change_to_pressed)
        self.obj.bind('<ButtonRelease>', self.change_to_active) 
        if show == True:
            self.show_self()


    #mouse enters
    def change_to_active(self, yo):
        if self.state == "ENABLED":
            self.obj.config(bg = self.activeback)
            placement.smart_place_configure_to_active(self.master, self)  
        # elif self.state == "DISABLED":
        #     self.obj.config(bg = self.disabledback)
        #     self.show_self()

    #mouse pressed
    def  change_to_pressed(self, yo):
        if self.state == "ENABLED":
            self.obj.config(bg = self.pressedback)     

            if self.command != None:              
                self.command()

    #mouse leaves
    def  change_to_idle(self, yo):
        if self.state == "ENABLED":
            self.obj.config(bg = self.idleback)
            placement.smart_place_configure_to_idle(self.master, self)

    def show_self(self):
        placement.smart_place(self.master, self)

    def hide_self(self):
        self.obj.place_forget()

    def enable(self):
        self.state = "ENABLED"      
        self.obj.config(bg = self.idleback)
        self.obj.config(fg = 'white')
        self.show_self()

    def disable(self):
        self.state = "DIABLED"
        self.obj.config(bg = self.disabledback)
        self.obj.config(fg = 'grey')
        self.show_self()