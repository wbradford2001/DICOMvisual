import tkinter as tk

class Divider:
    buffer = 4
    color= 'grey'
    activecolor = 'yellow'
    def __init__(self, master, root, orientation, relposx = None, relposy = None, width = None, height = None):
        self.master = master
        self.root = root
        self.orientation = orientation
        self.relposx = relposx
        self.relposy = relposy
        self.width = width
        self.relheight = height
        self.obj = tk.Label(self.root, bg = Divider.color)
        self.obj.bind("<Enter>", self.mouse_entered)
        self.obj.bind("<Leave>", self.mouse_exit)
        self.obj.bind("<B1-Motion>", self.move)

    def mouse_entered(self, yo):
        #self.obj.config(bg = Divider.activecolor)
        pass
    def mouse_exit(self, yo):
        self.obj.config(bg = Divider.color)
    def move(self, yo):
        pass


    def show_self(self):
        if self.orientation == "horizontal":
            self.obj.place(relx = 0, width = self.width, rely = self.relposy, height = Divider.buffer, anchor = 'w')
        if self.orientation == "vertical":
            self.obj.place(relx = self.relposx, width = Divider.buffer, rely = self.relposy, height = self.relheight, anchor = 'n')
    def hide_self(self):
        self.obj.place_forget()

