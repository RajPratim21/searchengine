import os
import time
import json
import subprocess
with open('caturl_list.json', 'r') as f:
    datastore = json.load(f)
counter=0
for key in datastore["catsubcat"]:
        print '$$$$$$$$$$$',key['Category']
        for val in key['Subcategories']:
                print '###########', val['Subcategory'], val['urls']
                for url in val['urls']:
			subprocess.call(['nohup', 'python', 'crawltest.py', url, 'doc'+key['Category'].lower().replace(' ','_')+val['Subcategory'].lower().replace(' ','_'),key['Category']+' '+val['Subcategory'], '&'])
                        print '&&&&&&&&&&&&&&&&&&&&&&'
                        time.sleep(5)

