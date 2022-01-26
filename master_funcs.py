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
    new_func = lambda x: ((y2-y1)/(x2-x1)) * (x - x1) + y1

    return  new_func

def convert_elements_to_dict(elements):
    new_dict = {}
    for element in elements:
        if str(element.tag)[1:5] not in new_dict:
            new_dict[str(element.tag)[1:5]] = []
        new_dict[str(element.tag)[1:5]].append(element)

    return new_dict