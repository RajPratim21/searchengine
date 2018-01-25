import os
import time
import json
import subprocess

def geturllist(Category, Subcategory):	
	counter =0
	with open('urllist.json', 'r') as f:
	    datastore = json.load(f)
	for key in datastore["catsubcat"]:
	        if key['Category']==Category:
	        	print '$$$$$$$$$$$',key['Category']
	        	for val in key['Subcategories']:
				if val['Subcategory']==Subcategory:		
	        	        	print '###########', val['Subcategory']
	        	                for url in val['urls']:
	        	                       	print url


geturllist("Algorithms", "Compression")
