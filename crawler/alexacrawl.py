import sys  

reload(sys)  
sys.setdefaultencoding('utf8')
import sys
import requests
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime
#from stack_spider import StackSpider
import urlparse
import time
 
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
import wikipedia
import urllib2
import urllib, re
#from scraper import grabContent
import nltk
import time
import networkx as nx
from nltk.corpus import stopwords
from script2 import scrape
import sys
from multiprocessing import Process 
import time
#from bs4 import BeautifulSoup
G=nx.DiGraph()
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
stop_words = set(stopwords.words('english'))
i=0
'''
with open("categoryAndTheirSubcategories",'r') as edges:

    for line in edges:
        line=line.rstrip()
        if i>1000000:
            break
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
'''
def is_absolute(url):
    return bool(urlparse.urlparse(url).netloc)

def get_soup(link):
    """
    Return the BeautifulSoup object for input link
    """
    request_object = requests.get(link, auth=('user', 'pass'))
    soup = BeautifulSoup(request_object.content)
    return soup

def get_soup_img(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')


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

'''
def find_internal_urlswiki(lufthansa_url, depth=0, max_depth=2):
    all_urls_info = [] 
    status_dict = {}
    soup = get_soup(lufthansa_url)
    a_tags = soup.findAll("a", href=True)

    if depth > max_depth:
        return {}
    else:
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
                        html = urllib2.urlopen(req).read()
                        print "inside"
                        try:
                                page = wikipedia.page(list_all[-1])
                                header = page.title.lower()
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

                                keyword=["Business", "Technology", "Water management", "Agriculture", "Sports", "Energy", "People","Entertainment"]
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
                                                		if x==2 or x==3 or x==4 :
	                                                			key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                			key_div[x]=key_div[x]+2
	                                                	else:
	                                                      		key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                      		key_div[x]=key_div[x]+1

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
                                                		if x==2 or x==3 or x==4 :
	                                                			key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                			key_div[x]=key_div[x]+2
	                                                	else:
	                                                      		key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                      		key_div[x]=key_div[x]+1


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
	                                                	if x==2 or x==3 or x==4 :
	                                                			key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                			key_div[x]=key_div[x]+2
	                                                	else:
	                                                      		key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                      		key_div[x]=key_div[x]+1


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
	                                                	if x==2 or x==3 or x==4 :
	                                                			key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                			key_div[x]=key_div[x]+2
	                                                	else:
	                                                      		key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
	                                                      		key_div[x]=key_div[x]+1
	                                
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

                                #print '$$$$$$$$$$$ '+ keyword[i] +' ####################'
                                if len(content)>4000:
                                    content =content[0:4000]
                                dict1= {"scores":[],"link":url ,"data": content,"header":header,"votes":0.5, "entity": entity_list, "flagindex":indexvar}
                                data = json.dumps(dict1, ensure_ascii=False)
                                es.index(index='docothers', doc_type='people', id=url,body=json.loads(data))
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

'''

json_dict = {}
url_hist=[]
def find_internal_urls(lufthansa_url, depth=0, max_depth=6, Grpindex='docall'):
    
    all_urls_info = []
    status_dict = {}
    soup = get_soup(lufthansa_url)
    a_tags = soup.findAll("a", href=True)
    imgs = soup.findAll("img", src=True)
    url_list = []
    new_dict = {}
    sub_dict = {"domain":lufthansa_url}

    if depth > max_depth :
        return {}
    else:
	counter=0
	
        for a_tag in a_tags:
            if "http" not in a_tag["href"] and "/" in a_tag["href"]:
                url = lufthansa_url + a_tag['href']
                print "relative",url
            elif "http" in a_tag["href"] and is_absolute(a_tag["href"]):
                url = a_tag["href"]
                print "absolute",url
	    else:
                continue
	    if url in url_hist:
		continue	
	    else:
		url_hist.append(url)
	    if lufthansa_url.lower() not in url.lower():
		continue
	    if counter>30:
	    	break 
            if True:
		#print i
		print url	
		if get_status_code(url) == 200:
			counter= counter+1
			url_hist.append(url)
			print '\\\\\\/////////',counter
			try:
                		headers = { 'User-Agent' : 'Googlebot/2.1' }
				req = urllib2.Request(url, None, headers)
                		htmi = urllib2.urlopen(req)
				html = urllib2.urlopen(req).read()
				info = htmi.info()
				date = info.getheader('date')
				print date
				#html = urllib.urlopen(url).read()
				#print html
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
				indexvar="Other category"
				print 'done'
				data = BeautifulSoup(html)
				header = data.find_all("title")
				#print "header",str(header[0])
				try:
					subheader = data.find_all("h1")
					if len(subheader)>0:
						cleanr = re.compile('<.*?>')
		                                header = re.sub(cleanr,'',str(subheader[0]))
					elif len(header)>0:
						cleanr = re.compile('<.*?>')
		                                header = re.sub(cleanr,'',str(header[0]))
					else: 
						header = raw[:30]
                                	print "sub_header",str(header)
				except:
					pass
				title=''
				query= str(header).split()
				query='+'.join(query)

				print query
				imgurl="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
				headerapi={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
				soup = get_soup_img(imgurl, headerapi)
				ActualImages = [] 
				for a in soup.find_all("div",{"class":"rg_meta"}):
	    				link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
	    				ActualImages.append((link,Type))
					
				img = data.find_all("img")
			
				jpg_img = []
				for i in ActualImages:
					#print i
					i=i[0]
					if (i.split('.')[-1] == 'jpg' or i.split('.')[-1] == 'png') and is_absolute(i):
						#print i
						jpg_img.append(i)
						break
				title=''
				header  = header.split()
				for hd in header:
					if hd.lower()=='google' or hd.lower()=='search' or hd =='-':
						pass
					else:
						title =title+' '+hd
				
				if len(jpg_img)>=1:
					imagenew = jpg_img[0]
					print imagenew
				else:
					imagenew = ''
				#with open('links.txt','a') as f:
		                #        f.write(url+'\t'+str(len(url)) +'\n')
				#url_list.append(url+'\t'+str(len(url)))

				if BeautifulSoup(urllib.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ url), "xml")!=None:
                                	
					alexa_score = BeautifulSoup(urllib.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ url), "xml").find("REACH")['RANK']
                       	 	else:
                                	alexa_score = 99999999
                       	 	import math
                        	dict1= {"scores":[],"link":url ,"date":date,"data": raw,"header":title,"votes":1/(1+math.log10(int(alexa_score))), "entity": [], "flagindex":'To be Classified',"sum":'abc', "img":imagenew}
                       		data = json.dumps(dict1, ensure_ascii=False)
                        	es.index(index=Grpindex, doc_type='peopleimg', id=url,body=json.loads(data))

			except Exception as e1:
				print str(e1),'exception 1'
				new_dict = {"url":url}
				continue
            time.sleep(1)
	    status_dict["url"] = url
	    #sub_dict["urls"] = url_list		
            status_dict["status_code"] = get_status_code(url)
            status_dict["timestamp"] = datetime.now()        
       	    status_dict["depth"] = depth + 1
            all_urls_info.append(status_dict)
	    json_dict[lufthansa_url]=sub_dict


    return all_urls_info


if __name__ == "__main__":
    depth = 2 # suppose 
    counter =0
    #total_list=[]
    #subcategory =sys.argv[1]
    #subcategory=subcategory.replace(' ','_')
    #print subcategory

    #list_ax = scrape(n=30, local='category',sub_local=subcategory)
    #total_list.append(list_ax)
    list_1 = ['bbc.com','techcrunch.com','ign.com']
    counterl=0
    if True: 
	
        #Grpindex='docrealestate'
	#Grpindex='docopportunities'
	Grpindex='docothers'

	#print Grpindex
	counterl=counterl+1

  	for i in list_1:
		    if not  is_absolute(i):
    		    	url = 'http://www.'+i
	    	    else:
			url =i
	   	    url_pool=[]
	            url_hist=[]
	   	    try:
	    
	    	    	all_page_urls = find_internal_urls(url, 2, 6, Grpindex)
	    		#count = 0
	    	
			if depth > 1:
				for status_dict in all_page_urls:
		   			try: 
  		        			counter=counter+1
		        			print '@@@@@@@@@@@@@@@@@@@@@@ ',counter
		        			#if counter>2:
		           	       		#	break
		        			if status_dict['url'] in url_pool or url not in status_dict['url']:
		            				continue
		        			else:
		            				url_pool.append(status_dict['url'])
		           	 			find_internal_urls(status_dict['url'],2,6, Grpindex)
		      					#count = count + 1
		    			except:
						print 'error'
	  	    except:
			print 'error2'
