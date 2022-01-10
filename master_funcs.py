import tkinter as tk
import LoadFileCascade
def remove_items(items):
    for item in items:
        item.place_forget()

def configure_buttons(configure_to, button_list):
    for button in button_list:
        button.configure(state= configure_to)

def display_new_dfs_and_dfs_meta(MainView,dfs, SideView1, SideView2):
        MainView.display_image(100)
        if len(dfs)>1:
            SideView1.display_image(100)
            SideView2.display_image(100)

def clear_pixel_array(Pixel_Array):

        Pixel_Array.scale.place_forget()

        Pixel_Array.title_text.place_forget()

        Pixel_Array.text_label.place_forget()

        Pixel_Array.tkcanvas.get_tk_widget().place_forget()
        Pixel_Array.next.place_forget()
        Pixel_Array.back.place_forget()
