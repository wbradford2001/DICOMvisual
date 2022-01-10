import tkinter as tk
import numpy as np

def load_df_data(dfs, dfs_metas, loading_bar):

    MainView_arr = []
    master_dict_of_catagories = {}

    #populate dict of catagories for dfs
    for index, dataframe in enumerate(dfs):
        loading_bar.increase_width()
        master_dict_of_catagories[str(index)] = {}
        for element in dataframe:
            if (str(element.tag)[1:5]) not in master_dict_of_catagories[str(index)]:
                master_dict_of_catagories[str(index)][(str(element.tag)[1:5])] = {}
            temp_dict = {}
            temp_dict[element.tag] = str(element.keyword), str(element.VR), str(element.value)
            master_dict_of_catagories[str(index)][(str(element.tag)[1:5])].update(temp_dict)
        MainView_arr.append(dataframe.pixel_array[0:-1:1, 0:-1:1])

    #populate dict of catagories for dfs_metas
    for index, dataframe in enumerate(dfs_metas):
        #loading_bar.increase_width()
        for element in dataframe:
            if (str(element.tag)[1:5]) not in master_dict_of_catagories[str(index)]:
                master_dict_of_catagories[str(index)][(str(element.tag)[1:5])] = {}
            temp_dict = {}
            temp_dict[element.tag] = str(element.keyword), str(element.VR), str(element.value)
            master_dict_of_catagories[str(index)][(str(element.tag)[1:5])].update(temp_dict)



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