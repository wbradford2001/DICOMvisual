import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class pixel_display:
    dpi = 50
    width = 300
    height = 300
    def __init__(self, root, title, arr, aspect, relposx, relposy):
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
    def display_image(self):
        self.ax1.cla()
        self.ax1.imshow(self.arr, cmap = 'bone')
        self.tkcanvas.draw()