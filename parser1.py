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
import numpy as np 
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize, word_tokenize
#from searchengine.settings import P
from searchengine.settings import T
from searchengine.settings import B
from searchengine.settings import E

import math 
 
def parse(url):
		
		
	data=[]
	print url
	techembedingMatrix = []
	EnergyembedingMatrix = []
	BusinessembedingMatrix = []
	#print "bigrams"
	if bs4.BeautifulSoup(urllib.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ url), "xml"):
		alexa_score = bs4.BeautifulSoup(urllib.urlopen("http://data.alexa.com/data?cli=10&dat=s&url="+ url), "xml").find("REACH")['RANK']
	else:
		alexa_score = 99999999
	print 'alexa ' +alexa_score
	idx=0
	stop_words = set(stopwords.words('english'))
	
	print "done till hhere"
	
	print 'started'
	headers = { 'User-Agent' : 'Mozilla/5.0' }
	req = urllib2.Request(url, None, headers)		
	data = urllib2.urlopen(req).read()
	data = BeautifulSoup(data)
	body = data.body
	if  body is None:
		return "", "", [], 0, "Energy", [] 

	Techscore=0
	BusinensScore=0
	Energyscore=0

	all_texts = body.find_all("p")
	#print(all_texts[1]) 
	header = data.title.string
	#all_texts = all_texts[0]
	#print(all_texts)
	#print(len(all_texts))
	text1 = ""
	for i in range(len(all_texts)):
		
		all_links = all_texts[i].find_all("a")
		
		for links in all_links:
		  	cleanr = re.compile('<.*?>')
  		  	all_texts[i] = re.sub(cleanr, '', str(all_texts[i]))
  		  	cleanr = re.compile('<script>.*?</script>')
  		  	all_texts[i] = re.sub(cleanr, '', str(all_texts[i]))
		#print(all_texts[i])
		text1 = text1 + str(all_texts[i]).lower()
	cleanr = re.compile('<.*?>')
	text1 = re.sub(cleanr, '', str(text1)).lower()
	#print
	#print(text)

	#print(data)
	#print(data.title.string)
	#print(data.h1.string)
	h = '\d{1,4}'
	hs = re.findall(h,str(data.string))
	#print(hs)
	#print(data.h2.string)
	#print(data.p.string)
	#print(data.body)
	data = data.body.get_text
	data = re.sub('<.*?>', '', str(data))
	data = re.sub('(\\t*\\n*)*', '	', str(data))
	data = re.sub('(\\n*\\t*)*', '', str(data))
	data = str(data).replace("\t","")
	data = data.replace("\n","")
	f = open("parser1.txt","w")
	f.write(data)
	f.close()
	#print(data)

	words = word_tokenize(data)

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
	Techentitity_list=[]
	Bizentitity_list=[]
	Energyentitity_list=[]
	
	for word in fin_list1:
		if word not in stop_words:
			fin_list.append(word)
	text = " ".join(fin_list)
	text = text.lower()
	#print text1
	valtext = text1.split(' ')
	for wordval in valtext:
		stop_words = set(stopwords.words('english'))
	  	data =[]
	  	for r in valtext:
	  		#print r
	  		if not r in stop_words:
	  			data.append(r.lower())
	TechList=[]

	bigrams2 = ngrams(data, 4)
	print "fourgrams"
	for grams in bigrams2:
		if B.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")!="not_exsist":
			print B.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")
			Bizentitity_list.append(B.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")[0])
			TechList.append(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3])
			BusinensScore= BusinensScore+100000-int(B.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")[0])
		if T.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")!="not_exsist":
			print T.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")
			TechList.append(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3])
			Techscore= Techscore+100000-int(T.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")[0])
		if E.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")!="not_exsist":
			Energyscore = Energyscore+ 100000-int(E.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")[0])
			print E.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")
			TechList.append(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3])
	    	Energyentitity_list.append(E.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")[0])
	     	#list(Q.keys(grams[0]+' '+grams[1]+' '+grams[2]))
	
	bigrams2 = ngrams(data, 3)
	print "trigrams"
	for grams in bigrams2:
		if B.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")!="not_exsist":
			TechList.append(grams[0]+' '+grams[1]+' '+grams[2])
			BusinensScore= BusinensScore+100000-int(B.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")[0])
	 		print B.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")
	 		Bizentitity_list.append(B.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")[0])	    	 
		if T.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")!="not_exsist":
	 		print T.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")
	 		TechList.append(grams[0]+' '+grams[1]+' '+grams[2])
	 		Techscore= Techscore+100000-int(T.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")[0])
	 		Techentitity_list.append(T.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")[0])	    	 
	  	if E.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")!="not_exsist":
	 		print E.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")
	 		Energyentitity_list.append(E.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")[0])	    	 
	  	  	TechList.append(grams[0]+' '+grams[1]+' '+grams[2])
	  	  	Energyscore = Energyscore+ 100000-int(E.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")[0])

	bigrams2 = ngrams(data, 2)
	print "bigrams"
	for grams in bigrams2:
		if B.get(grams[0]+' '+grams[1],"not_exsist")!="not_exsist":
			print B.get(grams[0]+' '+grams[1],"not_exsist")
			TechList.append(grams[0]+' '+grams[1])
			BusinensScore= BusinensScore+100000-int(B.get(grams[0]+' '+grams[1],"not_exsist")[0])
			Bizentitity_list.append(B.get(grams[0]+' '+grams[1],"not_exsist")[0])
		if T.get(grams[0]+' '+grams[1],"not_exsist")!="not_exsist":
			print T.get(grams[0]+' '+grams[1],"not_exsist")
			TechList.append(grams[0]+' '+grams[1])
			Techscore= Techscore+100000-int(T.get(grams[0]+' '+grams[1],"not_exsist")[0])
	 		Techentitity_list.append(T.get(grams[0]+' '+grams[1],"not_exsist")[0])
		if E.get(grams[0]+' '+grams[1],"not_exsist")!="not_exsist":
			print E.get(grams[0]+' '+grams[1],"not_exsist")
			TechList.append(grams[0]+' '+grams[1])
	 		Energyentitity_list.append(E.get(grams[0]+' '+grams[1],"not_exsist")[0])
			Energyscore = Energyscore+ 100000-int(E.get(grams[0]+' '+grams[1],"not_exsist")[0])
	bigrams2 = ngrams(data, 1)
	print "unigrams"
	for grams in bigrams2:
		if  B.get(grams[0],"not_exsist")!="not_exsist":
			#print B.get(grams[0],"not_exsist")
			TechList.append(grams[0])
			BusinensScore= BusinensScore+100000-int(B.get(grams[0],"not_exsist")[0])
	 		Bizentitity_list.append(B.get(grams[0],"not_exsist")[0])
		if  T.get(grams[0],"not_exsist")!="not_exsist":
			TechList.append(grams[0])
	 		print T.get(grams[0],"not_exsist")
	 		Techscore= Techscore+100000-int(T.get(grams[0],"not_exsist")[0])
			Techentitity_list.append(T.get(grams[0],"not_exsist")[0])
		if  E.get(grams[0],"not_exsist")!="not_exsist":
			TechList.append(grams[0])
			#print E.get(grams[0],"not_exsist")
			Energyentitity_list.append(E.get(grams[0],"not_exsist")[0])
			Energyscore = Energyscore+ 100000-int(E.get(grams[0],"not_exsist")[0])

	print Techentitity_list
	TechList=list(set(TechList))
	while 'n' in Energyentitity_list: Energyentitity_list.remove('n')
	#Energyentitity_list.remove(u'n')
	def MakeInt(elem):
		return int(elem)
	
	def MakeInt2(elem):
		return int(elem[0])


	Bizentitity_list.sort(key = MakeInt)
	Techentitity_list.sort(key = MakeInt)
	Energyentitity_list.sort(key = MakeInt)
	
	j=0
	k=0
		
	score_list=[]
	#print int(entitity_list[len(entitity_list)-1])+1
	#print "sorted"
	print "entity list"
	techmatrixlist1=[]
	intkvar=0
	entitity_list = Techentitity_list
	with open('Technology_file.txt_latest.emd_sorted') as f:
		for line in f:
			#print line.split('\t')[0]
			if intkvar<10:
				my_line =next(f)
				techmatrixlist1.append(my_line.rstrip().split(' ')[1:])
				#print my_line.rstrip().split(' ')[1:]
			else:
				break
			intkvar=intkvar+1

	techfloatmatrix1=[]
	for row in techmatrixlist1:
		floatrow=[]
		for val in row:
			floatrow.append(float(val))
		techfloatmatrix1.append(floatrow)


	k=0
	j=0
	with open('Technology_file.txt_latest.emd_sorted') as f:
		if len(entitity_list)>0:
			while k<=int(entitity_list[len(entitity_list)-1])+1 and j<len(entitity_list)-1:
				
				my_line= next(f)
				#print k
				if k==int(entitity_list[j]):
					#print "got T "+entitity_list[j]

					while k==int(entitity_list[j])and j<len(entitity_list)-1:
						j=j+1
						techembedingMatrix.append(my_line.rstrip().split(' ')[1:])
				k=k+1
		 
	floattechmatrix=[]
	for row in techembedingMatrix:
		floatrow=[]
		for val in row:
			#print val
			floatrow.append(float(val))
		floattechmatrix.append(floatrow)
	floattechmatrix = np.array(floattechmatrix)
	
	import scipy.spatial as sp
  	score =0
  	count_var=0
	for i in xrange(0,10):
		technprowfloatMatrix=[]
		technprowfloatMatrix.append(np.array(techfloatmatrix1[i]))
		technprowfloatMatrix.append(np.array(techfloatmatrix1[i]))
		
		#print floattechmatrix
		if len(floattechmatrix)<2:
			for x in xrange(0,10):
				score_list.append(0.001)
			break
		scorematrix = 1 - sp.distance.cdist(floattechmatrix,technprowfloatMatrix, 'cosine')  
  		for row in scorematrix:
  			for val in row:
	  			score = score+val
	  	 		count_var=count_var+1
  		#print str(score/count_var)#Scores for technology
  		score_list.append(score /count_var)
  	#doneeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee

	Businessmatrixlist=[]
	intkvar=0
	entitity_list = Bizentitity_list
	with open('Business_file.txt_latest.emd_sorted') as f:
		for line in f:
			#print line.split('\t')[0]
			if intkvar<10:
				my_line =next(f)
				Businessmatrixlist.append(my_line.rstrip().split(' ')[1:])
				#print my_line.rstrip().split(' ')[1:]
			else:
				break
			intkvar=intkvar+1

	Businessfloatmatrix=[]
	for row in Businessmatrixlist:
		floatBizrow=[]
		for val in row:
			floatBizrow.append(float(val))
		Businessfloatmatrix.append(floatBizrow)

 	print k,j
 	k=0
 	j=0
	with open('Business_file.txt_latest.emd_sorted') as f:
		if len(entitity_list)>0:
			while k<=int(entitity_list[len(entitity_list)-1])+1 and j<len(entitity_list)-1:
				my_line= next(f)
				if k==int(entitity_list[j]):
					#print "got T "+entitity_list[j]

					while k==int(entitity_list[j])and j<len(entitity_list)-1:
						j=j+1
						BusinessembedingMatrix.append(my_line.rstrip().split(' ')[1:])
				k=k+1

	 
	floatBizmatrix=[]
	for row in BusinessembedingMatrix:
		floatBizrow=[]
		for val in row:
			floatBizrow.append(float(val))
		floatBizmatrix.append(floatBizrow)
	floatBizmatrix = np.array(floatBizmatrix)
	
	import scipy.spatial as sp
  	score =0
  	count_var=0
	for i in xrange(0,10):
		BiznprowfloatMatrix=[]
		BiznprowfloatMatrix.append(np.array(Businessfloatmatrix[i]))
		BiznprowfloatMatrix.append(np.array(Businessfloatmatrix[i]))
		if len(floatBizmatrix)<2:
			for x in xrange(0,10):
				score_list.append(0.001)
			break
		scorematrix = 1 - sp.distance.cdist(floatBizmatrix,BiznprowfloatMatrix, 'cosine')  
  		for row in scorematrix:
  			for val in row:
	  			score = score+val
	  	 		count_var=count_var+1
  		#print str(score/count_var) #score for Business
  		score_list.append(score/count_var )
	#doneeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee

	Energymatrixlist=[]
	intkvar=0
	entitity_list = Energyentitity_list
	
	with open('Energy_file.txt_latest.emd_sorted') as f:
		for line in f:
			#print line.split('\t')[0]
			if intkvar<10:
				my_line =next(f)
				Energymatrixlist.append(my_line.rstrip().split(' ')[1:])
				#print my_line.rstrip().split(' ')[1:]
			else:
				break
			intkvar=intkvar+1

	Energyfloatmatrix=[]
	for row in Energymatrixlist:
		floatrow=[]
		for val in row:
			floatrow.append(float(val))
		Energyfloatmatrix.append(floatrow)

	print k,j
	k=0
	j=0
	with open('Energy_file.txt_latest.emd_sorted') as f:
		if len(entitity_list)>0:
		
			while k<=int(entitity_list[len(entitity_list)-1])+1 and j<len(entitity_list)-1:
				my_line= next(f)
				if k==int(entitity_list[j]):
					#print "got T "+entitity_list[j]

					while k==int(entitity_list[j])and j<len(entitity_list)-1:
						j=j+1
						EnergyembedingMatrix.append(my_line.rstrip().split(' ')[1:])
				k=k+1
		
	
	'''
	for indexval in entitity_list:
		#print indexval
		line_index = int(indexval)
		with open('Technology_file.txt_latest.emd_sorted') as f:
			c = count()
			while next(c) <= line_index-1:
				my_line =next(f)
			my_line=next(f)
	    	embedingMatrix.append(my_line.rstrip().split(' ')[1:])
	'''
	floatEnergymatrix=[]
	for row in EnergyembedingMatrix:
		floatrow=[]
		for val in row:
			floatrow.append(float(val))
		floatEnergymatrix.append(floatrow)
		
	floatEnergymatrix = np.array(floatEnergymatrix)
	import scipy.spatial as sp
  	score =0
  	count_var=0
	for i in xrange(0,10):
		EnergynprowfloatMatrix=[]
		EnergynprowfloatMatrix.append(np.array(Energyfloatmatrix[i]))
		EnergynprowfloatMatrix.append(np.array(Energyfloatmatrix[i]))
		if len(floatEnergymatrix)<2:
			for x in xrange(0,10):
				score_list.append(0.001)
			break
	
		scorematrix = 1 - sp.distance.cdist(floatEnergymatrix,EnergynprowfloatMatrix, 'cosine')  
  		for row in scorematrix:
  			for val in row:
	  			score = score+val
	  	 		count_var=count_var+1
  		#print str(score/count_var)#score for energy
  		score_list.append(score/count_var )
  	techscore=0
  	bizscore=0
  	energyscore=0
  	for x in xrange(0,10):
  		techscore=techscore+score_list[x]
	for x in xrange(10,20):
  		bizscore=bizscore+score_list[x]
  	for x in xrange(20,30):
  		energyscore=energyscore+score_list[x]


	'''	
	floatmatrix = np.array(floatmatrix)
	print floatmatrix
	print "*******DONE*******"
	'''


	print 'tex 1 '+text1
	print 'header '+ header
	#print score_list
	print 'tech score ' +str(techscore)
	print 'biz score '+ str(bizscore)
	print 'energy score '+str(energyscore)
	ent_final_list=[]
	flagindex="Energy"
	
	if techscore<3 and bizscore<3 and energyscore<3:
		flagindex ="Other Category"	
	else:
		techscore= Techscore*math.log(techscore)
		energyscore=  Energyscore*math.log(energyscore)
		bizscore= BusinensScore*math.log(bizscore)
		if techscore>bizscore and techscore>energyscore:
			flagindex = "Technology"
			print "Technology"
			
		elif bizscore>techscore and bizscore>energyscore:
			flagindex ="Business"
			print "Business"
		else:
			flagindex ="Energy"
			print "Energy"
			
	
	if len(TechList)>6:
		TechList=TechList[0:6]
	#print TechList
	#score_list=[-0.2,2 ,0.12,0.92]
	#print alexa_score
	return text1, header, score_list, 1/(1+math.log(int(alexa_score))), flagindex, TechList 
 

parse("https://stackoverflow.com/company/about")