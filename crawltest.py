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

import argparse
import time
import json
import StringIO
import gzip
import csv
import codecs
import urllib, re

from bs4 import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf8')

# parse the command line arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-d","--domain",required=True,help="The domain to target ie. cnn.com")
#args = vars(ap.parse_args())

#domain = args['domain']

# list of available indices
index_list = ["2017-34","2017-09","2017-13","2017-17","2017-22","2017-26","2017-30"]
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
 

domain_list = ["breitbart-news.com","business-insider.com","business-insider-uk.com","buzzfeed.com","cnbc.com","cnn.com","daily-mail.com","der-tagesspiegel.com","die-zeit.com","engadget.com","entertainment-weekly.com","espn-cric-info.com","espn.com","financial-times.com","football-italia.com","focus.com","four-four-two.com","fortune.com","fox-sports.com","google-news.com","gruenderszene.com","hacker-news.com","handelsblatt.com","ign.com","independent.com","mashable.com","metro.com","mirror.com","mtv-news.com","mtv-news-uk.com","national-geographic.com","new-scientist.com","newsweek.com","new-york-magazine.com","polygon.com","recode.com","reddit-r-all.com","reuters.com","spiegel-online.com","t3n.com","talksport.com","techradar.com","the-economist.com","the-guardian-au.com","the-guardian-uk.com","the-hindu.com","the-huffington-post.com","the-lad-bible.com","the-new-york-times.com","the-next-web.com","the-sport-bible.com","the-telegraph.com","the-verge.com","the-wall-street-journal.com","the-washington-post.com","usa-today.com","time.com","wired-de.com","wirtschafts-woche.com"]

for domain in domain_list:
    def search_domain(domain):

        record_list = []
        
        print "[*] Trying target domain: %s" % domain
        
        for index in index_list:
            
            print "[*] Trying index %s" % index
            
            cc_url  = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index
            cc_url += "url=%s&matchType=domain&output=json" % domain
            
            response = requests.get(cc_url)
            
            if response.status_code == 200:
                
                records = response.content.splitlines()
                
                for record in records:
                    record_list.append(json.loads(record))
                
                #print "[*] Added %d results." % len(records)
                
        
        print "[*] Found a total of %d hits." % len(record_list)
        
        return record_list        

    #
    # Downloads a page from Common Crawl - adapted graciously from @Smerity - thanks man!
    # https://gist.github.com/Smerity/56bc6f21a8adec920ebf
    #



    def download_page(record):

        offset, length = int(record['offset']), int(record['length'])
        offset_end = offset + length - 1

        # We'll get the file via HTTPS so we don't need to worry about S3 credentials
        # Getting the file on S3 is equivalent however - you can request a Range
        prefix = 'https://commoncrawl.s3.amazonaws.com/'
        
        # We can then use the Range header to ask for just this set of bytes
        resp = requests.get(prefix + record['filename'], headers={'Range': 'bytes={}-{}'.format(offset, offset_end)})
        
        # The page is stored compressed (gzip) to save space
        # We can extract it using the GZIP library
        raw_data = StringIO.StringIO(resp.content)
        f = gzip.GzipFile(fileobj=raw_data)
        
        # What we have now is just the WARC response, formatted:
        data = f.read()
        
        response = ""
        
        if len(data):
            try:
                warc, header, response = data.strip().split('\r\n\r\n', 2)
            except:
                pass
                
        return response

    #clean html_content
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



    #
    # Extract links from the HTML  
    #
    def extract_external_links(html_content,link_list, mainurl):

        parser = BeautifulSoup(html_content)
        links = parser.find_all("a")
        all_texts = parser.find_all("p")
        img = parser.find_all("img")
	all_imgs =[]
        #header = data.title.string
        #all_texts = all_texts[0]
        #print(all_texts)
        #print(len(all_texts))
        for j in range(len(img)):
	    all_imgs.append(img[j].attrs.get("src"))
            #print all_imgs
        allstr=""
        for i in range(len(all_texts)):	
            all_links = all_texts[i].find_all("a")
            for links in all_links:
                cleanr = re.compile('<.*?>')
                all_texts[i] = re.sub(cleanr, '', str(all_texts[i]))
                cleanr = re.compile('<script>.*?</script>')
                all_texts[i] = re.sub(cleanr, '', str(all_texts[i]))
                    
            #print(all_texts[i])
        for i in range(len(all_texts)):
            cleanr = re.compile('<.*?>')
            all_texts[i] = re.sub(cleanr, '', str(all_texts[i]))
            allstr = allstr+" "+ all_texts[i]
            #print all_texts[i]
        print all_texts
        try:
            #print image					
            if len(all_imgs)>0:
		image = all_imgs[0]
	    else:
		image =""
            header = parser.title.string
            print header
            allstr= allstr.lower().encode(sys.stdout.encoding, errors='replace')
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

            keyword=["Business", "Technology", "Water", "Agriculture", "Sports", "Energy", "People","Entertainment"]
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
                                        if  x==3 or x==4 or x==2 :
                                                key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                key_div[x]=key_div[x]+2.01
                                        elif x==5:
                                                        key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                        key_div[x]=key_div[x]+1.65

                                        else:
                                            key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                            key_div[x]=key_div[x]+1.01
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
                                        if x==3 or x==4 or x==2 :
                                                key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                key_div[x]=key_div[x]+2.01
                                        
                                        elif x==5:
                                                        key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                        key_div[x]=key_div[x]+1.65

                                        else:
                                                key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                key_div[x]=key_div[x]+1.01
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
                                        if x==3 or x==4 or x==2 :
                                                key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                key_div[x]=key_div[x]+2.01
                                        elif x==5:
                                                        key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                        key_div[x]=key_div[x]+1.65
                                        else:
                                                key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                key_div[x]=key_div[x]+1.01
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
                                        if  x==3 or x==4 or x==2:
                                                key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                key_div[x]=key_div[x]+2.01
                                        
                                        elif x==5:
                                            key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                            key_div[x]=key_div[x]+1.65

                                        else:
                                                key_len[x] = key_len[x]+ len(nx.shortest_path(G,source=keyword[x].lower(),target=entval))
                                                key_div[x]=key_div[x]+1.01
                    except Exception as e2:
                        print str(e2),'exception 3'
        
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
            if len(allstr)>180:
                sumary =allstr[0:180]
            else:
		sumary = allstr
	    dict1= {"scores":[],"link":mainurl ,"data": allstr,"header":header,"votes":0.8, "entity": entity_list, "flagindex":indexvar, "sum": sumary, "img": image}
            data = json.dumps(dict1, ensure_ascii=False)
             
            if keyword[0] in indexvar:
                    es.index(index='doctechnology', doc_type='peopleimg', id=mainurl,body=json.loads(data))
            if keyword[1] in indexvar:
                    es.index(index='docbusiness', doc_type='peopleimg', id=mainurl,body=json.loads(data))
            if keyword[2] in indexvar:
                    es.index(index='docwm', doc_type='peopleimg', id=mainurl,body=json.loads(data))
            if keyword[3] in indexvar:
                    es.index(index='docagri', doc_type='peopleimg', id=mainurl,body=json.loads(data))
            if keyword[4] in indexvar:
                    es.index(index='docsports', doc_type='peopleimg', id=mainurl,body=json.loads(data))
            if keyword[5] in indexvar:
                    es.index(index='docenergy', doc_type='peopleimg', id=mainurl,body=json.loads(data))
            if keyword[6] in indexvar:
                    es.index(index='docpeople', doc_type='peopleimg', id=mainurl,body=json.loads(data))
            if keyword[7] in indexvar:
                    es.index(index='docent', doc_type='peopleimg', id=mainurl,body=json.loads(data))
            if "Other category" == indexvar:
                    es.index(index='docothers', doc_type='peopleimg', id=mainurl,body=json.loads(data))
           
            print 'done'

        
        except Exception as e2:
            print str(e2),'exception 1'
                    
        '''
        if links:
            
            for link in links:
                href = link.attrs.get("href")
                print href
                cleanr = re.compile('<.*?>')
                all_texts[i] = re.sub(cleanr, '', str(all_texts[i]))
                cleanr = re.compile('<script>.*?</script>')
                all_texts[i] = re.sub(cleanr, '', str(all_texts[i]))
            #print(all_texts[i])
                if href is not None:     
                    if domain not in href:
                        if href not in link_list and href.startswith("http"):
                            print "[*] Discovered external link: %s" % href
                            #html = urllib.urlopen(href).read()
                            #raw = clean_html(html)
                            #print '##############3', raw
                            link_list.append(href)
        '''
        return link_list




    record_list = search_domain(domain)
    link_list   = []

    for record in record_list:
        
        html_content = download_page(record)
        
        print "[*] Retrieved %d bytes for %s" % (len(html_content),record['url'])
        
        link_list = extract_external_links(html_content,link_list, record['url'])
        
    print "[*] Total external links discovered: %d" % len(link_list)

    with codecs.open("%s-links.csv" % domain,"wb",encoding="utf-8", errors='ignore') as output:

        fields = ["URL"]
        
        logger = csv.DictWriter(output,fieldnames=fields)
        logger.writeheader()
        
        for link in link_list:
            logger.writerow({"URL":link})


