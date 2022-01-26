
import tkinter as tk
import CustomThings.TopLevelWindow as TopLevelWindow



#fix me
class delete_cascade:
    def __init__(self, master, parent_cascade):
        self.master = master
        self.parent_cascade = parent_cascade
        self.delete_elements = []
    def set_delete_elements(self, list):
        for button in list:
            if button.pressed == True:
                self.delete_elements.append(button.value)
    def final_delete(self, o_a):



        if o_a == "Just One":
            self.process_image(self.master.MainView.currentim.get())
        elif o_a == "All":
            for index, df in enumerate(self.master.dfs):
                self.process_image(index)
        self.parent_cascade.Full_DF_Wind.toplevel.destroy()
        self.master.hide_all()
        self.master.load(from_existing_df = True)
    def process_image(self, image_index):
        for tag in self.delete_elements:
            if tag in (self.master.dfs[image_index]):
                del (self.master.dfs[image_index][tag])
            elif tag in (self.master.dfs_metas[image_index]):
                del (self.master.dfs_metas[image_index][tag])        
