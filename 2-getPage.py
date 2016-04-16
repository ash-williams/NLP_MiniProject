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


links = db.links
pages = db.pages

for link in links.find():
	url = link['url']
	id = link['_id']
	
	try:
		response = urllib.request.urlopen(url)
		html = response.read()
		
		#print(html)
		
		json_html = {
			"url_link": id,
			"url": url,
			"html": html
		}
		pages.insert_one(json_html)
	except:
		print("error")

