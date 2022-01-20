import tkinter as tk


class image_indicator:
    height = 15
    defaultbg = '#%02x%02x%02x' % (70, 70, 70)
    def __init__(self, master, root, text, index):
        self.master = master
        self.index = index
        self.text = text
        self.root = root


        self.label = tk.Label(self.root.canvobject, text= self.text, bg = image_indicator.defaultbg, fg = 'grey', 
            font = (self.master.fontstyle, 6))
        self.label.bind("<Enter>", self.recolor_to_yellow)
        self.label.bind("<Leave>", self.color_to_original)
        self.label.bind("<ButtonPress>", self.adjust_Main_View)
        self.orig_color ='grey'
    def show_self(self):


        self.label.place(relx = 0, y = self.index * image_indicator.height, height = image_indicator.height, width = self.root.actualwidth-3, anchor = 'nw')

    
    def recolor(self, yo):

        self.label.configure(fg = 'red', height = 50, width = 100)
    def recolor_to_yellow(self, yo):
        self.label.configure(fg = 'yellow', height = 50, width = 100)
    def color_to_original(self, yo):
        self.label.configure(fg = self.orig_color)
    def adjust_Main_View(self, yo):

        self.master.MainView.currentim.set(self.index)
        self.master.MainView.display_image()
        self.master.MainView.display_GUI()  