from pymongo import MongoClient
import urllib.request
from bs4 import BeautifulSoup, SoupStrainer



def getAllLinks(url):
	try:
		response = urllib.request.urlopen(url)
		html = response.read()
		
		for link in BeautifulSoup(html, parse_only=SoupStrainer('a')):
			if link.has_attr('href'):
				toCrawl.append(link['href'])
	except:
		print("error")

#get page from html
seed = "http://www.joelonsoftware.com/backIssues.html"

toCrawl = []
crawled = []
notJoel = []

#Write to mongo
client = MongoClient('mongodb://localhost/27017')
db = client['uc-proto']
links = db.links


toCrawl.append(seed)

while len(toCrawl) != 0:

	#print("To Crawl: " + (str)(len(toCrawl)))
	#print("Crawled: " + (str)(len(crawled)))
	#print("Not Joel: " + (str)(len(notJoel)))

	link = toCrawl.pop()
	
	if link.startswith('http') and not link.startswith('http://www.joelonsoftware.com'):
		#print(link)
		notJoel.append(link)
	else:	
		if not link.startswith('http://www.joelonsoftware.com'):
			if link.startswith('/'):
				link = "http://www.joelonsoftware.com" + link
			else:
				link = "http://www.joelonsoftware.com/" + link
		
		if link not in crawled:
			#if link.startswith('http://www.joelonsoftware.com'):
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




	
