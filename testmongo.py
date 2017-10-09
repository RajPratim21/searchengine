from pymongo import MongoClient
client = MongoClient()    
db = client.test
cursor = db.config.find()
for document in cursor:
	print(document)
	print 'dxsxsxs', document['choice']
