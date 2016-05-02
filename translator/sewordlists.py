from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

#Search Engine Friendly Word List Translator

#Translates [url, [words]] into [word, [urls]] 
#Translate takes in source and destination collections
def translate(source, destination):
    named_ents = db[source]
    word_list = db[destination]
    
    count = 0
    word_list.drop()
    
    word_urls = []
    
    for ne in named_ents.find():
    	url = ne['url']
    	words = ne['words']
    	
    	for word in words:
    	    word = word.lower()
            doc = word_list.find_one({"word": word})
            if doc:
                doc_urls = doc['urls']
                if url not in doc_urls:
                    new_urls = doc_urls + [url]
                
                    word_list.update({"word": word }, {"$set": {
                    "urls": new_urls,
                    }})	
                
            else:
                json = {
                    "word": word,
                    "urls": [url]
                }
                #
                word_list.insert_one(json)
    	
    	count = count + 1
    	
    #return number of words found
    return count
