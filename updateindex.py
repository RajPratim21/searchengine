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

from newclassify import classifier
import math

import json 
# location given here
location = "delhi technological university"
 


list_word = ['awesome','wornderful']

URL=[("http://localhost:9200/docai/_search?size=1000&q=*:*" ,'AI', 'docai')]
# defining a params dict for the parameters to be sent to the API
PARAMS = {'address':location}
for i in URL:
# sending get request and saving the response as response object
	r = requests.get(url = i[0])
	from newclassify import classifier
	import math

	stop_words = set(stopwords.words('english'))

	client = MongoClient()
	db = client.test
	cursor = db.config.find()
	for document in cursor:
		print(document)


	T =ahocorasick.Automaton()

	with open('sorted_Tech.txt') as file:
    		for line in file:
        		#idx=idx+1
        		#if idx==50:
        		#    break
        		sen = line.split('\t')[1].rstrip().replace('_',' ')
       		        tokens=filter(lambda w: not w in stop_words,sen.split())
        		valstr=""
        		if(len(tokens)==1):
            			T.add_word(tokens[0].lower(), (line.split('\t')[0],tokens[0].lower()))
        		else:
            			for x in range(0,len(tokens)):
                			if x== len(tokens)-1:
                    				valstr = valstr+tokens[x]
               			 	else:
                    				valstr = valstr+tokens[x]+" "
            			T.add_word(valstr.lower(), (line.split('\t')[0],valstr.lower()))



	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	# extracting data in json format
	rdata = r.json()
	data = rdata['hits']['hits']
	for d in  data:
		print d['_source']['header'], d['_source']['scores']
		'''
		try:
			print d['_source']['header'], d['_source']['scores']
			da = d['_source']['data']
			text=''
			scoredict={}

	
			
			for word in da:
				try:
					if len(word)!=0 or str(word)!='\n' or str(word)!='\t':
						text=text+str(word)
				
					if word in list_word:
							score = score + 0.01
				except Exception as e:
					#print(e)
					pass
			#classifier(text.lower(),text.lower(), T)
			
			if text!=None or text!='':
				if len(d['_source']['scores'])>0:
					d['_source']['scores'][0] = classifier(text.lower(),text.lower(), T)
				else:
					d['_source']['scores'].append(classifier(text.lower(),text.lower(), T))
				d['_source']['flagindex'] = i[1]

			#es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
			#dict1 = {"scores":20.001,"link":'self.url',"data":'text',"header":'heade',"votes":'scores', "entity":'ent_list', "flagindex":'flagindex'}
			jsondata = d['_source']	#json.dumps(dict1, ensure_ascii=False)
			#if True:
			print "Inserting" 
			es.update(index=i[2], doc_type='peopleimg', id=d['_source']['link'],body={"doc":jsondata})
		except:
			print 'except'
		'''
