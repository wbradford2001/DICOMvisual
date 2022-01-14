import tkinter as tk
import numpy as np
from tkinter import filedialog
import TopLevelWindow
import LoadingBar
import pydicom
import os
import PixelDisplay



def load_file(master):


        files = filedialog.askopenfilenames(title = 'Select Dicom File(s)', filetypes=[("DICOM", '.dcm')])
        #try:

        master.loading_window = TopLevelWindow.top_window(master = master, root = master.root, width = 600, height = 400, title = "Loading Files", color = 'grey')
        master.loading_bar = LoadingBar.loading_bar(master = master, parent = master.loading_window, root = master.loading_window.toplevel, 
                                            number_of_loads = 5 + len(files) + len(files), 
                                            height = 80, 
                                            xpos = 50, 
                                            ypos = 200, 
                                            text_message = "Loading File Data", 
                                            text_y_offset = 100)
        
        dfs = []
        dfs_metas = []
        image_names = []
        for file in files:
            master.loading_bar.increase_width("Reading Files")
            temp_df = pydicom.dcmread(file)
            dfs.append(temp_df)
            dfs_metas.append(temp_df.file_meta)
            image_names.append(os.path.basename(file))

        return files, dfs, dfs_metas, image_names, False
        
        # except Exception as e:

        #     loading_window.toplevel.destroy()
        #     print(e)
        #     EW = TopLevelWindow.show_error_window(root, fontstyle, message="Unable to Load File(s)", ErrorString = e)
        #     return False, False, False, False
def load_df_data(dfs, dfs_metas, loading_bar):

    MainView_arr = []
    master_dict_of_catagories = {}

    #populate dict of catagories for dfs_metas
    for index, dataframe in enumerate(dfs_metas):
        #loading_bar.increase_width()
        master_dict_of_catagories[str(index)] = {}
        for element in dataframe:
            if (str(element.tag)[1:5]) not in master_dict_of_catagories[str(index)]:
                master_dict_of_catagories[str(index)][(str(element.tag)[1:5])] = {}
            temp_dict = {}
            temp_dict[element.tag] = str(element.keyword), str(element.VR), str(element.value)
            master_dict_of_catagories[str(index)][(str(element.tag)[1:5])].update(temp_dict)

    #populate dict of catagories for dfs
    for index, dataframe in enumerate(dfs):
        loading_bar.increase_width("Extracting Data Elements")
        #master_dict_of_catagories[str(index)] = {}
        for element in dataframe:
            if (str(element.tag)[1:5]) not in master_dict_of_catagories[str(index)]:
                master_dict_of_catagories[str(index)][(str(element.tag)[1:5])] = {}
            temp_dict = {}
            temp_dict[element.tag] = str(element.keyword), str(element.VR), str(element.value)
            master_dict_of_catagories[str(index)][(str(element.tag)[1:5])].update(temp_dict)
        MainView_arr.append(dataframe.pixel_array[0:-1:1, 0:-1:1])





    MainView_arr = np.asarray(MainView_arr)

    SideView2_arr = []
    for j in range(0, MainView_arr.shape[1]):
        
        SideView2_arr.append((MainView_arr[:,j,:]))
    SideView2_arr = np.array(SideView2_arr)

    SideView1_arr = []
    for k in range(0, MainView_arr.shape[2]):
            SideView1_arr.append(MainView_arr[:, :, k])
    SideView1_arr = np.array(SideView1_arr)  

    master_dict_display_strings = {}
    for key, value in master_dict_of_catagories.items():
        master_dict_display_strings[str(key)] = value.copy()
        for i in value.keys():
            temp_string = ''
            for j in value[i]:
                temp_string = temp_string + str('{:}: {:}\n'.format(
                    str(value[i][j][0]),
                    str(value[i][j][2])
                    ))
            master_dict_display_strings[str(key)][i] = temp_string

    ps = dfs[0].PixelSpacing
    ss = dfs[0].SliceThickness
    MainView_aspect=(ps[1]/ps[0])            
    SideView1_aspect=(ps[1]/ss)
    SideView2_aspect=(ss/ps[0])



    return master_dict_display_strings, MainView_arr, MainView_aspect, SideView1_arr, SideView1_aspect, SideView2_arr, SideView2_aspect

def populate_data_stuff(master):

    
        master.loading_window.toplevel.update()
        master.loading_bar.increase_width("Gathering Pixel Array Data")
    # try:
        display_strings, MainView_arr, MainView_aspect, SideView1_arr, SideView1_aspect, SideView2_arr, SideView2_aspect = load_df_data(master.dfs, master.dfs_metas, master.loading_bar)

        current_image_text_label = tk.Label(master.root, 
                                        bg = 'black',
                                        fg = 'white',
                                        font = (master.fontstyle, 10)
        )                                 
        if len(master.dfs) == 1:
            master.MainViewCanvas.relposx = 0.5-(master.MainViewCanvas.relwidth/2)

            MainView = PixelDisplay.pixel_display(master = master, parent_canv = master.MainViewCanvas, title= "Main View", arr=MainView_arr, aspect=MainView_aspect,main_or_side = "main")

            master.loading_bar.increase_width("Generated Main View")
            master.loading_bar.increase_width("Generated Main View")
            SideView1 = None
            SideView2 = None

        else:

            MainView = PixelDisplay.pixel_display(master = master, parent_canv = master.MainViewCanvas, title= "Main View", arr=MainView_arr, aspect=MainView_aspect, main_or_side = "main")
                
            master.loading_bar.increase_width("Generated Main View")


            SideView1 = PixelDisplay.pixel_display(master = master, parent_canv = master.SideView1Canvas, title= "Side View 1", arr=SideView1_arr, aspect=SideView1_aspect,  main_or_side = "side")


            SideView2 = PixelDisplay.pixel_display(master = master, parent_canv = master.SideView2Canvas, title= "Side View 2", arr=SideView2_arr, aspect=SideView2_aspect,main_or_side = "side")
            master.loading_bar.increase_width("Generated Side Views")

        master.loading_bar.increase_width("Loading Display Elements")

        



        

        master.loading_window.toplevel.destroy()



        
        return MainView, SideView1, SideView2, display_strings, False
    # except Exception as e:
        
    #     loading_window.toplevel.destroy()
    #     EW = TopLevelWindow.show_error_window(root, fontstyle, message="Unable to Load File(s)", ErrorString = e)
    #     print(e)
    #     return MainView, SideView1, SideView2, display_strings, True