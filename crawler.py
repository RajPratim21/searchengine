import sys  
import wikipedia
reload(sys)  
sys.setdefaultencoding('utf8')
import sys
import requests
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime
#from stack_spider import StackSpider
import urlparse
 
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

import urllib, re
#from scraper import grabContent
import nltk
import time
import networkx as nx
from nltk.corpus import stopwords
import sys
#from searchengine.settings import G 
import time
print 'start'
counter_ide =0
#from bs4 import BeautifulSoup
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
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

print 'reached......$$$$$'
def is_absolute(url):
    return bool(urlparse.urlparse(url).netloc)

def get_soup(link):
    """
    Return the BeautifulSoup object for input link
    """
    request_object = requests.get(link, auth=('user', 'pass'))
    soup = BeautifulSoup(request_object.content)
    return soup

def get_status_code(link):
    """
    Return the error code for any url
    param: link
    """
    try:
        error_code = requests.get(link).status_code
    except requests.exceptions.ConnectionError:
        error_code = None
    return error_code
def clean_html(html):
    """
    Copied from NLTK package.
    Remove HTML markup from the given string.

    :param html: the HTML string to be cleaned
    :type html: str
    :rtype: str
    """

    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()


def find_internal_urlswiki(lufthansa_url, depth=0, max_depth=500):
    all_urls_info = [] 
    status_dict = {}
    soup = get_soup(lufthansa_url)
    a_tags = soup.findAll("a", href=True)

    if depth > max_depth:
        return {}
    else:
    	global counter_ide
        print 'ide count',counter_ide
        counter_ide = counter_ide+1
        if counter_ide==1000:
           	return {}
        for a_tag in a_tags:
            if "http" not in a_tag["href"] and "/" in a_tag["href"]:
                url = lufthansa_url + a_tag['href']
                print "relative",url
            elif "http" in a_tag["href"] and is_absolute(a_tag["href"]):
                url = a_tag["href"]
                print "absolute",url
            else:
                continue
            list_all = url.split('/')
            print "inside1"
            try:
                        html = urllib.urlopen(url).read()
                        print "inside"
                        try:
                                page = wikipedia.page(list_all[-1])
                                header = page.title.lower()
				sumary = page.summary
				#print "summary",summary
				images = page.images
				if images[0][-2]=='j' and  images[0][-1]=='p':
					image =images[0]
				elif images[1][-2]=='j' and  images[1][-1]=='p':
                                        image =images[1]
				else:
                                        image =images[2]
					
				print image
					
                                print header.encode(sys.stdout.encoding, errors='replace')
                                url = page.url
                                print url

                                content = page.content.lower()
                                #print content.encode(sys.stdout.encoding, errors='replace')


                                #dict1= {"scores":[],"link":url ,"data":content,"header":header,"votes":1, "entity":entitity_list, "flagindex":'Agriculture'}

                                words = word_tokenize(content)

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

                                keyword=["Business", "Technology", "Water", "Agriculture", "Sports", "Energy", "People","Entertainment"]
                                key_len=[0 for x in range(0, len(keyword))]
                                key_div=[1 for x in range(0, len(keyword))]
                                count=0
                                print "fourgrams"
                                for grams in fourgrams2:
                                        entval = grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3]
                                        #print entval

                                        if entval in G:
                                                #print entva
                                                if count<=2:
                                                        entity_list.append(str(entval))
                                                        count=count+1

                                                for x in range(0, len(keyword)):
                                                	if nx.has_path(G,source=keyword[x].lower() ,target=entval):
                                                		if  x==3 or x==4 or x==2 :
	                                                			key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                			key_div[x]=key_div[x]+2.01
	                                                	elif x==5:
                                                                        key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                                        key_div[x]=key_div[x]+1.65

								else:
	                                                      		key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                      		key_div[x]=key_div[x]+1.01

                                count=0
                                trigrams2 = ngrams(data, 3)
                                print "trigrams"
                                for grams in trigrams2:
                                        entval = grams[0]+' '+grams[1]+' '+grams[2]
                                        #print entval
                                        #entity_list.append(entval)
                                        if entval in G:
                                                if count<=3:
                                                        entity_list.append(str(entval))
                                                        count=count+1
                                                #print entval
                                                for x in range(0, len(keyword)):
                                                	if nx.has_path(G,source=keyword[x].lower() ,target=entval):
                                                		if x==3 or x==4 or x==2 :
	                                                			key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                			key_div[x]=key_div[x]+2.01
	                                                	
								elif x==5:
                                                                        key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                                        key_div[x]=key_div[x]+1.65

								else:
	                                                      		key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                      		key_div[x]=key_div[x]+1.01


                                count=0
                                print "bigrams"
                                bigrams2 = ngrams(data, 2)
                                for grams in bigrams2:
                                        entval = grams[0]+' '+grams[1]
                                        #print entval
                                                                                                                    		                                        #entity_list.append(entval)
                                        if entval in G:
                                                if count<=4:
                                                        entity_list.append(str(entval))
                                                        count=count+1
                                                #print entval
                                                for x in range(0, len(keyword)):
                                                	if nx.has_path(G,source=keyword[x].lower() ,target=entval):
	                                                	if x==3 or x==4 or x==2 :
	                                                			key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                			key_div[x]=key_div[x]+2.01
	                                                	elif x==5:
                                                                        key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                                        key_div[x]=key_div[x]+1.65
								else:
	                                                      		key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                      		key_div[x]=key_div[x]+1.01


                                count=0
                                unigrams2 = ngrams(data, 1)
                                print "unigrams"
                                for grams in unigrams2:
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
	                                                	if  x==3 or x==4 or x==2:
	                                                			key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                			key_div[x]=key_div[x]+2.01
	                                                	
								elif x==5:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                                        key_div[x]=key_div[x]+1.65
			
								else:
	                                                      		key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                      		key_div[x]=key_div[x]+1.01
	                                
                                flaglist = [ int(key_len[x]/key_div[x]) for x in range(0,len(keyword))]
                                print flaglist

                                flaglist.sort()
                                indexvar=""
                                i=0
                                flag=True
                                while flaglist[i]==0:
                                        i=i+1
                                        if i== len(flaglist):
                                                flag=False
                                                break
                                print entity_list

                                if flag:
                                 	for x in range(0,len(keyword)):
                                   		if flaglist[i]==int(key_len[x]/key_div[x]):
                                   			print '$$$$$$$$$$$ '+ keyword[x] +' ####################'
                                   			if len(indexvar)==0:
                                   				indexvar=keyword[x]
                                   			else:
                                   				indexvar= indexvar+", "+keyword[x]
                                else:
                              		indexvar="Other category"

                                #print '$$$$$$$$$$$ '+ keyword[i] +' ####################'
                                if len(content)>4000:
                                    content =content[0:4000]
                                dict1= {"scores":[],"link":url ,"data": content,"header":header,"votes":0.8, "entity": entity_list, "flagindex":indexvar, "sum": sumary, "img": image}
                                data = json.dumps(dict1, ensure_ascii=False)
                                if keyword[0] in indexvar:
                                        es.index(index='doctechnology', doc_type='peopleimg', id=url,body=json.loads(data))
                                if keyword[1] in indexvar:
                                        es.index(index='docbusiness', doc_type='peopleimg', id=url,body=json.loads(data))
                                if keyword[2] in indexvar:
                                        es.index(index='docwm', doc_type='peopleimg', id=url,body=json.loads(data))
                                if keyword[3] in indexvar:
                                        es.index(index='docagri', doc_type='peopleimg', id=url,body=json.loads(data))
                                if keyword[4] in indexvar:
                                        es.index(index='docsports', doc_type='peopleimg', id=url,body=json.loads(data))
                                if keyword[5] in indexvar:
                                        es.index(index='docenergy', doc_type='peopleimg', id=url,body=json.loads(data))
                                if keyword[6] in indexvar:
                                        es.index(index='docpeople', doc_type='peopleimg', id=url,body=json.loads(data))
                                if keyword[7] in indexvar:
                                        es.index(index='docent', doc_type='peopleimg', id=url,body=json.loads(data))
                                if "Other category" == indexvar:
                                        es.index(index='docothers', doc_type='peopleimg', id=url,body=json.loads(data))

                                print 'done'





                        except Exception as e1:
                                print str(e1),'exception 1'
                                continue
            except Exception as e2:
                        print str(e2),'exception 2'
                        time.sleep(5)
                        continue
            status_dict["url"] = url
            status_dict["status_code"] = get_status_code(url)
            status_dict["timestamp"] = datetime.now()
            status_dict["depth"] = depth + 1
            all_urls_info.append(status_dict)
    return all_urls_info




url_pool=[]
def find_internal_urls(lufthansa_url, depth=0, max_depth=2):
    global url_pool
    if lufthansa_url in url_pool:
    	return {}
    else:
    	url_pool.append(lufthansa_url) 

    all_urls_info = []
    status_dict = {}
    soup = get_soup(lufthansa_url)
    a_tags = soup.findAll("a", href=True)
    if depth > max_depth:
        return {}
    else:
    	global counter_ide
        print 'ide count',counter_ide
        counter_ide = counter_ide+1
        if counter_ide==1000:
        	return {}    
        for a_tag in a_tags:
            if "http" not in a_tag["href"] and "/" in a_tag["href"]:
                url = lufthansa_url + a_tag['href']
                print "relative",url, counter_ide
                if url in url_pool:
                	continue
                else:
			    	url_pool.append(lufthansa_url) 

            elif "http" in a_tag["href"] and is_absolute(a_tag["href"]):
                url = a_tag["href"]
                print "absolute",url, counter_ide
                if url in url_pool:
                	continue
                else:
			    	url_pool.append(lufthansa_url) 

            else:
                continue
            for i in all_urls_info:
		
		if get_status_code(url) == 200:
			try:
				html = urllib.urlopen(url).read()
				raw = clean_html(html)
				words = word_tokenize(raw)
				fin_list1 = []
				for word in words:
					if wordnet.synsets(word):
						fin_list1.append(word)
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
	                   		if not r in stop_words:
	                   			data.append(r.lower())
				fourgrams2 = ngrams(data, 4)
				keyword=["Business", "Technology", "Water", "Agriculture", "Sports", "Energy", "People","Entertainment"]
				key_len=[0 for x in range(0, len(keyword))]
				key_div=[1 for x in range(0, len(keyword))]
				count=0
				print "fourgrams"
				for grams in fourgrams2:
					entval =grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3]
					if entval in G:
						if count<=2:
							entity_list.append(str(entval))
							count=count+1
						for x in range(0, len(keyword)):
							if nx.has_path(G,source=keyword[x].lower() ,target=entval):
								if  x==3 or x==4 or x==2:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))

								elif x==5:
                                                                        key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                                        key_div[x]=key_div[x]+1.31

								elif x==6:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
									key_div[x]=key_div[x]+0.8
								else:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
									key_div[x]=key_div[x]+1.01
								

				count=0
				trigrams2 = ngrams(data, 3)
				print "trigrams"
				for grams in trigrams2:
					entval =grams[0]+' '+grams[1]+' '+grams[2]
					if entval in G:
						if count<=3:
							entity_list.append(str(entval))
							count=count+1
						for x in range(0, len(keyword)):
							if nx.has_path(G,source=keyword[x].lower() ,target=entval):
								if x==3 or x==4 or x==2:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
									key_div[x]=key_div[x]+2.01
								elif x==5:
                                                                        key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                                        key_div[x]=key_div[x]+2.01
					
								elif x==6:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
									key_div[x]=key_div[x]+0.8
								else:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
									key_div[x]=key_div[x]+1.01
				

				count=0
				print "bigrams"
				bigrams2 = ngrams(data, 2)
				for grams in bigrams2:
					entval =grams[0]+' '+grams[1]
					if entval in G:
						if count<=4:
							entity_list.append(str(entval))
							count=count+1
						for x in range(0, len(keyword)):
							if nx.has_path(G,source=keyword[x].lower() ,target=entval):
								if x==3 or x==4 or x==2:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
									key_div[x]=key_div[x]+2.01
								elif x==5:
                                                                        key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                                        key_div[x]=key_div[x]+1.21

								elif x==6:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
									key_div[x]=key_div[x]+0.8
								else:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
									key_div[x]=key_div[x]+1.01
				
				count=0
				unigrams2 = ngrams(data, 1)
				print "unigrams"
				for grams in unigrams2:
					entval =grams[0]
					if entval in G:
						if count<=2:
							entity_list.append(str(entval))
							count=count+1
						for x in range(0, len(keyword)):
							if nx.has_path(G,source=keyword[x].lower() ,target=entval):
								if  x==3 or x==4 or x==2:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
									key_div[x]=key_div[x]+2.01
								elif x==6:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
									key_div[x]=key_div[x]+0.8
								elif x==5:
                                                                        key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                                        key_div[x]=key_div[x]+1.25
				
								else:
									key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
									key_div[x]=key_div[x]+1.01
				
				flaglist = [key_len[x]/key_div[x] for x in range(0,len(keyword))]
				print flaglist
				flaglist.sort()
				indexvar=""
				i=0
				flag=True
				while flaglist[i]==0:
					i=i+1
					if i== len(flaglist):
						flag=False
						break
				print entity_list
				if flag:
					for x in range(0,len(keyword)):
						if flaglist[i]==key_len[x]/key_div[x]:
							print '$$$$$$$$$$$ '+ keyword[x] +' ####################'
							if len(indexvar)==0:
								indexvar=keyword[x]
							else:
								indexvar= indexvar+", "+keyword[x]
				else:
					indexvar="Other category"

				if len(raw)>4000:
					raw =raw[0:4000]
            	
				print 'done'
				data = BeautifulSoup(html)
				header = data.find_all("title")
				print "header",str(header[0])
				cleanr = re.compile('<.*?>')
				header = re.sub(cleanr,'',str(header[0]))
				if BeautifulSoup(urllib.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ url), "xml"):
      			  		alexa_score = BeautifulSoup(urllib.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ url), "xml").find("REACH")['RANK']
      				else:
				        alexa_score = 1999999999999
      				import math
				dict1= {"scores":[],"link":url ,"data": raw,"header":header,"votes":1/(1+math.log10(int(alexa_score))), "entity": entity_list, "flagindex":indexvar}
				data = json.dumps(dict1, ensure_ascii=False)
				
				if keyword[0] in indexvar:
					es.index(index='doctechnology', doc_type='people', id=url,body=json.loads(data))
				if keyword[1] in indexvar:
					es.index(index='docbusiness', doc_type='people', id=url,body=json.loads(data))
				if keyword[2] in indexvar:
					es.index(index='docwm', doc_type='people', id=url,body=json.loads(data))
				if keyword[3] in indexvar:
					es.index(index='docagri', doc_type='people', id=url,body=json.loads(data))
				if keyword[4] in indexvar:
					es.index(index='docsports', doc_type='people', id=url,body=json.loads(data))
				if keyword[5] in indexvar:
					es.index(index='docenergy', doc_type='people', id=url,body=json.loads(data))
				if keyword[6] in indexvar:
					es.index(index='docpeople', doc_type='people', id=url,body=json.loads(data))
				if keyword[7] in indexvar:
					es.index(index='docent', doc_type='people', id=url,body=json.loads(data))
				if "Other category" == indexvar:
					es.index(index='docothers', doc_type='people', id=url,body=json.loads(data))
			 
				print "header",header
			except Exception as e1:
				print str(e1),'exception 1'
				continue
			status_dict["url"] = url
            status_dict["status_code"] = get_status_code(url)
            status_dict["timestamp"] = datetime.now()
            status_dict["depth"] = depth + 1
            all_urls_info.append(status_dict)
    return all_urls_info
def driver(url):
#if __name__ == "__main__":
    depth = 2 # suppose 
    all_page_urls = find_internal_urls(url, 2, 2)
    if depth > 1:
        for status_dict in all_page_urls:
            find_internal_urls(status_dict['url'])
def driverwiki(url):
#if __name__ == "__main__":
    depth = 2 # suppose 
    all_page_urls = find_internal_urlswiki(url, 2, 2)
    if depth > 1:
        for status_dict in all_page_urls:
            find_internal_urlswiki(status_dict['url'])



driverwiki("https://en.wikipedia.org/wiki/Category:Companies")
counter_ide=0
driverwiki("https://en.wikipedia.org/wiki/Lists_of_celebrities")   
counter_ide=0
driverwiki("https://en.wikipedia.org/wiki/Lists_of_people") 

counter_ide=0
#driverwiki("https://en.wikipedia.org/wiki/Sport")   
#driver("http://www.farmindustrynews.com")
#driver("http://www.indiaagristat.com")
#driver("http://www.beckag.com")
#driver("https://stackoverflow.com/")
counter_ide=0
driver("https://techcrunch.com/")

#driver("http://www.beckag.com")
#driver("http://www.soygrowers.com")
#driver("http://www.ncga.com")
#driver("http://www.ideglobal.com")
#driver("http://www.farmafrica.org")
#driver("http://www.africanfarming.net"
driverwiki("https://en.wikipedia.org/wiki/Business")    
counter_ide=0
driver("https://techcrunch.com/")
counter_ide=0
driverwiki("https://en.wikipedia.org/wiki/Energy")  

counter_ide=0
driverwiki("https://en.wikipedia.org/wiki/Technology")  
counter_ide=0

#driver("https://stackoverflow.com/")
counter_ide=0
#driverwiki("https://en.wikipedia.org/wiki/Energy")  
counter_ide=0
driver("http://mashable.com/")
counter_ide=0

driverwiki("https://en.wikipedia.org/wiki/Sport")   
counter_ide=0
#driverwiki("https://en.wikipedia.org/wiki/Sport")   

counter_ide=0
driver("http://www.wired.com")
counter_ide=0
driver("https://stackexchange.com/")
counter_ide=0
driver("https://www.wsj.com")
counter_ide=0
counter_ide=0
driver("http://www.thehindu.com/")
driver("http://www.espn.in/")
counter_ide=0
driver("https://www.theverge.com/")
counter_ide=0
driver("http://abc.go.com/")
counter_ide=0
driver("http://in.ign.com/")
counter_ide=0
driverwiki("https://en.wikipedia.org/wiki/Main_Page")   
counter_ide=0
driver("http://www.bbc.com")
 

