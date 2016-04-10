from pymongo import MongoClient
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer

#Connect to mongo
client = MongoClient('mongodb://localhost/27017')
db = client['uc-proto']
articles = db.articles

count = 0

for article in articles.find():
	body = article['body']
	id = article['_id']
	
	#try:
	soup = BeautifulSoup(body, "html.parser")
	
	from_pos = soup.find('div', {"class": "date"})
	to_pos = soup.find('br', {"clear":"all"})

	text = ""
	
	for tag in from_pos.next_siblings:
		if tag == to_pos:
			break
		else:
			try:
				text += tag.text
			except: 
				pass
			
	print("#")
	#print(from_pos)
	#print(to_pos)
	print(text.encode())
	print("#")
		
	articles.update({"_id": id }, {"$set": {
			"article_text": text,
		}})	
		
		
	count = count + 1
	
	#except:
	#	print("Error")

print(count)
	
