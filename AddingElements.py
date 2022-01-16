import tkinter as tk
import TopLevelWindow
import pydicom


#fix me
class add_element_entry:
    height = 50
    def __init__(self, master, parent_cascade, root, startval, relx, relwidth):
        self.master = master
        self.parent_cascade = parent_cascade
        self.root = root
        
        self.var = tk.StringVar()
        self.startval = startval
        self.relwidth = relwidth
        self.var.set(self.startval)
        self.obj = tk.Entry(self.root, textvariable = self.var, bg = '#%02x%02x%02x' % (200, 200, 200), fg= 'grey', 
                highlightcolor='black', bd = 0, highlightthickness=2, relief = tk.RIDGE, 
                justify=tk.CENTER, font = (self.master.fontstyle, 10))
        self.relx = relx
        self.obj.place(relx = self.relx, rely = 0.5, relwidth = self.relwidth, height = add_element_entry.height, anchor = 'center')
        self.obj.bind("<Button>", self.click_happened)

        self.var.trace_add("write", self.edit_happened)
        #self.var.trace("r", self.click_happened)        
      
    def click_happened(self, yo):
        print("YO")

        self.var.set("")
        #self.var.set(self.var.get())




    def edit_happened(self, yo, u, e):
        #if self.var.get() != self.startval:
            print("TO")
            self.obj.config(fg = 'black')


            self.parent_cascade.add_entry.enable()
            #self.obj.select_range(0, tk.END)

class add_element_cascade:
    def __init__(self, master, parent_cascade):
        self.master = master
        self.parent_cascade = parent_cascade
    def add_decide(self):
        if len(self.master.dfs) > 1:
            just_o_a_wind = TopLevelWindow.just_one_or_many(master=self.master, root =self.parent_cascade.Full_DF_Wind.toplevel
            , message = "Add Element for Just " + str(self.master.image_names[self.master.MainView.currentim.get()]) + " or for all files?", 
            image_name = str(self.master.image_names[self.master.MainView.currentim.get()]), proceed_command = self.add)
        else:
            self.add("Just One")            
    def add(self, o_a):
        if o_a == "Just One":
            errorflag = self.add_for_one_image(self.master.MainView.currentim.get())
        elif o_a == "All":
            errorflag = False
            for df_index in range(0, len(self.master.MainView.arr)):
                if errorflag == False:
                    errorflag  = self.add_for_one_image(df_index)
                

        if errorflag == False:
            self.master.hide_all()
            self.parent_cascade.Full_DF_Wind.toplevel.destroy()
            self.master.load(from_existing_df = True)
    
    def add_for_one_image(self, image):
        try:
            hex_one_string = self.parent_cascade.group_number_entry.var.get()
            hex_one = 0
            for index, digit in enumerate(reversed(hex_one_string)):
                hex_one += 16**index * int(digit)


            hex_two_string =self.parent_cascade.element_number_entry.var.get()
            hex_two = 0
            for index, digit in enumerate(reversed(hex_two_string)):
                hex_two += 16**index * int(digit)        

            self.master.dfs[image].add_new([hex(hex_one), hex(hex_two)], pydicom.datadict.dictionary_VR([hex(hex_one), hex(hex_two)]), self.parent_cascade.Value_Entry.var.get())
            print("Adding to image " + str(image))
            return False
        except Exception as e:
            print(e)
            TopLevelWindow.show_error_window(master = self.master, root = self.parent_cascade.add_element_top_window.toplevel, 
                message = "Unable to add element", ErrorString = e)
            return True

              
