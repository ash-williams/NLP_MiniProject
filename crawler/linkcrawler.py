import urllib3
import sys
from bs4 import BeautifulSoup

from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

# Seed page
seed = config['seed']

toCrawl = []
crawled = []
notBase = []

# Declare the collections
links = db.links
pages = db.pages

# Base url
base_url = config['base_url']

# Function to get all links from a page
def getAllLinks(url):
    try:
		http_pool = urllib3.connection_from_url(url)
		r = http_pool.urlopen('GET',url)
		html = r.data.decode('utf-8')
		
		soup = BeautifulSoup(html, "html5lib")
		
		for link in soup.find_all('a'):
			if link.has_attr('href'):
				toCrawl.append(link['href'])
    except:
        print("Unexpected error:", sys.exc_info()[0])

#Crawl the site
def crawlSite():
    links.drop()
    toCrawl.append(seed)

    while len(toCrawl) != 0:
    	link = toCrawl.pop()
    	
    	if link.startswith('http') and not link.startswith(base_url):
    		#print(link)
    		notBase.append(link)
    	else:	
    		if not link.startswith(base_url):
    			if link.startswith('/'):
    				link = base_url + link
    			else:
    				link = base_url + "/" + link
    		
    		if link not in crawled:
    			if link.endswith('.html') or link.endswith('/'):
    				#print(link)
    				getAllLinks(link)
    				crawled.append(link)
    				json_link = {
    					"url": link
    				}
    				links.insert_one(json_link)
    
    #Return number of links crawled
    return len(crawled)

#Get the content for each link  
def getcontent():
    pages.drop()
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
    		print("Unexpected error:", sys.exc_info()[0])
    
    #return number of pages retrieved
    return pages.count()