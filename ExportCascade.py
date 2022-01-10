import tkinter as tk
from tkinter import filedialog
import os
import TopLevelWindow




def produce_just_one_or_all_files_window(root, fontstyle, image_names, MainView, dfs, dfs_metas):
#create objects for final save changes window
    global just_one_or_all_files
    just_one_or_all_files = TopLevelWindow.top_window(root, width = 400, height=100, title = "Save Changes", color = 'grey')
    just_one_or_all_files.toplevel.withdraw()

    global option
    option = tk.StringVar()

    global just_one
    just_one = tk.Radiobutton(just_one_or_all_files.toplevel, text = 'Just for ' + image_names[int(MainView.currentim.get())], variable = option, value = "Just One",
    bg = 'grey', fg = 'black', font = fontstyle)
    just_one.select()
    
    global all
    all = tk.Radiobutton(just_one_or_all_files.toplevel, text = 'All Files', variable = option, value = "All", 
    bg = 'grey', fg = 'black', font = fontstyle)
    
    global final_save_changes
    final_export = tk.Button(just_one_or_all_files.toplevel, text = "Export", bg = 'black', fg = 'black', 
    command = lambda: pull_up_window(root, fontstyle, dfs, dfs_metas, MainView, image_names, option))

    just_one_or_all_files.toplevel.deiconify()
    just_one.place(relx = 0.33, rely = 0.33, anchor = 'center')
    all.place(relx = 0.75, rely = 0.33, anchor = 'center')
    final_export.place(relx = 0.5, rely = 0.66, relwidth = 0.4, relheight = 0.3, anchor = 'center')


    
def pull_up_window(root, fontstyle, dfs, dfs_metas, MainView, image_names, option):
    try:
        just_one_or_all_files.toplevel.destroy()
    except:
        pass
    if option.get() == "Just One":
        
        save_dest = filedialog.asksaveasfile(title = 'Select Export Destination', defaultextension=".dcm")
        try:
            save_as_srt = str(save_dest.name)
            dfs[int(MainView.currentim.get())].file_meta = dfs_metas[MainView.currentim.get()]
            dfs[int(MainView.currentim.get())].save_as(save_as_srt)
        except:
            EW = TopLevelWindow.show_error_window(root=root, fontstyle=fontstyle, message="Unable to Save File(s)")

    else:
        save_dest = filedialog.askdirectory(title = 'Select Export Destination')
        try:
            for index, dataframe in enumerate(dfs):
                    new_save_str = os.path.join(save_dest,"edited_" + image_names[index])
                    dataframe.file_meta = dfs_metas[index]
                    dataframe.save_as(new_save_str)
        except Exception as e:
            print(e)
            EW = TopLevelWindow.show_error_window(root=root, fontstyle=fontstyle, message="Unable to Save File(s)")
