import tkinter as tk


class data_window:
    width = 165
    height = 30
    text_box_height = 150
    def __init__(self, root, relposx, relposy, title, fontstyle):
        self.root = root
        self.relposx = relposx
        self.relposy = relposy
        self.title = title
        self.fontstyle = fontstyle
    def show_self(self, text):
        self.label = tk.Label(self.root, text = self.title, font = (self.fontstyle, 10), bg= 'black', fg ='white')
        self.label.place(relx = self.relposx, rely = self.relposy-0.1, anchor = 'center', width = data_window.width, height = data_window.height)


        self.text_box_label = tk.Text(self.root, bg = 'black', fg = 'white', font = (self.fontstyle, 8), wrap = 'word',bd = 0, relief = 'flat', height= data_window.text_box_height, width = data_window.width)
        self.text_box_label.insert(tk.END, text)
        self.text_box_label.place(relx = self.relposx, rely = self.relposy, anchor = 'center', width = data_window.width, height = data_window.text_box_height)
    def update(self, text):
        self.text_box_label.config(text = text)