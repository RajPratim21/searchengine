import networkx as nx
from nltk.corpus import stopwords
G=nx.DiGraph()
stop_words = set(stopwords.words('english'))

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
	G.add_edge(d1_string.lower(),d2_string.lower())

while True:
	print 'Enter'
	val = raw_input()
	if val in G:
		print 'exsist'
		iter =G.successors_iter(val)
		for neb in iter:
			print neb
	else: 
		print 'not'
