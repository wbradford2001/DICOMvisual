import tkinter as tk
import CustomThings.CustomEntry as CustomEntry
import pydicom
import CustomThings.TopLevelWindow as TopLevelWindow


class save_cascade:
    def __init__(self, master):
        self.error_flag = False
        self.master = master
    def save_from_boxes(self, input_full_df_cascade, image_indexes, box_list):
        self.input_full_df_cascade = input_full_df_cascade
        for index, box in enumerate(box_list):

                     
            if box.orig_string != box.entry_text.get():

                    for image_index in image_indexes:
                        if self.error_flag == False:
                            #check if its in DFS
                            if box.element.tag in self.master.dfs[image_index]:
                                self.master.dfs[image_index][box.element.tag].value = self.edit_match_type(box = box, editee = self.master.dfs[image_index][box.element.tag].value,
                                                        edit_to=box.entry_text.get())

                            #check if its in meta data
                            elif box.element.tag in self.master.dfs_metas[image_index]:
                                self.master.dfs_metas[image_index][box.element.tag].value = self.edit_match_type(box = box, editee = self.master.dfs_metas[image_index][box.element.tag].value,
                                                        edit_to=box.entry_text.get())     
            # elif self.input_full_df_cascade.view_or_edit == "anonymize":
            #     if box.pressed == True:
            #         for image_index in image_indexes:
            #             if self.error_flag == False:
            #                 #check if its in DFS
            #                 if box.value in self.master.dfs[image_index]:
            #                     self.master.dfs[image_index][box.value].value = self.edit_match_type(box = box, editee = self.master.dfs[image_index][box.value].value,
            #                                             edit_to=box.entry_text.get())

            #                 #check if its in meta data
            #                 elif box.value in self.master.dfs_metas[image_index]:
            #                     print(box.entry_text.get())
            #                     self.master.dfs_metas[image_index][box.value].value = self.edit_match_type(box = box, editee = self.master.dfs_metas[image_index][box.value].value,
            #                                             edit_to=box.entry_text.get())    
        return self.error_flag


    def edit_match_type(self, box, editee, edit_to):


        print("Editing {} of type {} to {}".format(editee, type(editee), edit_to))

        #base tag
        if isinstance(editee, pydicom.tag.BaseTag):
            
            try:
                editee = pydicom.tag.BaseTag(edit_to)
            except ValueError as e:
                print(e)
                self.show_error_message(box, editee, edit_to)
                

        #sequence
        elif isinstance(editee, pydicom.sequence.Sequence):
            try:

                editee = pydicom.sequence.Sequence(edit_to)
            except ValueError as e:
                self.show_error_message(box, editee, edit_to)        


        #float        
        elif isinstance(editee, float):
            try:
                editee = float(edit_to)
            except ValueError as e:
                self.show_error_message(box, editee, edit_to)   

        #multivalue            
        elif isinstance(editee, pydicom.multival.MultiValue):
            try:
                editee = pydicom.multival.MultiValue(edit_to)
            except ValueError as e:
                self.show_error_message(box, editee, edit_to)    

        #str               
        elif isinstance(editee, str):
            try:
                editee = str(edit_to)                                    
            except ValueError as e:
                self.show_error_message(box, editee, edit_to)  


        #int                 
        elif isinstance(editee, int):
            try:
                editee = int(edit_to)  
            except ValueError as e:
                self.show_error_message(box, editee, edit_to)    


        #DSfloat               
        elif isinstance(editee, pydicom.valuerep.DSfloat): 
            try:
                editee = pydicom.valuerep.DSfloat(edit_to)    
            except ValueError as e:
                self.show_error_message(box, editee, edit_to)      


        #bytes             
        elif isinstance(editee, bytes):
            try:
                editee = bytes(edit_to, 'utf-8')
            except ValueError as e:
                self.show_error_message(box, editee, edit_to)     


        #personname              
        elif isinstance(editee, pydicom.valuerep.PersonName):
            try:
                editee = pydicom.valuerep.PersonName(edit_to)  
            except ValueError as e:
                self.show_error_message(box, editee, edit_to)    


        #list               
        elif isinstance(editee, list):
            try:
                editee = list(edit_to)  
            except ValueError as e:
                self.show_error_message(box, editee, edit_to)     

        #IS              
        elif isinstance(editee, pydicom.valuerep.IS):
            try:
                editee = pydicom.valuerep.IS(edit_to)   
            except ValueError as e:
                self.show_error_message(box, editee, edit_to)  


        #UID    
            
        elif isinstance(editee, pydicom.uid.UID):
            try:
                editee = pydicom.uid.UID(edit_to)                                                
            except ValueError as e:
                self.show_error_message(box, editee, edit_to)     


        else:
            #editee = s(edit_to) 
            print("Unknown Data type: " + str(type(editee)))    

        
        
        return editee
    def show_error_message(self, box, editee, edit_to):
        self.error_flag = True

        message_text = "We are unable to edit " + str(box.element.tag) + ": " + box.element.keyword + ": '" + str(edit_to)  + "' to type " + str(type(editee))

        box.recolor_text('red')
        TopLevelWindow.show_error_window(master = self.master, root = self.input_full_df_cascade.Full_DF_Wind.toplevel, 
                        message = "Unable to Save Changes", width = 300, height = 100, ErrorString = message_text)
        if self.master.multiple_images == True:
            self.input_full_df_cascade.just_one_or_many_wind.toplevel.destroy()