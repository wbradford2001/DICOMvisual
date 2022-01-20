import tkinter as tk


def smart_place(master, parent, obj = None):
    if obj == None:
        obj = parent.obj
    print('\n')

 


    #relative placing, absolute dimensions
    try:
        obj.place(relx = parent.relx, rely = parent.rely, width = parent.width, height = parent.height, anchor = parent.anchor)        
    except AttributeError:
        pass
   



    #relative width, absolute height
    try:
        obj.place(relx = parent.relx, y = parent.y, relwidth = parent.relwidth, height = parent.height, anchor = parent.anchor)         
    except AttributeError:
        pass


    #absolute all
    try:
        obj.place(x = parent.x, y = parent.y, width = parent.width, height = parent.height, anchor = parent.anchor)         
    except AttributeError:
        pass
          



     
def smart_place_configure_to_active(master, parent):   



    #relative width, absolute height
    try:
        parent.obj.place_configure(relwidth = parent.relwidth * parent.size_reduce, height = parent.height * parent.size_reduce, anchor = parent.anchor)  
    except AttributeError:
        pass    

    #absolute dims
    try:
        parent.obj.place_configure(width = parent.width * parent.size_reduce, height = parent.height * parent.size_reduce, anchor = parent.anchor)  
    except AttributeError:
        pass           

def smart_place_configure_to_idle(master, parent):

    #relative width, absolute height
    try:
        parent.obj.place_configure(relwidth = parent.relwidth, height = parent.height, anchor = parent.anchor)  
    except AttributeError:
        pass     


    #absolute dims
    try:
        parent.obj.place_configure(width = parent.width, height = parent.height, anchor = parent.anchor)  
    except AttributeError:
        pass        

    
