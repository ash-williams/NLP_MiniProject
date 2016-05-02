import string, re, nltk, unicodedata

from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

named_entities = []

# Declare the collections
articles = db.articles
indicators = db.indicators
analysis = db.analysis
named_ents = db.noun_named_entities

def extract():
    count = 0
    named_ents.drop()
    
    for article in articles.find():
        text = article['article_text']
        url = article['url']
        
        #Add space after capitals unless what follows is multiple capitals e.g. .NET
        #This is a bug that needs fixing on the article extraction, currently new paragraphs in the HTML are
        #bunched together with no "space.Like" <-- here
        text = re.sub(r'\.([a-zA-Z"])([a-z ])', r'. \1\2', text)
        
        words = nltk.word_tokenize(text)
        tagged = nltk.pos_tag(words)
        
        words = []
        for item in tagged:
            if item[1] in ['NN', 'NNS', 'NNP', 'NNPS']:
                word = item[0]
                
                word = word.lower()
                word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore')
                
                punctuation_exceptions = ['/', '-']
                for c in string.punctuation:
                    if c in punctuation_exceptions:
                        word = word.replace(c, " ")
                    else:
                        word = word.replace(c,"")
                
                split = word.split(" ")
                for word in split:
                    if word != '':
                        words += [word]
               
        
        ne_url = [url] + [words]
        named_entities += [ne_url]
    
    for item in named_entities:
    	url = item[0]
    	words = item[1]
    	
    	for word in words:
    		doc = named_ents.find_one({"url": url})
    		if doc:
    			doc_words = doc['words']
    			if word in doc_words:
    				print("URL and word already exists")
    			else:
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
        count += 1
    #return number of articles extracted
    return count
    	
