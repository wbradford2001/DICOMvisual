import tkinter as tk

class top_window:
    def __init__(self, root, width, height, title, color = 'black'):
        self.root = root
        self.height = height
        self.width = width
        self.color= color
        self.toplevel = tk.Toplevel(self.root)
        self.toplevel.geometry("{}x{}".format(self.width,self.height))
        self.toplevel.title(title)
        self.toplevel.configure(bg = color)
        self.toplevel.resizable(False, False) 
        rootx = self.root.winfo_x()
        rooty = self.root.winfo_y()
        self.toplevel.geometry("+%d+%d" % ((
            rootx + root.winfo_screenwidth()/2 - self.width/2), (
            rooty + root.winfo_screenheight()/2 - self.height/2)))
        self.toplevel.attributes('-topmost', True)
        self.toplevel.focus_force()

def show_error_window(root, fontstyle, message, width = 300, height = 100, ErrorString = None):
    unable_to_save = top_window(root = root, width = width, height = height, title = 'Error',
                color= 'grey')
    unable_to_save_text_label = tk.Label(unable_to_save.toplevel, text = message, font = fontstyle,
                                    bg= 'grey', fg = 'black')
    if ErrorString != None:
        unable_to_save_text_label.place(relx = 0.5, rely = 0.2, anchor= 'center')
        error = tk.Text(unable_to_save.toplevel, font = fontstyle, fg = 'black', bg = 'grey')
        error.insert(tk.END, ErrorString)
        error.place(relx = 0.5, rely = 0.35, relwidth = 1, relheight = 0.4, anchor = 'n')
    else:
        unable_to_save_text_label.place(relx = 0.5, rely = 0.5, anchor= 'center')

    return unable_to_save