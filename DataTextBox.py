import tkinter as tk


class data_window:
    height = 30
    def __init__(self, root, relposx, relposy, title, fontstyle, width, height):
        self.root = root
        self.relposx = relposx
        self.relposy = relposy
        self.title = title
        self.fontstyle = fontstyle
        self.width = width
        self.height = height
        self.label = tk.Label(self.root, text = self.title, font = (self.fontstyle, 10), bg= 'black', fg ='white')
        self.text_box_label = tk.Text(self.root, bg = 'black', fg = 'white', font = (self.fontstyle, 8), wrap = 'word',bd = 0, relief = 'flat')

    def show_self(self, text):
        self.label.place(relx = self.relposx, rely = self.relposy-0.1, anchor = 'w', relwidth = self.width, height = data_window.height)

        self.text_box_label.delete("1.0", "end")
        self.text_box_label.insert(tk.END, text)
        self.text_box_label.place(relx = self.relposx, rely = self.relposy, anchor = 'w', relwidth = self.width, relheight = self.height)
    def update(self, text):
        self.text_box_label.config(text = text)