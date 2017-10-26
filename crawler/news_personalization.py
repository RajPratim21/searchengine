import json
from pprint import pprint
keyword=["Business", "Technology", "Climate","Agriculture", "Sports", "Energy","Entertainment", "Electronics", "finance", "Auditing", "Banking", "Insurance", "Magazines", "Real Estate", "Investment", "Manufacturing", "Security", "Small Business", "Marketing",
   "Advertising", "Taxation","Cricket", "Football", "Golf", "Gymnastics", "Hockey", "Horse Racing", "Basketball", "Billiards", "Running", "Soccer", "Tennis",
   "Water Sports", "Software", "Web Design", "bots", "Graphics", "Internet", "Health", "Machine learning", "Engineering",
"Internet Things", "Multimedia", "Telecommunications", "Biotechnology","Solar Energy", "Electric power", "Fuels","Geothermal Energy" , "Oil","Smart Grid","Mining","Coal","Natural Gas", "Renewable Energy", "Wind Energy","hydroelectricity","Chemistry", "Electronics", "Mechanics", "Medicine", "Open Source"]

from pymongo import MongoClient
client = MongoClient()    
db = client.test


keyfiles=[]
finalkeyfiles=[]
'''

for i in range(len(keyword)):
    keyfiles.append([])
    finalkeyfiles.append({})
'''
cursor = db.config.find()
for document in cursor:
    keyfiles.append([])
    finalkeyfiles.append({})
AlreadyList=[]
with open('newsjson.txt') as data_file:    
    data = json.load(data_file)
    for vals in data['articles']:
        #print vals
	cursor = db.config.find() 
	i=0       
	for document in cursor:
            #print 'cdscd
	    try:
                if  vals['Category'] in document['choice']:
                    keyfiles[i].append(vals)
		    AlreadyList.append(vals['title'])
                    print 'scdd'
		for chic in document['choice'].split(','):
			if len(chic)>4  and (chic.lower() in vals['title'].lower() or chic.lower() in vals['description'].lower()) :
				keyfiles[i].append(vals)
				print chic
				AlreadyList.append(vals['title'])
            except Exception as e:
                print str(e)
                pass
	    i=i+1

with open('newsjson.txt') as data_file:
    data = json.load(data_file)
    for vals in data['articles']:
        #print vals
        cursor = db.config.find()
	i=0
        for document in cursor:
            #print 'cdscdscds', document
            try:
                if  vals['Category'] not in document['choice'] and  vals['title'] not in AlreadyList:
                    keyfiles[i].append(vals)
                    print 'scdd', i
		    i=i+1
            except Exception as e:
                print 'second',  str(e)
                pass
            #i=i+1

for val in keyfiles:
	print 
cursor = db.config.find()
i=0
for document in cursor:
    finalkeyfiles[i].update({'articles':keyfiles[i]})
    i=i+1
i=0
cursor = db.config.find()
for document in cursor:
    with open( document['user']+'.txt', 'w') as outfile:
        json.dump(finalkeyfiles[i], outfile)
	i=i+1
