import os
import time
import json
import subprocess

counter =0
with open('cat_url_list.json', 'r') as f:
    datastore = json.load(f)
for key in datastore["catsubcat"]:
        print '$$$$$$$$$$$',key['Category']
	if counter<5:
		counter=counter+1
		continue
	counter = counter+1
        for val in key['Subcategories']:
                #print '###########', val['Category']#, val['urls']
                try:	
			
			scount=0
                        for url in val['urls']:
				if scount==5:
					break
				scount=scount+1
                                subprocess.call(['nohup', 'python', 'alexacrawl.py', url, 'doc'+key['Category'].lower().replace(' ','_'), '&'])
                                #subprocess.call(['rm', 'nohup.out']) 
                                print '&&&&&&&&&&&&&&&&&&&&&&'
                                time.sleep(1)
                except:
                        print 'excepting'
                                           
