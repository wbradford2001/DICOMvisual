import tkinter as tk

class menu_button:
    height = 40
    width = 200
    def __init__(self, root, text, command, fontstyle, x):
        self.root = root
        self.object = tk.Button(self.root, 
                                text = text, 
                                bg = 'grey', 
                                fg = 'black', 
                                overrelief = tk.RAISED, 
                                command = command, 
                                bd = 0, 
                                font = (fontstyle, 15))
        self.object.place(x = x, y = 0, anchor = 'nw', width = menu_button.width, height = menu_button.height)