# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.contrib.auth.models import User
from pymongo import MongoClient
import requests
import urllib2

import time,json
import re
import threading
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from crawler.models import RegistrationForm
from elasticsearch import Elasticsearch
#from parser1 import parse
from  crawler4 import driver
from crawler5 import driverwiki
from django.core.cache import cache
import sys
import ahocorasick
from nltk.corpus import stopwords
import os, sys, nltk
from nltk.util import ngrams
import io
import networkx as nx
from searchengine.settings import Q
import math

import urllib, re
#from scraper import grabContent
import nltk
import time
import networkx as nx
from nltk.corpus import stopwords
import sys
import requests
apikey = "7f647aab82f24c068e6509274ad8522c"

#from bs4 import BeautifulSoup
stop_words = set(stopwords.words('english'))

reload(sys)
#from settings import Q
sys.setdefaultencoding('utf-8')
print "Graph formation complete..."


url_pool = [
			#("https://www.theverge.com/tech",3)
			#("https://en.wikipedia.org/wiki/Portal:Contents",5)
			("https://torquemag.io/2014/08/10-wordpress-blogs-well-worth-read/",3)
			,("http://www.rediff.com",3)
			,("http://www.wallstreetsurvivor.com",3)
			,("https://naturalresources.virginia.gov/",3)
			,("http://www.michigan.gov",3)
			,("https://www.nrcan.gc.ca/",3)
			,("https://readwrite.com",3)
			,("http://dnr.maryland.gov/",3)
			,("https://resourcegovernance.org/",3)
			,("https://naturalresources.virginia.gov/",3)
			,("https://naturalresources.wales/?lang=en",3)
			,("http://www.bbc.com/news/business",3)
			,("https://www.theverge.com/tech",3)
			,("http://www.moneycontrol.com",3)
			,("http://www.gizmodo.in",3)
			,("https://www.engadget.com",3)		
			,("http://dnr.maryland.gov/",3),
			("https://resourcegovernance.org/",3),
			("https://naturalresources.virginia.gov/",3),
			("https://naturalresources.wales/?lang=en",3)
			,("http://www.businessinsider.com",3)
			,("http://economictimes.com",3)
			,("https://www.forbes.com",3)
			,("http://www.huffingtonpost.com",3)
			,("http://www.berkshirehathaway.com",3)
			,("https://www.walmart.com",3)
			#,("http://www.rediff.com",3)
			#,("http://www.wallstreetsurvivor.com",3)
			#,("http://www.renewableenergyworld.com",3)
			,("https://www.vccircle.com",3)
			
			,("https://www.theguardian.com/environment/energy",3)
			,("https://slashdot.org",3)
			]

client = MongoClient()
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
db = client.test
collection = db.docs
import urlparse

def is_absolute(url):
    return bool(urlparse.urlparse(url).netloc)



class AllThreads(threading.Thread):
	
	print('crawl')
	def __init__(self,url,period):
		period = period
		threading.Thread.__init__(self)
		self.url = url
	def crawl(self,url_pool,period):
		print "crawwling..."
		if(urllib2.urlopen(self.url)):
			page = urllib2.urlopen(self.url)
			soup = BeautifulSoup(page)
			all_links = soup.find_all("a") 
			for link in all_links:
				new_link = link.get("href")
				if new_link not in zip(*url_pool):
					if not is_absolute(new_link):
						try:
							if "/goo.gl" in new_link or"facebook" in new_link or "twitter" in new_link:
								return
							else:
								url_pool.append((self.url + str(new_link),1))
							
							#id = self.url
							#print id
							#id = datetime.now()
							if "/goo.gl" in new_link or "facebook" in new_link or "twitter" in new_link:
								return
							else:

								print '########if print'
								#print self.url 
								print 'new link ' +str(new_link)
								
								
								print "going to parse"
								try:
									text,header,scorelist,scores, flagindex, ent_list = parse(str(new_link))
									print "Success"
									ok=True
								except Exception as e:
									text=""
									header=""
									scorelist=[]
									scores=0
									flagindex=1
									ent_list=[]
									print "Fail"
									ok = False

								 
								id = header
								dict1 = {"scores":scorelist,"link":self.url + str(new_link),"data":text,"header":header,"votes":scores, "entity":ent_list, "flagindex":flagindex}
								data = json.dumps(dict1, ensure_ascii=False)
								if ok:
									print "Inserting "
									#print data
									#es.index(index='sw', doc_type='people', id=id,body=json.loads(data))
									if not header=="none":
										if(flagindex=="Technology"):
											es.index(index='doctechnology', doc_type='people', id=id,body=json.loads(data))
										elif(flagindex=="Business"):
											es.index(index='docbusiness', doc_type='people', id=id,body=json.loads(data))
										elif(flagindex=="Other Category"):
											es.index(index='docothers', doc_type='people', id=id,body=json.loads(data))
										else:
											es.index(index='docenergy', doc_type='people', id=id,body=json.loads(data))
								#with open("doc.json", "w") as f:
	    								#json.dump(list(collection.find()), f)
						except urllib2.HTTPError as e:
    							error_message = e.read()
    							print "error part1",error_message

					else:
						try:
							if "/goo.gl" in new_link or "facebook" in new_link or "twitter" in new_link:
								pass
							else:
								url_pool.append((str(new_link),1))
							id = datetime.now()
							ok=True
							print '########else print'
							#print self.url 
							print str(new_link)
								
							print str(new_link)
							if "/goo.gl" in new_link or "facebook" in new_link or "twitter" in new_link:
								pass
							else:
								try:
									text,header,scorelist,scores, flagindex, ent_list = parse(str(new_link))
									print "Success"
									ok=True
								except Exception as e:
									print "fail"
									text=""
									header=""
									scorelist=[]
									scores=0
									flagindex=1
									ent_list=[]
									ok=False
									#print data
								#print header
								#print scorelist
								#print scores
								

								
								dict1 = {"scores":scorelist,"link":self.url + str(new_link),"data":text,"header":header,"votes":scores, "entity":ent_list, "flagindex":flagindex}
								data = json.dumps(dict1, ensure_ascii=False)
								if ok:
									print "Inserting"

									#print data
									#es.index(index='sw', doc_type='people', id=id,body=json.loads(data))
									if not header=="none":
										if flagindex=="Technology":
											es.index(index='doctechnology', doc_type='people', id=id,body=json.loads(data))
										elif flagindex=="Business":
											es.index(index='docbusiness', doc_type='people', id=id,body=json.loads(data))
										elif flagindex=="Other Category":
											es.index(index='docothers', doc_type='people', id=id,body=json.loads(data))	
										else:
											es.index(index='docenergy', doc_type='people', id=id,body=json.loads(data))
							
						except urllib2.HTTPError as e:
							error_message = e.read()
    						#print "error part2",error_message
		 	time.sleep(period)
		 	self.crawl(url_pool,period)



def get_the_links(url_pool):
	k = 0
	for i in url_pool:
		if i[0] is not None:
			background = AllThreads(i[0],i[1])
			background.start()
			background.crawl(url_pool,i[1])
			background.join()
			k = k + 1
		else:
			break
	return url_pool
def crawldata():
	global url_pool
	print "Crawling"
	url_pool = get_the_links(url_pool)



@csrf_exempt
def crawl_page(request):
	global url_pool
	#for index in es.indices.get('*'):
  	#	print index
	url_pool = get_the_links(url_pool)
	return HttpResponse("Exhausted links.")

def start(request):
	return render(
        request,
        'crawler/startindex.html',
        {
            'title':'Demo Content',
            'year': datetime.now().year,
        }
    )

def newcrawlwired(request):
	print 'here'
	driver("http://www.wired.com")
def newcrawlmash(request):
	print 'here'
	driver("http://mashable.com/")

def newcrawltc(request):
	print 'here'
	driver("https://techcrunch.com/")
def newcrawlso(request):
	print 'here'
	driver("https://stackoverflow.com/")
def newcrawlse(request):
	print 'here'
	driver("https://stackexchange.com/")
def newcrawlQ(request):
	print 'here'
	driver("https://www.quora.com/How-much-have-you-invested-in-Bitcoin")
def newcrawlwsj(request):
	print 'here'
	driver("https://www.wsj.com/india")
def newcrawlespn(request):
	print 'here'
	driver("http://www.espn.in/")
def newcrawltv(request):
	print 'here'
	driver("https://www.theverge.com/")
def newcrawlabc(request):
	print 'here'
	driver("http://abc.go.com/")
def newcrawlign(request):
	print 'here'
	driver("http://in.ign.com/")
def newcrawlhindu(request):
	print 'here'
	driver("http://www.thehindu.com/")
def newcrawlppl(request):
	print 'here'
	driver("http://www.biographyonline.net/people/famous-100.html")

def newwikicrawlagri(request):
	print 'wiki crawl'
	driverwiki("https://en.wikipedia.org/wiki/Agriculture")	
def newwikicrawlbiz(request):
	print 'wiki crawl'
	driverwiki("https://en.wikipedia.org/wiki/Business")	
def newwikicrawltech(request):
	print 'wiki crawl'
	driverwiki("https://en.wikipedia.org/wiki/Technology")	
def newwikicrawlsports(request):
	print 'wiki crawl'
	driverwiki("https://en.wikipedia.org/wiki/Sport")	
def newwikicrawlppl(request):
	print 'wiki crawl'
	driverwiki("https://en.wikipedia.org/wiki/Sport")	
def newwikicrawlenergy(request):
	print 'wiki crawl'
	driverwiki("https://en.wikipedia.org/wiki/Energy")	
def newwikicrawlwm(request):
	print 'wiki crawl'
	driverwiki("https://en.wikipedia.org/wiki/Water_resource_management")	
def newwikicrawl(request):
	print 'wiki crawl'
	driverwiki("https://en.wikipedia.org/wiki/Main_Page")	

def signup(request):
	if request.method == 'POST':
	    form = RegistrationForm(request.POST)
	    if form.is_valid():
	        user = User.objects.create_user(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],email=form.cleaned_data['email'])
	        return HttpResponseRedirect('/login')
	    else:
	    	variables = RequestContext(request, {
				'form': form,
				'title':'Demo Content',
				'year': datetime.now().year,
	    	})
	    	return render_to_response('crawler/signup.html',variables)
	form = RegistrationForm()
	variables = RequestContext(request, {
		    'form': form,
	        'title':'Demo Content',
	        'year': datetime.now().year,
	    })
	return render_to_response('crawler/signup.html',variables)

def login(request):
	return render(
        request,
        'crawler/login.html',
        {
            'title':'Demo Content',
            'year': datetime.now().year,
        }
    )

def configuration(request):
	return render(
	        request,
	        'crawler/config.html'
	    )	

def news(request):
	if 1==1:
                template = loader.get_template('crawler/news.html')
                response = requests.get('https://newsapi.org/v1/articles?source=business-insider&sortBy=top&apiKey='+ apikey )
                response = response.json()
                #print response
                variables = Context({ 'user': request.user ,
                    'title':'Demo Content',
                    'year': datetime.now().year,
                    'feed': response
                })
                output = template.render(variables)
		return HttpResponse(output)
def home(request):
	
	if not request.GET.get('query'):
		template = loader.get_template('crawler/home.html')
		response = requests.get('https://newsapi.org/v1/articles?source=business-insider&sortBy=top&apiKey='+ apikey )
		response = response.json()
		#print response
		variables = Context({ 'user': request.user ,
	            'title':'Demo Content',
	            'year': datetime.now().year,
	            'feed': response
	        })
		output = template.render(variables)
	else :
		#print "poppy"
		x = str(request.GET.get('query')).lower() 
		x = x.split(' ')
		
		stop_words = set(stopwords.words('english'))
		entitity_querry=[]
		embedingQueryMatrix=[]
		data =[]
		query_string =''
		for r in x:
			if not r in stop_words:
				data.append(r)
				query_string=query_string+' '+r
		query_string = 	query_string[0:]

		bigrams2 = ngrams(data, 5)
	  	#print "fivegrams"
	  	for grams in bigrams2:
	  		if Q.get(str(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3]+' '+grams[4]),"not_exsist")!="not_exsist":
	  			#print Q.get(str(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3]+' '+grams[4]),"not_exsist")
	  			entitity_querry.append(str(Q.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3]+' '+grams[4])[0]))
	      #list(Q.keys(grams[0]+' '+grams[1]+' '+grams[2]))
	  


	  	bigrams2 = ngrams(data, 4)
	  	print "fourgrams"
	  	for grams in bigrams2:
	  		if Q.get(str(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3]),"not_exsist")!="not_exsist":
	  			#print Q.get(str(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3]),"not_exsist")
	  			entitity_querry.append(str(Q.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3])[0]))
	      #list(Q.keys(grams[0]+' '+grams[1]+' '+grams[2]))
	  

	  	bigrams2 = ngrams(data, 3)
	  	print "trigrams"
	  	for grams in bigrams2:
	  		if Q.get(str(grams[0]+' '+grams[1]+' '+grams[2]),"not_exsist")!="not_exsist":
	  			#print Q.get(str(grams[0]+' '+grams[1]+' '+grams[2]),"not_exsist")
	  			entitity_querry.append(str(Q.get(str(grams[0]+' '+grams[1]+' '+grams[2]))[0]))
	  
	  	bigrams2 = ngrams(data, 2)
	  	print "bigrams"
	  	for grams in bigrams2:
	  		if Q.get(str(grams[0]+' '+grams[1]),"not_exsist")!="not_exsist":
	  	 		#print Q.get(str(grams[0]+' '+grams[1]),"not_exsist")
	  	 		entitity_querry.append(str(Q.get(str(grams[0]+' '+grams[1]))[0]))
	   
	  	bigrams2 = ngrams(data, 1)
	  	print "unigrams"
	  	for grams in bigrams2:
	  		if Q.get(str(grams[0]),"not_exsist")!="not_exsist":
	  			#print Q.get(str(grams[0]),"not_exsist")
	  			entitity_querry.append(str(Q.get(str(grams[0]))[0]))
	  	entitity_querry=list(set(entitity_querry))
		print entitity_querry
		ent_int_list=[]
		for val in entitity_querry:
			#test here
			#print val
			ent_int_list.append(int(val))

		#print '********#####********* '+ str(sz_query)
		myquery ={
				  "query": {
				    "function_score": { 
					      "query": { 
					        "multi_match": 
					        {
					          "query": request.GET.get('query'),
					          "fields": [ "data", "header^3" ]
					        # "fuzziness" : "AUTO",
                    		  		#"prefix_length" : 5 
					        }  
				      	   },
				      	    "functions": [{
                                "script_score": {
                                   # "script": "return _score + doc['votes'].value;"  # this is where scoring occurs
                                "script" : 
								{ "params": 
									{
									  "a": ent_int_list,
									  #"sz": sz_query,
									  "x": 0.33,
									  "y": 0.8,
									  "z": 0.33
									}, #( (_score*0.33)/6 + (total*0.33)/sz + *0.33doc['votes'].value )
									"inline": "if(doc['votes'].value<1){return (_score*params.x)/4  + params.z*doc['votes'].value;}else{return (_score*params.x)/4  + 0.234;}" 
								}

                                }

                            }],
                             "score_mode": "sum"
				      	     
				 			
							}
						}
				}
				 
		#result = es.search(index="sw", body={"query": {"match": {'data': request.GET.get('query')}}})
		if request.GET.get('theme')=="all":
			result = es.search(index="_all", body=myquery)
		if request.GET.get('theme')=="tech":
			result = es.search(index="docbusiness", body=myquery)
		if request.GET.get('theme')=="business":
			result = es.search(index="doctechnology", body=myquery)
		if request.GET.get('theme')=="energy":
			result = es.search(index="docenergy", body=myquery)
		if request.GET.get('theme')=="agri":
                        result = es.search(index="docagri", body=myquery)
		if request.GET.get('theme')=="water":
                        result = es.search(index="docwm", body=myquery)
		if request.GET.get('theme')=="people":
                        result = es.search(index="docpeople", body=myquery)
		if request.GET.get('theme')=="ent":
                        result = es.search(index="docent", body=myquery)		
		#print result
		def MakeInt(elem):
			return int(elem)

		#entitity_querry.sort(key = MakeInt)
		j=0
		k=0
		
		res=[]
		summary=[]
		resdup=['asas','asa']
		for rows in result['hits']['hits']:
			if rows["_source"]["header"] in resdup:
				continue
			resdup.append(rows["_source"]["header"])
			f_sum={}
			f_res={}
			f_res["link"]=rows["_source"]["link"]
			f_res["theme"]=rows["_source"]["flagindex"]
			f_res["entity"]= rows["_source"]["entity"][0:8] 
			if len(rows["_source"]["data"]) >= 500:
				f_res["data"]=rows["_source"]["data"][:500]+"..."
				f_res["header"]= rows["_source"]["header"]
				f_res["scores"]= rows["_source"]["scores"]
				f_res["votes"]=  rows["_source"]["votes"]
			else:
				f_res["data"]=rows["_source"]["data"]
				f_res["header"]= rows["_source"]["header"]
				f_res["scores"]= rows["_source"]["scores"]
				f_res["votes"]=  rows["_source"]["votes"]
			try:
				if rows["_source"]["sum"] :
					#print rows["_source"]["img"], rows["_source"]["sum"]
					#if True:#rows["_source"]["img"][-1]=='p':
					f_sum["img"]=rows["_source"]["img"]
					if len(rows["_source"]["sum"])>180:
						f_sum["text"]=rows["_source"]["sum"][:180]+'...'		
					else:
						f_sum["text"]=rows["_source"]["sum"]	
					f_sum["url"]= rows["_source"]["link"]
					#print rows["_source"]["img"], f_sum["img"], f_sum["text"],rows["_source"]["sum"]
					#print '$$$$$$',f_sum
					summary.append(f_sum)
			except:
				print 'pass'
			res.append(f_res)
			#print f_res['votes']
		if len(res)==0:
			f_res={}
			f_res["link"]=""
			f_res["data"]="No results were found for "+request.GET.get('query')+""

			res.append(f_res)
		template = loader.get_template('crawler/search.html')
		if len(summary)>5:
			summary=summary[:5]
		variables = Context({ 'user': request.user ,
	            'title':'Demo Content',
	            'year': datetime.now().year,
	            'results' : res,
		    'summary':summary
	        })
		output = template.render(variables)
	return HttpResponse(output)

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login')



