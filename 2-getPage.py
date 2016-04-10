from pymongo import MongoClient
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer
#


#Connect to mongo
client = MongoClient('mongodb://localhost/27017')
db = client['uc-proto']
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

