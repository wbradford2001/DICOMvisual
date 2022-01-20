import tkinter as tk
import placement

class menu_button:
    active_menu_option = "Menu"
    top_botton_color = '#%02x%02x%02x' % (70, 70, 70)
    canvas_color = '#%02x%02x%02x' % (70, 70, 70)
    menubuttonheight = 30
    canvasheight = 50
    menu_buttons_so_far = []
    def __init__(self, master, root, title, num_buttons, **kwargs):
        #variables
        self.master = master
        self.root = root
        self.title = title
        self.num_buttons = num_buttons

        #kwargs
        self.__dict__.update(kwargs)

        self.height = menu_button.menubuttonheight
        self.y = menu_button.menubuttonheight/2

        #objectsw
        self.obj = tk.Label(root, bg = menu_button.top_botton_color, text = title, fg = 'white', font = self.master.fontstyle)        
        placement.smart_place(master = self.master, parent = self)
        self.obj.bind('<Enter>', self.display_canvas)

        self.canvobj = tk.Canvas(self.root, bg  = menu_button.canvas_color, bd = 0, highlightthickness=0, relief = 'ridge')
        #self.canvobj.bind('<Leave>', self.hide_canvas)

        menu_button.menu_buttons_so_far.append(self)


    def display_canvas(self, hey):
        
        self.obj.configure(bg = '#%02x%02x%02x' % (100, 100, 100))

        for button in menu_button.menu_buttons_so_far:
            if button != self:
                button.hide_canvas(6)
        self.canvobj.place(relx = 0.5, y = menu_button.menubuttonheight, relwidth = 1, height = menu_button.canvasheight, anchor = 'n')

    def hide_canvas(self, hey):
        self.canvobj.place_forget()
        self.obj.configure(bg = menu_button.top_botton_color)  



        

