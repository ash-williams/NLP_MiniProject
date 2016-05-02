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

# Declare links collection
links = db.links

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