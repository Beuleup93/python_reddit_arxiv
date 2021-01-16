#!/usr/bin/env python3
# -*- coding: utf-8 -*-

################################## Notre controller: Classe Corpus ##################################

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
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import numpy
import num2word
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

    # remove ponctuation
    def ponctuation(self,chaine):
      ponct = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
      for i in ponct:
        chaine = numpy.char.replace(chaine, i, ' ')

    # convertir les nombre en lettre 
    def convert_number(self,chaine):
      liste = chaine.split(' ')
      l = []
      for word in liste:
        if word.isdigit():
          word = num2word(word)
        l.append(word) 
      return ' '.join(l)
    
    # Trouver les documents d'un auteurs lamda
    def find_documents_authors(self):
        author_documents = defaultdict(list)
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        for nauth,author in self.authors.items():
            for ndoc,doc in author.get_production().items():
                author_documents[author] += tokenizer.tokenize(doc.get_text().lower())
        return author_documents

    # Sans prétraitement
    def freq_stats_corpus1(self, bySource = False): # bySource = False on étudier le cumul des document publié par chaque auteur
      # Ici on ne fait que Tokeniser puis compter la fréqence des mots selon le context
      tokenizer = nltk.RegexpTokenizer(r'\w+')
      #Statistique et fréquence
      freq_stats = defaultdict(list) 
      if bySource: # Cas on compare la fréquence des mot par rapport aux deux source
        for k,doc_source in self.collection.items():
          # Vérification de l'instance d'objet en question
          if isinstance(doc_source, RedditDocument):
            freq_stats['Reddit'] += tokenizer.tokenize(doc_source.get_text().lower())
          else:
            freq_stats['Arxiv'] += tokenizer.tokenize(doc_source.get_text().lower())
      # source reddit or arxiv: tout dépend de l'instance appelante 
      else: # Cas ou on étudie les source à part
        for k,doc in self.collection.items():
          current_author = doc.get_author()
          for num_doc, doc_author in self.collection.items():
            if doc_author.get_author()==current_author:
              freq_stats[current_author] += tokenizer.tokenize(doc_author.get_text().lower())
      # Calcul des fréquences d'apparition des mots (mots en doublons et uniques)
      stats, freq = dict(), dict() 
      for author, word in freq_stats.items():
        freq[author] = fq = nltk.FreqDist(word)
        stats[author] = {'total': len(word), 'unique': len(fq.keys())} 
      return (freq, stats, freq_stats)
     ####################################### Nettoyage et normalisation ##################################
    '''
      Les méthodes freq_stats_corpus3, freq_stats_corpus4,create_and_normalize_corpus2, create_and_normalize_corpus1, 
      ont été créée dans le but de voir l'effet de chaque traitement sur nos données. On cherche pas à optimiser ici.
      Une version finale de notre methode de pretraitement est développé pour la suite des opération

      Nous nous sommes basés sur le cours de openclassroom et adapté ca selon nos besoins.
      lien: https://openclassrooms.com/fr/courses/4470541-analysez-vos-donnees-textuelles/4855001-representez-votre-corpus-en-bag-of-words

      bySource: boolean. 
      si bySource = True => on applique la méthode pour voir la fréquence d'apparition de chaque mots
                            des corpus reddit et arxiv(compare reddit et arxiv)

         bySource = False => on veut voir la fréquence d'apparition de mots(double et unique) dasn l'ensemble
                             des documents publié par chaque auteurs de reddit ou de Arxiv
                             Histoire de voir la variétés des textes pour les auteurs des differentes source
              
        
    '''
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
        # Calcul des fréquences d'apparition des mots (mots en doublons et uniques)
        stats, freq = dict(), dict() 
        for key, word in freq_stats.items():
            freq[key] = fq = nltk.FreqDist(word)
            stats[key] = {'total': len(word), 'unique': len(fq.keys())} 
        return (freq, stats, freq_stats)
  
    # Freq et stats aprés suppression des stop word et lemmatisation
    def freq_stats_corpus3(self, bySource = False):
      # utilisation de nltk pour lemmatiser
      wordnet_lemmatizer = WordNetLemmatizer()
      #Tokenisation
      tokenizer = nltk.RegexpTokenizer(r'\w+')
      # pour stocker les statistiques
      freq_stats = defaultdict(list) 
      # utilisation des stopword anglais de nltk pour supprimer les mots peux informatifs
      stop_words = set(nltk.corpus.stopwords.words('english'))
      if bySource: # True => comparaison Reddit et Arxiv
        for k,doc_source in self.collection.items():
          tokens = tokenizer.tokenize(doc_source.get_text().lower())
          if isinstance(doc_source, RedditDocument):
            freq_stats['Reddit'] += [wordnet_lemmatizer.lemmatize(word, pos="v") for word in tokens if not word in stop_words]
          else:
            freq_stats['Arxiv'] += [wordnet_lemmatizer.lemmatize(word, pos="v") for word in tokens if not word in stop_words]
      # source reddit or arxiv: tout dépend de l'instance appelante 
      else: ## Frequence d'apparition des mots de l'enseble des docs de chaque auteurs
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
      # utilisation de PorterStemmer pour lemmatiser
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
      # source reddit or arxiv: tout dépend de l'instance appelante
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
    
    # chargement des données au démarrage de l'application
    def remplir_corpus(self):
        obj_reddit=Corpus("corona") #Corpus pour uniquement les opération sur reddit
        obj_arxiv=Corpus("corona") #Corpus pour uniquement les opération sur arxiv
        obj_general=Corpus("corona") # corpus pour les opérations sur les deux source
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
        # renvoyer les trois objets
        return (obj_general, obj_reddit, obj_arxiv)
    
    # Le ou les top nb_word mots les plus utilisés pour un jour donnée
    def most_frequent_word(self, date, nb_word): # format date: '2021-01-02'
      self.vocabulaires = list()
      y,m,d = [int(x) for x in date.split('-')] 
      date_choosed = dt.date(y,m,d)
      for k,v in self.collection.items():
        date_document = v.get_date()
        if date_document.date() == date_choosed:
          #nettoyage global de notre corpus
          tokensList = self.nettoyer_corpus(v.get_text())
          self.vocabulaires += tokensList
      #Comptons les occurence de mots dans le la liste vocabulaires
      occurences = Counter(self.vocabulaires)
      return occurences.most_common(nb_word)

    # Le ou les top nb_word mots les plus utilisés par année
    def most_frequent_word_by_year(self, year, nb_word): # format year: '2021'
      self.vocabulaires = list()
      for k,v in self.collection.items():
        date_document = v.get_date()
        if date_document.strftime('%Y') == year:
          #nettotyage global de notre corpus
          tokensList = self.nettoyer_corpus(v.get_text())
          self.vocabulaires += tokensList
      #Comptons les occurence de mots dans le la liste vocabulaires
      occurences = Counter(self.vocabulaires)
      return occurences.most_common(nb_word)

    # Le ou les top nb_word mots les plus utilisés par month
    def most_frequent_word_by_month(self, month, nb_word): # format month: 'December'
      self.vocabulaires = list()
      for k,v in self.collection.items():
        date_document = v.get_date()
        if date_document.strftime('%B') == month:
          #nettotyage global de notre corpus
          tokensList = self.nettoyer_corpus(v.get_text())
          self.vocabulaires += tokensList
      #Comptons les occurence de mots dans le la liste vocabulaires
      occurences = Counter(self.vocabulaires)
      return occurences.most_common(nb_word)

    # Le ou les top nb_word mots les plus utilisés pour un jour de tous les mois de l'année
    def most_frequent_word_by_day(self, jour,nb_word): # format jour: '01'
      self.vocabulaires = list()
      for k,v in self.collection.items():
          date_document = v.get_date()
          if date_document.strftime('%d') == jour:
            # nettotyage global de notre corpus
            tokensList = self.nettoyer_corpus(v.get_text())
            self.vocabulaires += tokensList
      # Comptons les occurence de mots dans le la liste vocabulaires
      occurences = Counter(self.vocabulaires)
      # On retourne les nb_word les plus fréquents
      return occurences.most_common(nb_word)
    
    ###### Mot commun et mot spécifique de chaque source
    def wordcommun_and_wordspecific(self):
      # recuperation des deux source nettoyer et normaliser
      all_source = self.find_documents_source()
      # source reddit et source arxiv
      source_reddit, source_arxiv = all_source['reddit'],all_source['arxiv']
      # utilisation des comprehension pour renvoyer les mots commun, specific
      word_communs = [wc for wc in source_reddit if wc in source_arxiv]
      word_specific_reddit = [word for word in source_reddit if not word in word_communs]
      word_specific_arxiv = [word for word in source_arxiv if not word in word_communs]
      # on retourne des sets pour eviter les doublons
      return (set(word_communs),set(word_specific_reddit),set(word_specific_arxiv))

    ###### Recuperer les docs de chaque source sous for de dictionnaire: source, valeur: liste chaine
    def find_documents_source(self):
      documents_source = defaultdict(list)
      for ndoc, doc in self.collection.items():
        if isinstance(doc,RedditDocument):
          documents_source['reddit'] += self.nettoyer_corpus(doc.get_text())
        else:
           documents_source['arxiv'] += self.nettoyer_corpus(doc.get_text())
      return documents_source
    
    ################# Fonction de nettoyage finale ###################
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
    
    ####### fonction concorde pour chercher les motif(Ecrit en Td)
    def concorde(self,motif):
       motif=motif.lower()
       #transformons notre collection en chaine
       text_corpus=". ".join(str(doc) for doc in self.collection.values())
       #tokenize et supprime ponctuation
       text_corpus=self.nettoyer_corpus(text_corpus)
       #reconversion en chaine
       text_corpus = " ".join(str(x) for x in text_corpus)
       #motif gauche
       gauche=re.findall(r"(.*?:^|\S+\s+\S+\s+\S+) {} ".format(motif), text_corpus)
       #motif droite
       droite=re.findall(r" {} (s*\S+\s+\S+\s+\S+|$)".format(motif), text_corpus)
       motif=[motif]*len(gauche)
       return pandas.DataFrame(list(zip(gauche, motif,droite)),columns =['gauche', 'motif','droite'])
      
    ######## TFIDF ###############
    # Source : https://towardsdatascience.com/natural-language-processing-feature-engineering-using-tf-idf-e8b9d00e7e76
    # Cette fonction nous calcule le tf-idf de chaque token du corpus
    def caluculTF_IDF(self):
      # recuperation les doc de chaque source sour forme de chaine de caractere
      doc_reddit, doc_arxiv = self.doc_reddit_arxiv()
      vectorizer = TfidfVectorizer()
      vectors = vectorizer.fit_transform(doc_reddit)
      feature_names = vectorizer.get_feature_names()
      dense = vectors.todense()
      denselist = dense.tolist()
      return pandas.DataFrame(denselist, columns=feature_names)

    def doc_reddit_arxiv(self):
      # renvoyer les doc de chaque source sour forme de liste chaine de caractere
      doc_reddit = [" ".join(self.nettoyer_corpus(doc.get_text())) for ndoc,doc in self.collection.items()  if isinstance(doc,RedditDocument)]
      doc_arxiv = [" ".join(self.nettoyer_corpus(doc.get_text())) for ndoc,doc in self.collection.items()  if isinstance(doc,ArxivDocument)]
      return (doc_reddit,doc_arxiv)
  