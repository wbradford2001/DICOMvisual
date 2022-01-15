#imports
import tkinter as tk
import MenuButton
import TopLevelWindow
import DataTextBox
import LoadingBar
import CustomDFEdit
import master_funcs
import LoadFileCascade
import ExportCascade
import CustomCanvas
import DivideLine
import ImageIndicator
import CustomButton
from tkinter import filedialog
import pydicom
import os

class app:


    def __init__(self):

        self.fontstyle = 'Cambria'
        self.background = '#%02x%02x%02x' % (0, 0, 0)
        self.root= tk.Tk()
        self.width = 1200
        self.height = 600
        #self.root.attributes('-fullscreen', False)
        self.root.geometry("{}x{}".format(self.width,self.height))
        self.root.title('MyDICOMvisual')
        self.root.configure(bg = self.background)

    def define_menus(self):
        menubar = tk.Label(self.root, bg = '#%02x%02x%02x' % (30, 30, 30))
        menubar.place(x = 0, y = 0, relwidth  = 1, height = MenuButton.menu_button.menubuttonheight)
        self.Menu= MenuButton.menu_button(master = self, root= self.root, xpos= 0, width = 100, title = "Menu")



        self.Clear = CustomButton.Button(master = self, root = self.Menu.canvobj, relxpos = 1/12, relypos = 0.5, width = self.width/6, height =MenuButton.menu_button.canvasheight, 
            text = 'Clear', size_reduce=6, command = self.hide_all, state = "DISABLED")  
        self.NewFile = CustomButton.Button(master = self, root = self.Menu.canvobj, relxpos = 3/12, relypos = 0.5, width = self.width/6, height =MenuButton.menu_button.canvasheight, 
            text = 'Import File(s)', size_reduce=6, command = self.load, state = "ENABLED")  
        self.Export_DICOM_file = CustomButton.Button(master = self, root = self.Menu.canvobj, relxpos = 5/12, relypos = 0.5, width = self.width/6+2, height =MenuButton.menu_button.canvasheight, 
            text = 'Export', size_reduce=6, command = self.decide_export, state = "DISABLED")
        
        self.View_Full_DF = CustomButton.Button(master = self, root = self.Menu.canvobj, relxpos = 7/12, relypos = 0.5, width = self.width/6, height =MenuButton.menu_button.canvasheight, 
            text = 'View Full Data Frame', size_reduce=6, command = self.view_full_df, state = "DISABLED") 
        
        self.Custom_DF_Edit = CustomButton.Button(master = self, root = self.Menu.canvobj, relxpos = 9/12, relypos = 0.5, width = self.width/6, height =MenuButton.menu_button.canvasheight, 
            text = 'Edit Data Element(s)', size_reduce=6, command = self.custom_df_edit, state = "DISABLED")
        
        self.Exit = CustomButton.Button(master = self, root = self.Menu.canvobj, relxpos = 11/12, relypos = 0.5, width = self.width/6, height =MenuButton.menu_button.canvasheight, 
            text = 'Exit', size_reduce=6, command = self.root.destroy, state = "ENABLED")
        
    def define_canvases_and_dividers(self):     
        #define_canvases              
        View_Top_Line_Pos = (MenuButton.menu_button.canvasheight + MenuButton.menu_button.menubuttonheight)/self.height
        Text_Box_Top_Line_Pos = 0.7
        pixel_display_height = Text_Box_Top_Line_Pos - View_Top_Line_Pos



        self.MainViewCanvas = CustomCanvas.CustomCanv(master = self, parent = self, root = self.root, color = 'red', relposx = 0.3, relposy = View_Top_Line_Pos, relwidth = 0.3, relheight = pixel_display_height)

        self.SideView1Canvas = CustomCanvas.CustomCanv(master = self, parent = self,root = self.root, color = 'black', relposx = 0, relposy = View_Top_Line_Pos, relwidth = 0.3, relheight = pixel_display_height)
        self.SideView2Canvas = CustomCanvas.CustomCanv(master = self, parent = self,root = self.root, color = 'black', relposx = 0.6, relposy = View_Top_Line_Pos, relwidth = 0.3, relheight = pixel_display_height)
        self.TempImageIndicatorCanvas = CustomCanvas.CustomCanv(master = self, parent = self,root = self.root, color = '#%02x%02x%02x' % (70, 70, 70), relposx = self.SideView2Canvas.relposx + self.SideView2Canvas.relwidth, relposy = View_Top_Line_Pos, 
                                                        relwidth = 1-(self.SideView2Canvas.relposx + self.SideView2Canvas.relwidth), relheight = pixel_display_height)
        self.ImageIndicatorCanvas = CustomCanvas.CustomCanv(master = self, parent = self,root = self.root, color = '#%02x%02x%02x' % (70, 70, 70), relposx = self.SideView2Canvas.relposx + self.SideView2Canvas.relwidth, relposy = View_Top_Line_Pos, 
                                                        relwidth = 1-(self.SideView2Canvas.relposx + self.SideView2Canvas.relwidth), relheight = pixel_display_height)
        
        self.TextBoxCanvas = CustomCanvas.CustomCanv(master = self, parent = self,root = self.root, color = 'black', relposx = 0, relposy = Text_Box_Top_Line_Pos, relwidth = 1, relheight = 1-Text_Box_Top_Line_Pos)


        #define dividers
        self.View_Top_Line = DivideLine.Divider(master = self,root = self.root, orientation = 'horizontal', relposy = View_Top_Line_Pos, 
                width = self.root.winfo_screenwidth())
        
        self.Text_Box_Top_Line = DivideLine.Divider(master = self, root = self.root, orientation = 'horizontal', relposy = Text_Box_Top_Line_Pos, 
                width = self.root.winfo_screenwidth())

        self.SideView1toMainDivider = DivideLine.Divider(master = self, root = self.root, orientation = 'vertical', relposy = View_Top_Line_Pos, height = self.MainViewCanvas.actualheight + DivideLine.Divider.buffer/2, relposx = 0.3)

        self.MainDividertoSideView2 = DivideLine.Divider(master = self, root = self.root, orientation = 'vertical', relposy = View_Top_Line_Pos, height = self.MainViewCanvas.actualheight + DivideLine.Divider.buffer/2, relposx = 0.6)

        self.SideView2toImageIndicator = DivideLine.Divider(master = self, root = self.root, orientation = 'vertical', relposy = View_Top_Line_Pos, height = self.MainViewCanvas.actualheight+ DivideLine.Divider.buffer/2, relposx = 0.9)

    def define_display_boxes_and_image_indicators(self): 

        #define_display_boxes
        self.matches = {
            '0002': 'Meta Data',        
            '0008': 'Identifying Information',
            '0010': 'Patient Information',
            '0018': 'Aquisition Information',
            '0020': 'Relationship Information',
            '0028': 'Image Presentation',
            '0040': 'Text Information'                           
        }
        keys_included = []
        for key in self.display_strings['0'].keys():
            if key in self.matches:
                keys_included.append(key)
        self.text_boxes = {}
        num_boxes = len(keys_included)
        for index, key in enumerate(keys_included):
            self.text_boxes[key] = DataTextBox.data_window(master = self, root = self.TextBoxCanvas.canvobject, relposx = index/num_boxes, relposy = 0, title = self.matches[str(key)],width  = 1/num_boxes)

        if len(self.dfs) > 1:
        #define_image_indicators()
            self.Image_Indicators = {}
            for index, name in enumerate(self.image_names):
                self.Image_Indicators[index] = ImageIndicator.image_indicator(master = self, root = self.ImageIndicatorCanvas, text = name, index= index)
            self.Image_Indicator = self.Image_Indicators[self.MainView.currentim.get()]

    def show_all(self):
        if len(self.dfs) > 1:
            #show image indicator canvas
            self.ImageIndicatorCanvas.canvobject.place_configure(height = len(self.MainView.arr) * 20)
            #show_image_indicators
            for name, object in self.Image_Indicators.items():
                object.show_self()

        
            #show canvases, divide lines, and Views
            for index, obj in enumerate([self.MainViewCanvas, self.SideView1Canvas, self.SideView2Canvas, self.ImageIndicatorCanvas, self.TempImageIndicatorCanvas, self.TextBoxCanvas,
                                        self.View_Top_Line, self.Text_Box_Top_Line, self.SideView1toMainDivider, self.MainDividertoSideView2, self.SideView2toImageIndicator,
                                        self.MainView, self.SideView1, self.SideView2]):
                obj.show_self()
        else:
            #show canvases, divide lines, and Views
            
            for index, obj in enumerate([self.MainViewCanvas, self.TextBoxCanvas,
                                        self.View_Top_Line, self.Text_Box_Top_Line,
                                        self.MainView]):
                obj.show_self()
        #NOTE: display boxes will be displayed when Views are displayed
    def hide_all(self):
        master_funcs.configure_buttons("ENABLED", [self.NewFile])

        if len(self.dfs) > 1:
            #hide image indicator canvas
            self.ImageIndicatorCanvas.canvobject.place_forget()

            #hide canvases, divide lines, and Views
            for index, obj in enumerate([self.MainViewCanvas, self.SideView1Canvas, self.SideView2Canvas, self.ImageIndicatorCanvas, self.TempImageIndicatorCanvas, self.TextBoxCanvas,
                                        self.View_Top_Line, self.Text_Box_Top_Line,self.SideView1toMainDivider, self.MainDividertoSideView2, self.SideView2toImageIndicator,
                                        self.MainView, self.SideView1, self.SideView2]):
                obj.hide_self()
        else:
            #hide canvases, divide lines, and Views
            for index, obj in enumerate([self.MainViewCanvas, self.TextBoxCanvas,
                                        self.View_Top_Line, self.Text_Box_Top_Line, 
                                        self.MainView]):
                obj.hide_self()
    def load(self, from_existing_df = False):
        if from_existing_df == False:
            welcome_window.toplevel.destroy()
            [self.files, self.dfs, self.dfs_metas, self.image_names, errorflag] = LoadFileCascade.load_file(master = self)
        elif from_existing_df == True:
            self.loading_window, self.loading_bar = TopLevelWindow.loading_win(master = self, root = self.root, number_of_loads = 5 + len(self.files) )
            errorflag = False
            # self.loading_window = TopLevelWindow.top_window(master = self, root = self.root, width = 600, height = 250, title = "Loading Files", color = 'grey')
            # self.loading_bar = LoadingBar.loading_bar(master = self, parent = self.loading_window, root = self.loading_window.toplevel, 
            #                                 number_of_loads = 5 + len(self.files), 
            #                                 height = 80, 
            #                                 xpos = 50, 
            #                                 ypos = 100, 
            #                                 text_message = "Loading File Data", 
            #                                 text_y_offset = 100)
        if errorflag == False: 
            self.define_canvases_and_dividers()
            [self.MainView, self.SideView1, self.SideView2, self.display_strings, errorflag] = LoadFileCascade.populate_data_stuff(master = self)                    
            self.define_display_boxes_and_image_indicators()
            self.show_all()

            #delete menu
            self.Menu.canvobj.place_forget()
            self.Menu.buttonobj.place_forget()
            #redefine menu
            self.define_menus()
            master_funcs.configure_buttons("ENABLED", [self.View_Full_DF, self.Custom_DF_Edit, self.Export_DICOM_file, self.Clear])
            master_funcs.configure_buttons("DISABLED", [self.NewFile])


            self.cascade = CustomDFEdit.full_df_cascade()

    def view_full_df(self):

        self.cascade.create_full_df_toplevel(master = self, view_or_edit = 'view')
        
    def custom_df_edit(self):
        self.cascade.create_full_df_toplevel(master = self, view_or_edit = 'ENABLED')

    def decide_export(self):
        if len(self.dfs) > 1:
            self.just_one_or_many_wind = TopLevelWindow.just_one_or_many(master = self, root = self.root
                        ,message = "Would you like to export just " + str(self.image_names[self.MainView.currentim.get()]) 
                                    + " or all files?", image_name = str(self.image_names[self.MainView.currentim.get()]) ,
                                    proceed_command = self.export_dfs)
        else:
            self.export_dfs("Just One")
    def export_dfs(self, one_or_all):
        if len(self.dfs) > 1:
            self.just_one_or_many_wind.toplevel.destroy()

        if one_or_all == "Just One":
                save_dest_no_name = filedialog.asksaveasfile(title = 'Select Output Destination', defaultextension=".dcm")
                
                if not save_dest_no_name is None:
                    save_dest = save_dest_no_name.name
                    #save_as_srt = str(save_dest.name)
                    self.dfs[int(self.MainView.currentim.get())].file_meta = self.dfs_metas[self.MainView.currentim.get()]

                    self.dfs[int(self.MainView.currentim.get())].save_as(save_dest) 


                    confirm_window = TopLevelWindow.top_window(master = self, root = self.root, width = 300, height = 200, title = "Success", color = 'grey')
                    success_text = tk.Label(confirm_window.toplevel, text = 'Successfully Saved as ' + str(save_dest),bg = 'grey', fg = 'white', wraplength = 200)
                    success_text.place(relx = 0.5, rely = 0.5, anchor = 'center')
        elif one_or_all == "All":
            save_dest = filedialog.askdirectory(title = 'Select Export Destination')
            if len(save_dest) != 0:
                for index, dataframe in enumerate(self.dfs):
                        new_save_str = os.path.join(save_dest,"edited_" + self.image_names[index])
                        dataframe.file_meta = self.dfs_metas[index]
                        dataframe.save_as(new_save_str)
            
                confirm_window = TopLevelWindow.top_window(master = self, root = self.root, width = 300, height = 200, title = "Success", color = 'grey')
                success_text = tk.Label(confirm_window.toplevel, text = 'Successfully Saved ' + str(len(self.dfs)) + ' files to ' + str(save_dest),bg = 'grey', fg = 'white', wraplength = 200)
                success_text.place(relx = 0.5, rely = 0.5, anchor = 'center')



        # if len(dfs) > 1:
        #     CustomDFEdit.final_save_changes.bind('<Button>', save_changes_Edit_DF)
        # else:
        #     CustomDFEdit.save_button.bind('<Button>', save_changes_Edit_DF)

    # def save_changes_Edit_DF(self, hi):
    #     global MainView
    #     global SideView1
    #     global SideView2
    #     global display_strings
    #     CustomDFEdit.Full_DF_Wind.toplevel.destroy()
    #     try:
    #         CustomDFEdit.just_one_or_all_files.toplevel.destroy()
    #     except:
    #         pass
    #     loading_window = TopLevelWindow.top_window(root, 600, 400, title = "Loading Files", color = 'grey')
    #     loading_bar = LoadingBar.loading_bar(parent = loading_window, 
    #                                         number_of_loads = 5 + len(files), 
    #                                         height = 80, 
    #                                         xpos = 50, 
    #                                         ypos = 200, 
    #                                         text_message = "Editing File Data", 
    #                                         fontstyle = fontstyle,
    #                                         fontsize = 30,
    #                                         text_y_offset = 100)
    #     if CustomDFEdit.option.get() == "Just One":
    #         dfs[int(MainView.currentim.get())] = CustomDFEdit.save_changes_regular(dfs[int(MainView.currentim.get())])
    #         dfs_metas[int(MainView.currentim.get())] = CustomDFEdit.save_changes_meta(dfs_metas[int(MainView.currentim.get())])  

    #     elif CustomDFEdit.option.get() == "All":
    #         for index, dataframe in enumerate(dfs):
    #             dataframe = CustomDFEdit.save_changes_regular(dataframe)
    #         for index, dataframe in enumerate(dfs_metas):
    #             dataframe = CustomDFEdit.save_changes_meta(dataframe)

    #     [MainView, SideView1, SideView2, display_strings, errorflag] = LoadFileCascade.populate_data_stuff(loading_window = loading_window, loading_bar = loading_bar, 
    #                             root=root, fontstyle=fontstyle, dfs=dfs, dfs_metas=dfs_metas, 
    #                             image_names=image_names,
    #                             input_disp_str_func=display_display_strings)
    #     master_funcs.display_new_dfs_and_dfs_meta(MainView,dfs, SideView1, SideView2)

    # def decide_export(self):
    #     if len(dfs) == 1:
    #         global option
    #         option = tk.StringVar()
    #         option.set("Just One")
    #         ExportCascade.pull_up_window(root=root, fontstyle=fontstyle, dfs=dfs, dfs_metas=dfs_metas, MainView=MainView, image_names=image_names, option = option)
    #     elif len(dfs) >1:
    #         ExportCascade.produce_just_one_or_all_files_window(root=root, fontstyle=fontstyle, image_names=image_names, MainView=MainView, dfs=dfs, dfs_metas=dfs_metas)
    # def clear(self):
    #     for key, box in text_boxes.items():
    #             box.text_box_label.destroy()
    #             box.label.destroy()

    #     master_funcs.clear_pixel_array(MainView)

    #     MainView.image_text_label.place_forget()


    #     if len(dfs) > 1:
    #         master_funcs.clear_pixel_array(SideView1)
    #         master_funcs.clear_pixel_array(SideView2)


    #     master_funcs.configure_buttons("DISABLED", [View_Full_DF, Custom_DF_Edit, Export_DICOM_file, Clear])


if __name__ == "__main__":
    MyDICOMvisual = app()

    MyDICOMvisual.define_menus()


    welcome_window = TopLevelWindow.top_window(master = MyDICOMvisual, root = MyDICOMvisual.root, width = 500, height = 300, title = "Welcome!", color = 'grey')
    welcome = tk.Label(welcome_window.toplevel, text = "Welcome! Thank you for using MyDICOMvisual", bg = 'grey', fg = 'white', font = (MyDICOMvisual.fontstyle, '20'))
    instructions = tk.Label(welcome_window.toplevel, text = "Click below to get started", bg = 'grey', fg = 'white', font = (MyDICOMvisual.fontstyle, '10'))
    New_File_Welcome = CustomButton.Button(master= MyDICOMvisual, root= welcome_window.toplevel, relxpos = 0.5, relypos = 0.6, width  = 100, height = 50,
                text = "Load File(s)", size_reduce = 3, command = MyDICOMvisual.load)
    welcome.place(relx = 0.5, rely = 0.2, anchor = 'center')
    instructions.place(relx = 0.5, rely = 0.4, anchor = 'center')

    MyDICOMvisual.root.mainloop()