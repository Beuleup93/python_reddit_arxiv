# -*- coding: utf-8 -*-
import sys
import time

import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from tkinter.messagebox import *

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

import interface_support as IS
from interface_support import *


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    IS.set_Tk_var()
    top = Interface (root)
    IS.init(root, top)
    root.mainloop()

w = None
def create_Interface(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Interface(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    interface_support.set_Tk_var()
    top = Interface (w)
    interface_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Interface():
    global w
    w.destroy()
    w = None

class Interface:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1360x768")
        top.title("Analyseur des Corpus")
        top.configure(background="#d9d9d9")
        top.configure(cursor="xterm")

        self.Titre = tk.Label(top)
        #self.Titre.place(relx=0.233, rely=0.089, height=40, width=390)
        self.Titre.pack()
        self.Titre.configure(background="#d9d9d9")
        self.Titre.configure(disabledforeground="#a3a3a3")
        self.Titre.configure(font="-family {8514oem} -size 18")
        self.Titre.configure(foreground="#000000")
        self.Titre.configure(text='''Analyseur des Corpus''')

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)
        
        #Fram champ de recherche
        self.zone_recherche = tk.LabelFrame(top)
        # self.zone_recherche.place(relx=0.223, rely=0.197, relheight=0.17
        #         , relwidth=0.507)
        self.zone_recherche.place(x=10, y=50, relheight=0.17
                 , width=300)
        self.zone_recherche.configure(relief='groove')
        self.zone_recherche.configure(foreground="black")
        self.zone_recherche.configure(text='''zône de recherche''')
        self.zone_recherche.configure(background="#d9d9d9")
        
        
        #Label mot clé
        self.Nom_auteur = tk.Label(self.zone_recherche)
        self.Nom_auteur.place(relx=0.018, rely=0.299, height=17.3, width=75.48
                , bordermode='ignore')
        self.Nom_auteur.configure(background="#d9d9d9")
        self.Nom_auteur.configure(disabledforeground="#a3a3a3")
        self.Nom_auteur.configure(foreground="#000000")
        self.Nom_auteur.configure(text='''Mot clé''')
        
        #champ de saisie pour le mot clé
        global nomAut
        nomAut=tk.StringVar()
        self.EntryNA = tk.Entry(self.zone_recherche, textvariable=nomAut)
        self.EntryNA.place(relx=0.331, rely=0.272, height=24, relwidth=0.504
                , bordermode='ignore')
        self.EntryNA.configure(background="white")
        self.EntryNA.configure(disabledforeground="#a3a3a3")
        self.EntryNA.configure(font="TkFixedFont")
        self.EntryNA.configure(foreground="#000000")
        self.EntryNA.configure(insertbackground="black")
        
        #Fram Paramétrage de la recherche
        self.parametre = tk.LabelFrame(top)
        # self.parametre.place(relx=0.112, rely=0.44, relheight=0.439
        #         , relwidth=0.764)
        self.parametre.place(x=10, y=200, relheight=0.439
                 , width=300)
        self.parametre.configure(relief='groove')
        self.parametre.configure(foreground="black")
        self.parametre.configure(text='''Paramétrage de la recherche''')
        self.parametre.configure(background="#d9d9d9")
        
        #Fram Résultat
        self.resultat = tk.LabelFrame(top)
        # self.parametre.place(relx=0.112, rely=0.44, relheight=0.439
        #         , relwidth=0.764)
        self.resultat.place(x=400, y=50, height=550
                 , width=900)
        self.resultat.configure(relief='groove')
        self.resultat.configure(foreground="black")
        self.resultat.configure(text='''Visualisation''')
        self.resultat.configure(background="#d9d9d9")
        

        
        #Label choix-corpus
        self.Affichage = tk.Label(self.parametre)
        self.Affichage.place(x=10, y=30 ,height=20.6, width=55.48
                , bordermode='ignore')
        self.Affichage.configure(background="#d9d9d9")
        self.Affichage.configure(disabledforeground="#a3a3a3")
        self.Affichage.configure(foreground="#000000")
        self.Affichage.configure(text='''Corpus''')
        
        #champ selectionné sur choix-corpus
        # On fait le filtre selon la table authors ou Publication
        self.TComboboxAff = ttk.Combobox(self.parametre)
        self.TComboboxAff.place(x=70, y=30, relheight=0.082
                , relwidth=0.284, bordermode='ignore')
        self.TComboboxAff.configure(textvariable=IS.comboAff)
        self.TComboboxAff.configure(takefocus="")
        self.TComboboxAff.configure(cursor="fleur")
        self.TComboboxAff.configure(values=["Reddit","Arxiv","Tous"])
        
        
        #Fram Filtrage temporelle
        self.temporelle = tk.LabelFrame(self.parametre)
        self.temporelle.place(relx=0.03, rely=0.20, relheight=0.400
                , width=250)
        self.temporelle.configure(relief='groove')
        self.temporelle.configure(foreground="black")
        self.temporelle.configure(text='''Filtrage temporelle''')
        self.temporelle.configure(background="#d9d9d9")

        
        #◘Label jour
        self.jour = tk.Label(self.temporelle)
        self.jour.place(relx=0.030, rely=0.30
                , bordermode='ignore')
        self.jour.configure(background="#d9d9d9")
        self.jour.configure(disabledforeground="#a3a3a3")
        self.jour.configure(foreground="#000000")
        self.jour.configure(text='''Jour''')
        
        #champ saisie jour
        self.entryJour = ttk.Combobox(self.temporelle)
        self.entryJour.place(relx=0.030, rely=0.60, relheight=0.200
                , relwidth=0.200, bordermode='ignore')
        self.entryJour.configure(textvariable="")
        self.entryJour.configure(takefocus="")
        #la liste jour contient les jours d'un mois
        days=[]
        for i in range(1,32):
            days.append(i)
        self.entryJour.configure(values=days)
        
        #◘Label Mois
        self.mois = tk.Label(self.temporelle)
        self.mois.place(relx=0.40, rely=0.30
                , bordermode='ignore')
        self.mois.configure(background="#d9d9d9")
        self.mois.configure(disabledforeground="#a3a3a3")
        self.mois.configure(foreground="#000000")
        self.mois.configure(text='''Mois''')
        
        #champ saisie Mois
        self.entryMois = ttk.Combobox(self.temporelle)
        self.entryMois.place(relx=0.30, rely=0.60, relheight=0.200
                , width=80, bordermode='ignore')
        self.entryMois.configure(textvariable="")
        self.entryMois.configure(takefocus="")
         # month contient les mois de l'année
        months=['Junary','February','March','April','May','June','July',
                'August','September','October','November','December']
        self.entryMois.configure(values=months)
        
        #◘Label Année
        self.annee = tk.Label(self.temporelle)
        self.annee.place(relx=0.70, rely=0.30
                , bordermode='ignore')
        self.annee.configure(background="#d9d9d9")
        self.annee.configure(disabledforeground="#a3a3a3")
        self.annee.configure(foreground="#000000")
        self.annee.configure(text='''Année''')
        
        #champ saisie Année
        self.entryAnnee = ttk.Combobox(self.temporelle)
        self.entryAnnee.place(relx=0.70, rely=0.60, relheight=0.200
                , relwidth=0.200, bordermode='ignore')
        self.entryAnnee.configure(textvariable=IS.annee)
        self.entryAnnee.configure(takefocus="")
        years=['2018','2019','2020','2021']
        self.entryAnnee.configure(values=years)

        #Label Fréquence
        self.frequence = tk.Label(self.parametre)
        self.frequence.place(relx=0.03, rely=0.70
                , bordermode='ignore')
        self.frequence.configure(background="#d9d9d9")
        self.frequence.configure(disabledforeground="#a3a3a3")
        self.frequence.configure(foreground="#000000")
        self.frequence.configure(text='''Fréquence''')
        
        ##boutton frequence
        self.CheckFr = tk.Checkbutton(self.parametre, variable ="", \
                 onvalue = 1, offvalue = 0, )
        self.CheckFr.place(relx=0.04, rely=0.80, bordermode='ignore')
        self.CheckFr.configure(background="#d9d9d9") 

        #Label Score
        self.score = tk.Label(self.parametre)
        self.score.place(relx=0.30, rely=0.70
                , bordermode='ignore')
        self.score.configure(background="#d9d9d9")
        self.score.configure(disabledforeground="#a3a3a3")
        self.score.configure(foreground="#000000")
        self.score.configure(text='''Score''')
        
        ##boutton Score
        self.CheckScore = tk.Checkbutton(self.parametre, variable ="", \
                 onvalue = 1, offvalue = 0, )
        self.CheckScore.place(relx=0.30, rely=0.80, bordermode='ignore')
        self.CheckScore.configure(background="#d9d9d9")            

        #ajouter les menus
        self.menubar = tk.Menu(top)
        self.menu1 = tk.Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Lemmatisation",command=alert)
        self.menu1.add_command(label="Stemming", command=self.plot)
        self.menu1.add_command(label="Stopwords", command=stopwords)
        self.menu1.add_command(label="Mots unique", command=motunique)
        self.menubar.add_cascade(label="Nettoyage & Normalisation", menu=self.menu1)
        top.config(menu=self.menubar)
        
        ### Frame cadre resultat
        #bouton recherche qui point vers la fonction getElement()
        self.ButtonRecherche = tk.Button(top, command=getElement)
        self.ButtonRecherche.place(x=10, y=550, height=28, width=76.13)
        self.ButtonRecherche.configure(activebackground="#ececec")
        self.ButtonRecherche.configure(activeforeground="#000000")
        self.ButtonRecherche.configure(background="#d9d9d9")
        self.ButtonRecherche.configure(disabledforeground="#a3a3a3")
        self.ButtonRecherche.configure(foreground="#000000")
        self.ButtonRecherche.configure(highlightbackground="#d9d9d9")
        self.ButtonRecherche.configure(highlightcolor="black")
        self.ButtonRecherche.configure(pady="0")
        self.ButtonRecherche.configure(text='''Recherche''')
        
        # graphe
    def plot (self):
            x=np.array ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
            v= np.array ([16,16.31925,17.6394,16.003,17.2861,17.3131,19.1259,18.9694,22.0003,22.81226])
            p= np.array ([16.23697,     17.31653,     17.22094,     17.68631,     17.73641 ,    18.6368,
                19.32125,     19.31756 ,    21.20247  ,   22.41444   ,  22.11718  ,   22.12453])
    
            fig = Figure(figsize=(6,6))
            a = fig.add_subplot(111)
            a.scatter(v,x,color='red')
            a.plot(p, range(2 +max(x)),color='blue')
            a.invert_yaxis()
    
            a.set_title ("Estimation Grid", fontsize=16)
            a.set_ylabel("Y", fontsize=14)
            a.set_xlabel("X", fontsize=14)
    
            canvas = FigureCanvasTkAgg(fig, master=self.resultat)
            canvas.get_tk_widget().pack()
            canvas.draw()
    
#fonction des recuperation des éléments


def getElement(*args):
    
   showinfo("Alerte", nomAut.get()) # message de teste 
   var1=IS.nomAut.get() # get the name of author
   var2=IS.nbrMinpub.get() # get number min of article
   var3=IS.keywords.get() # get the keys
   var4=IS.categorie.get() # name of categorie
   var5=IS.annee.get()
   var6=IS.nbAuthor.get()
   var7=IS.comboAff.get()
   var8 = IS.TcheckComp.get()
   
   var9 = IS.TcheckAut.get()
   var10 = IS.TcheckPub.get()
   var11 = IS.TcheckKey.get()
   var12 = IS.TcheckAnn.get()
   var13 = IS.limite.get()
   
def alert():
   showinfo("alerte", "Bravo!")

def stemming():
    pass

def stopwords():
    pass

def motunique():
    pass
if __name__ == '__main__':
    vp_start_gui()





