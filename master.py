import tkinter as tk
from tkinter import filedialog
import pydicom
import numpy as np
import MenuButton
import TopLevelWindow
import GenerateDfsData
import DataTextBox
import PixelDisplay

fontstyle = 'Cambria'

#initialize window
root= tk.Tk()
window_width = 1400
window_height = 1000
root.geometry("{}x{}".format(window_width,window_height))
root.title('Knee Renderer')
root.configure(bg = 'black')

no_data = tk.Label(root, text = 'No Data Available', bg = 'black', fg = 'white', font = (fontstyle, '20', 'bold italic') )
divide_line = tk.Label(bg = 'white')
no_pixel_array = tk.Label(root, text = 'No Pixel Array Available', bg = 'black', fg = 'white', font = (fontstyle, '20', 'bold italic') )

TBypos = 0.8
IdentifyTB = DataTextBox.data_window(root = root, relposx = 1/7, relposy = TBypos, title = "Identifying Information", fontstyle = fontstyle)
PatientTB = DataTextBox.data_window(root = root, relposx = 2/7, relposy = TBypos, title = "Patient Information", fontstyle = fontstyle)
AquisitionTB = DataTextBox.data_window(root = root, relposx = 3/7, relposy = TBypos, title = "Aquisition Information", fontstyle = fontstyle)
RelationshipTB = DataTextBox.data_window(root = root, relposx = 4/7, relposy = TBypos, title = "Relationship Information", fontstyle = fontstyle)
ImagePresentationTB = DataTextBox.data_window(root = root, relposx = 5/7, relposy = TBypos, title = "Image Presentation", fontstyle = fontstyle)
TextTB = DataTextBox.data_window(root = root, relposx = 6/7, relposy = TBypos, title = "Text Information", fontstyle = fontstyle)






def remove_items(items):
    for item in items:
        item.place_forget()

def start_screen():
    no_pixel_array.place(relx = 0.5, rely = 0.25, anchor = 'center')
    divide_line.place(relx = 0, rely = 0.6, width = root.winfo_screenwidth(), height = 5)
    no_data.place(relx = 0.5, rely = 0.8, anchor = 'center')

def load_file():
    files = filedialog.askopenfilenames(title = 'select dicome file(s)')
    global dfs
    dfs = []
    for file in files:
        dfs.append(pydicom.dcmread(file))

    display_strings, Axial_arr, Axial_aspect = GenerateDfsData.load_df_data(dfs)

    Axial = PixelDisplay.pixel_display(root, title= "Axial", arr=Axial_arr, aspect=Axial_aspect, relposx = 0.5, relposy = 0.3)
    Axial.display_image()

    remove_items([no_data, no_pixel_array])
    IdentifyTB.show_self(display_strings['0008'])
    PatientTB.show_self(display_strings['0010'])
    AquisitionTB.show_self(display_strings['0018'])
    RelationshipTB.show_self(display_strings['0020'])
    ImagePresentationTB.show_self(display_strings['0028'])
    TextTB.show_self(display_strings['0040'])

def view_full_df():
    full_df_window = TopLevelWindow.top_window(root=root, width=800, height=800, title = "Full Data Frame")
    full_df_label = tk.Text(full_df_window.toplevel, bg = 'black', fg = 'white', font = ('Arial', 15), wrap = 'word',bd = 0, relief = 'flat', height= 800, width = 800)
    full_df_label.insert(tk.END, str(dfs[0]))
    full_df_label.pack()



New_File = MenuButton.menu_button(root = root, text = "New File", command = load_file, fontstyle = fontstyle, x = 0)
View_Full_DF = MenuButton.menu_button(root = root, text = "View Full DF", command = view_full_df, fontstyle = fontstyle, x = MenuButton.menu_button.width)


welcome_window = TopLevelWindow.top_window(root, 400, 200, title = "Welcome!")
welcome = tk.Label(welcome_window.toplevel, text = "Welcome! Thank you for using DICOM-visualizer", bg = 'black', fg = 'white', font = (fontstyle, '15'))
instructions = tk.Label(welcome_window.toplevel, text = "Click 'Import File(s) to get started", bg = 'black', fg = 'white', font = (fontstyle, '10'))

welcome.place(relx = 0.5, rely = 0.2, anchor = 'center')
instructions.place(relx = 0.5, rely = 0.6, anchor = 'center')



start_screen()


root.mainloop()