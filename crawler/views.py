# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.html import escape
from datetime import datetime
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.contrib.auth.models import User
from pymongo import MongoClient
import requests
import urllib2
from collections import OrderedDict
import time,json
import re
import threading
from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
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
from searchengine.settings import G
import math
#from googletrans import Translator
#translator = Translator()
from textblob import TextBlob
import urllib, re

#from scraper import grabContent

import nltk

from search_crawler import duck_lets_go

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
supercounter = 0

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

def config(request):
        configlist=db.configlist.find()
        configsubcategory=db.configsubcat.find()
        themes_keywords=db.UserKeywords.find({'user':str(request.user)},{'_id':False,'user':False})
        categories={}
        categoryimg={}
        subcategoryimg={}
        newcategories=OrderedDict()
        
        #subsubcatimg={}
        with open("crawler/categoryimglinks2","r") as f1,open("crawler/subcatimglinks2","r") as f2:
            for line in f1:
                line=line.split(" : ")
                categoryimg[line[0].strip()]=line[1].strip()
            for line in f2:
                line=line.split(" : ")
                catsub=line[0].split("__")
                subcategoryimg.setdefault(catsub[0].strip(),{})
                subcategoryimg[catsub[0].strip()][catsub[1].strip()]=line[1].strip()
                
        for i in configlist:
            categories[i["Category"]]={}
            for j in i["Subcategories"]:
                categories[i["Category"]][j]=[]
        
        for i in configsubcategory:
            if i["Category"] in categories and i["Subcategory"] in categories[i["Category"]]:
                categories[i["Category"]][i["Subcategory"]]=i["Subsubcategories"]
        
        for i in themes_keywords:
            if i['theme'] in categories:
                for j in i['keywords']:
                    categories[i['theme']][j]=[]
                    if i['theme'] not in subcategoryimg:
                        subcategoryimg.setdefault(i['theme'],{})
                    subcategoryimg[i['theme']][j]="https://incomebully.com/wp-content/uploads/2015/05/keyword-research.png"
        
        options=OrderedDict()
        themes_keywords=db.UserKeywords.find({'user':str(request.user)},{'_id':False,'user':False})
        coll=db.config
        try:
            cur=coll.find_one({"user":str(request.user)},{'choice':1,'_id':False})
            for key,value in cur.items():
                print key,value
	    	if key=="choice":        
                    choice=value
        except:
                choice={"Mining and Drilling":[],"Environment":["Waste Management"],"Agriculture and Forestry":[],"Opportunities":["News and Media"],"Energy":["Oil and Gas"],"Business Services":[],"Information Technology":["Investing"]}

        for i in themes_keywords:
            if i['theme'] in choice:
                for j in i['keywords']:
                    if i['theme'] not in subcategoryimg:
                        subcategoryimg.setdefault(i['theme'],{})
                    subcategoryimg[i['theme']][j]="https://incomebully.com/wp-content/uploads/2015/05/keyword-research.png" 
                
        for i in choice:
            options[i]=categoryimg[i]
            for j in choice[i]:
                options[j+'/'+i]=subcategoryimg[i][j]
        
        
        for i in sorted(categories):
            newcategories.setdefault(i,categories[i])
	return render(
        request,
        'crawler/config.html',
        {
            'title':'Demo Content',
            'year': datetime.now().year,
            'categories':newcategories,
            'categoryimg':categoryimg,
            'subcategoryimg':subcategoryimg,
            'options':options,
            #'subsubcatimg':subsubcatimg,
        }
    )

def add_config(request):
	if request.user=="AnonymousUser":
		return HttpResponseRedirect('/login')
	print request.user
	choices=OrderedDict()
	priorities=request.POST.get("priorities",1)
	priorities=json.loads(priorities,object_pairs_hook=OrderedDict)
	print priorities
        category=[]
        """choices.setdefault("Mining and Drilling",[])
	choices.setdefault("Environment",["Waste Management"])
	choices.setdefault("Agriculture and Forestry",[])
	choices.setdefault("Opportunities",["News and Media"])
	choices.setdefault("Business Services",[])
        choices.setdefault("Energy",["Oil and Gas"])
        choices.setdefault("Information Technology",["Investing"])"""
	for key in request.POST:
	    if "cat_" in str(key):
	       key=request.POST.get(key,"")
	       key=key.split("__")
	       if len(key)>1:
	            if key[0] not in category:
        	       category.append(key[0])
       	            choices.setdefault(key[0],[])
       	            choices[key[0]].append(key[1])
	#print choices
        for i in category:
            choices[i].sort(key=priorities[i].get)
        print choices
        priortized=sorted(category,key=priorities.keys().index)
        print priortized
        prioritizedchoices=OrderedDict()
        for key in priortized:
            prioritizedchoices.setdefault(key,choices[key])
        choices=prioritizedchoices
	db.config.update_one({"user":str(request.user)},{"$set":{"user":str(request.user),"choice":choices}}, upsert=True)
	#import news_personalization
	return HttpResponseRedirect('/home')

def is_absolute(url):
    return bool(urlparse.urlparse(url).netloc)



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
import os
'''
def news2(request,home=False):
	preffered_list = ['forbes.com','bussinessinsider.com','techcrunch.com','dailymail.com','espn.com','renewable energy news']
	news_list = []
	for i in preffered_list:
		news_list1 = []
		new_list = duck_lets_go2(i)
		for art in new_list:
			new_dict = {"article":art}
			new_list1.append(new_dict)
		news_list.extend(new_list1)  
        if 1==1:
                import requests
                if request.GET.get('query'):
                   if request.GET.get('page'):
                       try:
                           page=int(request.GET.get('page'))
                       except:
                           page=1
                   else:
                       page=1
		
'''
def news(request,home=False):
	if 1==1:
	        import requests
	        if request.GET.get('query'):
	           if request.GET.get('page'):
	               try:
	                   page=int(request.GET.get('page'))
	               except:
	                   page=1
	           else:
	               page=1

	           jsondata={}
	           query=request.GET.get('query')
		   print query
		   temp = query.split('/')[0]
                   print temp
                   res=duck_lets_go(temp+" news")[3:]
                   maxpage=len(res)/30
                   jsondata.update({'articles':res,'page':page,'maxpage':maxpage})
	           return HttpResponse(json.dumps(jsondata),content_type="application/json")
                   """if len(temp)>1:
                   	if temp[0].replace(" ","").replace("_","").lower() in ["mininganddrilling","oilandgasccrawl","wastemanagement","agriculture","agricultureandforestry","opportunities","energy","environment","materials","newsandmedia","businessservices","investing","oilandgas","miningnewsandmedia","china","japan","korea"]:
                                docstring ='doc'+temp[0].replace(" ","").replace("_","").lower()
                        elif temp[1].replace(" ","").replace("_","").lower() in ["mininganddrilling","oilandgasccrawl","wastemanagement","agriculture","agricultureandforestry","opportunities","energy","environment","materials","newsandmedia","businessservices","investing","oilandgas","miningnewsandmedia"]:
                                docstring ='doc'+temp[1].replace(" ","").replace("_","").lower()
                        else:
                                docstring='doc'+temp[1].replace(' ','_').lower()+temp[0].replace(' ','_').lower()
				try:
					print docstring
					url ="http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"
					r = requests.get(url)
					data = r.json()
					data = data['hits']['hits']
				except:
					try:
						docstring='doc'+temp[1].replace(' ','_').lower()
						print docstring
						url ="http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"
                                        	r = requests.get(url)
                                        	data = r.json()
                                        	data = data['hits']['hits']
					except:
						try:
							docstring='doc'+str(request.user)+'home'
							print docstring
	                                                url ="http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"
        	                                        r = requests.get(url)
                	                                data = r.json()
                        	                        data = data['hits']['hits']
						except:
				       			docstring ='dochome'
		   else:

                        if temp[0].replace(" ","").replace("_","").lower() in ["mininganddrilling","oilandgasccrawl","wastemanagement","agriculture","agricultureandforestry","opportunities","energy","environment","materials","newsandmedia","businessservices","investing","oilandgas","miningnewsandmedia"]:
                                docstring ='doc'+temp[0].replace(" ","").replace("_","").lower()
                        else:
				try:
                                	docstring='doc'+str(request.user)+'home'
					print docstring
                                        url ="http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"
                                        r = requests.get(url)
                                        data = r.json()
                                        data = data['hits']['hits']
                                except:
                                        docstring ='dochome'
                               

                   URL = "http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"

		   '''
	           if query.replace(" ","").replace("_","").lower() in ["mininganddrilling","oilandgasccrawl","wastemanagement","agriculture","agricultureandforestry","opportunities","energy","environment","materials","newsandmedia","businessservices","investing","oilandgas","miningnewsandmedia"]:
	               URL = "http://localhost:9200/doc"+query.replace(" ","").replace("_","").lower()+"/_search?size=1000&q=*:*"
	           else:
	               URL = "http://localhost:9200/docai/_search?size=1000&q=*:*"  
	           '''
		   print 'reached'
		   r = requests.get(url = URL)
		   print 'recg2'
                   # extracting data in json format
                   data = r.json()
                   jsondata={}
                   jlist=[]
		   slist=[]
                   data = data['hits']['hits']
                   maxpage=len(data)/30
                   if maxpage<(page-1):
                       page=1
                   print page
                   histlist=[] 
		   '''for rows in data[30*(page-1):30*page]:
        	   	if rows['_source']['header'] not in histlist: # or 'secondlife' not in rows['_source']['link']:
	               		jlist.append(rows['_source'])
			#histlist.append(str(rows['_source']['header']))
		   '''#histlist.clear()
		   print histlist
		   cursor = db.config.find()
                   def getkey(val):

			user_id=0
                        for doc in cursor:
                                if str(request.user)==doc['user']:
	                                break
                        user_id =user_id+1

                          ###print val['scores'][1]
                       	if len(val['scores'])>user_id:
                        	return float(val['scores'][user_id])+float(val['votes'])*0.3
                        else:		
                        	return 0.209+float(val['votes'])*0.3
		   print 'dsd'
		   counter=-600
                   for row in data:
			if row['_source']['header'] not in histlist and 'secondlife' not in row['_source']['link'] and 'client' not in row['_source']['header'].lower():
		   		if len(row['_source']['data'])>600:
                                #while row['_source']['data'][counter]!=' ':    
                                	if row['_source']['data'][counter]!=' ':
                                	        counter=counter+1
                                	if row['_source']['data'][counter]!=' ':
                                	        counter=counter+1
                               		if row['_source']['data'][counter]!=' ':
                              	        	counter=counter+1
                                	if row['_source']['data'][counter]!=' ':
                                	        counter=counter+1
                                	if row['_source']['data'][counter]!=' ':
                                	        counter=counter+1
                                	if row['_source']['data'][counter]!=' ':
                                	        counter=counter+1

                                row['_source']['data'] =  row['_source']['data'][counter:]

				slist.append(row['_source']) 
				histlist.append(str(row['_source']['header']))
		   #print slist
		   print '*****Rec4**'
		   slist.sort(key =getkey, reverse=True) 
		   print '*****Rec5**'
		   ourlist =slist[30*(page-1):30*page] #[-51:]
                   #ourlist.sort(key =getkey, reverse=True)
		   print '*****Rec6**'
                   jsondata.update({'articles':ourlist,'page':page,'maxpage':maxpage})
	           return HttpResponse(json.dumps(jsondata),content_type="application/json")"""
	           
                if request.GET.get('page'):
                    try:
                        page=int(request.GET.get('page'))
                    except:
                        page=1
                else:
                    page=1
                if(not home):
                    template = loader.get_template('crawler/news.html')
                else:
                    template = loader.get_template('crawler/home.html')
                #response = requests.get('https://newsapi.org/v1/articles?source=business-insider&sortBy=top&apiKey='+ apikey )
                #response = response.json()
                #print response
                coll=db.config
                try:
                    cur=coll.find_one({"user":str(request.user)},{'choice':1,'_id':False})
                    for key,value in cur.items():
                        if key=="choice":        
                            choice=value
                except:
                    choice={"Mining and Drilling":[],"Environment":["Waste Management"],"Agriculture and Forestry":[],"Opportunities":["News and Media"],"Energy":["Oil and Gas"],"Business Services":[],"Information Technology":["Investing"]}

                options=OrderedDict()
                categoryimg={}
                subcategoryimg={}
                selectedcat=""
                #response = requests.get('https://newsapi.org/v1/articles?source=business-insider&sortBy=top&apiKey='+ apikey )
                #response = response.json()
                #print response
                coll=db.config
                try:
                    cur=coll.find_one({"user":str(request.user)},{'choice':1,'_id':False})
                    for key,value in cur.items():
                        print key,value
		    	if key=="choice":        
                            choice=value
                except:
                    choice={"Mining and Drilling":[],"Environment":["Waste Management"],"Agriculture and Forestry":[],"Opportunities":["News and Media"],"Energy":["Oil and Gas"],"Business Services":[],"Information Technology":["Investing"]}

                options=OrderedDict()
                categoryimg={}
                subcategoryimg={}
                selectedcat=""
                themes_keywords=db.UserKeywords.find({'user':str(request.user)},{'_id':False,'user':False})
                for key,value in choice.items():
                    if len(value)>0:
                        selectedcat=key+value[0]
                    else:
                        selectedcat=key
                    break
                
                with open("crawler/categoryimglinks2") as f1,open("crawler/subcatimglinks2") as f2:
                    for line in f1:
                        line=line.split(" : ")
                        if line[0].strip() in choice:
                            categoryimg[line[0].strip()]=line[1].strip()
                    for line in f2:
                        line=line.split(" : ")
                        catsub=line[0].split("__")
                        if catsub[0].strip() in choice:
                            subcategoryimg.setdefault(catsub[0].strip(),{})
                            if catsub[1].strip() in choice[catsub[0].strip()]:
                                subcategoryimg[catsub[0].strip()][catsub[1].strip()]=line[1].strip()
                
                for i in themes_keywords:
                    if i['theme'] in choice:
                        for j in i['keywords']:
                            if i['theme'] not in subcategoryimg:
                                subcategoryimg.setdefault(i['theme'],{})
                            subcategoryimg[i['theme']][j]="https://incomebully.com/wp-content/uploads/2015/05/keyword-research.png" 
                
                for i in choice:
                    options[i]=categoryimg[i]
                    for j in choice[i]:
                        options[j+'/'+i]=subcategoryimg[i][j]
			
                #print selectedcat, options
		# api-endpoint
		for key in options:
		    temp=key
		    print key
		    break
		temp = temp.split('/')
		"""if len(temp)>1:
			if temp[0].replace(" ","").replace("_","").lower() in ["mininganddrilling","oilandgasccrawl","wastemanagement","agriculture","agricultureandforestry","opportunities","energy","environment","materials","newsandmedia","businessservices","investing","oilandgas","miningnewsandmedia","china","korea","japan"]:
				docstring ='doc'+temp[0].replace(" ","").replace("_","").lower()
			elif temp[1].replace(" ","").replace("_","").lower() in ["mininganddrilling","oilandgasccrawl","wastemanagement","agriculture","agricultureandforestry","opportunities","energy","environment","materials","newsandmedia","businessservices","investing","oilandgas","miningnewsandmedia"]:
                                docstring ='doc'+temp[1].replace(" ","").replace("_","").lower()
			else:
				docstring='doc'+temp[1].replace(' ','').lower()+temp[0].replace(' ','').lower()
				try:
					url ="http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"
					r = requests.get(url)
					data = r.json()
					data = data['hits']['hits']
				except:
				        docstring ='doc'+str(request.user)+'home'
					try: 
						url ="http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"
                                        	r = requests.get(url)
                                        	data = r.json()
                                        	data = data['hits']['hits']
					except:
						docstring = 'dochome'

		else:

                        if temp[0].replace(" ","").replace("_","").lower() in ["mininganddrilling","oilandgasccrawl","wastemanagement","agriculture","agricultureandforestry","opportunities","energy","environment","materials","newsandmedia","businessservices","investing","oilandgas","miningnewsandmedia"]:
                                docstring ='doc'+temp[0].replace(" ","").replace("_","").lower()
                        else:
                                 docstring ='doc'+str(request.user)+'home'
                                 try:
                                 	url ="http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"
                                        r = requests.get(url)
                                        data = r.json()
                                        data = data['hits']['hits']
                                 except:
                                 	docstring = 'dochome'

		
		URL = "http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"						     
		if home:
		    #URL = "http://localhost:9200/dochome/_search?size=1000&q=*:*"  
		    docstring ='doc'+str(request.user)+'home'
                    try:
                    	url ="http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"
                        r = requests.get(url)
                        data = r.json()
                        data = data['hits']['hits']
                    except:
                        docstring = 'dochome'
		URL = "http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"
		if request.GET.get('theme'):
		    selectedcat=request.GET.get('theme')
		    myvar=False
		    for key,value in choice.items():
		        if selectedcat==key:
		            myvar=True
		            break
                        else:
                            if selectedcat in value:
                                myvar=True
                                break
                            for i in value:
                                if selectedcat==i+"/"+key:
                                    myvar=True
                                    break
                    if not myvar:
                        docstring='docnewsandmedia'
                        print "here"
                        selectedcat='News and Media'
                    else:
                        print "here1"
                        temp = selectedcat.split('/')
                        if len(temp)>1:
                            if temp[0].replace(" ","").replace("_","").lower() in ["mininganddrilling","oilandgasccrawl","wastemanagement","agriculture","agricultureandforestry","opportunities","energy","environment","materials","newsandmedia","businessservices","investing","oilandgas","miningnewsandmedia","china","korea","japan"]:
                                docstring ='doc'+temp[0].replace(" ","").replace("_","").lower()
                            elif temp[1].replace(" ","").replace("_","").lower() in ["mininganddrilling","oilandgasccrawl","wastemanagement","agriculture","agricultureandforestry","opportunities","energy","environment","materials","newsandmedia","businessservices","investing","oilandgas","miningnewsandmedia"]:
                                docstring ='doc'+temp[1].replace(" ","").replace("_","").lower()
                            else:
				docstring='doc'+temp[1].replace(' ','').lower()+temp[0].replace(' ','').lower()
				try:
					url ="http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"
					r = requests.get(url)
					data = r.json()
					data = data['hits']['hits']
				except:
				        docstring ='doc'+str(request.user)+'home'
                                        try:
                                                url ="http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"
                                                r = requests.get(url)
                                                data = r.json()
                                                data = data['hits']['hits']
                                        except:
                                                docstring = 'dochome'

			else:
			    if temp[0].replace(" ","").replace("_","").lower() in ["mininganddrilling","oilandgasccrawl","wastemanagement","agriculture","agricultureandforestry","opportunities","energy","environment","materials","newsandmedia","businessservices","investing","oilandgas","miningnewsandmedia"]:
			        docstring ='doc'+temp[0].replace(" ","").replace("_","").lower()
			    else:
                            	 docstring ='doc'+str(request.user)+'home'
                                 try:
                                 	url ="http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"
                                        r = requests.get(url)
                                        data = r.json()
                                        data = data['hits']['hits']
                                 except:
                                 	docstring = 'dochome'

                                
                    URL = "http://localhost:9200/"+docstring+"/_search?size=1000&q=*:*"

		# sending get request and saving the response as response object
		r = requests.get(url = URL)

		# extracting data in json format
		data = r.json()
		jsondata={}
		jlist=[]
		data = data['hits']['hits']
		maxpage=len(data)/30
		if maxpage<(page-1):
		    page=1  

		histlist=[] 
                #for rows in data[30*(page-1):30*page]:
                #	if rows['_source']['header'] not in histlist :#or'secondlife' not in rows['_source']['link']:
                #        	jlist.append(rows['_source'])
                #histlist.append(str(rows['_source']['header']))
                #histlist.clear()
		print histlist
		cursor = db.config.find()
		def getkey(val):
			#print val['scores'][1]
			user_id=0
		        for doc in cursor:
                		if str(request.user)==doc['user']:
	                        	break
               	 	user_id =user_id+1

			if len(val['scores'])>user_id:
				return float(val['scores'][user_id])#+float(val['votes'])
			else:		
				return 0.101#+val['votes']*0.3
		slist=[]
		counter=-600
	  	for row in data:
			if len(row['_source']['data'])>600:
				#while row['_source']['data'][counter]!=' ':    
				if row['_source']['data'][counter]!=' ': 
                                        counter=counter+1
				if row['_source']['data'][counter]!=' ':
                                        counter=counter+1
				if row['_source']['data'][counter]!=' ':
                                        counter=counter+1
				if row['_source']['data'][counter]!=' ':
                                        counter=counter+1
				if row['_source']['data'][counter]!=' ':
                                        counter=counter+1
				if row['_source']['data'][counter]!=' ':
                                        counter=counter+1
		
                                row['_source']['data'] =  row['_source']['data'][counter:]
	        	
		        if row['_source']['header'] not in histlist and 'secondlife' not in row['_source']['link'] and 'client' not in row['_source']['header'].lower():
                       		slist.append(row['_source'])
                 		histlist.append(str(row['_source']['header']))
		#print slist
                print '*****Rec**'
		slist.sort(key =getkey, reverse=True)
		if not home:
                    ourlist =slist[30*(page-1):30*page] #[-51:]	
                else:
                    ourlist =slist[100*(page-1):100*page]
                    maxpage=len(data)/100
                    if maxpage<(page-1):
		      page=1  
		print '*****Rec2**'
		#ourlist.sort(key =getkey, reverse=True)
	
		jsondata.update({'articles':ourlist})
		print '*****Rec3**'"""
		try:
			likedlinks=db.LikedPosts.find_one({'user':str(request.user)},{'cardlink':1,'_id':False})
			likedlinks=[i.encode('utf-8') for i in likedlinks['cardlink']]
			print likedlinks
		except:
			pass
		if not home:
		    if request.GET.get('query'):
		        res=duck_lets_go(request.GET.get('query').split("/")[0]+" news")[3:]
                    else:
              		res = duck_lets_go("xyz")[3:]
              	else:
              	    res=duck_lets_go("xyz")[3:]
              	    
              	maxpage=len(res)/30
		#for val in jlist:
		#	print val['header'], val['scores'][1]
		if True:
          		variables = Context({ 
			'user': request.user ,
                        'title':'Demo Content',
                        'year': datetime.now().year,
                        'feed': res,
                        'options': options,
                        'selectedcat': selectedcat,
                        'page': page,
                        'maxpage': maxpage,
                        'likedlinks': likedlinks
                        })
                else:
                        variables = Context({ 
			'user': request.user ,
                        'title':'Demo Content',
                        'year': datetime.now().year,
                        'feed': res,
                        'options': options,
                        'selectedcat': selectedcat,
                        'page': page,
                        'maxpage': maxpage,
                        'likedlinks': likedlinks
                        })
                output = template.render(variables)

		'''
           	if os.path.exists(str(request.user)+'.txt'):
                        with open(str(request.user)+'.txt') as json_file:
                                data = json.load(json_file)
                                variables = Context({ 'user': request.user ,
                                'title':'Demo Content',
                                'year': datetime.now().year,
                                'feed': data
                             })
                        output = template.render(variables)
                else:
                        with open('newsjson.txt') as json_file:
                                data = json.load(json_file)
                                variables = Context({ 'user': request.user ,
                                'title':'Demo Content',
                                'year': datetime.now().year,
                                'feed': data
                             })
                        output = template.render(variables)
   
		'''
		return HttpResponse(output)



def newsagri(request):
        if 1==1:
                template = loader.get_template('crawler/news.html')
                #response = requests.get('https://newsapi.org/v1/articles?source=business-insider&sortBy=top&apiKey='+ apikey )
                #response = response.json()
                #print response
                import requests

                # api-endpoint
                URL = "http://localhost:9200/docartificial_intelligencegames/_search?size=1000&q=*:*"

                # sending get request and saving the response as response object
                r = requests.get(url = URL)

                # extracting data in json format
                data = r.json()
                jsondata={}
                jlist=[]
                data = data['hits']['hits']
                for rows in data:
                        jlist.append(rows['_source'])
                def getkey(val):
                        #print val['scores'][1]
                        if len(val['scores'])>0:
                                return val['scores'][0]
                        else:
                                return 0.299
                ourlist =jlist #[-51:]
                ourlist.sort(key =getkey, reverse=True)
                jsondata.update({'articles':ourlist})

                #for val in jlist:
                #       print val['header'], val['scores'][1]
                variables = Context({
                        'user': request.user ,
                        'title':'Demo Content',
                        'year': datetime.now().year,
                        'feed': jsondata
                   })
                output = template.render(variables)
                return HttpResponse(output)




def newsenv(request):
        if 1==1:
                template = loader.get_template('crawler/home.html')
                #response = requests.get('https://newsapi.org/v1/articles?source=business-insider&sortBy=top&apiKey='+ apikey )
                #response = response.json()
                #print response
                import requests
                coll=db.config
                try:
                    cur=coll.find_one({"user":str(request.user)},{'choice':1,'_id':False})
                    for key,value in cur.items():
                        if key=="choice":        
                            choice=value
                except:
                    choice={"Mining and Drilling":[],"Environment":["Waste Management"],"Agriculture and Forestry":[],"Opportunities":["News and Media"],"Energy":["Oil and Gas"],"Business Services":[],"Information Technology":["Investing"]}

                options=OrderedDict()
                categoryimg={}
                subcategoryimg={}
                with open("crawler/categoryimglinks2") as f1,open("crawler/subcatimglinks2") as f2:
                    for line in f1:
                        line=line.split(" : ")
                        if line[0].strip() in choice:
                            categoryimg[line[0].strip()]=line[1].strip()
                    for line in f2:
                        line=line.split(" : ")
                        catsub=line[0].split("__")
                        if catsub[0].strip() in choice:
                            subcategoryimg.setdefault(catsub[0].strip(),{})
                            if catsub[1].strip() in choice[catsub[0].strip()]:
                                subcategoryimg[catsub[0].strip()][catsub[1].strip()]=line[1].strip()
                for i in choice:
                    options[i]=categoryimg[i]
                    for j in choice[i]:
                        options[j]=subcategoryimg[i][j]
                #print options
                # api-endpoint
                URL = "http://localhost:9200/docnewsandmedia/_search?size=1000&q=*:*"

                # sending get request and saving the response as response object
                r = requests.get(url = URL)

                # extracting data in json format
                data = r.json()
                jsondata={}
                jlist=[]
                data = data['hits']['hits']
                for rows in data:
                        jlist.append(rows['_source'])
                def getkey(val):
                        #print val['scores'][1]
                        if len(val['scores'])>0:
                                return val['scores'][0]
                        else:
                                return 0.299
                ourlist =jlist #[-51:]
                ourlist.sort(key =getkey, reverse=True)
                jsondata.update({'articles':ourlist})

                #for val in jlist:
                #       print val['header'], val['scores'][1]
                variables = Context({
                        'user': request.user ,
                        'title':'Demo Content',
                        'year': datetime.now().year,
                        'feed': jsondata,
                        'options':options
                   })
                output = template.render(variables)
                return HttpResponse(output)


def home(request):
	#import news_personalization
	
	if not request.GET.get('query'):
		output = news(request,home=True)	
		'''
		template = loader.get_template('crawler/home.html')
		#response = requests.get('https://newsapi.org/v1/articles?source=business-insider&sortBy=top&apiKey='+ apikey )
		#response = response.json()
		#print response
		cursor = db.config.find({"user":str(request.user)})
		for document in cursor:
			print(document)
		if os.path.exists(str(request.user)+'.txt'):
			with open(str(request.user)+'.txt') as json_file:
                   		data = json.load(json_file)
		    		variables = Context({ 'user': request.user ,
	            		'title':'Demo Content',
	            		'year': datetime.now().year,
	           		'feed': data
	        	     })
			output = template.render(variables)
		else:
			with open('newsjson.txt') as json_file:
                                data = json.load(json_file)
                                variables = Context({ 'user': request.user ,
                                'title':'Demo Content',
                                'year': datetime.now().year,
                                'feed': data
                             })
                        output = template.render(variables)
		'''
	else :
		#print "poppy"
		x = str(request.GET.get('query')).lower() 
		if request.GET.get('theme'):
                    theme=" ".join(request.GET.get('theme').split("/"))
                    if theme=="all":
                        theme=""
                else:
                    theme=""

		if request.GET.get('lang'):
		    lang = request.GET.get('lang').split("/")[0]
		    if lang=="Hebrew":
		        #x = translator.translate(x, dest='iw').text
			x = TextBlob(unicode(x))
			x = x.translate(to='iw')
		    if lang=="Japanese":
                        #x = translator.translate(x, dest='ja').text
			x = TextBlob(unicode(x))
                        x = x.translate(to='ja')
		    if lang=="Russian":
                        #x = translator.translate(x, dest='ru').text
			x = TextBlob(unicode(x))
                        x = x.translate(to='ru')
		    if lang=="Korean":
                        #x = translator.translate(x, dest='ko').text
			x = TextBlob(unicode(x))
                        x = x.translate(to='ko')
		    if lang=="Mandarin":
                        #x = translator.translate(x, dest='zh-TW').text
			x = TextBlob(unicode(x))
                        x = x.translate(to='zh-TW')
		y=x+' '+theme
		res = duck_lets_go(y)[3:]
	        #raise ValueError("hi")
		for i in res:
		    if "duckduckgo" in i.get("link"):
		        res.remove(i)
		    elif "Ad" == i.get("header")[:-2]:
		        res.remove(i)
		if request.GET.get('en'):
		    en=request.GET.get('en').split("/")[0]
                    if en=="eng":
	
			for i,j in enumerate(res):
		
				j["header"] = TextBlob(unicode(j["header"]))
                       	        j["header"] = j["header"].translate(to='en')
				res[i]["header"] = j["header"]
				j["sum"] = TextBlob(unicode(j["sum"]))
                                j["sum"] = j["sum"] .translate(to='en')
                                res[i]["sum"] = j["sum"]
			print res
          
	
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
		#query_string = 	query_string[1:].split(" ")
		#for string in query_string:
		db.SearchHistory.update_one({"user":str(request.user)},{"$push":{"history":query_string},"$set":{"user":str(request.user)}}, upsert=True)
		db.SearchHistory.update_one({"user":str(request.user)},{"$push":{"themehistory":theme},"$set":{"user":str(request.user)}}, upsert=True)

		import subprocess
		try:
		    subprocess.Popen([sys.executable,"updateindex2.py"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
		except:
		    print "na ho paega"

		'''
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
					          "fields": [ "data", "header^2" ]
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
									  "x": 0.0,
									  "y": 0.8,
									  "z": 0.33
									}, #( (_score*0.33)/6 + (total*0.33)/sz + *0.33doc['votes'].value )
									"inline": "if(doc['votes'].value<1){return (_score*params.x)/4  + params.z*doc['votes'].value;}else{return (_score*params.x)/4  + 0.234;}" 
								}

				}                                

                            }],
			
                             "score_mode": "sum"
				      	     
				 			
							}
						},
				"from" : 0, "size" : 20

				}
				 
		#result = es.search(index="sw", body={"query": {"match": {'data': request.GET.get('query')}}})
		
		import requests
                coll=db.config
                try:
                    cur=coll.find_one({"user":str(request.user)},{'choice':1,'_id':False})
                    for key,value in cur.items():
                        if key=="choice":        
                            choice=value
                except:
                    choice={"Mining and Drilling":[],"Environment":["Waste Management"],"Agriculture and Forestry":[],"Opportunities":["News and Media"],"Energy":["Oil and Gas"],"Business Services":[],"Information Technology":["Investing"]}

                options=OrderedDict()
                categoryimg={}
                subcategoryimg={}
                with open("crawler/categoryimglinks2") as f1,open("crawler/subcatimglinks2") as f2:
                    for line in f1:
                        line=line.split(" : ")
                        if line[0].strip() in choice:
                            categoryimg[line[0].strip()]=line[1].strip()
                    for line in f2:
                        line=line.split(" : ")
                        catsub=line[0].split("__")
                        if catsub[0].strip() in choice:
                            subcategoryimg.setdefault(catsub[0].strip(),{})
                            if catsub[1].strip() in choice[catsub[0].strip()]:
                                subcategoryimg[catsub[0].strip()][catsub[1].strip()]=line[1].strip()
                for i in choice:
                    options[i]=categoryimg[i]
                    for j in choice[i]:
                        options[j]=subcategoryimg[i][j]
                #print options
                
		selectedcat="None"
		if request.GET.get('theme'):
		    try:
		        theme=str(request.GET.get('theme')).strip().replace(" ","").replace("_","").lower()
		        selectedcat=request.GET.get('theme')
		        myvar=False
		        for key,value in choice.items():
		            if selectedcat==key:
		                myvar=True
		                break
		            else:
		                if selectedcat in value:
		                    myvar=True
		                    break
		        if not myvar:
		            selectedcat="None"
		        result = es.search(index="doc"+theme, body=myquery)
                    except:
                        result = es.search(index="_all", body=myquery)
		else:
		    result = es.search(index="_all", body=myquery)

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
			if rows["_source"]["header"] in resdup or 'client' in rows['_source']['header'].lower():
				continue
			resdup.append(rows["_source"]["header"])
			f_sum={}
			f_res={}
			f_res["link"]=rows["_source"]["link"]
			f_res["theme"]=rows["_source"]["flagindex"]
			f_res["entity"]= rows["_source"]["entity"][0:8] 
			if len(rows["_source"]["data"]) >= 900:
				if 'techcrunch' in f_res["link"] or 'cnbc' in f_res["link"]:
					f_res["data"]=rows["_source"]["data"][350:750]+"..."
				else:
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
					if len(f_res["data"])>180:
						f_sum["text"]=f_res["data"][:180]		
					else:
						f_sum["text"]=f_res["data"]	
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
		'''
		options=OrderedDict()
                categoryimg={}
                subcategoryimg={}
                selectedcat=""
                #response = requests.get('https://newsapi.org/v1/articles?source=business-insider&sortBy=top&apiKey='+ apikey )
                #response = response.json()
                #print response
                coll=db.config
                try:
                    cur=coll.find_one({"user":str(request.user)},{'choice':1,'_id':False})
                    for key,value in cur.items():
                        print key,value
		    	if key=="choice":        
                            choice=value
                except:
                    choice={"Mining and Drilling":[],"Environment":["Waste Management"],"Agriculture and Forestry":[],"Opportunities":["News and Media"],"Energy":["Oil and Gas"],"Business Services":[],"Information Technology":["Investing"]}

                options=OrderedDict()
                categoryimg={}
                subcategoryimg={}
                selectedcat=""
                themes_keywords=db.UserKeywords.find({'user':str(request.user)},{'_id':False,'user':False})
                for key,value in choice.items():
                    if len(value)>0:
                        selectedcat=key+value[0]
                    else:
                        selectedcat=key
                    break
                    
                if request.GET.get('theme'):
                    selectedcat=str(request.GET.get('theme'))
                
                with open("crawler/categoryimglinks2") as f1,open("crawler/subcatimglinks2") as f2:
                    for line in f1:
                        line=line.split(" : ")
                        if line[0].strip() in choice:
                            categoryimg[line[0].strip()]=line[1].strip()
                    for line in f2:
                        line=line.split(" : ")
                        catsub=line[0].split("__")
                        if catsub[0].strip() in choice:
                            subcategoryimg.setdefault(catsub[0].strip(),{})
                            if catsub[1].strip() in choice[catsub[0].strip()]:
                                subcategoryimg[catsub[0].strip()][catsub[1].strip()]=line[1].strip()
                
                for i in themes_keywords:
                    if i['theme'] in choice:
                        for j in i['keywords']:
                            if i['theme'] not in subcategoryimg:
                                subcategoryimg.setdefault(i['theme'],{})
                            subcategoryimg[i['theme']][j]="https://incomebully.com/wp-content/uploads/2015/05/keyword-research.png" 
                
                for i in choice:
                    options[i]=categoryimg[i]
                    for j in choice[i]:
                        options[j+'/'+i]=subcategoryimg[i][j]
                print 'RRRRRRRRRRRRRRRR', options 
		Scursor = db.SearchHistory.find({'user':str(request.user)})
       	 	'''
		search_hist = []
        	for hist in Scursor:
                	print hist['history']
                	for val in hist['history']:
				search_hist.append(val)
		'''
		from updateindex2 import find_history
		search_hist = find_history(str(request.user), G) 		
                template = loader.get_template('crawler/search.html')
		
		variables = Context({ 'user': request.user ,
	            'title':'Demo Content',
	            'year': datetime.now().year,
	            'results' : res,
		    'query': request.GET.get('query'),
		    'summary':zip(*res)[:2],
		    'options' :options,
		    'search_patern':search_hist,
		    'selectedcat' :selectedcat,
		 })
		output = template.render(variables)
	return HttpResponse(output)




def get_suggestion(request):
	if not request.GET.get('query'):
		return HttpResponse("null");
	else:
		urla='http://suggestqueries.google.com/complete/search?client=firefox&q='+urllib.quote_plus(request.GET.get('query'));
		print urla
		response = urllib2.urlopen(urla).read()
		return HttpResponse(response);

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/login')

def liked_card(request):
    if request.GET.get('card'):
        cardlink=request.GET.get('card')
        col=db.LikedPosts
        cur=col.find_one({'user':str(request.user)},{'cardlink':1,'_id':False})
        cur=cur['cardlink']
        if cardlink in cur:
            col.update_one({"user":str(request.user)},{"$pop":{"cardlink":cardlink},"$set":{"user":str(request.user)}}, upsert=True)
        else:
            col.update_one({"user":str(request.user)},{"$push":{"cardlink":cardlink},"$set":{"user":str(request.user)}}, upsert=True)
        response={"success":"true"}
        response=json.dumps(response)
    else:
        response={"success":"false"}
        response=json.dumps(response)
    return HttpResponse(response)

def add_keyword(request):
    if request.GET.get('keyword') and request.GET.get('theme'):
        theme=request.GET.get('theme')
        keyword=request.GET.get('keyword')
        col=db.UserKeywords
        cur=col.find_one({'user':str(request.user),'theme':theme},{'keywords':1,'_id':False})
        if cur is not None:
            cur=cur['keywords']
            if keyword not in cur:
                col.update_one({"user":str(request.user),"theme":theme},{"$push":{"keywords":keyword},"$set":{"user":str(request.user),"theme":theme}}, upsert=True)
        else:
            col.insert_one({"user":str(request.user),"theme":theme,"keywords":[keyword]})
        response={"success":"true"}
        response=json.dumps(response)
    else:
        response={"success":"false"}
        response=json.dumps(response)
    return HttpResponse(response)
