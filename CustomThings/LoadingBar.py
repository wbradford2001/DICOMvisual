import tkinter as tk

class loading_bar:
    border_width = 6
    def __init__(self, master, parent, root, number_of_loads, relheight, text_message):
        self.master = master
        self.number_of_loads = number_of_loads
        self.parent = parent
        self.root = root
        self.relheight = relheight
        self.text_message = text_message
        self.text_message_label = tk.Label(self.root,
                                            text = self.text_message, 
                                            font = (self.master.fontstyle, 30), 
                                            bg = self.parent.color, 
                                            fg = 'white')
        self.text_message_label.place(relx = 0.5, 
                                    rely = 0.5 - self.relheight/2, 
                                    anchor = 's')
        self.outside_rect = tk.Label(self.root, 
            bg = 'grey', 
            borderwidth = loading_bar.border_width, 
            relief = 'solid'
            )
        self.outside_rect.place(
            relx = 0.5, 
            rely = 0.5,
            relheight = self.relheight, 
            relwidth = 0.8, 
            anchor = 'c')
        self.loading_bar_rect = tk.Label(self.root, bg = 'red')
        self.loadingwidth = 0
        self.text_label = tk.Label(self.root, font = (self.master.fontstyle, 15),wraplength = self.parent.width*0.8, bg = self.parent.color, fg = 'white')
        self.text_label.place(relx = 0.5, rely = 0.5 + self.relheight/2, anchor = 'n', relwidth = 0.8)
    def increase_width(self, new_string = ""):
        total_loading_length = 0.8 - 2*loading_bar.border_width/self.parent.width
        self.loadingwidth = self.loadingwidth + total_loading_length/self.number_of_loads
        self.loading_bar_rect.place(relx = 0.1 + loading_bar.border_width/self.parent.width, 
                                    rely = 0.5, 
                                    relheight = self.relheight -2*loading_bar.border_width/self.parent.height, 
                                    relwidth = self.loadingwidth, 
                                    anchor = 'w')
        self.text_label.config(text = new_string)
        self.parent.toplevel.update()