import tkinter as tk

class Button:
    defaultdisabedcolor ='#%02x%02x%02x' % (40, 40, 40)
    defaultidlecolor = '#%02x%02x%02x' % (70, 70, 70)
    defaultactivecolor = '#%02x%02x%02x' % (100, 120, 100)
    defaultpressedcolor = 'blue'
    def __init__(self, master, root, relxpos, relypos, width, height,text, size_reduce, command,  
            disabledback = defaultdisabedcolor, idleback=defaultidlecolor, activeback=defaultactivecolor, pressedback=defaultpressedcolor, state = 'ENABLED', show = True,
            placing = 'relative', anchor = 'center'):
        self.master = master
        self.root = root
        self.relxpos = relxpos
        self.relypos = relypos
        self.width = width
        self.height = height
        self.disabledback = disabledback
        self.idleback = idleback
        self.activeback = activeback
        self.text = text
        self.pressedback = pressedback
        self.size_reduce = size_reduce
        self.placing = placing
        self.anchor = anchor
        self.obj  = tk.Label(self.root, text = self.text, borderwidth=2, font = self.master.fontstyle)
        self.state = state
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
        self.command = command
       
    def change_to_active(self, yo):
        if self.state == "ENABLED":
            if self.anchor == 'center':
                self.obj.config(bg = self.activeback)
                self.obj.place_configure(width = self.width - self.size_reduce, height = self.height - self.size_reduce)
        elif self.state == "DISABLED":
            self.obj.config(bg = self.disabledback)
            self.show_self()
    def  change_to_pressed(self, yo):
        if self.state == "ENABLED":
            self.obj.config(bg = self.pressedback)         
            self.command()



    def  change_to_idle(self, yo):
        if self.state == "ENABLED":
            self.obj.config(bg = self.idleback)
            self.obj.place_configure(width = self.width , height = self.height )
    def show_self(self):
        if self.placing == "relative":
            self.obj.place(relx= self.relxpos, rely = self.relypos, width = self.width, height = self.height, anchor = self.anchor)
        elif self.placing == "absolute":
            self.obj.place(x= self.relxpos, y = self.relypos, width = self.width, height = self.height, anchor = self.anchor)

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