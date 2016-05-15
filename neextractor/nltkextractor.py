import nltk

from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

named_entities = []

# Declare the collections
articles = db.articles
indicators = db.indicators
analysis = db.analysis
named_ents = db.named_entities

def getNodes(parent, url):
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == 'NE':
             	leaves = node.leaves()
             	ne = []
             	for leaf in leaves:
             		#print(leaf[0])
             		ne += [leaf[0]]
             	ne_url = [url] + [ne]
             	#print(ne_url)
             	
             	global named_entities
                named_entities += [ne_url]

            getNodes(node, url)

def extract():
    count = 0
    named_ents.drop()
    
    for article in articles.find(no_cursor_timeout=True):
    	text = article['article_text']
    	url = article['url']
    	
    	
    	words = nltk.word_tokenize(text)
    	tagged = nltk.pos_tag(words)
    	chunked = nltk.ne_chunk(tagged, binary=True)
    
    	getNodes(chunked, url)
    	print count
    	count = count + 1
    
    insert_count = 0	
    for item in named_entities:
    	url = item[0]
    	words = item[1]
    	
    	for word in words:
    		doc = named_ents.find_one({"url": url})
    		if doc:
    			doc_words = doc['words']
    			if word not in doc_words:
    				new_words = doc_words + [word]
    				
    				named_ents.update({"url": url }, {"$set": {
    				 	"words": new_words,
    				}})	
    		
    		else:
    			json = {
    						"url": url,
    						"words": [word]
    					}
    			named_ents.insert_one(json)
        print insert_count
        insert_count += 1
        
    
    #return number of articles extracted
    return count
    
	