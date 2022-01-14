import tkinter as tk



class CustomEntryClass:
    height = 30
    text_size = 15
    defaultdisabedcolor ='#%02x%02x%02x' % (40, 40, 40)
    defaultidlecolor = '#%02x%02x%02x' % (70, 70, 70)
    defaultactivecolor = '#%02x%02x%02x' % (100, 120, 100)
    defaultpressedcolor = 'blue'
    def __init__(self, master, root, index,  xpos, width, text, 
                    disableback = defaultdisabedcolor, idlecolor = defaultidlecolor, activecolor = defaultactivecolor, pressedcolor = defaultpressedcolor,
                    state = "ENABLED", view_or_edit = 'edit', size_reduce = 4):
        self.master = master
        self.root = root
        self.index = index
        self.width = width
        self.xpos = xpos
        self.state = state
        if len(str(text))< 60:
            self.text = str(text)
        else:
            self.text = "Unable to display date element with string"
            self.state = "DISABLED"
        self.disabledback= disableback
        self.idleback = idlecolor
        self.activeback = activecolor
        self.pressedback= pressedcolor
        self.obj = tk.Label(self.root, bg = self.idleback, borderwidth=2)
        self.text_label = tk.Text(self.obj, font= self.master.fontstyle, bg = CustomEntryClass.defaultidlecolor, fg = 'white', borderwidth=0, highlightthickness=0)
        self.text_label.place(relx =0.5, rely = 0.7, relwidth = 1, relheight = 1, anchor = 'center')
        self.text_label.tag_config('center', justify= 'center')
        self.text_label.insert(tk.END, self.text)
        self.text_label.tag_add('center', '1.0', 'end')



        self.view_or_edit = view_or_edit
        self.size_reduce = size_reduce
        if self.state == "ENABLED" or self.state == "view":
            self.obj.config(bg = self.idleback)
            self.obj.config(fg = 'white')
            self.text_label.config(bg = self.idleback)
            self.text_label.config(fg = 'white')            
        elif self.state == "DISABLED":
            self.obj.config(bg = self.disabledback)
            self.obj.config(fg = 'grey')
            self.text_label.config(bg = self.disabledback)
            self.text_label.config(fg = 'grey')              
        elif self.state == "TITLE":
            self.obj.config(bg = '#%02x%02x%02x' % (100, 100, 100))
            self.obj.config(fg = 'white')   
            self.text_label.config(bg = '#%02x%02x%02x' % (100, 100, 100))
            self.text_label.config(fg = 'white')                         
        self.obj.bind('<Enter>', self.change_to_active)
        self.obj.bind('<Leave>', self.change_to_idle) 
        self.obj.bind('<Button>', self.change_to_pressed)
        self.obj.bind('<ButtonRelease>', self.change_to_active) 
       
    def change_to_active(self, yo):
        if self.state == "ENABLED":
            self.text_label.config(bg = self.activeback)
            self.obj.config(bg = self.activeback)
            self.obj.place_configure(x = self.xpos + self.size_reduce/2, y = self.index * CustomEntryClass.height + self.size_reduce/2,
                width = self.width - self.size_reduce, height = CustomEntryClass.height - self.size_reduce)

    def  change_to_pressed(self, yo):
        if self.state == "ENABLED":
            self.obj.config(bg = self.pressedback)
            self.text_label.config(bg = self.pressedback)


    def  change_to_idle(self, yo):
        if self.state == "ENABLED":
            self.obj.config(bg = self.idleback)
            self.text_label.config(bg = self.idleback)
            self.obj.place_configure(x = self.xpos, y = self.index * CustomEntryClass.height, width = self.width , height = CustomEntryClass.height )
    def show_self(self):

        self.obj.place(x= self.xpos, y = self.index * CustomEntryClass.height, width = self.width, height = CustomEntryClass.height, anchor = 'nw')

    def hide_self(self):
        self.obj.place_forget()
    def enable(self):
        self.state = "ENABLED"        
        self.obj.config(bg = self.idleback)
        self.obj.config(fg = 'white')
        self.text_label.config(bg = self.idleback)
        self.text_label.config(fg = 'white')
        self.obj.place()

    def disable(self):
        self.state = "DIABLED"
        self.obj.config(bg = self.disabledback)
        self.obj.config(fg = 'grey')
        self.text_label.config(bg = self.disabledback)
        self.text_label.config(fg = 'grey')
        self.obj.place()
