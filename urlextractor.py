#scrape(n=30, local='category',sub_local=subcategory)
from script2 import scrape
import time
import json
urls = []
finalurls={}
with open('urls.json', 'r') as f:
    datastore = json.load(f)
for key in datastore["catsubcat"]:
    catsubcat={}
    sublist=[]
    for val in key["Subcategories"]:
        try:
            subcat={}
            print key['Category'], val
            subcategory='Computers/'+key['Category'].replace(' ','_')+'/'+val.replace(' ','_')
            print subcategory
            ulist1 =scrape(n=30, local='category',sub_local=subcategory)
            subcategory='Business/'+key['Category'].replace(' ','_')+'/'+val.replace(' ','_')
            print subcategory
            ulist2 =scrape(n=30, local='category',sub_local=subcategory)
            subcategory='Science/'+key['Category'].replace(' ','_')+'/'+val.replace(' ','_')
            print subcategory
            ulist3 =scrape(n=30, local='category',sub_local=subcategory)
            subcat.update({'Subcategory':val})
            if len(ulist1)!=0:
                subcat.update({'urls':ulist1})
            if len(ulist2)!=0:
                subcat.update({'urls':ulist2})
            if len(ulist3)!=0:
                subcat.update({'urls':ulist3})
            sublist.append(subcat)
            print sublist
            time.sleep(5)
        except Exception as e1:
            print str(e1)
            
        
    catsubcat.update({'Category':key['Category']})
    catsubcat.update({'Subcategories':sublist})
    urls.append(catsubcat)
    
finalurls.update({'catsubcat':urls})
with open("hidakiri.json",'w') as f:
    f.write(json.dumps(finalurls))
print catsubcat
