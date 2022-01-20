from multiprocessing.context import ForkServerContext
from re import M
import tkinter as tk
import numpy as np
from tkinter import filedialog
import TopLevelWindow
import LoadingBar
import pydicom
import os
import PixelDisplay
import master_funcs



class load_file_cascade:
    def __init__(self, master):
        self.master = master

    def load_file(self, from_existing_df, force_num_views = False):
        

        #LOAD FILE
            #if from existing DF
            if from_existing_df == False:

                #destroy welcom window
                self.master.welcome_window.toplevel.destroy()
                #produce filedialog
                self.master.files = filedialog.askopenfilenames(title = 'Select Dicom File(s)', filetypes=[("DICOM", '.dcm')])

                #if theres actuall files
                print(len(self.master.files))
                if (len(self.master.files)) != 0:
                    #create loading window
                    self.master.loading_window, self.master.loading_bar = TopLevelWindow.loading_win(master = self.master, root = self.master.root, number_of_loads = 5 + len(self.master.files) + len(self.master.files))

                    #populate dfs, dfs_metas, and image_names
                    self.master.dfs = []
                    self.master.dfs_metas = []
                    self.master.image_names = []
                    for file in self.master.files:
                            try:
                                self.master.loading_bar.increase_width("Reading Files")
                                temp_df = pydicom.dcmread(file)
                                self.master.dfs.append(temp_df)
                                self.master.dfs_metas.append(temp_df.file_meta)
                                self.master.image_names.append(os.path.basename(file))
                            except Exception as e:
                                errorstring = str(e)
                                if 'Use force=True to force reading' in str(e):
                                    errorstring = "File is missing DICOM File Meta Information header or the 'DICM' prefix is missing from the header."
                                self.master.loading_window.toplevel.destroy()
                                error_wind = TopLevelWindow.show_error_window(master = self.master, root = self.master.root,
                                            message = "Unable to Load " + str(file), ErrorString = errorstring, width = 500, height = 300)
                                return
                else:
                    return
            else:   
                self.master.hide_all()
                self.master.loading_window, self.master.loading_bar = TopLevelWindow.loading_win(master = self.master, root = self.master.root, number_of_loads = 5 + len(self.master.files))
            if force_num_views != False:
                self.master.num_views = force_num_views            
            #self multiple images to true or false
            if len(self.master.dfs) > 1:
                self.master.multiple_images = True
                
                
            else:
                self.master.multiple_images = False

            if len(self.master.dfs) < 100 and force_num_views == False:
                self.master.num_views= 1
                print("Set num_views to 1")                
            elif len(self.master.dfs) >= 100 and force_num_views == False:
                self.master.num_views = 3
                print("Set num_views to 3")

        #POPULATE DATA STUFF
            self.master.define_canvases_and_dividers()
            
            self.master.loading_window.toplevel.update()
            self.master.loading_bar.increase_width("Gathering Pixel Array Data")
        # LOAD DF DATA


            MainView_arr = []
            master_dict_of_catagories = {}

            #populate dict of catagories for dfs_metas
            for index, dataframe in enumerate(self.master.dfs_metas):
                #loading_bar.increase_width()
                master_dict_of_catagories[str(index)] = {}
                for element in dataframe:
                    if (str(element.tag)[1:5]) not in master_dict_of_catagories[str(index)]:
                        master_dict_of_catagories[str(index)][(str(element.tag)[1:5])] = {}
                    temp_dict = {}
                    temp_dict[element.tag] = str(element.keyword), str(element.VR), str(element.value)
                    master_dict_of_catagories[str(index)][(str(element.tag)[1:5])].update(temp_dict)

            #populate dict of catagories for dfs
            for index, dataframe in enumerate(self.master.dfs):
                self.master.loading_bar.increase_width("Extracting Data Elements")
                for element in dataframe:
                    if (str(element.tag)[1:5]) not in master_dict_of_catagories[str(index)]:
                        master_dict_of_catagories[str(index)][(str(element.tag)[1:5])] = {}
                    temp_dict = {}
                    temp_dict[element.tag] = str(element.keyword), str(element.VR), str(element.value)
                    master_dict_of_catagories[str(index)][(str(element.tag)[1:5])].update(temp_dict)
    
                #append pixel array to mainview arr
                if len(dataframe.pixel_array[0:-1:1, 0:-1:1].shape) == 2:
                    MainView_arr.append(dataframe.pixel_array[0:-1:1, 0:-1:1])
                else: 
                    if self.master.multiple_images == False:
                        MainView_arr = dataframe.pixel_array[0:-1:1, 0:-1:1]
                        self.master.multiframe = True
                        self.master.multiple_images = False

            #convert mainview arr to np array
            MainView_arr = np.asarray(MainView_arr)

            #define display_strings
            self.master.display_strings = {}
            for key, value in master_dict_of_catagories.items():
                self.master.display_strings[str(key)] = value.copy()
                for i in value.keys():
                    temp_string = ''
                    for j in value[i]:
                        temp_string = temp_string + str('{:}: {:}\n'.format(
                            str(value[i][j][0]),
                            str(value[i][j][2])
                            ))
                    self.master.display_strings[str(key)][i] = temp_string


            #populate array of other views
            if self.master.num_views == 3:
                SideView2_arr = []
                for j in range(0, MainView_arr.shape[1]):
                    SideView2_arr.append((MainView_arr[:,j,:]))
                SideView2_arr = np.array(SideView2_arr)
                SideView1_arr = []
                for k in range(0, MainView_arr.shape[2]):
                        SideView1_arr.append(MainView_arr[:, :, k])
                SideView1_arr = np.array(SideView1_arr)  
 
            #define aspects
            try:
                ps = self.master.dfs[0].PixelSpacing
                MainView_aspect=(ps[1]/ps[0])     
            except AttributeError:
                print("No PixelSpacing Attribute")
                MainView_aspect = 1

            if self.master.num_views == 3:
                try:
                    ss = self.master.dfs[0].SliceThickness
                    SideView1_aspect=(ps[1]/ss)
                    SideView2_aspect=(ss/ps[0])
                    if force_num_views == False:
                        self.master.num_views = 3

                except AttributeError:
                    print("No SliceThickness")

                    self.master.num_views = 1
                    if force_num_views == 3:
                        errorstring = "Unable to Display File in biplanar view: file missing SliceThickness Attribute"
                        self.master.loading_window.toplevel.destroy()
                        error_wind = TopLevelWindow.show_error_window(master = self.master, root = self.master.root,
                                    message = "Unable to Load " + str(file), ErrorString = errorstring, width = 500, height = 300)
                        return
                
            #make sure display strings display catagories of others
            total_keys = []
            for display_string in self.master.display_strings.values():
                total_keys.extend(display_string.keys())

            unique_keys = (np.unique(total_keys))
            for index, display_string in self.master.display_strings.items():
                for key in unique_keys:
                    if key not in display_string.keys():
                        self.master.display_strings[index][key] = ""


            #define views
             
            #single views              
            if self.master.num_views == 1:
                self.master.MainViewCanvas.relposx = 0.5-(self.master.MainViewCanvas.relwidth/2)

                self.master.MainView = PixelDisplay.pixel_display(master = self.master, parent_canv = self.master.MainViewCanvas, title= "Main View", arr=MainView_arr, aspect=MainView_aspect,main_or_side = "main")

                self.master.loading_bar.increase_width("Generated Main View")
                self.master.loading_bar.increase_width("Generated Main View")

            #multiple views
            elif self.master.num_views == 3:
                
                self.master.MainView = PixelDisplay.pixel_display(master = self.master, parent_canv = self.master.MainViewCanvas, title= "Main View", arr=MainView_arr, aspect=MainView_aspect, main_or_side = "main")
                
                self.master.loading_bar.increase_width("Generated Main View")
                self.master.SideView1 = PixelDisplay.pixel_display(master = self.master, parent_canv = self.master.SideView1Canvas, title= "Side View 1", arr=SideView1_arr, aspect=SideView1_aspect,  main_or_side = "side")
                self.master.SideView2 = PixelDisplay.pixel_display(master = self.master, parent_canv = self.master.SideView2Canvas, title= "Side View 2", arr=SideView2_arr, aspect=SideView2_aspect,main_or_side = "side")
                
                self.master.loading_bar.increase_width("Generated Side Views")

            self.master.loading_bar.increase_width("Loading Display Elements")

            self.master.loading_window.toplevel.destroy()


            #define display boxes and image indicators
            self.master.define_display_boxes_and_image_indicators()

            #delete menus
            self.master.File.obj.place_forget()
            self.master.Options.obj.place_forget()
                           

            #redefine menu
            self.master.define_menus()
            master_funcs.configure_buttons("ENABLED", [self.master.View_Full_DF, self.master.Custom_DF_Edit, self.master.Export_DICOM_file, self.master.Clear, self.master.Anonymize])
            

            master_funcs.configure_buttons("DISABLED", [self.master.Load_BiPlanar_View, self.master.Load_MonoPlanar_View])    
            if self.master.num_views == 1 and self.master.multiple_images == True or self.master.num_views == 1 and self.master.multiframe == True:
                master_funcs.configure_buttons("ENABLED", [self.master.Load_BiPlanar_View])     
            
            if self.master.num_views == 3 and self.master.multiple_images == True or self.master.num_views == 3 and self.master.multiframe == True:
                master_funcs.configure_buttons("ENABLED", [self.master.Load_MonoPlanar_View]) 
                                         
            
            master_funcs.configure_buttons("DISABLED", [self.master.NewFile])

            self.master.show_all()

