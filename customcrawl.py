mport sys  

reload(sys)  
sys.setdefaultencoding('utf8')
import sys
import requests
import hashlib
from bs4 import BeautifulSoup
from datetime import datetime
#from stack_spider import StackSpider
import urlparse
import urllib2
import urllib, re
#from scraper import grabContent
import nltk 
import time
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch
import time,json


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
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
def is_absolute(url):
    return bool(urlparse.urlparse(url).netloc)
def find_internal_urls(lufthansa_url, depth=0, max_depth=2):
    all_urls_info = []
    status_dict = {}
    soup = get_soup(lufthansa_url)
    a_tags = soup.findAll("a", href=True)

    if depth > max_depth:
        return {}
    else:
        for a_tag in a_tags[100:]:
            if "http" not in a_tag["href"] and "/" in a_tag["href"]:
                url = lufthansa_url + a_tag['href']
                print "relative",url
            elif "http" in a_tag["href"] and is_absolute(a_tag["href"]):
                url = a_tag["href"]
                print "absolute",url
            else:
                continue
            for i in all_urls_info:
		#spidy1 = StackSpider(i["url"])
		#print spidy1.url
		#print requests.get(spidy1.url)
		#result = spidy1.parse(requests.get(spidy1.url))
		
		'''
		result = grabContent(url, html)
		#"https://techcrunch.com/page/2/"
	
		result = BeautifulSoup(result)
		all_texts = result.find_all("p")
		#print(all_texts[1])
		#all_texts = all_texts[0]
		#print(all_texts)
		#print(len(all_texts))
		text1 = ""
		for i in range(len(all_texts)):
				#print(all_texts[i])
				all_links = all_texts[i].find_all("a")
		
				for links in all_links:
				  	cleanr = re.compile('<.*?>')
		  		  	all_texts[i] = re.sub(cleanr, '', str(all_texts[i]))
		  		  	cleanr = re.compile('<script>.*?</script>')
		  		  	all_texts[i] = re.sub(cleanr, '', str(all_texts[i]))
				#print(all_texts[i])
				text1 = text1 + str(all_texts[i])
		cleanr = re.compile('<.*?>')
		text1 = re.sub(cleanr, '', str(text1))

		print text1
	        '''
	    if get_status_code(url) == 200:
	    	try:
			headers = { 'User-Agent' : 'Mozilla/5.0' }
			req = urllib2.Request(url, None, headers)
            		#write the elastic search code here
            		html = urllib.urlopen(req).read()
            		raw = clean_html(html)  
	    		print(raw)
	    		data = BeautifulSoup(html,"lxml")
	    		#print data
	    		header = data.find_all("title")
	    		print "header",str(header[0])
			
			query= header.split()
			query='+'.join(query)
			url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
			header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"}
			soup = get_soup(url)
			ActualImages = [] 
			for a in soup.find_all("div",{"class":"rg_meta"}):
	    			link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
	    			ActualImages.append((link,Type))
	    		img = data.find_all("img")
                        #print '####################### ',image
			all_imgs=[]			
			for j in range(len(img)):
       				all_imgs.append(img[j].attrs.get("src"))
			#print '################################',all_imgs
			jpg_img = []
			for i in ActualImages:
				if (i.split('.')[-1] == 'jpg' or i.split('.')[-1] == 'png') and is_absolute(i):
					jpg_img.append(i)
			print '#############################jpeg',jpg_img
			image =''
	                if len(jpg_img)>0:
				image = jpg_img[0]
        	        print image
			cleanr = re.compile('<.*?>')
	    		header = re.sub(cleanr,'',str(header[0]))
	    		print "header",header
			if BeautifulSoup(urllib.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ url), "xml")!=None:
		                alexa_score = BeautifulSoup(urllib.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ url), "xml").find("REACH")['RANK']
        	        else:
				alexa_score = 99999999
			import math
			dict1= {"scores":[],"link":url ,"data": raw,"header":header,"votes":1/(1+math.log10(int(alexa_score))), "entity": [], "flagindex":'To be Classified',"sum":'abc', "img":image}
			data = json.dumps(dict1, ensure_ascii=False)
			es.index(index='docothers', doc_type='peopleimg', id=url,body=json.loads(data))
				
	    	except Exception as e1:
			print str(e1),'exception 1'
	    		time.sleep(5)
	    		continue
   	    print 'done here'            
            status_dict["url"] = url
            status_dict["status_code"] = get_status_code(url)
            status_dict["timestamp"] = datetime.now()
            status_dict["depth"] = depth + 1
            all_urls_info.append(status_dict)
    return all_urls_info
if __name__ == "__main__":
    depth = 2 # suppose 
    #all_page_urls = find_internal_urls("http://www.farmindustrynews.com", 2, 2)
    #all_page_urls = find_internal_urls("http://www.indiaagristat.com", 2, 2)
    #all_page_urls = find_internal_urls("http://www.beckag.com", 2, 2)
    #all_page_urls = find_internal_urls("http://www.soygrowers.com", 2, 2)
    #all_page_urls = find_internal_urls("http://www.ncga.com", 2, 2)
    all_page_urls = find_internal_urls("http://www.ideglobal.com", 2, 2)
    #all_page_urls = find_internal_urls("https://www.yahoo.com/news/", 2, 2)
    #all_page_urls = find_internal_urls("http://world.honda.com/ASIMO/", 2, 2)
    count = 0
    if depth > 1 and count<=150:
        for status_dict in all_page_urls:
            find_internal_urls(status_dict['url'])
            print count
            count = count + 1

