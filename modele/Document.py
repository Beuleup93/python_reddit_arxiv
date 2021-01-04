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
