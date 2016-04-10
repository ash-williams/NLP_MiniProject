from pymongo import MongoClient
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer

#Connect to mongo
client = MongoClient('mongodb://localhost/27017')
db = client['uc-proto']
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
	
