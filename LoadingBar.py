import tkinter as tk

class loading_bar:
    border_width = 6
    def __init__(self, parent, number_of_loads, height, xpos, ypos, text_message, text_y_offset = 20):
        self.xpos = xpos
        self.ypos = ypos
        self.number_of_loads = number_of_loads
        self.parent = parent
        self.height = height
        self.width = self.parent.width - (2 * self.xpos)
        self.text_message = text_message
        self.text_message_label = tk.Label(self.parent.toplevel,
                                            text = self.text_message, 
                                            font = (self.parent.parent.fontstyle, 30), 
                                            bg = self.parent.color, 
                                            fg = 'white')
        self.text_message_label.place(relx = 0.5, 
                                    y = self.ypos - text_y_offset, 
                                    anchor = 'center')
        self.outside_rect = tk.Label(self.parent.toplevel, 
            bg = 'grey', 
            borderwidth = loading_bar.border_width, 
            relief = 'solid'
            )
        self.outside_rect.place(
            x = self.xpos, 
            y = self.ypos, 
            height = self.height, 
            width = self.width, 
            anchor = 'w')
        self.loading_bar_rect = tk.Label(self.parent.toplevel, bg = 'red')
        self.loadingwidth = 0
        self.text_label = tk.Label(self.parent.toplevel, font = (self.parent.parent.fontstyle, 15),wraplength = self.parent.width*0.8, bg = self.parent.color, fg = 'white')
        self.text_label.place(relx = 0.5, y = self.ypos + self.height/2, anchor = 'n', relwidth = 0.8)
    def increase_width(self, new_string = ""):
        total_loading_length = self.width-2*loading_bar.border_width
        self.loadingwidth = self.loadingwidth + total_loading_length/self.number_of_loads
        self.loading_bar_rect.place(x = self.xpos + loading_bar.border_width, 
                                    y = self.ypos, 
                                    height = self.height -2*loading_bar.border_width, 
                                    width = self.loadingwidth, 
                                    anchor = 'w')
        self.text_label.config(text = new_string)
        self.parent.toplevel.update()