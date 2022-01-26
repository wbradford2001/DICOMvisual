import tkinter as tk
import CustomThings.TopLevelWindow as TopLevelWindow
import CustomThings.CustomButton as CustomButton
import placement



class CustomEntryClass:
    height = 30
    text_size = 15
    defaultdisabedcolor ='#%02x%02x%02x' % (40, 40, 40)
    defaultidlecolor = '#%02x%02x%02x' % (70, 70, 70)
    defaultactivecolor = '#%02x%02x%02x' % (100, 120, 100)
    defaultpressedcolor = 'blue'
    def __init__(self, master, parent, root, text, 
                    disableback = defaultdisabedcolor, idlecolor = defaultidlecolor, activecolor = defaultactivecolor, pressedcolor = defaultpressedcolor,
                    state = "ENABLED", view_or_edit = 'edit', element = None, attrib = None, **kwargs):
        #variables
        self.master = master
        self.parent = parent
        self.root = root
        self.entry_text = tk.StringVar()
        if len(str(text))< 200:
            self.entry_text.set(str(text))
        else:
            self.entry_text.set("Unable to display date element with string")
            self.state = "DISABLED"
        self.orig_string = self.entry_text.get()


        #auto filled variables
        self.state = state
        self.disabledback= disableback
        self.idleback = idlecolor
        self.activeback = activecolor
        self.pressedback= pressedcolor
        self.view_or_edit = view_or_edit
        self.element = element
        self.attrib = attrib        


        self.__dict__.update(kwargs)

        self.obj = tk.Label(self.root, bg = self.idleback, borderwidth=2, text = self.entry_text.get(),wraplength=((self.relwidth* self.parent.Full_DF_Wind.width)*0.9), font = (self.master.fontstyle, 10))
        self.height = CustomEntryClass.height
        self.anchor = 'nw'



        self.view_or_edit = view_or_edit
        if self.state == "ENABLED" or self.state == "view":
            self.obj.config(bg = self.idleback)
            self.obj.config(fg = 'white')
        elif self.state == "DISABLED":
            self.obj.config(bg = self.disabledback)
            self.obj.config(fg = 'grey')           
        elif self.state == "TITLE":
            self.obj.config(bg = '#%02x%02x%02x' % (100, 100, 100))
            self.obj.config(fg = 'white') 
                                 
        self.obj.bind('<Enter>', self.change_to_active)
        self.obj.bind('<Leave>', self.change_to_idle) 
        self.obj.bind('<Button>', self.change_to_pressed)



    def change_to_active(self, yo):
        if self.state == "ENABLED":
            self.obj.config(bg = self.activeback)

    def  change_to_pressed(self, yo):
        if self.state == "ENABLED":
            self.obj.config(bg = self.pressedback)
            self.new_wind_open = True
            self.new_wind = TopLevelWindow.top_window(master = self.master, root= self.root, width = 600, height=200, title = "Edit Data Element", color= 'grey')
            text_string = "Change Data Element:\n" + str(self.element.tag) + ": " + str(self.element.keyword)
            current_val = tk.Label(self.new_wind.toplevel, text =  text_string, bd = 0, bg = 'grey', fg='white', font = self.master.fontstyle)
            current_val.place(relx = 0.5, rely = 0.25, relwidth = 0.8, relheight = 0.5, anchor = 'center')

            self.Accept_change = CustomButton.Button(master = self.master, root = self.new_wind.toplevel, relx = 0.5, rely = 0.75, width = 100, height = 30, text = "Accept Change",  command = self.set_new_val ,state = "DISABLED")

            data_entry = tk.Entry(self.new_wind.toplevel, textvariable = self.entry_text, justify = tk.CENTER)
            self.entry_text.trace_add('write', self.enable_accept)
            data_entry.place(relx = 0.5, rely= 0.5, anchor = 'center')
            data_entry.bind("<Return>", self.set_new_val)

    def enable_accept(self, x, y, z):
        if self.new_wind_open == True:
            self.Accept_change.enable()

    def  change_to_idle(self, yo):
        if self.state == "ENABLED":
            self.obj.config(bg = self.idleback)  

    def show_self(self):
        self.obj.config(text = self.entry_text.get())
        placement.smart_place(master = self.master, parent = self)

    def hide_self(self):
        self.obj.place_forget()

    def enable(self):
        self.state = "ENABLED"        
        self.obj.config(bg = self.idleback)
        self.obj.config(fg = 'white')
  
        self.show_self()

    def disable(self):
        self.state = "DISABLED"
        self.obj.config(bg = self.disabledback)
        self.obj.config(fg = 'grey')
        self.show_self()

    def set_new_val(self, *args):
        self.obj.config(fg = 'white')
        self.new_wind.toplevel.destroy()
        self.new_wind_open = False
        self.obj.config(bg = self.idleback)
        self.show_self()

        self.parent.revert_changes.enable()
        self.parent.save_changes.enable()  

    def recolor_text(self, new_color):
        self.obj.config(fg = new_color)
        self.show_self()