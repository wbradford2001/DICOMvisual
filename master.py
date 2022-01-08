import tkinter as tk
from tkinter import filedialog, image_names
from matplotlib.pyplot import savefig
import pydicom
import numpy as np
import os

import MenuButton
import TopLevelWindow
import GenerateDfsData
import DataTextBox
import PixelDisplay
import LoadingBar
import ViewFullDataFrame
import CustomDFEdit

fontstyle = 'Cambria'


#initialize window

def display_display_strings(index):
    IdentifyTB.show_self(display_strings[str(index)]['0008'])
    PatientTB.show_self(display_strings[str(index)]['0010'])
    AquisitionTB.show_self(display_strings[str(index)]['0018'])
    RelationshipTB.show_self(display_strings[str(index)]['0020'])
    ImagePresentationTB.show_self(display_strings[str(index)]['0028'])
    TextTB.show_self(display_strings['0']['0040'])

def update_display_strings(index):
    IdentifyTB.show_self(display_strings[str(index)]['0008'])
    PatientTB.show_self(display_strings[str(index)]['0010'])
    AquisitionTB.show_self(display_strings[str(index)]['0018'])
    RelationshipTB.show_self(display_strings[str(index)]['0020'])
    ImagePresentationTB.show_self(display_strings[str(index)]['0028'])
    TextTB.show_self(display_strings[str(index)]['0040'])



def remove_items(items):
    for item in items:
        item.place_forget()

def configure_buttons(configure_to, button_list):
    for button in button_list:
        button.configure(state= configure_to)

def start_screen():
    no_pixel_array.place(relx = 0.5, rely = 0.35, anchor = 'center')
    divide_line.place(relx = 0, rely = 0.75, width = root.winfo_screenwidth(), height = 5)
    no_data.place(relx = 0.5, rely = 0.85, anchor = 'center')

def load_file():

    welcome_window.toplevel.destroy()

    global files
    files = filedialog.askopenfilenames(title = 'Select Dicom File(s)')

    loading_window = TopLevelWindow.top_window(root, 600, 400, title = "Loading Files", color = 'grey')
    loading_bar = LoadingBar.loading_bar(parent = loading_window, 
                                        number_of_loads = 5 + len(files) + len(files), 
                                        height = 80, 
                                        xpos = 50, 
                                        ypos = 200, 
                                        text_message = "Loading File Data", 
                                        fontstyle = fontstyle,
                                        fontsize = 30,
                                        text_y_offset = 100)
    global dfs
    global image_names
    dfs = []
    image_names = []
    for file in files:
        loading_bar.increase_width()
        dfs.append(pydicom.dcmread(file))
        image_names.append(os.path.basename(file))
    display_DFS(loading_window, loading_bar)
def display_DFS(loading_window, loading_bar):

    
    loading_window.toplevel.update()
    loading_bar.increase_width()
    global display_strings
    display_strings, Axial_arr, Axial_aspect, Sagittal_arr, Sagittal_aspect, Coronal_arr, Coronal_aspect = GenerateDfsData.load_df_data(dfs, loading_bar)

    current_image_text_label = tk.Label(root, 
                                    bg = 'black',
                                    fg = 'white',
                                    font = (fontstyle, 10)
    )
    global Axial                                  
    if len(dfs) == 1:

        Axial = PixelDisplay.pixel_display(root, title= "Axial", arr=Axial_arr, aspect=Axial_aspect, relposx = 0.5, relposy = 0.5, fontstyle = fontstyle,
                            image_text_label = current_image_text_label, image_names = image_names, display_display_strings_func = update_display_strings)
        Axial.display_image(100)
        Axial.scale.place_forget()
    else:

        Sagittal = PixelDisplay.pixel_display(root, title= "Sagittal", arr=Sagittal_arr, aspect=Sagittal_aspect, relposx = 1/6, relposy = 0.5, fontstyle = fontstyle)
        loading_bar.increase_width()


        Axial = PixelDisplay.pixel_display(root, title= "Axial", arr=Axial_arr, aspect=Axial_aspect, relposx = 0.5, relposy = 0.5, fontstyle = fontstyle,
                            image_text_label = current_image_text_label, image_names = image_names, display_display_strings_func = update_display_strings)
        loading_bar.increase_width()

        global Coronal
        Coronal = PixelDisplay.pixel_display(root, title= "Coronal", arr=Coronal_arr, aspect=Coronal_aspect, relposx = 5/6, relposy = 0.5, fontstyle = fontstyle)
        loading_bar.increase_width()

    loading_bar.increase_width()

    Axial.display_image(100)
    if len(dfs)>1:
        Coronal.display_image(100)
        Sagittal.display_image(100)
    
    configure_buttons(tk.NORMAL, [View_Full_DF.object, Custom_DF_Edit.object])


    remove_items([no_data, no_pixel_array])
    display_display_strings(Axial.currentim.get())

    current_image_text_label.place(relx = Axial.relposx, rely = Axial.relposy - 0.23, anchor = 'center')
    

    loading_window.toplevel.destroy()

def view_full_df():
    ViewFullDataFrame.create_full_df_toplevel(root = root, 
                                        imagename = image_names[Axial.currentim.get()], 
                                        df =  dfs[Axial.currentim.get()],
                                        fontstyle = fontstyle
                                        )
    
def custom_df_edit():
    CustomDFEdit.create_full_df_toplevel(root = root, 
                                        imagename = image_names[Axial.currentim.get()], 
                                        df =  dfs[Axial.currentim.get()],
                                        fontstyle = fontstyle
                                        )
    if len(dfs) > 1:
        CustomDFEdit.final_save_changes.bind('<Button>', save_changes_Edit_DF)
    else:
        CustomDFEdit.save_button.bind('<Button>', save_changes_Edit_DF)

def save_changes_Edit_DF(hi):
    CustomDFEdit.Full_DF_Wind.toplevel.destroy()
    try:
        CustomDFEdit.just_one_or_all_files.toplevel.destroy()
    except:
        pass
    loading_window = TopLevelWindow.top_window(root, 600, 400, title = "Loading Files", color = 'grey')
    loading_bar = LoadingBar.loading_bar(parent = loading_window, 
                                        number_of_loads = 5 + len(files), 
                                        height = 80, 
                                        xpos = 50, 
                                        ypos = 200, 
                                        text_message = "Editing File Data", 
                                        fontstyle = fontstyle,
                                        fontsize = 30,
                                        text_y_offset = 100)
    if CustomDFEdit.option.get() == "Just One":
        dfs[int(Axial.currentim.get())] = CustomDFEdit.save_changes(dfs[int(Axial.currentim.get())])
    elif CustomDFEdit.option.get() == "All":
        for index, dataframe in enumerate(dfs):
            dataframe = CustomDFEdit.save_changes(dataframe)
    display_DFS(loading_window,loading_bar)


if __name__ == "__main__":
    root= tk.Tk()
    #window_width = 1400
    #window_height = 1000
    root.attributes('-fullscreen', True)
    #root.geometry("{}x{}".format(window_width,window_height))
    root.title('MyDICOMvisual')
    root.configure(bg = 'black')

    no_data = tk.Label(root, text = 'No Data Available', bg = 'black', fg = 'white', font = (fontstyle, '20', 'bold italic') )
    divide_line = tk.Label(bg = 'white')
    no_pixel_array = tk.Label(root, text = 'No Pixel Array Available', bg = 'black', fg = 'white', font = (fontstyle, '20', 'bold italic') )

    TBypos = 0.9
    IdentifyTB = DataTextBox.data_window(root = root, relposx = 1/7, relposy = TBypos, title = "Identifying Information", fontstyle = fontstyle)
    PatientTB = DataTextBox.data_window(root = root, relposx = 2/7, relposy = TBypos, title = "Patient Information", fontstyle = fontstyle)
    AquisitionTB = DataTextBox.data_window(root = root, relposx = 3/7, relposy = TBypos, title = "Aquisition Information", fontstyle = fontstyle)
    RelationshipTB = DataTextBox.data_window(root = root, relposx = 4/7, relposy = TBypos, title = "Relationship Information", fontstyle = fontstyle)
    ImagePresentationTB = DataTextBox.data_window(root = root, relposx = 5/7, relposy = TBypos, title = "Image Presentation", fontstyle = fontstyle)
    TextTB = DataTextBox.data_window(root = root, relposx = 6/7, relposy = TBypos, title = "Text Information", fontstyle = fontstyle)

    Exit = MenuButton.menu_button(root = root, text = "Exit", command = root.destroy, fontstyle = fontstyle, x = 0, state= tk.NORMAL)
    New_File = MenuButton.menu_button(root = root, text = "New File", command = load_file, fontstyle = fontstyle, x = MenuButton.menu_button.width, state= tk.NORMAL)
    View_Full_DF = MenuButton.menu_button(root = root, text = "View Full DF", command = view_full_df, fontstyle = fontstyle, x = 2*MenuButton.menu_button.width, state = tk.DISABLED)
    Custom_DF_Edit = MenuButton.menu_button(root = root, text = "Custom DF Edit", command = custom_df_edit, fontstyle = fontstyle, x = 3*MenuButton.menu_button.width, state = tk.DISABLED)



    welcome_window = TopLevelWindow.top_window(root, 500, 300, title = "Welcome!", color = 'grey')
    welcome = tk.Label(welcome_window.toplevel, text = "Welcome! Thank you for using MyDICOMvisual", bg = 'grey', fg = 'white', font = (fontstyle, '20'))
    instructions = tk.Label(welcome_window.toplevel, text = "Click 'Import File(s) to get started", bg = 'grey', fg = 'white', font = (fontstyle, '10'))

    welcome.place(relx = 0.5, rely = 0.2, anchor = 'center')
    instructions.place(relx = 0.5, rely = 0.6, anchor = 'center')

    start_screen()


    root.mainloop()