import json
import os
import sys
from pymongo import MongoClient
import urllib3
from bs4 import BeautifulSoup, SoupStrainer
import string

# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient("mongodb://" + os.environ['IP'] + "/") #for cloud nine, use MongoClient(config['db_url']) for config
db = client[config['db_client']]

articles = db.articles

count = 0

for article in articles.find():
	body = article['body']
	id = article['_id']
	
	try:

		text = article['article_no_punctuation']
		
		text = text.lower()
		
		#print(text.encode())
		
		articles.update({"_id": id }, {"$set": {
			"article_no_punctuation_and_lower": text,
		}})	
		
		count = count + 1
	
	except:
		print("Error")

print(count)
	
