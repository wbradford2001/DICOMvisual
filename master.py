import tkinter as tk
from tkinter import filedialog
from matplotlib.pyplot import savefig, text
import pydicom
import numpy as np
import os

import MenuButton
import TopLevelWindow
import GenerateDfsData
import DataTextBox
import PixelDisplay
import LoadingBar
import CustomDFEdit
import master_funcs
import LoadFileCascade
import ExportCascade

fontstyle = 'Cambria'

def define_display_boxes():
    TBypos = 0.9
    matches = {
        '0002': 'Meta Data',        
        '0008': 'Identifying Information',
        '0010': 'Patient Information',
        '0018': 'Aquisition Information',
        '0020': 'Relationship Information',
        '0028': 'Image Presentation',
        '0040': 'Text Information'                           
    }

    keys_included = []
    for key in display_strings['0'].keys():

        if key in matches:

            keys_included.append(key)
    
    global text_boxes
    text_boxes = {}
    num_boxes = len(keys_included)


    for index, key in enumerate(keys_included):

        text_boxes[key] = DataTextBox.data_window(root = root, relposx = index/num_boxes, relposy = TBypos, title = matches[str(key)], fontstyle = fontstyle, width  = 1/num_boxes, height = 1/6)



def display_display_strings(index): 

    try:
        for key, box in text_boxes.items():
            box.show_self(display_strings[str(index)][str(key)])

    except KeyError:
        for key, box in text_boxes.items():
            box.show_self(display_strings[str(index-1)][str(key)])


def start_screen():
    no_pixel_array.place(relx = 0.5, rely = 0.35, anchor = 'center')
    divide_line.place(relx = 0, rely = 0.75, width = root.winfo_screenwidth(), height = 5)
    no_data.place(relx = 0.5, rely = 0.85, anchor = 'center')

def load():
    if no_data.winfo_ismapped() == False:
        clear()


    welcome_window.toplevel.destroy()
    global files
    global dfs
    global dfs_metas
    global image_names
    [files, dfs, dfs_metas, image_names] = LoadFileCascade.load_file(root = root, fontstyle = fontstyle)
    if files != False:
        global MainView
        global SideView1
        global SideView2
        global display_strings

        [MainView, SideView1, SideView2, display_strings, errorflag] = LoadFileCascade.populate_data_stuff(loading_window = LoadFileCascade.loading_window, 
                                                                            loading_bar = LoadFileCascade.loading_bar, 
                                                                            root = root, 
                                                                            fontstyle = fontstyle, 
                                                                            dfs = dfs, dfs_metas = dfs_metas, 
                                                                            image_names = image_names,
                                                                            input_disp_str_func=display_display_strings)
        if errorflag == False:                       
            master_funcs.configure_buttons(tk.NORMAL, [View_Full_DF.object, Custom_DF_Edit.object, Export_DICOM_file.object, Clear.object])
            master_funcs.remove_items([no_data, no_pixel_array])
            define_display_boxes()
            master_funcs.display_new_dfs_and_dfs_meta(MainView,dfs, SideView1, SideView2)
        else:

            clear()



def view_full_df():
    CustomDFEdit.create_full_df_toplevel(root = root, 
                                        imagename = image_names[MainView.currentim.get()], 
                                        df =  dfs[MainView.currentim.get()], df_meta = dfs_metas[MainView.currentim.get()],
                                        fontstyle = fontstyle, view_or_edit = 'view'
                                        )
    
def custom_df_edit():
    CustomDFEdit.create_full_df_toplevel(root = root, 
                                        imagename = image_names[MainView.currentim.get()], 
                                        df =  dfs[MainView.currentim.get()], df_meta = dfs_metas[MainView.currentim.get()],
                                        fontstyle = fontstyle
                                        )
    if len(dfs) > 1:
        CustomDFEdit.final_save_changes.bind('<Button>', save_changes_Edit_DF)
    else:
        CustomDFEdit.save_button.bind('<Button>', save_changes_Edit_DF)

def save_changes_Edit_DF(hi):
    global MainView
    global SideView1
    global SideView2
    global display_strings
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
        dfs[int(MainView.currentim.get())] = CustomDFEdit.save_changes_regular(dfs[int(MainView.currentim.get())])
        dfs_metas[int(MainView.currentim.get())] = CustomDFEdit.save_changes_meta(dfs_metas[int(MainView.currentim.get())])  

    elif CustomDFEdit.option.get() == "All":
        for index, dataframe in enumerate(dfs):
            dataframe = CustomDFEdit.save_changes_regular(dataframe)
        for index, dataframe in enumerate(dfs_metas):
            dataframe = CustomDFEdit.save_changes_meta(dataframe)

    [MainView, SideView1, SideView2, display_strings, errorflag] = LoadFileCascade.populate_data_stuff(loading_window = loading_window, loading_bar = loading_bar, 
                            root=root, fontstyle=fontstyle, dfs=dfs, dfs_metas=dfs_metas, 
                            image_names=image_names,
                            input_disp_str_func=display_display_strings)
    master_funcs.display_new_dfs_and_dfs_meta(MainView,dfs, SideView1, SideView2)

def decide_export():
    if len(dfs) == 1:
        global option
        option = tk.StringVar()
        option.set("Just One")
        ExportCascade.pull_up_window(root=root, fontstyle=fontstyle, dfs=dfs, dfs_metas=dfs_metas, MainView=MainView, image_names=image_names, option = option)
    elif len(dfs) >1:
        ExportCascade.produce_just_one_or_all_files_window(root=root, fontstyle=fontstyle, image_names=image_names, MainView=MainView, dfs=dfs, dfs_metas=dfs_metas)
def clear():
    for key, box in text_boxes.items():
            box.text_box_label.destroy()
            box.label.destroy()

    master_funcs.clear_pixel_array(MainView)

    MainView.image_text_label.place_forget()


    if len(dfs) > 1:
        master_funcs.clear_pixel_array(SideView1)
        master_funcs.clear_pixel_array(SideView2)










    start_screen()
    master_funcs.configure_buttons(tk.DISABLED, [View_Full_DF.object, Custom_DF_Edit.object, Export_DICOM_file.object, Clear.object])


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


    Clear = MenuButton.menu_button(root = root, text = "Clear", command = clear, fontstyle = fontstyle, 
        relx = 0, relwidth = 1/6, state= tk.DISABLED)
    New_File = MenuButton.menu_button(root = root, text = "New File", command = load, fontstyle = fontstyle, 
        relx = 1/6,  relwidth = 1/6,state= tk.NORMAL)
    Export_DICOM_file = MenuButton.menu_button(root = root, text = "Export DICOM file(s)", command = decide_export, fontstyle = fontstyle, 
        relx = 2/6, relwidth = 1/6, state= tk.DISABLED)
    View_Full_DF = MenuButton.menu_button(root = root, text = "View Full DF", command = view_full_df, fontstyle = fontstyle, 
        relx = 3/6, relwidth = 1/6, state = tk.DISABLED)
    Custom_DF_Edit = MenuButton.menu_button(root = root, text = "Custom DF Edit", command = custom_df_edit, fontstyle = fontstyle, 
        relx = 4/6,  relwidth = 1/6,state = tk.DISABLED)
    Exit = MenuButton.menu_button(root = root, text = "Exit", command = root.destroy, fontstyle = fontstyle, 
        relx = 5/6,  relwidth = 1/6,state= tk.NORMAL)



    welcome_window = TopLevelWindow.top_window(root, 500, 300, title = "Welcome!", color = 'grey')
    welcome = tk.Label(welcome_window.toplevel, text = "Welcome! Thank you for using MyDICOMvisual", bg = 'grey', fg = 'white', font = (fontstyle, '20'))
    instructions = tk.Label(welcome_window.toplevel, text = "Click 'Import File(s) to get started", bg = 'grey', fg = 'white', font = (fontstyle, '10'))

    welcome.place(relx = 0.5, rely = 0.2, anchor = 'center')
    instructions.place(relx = 0.5, rely = 0.6, anchor = 'center')

    start_screen()


    root.mainloop()