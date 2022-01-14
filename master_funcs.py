import tkinter as tk


def configure_buttons(configure_to, button_list):
    if configure_to == "ENABLED":
        for button in button_list:
            button.enable()
    elif configure_to == "DISABLED":
        for button in button_list:
            button.disable()

def map_ranges(range1, range2):
    y1 = range2[0]
    y2 = range2[1]
    x1 = range1[0]
    x2 = range1[1]
    #print("x1:{}, x2:{}, y1: {}, y2: {}".format(x1, x2, y1, y2))
    new_func = lambda x: ((y2-y1)/(x2-x1)) * (x - x1) + y1

    return  new_func