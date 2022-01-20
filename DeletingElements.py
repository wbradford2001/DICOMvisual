
import tkinter as tk
import TopLevelWindow



#fix me
class delete_cascade:
    def __init__(self):
        pass
    def Delete_From_Button_List(self, master, parent_cascade, ButtonList):

        self.master = master
        self.parent_cascade = parent_cascade
        self.ButtonList = ButtonList
        if self.master.multiple_images == True:
            just_o_o_m_wind = TopLevelWindow.just_one_or_many(master=master, root=parent_cascade.Full_DF_Wind.toplevel, 
                        message = "Would you like to delete Element(s) for just " + str(master.image_names[master.MainView.currentim.get()]) + " or for all files?", 
                        image_name = str(master.image_names[master.MainView.currentim.get()]), proceed_command = self.final_delete)
        else:
            self.final_delete("Just One")
    def final_delete(self, o_a):
        self.delete_elements = []
        for button in self.ButtonList:
            if button.pressed == True:
                self.delete_elements.append(button.value)

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
