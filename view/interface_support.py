#! /usr/bin/env python
#  -*- coding: utf-8 -*-


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
    
    global keyword
    keyword=tk.StringVar()
    
    global jour
    jour=tk.StringVar()
    
    global mois
    mois=tk.StringVar()
    
    
    global annee
    annee =tk.StringVar() #variable annee
    
    global limite
    limite =tk.IntVar()
    limite.set(10)
    
    
    global comboAff
    comboAff=tk.StringVar()
    comboAff.set("Tous") #valeur par defdéfaut
    
    
    #les couleurs
    global colorAllCorpus
    global colorReddit
    global colorArxiv
    colorAllCorpus=["#FFA07A","#885533"]
    colorReddit=["#008000","#aa5588"]
    colorArxiv=["#79F8F8","#FE1B00"]
    
    global dic_date
    dic_date={"January":"01","February":"02","March":"03","April":"04","May":"05","June":"06",
                  "July":"07","August":"08","September":"09","October":"10","November":"11","December":"12"}
    
    
    
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




