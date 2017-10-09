import requests
import sys
import networkx as nx
import time,json
import urllib, re
#from scraper import grabContent
import nltk
import time
import networkx as nx
from nltk.util import ngrams
from nltk.corpus import wordnet
from nltk import word_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from collections import Counter
#import ahocorasick
from nltk.corpus import stopwords
import os, sys, nltk
from nltk.util import ngrams
import io

import numpy as np
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
from elasticsearch import Elasticsearch
import time,json

newsdict= {}
file = open("newsfile.txt","w") 
apikey = "7f647aab82f24c068e6509274ad8522c"
#response = requests.get('https://newsapi.org/v1/articles?source=techcrunch&apiKey='+ apikey )
#response = response.json()

w = []
w.extend(["techcrunch","abc-news-au","al-jazeera-english","ars-technica","associated-press","bbc-news","bbc-sport","bild","bloomberg","breitbart-news","business-insider","business-insider-uk","buzzfeed","cnbc","cnn","daily-mail","der-tagesspiegel","die-zeit","engadget","entertainment-weekly","espn-cric-info","espn","financial-times","football-italia","focus","four-four-two","fortune","fox-sports","google-news","gruenderszene","hacker-news","handelsblatt","ign","independent","mashable","metro","mirror","mtv-news","mtv-news-uk","national-geographic","new-scientist","newsweek","new-york-magazine","polygon","recode","reddit-r-all","reuters","spiegel-online","t3n","talksport","techradar","the-economist","the-guardian-au","the-guardian-uk","the-hindu","the-huffington-post","the-huffington-post","the-lad-bible","the-new-york-times","the-next-web","the-sport-bible","the-telegraph","the-telegraph","the-verge","the-wall-street-journal","the-washington-post","usa-today","time","wired-de","wirtschafts-woche"])


stop_words = set(stopwords.words('english'))
G=nx.DiGraph()

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

onelist=[]
for k in range (0,len(w)-1):
	print "------------------"+w[k]+"------------------------"
	response = requests.get('https://newsapi.org/v1/articles?source='+w[k]+'&apiKey='+ apikey )
	response = response.json()
	print response
	#print response
	allstr=""
	onedict={}
	for valresp in response['articles']:
		print valresp['title'].encode(sys.stdout.encoding, errors='replace')
		if valresp['title']!=None:
			onedict.update({'title':valresp['title']})
			file.write(valresp['title'].encode(sys.stdout.encoding, errors='replace')+'\n')
		else:
			file.write('unavailable'+'\n')
			onedict.update({'title':'unavailable'})
		print valresp['description']
		
		if valresp['description']!=None:
			onedict.update({'description':valresp['description']})
			file.write(valresp['description'].encode(sys.stdout.encoding, errors='replace')+'\n')
		else:
			onedict.update({'description':'unavailable'})
			file.write('unavailable'+'\n')
		
		allstr = valresp['description']
		try:
		#print image					
			words = word_tokenize(allstr)

			#print(words)

			fin_list1 = []
			for word in words:
					if wordnet.synsets(word):
							fin_list1.append(word)

			#print(fin_list1)

			lemmatizer = WordNetLemmatizer()
			fin_lits1 = [lemmatizer.lemmatize(token) for token in fin_list1]

			stop_words = set(stopwords.words('english'))

			fin_list = []
			entity_list=[]
			for word in fin_list1:
					if word not in stop_words:
							fin_list.append(word)
			text = " ".join(fin_list)
			valtext = text.split(' ')
			stop_words = set(stopwords.words('english'))
			data =[]
			for r in valtext:
				#print r
				if not r in stop_words:
					data.append(r.lower())
			#print data
			fourgrams2 = ngrams(data, 4)

			keyword=["Business", "Technology", "Climate","Agriculture", "Sports", "Energy","Entertainment","Politics", "Electronics", "finance", "Auditing", "Banking", "Insurance", "Magazines", "Real Estate", "Investment", "Manufacturing", "Security", "Small Business", "Marketing",
   "Advertising", "Taxation","Cricket", "Football", "Golf", "Gymnastics", "Hockey", "Horse Racing", "Basketball", "Billiards", "Running", "Soccer", "Tennis",
   "Water Sports", "Software", "Web Design", "bots", "Graphics", "Internet", "Health", "Machine learning", "Engineering",
"Internet Things", "Multimedia", "Telecommunications", "Biotechnology","Solar Energy", "Electric power", "Fuels","Geothermal Energy" , "Oil","Smart Grid","Mining","Coal","Natural Gas", "Renewable Energy", "Wind Energy","hydroelectricity","Chemistry", "Electronics", "Mechanics"]
			key_len=[0 for x in range(0, len(keyword))]
			key_div=[1 for x in range(0, len(keyword))]
			count=0
			print "fourgrams"
			for grams in fourgrams2:
				try:
						entval = grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3]
						#print entval

						if entval in G:
								#print entva
								if count<=2:
										entity_list.append(str(entval))
										count=count+1

								for x in range(0, len(keyword)):
									if nx.has_path(G,source=keyword[x].lower() ,target=entval):
										if  x==3 or x==4 :
												key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
												#key_div[x]=key_div[x]+2.01
												key_div[x]=key_div[x]+1
										elif x==5:
														key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
														#key_div[x]=key_div[x]+1.65
														key_div[x]=key_div[x]+1
										else:
											key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
											#key_div[x]=key_div[x]+1.01
											key_div[x]=key_div[x]+1
				except Exception as e2:
					print str(e2),'exception 2'


			count=0
			trigrams2 = ngrams(data, 3)
			print "trigrams"
			for grams in trigrams2:
					entval = grams[0]+' '+grams[1]+' '+grams[2]
					#print entval
					#entity_list.append(entval)
					try:
						if entval in G:
								if count<=3:
										entity_list.append(str(entval))
										count=count+1
								#print entval
								for x in range(0, len(keyword)):
									if nx.has_path(G,source=keyword[x].lower() ,target=entval):
										if  x==3 or x==4:
												key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
												key_div[x]=key_div[x]+1
										
										elif x==5:
														key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
														key_div[x]=key_div[x]+1

										else:
												key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
												key_div[x]=key_div[x]+1
					except Exception as e2:
						print str(e2),'exception 3'


			count=0
			print "bigrams"
			bigrams2 = ngrams(data, 2)
			for grams in bigrams2:
					try:                                                                                                                            #entity_list.append(entval)
						entval = grams[0]+' '+grams[1]
						#print entval
						if entval in G:
								if count<=4:
										entity_list.append(str(entval))
										count=count+1
								#print entval
								for x in range(0, len(keyword)):
									if nx.has_path(G,source=keyword[x].lower() ,target=entval):
										if x==3 or x==4 :
												key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
												key_div[x]=key_div[x]+1
										elif x==5:
														key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
														key_div[x]=key_div[x]+1
										else:
												key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
												key_div[x]=key_div[x]+1
					except Exception as e2:
						print str(e2),'exception 3'
																																	#entity_list.append(entval)
					

			count=0
			unigrams2 = ngrams(data, 1)
			print "unigrams"
			for grams in unigrams2:
					try:
						entval = grams[0]
						#print entval

						if entval in G:
								#print entval
								if count<=5:
										entity_list.append(str(entval))
										#print entval
										count=count+1
								for x in range(0, len(keyword)):
									if nx.has_path(G,source=keyword[x].lower() ,target=entval):
										if x==3 or x==4:
												key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
												key_div[x]=key_div[x]+1
										
										elif x==5:
											key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
											key_div[x]=key_div[x]+1

										else:
												key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
												key_div[x]=key_div[x]+1
					except Exception as e2:
						print str(e2),'exception 3'
			indexvar=""
			flaglist = [int(key_len[x]/key_div[x]) for x in range(0,len(keyword))]
			print flaglist
			counter =0
			for i in range(len(keyword)):
				if True :
					#print 'jocjpco hococoho'
					if flaglist[i]<4 and flaglist[i]>0 and keyword[i]!='Politics':
						counter = counter+1
						if counter>2:
							break
						if len(indexvar)==0:
                                                        indexvar=keyword[i]
                                                else:
                                                        indexvar= indexvar+", "+keyword[i]		
					if keyword[i]=='Sports' and flaglist[i]<9 and flaglist[i]>0:
						indexvar= indexvar+", "+keyword[i]

			
			flaglist.sort()
			#indexvar=""
			i=0
			flag=True
			while flaglist[i]==0:
					i=i+1
					if i== len(flaglist):
							flag=False
							break
			print entity_list

			if flag:
				for x  in range(0,len(keyword)):
					if flaglist[i]==int(key_len[x]/key_div[x]):
						if keyword[x] in indexvar:
							continue
						print '$$$$$$$$$$$ '+ keyword[x] +' ####################'
						if len(indexvar)==0:
							indexvar=keyword[x]
						else:
							indexvar= indexvar+", "+keyword[x]
			else:
				indexvar="Other category"
			'''
			if indexvar=='':
				indexvar="Other category"
			'''
			print indexvar
			onedict.update({'Category':indexvar})
			file.write(indexvar+'\n')
		except Exception as e2:
			print str(e2),'exception 3'

		print  valresp['publishedAt']
		if valresp['publishedAt']!=None:
			onedict.update({'date':valresp['publishedAt']})
			file.write(valresp['publishedAt'].encode(sys.stdout.encoding, errors='replace')+'\n')
		else:
			onedict.update({'date':'unavailable'})
			file.write('unavailable'+'\n')
		print valresp['urlToImage']
		if valresp['urlToImage']!=None:
			onedict.update({'image':valresp['urlToImage']})
			file.write(valresp['urlToImage'].encode(sys.stdout.encoding, errors='replace')+'\n')
		else:
			onedict.update({'image':'unavailable'})
			file.write('unavailable'+'\n')
		print valresp['url']
		onedict.update({'url':valresp['url']})
		file.write(valresp['url'].encode(sys.stdout.encoding, errors='replace')+'\n')
		onelist.append(onedict)
#jsonfile = json.dump(newsdict)
newsdict.update({'articles':onelist})
#print newsdict
new_list = []
j = ''
for i in newsdict['articles']:
	print i
	if j != i:
		j = i
		new_list.append(j)
newsdict.update({'articles':new_list})
print newsdict
with open('newsjson.txt', 'w') as outfile:
	json.dump(newsdict, outfile)

	

