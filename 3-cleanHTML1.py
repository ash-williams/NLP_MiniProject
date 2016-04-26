import json
import os
import sys
from pymongo import MongoClient
import urllib3
from bs4 import BeautifulSoup, SoupStrainer

# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient("mongodb://" + os.environ['IP'] + "/") #for cloud nine, use MongoClient(config['db_url']) for config
db = client[config['db_client']]

pages = db.pages

for page in pages.find():
	html = page['html']
	id = page['_id']
	
	#try:
	soup = BeautifulSoup(html)
	
	head = soup.find('head')
	body = soup.find('body')
	
	#print(head.encode())
	#print(body.encode())
	
	pages.update({"_id": id }, {"$set": {
		"head": head.encode(),
		"body": body.encode()
	}})
		
	#except:
	#	print("error")
	
