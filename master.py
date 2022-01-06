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

def configure_buttons(configure_to, button_list):
    for button in button_list:
        button.configure(state= configure_to)

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

    display_strings, Axial_arr, Axial_aspect, Sagittal_arr, Sagittal_aspect, Coronal_arr, Coronal_aspect = GenerateDfsData.load_df_data(dfs)

    if len(dfs) == 1:
        Axial = PixelDisplay.pixel_display(root, title= "Axial", arr=Axial_arr, aspect=Axial_aspect, relposx = 0.5, relposy = 0.3, fontstyle = fontstyle)
        Axial.display_image(100)
    else:
        Axial = PixelDisplay.pixel_display(root, title= "Axial", arr=Axial_arr, aspect=Axial_aspect, relposx = 1/6, relposy = 0.3, fontstyle = fontstyle)
        Axial.display_image(100)

        Sagittal = PixelDisplay.pixel_display(root, title= "Sagittal", arr=Sagittal_arr, aspect=Sagittal_aspect, relposx = 0.5, relposy = 0.3, fontstyle = fontstyle)
        Sagittal.display_image(100)

        Coronal = PixelDisplay.pixel_display(root, title= "Coronal", arr=Coronal_arr, aspect=Coronal_aspect, relposx = 5/6, relposy = 0.3, fontstyle = fontstyle)
        Coronal.display_image(100)

    configure_buttons(tk.NORMAL, [View_Full_DF.object])

    remove_items([no_data, no_pixel_array])
    IdentifyTB.show_self(display_strings['0']['0008'])
    PatientTB.show_self(display_strings['0']['0010'])
    AquisitionTB.show_self(display_strings['0']['0018'])
    RelationshipTB.show_self(display_strings['0']['0020'])
    ImagePresentationTB.show_self(display_strings['0']['0028'])
    TextTB.show_self(display_strings['0']['0040'])

def view_full_df():
    full_df_window = TopLevelWindow.top_window(root=root, width=800, height=800, title = "Full Data Frame")
    full_df_label = tk.Text(full_df_window.toplevel, bg = 'black', fg = 'white', font = ('Arial', 15), wrap = 'word',bd = 0, relief = 'flat', height= 800, width = 800)
    full_df_label.insert(tk.END, str(dfs[0]))
    full_df_label.pack()


Exit = MenuButton.menu_button(root = root, text = "Exit", command = root.destroy, fontstyle = fontstyle, x = 0, state= tk.NORMAL)
New_File = MenuButton.menu_button(root = root, text = "New File", command = load_file, fontstyle = fontstyle, x = MenuButton.menu_button.width, state= tk.NORMAL)
View_Full_DF = MenuButton.menu_button(root = root, text = "View Full DF", command = view_full_df, fontstyle = fontstyle, x = 2*MenuButton.menu_button.width, state = tk.DISABLED)

welcome_window = TopLevelWindow.top_window(root, 600, 400, title = "Welcome!", color = 'grey')
welcome = tk.Label(welcome_window.toplevel, text = "Welcome! Thank you for using DICOM-visualizer", bg = 'grey', fg = 'white', font = (fontstyle, '20'))
instructions = tk.Label(welcome_window.toplevel, text = "Click 'Import File(s) to get started", bg = 'grey', fg = 'white', font = (fontstyle, '10'))

welcome.place(relx = 0.5, rely = 0.2, anchor = 'center')
instructions.place(relx = 0.5, rely = 0.6, anchor = 'center')



start_screen()


root.mainloop()