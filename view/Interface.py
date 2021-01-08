# -*- coding: utf-8 -*-
import sys

#########

import pandas
import nltk
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

import os
os.chdir('../controller')
from Corpus import Corpus

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
    fig=None
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
        self.Titre.configure(text='''Analyse Comparatif des Corpus''')

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)
        
        #Fram champ de recherche
        self.zone_recherche = tk.LabelFrame(top)
        # self.zone_recherche.place(relx=0.223, rely=0.197, relheight=0.17
        #         , relwidth=0.507)
        self.zone_recherche.place(x=10, y=50, relheight=0.13
                 , width=300)
        self.zone_recherche.configure(relief='groove')
        self.zone_recherche.configure(foreground="black")
        self.zone_recherche.configure(text='''recherche''')
        self.zone_recherche.configure(background="#d9d9d9")
        
        
        #Label mot clé
        self.Nom_auteur = tk.Label(self.zone_recherche)
        self.Nom_auteur.place(relx=0.018, rely=0.299, height=17.3, width=75.48
                , bordermode='ignore')
        self.Nom_auteur.configure(background="#d9d9d9",disabledforeground="#a3a3a3"
                                  ,foreground="#000000",text='''Mot clé''' )
        
        #champ de saisie pour le mot clé
        global keyword
        keyword=tk.StringVar()
        self.EntryNA = tk.Entry(self.zone_recherche, textvariable=keyword)
        self.EntryNA.place(relx=0.250, rely=0.272, height=24, width=130
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
        self.parametre.place(x=10, y=150, height=400
                 , width=300)
        self.parametre.configure(relief='groove')
        self.parametre.configure(foreground="black")
        self.parametre.configure(text='''Paramétrage de la recherche''')
        self.parametre.configure(background="#d9d9d9")
        
        #Fram Résultat
        self.resultat = tk.LabelFrame(top)
        # self.parametre.place(relx=0.112, rely=0.44, relheight=0.439
        #         , relwidth=0.764)
        self.resultat.place(x=320, y=50, height=550
                 , width=900)
        self.resultat.configure(relief='groove')
        self.resultat.configure(foreground="black")
        self.resultat.configure(text=' ')
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
        self.TComboboxAff = ttk.Combobox(self.parametre)
        self.TComboboxAff.place(x=70, y=30, height=24
                , width=80, bordermode='ignore')
        self.TComboboxAff.configure(textvariable=IS.comboAff)
        self.TComboboxAff.configure(validatecommand=alert)
        #self.TComboboxAff.configure(takefocus="")
        self.TComboboxAff.configure(cursor="fleur")
        self.TComboboxAff.configure(values=["Reddit","Arxiv","Tous"])
        
        
        #Fram Filtrage temporelle
        self.temporelle = tk.LabelFrame(self.parametre)
        self.temporelle.place(relx=0.03, rely=0.20, height=130
                , width=250)
        self.temporelle.configure(relief='groove')
        self.temporelle.configure(foreground="black")
        self.temporelle.configure(text='''Filtrage temporelle''')
        self.temporelle.configure(background="#d9d9d9")

        
        #◘Label jour
        self.jour = tk.Label(self.temporelle)
        self.jour.place(x=10, y=30
                , bordermode='ignore')
        self.jour.configure(background="#d9d9d9")
        self.jour.configure(disabledforeground="#a3a3a3")
        self.jour.configure(foreground="#000000")
        self.jour.configure(text='''Jour''')
        
        #champ saisie jour
        self.entryJour = ttk.Combobox(self.temporelle)
        self.entryJour.place(x=10, y=60, height=24
                , width=65, bordermode='ignore')
        self.entryJour.configure(textvariable=IS.jour)
        self.entryJour.configure(takefocus="")
        #la liste jour contient les jours d'un mois
        days=['01','02','03','04','05','06','07','08','09','10','11',
              '12','13','14','15','16','17','18','19','20','21','22','23',
              '24','25','26','27','28','30','31']
        self.entryJour.configure(values=days)
        
        #◘Label Mois
        self.mois = tk.Label(self.temporelle)
        self.mois.place(x=85, y=30
                , bordermode='ignore')
        self.mois.configure(background="#d9d9d9")
        self.mois.configure(disabledforeground="#a3a3a3")
        self.mois.configure(foreground="#000000")
        self.mois.configure(text='''Mois''')
        
        #champ saisie Mois
        self.entryMois = ttk.Combobox(self.temporelle)
        self.entryMois.place(x=85, y=60, height=24
                , width=80, bordermode='ignore')
        self.entryMois.configure(textvariable=IS.mois)
        self.entryMois.configure(takefocus="")
         # month contient les mois de l'année
        months=['January','February','March','April','May','June','July',
                'August','September','October','November','December']
        self.entryMois.configure(values=months)
        
        #◘Label Année
        self.annee = tk.Label(self.temporelle)
        self.annee.place(x=175, y=30
                , bordermode='ignore')
        self.annee.configure(background="#d9d9d9")
        self.annee.configure(disabledforeground="#a3a3a3")
        self.annee.configure(foreground="#000000")
        self.annee.configure(text='''Année''')
        
        #champ saisie Année
        self.entryAnnee = ttk.Combobox(self.temporelle)
        self.entryAnnee.place(x=175, y=60, height=24
                , width=65, bordermode='ignore')
        self.entryAnnee.configure(textvariable=IS.annee)
        self.entryAnnee.configure(takefocus="")
        years=['2018','2019','2020','2021']
        self.entryAnnee.configure(values=years)
        
        #Label champ limite
        self.labelLimite=tk.Label(self.temporelle, text="Top", background="#d9d9d9")
        self.labelLimite.place(x=85,y=80)
        
        #valeur limit
        self.valLimite=tk.Spinbox(self.temporelle, from_=1, to=10, width=5,textvariable=IS.limite)
        self.valLimite.place(x=120,y=80)
        
        
        # #Label Fréquence
        # self.frequence = tk.Label(self.parametre)
        # self.frequence.place(relx=0.03, rely=0.70
        #         , bordermode='ignore')
        # self.frequence.configure(background="#d9d9d9")
        # self.frequence.configure(disabledforeground="#a3a3a3")
        # self.frequence.configure(foreground="#000000")
        # self.frequence.configure(text='''Fréquence''')
        
        # ##case frequence
        # self.CheckFr = tk.Checkbutton(self.parametre, variable ="", \
        #          onvalue = 1, offvalue = 0, )
        # self.CheckFr.place(relx=0.04, rely=0.80, bordermode='ignore')
        # self.CheckFr.configure(background="#d9d9d9") 

        # #Label Score
        # self.score = tk.Label(self.parametre)
        # self.score.place(relx=0.30, rely=0.70
        #         , bordermode='ignore')
        # self.score.configure(background="#d9d9d9")
        # self.score.configure(disabledforeground="#a3a3a3")
        # self.score.configure(foreground="#000000")
        # self.score.configure(text='''Score''')
        
        # ##case Score
        # self.CheckScore = tk.Checkbutton(self.parametre, variable ="", \
        #          onvalue = 1, offvalue = 0, )
        # self.CheckScore.place(relx=0.30, rely=0.80, bordermode='ignore')
        # self.CheckScore.configure(background="#d9d9d9")            

        ############################################################
        ##################### Gestion des menus ####################
        
        #Nettoyage & Normalisation
        self.menubar = tk.Menu(top)
        self.menu1 = tk.Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Stopwords", command=self.stopwords)
        self.menu1.add_command(label="Lemmatisation",command=self.lemmatisation)
        self.menu1.add_command(label="Stemming", command=self.stemming)
        self.menubar.add_cascade(label="Nettoyage & Normalisation", menu=self.menu1)
        
        
        #action date
        self.menu2 = tk.Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="jour", command=self.day_management)
        self.menu2.add_command(label="mois",command=self.month_management)
        self.menu2.add_command(label="année", command=self.year_management)
        self.menu2.add_command(label="date complète", command=self.date_management)
        self.menubar.add_cascade(label="Time actions", menu=self.menu2)
        
        top.config(menu=self.menubar)
        
        ############ gestion des bouttons #####################
        
        # 1- boutton sur le mot clé
        
        self.Button1 = tk.Button(self.zone_recherche, text="recherche", command="")
        self.Button1.place(x=230,y=10, height=24)
        
        # 2- boutton choix corpus
        
        self.Button2 = tk.Button(self.parametre, text="recherche", command=self.action_corpus)
        self.Button2.place(x=230,y=12, height=24)
        
        
        #bouton recherche qui point vers la fonction getElement()
        self.ButtonRecherche = tk.Button(top, command="")
        self.ButtonRecherche.place(x=10, y=575, height=28, width=76.13)
        self.ButtonRecherche.configure(activebackground="#ececec")
        self.ButtonRecherche.configure(activeforeground="#000000")
        self.ButtonRecherche.configure(background="#d9d9d9")
        self.ButtonRecherche.configure(disabledforeground="#a3a3a3")
        self.ButtonRecherche.configure(foreground="#000000")
        self.ButtonRecherche.configure(highlightbackground="#d9d9d9")
        self.ButtonRecherche.configure(highlightcolor="black")
        self.ButtonRecherche.configure(pady="0")
        self.ButtonRecherche.configure(text='''Recherche''')

        #####instance corpus
        
        self.corpus_general,self.corpus_reddit,self.corpus_arxiv=Corpus("Corona").remplir_corpus()
######################################################################
##################### methode de classe ##############################    
    #reset le cadre resultat
    def clearFrame(self,frame):
        # destroy all widgets from frame
        for widget in frame.winfo_children():
           widget.destroy()
        
        # this will clear frame and frame will be empty
        # if you want to hide the empty panel then
        frame.pack_forget()
        
    def action_corpus(self):
        self.clearFrame(self.resultat)
        Interface.fig=None
        var=IS.comboAff.get()
        
        if var=="Tous":
            freq,stats,voc = self.corpus_general.freq_stats_corpus1(True)
            df = pandas.DataFrame.from_dict(stats, orient='index')
            df = df.sort_values(by = 'total', ascending = False)
            fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title='Top 200 publications Redit-Arxiv par nombre de mots').get_figure()
            canvas = FigureCanvasTkAgg(fig, master=self.resultat)
            canvas.get_tk_widget().pack()
            canvas.draw()
        elif var=="Reddit" :
            freq,stats,voc = self.corpus_reddit.freq_stats_corpus1(False)
            df = pandas.DataFrame.from_dict(stats, orient='index').head(20)
            df = df.sort_values(by = 'total', ascending = False)
            fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title='Top 20 publications Redit par nombre de mots').get_figure()
            canvas = FigureCanvasTkAgg(fig, master=self.resultat)
            canvas.get_tk_widget().pack()
            canvas.draw()
        else :
            freq,stats,voc = self.corpus_arxiv.freq_stats_corpus1(False)
            df = pandas.DataFrame.from_dict(stats, orient='index').head(20)
            df = df.sort_values(by = 'total', ascending = False)
            fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title='Top 20 publications Arxiv par nombre de mots').get_figure()
            canvas = FigureCanvasTkAgg(fig, master=self.resultat)
            canvas.get_tk_widget().pack()
            canvas.draw()
            
    #action stopwords
    def stopwords(self):
            self.clearFrame(self.resultat)
            var=IS.comboAff.get()
            if var=="Tous":
                freq,stats,voc = self.corpus_general.freq_stats_corpus2(True)
                df = pandas.DataFrame.from_dict(stats, orient='index')
                df = df.sort_values(by = 'total', ascending = False)
                fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title='Top 200 publications Redit-Arxiv apres suppression de stopwords').get_figure()
                
                canvas = FigureCanvasTkAgg(fig, master=self.resultat)
                canvas.get_tk_widget().pack()
                canvas.draw()
            elif var=="Reddit":
                print("bonjour")
                freq,stats,voc = self.corpus_reddit.freq_stats_corpus2(False)
                df = pandas.DataFrame.from_dict(stats, orient='index').head(20)
                df = df.sort_values(by = 'total', ascending = False)
                fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title='Top 20 publications Reddit apres suppression de stopwords').get_figure()
                
                canvas = FigureCanvasTkAgg(fig, master=self.resultat)
                canvas.get_tk_widget().pack()
                canvas.draw()
               
            else :
                freq,stats,voc = self.corpus_arxiv.freq_stats_corpus2(False)
                df = pandas.DataFrame.from_dict(stats, orient='index').head(20)
                df = df.sort_values(by = 'total', ascending = False)
                fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title='Top 20 publications Arxiv apres suppression de stopwords').get_figure()
                canvas = FigureCanvasTkAgg(fig, master=self.resultat)
                canvas.get_tk_widget().pack()
                canvas.draw()
            
    #action lemmatisation
    def lemmatisation(self):
            self.clearFrame(self.resultat)
            var=IS.comboAff.get()
            if var=="Tous" : 
                freq,stats,voc = self.corpus_general.freq_stats_corpus3(True)
                df = pandas.DataFrame.from_dict(stats, orient='index')
                df = df.sort_values(by = 'total', ascending = False)
                fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title='Top 200 publications Redit-Arxiv apres lemmatisation').get_figure()
                canvas = FigureCanvasTkAgg(fig, master=self.resultat)
                canvas.get_tk_widget().pack()
                canvas.draw()
            elif var=="Reddit":
                freq,stats,voc = self.corpus_reddit.freq_stats_corpus3(False)
                df = pandas.DataFrame.from_dict(stats, orient='index')
                df = df.sort_values(by = 'total', ascending = False).head(20)
                fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title='Top 20 publications Reddit apres lemmatisation').get_figure()
                canvas = FigureCanvasTkAgg(fig, master=self.resultat)
                canvas.get_tk_widget().pack()
                canvas.draw()
            else:
                freq,stats,voc = self.corpus_arxiv.freq_stats_corpus3(False)
                df = pandas.DataFrame.from_dict(stats, orient='index')
                df = df.sort_values(by = 'total', ascending = False).head(20)
                fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title='Top 20 publications Arxiv apres lemmatisation').get_figure()
                canvas = FigureCanvasTkAgg(fig, master=self.resultat)
                canvas.get_tk_widget().pack()
                canvas.draw()
            
    #action stemming
    def stemming(self):
            self.clearFrame(self.resultat)
            var=IS.comboAff.get()
            if var=="Tous":
                freq,stats,voc = self.corpus_general.freq_stats_corpus4(True)
                df = pandas.DataFrame.from_dict(stats, orient='index')
                df = df.sort_values(by = 'total', ascending = False)
                fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title='Top 200 publications Redit-Arxiv apres stemming').get_figure()
                
                canvas = FigureCanvasTkAgg(fig, master=self.resultat)
                canvas.get_tk_widget().pack()
                canvas.draw()
            elif var=="Reddit":
                freq,stats,voc = self.corpus_reddit.freq_stats_corpus4(False)
                df = pandas.DataFrame.from_dict(stats, orient='index').head(20)
                df = df.sort_values(by = 'total', ascending = False)
                fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title='Top 20 publications Reddit apres stemming').get_figure()
                
                canvas = FigureCanvasTkAgg(fig, master=self.resultat)
                canvas.get_tk_widget().pack()
                canvas.draw()
            else :
                freq,stats,voc = self.corpus_arxiv.freq_stats_corpus4(False)
                df = pandas.DataFrame.from_dict(stats, orient='index').head(20)
                df = df.sort_values(by = 'total', ascending = False)
                fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title='Top 20 publications Arxiv apres stemming').get_figure()
                
                canvas = FigureCanvasTkAgg(fig, master=self.resultat)
                canvas.get_tk_widget().pack()
                canvas.draw()
    #########################################
    #les action sur la date
    
    #sur l'année
    def year_management(self):
        self.clearFrame(self.resultat)
        var_year=IS.annee.get()
        var_limite=IS.limite.get()
        var_corpus=IS.comboAff.get()
        
        if var_corpus=="Tous":
           result=self.corpus_general.most_frequent_word_by_year(var_year, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) en "+var_year+" sur les deux Corpus"
        elif var_corpus=="Reddit":
           result=self.corpus_reddit.most_frequent_word_by_year(var_year, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) en "+var_year+" sur Reddit"
        else :
            result=self.corpus_arxiv.most_frequent_word_by_year(var_year, var_limite)
            titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) en "+var_year+" sur Arxiv"
        
        #print(result)
        if len(result) ==0:
            showinfo("alerte", "Pas de resultat!")
        else:
            mon_dic=dict((x,y) for x, y in result)
            #print(mon_dic)
            df = pandas.DataFrame.from_dict(mon_dic, orient='index')
            fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title=titre).get_figure()
            canvas = FigureCanvasTkAgg(fig, master=self.resultat)
            canvas.get_tk_widget().pack()
            canvas.draw()
    
    #sur le mois
    def month_management(self):
        self.clearFrame(self.resultat)
        var_month=IS.mois.get()
        var_limite=IS.limite.get()
        var_corpus=IS.comboAff.get()
        
        if var_corpus=="Tous":
           result=self.corpus_general.most_frequent_word_by_month(var_month, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) en "+var_month+" sur les deux Corpus"
        elif var_corpus=="Reddit":
           result=self.corpus_reddit.most_frequent_word_by_month(var_month, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) en "+var_month+" sur Reddit"
        else :
            result=self.corpus_arxiv.most_frequent_word_by_month(var_month, var_limite)
            titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) en "+var_month+" sur Arxiv"
        
        if len(result) ==0:
            showinfo("alerte", "Pas de resultat!")
        else:
            mon_dic=dict((x,y) for x, y in result)
            #print(mon_dic)
            df = pandas.DataFrame.from_dict(mon_dic, orient='index')
            fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title=titre).get_figure()
            canvas = FigureCanvasTkAgg(fig, master=self.resultat)
            canvas.get_tk_widget().pack()
            canvas.draw()
    #pour un jour donné
    def day_management(self):
        self.clearFrame(self.resultat)
        var_day=IS.jour.get()
        var_limite=IS.limite.get()
        var_corpus=IS.comboAff.get()
        
        if var_corpus=="Tous":
           result=self.corpus_general.most_frequent_word_by_day(var_day, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) le "+var_day+" de chaque mois sur les deux Corpus"
        elif var_corpus=="Reddit":
           result=self.corpus_reddit.most_frequent_word_by_day(var_day, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) le "+var_day+" de chaque mois sur Reddit"
        else :
            result=self.corpus_arxiv.most_frequent_word_by_day(var_day, var_limite)
            titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) le "+var_day+" de chaque mois sur Arxiv"
        
        if len(result) ==0:
            showinfo("alerte", "Pas de resultat!")
        else:
            mon_dic=dict((x,y) for x, y in result)
            #print(mon_dic)
            df = pandas.DataFrame.from_dict(mon_dic, orient='index')
            fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title=titre).get_figure()
            canvas = FigureCanvasTkAgg(fig, master=self.resultat)
            canvas.get_tk_widget().pack()
            canvas.draw()
    #pour une date donnée
    def date_management(self):
        self.clearFrame(self.resultat)
        var_day=IS.jour.get()
        var_m=IS.mois.get()
        var_year=IS.annee.get()
        dic_date={"January":"01","February":"02","March":"03","April":"04","May":"05","June":"06",
                  "July":"07","August":"08","September":"09","October":"10","November":"11","December":"12"}
        var_month=dic_date.get(var_m)
        var_date=var_year+"-"+var_month+"-"+var_day
        var_limite=IS.limite.get()
        var_corpus=IS.comboAff.get()
        
        if var_corpus=="Tous":
           result=self.corpus_general.most_frequent_word(var_date, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) le "+var_date+" sur les deux Corpus"
        elif var_corpus=="Reddit":
           result=self.corpus_reddit.most_frequent_word(var_date, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) le "+var_date+" sur Reddit"
        else :
            result=self.corpus_arxiv.most_frequent_word(var_date, var_limite)
            titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) le "+var_date+" sur Arxiv"
        
        if len(result) ==0:
            showinfo("alerte", "Pas de resultat!")
        else:
            mon_dic=dict((x,y) for x, y in result)
            #print(mon_dic)
            df = pandas.DataFrame.from_dict(mon_dic, orient='index')
            fig = df.plot(figsize=(20,10),kind='bar', color=["#FFA07A","#885533"], title=titre).get_figure()
            canvas = FigureCanvasTkAgg(fig, master=self.resultat)
            canvas.get_tk_widget().pack()
            canvas.draw()
   
def alert():
   showinfo("alerte", "Bravo!")

if __name__ == '__main__':
    vp_start_gui()





