# -*- coding: utf-8 -*-
import sys

#########

import pandas
import nltk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter.messagebox import *
nltk.download('wordnet')

=======

from tkinter.messagebox import showinfo

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
        self.zone_recherche.place(x=10, y=50, relheight=0.13,width=300)
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
        self.EntryNA = tk.Entry(self.zone_recherche, textvariable=IS.keyword)
        self.EntryNA.place(relx=0.250, rely=0.272, height=24, width=130, bordermode='ignore')
        self.EntryNA.configure(background="white")
        self.EntryNA.configure(disabledforeground="#a3a3a3")
        self.EntryNA.configure(font="TkFixedFont")
        self.EntryNA.configure(foreground="#000000")
        self.EntryNA.configure(insertbackground="black")
        
        #Fram Paramétrage de la recherche
        self.parametre = tk.LabelFrame(top)
        self.parametre.place(x=10, y=150, height=400, width=300)
        self.parametre.configure(relief='groove')
        self.parametre.configure(foreground="black")
        self.parametre.configure(text='''Paramétrage de la recherche''')
        self.parametre.configure(background="#d9d9d9")
        
        #Fram Résultat
        self.resultat = tk.LabelFrame(top)
        self.resultat.place(x=320, y=50, height=550, width=900)
        self.resultat.configure(relief='groove')
        self.resultat.configure(foreground="black")
        self.resultat.configure(text=' ')
        self.resultat.configure(background="#d9d9d9")
        

        
        #Label choix-corpus
        self.Affichage = tk.Label(self.parametre)
        self.Affichage.place(x=10, y=30 ,height=20.6, width=55.48, bordermode='ignore')
        self.Affichage.configure(background="#d9d9d9")
        self.Affichage.configure(disabledforeground="#a3a3a3")
        self.Affichage.configure(foreground="#000000")
        self.Affichage.configure(text='''Corpus''')
        
        #champ selectionné sur choix-corpus
        self.TComboboxAff = ttk.Combobox(self.parametre)
        self.TComboboxAff.place(x=70, y=30, height=24, width=80, bordermode='ignore')
        self.TComboboxAff.configure(textvariable=IS.comboAff)
        self.TComboboxAff.configure(cursor="fleur")
        self.TComboboxAff.configure(values=["Reddit","Arxiv","Tous"])
        
        
        #Fram Filtrage temporelle
        self.temporelle = tk.LabelFrame(self.parametre)
        self.temporelle.place(relx=0.03, rely=0.20, height=130
                , width=250)
        self.temporelle.configure(relief='groove')
        self.temporelle.configure(foreground="black")
        self.temporelle.configure(text='''Filtrage temporel''')
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
        self.entryJour.place(x=10, y=60, height=24, width=65, bordermode='ignore')
        self.entryJour.configure(textvariable=IS.jour)
        self.entryJour.configure(takefocus="")
        days=['01','02','03','04','05','06','07','08','09','10','11',
              '12','13','14','15','16','17','18','19','20','21','22','23',
              '24','25','26','27','28','30','31']
        self.entryJour.configure(values=days)
        
        #◘Label Mois
        self.mois = tk.Label(self.temporelle)
        self.mois.place(x=85, y=30, bordermode='ignore')
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
        self.labelLimite=tk.Label(self.parametre, text="Top", background="#d9d9d9")
        self.labelLimite.place(x=85,y=230)
        
        #valeur limit
        self.valLimite=tk.Spinbox(self.parametre, from_=1, to=10, width=5,textvariable=IS.limite)
        self.valLimite.place(x=120,y=230)
        
        
        #Nettoyage & Normalisation
        self.menubar = tk.Menu(top)
        self.menu1 = tk.Menu(self.menubar, tearoff=0)
        self.menu1.add_command(label="Stopwords", command=self.stopwords)
        self.menu1.add_command(label="Lemmatisation",command=self.lemmatisation)
        self.menu1.add_command(label="Stemming", command=self.stemming)
        self.menu1.add_command(label="Search Words", command=self.relationImportance) 
        self.menubar.add_cascade(label="Corpus actions", menu=self.menu1)
        
        #action date
        self.menu2 = tk.Menu(self.menubar, tearoff=0)
        self.menu2.add_command(label="jour/mois", command=self.day_management)
        self.menu2.add_command(label="mois",command=self.month_management)
        self.menu2.add_command(label="année", command=self.year_management)
        self.menu2.add_command(label="date complète", command=self.date_management)
        self.menubar.add_cascade(label="Time actions", menu=self.menu2)
        
        top.config(menu=self.menubar)
        
        ############ gestion des bouttons #####################
        
        # 1- boutton sur le mot clé
        
        self.Button1 = tk.Button(self.zone_recherche, text="recherche", command=self.conconrdance)
        self.Button1.place(x=230,y=10, height=24)
        
        # 2- boutton choix corpus
        
        self.Button2 = tk.Button(self.parametre, text="recherche", command=self.action_corpus)
        self.Button2.place(x=230,y=12, height=24)
        
        
        #bouton de renitialisation 
        self.ButtonRecherche = tk.Button(top, command=self.renitialisation)
        self.ButtonRecherche.place(x=10, y=575, height=28, width=76.13)
        self.ButtonRecherche.configure(activebackground="#ececec")
        self.ButtonRecherche.configure(activeforeground="#000000")
        self.ButtonRecherche.configure(background="#d9d9d9")
        self.ButtonRecherche.configure(disabledforeground="#a3a3a3")
        self.ButtonRecherche.configure(foreground="#000000")
        self.ButtonRecherche.configure(highlightbackground="#d9d9d9")
        self.ButtonRecherche.configure(highlightcolor="black")
        self.ButtonRecherche.configure(pady="0")
        self.ButtonRecherche.configure(text='''Reset''')

        #####instance corpus
        
        self.corpus_general,self.corpus_reddit,self.corpus_arxiv=Corpus("Corona").remplir_corpus()
######################################################################
##################### methode de classe ##############################    
    #reset le cadre resultat
    def clearFrame(self,frame):
        # destroy all widgets from frame
        for widget in frame.winfo_children():
           widget.destroy()
        frame.pack_forget()
        
    #### fonction renitialisation
    def renitialisation(self):
        self.clearFrame(self.resultat)
        IS.jour.set("day")
        IS.mois.set("Month")
        IS.annee.set("Year")
        IS.limite.set(10)
        IS.comboAff.set("Tous")
        IS.keyword.set("")
        
        
    # action freq_stats sur l'ensemble de doonées 
    def freq_stats(self,stats,couleur,titre,limite):
        df = pandas.DataFrame.from_dict(stats, orient='index').head(limite)
        df = df.sort_values(by = 'total', ascending = False)
        fig = df.plot(figsize=(20,10),kind='bar', color=couleur, title=titre).get_figure()
        canvas = FigureCanvasTkAgg(fig, master=self.resultat)
        canvas.get_tk_widget().pack()
        canvas.draw()
        
    def action_corpus(self):
        self.clearFrame(self.resultat)
        var=IS.comboAff.get()
        limite=IS.limite.get()
        
        if var=="Tous":
            freq,stats,voc = self.corpus_general.freq_stats_corpus1(True)
            titre="Top "+str(limite)+" publication(s) Redit-Arxiv par nombre de mots"
            self.freq_stats(stats, IS.colorAllCorpus, titre, limite)
        elif var=="Reddit" :
            freq,stats,voc = self.corpus_reddit.freq_stats_corpus1(False)
            titre="Top "+str(limite)+" publication(s) Reddit par nombre de mots"
            self.freq_stats(stats, IS.colorReddit, titre, limite)
        else :
            freq,stats,voc = self.corpus_arxiv.freq_stats_corpus1(False)
            titre="Top "+str(limite)+" publication(s) Arxiv par nombre de mots"
            self.freq_stats(stats, IS.colorArxiv, titre, limite)
            
    #action stopwords
    def stopwords(self):
            self.clearFrame(self.resultat)
            var=IS.comboAff.get()
            limite=IS.limite.get()
            if var=="Tous":
                freq,stats,voc = self.corpus_general.freq_stats_corpus2(True)
                titre="Top "+str(limite)+" publication(s) Reddit-Arxiv apres suppression de stopwords"
                self.freq_stats(stats, IS.colorAllCorpus, titre, limite)
            elif var=="Reddit":
                freq,stats,voc = self.corpus_reddit.freq_stats_corpus2(False)
                titre="Top "+str(limite)+" publication(s) Reddit apres suppression de stopwords"
                self.freq_stats(stats, IS.colorReddit, titre, limite)
               
            else :
                freq,stats,voc = self.corpus_arxiv.freq_stats_corpus2(False)
                titre="Top "+str(limite)+" publication(s) Arxiv apres suppression de stopwords"
                self.freq_stats(stats, IS.colorArxiv, titre, limite)
            
    #action lemmatisation
    def lemmatisation(self):
            self.clearFrame(self.resultat)
            var=IS.comboAff.get()
            limite=IS.limite.get()
            if var=="Tous" : 
                freq,stats,voc = self.corpus_general.freq_stats_corpus3(True)
                titre="Top "+str(limite)+" publication(s) Reddit-Arxiv apres lemmatisation"
                self.freq_stats(stats, IS.colorAllCorpus, titre, limite)
            elif var=="Reddit":
                freq,stats,voc = self.corpus_reddit.freq_stats_corpus3(False)
                titre="Top "+str(limite)+" publication(s) Reddit apres lemmatisation"
                self.freq_stats(stats, IS.colorReddit, titre, limite)
            else:
                freq,stats,voc = self.corpus_arxiv.freq_stats_corpus3(False)
                titre="Top "+str(limite)+" publication(s) Arxiv apres lemmatisation"
                self.freq_stats(stats, IS.colorArxiv, titre, limite)
                
            
    #action stemming
    def stemming(self):
            self.clearFrame(self.resultat)
            var=IS.comboAff.get()
            limite=IS.limite.get()
            if var=="Tous":
                freq,stats,voc = self.corpus_general.freq_stats_corpus4(True)
                titre="Top "+str(limite)+" publication(s) Reddit-Arxiv apres stemming"
                self.freq_stats(stats, IS.colorAllCorpus, titre, limite)   
            elif var=="Reddit":
                freq,stats,voc = self.corpus_reddit.freq_stats_corpus4(False)
                titre="Top "+str(limite)+" publication(s) Reddit apres stemming"
                self.freq_stats(stats, IS.colorReddit, titre, limite)
            else :
                freq,stats,voc = self.corpus_arxiv.freq_stats_corpus4(False)
                titre="Top "+str(limite)+" publication(s) Arxiv apres stemming"
                self.freq_stats(stats, IS.colorArxiv, titre, limite)

    #########################################
    #les action sur la date
    
    #sur l'année
    def year_management(self):
        self.clearFrame(self.resultat)
        IS.mois.set("")
        IS.jour.set("")
        var_year=IS.annee.get()
        var_limite=IS.limite.get()
        var_corpus=IS.comboAff.get()
        
        if var_corpus=="Tous":
           result=self.corpus_general.most_frequent_word_by_year(var_year, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) en "+var_year+" sur les deux Corpus"
           couleur=IS.colorAllCorpus
        elif var_corpus=="Reddit":
           result=self.corpus_reddit.most_frequent_word_by_year(var_year, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) en "+var_year+" sur Reddit"
           couleur=IS.colorReddit
        else :
            result=self.corpus_arxiv.most_frequent_word_by_year(var_year, var_limite)
            titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) en "+var_year+" sur Arxiv"
            couleur=IS.colorArxiv
        
        if len(result) ==0:
            showinfo("alerte", "Pas de resultat!")
        else:
            mon_dic=dict((x,y) for x, y in result)
            # for key in mon_dic.keys():
            #     if key.isdigit():
            #         del mon_dic[key]
            df = pandas.DataFrame.from_dict(mon_dic, orient='index')
            fig = df.plot(figsize=(20,10),kind='bar', color=couleur, title=titre).get_figure()
            canvas = FigureCanvasTkAgg(fig, master=self.resultat)
            canvas.get_tk_widget().pack()
            canvas.draw()
    
    #sur le mois
    def month_management(self):
        self.clearFrame(self.resultat)
        IS.annee.set("")
        IS.jour.set("")
        var_month=IS.mois.get()
        var_limite=IS.limite.get()
        var_corpus=IS.comboAff.get()
        
        if var_corpus=="Tous":
           result=self.corpus_general.most_frequent_word_by_month(var_month, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) en "+var_month+" sur les deux Corpus"
           couleur=IS.colorAllCorpus
        elif var_corpus=="Reddit":
           result=self.corpus_reddit.most_frequent_word_by_month(var_month, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) en "+var_month+" sur Reddit"
           couleur=IS.colorReddit
        else :
            result=self.corpus_arxiv.most_frequent_word_by_month(var_month, var_limite)
            titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) en "+var_month+" sur Arxiv"
            couleur=IS.colorArxiv
        
        if len(result) ==0:
            showinfo("alerte", "Pas de resultat!")
        else:
            mon_dic=dict((x,y) for x, y in result)
            df = pandas.DataFrame.from_dict(mon_dic, orient='index')
            fig = df.plot(figsize=(20,10),kind='bar', color=couleur, title=titre).get_figure()
            canvas = FigureCanvasTkAgg(fig, master=self.resultat)
            canvas.get_tk_widget().pack()
            canvas.draw()
    #pour un jour donné
    def day_management(self):
        self.clearFrame(self.resultat)
        IS.annee.set("")
        IS.mois.set("")
        var_day=IS.jour.get()
        var_limite=IS.limite.get()
        var_corpus=IS.comboAff.get()
        
        if var_corpus=="Tous":
           result=self.corpus_general.most_frequent_word_by_day(var_day, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) le "+var_day+" de chaque mois sur les deux Corpus"
           couleur=IS.colorAllCorpus
        elif var_corpus=="Reddit":
           result=self.corpus_reddit.most_frequent_word_by_day(var_day, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) le "+var_day+" de chaque mois sur Reddit"
           couleur=IS.colorReddit
        else :
            result=self.corpus_arxiv.most_frequent_word_by_day(var_day, var_limite)
            titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) le "+var_day+" de chaque mois sur Arxiv"
            couleur=IS.colorArxiv
        
        if len(result) ==0:
            showinfo("alerte", "Pas de resultat!")
        else:
            mon_dic=dict((x,y) for x, y in result)
            df = pandas.DataFrame.from_dict(mon_dic, orient='index')
            fig = df.plot(figsize=(20,10),kind='bar', color=couleur, title=titre).get_figure()
            canvas = FigureCanvasTkAgg(fig, master=self.resultat)
            canvas.get_tk_widget().pack()
            canvas.draw()
    #pour une date donnée
    def date_management(self):
        self.clearFrame(self.resultat)
        var_day=IS.jour.get()
        var_m=IS.mois.get()
        var_year=IS.annee.get()
        var_month=IS.dic_date.get(var_m)
        var_date=var_year+"-"+var_month+"-"+var_day
        var_limite=IS.limite.get()
        var_corpus=IS.comboAff.get()
        
        if var_corpus=="Tous":
           result=self.corpus_general.most_frequent_word(var_date, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) le "+var_date+" sur les deux Corpus"
           couleur=IS.colorAllCorpus
        elif var_corpus=="Reddit":
           result=self.corpus_reddit.most_frequent_word(var_date, var_limite)
           titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) le "+var_date+" sur Reddit"
           couleur=IS.colorReddit
        else :
            result=self.corpus_arxiv.most_frequent_word(var_date, var_limite)
            titre=" Le(s) "+str(var_limite)+" mots le(s) plus fréquent(s) le "+var_date+" sur Arxiv"
            couleur=IS.colorArxiv
        
        if len(result) ==0:
            showinfo("alerte", "Pas de resultat!")
        else:
            mon_dic=dict((x,y) for x, y in result)
            df = pandas.DataFrame.from_dict(mon_dic, orient='index')
            fig = df.plot(figsize=(20,10),kind='bar', color=couleur, title=titre).get_figure()
            canvas = FigureCanvasTkAgg(fig, master=self.resultat)
            canvas.get_tk_widget().pack()
            canvas.draw()
            
    ##################################### word_cummun and specifique
    
    def relationImportance(self):
        self.clearFrame(self.resultat)
        wordCommun,specificReddit,specifArxiv=self.corpus_general.wordcommun_and_wordspecific()
        var_corpus=IS.comboAff.get()
        
        if var_corpus=='Tous' :
            df=sorted(list(wordCommun))
            message="Mots communs pour les deux corpus"
        elif var_corpus =='Reddit':
            df=sorted(list(specificReddit))
            message='Mots spécifiques pour Reddit'
        else :
            df=sorted(list(specifArxiv))
            message='Mots spécifiques pour Arxiv'
        
        
        titre=tk.Label(self.resultat, text=message, background="#d9d9d9",font="-family {8514oem} -size 14")
        titre.pack()
        
        scrollbar = tk.Scrollbar(self.resultat)
        scrollbar.pack(side="right", fill="y")
        
        listbox = tk.Listbox(self.resultat, yscrollcommand=scrollbar.set)
        for i in df:
            listbox.insert("end", i)
        listbox.pack(side="left", fill="both")
        scrollbar.config(command=listbox.yview)
        
    #### recherche de la conconrdance
    
    def conconrdance(self):
        self.clearFrame(self.resultat)
        result=self.corpus_general.concorde(IS.keyword.get()).head(100)
        if len(result)==0:
            showinfo("alerte", "Pas de resultat!")
        else :
            vargauche=result['gauche'].values.tolist()
            vardroite=result['droite'].values.tolist()
            motif=result['motif'].values.tolist()
            
            titre=tk.Label(self.resultat, text="concordance du mot "+IS.keyword.get(), background="#d9d9d9",
                           font="-family {8514oem} -size 14")
            titre.pack()
            
            self.scrollbar = tk.Scrollbar(self.resultat,command=self.scrollBoth)
            self.scrollbar.pack(side="right", fill="y")
            
            self.listbox1 = tk.Listbox(self.resultat, yscrollcommand=self.scrollbar.set)
            for i in vargauche:
                self.listbox1.insert("end", i)
            self.listbox1.pack(side="left", fill="both")
            
            
            self.listbox2 = tk.Listbox(self.resultat, yscrollcommand=self.scrollbar.set)
            for i in motif:
                self.listbox2.insert("end", i)
            self.listbox2.pack(side="left", fill="both")
            
            self.listbox3 = tk.Listbox(self.resultat, yscrollcommand=self.scrollbar.set)
            for i in vardroite:
                self.listbox3.insert("end", i)
            self.listbox3.pack(side="left", fill="both")
            
    def scrollBoth(self,*args):
        self.listbox1.yview(*args)
        self.listbox2.yview(*args)
        self.listbox3.yview(*args)
        self.scrollbar.set(*args)
        
        

if __name__ == '__main__':
    vp_start_gui()





