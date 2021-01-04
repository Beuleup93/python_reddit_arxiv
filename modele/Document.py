#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import string
#from gensim.summarization.summarizer import summarize

class Document():
    
    # constructor
    def __init__(self, date, title, author, text, url):
        self.date = date
        self.title = title
        self.author = author
        self.text = text
        self.url = url
    
    # getters
    
    def get_author(self):
        return self.author

    def get_title(self):
        return self.title
    
    def get_date(self):
        return self.date
        
    def get_text(self):
        return self.text

    def get_url(self):
        return self.url

    def __str__(self):
        return "Title: " + self.title
    
    def __repr__(self):
        return self.title
    '''
    def sumup(self,ratio):
        try:
            auto_sum = summarize(self.text,ratio=ratio,split=True)
            out = " ".join(auto_sum)
        except:
            out =self.title            
        return out
    '''
    def nettoyer_texte(self,chaine):
       return chaine.lower().replace("\n", " ").strip(string.punctuation) 
    
    def getType(self):
        pass
  

class RedditDocument(Document):
    
    def __init__(self,nombreComments,date,title, author, text, url):
        Document.__init__(self,date,title, author, text, url)
        self.nombreComments = nombreComments
        self.source = "Reddit"
    
  
    def getNombreComments(self):
        return self.nombreComments
    
    def getSource(self):
        return "reddit"
  
    def setNombreComments(self,nombreComments):
        self.nombreComments = nombreComments
        
    def __str__(self):
        #return(super().__str__(self) + " [" + self.num_comments + " commentaires]")
        return "[Source: "+self.getSource() +"] "+Document.__str__(self) + " [" + str(self.nombreComments) + " commentaires]"

class ArxivDocument(Document):
    
    def __init__(self, coauteurs, date,title, author, text, url):
        #datet = dt.datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        Document.__init__(self, date, title, author, text, url)
        self.coauteurs = coauteurs
        self.source = "Arxiv"
    
    def get_num_coauteurs(self):
        if self.coauteurs is None:
            return(0)
        return(len(self.coauteurs) - 1)

    def get_coauteurs(self):
        if self.coauteurs is None:
            return([])
        return(self.coauteurs)
        
    def getSource(self):
        return "arxiv"

    def __str__(self):
       s = Document.__str__(self)
       if self.get_num_coauteurs() > 0:
           return "[Source: "+self.getSource() +"] "+s + " [" + str(self.get_num_coauteurs()) + " co-auteurs]"
       else:
           return "[Source: "+self.getSource() +"] "+s
