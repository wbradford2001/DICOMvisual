import tkinter as tk

from matplotlib.pyplot import savefig

import TopLevelWindow


class text_box:
    list_of_boxes = []
    error_box_already_exists = False
    height = 20
    fontstyle = None
    def __init__(self, toplevel, fontstyle, index, dataelement, xpos, width, attrib):
        self.toplevel = toplevel
        self.attrib = attrib
        self.border_width = 1
        self.fontsize = 8
        text_box.fontstyle = fontstyle
        self.xpos = xpos
        self.index = index
        self.width = width 
        self.element_str = tk.StringVar()
        if self.attrib == "tag":
            self.element_str.set(dataelement.tag)
        elif self.attrib == "keyword":
            self.element_str.set(dataelement.keyword)
        elif self.attrib == "VR":
            self.element_str.set(dataelement.VR)
        elif self.attrib == "value":
            self.element_str.set(dataelement.value)
        else:
            self.element_str.set(self.attrib)
        self.orig_string = self.element_str.get()
        text_box.list_of_boxes.append(self)
        self.label = tk.Entry(
                    self.toplevel, 
                    font = (self.fontstyle, self.fontsize),
                    textvariable=self.element_str,
                    bg = 'black',
                    bd = self.border_width,
                    fg = 'white',
                    relief = 'flat',
                    justify='center',
                    selectborderwidth = 1,
                    highlightcolor='black',
                    highlightbackground= 'black',

                    )
        self.element_str.trace_add("write", self.error_message)
    def place_self(self):
        self.label.place(x = self.xpos, y = self.index * self.height, anchor='nw', width = self.width, height = text_box.height-1)
    def error_message(self, one, two, three):
        self.element_str.set(self.orig_string)
        global Error_Window
        if  text_box.error_box_already_exists == False:
            text_box.error_box_already_exists = True
            Error_Window = TopLevelWindow.top_window(root=rootcopy, width=400, height=200, title="ERROR", color = 'grey')
            error_message = tk.Label(Error_Window.toplevel, text = "Editing Data is only possible in 'Custom Edit' mode",
                                    bg = 'grey',
                                    fg = 'white')
            error_message.place(relx = 0.5, rely = 0.5, anchor  ='center')
            Error_Window.toplevel.protocol("WM_DELETE_WINDOW", on_closing)
def on_closing():
    text_box.error_box_already_exists = False
    Error_Window.toplevel.destroy()
def mouse_move(val):
    scroll.set(scroll.get() - val.delta)
    update_scroll(66)

def update_scroll(yo):
    val = scroll.get()
    num_boxes = 120
    canv.place_configure(
        y = (-canv_length+Full_DF_Wind.height)/(scroll_bar_to_) * int(val)
        )
    if int(val) != 0:
        if int(val) <= scroll_bar_to_ - num_boxes:
            for box in text_box.list_of_boxes[int(val)-1:int(val)-1+num_boxes]:
                box.place_self() 
        else:
            for box in text_box.list_of_boxes[int(val)-1:-2]:
                box.place_self() 
        if int(val) >= num_boxes:
            for box in text_box.list_of_boxes[int(val)-num_boxes:int(val)]:
                box.place_self() 
        else:
            for box in text_box.list_of_boxes[0:int(val)]:
                box.place_self() 
    else:
        for box in text_box.list_of_boxes[0:num_boxes]:
                box.place_self() 

    if int(val)> num_boxes:
        for box in text_box.list_of_boxes[0:int(val)-num_boxes]:
            box.label.place_forget() 
    if int(val)< scroll_bar_to_ - num_boxes:
        for box in text_box.list_of_boxes[int(val)+num_boxes: -1]:
            box.label.place_forget() 

   
def create_full_df_toplevel(root, imagename, df, fontstyle):
    global rootcopy
    rootcopy= root
    global dataframe
    dataframe = df

    #create window
    global image_name
    image_name = imagename
    title = "Full Data Frame: " + image_name
    window_width = 1200
    window_height = 500
    global Full_DF_Wind
    Full_DF_Wind = TopLevelWindow.top_window(root = root, width = window_width, height=window_height, title = title)
    Full_DF_Wind.toplevel.bind('<MouseWheel>', mouse_move)

    #create scrollbar
    global scroll
    scroll = tk.IntVar()
    scroll.set(0)
    scrollbar = tk.Scale(Full_DF_Wind.toplevel, orient = 'vertical', bg ='black', command = update_scroll, from_ = 0,variable = scroll)
    scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

    #create canvas
    global canv
    canv_width = Full_DF_Wind.width - 22
    canv = tk.Canvas(Full_DF_Wind.toplevel, bg = 'white', width = Full_DF_Wind.width - 22, height = Full_DF_Wind.height)
    canv.place(x = 0, y = 0, anchor = 'nw')

    #clear text box list
    text_box.list_of_boxes.clear()

    #populate entries
    for index, dataelement in enumerate(df):
        #tag
        newTB = text_box(toplevel = canv, fontstyle=fontstyle, index=index, dataelement=dataelement, xpos=0, width=canv_width/8, attrib = 'tag')

        #keyword
        newTB2 = text_box(toplevel = canv, fontstyle=fontstyle, index=index, dataelement=dataelement, xpos=canv_width/8+1, width=canv_width/8, attrib = 'keyword')
        
        #value
        if index != 209:
            newTB3 = text_box(toplevel = canv, fontstyle=fontstyle, index=index, dataelement=dataelement, xpos=2*canv_width/8+1, width=5*canv_width/8, attrib = 'value')
        else:
            newTB3 = text_box(toplevel = canv, 
                    fontstyle=fontstyle, index=index, 
                    dataelement=dataelement, xpos=2*canv_width/8+1, width=5*canv_width/8, 
                    attrib = ("{} x {} array of pixels").format(str(len(dataframe.pixel_array)),str(len(dataframe.pixel_array[0]))))

        #VR
        newTB4 = text_box(toplevel = canv, fontstyle=fontstyle, index=index, dataelement=dataelement, xpos=7*canv_width/8+2, width=canv_width/8+2, attrib = 'VR')
    

    #configure scroll bar to and from
    global scroll_bar_to_
    scroll_bar_to_ = len(text_box.list_of_boxes)
    scrollbar.config(to = scroll_bar_to_)
    scrollbar.config(from_ = 0)

    #configure canvas length
    global canv_length
    canv_length = text_box.height * len(df)
    canv.place_configure(height = canv_length)
    update_scroll(1)

