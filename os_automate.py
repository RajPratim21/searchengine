import subprocess
import os
from pymongo import MongoClient
client = MongoClient()
db = client.test
cursor = db.configlist.find()
for document in cursor:
	print(document)
	'''
	for key in document['choice']:
		print key
		#os.system("python alexacrawl.py " + 'Computers/'+ key.replace(' ','_'))
		#os.system("python alexacrawl.py " + 'Business/'+ key.replace(' ','_'))
		#os.system("python alexacrawl.py " + 'Science/'+ key.replace(' ','_'))

		for value  in document['choice'][key]:
			print  value
			os.system("python alexacrawl.py " + 'Computers/'+ key.replace(' ','_') +'/'+value.replace(' ','_'))
			os.system("python alexacrawl.py " + 'Business/'+ key.replace(' ','_')+'/'+value.replace(' ','_'))
			os.system("python alexacrawl.py " + 'Science/'+ key.replace(' ','_')+'/'+value.replace(' ','_'))

	'''
