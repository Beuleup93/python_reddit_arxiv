#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import Document as document

class RedditDocument(document.Document):
    
    def __init__(self,nombreComments,date,title, author, text, url):
        document.Document.__init__(self,date,title, author, text, url)
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
        return "[Source: "+self.getSource() +"] "+document.Document.__str__(self) + " [" + str(self.nombreComments) + " commentaires]"
