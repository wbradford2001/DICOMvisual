import tkinter as tk
import numpy as np

def load_df_data(dfs):


    dictionary_of_catagories = {}
    for dataframe in dfs[0]:
        if (str(dataframe.tag)[1:5]) not in dictionary_of_catagories:
            dictionary_of_catagories[(str(dataframe.tag)[1:5])] = {}
        temp_dict = {}
        temp_dict[dataframe.tag] = str(dataframe.keyword), str(dataframe.VR), str(dataframe.value)
        dictionary_of_catagories[(str(dataframe.tag)[1:5])].update(temp_dict)
    Axial_arr = (np.array(dfs[0].pixel_array))


    display_strings = dictionary_of_catagories.copy()
    for i in dictionary_of_catagories.keys():
        temp_string = ''
        for j in dictionary_of_catagories[i]:
            temp_string = temp_string + str('{:}: {:}\n'.format(
                str(dictionary_of_catagories[i][j][0]),
                str(dictionary_of_catagories[i][j][2])
                ))
        display_strings[i] = temp_string

    ps = dfs[0].PixelSpacing
    ss = dfs[0].SliceThickness
    Axial_aspect=(ps[1]/ps[0])  



    return display_strings, Axial_arr, Axial_aspect