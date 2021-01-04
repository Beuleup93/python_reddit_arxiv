#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Author():
    
    def __init__(self,name):
      self.name = name
      self.production = {}
      self.ndoc = 0

    def __str__(self):
       return "Auteur: " + self.name + ", Number of docs: "+ str(self.ndoc)

    def __repr__(self):
      return self.name
  
    def add(self, doc): 
       self.production[self.ndoc] = doc
       self.ndoc += 1 # Incrément le nombre de document

       