#imports

import tkinter as tk
import EditWindows.AnonymizeDF as AnonymizeDF
import CustomThings.MenuButton as MenuButton
import CustomThings.TopLevelWindow as TopLevelWindow
import CustomThings.DataTextBox as DataTextBox

import master_funcs
import Cascades.LoadFileCascade as LoadFileCascade

import CustomThings.CustomCanvas as CustomCanvas
import CustomThings.DivideLine as DivideLine
import CustomThings.ImageIndicator as ImageIndicator
import CustomThings.CustomButton as CustomButton
from tkinter import filedialog
import pydicom
import os
import EditWindows.ViewFullDF as ViewFullDF
import EditWindows.EditAddDelete as EditAddDelete
import DataBaseStuff.AnonymizeDataBase as AnonymizeDataBase
import EditWindows.ViewPrivateElements as ViewPrivateElements

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

        self.load_file_cascade = LoadFileCascade.load_file_cascade(master = self)

        self.multiple_images =  None
        self.num_views = 3
        self.multiframe = False
        self.o_a = None
   

    def define_menus(self):

        menubar = tk.Label(self.root, bg =  MenuButton.menu_button.top_botton_color)
        menubar.place(x = 0, y = 0, relwidth = 1, height = MenuButton.menu_button.menubuttonheight)
        self.File= MenuButton.menu_button(master = self, root= self.root, title = "File", relx= 1/20, relwidth = 1/10, anchor = 'center', num_buttons = 4)

        self.Options= MenuButton.menu_button(master = self, root= self.root, title = "Options",  relx= 3/20, relwidth = 1/10, anchor = 'center', num_buttons = 1)


        

        self.NewFile = CustomButton.Button(master = self, root = self.File.canvobj, relx = 1/8, y = 0, relwidth = 1/4,  height =MenuButton.menu_button.canvasheight, 
            text = 'Import File(s)', command = self.load, state = "ENABLED", anchor = 'n')  
        self.Export_DICOM_file = CustomButton.Button(master = self, root = self.File.canvobj, relx = 3/8, y = 0, relwidth = 1/4,  height =MenuButton.menu_button.canvasheight, 
            text = 'Export',  command = self.decide_export, state = "DISABLED", anchor = 'n')  
        self.Clear = CustomButton.Button(master = self, root = self.File.canvobj, relx = 5/8, y = 0, relwidth = 1/4, height =MenuButton.menu_button.canvasheight, 
            text = 'Clear', command = self.hide_all, state = "DISABLED",anchor = 'n')  
        self.Exit = CustomButton.Button(master = self, root = self.File.canvobj, relx = 7/8, y = 0, relwidth = 1/4,  height =MenuButton.menu_button.canvasheight, 
            text = 'Exit',command = self.root.destroy, state = "ENABLED", anchor = 'n')              



        self.Custom_DF_Edit = CustomButton.Button(master = self, root = self.Options.canvobj, relx = 1/12, y = 0, relwidth = 1/5,  height =MenuButton.menu_button.canvasheight, 
            text = 'Edit Data Element(s)', command = self.custom_df_edit, state = "DISABLED", anchor = 'n') 

        self.Anonymize = CustomButton.Button(master = self, root = self.Options.canvobj, relx = 3/12, y = 0, relwidth = 1/5,  height =MenuButton.menu_button.canvasheight, 
            text = 'Anonymize', command = self.anonymize, state = "DISABLED", anchor = 'n')             


        self.Load_MonoPlanar_View = CustomButton.Button(master = self, root = self.Options.canvobj, relx = 5/12, y = 0, relwidth = 1/6,  height =MenuButton.menu_button.canvasheight, 
            text = 'Load Monopanar View',  command = lambda: self.load(True, 1), state = "DISABLED", anchor = 'n')  
        
        self.Load_BiPlanar_View = CustomButton.Button(master = self, root = self.Options.canvobj, relx = 7/12, y = 0, relwidth = 1/6, height =MenuButton.menu_button.canvasheight, 
            text = 'Load Biplanar View',  command = lambda: self.load(True, 3), state = "DISABLED", anchor = 'n')  
        
        self.View_Full_DF = CustomButton.Button(master = self, root = self.Options.canvobj,relx = 9/12, y = 0, relwidth = 1/6,  height =MenuButton.menu_button.canvasheight, 
            text = 'View Full Data Frame',  command = self.view_full_df, state = "DISABLED", anchor = 'n')  
        
        self.View_private_elements = CustomButton.Button(master = self, root = self.Options.canvobj,relx = 11/12, y = 0, relwidth = 1/6,  height =MenuButton.menu_button.canvasheight, 
            text = 'View Private Data Elements',  command = self.view_private_elements, state = "DISABLED", anchor = 'n')  


        self.File.display_canvas(5)

        

        
    def define_canvases_and_dividers(self):     
        #define_canvases              
        View_Top_Line_Pos = (MenuButton.menu_button.menubuttonheight + MenuButton.menu_button.canvasheight)/self.height
        Text_Box_Top_Line_Pos = 0.7
        pixel_display_height = Text_Box_Top_Line_Pos - View_Top_Line_Pos



        self.MainViewCanvas = CustomCanvas.CustomCanv(master = self, parent = self, root = self.root, color = 'red', relposx = 0.3, relposy = View_Top_Line_Pos, relwidth = 0.3, relheight = pixel_display_height)
        self.SideView2Canvas = CustomCanvas.CustomCanv(master = self, parent = self,root = self.root, color = 'black', relposx = 0.6, relposy = View_Top_Line_Pos, relwidth = 0.3, relheight = pixel_display_height)

        if self.num_views == 3:
            self.SideView1Canvas = CustomCanvas.CustomCanv(master = self, parent = self,root = self.root, color = 'black', relposx = 0, relposy = View_Top_Line_Pos, relwidth = 0.3, relheight = pixel_display_height)
        
        if self.multiple_images == True:
            self.TempImageIndicatorCanvas = CustomCanvas.CustomCanv(master = self, parent = self,root = self.root, color = '#%02x%02x%02x' % (70, 70, 70), relposx = self.SideView2Canvas.relposx + self.SideView2Canvas.relwidth, relposy = View_Top_Line_Pos, 
                                                        relwidth = 1-(self.SideView2Canvas.relposx + self.SideView2Canvas.relwidth), relheight = pixel_display_height)
            self.ImageIndicatorCanvas = CustomCanvas.CustomCanv(master = self, parent = self,root = self.root, color = '#%02x%02x%02x' % (70, 70, 70), relposx = self.SideView2Canvas.relposx + self.SideView2Canvas.relwidth, relposy = View_Top_Line_Pos, 
                                                        relwidth = 1-(self.SideView2Canvas.relposx + self.SideView2Canvas.relwidth), relheight = pixel_display_height)
        

            self.SideView1toMainDivider = DivideLine.Divider(master = self, root = self.root, orientation = 'vertical', relposy = View_Top_Line_Pos, height = self.MainViewCanvas.actualheight + DivideLine.Divider.buffer/2, relposx = 0.3)

            self.MainDividertoSideView2 = DivideLine.Divider(master = self, root = self.root, orientation = 'vertical', relposy = View_Top_Line_Pos, height = self.MainViewCanvas.actualheight + DivideLine.Divider.buffer/2, relposx = 0.6)

        
            self.SideView2toImageIndicator = DivideLine.Divider(master = self, root = self.root, orientation = 'vertical', relposy = View_Top_Line_Pos, height = self.MainViewCanvas.actualheight+ DivideLine.Divider.buffer/2, relposx = 0.9)

        
        self.TextBoxCanvas = CustomCanvas.CustomCanv(master = self, parent = self,root = self.root, color = 'black', relposx = 0, relposy = Text_Box_Top_Line_Pos, relwidth = 1, relheight = 1-Text_Box_Top_Line_Pos)


        #define dividers
        self.View_Top_Line = DivideLine.Divider(master = self,root = self.root, orientation = 'horizontal', relposy = View_Top_Line_Pos, 
                width = self.root.winfo_screenwidth())
        
        self.Text_Box_Top_Line = DivideLine.Divider(master = self, root = self.root, orientation = 'horizontal', relposy = Text_Box_Top_Line_Pos, 
                width = self.root.winfo_screenwidth())

        
  

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
        for index, df in enumerate(self.dfs):
            for key in self.display_strings[str(index)].keys():
                if key in self.matches:
                    if key not in keys_included:
                        keys_included.append(key)
        self.text_boxes = {}
        num_boxes = len(keys_included)
        for index, key in enumerate(keys_included):
            self.text_boxes[key] = DataTextBox.data_window(master = self, root = self.TextBoxCanvas.canvobject, relposx = index/num_boxes, relposy = 0, title = self.matches[str(key)],width  = 1/num_boxes)

        if self.multiple_images == True:
        #define_image_indicators()
            self.Image_Indicators = {}
            for index, name in enumerate(self.image_names):
                self.Image_Indicators[index] = ImageIndicator.image_indicator(master = self, root = self.ImageIndicatorCanvas, text = name, index= index)
            self.Image_Indicator = self.Image_Indicators[self.MainView.currentim.get()]

    def show_all(self):
        if self.multiple_images == True:
            #show image indicator canvas
            self.ImageIndicatorCanvas.canvobject.place_configure(height = len(self.MainView.arr) * 20)
            #show_image_indicators
            for name, object in self.Image_Indicators.items():
                object.show_self()

            #multiple views
            if self.num_views == 3:
            #show canvases, divide lines, and Views
                for index, obj in enumerate([self.MainViewCanvas, self.SideView1Canvas, self.SideView2Canvas, self.ImageIndicatorCanvas, self.TempImageIndicatorCanvas, self.TextBoxCanvas,
                                        self.View_Top_Line, self.Text_Box_Top_Line, self.SideView1toMainDivider, self.MainDividertoSideView2, self.SideView2toImageIndicator,
                                        self.MainView, self.SideView1, self.SideView2]):
                    obj.show_self()

            #only 1 view
            elif self.num_views == 1:
                for index, obj in enumerate([self.MainViewCanvas, self.ImageIndicatorCanvas, self.TempImageIndicatorCanvas, self.TextBoxCanvas,
                        self.View_Top_Line, self.Text_Box_Top_Line,
                        self.MainView, self.SideView2toImageIndicator]):
                    obj.show_self()
        elif self.multiple_images == False:
            #show canvases, divide lines, and Views
            for index, obj in enumerate([self.MainViewCanvas, self.TextBoxCanvas,
                                        self.View_Top_Line, self.Text_Box_Top_Line,
                                        self.MainView]):
                obj.show_self()
        #NOTE: display boxes will be displayed when Views are displayed
    def hide_all(self):
        print("Num Views: {}, MultiFrame: {}, multiple images: {}".format(self.num_views, self.multiframe, self.multiple_images))

        master_funcs.configure_buttons("ENABLED", [self.NewFile])
        master_funcs.configure_buttons("DISABLED", [self.Load_BiPlanar_View, self.Load_MonoPlanar_View, self.Anonymize, self.Custom_DF_Edit, self.View_Full_DF, self.Clear, self.Export_DICOM_file])        

        #GET RID OF MAIN VIEW CANVAS
        self.MainViewCanvas.hide_self()       
        #GET RID OF TEXT BOXES
        self.TextBoxCanvas.hide_self()
        #GET RID OF TOP AND BOTTOM DIVIDERS
        self.View_Top_Line.hide_self()
        self.Text_Box_Top_Line.hide_self()

        #MULTIPLE FRAMES - IMAGE INDICATORS
        if self.multiple_images == True:
            #hide image indicator canvas
            self.ImageIndicatorCanvas.canvobject.place_forget()
            self.TempImageIndicatorCanvas.canvobject.place_forget()   
            self.SideView2toImageIndicator.hide_self()                  

            #1 VIEW
        if self.num_views == 3:  
            self.SideView1Canvas.hide_self()
            self.SideView2Canvas.hide_self()
            self.SideView1toMainDivider.hide_self()
            self.MainDividertoSideView2.hide_self()
 

    def load(self, from_existing_df = False, force_num_views = False):
        self.load_file_cascade.load_file(from_existing_df= from_existing_df, force_num_views = force_num_views)
            
    def view_full_df(self):

        self.ViewFullDFCascade = ViewFullDF.ViewFullDF(master = self, title = "Full Data Frame")

    def view_private_elements(self):

        self.PrivateElementCascade = ViewPrivateElements.ViewPrivateElements(master = self, title = "Private Data Elements")        
        
    def custom_df_edit(self):
        #self.full_df_cascade.create_full_df_toplevel(view_or_edit = 'edit')
        self.EditAddDeleteCascade = EditAddDelete.EditAddDelete(master = self, title = "Edit Data Frame")

    def anonymize(self):
        AnonymizeDataBase.populate_anon()
        self.AnonymizeCascade = AnonymizeDF.AnonymizeDF(master = self, title = "Anonymize Data Frame")

    def decide_export(self):

        TopLevelWindow.just_one_or_many(master = self, root = self.root, message = "Export for",
                    proceed_command=self.export_dfs)
    def export_dfs(self, o_a):

        if o_a == "Just One":

                save_dest_no_name = filedialog.asksaveasfile(title = 'Select Output Destination', defaultextension=".dcm")
                
                if not save_dest_no_name is None:
                    save_dest = save_dest_no_name.name
                    #save_as_srt = str(save_dest.name)
                    self.dfs[int(self.MainView.currentim.get())].file_meta = self.dfs_metas[self.MainView.currentim.get()]

                    self.dfs[int(self.MainView.currentim.get())].save_as(save_dest) 


                    confirm_window = TopLevelWindow.top_window(master = self, root = self.root, width = 300, height = 200, title = "Success", color = 'grey')
                    success_text = tk.Label(confirm_window.toplevel, text = 'Successfully Saved as ' + str(save_dest),bg = 'grey', fg = 'white', wraplength = 200)
                    success_text.place(relx = 0.5, rely = 0.5, anchor = 'center')
        elif o_a == "All":
            save_dest_no_name = filedialog.asksaveasfile(title = 'Select Output Destination')

            #save_dest = filedialog.askdirectory(title = 'Select Export Destination')
            if not save_dest_no_name is None:
                #os.mkdir(save_dest_no_name.name)
                save_dest = save_dest_no_name.name
                os.remove(save_dest)
                os.mkdir(save_dest)
                # print(save_dest)
                for index, dataframe in enumerate(self.dfs):
                        new_save_str = os.path.join(save_dest,"edited_" + self.image_names[index])
                        dataframe.file_meta = self.dfs_metas[index]
                        dataframe.save_as(new_save_str)
            
                confirm_window = TopLevelWindow.top_window(master = self, root = self.root, width = 300, height = 200, title = "Success", color = 'grey')
                success_text = tk.Label(confirm_window.toplevel, text = 'Successfully Saved ' + str(len(self.dfs)) + ' files to ' + str(save_dest),bg = 'grey', fg = 'white', wraplength = 200)
                success_text.place(relx = 0.5, rely = 0.5, anchor = 'center')



if __name__ == "__main__":

    MyDICOMvisual = app()

    MyDICOMvisual.define_menus()


    MyDICOMvisual.welcome_window = TopLevelWindow.top_window(master = MyDICOMvisual, root = MyDICOMvisual.root, width = 500, height = 300, title = "Welcome!", color = 'grey')
    welcome = tk.Label(MyDICOMvisual.welcome_window.toplevel, text = "Welcome! Thank you for using MyDICOMvisual", bg = 'grey', fg = 'white', font = (MyDICOMvisual.fontstyle, '20'))
    instructions = tk.Label(MyDICOMvisual.welcome_window.toplevel, text = "Click below to get started", bg = 'grey', fg = 'white', font = (MyDICOMvisual.fontstyle, '10'))
    New_File_Welcome = CustomButton.Button(master= MyDICOMvisual, root= MyDICOMvisual.welcome_window.toplevel, relx = 0.5, rely = 0.6, width  = 100, height = 50,
                text = "Load File(s)",  command = MyDICOMvisual.load)
    welcome.place(relx = 0.5, rely = 0.2, anchor = 'center')
    instructions.place(relx = 0.5, rely = 0.4, anchor = 'center')

    MyDICOMvisual.root.mainloop()