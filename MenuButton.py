import tkinter as tk

class menu_button:
    active_menu_option = "Menu"
    top_botton_color = '#%02x%02x%02x' % (70, 70, 70)
    canvas_color = '#%02x%02x%02x' % (70, 70, 70)
    menubuttonheight = 30
    canvasheight = 50
    def __init__(self, root, xpos, width, title):
        self.canvobj = tk.Canvas(root, bg  = menu_button.canvas_color, bd = 0, highlightthickness=0, relief = 'ridge')
        self.canvobj.place(x = 0, y = menu_button.menubuttonheight, width = root.winfo_screenwidth(), height = menu_button.canvasheight)
        self.buttonobj = tk.Label(root, bg = menu_button.top_botton_color, text = title)
        self.buttonobj.place(x = xpos, width = width, y = 0, height = menu_button.menubuttonheight)

