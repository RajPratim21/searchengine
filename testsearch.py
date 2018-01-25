
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

myquery ={
	         "query": 
			{
			   
					"multi_match": 
					        {
					          "query": 'steam engine history superman hero enrgy business power cad ',
					          "fields": [ "data", "header^2" ]
					        }  
				    
			    
			},
		"from" : 0, "size" : 100
	}
result = es.search(index="_all", body=myquery)
for rows in result['hits']['hits']:
	print rows['_score']
