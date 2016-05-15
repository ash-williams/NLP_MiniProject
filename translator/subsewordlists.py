from settings import config, db

# Variables
config = config.getConfig()
db = db.getDB()

#Search Engine Friendly Word List Translator

#Translates [url, [words]] into [word, [urls]] 
#Translate takes in source and destination collections
def translate(source, destination, **kwargs):
    named_ents = db[source]
    word_list = db[destination]
    
    #Can be text/paragraph/sentence
    extract_type = kwargs.get('extract_type', None)
    
    count = 0
    word_list.drop()
    
    word_urls = []
    
    for ne in named_ents.find():
    	url = ne['url']
    	words = ne['words']
    	
    	if extract_type == "paragraph":
    	    pnum = ne['paragraph_number']
    	
    	if extract_type == "sentence":
    	    pnum = ne['paragraph_number']
    	    snum = ne['sentence_number']
    	
    	for word in words:
    	    word = word.lower()
            doc = word_list.find_one({"word": word})
            if doc:
                doc_urls = doc['urls']
                if url not in doc_urls:
                    if extract_type == "paragraph":
                        item = [url, pnum]
                    elif extract_type == "sentence":
                        item = [url, pnum, snum]
                    else:
                        item = [url]
                    
                    new_urls = doc_urls + [item]
                
                    word_list.update({"word": word }, {"$set": {
                        "urls": new_urls
                    }})	
                
            else:
                if extract_type == "paragraph":
                    item = [url, pnum]
                elif extract_type == "sentence":
                    item = [url, pnum, snum]
                else:
                    item = [url]
                
                json = {
                    "word": word,
                    "urls": [item]
                }
                #
                word_list.insert_one(json)
    	
    	count = count + 1
    	
    #return number of words found
    return count
