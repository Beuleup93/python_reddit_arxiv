#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################## Classe Corpus ##################################

import datetime as dt

import pickle
import re
from collections import defaultdict
import praw
import urllib.request
import xmltodict   
import datetime as dt
import pandas
import string
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from collections import Counter
#from nltk.book import *
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
#Import Class
import os
os.chdir('../modele')
from Author import Author
from RedditDocument import RedditDocument
from ArxivDocument import ArxivDocument
from Document import Document



class Corpus():
    def __init__(self,name):
        self.name = name
        self.collection = {}
        self.authors = {}
        self.id2doc = {}
        self.id2aut = {}
        self.ndoc = 0
        self.naut = 0
        self.chaineRegex = []
        self.vocabulaires = list()
            
    def add_doc(self, doc):
        self.collection[self.ndoc] = doc
        self.id2doc[self.ndoc] = doc.get_title()
        self.ndoc += 1
        aut_name = doc.get_author()
        aut = self.get_aut2id(aut_name)
        if aut is not None:
            self.authors[aut].add(doc)
        else:
            self.add_aut(aut_name,doc)
            
    def add_aut(self, aut_name,doc):
        aut_temp = Author(aut_name)
        aut_temp.add(doc)
        self.authors[self.naut] = aut_temp
        self.id2aut[self.naut] = aut_name
        self.naut += 1

    def get_aut2id(self, author_name):
        aut2id = {v: k for k, v in self.id2aut.items()}
        heidi = aut2id.get(author_name)
        return heidi

    def get_doc(self, i):
        return self.collection[i]
    
    def get_coll(self):
        return self.collection

    def __str__(self):
        return "Corpus: " + self.name + ", Number of docs: "+ str(self.ndoc)+ ", Number of authors: "+ str(self.naut)
    
    def __repr__(self):
        return self.name

    def sort_title(self,nreturn=None):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_title())][:(nreturn)]

    def sort_date(self,nreturn):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_date(), reverse=True)][:(nreturn)]
    
    def save(self,file):
            pickle.dump(self, open(file, "wb" ))
            
    def search(self, motif):
        if len(self.chaineRegex) == 0:
            self.chaineRegex = list(self.collection) 
        chaine = ', '.join([str(doc) for doc in self.chaineRegex ])
        return re.search(r"motif*", chaine)

    def vocabulaire(self):
        self.vocabulaires = list()
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        for ndoc, document in self.collection.items():
            chaine = document.get_text().lower()
            tokensList = tokenizer.tokenize(chaine)
            self.vocabulaires += tokensList
        return (self.vocabulaires, set(self.vocabulaires))
    
    def vocabulaire_by_source(self,source):
        self.vocabulaires = list()
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        for ndoc, doc in self.collection.items():
            if source == 'reddit' and isinstance(doc,RedditDocument):
                chaine = doc.get_text().lower()
                tokensList = tokenizer.tokenize(chaine)
                self.vocabulaires += tokensList
            elif source == 'arxiv' and isinstance(doc,ArxivDocument): 
                chaine = doc.get_text().lower()
                tokensList = tokenizer.tokenize(chaine)
                self.vocabulaires += tokensList
        return (self.vocabulaires, set(self.vocabulaires))

    def vocabulaire_by_date(self, date=None):
        self.vocabulaires = list()
        if date != None :
            y,m,d = [int(x) for x in date.split('-')] 
            date_choosed = dt.date(y,m,d)
            tokenizer = nltk.RegexpTokenizer(r'\w+')
            for k,v in self.collection.items():
                date_document = v.get_date()
                if date_document.date() == date_choosed:
                    chaine = v.get_text().lower()
                    tokensList = tokenizer.tokenize(chaine)
                    self.vocabulaires += tokensList
        return (self.vocabulaires, set(self.vocabulaires))
    
    def vocabulaire_by_month(self, month=None):
        self.vocabulaires = list()
        if month != None :
            tokenizer = nltk.RegexpTokenizer(r'\w+')
            for k,v in self.collection.items():
                date_document = v.get_date()
                if date_document.strftime('%B') == month:
                    chaine = v.get_text().lower()
                    tokensList = tokenizer.tokenize(chaine)
                    self.vocabulaires += tokensList
        return (self.vocabulaires, set(self.vocabulaires))

    def vocabulaire_by_jour(self, jour=None):
        self.vocabulaires = list()
        if jour != None :
            tokenizer = nltk.RegexpTokenizer(r'\w+')
            for k,v in self.collection.items():
                date_document = v.get_date()
                if date_document.strftime('%d') == jour:
                    chaine = v.get_text().lower()
                    tokensList = tokenizer.tokenize(chaine)
                    self.vocabulaires += tokensList
        return(self.vocabulaires, set(self.vocabulaires))

    # Sans prétraitement
    def freq_stats_corpus1(self, bySource = False):
      tokenizer = nltk.RegexpTokenizer(r'\w+')
      freq_stats = defaultdict(list) 
      if bySource:
        for k,doc_source in self.collection.items():
          if isinstance(doc_source, RedditDocument):
            freq_stats['Reddit'] += tokenizer.tokenize(doc_source.get_text().lower())
          else:
            freq_stats['Arxiv'] += tokenizer.tokenize(doc_source.get_text().lower())
      else:
        for k,doc in self.collection.items():
          current_author = doc.get_author()
          for num_doc, doc_author in self.collection.items():
            if doc_author.get_author()==current_author:
              freq_stats[current_author] += tokenizer.tokenize(doc_author.get_text().lower())
      stats, freq = dict(), dict() 
      for author, word in freq_stats.items():
        freq[author] = fq = nltk.FreqDist(word)
        stats[author] = {'total': len(word), 'unique': len(fq.keys())} 
      return (freq, stats, freq_stats)

    # Suppression des stops word
    def freq_stats_corpus2(self, bySource = False):
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        freq_stats = defaultdict(list) 
        stop_words = set(nltk.corpus.stopwords.words('english'))
        if bySource:
            for k,doc_source in self.collection.items():
                tokens = tokenizer.tokenize(doc_source.get_text().lower())
                if isinstance(doc_source, RedditDocument):
                    freq_stats['Reddit'] += [word for word in tokens if not word in stop_words]
                else:
                    freq_stats['Arxiv'] += [word for word in tokens if not word in stop_words]
        else:
            for k,doc in self.collection.items():
                current_author = doc.get_author()
                for num_doc, doc_author in self.collection.items():
                    tokens = tokenizer.tokenize(doc_author.get_text().lower())
                if doc_author.get_author()==current_author:
                    freq_stats[current_author] += [word for word in tokens if not word in stop_words]
        stats, freq = dict(), dict() 
        for key, word in freq_stats.items():
            freq[key] = fq = nltk.FreqDist(word)
            stats[key] = {'total': len(word), 'unique': len(fq.keys())} 
        return (freq, stats, freq_stats)
    
    # Freq et stats aprés suppression des stop word et lemmatisation
    def freq_stats_corpus3(self, bySource = False):
      wordnet_lemmatizer = WordNetLemmatizer()
      tokenizer = nltk.RegexpTokenizer(r'\w+')
      freq_stats = defaultdict(list) 
      stop_words = set(nltk.corpus.stopwords.words('english'))
      if bySource:
        for k,doc_source in self.collection.items():
          tokens = tokenizer.tokenize(doc_source.get_text().lower())
          if isinstance(doc_source, RedditDocument):
            freq_stats['Reddit'] += [wordnet_lemmatizer.lemmatize(word, pos="v") for word in tokens if not word in stop_words]
          else:
            freq_stats['Arxiv'] += [wordnet_lemmatizer.lemmatize(word, pos="v") for word in tokens if not word in stop_words]
      else:
        for k,doc in self.collection.items():
          current_author = doc.get_author()
          for num_doc, doc_author in self.collection.items():
            tokens = tokenizer.tokenize(doc_author.get_text().lower())
            if doc_author.get_author()==current_author:
              freq_stats[current_author] += [wordnet_lemmatizer.lemmatize(word, pos="v") for word in tokens if not word in stop_words]
      stats, freq = dict(), dict() 
      for key, word in freq_stats.items():
        freq[key] = fq = nltk.FreqDist(word)
        stats[key] = {'total': len(word), 'unique': len(fq.keys())} 
      return (freq, stats, freq_stats)
    
    # Freq et stats aprés stemming 
    def freq_stats_corpus4(self, bySource = False):
      porter=PorterStemmer()
      tokenizer = nltk.RegexpTokenizer(r'\w+')
      freq_stats = defaultdict(list) 
      stop_words = set(nltk.corpus.stopwords.words('english'))
      if bySource:
        for k,doc_source in self.collection.items():
          tokens = tokenizer.tokenize(doc_source.get_text().lower())
          if isinstance(doc_source, RedditDocument):
            freq_stats['Reddit'] += [porter.stem(word) for word in tokens if not word in stop_words]
          else:
            freq_stats['Arxiv'] += [porter.stem(word) for word in tokens if not word in stop_words]
      else:
        for k,doc in self.collection.items():
          current_author = doc.get_author()
          for num_doc, doc_author in self.collection.items():
            tokens = tokenizer.tokenize(doc_author.get_text().lower())
            if doc_author.get_author()==current_author:
              freq_stats[current_author] += [porter.stem(word) for word in tokens if not word in stop_words]
      stats, freq = dict(), dict() 
      for key, word in freq_stats.items():
        freq[key] = fq = nltk.FreqDist(word)
        stats[key] = {'total': len(word), 'unique': len(fq.keys())} 
      return (freq, stats, freq_stats)

      # Matrice document mots
    def tfidf(self):
        wordnet_lemmatizer = WordNetLemmatizer()
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        sources_docs = defaultdict(list) 
        stop_words = set(nltk.corpus.stopwords.words('english'))
        for k,doc_source in self.collection.items():
            tokens = tokenizer.tokenize(doc_source.get_text().lower())
            chaine = ' '.join([wordnet_lemmatizer.lemmatize(word, pos="v") for word in tokens if not word in stop_words])
            if isinstance(doc_source, RedditDocument):
                sources_docs['Reddit'] += [chaine]
            else:
                sources_docs['Arxiv'] += [chaine]
        vectorizer = TfidfVectorizer()
        X_redddit = vectorizer.fit_transform(sources_docs['Reddit'])
        X_arxiv = vectorizer.fit_transform(sources_docs['Arxiv'])
        return (X_redddit,X_arxiv)

    # Delete Stop word and lemmatiser
    def create_and_normalize_corpus1(self):
        wordnet_lemmatizer = WordNetLemmatizer()
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        sources_docs = defaultdict(list) 
        stop_words = set(nltk.corpus.stopwords.words('english'))
        for k,doc_source in self.collection.items():
            tokens = tokenizer.tokenize(doc_source.get_text().lower())
            if isinstance(doc_source, RedditDocument):
                sources_docs['Reddit'] += [wordnet_lemmatizer.lemmatize(word, pos="v") for word in tokens if not word in stop_words]
            else:
                sources_docs['Arxiv'] += [wordnet_lemmatizer.lemmatize(word, pos="v") for word in tokens if not word in stop_words]
        corpus_reddit = ' '.join(sources_docs['Reddit'])
        corpus_arxiv = ' '.join(sources_docs['Arxiv'])
        return (corpus_reddit,corpus_arxiv)

    # Delete Stop word and Stemming
    def create_and_normalize_corpus2(self):
        porter=PorterStemmer()
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        sources_docs = defaultdict(list) 
        stop_words = set(nltk.corpus.stopwords.words('english'))
        for k,doc_source in self.collection.items():
            tokens = tokenizer.tokenize(doc_source.get_text().lower())
        if isinstance(doc_source, RedditDocument):
            sources_docs['Reddit'] += [porter.stem(word) for word in tokens if not word in stop_words]
        else:
          sources_docs['Arxiv'] += [porter.stem(word) for word in tokens if not word in stop_words]
        corpus_reddit = ' '.join(sources_docs['Reddit'])
        corpus_arxiv = ' '.join(sources_docs['Arxiv'])
        return (corpus_reddit,corpus_arxiv)
        
    def find_documents_authors(self):
        author_documents = defaultdict(list)
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        for nauth,author in self.authors.items():
            for ndoc,doc in author.get_production().items():
                author_documents[author] += tokenizer.tokenize(doc.get_text().lower())
        return author_documents
    
    #chargement
    def remplir_corpus(self):
        obj_reddit=Corpus("corona")
        obj_arxiv=Corpus("corona")
        obj_general=Corpus("corona")
    ######### Source Reddit #########
        reddit = praw.Reddit(client_id='2R8dyFhAMrONHA', client_secret='HKBF3vfSYP6YOAPS4hgXf68OOJ4', user_agent='Reddit WebScraping')
        hot_posts = reddit.subreddit('Coronavirus').hot(limit=100)
    
        for post in hot_posts:
            # Get comments of post i
            try:
              submission = reddit.submission(url=post.url);
              nbComments = len(submission.comments)
            except:
              pass
            datet = dt.datetime.fromtimestamp(post.created)
            txt = post.title + ". "+ post.selftext
            txt = txt.replace('\n', ' ')
            txt = txt.replace('\r', ' ')
            doc = RedditDocument(nbComments,
                                 datet,
                                 post.title,
                                 post.author_fullname,
                                 txt,
                                 post.url)
            obj_general.add_doc(doc)
            obj_reddit.add_doc(doc)
            
    
        ######### Source Arxiv #########
        url = 'http://export.arxiv.org/api/query?search_query=all:covid&start=0&max_results=100'
        data =  urllib.request.urlopen(url).read().decode()
        docs = xmltodict.parse(data)['feed']['entry'] # Liste de dictionnaire
        
        for i in docs:
            datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
            try:
                author = [aut['name'] for aut in i['author']][0]
            except:
                author = i['author']['name']
            txt = i['title']+ ". " + i['summary']
            txt = txt.replace('\n', ' ')
            txt = txt.replace('\r', ' ')
            doc = ArxivDocument(i['author'],
                           datet,
                           i['title'],
                           author,
                           txt,
                           i['id']
                           )
            obj_general.add_doc(doc)
            obj_arxiv.add_doc(doc)
            
        return (obj_general, obj_reddit, obj_arxiv)
    
    
     # format date: '2021-01-02'
    def most_frequent_word(self, date, nb_word):
      self.vocabulaires = list()
      y,m,d = [int(x) for x in date.split('-')] 
      date_choosed = dt.date(y,m,d)
      tokenizer = nltk.RegexpTokenizer(r'\w+')
      for k,v in self.collection.items():
        date_document = v.get_date()
        if date_document.date() == date_choosed:
          chaine = v.get_text().lower()
          tokensList = tokenizer.tokenize(chaine)
          self.vocabulaires += tokensList
        #Comptons les occurence de mots dans le la liste vocabulaires
      self.vocabulaires = self.normalization(self.vocabulaires)
      occurences = Counter(self.vocabulaires)
      return occurences.most_common(nb_word)

    # format: '2021'
    def most_frequent_word_by_year(self, year, nb_word):
      self.vocabulaires = list()
      tokenizer = nltk.RegexpTokenizer(r'\w+')
      for k,v in self.collection.items():
        date_document = v.get_date()
        if date_document.strftime('%Y') == year:
          chaine = v.get_text().lower()
          tokensList = tokenizer.tokenize(chaine)
          self.vocabulaires += tokensList
        #Comptons les occurence de mots dans le la liste vocabulaires
      self.vocabulaires = self.normalization(self.vocabulaires)
      occurences = Counter(self.vocabulaires)
      return occurences.most_common(nb_word)
    
    # format: 'December'
    def most_frequent_word_by_month(self, month, nb_word):
      self.vocabulaires = list()
      tokenizer = nltk.RegexpTokenizer(r'\w+')
      for k,v in self.collection.items():
        date_document = v.get_date()
        if date_document.strftime('%B') == month:
          chaine = v.get_text().lower()
          tokensList = tokenizer.tokenize(chaine)
          self.vocabulaires += tokensList
        #Comptons les occurence de mots dans le la liste vocabulaires
      self.vocabulaires = self.normalization(self.vocabulaires)
      occurences = Counter(self.vocabulaires)
      return occurences.most_common(nb_word)

    # format: '01'
    def most_frequent_word_by_day(self, jour,nb_word):
      self.vocabulaires = list()
      tokenizer = nltk.RegexpTokenizer(r'\w+')
      for k,v in self.collection.items():
          date_document = v.get_date()
          if date_document.strftime('%d') == jour:
            chaine = v.get_text().lower()
            tokensList = tokenizer.tokenize(chaine)
            self.vocabulaires += tokensList
        #Comptons les occurence de mots dans le la liste vocabulaires
      self.vocabulaires = self.normalization(self.vocabulaires)
      occurences = Counter(self.vocabulaires)
      return occurences.most_common(nb_word)
        

    def normalization(self, liste):
        liste_normaliser = []
        wordnet_lemmatizer = WordNetLemmatizer()
        stop_words = set(nltk.corpus.stopwords.words('english'))
        for word in liste:
            if word not in stop_words:
                liste_normaliser.append(wordnet_lemmatizer.lemmatize(word, pos="v"))
        return liste_normaliser
    
    ###### Mot commun et spécifique 
    def wordcommun_and_wordspecific(self):
      # recuperation des deux source nettoyer et normaliser
      all_source = self.find_documents_source()
      # source reddit et source arxiv
      source_reddit, source_arxiv = all_source['reddit'],all_source['arxiv']
      #comprehension
      word_communs = [wc for wc in source_reddit if wc in source_arxiv]
      word_specific_reddit = [word for word in source_reddit if not word in word_communs]
      word_specific_arxiv = [word for word in source_arxiv if not word in word_communs]
      return (set(word_communs),set(word_specific_reddit),set(word_specific_arxiv))

    def find_documents_source(self):
      documents_source = defaultdict(list)
      for ndoc, doc in self.collection.items():
        if isinstance(doc,RedditDocument):
          documents_source['reddit'] += self.nettoyer_corpus(doc.get_text())
        else:
           documents_source['arxiv'] += self.nettoyer_corpus(doc.get_text())
      return documents_source
  
    
    def nettoyer_corpus(self,text_corpus):
        #Ce tokenizer  de nltk supprime en meme temps les ponctuation, sépare les apostrophes
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        #supprimer les url dans mon corpus
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        text_corpus = url_pattern.sub(r'', text_corpus)
        #supprime les nombres dans mon corpus
        text_corpus=re.sub("\d+", "", text_corpus)
        #mettre en minuscule et tokenize text
        text_corpus = tokenizer.tokenize(text_corpus.lower())
        #Supprime les tokens qui ne sont pas alphabetique
        text_corpus = [token for token in text_corpus if token.isalpha()]
        # suppression des mots peu informatifs
        stop_words = set(nltk.corpus.stopwords.words('english'))
        text_corpus = [token for token in text_corpus if not token in stop_words]
        #Lemmatizer: utiliser pour la lemmatisation
        wordnet_lemmatizer = WordNetLemmatizer()
        text_corpus = [wordnet_lemmatizer.lemmatize(token, pos="v") for token in text_corpus]
        # Supprimons les tokens de longueur égale à 1
        text_corpus = [token for token in text_corpus if len(token)>1]
        return text_corpus
    
    
    ####### fonction concorde
    def concorde(self,motif):
       motif=motif.lower()
       #transformons notre collection en chaine
       text_corpus=". ".join(str(doc) for doc in self.collection.values())
       #tokenize et supprime ponctuation
       text_corpus=self.nettoyer_corpus(text_corpus)
       #reconversion en chaine
       text_corpus = " ".join(str(x) for x in text_corpus)
       gauche=re.findall(r"(.*?:^|\S+\s+\S+\s+\S+) {} ".format(motif), text_corpus)
       droite=re.findall(r" {} (s*\S+\s+\S+\s+\S+|$)".format(motif), text_corpus)
       motif=[motif]*len(gauche)
       return pandas.DataFrame(list(zip(gauche, motif,droite)),columns =['gauche', 'motif','droite'])
    
    
################################################################################################

# corpus_reddit = Corpus("Corona")
# corpus_arxiv = Corpus("Corona")
# corpus_global = Corpus("Corona")

# ######### Source Reddit #########
# reddit = praw.Reddit(client_id='2R8dyFhAMrONHA', client_secret='HKBF3vfSYP6YOAPS4hgXf68OOJ4', user_agent='Reddit WebScraping')
# hot_posts = reddit.subreddit('Coronavirus').hot(limit=100)

# for post in hot_posts:
#     # Get comments of post i
#     try:
#       submission = reddit.submission(url=post.url);
#       nbComments = len(submission.comments)
#     except:
#       pass
#     datet = dt.datetime.fromtimestamp(post.created)
#     txt = post.title + ". "+ post.selftext
#     txt = txt.replace('\n', ' ')
#     txt = txt.replace('\r', ' ')
#     doc = RedditDocument(nbComments,
#                          datet,
#                          post.title,
#                          post.author_fullname,
#                          txt,
#                          post.url)
#     corpus_global.add_doc(doc)
#     corpus_reddit.add_doc(doc)
    
# ######### Source Reddit #########
# url = 'http://export.arxiv.org/api/query?search_query=all:covid&start=0&max_results=100'
# data =  urllib.request.urlopen(url).read().decode()
# docs = xmltodict.parse(data)['feed']['entry'] # Liste de dictionnaire

# for i in docs:
#     datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
#     try:
#         author = [aut['name'] for aut in i['author']][0]
#     except:
#         author = i['author']['name']
#     txt = i['title']+ ". " + i['summary']
#     txt = txt.replace('\n', ' ')
#     txt = txt.replace('\r', ' ')
#     doc = ArxivDocument(i['author'],
#                    datet,
#                    i['title'],
#                    author,
#                    txt,
#                    i['id']
#                    )
#     corpus_global.add_doc(doc)
#     corpus_arxiv.add_doc(doc)

# # Variété des champs léxical(nombre de mot unique utilisé par chaque author dans ces publication)
# # Histoire de savoir qui a le vocabulaire le plus riche
# freq,stats,voc = corpus_global.freq_stats_corpus2(True)
# df = pandas.DataFrame.from_dict(stats, orient='index')
# df = df.sort_values(by = 'total', ascending = False)
# fig = df.plot(figsize=(10,5),kind='bar', color=["#FFA07A","#885533"], title='Top 200 publications Redit-Arxiv par nombre de mots').get_figure()
# fig.savefig('histogramme/corpus/freq_corpus.png')

# # Récupération des comptages
# # Affichage des fréquences de mots aprés Tokenization(sans nettoyage)

# # Récupération des comptages
# freq,stats,voc = corpus_reddit.freq_stats_corpus1()
# df = pandas.DataFrame.from_dict(stats, orient='index')
# df = df.sort_values(by = 'total', ascending = False).head(30)
# fig = df.plot(figsize=(10,5),kind='bar', color=["#008000","#aa5588"], title='Top 100 publications Redit par nombre de mots').get_figure()
# fig.savefig('histogramme/reddit/freq_reddit.png')

# # Récupération des comptages
# freq,stats,voc = corpus_arxiv.freq_stats_corpus1()
# df = pandas.DataFrame.from_dict(stats, orient='index')
# df = df.sort_values(by = 'total', ascending = False).head(30)
# fig = df.plot(figsize=(10,5),kind='bar', color=["#008000","#aa5588"], title='Top 100 publications Arxiv par nombre de mots').get_figure()
# fig.savefig('histogramme/arxiv/arxiv.png')

