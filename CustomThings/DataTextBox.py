import tkinter as tk


class data_window:

    def __init__(self, master, root, relposx, relposy, title, width):
        self.master = master
        self.root = root
        self.relposx = relposx
        self.relposy = relposy
        self.title = title

        self.width = width
        self.height = 0.9
        self.label = tk.Label(self.root, text = self.title, font = (self.master.fontstyle, 10),bg = '#%02x%02x%02x' % (60, 60, 60), fg ='white')
        self.text_box_label = tk.Text(self.root, bg = '#%02x%02x%02x' % (0, 0, 0), fg = 'white', font = (self.master.fontstyle, 8), wrap = 'word',bd = 0, relief = 'flat')

    def show_self(self, text):
        self.label.place(relx = self.relposx, rely = self.relposy, anchor = 'nw', relwidth = self.width, relheight = 0.1)

        self.text_box_label.delete("1.0", "end")
        self.text_box_label.insert(tk.END, text)
        self.text_box_label.place(relx = self.relposx, rely = self.relposy + 0.1, anchor = 'nw', relwidth = self.width, relheight = self.height)
    def update(self, text):
        self.text_box_label.config(text = text)