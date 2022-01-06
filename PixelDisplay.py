import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class pixel_display:
    dpi = 50
    width = 300
    height = 300
    def __init__(self, root, title, arr, aspect, relposx, relposy, fontstyle):
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
        self.currentim.set(100)
        self.scale = tk.Scale(self.root, variable = self.currentim, background = 'black', fg = 'black', from_ = 0, to = self.arr.shape[0], command = self.display_image)
        self.scale.place(relx = self.relposx + 0.15, rely = self.relposy, anchor= 'center', height = pixel_display.height)

        self.title_text = tk.Label(self.root, text = self.title, bg = 'black', fg = 'white', font = (self.fontstyle, 14))
        self.title_text.place(relx = self.relposx, rely = self.relposy - 0.2, anchor = 'center')
    def display_image(self, image):
        image = self.currentim.get()
        self.ax1.cla()
        try:
            self.ax1.imshow(self.arr[int(image)], cmap = 'bone')
        except:
            self.ax1.imshow(self.arr[-1], cmap = 'bone')
        self.tkcanvas.draw()