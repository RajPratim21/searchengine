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
	wordlist1.extend(words)
    lemmatizer = WordNetLemmatizer()
    wordlist1 = [lemmatizer.lemmatize(token) for token in wordlist1]
   
    stop_words = set(stopwords.words('english'))

    for word in wordlist1:
		if word not in stop_words:
			wordlist.append(word)
    wordfreq = [wordlist.count(p) for p in wordlist]
    #sorted(wordfreq,key=itemgetter(1))
    result = list(set(zip(wordlist, wordfreq)))
    result = sorted(result,key=itemgetter(1))
    return result


def find_history(user):
        client = MongoClient()
        db = client.test
        Scursor = db.SearchHistory.find({'user':user})
        #search_hist = []
        for hist in Scursor:
                print hist['history']
                list_word= hist['history']
        #print "list_word",list_word
	return build_vocab(list_word)


def find_config(user):
	client = MongoClient()
	db = client.test
	Scursor = db.SearchHistory.find({'user':user})
	#search_hist = []
	for hist in Scursor:
	        print hist['history']
	        list_word= hist['history']
	print "list_word",list_word
	#csur= db.LikedPosts.find()
	#for dc in csur:
	#	print dc
	cursor = db.config.find()
	user_id=0
	for doc in cursor:
		if user==doc['user']:
			break
		user_id =user_id+1 
	#print user_id
	URL=[]
	
	cursor = db.config.find({'user':user})
	for document in cursor:
	
		for key in document['choice']:
			#print 'dssd'
			doccat = 'doc'+key.lower().replace(' ','_')
			#print doccat
			URL.append(("http://localhost:9200/"+doccat+"/_search?size=1000&q=*:*",key,doccat))
			doccat2 = 'doc'+key.lower().replace(' ','')
			#print doccat2
                	URL.append(("http://localhost:9200/"+doccat2+"/_search?size=1000&q=*:*",key,doccat2))

			for val in document['choice'][key]:
				#print key.lower().replace(' ','_')+val.lower().replace(' ','_')
				doccatsubcat = doccat+val.lower().replace(' ','_')
				try:    
					r = requests.get(url = "http://localhost:9200/"+doccatsubcat+"/_search?size=1000&q=*:*")
					rdata = r.json()
					#print rdata
        				data = rdata['hits']['hits']
					#print doccatsubcat
	            			URL.append(("http://localhost:9200/"+doccatsubcat+"/_search?size=1000&q=*:*",key+' '+val,doccatsubcat))
				except:
					continue

	if len(list_word)>10:
                list_word = list_word[-10:]
	#print list_word, "dscscs@@@@@@@@@@@@"        
			
	myquery ={
                     "query":
                            {

                                                "multi_match":
                                                        {
                                                          "query": " ".join(list_word),
                                                          "fields": [ "data", "header" ]
                                                        }


                          },
                        "from" : 0, "size" : 100
                        }
               
        es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
	result = es.search(index="_all", body=myquery)
        max_score =0
        for rows in result['hits']['hits']:
        	if max_score<rows['_score']:
                	 max_score=rows['_score']
        for rows in result['hits']['hits']:
        	score =( rows['_score']/max_score)*0.5
                if len(rows['_source']['scores'])>user_id:
                	rows['_source']['scores'][user_id] =rows['_source']['scores'][user_id]+ score
                else:
                	for i in range(user_id):
                       		rows['_source']['scores'].append(0.15)
             	        rows['_source']['scores'].append(0.15+score)
                jsondata = rows['_source'] #json.dumps(dict1, ensure_ascii=False)
                es.index(index='doc'+user.lower() +'home', doc_type='peopleimg', id=rows['_source']['link'],body=jsondata)

	print URL
	for i in URL:
		myquery ={
	                 "query":
        	                {
	
        	                                "multi_match":
                	                                {
                                	                  "query": " ".join(list_word),
                        	                          "fields": [ "data", "header" ]
                                        	        }


                      	  },	
                	"from" : 0, "size" : 100
        		}
		try:
			es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
			


			result = es.search(index=i[2], body=myquery)
			max_score =0
			for rows in result['hits']['hits']:
				if max_score<rows['_score']:
					max_score=rows['_score']
			for rows in result['hits']['hits']:
				#print rows['_source']['header']
				score =( rows['_score']/max_score)*0.5
        			
				if len(rows['_source']['scores'])>user_id:
        	        		rows['_source']['scores'][user_id] =rows['_source']['scores'][user_id]+ score
                           
        	        	else:
        	        		for i in range(user_id):
        	                		rows['_source']['scores'].append(0.15)
       		               		rows['_source']['scores'].append(0.15+score)
				jsondata = rows['_source'] #json.dumps(dict1, ensure_ascii=False)
                                       
        	        	es.update(index=i[2], doc_type='peopleimg', id=rows['_source']['link'],body={"doc":jsondata})

		except Exception as e:
			pass #print e
	'''
    	for i in URL:
		try:
	    		print '#$$##############', i
			# sending get request and saving the response as response object
            		r = requests.get(url = i[0])
            		#from newclassify import classifier
            		import math

            		stop_words = set(stopwords.words('english'))

            		client = MongoClient()
            		db = client.test
            		cursor = db.config.find()
        
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
                                                		score = score + 0.01
                                		except Exception as e:
                                        		pass
                                
                    
                                
                            		if len(d['_source']['scores'])>user_id:
                                		d['_source']['scores'][user_id] =d['_source']['scores'][user_id]+ score
                            
                            		else:
						for i in range(user_id):
                                    			d['_source']['scores'].append(0.25)
						d['_source']['scores'].append(0.25+score)
                                    
                	    		d['_source']['flagindex'] = i[1]
                                        #dict_list[user] = d['_source']['scores'] 
                            		jsondata = d['_source'] #json.dumps(dict1, ensure_ascii=False)
                            		#print "Inserting"
                            		es.update(index=i[2], doc_type='peopleimg', id=d['_source']['link'],body={"doc":jsondata})
                		except Exception as e:
	                		print e
		except Exception as e:
    			print e
	'''
	#return dict_list
likecur = db.LikedPosts.find()
for doc in likecur:
	print doc
Scursor = db.SearchHistory.find({'user':'asd'})
#for i in Scursor:
#	print i
x = find_history('asd')
print "x:",x
import time

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

if True:
	for doc in Scursor:
	#if True:
		#print doc['user']
		es.indices.delete(index='doc'+ doc['user']+'home', ignore=[400, 404])
		find_config( doc['user'])
		#time.sleep(2)
	time.sleep(5)
