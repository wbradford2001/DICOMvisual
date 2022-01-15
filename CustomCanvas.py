import tkinter as tk


class CustomCanv:
    def __init__(self, master, parent, root, color, relposx, relposy, relwidth, relheight, anchor = 'nw'):
        self.master = master
        self.root = root
        self.color = color
        self.relposx = relposx
        self.actualx = relposx * parent.width
        self.actualy = relposy * parent.height
        self.relposy = relposy
        self.relwidth = relwidth
        self.actualwidth = self.relwidth * parent.width
        self.relheight = relheight
        self.actualheight = self.relheight * parent.height
        self.anchor = anchor
        self.canvobject = tk.Canvas(self.root, bg = color, highlightthickness=0)
    def show_self(self):
        self.canvobject.place(relx = self.relposx, rely = self.relposy, relwidth = self.relwidth, relheight = self.relheight, anchor = self.anchor)
    def hide_self(self):
        self.canvobject.place_forget()

