import os
import time
import json
import subprocess

counter =0
with open('caturl_list.json', 'r') as f:
    datastore = json.load(f)
for key in datastore["catsubcat"]:
	#if key['Category']=='Algorithms':
	#	continue
	print '$$$$$$$$$$$',key['Category']
	for val in key['Subcategories']:
		print '###########', val['Subcategory']#, val['urls']
		try:		
			for url in val['urls']:
				subprocess.call(['nohup','python', 'alexacrawl.py', url, 'doc'+key['Category'].lower().replace(' ','_')+val['Subcategory'].lower().replace(' ','_'), '&'])
				#subprocess.call(['rm', 'nohup.out']) 
   				print '&&&&&&&&&&&&&&&&&&&&&&'
				time.sleep(1)
		except:
			print 'excepting'	
