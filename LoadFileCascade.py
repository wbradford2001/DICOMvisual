import tkinter as tk
from tkinter import filedialog
import TopLevelWindow
import LoadingBar
import pydicom
import os
import GenerateDfsData
import PixelDisplay
import master_funcs
import ViewFullDataFrame
import CustomDFEdit


def load_file(root, fontstyle):


        files = filedialog.askopenfilenames(title = 'Select Dicom File(s)', filetypes=[("DICOM", '.dcm')])
        try:

            global loading_window
            global loading_bar
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
            
            dfs = []
            dfs_metas = []
            image_names = []
            for file in files:
                loading_bar.increase_width()
                temp_df = pydicom.dcmread(file)
                dfs.append(temp_df)
                dfs_metas.append(temp_df.file_meta)
                image_names.append(os.path.basename(file))

            return files, dfs, dfs_metas, image_names
        
        except Exception as e:

            loading_window.toplevel.destroy()
            EW = TopLevelWindow.show_error_window(root, fontstyle, message="Unable to Load File(s)", ErrorString = e)
            return False, False, False, False


def populate_data_stuff(loading_window, loading_bar, root, fontstyle, dfs, dfs_metas, image_names, input_disp_str_func):

    
    loading_window.toplevel.update()
    loading_bar.increase_width()
    try:
        global display_strings
        display_strings, MainView_arr, MainView_aspect, SideView1_arr, SideView1_aspect, SideView2_arr, SideView2_aspect = GenerateDfsData.load_df_data(dfs, dfs_metas, loading_bar)

        current_image_text_label = tk.Label(root, 
                                        bg = 'black',
                                        fg = 'white',
                                        font = (fontstyle, 10)
        )                                 
        if len(dfs) == 1:

            MainView = PixelDisplay.pixel_display(root, title= "Main View", arr=MainView_arr, aspect=MainView_aspect, relposx = 0.5, relposy = 0.5, fontstyle = fontstyle,
                            image_text_label = current_image_text_label, image_names = image_names, display_display_strings_func = input_disp_str_func)

            MainView.scale.place_forget()


            SideView1 =None
            SideView2 = None
        else:

            MainView = PixelDisplay.pixel_display(root, title= "Main View", arr=MainView_arr, aspect=MainView_aspect, relposx = 0.5, relposy = 0.5, fontstyle = fontstyle,
                            image_text_label = current_image_text_label, image_names = image_names, display_display_strings_func = input_disp_str_func)
            loading_bar.increase_width()


            SideView1 = PixelDisplay.pixel_display(root, title= "Side View 1", arr=SideView1_arr, aspect=SideView1_aspect, relposx = 1/6, relposy = 0.5, fontstyle = fontstyle)
            loading_bar.increase_width()



            SideView2 = PixelDisplay.pixel_display(root, title= "Side View 2", arr=SideView2_arr, aspect=SideView2_aspect, relposx = 5/6, relposy = 0.5, fontstyle = fontstyle)
            loading_bar.increase_width()

        loading_bar.increase_width()

        


        current_image_text_label.place(relx = MainView.relposx, rely = MainView.relposy - 0.23, anchor = 'center')
        

        loading_window.toplevel.destroy()



        
        return MainView, SideView1, SideView2, display_strings, False
    except Exception as e:

        loading_window.toplevel.destroy()
        EW = TopLevelWindow.show_error_window(root, fontstyle, message="Unable to Load File(s)", ErrorString = e)
            
        return MainView, SideView1, SideView2, display_strings, True