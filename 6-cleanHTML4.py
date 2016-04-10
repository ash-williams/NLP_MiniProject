from pymongo import MongoClient
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer
import string

#Connect to mongo
client = MongoClient('mongodb://localhost/27017')
db = client['uc-proto']
articles = db.articles

count = 0

for article in articles.find():
	body = article['body']
	id = article['_id']
	
	try:

		text = article['article_text']
		
		for c in string.punctuation:
			#try:
			text = text.replace(c,"")
			#except:
			#	pass
		
		#print(text.encode())
		
		articles.update({"_id": id }, {"$set": {
			"article_no_punctuation": text,
		}})	
		
		count = count + 1
	
	except:
		print("Error")

print(count)
	
