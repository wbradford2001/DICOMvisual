import tkinter as tk
import LoadingBar
import CustomRadioButton
import CustomButton

class top_window:
    def __init__(self, master, root, width, height, title, color = 'black'):
        self.master = master
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
            34 + self.master.width/2 - self.width/2), (
            59 + self.master.height/2 - self.height/2)))
        #self.master.root.eval(f'tk::PlaceWindow {str(self.toplevel)} center')
        self.toplevel.attributes('-topmost', True)
        self.toplevel.focus_force()



def loading_win(master, root, number_of_loads, width = 500, height = 300, message = "Loading File Data"):
    
    loading_window = top_window(master = master, root = root, width = width, height = height, title = "Loading", color = 'grey')
    loading_bar = LoadingBar.loading_bar(master = master, parent = loading_window, root = loading_window.toplevel, 
                                            number_of_loads = number_of_loads,
                                            relheight = 0.2, 
                                            text_message = message, 
                                            )
    return loading_window, loading_bar

def show_error_window(master, root, message, width = 300, height = 100, ErrorString = None):
    unable_to_save = top_window(master = master, root = root, width = width, height = height, title = 'Error',
                color= 'grey')
    unable_to_save_text_label = tk.Label(unable_to_save.toplevel, text = message, font = master.fontstyle,
                                    bg= 'grey', fg = 'red', wraplength = unable_to_save.width * 0.8)
    if ErrorString != None:
        unable_to_save_text_label.place(relx = 0.5, rely = 0.2, anchor= 'center')
        error = tk.Text(unable_to_save.toplevel, font = master.fontstyle, fg = 'white', bg = 'grey', highlightthickness=0)
        error.tag_configure("tag_name", justify='center')
        error.insert(tk.END, ErrorString)
        error.tag_add("tag_name", "1.0", "end")
        error.place(relx = 0.5, rely = 0.35, relwidth = 0.7, relheight = 0.5, anchor = 'n')
    else:
        unable_to_save_text_label.place(relx = 0.5, rely = 0.5, anchor= 'center')

    return unable_to_save

def just_one_or_many(master, root, message, image_name, proceed_command, width = 500, height = 300):
    just_one_or_many_wind = top_window(master = master, root = root, width = width, height = height, title = "Select Option Below",
                color= 'grey', )
    main_text = tk.Label(just_one_or_many_wind.toplevel, text = message, font = master.fontstyle,
                                    bg= 'grey', fg = 'white')
    main_text.place(relx = 0.5, rely = 0.2, relwidth = 1, relheight = 0.25, anchor = 'center')




    Just_One_Or_All_Menu = CustomRadioButton.RadioMenu(master = master, root = just_one_or_many_wind.toplevel,
        background_color='grey', height = 50, width = 50)

    Just_One=Just_One_Or_All_Menu.add_button(value = "Just One", xpos = just_one_or_many_wind.width * 0.3, ypos = just_one_or_many_wind.height * 0.4,
         text = "Just " + str(image_name))
    All = Just_One_Or_All_Menu.add_button(value = "All", xpos = just_one_or_many_wind.width * 0.3, ypos = just_one_or_many_wind.height * 0.6,
         text = "All Files", selected = True)


    proceed = CustomButton.Button(master = master, root = just_one_or_many_wind.toplevel, relx = 0.5, 
                        rely = 0.9, width = 100, height = 50, text = "Proceed",  command = lambda : proceed_command(Just_One_Or_All_Menu.variable))

    return just_one_or_many_wind