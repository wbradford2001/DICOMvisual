import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import CustomThings.DivideLine as DivideLine
import master_funcs
import CustomThings.ImageIndicator as ImageIndicator
import CustomThings.CustomButton as CustomButton

class pixel_display:
    scale_vals = [0]
    button_pressed = False
    dpi =50
    def __init__(self, master, parent_canv, title, arr, aspect, main_or_side):
        #initialize
        self.master = master
        self.parent_canv = parent_canv    
        self.title = title
        self.arr = arr
        self.aspect = aspect
        self.main_or_side = main_or_side
        self.already_moving = False

        #tkcanvas stuff
        self.figure1 = plt.Figure(figsize=(5,5), dpi=pixel_display.dpi)
        self.figure1.patch.set_facecolor('black')
        self.ax1 = self.figure1.add_subplot(111)
        self.ax1.get_xaxis().set_visible(False)
        self.ax1.get_yaxis().set_visible(False)
        self.ax1.set_aspect(self.aspect)
        self.tkcanvas = FigureCanvasTkAgg(self.figure1, self.parent_canv.canvobject)
        self.tkcanvas.get_tk_widget().place(
            relx = 0.5, rely = 0.5, anchor = 'center', relwidth = 1, relheight = 1)
 
        #scale
        self.currentim = tk.IntVar()
        self.currentim.set(self.arr.shape[0]//2)
        self.scale = tk.Scale(self.parent_canv.canvobject, variable = self.currentim, background = 'black', fg = 'black', from_ = 0, to = self.arr.shape[0]-1, showvalue = False)
        self.scale.bind('<B1-Motion>', self.decide)
      
        #title
        self.title_text = tk.Label(self.parent_canv.canvobject, text = self.title, bg = 'black', fg = 'white', font = (self.master.fontstyle, 14), wraplength = self.parent_canv.actualwidth/2)

        #text box at bottom
        self.text_label = tk.Label(self.parent_canv.canvobject, bg = 'black', fg = 'white', font = (self.master.fontstyle, 8))

        #next
        self.next_button = CustomButton.Button(master = self.master, root = self.parent_canv.canvobject, x = self.parent_canv.actualwidth - 20 - 30, y = self.parent_canv.actualheight - DivideLine.Divider.buffer/2 - 15,
                                width = 60, height = 30, text = 'Next',  command = self.next, show= False, )

        #back
        self.back_button = CustomButton.Button(master = self.master, root = self.parent_canv.canvobject, x = 20 + 30, y = self.parent_canv.actualheight - DivideLine.Divider.buffer/2 - 15,
                                width = 60, height = 30, text = 'Previous',  command = self.back, show= False, )
    

        #Go to entry
        self.tempcurrentim = tk.IntVar()
        self.goto_entry = tk.Entry(self.parent_canv.canvobject, bd = 0, textvariable = self.tempcurrentim, justify=tk.CENTER, selectborderwidth = 0, highlightcolor = 'black', relief = tk.FLAT, highlightthickness=0, highlightbackground='black')
        self.goto_entry.config({"background": 'grey'})
        #Go to button
        self.goto_button = CustomButton.Button(master = self.master, root = self.parent_canv.canvobject,
                                    x = self.parent_canv.actualwidth - DivideLine.Divider.buffer/2 - 20 - 75/2, 
                                    y = DivideLine.Divider.buffer/2 + 20/2 + 2, 
                                    width = 75, 
                                    height = 20, text = "Set Frame",  command = self.go_to, show = False)



        #main stuff
        if self.main_or_side == "main" and len(self.master.dfs) > 1:
                self.mapfunc = master_funcs.map_ranges(
                        [0, len(self.arr)-1], 
                        [self.master.ImageIndicatorCanvas.actualheight/2-ImageIndicator.image_indicator.height/2, 
                        -(ImageIndicator.image_indicator.height*len(self.arr)) + self.master.ImageIndicatorCanvas.actualheight/2+ImageIndicator.image_indicator.height/2]
                    )
    def show_self(self):
        #if multiple frames
        if self.master.multiple_images == True or self.master.multiframe == True: 
            self.scale.place(x = self.parent_canv.actualwidth - DivideLine.Divider.buffer/2, rely = 0.5, anchor= 'e', relheight = 1)
            #self.next_button.place(x = self.root.actualwidth - 20, y = self.root.actualheight - DivideLine.Divider.buffer/2, width = 60, height = 30, anchor = 'se')
            self.next_button.show_self()
            self.back_button.show_self()            
            self.goto_entry.place(x = self.parent_canv.actualwidth - DivideLine.Divider.buffer/2 - 20 - 80, y = DivideLine.Divider.buffer, anchor = 'ne', width = 35)
            self.goto_button.show_self()           
        else:
            self.title_text.config(text = self.master.image_names[0])

        self.title_text.place(x = DivideLine.Divider.buffer/2, y = DivideLine.Divider.buffer/2, anchor = 'nw')
        self.text_label.place(relx=0.5, y = self.parent_canv.actualheight - DivideLine.Divider.buffer/2 - 15, anchor = 'center')

        self.display_image()
        self.display_GUI()
    def hide_self(self):
        self.scale.place_forget()
        self.title_text.place_forget()
        self.text_label.place_forget()
        self.next_button.hide_self()
        self.back_button.hide_self()   
        self.goto_entry.place_forget()
        self.back_button.hide_self()  
    def next(self):
        if self.currentim.get() < len(self.arr):
            self.currentim.set(self.currentim.get() + 1)
            self.display_image()
            self.display_GUI()  
    def back(self):
        if self.currentim.get() > 0:
            self.currentim.set(self.currentim.get() - 1)
            self.display_image()
            self.display_GUI()  
    def go_to(self):
        try:
            self.currentim.set(self.tempcurrentim.get())
            self.goto_entry.config(fg = 'black')
            self.display_image()
            self.display_GUI()            
        except Exception as e:
            print("Error in Go To Entry")
            print(e)
            self.goto_entry.config(fg = 'red')

    def decide(self, e):
        if self.already_moving == False and self.main_or_side == 'main':
            for box in self.master.text_boxes.values():
                    box.text_box_label.configure(bg = '#%02x%02x%02x' % (40, 40, 40))       
            self.already_moving = True 
            if self.master.multiple_images == True:
                self.master.TempImageIndicatorCanvas.canvobject.config(bg = '#%02x%02x%02x' % (90, 90, 90))
                for indicator in self.master.Image_Indicators.values():
                    indicator.label.config(bg = '#%02x%02x%02x' % (90, 90, 90))
        self.display_image()

        print(e.y)
        print(self.master.root.winfo_pointery())
        if e.y == (self.master.root.winfo_pointery()-147):
             self.display_GUI()
             self.already_moving = False
    def display_GUI(self):

            if self.master.multiple_images == True:
                self.text_label.config(text = ("Array Bounds: {} x {}\nCurrent Frame: {} out of {}").format(
                    self.arr.shape[1],
                    self.arr.shape[2],
                    self.currentim.get(),
                    self.arr.shape[0]
                    ))
                #set go to entry
                self.tempcurrentim.set(self.currentim.get())
            elif self.master.multiple_images == False:            
                self.text_label.config(text = ("Array Bounds: {} x {}").format(
                    self.arr.shape[1],
                    self.arr.shape[2],
                    ))
            #main stuff
            if self.main_or_side == "main":
                #update title
                if self.master.multiframe == False:
                    self.title_text.config(text = "Main View: " + str(self.master.image_names[self.currentim.get()]))

                    #update display strings
                    for key, box in self.master.text_boxes.items():
                        box.text_box_label.configure(bg = 'black')
                        box.show_self(self.master.display_strings[str(self.currentim.get())][str(key)])
                elif self.master.multiframe == True:
                    self.title_text.config(text = "Main View: " + str(self.master.image_names[0]))
                    #update display strings
                    for key, box in self.master.text_boxes.items():
                        box.text_box_label.configure(bg = 'black')
                        box.show_self(self.master.display_strings[str(0)][str(key)])                    
                  

                if self.master.multiple_images == True:
                    #set the current image indicators colors to grey
                    self.master.Image_Indicator.orig_color = 'grey'
                    self.master.Image_Indicator.color_to_original(yo = 3)

                    #set new image indicator to currentim
                    self.master.Image_Indicator = self.master.Image_Indicators[self.currentim.get()]
                    self.master.Image_Indicator.orig_color = 'red'
                    self.master.Image_Indicator.recolor(yo = 3)

                    #configure image indicator canvas
                    self.master.ImageIndicatorCanvas.canvobject.place_configure(
                        y = self.mapfunc(self.currentim.get()),
                    
                    )


                    #recolor image indicators
                    for indicator in self.master.Image_Indicators.values():
                        indicator.label.config(bg = ImageIndicator.image_indicator.defaultbg)  
                    self.master.TempImageIndicatorCanvas.canvobject.config(bg = ImageIndicator.image_indicator.defaultbg)


    def display_image(self):
        self.ax1.cla()
        self.ax1.imshow(self.arr[self.currentim.get()], cmap = 'bone')
        self.tkcanvas.draw()



          