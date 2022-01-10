import tkinter as tk

class menu_button:
    height = 40
    width = 200
    def __init__(self, root, text, command, fontstyle, relx, relwidth, state):
        self.root = root
        self.state = state
        self.object = tk.Button(self.root, 
                                text = text, 
                                bg = 'grey', 
                                fg = 'black', 
                                overrelief = tk.RAISED, 
                                command = command, 
                                bd = 0, 
                                font = (fontstyle, 15),
                                state = self.state)
        self.object.place(relx = relx, y = 0, anchor = 'nw', relwidth = relwidth, height = menu_button.height)