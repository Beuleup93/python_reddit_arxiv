#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.6
#  in conjunction with Tcl version 8.6
#    Nov 08, 2020 01:36:25 AM CET  platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def set_Tk_var():
    global nomAut   #variable autheur
    nomAut=tk.StringVar()
    
        
    global categorie # variable catégorie
    categorie =tk.StringVar()
    
    
    global annee
    annee =tk.StringVar() #variable annee
    
    
    global nbAuthor
    nbAuthor =tk.IntVar() #Nombre de Co-auteur 
    
    global comboAff
    comboAff=tk.StringVar()
    
    
    global TcheckAut
    TcheckAut = tk.IntVar()
    
    
    global TcheckComp
    TcheckComp = tk.IntVar()
    
    global TcheckAnn
    TcheckAnn = tk.IntVar()
    
    global limite
    limite = tk.IntVar()
    
    
def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import interface
    interface.vp_start_gui()




