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

URL=[]
import json
# location given here
location = "delhi technological university"

list_word = ['awesome','artificial', 'intelligence','chatbot', 'business','kaggle','ai', 'tensorflow']
client = MongoClient()
db = client.test

#db.users.deleteOne( { status: "D" } )
Scursor = db.SearchHistory.find()
for hist in Scursor:
	print hist

cursor = db.config.find({'user':'asd'})
for document in cursor:
	 for key in document['choice']:
		doccat = 'doc'+key.lower().replace(' ','_')
		URL.append(("http://localhost:9200/"+doccat+"/_search?size=1000&q=*:*",key,doccat))
		for val in document['choice'][key]:
			print key.lower().replace(' ','_')+val.lower().replace(' ','_')
			doccatsubcat = doccat+val.lower().replace(' ','_')
                	URL.append(("http://localhost:9200/"+doccatsubcat+"/_search?size=1000&q=*:*",key+' '+val,doccatsubcat))

raw_input("Stop") 

# defining a params dict for the parameters to be sent to the API
PARAMS = {'address':location}
for i in URL:
# sending get request and saving the response as response object
        r = requests.get(url = i[0])
        #from newclassify import classifier
        import math

        stop_words = set(stopwords.words('english'))

        client = MongoClient()
        db = client.test
        cursor = db.config.find()
        for document in cursor:
                print document['choice']
	
	es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
       	# extracting data in json format
        rdata = r.json()
        data = rdata['hits']['hits']
        for d in  data:
        	try:
			score = 0.0
                        #print d['_source']['header']
                        da = d['_source']['data']
                        text=''
                        scoredict={}
                        for word in list_word:
                               try:
                               		#if len(word)!=0 or str(word)!='\n' or str(word)!='\t':
                                        #text=text+str(word)

                                        if word.lower() in da:
						#print 'boom', word
                                        	score = score + 0.01
					#print score
                               except Exception as e:
                                	pass
                        	
				
                        	
                        if len(d['_source']['scores'])>0:
                        	d['_source']['scores'][0] =d['_source']['scores'][0]+ score
						
                        else:
                                d['_source']['scores'].append(score+0.26)
                                
			d['_source']['flagindex'] = i[1]
                        	
			#es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
                       	#dict1 = {"scores":20.001,"link":'self.url',"data":'text',"header":'heade',"votes":'scores', "entity":'ent_list', "flagindex":'flagindex'}
                        jsondata = d['_source'] #json.dumps(dict1, ensure_ascii=False)
                        #print "Inserting"
                        es.update(index=i[2], doc_type='peopleimg', id=d['_source']['link'],body={"doc":jsondata})
                except:
			print "error2"



