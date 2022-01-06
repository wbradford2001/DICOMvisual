import tkinter as tk

class top_window:
    def __init__(self, root, width, height, title, color = 'black'):
        self.root = root
        self.height = height
        self.width = width
        self.toplevel = tk.Toplevel(self.root)
        self.toplevel.geometry("{}x{}".format(self.width,self.height))
        self.toplevel.title(title)
        self.toplevel.configure(bg = color)
        rootx = self.root.winfo_x()
        rooty = self.root.winfo_y()
        self.toplevel.geometry("+%d+%d" % ((
            rootx + root.winfo_screenwidth()/2 - self.width/2), (
            rooty + root.winfo_screenheight()/2 - self.height/2)))
        self.toplevel.attributes('-topmost', True)
        self.toplevel.focus_force()