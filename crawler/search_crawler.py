
import urllib2
import requests
from bs4 import BeautifulSoup
def get_soup_img(url,header):
    return BeautifulSoup(urllib2.urlopen(urllib2.Request(url,headers=header)),'html.parser')
import urlparse

def is_absolute(url):
    return bool(urlparse.urlparse(url).netloc)



import urllib

from random import shuffle

import re

import json
def duck_lets_go(query):
	api_url = "https://duckduckgo.com/html/?q=" + query + "&format=json"
	#query_url = api_url %query
	response = requests.get(api_url)
	#print response.text
	data = BeautifulSoup(response.text)


	#print data
	all_headers = data.find_all("h2",{"class":"result__title"})

	header = []

	images = []

	for i in all_headers:
	
		cleanr = re.compile('<.*?>')
	  	i = re.sub(cleanr, '', str(i))
	  	cleanr = re.compile('<script>.*?</script>')
	  	i = re.sub(cleanr, '', i[1:-1])
	  	header.append(i)
	
	#print header


	all_texts = data.find_all("a",{"class":"result__snippet"})

	#print all_texts

	texts = []


	for i in all_texts:
		cleanr = re.compile('<.*?>')
	  	i = re.sub(cleanr, '', str(i))
	  	cleanr = re.compile('<script>.*?</script>')
	  	i = re.sub(cleanr, '', i)
	  	texts.append(i)
	
	#print texts

	all_links = data.find_all("a",{"class":"result__url"})

	#print all_links

	links = []


	for i in all_links:
		i = i.get("href")[15:]
		i = re.sub("%20"," ",i)
		i = re.sub("%21","!",i)
		i = re.sub("%22",'"',i)
		i = re.sub("%23","#",i)
		i = re.sub("%24","$",i)
		i = re.sub("%25","%",i)
		i = re.sub("%26","&",i)
		i = re.sub("%27","'",i)
		i = re.sub("%28","(",i)
		i = re.sub("%29",")",i)
		i = re.sub("%2A","*",i)
		i = re.sub("%2B","+",i)
		i = re.sub("%2D","-",i)
		i = re.sub("%2E",".",i)
		i = re.sub("%2F","/",i)
		i = re.sub("%30","0",i)
		i = re.sub("%31","1",i)
		i = re.sub("%32","2",i)
		i = re.sub("%33","3",i)
		i = re.sub("%34","4",i)
		i = re.sub("%35","5",i)
		i = re.sub("%36","6",i)
		i = re.sub("%37","7",i)
		i = re.sub("%38","8",i)
		i = re.sub("%39","9",i)
		i = re.sub("%3A",":",i)
		i = re.sub("%3B",";",i)
		i = re.sub("%3C","<",i)
		i = re.sub("%3D","=",i)
		i = re.sub("%3E",">",i)
		i = re.sub("%3F","?",i)
		#print i
		links.append(i)


	 
	#print links
	data_list=[]    
	for i in zip(header,links,texts):
		data = {}
		data["header"] = i[0]
		#print i[0]
		data["link"] = i[1]
		#print i[1]
		data["data"] = i[2]
		#print i[2]
		data['img']='https://www.cleverfiles.com/howto/wp-content/uploads/2016/08/mini.jpg'
		data_list.append(data)
	tp = zip(header,links,texts)
	#print zip(*tp)[:2]
	return data_list

def duck_lets_go2(query):
	#print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!', query
	api_url = "https://duckduckgo.com/html/?q=" + query + "&format=json"
	#query_url = api_url %query
	response = requests.get(api_url)
	#print response.text
	data = BeautifulSoup(response.text)


	#print data
	all_headers = data.find_all("h2",{"class":"result__title"})

	header = []

	images = []
	#print '#####################'
	for i in all_headers:
	
		cleanr = re.compile('<.*?>')
	  	i = re.sub(cleanr, '', str(i))
	  	cleanr = re.compile('<script>.*?</script>')
	  	i = re.sub(cleanr, '', i[1:-1])
	  	header.append(i)
	
	#print header
	

	all_texts = data.find_all("a",{"class":"result__snippet"})

	#print all_texts

	texts = []


	for i in all_texts:
		cleanr = re.compile('<.*?>')
	  	i = re.sub(cleanr, '', str(i))
	  	cleanr = re.compile('<script>.*?</script>')
	  	i = re.sub(cleanr, '', i)
	  	texts.append(i)
	
	#print texts

	all_links = data.find_all("a",{"class":"result__url"})

	#print all_links

	links = []


	for i in all_links:
		i = i.get("href")[15:]
		i = re.sub("%20"," ",i)
		i = re.sub("%21","!",i)
		i = re.sub("%22",'"',i)
		i = re.sub("%23","#",i)
		i = re.sub("%24","$",i)
		i = re.sub("%25","%",i)
		i = re.sub("%26","&",i)
		i = re.sub("%27","'",i)
		i = re.sub("%28","(",i)
		i = re.sub("%29",")",i)
		i = re.sub("%2A","*",i)
		i = re.sub("%2B","+",i)
		i = re.sub("%2D","-",i)
		i = re.sub("%2E",".",i)
		i = re.sub("%2F","/",i)
		i = re.sub("%30","0",i)
		i = re.sub("%31","1",i)
		i = re.sub("%32","2",i)
		i = re.sub("%33","3",i)
		i = re.sub("%34","4",i)
		i = re.sub("%35","5",i)
		i = re.sub("%36","6",i)
		i = re.sub("%37","7",i)
		i = re.sub("%38","8",i)
		i = re.sub("%39","9",i)
		i = re.sub("%3A",":",i)
		i = re.sub("%3B",";",i)
		i = re.sub("%3C","<",i)
		i = re.sub("%3D","=",i)
		i = re.sub("%3E",">",i)
		i = re.sub("%3F","?",i)
		#print i
		links.append(i)


	#all_imgs = data.find_all("img",{"class":"result__icon__img"})
 	imgs = []
	'''
	for i in all_imgs:
		i = i.get("src")
		i = "https:" + i
		imgs.append(i)
	#print imgs
	'''
	data_list=[]
	'''
	query= str(query).split()
        query='+'.join(query)
        print 'd$$$$$$$$$'
        print "ye rahii queryyy",query
        imgurl="https://www.google.com/search?q="+query+"&source=lnms&tbm=isch"
        headerapi={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
        soup = get_soup_img(imgurl, headerapi)
        ActualImages = []
        for a in soup.find_all("div",{"class":"rg_meta"}):
                link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
                ActualImages.append((link,Type))
	jpg_img = []
        for i in ActualImages:
                     #print i
  		     i=i[0]                 
                     if (i.split('.')[-1] == 'jpg' or i.split('.')[-1] == 'png'):
                                   #print i
                                    jpg_img.append(i)
                                   #break
	
	print "dekhhho ",jpg_img
	'''
	import subprocess
	import sys
  	#if 'Oil' in query:
	#	query = "Natural gas extraction"	
	val= subprocess.check_output(['python3 msimage.py '+ query ], shell=True)
	jpg_img=val.split('\n')
    	try:
    	   while len(jpg_img)<len(header):
		jpg_img.extend(shuffle(jpg_img))
        except:
            print "nonetype not iterable"
		
	for i in zip(header,links,texts,jpg_img):
		data = {}
		data["header"] = i[0]
		#print i[0]
		data["link"] = i[1]
		#print i[1]
		data["data"] = i[2]
		#print i[2]
		data["img"] = i[3]
		#print data["img"]
		data_list.append(data)
	tp = zip(header,links,texts)
	#print zip(*tp)[:2]
	return data_list

#x = duck_lets_go("bill clinton")
#print x

'''
results = response['responseData']['results']
if results:
   first_result_url = results[0]['url']
'''

