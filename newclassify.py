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
from searchengine.settings import B
from searchengine.settings import E

#from newclassify import classifier
import math


'''
T = ahocorasick.Automaton()
techembedingMatrix=[]

stop_words = set(stopwords.words('english'))


with open('sorted_Tech.txt') as file:
    for line in file:
        #idx=idx+1
        #if idx==50:
        #    break
        sen = line.split('\t')[1].rstrip().replace('_',' ')
        tokens=filter(lambda w: not w in stop_words,sen.split())
        valstr=""
        if(len(tokens)==1):
            T.add_word(tokens[0].lower(), (line.split('\t')[0],tokens[0].lower()))
        else:
            for x in range(0,len(tokens)):
                if x== len(tokens)-1:
                    valstr = valstr+tokens[x]
                else:
                    valstr = valstr+tokens[x]+" "
            T.add_word(valstr.lower(), (line.split('\t')[0],valstr.lower()))

'''

techembedingMatrix=[]

def classifier(data,text1, T,writeflag,docname):
	words=word_tokenize(data)


             #print(words)

        fin_list1 = []
        for word in words:
        	if wordnet.synsets(word):
        		fin_list1.append(word)
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
	#print data
        tech_count=0
        biz_count=0
        enrrgy_count=-1
        try:
		bigrams2 = ngrams(data, 4)
        	#print "fourgrams"
		#print bigrams2
        	for grams in bigrams2:
			#print grams
        		if T.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")!="not_exsist":
        			#print T.get(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3],"not_exsist")
                        	TechList.append(grams[0]+' '+grams[1]+' '+grams[2]+' '+grams[3])
                       		tech_count=tech_count+1

        	bigrams2 = ngrams(data, 3)
        	#print "trigrams"
        	for grams in bigrams2:
        		if T.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")!="not_exsist":
        			#print T.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")
                        	TechList.append(grams[0]+' '+grams[1]+' '+grams[2])
                        	tech_count=tech_count+1
                        	Techentitity_list.append(T.get(grams[0]+' '+grams[1]+' '+grams[2],"not_exsist")[0])
                bigrams2 = ngrams(data, 2)
       		print "bigrams"
        	bigrams2 = ngrams(data,2)
        	for grams in bigrams2:
        		if T.get(grams[0]+' '+grams[1],"not_exsist")!="not_exsist":
        	        	#print T.get(grams[0]+' '+grams[1],"not_exsist")
                        	TechList.append(grams[0]+' '+grams[1])
                        	tech_count=tech_count+1
                        	Techentitity_list.append(T.get(grams[0]+' '+grams[1],"not_exsist")[0])

        	bigrams2 = ngrams(data, 1)
        	#print "unigrams"
        	for grams in bigrams2:
			#print grams
        		if  T.get(grams[0],"not_exsist")!="not_exsist":
        			TechList.append(grams[0])
                	        tech_count=tech_count+1
                       		#print T.get(grams[0],"not_exsist")
                        	Techentitity_list.append(T.get(grams[0],"not_exsist")[0])
        	#print Techentitity_list
       		TechList=list(set(TechList))
  	        while 'n' in Energyentitity_list: Energyentitity_list.remove('n')
        	#Energyentitity_list.remove(u'n')
 
	except Exception as e:
		print(e)
        def MakeInt(elem):
                return int(elem)
       	def MakeInt2(elem):
                return int(elem[0])
		#def MakeInt(elem):
               

	Techentitity_list.sort(key = MakeInt)

        j=0
        k=0

        score_list=[]
        #print int(entitity_list[len(entitity_list)-1])+1
        #print "sorted"
        #print "entity list"
        techmatrixlist1=[]
        intkvar=0
        entitity_list = Techentitity_list
        #print entitity_list
       	if len(entitity_list)<=5:
		return 0.000	
	with open('likedocfiles/'+docname+'.txt') as f:
            for line in f:
                    techmatrixlist1.append(line.rstrip().split(' ')[1:])
			
        techfloatmatrix1=[]
        for row in techmatrixlist1:
            floatrow=[]
            for val in row:
                    floatrow.append(float(val))
	    if len(floatrow)>0:
            	techfloatmatrix1.append(floatrow)
        techfloatmatrix1 = np.array(techfloatmatrix1)
        #print techfloatmatrix1
	
        k=0
        j=0
	linecount=0
	if writeflag:
		with open('likedocfiles/'+docname+'.txt') as f:
			for  line in f:
				linecount=linecount+1
			if linecount>100:
				likefile = open('likedocfiles/'+docname+'.txt','w')
			else:
				likefile = open('likedocfiles/'+docname+'.txt','a')
	
        with open('Technology_file.txt_latest.emd_sorted') as f:
            if len(entitity_list)>0:
                    while k<=int(entitity_list[len(entitity_list)-1])+1 and j<len(entitity_list)-1:

                            my_line= next(f)
                            #print ki
                            if k==int(entitity_list[j]):
                                    #print "got T "+entitity_list[j]

                                    while k==int(entitity_list[j])and j<len(entitity_list)-1:
                                            j=j+1
					    if writeflag:		    
                                            	likefile.write(my_line)
					    
                                            techembedingMatrix.append(my_line.rstrip().split(' ')[1:])
                            k=k+1
	if writeflag:
		return  'done writing'
        
	floattechmatrix=[]
	
        for row in techembedingMatrix:
            floatrow=[]
            for val in row:
                    #print val
                    floatrow.append(float(val))
            floattechmatrix.append(floatrow)

        floattechmatrix = np.array(floattechmatrix)
	#scipy.spatial.distance.euclidean


        import scipy.spatial as sp
        score =0
        count_var=0
        #print floattechmatrix
        print
        #print techfloatmatrix1
        scorematrix = 1 - sp.distance.cdist( floattechmatrix,techfloatmatrix1, "cosine")
        print 'sscore'
        #print scorematrix
        for row in scorematrix:
                for val in row:
                        score = score+val
                        count_var=count_var+1
        print score/count_var
	
	return score/count_var
	
