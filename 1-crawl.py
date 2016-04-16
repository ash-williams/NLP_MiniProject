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

# Function to get all links from a page
def getAllLinks(url):
	try:
		response = urllib.request.urlopen(url)
		html = response.read()
		
		for link in BeautifulSoup(html, parse_only=SoupStrainer('a')):
			if link.has_attr('href'):
				toCrawl.append(link['href'])
	except:
		print("error")

# Variables
# Seed page
seed = config['seed']

toCrawl = []
crawled = []
notJoel = []

# Declare links collection
links = db.links

# Base url
base_url = config['base_url']


toCrawl.append(seed)

while len(toCrawl) != 0:

	link = toCrawl.pop()
	
	if link.startswith('http') and not link.startswith(base_url):
		#print(link)
		notJoel.append(link)
	else:	
		if not link.startswith(base_url):
			if link.startswith('/'):
				link = base_url + link
			else:
				link = base_url + "/" + link
		
		if link not in crawled:
			if link.endswith('.html') or link.endswith('/'):
				print(link)
				getAllLinks(link)
				crawled.append(link)
				json_link = {
					"url": link
				}
				links.insert_one(json_link)
				

print("To Crawl: " + (str)(len(toCrawl)))
print("Crawled: " + (str)(len(crawled)))
print("Not Joel: " + (str)(len(notJoel)))




	
