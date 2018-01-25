import requests
from nltk.corpus import stopwords
from elasticsearch import Elasticsearch
# api-endpoint
import urllib2
import re
from bs4 import BeautifulSoup
from nltk.corpus import wordnet
from nltk import word_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter
import ahocorasick
from nltk.corpus import stopwords
import os, sys, nltk
from nltk.util import ngrams
import io
import urllib, sys, bs4
import networkx as nx
import numpy as np
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
#from searchengine.settings import P
#from searchengine.settings import T
#from searchengine.settings import B
#from searchengine.settings import E
from pymongo import MongoClient
import networkx as nx
from nltk.corpus import stopwords
G=nx.DiGraph()
stop_words = set(stopwords.words('english'))

with open("categoryAndTheirSubcategories",'r') as edges:

    for line in edges:
        line=line.rstrip()
        data1=[]
        data2=[]
        d1_string=''
        d2_string=''
        toks=line.split('\t')
        list1 = toks[0].split('_')
        for word in list1:
            if word not in stop_words:
                #data1.append(word)
                d1_string=d1_string+' '+word
        d1_string = d1_string[1:]

        list2 = toks[1].split('_')
        for word in list2:
            if word not in stop_words:
                #data2.append(word)
                d2_string=d2_string+' '+word
        d2_string = d2_string[1:]
        #tech_file.write(d2_string.lower()+' '+d1_string.lower()+"\n")
        #print d2_string.lower(), d1_string.lower()
        G.add_edge(d2_string.lower(),d1_string.lower())
        #G.add_edge(d1_string.lower(),d2_string.lower())


from operator import itemgetter

import itertools
from collections import Counter

#from newclassify import classifier
import math

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

import json
# location given here
location = "delhi technological university"

list_word = ['artificial', 'intelligence']
client = MongoClient()
db = client.test

#db.users.deleteOne( { status: "D" } )
Scursor = db.SearchHistory.find()

search_hist = []


def build_vocab(sentences):
    wordlist1 = []
    wordlist = []
    for i in sentences:
	words = word_tokenize(i)
	words2 = []
	#print "words",words
	if len(words)==2:
		     bi = words[0] + " " + words[1]
                     print bi
                     words2.append(bi)
	if len(words)>2:
		for i,j in enumerate(words[0:-2]):
			print j
			bi = words[i] + " " + words[i+1]
			print bi
			words2.append(bi)
	if len(words)==3:
		     tri = words[0] + " " + words[1] + " " + words[2]
                     print tri
                     words2.append(tri) 
	if len(words)>2:
                for i,j in enumerate(words[0:-3]):
			print j
                        tri = words[i] + " " + words[i+1] + " " + words[i+2] 
                        print tri
			words2.append(tri)

	wordlist1.extend(words)
	wordlist1.extend(words2)
	print "words2",words2
    lemmatizer = WordNetLemmatizer()
    wordlist1 = [lemmatizer.lemmatize(token) for token in wordlist1]
   
    stop_words = set(stopwords.words('english'))

    for word in wordlist1:
		if word not in stop_words:
			wordlist.append(word)
    wordfreq = [wordlist.count(p) for p in wordlist]
    #sorted(wordfreq,key=itemgetter(1))
    result = list(set(zip(wordlist, wordfreq)))
    result = sorted(result,key=itemgetter(1), reverse=True)
    return result


def find_history(user):
        client = MongoClient()
        db = client.test
        Scursor = db.SearchHistory.find({'user':user})
        #search_hist = []
        for hist in Scursor:
                print hist['history']
                list_word= hist['history']
		for val in list_word:
			print val
			bigrams = ngrams(val, 1)
			for key in bigrams:
				print key
        #print "list_word",list_word
	reclist= build_vocab(list_word)
	paternlist=[]
	for key in reclist:
		val = key[0]	
		paternlist.append(val)
		if val in G:
                	iterval =G.successors_iter(val)
			counter=0
                	for neb in iterval:
				if  counter<=10:
					paternlist.append(neb)
					counter=counter+1

	return paternlist
                        


	#return dict_list
likecur = db.LikedPosts.find()
for doc in likecur:
	print doc
Scursor = db.SearchHistory.find({'user':'testuser'})
#for i in Scursor:
#	print i
x = find_history('testuser')
print "x:",x



