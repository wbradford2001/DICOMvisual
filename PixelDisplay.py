import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class pixel_display:
    scale_vals = [0]
    button_pressed = False
    dpi =500
    width = 250
    height = 250
    def __init__(self, root, title, arr, aspect, relposx, relposy, fontstyle, image_text_label = None, image_names = None, display_display_strings_func = None):
        self.fontstyle = fontstyle
        self.relposx = relposx
        self.relposy = relposy
        self.root = root
        self.title = title
        self.arr = arr
        self.aspect = aspect

        self.figure1 = plt.Figure(figsize=(5,5), dpi=pixel_display.dpi)
        self.figure1.patch.set_facecolor('black')

        self.ax1 = self.figure1.add_subplot(111)
        self.ax1.get_xaxis().set_visible(False)
        self.ax1.get_yaxis().set_visible(False)
        self.ax1.set_aspect(self.aspect)
        self.tkcanvas = FigureCanvasTkAgg(self.figure1, self.root)
        self.tkcanvas.get_tk_widget().place(relx = self.relposx, rely = self.relposy, anchor = 'center', width = pixel_display.width, height = pixel_display.height)
 



        self.currentim = tk.IntVar()
        self.currentim.set(self.arr.shape[0]//2)
        self.scale = tk.Scale(self.root, variable = self.currentim, background = 'black', fg = 'black', from_ = 0, to = self.arr.shape[0], showvalue = False)
        self.scale.place(relx = self.relposx + 0.15, rely = self.relposy, anchor= 'center', height = pixel_display.height)
        self.scale.bind('<B1-Motion>', self.decide)
      



        self.title_text = tk.Label(self.root, text = self.title, bg = 'black', fg = 'white', font = (self.fontstyle, 14))
        self.title_text.place(relx = self.relposx, rely = self.relposy - 0.2, anchor = 'center')

        self.text_label = tk.Label(self.root, bg = 'grey', fg = 'white', font = (self.fontstyle, 8))

        self.next_button = tk.Button(self.root, bg = 'grey', fg = 'black', font = self.fontstyle, text = 'next',command = self.next)
        self.next_button.place(relx = self.relposx + 0.09, rely = self.relposy + 0.2, width = 75, height = 25, anchor = 'center')

        self.back_button = tk.Button(self.root, bg = 'grey', fg = 'black', font = self.fontstyle, text = 'previous',command = self.back)
        self.back_button.place(relx = self.relposx - 0.09, rely = self.relposy + 0.2, width = 75, height = 25, anchor = 'center')


        self.tempcurrentim = tk.IntVar()
        self.goto_entry = tk.Entry(self.root, bd = 0, textvariable = self.tempcurrentim)
        self.goto_entry.place(relx = self.relposx, rely = self.relposy + 0.16, anchor = 'center', width = 40)
        self.tempcurrentim.trace_add("write", self.go_to)


        print("Defining it here")
        self.image_text_label = image_text_label
        self.image_names = image_names
        self.display_display_strings_func = display_display_strings_func
        self.text_label.place(relx=self.relposx, rely = self.relposy + 0.2, anchor = 'center')

    def next(self):
        try:
            self.currentim.set(self.currentim.get() + 1)
            self.display_image(2)
        except:
            print("Error - forward")
    def back(self):
        try:
            self.currentim.set(self.currentim.get() - 1)
            self.display_image(2)
        except:
            print("Error - back")
    def go_to(self, one, two, three):
        try:
            self.currentim.set(self.tempcurrentim.get())
            self.goto_entry.config(fg = 'black')
            self.display_image()
            self.display_GUI()            
        except Exception as e:
            self.goto_entry.config(fg = 'red')

    

    def decide(self, e):
        self.display_image()
        if self.root.winfo_pointery()-275 == e.y:
            self.display_GUI()
    def display_GUI(self):
            self.text_label.config(text = ("Array Bounds: {} x {}\nCurrent Frame: {} out of {}").format(
                self.arr.shape[1],
                self.arr.shape[2],
                self.currentim.get(),
                self.arr.shape[0]
                ))
            self.tempcurrentim.set(self.currentim.get())
            if self.image_text_label != None:
                try:
                    self.image_text_label.config(text = self.image_names[int(self.currentim.get())])
                except:
                    self.image_text_label.config(text = self.image_names[-1])   


                self.display_display_strings_func(self.currentim.get())   


    def display_image(self):

        #image = self.currentim.get()
        self.ax1.cla()
        if self.currentim.get() < len(self.arr):
            self.ax1.imshow(self.arr[self.currentim.get()], cmap = 'bone')
        else:
            self.ax1.imshow(self.arr[-1], cmap = 'bone')

        self.tkcanvas.draw()

          