import tkinter as tk
import numpy as np

def load_df_data(dfs):

    master_dict_of_catagories = {}
    for index, dataframe in enumerate(dfs):
        master_dict_of_catagories[str(index)] = {}
        for element in dataframe:
            if (str(element.tag)[1:5]) not in master_dict_of_catagories[str(index)]:
                master_dict_of_catagories[str(index)][(str(element.tag)[1:5])] = {}
            temp_dict = {}
            temp_dict[element.tag] = str(element.keyword), str(element.VR), str(element.value)
            master_dict_of_catagories[str(index)][(str(element.tag)[1:5])].update(temp_dict)
        Axial_arr = (np.array(dfs[0].pixel_array))

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
    Axial_aspect=(ps[1]/ps[0])  



    return master_dict_display_strings, Axial_arr, Axial_aspect