<<<<<<< HEAD
import json
from pymongo import MongoClient
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer

# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient(config['db_url'])
db = client[config['db_client']]

pages = db.pages

for page in pages.find():
	html = page['html']
	id = page['_id']
	
	#try:
	soup = BeautifulSoup(html, "html.parser")
	
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
	
=======
import json
from pymongo import MongoClient
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer

# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient(config['db_url'])
db = client[config['db_client']]

pages = db.pages

for page in pages.find():
	html = page['html']
	id = page['_id']
	
	#try:
	soup = BeautifulSoup(html, "html.parser")
	
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
	
>>>>>>> d60802d8e614c209359ffbcff608940a2dce4ea3
