#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Document as document


class ArxivDocument(document.Document):
    
    def __init__(self, coauteurs, date,title, author, text, url):
        document.Document.__init__(self, date, title, author, text, url)
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
       s = document.Document.__str__(self)
       if self.get_num_coauteurs() > 0:
           return "[Source: "+self.getSource() +"] "+s + " [" + str(self.get_num_coauteurs()) + " co-auteurs]"
       else:
           return "[Source: "+self.getSource() +"] "+s
