import json
def list_return():
	with open('urllist.json') as data_file:    
    		data = json.load(data_file)
    		data = data['catsubcat']
    		ult_list = []
    		for i in data:
			for key1,value1 in i:
				for k in value1:
					for key2, value2 in k.iteritems():
						for b in value2:
							ult_list.append(key1 +" " +  key2 + " " +  b)
		return ulti_list

print list_return()
