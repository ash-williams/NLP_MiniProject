import json
import os
from pymongo import MongoClient
import urllib3
from bs4 import BeautifulSoup, SoupStrainer

# Get Config file
with open("config.json") as config_file:
    config = json.load(config_file)

# Connect to mongo
client = MongoClient("mongodb://" + os.environ['IP'] + "/") #for cloud nine, use MongoClient(config['db_url']) for config
db = client[config['db_client']]


links = db.links
pages = db.pages

for link in links.find():
	url = link['url']
	id = link['_id']
	
	try:
		http_pool = urllib3.connection_from_url(url)
		r = http_pool.urlopen('GET',url)
		html = r.data.decode('utf-8')
		
		#print(html)
		
		json_html = {
			"url_link": id,
			"url": url,
			"html": html
		}
		pages.insert_one(json_html)
	except:
		print("error")

